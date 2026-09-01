"""Tests for :mod:`loganalyzer.parsing`."""

from __future__ import annotations

import gzip
from pathlib import Path

import pytest

from loganalyzer.models import LogRecord
from loganalyzer.parsing import open_log, parse_line, read_records

# ------------------------------------------------------------- parse_line ---


def test_parse_line_extracts_all_four_fields() -> None:
    record = parse_line("2026-05-13 14:30:01 INFO     Connection opened to db-primary")

    assert record == LogRecord(
        date="2026-05-13",
        time="14:30:01",
        level="INFO",
        message="Connection opened to db-primary",
    )


def test_parse_line_keeps_internal_whitespace_in_the_message() -> None:
    record = parse_line("2026-05-13 14:30:02 WARNING  Slow query: SELECT *  FROM users (1.2s)")

    assert record is not None
    assert record.message == "Slow query: SELECT *  FROM users (1.2s)"


def test_parse_line_strips_the_trailing_newline() -> None:
    record = parse_line("2026-05-13 14:30:01 INFO     done\n")

    assert record is not None
    assert record.message == "done"


@pytest.mark.parametrize(
    ("line", "why"),
    [
        ("-- log rotated by logrotate at 14:30:05 --", "no timestamp at all"),
        ("2026-05-13 14:31:07 TRACE    entering render loop", "TRACE is not a known level"),
        ("13/05/2026 14:30:01 INFO      wrong date format", "date is not ISO"),
        ("2026-05-13 14:30 INFO         time has no seconds", "time is not HH:MM:SS"),
        ("2026-05-13 14:30:01 INFO", "level present, message missing"),
        ("", "empty line"),
    ],
    ids=["prose", "unknown-level", "dd-mm-yyyy", "short-time", "no-message", "empty"],
)
def test_parse_line_returns_none_for_malformed_input(line: str, why: str) -> None:
    assert parse_line(line) is None, why


def test_parse_line_does_not_match_a_level_inside_the_message() -> None:
    """``ERROR`` in the message body must not become the record's level."""
    record = parse_line("2026-05-13 14:30:01 INFO     retrying after ERROR earlier")

    assert record is not None
    assert record.level == "INFO"
    assert record.message == "retrying after ERROR earlier"


# ----------------------------------------------------------- LogRecord API --


def test_logrecord_timestamp_joins_date_and_time() -> None:
    record = LogRecord(date="2026-05-13", time="14:30:01", level="INFO", message="x")
    assert record.timestamp == "2026-05-13 14:30:01"


def test_logrecord_hour_truncates_to_the_hour() -> None:
    record = LogRecord(date="2026-05-13", time="14:30:01", level="INFO", message="x")
    assert record.hour == "2026-05-13 14"


def test_logrecord_is_frozen() -> None:
    """Records are immutable, so a wide-scoped fixture cannot leak between tests."""
    record = LogRecord(date="2026-05-13", time="14:30:01", level="INFO", message="x")
    with pytest.raises(AttributeError):
        record.level = "ERROR"  # type: ignore[misc]


# ----------------------------------------------------------- read_records ---


def test_read_records_counts_every_line_including_the_bad_ones(
    sample_log: Path, sample_facts: dict[str, int]
) -> None:
    records, total_lines = read_records(sample_log)

    assert total_lines == sample_facts["total_lines"]
    assert len(records) == sample_facts["parsed_lines"]


def test_read_records_warns_once_per_skipped_line(
    sample_log: Path, sample_facts: dict[str, int], caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level("WARNING", logger="loganalyzer.parsing"):
        read_records(sample_log)

    skipped = [r for r in caplog.records if "skipping" in r.message]
    assert len(skipped) == sample_facts["skipped_lines"]
    assert "sample.log:7: skipping malformed line" in skipped[0].message


def test_read_records_names_blank_lines_separately(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    path = tmp_path / "gappy.log"
    path.write_text("2026-05-13 14:30:01 INFO     one\n\n2026-05-13 14:30:02 INFO     two\n")

    with caplog.at_level("WARNING", logger="loganalyzer.parsing"):
        records, total_lines = read_records(path)

    assert (len(records), total_lines) == (2, 3)
    assert any("skipping blank line" in r.message for r in caplog.records)


def test_read_records_returns_zero_lines_for_an_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.log"
    path.write_text("")

    assert read_records(path) == ([], 0)


def test_read_records_reads_gzipped_logs(
    tmp_path: Path, sample_log: Path, sample_facts: dict[str, int]
) -> None:
    archived = tmp_path / "sample.log.gz"
    archived.write_bytes(gzip.compress(sample_log.read_bytes()))

    records, total_lines = read_records(archived)

    assert total_lines == sample_facts["total_lines"]
    assert len(records) == sample_facts["parsed_lines"]


def test_read_records_raises_for_a_missing_file(tmp_path: Path) -> None:
    """The documented error path: parsing does not swallow a missing file."""
    with pytest.raises(FileNotFoundError):
        read_records(tmp_path / "not-here.log")


def test_open_log_yields_text_lines_for_plain_files(sample_log: Path) -> None:
    with open_log(sample_log) as handle:
        first = handle.readline()

    assert isinstance(first, str)
    assert first.startswith("2026-05-13")
