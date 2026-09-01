"""Sum a list of ints two ways: recursively and iteratively.

Week 4 homework, problem 4, Code Crunch Convos.

Save your own copy as ``recursive_sum.py`` in your ``homework/`` folder.

Two functions answer the same question by different routes, and
``_run_tests`` checks both against the same expected totals. Two
implementations that disagree tell you one of them is wrong, which is more
than one implementation that merely looks right can ever tell you.
"""

CASES: list[tuple[list[int], int]] = [
    ([], 0),
    ([5], 5),
    ([1, 2, 3, 4], 10),
    ([-1, 1], 0),
]


def sum_recursive(nums: list[int]) -> int:
    """Return the sum of `nums` using recursion, without `sum` or a loop.

    Args:
        nums: A list of integers.

    Returns:
        The total.

    Example:
        >>> sum_recursive([1, 2, 3, 4])
        10
    """
    if not nums:
        return 0
    return nums[0] + sum_recursive(nums[1:])


def sum_iterative(nums: list[int]) -> int:
    """Return the sum of `nums` with a plain loop, for comparison.

    Args:
        nums: A list of integers.

    Returns:
        The total.

    Example:
        >>> sum_iterative([1, 2, 3, 4])
        10
    """
    total = 0
    for num in nums:
        total += num
    return total


def _run_tests() -> None:
    """Check both functions against CASES and against each other."""
    for nums, expected in CASES:
        rec = sum_recursive(nums)
        itr = sum_iterative(nums)
        if rec != expected or itr != expected:
            print(f"FAIL: {nums} -> recursive {rec}, iterative {itr}, expected {expected}")
            return
    print("All tests passed")


if __name__ == "__main__":
    _run_tests()
