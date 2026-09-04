# Exercise 5 — Comprehensions

> **Topic:** rewriting six working `for` loops as list, dict and set comprehensions
> **Lecture:** [03 — Comprehensions and Big-O](../lecture-notes/03-comprehensions-and-big-o.md)
> **Difficulty:** Easy
> **Target time:** 90 minutes
> **Why this one:** comprehensions are the syntax that makes Python look like Python, and reading them fluently is what lets you read everyone else's code — you will meet one in the first file of every project you ever join. Here you get six loops that already work and write the one-line version of each, so every translation can be checked against an answer that is already correct and sitting eight lines above it.

## The Brief

A **comprehension** is a way of building a list, a dict or a set in one line
instead of four. Every comprehension is the same three pieces in the same
order:

```text
[  what I want    for  each thing  in  the collection   if  it qualifies  ]
   ^expression         ^variable       ^what you loop       ^optional filter
```

Read left to right and it is nearly English: *the lowercase title, for each
title in the list.*

Six small transformations of community session data are already written as
plain `for` loops in the starter. Every one of them works. Your job is to
write the comprehension that produces the identical result. The self-checks
compare the two directly, so when they disagree you have a translation bug and
the working version is right there to compare against. This is the rare
exercise where you can debug by reading.

Six is enough to cover the whole grammar:

1. a plain transformation,
2. a filter,
3. a choice between two values,
4. a dict comprehension,
5. a set comprehension,
6. a nested one.

Every other comprehension you will ever meet is a combination of those six.

## Starter

Create `exercise-05-comprehensions.py` in your practice repo and paste the
whole thing in, reference loops included. The `_loop` functions are given and
must not change; the six below them are yours.

