"""Exercise 01 — Your first SQLite table.

Goal
----
Open a SQLite database, create a `books` table, insert three rows,
select them all, and print each row.

Run it
------
    python exercise-01-first-table.py

What you'll see
---------------
The script prints the three rows you inserted, one per line.

Notes
-----
* Re-running the script will keep adding the same three rows because
  `INSERT` is unconditional. Delete `exercise-01.db` to start fresh, or
  swap in `INSERT OR IGNORE` once you understand `UNIQUE` constraints.
* All values flow through `?` placeholders — no f-strings into SQL.

Docs
----
Python sqlite3: https://docs.python.org/3/library/sqlite3.html
"""

from __future__ import annotations

import sqlite3
from typing import Final

DB_PATH: Final[str] = "exercise-01.db"


def create_table(conn: sqlite3.Connection) -> None:
    """Create the `books` table if it does not already exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            title  TEXT NOT NULL,
            author TEXT NOT NULL,
            year   INTEGER
        )
        """
    )


def insert_books(conn: sqlite3.Connection) -> None:
    """Insert three sample books using a parameterized query."""
    books: list[tuple[str, str, int]] = [
        ("The Pragmatic Programmer", "Hunt & Thomas", 1999),
        ("Code Complete",            "Steve McConnell", 2004),
        ("Clean Code",               "Robert Martin",  2008),
    ]
    # `executemany` runs the same INSERT for every tuple in the list.
    conn.executemany(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        books,
    )


def fetch_all_books(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return every row from `books`, ordered by id."""
    conn.row_factory = sqlite3.Row     # so we can access columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, year FROM books ORDER BY id")
    return cursor.fetchall()


def main() -> None:
    # `with sqlite3.connect(...)` commits on success, rolls back on exception.
    with sqlite3.connect(DB_PATH) as conn:
        create_table(conn)
        insert_books(conn)

        rows = fetch_all_books(conn)
        print(f"Found {len(rows)} books:")
        for row in rows:
            print(f"  [{row['id']:>3}] {row['title']!r} by {row['author']} ({row['year']})")


if __name__ == "__main__":
    main()
