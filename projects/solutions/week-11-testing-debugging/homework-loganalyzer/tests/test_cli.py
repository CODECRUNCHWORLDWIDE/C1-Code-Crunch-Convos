"""Tests for :mod:`loganalyzer.cli` — the only layer that prints.

These are the closest thing this project has to end-to-end tests: they call
``main`` with an argv list, let it read a real file and write real reports, and
assert on stdout, stderr, the exit code, and the files on disk. There are far
fewer of them than there are unit tests, which is the testing pyramid doing its
job.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from loganalyzer import cli
from loganalyzer.cli import build_parser, main
from loganalyzer.reporting import BY_HOUR_FILENAME, BY_LEVEL_FILENAME, SUMMARY_FILENAME


def _run(sample_log: Path, out_dir: Path, *flags: str) -> int:
    return main([str(sample_log), "--out-dir", str(out_dir), *flags])


def _summary_of(out_dir: Path) -> dict[str, object]:
    payload: dict[str, object] = json.loads(
        (out_dir / SUMMARY_FILENAME).read_text(encoding="utf-8")
    )
    return payload


# ------------------------------------------------------------ happy path ----


def test_main_returns_zero_and_writes_both_reports(sample_log: Path, out_dir: Path) -> None:
    assert _run(sample_log, out_dir) == 0
    assert (out_dir / SUMMARY_FILENAME).exists()
    assert (out_dir / BY_LEVEL_FILENAME).exists()


def test_main_summary_matches_the_sample_log(
    sample_log: Path, out_dir: Path, sample_facts: dict[str, int]
) -> None:
    _run(sample_log, out_dir)

    assert _summary_of(out_dir) == {
        "source_file": "sample.log",
        "total_lines": sample_facts["total_lines"],
        "parsed_lines": sample_facts["parsed_lines"],
        "skipped_lines": sample_facts["skipped_lines"],
        "counts": {
            "DEBUG": sample_facts["debug"],
            "INFO": sample_facts["info"],
            "WARNING": sample_facts["warning"],
            "ERROR": sample_facts["error"],
        },
        "most_common_error": {"message": "Failed to connect to cache: timeout", "count": 2},
    }


def test_main_prints_the_two_summary_lines(
    sample_log: Path, out_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _run(sample_log, out_dir)

    out = capsys.readouterr().out.splitlines()

    assert out[0] == ("Parsed 28/30 lines. Top error: 'Failed to connect to cache: timeout' (2x).")
    assert out[1].startswith("Reports written to ")
    assert out[1].endswith(f"/{SUMMARY_FILENAME} and {(out_dir / BY_LEVEL_FILENAME).as_posix()}.")


def test_main_says_none_when_there_are_no_errors(
    tmp_path: Path, out_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    quiet = tmp_path / "quiet.log"
    quiet.write_text("2026-05-13 14:30:01 INFO     nothing to see here\n", encoding="utf-8")

    assert main([str(quiet), "--out-dir", str(out_dir)]) == 0
    assert "Top error: none." in capsys.readouterr().out


# ----------------------------------------------------------------- flags ----


def test_main_timestamps_flag_adds_the_two_keys(sample_log: Path, out_dir: Path) -> None:
    _run(sample_log, out_dir, "--timestamps")

    summary = _summary_of(out_dir)
    assert summary["first_timestamp"] == "2026-05-13 14:30:01"
    assert summary["last_timestamp"] == "2026-05-13 14:31:21"


def test_main_top_errors_flag_adds_the_array(sample_log: Path, out_dir: Path) -> None:
    _run(sample_log, out_dir, "--top-errors", "2")

    assert _summary_of(out_dir)["top_errors"] == [
        {"message": "Failed to connect to cache: timeout", "count": 2},
        {"message": "Payment gateway returned 502", "count": 1},
    ]


def test_main_by_hour_flag_writes_the_third_report(sample_log: Path, out_dir: Path) -> None:
    _run(sample_log, out_dir, "--by-hour")

    hourly = (out_dir / BY_HOUR_FILENAME).read_text(encoding="utf-8")
    assert "hour,count" in hourly
    assert "2026-05-13 14,28" in hourly


def test_main_min_level_drops_the_quieter_entries(sample_log: Path, out_dir: Path) -> None:
    _run(sample_log, out_dir, "--min-level", "WARNING")

    summary = _summary_of(out_dir)
    assert summary["parsed_lines"] == 10
    assert summary["counts"] == {"DEBUG": 0, "INFO": 0, "WARNING": 6, "ERROR": 4}


def test_main_min_level_leaves_total_lines_alone(sample_log: Path, out_dir: Path) -> None:
    """Filtering changes what was *analysed*, not what was *read*."""
    _run(sample_log, out_dir, "--min-level", "ERROR")

    assert _summary_of(out_dir)["total_lines"] == 30


def test_main_verbose_flag_is_accepted(sample_log: Path, out_dir: Path) -> None:
    assert _run(sample_log, out_dir, "--verbose") == 0


def test_main_lists_every_source_when_given_several_logs(
    tmp_path: Path, sample_log: Path, out_dir: Path
) -> None:
    second = tmp_path / "extra.log"
    second.write_text("2026-05-13 14:32:00 ERROR    second file\n", encoding="utf-8")

    assert main([str(sample_log), str(second), "--out-dir", str(out_dir)]) == 0

    summary = _summary_of(out_dir)
    assert summary["source_file"] == ["sample.log", "extra.log"]
    assert summary["total_lines"] == 31
    assert summary["parsed_lines"] == 29


# ----------------------------------------------------------- error paths ----


def test_main_returns_one_for_a_missing_file(
    tmp_path: Path, out_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nope.log"

    assert main([str(missing), "--out-dir", str(out_dir)]) == 1
    assert capsys.readouterr().err == f"loganalyzer: error: log file not found: {missing}\n"


def test_main_returns_one_when_the_file_cannot_be_read(
    monkeypatch: pytest.MonkeyPatch,
    sample_log: Path,
    out_dir: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The one place a mock earns its keep: a real unreadable file is not portable.

    Chmod semantics differ across Windows, macOS and Linux and root ignores
    them entirely, so the honest way to exercise this branch is to make the
    boundary function raise.
    """

    def boom(path: Path) -> tuple[list[object], int]:
        raise PermissionError(13, "Permission denied", str(path))

    monkeypatch.setattr(cli, "read_records", boom)

    assert main([str(sample_log), "--out-dir", str(out_dir)]) == 1
    assert "permission denied" in capsys.readouterr().err


def test_main_writes_nothing_when_a_file_is_missing(tmp_path: Path, out_dir: Path) -> None:
    main([str(tmp_path / "nope.log"), "--out-dir", str(out_dir)])

    assert not out_dir.exists()


# --------------------------------------------------------------- parser -----


def test_parser_defaults_to_a_reports_directory() -> None:
    args = build_parser().parse_args(["app.log"])

    assert args.out_dir == Path("reports")
    assert args.top_errors == 0
    assert args.min_level is None
    assert args.by_hour is False


def test_parser_rejects_an_unknown_min_level(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as excinfo:
        build_parser().parse_args(["app.log", "--min-level", "TRACE"])

    assert excinfo.value.code == 2
    assert "invalid choice: 'TRACE'" in capsys.readouterr().err


def test_parser_requires_at_least_one_log() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args([])
