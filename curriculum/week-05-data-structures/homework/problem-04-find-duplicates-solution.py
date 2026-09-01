"""Report every item that turns up more than once, by counting.

Week 5 homework, problem 4, Code Crunch Convos.

Add ``find_duplicates`` to your own ``week-05-solutions.py``. This file is the
published answer, and the longer name keeps it from landing on top of your work.

One pass builds a tally. A second pass keeps the tallies above one. Nothing is
ever compared against everything else, which is why this stays fast on a long
list.
"""


def find_duplicates(items: list) -> list:
    """Return a sorted list of the items that appear more than once.

    Args:
        items: The items to inspect. They must be hashable, so that they can be
            counted in a dict, and comparable to each other, so that the answer
            can be sorted.

    Returns:
        A new sorted list. Each repeated item appears once, however many copies
        there were.

    Example:
        >>> find_duplicates([1, 2, 3, 2, 4, 5, 1, 1])
        [1, 2]
    """
    counts: dict = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return sorted(item for item, n in counts.items() if n > 1)


def _check() -> None:
    """Run the three asserts the brief requires, plus two it implies."""
    assert find_duplicates([1, 2, 3, 2, 4, 5, 1, 1]) == [1, 2]
    assert find_duplicates(["a", "b", "c"]) == []
    assert find_duplicates(["x", "x", "y", "y", "z"]) == ["x", "y"]
    assert find_duplicates([]) == []
    assert find_duplicates([5, 5, 5, 5]) == [5]


def _demo() -> None:
    """Print the brief's two examples, then the two edge cases."""
    print(find_duplicates([1, 2, 3, 2, 4, 5, 1, 1]))
    print(find_duplicates(["a", "b", "c"]))
    print(find_duplicates(["x", "x", "y", "y", "z"]))
    print(find_duplicates([5, 5, 5, 5]))
    print("All 5 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
