"""problem-03-csv-to-markdown-solution.py — CSV to a Markdown table, headless.

The homework answer reads a CSV and prints a GitHub-flavored Markdown table:
columns padded to their widest cell, `|` escaped inside cells, and an optional
--align. Your own problem-03-csv-to-markdown.py ends in
``raise SystemExit(main())`` and you point it at a real CSV.

This is pure standard library and already deterministic, so the demo just builds
a small CSV in a temp file — with a cell that contains a `|`, and an empty cell —
and renders it left-aligned and centered. The converter being tested is
identical either way.

Run it with::

    python problem-03-csv-to-markdown-solution.py
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

MIN_WIDTH = 3  # a column narrower than "---" cannot hold a separator

SEPARATORS = {
    "l": lambda width: ":" + "-" * (width - 1),
    "c": lambda width: ":" + "-" * (width - 2) + ":",
    "r": lambda width: "-" * (width - 1) + ":",
}


def escape(cell: str) -> str:
    """A pipe inside a cell would start a new column; backslash-escape it."""
    return cell.replace("|", "\\|")


def render_table(rows: list[list[str]], align: str) -> str:
    """Render rows (header first) as a padded GitHub-flavored Markdown table."""
    grid = [[escape(cell) for cell in row] for row in rows]
    columns = max(len(row) for row in grid)
    grid = [row + [""] * (columns - len(row)) for row in grid]  # ragged rows squared off
    widths = [max(MIN_WIDTH, max(len(row[i]) for row in grid)) for i in range(columns)]

    def line(cells: list[str]) -> str:
        return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)) + " |"

    separator = "| " + " | ".join(SEPARATORS[align](widths[i]) for i in range(columns)) + " |"
    header, *body = grid
    return "\n".join([line(header), separator, *(line(row) for row in body)])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv2md",
        description="Turn a CSV file into a GitHub-flavored Markdown table.",
    )
    parser.add_argument("csv", type=Path, help="The CSV file to read.")
    parser.add_argument("--align", choices=("l", "c", "r"), default="l",
                        help="Column alignment (default: %(default)s)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Read the CSV, print the Markdown table. Return an exit code."""
    args = build_parser().parse_args(argv)
    if not args.csv.is_file():
        print(f"error: no such CSV file: {args.csv}", file=sys.stderr)
        return 1

    with args.csv.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.reader(handle) if row]
    if not rows:
        print(f"error: {args.csv} is empty", file=sys.stderr)
        return 1

    print(render_table(rows, args.align))
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — a small CSV built in a temp file. Your own file has no
# demo; it reads a CSV path from the command line.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Render one small CSV two ways."""
    print("CSV to Markdown — driven headless on a CSV this file builds.")
    print()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = Path(tmp) / "data.csv"
        csv_path.write_text(
            "Name,Score,Note\n"
            "Alice,95,top | marks\n"   # the pipe must be escaped
            "Bob,87,steady\n"
            "Carol,100,\n",            # an empty cell
            encoding="utf-8",
        )
        print("Default (left-aligned):")
        print(f"[exit {main([str(csv_path)])}]")
        print()
        print("Center-aligned (--align c):")
        print(f"[exit {main([str(csv_path), '--align', 'c'])}]")


if __name__ == "__main__":
    demo()
