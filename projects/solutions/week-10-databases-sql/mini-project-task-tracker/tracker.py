#!/usr/bin/env python3
"""tracker.py -- a task tracker CLI whose storage is a real SQLite database.

Week 10 mini-project reference solution. Standard library only: sqlite3,
argparse, pathlib, sys, typing (plus datetime, used only to validate dates).

Commands:

    python tracker.py add TITLE [--due YYYY-MM-DD] [--priority N]
    python tracker.py list [--priority N] [--status open|done|all]
    python tracker.py done ID
    python tracker.py delete ID

The database file lives next to this script as tasks.db. Override it with the
TRACKER_DB environment variable if you want a throwaway copy:

    TRACKER_DB=scratch.db python tracker.py list

Every value that reaches SQL goes through a `?` placeholder. There is not one
f-string, `%`, `+` or `.format()` anywhere inside a SQL statement in this file.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from collections.abc import Iterator, Sequence
from contextlib import closing, contextmanager
from datetime import date
from pathlib import Path
from typing import Final

# --------------------------------------------------------------------------
# Configuration and schema
# --------------------------------------------------------------------------

DB_PATH: Final[Path] = Path(os.environ.get("TRACKER_DB", Path(__file__).with_name("tasks.db")))

# Every statement is IF NOT EXISTS, which is what makes init_db() idempotent:
# running the app for the hundredth time does exactly as much work as the
# second time, which is none.
SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    due_date  TEXT,                              -- ISO-8601 'YYYY-MM-DD' or NULL
    priority  INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    done      INTEGER NOT NULL DEFAULT 0         -- 0 = open, 1 = done
);

-- `list` filters on done and/or priority and always sorts by id. One index
-- over all three lets SQLite answer the filtered list from the index alone
-- once the table is big enough for that to matter.
CREATE INDEX IF NOT EXISTS idx_tasks_done_priority ON tasks(done, priority, id);
"""

# Column widths for the list output, kept in one place so the header, the
# rule and the rows can never drift apart.
ROW_FORMAT: Final[str] = "{id:>2}  {priority:>3}  {status:<6}  {due:<10}  {title}"
TITLE_RULE_WIDTH: Final[int] = 31


# --------------------------------------------------------------------------
# Database plumbing
# --------------------------------------------------------------------------