```python
"""exercise-05-comprehensions.py — six loops, six one-liners.

Rewrite six working for-loops as comprehensions with identical results.

The six `_loop` functions are given and must not be edited -- they are the
tests. Fill in the six below them, then run the file. The self-checks at the
bottom print "All checks passed." when the module is correct.
"""

# ---- Given data ----
TITLES: list[str] = [
    "Intro to Loops", "Debugging Clinic", "List Comprehensions",
    "Git Basics", "Dict Patterns",
]

MINUTES: list[int] = [90, 60, 120, 45, 75]

SCORES: dict[str, int] = {
    "ada": 88, "grace": 54, "linus": 71, "margaret": 59, "guido": 95,
}

ROSTERS: list[list[str]] = [["ada", "grace"], ["linus"], ["margaret", "guido", "ada"]]


# ---- Reference loops (do not edit) ----
def slugs_loop(titles: list[str]) -> list[str]:
    """Lowercase each title and replace spaces with hyphens, the long way."""
    out = []
    for title in titles:
        out.append(title.lower().replace(" ", "-"))
    return out


def long_sessions_loop(titles: list[str], minutes: list[int]) -> list[str]:
    """Return the titles of sessions longer than 60 minutes, the long way."""
    out = []
    for title, mins in zip(titles, minutes):
        if mins > 60:
            out.append(title)
    return out


def labels_loop(scores: dict[str, int]) -> list[str]:
    """Return "pass" for scores of 60 or more, "retry" otherwise, the long way."""
    out = []
    for score in scores.values():
        if score >= 60:
            out.append("pass")
        else:
            out.append("retry")
    return out


def title_to_minutes_loop(titles: list[str], minutes: list[int]) -> dict[str, int]:
    """Map each title to its length in minutes, the long way."""
    out = {}
    for title, mins in zip(titles, minutes):
        out[title] = mins
    return out


def initials_loop(names: dict[str, int]) -> set[str]:
    """Return the uppercase first letters of the names, the long way."""
    out = set()
    for name in names:
        out.add(name[0].upper())
    return out


def flatten_loop(rosters: list[list[str]]) -> list[str]:
    """Return every name from every roster, in order, the long way."""
    out = []
    for roster in rosters:
        for name in roster:
            out.append(name)
    return out


# ---- Your task: one comprehension per function ----
def slugs(titles: list[str]) -> list[str]:
    """Lowercase each title and replace spaces with hyphens.

    Args:
        titles: The session titles.

    Returns:
        One slug per title, in the same order.
    """
    ...  # TODO: list comprehension, plain transformation


def long_sessions(titles: list[str], minutes: list[int]) -> list[str]:
    """Return the titles of sessions longer than 60 minutes.

    Args:
        titles: The session titles.
        minutes: Each session's length, in the same order as `titles`.

    Returns:
        The titles that run over an hour.
    """
    ...  # TODO: list comprehension with an `if` filter, over zip()


def labels(scores: dict[str, int]) -> list[str]:
    """Return "pass" for scores of 60 or more, "retry" otherwise.

    Args:
        scores: A name-to-score mapping.

    Returns:
        One label per score, in the dict's own order.
    """
    ...  # TODO: conditional EXPRESSION before the `for`


def title_to_minutes(titles: list[str], minutes: list[int]) -> dict[str, int]:
    """Map each title to its length in minutes.

    Args:
        titles: The session titles.
        minutes: Each session's length, in the same order as `titles`.

    Returns:
        A dict from title to minutes.
    """
    ...  # TODO: dict comprehension over zip()


def initials(names: dict[str, int]) -> set[str]:
    """Return the uppercase first letters of the names, deduplicated.

    Args:
        names: A mapping whose keys are the names.

    Returns:
        A set of single uppercase letters.
    """
    ...  # TODO: set comprehension


def flatten(rosters: list[list[str]]) -> list[str]:
    """Return every name from every roster, in order, duplicates kept.

    Args:
        rosters: One list of names per study circle.

    Returns:
        A single flat list of names.
    """
    ...  # TODO: list comprehension with two `for` clauses


# ---- Self-check ----
if __name__ == "__main__":
    print(f"slugs:     {slugs(TITLES)[0]}")
    print(f"long:      {', '.join(long_sessions(TITLES, MINUTES))}")
    print(f"labels:    {' '.join(labels(SCORES))}")
    print(f"lookup:    Git Basics -> {title_to_minutes(TITLES, MINUTES)['Git Basics']}")
    print(f"initials:  {', '.join(sorted(initials(SCORES)))}")
    print(f"flattened: {len(flatten(ROSTERS))} names, {len(set(flatten(ROSTERS)))} unique")

    assert slugs(TITLES) == slugs_loop(TITLES)
    assert long_sessions(TITLES, MINUTES) == long_sessions_loop(TITLES, MINUTES)
    assert long_sessions(TITLES, MINUTES) == ["Intro to Loops", "List Comprehensions", "Dict Patterns"]
    assert labels(SCORES) == labels_loop(SCORES) == ["pass", "retry", "pass", "retry", "pass"]
    assert title_to_minutes(TITLES, MINUTES) == title_to_minutes_loop(TITLES, MINUTES)
    assert initials(SCORES) == initials_loop(SCORES) == {"A", "G", "L", "M"}
    assert flatten(ROSTERS) == flatten_loop(ROSTERS)
    assert flatten(ROSTERS) == ["ada", "grace", "linus", "margaret", "guido", "ada"]
    print("All checks passed.")
```

Four things you need before you start.

**The brackets pick the type.** `[...]` builds a list. `{...}` with a colon
inside builds a dict. `{...}` without a colon builds a set. Same grammar,
three containers, and the punctuation is the only difference.

**`zip`.** `zip(titles, minutes)` walks two lists at the same time and hands
you one pair at a time. `for title, mins in zip(...)` unpacks that pair into
two names, exactly as you would in a loop header. `zip` stops at the shorter
list, silently, which is on the bug list below.

**The filter versus the choice.** These look similar and do completely
different jobs:

