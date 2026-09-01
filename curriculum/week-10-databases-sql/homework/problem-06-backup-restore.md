# Homework Problem 6 — Backup and Restore Script

> **Topic:** snapshotting a live SQLite database safely with `Connection.backup()`, two subcommands, and honest exit codes
> **Lecture:** [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md) (the `sqlite3` sections)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** your mini-project keeps every task in a single `tasks.db` file, and one day you will want a copy of it you can trust — before a risky change, or on a schedule. The lazy way is `cp tasks.db backup.db`, and it works right up until the app is mid-write, at which point the copy holds half a change and SQLite calls it corrupt. This problem is the safe way: a page-by-page snapshot that SQLite itself takes, correct even while the database is being written.

## The Brief

Write `backup.py`, a small command-line tool with two jobs:

- **Back up:** `python backup.py backup tasks.db tasks.backup.db` makes a
  snapshot of a database into a new file.
- **Restore:** `python backup.py restore tasks.backup.db tasks.db` copies a
  snapshot back out to a target file.

Think of a database file as a book someone might be writing in right now.
Copying the file with `cp` is like running the book through a photocopier while
a hand is still writing on page 200 — you get a copy where page 200 is half a
sentence. SQLite's own `Connection.backup()` is like asking the writer to pause
between pages: it copies the book one page at a time, *through the database*,
taking the same short locks a normal reader takes, so the copy is always a
whole, consistent book even if the writing never stops.

The two subcommands are the same move seen twice — copy one database file into
another — so one function does the work and the command line just decides which
file is the source and which is the target. "Restore" is not special; it is a
backup pointed the other way.

## Starter

Save this as `backup.py` and fill in the `TODO`s. It needs nothing but the
standard library — `sqlite3` ships with Python — and runs as pasted, though
the copy raises `NotImplementedError` until you write it.

