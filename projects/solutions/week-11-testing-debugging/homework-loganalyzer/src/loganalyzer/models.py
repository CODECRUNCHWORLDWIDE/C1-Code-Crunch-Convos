"""The shapes the rest of the package passes around.

Week 6 moved log entries around as ``dict[str, str]`` and the summary as a bare
``dict``. Both work at runtime and both are opaque to ``mypy``: nothing stops
you writing ``record["mesage"]`` and nothing tells you the summary has a
``counts`` key until you run it. A frozen dataclass and a ``TypedDict`` fix
that without changing a single byte of the program's output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

__all__ = ["LEVELS", "ErrorSummary", "LogRecord", "Summary"]

#: Levels in severity order. The JSON summary reports counts in this order; the
#: CSV report sorts them alphabetically, which is what the Week 6 spec shows.
LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR")


@dataclass(frozen=True, slots=True)
class LogRecord:
    """One parsed log entry.

    Frozen because nothing in the pipeline mutates a record; making that a type
    error rather than a code-review comment is free.
    """

    date: str
    time: str
    level: str
    message: str

    @property
    def timestamp(self) -> str:
        """``"2026-05-13 14:30:01"`` — the sort key for first/last."""
        return f"{self.date} {self.time}"

    @property
    def hour(self) -> str:
        """``"2026-05-13 14"`` — the bucket key for the by-hour report."""
        return f"{self.date} {self.time[:2]}"


class ErrorSummary(TypedDict):
    """One row of the error tally."""

    message: str
    count: int


class Summary(TypedDict, total=False):
    """The JSON summary.

    ``total=False`` because ``first_timestamp``, ``last_timestamp`` and
    ``top_errors`` only appear when the matching flag is passed — that is the
    Week 6 behaviour, preserved exactly.
    """

    source_file: str | list[str]
    total_lines: int
    parsed_lines: int
    skipped_lines: int
    counts: dict[str, int]
    most_common_error: ErrorSummary | None
    first_timestamp: str | None
    last_timestamp: str | None
    top_errors: list[ErrorSummary]
