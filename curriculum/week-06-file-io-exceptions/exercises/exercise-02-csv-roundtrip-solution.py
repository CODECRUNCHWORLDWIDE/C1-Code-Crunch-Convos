"""exercise-02-csv-roundtrip-solution.py — filter a CSV export into a smaller CSV.

Reads a mentor-hours export, keeps every mentor with at least MIN_HOURS logged,
and writes the surviving rows to a second CSV with the same header.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact export the page gives
you, so the download runs on any machine with nothing set up beforehand. It
then reads its own output back to prove the roundtrip. ``qualifies`` and
``filter_rows`` are the whole exercise and know nothing about the harness.

Run it with::

    python exercise-02-csv-roundtrip-solution.py
"""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

MIN_HOURS = 10

#: The export exactly as the exercise page gives it, quotes included. The
#: "Chen, Lin" row is the reason this exercise forbids .split(",").
SAMPLE_EXPORT = (
    "name,chapter,hours,role\n"
    "Ada Lovelace,Lagos,12,mentor\n"
    "Grace Hopper,Manila,4,mentor\n"
    '"Chen, Lin",Lagos,19,lead\n'
    "Katherine Johnson,Bogota,7,mentor\n"
    "Alan Turing,Manila,0,observer\n"
    "Mary Jackson,Bogota,25,lead\n"
)


def qualifies(row: dict[str, str], min_hours: int) -> bool:
    """Return True when *row* logged at least *min_hours* hours.

    Every value in *row* is a string, because that is all a CSV holds.
    """
    return int(row["hours"]) >= min_hours


def filter_rows(source: Path, target: Path, min_hours: int) -> tuple[int, int]:
    """Copy the qualifying rows of *source* into *target*.

    Returns:
        A ``(rows_read, rows_kept)`` pair.
    """
    rows_read = 0
    rows_kept = 0
    with source.open("r", encoding="utf-8", newline="") as src, \
         target.open("w", encoding="utf-8", newline="") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=reader.fieldnames or [])
        writer.writeheader()
        for row in reader:
            rows_read += 1
            if qualifies(row, min_hours):
                writer.writerow(row)
                rows_kept += 1
    return rows_read, rows_kept


def build_sample(folder: Path) -> Path:
    """Write the sample mentor-hours export into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "mentor-hours.csv"
    path.write_text(SAMPLE_EXPORT, encoding="utf-8", newline="")
    return path


def read_back(path: Path) -> None:
    """Parse *path* again and print each row, so the roundtrip is visible."""
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            print(repr(row["name"]), row["chapter"], row["hours"], row["role"])


def main() -> None:
    """Build the sample export, filter it, and read the result back."""
    with tempfile.TemporaryDirectory() as workspace:
        data = Path(workspace) / "data"
        source = build_sample(data)
        target = data / "mentor-hours-certified.csv"

        read, kept = filter_rows(source, target, MIN_HOURS)
        print(f"Read {read} rows from {source.name}")
        print(f"Kept {kept} rows at or above {MIN_HOURS} hours")
        print(f"Wrote {target.name}")

        print()
        print(f"--- {target.name} ---")
        print(target.read_text(encoding="utf-8"), end="")

        print()
        print("--- read back with DictReader ---")
        read_back(target)


if __name__ == "__main__":
    main()
