"""Exercise 02 — CSV round-trip.

Topic: csv.DictReader, csv.DictWriter, filtering.
Reference: lecture-notes/02-csv-and-json.md sections 2 and 3.

Task
----
You will be given a `students.csv` file with the columns:

    name,grade,class

Write a function `filter_passing(src, dst, threshold)` that:

  * Reads `src` as CSV using `csv.DictReader`.
  * Keeps only rows where the student's grade is >= `threshold`.
  * Writes the kept rows to `dst` using `csv.DictWriter`, preserving
    the column order from the source.
  * Returns a tuple `(kept, total)` of the row counts.

A small CSV is embedded in this file as `SAMPLE_CSV` so you can run it
without any external data file.

Expected output (default threshold = 70):

    Kept 4 of 6 students.
    --- passing.csv ---
    name,grade,class
    Alice,92,Math
    Bob,85,Math
    Diana,71,Science
    Frank,70,History
"""

from __future__ import annotations

import csv
from pathlib import Path

SAMPLE_CSV = """\
name,grade,class
Alice,92,Math
Bob,85,Math
Carlos,55,Math
Diana,71,Science
Eve,40,Science
Frank,70,History
"""


def filter_passing(src: Path, dst: Path, threshold: int = 70) -> tuple[int, int]:
    """Copy rows from `src` to `dst` where grade >= `threshold`.

    Returns (kept_count, total_count).
    """
    kept = 0
    total = 0
    with src.open("r", encoding="utf-8", newline="") as fin, \
         dst.open("w", encoding="utf-8", newline="") as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames or []
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            total += 1
            # CSV always returns strings — convert before comparing.
            try:
                grade = int(row["grade"])
            except (KeyError, ValueError):
                # Malformed row — skip it. We will learn better error
                # handling in exercise 04.
                continue
            if grade >= threshold:
                writer.writerow(row)
                kept += 1
    return kept, total


if __name__ == "__main__":
    here = Path(__file__).parent
    src = here / "students.csv"
    dst = here / "passing.csv"

    # Create the sample input.
    src.write_text(SAMPLE_CSV, encoding="utf-8")

    kept, total = filter_passing(src, dst, threshold=70)
    print(f"Kept {kept} of {total} students.")

    print("--- passing.csv ---")
    print(dst.read_text(encoding="utf-8"), end="")
