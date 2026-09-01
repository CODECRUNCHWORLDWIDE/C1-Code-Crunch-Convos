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
