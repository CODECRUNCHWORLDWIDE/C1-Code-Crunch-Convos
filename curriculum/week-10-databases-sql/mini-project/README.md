# Mini-Project — SQLite Task Tracker CLI

> **Topic:** one small tool that uses the whole week — a table you design, all four CRUD verbs, `WHERE`/`ORDER BY`, and a placeholder in front of every value
> **Lecture:** [01 — Relational databases and SQL](../lecture-notes/01-relational-databases-and-sql.md) · [03 — Python with SQLite and an ORM](../lecture-notes/03-python-with-sqlite-and-orm.md)
> **Difficulty:** Medium
> **Target time:** 4-6 hours
> **Why this one:** it is the first program you write whose memory outlives it. Close it, reboot the laptop, open it again, and your tasks are still there. Week 9's blog kept its posts in a Python list and lost them on every restart; this is the week that fixes that, and this project is where every piece of it meets.

<!-- no-runnable-file: what you hand in is a folder in your own repository - tracker.py, the tasks.db it built, and a commit history - not one script named after this page. The runnable answer ships beside this page as tracker-solution.py and is linked from Download and run, because a download called README-solution.py would tell nobody what it is. -->

## The Brief

Build a to-do list you drive from the terminal.

Think of the tasks as index cards. Until now your programs kept their cards
loose on a desk: when the program ended, somebody swept the desk clean. A
database is a filing cabinet instead. You slide a card into the drawer, the
program ends, and the card is still in the drawer tomorrow morning.

The cabinet here is one file, `tasks.db`. SQLite is a whole database that lives
inside a single file — no server to start, no password, nothing to install.
Python already ships with it.

Your program is the clerk standing at the cabinet. It takes four orders — file a
new card, read the cards back, stamp one done, throw one away:

```text
python tracker.py add "Finish quiz" --due 2026-05-15 --priority 2
python tracker.py add "Pet the cat" --priority 5
python tracker.py list
python tracker.py list --priority 2
python tracker.py list --status open
python tracker.py done 1
python tracker.py delete 2
```

Those four orders have real names in SQL: `INSERT`, `SELECT`, `UPDATE`,
`DELETE`. People say **CRUD** — create, read, update, delete. Every database
program you ever write is those four, wearing different clothes.

Run the tool with no order at all, or with `--help`, and it prints the orders it
understands.

## Starter

Copy this into a file called **`tracker.py`** in a folder of your own. Mind the
name: `tracker.py` is yours to write, and the finished answer downloads under
the longer name `tracker-solution.py` so it can never land on top of your work.

It runs exactly as pasted. It just does not do much yet — `list` prints an empty
table and `add` claims task 0. Fill in one TODO, run it, then fill in the next.

```python
"""tracker.py — a command-line task tracker backed by a SQLite database."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path

DEFAULT_DB = "tasks.db"

# One table is plenty. IF NOT EXISTS means running this every time is safe.
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    due_date  TEXT,                              -- ISO-8601 'YYYY-MM-DD' or NULL
    priority  INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    done      INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    """Open the file, read rows by column name, make sure the table exists."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def add_task(
    conn: sqlite3.Connection, title: str, due: str | None, priority: int
) -> int:
    """Insert one task and return its new id."""
    # TODO: INSERT INTO tasks (title, due_date, priority) VALUES (?, ?, ?)
    # Wrap it in `with conn:` so it commits, then return cursor.lastrowid.
    return 0


def list_tasks(
    conn: sqlite3.Connection,
    priority: int | None = None,
    status: str = "all",
) -> list[sqlite3.Row]:
    """Return the tasks that survive the filters, in a sensible order."""
    # TODO: start from "SELECT id, title, due_date, priority, done FROM tasks".
    # Collect a clause like "priority = ?" for each filter that was given, join
    # them with " AND ", and keep every value in a separate params list.
    # Finish with ORDER BY, and pass params as the second argument to execute.
    return []


def mark_done(conn: sqlite3.Connection, task_id: int) -> bool:
    """Set done = 1 for one task. False when no such id exists."""
    # TODO: UPDATE tasks SET done = 1 WHERE id = ?
    # cursor.rowcount tells you how many rows actually changed.
    return False


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    """Delete one task. False when no such id exists."""
    # TODO: DELETE FROM tasks WHERE id = ?  — same rowcount trick.
    return False


def format_rows(rows: list[sqlite3.Row]) -> str:
    """Render tasks as the fixed-width table from Expected output."""
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
    """argparse type: an integer SQLite's CHECK would also accept."""
    # TODO: reject anything outside 1-5 with argparse.ArgumentTypeError.
    return int(value)


def valid_date(value: str) -> str:
    """argparse type: a string that parses as an ISO-8601 date."""
    # TODO: date.fromisoformat(value) raises ValueError on junk. Catch it and
    # raise argparse.ArgumentTypeError instead, so argparse prints the usage.
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
    show.add_argument("--status", choices=("open", "done", "all"), default="all")

    finish = commands.add_parser("done", help="mark a task done")
    finish.add_argument("id", type=int)

    remove = commands.add_parser("delete", help="delete a task")
    remove.add_argument("id", type=int)

    return parser


def run_command(conn: sqlite3.Connection, args: argparse.Namespace) -> int:
    """Carry out one parsed command. Returns the exit code."""
    if args.command == "add":
        task_id = add_task(conn, args.title, args.due, args.priority)
        print(f"Added task {task_id}: {args.title}")
        return 0
    if args.command == "list":
        print(format_rows(list_tasks(conn, args.priority, args.status)))
        return 0
    # TODO: done and delete. On a missing id, print to sys.stderr and return 1.
    return 0


def main(argv: list[str]) -> int:
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
```

