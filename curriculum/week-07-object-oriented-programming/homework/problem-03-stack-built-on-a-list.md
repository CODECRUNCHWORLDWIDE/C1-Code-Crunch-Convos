# Problem 3 — `Stack` built on a list

> **Topic:** wrapping instead of subclassing, and the one data structure that makes bracket matching easy
> **Lecture:** [02 — Inheritance and Composition](../lecture-notes/02-inheritance-and-composition.md)
> **Difficulty:** Intermediate
> **Target time:** 50 minutes
> **Why this one:** it is the textbook case for "composition over inheritance", and the reason is concrete rather than philosophical. `class Stack(list)` is shorter and it hands every caller a `sort()` and an `insert(0, x)` that break the whole point of a stack. Then the second half shows you what a stack is actually *for*, which is the part people remember.

## The Brief

A **stack** is a pile. You put things on the top and you take them off the
top, and you can never reach into the middle. Last in, first out — LIFO.

You are building one, wrapping a Python list, and exposing exactly six
things:

- `push(item)` — put something on top.
- `pop()` — take the top item off and return it. Raises `IndexError` when
  empty.
- `peek()` — look at the top item without removing it. Raises `IndexError`
  when empty.
- `is_empty` — a property, not a method.
- `__len__`, `__iter__` (top to bottom), `__repr__`.

**Wrap, do not inherit.** `class Stack(list)` would be less code and would be
wrong. A stack is not a list; it *has* one. Subclass `list` and your callers
get `insert`, `sort`, `remove`, indexing and slicing thrown in — every one of
which lets somebody violate LIFO while still holding an object the type
system calls a `Stack`. You cannot inherit and then take capabilities away.
Wrapping means the public surface is exactly the six operations you chose.

Then the second half, which is why anyone cares. Write

```python
def is_balanced(s: str) -> bool: ...
```

which returns `True` when every `(`, `[` and `{` in `s` is closed by the
right partner in the right order. `"(a+b)[i]"` is balanced. `"(a+b]"` is not.

A stack is the right structure because nesting is last-in-first-out **by
definition**: the bracket you must close next is always the most recently
opened one still open. That sentence *is* a stack. Recognising it is the
actual skill this problem is teaching.

## Starter

Save this as `stack.py` and fill in the `TODO` markers.

```python
"""stack.py — a Stack over a list, and a bracket-balance checker built on it.

    python stack.py
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

PAIRS: dict[str, str] = {")": "(", "]": "[", "}": "{"}
OPENERS: frozenset[str] = frozenset(PAIRS.values())


class Stack:
    """Last in, first out. The top of the stack is the end of the list."""

    def __init__(self, items: list[Any] | None = None) -> None:
        """Start empty, or from a copy of `items` with the last item on top."""
        # TODO: store a COPY of items in self._items, or an empty list

    def push(self, item: Any) -> None:
        """Put `item` on top."""
        # TODO

    def pop(self) -> Any:
        """Take the top item off and return it."""
        # TODO: raise IndexError("pop from an empty stack") when empty

    def peek(self) -> Any:
        """Return the top item without removing it."""
        # TODO: raise IndexError("peek at an empty stack") when empty

    @property
    def is_empty(self) -> bool:
        """True when there is nothing on the stack."""
        # TODO
        raise NotImplementedError

    def __len__(self) -> int:
        """How many items are on the stack."""
        # TODO
        raise NotImplementedError

    def __iter__(self) -> Iterator[Any]:
        """Top to bottom — the order you would pop them off."""
        # TODO: a reversed COPY, so pushing or popping mid-loop is safe
        raise NotImplementedError

    def __repr__(self) -> str:
        """Developer form, bottom-to-top, with the top marked."""
        # TODO: "Stack([])" when empty, otherwise
        # "Stack(['a', 'b'])  # top -> 'b'"
        raise NotImplementedError


def is_balanced(s: str) -> bool:
    """True iff every (), [] and {} in `s` is closed in the right order.

    Characters that are not brackets are ignored, so this works on real source
    text, not just bracket soup.
    """
    # TODO: push every opener.
    # TODO: on a closer, refuse if the stack is empty, and refuse if the
    #       thing you pop is not the matching opener.
    # TODO: at the end, the stack must be empty.
    raise NotImplementedError


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
```

Two given lines are doing more work than they look.

