"""problem-03-hours-minutes-solution.py — table-driven tests, proven headless.

The front desk shows how long a tool has been out as ``H:MM``. The rule fits on
one line and still hides an off-by-one: five minutes must render ``0:05``, not
``0:5``. A parametrized test — one function run once per row of a table — makes a
tenth case cost one line, so you stop rationing the cases the bugs hide in.

One file carries the module, the two tables, and a ``main()`` that drives pytest
and prints a plain, same-every-time report.

Run it with::

    python problem-03-hours-minutes-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# checkout.py — the module under test
# --------------------------------------------------------------------------- #


def format_hm(total_minutes: int) -> str:
    """Render a whole number of minutes as ``H:MM``.

    The minutes part is always two digits (``0:05``), the hours part has no
    upper bound (``10:00``). A negative duration is a caller bug.
    """
    if total_minutes < 0:
        raise ValueError("total_minutes cannot be negative")
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}:{minutes:02d}"


# --------------------------------------------------------------------------- #
# test_checkout.py — one table of good inputs, one of bad inputs
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "minutes, expected",
    [
        (0, "0:00"),
        (5, "0:05"),
        (59, "0:59"),
        (60, "1:00"),
        (65, "1:05"),
        (600, "10:00"),
        (1_439, "23:59"),
    ],
    ids=[
        "zero",
        "five-minutes",
        "under-an-hour",
        "one-hour",
        "one-hour-five",
        "ten-hours",
        "almost-a-day",
    ],
)
def test_format_hm(minutes: int, expected: str) -> None:
    """Every listed duration renders exactly as written."""
    assert format_hm(minutes) == expected


@pytest.mark.parametrize(
    "minutes",
    [-1, -60],
    ids=["minus-one", "minus-an-hour"],
)
def test_negative_is_rejected(minutes: int) -> None:
    """A negative duration is a caller bug, not a display problem."""
    with pytest.raises(ValueError, match="cannot be negative"):
        format_hm(minutes)


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each case's id and outcome, in order."""

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
    """Show a few durations, then run the suite and print the outcomes."""
    print("format_hm(minutes):")
    for minutes in (5, 65, 600):
        print(f"  {minutes:>5} minutes -> {format_hm(minutes)}")

    print()
    print("The nine cases, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
