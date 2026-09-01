# Mini-Project — Log File Analyzer

> **Topic:** turning a messy text log into two clean report files, without falling over on the messy parts
> **Lecture:** [Lecture 01 — Files and pathlib](../lecture-notes/01-files-and-pathlib.md) · [Lecture 02 — CSV and JSON](../lecture-notes/02-csv-and-json.md) · [Lecture 03 — Exceptions and Logging](../lecture-notes/03-exceptions-and-logging.md)
> **Difficulty:** Advanced
> **Target time:** 6 hours
> **Why this one:** it is the week's capstone and it uses every topic at once — files, `pathlib`, a little regular expression work, CSV, JSON, narrow exception handling and `logging`. More than that, it is the first program you write whose input is *hostile*: real log files contain lines your parser has never heard of, and the tool is only finished when those lines are a warning rather than a crash.

<!-- no-runnable-file: this page is the project brief, and the project's deliverable is a folder in your own repository holding a script, two report files it produced, and a commit history. The runnable answer is log_analyzer.py, which ships beside this page and is linked from Download and run. It is named after the project rather than the page because a file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

A log file is what a program writes down about its own day. One line per
thing that happened, oldest first:

```text
2026-05-13 14:30:01 INFO     Connection opened to db-primary
2026-05-13 14:30:02 WARNING  Slow query: SELECT * FROM users (1.2s)
2026-05-13 14:30:03 ERROR    Failed to connect to cache: timeout
```

Four fields on each line:

1. **Date** — `YYYY-MM-DD`
2. **Time** — `HH:MM:SS`
3. **Level** — `INFO`, `WARNING`, `ERROR` or `DEBUG`
4. **Message** — free-form text, which may contain anything, including
   spaces

The fields are separated by whitespace, but the *message* can contain
whitespace too. That one sentence is the whole difficulty of the parsing.

Nobody reads thirty thousand of those lines. You are building the tool
that reads them for you and answers three questions: how many of each
level, what is the single most common error, and how much of the file
did we fail to understand.

```bash
python analyzer.py sample.log --out-dir reports/
```

It writes two files. `reports/summary.json`, for a program to read:

```json
{
  "source_file": "sample.log",
  "total_lines": 30,
  "parsed_lines": 28,
  "skipped_lines": 2,
  "counts": {
    "DEBUG": 0,
    "INFO": 18,
    "WARNING": 6,
    "ERROR": 4
  },
  "most_common_error": {
    "message": "Failed to connect to cache: timeout",
    "count": 2
  }
}
```

And `reports/by-level.csv`, for a spreadsheet:

```text
level,count
DEBUG,0
ERROR,4
INFO,18
WARNING,6
```

Then it prints one line to the screen saying what it did.

**The part that makes it a real tool.** Actual log files are not tidy.
They contain rotation banners, blank lines, stack traces spilling over
several lines, and entries from a logging level your tool has never
heard of. A line your parser cannot read is **not** an error in the file
and **not** an error in your program — it is normal input. Log a WARNING
naming the line number, skip it, and carry on. A tool that stops at the
first strange line is not finished.

## Starter

There is no separate starter file for this project — the stubs below are
the whole of the scaffolding, and they are the shape the finished tool
takes. Save this as `analyzer.py` in your project folder and fill in the
`TODO`s. It runs as pasted; it just reports that every line is
malformed:

