"""problem-02-json-path-walker-solution.py — list every value in a JSON document.

Walks a decoded JSON document and yields one (path, value) pair for every
primitive value inside it, with the path written the way you would type it:
``address.city``, ``friends[0].name``.

There is no network here. This is the tool you reach for when an API sends you
something large and you need to see what is actually in it -- which is most
Tuesdays.

Run it with::

    python problem-02-json-path-walker-solution.py
"""

from __future__ import annotations

import json
from typing import Any, Iterator

SAMPLE: dict[str, Any] = {
    "name": "Ada",
    "age": 207,
    "address": {"city": "London", "zip": "E1 6AN"},
    "friends": [{"name": "Bob"}, {"name": "Carol"}],
}


def walk(node: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    """Yield (dotted path, value) for every primitive value inside *node*.

    A primitive is anything that is not a dict or a list: str, int, float,
    bool, None. Containers are walked into; only their leaves are yielded.

    Empty containers yield nothing at all, which is the honest answer -- there
    is no value in them to report.

    Args:
        node: A decoded JSON document, or any part of one.
        path: The path that led here. Callers leave this empty.

    Yields:
        One pair per primitive value, in document order.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            yield from walk(value, child)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, f"{path}[{index}]")
    else:
        yield path, node


def check() -> int:
    """Run every example and report.

    Returns:
        The number of checks that ran.
    """
    cases: tuple[tuple[str, Any, list[tuple[str, Any]]], ...] = (
        (
            "the sample document",
            SAMPLE,
            [
                ("name", "Ada"),
                ("age", 207),
                ("address.city", "London"),
                ("address.zip", "E1 6AN"),
                ("friends[0].name", "Bob"),
                ("friends[1].name", "Carol"),
            ],
        ),
        ("an empty document", {}, []),
        ("an empty list inside a key", {"tags": []}, []),
        (
            "lists inside lists",
            {"grid": [[1, 2], [3]]},
            [("grid[0][0]", 1), ("grid[0][1]", 2), ("grid[1][0]", 3)],
        ),
        (
            "the JSON types that are not containers",
            {"a": None, "b": True, "c": 1.5, "d": ""},
            [("a", None), ("b", True), ("c", 1.5), ("d", "")],
        ),
        ("a bare value with no container at all", 42, [("", 42)]),
    )
    for label, document, expected in cases:
        actual = list(walk(document))
        assert actual == expected, f"{label}: expected {expected}, got {actual}"
        print(f"ok  {label}: {len(actual)} value(s)")
    return len(cases)


if __name__ == "__main__":
    print("walk of the sample document:")
    for dotted, value in walk(SAMPLE):
        print(f"  {dotted:<18} {json.dumps(value)}")
    print()
    total = check()
    print()
    print(f"{total} checks passed.")
