"""Shared fixtures.

Five fixtures, and the interesting decision is the *scope* of each one.

``sample_log`` and ``sample_records`` are ``scope="module"``: parsing the
shipped 30-line ``sample.log`` costs a file open and a regex pass, and every
test in a file wants the same answer. Re-doing it per test would be pure waste.
The safety condition for widening a scope is that nothing mutates the shared
object — ``LogRecord`` is a frozen dataclass and no test appends to the list,
so that condition holds here. If you ever add a test that mutates
``sample_records``, narrow the scope back to ``function`` in the same commit.

``out_dir``, ``make_records`` and ``error_records`` stay function-scoped.
``out_dir`` builds on ``tmp_path``, which is function-scoped by definition, and
the other two are cheap enough that sharing them would buy nothing and risk
cross-test leakage.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from loganalyzer.models import LogRecord
from loganalyzer.parsing import read_records

#: The log that ships with the reference implementation. Tests assert on its
#: real contents, so the file and the expectations move together.
SAMPLE_LOG_PATH = Path(__file__).resolve().parents[1] / "sample.log"


@pytest.fixture(scope="module")
def sample_log() -> Path:
    """Path to the 30-line ``sample.log`` shipped with the project."""
    return SAMPLE_LOG_PATH


@pytest.fixture(scope="module")
def sample_facts() -> dict[str, int]:
    """What ``sample.log`` contains, stated once instead of as magic numbers.

    Handed over as a *fixture* rather than a module constant on purpose:
    ``from tests.conftest import SAMPLE_TOTAL_LINES`` only works when ``tests/``
    happens to be an importable package, which depends on ``pythonpath`` and on
    whether an ``__init__.py`` exists. A fixture always works.
    """
    return {
        "total_lines": 30,
        "parsed_lines": 28,
        "skipped_lines": 2,
        "debug": 0,
        "info": 18,
        "warning": 6,
        "error": 4,
    }


@pytest.fixture(scope="module")
def sample_records(sample_log: Path) -> list[LogRecord]:
    """Every parseable record in ``sample.log``, parsed exactly once per file.

    Module-scoped: 28 frozen records that no test mutates.
    """
    records, _ = read_records(sample_log)
    return records


@pytest.fixture
def out_dir(tmp_path: Path) -> Path:
    """A report directory that does *not* exist yet.

    Deliberately not created, so ``write_reports`` has to do the ``mkdir``
    itself and a test can prove it does.
    """
    return tmp_path / "reports"


@pytest.fixture
def make_records() -> Callable[..., list[LogRecord]]:
    """Build records from ``(level, message)`` pairs with plausible timestamps.

    A factory rather than a fixed list: analysis tests each want a *different*
    shape, and a factory keeps the interesting part (the levels and messages)
    on the line where the test reads it.
    """

    def _make(*pairs: tuple[str, str], date: str = "2026-05-13") -> list[LogRecord]:
        return [
            LogRecord(date=date, time=f"14:30:{index:02d}", level=level, message=message)
            for index, (level, message) in enumerate(pairs)
        ]

    return _make


@pytest.fixture
def error_records(make_records: Callable[..., list[LogRecord]]) -> list[LogRecord]:
    """Three ``timeout`` errors, two ``disk full``, one ``502`` — a clear ranking."""
    return make_records(
        ("ERROR", "timeout"),
        ("ERROR", "disk full"),
        ("ERROR", "timeout"),
        ("INFO", "all good"),
        ("ERROR", "disk full"),
        ("ERROR", "timeout"),
        ("ERROR", "502 from gateway"),
    )
