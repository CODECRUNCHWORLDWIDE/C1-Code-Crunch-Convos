# Exercise 4 — Aggregating Sales

> **Topic:** `GROUP BY` with `COUNT`, `SUM` and `AVG`, plus a `HAVING` filter on a bound parameter
> **Lecture:** [02 — JOINs and Aggregations](../lecture-notes/02-joins-and-aggregations.md), sections 6–9
> **Difficulty:** Medium
> **Target time:** 30 minutes
> **Why this one:** aggregation is the difference between a database that stores answers and a database that *computes* them. Pull ten rows into Python and total them in a loop and you have written the query the slow way; at ten million rows that loop is a crash and the `GROUP BY` is still a query. This is also where the `WHERE` versus `HAVING` distinction lands, and it is the single most reliable place to lose points on the quiz.

## The Brief

A small hardware reseller has ten sales on the books for April. Each row
records the day, the region, the product, how many units went out, and the
price per unit. Nobody wants to read ten rows. They want three numbers per
region and three per product.

The interesting column is the one that is not in the table: **revenue**.
Nowhere does the schema store the money. Revenue is `units * unit_price`,
computed at query time. This is deliberate — storing a total that can be
derived means storing a number that can disagree with the numbers it came
from.

You will produce a regional report sorted by revenue, a product report, and
one `HAVING` query that keeps only the regions clearing a threshold you pass
in as a parameter.

## Starter

Create `exercise-04-aggregate.py` in your practice repo.

```python
"""exercise-04-aggregate.py — GROUP BY totals over a sales table.

Summarises ten April sales by region and by product, then filters the
regional groups with HAVING.
"""

import sqlite3
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
    # TODO: executemany with five ? placeholders
    conn.commit()


def by_region(conn: sqlite3.Connection) -> list[tuple[str, int, int, float, float]]:
    """Return (region, orders, units, revenue, avg_order) per region.

    Ordered by revenue, largest first.
    """
    # TODO: SELECT region,
    #              COUNT(*)                 AS orders,
    #              SUM(units)               AS units,
    #              SUM(units * unit_price)  AS revenue,
    #              AVG(units * unit_price)  AS avg_order
    #       FROM sales GROUP BY region ORDER BY revenue DESC
    return []


def by_product(conn: sqlite3.Connection) -> list[tuple[str, int, float]]:
    """Return (product, units, revenue) per product, best revenue first."""
    # TODO: the same shape, grouped by product
    return []


def regions_above(conn: sqlite3.Connection, threshold: float) -> list[tuple[str, float]]:
    """Return (region, revenue) for regions whose revenue clears `threshold`."""
    # TODO: GROUP BY region HAVING SUM(units * unit_price) >= ?
    #       The threshold is a bound parameter.
    return []


def total_revenue(conn: sqlite3.Connection) -> float:
    """Return the revenue of every sale added together."""
    # TODO: SELECT SUM(units * unit_price) FROM sales
    return 0.0


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


if __name__ == "__main__":
    main()
```

## Requirements

1. `by_region` returns exactly three rows — `North`, `East`, `South` — in
   that order, because that is descending revenue.
2. `orders` is `COUNT(*)`, the number of sale rows in the group. `units` is
   `SUM(units)`, the number of items. They are different questions and the
   North group answers them `4` and `10`.
3. Revenue is computed in SQL as `SUM(units * unit_price)`. Do not fetch
   rows and multiply them in Python.
4. `avg_order` is `AVG(units * unit_price)` — the average revenue of one
   sale in that group. It is not `revenue / SUM(units)`.
5. `regions_above` filters with `HAVING`, not `WHERE`, and binds the
   threshold as `?`. With `500.00` it returns `North` and `East`.
6. `total_revenue` returns `2115.0`, and the per-region and per-product
   revenues each add up to it. Check both — that is your arithmetic proof.
7. The columns line up exactly as shown in the Expected output. The format
   strings in `main` are given; do not change the widths.

## Constraints

- **Aggregate in SQL, not in Python.** A `SELECT *` plus a `for` loop with a
  running total produces the same three numbers today. It also drags every
  row across the process boundary, which is fine for ten rows and fatal for
  ten million. The database was built to do this, and it will do it in one
  pass over the data.
- **Use `HAVING` for the threshold, never `WHERE`.** `WHERE` runs before
  grouping, so the aggregate does not exist yet and `WHERE SUM(...) >= ?`
  raises `misuse of aggregate function SUM()`. `HAVING` runs after. The
  short version: `WHERE` filters rows, `HAVING` filters groups.
