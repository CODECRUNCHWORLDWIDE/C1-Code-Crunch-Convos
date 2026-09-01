# Challenge 2 — Inventory Tracker

> **Topic:** a dict inside a dict, six small functions over it, and the order in which a function is allowed to change things
> **Lecture:** [02 — Sets and Dicts](../lecture-notes/02-sets-and-dicts.md) and [03 — Comprehensions and Big-O](../lecture-notes/03-comprehensions-and-big-o.md)
> **Difficulty:** no single function is hard; keeping six of them honest about the same data is
> **Target time:** 90–120 minutes
> **Why this one:** this is your first program where several functions share one piece of live data, and that is where a new category of bug starts. Not "this line is wrong" but "this line was right and something else changed the world underneath it". The habit this challenge builds — check everything that can fail *before* you change anything — is the one that separates code you can retry from code you cannot.

## The Brief

You are writing the back end for a very small warehouse. The stock is
organised by **category**, and each category holds **items** with **counts**.
You model that as a dict inside a dict:

```python
inventory: dict[str, dict[str, int]] = {
    "fruit": {"apple": 5, "banana": 3, "cherry": 12},
    "tools": {"hammer": 1, "saw": 2},
    "books": {},
}
```

Read that shape out loud: the outer dict is labelled with category names, and
what is inside each of those boxes is *another* dict, labelled with item names,
holding numbers. So `inventory["fruit"]["cherry"]` is two hops — open the
`fruit` box, then open the `cherry` box inside it.

Build six small functions that work on that structure. Every one of them takes
the inventory as an **argument**. None of them reaches for a global. That is
not a style preference: the same six functions then work on a test fixture, on
something loaded from a file, and on a real request, without a single change.

Two rules in the brief are more interesting than they look.

**Empty things must disappear.** When the last of an item is removed, the item
key goes. When that leaves the category empty, the category key goes too. A
warehouse with a shelf labelled `tools` and nothing on it is a lie about the
warehouse.

**Removing from somewhere that does not exist must raise `KeyError`.** Not
"quietly do nothing". Asking to remove stock from a category that was never
stocked is a caller bug, and a function that silently shrugs hides caller
bugs. Notice this is the *opposite* choice from `category_total`, which is
asked to return `0` for a missing category rather than raise. Same data, two
different questions, two different right answers. Working out which is which
is most of the design work in this challenge.

## Starter

Create `challenge-02-inventory-tracker.py` in your `challenges/` folder and
paste this in. The checks are given; the six functions are yours.

```python
"""challenge-02-inventory-tracker.py — a tiny warehouse backend.

TODO: replace this docstring with a short paragraph saying why you kept the
nested dict rather than flattening it, and what that choice costs. That
reflection is part of the grade.
"""

Inventory = dict[str, dict[str, int]]


def add_item(inv: Inventory, category: str, item: str, count: int = 1) -> None:
    """Add `count` of `item` to `category`, creating either if needed."""
    # TODO: inv.setdefault(category, {}) ensures the shelf exists and hands
    # it to you. Then .get(item, 0) + count for the running total.
    ...


def remove_item(inv: Inventory, category: str, item: str, count: int = 1) -> None:
    """Subtract `count` of `item`; prune the item and the category when empty."""
    # TODO: square brackets, not .get -- an unknown category or item must
    # raise KeyError, and it must raise BEFORE anything is changed.
    # Then: drop the item at zero or below, drop the category if it empties.
    ...


def category_total(inv: Inventory, category: str) -> int:
    """Return the sum of all counts in `category`, or 0 if it does not exist."""
    # TODO: one expression. A missing category is 0, not an error.
    ...


def grand_total(inv: Inventory) -> int:
    """Return the sum of all counts across every category."""
    # TODO: one expression over both levels.
    ...


def find_item(inv: Inventory, item: str) -> list[str]:
    """Return the categories that hold `item`."""
    # TODO: `in` on a dict tests its KEYS.
    ...


def top_n_items(inv: Inventory, n: int = 3) -> list[tuple[str, str, int]]:
    """Return the n highest-count items in the whole inventory.

    Count descending, ties broken by category then item, both A to Z.
    """
    # TODO: flatten to (category, item, count) rows, sort by a tuple key,
    # then slice.
    ...


def run_tests() -> None:
    """Run the brief's own scaffolding and report."""
    inv: Inventory = {}

    add_item(inv, "fruit", "apple", 5)
    add_item(inv, "fruit", "banana", 3)
    add_item(inv, "tools", "hammer", 1)
    add_item(inv, "fruit", "apple", 2)        # accumulates

    assert inv == {
        "fruit": {"apple": 7, "banana": 3},
        "tools": {"hammer": 1},
    }, inv

    assert category_total(inv, "fruit") == 10
    assert category_total(inv, "missing") == 0
    assert grand_total(inv) == 11

    assert find_item(inv, "apple") == ["fruit"]
    assert find_item(inv, "ghost") == []

    remove_item(inv, "fruit", "banana", 3)    # banana -> 0 -> deleted
    assert "banana" not in inv["fruit"]

    remove_item(inv, "tools", "hammer", 1)    # hammer gone -> category empty -> deleted
    assert "tools" not in inv

    try:
        remove_item(inv, "fruit", "phantom", 1)
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError")

    add_item(inv, "fruit", "cherry", 12)
    add_item(inv, "fruit", "date", 2)
    top = top_n_items(inv, 3)
    assert top[0] == ("fruit", "cherry", 12)
    assert len(top) == 3

    print("All checks passed.")


if __name__ == "__main__":
    run_tests()
```

