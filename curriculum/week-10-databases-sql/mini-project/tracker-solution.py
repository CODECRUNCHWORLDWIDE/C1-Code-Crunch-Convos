"""tracker-solution.py — the Week 10 mini-project, finished: a SQLite task tracker.

A command-line to-do list that keeps its tasks in a real SQLite database
instead of a text file, so they survive the program closing. It can add a
task, list tasks (with filters that stack), mark one done, and delete one.

Every value handed to SQL travels through a ``?`` placeholder — never an
f-string — so a task titled ``'; DROP TABLE tasks; --`` is stored as that
literal text and changes nothing. ``sqlite3.Row`` lets the list command read
columns by name instead of by position, and the optional filters compose by
appending fixed clause fragments while every value stays a bound parameter.

Two ways to run it::

    # Against a real database file you keep:
    python tracker-solution.py add "Finish quiz" --due 2026-05-15 --priority 2
    python tracker-solution.py list --status open
    python tracker-solution.py done 1
    python tracker-solution.py delete 2

    # With no arguments it demonstrates itself end to end in a throwaway
    # folder — build, add, list, filter, done, delete — and deletes the folder
    # on the way out, so it runs anywhere and leaves no .db behind.
    python tracker-solution.py

Save your own copy as ``tracker.py`` in your mini-project folder. The longer
download name is here so it cannot land on top of the file you are writing.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Final

DEFAULT_DB: Final[str] = "tasks.db"

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    due_date  TEXT,                              -- ISO-8601 'YYYY-MM-DD' or NULL
    priority  INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    done      INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    """Open `db_path`, read rows by name, and make sure the table exists."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def add_task(
    conn: sqlite3.Connection, title: str, due: str | None, priority: int
) -> int:
    """Insert one task and return its new id."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, due_date, priority) VALUES (?, ?, ?)",
            (title, due, priority),
        )
    return int(cursor.lastrowid or 0)


def list_tasks(
    conn: sqlite3.Connection,
    priority: int | None = None,
    status: str = "all",
) -> list[sqlite3.Row]:
    """Return tasks, newest filters composing on top of each other.

    The WHERE clause is built from fixed fragments only — a column name and an
    operator are code, never data — while every value travels as a bound ``?``.
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

    sql = "SELECT id, title, due_date, priority, done FROM tasks"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY done, priority, id"
    return conn.execute(sql, params).fetchall()


def mark_done(conn: sqlite3.Connection, task_id: int) -> bool:
    """Set done = 1 for one task. Returns False when no such id exists."""
    with conn:
        cursor = conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)
        )
    return cursor.rowcount > 0


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    """Delete one task. Returns False when no such id exists."""
    with conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return cursor.rowcount > 0


def format_rows(rows: list[sqlite3.Row]) -> str:
    """Render tasks as the fixed-width table from the brief."""
    lines = [
        "ID  Pri  Status  Due         Title",
        "--  ---  ------  ----------  -------------------------------",
    ]
    for row in rows:
        status = "done" if row["done"] else "open"
        due = row["due_date"] or "-"
        lines.append(
            f"{row['id']:>2}  {row['priority']:>3}  "
            f"{status:<6}  {due:<10}  {row['title']}"
        )
    if not rows:
        lines.append("(no tasks match)")
    return "\n".join(lines)


def valid_priority(value: str) -> int:
    """argparse type: an integer that SQLite's CHECK would also accept."""
    number = int(value)
    if not 1 <= number <= 5:
        raise argparse.ArgumentTypeError("priority must be between 1 and 5")
    return number


def valid_date(value: str) -> str:
    """argparse type: a string that parses as an ISO-8601 date."""
    try:
        date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"due date must be ISO-8601 (YYYY-MM-DD), got {value!r}"
        )
    return value


def build_parser() -> argparse.ArgumentParser:
    """The add / list / done / delete command line."""
    parser = argparse.ArgumentParser(
        description="A tiny task tracker backed by a SQLite database."
    )
    parser.add_argument(
        "--db", type=Path, default=Path(DEFAULT_DB),
        help=f"database file (default: {DEFAULT_DB})",
    )
    commands = parser.add_subparsers(dest="command")

    add = commands.add_parser("add", help="add a task")
    add.add_argument("title")
    add.add_argument("--due", type=valid_date, default=None)
    add.add_argument("--priority", type=valid_priority, default=3)

    show = commands.add_parser("list", help="list tasks")
    show.add_argument("--priority", type=valid_priority, default=None)
    show.add_argument(
        "--status", choices=("open", "done", "all"), default="all"
    )

    finish = commands.add_parser("done", help="mark a task done")
    finish.add_argument("id", type=int)

    remove = commands.add_parser("delete", help="delete a task")
    remove.add_argument("id", type=int)

    return parser


def run_command(conn: sqlite3.Connection, args: argparse.Namespace) -> int:
    """Carry out one parsed command against `conn`. Returns an exit code."""
    if args.command == "add":
        task_id = add_task(conn, args.title, args.due, args.priority)
        print(f"Added task {task_id}: {args.title}")
        return 0
    if args.command == "list":
        print(format_rows(list_tasks(conn, args.priority, args.status)))
        return 0
    if args.command == "done":
        if mark_done(conn, args.id):
            print(f"Marked task {args.id} done.")
            return 0
        print(f"error: no task with id {args.id}", file=sys.stderr)
        return 1
    if args.command == "delete":
        if delete_task(conn, args.id):
            print(f"Deleted task {args.id}.")
            return 0
        print(f"error: no task with id {args.id}", file=sys.stderr)
        return 1
    return 0


def demo() -> int:
    """A full session in a throwaway folder, printed as it happens."""
    print("Demo run (no arguments): a full session in a throwaway folder.\n")
    with tempfile.TemporaryDirectory(prefix="tracker_") as workspace:
        conn = connect(Path(workspace) / "tasks.db")
        try:
            print('$ add "Finish quiz" --due 2026-05-15 --priority 2')
            add_task(conn, "Finish quiz", "2026-05-15", 2)
            print('$ add "Pet the cat" --priority 5')
            add_task(conn, "Pet the cat", None, 5)
            print('$ add "Review SQL injection notes" --due 2026-05-12 --priority 1')
            add_task(conn, "Review SQL injection notes", "2026-05-12", 1)

            print("\n$ list")
            print(format_rows(list_tasks(conn)))

            print("\n$ done 3")
            mark_done(conn, 3)
            print("Marked task 3 done.")

            print("\n$ list --status open")
            print(format_rows(list_tasks(conn, status="open")))

            print("\n$ list --priority 2")
            print(format_rows(list_tasks(conn, priority=2)))

            print("\n$ delete 2")
            delete_task(conn, 2)
            print("Deleted task 2.")

            print("\n$ list")
            print(format_rows(list_tasks(conn)))
        finally:
            conn.close()
    return 0


def main(argv: list[str]) -> int:
    """No arguments runs the self-demonstration; otherwise a real command."""
    if not argv:
        return demo()
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    conn = connect(args.db)
    try:
        return run_command(conn, args)
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
