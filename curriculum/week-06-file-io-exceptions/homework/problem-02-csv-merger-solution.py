"""Homework 2 — CSV merger.

Concatenates several CSV files that share one header into a single output file,
adding a `source` column holding each row's originating filename (no extension).

    python csv_merge.py q1.csv q2.csv q3.csv --out year.csv

Run it with no arguments and it builds its own three quarters of orders in a
scratch folder first, so the download works from a clean checkout with nothing
set up.

Save your own copy as ``csv_merge.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import sys
import tempfile
from pathlib import Path

SOURCE_COLUMN = "source"

#: The spec's example prints U+2192 RIGHTWARDS ARROW here. This answer prints
#: ASCII instead, so the summary line is the same bytes on every console. The
#: page beside this file explains what goes wrong with the pretty one.
ARROW = "->"


def read_header(path: Path) -> list[str]:
    """Return the header row of *path*, or raise ValueError if there is none.

    Args:
        path: The CSV file to inspect.

    Returns:
        The header row as a list of column names.

    Raises:
        ValueError: If the file is empty and so has no header row.
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f), None)
    if header is None:
        raise ValueError(f"{path} is empty: no header row to merge")
    return header


def common_header(paths: list[Path]) -> list[str]:
    """Return the shared header, or raise ValueError naming the first mismatch.

    Runs before the output file is opened, so a mismatch leaves the filesystem
    exactly as it was.

    Args:
        paths: The input files, in the order they will be merged.

    Returns:
        The header every input agrees on.

    Raises:
        ValueError: If two inputs disagree, or the first already has a
            ``source`` column.
    """
    reference = read_header(paths[0])
    if SOURCE_COLUMN in reference:
        raise ValueError(
            f"{paths[0]} already has a {SOURCE_COLUMN!r} column; "
            "merging would produce two columns with the same name"
        )
    for path in paths[1:]:
        header = read_header(path)
        if header != reference:
            raise ValueError(
                f"header mismatch: {paths[0]} has {reference} "
                f"but {path} has {header}"
            )
    return reference


def merge(paths: list[Path], out_path: Path) -> int:
    """Merge *paths* into *out_path*. Return the number of data rows written.

    Args:
        paths: The input files.
        out_path: The file to create.

    Returns:
        How many data rows were written, not counting the header.
    """
    header = common_header(paths)
    fieldnames = [*header, SOURCE_COLUMN]
    rows_written = 0

    with out_path.open("w", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as src:
                for row in csv.DictReader(src):
                    row[SOURCE_COLUMN] = path.stem
                    writer.writerow(row)
                    rows_written += 1
    return rows_written


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Turn the command line into an inputs list and an output path.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        A namespace with ``inputs`` and ``out``.
    """
    parser = argparse.ArgumentParser(
        prog="csv_merge.py",
        description="Concatenate CSV files that share a header.",
    )
    parser.add_argument("inputs", nargs="+", type=Path, metavar="CSV")
    parser.add_argument("--out", required=True, type=Path, metavar="PATH")
    return parser.parse_args(argv)


def _write_quarter(path: Path, prefix: str, rows: int) -> None:
    """Write one sample quarter of orders to *path*.

    Args:
        path: The CSV file to create.
        prefix: The two-letter order-id prefix, such as ``Q1``.
        rows: How many data rows to write.
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "customer", "amount"])
        for i in range(rows):
            writer.writerow(
                [
                    f"{prefix}-{i:04d}",
                    f"Customer {i % 40}",
                    f"{random.randint(500, 90000) / 100:.2f}",
                ]
            )


def _demo() -> int:
    """Build four sample CSV files in a scratch folder and merge them.

    Shows both paths the problem cares about: three files that agree merge
    cleanly, and a fourth whose header disagrees stops the run before the
    output file is created. The scratch folder is a temporary directory this
    function makes and deletes, so nothing has to be placed by hand.

    Returns:
        Always 0. Both demonstrated outcomes are the intended ones.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="csv_merge_") as scratch:
        try:
            os.chdir(scratch)
            # A fixed seed makes the amounts the same on every machine, so the
            # sample row printed below is something you can compare against.
            random.seed(6)
            _write_quarter(Path("q1.csv"), "Q1", 280)
            _write_quarter(Path("q2.csv"), "Q2", 300)
            _write_quarter(Path("q3.csv"), "Q3", 262)
            with Path("q4-bad.csv").open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["order_id", "customer", "total"])
                writer.writerow(["Q4-0000", "Customer 1", "10.00"])

            main(["q1.csv", "q2.csv", "q3.csv", "--out", "year.csv"])
            with Path("year.csv").open("r", encoding="utf-8", newline="") as f:
                for line in list(f)[:2]:
                    print(line.rstrip("\r\n"))

            code = main(["q1.csv", "q4-bad.csv", "--out", "year2.csv"])
            print(f"exit code {code}, year2.csv created: {Path('year2.csv').exists()}")
        finally:
            os.chdir(home)
    return 0


def main(argv: list[str] | None = None) -> int:
    """Merge the files named on the command line, or run the demo if there are none.

    Args:
        argv: Command-line arguments, without the program name. ``None`` means
            read them from ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return _demo()
    parsed = parse_args(args)
    try:
        rows = merge(parsed.inputs, parsed.out)
    except ValueError as e:
        print(f"csv_merge.py: error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"csv_merge.py: error: no such file: {e.filename}", file=sys.stderr)
        return 1
    print(f"Merged {len(parsed.inputs)} files {ARROW} {parsed.out} ({rows} total rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
