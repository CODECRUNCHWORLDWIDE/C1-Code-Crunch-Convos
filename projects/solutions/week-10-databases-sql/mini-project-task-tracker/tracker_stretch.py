#!/usr/bin/env python3
"""tracker_stretch.py -- tracker.py plus all five mini-project stretch goals.

This is a separate script rather than a patch to tracker.py because it uses a
different schema (it adds two tables) and therefore a different database file,
`tasks-stretch.db`. Read tracker.py first; then read this for the deltas.

What is added, in the order the README lists them:

1. `undone ID`      -- flip a task back to open.
2. `list --sort {priority,due,id}` -- the identifier-whitelist pattern, because
                       ORDER BY column names can never be parameterized.
3. Colour by priority (1 red, 2 yellow, 3 default, 4-5 dim), with
   `--color {auto,always,never}`; auto means "only when stdout is a terminal".
4. A `tags` table, a `task_tags` junction table, `add --tag NAME` (repeatable)
   and `list --tag NAME`.
5. (The test suite stretch goal is test_tracker.py, next to this file.)

Still standard library only, and still zero values interpolated into SQL.
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

DB_PATH: Final[Path] = Path(
    os.environ.get("TRACKER_DB", Path(__file__).with_name("tasks-stretch.db"))
)

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    due_date  TEXT,
    priority  INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    done      INTEGER NOT NULL DEFAULT 0
);

-- Tag names are unique case-insensitively, so "Work" and "work" are one tag.
CREATE TABLE IF NOT EXISTS tags (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);

-- The junction table. Its primary key is the pair, which both enforces "a tag
-- can only be on a task once" and gives the lookup index for free.
CREATE TABLE IF NOT EXISTS task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags(id)  ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- The PK above indexes (task_id, tag_id). The reverse direction -- "which
-- tasks carry this tag?" -- needs its own index.
CREATE INDEX IF NOT EXISTS idx_task_tags_tag ON task_tags(tag_id, task_id);
CREATE INDEX IF NOT EXISTS idx_tasks_done_priority ON tasks(done, priority, id);
"""

ROW_FORMAT: Final[str] = "{id:>2}  {priority:>3}  {status:<6}  {due:<10}  {title:<31}  {tags}"

# ORDER BY takes an identifier, and identifiers cannot be bound with `?`.
# The safe pattern is a whitelist: the user picks a *key*, and the SQL comes
# from this dictionary of constants. User text never reaches the query.
SORT_CLAUSES: Final[dict[str, str]] = {
    "id": "ORDER BY t.id",
    "priority": "ORDER BY t.priority, t.id",
    # NULL due dates sort last: `due_date IS NULL` is 0 for real dates, 1 for
    # NULLs, so ordering by it first pushes the undated tasks to the bottom.
    "due": "ORDER BY t.due_date IS NULL, t.due_date, t.id",
}

ANSI: Final[dict[int, str]] = {1: "\033[31m", 2: "\033[33m", 3: "", 4: "\033[2m", 5: "\033[2m"}
RESET: Final[str] = "\033[0m"


# --------------------------------------------------------------------------
# Database plumbing (identical to tracker.py)
# --------------------------------------------------------------------------