Four words you need before you start.

**`setdefault` versus `.get`.** Both hand you a value with a fallback, and
only one of them **writes**. `inv.setdefault("fruit", {})` puts an empty dict
into `inv` if `fruit` was missing, and hands you the dict that is now
*inside* `inv`. `inv.get("fruit", {})` puts nothing anywhere and hands you a
throwaway. Say the verbs out loud when you write them: `setdefault` means
*ensure*, `get` means *peek*.

**Alias.** When two names refer to the same object, they are **aliases**.
`bucket = inv["fruit"]` does not copy anything — `bucket` and `inv["fruit"]`
are two names for one dict, so `del bucket["apple"]` and
`del inv["fruit"]["apple"]` do the same thing. This challenge relies on that.

**Falsy.** An empty dict, an empty list and an empty string are all **falsy**,
which means `if not bucket:` is `True` when `bucket` is empty. That is the
idiomatic Python way to ask "is this container empty?".

**Atomic.** An operation is atomic when it either happens completely or does
not happen at all. You get that here for free, by putting every check that can
fail *before* the first line that changes anything.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/challenges/challenge-02-inventory-tracker.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `add_item` creates the category if it is missing, creates the item if it is
   missing, and **adds to** the count if the item is already there. Two calls
   of five and two leave seven, not two.
2. `remove_item` raises `KeyError` for an unknown category **or** an unknown
   item, and raises it before changing anything. Otherwise it subtracts,
   deletes the item at zero or below, and deletes the category if that leaves
   it empty.
3. `category_total` returns `0` for a category that does not exist. It does
   not raise, and it does not create the category on the way past.
4. `grand_total` adds up everything, across both levels.
5. `find_item` returns a list of category names, empty when the item is
   nowhere.
6. `top_n_items` returns `(category, item, count)` tuples, count descending,
   ties broken by category then item alphabetically. `n` larger than the
   inventory is not an error.
7. Type hints on all six signatures, a docstring on each, and the module
   docstring replaced with your reflection paragraph.

## Constraints

- **Square brackets where the brief wants a `KeyError`; `.get` where it wants
  a default.** This is the one place in the challenge where the choice between
  two nearly identical spellings is a *requirement* rather than a preference.
  `remove_item` must use `inv[category]`. `category_total` must use
  `inv.get(category, {})`. Getting them the wrong way round makes one function
  silently do nothing and the other one blow up on a perfectly ordinary
  question.

- **Validate first, then change.** In `remove_item`, work out the new count
  *before* you delete or assign anything. Then if the item is unknown, the
  `KeyError` happens while the inventory is still exactly as it was, and the
  caller can fix the call and try again. Do it the other way round — subtract
  first, check afterwards — and a failed call leaves a mess behind that the
  exception does not describe.

