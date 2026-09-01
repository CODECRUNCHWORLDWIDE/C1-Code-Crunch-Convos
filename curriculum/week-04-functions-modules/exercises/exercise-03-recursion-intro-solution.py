"""exercise-03-recursion-intro-solution.py — counting ways to seat volunteers.

Two factorials that agree: one built from a loop, one built from the
recurrence n! = n * (n - 1)!. Then one real use for them.

The self-checks at the bottom are the starter's, unchanged. The loop over
range(16) is the important one: it proves the two implementations agree
sixteen times running.
"""


def factorial_iterative(n: int) -> int:
    """Return n! computed with a loop.

    Args:
        n: A non-negative integer.

    Returns:
        The product 1 * 2 * ... * n, and 1 when n is 0.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    product = 1
    for factor in range(2, n + 1):
        product *= factor
    return product


def factorial_recursive(n: int) -> int:
    """Return n! by calling itself. Same contract as factorial_iterative.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


def arrangements(n: int, k: int) -> int:
    """Return the number of ordered ways to seat k of n volunteers.

    Args:
        n: How many volunteers turned up.
        k: How many chairs there are.

    Returns:
        n! // (n - k)!

    Raises:
        ValueError: If n or k is negative, or if k is greater than n.
    """
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    if k > n:
        raise ValueError("k must not be greater than n")
    return factorial_iterative(n) // factorial_iterative(n - k)


if __name__ == "__main__":
    assert factorial_iterative(0) == 1, factorial_iterative(0)
    assert factorial_iterative(1) == 1, factorial_iterative(1)
    assert factorial_iterative(5) == 120, factorial_iterative(5)
    assert factorial_iterative(10) == 3_628_800, factorial_iterative(10)
    assert factorial_iterative(20) == 2_432_902_008_176_640_000

    for n in range(16):
        assert factorial_recursive(n) == factorial_iterative(n), n

    for fn in (factorial_iterative, factorial_recursive):
        try:
            fn(-1)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{fn.__name__}(-1) should raise ValueError")

    assert arrangements(5, 0) == 1, arrangements(5, 0)
    assert arrangements(5, 2) == 20, arrangements(5, 2)
    assert arrangements(6, 3) == 120, arrangements(6, 3)
    assert arrangements(4, 4) == 24, arrangements(4, 4)

    try:
        arrangements(3, 5)
    except ValueError:
        pass
    else:
        raise AssertionError("k greater than n should raise ValueError")

    print(f"0! = {factorial_iterative(0)}")
    print(f"5! = {factorial_recursive(5)}")
    print(f"20! = {factorial_iterative(20)}")
    print(f"Seating 2 of 5 volunteers: {arrangements(5, 2)} ways")
    print("Iterative and recursive agree for n = 0 through 15.")
    print("All checks passed.")
