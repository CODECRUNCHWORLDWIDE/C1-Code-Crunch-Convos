"""Log file analyzer — reference solution for Week 6's mini-project.

Reads one or more plain-text log files, counts entries per level, finds the most
common ERROR message, and writes a JSON summary plus a CSV breakdown.

Base usage (matches the mini-project spec exactly):

    python analyzer.py sample.log --out-dir reports/

Stretch-goal flags are all opt-in so that the default output stays byte-for-byte
identical to the spec:

    --timestamps        add first_timestamp / last_timestamp to the JSON summary
    --by-hour           also write <out-dir>/by-hour.csv with hour,count
    --min-level LEVEL   ignore entries below LEVEL entirely
    --top-errors N      add a top_errors array (N most common ERROR messages)

Multiple log files and .gz inputs are supported without a flag:

    python analyzer.py app.log app.log.1.gz --out-dir reports/

Standard library only. Python 3.10+.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path
from typing import IO

log = logging.getLogger("analyzer")

#: Levels in severity order. The JSON summary reports counts in this order; the
#: CSV report sorts them alphabetically (that is what the spec's example shows).
LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR")

#: One log entry: date, time, level, then a free-form message that may contain
#: anything at all — including whitespace, which is why the message group is the
#: last thing in the pattern and simply runs to end of line.
LINE_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})"
    r"\s+(?P<time>\d{2}:\d{2}:\d{2})"
    r"\s+(?P<level>DEBUG|INFO|WARNING|ERROR)"
    r"\s+(?P<message>\S.*?)\s*$"
)


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #
def parse_line(line: str) -> dict[str, str] | None:
    """Parse one log line into a record dict, or return None if it is malformed.

    A record has the keys ``date``, ``time``, ``level`` and ``message``.
    Returning ``None`` rather than raising keeps the caller's loop flat: a
    malformed line is expected input, not an exceptional condition.
    """
    match = LINE_RE.match(line)
    if match is None:
        return None
    return match.groupdict()


def open_log(path: Path) -> IO[str]:
    """Open *path* for reading as text, transparently decompressing ``.gz``.

    Both objects are context managers yielding ``str`` lines, so the caller does
    not need to care which one it got.
    """
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def read_records(path: Path) -> tuple[list[dict[str, str]], int]:
    """Return ``(records, total_lines)`` for the log file at *path*.

    Malformed lines are logged as warnings (with their line number) and skipped.
    Iterating the file object keeps memory flat regardless of file size.
    """
    records: list[dict[str, str]] = []
    total_lines = 0
    with open_log(path) as f:
        for lineno, line in enumerate(f, start=1):
            total_lines = lineno
            if not line.strip():
                # A blank line is not an entry; count it as skipped like any
                # other unparseable line, but do not shout about it.
                log.warning("%s:%d: skipping blank line", path.name, lineno)
                continue
            record = parse_line(line)
            if record is None:
                log.warning(
                    "%s:%d: skipping malformed line: %s",
                    path.name,
                    lineno,
                    line.rstrip("\n"),
                )
                continue
            records.append(record)
    return records, total_lines


# --------------------------------------------------------------------------- #
# Analysis
# --------------------------------------------------------------------------- #
def analyze(records: list[dict[str, str]]) -> dict:
    """Compute the level counts and the most common ERROR message.

    Returns a dict with the keys ``counts`` and ``most_common_error``. The
    file-level fields (``source_file`` and the line tallies) are added by
    :func:`build_summary`, which is the only place that knows about files.
    """
    counts = {level: 0 for level in LEVELS}
    for record in records:
        counts[record["level"]] += 1

    errors = Counter(r["message"] for r in records if r["level"] == "ERROR")
    most_common_error: dict | None = None
    if errors:
        message, count = errors.most_common(1)[0]
        most_common_error = {"message": message, "count": count}

    return {"counts": counts, "most_common_error": most_common_error}


def build_summary(
    source: str | list[str],
    records: list[dict[str, str]],
    total_lines: int,
    *,
    timestamps: bool = False,
    top_errors: int = 0,
) -> dict:
    """Assemble the full summary dict, in the key order the spec shows."""
    summary: dict = {
        "source_file": source,
        "total_lines": total_lines,
        "parsed_lines": len(records),
        "skipped_lines": total_lines - len(records),
        **analyze(records),
    }

    if timestamps:
        stamps = sorted(f"{r['date']} {r['time']}" for r in records)
        summary["first_timestamp"] = stamps[0] if stamps else None
        summary["last_timestamp"] = stamps[-1] if stamps else None

    if top_errors > 0:
        errors = Counter(r["message"] for r in records if r["level"] == "ERROR")
        summary["top_errors"] = [
            {"message": message, "count": count}
            for message, count in errors.most_common(top_errors)
        ]

    return summary


def hourly_counts(records: list[dict[str, str]]) -> Counter[str]:
    """Count entries per ``YYYY-MM-DD HH`` bucket."""
    return Counter(f"{r['date']} {r['time'][:2]}" for r in records)


def filter_min_level(
    records: list[dict[str, str]], min_level: str
) -> list[dict[str, str]]:
    """Drop records whose level is less severe than *min_level*."""
    threshold = LEVELS.index(min_level)
    return [r for r in records if LEVELS.index(r["level"]) >= threshold]


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def write_summary(summary: dict, path: Path) -> None:
    """Write *summary* as pretty-printed JSON to *path*."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")


