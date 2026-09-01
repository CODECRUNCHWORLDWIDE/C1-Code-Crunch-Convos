"""exercise-03-parametrize-solution.py — table-driven tests, proven headless.

Normally you keep ``money.py`` and ``test_money.py`` in two files and run
``pytest``. A published answer is run as a plain script, so this one file
carries the module, the two parametrized tests, and a ``main()`` that drives
pytest itself and prints a plain, same-every-time report.

A parametrized test is one function run once per row of a table. Twelve rows,
twelve tests, one body — and when a row fails, the report names that row so you
know exactly which input broke.

Run it with::

    python exercise-03-parametrize-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# money.py — the module under test, three lines of body
# --------------------------------------------------------------------------- #


def format_cents(cents: int) -> str:
    """Render a whole number of cents as a US dollar string.

    Always two decimal places, always comma-grouped thousands, e.g.
    ``"$1,234.56"``. A negative amount is a caller bug, not a credit, so it
    raises rather than printing ``"$-1.99"``.
    """
    if cents < 0:
        raise ValueError("cents cannot be negative")
    dollars, remainder = divmod(cents, 100)
    return f"${dollars:,}.{remainder:02d}"


# --------------------------------------------------------------------------- #
# test_money.py — one table of good inputs, one table of bad inputs
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "cents, expected",
    [
        (0, "$0.00"),
        (5, "$0.05"),
        (25, "$0.25"),
        (99, "$0.99"),
        (100, "$1.00"),
        (250, "$2.50"),
        (1_000, "$10.00"),
        (123_456, "$1,234.56"),
        (100_000_000, "$1,000,000.00"),
    ],
    ids=[
        "zero",
        "nickel",
        "quarter",
        "under-a-dollar",
        "one-dollar",
        "two-fifty",
        "ten-dollars",
        "four-figures",
        "one-million",
    ],
)
def test_format_cents(cents: int, expected: str) -> None:
    """Every listed amount renders exactly as written."""
    assert format_cents(cents) == expected


@pytest.mark.parametrize(
    "cents",
    [-1, -25, -100],
    ids=["minus-one-cent", "minus-a-quarter", "minus-a-dollar"],
)
def test_negative_cents_is_rejected(cents: int) -> None:
    """A negative amount is a caller bug, not a credit."""
    with pytest.raises(ValueError, match="cannot be negative"):
        format_cents(cents)


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


def _unguarded(cents: int) -> str:
    """What format_cents would return with the guard deleted — for the demo."""
    dollars, remainder = divmod(cents, 100)
    return f"${dollars:,}.{remainder:02d}"


def main() -> None:
    """Show the formatter, the hazard the guard prevents, then run the suite."""
    print("A few amounts, formatted:")
    for cents in (5, 250, 123_456, 100_000_000):
        print(f"  {cents:>11} cents -> {format_cents(cents)}")

    print()
    print("Why the guard matters — divmod on a negative rounds toward -inf:")
    print(f"  divmod(-1, 100) == {divmod(-1, 100)}")
    print(f"  with NO guard, format_cents(-1) would return {_unguarded(-1)!r}")
    try:
        format_cents(-1)
    except ValueError as error:
        print(f"  with the guard, format_cents(-1) raises ValueError: {error}")

    print()
    print("The twelve cases, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
