"""Turning bytes on disk into :class:`~loganalyzer.models.LogRecord` objects.

One responsibility: reading. Nothing here counts, formats, or writes. That is
what makes ``parse_line`` testable with a string literal and no file at all.
"""

from __future__ import annotations

import gzip
import logging
import re
from pathlib import Path
from typing import IO

from loganalyzer.models import LEVELS, LogRecord

__all__ = ["LINE_RE", "open_log", "parse_line", "read_records"]

logger = logging.getLogger(__name__)

#: One log entry: date, time, level, then a free-form message that may contain
#: anything at all — including whitespace, which is why the message group is
#: last and simply runs to end of line.
LINE_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})"
    r"\s+(?P<time>\d{2}:\d{2}:\d{2})"
    rf"\s+(?P<level>{'|'.join(LEVELS)})"
    r"\s+(?P<message>\S.*?)\s*$"
)


def parse_line(line: str) -> LogRecord | None:
    """Parse one log line, or return ``None`` if it is malformed.

    Returning ``None`` rather than raising keeps the caller's loop flat: a
    malformed line is expected input, not an exceptional condition.
    """
    match = LINE_RE.match(line)
    if match is None:
        return None
    return LogRecord(**match.groupdict())


def open_log(path: Path) -> IO[str]:
    """Open *path* for reading as text, transparently decompressing ``.gz``.

    Both branches return a context manager yielding ``str`` lines, so the
    caller does not need to care which one it got.
    """
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def read_records(path: Path) -> tuple[list[LogRecord], int]:
    """Return ``(records, total_lines)`` for the log file at *path*.

    Malformed lines are logged as warnings with their line number and skipped.
    Iterating the file object keeps memory flat regardless of file size.
    """
    records: list[LogRecord] = []
    total_lines = 0
    with open_log(path) as handle:
        for lineno, line in enumerate(handle, start=1):
            total_lines = lineno
            if not line.strip():
                # A blank line is not an entry. Count it as skipped like any
                # other unparseable line, but do not shout about it.
                logger.warning("%s:%d: skipping blank line", path.name, lineno)
                continue
            record = parse_line(line)
            if record is None:
                logger.warning(
                    "%s:%d: skipping malformed line: %s",
                    path.name,
                    lineno,
                    line.rstrip("\n"),
                )
                continue
            records.append(record)
    return records, total_lines