## Requirements

1. **One table, built on the first run.** Exactly this schema, and running it
   again must be harmless:

   ```sql
   CREATE TABLE IF NOT EXISTS tasks (
       id        INTEGER PRIMARY KEY AUTOINCREMENT,
       title     TEXT    NOT NULL,
       due_date  TEXT,                              -- ISO-8601 'YYYY-MM-DD' or NULL
       priority  INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
       done      INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
   );
   ```

   `CHECK` is the table refusing bad data itself, so a bug in your Python cannot
   sneak a priority of 99 into the drawer. `done` is a 0 or a 1 because SQLite
   has no true/false type of its own.

2. **Four commands**, behaving like this:

   | Command | Effect |
   |---------|--------|
   | `add TITLE [--due YYYY-MM-DD] [--priority N]` | Insert a task. Priority defaults to 3, due date may be missing. Print the new id. |
   | `list [--priority N] [--status open\|done\|all]` | Print the table. Filters stack. Status defaults to `all`. |
   | `done ID` | Set `done = 1` on that one row and say so. |
   | `delete ID` | Remove that one row and say so. |
   | *(nothing)* or `--help` | Print the usage. |

3. **The filters stack.** `list --priority 2 --status open` shows only the open
   tasks whose priority is 2. Each filter you were given adds one more clause;
   a filter you were not given adds nothing.
4. **A sensible order.** `ORDER BY done, priority, id` — open work first, then
   the most urgent, then oldest first inside a tie.
5. **Bad input is refused before it reaches SQL.** A priority outside 1-5 and a
   due date that is not `YYYY-MM-DD` both stop at the command line with a usage
   message.
6. **A missing id is an error, not a shrug.** `done 99` and `delete 99` print to
   `stderr` and exit with code 1. Ask the row how many rows changed —
   `cursor.rowcount` — rather than assuming.
7. **Type hints on every function**, parameters and return alike.
8. **An empty result still prints a table**, with `(no tasks match)` under the
   header. Silence looks like a crash.

## Constraints

- **Standard library only:** `sqlite3`, `argparse`, `pathlib`, `sys`, `typing`.
  Everything this project needs is already on the machine, and the point of the
  week is the database, not a package list.
- **Every value reaches SQL through a `?` placeholder. No exceptions, ever.**
  Not an f-string, not a `+`, not `%`. Writing
  `f"... WHERE id = {task_id}"` glues the user's text into the sentence the
  database is about to obey, so a task titled `'); DROP TABLE tasks; --` stops
  being a title and becomes a command. With a `?`, the database reads the
  sentence first and the value afterwards — the value can never turn into
  instructions. That is SQL injection, and the `?` is the whole fix.
- **Column names and operators are code; only values are data.** You may build
  a `WHERE` clause by joining fixed fragments like `"priority = ?"`. You may
  never build one by pasting in something the user typed.