- **Prune with `<= 0`, not `== 0`.** Removing 99 apples when you have 2 should
  leave you with no apples, not with -97. `== 0` only catches the exact
  landing.

- **Do not delete keys while looping over the dict they are in.** Python
  raises `RuntimeError: dictionary changed size during iteration`. In a
  well-built `remove_item` this never comes up, because you prune the one
  category you already have in your hand rather than sweeping the whole
  inventory looking for empties.

- **`find_item` tests membership on the inner dict, not on a list of its
  keys.** `item in bucket` asks the dict directly and does not depend on how
  many items are on the shelf. `item in list(bucket)` builds a list first and
  then reads through it, which is slower and longer for the same answer.

- **`top_n_items` sorts by a tuple key, never with `reverse=True`.** The rule
  mixes directions — count downwards, then category and item upwards — and
  `reverse=True` would flip the tie-breakers as well. Negate the count. This
  is Exercise 1's rule, arriving for the third time this week, which is the
  point.

- **No global inventory.** Every function takes `inv` as its first argument.
  A function that reaches for a module-level variable can only ever serve one
  warehouse.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-inventory-tracker.py
All checks passed.
Extra checks passed.
[('fruit', 'cherry', 12), ('fruit', 'apple', 5), ('fruit', 'banana', 3)]
```

The first line is the brief's own scaffolding. The second is a set of edge
cases the scaffolding never reaches, which the solution adds and which you
should add too — over-removing past zero, an unknown category leaving the data
untouched, the tie-break, an `n` bigger than the inventory, and every function
against an empty inventory. The last line is the example from the brief,
reproduced exactly.

## Steps

1. Create the file, paste the starter, and run it. It fails immediately —
   `add_item` is a stub, so `inv` never gets anything in it.
2. Write `add_item` first; nothing else can be tested until stock exists. In a
   REPL, try the broken version deliberately:

   ```text
   >>> inv = {}
   >>> inv["tools"]["hammer"] = 1
   ```

   Read the error and note *which* of the two lookups the caret is under.
3. Write `category_total`, `grand_total` and `find_item`. All three are one
   expression each, and all three only read.
4. Write `remove_item` last of the mutating pair, and write it in the order
   the constraints describe: look up, compute, then change. Say each line out
   loud as "this can fail" or "this changes something", and check that all the
   first kind come before all the second kind.
5. Write `top_n_items`. Flatten to rows first, then sort, then slice —
   in that order, and with the flattening as its own visible step.
6. When `All checks passed.` prints, write your own `extra_tests()`. Find at
   least five things the given scaffolding never checks. This is the part of
   the challenge that teaches the most, and it is the part most people skip.
7. Write your reflection paragraph. Why a dict inside a dict, rather than one
   flat dict keyed by `(category, item)`? Name what each shape makes cheap and
   what it makes expensive.

## The Solution

```python
"""challenge-02-inventory-tracker-solution.py — a tiny warehouse backend.

Reflection on the structure I picked, as the rubric asks for.

I kept the nested dict[str, dict[str, int]] the brief hands me rather than
inventing a flat dict[(category, item), int]. Two reasons. First, the two
questions the app asks most often -- "what is in this category?" and
"how much of this item?" -- are both single O(1) hops in the nested shape,
whereas a flat dict answers the second in O(1) but needs a full O(n) scan
for the first. Second, the brief requires empty categories to disappear,
which is a statement about the inner dict's identity; a flat key space has
no inner dict to be empty. Every function is pure with respect to globals:
the inventory arrives as an argument, so the same code serves a test
fixture, a file-backed store, or a request handler without change.
"""

Inventory = dict[str, dict[str, int]]


def add_item(inv: Inventory, category: str, item: str, count: int = 1) -> None:
    """Add `count` of `item` to `category`, creating either if needed.

    Args:
        inv: The inventory, modified in place.
        category: The shelf the item lives on.
        item: The thing being stocked.
        count: How many to add. Must be positive.

    Raises:
        ValueError: If `count` is zero or negative.
    """
    if count <= 0:
        raise ValueError(f"count must be positive, got {count}")
    bucket = inv.setdefault(category, {})
    bucket[item] = bucket.get(item, 0) + count