- **Name every non-aggregated column in `GROUP BY`.** SQLite lets you get
  away with omitting one and quietly hands you an arbitrary row's value.
  PostgreSQL rejects the same query outright. Write it correctly here and
  the query ports without edits.
- **Do not store a `revenue` column, and do not round in SQL.** Revenue is
  derivable from `units` and `unit_price`; a stored copy is a second source
  of truth that goes stale the first time someone corrects a price. Format
  at print time with `:.2f` — rounding inside the aggregate rounds every
  group separately, and rounded parts stop adding up to the rounded whole.
- **Every value that varies goes through `?`.** The threshold is a constant
  in your file today and a form field next month. Note that `HAVING` accepts
  a parameter just like `WHERE` does.
- **Commit after seeding, and close in a `finally`.** `sqlite3` opens the
  transaction for your inserts and never closes it. With no commit, closing
  the connection throws the ten rows away silently — every total prints as
  `None` or the loop prints nothing at all, and there is no traceback
  pointing at the real cause.

## Expected output

```text
$ python exercise-04-aggregate.py
Seeded sales.db with 10 sales.

Region   Orders  Units     Revenue   Avg order
North         4     10      915.00      228.75
East          3     10      885.00      295.00
South         3      4      315.00      105.00

Product     Units     Revenue
monitor         7     1260.00
keyboard       11      495.00
headset         6      360.00

Total revenue: $2115.00

Regions with at least $500.00 in revenue:
  North  $915.00
  East   $885.00
```

Look at `North` and `East`: both moved 10 units, but North did it across
four orders and East across three, and East's revenue is lower. Unit count
and revenue are not the same ranking, which is the entire reason the report
carries both columns. The same trap is in the product table — `keyboard`
sells the most units and earns the least money.

## Steps

1. Create the file and fill in `seed`. Run it and confirm the seeded line.
2. Before writing `by_region`, open the shell — `python -m sqlite3 sales.db`
   — and run `SELECT region, SUM(units * unit_price) FROM sales GROUP BY
   region;` by hand. Getting the SQL right in the shell first is faster than
   debugging it through Python.
3. Fill in `by_region` and compare your three rows with the expected block,
   column alignment included.
4. Fill in `by_product` and `total_revenue`. Add the three product revenues
   on paper: 1260 + 495 + 360. If it is not 2115, one group is wrong.
5. Fill in `regions_above` with `HAVING`. Then change it to `WHERE` on
   purpose, run it, and read the error. That message is the one you want to
   recognise instantly on the quiz.
6. Change `THRESHOLD` to `300.00` and rerun — all three regions should
   appear. Set it back, delete `sales.db`, and run clean.

## The Solution

```python
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
```

**Why it works.**

**`GROUP BY` deals the rows into piles, and each aggregate is one number
per pile.** Picture the ten sales slips going onto the table, one pile per
region. `GROUP BY region` makes the piles. `COUNT(*)` counts the slips in a
pile. `SUM(units)` runs down a column and adds it up. `SUM(units *
unit_price)` multiplies each slip first and then adds. One row comes back
per pile — never one per slip.

**Revenue is computed, never stored.** The `sales` table holds `units` and
`unit_price` and no money column at all. `units * unit_price` runs on each
row as the query passes over it, and `SUM` totals those products. So a
price lives in exactly one place. Correct a price and every report that
mentions it is right on the very next run, because nothing was ever copied
anywhere to go stale.

**`COUNT(*)` and `SUM(units)` are different questions.** North reports `4`
and `10`: four sales happened, ten items went out of the door. Those read
like the same fact and are not. East moved ten units too, across three
orders, and earned less money for them. Units sold and money earned rank
the regions differently, which is the whole reason the report carries both
columns instead of the one that sounds good.