- **Wrap every write in `with conn:`.** That context manager commits when the
  block finishes and rolls back if it raises. Without it your `INSERT` is a
  promise the database never keeps: the program exits and the row is gone.
- **Set `conn.row_factory = sqlite3.Row`.** Default rows are plain tuples, so
  you would be writing `row[3]` and counting columns on your fingers. With
  `Row` you write `row["priority"]`, and adding a column later cannot silently
  shift every number.
- **Results go to `stdout`, complaints go to `stderr`.** It is why
  `python tracker.py list > today.txt` saves a clean table and still shows you
  the error on screen.
- **One table.** Tags and projects are tempting and they are in Stretch. Two
  tables means joins, and joins are a second lesson stacked on this one.

## Expected output

The shipped answer, run with no arguments, demonstrates itself end to end in a
throwaway folder and cleans up after itself. Captured from a real run:

```bash
cd curriculum/week-10-databases-sql/mini-project
PYTHONIOENCODING=utf-8 python tracker.py
```

```text
Demo run (no arguments): a full session in a throwaway folder.

$ add "Finish quiz" --due 2026-05-15 --priority 2
$ add "Pet the cat" --priority 5
$ add "Review SQL injection notes" --due 2026-05-12 --priority 1

$ list
ID  Pri  Status  Due         Title
--  ---  ------  ----------  -------------------------------
 3    1  open    2026-05-12  Review SQL injection notes
 1    2  open    2026-05-15  Finish quiz
 2    5  open    -           Pet the cat

$ done 3
Marked task 3 done.

$ list --status open
ID  Pri  Status  Due         Title
--  ---  ------  ----------  -------------------------------
 1    2  open    2026-05-15  Finish quiz
 2    5  open    -           Pet the cat

$ list --priority 2
ID  Pri  Status  Due         Title
--  ---  ------  ----------  -------------------------------
 1    2  open    2026-05-15  Finish quiz

$ delete 2
Deleted task 2.

$ list
ID  Pri  Status  Due         Title
--  ---  ------  ----------  -------------------------------
 1    2  open    2026-05-15  Finish quiz
 3    1  done    2026-05-12  Review SQL injection notes
```

Read the `list` blocks against the `ORDER BY`. After `done 3`, task 3 drops to
the bottom — not because it was deleted, but because `done` sorts first and a 1
sorts after a 0.

## Steps

1. **Get the cabinet built.** Write `connect()`, run the program once, and check
   that a `tasks.db` file appeared. Run it twice; nothing should break, because
   of `IF NOT EXISTS`.
2. **`add` next.** One `INSERT`, three `?`, inside `with conn:`. Print the id
   that `cursor.lastrowid` hands back.
3. **`list` with no filters.** A plain `SELECT`, straight into `format_rows`.
   Now you can see whether step 2 really wrote anything.
4. **Add the filters one at a time.** Build a list of clause strings and a list
   of values side by side. Join the clauses with `" AND "`, stick `" WHERE "` in
   front only if the list is not empty, and hand the values to `execute` as the
   second argument.
5. **`done` and `delete`.** Both are one statement with one `?`. Return
   `cursor.rowcount > 0` and let the caller decide what to print.
6. **Wire the failures.** `done 99` should now print to `stderr` and exit 1.
7. **Validate at the door.** Give argparse your own `type=` functions so a bad
   priority or a bad date never reaches the database.
8. **Try to break it.** Add a task titled `'); DROP TABLE tasks; --` and then
   `list`. If your placeholders are right, the title prints back at you word for
   word and the table is untouched. That is the moment the lesson lands.

## The Solution

```python
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
```

**Why it works.** Every function here is the same three moves: open the cabinet,
hand SQL a sentence with `?` where the values go, hand it the values separately.
Nothing in the program ever builds a sentence out of what somebody typed.

`connect()` does three small things at once. It opens the file, it turns rows
into things you can read by name, and it runs the schema. Running the schema on
every single startup sounds wasteful, and it is the reason you never have to
think about setup: `IF NOT EXISTS` makes the first run and the thousandth run
identical.

`list_tasks` is the only clever part, and the cleverness is in what it refuses
to do. It grows two lists in step — clause strings on one side, values on the
other. `"priority = ?"` is a fragment written by you, in the file, and it is the
same fragment whatever the user types. The number the user typed goes into
`params` and never touches the string. So the SQL text has a fixed shape no
input can change, while the filters still combine freely.

