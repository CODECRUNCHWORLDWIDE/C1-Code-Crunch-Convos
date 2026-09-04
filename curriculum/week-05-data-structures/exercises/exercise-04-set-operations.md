# Exercise 4 — Set Operations

> **Topic:** union, intersection, difference, symmetric difference, and the subset test
> **Lecture:** [02 — Sets and Dicts](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** "which of these are in both", "what is missing", "have we covered everything" are questions you will answer in code hundreds of times. Done with lists they take loops inside loops and can hand you the same answer twice. Done with sets they are **one operator each**, and the operator says what you meant. Once you can see the four operators, you stop writing the loops.

## The Brief

Two study circles meet each week — one in the morning, one in the evening —
and each keeps a list of the topics it has covered. Before planning next term
the organisers need four answers and one yes-or-no:

- What has the community covered **between them**?
- What have **both** circles already done?
- What has **only one** circle seen? (And which one — that question has two
  different answers depending on which way round you ask it.)
- Is the required core list **fully covered** by each circle on its own?

Every one of those is a set operation. A **set** is a bag that holds each
thing at most once and does not remember what order they went in — you met one
in Exercise 2, where you used it to answer "have I seen this?". Today you use
the other half of what a set is for: comparing two whole bags at once.

Write the five functions that answer the questions, and write them so they do
not quietly change the rosters they were handed. That last point matters more
than it sounds: `|` and `|=` look nearly identical and do very different
things to the caller's data.

## Starter

Create `exercise-04-set-operations.py` in your practice repo and paste this
in. Fill in every `TODO`. Every body is one line.

```python
"""exercise-04-set-operations.py — the coverage report.

Answer coverage questions with set operations instead of nested loops,
returning new sets rather than changing the ones you were given.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
MORNING: set[str] = {"lists", "tuples", "slicing", "dicts", "big-o"}
EVENING: set[str] = {"dicts", "sets", "comprehensions", "big-o", "slicing"}
REQUIRED: set[str] = {"lists", "dicts", "big-o"}


# ---- Your task ----
def covered_by_either(a: set[str], b: set[str]) -> set[str]:
    """Return every topic covered by at least one circle.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding the topics in a, in b, or in both.
    """
    # TODO: union
    ...


def covered_by_both(a: set[str], b: set[str]) -> set[str]:
    """Return the topics covered by both circles.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding only the topics that appear in both.
    """
    # TODO: intersection
    ...


def only_in_first(a: set[str], b: set[str]) -> set[str]:
    """Return the topics in `a` that `b` has not covered.

    Swapping the arguments gives a different answer.

    Args:
        a: The circle being reported on.
        b: The circle being compared against.

    Returns:
        A new set holding the topics in a and not in b.
    """
    # TODO: difference -- this one is NOT symmetric
    ...


def covered_exactly_once(a: set[str], b: set[str]) -> set[str]:
    """Return the topics covered by exactly one of the two circles.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding the topics in one circle but not the other.
    """
    # TODO: symmetric difference
    ...


def is_fully_covered(required: set[str], covered: set[str]) -> bool:
    """Return True if every required topic appears in `covered`.

    Args:
        required: The core topics that must be taught.
        covered: What one circle has actually taught.

    Returns:
        True when nothing required is outstanding, otherwise False.
    """
    # TODO: subset test -- return a real bool, not a set
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"{'either:':<15}{len(covered_by_either(MORNING, EVENING))} topics")
    print(f"{'both:':<15}{', '.join(sorted(covered_by_both(MORNING, EVENING)))}")
    print(f"{'morning only:':<15}{', '.join(sorted(only_in_first(MORNING, EVENING)))}")
    print(f"{'evening only:':<15}{', '.join(sorted(only_in_first(EVENING, MORNING)))}")
    print(f"{'exactly once:':<15}{len(covered_exactly_once(MORNING, EVENING))} topics")

    assert covered_by_either(MORNING, EVENING) == {
        "lists", "tuples", "slicing", "dicts", "big-o", "sets", "comprehensions",
    }
    assert covered_by_both(MORNING, EVENING) == {"slicing", "dicts", "big-o"}
    assert only_in_first(MORNING, EVENING) == {"lists", "tuples"}
    assert only_in_first(EVENING, MORNING) == {"sets", "comprehensions"}
    assert covered_exactly_once(MORNING, EVENING) == {
        "lists", "tuples", "sets", "comprehensions",
    }
    assert is_fully_covered(REQUIRED, MORNING) is True
    assert is_fully_covered(REQUIRED, EVENING) is False
    assert len(MORNING) == 5 and len(EVENING) == 5  # inputs untouched
    print("All checks passed.")
```

The five operators, each as one English sentence.

| You write | It means | Called |
|---|---|---|
| `a \| b` | in `a`, or in `b`, or in both | union |
| `a & b` | in `a` **and** in `b` | intersection |
| `a - b` | in `a` but **not** in `b` | difference |
| `a ^ b` | in one of them but **not** both | symmetric difference |
| `a <= b` | everything in `a` is also in `b` | subset test |

Two more words.

**Symmetric.** An operation is symmetric when swapping the two sides gives the
same answer. `|`, `&` and `^` are symmetric. `-` is not, and neither is `<=`.

**In place.** `a |= b` does *not* build a new set. It changes `a` itself,
right where it sits, and everyone else holding that same set sees the change.
All four operators have an in-place twin — `|=`, `&=`, `-=`, `^=` — and this
page bans all of them.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/exercises/exercise-04-set-operations.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Each of the first four functions returns a **new** `set`. `MORNING` and
   `EVENING` still have five members each when the file finishes.
2. `only_in_first` is directional: swapping the arguments gives a different
   answer, and both directions are asserted.
3. `is_fully_covered` returns a real `bool`. The asserts use `is True` and
   `is False`, so a truthy set or a `1` will not pass.
4. The union has 7 members, the intersection 3, each difference 2, the
   symmetric difference 4.
5. Everything printed goes through `sorted(...)`, so the output is identical
   on every run and every machine.
6. Every function keeps its type hints and its docstring, and every body is a
   single expression.

## Constraints

- **Use the operators. No loops, no comprehensions.** `[x for x in a if x in
  b]` gets the right topics here and it is the wrong answer in two ways. It
  hands you a **list**, and a list never equals a set no matter what is in it,
  so the assert fails. And the moment `b` arrives from a file as a list rather
  than a set, `x in b` starts reading through `b` for every single item of
  `a`, and a one-pass job becomes a read-through-per-item job.

- **`a & b` costs about as much as walking the smaller of the two sets.**
  Python takes the smaller side, walks it once, and asks the bigger side "have
  you got this?" — and a set answers that question without reading through
  itself, for the reason Exercise 2's *Under the hood* explains. So the cost
  is the size of the smaller set, not the two sizes multiplied together. That
  multiplication is exactly what the list version costs.

- **Return new sets. Never `|=`, `&=`, `-=`, `^=` or `.update()`.** The
  in-place forms rewrite the caller's set. You were handed the organisers'
  live rosters, so changing one while computing a report is a bug that shows
  up three functions later, in a completely different answer. That is what the
  `len(MORNING) == 5` assert guards.

- **Sort before you print. Never sort before you compare.** Set order is
  undefined and, for strings, deliberately scrambled differently on every run
  of Python, so printing a raw set gives output that changes between runs. But
  compare sets to sets in your asserts: `{"a", "b"} == {"b", "a"}` is `True`,
  which is the whole point of a set, and sorting first just adds work to reach
  an answer you already had.

- **Use `<=` or `.issubset()` for coverage, never arithmetic on `len()`.**
  Comparing sizes tells you the two bags are the same size, not that they hold
  the same things. Two three-member sets with nothing in common pass a length
  check with flying colours.

- **Do not convert to lists.** Once a set becomes a list, `in` goes back to
  reading through everything, and duplicates become possible again. The only
  list on this page should be the one `sorted()` hands to `", ".join(...)`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-set-operations.py
either:        7 topics
both:          big-o, dicts, slicing
morning only:  lists, tuples
evening only:  comprehensions, sets
exactly once:  4 topics
All checks passed.
```

Read the two "only" lines together, then the last line. Four topics are
covered by exactly one circle: two on the morning side, two on the evening
side. That is what `^` means — the symmetric difference is precisely the two
differences added together. Seeing it laid out beats memorising a definition.

## Steps

1. Create `exercise-04-set-operations.py` and paste the starter in.
2. Work the answers out **on paper first**. Five topics each, three shared.
   You should be able to predict all four result sets before you write a line
   of code, and if you cannot, the code will not teach you.
3. In a REPL, paste the two sets and try `MORNING | EVENING`,
   `MORNING & EVENING`, both differences, and `MORNING ^ EVENING`. Compare
   each one to your paper answer.
4. In that same REPL, run `MORNING.update(EVENING)` and then look at
   `MORNING`. That is the mutation the constraints warn about, and seeing it
   once is worth more than reading about it three times. Restart the REPL
   afterwards.
5. Fill in the five functions. Each body is one line.
6. Run the file and check the printed block against the expected output. Then
   add a topic to `EVENING` and predict all five lines before running again.
   Getting all five right means you have the operators.

## The Solution

```python
"""exercise-04-set-operations-solution.py — the coverage report.

Five questions the organisers ask in English, five set operations that mean
exactly those questions. Every body is one expression, and none of them
changes the rosters it was handed.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
MORNING: set[str] = {"lists", "tuples", "slicing", "dicts", "big-o"}
EVENING: set[str] = {"dicts", "sets", "comprehensions", "big-o", "slicing"}
REQUIRED: set[str] = {"lists", "dicts", "big-o"}


# ---- Your task ----
def covered_by_either(a: set[str], b: set[str]) -> set[str]:
    """Return every topic covered by at least one circle.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding the topics in a, in b, or in both.
    """
    return a | b


def covered_by_both(a: set[str], b: set[str]) -> set[str]:
    """Return the topics covered by both circles.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding only the topics that appear in both.
    """
    return a & b


def only_in_first(a: set[str], b: set[str]) -> set[str]:
    """Return the topics in `a` that `b` has not covered.

    Swapping the arguments gives a different answer.

    Args:
        a: The circle being reported on.
        b: The circle being compared against.

    Returns:
        A new set holding the topics in a and not in b.
    """
    return a - b


def covered_exactly_once(a: set[str], b: set[str]) -> set[str]:
    """Return the topics covered by exactly one of the two circles.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding the topics in one circle but not the other.
    """
    return a ^ b


def is_fully_covered(required: set[str], covered: set[str]) -> bool:
    """Return True if every required topic appears in `covered`.

    Args:
        required: The core topics that must be taught.
        covered: What one circle has actually taught.

    Returns:
        True when nothing required is outstanding, otherwise False.
    """
    return required <= covered


# ---- Self-check ----
if __name__ == "__main__":
    print(f"{'either:':<15}{len(covered_by_either(MORNING, EVENING))} topics")
    print(f"{'both:':<15}{', '.join(sorted(covered_by_both(MORNING, EVENING)))}")
    print(f"{'morning only:':<15}{', '.join(sorted(only_in_first(MORNING, EVENING)))}")
    print(f"{'evening only:':<15}{', '.join(sorted(only_in_first(EVENING, MORNING)))}")
    print(f"{'exactly once:':<15}{len(covered_exactly_once(MORNING, EVENING))} topics")

    assert covered_by_either(MORNING, EVENING) == {
        "lists", "tuples", "slicing", "dicts", "big-o", "sets", "comprehensions",
    }
    assert covered_by_both(MORNING, EVENING) == {"slicing", "dicts", "big-o"}
    assert only_in_first(MORNING, EVENING) == {"lists", "tuples"}
    assert only_in_first(EVENING, MORNING) == {"sets", "comprehensions"}
    assert covered_exactly_once(MORNING, EVENING) == {
        "lists", "tuples", "sets", "comprehensions",
    }
    assert is_fully_covered(REQUIRED, MORNING) is True
    assert is_fully_covered(REQUIRED, EVENING) is False
    assert len(MORNING) == 5 and len(EVENING) == 5  # inputs untouched
    print("All checks passed.")
```

**Each operator is a sentence, so the five functions are transcription rather
than programming.** `|` is "or". `&` is "and". `-` is "but not". `^` is "one
or the other, not both". `<=` is "is contained in". The docstring states the
question and the operator answers it, with nothing in between for a bug to
hide in.

**The one to be careful with is `-`.** Union and intersection are symmetric,
so argument order cannot catch you out. Difference is not. `MORNING - EVENING`
is `{"lists", "tuples"}` and `EVENING - MORNING` is
`{"sets", "comprehensions"}`, and the self-check asserts both directions for
exactly that reason. The docstring wording — "the topics in `a` that `b` has
not covered" — is load-bearing.

**`^` is the two differences added together**, which the printed report shows
you: two morning-only topics plus two evening-only topics is the four topics
covered exactly once.

**Cost.** All four operators walk the smaller set once and ask the bigger set
one instant question per item, so each costs about the size of the two sets
added together — never multiplied. `required <= covered` is cheaper still: it
walks the required topics and **stops at the first one missing**. Nothing here
reads anything twice.

The version the constraints forbid does:

```python
def covered_by_both(a, b):
    return [x for x in a if x in b]
```

If `b` is a set, that costs the same and merely returns the wrong type. If `b`
is a list — and it will be, the first time this code meets data from a file —
`x in b` reads through `b` for every item in `a`. It can also return the same
topic twice, because a list can hold duplicates and a set cannot. That last
property is the one worth wanting: not "I remembered to deduplicate" but
"there is no way for this to contain a duplicate".

**`|` versus `|=` is the entire reason for the last assert.** The in-place
forms modify the left-hand set instead of building a new one. A report
function that grows `MORNING` by five topics has corrupted the data every
later question depends on, and the bug surfaces in a *different* function,
which is the worst possible place to find it.

**`is_fully_covered` must return a real `bool`.** `required <= covered`
evaluates to `True` or `False`, which is why the assert can say `is True`.
That is stricter than `== True`: `is` asks whether this is the one and only
`True` object, so a truthy set, a `1`, or a non-empty string all fail it. The
assert is written that way on purpose, because "returns something truthy" and
"returns a boolean" are different promises, and the second one is what a
function named `is_...` is making.

## Run it

Copy the worked answer on this page into `exercise-04-set-operations.py` and run it:

```bash
python exercise-04-set-operations.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-04-set-operations.py`.

## Common bugs to catch

- **One function used `|=`, and four other answers went wrong.** This is the
  most instructive failure on the page:

  ```text
  either:        7 topics
  both:          big-o, comprehensions, dicts, sets, slicing
  morning only:  lists, tuples
  evening only:
  exactly once:  2 topics
  Traceback (most recent call last):
      assert covered_by_both(MORNING, EVENING) == {"slicing", "dicts", "big-o"}
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Look at *where* it broke. `covered_by_either` returned the right answer and
  printed `7 topics`. The failure is in `covered_by_both`, the **next**
  function, which now finds five shared topics because `MORNING` has swallowed
  `EVENING`. `evening only:` is empty for the same reason. One function
  corrupted the data; four other functions produced wrong answers. That is why
  "return a new value" is a habit and not a preference — the cost of the
  in-place version is always paid somewhere else.

- **`is_fully_covered` fails the `is True` assert although the logic looks
  right.** You returned `required - covered`:

  ```text
  Traceback (most recent call last):
      assert is_fully_covered(REQUIRED, MORNING) is True
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  The reasoning is sound — the difference is empty exactly when coverage is
  complete — but the value you returned is `set()`, and `set() is True` is
  `False`. Empty containers are **falsy**, which is a different thing from
  being `False`. If you like the difference version, wrap it:
  `return not (required - covered)` gives you a genuine `bool`.
  `required <= covered` says the same thing more directly and stops at the
  first missing topic instead of building a set it throws away.

- **`is_fully_covered(REQUIRED, EVENING)` returns `True`.** You tested for
  *any* overlap — `bool(required & covered)` — instead of full coverage. It
  returns a proper `bool`, it passes the morning assert, and it is still
  wrong:

  ```text
  bool(required & covered): True
  required <= covered     : False
  ```

  The evening circle shares `dicts` and `big-o` with the core list but has
  never taught `lists`. "Some" and "all" are different questions, and only
  `<=` asks the second. A test that happens to pass on one of your two cases
  is exactly how a bug of this kind survives.

- **`TypeError: unsupported operand type(s) for |: 'set' and 'list'`.** One
  side is still a list:

  ```text
  Traceback (most recent call last):
      MORNING | ["dicts"]
      ~~~~~~~~^~~~~~~~~~~
  TypeError: unsupported operand type(s) for |: 'set' and 'list'
  ```

  The operators want sets on both sides, and the message names whichever
  operator you reached first — `&`, `-` and `^` all fail the same way. This is
  a good error to get, because it is loud and immediate: wrap the other side
  in `set(...)` once, at the top, where the data arrives. The method forms are
  more forgiving — `MORNING.intersection(EVENING)` accepts any iterable and
  quietly converts — and that flexibility is occasionally handy and mostly a
  way to lose track of what type you are holding.

- **`AttributeError: 'dict' object has no attribute 'add'`.** You built an
  empty collection with `{}`, which is a dict. An empty set is `set()`; there
  is no empty-set literal in Python.

- **`TypeError: unhashable type: 'list'`.** You tried to put a list inside a
  set. Members must be things whose value cannot change underneath the set;
  convert inner lists to tuples first.

- **A subset test on two lists gives a confident, meaningless answer.**

  ```text
  >>> ["a"] <= ["b"]
  True
  ```

  No error, no warning, and the answer has nothing to do with membership —
  lists compare item by item like words in a dictionary, so this is really
  asking whether `"a"` sorts before `"b"`. It is the most dangerous item on
  this page precisely because there is no traceback to search for. If `<=` is
  going to mean "is a subset of", both sides have to be sets.

- **The printed order differs from the expected output.** You printed the set
  directly instead of `", ".join(sorted(...))`. A set has no order to print.

## Under the hood

<details>
<summary>Under the hood — why `a <= b` and `b <= a` can both be False</summary>

`<=` on numbers has a property you have relied on since you were seven and
have probably never had to name: for any two numbers, one of them is smaller,
or they are equal. Always. There is no third possibility. That is called a
**total order** — every pair can be lined up.

Sets are different, and it is worth seeing it happen:

```text
>>> {"a"} <= {"b"}
False
>>> {"b"} <= {"a"}
False
```

Neither is a subset of the other. Both comparisons are `False`, and neither
set is "bigger". This is a **partial order** — some pairs can be lined up and
some genuinely cannot. Picture two overlapping circles: one circle inside the
other is a subset, but two circles that merely overlap have no order between
them at all.

Three practical consequences.

**`not (a <= b)` does not mean `b < a`.** With numbers that reasoning is safe.
With sets it is wrong, and the two-line transcript above is the
counterexample. If your code says "if the required topics are not covered,
then the circle has taught extra things", you have quietly assumed a total
order that does not exist.

**`sorted()` on a list of sets does not do what you hope.** Python's sort
assumes a total order, and when it does not get one the result depends on
which pairs happened to be compared. No exception, just an arbitrary answer.
Sort sets by `len` or by a `sorted(...)` of their contents instead.

**All six comparisons have set meanings, and they are not the ones you have
memorised.**

| Operator | On sets it means |
|---|---|
| `a <= b` | every member of `a` is in `b` (subset) |
| `a < b` | subset, **and** `b` has something `a` does not (proper subset) |
| `a >= b` | `b` is a subset of `a` (superset) |
| `a == b` | same members, in any order |
| `a != b` | not the same members |

`a > b` and `a < b` are strict versions, and `{"a"} < {"a"}` is `False` while
`{"a"} <= {"a"}` is `True`. Every set is a subset of itself.

**The empty set is a subset of everything.** `set() <= anything` is `True`,
and that follows from the definition rather than from a special case: there is
no member of the empty set that is missing from the other one, because there
is no member of the empty set. That is why the `coverage_percent` stretch
below returns `100.0` for an empty requirement list — it is the only answer
that agrees with `is_fully_covered`.

**Two smaller notes.**

Sets have method forms as well as operators: `.union()`, `.intersection()`,
`.difference()`, `.symmetric_difference()`, `.issubset()`. The methods accept
any iterable — a list, a string, a generator — and convert it for you. The
operators demand sets on both sides. The methods also take more than one
argument: `a.union(b, c, d)`. Use the operator when both sides are already
sets, because the type error is a feature.

And `frozenset` is a set that cannot be changed after it is made — which means
it *can* be hashed, which means you can put a `frozenset` inside another set
or use one as a dict key:

```text
>>> {frozenset({"a", "b"})}
{frozenset({'a', 'b'})}
```

That is how you build a set of groups, or a dict keyed by "which topics did
this circle cover". A plain `set` in either of those places raises
`TypeError: unhashable type: 'set'`, for the same reason a list does.

</details>

## Acceptance checklist

- [ ] `python exercise-04-set-operations.py` prints five report lines then `All checks passed.`
- [ ] The printed lines match the expected output character for character.
- [ ] Every function body is a single expression.
- [ ] No `for` loop, comprehension, or list conversion outside `sorted()`.
- [ ] The file contains no `|=`, `&=`, `-=`, `^=` or `.update()`.
- [ ] `MORNING` and `EVENING` still have five members at the end of the run.
- [ ] `is_fully_covered` returns an actual `bool`.
- [ ] Committed to Git with a message like `Add Week 5 exercise 4: set operations`.

## Stretch

- **`missing_from` — a circle's teaching backlog, and a second way to write
  the coverage test.**

  ```python
  def missing_from(required: set[str], covered: set[str]) -> set[str]:
      """Return the required topics a circle has not taught yet."""
      return required - covered


  def is_fully_covered(required: set[str], covered: set[str]) -> bool:
      """Return True if nothing required is still outstanding."""
      return not missing_from(required, covered)
  ```

  ```text
  missing from morning : []
  missing from evening : ['lists']
  fully covered (m/e)  : True False
  ```

  Both versions are correct, and `not` returns a real `bool`, so the `is True`
  asserts still pass. Which reads better depends on what the caller needs
  next. If they only want a yes or no, `required <= covered` says exactly that
  and stops early. If they are going to ask "what is missing?" straight
  afterwards — and a teaching backlog is precisely that — computing the
  difference once and deriving the boolean from it avoids answering the same
  question twice. Write the version whose intermediate value somebody wants.

- **`coverage_percent`, with the division guarded.**

  ```python
  def coverage_percent(required: set[str], covered: set[str]) -> float:
      """Return the percentage of required topics covered, to one decimal."""
      if not required:
          return 100.0
      return round(len(required & covered) / len(required) * 100, 1)
  ```

  ```text
  coverage morning     : 100.0
  coverage evening     : 66.7
  coverage of nothing  : 100.0
  ```

  The guard is the interesting line. An empty `required` would divide by zero,
  so you have to decide what "how much of nothing have you covered" means
  before you can write the function at all. `100.0` is the defensible answer:
  nothing is outstanding, and it agrees with `is_fully_covered(set(),
  anything)`, which is `True`. Returning `0.0` would contradict your own other
  function; letting it raise pushes the decision onto every caller.

  Note the numerator is `len(required & covered)`, not `len(covered)`. Topics
  a circle taught that are not on the core list must not inflate the score,
  and `&` restricts the count to the ones that count.

- **A third circle, and why `^` does not mean what you expect.**

  ```python
  WEEKEND_RAW: list[str] = ["lists", "sets", "lists", "recursion", "dicts", "sets"]
  weekend: set[str] = set(WEEKEND_RAW)


  def covered_by_all(a: set[str], b: set[str], c: set[str]) -> set[str]:
      """Return the topics all three circles have covered."""
      return a & b & c


  def covered_by_exactly_one(a: set[str], b: set[str], c: set[str]) -> set[str]:
      """Return the topics exactly one of the three circles has covered."""
      return (a - b - c) | (b - a - c) | (c - a - b)
  ```

  ```text
  weekend raw / set    : 6 / 4
  covered by all three : ['dicts']
  XOR across three     : ['comprehensions', 'dicts', 'recursion', 'tuples']
  exactly one of three : ['comprehensions', 'recursion', 'tuples']
  ```

  Two things to take from that.

  The `set(WEEKEND_RAW)` conversion happens **once**, at the top, and turns
  six raw entries into four topics. Converting once is not merely tidier than
  converting inside every function — it is the difference between paying for
  the conversion once and paying for it on every call.

  And `MORNING ^ EVENING ^ weekend` is **wrong** for "exactly one", even
  though `^` is right for two sets. `dicts` appears in all three and survives
  the chain, because `^` really means "in an odd number of these sets", and
  three is odd. With two sets, "odd" and "exactly one" happen to coincide,
  which is how the wrong intuition forms. The spelled-out version keeps
  working for four sets and five. When an operator's meaning depends on how
  many things you chained, write the sentence out.

When your coverage report is right, move on to
[Exercise 5 — Comprehensions](./exercise-05-comprehensions.md).