```python
"""Summarize a log file: counts per level, top error, JSON and CSV reports."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path

log = logging.getLogger("analyzer")

LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR")

# TODO: a pattern with named groups for date, time, level and message
LINE_RE = re.compile(r"^(?P<date>NOPE)$")


def parse_line(line: str) -> dict[str, str] | None:
    """Parse one log line into a record dict, or return None if malformed.

    Args:
        line: One line of the log file.

    Returns:
        A dict with date, time, level and message, or None.
    """
    match = LINE_RE.match(line)
    if match is None:
        return None
    return match.groupdict()


def read_records(path: Path) -> tuple[list[dict[str, str]], int]:
    """Return (records, total_lines) for the log file at `path`."""
    records: list[dict[str, str]] = []
    total_lines = 0
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            total_lines = lineno
            record = parse_line(line)
            if record is None:
                # TODO: log a WARNING naming the file, the line number and
                #       the offending line, then skip it
                continue
            records.append(record)
    return records, total_lines


def analyze(records: list[dict[str, str]]) -> dict:
    """Compute the level counts and the most common ERROR message."""
    counts = {level: 0 for level in LEVELS}
    # TODO: count each record's level
    # TODO: build a Counter of ERROR messages and take the most common one,
    #       guarding against there being none at all
    most_common_error: dict | None = None
    return {"counts": counts, "most_common_error": most_common_error}


def build_summary(
    source: str, records: list[dict[str, str]], total_lines: int
) -> dict:
    """Assemble the full summary dict, in the key order the brief shows."""
    return {
        "source_file": source,
        "total_lines": total_lines,
        "parsed_lines": len(records),
        "skipped_lines": total_lines - len(records),
        **analyze(records),
    }


def write_summary(summary: dict, path: Path) -> None:
    """Write `summary` as pretty-printed JSON to `path`."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")


def write_csv(summary: dict, path: Path) -> None:
    """Write the per-level counts as level,count rows, sorted by level."""
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["level", "count"])
        # TODO: one row per level, in alphabetical order


def main(argv: list[str]) -> int:
    """Run the analyzer. Returns the process exit code."""
    parser = argparse.ArgumentParser(prog="analyzer.py")
    parser.add_argument("logs", nargs="+", type=Path, metavar="LOG")
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)-8s %(name)s  %(message)s"
    )

    # TODO: read each log, catching FileNotFoundError with a friendly
    #       message and returning 1
    records, total_lines = read_records(args.logs[0])

    summary = build_summary(args.logs[0].name, records, total_lines)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_summary(summary, args.out_dir / "summary.json")
    write_csv(summary, args.out_dir / "by-level.csv")

    top = summary["most_common_error"]
    top_text = f"'{top['message']}' ({top['count']}x)" if top else "none"
    print(f"Parsed {summary['parsed_lines']}/{summary['total_lines']} lines. "
          f"Top error: {top_text}.")
    print("Reports written to "
          f"{(args.out_dir / 'summary.json').as_posix()} and "
          f"{(args.out_dir / 'by-level.csv').as_posix()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

You need a log file to point it at. The shipped answer carries its own
thirty-line sample as a string constant, and this command pulls it out
into a real file beside you:

```bash
python -c "
from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('a', 'log_analyzer.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
Path('sample.log').write_text(m.SAMPLE_LOG, encoding='utf-8')
print('wrote sample.log')
"
python analyzer.py sample.log --out-dir reports/
```

**No setup needed — you can build this one in the browser.** Open the starter in the [online code editor](../../../README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The tool takes one or more log paths and an `--out-dir`, parsed with
   `argparse` and converted to `Path` objects.
2. It parses the log line by line, streaming — never `readlines()`.
3. A line that does not match the entry format logs a WARNING naming the
   file and the 1-based line number, and is skipped.
4. It counts entries per level, and every one of `DEBUG`, `INFO`,
   `WARNING`, `ERROR` appears in the output even when its count is zero.
5. It identifies the most common `ERROR` message and how many times it
   occurred, and copes with a log that has no errors at all.
6. It writes `<out-dir>/summary.json` with `json.dump(..., indent=2)`,
   in the key order the brief shows.
7. It writes `<out-dir>/by-level.csv` with `csv.writer`, sorted
   alphabetically by level.
8. It creates the output directory if it does not exist.
9. A missing input file prints a friendly one-line message and exits
   with code 1 — no traceback.
10. Every function has type hints and a docstring.

## Constraints

- **Standard library only, Python 3.10 or newer.** Everything this needs
  is already installed.
- **`pathlib.Path` for every path.** No string concatenation, no
  `os.path.join`. `argparse` will build them for you with `type=Path`.
- **`logging` for diagnostics, `print` for results.** The two summary
  lines at the end are the result and belong on stdout. Every skip
  warning is a diagnostic and belongs on stderr. That split is what makes
  `python analyzer.py app.log > run.txt` behave sensibly.
- **`csv.writer` for the CSV and `json.dump` for the JSON.** Do not
  build either format with f-strings. A message containing a comma will
  find you.
- **Catch specific exceptions, and let one specific thing crash.**
  - `FileNotFoundError` on the input → friendly message, exit 1.
  - A malformed line → WARNING, carry on.
  - `re.error` from a broken pattern → **let it crash.** That is your
    bug, not the user's data, and the traceback is the fastest way to
    find it.
- **`parse_line` returns `None` for a bad line rather than raising.** A
  malformed line is expected input, and exceptions are for the
  unexpected. This is the decision that shapes the rest of the program,
  and the reasoning is spelled out under **The Solution**.

## Expected output

The shipped answer runs a demo when you give it no arguments: it writes
its own thirty-line sample log into a scratch folder, analyzes it there,
and prints both report files so you can see them without opening
anything.

```bash
$ python log_analyzer.py
```

```text
Parsed 28/30 lines. Top error: 'Failed to connect to cache: timeout' (2x).
Reports written to reports/summary.json and reports/by-level.csv.

reports/summary.json:
{
  "source_file": "sample.log",
  "total_lines": 30,
  "parsed_lines": 28,
  "skipped_lines": 2,
  "counts": {
    "DEBUG": 0,
    "INFO": 18,
    "WARNING": 6,
    "ERROR": 4
  },
  "most_common_error": {
    "message": "Failed to connect to cache: timeout",
    "count": 2
  }
}

reports/by-level.csv:
level,count
DEBUG,0
ERROR,4
INFO,18
WARNING,6
```

The two skip warnings went to stderr, where diagnostics belong:

```console
WARNING  analyzer  sample.log:7: skipping malformed line: -- log rotated by logrotate at 14:30:05 --
WARNING  analyzer  sample.log:23: skipping malformed line: 2026-05-13 14:31:07 TRACE    entering render loop
```

Check the arithmetic yourself. `18 + 6 + 4 = 28` parsed, and
`30 - 28 = 2` skipped — the two lines the warnings named. Line 7 is a
rotation banner and line 23 has a level, `TRACE`, that this tool does not
support.

Given a real path it behaves exactly as the brief describes:

```bash
python log_analyzer.py sample.log --out-dir reports/
```

And the missing-file path:

```bash
python log_analyzer.py nope.log --out-dir reports/
echo "exit=$?"
```

One line, no traceback, exit 1:

```console
analyzer.py: error: log file not found: nope.log
exit=1
```

## Steps

Build it bottom-up, in the order the data flows. That is also the order
it is easiest to test, because each stage can be checked on its own
before the next one exists.

1. **Get the regular expression right first, in a REPL.** Before you
   open a single file. Write `LINE_RE`, then feed `parse_line` the six
   strings under **Common bugs to catch** and check each answer. Five
   minutes here saves an hour later.
2. **Then `read_records`.** A file in, a list of records and a line
   count out. Add the WARNING with `enumerate(f, start=1)` so the line
   numbers match what your editor shows.
3. **Then `analyze` and `build_summary`.** Pure data — no files, no
   paths. Seed the counts from `LEVELS` so `DEBUG: 0` is present, and
   guard the most-common-error lookup against there being none.
4. **Then the two writers.** Compare your `summary.json` against the
   brief's example key by key, and your CSV row by row.
5. **Then `main`.** Read it last, write it last. It is only glue, and
   glue makes no sense until you know what it is gluing.
6. **Now break it on purpose.** Point it at a file that does not exist.
   You want one friendly line and exit 1, not eleven lines of
   traceback.
7. **Then check the reports really are valid**, rather than trusting
   your eyes:

   ```bash
   python -c "import json; print(json.load(open('reports/summary.json', encoding='utf-8')))"
   python -c "import csv; print(list(csv.DictReader(open('reports/by-level.csv', newline='', encoding='utf-8'))))"
   ```

8. **Commit as you go**, one commit per stage, not one at the end. The
   history is part of what you hand in.

## The Solution

The reference answer is one file. It keeps the five function names the
brief suggests, adds three more, and implements all six stretch goals as
opt-in flags so the default run stays byte-for-byte what the brief asks
for.

```python
"""Log file analyzer — the finished answer to Week 6's mini-project.

Reads one or more plain-text log files, counts entries per level, finds the most
common ERROR message, and writes a JSON summary plus a CSV breakdown.

Base usage (matches the mini-project spec exactly):

    python log_analyzer.py sample.log --out-dir reports/

Stretch-goal flags are all opt-in so that the default output stays byte-for-byte
identical to the spec:

    --timestamps        add first_timestamp / last_timestamp to the JSON summary
    --by-hour           also write <out-dir>/by-hour.csv with hour,count
    --min-level LEVEL   ignore entries below LEVEL entirely
    --top-errors N      add a top_errors array (N most common ERROR messages)

Multiple log files and .gz inputs are supported without a flag:

    python log_analyzer.py app.log app.log.1.gz --out-dir reports/

Run it with no arguments and it writes its own sample log into a scratch folder
and analyzes that, so the download works from a clean checkout with no data
placed by hand.

Save your own copy as ``analyzer.py`` in your project folder.

Standard library only. Python 3.10+.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import logging
import os
import re
import sys
import tempfile
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

#: Thirty lines of realistic input: 28 well-formed entries, a rotation banner on
#: line 7, and a TRACE level on line 23 that this tool does not support. The
#: demo writes this to a scratch folder so the download has something to read.
SAMPLE_LOG = """\
2026-05-13 14:30:01 INFO     Connection opened to db-primary
2026-05-13 14:30:01 INFO     Worker pool started with 4 workers
2026-05-13 14:30:02 WARNING  Slow query: SELECT * FROM users (1.2s)
2026-05-13 14:30:03 ERROR    Failed to connect to cache: timeout
2026-05-13 14:30:03 INFO     Retrying cache connection (attempt 1/3)
2026-05-13 14:30:04 INFO     Cache connection established
-- log rotated by logrotate at 14:30:05 --
2026-05-13 14:30:06 INFO     GET /health 200 3ms
2026-05-13 14:30:07 INFO     GET /api/users 200 41ms
2026-05-13 14:30:08 WARNING  Request body larger than 1 MB; truncating
2026-05-13 14:30:09 INFO     POST /api/users 201 88ms
2026-05-13 14:30:11 INFO     GET /api/users/42 200 12ms
2026-05-13 14:30:12 ERROR    Payment gateway returned 502
2026-05-13 14:30:12 WARNING  Falling back to secondary payment provider
2026-05-13 14:30:13 INFO     Payment 8f21 captured via secondary provider
2026-05-13 14:30:15 INFO     Scheduled job nightly-report queued
2026-05-13 14:31:00 INFO     Scheduled job nightly-report started
2026-05-13 14:31:02 WARNING  Slow query: SELECT * FROM events (2.9s)
2026-05-13 14:31:04 ERROR    Failed to connect to cache: timeout
2026-05-13 14:31:04 INFO     Retrying cache connection (attempt 1/3)
2026-05-13 14:31:05 INFO     Cache connection established
2026-05-13 14:31:06 INFO     Scheduled job nightly-report finished in 6s
2026-05-13 14:31:07 TRACE    entering render loop
2026-05-13 14:31:09 INFO     GET /reports/nightly 200 210ms
2026-05-13 14:31:10 WARNING  Disk usage at 81% on /var/log
2026-05-13 14:31:12 ERROR    Unhandled exception in worker 3
2026-05-13 14:31:12 WARNING  Worker 3 restarted
2026-05-13 14:31:14 INFO     Worker 3 healthy
2026-05-13 14:31:20 INFO     Connection closed to db-primary
2026-05-13 14:31:21 INFO     Shutdown complete
"""


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #
def parse_line(line: str) -> dict[str, str] | None:
    """Parse one log line into a record dict, or return None if it is malformed.

    A record has the keys ``date``, ``time``, ``level`` and ``message``.
    Returning ``None`` rather than raising keeps the caller's loop flat: a
    malformed line is expected input, not an exceptional condition.

    Args:
        line: One line of the log file, newline included or not.

    Returns:
        The record, or None if the line does not match the entry format.
    """
    match = LINE_RE.match(line)
    if match is None:
        return None
    return match.groupdict()


def open_log(path: Path) -> IO[str]:
    """Open *path* for reading as text, transparently decompressing ``.gz``.

    Both objects are context managers yielding ``str`` lines, so the caller does
    not need to care which one it got.

    Args:
        path: The log file to open.

    Returns:
        An open text-mode file object.
    """
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def read_records(path: Path) -> tuple[list[dict[str, str]], int]:
    """Return ``(records, total_lines)`` for the log file at *path*.

    Malformed lines are logged as warnings (with their line number) and skipped.
    Iterating the file object keeps memory flat regardless of file size.

    Args:
        path: The log file to read.

    Returns:
        The parsed records, and how many lines the file held in total.
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

    Args:
        records: The parsed log entries.

    Returns:
        A dict with ``counts`` and ``most_common_error``.
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
    """Assemble the full summary dict, in the key order the spec shows.

    Args:
        source: The input filename, or a list of them.
        records: The parsed log entries.
        total_lines: How many lines the inputs held in total.
        timestamps: Add first and last timestamps (stretch goal 1).
        top_errors: Add the N most common errors (stretch goal 6).

    Returns:
        The summary dict, ready to be written as JSON.
    """
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
    """Count entries per ``YYYY-MM-DD HH`` bucket.

    Args:
        records: The parsed log entries.

    Returns:
        A counter keyed by hour bucket.
    """
    return Counter(f"{r['date']} {r['time'][:2]}" for r in records)


def filter_min_level(
    records: list[dict[str, str]], min_level: str
) -> list[dict[str, str]]:
    """Drop records whose level is less severe than *min_level*.

    Args:
        records: The parsed log entries.
        min_level: The lowest level to keep.

    Returns:
        The records at or above *min_level*.
    """
    threshold = LEVELS.index(min_level)
    return [r for r in records if LEVELS.index(r["level"]) >= threshold]


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def write_summary(summary: dict, path: Path) -> None:
    """Write *summary* as pretty-printed JSON to *path*.

    Args:
        summary: The summary dict.
        path: The file to write.
    """
    with path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")


def write_csv(summary: dict, path: Path) -> None:
    """Write the per-level counts as ``level,count`` rows, sorted by level.

    Args:
        summary: The summary dict.
        path: The file to write.
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["level", "count"])
        for level in sorted(summary["counts"]):
            writer.writerow([level, summary["counts"][level]])


def write_hourly_csv(records: list[dict[str, str]], path: Path) -> None:
    """Write ``hour,count`` rows, sorted chronologically. (Stretch goal 2.)

    Args:
        records: The parsed log entries.
        path: The file to write.
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hour", "count"])
        for hour, count in sorted(hourly_counts(records).items()):
            writer.writerow([hour, count])


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Turn the command line into the options the analyzer needs.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The parsed options.
    """
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


def run(argv: list[str]) -> int:
    """Analyze the logs named in *argv* and write the reports.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The process exit code.
    """
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
            print(
                f"analyzer.py: error: cannot read {path}: permission denied",
                file=sys.stderr,
            )
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
        f"Reports written to {summary_path.as_posix()} and {csv_path.as_posix()}."
    )
    return 0


def _demo() -> int:
    """Write the sample log into a scratch folder and analyze it there.

    The scratch folder is a temporary directory this function makes and
    deletes, so the download needs no data placed by hand and leaves nothing
    behind. It changes into that folder first, so the paths in the output are
    the short ones the spec's example shows.

    Returns:
        The exit code of the analysis run.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="log_analyzer_") as scratch:
        try:
            os.chdir(scratch)
            Path("sample.log").write_text(SAMPLE_LOG, encoding="utf-8")
            code = run(["sample.log", "--out-dir", "reports"])
            print()
            print("reports/summary.json:")
            print(Path("reports/summary.json").read_text(encoding="utf-8"), end="")
            print()
            print("reports/by-level.csv:")
            print(Path("reports/by-level.csv").read_text(encoding="utf-8"), end="")
        finally:
            os.chdir(home)
    return code


