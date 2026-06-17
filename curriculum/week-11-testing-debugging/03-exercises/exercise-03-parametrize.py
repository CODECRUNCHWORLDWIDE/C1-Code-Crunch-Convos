"""
Exercise 03 — Table-driven tests with ``@pytest.mark.parametrize``.

Goal: replace one boring repetitive test with one parametrized test
that covers 6 different leap-year cases.

Run with:

    pytest exercise-03-parametrize.py -v

You should see 6 individual test runs (one per row of the parametrize
table) once you finish the TODOs.

Reference:
    https://docs.pytest.org/en/stable/how-to/parametrize.html
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Code under test.
# ---------------------------------------------------------------------------


def is_leap_year(year: int) -> bool:
    """Return True if ``year`` is a Gregorian leap year.

    A year is a leap year if it is divisible by 4, *except* end-of-century
    years (divisible by 100) — those are only leap years if they are also
    divisible by 400.

    Examples:
        2020 -> True   (divisible by 4)
        2021 -> False  (not divisible by 4)
        1900 -> False  (divisible by 100 but not 400)
        2000 -> True   (divisible by 400)
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


# ---------------------------------------------------------------------------
# TESTS — finish the parametrize call below.
# ---------------------------------------------------------------------------


# TODO: fill in 6 (year, expected) pairs that together cover:
#       1. A year divisible by 4 but not 100 (e.g. 2024 -> True)
#       2. A year not divisible by 4         (e.g. 2023 -> False)
#       3. A year divisible by 100 but not 400 (e.g. 1900 -> False)
#       4. A year divisible by 400            (e.g. 2000 -> True)
#       5. A pre-1900 leap year               (e.g. 1600 -> True)
#       6. A far-future ordinary year         (e.g. 2101 -> False)


@pytest.mark.parametrize(
    "year, expected",
    [
        # TODO: replace these placeholders with the 6 real cases.
        (0, False),
        (0, False),
        (0, False),
        (0, False),
        (0, False),
        (0, False),
    ],
)
def test_is_leap_year(year: int, expected: bool) -> None:
    assert is_leap_year(year) == expected, (
        f"is_leap_year({year}) returned {is_leap_year(year)!r}, "
        f"expected {expected!r}"
    )


# ---------------------------------------------------------------------------
# Stretch goal — add ``ids=`` to give each row a readable name.
# ---------------------------------------------------------------------------
#
# TODO (optional): re-write the decorator with an ``ids`` argument like
#
#     ids=["common-leap", "ordinary-odd", "century-not-400",
#          "divisible-by-400", "ancient-leap", "far-future-ordinary"]
#
# Run with ``pytest -v`` and notice how the test names change.
