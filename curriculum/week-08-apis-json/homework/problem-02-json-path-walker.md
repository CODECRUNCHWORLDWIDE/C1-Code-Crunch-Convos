# Homework Problem 2 — JSON Path Walker

> **Topic:** walking a nested JSON document with a recursive generator, and naming every value's address
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** real API responses are big and deep, and the question you actually have on a Tuesday afternoon is "where inside this thing is the value I need?" This problem builds the tool that answers it — and on the way, it teaches the recursive shape that fits every nested structure you will ever meet.

## The Brief

A JSON document is a box of boxes. A dict can hold dicts, which hold lists,
which hold more dicts, as deep as anybody cared to nest them. When an API
hands you three hundred lines of that, you do not want to read it — you want
an **inventory**: every plain value in the document, each one labelled with
the exact directions for reaching it.

The directions are called a **dotted path**, and you already write them every
day without naming them. `data["address"]["city"]` in code is `address.city`
as a path. `data["friends"][0]["name"]` is `friends[0].name`. Dict keys join
with dots; list positions ride in square brackets.

You are writing `walk`, a **generator** that takes a decoded JSON document
and yields one `(path, value)` pair for every primitive value in it — where a
primitive is anything that is not a dict or a list: strings, numbers, `True`,
`False`, `None`.

```python
data = {
    "name": "Ada",
    "age": 207,
    "address": {"city": "London", "zip": "E1 6AN"},
    "friends": [{"name": "Bob"}, {"name": "Carol"}],
}

list(walk(data)) == [
    ("name", "Ada"),
    ("age", 207),
    ("address.city", "London"),
    ("address.zip", "E1 6AN"),
    ("friends[0].name", "Bob"),
    ("friends[1].name", "Carol"),
]
```

Containers are walked into, never reported themselves. Empty containers
contribute nothing — there is no value inside them to report.

There is no network in this problem. There does not need to be: `walk` does
not care whether its input came from `response.json()`, a file, or a literal
in a test, which is exactly what will make it easy to check.

## Starter

Save this as `hw02_json_walker.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it reports the whole document as one value at
path `""` until you teach it to recurse:

```python
"""Yield (dotted path, value) for every primitive value in a JSON document."""

from __future__ import annotations

from typing import Any, Iterator

SAMPLE: dict[str, Any] = {
    "name": "Ada",
    "age": 207,
    "address": {"city": "London", "zip": "E1 6AN"},
    "friends": [{"name": "Bob"}, {"name": "Carol"}],
}


