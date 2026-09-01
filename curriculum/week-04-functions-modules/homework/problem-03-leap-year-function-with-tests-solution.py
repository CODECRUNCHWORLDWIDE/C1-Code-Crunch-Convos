"""Gregorian leap-year test, plus a self-check that runs with the file.

Week 4 homework, problem 3, Code Crunch Convos.

Save your own copy as ``leap.py`` in your ``homework/`` folder.

``is_leap_year`` answers the question. ``_run_tests`` asks it six times
with answers already known, and says one line about how it went. That
second function is the point of this problem: a function you can check is
worth more than a function you believe.
"""

CASES: list[tuple[int, bool]] = [
    (2000, True),
    (1900, False),
    (2024, True),
    (2023, False),
    (2100, False),
    (2400, True),
]


def is_leap_year(year: int) -> bool:
    """Return True if `year` is a leap year in the Gregorian calendar.

    Args:
        year: A year number, for example 2024.

    Returns:
        True for a leap year, False otherwise.

    Example:
        >>> is_leap_year(1900)
        False
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


def _run_tests() -> None:
    """Check every case in CASES and report the first failure, or success."""
    for year, expected in CASES:
        got = is_leap_year(year)
        if got != expected:
            print(f"FAIL: is_leap_year({year}) -> {got}, expected {expected}")
            return
    print("All tests passed")


if __name__ == "__main__":
    _run_tests()
