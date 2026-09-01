# Homework Problem 3 — CSV → SQLite Importer

> **Topic:** loading a file you did not write into a table, with an all-or-nothing transaction and a name you can trust
> **Lecture:** [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md) (sections 1–4)
> **Difficulty:** Intermediate
> **Target time:** 45 minutes
> **Why this one:** a `?` placeholder protects every *value* you put into SQL. This problem is where you meet the one thing a placeholder cannot carry — a table or column *name* — and learn the completely different tool you need for it. That gap is where a whole class of injection bugs hides, and closing it properly is the point.

## The Brief

Someone hands you a CSV file — a spreadsheet exported to plain text,
first row the column names, every row after that a record. You want it in
a SQLite table so you can query it. Write a tool that reads any CSV and
loads it, no matter what the file is called or what columns it has.

That "no matter what it's called" is the interesting part. You will name
the table after the file and the columns after the header row. But a
table name is not a *value* — it is part of the SQL *syntax*, and a `?`
placeholder can only stand in for values. So `SELECT ?` can hold a
number or a string, but `CREATE TABLE ?` is a syntax error. You cannot
bind a name.

This is exactly the hole SQL injection crawls through. If you build the
table name by pasting the filename straight into the SQL, a file called
`students; DROP TABLE users; --.csv` becomes a command. The fix is not to
*escape* the name — it is to **allow-list** it: strip it down to only the
characters `a-z`, `0-9`, and `_`, so nothing dangerous can survive to be
part of the SQL at all.

Your importer:

- Reads a CSV whose path is on the command line.
- Names the table after the file (sanitized), the columns after the
  header (sanitized), every column `TEXT` for simplicity.
- Inserts every row with one `executemany` and a parameterized query.
- Wraps the whole import in one transaction, so a single bad row rolls
  everything back.
- Run with no arguments, it demonstrates itself: writes a ten-row sample,
  imports it, shows the sanitizer at work on hostile names, and proves
  the all-or-nothing rollback with a broken row.

## Starter

Save this as `importer.py` and fill in the `TODO`s. It runs as pasted —
the sanitizer returns the name unchanged until you write it.

