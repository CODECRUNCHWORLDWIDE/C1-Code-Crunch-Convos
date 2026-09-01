"""Tests for :mod:`loganalyzer.reporting`.

Every test writes into ``tmp_path``. Nothing here touches the repository, and
nothing here needs a mock: the file system is fast, real, and disposable, so
faking it would only prove that the fake works.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Callable
from pathlib import Path

from loganalyzer.analysis import build_summary
from loganalyzer.models import LogRecord, Summary
from loganalyzer.reporting import (
    BY_HOUR_FILENAME,
    BY_LEVEL_FILENAME,
    SUMMARY_FILENAME,
    write_hourly_csv,
    write_level_csv,
    write_reports,
    write_summary,
)

MakeRecords = Callable[..., list[LogRecord]]


def _summary(records: list[LogRecord]) -> Summary:
    return build_summary("app.log", records, total_lines=len(records))


# --------------------------------------------------------- write_summary ----


def test_write_summary_round_trips_through_json(
    tmp_path: Path, error_records: list[LogRecord]
) -> None:
    path = tmp_path / SUMMARY_FILENAME
    summary = _summary(error_records)

    write_summary(summary, path)

    assert json.loads(path.read_text(encoding="utf-8")) == summary


def test_write_summary_ends_with_a_newline(tmp_path: Path, error_records: list[LogRecord]) -> None:
    """POSIX text files end in a newline; ``json.dump`` does not add one."""
    path = tmp_path / SUMMARY_FILENAME

    write_summary(_summary(error_records), path)

    assert path.read_text(encoding="utf-8").endswith("}\n")


def test_write_summary_is_indented_for_humans(
    tmp_path: Path, error_records: list[LogRecord]
) -> None:
    path = tmp_path / SUMMARY_FILENAME

    write_summary(_summary(error_records), path)

    assert '\n  "total_lines": 7' in path.read_text(encoding="utf-8")


# ------------------------------------------------------- write_level_csv ----


def test_write_level_csv_sorts_levels_alphabetically(
    tmp_path: Path, make_records: MakeRecords
) -> None:
    path = tmp_path / BY_LEVEL_FILENAME
    records = make_records(("INFO", "a"), ("ERROR", "b"), ("ERROR", "c"))

    write_level_csv(_summary(records), path)

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))

    assert rows == [
        ["level", "count"],
        ["DEBUG", "0"],
        ["ERROR", "2"],
        ["INFO", "1"],
        ["WARNING", "0"],
    ]


def test_write_level_csv_uses_unix_row_endings(tmp_path: Path, make_records: MakeRecords) -> None:
    """``newline=""`` plus ``csv`` gives ``\\r\\n`` rows on every platform."""
    path = tmp_path / BY_LEVEL_FILENAME

    write_level_csv(_summary(make_records(("INFO", "a"))), path)

    assert path.read_bytes().startswith(b"level,count\r\n")


# ------------------------------------------------------ write_hourly_csv ----


def test_write_hourly_csv_sorts_chronologically(tmp_path: Path) -> None:
    path = tmp_path / BY_HOUR_FILENAME
    records = [
        LogRecord("2026-05-13", "15:00:00", "INFO", "later"),
        LogRecord("2026-05-13", "14:30:01", "INFO", "earlier"),
        LogRecord("2026-05-13", "14:59:59", "INFO", "earlier still"),
    ]

    write_hourly_csv(records, path)

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))

    assert rows == [["hour", "count"], ["2026-05-13 14", "2"], ["2026-05-13 15", "1"]]


# --------------------------------------------------------- write_reports ----


def test_write_reports_creates_a_missing_output_directory(
    out_dir: Path, error_records: list[LogRecord]
) -> None:
    assert not out_dir.exists()

    write_reports(_summary(error_records), error_records, out_dir)

    assert out_dir.is_dir()


def test_write_reports_creates_nested_directories(
    tmp_path: Path, error_records: list[LogRecord]
) -> None:
    deep = tmp_path / "a" / "b" / "c"

    write_reports(_summary(error_records), error_records, deep)

    assert (deep / SUMMARY_FILENAME).exists()


def test_write_reports_returns_the_two_paths_it_wrote(
    out_dir: Path, error_records: list[LogRecord]
) -> None:
    summary_path, level_path = write_reports(_summary(error_records), error_records, out_dir)

    assert summary_path == out_dir / SUMMARY_FILENAME
    assert level_path == out_dir / BY_LEVEL_FILENAME
    assert summary_path.exists()
    assert level_path.exists()


def test_write_reports_skips_by_hour_unless_asked(
    out_dir: Path, error_records: list[LogRecord]
) -> None:
    write_reports(_summary(error_records), error_records, out_dir)

    assert not (out_dir / BY_HOUR_FILENAME).exists()


def test_write_reports_writes_by_hour_when_asked(
    out_dir: Path, error_records: list[LogRecord]
) -> None:
    write_reports(_summary(error_records), error_records, out_dir, by_hour=True)

    assert (out_dir / BY_HOUR_FILENAME).exists()


def test_write_reports_honours_custom_filenames(
    out_dir: Path, error_records: list[LogRecord]
) -> None:
    summary_path, level_path = write_reports(
        _summary(error_records),
        error_records,
        out_dir,
        by_hour=True,
        summary_name="s.json",
        level_name="l.csv",
        hour_name="h.csv",
    )

    assert summary_path.name == "s.json"
    assert level_path.name == "l.csv"
    assert (out_dir / "h.csv").exists()


def test_write_reports_is_idempotent(out_dir: Path, error_records: list[LogRecord]) -> None:
    """Running twice must overwrite, not append or explode on ``mkdir``."""
    summary = _summary(error_records)

    write_reports(summary, error_records, out_dir)
    first = (out_dir / SUMMARY_FILENAME).read_text(encoding="utf-8")
    write_reports(summary, error_records, out_dir)

    assert (out_dir / SUMMARY_FILENAME).read_text(encoding="utf-8") == first
