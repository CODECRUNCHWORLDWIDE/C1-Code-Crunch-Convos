"""Swap every key with its value, using one dict comprehension.

Week 5 homework, problem 2, Code Crunch Convos.

Add ``invert`` to your own ``week-05-solutions.py``. This file is the published
answer, and the longer name keeps it from landing on top of your work.

``d.items()`` hands out ``(key, value)`` pairs. The comprehension unpacks each
pair into two names and writes them back the other way round. That is the whole
function: one unpack, one re-pack.
"""


def invert(d: dict) -> dict:
    """Swap keys and values. Assumes values are unique and hashable.

    Args:
        d: Any dict whose values can themselves be used as dict keys.

    Returns:
        A new dict. The input is not changed.

    Example:
        >>> invert({"red": 1, "green": 2, "blue": 3})
        {1: 'red', 2: 'green', 3: 'blue'}
    """
    return {value: key for key, value in d.items()}


def _check() -> None:
    """Run the three asserts the brief requires, plus two it implies."""
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert invert({}) == {}
    assert invert({"x": "X", "y": "Y"}) == {"X": "x", "Y": "y"}
    assert invert({"red": 1, "green": 2, "blue": 3}) == {1: "red", 2: "green", 3: "blue"}
    assert invert({"a": 1, "b": 1}) == {1: "b"}


def _demo() -> None:
    """Print the brief's example, the empty case, and the lossy case."""
    print(invert({"red": 1, "green": 2, "blue": 3}))
    print(invert({}))
    print(invert({"x": "X", "y": "Y"}))
    print(invert({"a": 1, "b": 1}))
    print("All 5 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
