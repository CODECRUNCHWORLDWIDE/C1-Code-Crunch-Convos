"""problem-06-shelf-order-regression-solution.py — reproduce a bug, then fix it.

A bug report says shelf ``A-10`` is listed before ``A-2``. The discipline is:
write a test that *reproduces* the report and fails on the broken code (RED),
then fix the code so the test passes (GREEN), and keep that test forever so the
bug can never sneak back. That kept test is a *regression test*.

This file ships the fixed ``shelf_order`` plus the regression suite, and its
``main()`` shows the broken behaviour beside the fixed one before running the
suite. One file, driven by pytest, printing a plain, same-every-time report.

Run it with::

    python problem-06-shelf-order-regression-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# shelving.py — the FIXED module: a natural sort key, not a plain string sort
# --------------------------------------------------------------------------- #


def shelf_order(codes: list[str]) -> list[str]:
    """Sort shelf codes like ``"A-2"`` in natural order (``A-2`` before ``A-10``).

    A plain string sort puts ``"A-10"`` before ``"A-2"``, because ``"1"`` sorts
    before ``"2"`` character by character. The fix is a key that reads the slot
    as a number.
    """
    return sorted(codes, key=_natural_key)


def _natural_key(code: str) -> tuple[str, int]:
    """Split ``"A-10"`` into ``("A", 10)`` so the slot sorts numerically."""
    aisle, dash, slot = code.partition("-")
    if not dash or not slot.isdigit():
        raise ValueError(f"malformed shelf code: {code!r}")
    return aisle, int(slot)


def _broken_shelf_order(codes: list[str]) -> list[str]:
    """The original, buggy version — a plain string sort. Kept only for the demo."""
    return sorted(codes)


# --------------------------------------------------------------------------- #
# test_shelving.py — the regression test plus the rest of the contract
# --------------------------------------------------------------------------- #


def test_regression_a10_sorts_after_a2() -> None:
    """The exact bug from the report: A-10 must come after A-2, not before."""
    assert shelf_order(["A-10", "A-2"]) == ["A-2", "A-10"]


def test_natural_order_within_an_aisle() -> None:
    """A whole aisle sorts by slot number, not by string."""
    assert shelf_order(["A-2", "A-10", "A-1"]) == ["A-1", "A-2", "A-10"]


def test_sorts_across_aisles_then_slots() -> None:
    """Aisle letter first, then slot number."""
    assert shelf_order(["B-1", "A-2", "A-10"]) == ["A-2", "A-10", "B-1"]


def test_empty_list_stays_empty() -> None:
    """No codes in, an empty list out — not None."""
    assert shelf_order([]) == []


def test_malformed_code_is_rejected() -> None:
    """A code with no numeric slot is bad data, and says so."""
    with pytest.raises(ValueError, match="malformed shelf code"):
        shelf_order(["A-2", "A-top"])


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
    """Show the bug beside the fix, then run the regression suite."""
    codes = ["A-10", "A-2", "A-1", "B-1"]
    print(f"Input: {codes}")
    print(f"  broken (plain string sort): {_broken_shelf_order(codes)}")
    print(f"  fixed  (natural-key sort) : {shelf_order(codes)}")
    print("  the bug was A-10 landing before A-2; the fix reads the slot as a number.")

    print()
    print("The regression suite, run the way pytest runs it:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
