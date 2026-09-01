"""challenge-01-tdd-fizzbuzz-solution.py — FizzBuzz grown one failing test at a time.

The point of this challenge is not FizzBuzz — it is the rhythm: write a failing
test (RED), write the smallest code that passes it (GREEN), tidy up while the
bar stays green (REFACTOR). Nothing in ``fizzbuzz`` below was written before a
test demanded it. See the exercise page for the full commit log.

You would normally keep ``fizzbuzz.py`` and ``test_fizzbuzz.py`` in two files
and run ``pytest``. A published answer is run as a plain script, so this one
file carries the module, the nine tests, and a ``main()`` that drives pytest
itself and prints a plain, same-every-time report.

Run it with::

    python challenge-01-tdd-fizzbuzz-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# fizzbuzz.py — every line here was demanded by one of the tests below
# --------------------------------------------------------------------------- #


def fizzbuzz(n: int) -> list[str]:
    """Return the FizzBuzz sequence for the numbers 1..n inclusive.

    ``0`` produces an empty list. A negative ``n`` is a caller bug, not an empty
    request, so it raises ``ValueError``.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    return [_label(number) for number in range(1, n + 1)]


def _label(number: int) -> str:
    """Return the FizzBuzz label for a single number."""
    label = ""
    if number % 3 == 0:
        label += "Fizz"
    if number % 5 == 0:
        label += "Buzz"
    return label or str(number)


# --------------------------------------------------------------------------- #
# test_fizzbuzz.py — the nine tests, in the order they were written
# --------------------------------------------------------------------------- #


def test_returns_a_list() -> None:
    assert isinstance(fizzbuzz(1), list)


def test_length_matches_n() -> None:
    assert len(fizzbuzz(5)) == 5


def test_plain_numbers() -> None:
    assert fizzbuzz(2) == ["1", "2"]


def test_three_is_fizz() -> None:
    assert fizzbuzz(3)[2] == "Fizz"


def test_five_is_buzz() -> None:
    assert fizzbuzz(5)[4] == "Buzz"


def test_fifteen_is_fizzbuzz() -> None:
    assert fizzbuzz(15)[14] == "FizzBuzz"


def test_full_output_to_fifteen() -> None:
    assert fizzbuzz(15) == [
        "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz",
        "Buzz", "11", "Fizz", "13", "14", "FizzBuzz",
    ]


def test_zero_returns_empty_list() -> None:
    assert fizzbuzz(0) == []


def test_negative_raises_value_error() -> None:
    with pytest.raises(ValueError, match="must be non-negative"):
        fizzbuzz(-1)


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
    """Show the finished output, then run the suite and print the outcomes."""
    print("fizzbuzz(15):")
    print(f"  {fizzbuzz(15)}")

    print()
    print("The nine tests, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