```python
"""backup.py — snapshot a SQLite database safely, then restore it.

Two subcommands::

    python backup.py backup  source.db backup.db
    python backup.py restore backup.db target.db

Both copy a database file through sqlite3.Connection.backup(), never through a
file copy, so the snapshot is consistent even while the source is being
written. Neither will overwrite an existing target unless --force is passed,
and any error exits non-zero.
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def copy_database(source: Path, target: Path, force: bool) -> int:
    """Snapshot `source` into `target` via Connection.backup(). Returns pages.

    Raises FileNotFoundError / FileExistsError for the two refusals so the CLI
    layer can turn them into a message and an exit code.
    """
    if not source.exists():
        raise FileNotFoundError(f"{source} does not exist")
    # TODO: if target exists and not force, raise FileExistsError

    # TODO: open both databases with sqlite3.connect(...)
    # TODO: call src.backup(dst, progress=callback) to copy page by page, and
    #       capture the total page count from the callback's `total` argument
    # TODO: read the page size with dst.execute("PRAGMA page_size").fetchone()
    # TODO: close both connections in a finally, then print
    #       f"Backed up {pages} pages to {target.name} ({page_size} bytes/page)."
    raise NotImplementedError


def main(argv: list[str]) -> int:
    """Parse the command line and run the copy."""
    parser = argparse.ArgumentParser(
        description="Back up and restore SQLite databases via Connection.backup()."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("backup", "snapshot a database into a new file"),
        ("restore", "copy a snapshot back out to a target file"),
    ):
        sub = commands.add_parser(name, help=help_text)
        sub.add_argument("source", type=Path)
        sub.add_argument("target", type=Path)
        sub.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    try:
        copy_database(args.source, args.target, force=args.force)
    except (FileNotFoundError, FileExistsError, sqlite3.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-10-databases-sql/homework/problem-06-backup-restore.md) and run it there. `sqlite3` ships with Python, so there is nothing to install.

## Requirements

1. A `backup` subcommand: `backup <source> <target>` snapshots `source` into a
   new `target` file.
2. A `restore` subcommand: `restore <backup> <target>` copies a snapshot back
   out — the same operation, source and target swapped.
3. The copy uses `sqlite3.Connection.backup()`, **not** `shutil.copy` or any
   byte-for-byte file copy.
4. Both subcommands refuse to overwrite an existing target unless `--force` is
   passed.
5. A progress message reports how many pages were copied and the page size,
   e.g. `Backed up 3 pages to tasks.backup.db (4096 bytes/page).`
6. Any error — a missing source, a refused overwrite, a SQLite failure — exits
   with a **non-zero** status code.
7. A module docstring at the top explains the trade-off against a plain file
   copy.

## Constraints

- **Use `Connection.backup()`, never `shutil.copy`.** A file copy reads raw
  bytes off the disk with no locks at all. Catch the source mid-transaction and
  the copy holds half a write, which SQLite will later refuse to open as a
  corrupt database. `backup()` copies page by page *through SQLite*, taking the
  same locks any reader takes, so the snapshot is always internally consistent —
  that safety is the entire reason this method exists, and the reason the
  problem forbids the shortcut.
- **Refuse to overwrite unless `--force`.** A backup tool that silently
  clobbers an existing file is one fat-fingered path away from destroying the
  very copy you were trying to protect. Default to refusing; make overwriting a
  thing the user asks for out loud.
- **Return a non-zero exit code on any error.** A script meant for a cron job
  or a `backup && deploy` chain has to *say* it failed in the one language those
  tools read — the exit code. Print the human message to `stderr`, then
  `return 1`; a silent failure that exits `0` is worse than a loud one.
- **Standard library only, with type hints and narrow `except`.** `sqlite3`,
  `argparse`, `pathlib`, `sys`, `tempfile` — nothing to install. Catch
  `FileNotFoundError`, `FileExistsError`, and `sqlite3.Error` by name, never a
  bare `except:`, so a bug in your own code still crashes loudly instead of
  being mistaken for a handled error.

## Expected output

Run with **no arguments**, the shipped answer demonstrates itself in a
throwaway folder — create a database, back it up, refuse to clobber it, restore
it, and check the row counts match. Real stdout, captured on CPython 3.13.2:

```text
Demo run (no arguments): working in a throwaway folder.

Created tasks.db with 3 tasks.

-- backup tasks.db tasks.backup.db --
Backed up 3 pages to tasks.backup.db (4096 bytes/page).

-- backup tasks.db tasks.backup.db  (again, no --force) --
error: tasks.backup.db already exists (use --force to overwrite)
exit code would be: 1

-- restore tasks.backup.db restored.db --
Backed up 3 pages to restored.db (4096 bytes/page).
restored.db holds 3 tasks - same as the source.
```

## Steps

1. Write `copy_database`: guard the two refusals first (`FileNotFoundError`,
   `FileExistsError`), then open both connections.
2. Add a small progress callback and pass it to `src.backup(dst, progress=...)`.
   It is called after each batch of pages with `(status, remaining, total)`;
   stash `total` so you can report it.
3. Read `PRAGMA page_size` from the *destination* and print the progress line.
4. Wrap the two connection closes in a `finally` so a mid-copy error still
   closes them.
5. Build the `argparse` front end: two subparsers, `source`, `target`, and
   `--force`, and turn the two refusals into `error: ...` on stderr plus
   `return 1`.
6. Test it by hand: `backup` a small database, run the same command again and
   read the refusal, add `--force` and watch it overwrite, then `restore` into
   a fresh file and compare.

## The Solution

```python
"""problem-06-backup-restore-solution.py — snapshot a live SQLite database safely.

Two subcommands, exactly as the problem asks::

    python problem-06-backup-restore-solution.py backup  source.db backup.db
    python problem-06-backup-restore-solution.py restore backup.db target.db

Both use ``sqlite3.Connection.backup()``, never a file copy. The difference
matters: ``backup()`` copies the database page by page *through SQLite*, so
it takes the same locks any reader takes and produces a consistent snapshot
even while another process is writing. ``shutil.copy`` reads bytes off the
disk with no locks at all — catch it mid-transaction and the copy holds half
a write, which SQLite will later call a corrupt database.

Neither subcommand will overwrite an existing target unless ``--force`` is
passed, and any error exits non-zero.

Run with **no arguments** and it demonstrates itself in a throwaway folder:
create, back up, refuse to clobber, restore, verify. Nothing is left behind.
"""

