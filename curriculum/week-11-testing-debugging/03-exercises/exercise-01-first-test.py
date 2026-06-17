"""
Exercise 01 — Your first pytest tests.

Goal: write tests for the small ``Calculator`` class below.

This file plays two roles at once: it contains both the code under test
(the ``Calculator`` class) and the tests that exercise it. In real
projects you would split them into ``calculator.py`` and
``test_calculator.py`` — for a learning exercise it is easier to keep
them together.

Run with:

    pytest exercise-01-first-test.py -v

You should see 6 failing tests when you start, all marked with TODO.
When you are done, all 6 must pass.

Reference:
    https://docs.pytest.org/en/stable/getting-started.html
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Code under test — DO NOT modify the class. Modify only the test functions.
# ---------------------------------------------------------------------------


class Calculator:
    """A tiny calculator that tracks the last computed result."""

    def __init__(self) -> None:
        self.last_result: float = 0.0

    def add(self, a: float, b: float) -> float:
        """Return ``a + b`` and remember the result."""
        self.last_result = a + b
        return self.last_result

    def subtract(self, a: float, b: float) -> float:
        """Return ``a - b`` and remember the result."""
        self.last_result = a - b
        return self.last_result

    def divide(self, a: float, b: float) -> float:
        """Return ``a / b``. Raises ``ZeroDivisionError`` if ``b`` is 0."""
        if b == 0:
            raise ZeroDivisionError("cannot divide by zero")
        self.last_result = a / b
        return self.last_result


# ---------------------------------------------------------------------------
# TESTS — replace each ``assert False`` with a real assertion.
# ---------------------------------------------------------------------------


def test_add_two_positive_numbers() -> None:
    """``add`` should return the arithmetic sum of two positive numbers."""
    calc = Calculator()
    # TODO: assert that calc.add(2, 3) returns 5
    assert False, "replace me"


def test_add_updates_last_result() -> None:
    """After calling ``add``, ``last_result`` should equal the return value."""
    calc = Calculator()
    calc.add(10, 5)
    # TODO: assert that calc.last_result equals 15
    assert False, "replace me"


def test_subtract_negative_result() -> None:
    """Subtracting a larger value should give a negative result."""
    calc = Calculator()
    # TODO: assert that calc.subtract(3, 10) returns -7
    assert False, "replace me"


def test_divide_normal_case() -> None:
    """Plain division should return a float."""
    calc = Calculator()
    # TODO: assert that calc.divide(10, 4) returns 2.5
    assert False, "replace me"


def test_divide_by_zero_raises() -> None:
    """Dividing by zero must raise ``ZeroDivisionError``."""
    calc = Calculator()
    # TODO: use ``with pytest.raises(...)`` to assert the right exception fires.
    # Hint:
    #     with pytest.raises(ZeroDivisionError):
    #         calc.divide(5, 0)
    assert False, "replace me"


def test_divide_by_zero_error_message() -> None:
    """The error message should be helpful."""
    calc = Calculator()
    # TODO: use ``pytest.raises(..., match="cannot divide by zero")`` to
    # also assert the message text.
    assert False, "replace me"