def walk(node: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    """Yield (dotted path, value) for every primitive value inside *node*.

    Args:
        node: A decoded JSON document, or any part of one.
        path: The path that led here. Callers leave this empty.

    Yields:
        One pair per primitive value, in document order.
    """
    # TODO: if node is a dict, recurse into each value. The child path is
    #       f"{path}.{key}" -- unless path is empty, in which case it is
    #       just the key.
    # TODO: if node is a list, recurse into each element with f"{path}[{i}]".
    # TODO: otherwise node is a primitive: yield the pair.
    yield path, node


if __name__ == "__main__":
    for dotted, value in walk(SAMPLE):
        print(dotted, "=", repr(value))

    assert list(walk({})) == []
    assert list(walk(SAMPLE))[0] == ("name", "Ada")
    assert ("friends[1].name", "Carol") in list(walk(SAMPLE))
    print("all checks passed")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-08-apis-json/homework/problem-02-json-path-walker.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `walk(node, path="")` is a generator with the signature above, type hints
   included.
2. Dict keys join with dots: `address.city`. Top-level keys have no leading
   dot: `name`, never `.name`.
3. List indices ride in brackets, glued straight on: `friends[0].name`, and
   nested lists stack them: `grid[0][1]`.
4. Pairs come out in **document order** — the order the keys and elements
   appear in the input.
5. Empty dicts and empty lists yield nothing.
6. At least four test cases run under `if __name__ == "__main__":`, including
   one empty dict and one with a list inside a list.

## Constraints

- **A generator, not a function that builds a list.** `walk` on a
  thirty-thousand-value document should hand you the first pair immediately
  and never hold more than one pair at a time. The caller decides whether to
  collect them (`list(walk(data))`), filter them, or stop early — and
  stopping early costs nothing, because a generator only computes what is
  asked of it.

- **Recursion, because the data is recursive.** A dict-of-lists-of-dicts is
  defined in terms of itself, so the function that walks it is too. You could
  manage an explicit stack in a loop — Under the hood shows it — but the
  recursive version is eight lines and reads like the definition of the data.

- **Exactly two container types: `dict` and `list`.** That is all
  `json.loads` can produce for containers, so checking for anything else —
  tuples, sets, custom classes — is code for inputs that cannot arrive. Keep
  the door as narrow as the data.

- **Yield leaves only.** The pair `("address", {...})` would double-report
  everything inside it. A container is a place values live, not a value.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-json-path-walker-solution.py
walk of the sample document:
  name               "Ada"
  age                207
  address.city       "London"
  address.zip        "E1 6AN"
  friends[0].name    "Bob"
  friends[1].name    "Carol"

ok  the sample document: 6 value(s)
ok  an empty document: 0 value(s)
ok  an empty list inside a key: 0 value(s)
ok  lists inside lists: 3 value(s)
ok  the JSON types that are not containers: 4 value(s)
ok  a bare value with no container at all: 1 value(s)

6 checks passed.
```

Your own `hw02_json_walker.py` prints whatever your harness prints. What must
agree is the pairs: six of them for the sample, in that order, with those
paths.

## Steps

1. Copy the starter into `hw02_json_walker.py` and run it. It prints one line
   — the whole document at path `""` — which is wrong in an instructive way:
   the primitive branch already works, and everything missing is the two
   recursive branches above it.
2. Write the dict branch. Recurse with `yield from`, building the child path
   with a dot — except at the top, where the path so far is empty and the
   child path is just the key. Run it: the sample now walks, but lists still
   come out whole.
3. Write the list branch with `enumerate`. Run it again and compare your six
   pairs against the brief's, character for character.
4. Feed it `{}`, then `{"tags": []}`, then `{"grid": [[1, 2], [3]]}`. The
   first two yield nothing; the third is where `grid[0][1]` either looks
   right or teaches you something.
5. Feed it a bare value — `walk(42)` — and decide what your function does.
   The shipped answer yields `("", 42)`: the value exists and its address is
   "the whole document".
6. Turn each of those experiments into an `assert` before moving on.

## The Solution

```python
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
```

**The function is a fork with three tines, and the data picks the tine.** A
dict? Walk into every value. A list? Walk into every element. Anything else
is a leaf: report it. That is the entire algorithm, and it works at any depth
because each recursive call faces exactly the same three-way question one
level further down.

**`yield from` is the line that makes recursion and generators compose.** A
recursive call like `walk(value, child)` does not *run* the walk — it builds
a generator object and hands it back. `yield from` says "everything that
generator produces, pass through as mine". Without it you would yield the
generator objects themselves, and the caller would receive machinery instead
of pairs. It is the single most common bug in this problem, and it is first
in the list below.

**The path logic is one conditional, placed carefully.**
`f"{path}.{key}" if path else str(key)` — the dot is a *joiner*, so it only
appears between two things. At the top level there is nothing on the left,
so no dot. Indices are different on purpose: `[0]` glues straight onto
whatever came before, because that is how you would type it back into
Python, which is exactly what makes these paths useful — every path in the
output can be replayed as real subscripts to reach the value again.

**Document order comes for free, and it is a real promise.** Dicts preserve
insertion order in Python, `json.loads` inserts keys in the order they appear
in the text, and `enumerate` walks lists front to back. So the pairs come out
in the order a human reading the JSON would meet them — which makes the
output diffable, and makes your tests able to assert on exact lists instead
of sets.

**The bare-value case costs nothing and defines an edge.** `walk(42)` never
enters either branch and yields `("", 42)`. You will likely never feed it a
bare value on purpose — but a function whose edges are defined is a function
you can test without arguing about what "should" happen.

**`json.dumps(value)` in the demo print is a small honesty trick.** It prints
values in JSON's own spelling — `"Ada"` with quotes, `true`, `null` — so
strings are visibly strings. `print("Ada")` and `print(207)` look
confusingly alike; `"Ada"` and `207` do not.

## Download and run

Download
[problem-02-json-path-walker-solution.py](./problem-02-json-path-walker-solution.py)
and run it:

```bash
python problem-02-json-path-walker-solution.py
```

It needs nothing installed and never touches the network. The `-solution` in
the filename keeps it from colliding with your own `hw02_json_walker.py`.

## Common bugs to catch

- **`walk(value, child)` without `yield from`.** The recursive call builds a
  generator and throws it away — or worse, you `yield` it and the caller
  receives generator objects as "values":

  ```text
  ('address', <generator object walk at 0x000001E14F0D2F80>)
  ```

  Anywhere a recursive generator calls itself, the call rides behind
  `yield from`.

- **`return` instead of `yield` in one branch.** A function containing even
  one `yield` anywhere is a generator, and `return` inside it means "stop
  iterating", not "here is the answer". Symptom: the walk quietly ends after
  the first leaf.

- **A leading dot on top-level keys.** `path + "." + key` without the
  emptiness check produces `.name`, `.address.city`. Every path is wrong by
  one character, and if your tests only check `in` rather than equality, they
  all still pass. Assert on exact pairs.

- **`friends.0.name` instead of `friends[0].name`.** Treating list indices
  like dict keys loses the information about which container each step goes
  into — you can no longer replay the path as subscripts without guessing.
  The brief's format keeps dicts and lists visibly different.

- **Checking `isinstance(node, (int, float, str, bool))` to find leaves.**
  Listing the primitive types instead of the container types breaks on
  `None` — which is in every real API response, is none of those types, and
  silently vanishes from your inventory. There are exactly two container
  types; test for those and let *everything* else be a leaf.

- **`RecursionError: maximum recursion depth exceeded`.** Two ways to earn
  it: a document nested a thousand levels deep (real, but rare — Under the
  hood has the fix), or a structure that contains itself:

  ```python
  d = {}
  d["self"] = d          # a dict that holds itself
  list(walk(d))          # RecursionError
  ```

  Decoded JSON can never contain a cycle — text cannot point backwards into
  itself — so this only bites when someone feeds `walk` a hand-built Python
  structure. Worth knowing which inputs your tool's promise covers.

## Under the hood

<details>
<summary>Under the hood — the same walk without recursion, and when you would want it</summary>

Python caps recursion depth — `sys.getrecursionlimit()` is 1000 by default —
because each nested call takes a frame of real memory on the C stack. A JSON
document a thousand levels deep therefore kills the recursive walker. Such
documents are rare and usually machine-generated, but "rare" is not "never",
and the fix is worth seeing once, because it is the standard trade: **your
own stack instead of the call stack.**

```python
def walk_iterative(node: Any) -> Iterator[tuple[str, Any]]:
    """The same inventory, no recursion, any depth."""
    stack: list[tuple[str, Any]] = [("", node)]
    while stack:
        path, current = stack.pop()
        if isinstance(current, dict):
            for key, value in reversed(current.items()):
                stack.append((f"{path}.{key}" if path else str(key), value))
        elif isinstance(current, list):
            for index in range(len(current) - 1, -1, -1):
                stack.append((f"{path}[{index}]", current[index]))
        else:
            yield path, current
```

Same three-way fork, but pending work waits in a list you own, which grows on
the heap and has no thousand-frame ceiling. The two `reversed` walks exist
only to keep document order: a stack pops last-in-first-out, so children are
pushed backwards to come off forwards.

Read them side by side and the recursive version wins on clarity by a mile —
the iterative one spends half its lines managing bookkeeping the call stack
would have done silently. That is the honest shape of this trade everywhere
it appears: recursion pays in depth ceiling, iteration pays in bookkeeping.
Default to the readable one; switch when the data proves it can exceed the
ceiling.

`sys.setrecursionlimit(100_000)` also exists and is almost always the wrong
tool: the limit protects you from crashing the interpreter itself, and
raising it trades a clean `RecursionError` for a possible hard crash.

</details>

<details>
<summary>Under the hood — JSONPath, jq, and where dotted paths come from</summary>

The path format this problem uses is not something the course invented. It is
the common core of a small family of real query languages:

- **JSONPath** writes `$.friends[0].name` — a `$` for the root, then exactly
  the dots and brackets you generated. Libraries like `jsonpath-ng` evaluate
  these against documents.
- **jq**, the command-line JSON tool, writes `.friends[0].name` and is the
  fastest way to explore an API response you saved with
  `python -m json.tool` or `curl`.
- **JMESPath** (used by the AWS CLI) writes `friends[0].name` — precisely
  your output.

So the tool you built is one half of those systems: they *parse* paths and
fetch one value; you *generate* paths for every value. The inverse function —
take `"friends[0].name"`, split it back into steps, follow them with
subscripts — is the natural companion, and it is this page's first stretch
goal.

One design detail the real languages had to solve that your generator dodged:
a dict key can *contain* a dot (`{"a.b": 1}`), and then `a.b` is ambiguous —
one key or two? JSONPath answers with bracket-and-quote syntax, `$['a.b']`.
Your walker inherits the ambiguity silently, which is fine for an inventory
tool a human reads, and not fine for a parser. Edges like this are why "just
split on dots" parsers eventually meet a document that breaks them.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] `list(walk(SAMPLE))` equals the brief's six pairs exactly, in order.
- [ ] Top-level paths have no leading dot.
- [ ] `grid[0][1]` — brackets stack, no dot between them.
- [ ] `walk({})` and `walk({"tags": []})` both yield nothing.
- [ ] `None`, `True`, `1.5` and `""` all appear as values in some test.
- [ ] `walk` is a generator: `walk(SAMPLE)` prints as a generator object, not
      a list.
- [ ] Four or more asserts, including the empty dict and nested lists.
- [ ] Committed with a message like `Add Week 8 homework 2: JSON path walker`.

## Stretch

- Write the inverse: `fetch(data, "friends[0].name")` returns `"Bob"`. Parse
  the path into steps, then follow them with subscripts. Round-trip every
  pair your walker yields: `fetch(data, path) == value` for all of them —
  that property test is one loop and catches a remarkable number of bugs.

- Add `find(data, key)` that yields the full path of every value whose final
  key matches — `find(response, "name")` on the sample yields three paths.
  This is the tool's real Tuesday-afternoon use.

- Point it at something real: `python -m json.tool` a saved response from
  [Exercise 2's PokeAPI call](../exercises/exercise-02-pokemon-api.md), load
  it with `json.load`, and walk it. Three hundred lines of nested JSON become
  a flat, searchable inventory — which is the moment this problem pays for
  itself.

Once your walker inventories cleanly, move on to
[Homework Problem 3 — Rate-Limit Decorator](./problem-03-rate-limit-decorator.md).
