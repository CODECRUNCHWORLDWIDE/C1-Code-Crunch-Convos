"""Mini-Project — Task tracker CLI starter.

This file is a *skeleton*. Your job is to fill in the TODOs.

Usage when finished
-------------------
    python starter.py add "Finish quiz" --due 2026-05-15 --priority 2
    python starter.py list
    python starter.py list --priority 2 --status open
    python starter.py done 1
    python starter.py delete 2

Rules
-----
* Every value that enters SQL must go through a `?` placeholder.
* Use type hints on every function.
* Use the `with sqlite3.connect(...)` pattern so transactions commit
  on success and roll back on exception.

Docs
----
sqlite3 module:  https://docs.python.org/3/library/sqlite3.html
argparse:        https://docs.python.org/3/library/argparse.html
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
DB_PATH: Final[Path] = Path("tasks.db")

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    due_date  TEXT,
    priority  INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    done      INTEGER NOT NULL DEFAULT 0
);
"""

VALID_STATUSES: Final[set[str]] = {"open", "done", "all"}


# ---------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------
def get_connection() -> sqlite3.Connection:
    """Open a connection with row factory + foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create the tasks table if it doesn't exist."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)


# ---------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------
def parse_due_date(value: str | None) -> str | None:
    """Validate a YYYY-MM-DD string. Return it on success, or None if value is None."""
    if value is None:
        return None
    try:
        # `date.fromisoformat` enforces YYYY-MM-DD in Python 3.11+.
        date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid due date {value!r}: {exc}")
    return value


def parse_priority(value: int) -> int:
    if not 1 <= value <= 5:
        raise SystemExit(f"Priority must be between 1 and 5, got {value}")
    return value


# ---------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------
def cmd_add(title: str, due: str | None, priority: int) -> None:
    """Insert a new task and print the new row id.

    TODO (student):
      * Insert a row into `tasks`. Use a parameterized query.
      * Print: f"Added task #{new_id}: {title!r}"
    """
    due_clean = parse_due_date(due)
    priority_clean = parse_priority(priority)

    with get_connection() as conn:
        # --- BEGIN your code ---
        # cursor = conn.cursor()
        # cursor.execute(
        #     "INSERT INTO tasks (title, due_date, priority) VALUES (?, ?, ?)",
        #     (title, due_clean, priority_clean),
        # )
        # new_id = cursor.lastrowid
        # print(f"Added task #{new_id}: {title!r}")
        raise NotImplementedError("cmd_add: implement the parameterized INSERT")
        # --- END your code ---


def cmd_list(priority: int | None, status: str) -> None:
    """List tasks, applying optional filters.

    TODO (student):
      * Build a SELECT with WHERE conditions that depend on which filters
        are set. Keep the query parameterized — accumulate values into a
        list called `params` and the conditions into `where_parts`.
      * Order results by priority, then due_date NULLS LAST, then id.
      * Print a tidy table (see README for sample output).
    """
    if status not in VALID_STATUSES:
        raise SystemExit(f"--status must be one of {sorted(VALID_STATUSES)}; got {status!r}")

    where_parts: list[str] = []
    params: list[object] = []

    if priority is not None:
        where_parts.append("priority = ?")
        params.append(priority)

    if status == "open":
        where_parts.append("done = ?")
        params.append(0)
    elif status == "done":
        where_parts.append("done = ?")
        params.append(1)
    # status == "all" -> no filter

    query = "SELECT id, title, due_date, priority, done FROM tasks"
    if where_parts:
        query += " WHERE " + " AND ".join(where_parts)
    query += " ORDER BY priority ASC, COALESCE(due_date, '9999-12-31') ASC, id ASC"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    if not rows:
        print("No tasks match those filters.")
        return

    # TODO (student): format the rows like the README sample.
    # Replace the dumb loop below with a nicely formatted table.
    print("ID  Pri  Status  Due         Title")
    print("--  ---  ------  ----------  -------------------------------")
    for row in rows:
        status_str = "done" if row["done"] else "open"
        due_str = row["due_date"] or "-"
        print(f"{row['id']:>2}  {row['priority']:>3}  {status_str:<6}  {due_str:<10}  {row['title']}")


def cmd_done(task_id: int) -> None:
    """Mark a task as done.

    TODO (student):
      * UPDATE tasks SET done = 1 WHERE id = ?
      * Check cursor.rowcount; if 0, print "No task with id {task_id}".
    """
    with get_connection() as conn:
        # --- BEGIN your code ---
        raise NotImplementedError("cmd_done: implement the parameterized UPDATE")
        # --- END your code ---


def cmd_delete(task_id: int) -> None:
    """Delete a task by id.

    TODO (student):
      * DELETE FROM tasks WHERE id = ?
      * Check rowcount; if 0, print a clear error and exit with code 1.
    """
    with get_connection() as conn:
        # --- BEGIN your code ---
        raise NotImplementedError("cmd_delete: implement the parameterized DELETE")
        # --- END your code ---


# ---------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker",
        description="A tiny SQLite-backed task tracker.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="The task title")
    p_add.add_argument("--due", default=None, help="Due date in YYYY-MM-DD format")
    p_add.add_argument("--priority", type=int, default=3, help="Priority 1 (high) to 5 (low)")

    # list
    p_list = subparsers.add_parser("list", help="List tasks")
    p_list.add_argument("--priority", type=int, default=None, help="Filter by priority")
    p_list.add_argument(
        "--status",
        choices=sorted(VALID_STATUSES),
        default="all",
        help="Filter by status",
    )

    # done
    p_done = subparsers.add_parser("done", help="Mark a task as done")
    p_done.add_argument("task_id", type=int, help="Task id")

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("task_id", type=int, help="Task id")

    return parser


def main(argv: list[str] | None = None) -> int:
    init_db()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "add":
            cmd_add(args.title, args.due, args.priority)
        elif args.command == "list":
            cmd_list(args.priority, args.status)
        elif args.command == "done":
            cmd_done(args.task_id)
        elif args.command == "delete":
            cmd_delete(args.task_id)
        else:
            parser.print_help()
            return 1
    except NotImplementedError as exc:
        # Friendly message while the student is still filling in TODOs.
        print(f"[not implemented yet] {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