def write_csv(summary: dict, path: Path) -> None:
    """Write the per-level counts as ``level,count`` rows, sorted by level."""
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["level", "count"])
        for level in sorted(summary["counts"]):
            writer.writerow([level, summary["counts"][level]])


def write_hourly_csv(records: list[dict[str, str]], path: Path) -> None:
    """Write ``hour,count`` rows, sorted chronologically. (Stretch goal 2.)"""
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hour", "count"])
        for hour, count in sorted(hourly_counts(records).items()):
            writer.writerow([hour, count])


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="analyzer.py",
        description="Summarize one or more log files.",
    )
    parser.add_argument("logs", nargs="+", type=Path, metavar="LOG")
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="add first_timestamp/last_timestamp to the JSON summary",
    )
    parser.add_argument(
        "--by-hour", action="store_true", help="also write by-hour.csv"
    )
    parser.add_argument(
        "--min-level",
        choices=LEVELS,
        help="ignore entries below this level entirely",
    )
    parser.add_argument(
        "--top-errors",
        type=int,
        default=0,
        metavar="N",
        help="add a top_errors array with the N most common ERROR messages",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="log at DEBUG level"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the analyzer. Returns the process exit code."""
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)-8s %(name)s  %(message)s",
    )

    records: list[dict[str, str]] = []
    total_lines = 0
    for path in args.logs:
        try:
            file_records, file_lines = read_records(path)
        except FileNotFoundError:
            print(f"analyzer.py: error: log file not found: {path}", file=sys.stderr)
            return 1
        except PermissionError:
            print(f"analyzer.py: error: cannot read {path}: permission denied",
                  file=sys.stderr)
            return 1
        records.extend(file_records)
        total_lines += file_lines

    if args.min_level:
        before = len(records)
        records = filter_min_level(records, args.min_level)
        log.info("dropped %d entries below %s", before - len(records), args.min_level)

    source: str | list[str]
    source = args.logs[0].name if len(args.logs) == 1 else [p.name for p in args.logs]
    summary = build_summary(
        source,
        records,
        total_lines,
        timestamps=args.timestamps,
        top_errors=args.top_errors,
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.out_dir / "summary.json"
    csv_path = args.out_dir / "by-level.csv"
    write_summary(summary, summary_path)
    write_csv(summary, csv_path)
    if args.by_hour:
        write_hourly_csv(records, args.out_dir / "by-hour.csv")

    top = summary["most_common_error"]
    top_text = f"'{top['message']}' ({top['count']}x)" if top else "none"
    print(
        f"Parsed {summary['parsed_lines']}/{summary['total_lines']} lines. "
        f"Top error: {top_text}."
    )
    print(
        f"Reports written to {summary_path.as_posix()} "
        f"and {csv_path.as_posix()}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