def remove_item(inv: Inventory, category: str, item: str, count: int = 1) -> None:
    """Subtract `count` of `item`; prune the item and the category when empty.

    Args:
        inv: The inventory, modified in place.
        category: The shelf to take from.
        item: The thing being removed.
        count: How many to take. Taking more than there is empties the item.

    Raises:
        KeyError: If the category or the item is unknown. Nothing is changed
            when that happens.
    """
    bucket = inv[category]              # KeyError if the category is unknown
    remaining = bucket[item] - count    # KeyError if the item is unknown
    if remaining <= 0:
        del bucket[item]
    else:
        bucket[item] = remaining
    if not bucket:
        del inv[category]


def category_total(inv: Inventory, category: str) -> int:
    """Return the sum of all counts in `category`, or 0 if it does not exist.

    Args:
        inv: The inventory to read.
        category: The shelf to add up.

    Returns:
        The total count on that shelf. An unknown category is 0, not an error.
    """
    return sum(inv.get(category, {}).values())


def grand_total(inv: Inventory) -> int:
    """Return the sum of all counts across every category.

    Args:
        inv: The inventory to read.

    Returns:
        The total number of things in the warehouse.
    """
    return sum(count for bucket in inv.values() for count in bucket.values())


def find_item(inv: Inventory, item: str) -> list[str]:
    """Return the categories that hold `item`.

    Args:
        inv: The inventory to search.
        item: The thing to look for.

    Returns:
        The matching category names, in inventory order. Empty when the item
        is nowhere.
    """
    return [category for category, bucket in inv.items() if item in bucket]


def top_n_items(inv: Inventory, n: int = 3) -> list[tuple[str, str, int]]:
    """Return the n highest-count items in the whole inventory.

    Args:
        inv: The inventory to rank.
        n: How many rows to return. More than there are is not an error.

    Returns:
        Up to n (category, item, count) rows, count descending, ties broken
        by category then item, both A to Z.
    """
    rows = [
        (category, item, count)
        for category, bucket in inv.items()
        for item, count in bucket.items()
    ]
    rows.sort(key=lambda row: (-row[2], row[0], row[1]))
    return rows[:n]


def run_tests() -> None:
    """Run the brief's own scaffolding and report."""
    inv: Inventory = {}

    add_item(inv, "fruit", "apple", 5)
    add_item(inv, "fruit", "banana", 3)
    add_item(inv, "tools", "hammer", 1)
    add_item(inv, "fruit", "apple", 2)        # accumulates

    assert inv == {
        "fruit": {"apple": 7, "banana": 3},
        "tools": {"hammer": 1},
    }, inv

    assert category_total(inv, "fruit") == 10
    assert category_total(inv, "missing") == 0
    assert grand_total(inv) == 11

    assert find_item(inv, "apple") == ["fruit"]
    assert find_item(inv, "ghost") == []

    remove_item(inv, "fruit", "banana", 3)    # banana -> 0 -> deleted
    assert "banana" not in inv["fruit"]

    remove_item(inv, "tools", "hammer", 1)    # hammer gone -> category empty -> deleted
    assert "tools" not in inv

    try:
        remove_item(inv, "fruit", "phantom", 1)
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError")

    add_item(inv, "fruit", "cherry", 12)
    add_item(inv, "fruit", "date", 2)
    top = top_n_items(inv, 3)
    assert top[0] == ("fruit", "cherry", 12)
    assert len(top) == 3

    print("All checks passed.")


def extra_tests() -> None:
    """Check the edge cases the supplied scaffolding does not reach."""
    inv: Inventory = {"fruit": {"apple": 2}, "tools": {"saw": 1}}

    # over-removal clamps to deletion, never a negative count
    remove_item(inv, "fruit", "apple", 99)
    assert inv == {"tools": {"saw": 1}}, inv

    # an unknown category raises before touching anything
    try:
        remove_item(inv, "nope", "saw", 1)
    except KeyError as exc:
        assert exc.args[0] == "nope", exc.args
    else:
        raise AssertionError("Expected KeyError")
    assert inv == {"tools": {"saw": 1}}, inv

    # ties break on (category, item) alphabetical
    inv = {"b": {"x": 5, "a": 5}, "a": {"z": 5}}
    assert top_n_items(inv, 3) == [("a", "z", 5), ("b", "a", 5), ("b", "x", 5)]
    assert len(top_n_items(inv, 99)) == 3      # n larger than the inventory

    # everything survives an empty inventory
    assert top_n_items({}, 3) == []
    assert grand_total({}) == 0
    assert find_item({}, "apple") == []

    print("Extra checks passed.")


