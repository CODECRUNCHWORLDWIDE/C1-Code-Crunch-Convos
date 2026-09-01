"""exercise-01-first-table-solution.py — connect, create, insert, select, print.

Builds a small coffee catalogue in a SQLite file called roastery.db and
prints the roasts that are currently in stock, most expensive first.

Your own exercise-01-first-table.py keeps roastery.db in the folder you run
it from, so you can reopen the file afterwards and poke at it. This shipped
answer runs the same code inside a throwaway temporary folder instead, so the
download can never collide with a database of yours and never leaves a file
behind. Every run is therefore a first run: fresh file, four inserts. The
four query functions are the whole exercise and know nothing about the
harness.

Run it with::

    python exercise-01-first-table-solution.py
"""

import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Final

DB_PATH: Final[str] = "roastery.db"

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS roasts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL UNIQUE,
    origin        TEXT    NOT NULL,
    price_per_bag REAL    NOT NULL CHECK (price_per_bag >= 0),
    in_stock      INTEGER NOT NULL DEFAULT 0
);
"""

SEED_ROWS: Final[list[tuple[str, str, float, int]]] = [
    ("Sunrise Blend",     "Colombia", 14.50, 12),
    ("Night Shift",       "Ethiopia", 17.25, 5),
    ("Cold Brew Base",    "Brazil",   12.00, 30),
    ("Decaf Quiet Hours", "Peru",     15.75, 0),
]

INSERT_ROAST: Final[str] = (
    "INSERT OR IGNORE INTO roasts (name, origin, price_per_bag, in_stock) "
    "VALUES (?, ?, ?, ?)"
)

SELECT_IN_STOCK: Final[str] = (
    "SELECT id, name, origin, price_per_bag FROM roasts "
    "WHERE in_stock > ? ORDER BY price_per_bag DESC"
)


def create_table(conn: sqlite3.Connection) -> None:
    """Create the roasts table if it does not already exist."""
    conn.execute(SCHEMA)


def seed(conn: sqlite3.Connection) -> int:
    """Insert SEED_ROWS and return how many rows were actually inserted."""
    cursor = conn.executemany(INSERT_ROAST, SEED_ROWS)
    return cursor.rowcount


def in_stock_rows(conn: sqlite3.Connection) -> list[tuple[int, str, str, float]]:
    """Return the in-stock roasts, most expensive first."""
    cursor = conn.execute(SELECT_IN_STOCK, (0,))
    return cursor.fetchall()


def total_count(conn: sqlite3.Connection) -> int:
    """Return the number of rows in the roasts table."""
    cursor = conn.execute("SELECT COUNT(*) FROM roasts")
    return cursor.fetchone()[0]


def main() -> None:
    """Open the database, build it, read it back, close it."""
    conn = sqlite3.connect(DB_PATH)
    try:
        print(f"Connected to {DB_PATH}")
        create_table(conn)
        print("Created table: roasts")
        inserted = seed(conn)
        print(f"Inserted {inserted} roasts.")
        conn.commit()

        rows = in_stock_rows(conn)
        print("\nIn stock, most expensive first:")
        for roast_id, name, origin, price in rows:
            print(f"{roast_id:>2}  {name:<18} {origin:<10} ${price:.2f}")
        print(f"\n{len(rows)} of {total_count(conn)} roasts are in stock.")
    finally:
        conn.close()
        print("Closed the connection.")


def run_in_throwaway_folder() -> None:
    """Run main() inside a temporary folder that is deleted afterwards.

    DB_PATH is relative, so the database lands in the current folder. Moving
    into a temporary folder first means this download builds its catalogue,
    prints it, and leaves your disk exactly as it found it.
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
