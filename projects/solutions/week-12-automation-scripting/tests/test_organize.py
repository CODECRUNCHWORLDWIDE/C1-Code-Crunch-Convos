"""Tests for the File Organizer Bot.

Run from this project folder:

    pip install pytest
    python -m pytest -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import organize  # noqa: E402  (path shim above must run first)

CONFIG = {
    "Images": [".jpg", ".png"],
    "Documents": [".pdf", ".md"],
    "Code": [".py"],
    "Other": [],
}


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    """A directory with one file per category plus an unmatched one."""
    for name in ("beach.jpg", "notes.md", "script.py", "weird_thing.xyz"):
        (tmp_path / name).write_text(name, encoding="utf-8")
    return tmp_path


@pytest.fixture()
def config_file(tmp_path: Path) -> Path:
    path = tmp_path / "config.json"
    path.write_text(json.dumps(CONFIG), encoding="utf-8")
    return path


def test_dry_run_moves_nothing(workspace: Path) -> None:
    acted = organize.organize_once(workspace, CONFIG, apply=False)
    assert acted == 4
    assert (workspace / "beach.jpg").exists()
    assert not (workspace / "Images").exists()


def test_apply_moves_files_into_categories(workspace: Path) -> None:
    acted = organize.organize_once(workspace, CONFIG, apply=True)
    assert acted == 4
    assert (workspace / "Images" / "beach.jpg").is_file()
    assert (workspace / "Documents" / "notes.md").is_file()
    assert (workspace / "Code" / "script.py").is_file()
    # No category claims .xyz, so the empty-list category catches it.
    assert (workspace / "Other" / "weird_thing.xyz").is_file()
    assert not (workspace / "beach.jpg").exists()


def test_collision_gets_numeric_suffix(tmp_path: Path) -> None:
    (tmp_path / "Images").mkdir()
    (tmp_path / "Images" / "beach.jpg").write_text("old", encoding="utf-8")
    (tmp_path / "beach.jpg").write_text("new", encoding="utf-8")

    organize.organize_once(tmp_path, CONFIG, apply=True)

    assert (tmp_path / "Images" / "beach.jpg").read_text(encoding="utf-8") == "old"
    assert (tmp_path / "Images" / "beach-1.jpg").read_text(encoding="utf-8") == "new"


def test_extension_match_is_case_insensitive(tmp_path: Path) -> None:
    (tmp_path / "HOLIDAY.JPG").write_text("x", encoding="utf-8")
    organize.organize_once(tmp_path, CONFIG, apply=True)
    assert (tmp_path / "Images" / "HOLIDAY.JPG").is_file()


def test_log_file_and_directories_are_skipped(workspace: Path) -> None:
    log_path = workspace / "organize.log"
    log_path.write_text("previous run\n", encoding="utf-8")
    (workspace / "already-sorted").mkdir()

    organize.organize_once(workspace, CONFIG, apply=True, log_path=log_path)

    assert log_path.is_file()  # not swept into Other/
    assert (workspace / "already-sorted").is_dir()


def test_running_twice_is_idempotent(workspace: Path) -> None:
    first = organize.organize_once(workspace, CONFIG, apply=True)
    second = organize.organize_once(workspace, CONFIG, apply=True)
    assert first == 4
    assert second == 0  # everything already lives in a category folder


def test_missing_directory_exits_1(tmp_path: Path, config_file: Path) -> None:
    missing = tmp_path / "nope"
    assert organize.main([str(missing), "--config", str(config_file)]) == 1


def test_malformed_config_exits_1(workspace: Path) -> None:
    bad = workspace / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert organize.main([str(workspace), "--config", str(bad)]) == 1


def test_bad_arguments_exit_2(workspace: Path, config_file: Path) -> None:
    with pytest.raises(SystemExit) as excinfo:
        organize.main([str(workspace), "--config", str(config_file), "--interval", "0"])
    assert excinfo.value.code == 2


def test_main_dry_run_writes_a_log_line(workspace: Path, config_file: Path) -> None:
    assert organize.main([str(workspace), "--config", str(config_file)]) == 0
    log_text = (workspace / "organize.log").read_text(encoding="utf-8")
    assert "would move beach.jpg -> Images/beach.jpg" in log_text
