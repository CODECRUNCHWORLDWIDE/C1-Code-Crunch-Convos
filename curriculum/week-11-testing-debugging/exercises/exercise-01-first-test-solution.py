"""exercise-01-first-test-solution.py — first pytest tests, proven headless.

You normally run tests with the ``pytest`` command, which finds every
``test_*`` function and reports on it. A published answer cannot lean on that,
because the grader runs it as a plain script: ``python this_file.py``. A file
full of ``test_`` functions prints nothing when you do that — pytest is what
calls them, and pytest is not in the room.

So this one file carries three things at once: the fixed ``lending.py`` code,
the five tests from ``test_lending.py``, and a tiny ``main()`` that *drives
pytest itself* and prints a plain, same-every-time report. In your own Week 11
folder you keep the module and the tests in two files and run ``pytest``. Here
they travel together so the download runs on its own.

Run it with::

    python exercise-01-first-test-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# lending.py — the module under test, with the two-line fix applied
# --------------------------------------------------------------------------- #

DAILY_FEE_CENTS: int = 25
MAX_FEE_CENTS: int = 1_000


def late_fee_cents(days_late: int) -> int:
    """Return the late fee, in whole cents, for an item returned late.

    Zero days late is free. Each further day adds ``DAILY_FEE_CENTS``, and the
    total never climbs past ``MAX_FEE_CENTS``. A negative day count is a caller
    bug, not a refund, so it raises.
    """
    if days_late < 0:
        raise ValueError("days_late cannot be negative")
    return min(days_late * DAILY_FEE_CENTS, MAX_FEE_CENTS)


# --------------------------------------------------------------------------- #
# test_lending.py — the five tests, exactly as the exercise asks for them
# --------------------------------------------------------------------------- #


def test_on_time_is_free() -> None:
    """Zero days late costs nothing."""
    assert late_fee_cents(0) == 0


def test_one_day_late_costs_a_quarter() -> None:
    """One day late is a single daily charge."""
    assert late_fee_cents(1) == 25


def test_ten_days_late_costs_two_fifty() -> None:
    """Ten days late is ten daily charges, still under the cap."""
    assert late_fee_cents(10) == 250


def test_fee_stops_at_the_cap() -> None:
    """A very late return is billed at the cap, not the raw daily rate."""
    assert late_fee_cents(100) == MAX_FEE_CENTS


def test_negative_days_is_rejected() -> None:
    """A negative day count is a caller bug, not a refund."""
    with pytest.raises(ValueError):
        late_fee_cents(-3)


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        # The "call" phase is the test body itself; setup/teardown are separate.
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes.

    pytest's own console output is captured and dropped so the report below is
    identical on every machine — no timings, no platform banner, no plugin
    version line to drift.
    """
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Show the fixed fee rules, then run the suite and print the outcomes."""
    print("The late-fee rules, after the two-line fix:")
    for day in (0, 1, 10, 100):
        note = "  (capped: the raw rate was 2500)" if day == 100 else ""
        print(f"  {day:>3} days late -> {late_fee_cents(day):>4} cents{note}")
    try:
        late_fee_cents(-3)
    except ValueError as error:
        print(f"   -3 days late -> ValueError: {error}")

    print()
    print("The five tests, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
