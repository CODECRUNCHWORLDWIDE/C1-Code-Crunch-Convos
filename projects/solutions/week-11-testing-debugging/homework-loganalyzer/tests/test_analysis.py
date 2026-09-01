"""Tests for :mod:`loganalyzer.analysis`.

Not one fixture in this file opens a file, because not one function under test
can. That is the payoff from Problem 1's split: the analysis layer takes a list
and returns a number, so its tests are list literals and equality assertions.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from loganalyzer.analysis import (
    build_summary,
    count_levels,
    filter_min_level,
    hourly_counts,
    most_common_error,
    timestamp_range,
    top_errors,
)
from loganalyzer.models import LogRecord

MakeRecords = Callable[..., list[LogRecord]]

# ----------------------------------------------------------- count_levels ---


def test_count_levels_reports_every_level_even_at_zero(make_records: MakeRecords) -> None:
    counts = count_levels(make_records(("INFO", "a"), ("INFO", "b")))

    assert counts == {"DEBUG": 0, "INFO": 2, "WARNING": 0, "ERROR": 0}


def test_count_levels_on_the_real_sample_log(
    sample_records: list[LogRecord], sample_facts: dict[str, int]
) -> None:
    assert count_levels(sample_records) == {
        "DEBUG": sample_facts["debug"],
        "INFO": sample_facts["info"],
        "WARNING": sample_facts["warning"],
        "ERROR": sample_facts["error"],
    }


def test_count_levels_accepts_a_custom_level_tuple(make_records: MakeRecords) -> None:
    """The argument Week 6 did not have. Passing it needs no edit to the module."""
    records = make_records(("INFO", "a"), ("ERROR", "b"))

    assert count_levels(records, levels=("INFO", "ERROR")) == {"INFO": 1, "ERROR": 1}


def test_count_levels_ignores_levels_outside_the_tuple(make_records: MakeRecords) -> None:
    records = make_records(("INFO", "a"), ("ERROR", "b"))

    assert count_levels(records, levels=("INFO",)) == {"INFO": 1}


def test_count_levels_of_nothing_is_all_zeros() -> None:
    assert count_levels([]) == {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0}


# ------------------------------------------------- most_common / top_errors --


def test_most_common_error_returns_none_when_there_are_no_errors(
    make_records: MakeRecords,
) -> None:
    assert most_common_error(make_records(("INFO", "fine"), ("WARNING", "hmm"))) is None


def test_most_common_error_picks_the_most_frequent(error_records: list[LogRecord]) -> None:
    assert most_common_error(error_records) == {"message": "timeout", "count": 3}


def test_most_common_error_ignores_non_error_levels(make_records: MakeRecords) -> None:
    records = make_records(
        ("WARNING", "repeated"),
        ("WARNING", "repeated"),
        ("ERROR", "only once"),
    )

    assert most_common_error(records) == {"message": "only once", "count": 1}


def test_most_common_error_breaks_ties_in_file_order(make_records: MakeRecords) -> None:
    """Arbitrary but deterministic — pinned so a refactor cannot silently flip it."""
    records = make_records(("ERROR", "first"), ("ERROR", "second"))

    assert most_common_error(records) == {"message": "first", "count": 1}


def test_top_errors_is_ordered_most_frequent_first(error_records: list[LogRecord]) -> None:
    assert top_errors(error_records, limit=2) == [
        {"message": "timeout", "count": 3},
        {"message": "disk full", "count": 2},
    ]


def test_top_errors_returns_everything_when_the_limit_is_generous(
    error_records: list[LogRecord],
) -> None:
    assert len(top_errors(error_records, limit=99)) == 3


def test_top_errors_of_nothing_is_an_empty_list() -> None:
    assert top_errors([], limit=5) == []


# -------------------------------------------- timestamp_range / hourly ------


def test_timestamp_range_is_none_none_for_no_records() -> None:
    assert timestamp_range([]) == (None, None)


def test_timestamp_range_returns_first_and_last_chronologically() -> None:
    records = [
        LogRecord("2026-05-13", "23:59:59", "INFO", "late"),
        LogRecord("2026-05-13", "00:00:01", "INFO", "early"),
        LogRecord("2026-05-12", "12:00:00", "INFO", "yesterday"),
    ]

    assert timestamp_range(records) == ("2026-05-12 12:00:00", "2026-05-13 23:59:59")


def test_timestamp_range_on_the_real_sample_log(sample_records: list[LogRecord]) -> None:
    assert timestamp_range(sample_records) == (
        "2026-05-13 14:30:01",
        "2026-05-13 14:31:21",
    )


def test_hourly_counts_buckets_by_the_hour() -> None:
    records = [
        LogRecord("2026-05-13", "14:30:01", "INFO", "a"),
        LogRecord("2026-05-13", "14:59:59", "INFO", "b"),
        LogRecord("2026-05-13", "15:00:00", "INFO", "c"),
    ]

    assert dict(hourly_counts(records)) == {"2026-05-13 14": 2, "2026-05-13 15": 1}


# -------------------------------------------------------- filter_min_level --


@pytest.mark.parametrize(
    ("min_level", "expected_messages"),
    [
        ("DEBUG", ["dbg", "inf", "wrn", "err"]),
        ("INFO", ["inf", "wrn", "err"]),
        ("WARNING", ["wrn", "err"]),
        ("ERROR", ["err"]),
    ],
    ids=["keeps-everything", "drops-debug", "drops-info-too", "errors-only"],
)
def test_filter_min_level_keeps_that_level_and_above(
    make_records: MakeRecords, min_level: str, expected_messages: list[str]
) -> None:
    records = make_records(
        ("DEBUG", "dbg"),
        ("INFO", "inf"),
        ("WARNING", "wrn"),
        ("ERROR", "err"),
    )

    kept = filter_min_level(records, min_level)

    assert [r.message for r in kept] == expected_messages


def test_filter_min_level_rejects_an_unknown_level(make_records: MakeRecords) -> None:
    """Week 6 leaked ``ValueError: tuple.index(x): x not in tuple`` from here."""
    with pytest.raises(ValueError, match=r"unknown level 'TRACE'; expected one of DEBUG, INFO"):
        filter_min_level(make_records(("INFO", "a")), "TRACE")


def test_filter_min_level_accepts_a_custom_level_ordering(make_records: MakeRecords) -> None:
    records = make_records(("INFO", "inf"), ("ERROR", "err"))

    kept = filter_min_level(records, "ERROR", levels=("INFO", "ERROR"))

    assert [r.message for r in kept] == ["err"]


# ------------------------------------------------------------ build_summary -


def test_build_summary_has_exactly_the_week_6_keys_by_default(
    error_records: list[LogRecord],
) -> None:
    summary = build_summary("app.log", error_records, total_lines=9)

    assert list(summary) == [
        "source_file",
        "total_lines",
        "parsed_lines",
        "skipped_lines",
        "counts",
        "most_common_error",
    ]


def test_build_summary_computes_the_skipped_line_count(
    error_records: list[LogRecord],
) -> None:
    summary = build_summary("app.log", error_records, total_lines=9)

    assert summary["total_lines"] == 9
    assert summary["parsed_lines"] == 7
    assert summary["skipped_lines"] == 2


def test_build_summary_adds_timestamps_only_when_asked(
    error_records: list[LogRecord],
) -> None:
    summary = build_summary("app.log", error_records, total_lines=9, timestamps=True)

    assert summary["first_timestamp"] == "2026-05-13 14:30:00"
    assert summary["last_timestamp"] == "2026-05-13 14:30:06"


def test_build_summary_timestamps_are_none_for_no_records() -> None:
    summary = build_summary("empty.log", [], total_lines=0, timestamps=True)

    assert summary["first_timestamp"] is None
    assert summary["last_timestamp"] is None


def test_build_summary_adds_top_errors_only_when_the_limit_is_positive(
    error_records: list[LogRecord],
) -> None:
    with_limit = build_summary("app.log", error_records, total_lines=9, error_limit=2)
    without = build_summary("app.log", error_records, total_lines=9, error_limit=0)

    assert with_limit["top_errors"] == [
        {"message": "timeout", "count": 3},
        {"message": "disk full", "count": 2},
    ]
    assert "top_errors" not in without


def test_build_summary_accepts_a_list_of_sources(error_records: list[LogRecord]) -> None:
    summary = build_summary(["a.log", "b.log"], error_records, total_lines=9)

    assert summary["source_file"] == ["a.log", "b.log"]