if __name__ == "__main__":
    run_tests()
    extra_tests()

    demo: Inventory = {
        "fruit": {"apple": 5, "banana": 3, "cherry": 12},
        "tools": {"hammer": 1, "saw": 2},
    }
    print(top_n_items(demo, 3))
```

**`add_item` uses two different get-or-default tools in two lines, and they
are not interchangeable.**

```python
bucket = inv.setdefault(category, {})       # I want the shelf to EXIST afterwards
bucket[item] = bucket.get(item, 0) + count  # I only want a number; no key needed yet
```

`setdefault` **writes**. After that line `inv[category]` is guaranteed to be a
dict, and `bucket` is a name for **that** dict, so the next line lands inside
the inventory. `.get` does **not** write; it supplies `0` for an item you have
never seen, and the assignment on the left is what creates the key.

Swap them and you get one of the quietest bugs in this course:

```python
bucket = inv.get(category, {})   # BUG: on a new category this dict is not in inv
bucket[item] = count             # ...so this writes into an object nobody holds
```

No exception. No output. The item simply never appears, and the dict you wrote
into is thrown away the moment the function returns.

**The `count <= 0` guard is beyond the brief.** Nothing asked for it. It is
there because `add_item(inv, "fruit", "apple", -5)` would otherwise quietly
create negative stock, and a warehouse with -5 apples is a bug you find three
days later in a report. Deleting the guard changes no test result. Keeping it
is a cheap promise about what the data can ever contain. Either choice is
defensible as long as you can say why — which is exactly what the reflection
paragraph is for.

**`remove_item` is entirely about the order of its lines.**

1. `bucket = inv[category]` — square brackets, because the brief says an
   unknown category must raise. This is a requirement, not a style choice.
2. `remaining = bucket[item] - count` — same reasoning for the item, and it
   happens **before** any change. If this line raises, nothing has been
   touched, so a failed call leaves the inventory exactly as it was.
3. Prune the item if it hit zero or went below. `<= 0` and not `== 0`.
4. Prune the category if the inner dict is now empty. `if not bucket:` works
   because an empty dict is falsy.

Step 4 only works because `bucket` is a **name for** the dict inside `inv`,
not a copy of it. There is one dict and two names, so `del bucket[item]` and
`del inv[category][item]` are the same action.

**`category_total` substitutes an empty container for a missing level.**
`sum(inv.get(category, {}).values())` covers "return 0, do not raise" in one
expression, because summing nothing is `0`. That is the safe-nested-read
pattern: put an empty thing where the missing thing was, and let the rest of
the expression run unchanged.

**`grand_total` walks two levels with a generator.** `sum(count for bucket in
inv.values() for count in bucket.values())` reads exactly like the nested loop
it replaces — outer clause walks the categories, inner clause walks each
category's counts. Round brackets rather than square means no intermediate
list is ever built.

**`find_item` relies on `in` testing a dict's keys.** For dicts, `item in
bucket` asks about keys, not values, and it does not depend on how many items
the shelf holds. So the whole function costs the number of *categories*, not
the number of items. It returns a list rather than a set so the order is
defined, which is what lets the assert say `== ["fruit"]`.

**`top_n_items` flattens, then sorts by a tuple key, then slices.**

```python
rows.sort(key=lambda row: (-row[2], row[0], row[1]))
```

Count downwards, then category upwards, then item upwards — exactly the
brief's rule, in the order the brief says it. The minus is what lets you mix
directions in one key. Slicing afterwards is safe for any `n`, because an
out-of-range slice clamps instead of raising, which is why
`top_n_items(inv, 99)` on a three-item inventory returns three rows rather
than exploding.

`.sort()` in place is correct here, unlike in Exercise 1, because `rows` is a
list this function built two lines earlier. Nobody else is holding it. The
rule was never "never sort in place"; it was "never rearrange something you
were handed".

## Download and run

Download
[challenge-02-inventory-tracker-solution.py](./challenge-02-inventory-tracker-solution.py)
and run it:

```bash
python challenge-02-inventory-tracker-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-02-inventory-tracker.py`.

## Common bugs to catch

- **`KeyError: 'tools'` when you were trying to *create* `tools`.**

  ```text
  Traceback (most recent call last):
      inv["tools"]["hammer"] = 1
      ~~~^^^^^^^^^
  KeyError: 'tools'
  ```

  Read the caret position: it is under `inv["tools"]`, the **inner** lookup,
  not under the assignment. Python has to evaluate `inv["tools"]` down to a
  real dict before it can store anything into it, and there is nothing there
  to evaluate. `inv.setdefault("tools", {})["hammer"] = 1` fixes it.

- **`add_item` runs, raises nothing, and adds nothing.** You used
  `inv.get(category, {})` instead of `inv.setdefault(category, {})`. On a
  category that already exists the two behave identically, so your first few
  calls work and only *new* categories vanish. There is no traceback and no
  output — the only symptom is a missing row. Check by printing `inv`
  immediately after the call that should have created it.

- **`AssertionError: Expected KeyError`.** You used `.get` inside
  `remove_item`, so removing from an unknown category silently does nothing
  instead of raising. The brief chose `KeyError` deliberately. Match the
  contract you were given rather than the one that felt friendlier.

- **A phantom item appears and disappears, and no error is raised.** You
  subtracted first and checked afterwards:

  ```python
  bucket[item] = bucket.get(item, 0) - count
  if bucket[item] <= 0:
      del bucket[item]
  ```

  ```text
  created: {'fruit': {'apple': 2, 'phantom': -1}}
  and deleted again: {'fruit': {'apple': 2}}
  ```

  `remove_item(inv, "fruit", "phantom", 1)` creates `phantom: -1`, notices it
  is negative, and deletes it — so the data ends up correct and the required
  `KeyError` never happens. The test fails and the inventory looks fine, which
  is a confusing combination until you see it. Validate, then change. That
  ordering is also what makes a function safe to retry after a failure.

- **`RuntimeError: dictionary changed size during iteration`.** You swept the
  whole inventory looking for empty categories:

  ```text
  Traceback (most recent call last):
      for cat in inv:
                 ^^^
  RuntimeError: dictionary changed size during iteration
  ```

  Iterate a snapshot instead: `for cat in list(inv):`. Better still, do not
  sweep at all — `remove_item` already has the one category that could have
  emptied, right there in `bucket`.

- **`top_n_items` breaks ties backwards.** You wrote
  `rows.sort(key=lambda row: (row[2], row[0], row[1]), reverse=True)`:

  ```text
  [('b', 'x', 5), ('b', 'a', 5), ('a', 'z', 5)]
  ```

  The counts come out descending, and so do the tie-breakers, so ties resolve
  in reverse alphabetical order. The brief's own tie-break example wants
  `[('a', 'z', 5), ('b', 'a', 5), ('b', 'x', 5)]`. Negate the field you want
  descending; leave `reverse` alone when the key mixes directions.

- **`category_total` creates the category it was asked about.** You wrote
  `inv.setdefault(category, {})` where `.get` belonged. A function whose name
  begins with a noun, and whose job is to answer a question, should not leave
  a mark on the data. Two calls to `category_total(inv, "missing")` would grow
  the inventory by an empty shelf.

## Under the hood

<details>
<summary>Under the hood — nested versus flat, and what `defaultdict` really costs</summary>

**The shape you did not build.** The obvious alternative to a dict inside a
dict is one flat dict keyed by a pair:

```python
flat: dict[tuple[str, str], int] = {
    ("fruit", "apple"): 5,
    ("fruit", "banana"): 3,
    ("tools", "hammer"): 1,
}
```

That is perfectly legal — a tuple of strings is hashable, so it can be a key.
Compare the two on the questions the app actually asks:

| Question | Nested | Flat |
|---|---|---|
| how much of this exact item? | two hops, both instant | one hop, instant |
| what is on this shelf? | one hop, then read that shelf | read the **whole** dict, filtering |
| is this shelf empty? | ask the inner dict | there is no inner dict to ask |
| save it as JSON | works as-is | keys are tuples; `json` refuses |

The flat shape wins one row and loses three. That is why the brief chose the
nested one, and why the reflection paragraph asks you to say so in your own
words.

The last row is worth a sentence on its own. JSON object keys are always
strings, so `json.dumps` on the flat version raises `TypeError: keys must be
str, int, float, bool or None, not tuple`. The nested shape is JSON-native by
accident, which is a real argument in its favour even though nobody designed
for it.

**`setdefault` is one lookup, not two.** The version people write first is:

```python
if category not in inv:
    inv[category] = {}