import argparse
import sqlite3
import sys
import tempfile
from pathlib import Path
from typing import Final

DEMO_TASKS: Final[list[tuple[str, int]]] = [
    ("Finish quiz",                 2),
    ("Pet the cat",                 5),
    ("Review SQL injection notes",  1),
]


def copy_database(source: Path, target: Path, force: bool) -> int:
    """Snapshot `source` into `target` via Connection.backup(). Returns pages.

    Raises FileNotFoundError / FileExistsError for the two refusals, so the
    CLI layer can turn them into messages and exit codes.
    """
    if not source.exists():
        raise FileNotFoundError(f"{source} does not exist")
    if target.exists() and not force:
        raise FileExistsError(f"{target} already exists (use --force to overwrite)")

    pages_total = 0

    def note_progress(status: int, remaining: int, total: int) -> None:
        nonlocal pages_total
        pages_total = total

    src = sqlite3.connect(source)
    dst = sqlite3.connect(target)
    try:
        src.backup(dst, progress=note_progress)
        page_size = dst.execute("PRAGMA page_size").fetchone()[0]
    finally:
        dst.close()
        src.close()
    print(f"Backed up {pages_total} pages to {target.name} ({page_size} bytes/page).")
    return pages_total


def build_demo_db(path: Path) -> None:
    """A small tasks database to have something worth backing up."""
    conn = sqlite3.connect(path)
    try:
        with conn:
            conn.execute(
                "CREATE TABLE tasks ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "title TEXT NOT NULL, "
                "priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5))"
            )
            conn.executemany(
                "INSERT INTO tasks (title, priority) VALUES (?, ?)", DEMO_TASKS
            )
    finally:
        conn.close()


def task_count(path: Path) -> int:
    """How many tasks a database file holds."""
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    finally:
        conn.close()


def demo() -> int:
    """Create, back up, refuse, restore, verify — all in a temporary folder."""
    print("Demo run (no arguments): working in a throwaway folder.\n")
    with tempfile.TemporaryDirectory() as workspace:
        folder = Path(workspace)
        source = folder / "tasks.db"
        backup = folder / "tasks.backup.db"
        restored = folder / "restored.db"

        build_demo_db(source)
        print(f"Created {source.name} with {task_count(source)} tasks.")

        print("\n-- backup tasks.db tasks.backup.db --")
        copy_database(source, backup, force=False)

        print("\n-- backup tasks.db tasks.backup.db  (again, no --force) --")
        try:
            copy_database(source, backup, force=False)
        except FileExistsError:
            print(f"error: {backup.name} already exists (use --force to overwrite)")
            print("exit code would be: 1")

        print("\n-- restore tasks.backup.db restored.db --")
        copy_database(backup, restored, force=False)
        print(f"{restored.name} holds {task_count(restored)} tasks - "
              "same as the source.")
    return 0