def connect(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    """Open a connection with the settings this app always wants.

    A db_path beginning with `file:` is treated as a SQLite URI, which is how
    the test suite asks for a shared in-memory database. Ordinary filenames
    are unaffected.
    """
    target = str(db_path)
    conn = sqlite3.connect(target, uri=target.startswith("file:"))
    conn.row_factory = sqlite3.Row          # read columns by name, not by index
    conn.execute("PRAGMA foreign_keys = ON")  # harmless here, habit-forming
    return conn


@contextmanager
def cursor(db_path: Path | str = DB_PATH) -> Iterator[sqlite3.Cursor]:
    """Yield a cursor inside one transaction, then commit, then close.

    `with conn:` is the transaction: leaving the block normally commits, and
    leaving it via an exception rolls back. `closing(...)` is the file handle:
    it calls conn.close() whichever way we leave. You need both -- `with
    sqlite3.connect(...)` alone commits but never closes.
    """
    with closing(connect(db_path)) as conn:
        with conn:
            yield conn.cursor()


def init_db(db_path: Path | str = DB_PATH) -> None:
    """Create the schema if it is missing. Safe to call on every run."""
    with closing(connect(db_path)) as conn:
        with conn:
            conn.executescript(SCHEMA)


# --------------------------------------------------------------------------
# Operations -- one function per command, each one parameterized
# --------------------------------------------------------------------------


def add_task(title: str, due: str | None, priority: int,
             db_path: Path | str = DB_PATH) -> int:
    """Insert one task and return its new id."""
    with cursor(db_path) as cur:
        cur.execute(
            "INSERT INTO tasks (title, due_date, priority) VALUES (?, ?, ?)",
            (title, due, priority),
        )
        new_id = cur.lastrowid
    assert new_id is not None      # INSERT always sets lastrowid
    return new_id


def list_tasks(
    priority: int | None = None,
    status: str = "all",
    db_path: Path | str = DB_PATH,
) -> list[sqlite3.Row]:
    """Return tasks matching the filters, in id order.

    Id order is what the README's sample output shows, so that is what the
    default is. (The stretch version adds a --sort flag for priority and due.)

    The filters compose: the WHERE clause is assembled from a list of fixed
    SQL fragments, and every fragment that needs a value uses `?`. The only
    thing user input decides is *which* constant fragments get used -- it never
    becomes part of the query text.
    """
    clauses: list[str] = []
    params: list[object] = []

    if priority is not None:
        clauses.append("priority = ?")
        params.append(priority)

    if status == "open":
        clauses.append("done = ?")
        params.append(0)
    elif status == "done":
        clauses.append("done = ?")
        params.append(1)
    elif status != "all":
        raise ValueError(f"unknown status: {status!r}")

    query = "SELECT id, title, due_date, priority, done FROM tasks"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY id"

    with cursor(db_path) as cur:
        cur.execute(query, params)
        return cur.fetchall()


def mark_done(task_id: int, db_path: Path | str = DB_PATH) -> sqlite3.Row:
    """Set done = 1 for one task. Raises LookupError if the id is unknown."""
    with cursor(db_path) as cur:
        cur.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if row is None:
            raise LookupError(f"no task with id {task_id}")
        cur.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        return row


def delete_task(task_id: int, db_path: Path | str = DB_PATH) -> sqlite3.Row:
    """Delete one task. Raises LookupError if the id is unknown."""
    with cursor(db_path) as cur:
        cur.execute("SELECT id, title FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if row is None:
            raise LookupError(f"no task with id {task_id}")
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return row


# --------------------------------------------------------------------------
# Presentation
# --------------------------------------------------------------------------


def format_table(rows: Sequence[sqlite3.Row]) -> str:
    """Render task rows as the fixed-width table the spec asks for."""
    header = ROW_FORMAT.format(
        id="ID", priority="Pri", status="Status", due="Due", title="Title"
    )
    rule = ROW_FORMAT.format(
        id="--",
        priority="---",
        status="------",
        due="-" * 10,
        title="-" * TITLE_RULE_WIDTH,
    )
    lines = [header, rule]
    for row in rows:
        lines.append(
            ROW_FORMAT.format(
                id=row["id"],
                priority=row["priority"],
                status="done" if row["done"] else "open",
                due=row["due_date"] if row["due_date"] else "-",
                title=row["title"],
            )
        )
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Argument parsing and validation
# --------------------------------------------------------------------------


def priority_type(raw: str) -> int:
    """argparse type: an integer in 1..5."""
    try:
        value = int(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"priority must be a whole number, got {raw!r}")
    if not 1 <= value <= 5:
        raise argparse.ArgumentTypeError(f"priority must be between 1 and 5, got {value}")
    return value


def iso_date_type(raw: str) -> str:
    """argparse type: a string that really parses as an ISO-8601 date."""
    try:
        date.fromisoformat(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"due date must be ISO-8601 YYYY-MM-DD, got {raw!r}"
        )
    return raw


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker.py",
        description="A task tracker backed by SQLite.",
        epilog="Run 'tracker.py COMMAND --help' for help on one command.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    p_add = subparsers.add_parser("add", help="add a new task")
    p_add.add_argument("title", help="what needs doing")
    p_add.add_argument("--due", type=iso_date_type, default=None, metavar="YYYY-MM-DD",
                       help="optional due date")
    p_add.add_argument("--priority", type=priority_type, default=3, metavar="N",
                       help="1 (highest) to 5 (lowest); default 3")

    p_list = subparsers.add_parser("list", help="list tasks")
    p_list.add_argument("--priority", type=priority_type, default=None, metavar="N",
                        help="show only this priority")
    p_list.add_argument("--status", choices=("open", "done", "all"), default="all",
                        help="show only open, only done, or all (default: all)")

    p_done = subparsers.add_parser("done", help="mark a task done")
    p_done.add_argument("id", type=int, help="the task id")

    p_delete = subparsers.add_parser("delete", help="delete a task")
    p_delete.add_argument("id", type=int, help="the task id")

    return parser


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    init_db()

    if args.command == "add":
        new_id = add_task(args.title, args.due, args.priority)
        print(f"Added task {new_id}: {args.title}")
        return 0

    if args.command == "list":
        rows = list_tasks(priority=args.priority, status=args.status)
        if not rows:
            print("No tasks match those filters.")
            return 0
        print(format_table(rows))
        return 0

    if args.command == "done":
        try:
            row = mark_done(args.id)
        except LookupError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        if row["done"]:
            print(f"Task {row['id']} was already done: {row['title']}")
        else:
            print(f"Nice. Task {row['id']} is done: {row['title']}")
        return 0

    if args.command == "delete":
        try:
            row = delete_task(args.id)
        except LookupError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"Deleted task {row['id']}: {row['title']}")
        return 0

    parser.print_help()          # unreachable while every subcommand is handled
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