**`PAIRS` maps closer to opener**, not the other way round. That direction is
deliberate: when you meet a `)`, one dict lookup tells you what you needed to
have open. The reverse mapping would need a search.

**`OPENERS` is a `frozenset`** of the values. `char in OPENERS` is a
constant-time check no matter how many bracket kinds you add, and a frozenset
cannot be modified by accident.

## Requirements

1. `Stack` wraps a list. It does **not** inherit from `list` or from anything
   else.
2. `push`, `pop`, `peek`, `is_empty`, `__len__`, `__iter__`, `__repr__`, and
   nothing else public.
3. `pop` and `peek` on an empty stack raise `IndexError` with a message that
   says "stack".
4. `is_empty` is a property.
5. `__iter__` yields top to bottom, from a snapshot.
6. `is_balanced("")` is `True`. An empty string is balanced, vacuously.
7. `is_balanced` ignores every character that is not one of the six brackets,
   so it works on real source text.
8. Do not edit `main()`.

## Constraints

- **Wrap, never subclass `list`.** `class Stack(list)` runs, passes the demo,
  and then somebody writes `stack.sort()` or `stack[0]` and the LIFO promise
  is gone with no error anywhere. If you want the shorter version honestly,
  `collections.deque` with `append`/`pop` is the standard-library answer —
  still wrapped, not subclassed.
- **Copy the list you are handed.** `list(items)` means the caller's list and
  the stack's list are different objects, so a later append on the caller's
  side cannot reach into your stack.
- **The top of the stack is the end of the list.** `list.pop()` with no index
  removes the last element and moves nothing; `list.pop(0)` shifts everything
  down. Nobody will notice at three items. The habit is the thing.
- **`is_empty` is a property, not a method.** `if stack.is_empty:` reads as a
  fact about the object rather than an action — and there is a real trap in
  the alternative. A bound method object is always truthy, so
  `if stack.is_empty():` written without the parentheses makes the branch
  *always* taken, silently.
- **`__iter__` returns a reversed snapshot.** `self._items[::-1]` makes a
  copy. `reversed(self._items)` would be a live view and would go strange
  under mutation.
- **`is_balanced` returns a bool; it never raises.** A malformed input string
  is not an exceptional condition here. It is the entire question being
  asked.
- **Check emptiness before you pop.** `if stack.pop() != PAIRS[char]` with no
  emptiness check turns `")"` into an uncaught `IndexError` instead of
  `False`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-03-stack-built-on-a-list.py