```python
"""Import any CSV file into a SQLite table named after the file."""

import csv
import re
import sqlite3
import sys
from pathlib import Path


def sanitize_identifier(raw: str) -> str:
    """Reduce any text to a safe identifier: a-z, 0-9 and _ only."""
    # TODO: lowercase; turn every run of other chars into one underscore;
    #       strip leading/trailing underscores; prefix 't_' if it starts
    #       with a digit or ends up empty.
    return raw


def import_csv(conn: sqlite3.Connection, csv_path: Path) -> tuple[str, int]:
    """Import csv_path into a table named after the file. Returns (table, rows)."""
    table = sanitize_identifier(csv_path.stem)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        columns = [sanitize_identifier(name) for name in header]
        # TODO: build "CREATE TABLE {table} (col TEXT, col TEXT, ...)"
        # TODO: inside `with conn:` create the table and executemany the rows
        #       through a "(?, ?, ...)" placeholder string
        rows = 0
    return table, rows


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: importer.py FILE.csv", file=sys.stderr)
        return 1
    conn = sqlite3.connect("import.db")
    try:
        table, rows = import_csv(conn, Path(argv[0]))
        print(f"Imported {rows} rows into '{table}'.")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-10-databases-sql/homework/problem-03-csv-importer.md) and run it there. `csv` and `sqlite3` both ship with Python.

## Requirements

1. `sanitize_identifier(raw)` returns a string containing only `a-z`,
   `0-9`, and `_`. It lowercases, collapses every run of other characters
   into a single `_`, and prefixes `t_` if the result starts with a digit
   or is empty.
2. The table is named after the CSV file's stem; the columns are named
   after the header, each sanitized.
3. Column names that collide after sanitizing are made unique.
4. Rows are inserted with one `executemany` and a `?` placeholder per
   column.
5. The whole import is one transaction: a row with the wrong number of
   fields raises, and nothing — not even the `CREATE TABLE` — survives.
6. Run with no arguments, the file demonstrates itself and leaves no
   `.db` behind.

## Constraints

- **A `?` placeholder is for values, never for identifiers.** Table and
  column names are part of the SQL grammar. `conn.execute("CREATE TABLE
  ?", (name,))` raises a syntax error — the database will not let you
  parameterize a name. This is not a limitation to work around; it is the
  reason identifiers need their own, stricter defence.
- **Allow-list the name; do not escape it.** Escaping asks "how do I make
  these hostile characters safe?" Allow-listing asks "which characters am
  I willing to keep?" and throws away everything else. After
  `re.sub(r"[^a-z0-9]+", "_", raw.lower())`, there is no quote to break
  out of and no semicolon to start a second statement — the dangerous
  characters do not exist in the result. That is why
  `DROP TABLE users; --` becomes the harmless table name `drop_table_users`.
- **The whole import is one transaction.** `with conn:` opens one, commits
  it if the block finishes, and rolls it all back if anything raises.
  Half a file is worse than none: you would not know where it stopped, so
  you could not safely resume. All-or-nothing means "run it again" is
  always the right recovery.
- **The row values still go through `?`.** Sanitizing is only for the
  names. The actual cell contents are bound as parameters, exactly as
  always, because those *are* values and a placeholder is exactly right
  for them.

## Expected output

Run with no arguments, the importer demonstrates itself. The elapsed time
goes to stderr, so the comparable output is just this:

```text
Wrote sample.csv (10 data rows).
Imported 10 rows into table 'sample'.
Columns (from the header): full_name, email, city

The sanitizer on names you cannot bind:
  '2026 Sales / Q1'         -> 't_2026_sales_q1'
  'DROP TABLE users; --'    -> 'drop_table_users'

A bad row rolls the whole import back:
  rejected: row 3 has 2 fields, expected 3
  rows in 'broken' after the failed import: 0 (all or nothing)
```

## Steps

1. Run the starter with a file path. It reads the header but imports zero
   rows — the body is still `TODO`. That is your scaffold.
2. Write `sanitize_identifier`. Test it at the REPL on `"Full Name"`,
   `"2026 Sales / Q1"`, and `"DROP TABLE users; --"` before wiring it in.
   You are looking for `full_name`, `t_2026_sales_q1`, `drop_table_users`.
3. Build the `CREATE TABLE` and the `executemany`. Import a real file and
   query it in the shell to confirm the rows landed.
4. Add the field-count check that raises on a short or long row, inside
   the `with conn:` block, so the raise rolls the import back.
5. Switch to the no-argument demo and confirm every line of the Expected
   output, including the rollback proof.

## The Solution

```python
"""problem-03-csv-importer-solution.py — any CSV file into a SQLite table.

Give it a CSV path and it creates a table named after the file, columns
named after the header, every column TEXT, every row inserted through one
``executemany`` inside one transaction — so a bad row rolls the whole
import back.

The one thing a ``?`` placeholder cannot carry is an identifier: table and
column names are syntax, not values. So every identifier is squeezed through
``sanitize_identifier`` first, which reduces it to the characters
``a-z 0-9 _`` — after that, nothing hostile can survive in the name.
``2026 Sales / Q1.csv`` becomes the table ``t_2026_sales_q1``.

Run it on your own file::

    python problem-03-csv-importer-solution.py people.csv people.db

Run it with no arguments and it demonstrates itself in a throwaway folder:
it writes a ten-row sample.csv, imports it, shows the sanitizer working on
hostile names, and proves the all-or-nothing transaction with a bad row.
The elapsed time goes to stderr, so it never muddies the comparable output.
"""

import csv
import re
import sqlite3
import sys
import tempfile
import time
from pathlib import Path
from typing import Final

SAMPLE_ROWS: Final[list[tuple[str, str, str]]] = [
    ("Ada Lovelace",      "ada@example.com",       "London"),
    ("Grace Hopper",      "grace@example.com",     "Arlington"),
    ("Alan Turing",       "alan@example.com",      "Wilmslow"),
    ("Katherine Johnson", "katherine@example.com", "Hampton"),
    ("Margaret Hamilton", "margaret@example.com",  "Boston"),
    ("Guido van Rossum",  "guido@example.com",     "San Francisco"),
    ("Radia Perlman",     "radia@example.com",     "Redmond"),
    ("Tim Berners-Lee",   "tim@example.com",       "Geneva"),
    ("Annie Easley",      "annie@example.com",     "Cleveland"),
    ("Dennis Ritchie",    "dennis@example.com",    "Murray Hill"),
]


def sanitize_identifier(raw: str) -> str:
    """Reduce any text to a safe SQLite identifier: a-z, 0-9 and _ only.

    Lowercase, every run of anything else becomes one underscore, and a name
    that starts with a digit (or ends up empty) gets a ``t_`` prefix so it is
    still a legal identifier. This is an allow-list, not an escape: hostile
    characters do not get quoted, they simply cannot exist in the result.
    """
    cleaned = re.sub(r"[^a-z0-9]+", "_", raw.lower()).strip("_")
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"t_{cleaned}" if cleaned else "t_unnamed"
    return cleaned


def unique_names(raw_names: list[str]) -> list[str]:
    """Sanitize every column name, numbering any that collide afterwards."""
    seen: dict[str, int] = {}
    result: list[str] = []
    for raw in raw_names:
        name = sanitize_identifier(raw)
        seen[name] = seen.get(name, 0) + 1
        result.append(name if seen[name] == 1 else f"{name}_{seen[name]}")
    return result


def import_csv(conn: sqlite3.Connection, csv_path: Path) -> tuple[str, int]:
    """Import `csv_path` into a table named after the file. Returns (table, rows).

    The whole import is one transaction (``with conn:``): if any row has the
    wrong number of fields, everything — including the CREATE TABLE — is
    rolled back and the database is exactly as it was.
    """
    table = sanitize_identifier(csv_path.stem)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if not header:
            raise ValueError(f"{csv_path.name} has no header row")
        columns = unique_names(header)
        column_ddl = ", ".join(f"{name} TEXT" for name in columns)
        placeholders = ", ".join("?" for _ in columns)
        with conn:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
            conn.execute(f"CREATE TABLE {table} ({column_ddl})")
            rows = 0
            for line_number, row in enumerate(reader, start=2):
                if len(row) != len(columns):
                    raise ValueError(
                        f"row {line_number} has {len(row)} fields, "
                        f"expected {len(columns)}"
                    )
                conn.execute(
                    f"INSERT INTO {table} VALUES ({placeholders})", row
                )
                rows += 1
    return table, rows


def row_count(conn: sqlite3.Connection, table: str) -> int:
    """Count rows in a table this module created (name already sanitized)."""
    exists = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?",
        ("table", table),
    ).fetchone()[0]
    if not exists:
        return 0
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def demo() -> None:
    """Self-contained demonstration in a temporary folder."""
    with tempfile.TemporaryDirectory() as workspace:
        folder = Path(workspace)
        sample = folder / "sample.csv"
        with sample.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["Full Name", "Email", "City"])
            writer.writerows(SAMPLE_ROWS)
        print(f"Wrote {sample.name} ({len(SAMPLE_ROWS)} data rows).")

        conn = sqlite3.connect(folder / "import_demo.db")
        try:
            table, rows = import_csv(conn, sample)
            print(f"Imported {rows} rows into table '{table}'.")
            columns = [name for (name, ) in conn.execute(
                "SELECT name FROM pragma_table_info(?)", (table,)
            ).fetchall()]
            print(f"Columns (from the header): {', '.join(columns)}")

            print("\nThe sanitizer on names you cannot bind:")
            for hostile in ("2026 Sales / Q1", "DROP TABLE users; --"):
                print(f"  {hostile!r:<25} -> {sanitize_identifier(hostile)!r}")

            print("\nA bad row rolls the whole import back:")
            broken = folder / "broken.csv"
            broken.write_text(
                "name,email,city\n"
                "Ada,ada@example.com,London\n"
                "Grace,grace@example.com\n",   # one field short
                encoding="utf-8",
            )
            try:
                import_csv(conn, broken)
            except ValueError as exc:
                print(f"  rejected: {exc}")
            print(f"  rows in 'broken' after the failed import: "
                  f"{row_count(conn, 'broken')} (all or nothing)")
        finally:
            conn.close()


def main(argv: list[str]) -> int:
    """CLI entry point: a path imports that file; no arguments runs the demo."""
    started = time.perf_counter()
    if not argv:
        demo()
    else:
        csv_path = Path(argv[0])
        if not csv_path.exists():
            print(f"error: no such file: {csv_path}", file=sys.stderr)
            return 1
        db_path = Path(argv[1]) if len(argv) > 1 else csv_path.with_suffix(".db")
        conn = sqlite3.connect(db_path)
        try:
            table, rows = import_csv(conn, csv_path)
            print(f"Imported {rows} rows into table '{table}' in {db_path.name}.")
        except ValueError as exc:
            print(f"error: {exc} - nothing imported", file=sys.stderr)
            return 1
        finally:
            conn.close()
    elapsed = time.perf_counter() - started
    print(f"[{elapsed:.3f}s]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

<!--@@INSERT:problem-03-csv-importer-solution.py@@-->

**Why it works.**

**The one thing you cannot bind is a name.** A `?` placeholder tells
SQLite "a value goes here" and keeps that value forever separate from the
SQL text. But a table or column name is not a value — it is grammar, like
a keyword or a parenthesis. There is nowhere in `CREATE TABLE x (...)`
for a placeholder to stand, because the name *is* the structure. So
identifiers need a different guarantee, and `sanitize_identifier` is it.

**Allow-listing is stronger than escaping, because it removes the
problem instead of taming it.** `re.sub(r"[^a-z0-9]+", "_", raw.lower())`
keeps letters, digits, and nothing else; every run of anything else
becomes a single underscore. A quote cannot end a string that no longer
contains a quote. A semicolon cannot start a new statement that no longer
contains a semicolon. `DROP TABLE users; --` does not get *quoted* into
safety — it gets *reduced* to `drop_table_users`, a perfectly boring
table name. There is nothing left to escape.

**Once the name is safe, it is safe to format into the SQL.** This is the
subtle part. The code does write `f"CREATE TABLE {table}"` — an f-string
in a SQL statement, the exact thing the week tells you never to do. The
difference is that `table` has already been through the allow-list, so it
is provably one of a tiny set of harmless strings. The rule "never
f-string into SQL" is really "never f-string *untrusted input* into SQL";
an identifier you have sanitized down to `[a-z0-9_]` is no longer
untrusted. The row *values*, which are still untrusted, go through `?`.

**One transaction makes failure recoverable.** `with conn:` wraps the
`CREATE TABLE` and every `INSERT` in a single transaction. A row with the
wrong field count raises a `ValueError`, the `with` block rolls the whole
thing back, and the table is not even created. `row_count` afterwards
returns `0`, not "however many rows we got through before the bad one".
That is what makes the recovery trivial: fix the file, run it again.

## Download and run

Download [problem-03-csv-importer-solution.py](./problem-03-csv-importer-solution.py)
and run it two ways. With no arguments, it demonstrates itself in a
throwaway folder:

```bash
python problem-03-csv-importer-solution.py
```

With a path, it imports your own file:

```bash
python problem-03-csv-importer-solution.py people.csv people.db
```

The demo creates its sample, its database, and a deliberately broken CSV
inside a temporary directory it deletes on the way out, so it runs
anywhere and leaves nothing behind.

## Common bugs to catch

- **`sqlite3.OperationalError: near "?": syntax error`.** You tried to
  bind the table or column name: `conn.execute("CREATE TABLE ?", (name,))`.
  Names are syntax, not values — sanitize them and format them in.
- **`sqlite3.OperationalError: near "Sales": syntax error`.** You pasted
  a raw filename with a space (`2026 Sales`) straight into the SQL. This
  is the injection hole; the sanitizer closes it by turning the name into
  `t_2026_sales_q1`.
- **The bad row leaves a half-filled table behind.** Your field-count
  check raised *outside* the `with conn:` block, or you committed each row
  as you went. The check has to raise inside the transaction so the
  rollback undoes everything.
- **`sqlite3.ProgrammingError: Incorrect number of bindings supplied.`**
  Your placeholder string does not have one `?` per column. Build it from
  the columns you actually created: `", ".join("?" for _ in columns)`.
- **Two header columns sanitize to the same name.** `"First Name"` and
  `"first_name"` both become `first_name`, and
  `CREATE TABLE ... (first_name TEXT, first_name TEXT)` is a duplicate-
  column error. `unique_names` numbers the collisions so they survive.

## Under the hood

<details>
<summary>Under the hood — why parameter binding is not "escaping done well"</summary>

It is tempting to picture a `?` placeholder as a very careful
find-and-replace: the driver takes your value, wraps it in quotes,
doubles any quotes inside it, and pastes the result into the SQL string.
If that were how it worked, injection would still be possible — just
harder — because it is still one string of SQL in the end.

That is not how it works. The Python `sqlite3` driver sends the SQL text
and the parameters to SQLite as **two separate things**. The SQL —
`INSERT INTO t VALUES (?)` — is parsed and compiled into a little program
(a "prepared statement") *before* your value is anywhere near it. Then
the value is handed to that compiled program as data, dropped into a slot
the parser already marked. Your value is never text that gets parsed as
SQL. There is no string for it to break out of, because at the moment of
parsing, it was not in the string.

This is why `sanitize_identifier` is a genuinely different tool for a
genuinely different job. Values get the two-channel guarantee for free.
Identifiers cannot — the name has to be in the SQL text before parsing,
because it *is* part of what gets parsed — so they need their own,
weaker-but-sufficient defence: reduce them to a character set that cannot
express an attack.

The order of strength: **binding beats sanitizing beats escaping.** Use
binding wherever you can (all values). Where you cannot (identifiers),
sanitize with an allow-list. Never hand-roll escaping — the reason
libraries exist is that everyone who tried to escape SQL by hand
eventually got it wrong.

</details>

<details>
<summary>Under the hood — why executemany is faster than a loop of execute</summary>

`conn.execute("INSERT ...", row)` called in a Python loop does real work
every single time: it looks up the prepared statement, checks the
parameters, and — depending on how the transaction is managed — may sync
to disk. Ten rows, nobody notices. Ten million rows, it is the reason
the import takes nine minutes.

`executemany` prepares the statement **once** and feeds every row through
that same compiled program, all inside one transaction. The parsing cost
is paid a single time instead of ten million times, and the whole batch
commits together rather than row by row.

The reference solution uses a loop of `execute` on purpose, though —
because it needs to check each row's field count and raise on the first
bad one, which `executemany` cannot do (it takes the rows all at once).
It keeps the *transaction* benefit by wrapping the loop in `with conn:`,
so all the inserts still commit together. The speed lesson is: reach for
`executemany` when you trust the rows, and a transaction-wrapped loop
when you need to inspect each one. Both beat a loop of auto-committed
inserts, which is the genuinely slow shape.

</details>

## Acceptance checklist

- [ ] `sanitize_identifier` yields only `[a-z0-9_]`, lowercased.
- [ ] `"DROP TABLE users; --"` becomes `drop_table_users`.
- [ ] The table is named after the file, columns after the header.
- [ ] Colliding column names are made unique.
- [ ] Rows insert through a `?` placeholder per column.
- [ ] A short or long row rolls the whole import back to zero rows.
- [ ] The no-argument demo runs and leaves no `.db` file behind.

## Stretch

- **Infer types instead of making everything `TEXT`.** Peek at the first
  few rows: if every value in a column parses as an `int`, make it
  `INTEGER`; as a `float`, `REAL`; otherwise `TEXT`. Notice how much
  trickier "looks like a number" is than it sounds (leading zeros? empty
  cells?).
- **Stream a huge file.** Instead of one giant transaction, commit every
  10,000 rows so a million-row import does not hold one enormous
  transaction open. What do you lose in exchange? (Hint: a failure now
  leaves the committed batches behind.)
- **Handle a header with duplicate names in the file itself** —
  `id,id,id` — and confirm your `unique_names` numbering copes.
- **Add a `--table NAME` flag** to override the auto-generated table name.
  Run its value through `sanitize_identifier` too — an override from the
  command line is exactly as untrusted as the filename.

Next: [Problem 4 — Query Optimizer Puzzle](./problem-04-query-optimizer.md),
where you make a slow query fast and *watch* the plan change.
