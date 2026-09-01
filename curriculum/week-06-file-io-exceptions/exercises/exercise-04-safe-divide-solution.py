"""exercise-04-safe-divide-solution.py — a report that survives bad rows.

Reads a chapter-totals export and prints average attendance per session for
each chapter. Rows that cannot be computed are logged and reported as "--".
The report goes to stdout; every failure notice goes to stderr through the
logging module.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact export the page gives
you, so the download runs on any machine with nothing set up beforehand.

Every print in the report carries flush=True. Without it stdout is held in a
buffer whenever it is not a terminal, so `python ... 2>&1 | more` would show all
six report lines in a block after all the log lines instead of interleaved with
them. Flushing each line as it is produced makes the combined transcript on the
page reproducible on your machine too.

Run it with::

    python exercise-04-safe-divide-solution.py
"""

from __future__ import annotations

import csv
import logging
import tempfile
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
log = logging.getLogger(__name__)

#: The export exactly as the exercise page gives it. Quito's trailing comma is
#: an empty field, and Osaka's real average is 0.00 rather than "no answer".
SAMPLE_TOTALS = (
    "chapter,attendees,sessions\n"
    "Lagos,180,12\n"
    "Manila,64,8\n"
    "Bogota,0,0\n"
    "Nairobi,45,three\n"
    "Quito,90,\n"
    "Osaka,0,4\n"
)


def safe_divide(numerator: float, denominator: float, label: str) -> float | None:
    """Return numerator / denominator, or None when the division is impossible.

    *label* names the thing being divided so the log line is searchable.
    Logs a warning for a zero denominator and an error for non-numeric input.
    """
    try:
        return numerator / denominator
    except ZeroDivisionError:
        log.warning("%s: denominator is zero; average is undefined", label)
        return None
    except TypeError:
        log.error("%s: cannot divide %r by %r", label, numerator, denominator)
        return None


def average_attendance(row: dict[str, str]) -> float | None:
    """Return the average attendance for one CSV row, or None if it is unusable."""
    chapter = row["chapter"]
    try:
        attendees = int(row["attendees"])
    except ValueError:
        log.error(
            "%s: attendees value %r is not a whole number", chapter, row["attendees"]
        )
        return None
    try:
        sessions = int(row["sessions"])
    except ValueError:
        log.error(
            "%s: sessions value %r is not a whole number", chapter, row["sessions"]
        )
        return None
    return safe_divide(attendees, sessions, chapter)


def report(source: Path) -> None:
    """Print the attendance report for *source* and log a summary count."""
    with source.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    log.info("read %d rows from %s", len(rows), source.name)

    usable = 0
    for row in rows:
        average = average_attendance(row)
        if average is None:
            text = "--"
        else:
            usable += 1
            text = f"{average:.2f}"
        print(f"{row['chapter']:<10} {text:>6}", flush=True)

    # Deliberate mistake, so you can watch the TypeError branch fire:
    safe_divide("64", 8, "unconverted string")

    log.info("%d of %d chapters had a usable average", usable, len(rows))


def build_sample(folder: Path) -> Path:
    """Write the sample chapter-totals export into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "chapter-totals.csv"
    path.write_text(SAMPLE_TOTALS, encoding="utf-8", newline="")
    return path


def main() -> None:
    """Build the sample data and run the report over it."""
    with tempfile.TemporaryDirectory() as workspace:
        report(build_sample(Path(workspace) / "data"))


if __name__ == "__main__":
    main()