**`HAVING` filters piles; `WHERE` filters slips.** SQL works in an order:
pick the rows (`WHERE`), deal them into piles (`GROUP BY`), work out each
pile's numbers, then throw away whole piles (`HAVING`). Writing `WHERE
SUM(...) >= ?` asks for a pile's total at a moment when no pile exists yet,
which is why SQLite answers `misuse of aggregate function SUM()`. The same
condition in `HAVING` is asked after the totals are known, and it works.

**The threshold binds with `?` even inside `HAVING`.** `regions_above`
passes `(threshold,)` beside the query, just as `WHERE` would. People
expect `?` in a `WHERE` and are surprised it is allowed here; it is,
because a bound parameter is a slot for a value and `HAVING` compares
values like everything else. That number is a constant in your file today
and a box on a form next month.

**`HAVING` repeats the expression rather than the alias.** The query says
`HAVING SUM(units * unit_price) >= ?`, not `HAVING revenue >= ?`. SQLite
would accept the alias; PostgreSQL rejects it, because the alias is not
created until after `HAVING` has run. Writing the expression out twice
costs a few words now and saves a rewrite the day the project moves to a
different database. An alias in `ORDER BY` is fine everywhere, which is why
`ORDER BY revenue DESC` stays.

**Nothing rounds until it is printed.** No `ROUND` appears in any query.
`total_revenue` hands back `2115.0` and the `:.2f` in the f-strings decides
how it looks on screen. Round inside each `SUM` instead and every group
gets rounded on its own, and rounded parts stop adding up to the rounded
whole. A report whose column does not match its own total is nearly always
this bug.

**The shipped answer runs in a throwaway folder.** `DB_PATH` is
`"sales.db"` with no folder in front of it, so the database lands wherever
you are standing. `run_in_throwaway_folder` steps into a temporary
directory, calls `main`, and steps back out so the directory can be
deleted. Your own `exercise-04-aggregate.py` should not do this — you want
`sales.db` left behind so you can rerun the `GROUP BY` in the SQLite shell
and check it by hand.

## Download and run

Download [exercise-04-aggregate-solution.py](./exercise-04-aggregate-solution.py)
and run it:

```bash
python exercise-04-aggregate-solution.py
```

Nothing to install — `sqlite3` comes with Python. It seeds the ten sales,
prints both reports, the total and the `HAVING` filter, then takes its
database with it on the way out, so your folder is left untouched.

Your own file is `exercise-04-aggregate.py`. The `-solution` suffix is what
keeps the shipped answer from overwriting it.

## Common bugs to catch

- **`sqlite3.OperationalError: misuse of aggregate function SUM()`.** You
  put the aggregate in `WHERE`. Move it to `HAVING`.
- **`North` reports 10 orders instead of 4.** You wrote `COUNT(units)` or
  `SUM(units)` where `orders` should be `COUNT(*)`. Counting rows and adding
  a column are different operations that happen to be equal when every row
  has one unit — which is never.
- **Every region shows the same revenue.** The `GROUP BY` is missing, so
  SQLite collapsed the whole table into one group and paired the total with
  whichever `region` value it happened to be holding. One row out of a query
  you expected to return three is the tell.
- **Revenue comes back as `None`.** The table is empty — you forgot the
  commit, or `seed` still has only its `TODO` comments. `SUM` over zero rows
  is `NULL`, which arrives in Python as `None`, and then `:.2f` raises
  `TypeError: unsupported format string passed to NoneType.__format__`.
- **`avg_order` for North is `91.50` instead of `228.75`.** You averaged the
  wrong thing — `AVG(units * unit_price)` averages the ten sales, one group
  at a time. Dividing revenue by units answers "average price per item", a
  different question with a different name.
- **`sqlite3.OperationalError: no such column: revenue`.** You referenced a
  `SELECT` alias somewhere the database will not accept it. SQLite is
  generous about this and PostgreSQL is not, so the portable habit is to
  repeat the expression rather than the alias inside `HAVING`:
  `HAVING SUM(units * unit_price) >= ?`. An alias in `ORDER BY` is fine
  everywhere.
- **`ValueError: not enough values to unpack (expected 5, got 4)`.** Your
  `by_region` query selects four columns and `main` unpacks five. The
  `SELECT` list and the loop variables are one contract in two places.

## Acceptance checklist

- [ ] Three region rows print in the order `North`, `East`, `South`.
- [ ] `orders` and `units` differ for North (4 and 10), and you can explain why.
- [ ] Region revenues and product revenues each sum to `2115.00`.
- [ ] The threshold filter uses `HAVING` with a `?` parameter and returns North and East.
- [ ] No revenue is computed in a Python loop.
- [ ] Seeding commits, and the connection closes in a `finally` block.
- [ ] The file is committed to Git with a message like `Add Week 10 exercise 4: GROUP BY sales report`.

## Stretch

- Add `MIN(units * unit_price)` and `MAX(units * unit_price)` columns to the
  regional report to see the spread inside each group.
- Group by two columns at once — `GROUP BY region, product` — and read the
  nine rows that come back. Work out which three region/product pairs are
  missing from the data and why they are absent rather than zero.
- Add a `WHERE sold_on >= ?` clause alongside the `HAVING`, then trace which
  runs first. Filtering to sales from the 5th onward changes every group
  total; predict the new North revenue before you run it.

Last one for the week, and the first that needs an install:
[Exercise 5 — The Same Table with SQLAlchemy](./exercise-05-sqlalchemy-basic.md).
