# Homework Problem 4 — Find duplicates

> **Topic:** counting with a dict, generator expressions inside `sorted`, and why `list.count` inside a loop is a trap
> **Lecture:** [02 — Sets and Dictionaries](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** there is a two-line answer to this problem that passes every test the brief gives you and is still wrong, because it breaks the one rule the brief bothered to write down. Learning to spot a scan hidden inside a loop — which is what that answer is — is a skill you will use for the rest of your life, and this is the cheapest place to learn it.

## The Brief

Given a list, tell me which items turned up more than once.

```python
find_duplicates([1, 2, 3, 2, 4, 5, 1, 1])
# [1, 2]

find_duplicates(["a", "b", "c"])
# []
```

Read that first answer carefully. The `1` appears three times in the input and
**once** in the output. The question is "which items repeated", not "how many
copies were there", so each repeated item is named once no matter how many
copies existed. The answer comes back sorted.

Write one function.

```python
def find_duplicates(items: list) -> list:
    ...
```

**The rule that makes this a problem:** look at each item once. Do not compare
every item with every other item.

The way to do that is to stop asking "does this item appear anywhere else?" and
start **counting**. Walk the list once, keeping a tally for each item as you go.
Then look at the tallies and keep the ones above one. Nothing is ever compared
against the whole list, because after the walk you already know.

A dict is the tally. The item is the key and the count is the value.

## Starter

Save this in your `homework/` folder as part of `week-05-solutions.py` and fill
in the `TODO`s. It runs as pasted — it just finds nothing:

```python
"""Week 5 homework, problem 4: name the items that appear more than once."""


def find_duplicates(items: list) -> list:
    """Return a sorted list of the items that appear more than once.

    Args:
        items: The items to inspect. They must be hashable and comparable.

    Returns:
        A new sorted list, each repeated item appearing once.

    Example:
        >>> find_duplicates([1, 2, 3, 2, 4, 5, 1, 1])
        [1, 2]
    """
    counts: dict = {}
    # TODO 1: one pass over items, adding 1 to that item's tally.
    #         `counts.get(item, 0)` supplies the 0 for a first sighting.
    # TODO 2: keep the items whose tally is above 1, and sort them.
    return []


def _demo() -> None:
    """Print the brief's two examples."""
    print(find_duplicates([1, 2, 3, 2, 4, 5, 1, 1]))
    print(find_duplicates(["a", "b", "c"]))


if __name__ == "__main__":
    _demo()
```

Print the tally before you filter it — it is the part worth seeing:

```python
print({1: 3, 2: 2, 3: 1, 4: 1, 5: 1})
```

```text
{1: 3, 2: 2, 3: 1, 4: 1, 5: 1}
```

Two entries there are above 1. Those two are the whole answer.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/homework/problem-04-find-duplicates.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_duplicates(items)` returns a sorted list of the items that appear more
   than once.
2. Each repeated item appears **once** in the answer:
   `find_duplicates([5, 5, 5, 5])` is `[5]`.
3. `find_duplicates([])` returns `[]`, and a list with no repeats returns `[]`.
4. The input list is not changed.
5. Each item is looked at a fixed number of times. No `list.count`, no `in`
   test against a list, no nested loops.
6. Type hints on the signature and a docstring on the function.
7. These three asserts pass:

   ```python
   assert find_duplicates([1, 2, 3, 2, 4, 5, 1, 1]) == [1, 2]
   assert find_duplicates(["a", "b", "c"]) == []
   assert find_duplicates(["x", "x", "y", "y", "z"]) == ["x", "y"]
   ```

## Constraints

- **Count first, filter second.** Two separate passes, each of them straight
  through. The moment a search appears *inside* the walk, you have written the
  slow version.
- **No `items.count(x)`.** It looks like a method call and it is a walk of the
  whole list. Called once per item, it is the thing requirement 5 forbids,
  dressed up.
- **Use `counts.get(item, 0) + 1` rather than an `if`.** `.get` supplies the
  zero for an item you have not seen, so there is no "have I met this before"
  branch to get wrong.
- **Sort at the end, and sort the result.** Dicts come out in first-seen order,
  which is not the order the brief asks for. `sorted()` on the filtered items is
  one call and makes the output the same every run.
- **`_demo` prints; `find_duplicates` does not.**

## Expected output

```text
$ python problem-04-find-duplicates.py
[1, 2]
[]
['x', 'y']
[5]
All 5 asserts passed.
```

The first three lines are the brief's examples and the required asserts. The
fourth is `find_duplicates([5, 5, 5, 5])`, and it is the one that catches the
most common wrong answer: four copies of the `5`, but the `5` is a single
repeated item, so it is named **once**.

Prove the input survived:

```bash
python -c "from week_05_solutions import find_duplicates as f; xs=[1,1,2]; f(xs); print(xs)"
```

```text
[1, 1, 2]
```

## Steps

1. Save the Starter into `week-05-solutions.py` and run it. Two empty lists.
2. Write TODO 1 — three lines, one of which is the loop:

   ```python
   for item in items:
       counts[item] = counts.get(item, 0) + 1
   ```

3. Add `print(counts)` just after the loop and run it. You should see
   `{1: 3, 2: 2, 3: 1, 4: 1, 5: 1}`. Take the print out again.
4. Write TODO 2. Filter and sort in one expression:

   ```python
   return sorted(item for item, n in counts.items() if n > 1)
   ```

   Note the round brackets. That is a **generator expression** — it hands
   `sorted` one item at a time rather than building a list first for `sorted` to
   copy.
5. Run it. You want `[1, 2]` and `[]`.
6. Add the three required asserts, plus these two:

   ```python
   assert find_duplicates([]) == []
   assert find_duplicates([5, 5, 5, 5]) == [5]
   ```

7. Try `find_duplicates([1, 1, "a", "a"])` and read the error. The *counting*
   worked; it is the **sort** that refused. Add a sentence to your docstring
   saying the items have to be comparable to each other.
8. Compare with **The Solution**, tick the acceptance checklist, and commit:
   `git commit -m "Week 5 homework: find duplicates"`.

## The Solution

```python
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
```

**Why it works.**

There are three phases, and the point of the design is that not one of them
compares everything with everything.

**1. Count.** One walk over `items`. Each turn does one dict read and one dict
write, and neither of those looks at the rest of the dict. `counts.get(item, 0)`
is the counting idiom from
[lecture 02](../lecture-notes/02-sets-and-dicts.md#counting): the `0` default is
what a first sighting gets, so there is never an "if I have seen this before"
branch. Cost: proportional to the number of items.

**2. Filter.** `if n > 1` over the tallies. There are at most as many tallies as
there were items, so this is another straight walk. The round brackets make it a
**generator expression**, so no throwaway list is built — `sorted` pulls the
items as they are produced. See
[lecture 03](../lecture-notes/03-comprehensions-and-big-o.md#4-generator-expressions-a-preview).

**3. Sort.** Only the answer is sorted, and the answer is usually much smaller
than the input.

Add those together and the honest description is "linear in the input, plus a
sort of the output" — which is what the brief means when it says `O(n)`.

**Why counting rather than comparing.** The version everybody writes first asks,
of each item, "does this appear anywhere else?", and answering that means
looking at the whole list. Counting never compares two items at all. It uses
each item as an **address**, goes to that address, and adds one to whatever is
there. That is the same "turn a search into a lookup" move as Problem 3, and it
is why the items have to be hashable — being usable as an address is exactly
what hashable means.

**Why each item is named once.** `[5, 5, 5, 5]` gives `[5]`. The tally has one
row per distinct item however many copies arrived, so iterating
`counts.items()` can only ever produce each item once. That is not a special
case in the code; it falls out of the structure, which is usually the sign that
the structure is right.

**Why `sorted` at the end.** A dict comes out in first-seen order —
`{1: 3, 2: 2, 3: 1, ...}` for the brief's example. First-seen order is not the
brief's order and it changes when the input is reordered, so the answer would
not be stable. One `sorted()` call fixes both.

## Run it

Copy the worked answer on this page into `problem-04-find-duplicates.py` and run it:
and run it:

```bash
python problem-04-find-duplicates.py
```

Your own copy of `find_duplicates` belongs in `week-05-solutions.py`, and that
is the file you commit. The longer download name keeps the published answer from
landing on top of your work.

## Common bugs to catch

- **The two-line answer that passes every required test.**

  ```python
  return sorted({x for x in items if items.count(x) > 1})
  ```

  It returns the right answer for all three required asserts, which is exactly
  why it survives a careless review. But `items.count(x)` walks the entire list,
  and you call it once per item, so this compares everything with everything —
  the one thing requirement 5 forbids. The tell is always the same shape: **a
  scan of a list, inside a loop over that same list.** Once you can see that
  shape you will see it everywhere.
- **Reporting every copy instead of every repeated item.**

  ```python
  dups = []
  for x in items:
      if items.count(x) > 1:
          dups.append(x)
  return sorted(dups)
  ```

  ```text
  find_duplicates([1, 2, 3, 2, 4, 5, 1, 1]) -> [1, 1, 1, 2, 2]
  ```

  Slow *and* wrong. `assert find_duplicates([5, 5, 5, 5]) == [5]` catches it
  instantly; the brief's own examples happen not to.
- **A "seen" set with nowhere to put the answer.**

  ```python
  seen = set()
  dups = []
  for x in items:
      if x in seen:
          dups.append(x)      # appends again on the third, fourth, ... copy
      seen.add(x)
  return sorted(dups)
  ```

  The set approach is genuinely fast and perfectly fine — but it needs **two**
  sets, not one set and a list, so that the third copy of an item does not name
  it a second time. Making `dups` a `set` and returning `sorted(dups)` fixes it.
  Counting sidesteps the whole question.
- **Sorting a mixed-type answer.**

  ```python
  find_duplicates([1, 1, "a", "a"])
  ```

  ```text
  Traceback (most recent call last):
    File "week-05-solutions.py", line 4, in <module>
      print(find_duplicates([1, 1, "a", "a"]))
            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
    File "week-05-solutions.py", line 3, in find_duplicates
      return sorted(i for i, n in counts.items() if n > 1)
  TypeError: '<' not supported between instances of 'str' and 'int'
  ```

  The counting was fine — a dict is perfectly happy to mix key types. It is the
  **sort** that refuses, because Python 3 will not put a `str` in order against
  an `int`. The signature `items: list` promises nothing about the contents, so
  say in the docstring that the items must be comparable to each other.
- **Unhashable items.** `find_duplicates([[1], [1]])` raises
  `TypeError: unhashable type: 'list'` at the counting step, not the sorting
  step. Same rule as Problem 2: a key has to be hashable. Convert the inner
  lists to tuples if you genuinely need this.
- **Reaching for `Counter.most_common()`.** It sorts by **count**, and the brief
  wants the items sorted by value. It is the right method for "what are the top
  three words" and the wrong one here.

## Under the hood

<details>
<summary>Under the hood — building a set from a list, versus scanning the list again and again</summary>

Every wrong turn on this page is the same mistake in a different costume:
answering "have I seen this before?" by looking through everything you have seen
so far. It is worth understanding precisely what that costs and precisely what
building a set instead buys you, because the trade shows up constantly and the
answer is not always the same.

**A list has no idea what is inside it.** `x in some_list` starts at the front
and compares, one item at a time, until it finds a match or runs off the end.
For a list of `n` items that is up to `n` comparisons. Nothing about a list is
sorted or indexed by value, so there is nothing cleverer it could do.

**A set knows where things live.** `x in some_set` hashes `x`, goes to that one
slot, and looks. One hash, one probe, regardless of whether the set holds ten
items or ten million.

So:

| | Build cost | Each membership test | `m` tests over `n` items |
|---|---|---|---|
| Keep the list, scan it | free — you already have it | up to `n` comparisons | about `m × n` |
| Build a set first | `n` hashes, plus memory | one hash and a probe | about `n + m` |

Read the last column, because that is where the decision lives.

**One test:** `m = 1`, so scanning costs `n` and the set costs `n + 1`. Building
the set is *worse*. If you are going to ask exactly once, ask the list.

**Many tests:** `m` and `n` both large, and `m × n` pulls away from `n + m`
fast. At `n = m = 20,000` that is 400 million comparisons against 40,000
operations. This is the case in the wrong turns above, and in Exercise 02 of
this week, where the same swap was measured at 536 times faster on 20,000 rows.

**The break-even is at roughly one test.** That is why the rule of thumb is so
blunt: **if you are going to test membership more than once, build the set.**
The build is one pass, and it pays for itself almost immediately.

What the set costs you is real, though, and worth saying out loud:

- **Memory.** A hash table keeps empty slots on purpose — it grows itself when
  it gets past about two thirds full, because a crowded table starts colliding
  and slowing down. A set of `n` items uses noticeably more memory than a list
  of the same `n` items.
- **Order.** A set has none. If you need to know which came first, a set cannot
  tell you, and you want the dict of counts — or, for order alone,
  `dict.fromkeys(items)`, which deduplicates while keeping first-seen order.
- **Hashability.** Everything going in must be hashable, which rules out lists
  and dicts as members.
- **Duplicates.** They vanish. That is usually the point, and occasionally the
  bug.

This problem needs counts rather than mere membership, so it uses a dict rather
than a set — but a dict is a set with values attached, and every cost and
benefit above applies unchanged. The one extra thing counting buys you over a
set is the ability to tell "seen twice" from "seen four times", which is exactly
the distinction the `[5, 5, 5, 5]` case turns on.

</details>

<details>
<summary>Under the hood — Counter, and what a dict subclass gets you</summary>

The standard library has already written the counting loop. It lives in
`collections`:

```python
>>> from collections import Counter
>>> Counter([1, 2, 3, 2, 4, 5, 1, 1])
Counter({1: 3, 2: 2, 3: 1, 4: 1, 5: 1})
```

So the whole function collapses to one line:

```python
from collections import Counter


def find_duplicates_counter(items: list) -> list:
    """Same thing with collections.Counter."""
    return sorted(item for item, n in Counter(items).items() if n > 1)
```

This is what you should write at work, and it is **stretch goal 1** from
[the week README](../README.md#stretch-goals), which asks you to redo the
word-frequency exercise with `Counter`.

Two reasons the hand-rolled loop is still the one to learn first.

**A `Counter` is a `dict`.** Not something like one — a subclass. Everything you
know still applies:

```python
>>> c = Counter("hello")
>>> isinstance(c, dict)
True
>>> c["l"]
2
>>> c["z"]
0
```

The only interesting difference is that last line. An ordinary dict raises
`KeyError` for a missing key; a `Counter` answers `0`, because "a thing I have
never seen appeared zero times" is the sensible answer for a tally. It does that
through `__missing__`, a hook a dict subclass can define — and note that
reading `c["z"]` does **not** insert it, which is where `Counter` differs from
`defaultdict`:

```python
>>> c["z"]
0
>>> "z" in c
False
```

**The counting loop is the thing you are practising.** `Counter` does that loop
in C, which makes it faster, but "faster" is not why you learn a loop. The loop
is the shape you will need the next time the tally is not a plain count — a
running total of prices, a longest-so-far, a set of tags per key. `Counter`
solves exactly one of those; the loop solves all of them.

Two `Counter` conveniences worth knowing when you do reach for it:

```python
>>> Counter("hello").most_common(2)
[('l', 2), ('h', 1)]
>>> Counter("aab") - Counter("ab")
Counter({'a': 1})
```

`most_common` sorts by count, which is the wrong order for this problem and the
right one for a top-N list. And counters subtract, which is a neat way to ask
"what is in this bag that is not in that one, allowing for copies" — a question
plain sets cannot answer, because sets have no notion of "two of them".

</details>

## Acceptance checklist

- [ ] `find_duplicates([1, 2, 3, 2, 4, 5, 1, 1])` gives `[1, 2]`.
- [ ] `find_duplicates(["a", "b", "c"])` gives `[]`.
- [ ] `find_duplicates(["x", "x", "y", "y", "z"])` gives `['x', 'y']`.
- [ ] `find_duplicates([])` gives `[]`.
- [ ] `find_duplicates([5, 5, 5, 5])` gives `[5]`, not `[5, 5, 5]`.
- [ ] There is no `items.count(...)` and no `x in items` anywhere.
- [ ] The answer is sorted, and the input list is unchanged.
- [ ] The docstring says the items must be hashable and comparable.
- [ ] The signature has type hints and the function has a docstring.
- [ ] Committed with a message like `Week 5 homework: find duplicates`.

## Stretch

- **Rewrite it with `Counter`.** One line, shown in the second *Under the hood*
  block. Keep both versions and assert they agree on the same inputs — two
  implementations that must produce identical answers make an excellent test of
  each other.
- **Return the counts as well.** Change the answer to
  `list[tuple[object, int]]`, sorted by item, so a caller can see *how many*
  copies there were. Then decide whether you prefer that signature to the
  simple one, and write down why. A richer return type is not automatically a
  better one.
- **Find the items that appear exactly once.** Change `> 1` to `== 1` and you
  have the opposite question, which is the usual way "find the odd one out"
  puzzles are phrased. Both answers come out of the same single tally, which is
  the argument for counting rather than for a `seen` set.
- **Handle unhashable items.** Make it work for a list of lists by counting
  `tuple(item)` instead, and converting back on the way out. Then explain in a
  comment what you gave up: two lists that are `==` now share a tally even if
  the caller thought of them as separate objects.
- **Measure the trap.** Time the `items.count(x)` version against the counting
  version on a list of 20,000 random integers, using `timeit`. Then double the
  list to 40,000 and run both again. One time roughly doubles and the other
  roughly quadruples, which is the whole of the first *Under the hood* block in
  two numbers.

Next: [Homework Problem 5 — Group by first letter](./problem-05-group-by-first-letter.md).
