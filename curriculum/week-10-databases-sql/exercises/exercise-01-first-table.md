# Exercise 1 — Your First Table

> **Topic:** Connect to SQLite from Python, create a table, insert rows, select them back, print
> **Lecture:** [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md) (sections 1–4), with the SQL itself from [01 — Relational Databases & SQL](../lecture-notes/01-relational-databases-and-sql.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** every other database thing you will ever do sits on top of this five-step loop — connect, create, write, read, close. If the loop is shaky, the joins in Exercise 3 and the ORM in Exercise 5 will feel like magic instead of like SQL. Do it once slowly here and the rest of the week is just variations.

## The Brief

A neighbourhood coffee roaster keeps their catalogue in a spreadsheet that
two people edit at once, which goes about as well as you would expect. You
are going to replace it with a real table in a real database file — a
single file called `roastery.db`, created the first time you connect. No
server, no configuration, no account.

Think of a database as a filing cabinet and a table as one drawer in it,
with every folder in that drawer holding the same kind of card. Our drawer
holds roast cards: a name, where the beans came from, the price of a bag,
and how many bags are on the shelf. The one question the roaster asks it
every morning is *"what can I sell today, most expensive first?"* — so that
is the query you will write. Notice that this is not "show me everything". A
row with zero bags in stock is real data that must stay in the table and
stay out of that answer.

## Starter

Create `exercise-01-first-table.py` in your practice repo and paste this in.
Fill in the `TODO`s.

```python
"""exercise-01-first-table.py — connect, create, insert, select, print.

Builds a small coffee catalogue in a SQLite file called roastery.db and
prints the roasts that are currently in stock, most expensive first.
"""

import sqlite3
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


def create_table(conn: sqlite3.Connection) -> None:
    """Create the roasts table if it does not already exist."""
    # TODO: run SCHEMA with conn.execute(...)


def seed(conn: sqlite3.Connection) -> int:
    """Insert SEED_ROWS and return how many rows were actually inserted."""
    # TODO: one executemany with "INSERT OR IGNORE INTO roasts
    #       (name, origin, price_per_bag, in_stock) VALUES (?, ?, ?, ?)"
    # TODO: return the cursor's rowcount
    return 0


def in_stock_rows(conn: sqlite3.Connection) -> list[tuple[int, str, str, float]]:
    """Return the in-stock roasts, most expensive first."""
    # TODO: SELECT id, name, origin, price_per_bag FROM roasts
    #       WHERE in_stock > ? ORDER BY price_per_bag DESC
    #       Pass 0 as a parameter, not as text inside the query.
    return []


def total_count(conn: sqlite3.Connection) -> int:
    """Return the number of rows in the roasts table."""
    # TODO: SELECT COUNT(*) FROM roasts, then pull the single value out
    #       of the single row that comes back.
    return 0


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


if __name__ == "__main__":
    main()
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-10-databases-sql/exercises/exercise-01-first-table.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `create_table` runs the `SCHEMA` string exactly as given. Do not drop the
   `IF NOT EXISTS`, and do not retype the SQL inline.
2. `seed` uses a single `executemany` call with four `?` placeholders and
   returns `cursor.rowcount`. On a fresh database that is `4`; on a second
   run it is `0`, because `INSERT OR IGNORE` skips the duplicate names.
3. `in_stock_rows` returns only roasts with `in_stock` greater than zero,
   ordered by `price_per_bag` descending. `Decaf Quiet Hours` has zero bags
   and must not appear. The threshold is passed as a parameter — the SQL
   text ends in `in_stock > ?` and the value `0` travels in the tuple.
4. `total_count` returns `4`, counting every row including the out-of-stock
   one. `fetchone()` gives you a one-element tuple; index it.
5. The output lines match the format in the Expected output section exactly,
   including the two spaces after the id and the `$` with two decimals.

## Constraints

- **Use `?` placeholders for every value, even the ones you typed yourself.**
  You know `0` is safe today. The habit is what protects you on the day the
  value comes from a web form instead of from your own source file, and
  habits do not form on the days you make exceptions. Exercise 2 shows what
  the exception costs.
- **Call `conn.commit()` before you read, and `conn.close()` in a `finally`
  block.** `sqlite3` opens a transaction for you before an `INSERT` but
  never ends one. Skip the commit, close the connection, and those four
  rows are rolled back and thrown away — no error, no warning, no
  traceback. The script prints "Inserted 4 roasts", exits cheerfully, and
  the file on disk is empty. That silence is why this is the most common
  database bug of the week. The confusing part: `sqlite3` opens transactions
  only for `INSERT`, `UPDATE`, `DELETE` and `REPLACE`, not for
  `CREATE TABLE`, so what you are left with is a table that exists and is
  empty — which looks like a broken `INSERT` rather than a missing commit.
- **Use `executemany` for the four rows, not a `for` loop of `execute`.**
  Four rows will not measure differently. Forty thousand will, and this is
  the shape you want in your fingers by then.
- **Standard library only, and no `.db` file in Git.** `sqlite3` ships with
  Python; nothing to install until Exercise 5. Add `*.db` to your
  `.gitignore` now — a database file is generated binary output and will
  conflict on every merge.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-first-table.py
Connected to roastery.db
Created table: roasts
Inserted 4 roasts.

In stock, most expensive first:
 2  Night Shift        Ethiopia   $17.25
 1  Sunrise Blend      Colombia   $14.50
 3  Cold Brew Base     Brazil     $12.00

3 of 4 roasts are in stock.
Closed the connection.
```

Three roasts print, not four: `Decaf Quiet Hours` has zero bags, so the
`WHERE in_stock > ?` filter leaves it out — but the summary line still counts
it, because `total_count` counts every row. That gap between "3" and "4" is
the whole point of keeping the out-of-stock row in the table.

Run *your own* `exercise-01-first-table.py` a second time without deleting the
file, and everything is the same except one line — the line that is the point
of `INSERT OR IGNORE`:

```text
Inserted 0 roasts.
```

The four names are already there, and each is `UNIQUE`, so the second insert
is skipped rather than refused with an error. The shipped answer always prints
`Inserted 4 roasts.` because it builds its database in a fresh throwaway
folder every run — more on that below.

## Steps

1. Activate your virtual environment, change into your practice folder,
   create the file, and run it before filling in a single `TODO`. It should
   print the connect line, an empty listing, and `0 of 0 roasts are in
   stock.` Starting from a script that runs is easier than starting from
   one that does not.
2. Fill in `create_table` and rerun. Nothing visible changes — that is
   expected. Confirm the table exists: `python -m sqlite3 roastery.db`, then
   type `.schema` and `.exit`.
3. Fill in `seed` and rerun. You should see `Inserted 4 roasts.`
4. Fill in `in_stock_rows` and `total_count`. Compare your three lines,
   character for character, with the Expected output block.
5. Now delete the commit: comment out `conn.commit()`, delete `roastery.db`,
   and run it twice. Watch what happens, because it is not what you expect.
   Both runs print exactly the same thing — `Inserted 4 roasts.` and
   `3 of 4 roasts are in stock.` — every single time. **The program never
   notices anything is wrong.** It reads back its own rows through the same
   connection that wrote them, and a connection can always see its own
   uncommitted work.

   The loss only shows up from outside. With the program finished, open the
   file yourself and count:

   ```bash
   python -c "import sqlite3;print(sqlite3.connect('roastery.db').execute('SELECT COUNT(*) FROM roasts').fetchone()[0])"
   ```

   It prints `0`. Four rows went in, the program read all four back, and
   nothing was kept. Put the commit back. This is the shape of the bug you
   have to watch for: it is silent from the inside, and a test that checks the
   program's own output will pass while the data quietly goes nowhere.
6. Delete `roastery.db` one last time and run clean.

## The Solution

```python
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
```

**The five-step loop is the whole exercise.** Read `main` top to bottom and
you can say it in one breath: connect to the file, create the table, write
the rows, commit, read them back, close. Every database program you write
this week is a longer version of exactly this shape.

**`create_table` hands SQLite one string and lets it do the work.** The
`SCHEMA` text says what a roast card looks like — a name that cannot be blank
and cannot repeat (`NOT NULL UNIQUE`), a price that cannot be negative
(`CHECK (price_per_bag >= 0)`), and a stock count that starts at zero
(`DEFAULT 0`). Those rules live in the database, not in your Python, so they
hold no matter who writes to the table later. `IF NOT EXISTS` means running
the program twice does not error on the second create.

**`seed` writes four rows with one call.** `executemany` takes the query once
and the list of rows once, and loops inside C rather than in your Python. It
returns a cursor whose `rowcount` is how many rows actually went in — `4` the
first time, `0` after that, because `INSERT OR IGNORE` quietly skips a name
that is already present instead of raising `IntegrityError`.

**Every value rides in on a `?`, even `0`.** Look at `in_stock_rows`: the SQL
text ends `in_stock > ?`, and the number `0` travels in the tuple `(0,)`. The
database never sees your value as part of the query — it sees a slot and a
value to drop into it. Today the value is a constant you typed. The day it
comes from a form, this exact habit is the only thing standing between you and
Exercise 2's disaster.

**`total_count` counts rows; the filter picks rows.** `SELECT COUNT(*)`
answers "how many roasts exist" — all four, including the one with no bags.
`in_stock_rows` answers "which can I sell" — the three with stock. Keeping the
zero-stock row in the table and out of the listing is why those two numbers
differ, and why the summary reads `3 of 4`.

**Commit, then close in a `finally`.** `conn.commit()` is what makes the four
writes permanent; without it they vanish when the connection closes.
`conn.close()` sits in `finally` so it runs even if a query above it throws —
a connection left open holds a lock on the file.

**Why the shipped file differs from yours.** Your `exercise-01-first-table.py`
keeps `roastery.db` in the folder you run it from, so you can reopen it and
poke around. The shipped answer runs the very same `main` inside a temporary
folder that is deleted on the way out, so the download can never collide with
a database of yours and never litters your disk. That is the only difference:
every run is a first run, which is why it always says `Inserted 4 roasts.` The
four query functions — the actual exercise — know nothing about the harness.

<details>
<summary>Under the hood — what "opening a transaction" actually means</summary>

A transaction is a set of changes the database treats as one all-or-nothing
move: either every change lands or none does. `sqlite3` in its default mode
opens one silently the first time you run an `INSERT`, `UPDATE`, `DELETE` or
`REPLACE`, and holds it open until you call `commit()` (save it) or
`rollback()` (throw it away). Closing the connection with an open transaction
rolls it back.

This is why the missing-commit bug is so quiet. `CREATE TABLE` is a schema
change and `sqlite3` commits it for you, so the table survives; the `INSERT`
rows are inside the open transaction, so they do not. You end up with a table
that exists and is empty — the exact shape that makes you suspect the
`INSERT` when the real fault is upstream.

Two ways to stop hitting it: call `commit()` yourself, as here, or wrap the
writes in `with conn:`, which commits on a clean exit and rolls back on an
exception. The stretch below has you try the second form.

</details>

## Run it

Copy the worked answer on this page into `exercise-01-first-table.py` and run it:

```bash
python exercise-01-first-table.py
```

It needs only the standard library, builds its catalogue in a throwaway
folder, prints it, and leaves your disk exactly as it found it. The
`-solution` in the name keeps it from colliding with your own
`exercise-01-first-table.py`.

## Common bugs to catch

- **`sqlite3.OperationalError: no such table: roasts`.** Your `SELECT` ran
  before `create_table`, or `create_table` still has only the `TODO`
  comment in it and silently returns `None`. A function body of just a
  comment is legal Python and does nothing.
- **`sqlite3.ProgrammingError: Incorrect number of bindings supplied. The
  current statement uses 1, and there are 4 supplied.`** You passed the
  parameter as a bare value instead of a tuple, or you passed a whole row
  to a one-placeholder query. One parameter needs the trailing comma:
  `(0,)`, not `(0)`.
- **`sqlite3.IntegrityError: UNIQUE constraint failed: roasts.name`.** You
  used a plain `INSERT` instead of `INSERT OR IGNORE` and ran the script
  twice. The constraint is doing its job — the database refused to store a
  second "Sunrise Blend". Either use `OR IGNORE` as specified, or delete
  the `.db` file between runs.
- **The rows come back but the table is empty tomorrow.** No `commit`. See
  the Constraints. Nothing raises; the rows simply were never saved.
- **`Decaf Quiet Hours` shows up in the listing.** Your condition is
  `in_stock >= ?` instead of `in_stock > ?`, or you dropped the `WHERE`
  clause. Zero bags in stock is still a row in the table, which is exactly
  why the filter has to be in the query.
- **`TypeError: 'int' object is not subscriptable` in `total_count`.**
  `fetchone()` returns a tuple like `(4,)`. You need `[0]` on the row, not
  on the integer inside it.
- **`ValueError: Unknown format code 'f' for object of type 'str'`.** Your
  `SELECT` column order does not match the tuple unpacking in `main`, so
  `price` is holding the origin string. Name the columns in the query in
  the order the code expects.

## Acceptance checklist

- [ ] The script runs from a deleted `roastery.db` with no traceback.
- [ ] Three roasts print, most expensive first, and `Decaf Quiet Hours` is not one of them.
- [ ] The summary line reads `3 of 4 roasts are in stock.`
- [ ] Every value in every query is bound through a `?` placeholder.
- [ ] `conn.commit()` is called before the reads and `conn.close()` is in a `finally` block.
- [ ] Running the script twice in a row does not raise, and the second run reports 0 inserted.
- [ ] `*.db` is in your `.gitignore`, and the file is committed to Git with a message like `Add Week 10 exercise 1: first SQLite table`.

## Stretch

- Set `conn.row_factory = sqlite3.Row` right after connecting and rewrite
  the print loop to use `row["name"]` instead of positional unpacking. The
  output should be identical and the code should stop caring about column
  order.
- Add a `restock(conn, name, bags)` function that runs an `UPDATE` with two
  parameters, then call it to give `Decaf Quiet Hours` six bags and watch it
  join the listing.
- Replace the `try`/`finally` with `contextlib.closing` plus a `with conn:`
  block, as in Lecture 3 section 2. Confirm the output does not change, then
  raise an exception in the middle of `seed` and confirm nothing is saved.

When your three lines look right, move on to
[Exercise 2 — Parameterized Queries](./exercise-02-parameterized.md).