def connect(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    target = str(db_path)
    conn = sqlite3.connect(target, uri=target.startswith("file:"))
    conn.row_factory = sqlite3.Row
    # Now that there are foreign keys, this PRAGMA stops being decorative:
    # without it ON DELETE CASCADE on task_tags does nothing.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def cursor(db_path: Path | str = DB_PATH) -> Iterator[sqlite3.Cursor]:
    with closing(connect(db_path)) as conn:
        with conn:
            yield conn.cursor()


def init_db(db_path: Path | str = DB_PATH) -> None:
    with closing(connect(db_path)) as conn:
        with conn:
            conn.executescript(SCHEMA)


# --------------------------------------------------------------------------
# Operations
# --------------------------------------------------------------------------


def add_task(
    title: str,
    due: str | None,
    priority: int,
    tags: Sequence[str] = (),
    db_path: Path | str = DB_PATH,
) -> int:
    """Insert a task and its tags in one transaction.

    Inserting the task and linking its tags must be atomic: a task that exists
    with half its tags is worse than no task at all. Both happen inside the
    single `with cursor(...)` block, so an exception on the third tag rolls the
    task insert back too.
    """
    with cursor(db_path) as cur:
        cur.execute(
            "INSERT INTO tasks (title, due_date, priority) VALUES (?, ?, ?)",
            (title, due, priority),
        )
        task_id = cur.lastrowid
        assert task_id is not None
        for name in tags:
            # ON CONFLICT DO NOTHING makes "create the tag if new" idempotent
            # without a SELECT-then-INSERT race.
            cur.execute("INSERT INTO tags (name) VALUES (?) ON CONFLICT(name) DO NOTHING",
                        (name,))
            cur.execute("SELECT id FROM tags WHERE name = ?", (name,))
            tag_id = cur.fetchone()["id"]
            cur.execute(
                "INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?) "
                "ON CONFLICT DO NOTHING",
                (task_id, tag_id),
            )
        return task_id


def list_tasks(
    priority: int | None = None,
    status: str = "all",
    tag: str | None = None,
    sort: str = "id",
    db_path: Path | str = DB_PATH,
) -> list[sqlite3.Row]:
    """List tasks with their tags collapsed into one column."""
    clauses: list[str] = []
    params: list[object] = []

    if priority is not None:
        clauses.append("t.priority = ?")
        params.append(priority)
    if status == "open":
        clauses.append("t.done = ?")
        params.append(0)
    elif status == "done":
        clauses.append("t.done = ?")
        params.append(1)
    elif status != "all":
        raise ValueError(f"unknown status: {status!r}")
    if tag is not None:
        # EXISTS rather than a JOIN, so filtering by one tag cannot duplicate a
        # task row that also carries three other tags.
        clauses.append(
            "EXISTS (SELECT 1 FROM task_tags tt "
            "        JOIN tags g ON g.id = tt.tag_id "
            "        WHERE tt.task_id = t.id AND g.name = ?)"
        )
        params.append(tag)

    if sort not in SORT_CLAUSES:
        raise ValueError(f"unknown sort key: {sort!r}")

    query = (
        "SELECT t.id, t.title, t.due_date, t.priority, t.done, "
        "       COALESCE(GROUP_CONCAT(g.name, ','), '') AS tags "
        "FROM tasks AS t "
        "LEFT JOIN task_tags AS tt ON tt.task_id = t.id "
        "LEFT JOIN tags      AS g  ON g.id = tt.tag_id"
    )
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    # GROUP BY collapses the one-row-per-tag fan-out from the LEFT JOINs back
    # to one row per task.
    query += " GROUP BY t.id " + SORT_CLAUSES[sort]

    with cursor(db_path) as cur:
        cur.execute(query, params)
        return cur.fetchall()


def set_done(task_id: int, done: bool, db_path: Path | str = DB_PATH) -> sqlite3.Row:
    with cursor(db_path) as cur:
        cur.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if row is None:
            raise LookupError(f"no task with id {task_id}")
        cur.execute("UPDATE tasks SET done = ? WHERE id = ?", (1 if done else 0, task_id))
        return row


def delete_task(task_id: int, db_path: Path | str = DB_PATH) -> sqlite3.Row:
    with cursor(db_path) as cur:
        cur.execute("SELECT id, title FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if row is None:
            raise LookupError(f"no task with id {task_id}")
        # task_tags rows go with it, thanks to ON DELETE CASCADE + the PRAGMA.
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return row


# --------------------------------------------------------------------------
# Presentation
# --------------------------------------------------------------------------


def format_table(rows: Sequence[sqlite3.Row], color: bool) -> str:
    lines = [
        ROW_FORMAT.format(id="ID", priority="Pri", status="Status", due="Due",
                          title="Title", tags="Tags"),
        ROW_FORMAT.format(id="--", priority="---", status="------", due="-" * 10,
                          title="-" * 31, tags="-" * 12),
    ]
    for row in rows:
        line = ROW_FORMAT.format(
            id=row["id"],
            priority=row["priority"],
            status="done" if row["done"] else "open",
            due=row["due_date"] if row["due_date"] else "-",
            title=row["title"],
            tags=row["tags"] or "-",
        ).rstrip()
        if color:
            line = f"{ANSI[row['priority']]}{line}{RESET}" if ANSI[row["priority"]] else line
        lines.append(line)
    return "\n".join(lines)


def want_color(choice: str) -> bool:
    if choice == "always":
        return True
    if choice == "never":
        return False
    # "auto": colour a terminal, stay plain when piped into a file or `less`.
    # NO_COLOR is the community convention: https://no-color.org/
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def priority_type(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"priority must be a whole number, got {raw!r}")
    if not 1 <= value <= 5:
        raise argparse.ArgumentTypeError(f"priority must be between 1 and 5, got {value}")
    return value


def iso_date_type(raw: str) -> str:
    try:
        date.fromisoformat(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"due date must be ISO-8601 YYYY-MM-DD, got {raw!r}")
    return raw


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker_stretch.py",
        description="A task tracker backed by SQLite, with tags, sorting and colour.",
    )
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto",
                        help="colour output by priority (default: auto)")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    p_add = sub.add_parser("add", help="add a new task")
    p_add.add_argument("title")
    p_add.add_argument("--due", type=iso_date_type, default=None, metavar="YYYY-MM-DD")
    p_add.add_argument("--priority", type=priority_type, default=3, metavar="N")
    p_add.add_argument("--tag", action="append", default=[], metavar="NAME",
                       help="attach a tag; repeat for several")

    p_list = sub.add_parser("list", help="list tasks")
    p_list.add_argument("--priority", type=priority_type, default=None, metavar="N")
    p_list.add_argument("--status", choices=("open", "done", "all"), default="all")
    p_list.add_argument("--tag", default=None, metavar="NAME", help="only tasks with this tag")
    p_list.add_argument("--sort", choices=tuple(SORT_CLAUSES), default="id")

    sub.add_parser("done", help="mark a task done").add_argument("id", type=int)
    sub.add_parser("undone", help="flip a task back to open").add_argument("id", type=int)
    sub.add_parser("delete", help="delete a task").add_argument("id", type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    init_db()

    if args.command == "add":
        new_id = add_task(args.title, args.due, args.priority, args.tag)
        print(f"Added task {new_id}: {args.title}")
        return 0

    if args.command == "list":
        rows = list_tasks(priority=args.priority, status=args.status,
                          tag=args.tag, sort=args.sort)
        print(format_table(rows, want_color(args.color)) if rows
              else "No tasks match those filters.")
        return 0

    if args.command in {"done", "undone"}:
        try:
            row = set_done(args.id, args.command == "done")
        except LookupError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        verb = "done" if args.command == "done" else "open again"
        print(f"Task {row['id']} is {verb}: {row['title']}")
        return 0

    if args.command == "delete":
        try:
            row = delete_task(args.id)
        except LookupError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"Deleted task {row['id']}: {row['title']}")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
