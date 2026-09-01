"""Find the two numbers that add up to a target, in one pass.

Week 5 homework, problem 3, Code Crunch Convos.

Add ``two_sum`` to your own ``week-05-solutions.py``. This file is the published
answer, and the longer name keeps it from landing on top of your work.

The slow way asks, of every pair, "do these two add up?". This way asks one
question per number instead: "have I already walked past the number that would
finish this pair?". That question is a dict lookup, so the whole search is one
pass over the list.
"""


def two_sum(nums: list[int], t: int) -> tuple[int, int] | None:
    """Return the indices (i, j), i < j, with nums[i] + nums[j] == t.

    Args:
        nums: The numbers to search. May be empty.
        t: The total the two numbers must reach.

    Returns:
        The pair of indices, or None when no pair reaches ``t``. When several
        pairs would work, the one that finishes earliest wins.

    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        (0, 1)
    """
    seen: dict[int, int] = {}
    for j, num in enumerate(nums):
        i = seen.get(t - num)
        if i is not None:
            return (i, j)
        seen.setdefault(num, j)
    return None


def _check() -> None:
    """Run the four asserts the brief requires, plus four it implies."""
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert two_sum([1, 2, 3], 100) is None
    assert two_sum([], 5) is None
    assert two_sum([3, 3], 6) == (0, 1)
    assert two_sum([3], 6) is None
    assert two_sum([0, 0], 0) == (0, 1)
    assert two_sum([-3, 4, 3, 90], 0) == (0, 2)


def _demo() -> None:
    """Print the brief's three examples, then the two that catch the bugs."""
    print(two_sum([2, 7, 11, 15], 9))
    print(two_sum([3, 2, 4], 6))
    print(two_sum([1, 2, 3], 100))
    print(two_sum([3, 3], 6))
    print(two_sum([3], 6))
    print("All 8 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