`mark_done` and `delete_task` both return a bool instead of printing. They ask
`cursor.rowcount` — how many rows did that actually change? — and hand the
answer up to `run_command`, which owns all the printing and all the exit codes.
That split is why the same two functions would work unchanged behind a website.

## Run it

Copy the worked answer on this page into `tracker.py` and run it:

```bash
python tracker.py
```

With no arguments it plays the whole session above inside a temporary folder and
deletes the folder on the way out, so it leaves no `tasks.db` behind. Give it a
real command and it works on a real file:

```bash
python tracker.py add "Finish quiz" --due 2026-05-15 --priority 2
python tracker.py list --status open
```

Save your own version as `tracker.py`. The download keeps the longer name on
purpose, so it cannot overwrite the file you are writing.

## Common bugs to catch

- **`sqlite3.OperationalError: no such table: tasks`** — you opened the database
  but never ran the schema, or you ran it against a different path. Put
  `conn.executescript(SCHEMA)` inside `connect()` so it is impossible to forget.
- **`sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 2 supplied.`**
  — you passed `(task_id)` instead of `(task_id,)`. Without the comma that is
  just a number in brackets; Python only sees a tuple when the comma is there.
- **Rows appear while the program runs, then vanish.** You never committed. Wrap
  the write in `with conn:`, which commits at the end of the block.
- **`sqlite3.IntegrityError: CHECK constraint failed: tasks`** — a priority
  outside 1-5 got through. The table caught what your validation missed; fix the
  validation, do not remove the `CHECK`.
- **`done 99` cheerfully says it worked.** You printed success without looking.
  `UPDATE` on a row that does not exist is not an error — it just changes
  nothing. Check `cursor.rowcount > 0`.
- **A title with an apostrophe crashes, or a title like `'); DROP TABLE tasks; --` does damage.**
  Both are the same bug: a value was pasted into the SQL text. Every value gets
  a `?`.
- **`list --status open` returns everything.** The clause was appended but its
  value was not, or `WHERE` was never added because you built the string in the
  wrong order. Print your `sql` and `params` side by side; the mismatch is
  usually obvious in one line.

## Under the hood

<details>
<summary>Under the hood — why a placeholder is safe when an f-string is not</summary>

The database does not read your query the way you read a sentence, all at once.
It **parses** first, turning the text into a plan: this is a `SELECT`, this is
the table, this is the filter. Only then does it fill the `?` slots with your
values and run the plan.

An f-string does its work before any of that. By the time SQLite sees the text,
`'); DROP TABLE tasks; --` is already part of the sentence, and the parser has
no way to know those characters came from a user rather than from you. It parses
two statements and obeys both.

With a `?`, the plan is already built when the value arrives. A value can be a
number, a string, or NULL. It cannot be a statement, because the shape of the
statement was decided before the value existed.

This is also why you cannot use a placeholder for a table or column name.
`SELECT * FROM ?` fails: the name is part of the plan, and the plan is fixed
before binding. When a column name really has to vary, pick it from a hard-coded
allow-list in your own code — never from user text.

Bound parameters are usually faster too. The same statement text with different
values reuses SQLite's cached plan; a fresh f-string is a new statement every
time and gets re-parsed.

</details>

<details>
<summary>Under the hood — what INTEGER PRIMARY KEY AUTOINCREMENT really does</summary>

Every ordinary SQLite table secretly has a 64-bit `rowid` that indexes it.
Declaring a column `INTEGER PRIMARY KEY` does not add a column beside the rowid
— it makes your column *become* the rowid. That is why `id` lookups are fast
without an index of your own, and why `id` is spelled `INTEGER` and not `INT`
(only that exact spelling triggers the aliasing).

`AUTOINCREMENT` adds one extra promise on top: an id is never reused. Without
it, deleting the highest row lets the next insert take that number back. With
it, SQLite keeps a high-water mark in an internal `sqlite_sequence` table and
always goes higher.

That promise costs a little write and can eventually run out of numbers, so the
SQLite documentation suggests skipping it unless you need it. It is here because
a task tracker is exactly the case that needs it: `delete 2` then `add` should
not hand the new task the dead task's number, or yesterday's note saying "task 2
is the quiz" becomes a lie.

</details>

