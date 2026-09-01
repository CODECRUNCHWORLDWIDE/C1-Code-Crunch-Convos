"""FizzBuzz, grown one failing test at a time.

Nothing in this module was written before a test demanded it. See README.md for
the RED / GREEN / REFACTOR log that produced it.
"""

from __future__ import annotations

__all__ = ["fizzbuzz"]


def fizzbuzz(n: int) -> list[str]:
    """Return the FizzBuzz sequence for the numbers 1..n inclusive.

    Args:
        n: How many entries to produce. ``0`` produces an empty list.

    Raises:
        ValueError: if *n* is negative.
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