```python
[x for x in xs if cond]          # which items survive
[a if cond else b for x in xs]   # what each item becomes
```

The filter goes **after** the `for` and has no `else`. The choice goes
**before** the `for` and must have one.

**`...`** is a real Python object, called `Ellipsis`, and Python accepts it as
a whole function body. So an unfinished stub runs perfectly happily and hands
back `None`. That is why the first thing this file does when you run it
unfinished is complain about `None` rather than about the stub.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/exercises/exercise-05-comprehensions.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Each of the six functions is **one** comprehension, returned directly. No
   temporary list, no `append`, no `for` statement.
2. Each result equals its `_loop` counterpart exactly, order included.
3. `labels` follows the order of `SCORES`. Dicts have remembered insertion
   order since Python 3.7, so `["pass", "retry", "pass", "retry", "pass"]` is
   a defined answer, not a coincidence.
4. `initials` is built by a set comprehension, not a list comprehension
   wrapped in `set(...)`. Five names give four initials, because `grace` and
   `guido` share a `G`.
5. `flatten` keeps duplicates and order: `ada` appears first and last.
6. The reference loops stay in the file, unedited. They are the tests.

## Constraints

- **A comprehension does not make anything faster in the way that matters.**
  `slugs` walks the list once as a loop and once as a comprehension. The
  comprehension is a bit quicker because it has a dedicated instruction for
  "add this to the list" and so skips looking up `.append` on every turn — but
  that is a small, fixed saving, not a change in shape. If you are hoping a
  comprehension will rescue a slow function, you need a better algorithm or a
  better data structure, which is what Exercises 2, 3 and 4 were about.

- **The `if` filter goes after the `for`; the `if`/`else` goes before it.**
  Different jobs, different places. Putting an `else` in the filter slot is a
  `SyntaxError` rather than a subtle bug, so Python catches this one for you.

- **Nested `for` clauses read in the same order as the nested loops they
  replace.** `[name for roster in rosters for name in roster]` puts the outer
  loop first, exactly as `flatten_loop` writes it. The clauses run left to
  right, so a name introduced by one clause is available to the next. Reverse
  them and the inner variable does not exist yet.

- **Use a set comprehension, not `set([...])`.** The wrapped version builds a
  whole list and throws it away: same answer, twice the allocation, and the
  reader does not learn "unique" until the end of the line. The braces say it
  up front.

- **Never put a comprehension inside a comprehension's filter.**

  ```python
  [x for x in a if x in [y for y in b]]
  ```

  That rebuilds the inner list from scratch for every single item in `a`, and
  then reads through it. This is the one comprehension habit that genuinely
  does change your program's shape, and it changes it for the worse. Build the
  set once, outside, then filter against it.

- **Stop when it stops reading.** Lecture 03 is blunt about this: a
  comprehension that needs a comment should be a loop. All six here fit
  legibly on one line, which is exactly why they were chosen. When yours does
  not, that is information, not a challenge.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-comprehensions.py
