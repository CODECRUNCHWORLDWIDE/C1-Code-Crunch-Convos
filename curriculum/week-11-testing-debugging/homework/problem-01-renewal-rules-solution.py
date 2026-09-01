"""problem-01-renewal-rules-solution.py — a decision function, fully tested.

You are handed a rule in English and asked to turn it into a function *and* the
tests that prove it. The skill is choosing inputs that pin every clause of the
rule — including the boundary, where off-by-one bugs live.

One file carries the module, the tests, and a ``main()`` that drives pytest and
prints a plain, same-every-time report. In your own folder you keep the module
and the tests in two files and run ``pytest``.

Run it with::

    python problem-01-renewal-rules-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# renewal.py — the module under test
# --------------------------------------------------------------------------- #

MAX_RENEWALS: int = 2


def can_renew(times_renewed: int, someone_waiting: bool) -> bool:
    """Decide whether a member may renew a loan again.

    A loan may be renewed up to ``MAX_RENEWALS`` times, but never while another
    member is waiting for the item. A negative renewal count is a caller bug.
    """
    if times_renewed < 0:
        raise ValueError("times_renewed cannot be negative")
    if someone_waiting:
        return False
    return times_renewed < MAX_RENEWALS


# --------------------------------------------------------------------------- #
# test_renewal.py — one clause of the rule per test
# --------------------------------------------------------------------------- #


def test_fresh_loan_can_renew() -> None:
    """Never renewed, nobody waiting: yes."""
    assert can_renew(0, someone_waiting=False) is True


def test_one_renewal_can_renew_again() -> None:
    """One renewal used, one still allowed."""
    assert can_renew(1, someone_waiting=False) is True


def test_at_the_limit_cannot_renew() -> None:
    """Two renewals used is the limit, so a third is refused."""
    assert can_renew(MAX_RENEWALS, someone_waiting=False) is False


def test_waitlist_blocks_even_a_fresh_loan() -> None:
    """Someone waiting outranks a renewal you would otherwise be owed."""
    assert can_renew(0, someone_waiting=True) is False


def test_negative_count_is_rejected() -> None:
    """A negative renewal count is a caller bug, not a decision."""
    with pytest.raises(ValueError, match="cannot be negative"):
        can_renew(-1, someone_waiting=False)


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
    """Show the decision table, then run the suite and print the outcomes."""
    print("can_renew(times_renewed, someone_waiting):")
    for renewed, waiting in [(0, False), (1, False), (2, False), (0, True)]:
        print(f"  renewed={renewed}, waiting={waiting!s:<5} -> "
              f"{can_renew(renewed, waiting)}")
    try:
        can_renew(-1, someone_waiting=False)
    except ValueError as error:
        print(f"  renewed=-1                 -> ValueError: {error}")

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
