# Homework Problem 6 — Intersect dictionaries

> **Topic:** membership tests on keys, dict comprehensions with a filter, and the set algebra hiding inside `.keys()`
> **Lecture:** [02 — Sets and Dictionaries](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Medium
> **Target time:** 35 minutes
> **Why this one:** it is the last problem of the week and the smallest, and it quietly asks you to say out loud which of two structures your values come from. That question — "these two things share keys, so whose values win?" — turns up every time you merge, reconcile or compare two sources of data, and getting it wrong produces an answer that looks completely plausible.

## The Brief

Two dicts. Give me back only the keys they have in common, with the values taken
from the **first** one.

```python
intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4})
# {"b": 2, "c": 3}
```

Follow that carefully. `"a"` is only in the first dict, so it goes. `"d"` is
only in the second, so it goes. `"b"` and `"c"` are in both, so they stay — and
they stay with the values `2` and `3`, which came from the first dict. The `99`
and the `100` are never used at all.

That is the shape worth naming: the second dict is a **filter**, not a source of
data. You read its keys and you never read its values.

Write one function.

```python
def intersect_dicts(d1: dict, d2: dict) -> dict:
    ...
```

Build it with a dict comprehension, or with the set operation that dicts offer
on their keys — `d1.keys() & d2.keys()`. The brief allows either. They differ in
one visible way, and *Why it works* is about that difference.

## Starter

Save this in your `homework/` folder as part of `week-05-solutions.py` and fill
in the `TODO`. It runs as pasted — it just gives back an empty dict:

```python
"""Week 5 homework, problem 6: keep the keys two dicts share."""


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
    # TODO: one dict comprehension over d1.items(), keeping only the pairs
    #       whose key is also in d2.
    return {}


def _demo() -> None:
    """Print the brief's example and the empty case."""
    print(intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4}))
    print(intersect_dicts({}, {"a": 1}))


if __name__ == "__main__":
    _demo()
```

One thing to check at the REPL before you start, because it is the fact the
whole problem rests on:

```python
d2 = {"b": 99, "c": 100}
print("b" in d2, 99 in d2)
```

```text
True False
```

`in` on a dict asks about **keys**. The `99` is right there as a value and `in`
says `False`, because it never looked at the values.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/homework/problem-06-intersect-dictionaries.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `intersect_dicts(d1, d2)` returns a new dict holding only the keys present
   in both.
2. Every value comes from `d1`. `d2`'s values are never read.
3. `intersect_dicts({}, {"a": 1})` and `intersect_dicts({"a": 1}, {})` both
   return `{}`.
4. Neither input dict is changed.
5. The body is a dict comprehension, or uses `d1.keys() & d2.keys()`.
6. Type hints on the signature and a docstring on the function.
7. These three asserts pass:

   ```python
   assert intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4}) == {"b": 2, "c": 3}
   assert intersect_dicts({}, {"a": 1}) == {}
   assert intersect_dicts({"x": 1}, {"x": 1}) == {"x": 1}
   ```

## Constraints

- **Test with `key in d2`, not `key in d2.keys()` and not `key in d2.values()`.**
  The first is the same thing with three extra words; the third is a different
  question and a slow one.
- **No nested loop over both dicts.** `for k1 in d1: for k2 in d2:` gives the
  right answer by comparing every key with every key, when a single membership
  test already knows.
- **Say out loud which dict the values come from.** The brief puts "first" in
  bold for a reason. If you find yourself writing `d2[key]`, stop and re-read
  the requirement.
- **Build a new dict.** Do not delete keys out of `d1` in place — the caller is
  still holding it.
- **`_demo` prints; `intersect_dicts` does not.**

## Expected output

```text
$ python problem-06-intersect-dictionaries-solution.py
{'b': 2, 'c': 3}
{}
{'x': 1}
['c', 'a']
All 5 asserts passed.
```

The first three lines are the brief's example and the two required asserts.

The fourth is the interesting one. It is
`list(intersect_dicts({"c": 1, "a": 2}, {"a": 0, "c": 0}))` — the **keys** of
the answer — and they come out `['c', 'a']`, which is the order they were in
inside `d1`. The comprehension walks `d1` and writes as it goes, so `d1`'s order
survives. The `keys() & keys()` version produces a set, and a set has no order
to give you.

Prove that neither input was touched:

```bash
python -c "from week_05_solutions import intersect_dicts as f; a={'x':1}; b={'x':9}; f(a,b); print(a, b)"
```

```text
{'x': 1} {'x': 9}
```

## Steps

1. Save the Starter into `week-05-solutions.py` and run it. Two empty dicts.
2. Check the fact the problem rests on, at the REPL:

   ```python
   d2 = {"b": 99, "c": 100}
   print("b" in d2)
   print(99 in d2)
   ```

   ```text
   True
   False
   ```

3. Write the comprehension. It is Problem 2's shape with a filter bolted on:

   ```python
   return {key: value for key, value in d1.items() if key in d2}
   ```

   Read it in the order it runs: for each pair in `d1`, keep it if its key is
   also in `d2`.
4. Run it. You want `{'b': 2, 'c': 3}` and `{}`.
5. Add the three required asserts, plus these two:

   ```python
   assert intersect_dicts({"a": 1}, {}) == {}
   assert list(intersect_dicts({"c": 1, "a": 2}, {"a": 0, "c": 0})) == ["c", "a"]
   ```

6. Now write the other version and compare them:

   ```python
   {key: d1[key] for key in d1.keys() & d2.keys()}
   ```

   Both pass every equality assert. Only one passes the key-order assert. Run
   `print(d1.keys() & d2.keys())` on its own and look at what type comes back.
7. Compare with **The Solution**, tick the acceptance checklist, and commit:
   `git commit -m "Week 5 homework: intersect dictionaries"`.

## The Solution

```python
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
```

**Why it works.**

**`key in d2` tests keys, and it is a lookup rather than a search.** That single
fact is the whole problem. Walking `d1.items()` looks at each of its pairs once,
and each membership test costs the same whether `d2` holds three keys or three
million, so the function's cost is set entirely by the size of `d1`. The obvious
alternative — comparing every key of `d1` with every key of `d2` — produces
exactly the same answer for the product of the two sizes.

**`{key: value for ...}` rebuilds a dict from the survivors**, and `value` comes
from the pair that was unpacked out of `d1`. That is how "values taken from the
first dict" is satisfied: `d2` appears in the function exactly once, inside the
`if`, and nowhere else. When you can point at a parameter and say "this one is
only a filter", the shape is right.

**Why this version and not the `keys() & keys()` one.** Both are allowed. Both
pass every equality assert, because `==` on dicts ignores order. They differ in
one visible way:

```python
>>> d1 = {"a": 1, "b": 2, "c": 3}
>>> d2 = {"b": 99, "c": 100, "d": 4}
>>> d1.keys() & d2.keys()
{'b', 'c'}
```

Those are curly braces with no colons in them — that is a **set**. `.keys()`
gives back a view that supports the set operators, so `&` hands you a genuine
set of the shared keys. A set has no meaningful order, so building the result by
iterating it means the output's key order depends on hash values rather than on
`d1`. Within one run it is stable; it is not `d1`'s order and you should not
lean on it. The `items()` comprehension keeps `d1`'s insertion order, which is
why `list(intersect_dicts({"c": 1, "a": 2}, ...)) == ["c", "a"]` is a thing you
can assert and the view version's order is not.

Reach for the view form when what you actually want is **set algebra on keys**
and a set is the right answer — `d1.keys() - d2.keys()` for "keys only in the
first" is genuinely lovely, and hard to beat for saying what it means. Reach for
the comprehension when the answer is a dict and order matters.

**Which dict should you walk?** The smaller one, if you know which that is. The
answer is the same either way, because the shared-key set is symmetric, but the
cost follows whichever one you iterate. If `d1` is enormous and `d2` is tiny,
`{k: d1[k] for k in d2 if k in d1}` is faster — at the price of losing `d1`'s
order. Worth knowing. Not worth doing until you have measured.

## Download and run

Download [problem-06-intersect-dictionaries-solution.py](./problem-06-intersect-dictionaries-solution.py)
and run it:

```bash
python problem-06-intersect-dictionaries-solution.py
```

Your own copy of `intersect_dicts` belongs in `week-05-solutions.py`, and that
is the file you commit. The longer download name keeps the published answer from
landing on top of your work.

## Common bugs to catch

- **Taking the values from the wrong dict.**

  ```python
  {k: d2[k] for k in d1.keys() & d2.keys()}
  ```

  ```text
  values from d2 : {'b': 99, 'c': 100}
  ```

  No error, and the keys are right, so a glance says it works. The brief says
  "with values taken from the **first** dict", and that emphasis is in the
  original. Whenever two structures share keys, say out loud which one the
  values come from before you type the line.
- **`&` on the dicts themselves.**

  ```python
  d1 & d2
  ```

  ```text
  Traceback (most recent call last):
    File "week-05-solutions.py", line 7, in <module>
      d1 & d2
      ~~~^~~~
  TypeError: unsupported operand type(s) for &: 'dict' and 'dict'
  ```

  Dicts support `|` for merging, since Python 3.9, but **not** `&`. The set
  operators live on the *views*, not on the mapping itself:
  `d1.keys() & d2.keys()`. This trips people who learned `|` and reasonably
  assumed the family was symmetric — but `|` on dicts means merge rather than
  union-of-keys, so it never was.
- **`items() & items()` when the values differ.**

  ```python
  d1.items() & d2.items()
  ```

  ```text
  set()
  ```

  Empty, silently. The items view is a set of `(key, value)` **pairs**, so it
  only matches entries where the key *and* the value are equal — and here
  `d1["b"]` is `2` while `d2["b"]` is `99`. It also raises
  `TypeError: unhashable type` outright if any value is a list. Items-view set
  operations answer "which entries are identical in both dicts?", which is a
  different question from the one asked.
- **`if key in d2.values()`.** Wrong container and slow with it. A values view
  has no hashing behind it, so `in` walks the lot. This one usually comes from
  typing on autopilot; the fix is to read the line back and ask "am I testing a
  key or a value?".
- **Deleting from `d1` instead of building a new dict.**

  ```python
  for key in list(d1):
      if key not in d2:
          del d1[key]
  return d1
  ```

  It returns the right answer and destroys the caller's dict on the way. Note
  also the `list(d1)` — without it, deleting while iterating raises
  `RuntimeError: dictionary changed size during iteration`, which at least tells
  you something is wrong. The version above silences the warning and keeps the
  bug.

## Under the hood

<details>
<summary>Under the hood — dict views, and why they are not lists of your keys</summary>

`d.keys()`, `d.values()` and `d.items()` do not build anything. They hand back a
**view**: a small object that knows which dict to look at and answers questions
by looking at it right now.

That has one consequence you will meet, and it surprises everybody once:

```python
>>> d = {"a": 1}
>>> keys = d.keys()
>>> d["b"] = 2
>>> keys
dict_keys(['a', 'b'])
```

`keys` was made before `"b"` existed and it knows about `"b"` anyway, because it
never copied anything. It is a window, not a photograph.

The upside is that it is free. `for key in d.keys()` on a million-key dict
allocates nothing at all, where `for key in list(d.keys())` builds a
million-item list first. That is why plain `key in d2` is the idiom — it goes
through the same machinery with less typing.

The downside is that you cannot change the dict while you are looking through
the window:

```python
>>> d = {"a": 1, "b": 2}
>>> for key in d:
...     if key == "a":
...         del d[key]
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: dictionary changed size during iteration
```

`list(d)` takes the photograph, and then deleting is safe. Note that a **list**
does not protect you this way — removing items from a list while looping over it
silently skips things instead of raising, which is the mini-project's third
common wrong turn.

**Why the keys view supports set operators.** Keys are unique and hashable,
which is the definition of a set's contents, so a keys view really is a set in
everything but name — and Python makes that official by giving it `&`, `|`, `-`
and `^`:

```python
>>> a = {"x": 1, "y": 2}
>>> b = {"y": 0, "z": 0}
>>> a.keys() & b.keys()
{'y'}
>>> a.keys() | b.keys()
{'x', 'y', 'z'}
>>> a.keys() - b.keys()
{'x'}
>>> a.keys() ^ b.keys()
{'x', 'z'}
```

Four one-line answers to four questions that would otherwise be four loops:
shared, either, only-mine, exactly-one-of-us. Reconciling two sources of data is
mostly these four operators.

**Values views get none of that**, because values are neither unique nor
necessarily hashable — `{"a": 1, "b": 1}.values()` has two members that are the
same, so it cannot be a set. `in` on a values view therefore walks the whole
thing.

**Items views are the interesting middle case.** A `(key, value)` pair is
unique, so an items view can be a set — but only if the values are hashable:

```python
>>> {"a": 1}.items() & {"a": 1}.items()
{('a', 1)}
>>> {"a": [1]}.items() & {"a": [1]}.items()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

Which is the same hashability rule from Problem 2, arriving from a new
direction.

</details>

<details>
<summary>Under the hood — the four ways two dicts can disagree, and the shape of a reconcile</summary>

"Which keys do these two share" is one question out of four, and in real work
you almost always want all four at once. Comparing yesterday's inventory with
today's, or a config file with its defaults, or a database table with a CSV
export — the shape is always the same.

```python
>>> old = {"a": 1, "b": 2, "c": 3}
>>> new = {"b": 2, "c": 30, "d": 4}
>>> removed = old.keys() - new.keys()
>>> added = new.keys() - old.keys()
>>> shared = old.keys() & new.keys()
>>> changed = {k for k in shared if old[k] != new[k]}
>>> removed, added, shared, changed
({'a'}, {'d'}, {'b', 'c'}, {'c'})
```

Four sets, four lines, and every one of them is a set operation on keys except
the last, which is the only one that has to look at values at all.

Three things in that snippet are worth taking away.

**`shared` is computed once and reused.** `changed` is a filter over `shared`,
not a fresh comparison of both dicts. Naming the intermediate result stops you
recomputing it and, more importantly, stops the two computations drifting apart
when somebody edits one of them.

**`changed` needs `old[k] != new[k]`, and that is the only value comparison in
the whole thing.** Everything else is key algebra. When a reconcile feels
complicated, it is usually because values are being compared where keys would
do.

**The four sets are exhaustive and do not overlap** — every key of either dict
is in exactly one of removed, added, or shared, and `changed` is a subset of
shared. That is a property worth asserting in a test:
`len(removed) + len(added) + len(shared) == len(old.keys() | new.keys())`.

`intersect_dicts` is the `shared` line, wrapped up with the values attached.
Once you see it as one quarter of a reconcile, the "which dict do the values
come from" question stops being pedantry: in a reconcile the answer is
*sometimes both*, and a function that quietly picks one would be hiding the
thing you were trying to look at.

One caution about `!=` on values. It compares by equality, so `1` and `1.0`
count as unchanged, and two dicts that are equal but ordered differently also
count as unchanged. That is usually what you want. When it is not — when you
care that the type changed from `int` to `float` — you need
`type(a) is type(b) and a == b`, and you should write down why.

</details>

## Acceptance checklist

- [ ] `intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4})`
      gives `{'b': 2, 'c': 3}`.
- [ ] `intersect_dicts({}, {"a": 1})` gives `{}`.
- [ ] `intersect_dicts({"a": 1}, {})` gives `{}`.
- [ ] `intersect_dicts({"x": 1}, {"x": 1})` gives `{'x': 1}`.
- [ ] Every value in the answer came from the first dict.
- [ ] The keys come out in the first dict's order.
- [ ] Both input dicts are unchanged afterwards.
- [ ] There is no nested loop and no `in d2.values()`.
- [ ] The signature has type hints and the function has a docstring.
- [ ] Committed with a message like `Week 5 homework: intersect dictionaries`.
- [ ] All six problems live in one `week-05-solutions.py` that runs clean.

## Stretch

- **Write the other three quarters.** Add `only_in_first(d1, d2)`,
  `only_in_second(d1, d2)` and `changed_values(d1, d2)`. Each is one line of key
  algebra, and together with this problem they are a complete reconcile — the
  shape in the second *Under the hood* block. Assert that the four results
  partition every key in `d1.keys() | d2.keys()`.
- **Let the caller choose the winner.** Add a keyword-only parameter:
  `intersect_dicts(d1, d2, *, values_from="first")`. The bare `*` forces it to
  be passed by name, so it can never be mistaken for a third dict. Then decide
  whether the parameter is an improvement or whether two clearly named functions
  would read better at the call site.
- **Intersect any number of dicts.** `intersect_all(*dicts)` should keep the
  keys present in every one of them, with values from the first. Sort out the
  no-arguments case before you write the loop —
  `functools.reduce` with a starting value makes this pleasant, and the empty
  case is where most attempts fall over.
- **Compare with the nested-loop version.** Write the `for k1 in d1: for k2 in
  d2:` version, check it gives the same answers, then time both with `timeit`
  on two dicts of 2,000 keys. Double both sizes and run again: one time roughly
  doubles, the other roughly quadruples.
- **Intersect on values instead of keys.** Return the pairs where both dicts
  agree on the key *and* the value — which is exactly `d1.items() & d2.items()`
  when the values are hashable. Then write the version that works when they are
  not, and notice you are back to a comprehension with an explicit comparison in
  it.

That is the last problem of Week 5. Back to the
[homework index](./README.md), or on to the week's capstone, the
[Contact Book Manager](../mini-project/README.md).
