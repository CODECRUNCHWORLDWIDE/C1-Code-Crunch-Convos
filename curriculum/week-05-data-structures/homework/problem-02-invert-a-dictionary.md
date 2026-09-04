# Homework Problem 2 — Invert a dictionary

> **Topic:** dict comprehensions, tuple unpacking over `.items()`, and what it costs when two keys share a value
> **Lecture:** [02 — Sets and Dictionaries](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Easy
> **Target time:** 25 minutes
> **Why this one:** the code is one line, and the interesting part is entirely in the two words the brief attaches to it — "unique and hashable". Break either one and Python behaves differently: one of them raises immediately, the other loses your data without a sound. Knowing which is which is worth more than the line.

## The Brief

A dictionary maps keys to values. A phone book maps names to numbers:

```python
{"red": 1, "green": 2, "blue": 3}
```

Sometimes you have it the wrong way round. You have colours pointing at numbers
and what you needed was numbers pointing at colours. **Inverting** a dict means
building a new one where every key becomes a value and every value becomes a
key.

```python
invert({"red": 1, "green": 2, "blue": 3})
# {1: "red", 2: "green", 3: "blue"}
```

Write one function.

```python
def invert(d: dict) -> dict:
    ...
```

The brief hands you two promises about the input, and both of them are load
bearing:

- The values are **hashable**, which means each one is allowed to be used as a
  dict key. Numbers, strings and tuples are. Lists are not.
- The values are **unique**, meaning no two keys share one. Dict keys have to be
  unique, so if two of them shared a value, one of the pairs would have nowhere
  to go.

Build it with a **dict comprehension** — the `{key: value for ...}` form. It is
one expression, so the whole function can be a single `return`.

## Starter

Save this in your `homework/` folder as part of `week-05-solutions.py` and fill
in the `TODO`. It runs as pasted — it just gives back an empty dict:

```python
"""Week 5 homework, problem 2: swap a dict's keys with its values."""


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
    # TODO: one dict comprehension over d.items(), writing the pair back
    #       the other way round.
    return {}


def _demo() -> None:
    """Print the brief's example and the empty case."""
    print(invert({"red": 1, "green": 2, "blue": 3}))
    print(invert({}))


if __name__ == "__main__":
    _demo()
```

Before you write the comprehension, run this once so you can see what you are
looping over:

```python
print(list({"red": 1, "green": 2}.items()))
```

```text
[('red', 1), ('green', 2)]
```

Pairs. Not keys, not values — pairs.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/homework/problem-02-invert-a-dictionary.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `invert(d)` returns a new dict whose keys are `d`'s values and whose values
   are `d`'s keys.
2. `invert({})` returns `{}`.
3. The input dict is not changed.
4. The body is a dict comprehension.
5. Type hints on the signature and a docstring on the function.
6. These three asserts pass:

   ```python
   assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}
   assert invert({}) == {}
   assert invert({"x": "X", "y": "Y"}) == {"X": "x", "Y": "y"}
   ```

## Constraints

- **Loop over `.items()`, not over the dict itself.** Iterating a dict gives you
  its **keys** and nothing else. `.items()` is what hands you both halves.
- **Write it as a comprehension, not as a loop with an accumulator.** When the
  entire body of a function is "build a container from an iterable, with no
  branching", the comprehension form is the one to reach for. No `result = {}`,
  no `result[v] = k`, no final `return result`.
- **Do not try to be clever about repeated values.** The brief promises they are
  unique. Handling the other case is a different function with a different
  return type, and it is waiting for you under *Stretch*.
- **Do not convert unhashable values to make them fit.** If a value is a list,
  the honest response is the `TypeError`, not a silent `tuple()` behind the
  caller's back.
- **`_demo` prints; `invert` does not.**

## Expected output

```text
$ python problem-02-invert-a-dictionary.py
{1: 'red', 2: 'green', 3: 'blue'}
{}
{'X': 'x', 'Y': 'y'}
{1: 'b'}
All 5 asserts passed.
```

The first three lines are the brief's example and two of the required asserts.

The fourth line is the one to stare at. That is `invert({"a": 1, "b": 1})` —
two keys sharing a value, which the brief said would not happen. Look at what
came back: **one pair, not two.** No exception, no warning, no note in the log.
The `"a"` was written first and then flattened by `"b"`, and the only evidence
is that the output is shorter than the input.

Check the input survived:

```bash
python -c "from week_05_solutions import invert; d={'a':1}; invert(d); print(d)"
```

```text
{'a': 1}
```

## Steps

1. Save the Starter into `week-05-solutions.py` and run it. Two empty dicts.
2. Print `list(d.items())` for the brief's example and look at the pairs.
3. Write the comprehension. The `for` clause unpacks each pair into two names,
   and the expression in front writes them back the other way round:

   ```python
   {value: key for key, value in d.items()}
   ```

   Say the two halves out loud in the order they run: "for each key and value,
   store the value pointing at the key".
4. Run it. The first line should be `{1: 'red', 2: 'green', 3: 'blue'}`.
5. Add the three required asserts.
6. Now break it on purpose, twice, and read both messages:

   ```python
   print(invert({"a": [1, 2]}))
   print(invert({"a": 1, "b": 1}))
   ```

   The first one raises. The second one does not, and that is the more
   dangerous of the two. Add
   `assert invert({"a": 1, "b": 1}) == {1: "b"}` so the behaviour is written
   down rather than discovered later.
7. Compare with **The Solution**, tick the acceptance checklist, and commit:
   `git commit -m "Week 5 homework: invert a dictionary"`.

## The Solution

```python
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
```

**Why it works.**

**`.items()` yields pairs, and the `for` clause takes them apart.**
`for key, value in d.items()` is the tuple unpacking from
[lecture 01](../lecture-notes/01-lists-and-tuples.md#packing-and-unpacking): each
pair arrives as a two-item tuple and the two names on the left catch its two
halves. Then `{value: key ...}` writes them back in the opposite order. One
unpack, one re-pack, and that is the entire function.

**Why "hashable" is in the brief.** The values are about to become keys, and
only a hashable object can be a key. Hand `invert` a list value and it raises on
the spot — see *Common bugs to catch* for the exact message, and the first
*Under the hood* block for what "hashable" actually means.

**Why "unique" is in the brief, and why this half is worse.** Keys are unique by
definition. If two input keys share a value, the second write lands on the same
key as the first and replaces it. Nothing raises. The output is simply one pair
shorter than the input:

```python
>>> invert({"a": 1, "b": 1})
{1: 'b'}
```

Silent loss is worse than a crash. A crash tells you where and when; this tells
you nothing, and the shortfall is discovered by somebody else, later, looking at
a report with a missing row. That is the entire reason the *Stretch* version
exists.

**Insertion order survives.** The comprehension writes in `items()` order, and
since Python 3.7 a dict keeps its keys in the order they were first inserted. So
the brief's example prints `1, 2, 3` rather than something scrambled. Your
asserts do not depend on this, because `==` on dicts ignores order — but your
printed output does, and so does anybody reading it.

**Notice what is not in the function.** No `result = {}`. No loop counter. No
`result[value] = key`. No final `return result`. A dict comprehension is a
single expression, so it can be returned directly, and four lines of bookkeeping
that could each have a typo in them never get written.

## Run it

Copy the worked answer on this page into `problem-02-invert-a-dictionary.py` and run it:
and run it:

```bash
python problem-02-invert-a-dictionary.py
```

Your own copy of `invert` belongs in `week-05-solutions.py`, and that is the
file you commit. The longer download name keeps the published answer from
landing on top of your work.

## Common bugs to catch

- **A value that cannot be a key.**

  ```python
  invert({"a": [1, 2]})
  ```

  ```text
  Traceback (most recent call last):
    File "week-05-solutions.py", line 3, in <module>
      print(invert({"a": [1, 2]}))
            ~~~~~~^^^^^^^^^^^^^^^
    File "week-05-solutions.py", line 2, in invert
      return {v: k for k, v in d.items()}
              ^^^^
  TypeError: unhashable type: 'list'
  ```

  The squiggle sits on `v: k` — the **key** half of the pair. Python is telling
  you the thing being used as a key is the problem, which is the value you
  handed in. If your values really are lists, `tuple(v)` makes them hashable, or
  the *Stretch* version keeps them as they are.
- **Iterating the dict instead of `.items()`.**

  ```python
  {v: k for k, v in d}
  ```

  ```text
  ValueError: too many values to unpack (expected 2)
  ```

  Iterating a dict yields **keys**. With three-letter keys Python tries to
  unpack `"red"` into `k, v` and complains about the length. The nasty case is
  two-character keys, where the unpack *succeeds* and you get a dict built out
  of individual letters. Say `.items()` whenever you want both halves.
- **Forgetting the swap.**

  ```python
  out = {}
  for k, v in d.items():
      out[k] = v          # this just copies the dict
  ```

  No error, and every assert fails with a bare `AssertionError` that names no
  values. If your failing assert has the *input* on its right-hand side, look for
  a missing swap before you look anywhere else.
- **Assuming `invert(invert(d)) == d`.** It holds only when the values are
  unique. `invert(invert({"a": 1, "b": 1}))` is `{"b": 1}`, not the original.
  Round-trip properties make excellent tests, so check that yours actually holds
  before you assert it.
- **Sorting the result to "fix" the order.** `dict(sorted(...))` changes what
  you print but not what the dict means, and it throws away the input order that
  the comprehension preserved for free. If order matters to a caller, that is
  worth a sentence in the docstring, not a silent sort.

## Under the hood

<details>
<summary>Under the hood — what hashable means, and why a list can never be a key</summary>

A dict does not search for your key. It **computes where the key should live**
and looks there. That computation is the hash: a function that turns an object
into a number.

```python
>>> hash("red")
-4074087700889260410
>>> hash(1)
1
>>> hash((1, 2))
-3550055125485641917
```

That number decides which slot of the dict's internal table the pair goes in.
Storing and finding are both "compute the number, go to that slot", which is why
a dict lookup costs the same whether the dict holds ten pairs or ten million.

Everything about hashing rests on one promise: **an object's hash must never
change while it is being used as a key.** If it changed, the pair would still be
sitting in the old slot while every future lookup went to the new one, and the
value would be lost inside its own dictionary.

That promise is impossible for a mutable object to keep. So Python does not let
you make one:

```python
>>> {[1, 2]: "nope"}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

A list can grow, shrink and be reordered, all in place, all while sitting inside
a dict. Its hash would have to change with its contents, and then it would be
lost. Rather than let that happen quietly, `list` simply has no working hash —
that is all "unhashable" means.

The tuple is the same data with the mutability taken away, so it hashes:

```python
>>> hash((1, 2))
-3550055125485641917
>>> {(1, 2): "fine"}
{(1, 2): 'fine'}
```

But only if everything inside it is hashable too, because a tuple's hash is
built from its items' hashes:

```python
>>> hash((1, [2]))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

"Immutable" is not quite the same as "hashable" — it is closer to "immutable all
the way down".

The same rule governs sets, which are dicts without the values. It is why
`set()` refuses a list and accepts a tuple, and it is the rule behind Challenge
01's anagram grouper, where a sorted string is used as a key precisely because a
string cannot change underneath the dict.

Two hashable objects that are `==` must have the same hash, which is why
`hash(1) == hash(1.0)` and why `{1: "a", 1.0: "b"}` is a dict with **one** pair
in it. `invert({"a": 1, "b": 1.0})` collapses for the same reason your repeated
value did.

</details>

<details>
<summary>Under the hood — the boundary between a comprehension and a loop</summary>

`invert` is a comprehension. The `invert_multi` in *Stretch* cannot be, and the
reason is a genuinely useful rule rather than a quirk.

**A comprehension builds each entry independently.** It walks an iterable and
produces one result per item, and nothing it produces can look at anything it
produced earlier. That is what makes it an expression you can read in one go: no
state, no order dependence, nothing accumulating off to the side.

`invert` fits perfectly. Each `(key, value)` pair becomes exactly one output
pair, and no pair needs to know about any other.

Grouping does not fit. To put `"b"` into the list that already contains `"a"`,
the code has to reach into an entry it made on a previous turn and change it.
That is **accumulation**, and a comprehension has no way to express it.

The rule, in six words: **comprehensions map, loops accumulate.**

Reaching for a loop when you are accumulating is not a failure of style. It is
reading the problem correctly. The failure of style is contorting a
comprehension until it can accumulate — usually by calling a mutating method
inside it for its side effect:

```python
out = {}
[out.setdefault(v, []).append(k) for k, v in d.items()]     # do not do this
```

That works, and it is worse than the loop in three ways at once. It builds and
throws away a list of `None`s, one per item, purely as litter. It hides a
mutation inside something that reads like an expression. And it puts the effect
you care about in a place a reader does not look for effects. If you are only
running the comprehension for what it does rather than for what it returns, you
wanted a `for` loop and should write one.

There is one honourable middle case: a **generator expression** looks like a
comprehension but produces items lazily, one at a time. It maps too — it just
does not build the container. Problem 4 uses one inside `sorted`.

</details>

## Acceptance checklist

- [ ] `invert({"a": 1, "b": 2})` gives `{1: 'a', 2: 'b'}`.
- [ ] `invert({})` gives `{}`.
- [ ] `invert({"x": "X", "y": "Y"})` gives `{'X': 'x', 'Y': 'y'}`.
- [ ] The body is a dict comprehension over `.items()`.
- [ ] The dict you passed in is unchanged afterwards.
- [ ] `invert({"a": [1, 2]})` raises `TypeError: unhashable type: 'list'` and
      you can say why.
- [ ] `invert({"a": 1, "b": 1})` gives `{1: 'b'}`, and there is an assert saying
      so.
- [ ] The signature has type hints and the function has a docstring.
- [ ] Committed with a message like `Week 5 homework: invert a dictionary`.

## Stretch

- **Handle values that repeat.** This is the brief's own stretch. Write
  `invert_multi(d) -> dict` so that every value maps to the **list** of keys
  that had it, and nothing is ever lost:

  ```python
  def invert_multi(d: dict) -> dict:
      """Values need not be unique; each maps to the list of keys that had it."""
      out: dict = {}
      for key, value in d.items():
          out.setdefault(value, []).append(key)
      return out
  ```

  ```python
  >>> invert_multi({"a": 1, "b": 1, "c": 2})
  {1: ['a', 'b'], 2: ['c']}
  ```

  Two things changed and only one is obvious. The value type became a list, so a
  repeated value appends instead of replacing — `setdefault` hands back the list
  already stored under `value`, or puts a fresh one there and hands back that,
  and `.append` changes it where it lives. The non-obvious change is that **it
  stopped being a comprehension**, for the reason in the second *Under the hood*
  block. `collections.defaultdict(list)` shortens the body to
  `out[value].append(key)` at the price of returning a `defaultdict`; wrap it in
  `dict(...)` if callers care.
- **Assert that nothing is lost.** For any `d`,
  `sum(len(v) for v in invert_multi(d).values()) == len(d)`. That invariant says
  "every input pair is still in there somewhere" in one line, and it is a far
  better test than any single example.
- **Detect the collision instead of absorbing it.** Write `invert_strict` that
  raises `ValueError` naming the repeated value when two keys share one. Then
  argue with yourself about which of the three behaviours — overwrite, collect,
  raise — you would want if this were reading a file somebody else edited.
- **Invert a dict of lists.** Given `{"a": [1, 2], "b": [2, 3]}`, produce
  `{1: ["a"], 2: ["a", "b"], 3: ["b"]}`. The values are unhashable but the
  things *inside* them are not, so the loop gains one more level. This is the
  shape behind every search index you have ever used.
- **Time it against a plain loop.** Use `timeit` on a dict of 100,000 pairs to
  compare the comprehension with the accumulate-into-a-dict version. Both are
  linear, so expect a modest constant-factor win rather than a different curve —
  and note that "modest" is the honest word here. Choose the comprehension for
  what it does to the reader, not for the microseconds.

Next: [Homework Problem 3 — Two-Sum (classic)](./problem-03-two-sum-classic.md).
