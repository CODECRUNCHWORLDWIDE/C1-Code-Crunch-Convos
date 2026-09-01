"""Sort words into one bucket per starting letter, keeping their order.

Week 5 homework, problem 5, Code Crunch Convos.

Add ``group_by_first_letter`` to your own ``week-05-solutions.py``. This file is
the published answer, and the longer name keeps it from landing on top of your
work.

``setdefault`` is the whole trick. It hands back the list already stored under a
letter, or puts a fresh empty one there first and hands back that. Either way
what comes back is the list living inside the dict, so appending to it changes
the dict.
"""


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    """Map each starting letter to the words that begin with it, in order.

    Args:
        words: Already-lowercased words. None of them may be empty.

    Returns:
        A new dict. Each list holds its words in the order they arrived, and the
        letters themselves come out in first-seen order.

    Example:
        >>> group_by_first_letter(["apple", "ant", "bee"])
        {'a': ['apple', 'ant'], 'b': ['bee']}
    """
    groups: dict[str, list[str]] = {}
    for word in words:
        groups.setdefault(word[0], []).append(word)
    return groups


def _check() -> None:
    """Run the three asserts the brief requires, plus one it implies."""
    result = group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])
    assert result == {"a": ["apple", "ant"], "b": ["bee", "banana"], "c": ["cherry"]}
    assert group_by_first_letter([]) == {}
    assert group_by_first_letter(["zebra"]) == {"z": ["zebra"]}
    assert list(result) == ["a", "b", "c"]


def _demo() -> None:
    """Print the brief's example, the two small cases, and the key order."""
    print(group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"]))
    print(group_by_first_letter([]))
    print(group_by_first_letter(["zebra"]))
    print(list(group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])))
    print("All 4 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
