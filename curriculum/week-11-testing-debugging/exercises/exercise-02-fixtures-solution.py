"""exercise-02-fixtures-solution.py — fixture-driven tests, proven headless.

Normally you keep ``roster.py`` and ``test_roster.py`` in two files and run
``pytest``. A published answer is run as a plain script instead, so this one
file carries the module, the tests, and a small ``main()`` that drives pytest
itself and prints a plain, same-every-time report.

The two fixtures are the point of the exercise. ``loans`` is a *factory* —
pytest calls it again for every test, so one test cannot damage the next.
``roster_csv`` writes a real file into pytest's throwaway ``tmp_path`` directory,
hands the test its path, and then cleans it up after the ``yield``.

Run it with::

    python exercise-02-fixtures-solution.py
"""

from __future__ import annotations

import contextlib
import csv
import io
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Any

import pytest

# --------------------------------------------------------------------------- #
# roster.py — the module under test, given complete
# --------------------------------------------------------------------------- #

Loan = dict[str, Any]


def load_loans(path: Path) -> list[Loan]:
    """Read a loan roster CSV into a list of loan records.

    The file has three columns: ``item``, ``borrower``, ``due``. The ``due``
    column is parsed from ISO format (``YYYY-MM-DD``) into a ``date``.
    """
    loans: list[Loan] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            loans.append(
                {
                    "item": row["item"],
                    "borrower": row["borrower"],
                    "due": date.fromisoformat(row["due"]),
                }
            )
    return loans


def overdue_items(loans: list[Loan], today: date) -> list[str]:
    """Return the names of items due strictly before ``today``, sorted A-Z."""
    return sorted(loan["item"] for loan in loans if loan["due"] < today)


# --------------------------------------------------------------------------- #
# test_roster.py — the seven fixture-driven tests
# --------------------------------------------------------------------------- #

TODAY = date(2026, 3, 10)

ROSTER_ROWS: tuple[tuple[str, str, str], ...] = (
    ("circular saw", "Ada", "2026-03-01"),
    ("hedge trimmer", "Linus", "2026-03-09"),
    ("ladder", "Grace", "2026-03-10"),
    ("pressure washer", "Ada", "2026-03-15"),
)


@pytest.fixture
def loans() -> list[Loan]:
    """Four loans: two overdue, one due today, one due next week."""
    return [
        {"item": item, "borrower": borrower, "due": date.fromisoformat(due)}
        for item, borrower, due in ROSTER_ROWS
    ]


@pytest.fixture
def roster_csv(tmp_path: Path) -> Iterator[Path]:
    """Write the same four loans to a real CSV and yield its path."""
    path = tmp_path / "roster.csv"
    rows = ["item,borrower,due"]
    rows.extend(",".join(row) for row in ROSTER_ROWS)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    yield path
    path.unlink()
    assert not path.exists()


def test_overdue_items_are_sorted_alphabetically(loans: list[Loan]) -> None:
    """Both genuinely late items come back, in alphabetical order."""
    assert overdue_items(loans, TODAY) == ["circular saw", "hedge trimmer"]


def test_due_today_is_not_overdue(loans: list[Loan]) -> None:
    """An item due today has until closing time, so it is not late yet."""
    assert "ladder" not in overdue_items(loans, TODAY)


def test_nothing_overdue_returns_empty_list(loans: list[Loan]) -> None:
    """Before every due date the answer is an empty list, not None."""
    assert overdue_items(loans, date(2026, 2, 1)) == []


def test_mutating_the_fixture_does_not_leak_part_one(loans: list[Loan]) -> None:
    """Damage the fixture data on purpose."""
    loans.pop()
    assert len(loans) == 3


def test_mutating_the_fixture_does_not_leak_part_two(loans: list[Loan]) -> None:
    """The damage did not survive: this test gets all four loans back."""
    assert len(loans) == 4


def test_load_loans_reads_every_row(roster_csv: Path) -> None:
    """Four data rows become four records; the header becomes none."""
    assert len(load_loans(roster_csv)) == 4


def test_load_loans_parses_the_due_date(roster_csv: Path) -> None:
    """The due column arrives as a date object, not as a string."""
    assert load_loans(roster_csv)[0]["due"] == date(2026, 3, 1)


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
    """Show what the filter returns, then run the suite and print outcomes."""
    sample = [
        {"item": item, "borrower": borrower, "due": date.fromisoformat(due)}
        for item, borrower, due in ROSTER_ROWS
    ]
    print(f"Today is {TODAY.isoformat()}. Overdue means due strictly before that.")
    print(f"  overdue right now : {overdue_items(sample, TODAY)}")
    print("  the ladder is due today, so it is NOT overdue: "
          f"{'ladder' not in overdue_items(sample, TODAY)}")

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
