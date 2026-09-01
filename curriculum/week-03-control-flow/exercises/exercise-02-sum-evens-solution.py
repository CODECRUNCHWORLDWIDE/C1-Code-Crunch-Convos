"""exercise-02-sum-evens-solution.py — the accumulator pattern, checked by arithmetic.

Adds the even numbers from 2 up to a limit, two different ways, and
asserts that the loop and the closed-form formula agree.
"""

CHECK_LIMITS = [-4, 0, 1, 2, 7, 10, 100]


def sum_evens(limit: int) -> int:
    """Return the sum of every even number from 2 to `limit` inclusive.

    Returns 0 when `limit` is less than 2, because there are no even
    numbers in that range to add.
    """
    total = 0
    for number in range(2, limit + 1, 2):
        total += number
    return total


def sum_evens_formula(limit: int) -> int:
    """Return the same sum using the closed form k * (k + 1)."""
    if limit < 2:
        return 0
    k = limit // 2
    return k * (k + 1)


def main() -> None:
    """Compare the loop against the formula for every limit in CHECK_LIMITS."""
    for limit in CHECK_LIMITS:
        looped = sum_evens(limit)
        closed = sum_evens_formula(limit)
        status = "ok" if looped == closed else "MISMATCH"
        print(f"limit={limit:>4}  loop={looped:>6}  formula={closed:>6}  {status}")
        assert looped == closed, f"disagreement at limit={limit}"


if __name__ == "__main__":
    main()