<details>
<summary>Under the hood — what `with conn:` commits, and what it does not</summary>

`with conn:` is a transaction, not a file handle. Leaving the block normally
commits; leaving it because of an exception rolls back. It does **not** close
the connection — that is why the solution still calls `conn.close()` in a
`finally`.

A transaction is all-or-nothing. Two `INSERT`s inside one `with` block either
both land or neither does, even if the power goes out between them. SQLite gets
that by writing the change to a side file first — a rollback journal, or a
write-ahead log — and only then declaring the change official. A crash mid-write
leaves the side file, and the next open finishes or undoes the job.

There is one trap worth knowing. Python's `sqlite3` opens a transaction
automatically before an `INSERT`, `UPDATE` or `DELETE`, but historically not
before a `SELECT`. So a read can see a state a write in the same program has not
committed yet. Keeping writes inside `with conn:` and reading afterwards, as
this project does, sidesteps the whole question.

</details>

<details>
<summary>Under the hood — sqlite3.Row, and why it beats both tuples and dicts</summary>

A default row is a tuple, so `row[3]` means "the fourth column of whatever this
SELECT happened to list". Add a column to the query and every number after it
quietly points at the wrong thing. No error, just wrong answers.

`sqlite3.Row` fixes the reading without paying for a dict. It keeps the tuple's
compact storage and adds name lookup on top, so `row["priority"]` and `row[3]`
both work, and `dict(row)` converts when you need JSON. Names are matched
case-insensitively, and `row.keys()` tells you what came back.

It is one line — `conn.row_factory = sqlite3.Row` — set once on the connection,
and every cursor from that connection inherits it.

</details>

## Acceptance checklist

- [ ] The first run creates `tasks.db` and the `tasks` table; the second run is
      harmless.
- [ ] `add` inserts, defaults priority to 3, accepts a missing due date, and
      prints the new id.
- [ ] `list` prints the table; `--priority` and `--status` work alone and stack.
- [ ] `done ID` marks exactly one row and nothing else.
- [ ] `delete ID` removes exactly one row; a missing id errors on `stderr` and
      exits 1.
- [ ] Every value in every statement is a `?`. No f-string, no `+`, no `%`.
- [ ] A task titled `'); DROP TABLE tasks; --` round-trips as plain text.
- [ ] Priority outside 1-5 and a non-ISO date are both refused at the command
      line.
- [ ] Every function has type hints, and no subcommand prints the usage.
- [ ] Committed to Git with a clear message, e.g.
      `feat(tracker): sqlite task tracker mini-project`.

How it is marked, out of 100:

| Area | Points |
|------|--------|
| Schema correctly created on first run (idempotent) | 10 |
| `add` works, default priority is 3, due date optional | 15 |
| `list` works and the three filters compose correctly | 20 |
| `done` updates exactly the right row | 10 |
| `delete` removes exactly the right row, errors when no match | 10 |
| Parameterized queries everywhere (no f-strings into SQL) | 15 |
| Input validation (priority range, ISO date) | 10 |
| Clean help / usage output | 5 |
| Type hints on every function | 5 |

A submission that f-strings a value into SQL loses **all** points for
parameterization and is flagged in review. It is the one line in the rubric
that is not about neatness — it is the difference between a tool and a hole.

## Stretch

- **`undone ID`.** Flip a finished task back to open. One `UPDATE`, one `?`, and
  it is nearly `mark_done` in a mirror.
- **`--sort {priority,due,id}` on `list`.** Careful: a sort key is a column
  name, so it is code, not data. Map the flag to a fixed SQL fragment through a
  dictionary you wrote; never paste the flag into the query.
- **Colour by priority** — 1 red, 2 yellow, 3 plain, 4-5 dim. ANSI escape codes
  are enough, and `rich` is nicer if you want it.
- **A `tags` table.** A task can have many tags, a tag can have many tasks, so
  you need a third table joining them, and a `--tag` filter that joins on it.
  This is Week 10's join lecture, cashed in.
- **A tiny test suite** against `sqlite3.connect(":memory:")` — a whole database
  that never touches the disk and disappears when the test ends, so each test
  starts spotless.

When you finish, push the project to GitHub and post the link in `#week-10` on
Discord. Week 11 puts real tests on top of exactly this code, so the tidier you
leave it now, the shorter that week is.