empty: Stack([]) | is_empty: True
after pushes: Stack(['a', 'b', 'c'])  # top -> 'c' | len: 3
peek: c | top-to-bottom: ['c', 'b', 'a']
pop: c | now: Stack(['a', 'b'])  # top -> 'b'
IndexError (pop): pop from an empty stack
IndexError (peek): peek at an empty stack
'(a+b)[i]'                        ->  True
'(a+b]'                           ->  False
''                                ->  True
'()'                              ->  True
'([{}])'                          ->  True
'([)]'                            ->  False
'(()'                             ->  False
'())('                            ->  False
')('                              ->  False
"def f(x): return {'a': [1, 2]}"  ->  True
'no brackets at all'              ->  True
```

The first two cases are the ones the brief names. The rest are there to catch
the three classic bugs, and it is worth knowing which is which:

- `'([)]'` catches **counting instead of stacking**. The counts balance; the
  nesting does not.
- `'(()'` catches the **missing final check**. Two openers, one closer, and
  the function must notice something is still open when the string ends.
- `')('` catches **popping from empty**. The first character is a closer with
  nothing open.

An empty string is balanced — vacuously, and that is the right answer.

Note the last case in the list prints with double quotes:
`"def f(x): return {'a': [1, 2]}"`. That is `repr` choosing the quote
character that avoids escaping, because the string contains single quotes.
Nothing to fix.

## Steps

1. Write `Stack` first and get the first four output lines right. Do not
   touch `is_balanced` yet.
2. Check the empty-stack errors before going further. Those two guards are
   what stop `is_balanced` from crashing on `")("`.
3. Now write out the three ways `is_balanced` can fail, in words, before you
   write any code:
   1. a closer arrives with nothing open;
   2. a closer arrives that does not match the most recent opener;
   3. the string ends with something still open.
   The function has exactly three exits, one per failure, and writing them
   down first is how you avoid missing the third.
4. Implement the loop. Push on an opener, check-and-pop on a closer, ignore
   everything else.
5. End the function with `return stack.is_empty`, **not** `return True`.
   That is failure 3.
6. Run the eleven cases and check each `True`/`False` against your own
   reasoning. If `'(()'` says `True`, go back to step 5.
7. Try it on a real file:
   `print(is_balanced(open("stack.py", encoding="utf-8").read()))`. It should
   say `True`, because Python source with balanced brackets is exactly what
   this checks. Then delete a closing bracket and watch it flip.

## The Solution

```python
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
```

**`is_balanced` has exactly three ways to fail, and the code has exactly three
exits.** Enumerate them before writing anything and the function writes
itself. The third one — the string ends with something still open — is the
one people forget, and it is why the function ends with
`return stack.is_empty` rather than `return True`.

**A stack is the right structure because nesting is last-in-first-out by
definition.** `PAIRS` maps closer to opener, so a match check is a single
dict lookup rather than a chain of `if`s.

**Composition, not inheritance — and this is the textbook case.**
`class Stack(list)` would be less code and would be wrong in the specific way
Lecture 02 warns about. You would inherit `insert(0, x)`, `sort()`,
`remove()`, `__getitem__`, slicing — every one of which lets a caller violate
LIFO while still holding something the type system calls a `Stack`. You
cannot inherit and then take capabilities away.

**`pop` and `peek` raise `IndexError`, matching both the brief and the
language.** `list.pop()` on an empty list raises
`IndexError: pop from empty list`; a stack behaving the same way is the least
surprising choice. The messages here are custom so the traceback says
"stack", not "list" — a small thing that saves a moment of confusion when the
failure is three frames deep.

**`is_empty` is a property**, because it reads as a fact rather than an
action, and because forgetting the parentheses on a method version is a
silent always-true bug.

**`__iter__` returns a reversed snapshot.** `self._items[::-1]` makes a copy,
so a `for` loop over the stack is safe even if the body pushes or pops.

**Non-bracket characters are ignored, not rejected.** That is what makes
`"def f(x): return {'a': [1, 2]}"` work, and it is why the checker is useful
on real source text. The `elif char in PAIRS` branch only fires for the three
closers; everything else falls through untouched.

## Run it

Copy the worked answer on this page into `problem-03-stack-built-on-a-list.py` and run it:

```bash
python problem-03-stack-built-on-a-list.py
```

It imports only from the standard library and needs no setup. Save your own
version as `stack.py`.

## Common bugs to catch

- **`'([)]'` reports `True`.** You counted instead of stacking — one counter
  per bracket type, increment on open, decrement on close, all zero at the
  end. The counts balance and the nesting does not. Any counting solution
  fails on ordering; only a stack tracks it.

- **`'(()'` reports `True`.** You ended with `return True` instead of
  `return stack.is_empty`. This is the most common bug in the problem, and it
  passes any test suite that only tries strings with equal numbers of openers
  and closers — so make sure yours does not.

- **`IndexError: pop from an empty stack` escapes from `is_balanced`.** You
  popped before checking emptiness, so `")("` crashed instead of returning
  `False`. The guard goes first.

- **`class Stack(list):`.** It runs. It passes the demo. Then somebody writes
  `stack.sort()` and the invariant is gone with no error anywhere.

- **`AttributeError: 'Stack' object has no attribute '_items'`.** Your
  `__init__` body is only comments, so it sets nothing.

- **`TypeError: 'bool' object is not callable`,** or a branch that is always
  taken. You made `is_empty` a method and then wrote `if stack.is_empty:`
  without parentheses somewhere, or a property and called it with them. Pick
  one and be consistent — the brief says property.

- **`IndexError: list index out of range` from `__repr__`.** Your repr reads
  `self._items[-1]` unconditionally. An empty stack has no last item; the
  conditional expression is what handles it.

- **The `top-to-bottom` line prints `['a', 'b', 'c']`.** Your `__iter__`
  returns `iter(self._items)` without reversing. The top of the stack is the
  end of the list, so iteration has to walk backwards.

## Under the hood

<details>
<summary>Under the hood — why wrapping costs one line and buys you the whole public surface</summary>

The argument for wrapping is usually made abstractly. Here it is
concretely — build both and count what a caller can do.

```text
>>> class BadStack(list):
...     def push(self, item): self.append(item)
...     @property
...     def is_empty(self): return not self
...
>>> s = BadStack()
>>> s.push("a"); s.push("b"); s.push("c")
>>> s.insert(0, "smuggled")
>>> s.sort()
>>> s[1] = "rewritten"
>>> list(s)
['a', 'rewritten', 'c', 'smuggled']
```

Not one of those four lines raised. The object is still a `BadStack`, still
passes `isinstance(s, BadStack)`, and its contents have been reordered,
injected into and overwritten in the middle. Every one of those operations
came from `list`, and you never chose to offer any of them.

Count the surface:

```text
>>> len([n for n in dir(BadStack) if not n.startswith("_")])
13
>>> len([n for n in dir(Stack) if not n.startswith("_")])
4
```

Thirteen public names against four. Nine of those thirteen you did not write,
did not document, and cannot remove — because **inheritance only ever adds**. There is no syntax for "and not `sort`". You can override `sort` to
raise, but then you have a `list` that is not substitutable for a `list`,
which is the Liskov failure from Challenge 02 pointed the other way.

The wrapped version's whole surface is `push`, `pop`, `peek`, `is_empty`, and
whatever dunder methods you chose to add. That is the design decision, made
once, in the class body, visible to anyone reading it.

The cost of wrapping is **delegation**: every operation you *do* want has to
be written out. `__len__` is `return len(self._items)`, `__iter__` is one
line, and so on. Four lines here. For a class wrapping something with fifty
useful methods, that cost is real, and it is the reason people reach for
inheritance when they should not.

Three ways to pay less, in increasing order of cleverness:

1. **Only delegate what you need.** Usually the right answer. You are not
   building a general list replacement; you are building a stack.
2. **Inherit from the right thing.** `collections.UserList` exists precisely
   so you can subclass list-like behaviour without subclassing the built-in,
   and `collections.abc.MutableSequence` gives you most methods free once you
   supply five. Both are still "I want to be a sequence", which a stack is
   not.
3. **`__getattr__` forwarding.** Define `__getattr__` to pass unknown names
   through to `self._items` and you delegate everything in three lines — and
   you have re-created the problem, because now `stack.sort()` works again.
   Cleverness that undoes the design decision is not a saving.

One last thing worth seeing: what the standard library did with the same
question. `collections.deque` is the "real" answer for stacks and queues, and
it does **not** inherit from `list`. It is its own type with its own surface,
and it offers `append`/`pop` at both ends in constant time. If you rewrote
`Stack` over a `deque` tomorrow, not one line of `is_balanced` would change —
which is the actual payoff of having kept the surface to four names.

</details>

## Acceptance checklist

- [ ] `python stack.py` runs with no traceback.
- [ ] All seventeen output lines match exactly.
- [ ] `Stack` does not inherit from `list` or anything else.
- [ ] `pop` and `peek` on an empty stack raise `IndexError` with a message
      naming the stack.
- [ ] `is_empty` is a property.
- [ ] `list(stack)` yields top to bottom.
- [ ] `is_balanced("")` is `True` and `is_balanced("(()")` is `False`.
- [ ] `is_balanced` never raises, whatever string you feed it.
- [ ] Every signature is type-hinted.
- [ ] Committed to Git with a message like
      `Add Week 7 homework 3: stack and bracket checker`.

## Stretch

- Make `is_balanced` report *where* it failed. Push `(char, index)` pairs
  instead of bare characters, and return a small result object or a
  `tuple[bool, int | None]` naming the offending position. Note what that
  costs you at every call site, and decide whether it was worth it.
- Rebuild `Stack` over `collections.deque` and confirm `is_balanced` needs
  zero changes. That is the payoff of a four-name surface.
- Add `__contains__` and `__bool__`. Then work out what `bool(stack)` already
  did before you added it, and write one sentence saying whether your
  `__bool__` changed any behaviour at all.
- Use your `Stack` to write `evaluate_rpn(tokens: str) -> float`, evaluating
  reverse Polish notation — `"3 4 + 2 *"` is `14.0`. It is the same structure
  doing a different job, which is the best evidence that you picked the right
  one.

Next: [Problem 4 — Simple ORM-like model](./problem-04-simple-orm-like-model.md).
