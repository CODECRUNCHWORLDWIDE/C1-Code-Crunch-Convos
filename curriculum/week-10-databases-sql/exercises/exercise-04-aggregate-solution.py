"""exercise-04-aggregate-solution.py — GROUP BY totals over a sales table.

Summarises ten April sales by region and by product, then filters the
regional groups with HAVING.

Your own exercise-04-aggregate.py keeps sales.db in the folder you run it
from, so you can rerun the queries in the SQLite shell. This shipped answer
runs the same code inside a throwaway temporary folder instead, so the
download never collides with a database of yours and never leaves a file
behind. The four query functions are the whole exercise and know nothing
about the harness.

Run it with::

    python exercise-04-aggregate-solution.py
"""

import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Final

DB_PATH: Final[str] = "sales.db"

SCHEMA: Final[str] = """
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    sold_on    TEXT    NOT NULL,
    region     TEXT    NOT NULL,
    product    TEXT    NOT NULL,
    units      INTEGER NOT NULL CHECK (units > 0),
    unit_price REAL    NOT NULL CHECK (unit_price >= 0)
);
"""

SALES: Final[list[tuple[str, str, str, int, float]]] = [
    ("2026-04-02", "North", "keyboard", 3,  45.00),
    ("2026-04-02", "South", "keyboard", 1,  45.00),
    ("2026-04-03", "North", "monitor",  2, 180.00),
    ("2026-04-04", "East",  "keyboard", 5,  45.00),
    ("2026-04-05", "South", "monitor",  1, 180.00),
    ("2026-04-05", "North", "headset",  4,  60.00),
    ("2026-04-08", "East",  "headset",  2,  60.00),
    ("2026-04-09", "South", "keyboard", 2,  45.00),
    ("2026-04-10", "North", "monitor",  1, 180.00),
    ("2026-04-11", "East",  "monitor",  3, 180.00),
]

THRESHOLD: Final[float] = 500.00


def seed(conn: sqlite3.Connection) -> None:
    """Rebuild the sales table and insert the April rows."""
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO sales (sold_on, region, product, units, unit_price) "
        "VALUES (?, ?, ?, ?, ?)",
        SALES,
    )
    conn.commit()


def by_region(conn: sqlite3.Connection) -> list[tuple[str, int, int, float, float]]:
    """Return (region, orders, units, revenue, avg_order) per region.

    Ordered by revenue, largest first.
    """
    cursor = conn.execute(
        """
        SELECT region,
               COUNT(*)                AS orders,
               SUM(units)              AS units,
               SUM(units * unit_price) AS revenue,
               AVG(units * unit_price) AS avg_order
        FROM sales
        GROUP BY region
        ORDER BY revenue DESC
        """
    )
    return cursor.fetchall()


def by_product(conn: sqlite3.Connection) -> list[tuple[str, int, float]]:
    """Return (product, units, revenue) per product, best revenue first."""
    cursor = conn.execute(
        """
        SELECT product,
               SUM(units)              AS units,
               SUM(units * unit_price) AS revenue
        FROM sales
        GROUP BY product
        ORDER BY revenue DESC
        """
    )
    return cursor.fetchall()


def regions_above(conn: sqlite3.Connection, threshold: float) -> list[tuple[str, float]]:
    """Return (region, revenue) for regions whose revenue clears `threshold`."""
    cursor = conn.execute(
        """
        SELECT region,
               SUM(units * unit_price) AS revenue
        FROM sales
        GROUP BY region
        HAVING SUM(units * unit_price) >= ?
        ORDER BY revenue DESC
        """,
        (threshold,),
    )
    return cursor.fetchall()


def total_revenue(conn: sqlite3.Connection) -> float:
    """Return the revenue of every sale added together."""
    cursor = conn.execute("SELECT SUM(units * unit_price) FROM sales")
    total: float | None = cursor.fetchone()[0]
    return 0.0 if total is None else float(total)


def main() -> None:
    """Seed the sales table and print the three reports."""
    conn = sqlite3.connect(DB_PATH)
    try:
        seed(conn)
        print(f"Seeded {DB_PATH} with {len(SALES)} sales.\n")

        print(f"{'Region':<8}{'Orders':>7}{'Units':>7}{'Revenue':>12}{'Avg order':>12}")
        for region, orders, units, revenue, avg_order in by_region(conn):
            print(f"{region:<8}{orders:>7}{units:>7}{revenue:>12.2f}{avg_order:>12.2f}")

        print(f"\n{'Product':<10}{'Units':>7}{'Revenue':>12}")
        for product, units, revenue in by_product(conn):
            print(f"{product:<10}{units:>7}{revenue:>12.2f}")

        print(f"\nTotal revenue: ${total_revenue(conn):.2f}")

        print(f"\nRegions with at least ${THRESHOLD:.2f} in revenue:")
        for region, revenue in regions_above(conn, THRESHOLD):
            print(f"  {region:<7}${revenue:.2f}")
    finally:
        conn.close()


def run_in_throwaway_folder() -> None:
    """Run main() inside a temporary folder that is deleted afterwards.

    DB_PATH is relative, so the database lands in the current folder. Moving
    into a temporary folder first means this download builds its reports and
    leaves your disk exactly as it found it.
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