slugs:     intro-to-loops
long:      Intro to Loops, List Comprehensions, Dict Patterns
labels:    pass retry pass retry pass
lookup:    Git Basics -> 45
initials:  A, G, L, M
flattened: 6 names, 5 unique
All checks passed.
```

Two lines to check carefully. `long:` has three titles, not four —
`Debugging Clinic` is exactly 60 minutes and the filter is `> 60`, not `>=`.
And `initials:` has four letters from five names, which is the set
comprehension doing its job silently.

## Steps

1. Create `exercise-05-comprehensions.py` and paste the whole starter in,
   reference loops included.
2. Run it once. It dies on the first `print`, because `slugs` still hands back
   `None`. The loops are already correct, so every failure from here on is
   yours.
3. Work in order, running the file after each function. The asserts are
   grouped so you can see exactly how far you got.
4. For each one, read the loop out loud as a single sentence before you write
   the comprehension. "Append the hyphenated lowercase title, for each title"
   converts almost word for word.
5. At `labels`, put the `if`/`else` after the `for` on purpose and read the
   `SyntaxError` Python gives you. Then move it and watch the error go.
6. When `All checks passed.` prints, cut a reference loop into a scratch file
   and try to recover it from your comprehension without looking. Translating
   back the other way is the skill that makes unfamiliar code readable.

## The Solution

```python
"""exercise-05-comprehensions-solution.py — six loops, six one-liners.

The six `_loop` functions are the starter's, unedited. They already work, and
they are the tests: each of the six comprehensions below has to produce the
identical result.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
TITLES: list[str] = [
    "Intro to Loops", "Debugging Clinic", "List Comprehensions",
    "Git Basics", "Dict Patterns",
]

MINUTES: list[int] = [90, 60, 120, 45, 75]

SCORES: dict[str, int] = {
    "ada": 88, "grace": 54, "linus": 71, "margaret": 59, "guido": 95,
}

ROSTERS: list[list[str]] = [["ada", "grace"], ["linus"], ["margaret", "guido", "ada"]]


# ---- Reference loops (do not edit) ----
def slugs_loop(titles: list[str]) -> list[str]:
    """Lowercase each title and replace spaces with hyphens, the long way."""
    out = []
    for title in titles:
        out.append(title.lower().replace(" ", "-"))
    return out


def long_sessions_loop(titles: list[str], minutes: list[int]) -> list[str]:
    """Return the titles of sessions longer than 60 minutes, the long way."""
    out = []
    for title, mins in zip(titles, minutes):
        if mins > 60:
            out.append(title)
    return out


def labels_loop(scores: dict[str, int]) -> list[str]:
    """Return "pass" for scores of 60 or more, "retry" otherwise, the long way."""
    out = []
    for score in scores.values():
        if score >= 60:
            out.append("pass")
        else:
            out.append("retry")
    return out


def title_to_minutes_loop(titles: list[str], minutes: list[int]) -> dict[str, int]:
    """Map each title to its length in minutes, the long way."""
    out = {}
    for title, mins in zip(titles, minutes):
        out[title] = mins
    return out


def initials_loop(names: dict[str, int]) -> set[str]:
    """Return the uppercase first letters of the names, the long way."""
    out = set()
    for name in names:
        out.add(name[0].upper())
    return out


def flatten_loop(rosters: list[list[str]]) -> list[str]:
    """Return every name from every roster, in order, the long way."""
    out = []
    for roster in rosters:
        for name in roster:
            out.append(name)
    return out


# ---- Your task: one comprehension per function ----
def slugs(titles: list[str]) -> list[str]:
    """Lowercase each title and replace spaces with hyphens.

    Args:
        titles: The session titles.

    Returns:
        One slug per title, in the same order.
    """
    return [title.lower().replace(" ", "-") for title in titles]


def long_sessions(titles: list[str], minutes: list[int]) -> list[str]:
    """Return the titles of sessions longer than 60 minutes.

    Args:
        titles: The session titles.
        minutes: Each session's length, in the same order as `titles`.

    Returns:
        The titles that run over an hour.
    """
    return [title for title, mins in zip(titles, minutes) if mins > 60]


def labels(scores: dict[str, int]) -> list[str]:
    """Return "pass" for scores of 60 or more, "retry" otherwise.

    Args:
        scores: A name-to-score mapping.

    Returns:
        One label per score, in the dict's own order.
    """
    return ["pass" if score >= 60 else "retry" for score in scores.values()]


def title_to_minutes(titles: list[str], minutes: list[int]) -> dict[str, int]:
    """Map each title to its length in minutes.

    Args:
        titles: The session titles.
        minutes: Each session's length, in the same order as `titles`.

    Returns:
        A dict from title to minutes.
    """
    return {title: mins for title, mins in zip(titles, minutes)}


def initials(names: dict[str, int]) -> set[str]:
    """Return the uppercase first letters of the names, deduplicated.

    Args:
        names: A mapping whose keys are the names.

    Returns:
        A set of single uppercase letters.
    """
    return {name[0].upper() for name in names}


def flatten(rosters: list[list[str]]) -> list[str]:
    """Return every name from every roster, in order, duplicates kept.

    Args:
        rosters: One list of names per study circle.

    Returns:
        A single flat list of names.
    """
    return [name for roster in rosters for name in roster]


# ---- Self-check ----
if __name__ == "__main__":
    print(f"slugs:     {slugs(TITLES)[0]}")
    print(f"long:      {', '.join(long_sessions(TITLES, MINUTES))}")
    print(f"labels:    {' '.join(labels(SCORES))}")
    print(f"lookup:    Git Basics -> {title_to_minutes(TITLES, MINUTES)['Git Basics']}")
    print(f"initials:  {', '.join(sorted(initials(SCORES)))}")
    print(f"flattened: {len(flatten(ROSTERS))} names, {len(set(flatten(ROSTERS)))} unique")

    assert slugs(TITLES) == slugs_loop(TITLES)
    assert long_sessions(TITLES, MINUTES) == long_sessions_loop(TITLES, MINUTES)
    assert long_sessions(TITLES, MINUTES) == ["Intro to Loops", "List Comprehensions", "Dict Patterns"]
    assert labels(SCORES) == labels_loop(SCORES) == ["pass", "retry", "pass", "retry", "pass"]
    assert title_to_minutes(TITLES, MINUTES) == title_to_minutes_loop(TITLES, MINUTES)
    assert initials(SCORES) == initials_loop(SCORES) == {"A", "G", "L", "M"}
    assert flatten(ROSTERS) == flatten_loop(ROSTERS)
    assert flatten(ROSTERS) == ["ada", "grace", "linus", "margaret", "guido", "ada"]
    print("All checks passed.")
```

**Every comprehension has the same skeleton:** an output expression, then one
or more `for` clauses, then an optional `if` filter. Read it left to right and
you get "what I want, for each thing, where the thing qualifies".

**`slugs` — the plain transformation.** `title.lower().replace(" ", "-")` runs
once per title and the results land in a new list, in order. Same shape as the
loop, minus the `out = []` and the `.append`.

**`long_sessions` — the filter goes after the `for`.** The tuple unpacking in
`for title, mins in zip(titles, minutes)` is the same unpacking you would
write in a loop header, and it is what lets the filter test one variable while
the output expression hands back another. Getting `[mins for ...]` instead of
`[title for ...]` is the most common slip here: **the expression before the
`for` is what you get back.**

**`labels` — the conditional goes before the `for`.** This is the distinction
worth carving into your desk:

```python
[x for x in xs if cond]          # which items survive
[a if cond else b for x in xs]   # what each item becomes
```

`labels` iterates `scores.values()` because it compares numbers; iterating
`scores` gives keys, which are names. And the answer is defined rather than
lucky, because dicts have remembered insertion order since Python 3.7 —
Exercise 3's *Under the hood* explains how they manage it.

**`title_to_minutes` — braces plus a colon make a dict.** The colon between
the key and the value is the entire difference from a set comprehension. Later
duplicate keys quietly overwrite earlier ones, which is worth knowing before
you build a dict comprehension over data you have not checked.

**`initials` — braces without a colon make a set.** It deduplicates as it
builds, which is why five names give four initials: `grace` and `guido` both
contribute `G` and the set keeps one. The alternative,
`set([name[0].upper() for name in names])`, gets the same answer by building a
five-element list and throwing it away.

**`flatten` — nested `for` clauses read in loop order.** Outer collection
first, exactly as the reference loop writes it. The clauses run left to right,
so a name introduced by one clause is available to the next.

**Cost — the honest version.** A comprehension does not change the shape of
anything. `slugs` walks the list once either way; `flatten` touches every name
once either way. What you gain is a constant factor, and what you gain it from
is visible in the bytecode — see *Under the hood*. Comprehensions are for
readability. Use them when the one-liner reads better than the loop, and stop
when it does not.

## Run it

Copy the worked answer on this page into `exercise-05-comprehensions.py` and run it:

```bash
python exercise-05-comprehensions.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-05-comprehensions.py`.

## Common bugs to catch

- **`SyntaxError: invalid syntax`, with the caret under the `else`.**

  ```text
      return ["pass" for score in scores.values() if score >= 60 else "retry"]
                                                                 ^^^^
  SyntaxError: invalid syntax
  ```

  The trailing `if` is a filter, and a filter has no alternative branch — an
  item either survives or it does not. If you need an `else`, the whole
  conditional moves in front of the `for`. Note this is a `SyntaxError`,
  raised before anything runs at all, so none of your other functions get
  tested. Fix it and the rest of your work reappears.

- **`NameError: name 'roster' is not defined`.** Your two `for` clauses are in
  the wrong order:

  ```text
  Traceback (most recent call last):
      return [name for name in roster for roster in rosters]
                               ^^^^^^
  NameError: name 'roster' is not defined. Did you mean: 'rosters'?
  ```

  The caret is under the *first* `roster`, and that is the message: at the
  moment the first clause runs, nothing has defined `roster` yet. Clauses read
  left to right, in the same order as the nested loops they replace — outer
  collection first. If you get lost, write the loops out and read them top to
  bottom onto one line.

- **`TypeError: '>=' not supported between instances of 'str' and 'int'`.**
  You iterated the dict instead of its values:

  ```text
  Traceback (most recent call last):
      return ["pass" if score >= 60 else "retry" for score in scores]
                        ^^^^^^^^^^^
  TypeError: '>=' not supported between instances of 'str' and 'int'
  ```

  Looping a dict yields keys, so `score` is the name `"ada"` and you are
  asking whether a string is at least 60. The variable name lied to you, which
  is a real hazard — a loop variable is only as honest as you make it. Use
  `.values()` for the numbers, `.items()` if you decide the label should
  mention the name.

- **`initials:  A, G, G, L, M`.** You built a list where a set was asked for:

  ```text
  initials:  A, G, G, L, M
  flattened: 6 names, 5 unique
  Traceback (most recent call last):
      assert initials(SCORES) == initials_loop(SCORES) == {"A", "G", "L", "M"}
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Five items with `G` twice, because a list keeps what a set would have
  collapsed. The printed line gives it away well before the assert does, which
  is the argument for the starter printing a report at all. Two neighbouring
  mistakes: `{n: n[0].upper() for n in names}` has a colon, so it builds a
  dict; and dropping `.upper()` gives you lowercase letters and a bare
  `AssertionError` that shows you nothing — print both sets when that one
  bites.

- **`long_sessions` returns four titles.**

  ```text
  long:      Intro to Loops, Debugging Clinic, List Comprehensions, Dict Patterns
  ```

  Your filter is `>= 60`. The brief says longer than 60, and `Debugging
  Clinic` sits exactly on the line — it is in the data for precisely this
  reason. Whenever you write a `>` or a `<`, say out loud whether the boundary
  value is in or out, then check that some row in your data *is* the boundary
  value.

- **`long_sessions` returns minutes.** The expression before the `for` is what
  you get back: `[title for title, mins in zip(...)]`, not `[mins for ...]`.

- **`zip` silently truncates.** Add a title without adding a minutes value and
  `zip` stops at the shorter list, losing the last row with no error at all.
  Check `len(TITLES) == len(MINUTES)` whenever you extend the data.

- **`TypeError: 'NoneType' object is not subscriptable` on the first
  `print`.**

  ```text
  Traceback (most recent call last):
      print(f"slugs:     {slugs(TITLES)[0]}")
                          ~~~~~~~~~~~~~^^^
  TypeError: 'NoneType' object is not subscriptable
  ```

  The `...` stub is still in the body, and `...` is a real object Python
  accepts as a whole function body — so an unfinished function runs without
  complaint and hands back `None`. The error surfaces at the **caller**, one
  frame away from the actual problem. Whenever a `NoneType` error points at a
  line that looks fine, go and look at the function that produced the value.

## Under the hood

<details>
<summary>Under the hood — what the interpreter really does differently</summary>

Python compiles your source into **bytecode**, a list of small instructions
the interpreter walks through. You can look at it with `dis`, and looking at
it settles the "are comprehensions faster?" argument in about thirty seconds.

Here are two functions that do the same job, on CPython 3.13.2:

```python
import dis


def slugs_loop(titles):
    out = []
    for title in titles:
        out.append(title.lower())
    return out


def slugs_comp(titles):
    return [title.lower() for title in titles]
```

The loop's inner section:

```text
  7           LOAD_FAST                1 (out)
              LOAD_ATTR                1 (append + NULL|self)
              LOAD_FAST                2 (title)
              LOAD_ATTR                3 (lower + NULL|self)
              CALL                     0
              CALL                     1
              POP_TOP
              JUMP_BACKWARD           36 (to L1)
```

And the comprehension's:

```text
       L2:     FOR_ITER                18 (to L3)
               STORE_FAST_LOAD_FAST    17 (title, title)
               LOAD_ATTR                1 (lower + NULL|self)
               CALL                     0
               LIST_APPEND              2
               JUMP_BACKWARD           20 (to L2)
```

Read the two side by side and the whole story is three instructions.

**The loop loads `out`, then looks up `.append` on it, then calls it.** That
attribute lookup happens on *every single turn*, and it produces a bound
method object each time. Then `CALL 1` runs it, and `POP_TOP` throws away the
`None` that `.append` returns, because nobody wants it.

**The comprehension does all of that with one instruction: `LIST_APPEND`.**
The list being built is sitting on the interpreter's stack, so there is
nothing to look up, nothing to call, and no return value to discard.

That is the entire speed difference, and it is why the honest claim is "a
constant factor, and a small one". The number of times round the loop is
identical. If your function is slow because it reads through a list once per
item, no amount of bracket-swapping will help you — you need the set from
Exercise 2 or the dict from Exercise 3.

**Two other things that block shows.**

**`STORE_FAST_LOAD_FAST` is a superinstruction.** CPython 3.13 merges some
common instruction pairs into one, so "store the loop variable, then load it
again" costs one dispatch instead of two. There are dozens of these; they are
part of the ongoing speed work in CPython 3.11 onwards and they are invisible
unless you go looking.

**The comprehension does not leak its variable, and now you can see how.**
Notice `LOAD_FAST_AND_CLEAR` before the loop and `STORE_FAST` after it, with
an exception table entry to make sure the restore happens even if something
raises. Python saves whatever `title` meant before, uses the name, and puts
the old value back:

```text
>>> x = "outer"
>>> result = [x for x in range(3)]
>>> x, result
('outer', [0, 1, 2])
```

`x` is still `"outer"`. A plain `for` loop would have left it as `2`.

That behaviour is older than the bytecode. Until Python 3.11 a comprehension
was compiled as a **hidden function** that got created and called on every
evaluation, which gave it its own scope for free but cost a function call
every time. PEP 709, in Python 3.12, inlined comprehensions into the
surrounding function and kept the scoping promise by hand — which is what all
that `SWAP`/`STORE_FAST` machinery is doing. The reported speedup was roughly
twofold for small comprehensions, and nothing about how you write them
changed.

**Where a generator expression fits.** Swap the square brackets for round ones
and you get a **generator**: it produces values one at a time instead of
building the whole list first. The usual claim is that generators are faster.
Timed on 10,000 integers over 20,000 repetitions, CPython 3.13.2:

```text
generator : 5.280 s
list comp : 5.147 s
```

The list comprehension is very slightly **quicker**, because a generator pays
a small cost each time it resumes that a comprehension's tight loop does not.
The generator's win is memory, and that one is not slight. Peak allocation
while summing 200,000 integers, measured with `tracemalloc`:

```text
generator peak  : 408 bytes
list comp peak  : 1,624,048 bytes
```

The list version builds every value before adding any of them; the generator
holds one at a time. So the honest rule is: reach for a generator when the
intermediate collection would be large or you do not need it afterwards, not
because you expect it to be quicker.

</details>

## Acceptance checklist

- [ ] `python exercise-05-comprehensions.py` prints six report lines then `All checks passed.`
- [ ] All six functions are a single returned comprehension.
- [ ] The word `append` appears only in the reference loops — five hits, and
      `labels_loop` has two of them, one per branch.
- [ ] The reference loops are unedited.
- [ ] `initials` uses `{...}` directly, with no `set(` call.
- [ ] Type hints and docstrings on all six of your signatures.
- [ ] Committed to Git with a message like `Add Week 5 exercise 5: comprehensions`.

## Stretch

- **A generator expression inside `sum`.**

  ```python
  def total_long_minutes(minutes: list[int] = MINUTES) -> int:
      """Return the combined minutes of the sessions longer than an hour."""
      return sum(m for m in minutes if m > 60)
  ```

  ```text
  total_long_minutes: 285
  ```

  Note the missing brackets. When a generator expression is a call's only
  argument, the call's own parentheses are enough — `sum((m for m in ...))` is
  legal and redundant. What this buys you is memory rather than speed, and
  *Under the hood* has the measurements.

- **A generator expression inside a filter.**

  ```python
  def short_titles(titles: list[str]) -> list[str]:
      """Return the titles whose longest word is five letters or fewer."""
      return [t for t in titles if max(len(w) for w in t.split()) <= 5]
  ```

  ```text
  short_titles      : ['Intro to Loops']
  ```

  It works, and it is right at the edge of readable. The filter now contains a
  `max` over a generator over a `split`, so reading it means holding three
  levels at once. The honest answer to "does the loop version read better?" is
  roughly a tie for this one, and it tips to the loop the moment you add a
  second condition.

  There is a real bug hiding in it, too. `max` over an empty generator raises
  `ValueError: max() iterable argument is empty`, so a title that is nothing
  but whitespace would take the whole function down. A loop gives you
  somewhere to put that guard; the comprehension does not.

- **`transpose`, two ways.**

  ```python
  def transpose(matrix: list[list[int]]) -> list[list[int]]:
      """Return the matrix with rows and columns swapped."""
      return [[row[i] for row in matrix] for i in range(len(matrix[0]))]
  ```

  ```text
  transpose         : [[1, 4], [2, 5], [3, 6]]
  zip(*matrix)      : [(1, 4), (2, 5), (3, 6)]
  as lists          : [[1, 4], [2, 5], [3, 6]]
  transpose([])     : IndexError: list index out of range
  ```

  The nested comprehension reads outside-in: the outer clause walks column
  numbers, and for each one the inner clause collects that position from every
  row. `len(matrix[0])` assumes the matrix is rectangular and non-empty, which
  is why the empty case raises — a real limitation, stated rather than hidden.

  `zip(*matrix)` does the same job in eight characters. The `*` unpacks the
  rows into separate arguments, so `zip([1,2,3], [4,5,6])` pairs them up by
  position, which is exactly transposition. It hands back tuples rather than
  lists, and it handles the empty matrix by returning nothing instead of
  raising. Write the comprehension once to understand the operation; use
  `zip(*matrix)` afterwards.

That is Week 5's exercises done. Next come the two
[challenges](../challenges/README.md), which hand you the same ideas as whole
problems to plan rather than blanks to fill in.
