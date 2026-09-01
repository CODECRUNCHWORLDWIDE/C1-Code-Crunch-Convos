"""Counting and summarising records.

Every function here is pure: records in, numbers out. No file handles, no
``argparse.Namespace``, no printing. That is why this module needs no fixtures
at all — the tests hand it a list and assert on the return value.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from loganalyzer.models import LEVELS, ErrorSummary, LogRecord, Summary

__all__ = [
    "build_summary",
    "count_levels",
    "filter_min_level",
    "hourly_counts",
    "most_common_error",
    "timestamp_range",
    "top_errors",
]


def count_levels(records: Sequence[LogRecord], levels: Sequence[str] = LEVELS) -> dict[str, int]:
    """Return a count per level, with every level present even at zero.

    Week 6 hard-coded the level tuple inside the function. Taking *levels* as an
    argument is what lets a test say "count these three levels" without editing
    the module — the change Problem 1 asks for, in one line.
    """
    counts = dict.fromkeys(levels, 0)
    for record in records:
        if record.level in counts:
            counts[record.level] += 1
    return counts


def _error_tally(records: Sequence[LogRecord]) -> Counter[str]:
    """Count ERROR messages by exact text."""
    return Counter(r.message for r in records if r.level == "ERROR")


def most_common_error(records: Sequence[LogRecord]) -> ErrorSummary | None:
    """Return the most frequent ERROR message, or ``None`` if there were none.

    Ties go to whichever message ``Counter`` saw first, which is insertion
    order, which is file order. That is arbitrary but deterministic, and a test
    pins it so a future refactor cannot change it by accident.
    """
    tally = _error_tally(records)
    if not tally:
        return None
    message, count = tally.most_common(1)[0]
    return {"message": message, "count": count}


def top_errors(records: Sequence[LogRecord], limit: int) -> list[ErrorSummary]:
    """Return the *limit* most frequent ERROR messages, most frequent first."""
    return [
        {"message": message, "count": count}
        for message, count in _error_tally(records).most_common(limit)
    ]


def timestamp_range(records: Sequence[LogRecord]) -> tuple[str | None, str | None]:
    """Return ``(first, last)`` timestamps, or ``(None, None)`` for no records.

    Sorting the ``"YYYY-MM-DD HH:MM:SS"`` strings is correct here because that
    format is lexicographically ordered — zero-padded, biggest unit first.
    """
    stamps = sorted(r.timestamp for r in records)
    if not stamps:
        return None, None
    return stamps[0], stamps[-1]


def hourly_counts(records: Sequence[LogRecord]) -> Counter[str]:
    """Count entries per ``"YYYY-MM-DD HH"`` bucket."""
    return Counter(r.hour for r in records)


def filter_min_level(
    records: Sequence[LogRecord],
    min_level: str,
    levels: Sequence[str] = LEVELS,
) -> list[LogRecord]:
    """Drop records less severe than *min_level*.

    Raises:
        ValueError: if *min_level* is not one of *levels*. Week 6 leaked
            ``ValueError: tuple.index(x): x not in tuple`` from here, which is
            true and useless. Naming the valid levels costs two lines.
    """
    if min_level not in levels:
        raise ValueError(f"unknown level {min_level!r}; expected one of {', '.join(levels)}")
    threshold = levels.index(min_level)
    return [r for r in records if levels.index(r.level) >= threshold]


def build_summary(
    source: str | list[str],
    records: Sequence[LogRecord],
    total_lines: int,
    *,
    timestamps: bool = False,
    error_limit: int = 0,
) -> Summary:
    """Assemble the full summary, in the key order the Week 6 spec shows.

    The optional keys are added only when asked for, so the default output is
    byte-for-byte identical to Week 6's.
    """
    summary: Summary = {
        "source_file": source,
        "total_lines": total_lines,
        "parsed_lines": len(records),
        "skipped_lines": total_lines - len(records),
        "counts": count_levels(records),
        "most_common_error": most_common_error(records),
    }

    if timestamps:
        first, last = timestamp_range(records)
        summary["first_timestamp"] = first
        summary["last_timestamp"] = last

    if error_limit > 0:
        summary["top_errors"] = top_errors(records, error_limit)

    return summary
