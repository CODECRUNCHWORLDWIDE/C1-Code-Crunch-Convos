"""Writing the reports.

The only module that touches the output directory. Week 6 hard-coded the three
report filenames in the middle of ``main``; here they are module constants with
keyword arguments in front of them, so a test can write to ``tmp_path`` under
any name it likes.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Sequence
from pathlib import Path

from loganalyzer.analysis import hourly_counts
from loganalyzer.models import LogRecord, Summary

__all__ = [
    "BY_HOUR_FILENAME",
    "BY_LEVEL_FILENAME",
    "SUMMARY_FILENAME",
    "write_hourly_csv",
    "write_level_csv",
    "write_reports",
    "write_summary",
]

SUMMARY_FILENAME = "summary.json"
BY_LEVEL_FILENAME = "by-level.csv"
BY_HOUR_FILENAME = "by-hour.csv"


def write_summary(summary: Summary, path: Path) -> None:
    """Write *summary* as pretty-printed JSON, with a trailing newline."""
    with path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")


def write_level_csv(summary: Summary, path: Path) -> None:
    """Write the per-level counts as ``level,count`` rows, sorted by level."""
    counts = summary["counts"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["level", "count"])
        for level in sorted(counts):
            writer.writerow([level, counts[level]])


def write_hourly_csv(records: Sequence[LogRecord], path: Path) -> None:
    """Write ``hour,count`` rows, sorted chronologically."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["hour", "count"])
        for hour, count in sorted(hourly_counts(records).items()):
            writer.writerow([hour, count])


def write_reports(
    summary: Summary,
    records: Sequence[LogRecord],
    out_dir: Path,
    *,
    by_hour: bool = False,
    summary_name: str = SUMMARY_FILENAME,
    level_name: str = BY_LEVEL_FILENAME,
    hour_name: str = BY_HOUR_FILENAME,
) -> tuple[Path, Path]:
    """Create *out_dir* if needed, write the reports, return the two main paths.

    Returning the paths rather than printing them is what lets ``cli.main``
    decide on the wording and a test assert on the files.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / summary_name
    level_path = out_dir / level_name

    write_summary(summary, summary_path)
    write_level_csv(summary, level_path)
    if by_hour:
        write_hourly_csv(records, out_dir / hour_name)

    return summary_path, level_path
