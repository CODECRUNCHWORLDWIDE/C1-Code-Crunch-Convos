# Mini-Project — SQLite Task Tracker CLI

Build a command-line task tracker. Tasks live in a SQLite database. The CLI supports adding tasks, listing them (with filters), marking them done, and deleting them.

This project ties together everything from Week 10: schema design, CRUD, parameterized queries, `WHERE`/`ORDER BY`, and a small dose of UX polish.

## What it should do

```
python tracker.py add "Finish quiz" --due 2026-05-15 --priority 2
python tracker.py add "Pet the cat" --priority 5
python tracker.py list
python tracker.py list --priority 2
python tracker.py list --status open
python tracker.py done 1
python tracker.py delete 2
```

When invoked with no subcommand (or `--help`), print a help message listing the commands.

## Data model

One table is plenty:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    due_date  TEXT,                              -- ISO-8601 'YYYY-MM-DD' or NULL
    priority  INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    done      INTEGER NOT NULL DEFAULT 0         -- 0 = open, 1 = done
);
```

A separate `CHECK` keeps the priority in range. We treat `done` as a 0/1 integer because SQLite does not have a native boolean.

## CLI commands

| Command                                          | Effect                                                                   |
|--------------------------------------------------|--------------------------------------------------------------------------|
| `add TITLE [--due YYYY-MM-DD] [--priority N]`    | Insert a new task. Default priority 3.                                   |
| `list [--priority N] [--status open|done|all]`   | Print tasks. Filters compose. Default status = `all`.                    |
| `done ID`                                        | Set `done = 1` for the given id. Print a friendly confirmation.          |
| `delete ID`                                      | Delete the row with the given id. Refuse if no such id exists.           |
| `--help`                                         | Show help.                                                               |

## Required techniques

- Standard library only: `sqlite3`, `argparse`, `pathlib`, `sys`, `typing`.
- **Every** value goes through a `?` placeholder. No exceptions.
- Use `with sqlite3.connect(...)` (or an equivalent context manager) so transactions commit/rollback automatically.
- Use `conn.row_factory = sqlite3.Row` so you can read columns by name in the list output.
- Validate user input: priority must be 1–5; due-date must parse as ISO-8601.

## Suggested output

```
$ python tracker.py list
ID  Pri  Status  Due         Title
--  ---  ------  ----------  -------------------------------
 1    2  open    2026-05-15  Finish quiz
 2    5  open    -           Pet the cat
 3    1  done    2026-05-12  Review SQL injection notes
```

## File layout

```
mini-project/
├── README.md          (this file)
├── starter.py         (skeleton — fill in the TODOs)
└── tracker.py         (your finished CLI)
```

You don't have to keep these names — but `starter.py` is the recommended jumping-off point.

## Rubric (out of 100)

| Area                                                          | Points |
|---------------------------------------------------------------|--------|
| Schema correctly created on first run (idempotent)            | 10     |
| `add` works, default priority is 3, due-date optional         | 15     |
| `list` works and the three filters compose correctly          | 20     |
| `done` updates exactly the right row                          | 10     |
| `delete` updates exactly the right row, errors when no match  | 10     |
| Parameterized queries everywhere (no f-strings into SQL)      | 15     |
| Input validation (priority range, ISO date)                   | 10     |
| Clean help / usage output                                     | 5      |
| Type hints on every function                                  | 5      |

A submission that f-strings a value into SQL loses **all** points for parameterization and is flagged in review.

## Stretch goals

- Add an `--undone ID` command to flip a task back to open.
- Add a `--sort {priority,due,id}` flag to `list`.
- Color the output by priority (1 red, 2 yellow, 3 default, 4–5 dim). Use ANSI codes or the `rich` library.
- Add a `tags` table (many-to-many) and a `--tag` filter.
- Add a tiny test suite that uses an in-memory database (`sqlite3.connect(":memory:")`).

## Next steps

When you finish, push the project to GitHub and post the link in `#week-10` Discord. In Week 11 we'll add real tests on top of it.
