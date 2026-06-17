"""Log file analyzer — starter skeleton.

Reads a .log file, counts entries per level (INFO/WARNING/ERROR/DEBUG),
finds the most common ERROR message, and writes a JSON summary plus a
CSV breakdown.

Usage
-----
    python starter.py sample.log --out-dir reports/

What you need to fill in
------------------------
Every function with a `# TODO:` comment. The structure is suggested but
not mandatory — if you have a cleaner design, use it.

References
----------
- lecture-notes/01-files-and-pathlib.md
- lecture-notes/02-csv-and-json.md
- lecture-notes/03-exceptions-and-logging.md
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

# ----------------------------------------------------------------------
# Logging setup
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s | %(name)s | %(message)s",
)
log = logging.getLogger("analyzer")


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
# A log line looks like:
#   2026-05-13 14:30:01 ERROR    Failed to connect to cache: timeout
# Capture groups: date, time, level, message.
LINE_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|ERROR)\s+"
    r"(?P<message>.+)$"
)

KNOWN_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


# ----------------------------------------------------------------------
# Parsing
# ----------------------------------------------------------------------
def parse_line(line: str) -> Optional[dict]:
    """Parse a single log line.

    Returns a dict with keys 'date', 'time', 'level', 'message' on success,
    or None if the line does not match the expected format.
    """
    # TODO: strip the line, match against LINE_RE, return groupdict() or None.
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    return m.groupdict()


# ----------------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------------
def analyze(records: list[dict], source_name: str, total_lines: int) -> dict:
    """Build the summary dict from a list of parsed records.

    The returned dict matches the schema described in mini-project/README.md.
    """
    # TODO: count records per level using Counter.
    # TODO: find the most common ERROR message (or None if no errors).
    # TODO: return the assembled summary dict.

    level_counts: Counter[str] = Counter()
    error_messages: Counter[str] = Counter()

    for rec in records:
        lvl = rec["level"]
        level_counts[lvl] += 1
        if lvl == "ERROR":
            error_messages[rec["message"]] += 1

    # Make sure every known level appears in the summary, even if zero.
    counts = {lvl: level_counts.get(lvl, 0) for lvl in KNOWN_LEVELS}

    most_common_error: Optional[dict] = None
    if error_messages:
        msg, count = error_messages.most_common(1)[0]
        most_common_error = {"message": msg, "count": count}

    return {
        "source_file": source_name,
        "total_lines": total_lines,
        "parsed_lines": len(records),
        "skipped_lines": total_lines - len(records),
        "counts": counts,
        "most_common_error": most_common_error,
    }


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------
def write_summary(summary: dict, path: Path) -> None:
    """Write the summary dict to `path` as pretty-printed JSON."""
    # TODO: open path for write with encoding="utf-8" and json.dump with indent=2.
    with path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")


def write_csv(summary: dict, path: Path) -> None:
    """Write a level,count CSV report to `path`."""
    # TODO: open path for write with newline="" and encoding="utf-8".
    # TODO: write the header row, then one row per known level.
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["level", "count"])
        for level in sorted(summary["counts"]):
            writer.writerow([level, summary["counts"][level]])


# ----------------------------------------------------------------------
# File reading with graceful skipping
# ----------------------------------------------------------------------
def read_records(path: Path) -> tuple[list[dict], int]:
    """Read and parse `path` line by line.

    Returns (records, total_lines).  Lines that fail to parse are logged
    at WARNING level and skipped.
    """
    records: list[dict] = []
    total = 0
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            total += 1
            parsed = parse_line(line)
            if parsed is None:
                # Empty lines are common and not worth warning about.
                if line.strip():
                    log.warning("skipping malformed line %d: %r", lineno, line.strip())
                continue
            records.append(parsed)
    return records, total


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze a .log file.")
    parser.add_argument("log_file", type=Path, help="Path to the .log file to analyze.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("reports"),
        help="Directory to write summary.json and by-level.csv (default: reports/).",
    )
    args = parser.parse_args(argv)

    try:
        records, total = read_records(args.log_file)
    except FileNotFoundError:
        log.error("input file not found: %s", args.log_file)
        return 1
    except PermissionError:
        log.error("permission denied: %s", args.log_file)
        return 1

    summary = analyze(records, source_name=args.log_file.name, total_lines=total)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.out_dir / "summary.json"
    csv_path = args.out_dir / "by-level.csv"

    write_summary(summary, summary_path)
    write_csv(summary, csv_path)

    err = summary["most_common_error"]
    if err:
        print(
            f"Parsed {summary['parsed_lines']}/{summary['total_lines']} lines. "
            f"Top error: {err['message']!r} ({err['count']}x)."
        )
    else:
        print(
            f"Parsed {summary['parsed_lines']}/{summary['total_lines']} lines. "
            f"No errors found."
        )
    print(f"Reports written to {summary_path} and {csv_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
