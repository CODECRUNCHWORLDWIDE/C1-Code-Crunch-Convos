"""Keep only the keys two dicts share, with the first dict's values.

Week 5 homework, problem 6, Code Crunch Convos.

Add ``intersect_dicts`` to your own ``week-05-solutions.py``. This file is the
published answer, and the longer name keeps it from landing on top of your work.

``key in d2`` tests keys, and it is a single lookup rather than a scan. That one
fact is what turns this from a loop inside a loop into a single walk over the
first dict.
"""


def intersect_dicts(d1: dict, d2: dict) -> dict:
    """Return the keys present in both dicts, with the values from d1.

    Args:
        d1: The dict the keys and the values come from.
        d2: The dict used only as a filter. Its values are never read.

    Returns:
        A new dict, in d1's insertion order. Neither input is changed.

    Example:
        >>> intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100})
        {'b': 2, 'c': 3}
    """
    return {key: value for key, value in d1.items() if key in d2}


def _check() -> None:
    """Run the three asserts the brief requires, plus two it implies."""
    assert intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4}) == {
        "b": 2,
        "c": 3,
    }
    assert intersect_dicts({}, {"a": 1}) == {}
    assert intersect_dicts({"x": 1}, {"x": 1}) == {"x": 1}
    assert intersect_dicts({"a": 1}, {}) == {}
    assert list(intersect_dicts({"c": 1, "a": 2}, {"a": 0, "c": 0})) == ["c", "a"]


def _demo() -> None:
    """Print the brief's example, the two empty cases, and the key order."""
    print(intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4}))
    print(intersect_dicts({}, {"a": 1}))
    print(intersect_dicts({"x": 1}, {"x": 1}))
    print(list(intersect_dicts({"c": 1, "a": 2}, {"a": 0, "c": 0})))
    print("All 5 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
