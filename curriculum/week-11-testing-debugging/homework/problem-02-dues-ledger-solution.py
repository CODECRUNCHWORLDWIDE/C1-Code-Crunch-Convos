"""problem-02-dues-ledger-solution.py — fixtures over a real CSV, proven headless.

Two fixtures share the sample data: one hands back a list of dues records, the
other writes those same records to a real CSV in pytest's throwaway ``tmp_path``
and cleans it up afterwards. Building the data from one table keeps the two
fixtures from drifting apart.

One file carries the module, the tests, and a ``main()`` that drives pytest and
prints a plain, same-every-time report.

Run it with::

    python problem-02-dues-ledger-solution.py
"""

from __future__ import annotations

import contextlib
import csv
import io
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

# --------------------------------------------------------------------------- #
# ledger.py — the module under test, given complete
# --------------------------------------------------------------------------- #

Dues = dict[str, Any]


def load_dues(path: Path) -> list[Dues]:
    """Read a dues CSV (columns: ``member``, ``owed_cents``) into records.

    ``owed_cents`` is parsed from text into an int, so callers never do
    arithmetic on strings.
    """
    dues: list[Dues] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            dues.append({"member": row["member"], "owed_cents": int(row["owed_cents"])})
    return dues


def members_in_arrears(dues: list[Dues], threshold_cents: int) -> list[str]:
    """Names of members owing strictly more than ``threshold_cents``, sorted A-Z."""
    return sorted(row["member"] for row in dues if row["owed_cents"] > threshold_cents)


# --------------------------------------------------------------------------- #
# test_ledger.py — fixture-driven tests
# --------------------------------------------------------------------------- #

THRESHOLD = 500

DUES_ROWS: tuple[tuple[str, str], ...] = (
    ("Ada", "1200"),
    ("Grace", "500"),
    ("Linus", "0"),
    ("Yukihiro", "750"),
)


@pytest.fixture
def dues() -> list[Dues]:
    """Four members: two over the threshold, one exactly on it, one clear."""
    return [{"member": member, "owed_cents": int(owed)} for member, owed in DUES_ROWS]


@pytest.fixture
def dues_csv(tmp_path: Path) -> Iterator[Path]:
    """Write the same four rows to a real CSV and yield its path."""
    path = tmp_path / "dues.csv"
    rows = ["member,owed_cents"]
    rows.extend(",".join(row) for row in DUES_ROWS)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    yield path
    path.unlink()
    assert not path.exists()


def test_arrears_are_sorted_alphabetically(dues: list[Dues]) -> None:
    """Only the two who owe more than the threshold, in order."""
    assert members_in_arrears(dues, THRESHOLD) == ["Ada", "Yukihiro"]


def test_exactly_on_the_threshold_is_not_in_arrears(dues: list[Dues]) -> None:
    """Owing exactly the threshold is not owing *more* than it."""
    assert "Grace" not in members_in_arrears(dues, THRESHOLD)


def test_nobody_over_a_high_threshold_returns_empty_list(dues: list[Dues]) -> None:
    """The answer is an empty list, not None."""
    assert members_in_arrears(dues, 100_000) == []


def test_mutation_does_not_leak_part_one(dues: list[Dues]) -> None:
    """Damage the fixture data on purpose."""
    dues.pop()
    assert len(dues) == 3


def test_mutation_does_not_leak_part_two(dues: list[Dues]) -> None:
    """The damage did not survive: this test gets all four rows back."""
    assert len(dues) == 4


def test_load_dues_reads_every_row(dues_csv: Path) -> None:
    """Four data rows become four records; the header becomes none."""
    assert len(load_dues(dues_csv)) == 4


def test_load_dues_parses_amount_as_int(dues_csv: Path) -> None:
    """The owed column arrives as an int, not as a string."""
    assert load_dues(dues_csv)[0]["owed_cents"] == 1200


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes."""
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Show who is in arrears, then run the suite and print the outcomes."""
    sample = [{"member": m, "owed_cents": int(o)} for m, o in DUES_ROWS]
    print(f"Threshold is {THRESHOLD} cents. In arrears = owing strictly more.")
    print(f"  in arrears: {members_in_arrears(sample, THRESHOLD)}")
    print("  Grace owes exactly the threshold, so she is NOT in arrears: "
          f"{'Grace' not in members_in_arrears(sample, THRESHOLD)}")

    print()
    print("The seven tests, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
