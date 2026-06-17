"""Exercise 04 — GROUP BY and aggregate functions.

Goal
----
Build a `sales` table, then write SQL that groups sales by category and
shows for each category: number of sales, total revenue, average sale,
and the most recent sale date.

Run it
------
    python exercise-04-aggregate.py

Stretch
-------
* Add a HAVING clause that keeps only categories with total revenue > 100.
* Order the result by total revenue descending.
* Add a second GROUP BY column (`category, region`) and watch how the
  result expands.

Docs
----
SQLite aggregate functions: https://www.sqlite.org/lang_aggfunc.html
"""

from __future__ import annotations

import sqlite3
from typing import Final

DB_PATH: Final[str] = "exercise-04.db"


def setup(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS sales;
        CREATE TABLE sales (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT    NOT NULL,
            amount   REAL    NOT NULL CHECK (amount >= 0),
            sold_on  TEXT    NOT NULL                  -- ISO-8601 date
        );
        """
    )

    rows: list[tuple[str, float, str]] = [
        ("Books",       19.99, "2026-05-01"),
        ("Books",       32.50, "2026-05-02"),
        ("Books",       14.00, "2026-05-09"),
        ("Electronics", 199.00, "2026-05-03"),
        ("Electronics", 349.00, "2026-05-08"),
        ("Toys",         24.99, "2026-05-04"),
        ("Toys",         11.50, "2026-05-07"),
        ("Toys",         11.50, "2026-05-12"),
        ("Snacks",        3.25, "2026-05-05"),
        ("Snacks",        4.75, "2026-05-06"),
    ]
    conn.executemany(
        "INSERT INTO sales (category, amount, sold_on) VALUES (?, ?, ?)",
        rows,
    )


def totals_per_category(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Aggregate the sales table by category."""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  category,
                COUNT(*)        AS num_sales,
                SUM(amount)     AS total_revenue,
                AVG(amount)     AS avg_sale,
                MAX(sold_on)    AS latest_sale
        FROM    sales
        GROUP BY category
        ORDER BY total_revenue DESC
        """
    )
    return cursor.fetchall()


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        setup(conn)
        rows = totals_per_category(conn)

        print(f"{'Category':<14}{'Sales':>6}{'Total':>12}{'Avg':>10}  Latest")
        print("-" * 50)
        for row in rows:
            print(
                f"{row['category']:<14}"
                f"{row['num_sales']:>6}"
                f"{row['total_revenue']:>12.2f}"
                f"{row['avg_sale']:>10.2f}  "
                f"{row['latest_sale']}"
            )


if __name__ == "__main__":
    main()