def main(argv: list[str]) -> int:
    """Parse the CLI. No arguments at all runs the self-demonstration."""
    if not argv:
        return demo()

    parser = argparse.ArgumentParser(
        description="Back up and restore SQLite databases via Connection.backup()."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("backup", "snapshot a database into a new file"),
        ("restore", "copy a snapshot back out to a target file"),
    ):
        sub = commands.add_parser(name, help=help_text)
        sub.add_argument("source", type=Path)
        sub.add_argument("target", type=Path)
        sub.add_argument(
            "--force", action="store_true",
            help="overwrite the target if it already exists",
        )
    args = parser.parse_args(argv)

    try:
        copy_database(args.source, args.target, force=args.force)
    except (FileNotFoundError, FileExistsError, sqlite3.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

<!--@@INSERT:problem-06-backup-restore-solution.py@@-->

**Why it works.**

**One function does both jobs.** `backup` and `restore` are the same
operation — copy a whole SQLite database from one file to another — so
`copy_database(source, target, force)` is the only worker, and `main` just
maps whichever subcommand you typed onto it. "Restore" is a backup with the
source and target swapped; there is nothing extra to write.

**`src.backup(dst)` copies the database the safe way.** It walks the source a
page at a time and writes each page into the destination connection, holding
the ordinary SQLite locks as it goes. Because it works *through* the database
engine rather than reading the file behind its back, the copy is consistent
even if another process is writing to the source at the same time — the exact
thing `shutil.copy` cannot promise. The `progress` callback is called after
each batch with the number of pages left and the total, and stashing `total`
is how the script knows how big the database was.

**The two refusals are raised, not printed, deep in the worker.**
`copy_database` raises `FileNotFoundError` when the source is missing and
`FileExistsError` when the target is there without `--force`. It does not know
about exit codes or stderr — that is the CLI layer's job. `main` catches those
two plus `sqlite3.Error`, prints one `error:` line to stderr, and returns `1`.
Keeping the policy (how to report a failure) out of the mechanism (how to copy)
is why the same `copy_database` serves both subcommands and the self-demo
without change.

**The page size comes from the destination, after the copy.** `PRAGMA
page_size` asks SQLite how many bytes are in one page — 4096 by default — and
reading it from the freshly written `dst` proves the destination is a real,
openable database, not just a file that exists. Multiply pages by page size and
you have the database's size on disk, which is why the progress line reports
both numbers.

**No arguments runs a full rehearsal.** With an empty `argv`, `main` calls
`demo()`, which builds a three-row tasks database inside a
`tempfile.TemporaryDirectory`, backs it up, tries the same backup again to show
the refusal, restores it, and confirms the restored copy holds the same three
tasks. The temporary folder deletes itself on the way out, so the script proves
every path end to end and leaves nothing behind — which is exactly what lets
the course's test run it and check the output.

## Download and run

Download
[problem-06-backup-restore-solution.py](./problem-06-backup-restore-solution.py)
and run it:

```bash
python problem-06-backup-restore-solution.py
```

With no arguments it runs the self-demonstration above in a throwaway folder and
exits `0`, so it works on any machine with Python and needs nothing installed.
To use it for real, give it a subcommand:

```bash
python problem-06-backup-restore-solution.py backup tasks.db tasks.backup.db
python problem-06-backup-restore-solution.py restore tasks.backup.db restored.db
```

The `-solution` in the filename keeps this download from landing on top of the
`backup.py` you are writing yourself.

## Common bugs to catch

- **`sqlite3.OperationalError: database is locked` — but only sometimes.** You
  reached for `shutil.copy` and it *usually* worked, then failed under load.
  That is the whole point of the problem: a file copy is unsafe exactly when the
  database is busy, which is exactly when you most want a backup. Use
  `Connection.backup()` and the locking is handled for you.
- **The backup file is empty or 0 pages.** You called `backup()` on the wrong
  object — it is a method on the *source* connection, taking the destination as
  its argument: `src.backup(dst)`, not `dst.backup(src)`. Backwards, and you
  snapshot the empty new file over nothing.
- **It happily overwrites your only good backup.** You skipped the
  `FileExistsError` guard, or checked `force` with the wrong sense. Refuse when
  the target exists **and** `not force`; overwrite only when `--force` is
  present.
- **A failure still exits `0`.** You printed the error but forgot to
  `return 1` (and to `raise SystemExit(main(...))`). Cron and shell `&&` chains
  read the exit code, not your message, so a silent `0` tells them the backup
  succeeded when it did not.
- **`sqlite3.OperationalError: unable to open database file`.** The target's
  parent folder does not exist. `backup()` writes into a directory that must
  already be there; create it first, or point the target at one that exists.

## Under the hood

<details>
<summary>Under the hood — what "page by page" really means, and why it beats a file copy</summary>

A SQLite database is not a stream of bytes; it is an array of fixed-size
**pages**, 4096 bytes each by default. A table, an index, the schema itself —
all of it lives in numbered pages, and every change SQLite makes is a change to
one or more whole pages, wrapped in a transaction.

`Connection.backup()` copies those pages one batch at a time through the
running engine. Between batches it releases and re-takes its lock, so a writer
that needs the database can slip in, make its change, and hand control back —
and the backup notices, re-reading any page that changed underneath it. The
result is a copy that corresponds to a single consistent moment, never a mix of
"before" on page 5 and "after" on page 900.

`shutil.copy` has none of this. It reads the file's bytes in order with no idea
that a transaction is halfway through rewriting pages 5 and 900 together. Copy
page 5's old bytes and page 900's new bytes and you have a file that never
existed as a real database state — SQLite opens it and reports corruption. The
file copy is not *wrong*, it is *unsynchronised*, and on a database nobody is
writing to it happens to be fine. "Happens to be fine" is not a property you
want a backup tool to rely on.

</details>

<details>
<summary>Under the hood — the progress callback, and backing up to another live database</summary>

The `progress` callback exists because a large backup is not instant, and a
long-running tool should be able to show a bar. Its signature is
`(status, remaining, total)`: `remaining` counts down to zero as pages are
copied, `total` is the size of the job. The reference ignores `status` and
`remaining` and keeps only `total`, because all it wants is the final page
count — but `1 - remaining / total` is the fraction done, which is a progress
bar waiting to be drawn.

There is a second trick hiding in the API. `backup()` copies into any
destination *connection*, and that connection does not have to be a fresh file —
it can be `sqlite3.connect(":memory:")`. Backing a disk database up *into
memory* gives you a fast, throwaway working copy you can hammer with test
queries and discard, without touching the original. Backing memory back *out to
disk* is how a program that does all its work in RAM saves its state on exit.
Same method, both directions, which is the same symmetry that let one
`copy_database` serve both `backup` and `restore`.

</details>

## Acceptance checklist

- [ ] `backup <source> <target>` writes a snapshot using `Connection.backup()`.
- [ ] `restore <backup> <target>` does the same operation in reverse.
- [ ] Neither subcommand overwrites an existing target without `--force`.
- [ ] The progress line reports the page count and page size.
- [ ] A missing source, a refused overwrite, and a SQLite error each exit
      non-zero.
- [ ] No `shutil.copy` anywhere; the copy goes through `Connection.backup()`.
- [ ] The top-of-file docstring explains why `backup()` beats a file copy.

## Stretch

- **Add a progress bar.** Use the callback's `remaining` and `total` to print a
  percentage that updates as the copy runs. On a three-page database it flashes
  by; make a database with a few hundred thousand rows and watch it climb.
- **Back up into memory.** Add a `--memory` mode that restores a disk database
  into `sqlite3.connect(":memory:")`, runs a `SELECT COUNT(*)` against it, and
  reports the total — proving the in-memory copy is real without ever writing a
  second file.
- **Time it against `shutil.copy`.** Copy a large database both ways and time
  each. The file copy is often faster on an idle database — then start a writer
  in another process and watch the file copy start producing databases that
  will not open, while `backup()` keeps producing good ones. That contrast is
  the lesson made measurable.
- **Wire it into the mini-project.** Add a `tracker.py backup` subcommand that
  snapshots the tracker's own `tasks.db` before a risky bulk delete, so an
  `undo` is one restore away.

Next: the [mini-project](../mini-project/README.md) — the SQLite task tracker
that ties every idea from the week into one small program worth backing up.