bucket = inv[category]
```

Three lines and up to three hash lookups of the same key. `setdefault` does it
in one call and one lookup. It also fixes an entire class of race in
concurrent code, though that is a story for a much later week.

The catch: `setdefault` builds its default **every time**, even when the key
is already there. With `{}` that is a tiny wasted allocation nobody can
measure. With something expensive it is a real cost, and that is when you want
`defaultdict` instead — it only calls the factory on an actual miss.

**`defaultdict`, and the price of the convenience.**

```python
from collections import defaultdict

NestedCounts = defaultdict[str, defaultdict[str, int]]


def new_inventory() -> NestedCounts:
    """Return an inventory that creates its own levels on demand."""
    return defaultdict(lambda: defaultdict(int))


def add_item_dd(inv: NestedCounts, category: str, item: str, count: int = 1) -> None:
    """Add `count` of `item` to `category`."""
    inv[category][item] += count
```

`add_item` goes from three lines to one, and it is genuinely more readable.
Now look at the price:

```text
equal to plain dict? True
reading a missing key AUTOVIVIFIES: 0 -> {'fruit': defaultdict(<class 'int'>, {'apple': 7}), 'ghost': defaultdict(<class 'int'>, {'thing': 0})}
```

Two things to notice. It compares equal to a plain dict, so all your asserts
still pass. But **reading** `inv["ghost"]["thing"]` *created* both levels.
That is called **autovivification**, and it means a `defaultdict` has no
read-only mode: every square-bracket access is potentially a write. So
`category_total` and `find_item` must keep using `.get` and `in` even after
the rewrite, or merely asking a question grows the warehouse.

It also does not print nicely, and it does not survive `json.dumps` as a
`defaultdict` — it comes back as a plain dict. The usual advice: use it where
insertion dominates, and keep plain dicts on the boundaries where data enters
and leaves.

**Would `Counter` help?** Partly, and it brings one trap:

```text
Counter after update: Counter({'apple': 7, 'banana': 3})
Counter after subtract past zero: Counter({'apple': 7, 'banana': -2})
most_common(2): [('apple', 7), ('banana', -2)]
```

`Counter.update({"apple": 2})` **adds** counts, unlike `dict.update`, which
replaces them — a nice fit for `add_item`. And `most_common(n)` looks like a
free `top_n_items`. But `Counter.subtract` happily goes negative and does not
delete the key, so it does not implement this brief's `remove_item` at all;
and `most_common` sorts by count with no defined tie-break, so it does not
implement the ordering either — the same gap Exercise 3 found. The verdict:
`Counter` is the right tool for **counting** and the wrong tool for **stock
levels**, because stock has a floor at zero and this challenge's rules all
live at that floor.

**Where the cost actually is.** Every function here is one pass over something:
`grand_total` and `top_n_items` touch every item once, `find_item` touches
every category once, `add_item` and `remove_item` touch a fixed number of
keys. The only thing that grows faster than the data is the sort inside
`top_n_items`, and sorting is `O(n log n)`, which for any warehouse you will
ever hold in memory is indistinguishable from free. There is no clever
optimisation waiting here — the structure already made the program cheap,
which is what picking the right structure buys you.

</details>

## Acceptance checklist

- [ ] `python challenge-02-inventory-tracker.py` prints `All checks passed.` and your own extra checks.
- [ ] `remove_item` raises `KeyError` for an unknown category and for an
      unknown item, and the inventory is unchanged afterwards in both cases.
- [ ] Removing the last of an item deletes the item; emptying a category
      deletes the category.
- [ ] `category_total` returns `0` for a missing category and does not create it.
- [ ] `top_n_items` ties break on category then item, and `n` larger than the
      inventory returns everything rather than raising.
- [ ] No function reads a global inventory.
- [ ] Type hints on all six signatures and a docstring on each.
- [ ] The module docstring holds your own reflection on nested versus flat.
- [ ] You wrote at least five checks the given scaffolding does not contain.
- [ ] Committed to Git with a message like `Add Week 5 challenge 2: inventory tracker`.

## Stretch

- **Persistence with `json`.**

  ```python
  import json
  from pathlib import Path

  INVENTORY_PATH = Path("inventory.json")


  def save_inventory(inv: Inventory, path: Path = INVENTORY_PATH) -> None:
      """Write the inventory to `path` as sorted, indented JSON."""
      path.write_text(json.dumps(inv, indent=2, sort_keys=True), encoding="utf-8")


  def load_inventory(path: Path = INVENTORY_PATH) -> Inventory:
      """Read the inventory back, returning an empty one if the file is absent."""
      if not path.exists():
          return {}
      return json.loads(path.read_text(encoding="utf-8"))
  ```

  ```text
  round trip equal? True
  {
    "fruit": {
      "apple": 5,
      "cherry": 12
    },
    "tools": {
      "saw": 2
    }
  }
  missing file -> {}
  ```

  This round-trips cleanly *because* every key is a string and every value is
  a number. Try the same thing with the flat, tuple-keyed shape from *Under
  the hood* and `json.dumps` refuses outright.

- **The `defaultdict` rewrite.** Covered in *Under the hood*, including the
  autovivification trap. Do the rewrite, then deliberately call
  `category_total` on a category that does not exist and check whether your
  inventory grew.

- **Would `Counter` simplify the inner dicts?** Also in *Under the hood*. Try
  it, then write two sentences in your file saying what you decided and why.
  The answer is more interesting than a yes or a no.

- **`render(inv)` — a printable inventory.**

  ```python
  def render(inv: Inventory) -> str:
      """Return the inventory as a readable block of text."""
      if not inv:
          return "(empty inventory)"
      lines: list[str] = []
      for category in sorted(inv):
          lines.append(f"{category} ({category_total(inv, category)})")
          for item in sorted(inv[category]):
              lines.append(f"  {item:<10} {inv[category][item]:>4}")
      lines.append(f"TOTAL {grand_total(inv)}")
      return "\n".join(lines)
  ```

  ```text
  fruit (20)
    apple         5
    banana        3
    cherry       12
  tools (3)
    hammer        1
    saw           2
  TOTAL 23
  ```

  `{item:<10}` left-aligns in a ten-wide column and `{count:>4}` right-aligns
  in four, which is what makes the numbers line up. Note it **returns** a
  string rather than printing one. A function that returns text can be
  asserted on, written to a file, or sent over a network. A function that
  prints can only be watched.

- **`move_item`, atomically.**

  ```python
  def move_item(
      inv: Inventory, from_cat: str, to_cat: str, item: str, count: int = 1
  ) -> None:
      """Move `count` of `item` between categories, or change nothing at all."""
      if count <= 0:
          raise ValueError(f"count must be positive, got {count}")
      available = inv[from_cat][item]          # KeyError before any mutation
      if count > available:
          raise ValueError(
              f"cannot move {count} of {item!r}: only {available} in {from_cat!r}"
          )
      remove_item(inv, from_cat, item, count)
      add_item(inv, to_cat, item, count)
  ```

  ```text
  move_item guard: cannot move 10 of 'bolt': only 4 in 'warehouse'
  ```

  "Atomic" here means: **every check that can fail happens before the first
  change.** Once `remove_item` runs, nothing left in the function is capable
  of raising, so there is no path that deletes stock from one category and
  never adds it to the other. That is the same discipline as `remove_item`'s
  own step 2, and it is the whole technique.

  Check the degenerate case too. `move_item(inv, "fruit", "fruit", "apple",
  2)` should end where it started: the remove may delete the category, and the
  add recreates it with the same count.

That is Week 5's challenges done. The rest of the week's work is listed in the
[week overview](../README.md).
