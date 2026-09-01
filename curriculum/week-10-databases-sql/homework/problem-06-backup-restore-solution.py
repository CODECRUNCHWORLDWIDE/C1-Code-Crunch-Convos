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
