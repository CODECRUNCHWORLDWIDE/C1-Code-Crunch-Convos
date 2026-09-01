"""The command-line entry point.

Everything that touches ``sys.argv``, ``stdout``, ``stderr`` or the process exit
code lives here and nowhere else. That is the whole reason the other four
modules need no ``capsys`` and no ``monkeypatch`` — they cannot print, so there
is nothing to capture.

:func:`main` takes *argv* as an argument instead of reading ``sys.argv``
directly, and returns an exit code instead of calling ``sys.exit``. Those two
choices are what let a test call ``main(["sample.log", "--out-dir", str(tmp)])``
like an ordinary function and assert on the return value.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from loganalyzer.analysis import build_summary, filter_min_level
from loganalyzer.models import LEVELS, LogRecord
from loganalyzer.parsing import read_records
from loganalyzer.reporting import write_reports

__all__ = ["PROG", "build_parser", "main"]

#: The name that appears in ``--help`` and in error messages. Week 6 printed
#: ``analyzer.py: error: ...`` because the script *was* ``analyzer.py``; the
#: package is invoked as ``python -m loganalyzer``, so the prefix moved with it.
#: That is the only observable change the refactor made.
PROG = "loganalyzer"

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser.

    Split out from :func:`main` so a test can inspect defaults and rejections
    without running the program.
    """
    parser = argparse.ArgumentParser(prog=PROG, description="Summarize one or more log files.")
    parser.add_argument("logs", nargs="+", type=Path, metavar="LOG")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("reports"),
        help="directory to write the reports into (default: reports)",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="add first_timestamp/last_timestamp to the JSON summary",
    )
    parser.add_argument("--by-hour", action="store_true", help="also write by-hour.csv")
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
    parser.add_argument("-v", "--verbose", action="store_true", help="log at DEBUG level")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the analyzer. Returns the process exit code: 0 on success, 1 on error."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)-8s %(name)s  %(message)s",
    )

    paths: list[Path] = args.logs
    records: list[LogRecord] = []
    total_lines = 0
    for path in paths:
        try:
            file_records, file_lines = read_records(path)
        except FileNotFoundError:
            print(f"{PROG}: error: log file not found: {path}", file=sys.stderr)
            return 1
        except PermissionError:
            print(f"{PROG}: error: cannot read {path}: permission denied", file=sys.stderr)
            return 1
        records.extend(file_records)
        total_lines += file_lines

    if args.min_level:
        before = len(records)
        records = filter_min_level(records, args.min_level)
        logger.info("dropped %d entries below %s", before - len(records), args.min_level)

    source: str | list[str] = paths[0].name if len(paths) == 1 else [p.name for p in paths]
    summary = build_summary(
        source,
        records,
        total_lines,
        timestamps=args.timestamps,
        error_limit=args.top_errors,
    )

    summary_path, level_path = write_reports(summary, records, args.out_dir, by_hour=args.by_hour)

    top = summary["most_common_error"]
    top_text = f"'{top['message']}' ({top['count']}x)" if top else "none"
    print(
        f"Parsed {summary['parsed_lines']}/{summary['total_lines']} lines. "
        f"Top error: {top_text}."
    )
    print(f"Reports written to {summary_path.as_posix()} and {level_path.as_posix()}.")
    return 0
