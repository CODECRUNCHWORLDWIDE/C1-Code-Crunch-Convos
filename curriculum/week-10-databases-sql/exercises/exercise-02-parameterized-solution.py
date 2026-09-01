"""exercise-02-parameterized-solution.py — see SQL injection, then prevent it.

Runs against a throwaway local file, injection_demo.db, which this script
creates and destroys. Never point this technique at a system you do not own.

Your own exercise-02-parameterized.py keeps injection_demo.db in the folder
you run it from and asks you to delete it afterwards. This shipped answer
runs the same code inside a temporary folder that is deleted on the way out,
so the deletion step is built in. The lookups are the whole exercise and know
nothing about the harness.

Run it with::

    python exercise-02-parameterized-solution.py
"""

import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Final

DB_PATH: Final[str] = "injection_demo.db"

SCHEMA: Final[str] = """
DROP TABLE IF EXISTS members;
CREATE TABLE members (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    secret_code TEXT NOT NULL
);
"""

MEMBERS: Final[list[tuple[str, str, str]]] = [
    ("Ada Lovelace",      "ada@example.com",       "CC-1001"),
    ("Grace Hopper",      "grace@example.com",     "CC-1002"),
    ("Alan Turing",       "alan@example.com",      "CC-1003"),
    ("Katherine Johnson", "katherine@example.com", "CC-1004"),
]

HOSTILE_INPUT: Final[str] = "' OR '1'='1"
DROP_ATTEMPT: Final[str] = "'; DROP TABLE members; --"


def seed(conn: sqlite3.Connection) -> None:
    """Rebuild the demo table from scratch and insert the four members."""
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO members (name, email, secret_code) VALUES (?, ?, ?)",
        MEMBERS,
    )
    conn.commit()


def unsafe_lookup(conn: sqlite3.Connection, name: str) -> list[tuple[int, str, str]]:
    """Look up a member the wrong way. Never write this in real code.

    Builds the query by string formatting, so the caller's text becomes
    part of the SQL instead of staying a value.
    """
    query: str = f"SELECT id, name, email FROM members WHERE name = '{name}'"
    print(f"Query sent: {query}")
    return conn.execute(query).fetchall()


def safe_lookup(conn: sqlite3.Connection, name: str) -> list[tuple[int, str, str]]:
    """Look up a member the right way, with a bound parameter."""
    query: Final[str] = "SELECT id, name, email FROM members WHERE name = ?"
    print(f"Query sent: {query}")
    print(f'Parameter: "{name}"')
    return conn.execute(query, (name,)).fetchall()


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    """Return True if a table with this name is in the schema."""
    cursor = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?",
        ("table", table),
    )
    return cursor.fetchone()[0] > 0


def show(rows: list[tuple[int, str, str]]) -> None:
    """Print a row count and then each row."""
    print(f"{len(rows)} row(s) returned.")
    for row in rows:
        print(f"  {row}")


def main() -> None:
    """Run the same two inputs through the broken and the fixed lookup."""
    conn = sqlite3.connect(DB_PATH)
    try:
        seed(conn)
        print(f"Seeded {DB_PATH} with {len(MEMBERS)} members.")

        print("\n--- Unsafe lookup: normal input ---")
        show(unsafe_lookup(conn, "Ada Lovelace"))

        print("\n--- Unsafe lookup: hostile input ---")
        show(unsafe_lookup(conn, HOSTILE_INPUT))
        print("The whole table leaked. One quote did that.")

        print("\n--- Safe lookup: same hostile input, ? placeholder ---")
        show(safe_lookup(conn, HOSTILE_INPUT))
        print("Nothing matched, because the input was treated as a name, not as SQL.")

        print("\n--- Multi-statement attempt through execute() ---")
        try:
            unsafe_lookup(conn, DROP_ATTEMPT)
        except sqlite3.ProgrammingError as exc:
            print(f"sqlite3.ProgrammingError: {exc}")
        print("execute() refuses a second statement. That is a seatbelt, not a fix:")
        print("the leak above needed only one statement.")

        print(f"\nmembers table still present: {table_exists(conn, 'members')}")
    finally:
        conn.close()


def run_in_throwaway_folder() -> None:
    """Run main() inside a temporary folder that is deleted afterwards.

    DB_PATH is relative, so the demo database lands in the current folder.
    Moving into a temporary folder first means the file this attack runs
    against is created for the run and destroyed with it.
    """
    keep = Path.cwd()
    with tempfile.TemporaryDirectory() as workspace:
        os.chdir(workspace)
        try:
            main()
        finally:
            os.chdir(keep)


if __name__ == "__main__":
    run_in_throwaway_folder()