def main(argv: list[str] | None = None) -> int:
    """Run the analyzer, or the built-in demo when no logs are named.

    Args:
        argv: Command-line arguments, without the program name. ``None`` means
            read them from ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return _demo()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

**Why it works.**

**The whole program is a pipeline, and every stage has one kind of input
and one kind of output.**

```text
str            parse_line       dict | None
Path           read_records     (list[dict], int)
list[dict]     analyze          dict
list[dict]     build_summary    dict
dict           write_summary    -> summary.json
dict           write_csv        -> by-level.csv
list[str]      run              int
```

That is not decoration. Three things fall out of it, and they are why
this program is pleasant to work on.

*Every stage can be tested without a file.* `parse_line` takes a string
and gives back a dict, so you can check a hundred awkward inputs in a
REPL with no fixtures at all. Only `read_records` touches the disk for
input, and only the two writers touch it for output.

*The layer that knows about files is separate from the layer that knows
about counting.* `analyze` has never heard of a path. `build_summary` is
the only function that knows the summary has a `source_file` key. That
split is why aggregating several files — stretch goal 3 — needed no
change to `analyze` at all.

*Diagnostics go to `logging`, results go to `print`.* Exactly two calls
to `print` on the success path, and everything else through the
module-level `log`.

**The one decision that shapes everything else: `parse_line` returns
`None` instead of raising.**

Raising a `MalformedLineError` would be defensible. It is what
[challenge 02](../challenges/challenge-02-config-validator.md) does for
a bad config file, and it is what you would want if a malformed line
meant the whole file was corrupt.

But it does not mean that. Real log files contain rotation markers,
banners, stack traces and levels your regular expression has never heard
of. A malformed line is not an exceptional condition — it is **expected
input**, and exceptions are for the unexpected. Using them for the
routine case costs you twice: the caller's loop grows a `try` around
every iteration, and raising is genuinely expensive when it happens
thousands of times on a big file.

So `None` is a *value* meaning "not an entry", and the caller's
`if record is None: log.warning(...); continue` is three lines of
ordinary control flow. Meanwhile the things that genuinely *are*
exceptional — a missing file, an unreadable one — do raise, and `run`
catches them.

That is this week's three-way question applied to one project:

| Failure | Decision | Where |
|---|---|---|
| A line does not match the format | skip it and say so | `read_records`: `log.warning`, `continue` |
| The input file does not exist | stop and explain | `run`: `except FileNotFoundError`, `return 1` |
| The pattern itself is malformed | let it crash | nothing catches `re.error` |

**The regular expression is the hard part, and every piece of it is
answering something the brief said.**

```python
LINE_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})"
    r"\s+(?P<time>\d{2}:\d{2}:\d{2})"
    r"\s+(?P<level>DEBUG|INFO|WARNING|ERROR)"
    r"\s+(?P<message>\S.*?)\s*$"
)
```

- **`^...$` with `.match()`.** Anchored at both ends, so a line with
  junk before the date or after the message does not half-match.
- **`\d{4}-\d{2}-\d{2}`, not `\S+`.** The brief defines the date shape
  exactly. Matching the shape means a rotation banner is rejected on its
  very first token rather than dragged through the whole pattern.
- **`\s+` between fields, never a literal space.** The brief says
  "separated by whitespace", and the sample pads the level to a fixed
  width — `INFO` is followed by five spaces and `WARNING` by two.
- **`DEBUG|INFO|WARNING|ERROR`, not `\w+`.** This is the important one.
  Spelling out the four levels means a `TRACE` line is *rejected and
  reported*, which is what the brief asks for. `\w+` would accept
  `TRACE` happily, and then `counts[record["level"]] += 1` raises
  `KeyError: 'TRACE'` several functions away from the actual problem.

  It also handles something you did not think of. Try
  `2026-05-13 14:30:01 INFOX  hello`: the alternation matches `INFO`,
  then `\s+` demands whitespace and finds `X`, so the match fails and
  there is no other alternative to try. Correctly rejected. A `\w+`
  level group would have parsed the level as `INFOX`.
- **`(?P<message>\S.*?)\s*$`.** The message is free-form, so it runs to
  the end of the line. The leading `\S` requires at least one non-space
  character, so a line with a level and no message is malformed rather
  than an entry with an empty message. The lazy `.*?` with `\s*$` strips
  trailing whitespace and the newline without a separate `.strip()`. And
  `.` does not match a newline by default, so the pattern cannot run
  past the end of the line.
- **Named groups.** `match.groupdict()` hands back
  `{"date": ..., "time": ..., "level": ..., "message": ...}` in one
  call. That is the entire body of `parse_line` after the `None` check.

**The counts are seeded, not accumulated.** `{level: 0 for level in
LEVELS}` means `DEBUG` appears with a count of zero even though the
sample has no DEBUG lines. A `Counter` built from the records alone
would leave the key out, the CSV would have three rows instead of four,
and anything downstream — a spreadsheet, a dashboard, a diff against
yesterday — would see a shape that changes with the data. A missing row
and a zero row look very different to a chart.

**The two outputs order the levels differently, on purpose.** The JSON
lists them in severity order because that is how a person reads a
summary and it is what the brief's example shows. The CSV sorts them
alphabetically because that is what the brief's *other* example shows
and it makes the file trivially diffable. Both examples are in the
brief. Matching a specification sometimes means doing two inconsistent
things deliberately.

**`Counter.most_common(1)` needs an empty guard.** `Counter().most_common(1)`
returns `[]`, so `[0]` on an error-free log raises `IndexError`. A log
with no errors is the *good* case and must not crash the tool. `null` in
the JSON is the honest representation, and `run` renders it as
`Top error: none.` On a tie, `most_common` returns insertion order, so
the message that appeared first in the file wins — arbitrary, but stable,
which is what matters for a report somebody might diff.

**`total_lines` is counted, not derived.** `read_records` tracks the line
number as it goes and returns it, so `skipped_lines = total_lines -
len(records)` is exact. Counting again in a second pass reads the file
twice and can disagree with the first pass if the file is still being
written.

**Streaming, not slurping.** `for lineno, line in enumerate(f, start=1)`
never holds more than one line. `f.readlines()` works fine on a 30-line
sample and takes your laptop out on the 10 GB log this tool exists for.
`start=1` gives 1-based line numbers, matching what your editor shows —
a warning that says `sample.log:7` should point at the line the editor
calls 7.

**`--out-dir` is created, not assumed.**
`mkdir(parents=True, exist_ok=True)` — `parents=True` so `--out-dir
a/b/c` works, `exist_ok=True` so a second run is not an error. Without
it the first run fails with `FileNotFoundError` on the *output* file,
which is a confusing thing to be told by a tool you just pointed at a
perfectly good input.

**One honest wart.** With `--min-level` active, `skipped_lines` counts
both malformed lines *and* deliberately filtered ones — 20 rather than 2
for `--min-level WARNING`. The brief does not define what that field
should mean when filtering is on, and both readings are defensible. If
this were shipping, the fix is a separate `filtered_lines` key. It is
written down here rather than papered over, because noticing that a
field's meaning has quietly changed is the skill.

## Download and run

The answer to this project is a **folder in your own repository** — your
`analyzer.py`, the reports it produced, and a commit history showing how
you got there. That is why this page carries no `README.py`.

The runnable answer ships beside it, named after the project:

Download [log_analyzer.py](./log_analyzer.py) and run it:

```bash
python log_analyzer.py
```

With no arguments it writes its own thirty-line sample log into a
temporary folder, analyzes it there, prints both reports, and deletes
the folder on the way out — so it works from a clean checkout with
nothing set up. Point it at real logs and it does the real job:

```bash
python log_analyzer.py app.log app.log.1.gz --out-dir reports/ --timestamps --top-errors 3
```

Save your own copy as `analyzer.py` in your project folder, and commit
that one. The longer download name is there so it cannot overwrite your
work.

## Common bugs to catch

- **`line.split()` instead of a pattern.**

  ```python
  parts = line.split()
  date, time, level, message = parts[0], parts[1], parts[2], parts[3]
  ```

  The message loses everything after its first word:
  `Slow query: SELECT * FROM users (1.2s)` becomes `Slow`. The fix
  people reach for next is `" ".join(parts[3:])`, which gets the words
  back but flattens the original spacing. `split(None, 3)` is genuinely
  close and is a defensible answer — but it still accepts
  `-- log rotated by logrotate at 14:30:05 --` as a valid entry with the
  level `by`, because nothing checked the *shape* of the fields.
  Validating is the job the pattern is doing.
- **A permissive level pattern, and then `KeyError: 'TRACE'`.**

  ```text
  Traceback (most recent call last):
    File "analyzer.py", line 122, in analyze
      counts[record["level"]] += 1
      ~~~~~~^^^^^^^^^^^^^^^^^
  KeyError: 'TRACE'
  ```

  The crash is in `analyze`, and the bug is in `LINE_RE`, four functions
  earlier. The general lesson is worth more than the fix: **validate at
  the edge, so the interior can assume.**
- **`except Exception:` around the parse loop.** It "handles malformed
  lines", and it also handles the `KeyError` above, the `AttributeError`
  from a typo, and the `re.error` the brief explicitly told you to let
  crash. You get a run that reports 30 skipped lines and an empty
  summary, with nothing to suggest the problem is in your code rather
  than the data.
- **Catching `re.error`.** Tempting, because it feels like being
  thorough. A malformed pattern is a programmer bug, found at import,
  fixed in ten seconds by reading the traceback. Caught and logged, it
  becomes "every line is malformed" and you go and stare at the log file
  instead.
- **`counts = Counter(r["level"] for r in records)` with no seeding.**
  Produces a summary with no `DEBUG` key, which does not match the
  brief's example and gives the CSV a variable number of rows.
- **Forgetting `newline=""` on the CSV writer.** On Windows the module's
  `\r\n` is translated again to `\r\r\n` and every other row in a
  spreadsheet is blank. It is
  [quiz question 4](../quiz.md#answer-key) this week, and it will bite
  you in real work more than once.
- **Letting `FileNotFoundError` reach the user as a traceback.** It does
  technically exit non-zero — with code 1, by coincidence, after eleven
  lines of noise. The brief asks for a friendly message.
- **`print` for the skip warnings.** They land in stdout, in the middle
  of the machine-readable output.

Six strings are worth checking `parse_line` against before you go
anywhere near a file. Five of them must come back `None`:

```text
'2026-05-13 14:30:02 WARNING  Slow query: SELECT * FROM users (1.2s)   \n'
'2026-05-13 14:30:01 INFO\n'
'2026-05-13 14:30:01 INFOX     hello\n'
'2026-05-13 14:30:01 TRACE    entering render loop\n'
'-- log rotated --\n'
'2026-05-13T14:30:01 INFO  iso style\n'
```

## Under the hood

<details>
<summary>Under the hood — how the four stretch goals were added without changing the default output</summary>

All six stretch goals are implemented in the shipped answer, and every
one is **opt-in**. That constraint is itself the lesson: a new feature
that changes existing output is a breaking change, and a flag is what
makes it additive instead.

| Flag or behaviour | Goal | How |
|---|---|---|
| `--timestamps` | earliest and latest entry | `build_summary` sorts `"date time"` strings |
| `--by-hour` | events per hour | `hourly_counts` + `write_hourly_csv` |
| several `LOG` arguments | aggregate many files | `nargs="+"`; `run` extends one list |
| `--min-level WARNING` | drop entries below a level | `filter_min_level` using `LEVELS.index` |
| `.gz` inputs, automatic | transparent decompression | `open_log` dispatches on `path.suffix` |
| `--top-errors N` | top N errors | `Counter.most_common(n)` |

**Timestamps by string sort.** `sorted(f"{r['date']} {r['time']}")`
sorts `YYYY-MM-DD HH:MM:SS` strings lexicographically, and that order
*is* chronological order, because ISO 8601 was designed so that string
order equals time order. No `datetime` parsing, no time-zone questions,
no `strptime` cost per line. This is the practical argument for ISO 8601
that [lecture 02](../lecture-notes/02-csv-and-json.md) makes: it is the
format where the lazy thing is also the correct thing. It stops being
true the moment your log mixes time zones — then you must parse.

**Multiple files needed almost no code.** `analyze` never knew about
files, so aggregation is `records.extend(file_records)` in `run`'s loop.
The only real decision was `source_file`: a plain string for one file,
matching the brief, or a list for several. Changing a field's *type*
based on how many inputs there were is not something to do lightly — it
forces every consumer to check — but the alternative was breaking the
brief's single-file example, and staying compatible by default won.

**Gzip, and why the context-manager protocol is the point.**

```python
def open_log(path: Path) -> IO[str]:
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")
```

`gzip.open` in `"rt"` mode returns something that is a context manager
and yields `str` lines — exactly like a plain file object. So
`read_records` needs **zero** changes: `with open_log(path) as f: for
line in f:` works on both. That is duck typing and the context-manager
protocol paying a real dividend. The `"t"` is essential; `gzip.open(path)`
defaults to binary and you would get
`TypeError: cannot use a string pattern on a bytes-like object` from the
regular expression.

**The ordering trick behind `--min-level`.** `LEVELS` is a tuple in
severity order, so `LEVELS.index(level)` *is* the severity as an
integer, and the filter is one comparison. Defining a separate
`{"DEBUG": 0, "INFO": 1, ...}` dict would work and would be a second
thing to keep in step with `LEVELS`. Deriving the order from the
constant you already have means there is one source of truth.

</details>

<details>
<summary>Under the hood — why the record is a plain dict, and what it will become in Week 7</summary>

Every parsed entry in this program is a `dict[str, str]`:

```python
{"date": "2026-05-13", "time": "14:30:01", "level": "INFO",
 "message": "Connection opened to db-primary"}
```

That is deliberately the simplest thing that works, and it is what
`match.groupdict()` hands you for free. It is also not what you would
choose if you had met classes yet — Week 6 comes before Week 7, and this
answer only uses tools the course has already taught.

Here is what the dict costs you, so you can recognise it when you feel
it.

**Typos are silent.** `record["mesage"]` raises `KeyError` at runtime,
somewhere far from where the record was built. Nothing warns you when
you write it.

**Every field is a string.** `record["time"]` is `"14:30:01"`, not a
time. Comparing, sorting or subtracting them works only because ISO
formats sort correctly as text — which is a happy accident this program
leans on quite hard.

**The shape is not written down anywhere.** The only way to know a
record has four keys is to read the regular expression.

Three ways to fix that, in increasing order of Python you need to know:

```python
from typing import NamedTuple

class LogRecord(NamedTuple):
    """One parsed log entry."""
    date: str
    time: str
    level: str
    message: str
```

A `NamedTuple` gives you `record.level` with autocompletion, a readable
`repr`, and an error at the point of the typo. It is still a tuple, so
it is immutable and cheap.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class LogRecord:
    """One parsed log entry."""
    date: str
    time: str
    level: str
    message: str
```

A frozen dataclass is the same idea with more room to grow — you can add
methods, computed properties, validation in `__post_init__`. `slots=True`
makes it smaller in memory than a dict, which starts to matter at ten
million records.

And the version you will actually want, once Week 7 has happened:

```python
@dataclass(frozen=True, slots=True)
class LogRecord:
    """One parsed log entry, with the timestamp already parsed."""
    when: datetime
    level: str
    message: str

    @property
    def hour(self) -> str:
        """The YYYY-MM-DD HH bucket this entry falls in."""
        return self.when.strftime("%Y-%m-%d %H")
```

Now `hourly_counts` is `Counter(r.hour for r in records)` and the
knowledge of what an hour bucket looks like lives with the record rather
than being spelled out at the call site.

None of this is required here, and none of it would make the program
work better on `sample.log`. It is what the program grows into, and
knowing that in advance is why the dict is confined to one function's
return value instead of being passed around raw.

</details>

## Acceptance checklist

- [ ] `python analyzer.py sample.log --out-dir reports/` prints two
      summary lines and creates both report files.
- [ ] `reports/summary.json` parses with `json.load` and matches the
      brief's example key for key.
- [ ] `reports/by-level.csv` has five lines: a header and four levels,
      alphabetical.
- [ ] `DEBUG` appears with a count of `0`, not missing.
- [ ] The two malformed lines log a WARNING each, naming the file and
      the line number, and do not stop the run.
- [ ] Those warnings go to stderr, so
      `python analyzer.py sample.log > run.txt` leaves them on screen.
- [ ] A log with no ERROR entries produces `"most_common_error": null`
      and prints `Top error: none.` rather than crashing.
- [ ] A missing input file prints one friendly line and exits 1.
- [ ] `--out-dir reports/nested/deep` works on a first run.
- [ ] Every path in the program is a `Path`.
- [ ] No bare `except:` and no `except Exception:` anywhere.
- [ ] Every function has type hints and a docstring.
- [ ] Committed in stages, not in one lump, and pushed to your fork.

## Stretch

1. **Timestamps in the summary.** Record the earliest and latest entry
   timestamp in the JSON. The Under the hood block explains why you do
   not need `datetime` to do it.
2. **Per-hour buckets.** A second CSV with `hour,count`.
3. **Multiple log files.** Accept several and aggregate them into one
   summary. Decide what `source_file` should be, and write down why.
4. **Filter by level.** `--min-level WARNING` ignores DEBUG and INFO
   entirely. Then work out what `skipped_lines` ought to mean when that
   flag is on — the shipped answer has an honest wart there and says so.
5. **Gzip support.** If the file ends in `.gz`, open it with the `gzip`
   module. Same context-manager protocol, so almost nothing changes.
6. **`--top-errors N`.** The top N errors instead of just the single
   most common one.
7. **Split the tool into modules.** `parser.py`, `report.py`, `cli.py`.
   The reference answer is one file only because a learner reading it
   top to bottom should not have to jump between tabs. Three files is
   arguably better practice, and Week 4 gave you everything you need.
8. **Write it atomically.** Use problem 6's helper so that a crash
   halfway through writing `summary.json` cannot leave a half-written
   report behind.

## Up next

The custom exception from
[challenge 02](../challenges/challenge-02-config-validator.md) and the
record dict you built here are both stepping stones into
[Week 7 — Object-Oriented Programming](../../week-07-object-oriented-programming/).
The first two things you will want to do there are turn
`dict[str, str]` into a real `LogRecord` class with a `level` attribute
and a `__repr__`, and turn `open_log` into a context manager you wrote
yourself. Both are a few lines away once you have classes.
