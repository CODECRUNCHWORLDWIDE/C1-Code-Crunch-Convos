"""problem-03-stack-built-on-a-list-solution.py — a Stack over a list, and a bracket checker.

The `-solution` in the name keeps this file from colliding with the `stack.py`
you write yourself. Run it with::

    python problem-03-stack-built-on-a-list-solution.py
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

PAIRS: dict[str, str] = {")": "(", "]": "[", "}": "{"}
OPENERS: frozenset[str] = frozenset(PAIRS.values())


class Stack:
    """Last in, first out. The top of the stack is the end of the list.

    Wrapping a list rather than subclassing it is deliberate: a stack is not a
    list, it *has* one. Subclassing `list` would hand callers `insert`,
    `sort`, and indexing — every one of which breaks the LIFO promise.
    """

    def __init__(self, items: list[Any] | None = None) -> None:
        """Start empty, or from a copy of `items` with the last item on top."""
        self._items: list[Any] = list(items) if items else []

    def push(self, item: Any) -> None:
        """Put `item` on top."""
        self._items.append(item)

    def pop(self) -> Any:
        """Take the top item off and return it."""
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Return the top item without removing it."""
        if not self._items:
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    @property
    def is_empty(self) -> bool:
        """True when there is nothing on the stack."""
        return not self._items

    def __len__(self) -> int:
        """How many items are on the stack."""
        return len(self._items)

    def __iter__(self) -> Iterator[Any]:
        """Top to bottom — the order you would pop them off."""
        return iter(self._items[::-1])

    def __repr__(self) -> str:
        """Developer form, bottom-to-top, with the top marked."""
        # Bottom-to-top, with the top marked, so a debug print is unambiguous.
        return f"Stack({self._items!r})  # top -> {self._items[-1]!r}" if self._items else "Stack([])"


def is_balanced(s: str) -> bool:
    """True iff every (), [] and {} in `s` is closed in the right order.

    Characters that are not brackets are ignored, so this works on real source
    text, not just bracket soup.
    """
    stack = Stack()
    for char in s:
        if char in OPENERS:
            stack.push(char)
        elif char in PAIRS:
            if stack.is_empty:                 # a closer with nothing open
                return False
            if stack.pop() != PAIRS[char]:     # closed the wrong kind
                return False
    return stack.is_empty                      # anything left open fails


def main() -> None:
    """Drive the stack, then run the balance checker over eleven strings."""
    stack = Stack()
    print("empty:", repr(stack), "| is_empty:", stack.is_empty)

    for item in ["a", "b", "c"]:
        stack.push(item)
    print("after pushes:", repr(stack), "| len:", len(stack))
    print("peek:", stack.peek(), "| top-to-bottom:", list(stack))
    print("pop:", stack.pop(), "| now:", repr(stack))

    empty = Stack()
    for name, call in [("pop", empty.pop), ("peek", empty.peek)]:
        try:
            call()
        except IndexError as exc:
            print(f"IndexError ({name}):", exc)

    cases = [
        "(a+b)[i]",
        "(a+b]",
        "",
        "()",
        "([{}])",
        "([)]",
        "(()",
        "())(",
        ")(",
        "def f(x): return {'a': [1, 2]}",
        "no brackets at all",
    ]
    width = max(len(repr(c)) for c in cases)
    for case in cases:
        print(f"{repr(case):<{width}}  ->  {is_balanced(case)}")


if __name__ == "__main__":
    main()
