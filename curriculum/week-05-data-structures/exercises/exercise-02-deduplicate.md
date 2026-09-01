# Exercise 2 — Deduplicate

> **Topic:** removing duplicates from a list while keeping the order things first appeared
> **Lecture:** [01 — Lists and Tuples](../lecture-notes/01-lists-and-tuples.md) and [02 — Sets and Dicts](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** `set(items)` removes duplicates and destroys the order. `sorted(set(items))` removes duplicates and imposes a *different* order. Real data — sign-up sheets, log lines, rows from a spreadsheet — needs the duplicates gone **and** the original order kept. The pattern you build here is four lines long, stays fast on a million rows, and you will reach for it every month for the rest of your career.

## The Brief

Three sign-up sheets went round at community events, and the organisers typed
all of them into one list. People signed more than one sheet, so the list has
repeats.

It is messier than that. One person wrote their address with a capital letter
the first time and all lowercase the second. Another person's address arrived
with a space in front of it, because whoever typed it hit the space bar first.
To a human all of those are the same person. To Python they are four different
strings, because Python compares strings character by character and a capital
`A` is not the letter `a`.

Your job: collapse the list to one entry per human, keeping the order people
first appeared **and** the spelling they first used.

You are going to write it twice.

- `dedupe` matches **exactly**. `"Ada@crunch.dev"` and `"ada@crunch.dev"` both
  survive, because as far as `==` is concerned they are different.
- `dedupe_case_insensitive` matches after tidying: ignore the outside spaces,
  ignore the capital letters. Those four spellings collapse into one entry —
  and the entry you keep is the **original** spelling, not the tidied one.

Writing both is the point. Removing duplicates is the easy half. Deciding what
"the same" *means* is the half that ships bugs, and putting the two versions
side by side is the fastest way to see the difference.

Then one more, smaller function: `first_duplicate`, which walks the list and
reports the first thing it meets twice, stopping right there.

## Starter

Create `exercise-02-deduplicate.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""exercise-02-deduplicate.py — one entry per human, order kept.

Remove duplicates from a list while preserving first-seen order, using a
set for the "have I seen this?" test.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
SIGNUPS: list[str] = [
    "Ada@crunch.dev",
    "grace@crunch.dev",
    "ada@crunch.dev",
    "linus@crunch.dev",
    "grace@crunch.dev",
    "  ada@crunch.dev  ",
    " margaret@crunch.dev",
]


# ---- Your task ----
def dedupe(items: list[str]) -> list[str]:
    """Return a new list with exact duplicates removed, first-seen order kept.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        A new list holding the first sighting of each exact string.
    """
    # TODO: keep a `seen` set; append to the result only on a first sighting
    ...


def dedupe_case_insensitive(items: list[str]) -> list[str]:
    """Return a new list deduplicated after stripping and lowercasing.

    The output keeps the ORIGINAL spelling of the first occurrence, not the
    normalised form used for comparison.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        A new list holding the first sighting of each normalised address,
        spelled the way it arrived.
    """
    # TODO: normalise for the `seen` key, append the untouched item
    ...


def first_duplicate(items: list[str]) -> str | None:
    """Return the first item that appears twice (exact match), or None.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        The repeated string, or None when nothing repeats.
    """
    # TODO: return as soon as you meet something already in `seen`
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"raw signups:        {len(SIGNUPS)}")
    print(f"exact dedupe:       {len(dedupe(SIGNUPS))}")
    print(f"normalised dedupe:  {len(dedupe_case_insensitive(SIGNUPS))}")
    print(f"first duplicate:    {first_duplicate(SIGNUPS)}")

    assert dedupe(SIGNUPS) == [
        "Ada@crunch.dev",
        "grace@crunch.dev",
        "ada@crunch.dev",
        "linus@crunch.dev",
        "  ada@crunch.dev  ",
        " margaret@crunch.dev",
    ]
    assert dedupe_case_insensitive(SIGNUPS) == [
        "Ada@crunch.dev",
        "grace@crunch.dev",
        "linus@crunch.dev",
        " margaret@crunch.dev",
    ]
    assert first_duplicate(SIGNUPS) == "grace@crunch.dev"
    assert first_duplicate(["a", "b", "c"]) is None
    assert dedupe([]) == []
    assert SIGNUPS[2] == "ada@crunch.dev"  # input list untouched
    print("All checks passed.")
```

Four words you need before you start.

**Set.** A set is a bag that holds each thing at most once and does not
remember what order they went in. Its whole reason for existing is the
question *is this in here?* — and it answers that question without looking
through everything it holds. The empty set is written `set()`. It is **not**
`{}`, because the curly braces were already taken by dicts.

**`.add` versus `.append`.** Lists append; sets add. A list keeps an order, so
"put this on the end" makes sense. A set has no end.

**Normalise.** To normalise a value is to tidy it into a standard shape before
you compare it. Here that means `item.strip().lower()` — `.strip()` removes
whitespace from both ends and `.lower()` makes every letter small. Neither one
changes the original string; both hand you a new one.

**Key versus value.** The **key** is the tidied form you compare with. The
**value** is what you actually keep. On this page they are deliberately
different, and keeping them apart is the whole lesson of the second function.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/exercises/exercise-02-deduplicate.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `dedupe` compares exactly, so `"Ada@crunch.dev"` and `"ada@crunch.dev"`
   both survive. Seven entries become six.
2. `dedupe_case_insensitive` compares `item.strip().lower()`. Seven entries
   become four, and those four are the **original** strings — capital letter
   and leading space included.
3. `first_duplicate` returns the string itself, not its position, and `None`
   when nothing repeats. It stops at the first repeat instead of reading on.
4. None of the three functions modifies the list it was handed.
5. `dedupe([])` returns `[]` with no special case. A correct loop handles the
   empty list for free.
6. Every function keeps its type hints and its docstring, `str | None`
   included.

## Constraints

- **Track what you have seen in a `set`, never in the result list.**
  `if item not in result` looks tidier and it is the trap. `in` on a list
  reads through the list from the start, so as the result grows, every new
  item costs more than the last one. With seven addresses you will never feel
  it. Double the input and the set version takes twice as long while the list
  version takes **four** times as long — that is what makes it a different
  shape of program, not just a slower one. Measured on 20,000 addresses, the
  set version was over five hundred times faster; the numbers are in *Under
  the hood*.

- **Check first, add second.** The two lines inside the `if` go in that order
  and no other. Add before you check and every item is already in `seen` by
  the time you test it, so nothing is ever kept and your result is empty. It
  is worth writing that bug once on purpose — the empty list is genuinely
  puzzling until you trace two turns of the loop by hand.

- **Do not use `list(set(items))`.** It removes duplicates in one call and
  destroys the order — and not in a fixed way. Python scrambles string hashing
  differently on every run of the interpreter, so the same expression can give
  you a different order on the same machine an hour later. An assert written
  against that fails one time in five, which is far worse than failing every
  time.

- **Do not use `sorted(set(items))` either.** It is at least the same every
  run, but alphabetical is not sign-up order, and the brief asked for sign-up
  order.

- **Normalise the key, never the value.** `item.strip().lower()` goes into
  `seen`; the untouched `item` goes into the result. Lowercase what you
  *store* and you have thrown away information the organisers typed on
  purpose, and there is no way to get it back.

- **Do not remove items from the list you are looping over.**
  `items.remove(x)` inside `for item in items` shifts everything after it one
  place to the left, and the loop skips one. Build a new list instead. You are
  never fighting the loop when you build a new list.

- **No `collections` imports yet.** `Counter` and `OrderedDict` would answer
  parts of this in a single call. Today is about the pattern underneath them,
  so that when you do reach for those, you know what they are doing.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-deduplicate.py
raw signups:        7
exact dedupe:       6
normalised dedupe:  4
first duplicate:    grace@crunch.dev
All checks passed.
```

Exact matching removes exactly one row: the repeated plain
`grace@crunch.dev`. To Python, `Ada@crunch.dev`, `ada@crunch.dev` and
`"  ada@crunch.dev  "` are three entirely different strings.

Six is the honest answer to the question as asked. Four is the answer the
organisers wanted. That gap **is** the exercise, and holding both numbers in
your head at once is the skill: six is what the computer sees, four is what a
human means.

## Steps

1. Create `exercise-02-deduplicate.py` and paste the starter in. Run it once
   to see it fail.
2. In a REPL, paste `SIGNUPS` and run `len(set(SIGNUPS))`. You should get 6.
   Then run `list(set(SIGNUPS))` in a few *fresh* REPLs — quit and restart
   Python between tries — and watch the order move around.
3. Write `dedupe` with a `seen` set and a `result` list. At most four lines
   inside the loop.
4. Run the file. The first assert should pass and the second should fail,
   because `dedupe_case_insensitive` is still a stub.
5. Write `dedupe_case_insensitive`. Exactly one line differs from `dedupe`:
   what you put in `seen`. Everything else, including what you append, stays
   the same. If you find yourself changing the `append` line, stop and reread
   requirement 2.
6. Write `first_duplicate`. It returns from *inside* the loop and never reads
   the rest of the list.
7. When `All checks passed.` prints, add your own address to `SIGNUPS` twice,
   once tidy and once with a capital letter, and predict both counts before
   you run it.

## The Solution

```python
"""exercise-02-deduplicate-solution.py — one entry per human, order kept.

Three functions over a sign-up list. Two of them remove duplicates while
keeping the order people first appeared; the third reports the first repeat
it meets and stops there.

All three keep a `set` beside a `list` and use each for the one job it is
good at: the set answers "have I seen this?", the list remembers the order.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
SIGNUPS: list[str] = [
    "Ada@crunch.dev",
    "grace@crunch.dev",
    "ada@crunch.dev",
    "linus@crunch.dev",
    "grace@crunch.dev",
    "  ada@crunch.dev  ",
    " margaret@crunch.dev",
]


# ---- Your task ----
def dedupe(items: list[str]) -> list[str]:
    """Return a new list with exact duplicates removed, first-seen order kept.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        A new list holding the first sighting of each exact string.
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def dedupe_case_insensitive(items: list[str]) -> list[str]:
    """Return a new list deduplicated after stripping and lowercasing.

    The output keeps the ORIGINAL spelling of the first occurrence, not the
    normalised form used for comparison.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        A new list holding the first sighting of each normalised address,
        spelled the way it arrived.
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.strip().lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def first_duplicate(items: list[str]) -> str | None:
    """Return the first item that appears twice (exact match), or None.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        The repeated string, or None when nothing repeats.
    """
    seen: set[str] = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print(f"raw signups:        {len(SIGNUPS)}")
    print(f"exact dedupe:       {len(dedupe(SIGNUPS))}")
    print(f"normalised dedupe:  {len(dedupe_case_insensitive(SIGNUPS))}")
    print(f"first duplicate:    {first_duplicate(SIGNUPS)}")

    assert dedupe(SIGNUPS) == [
        "Ada@crunch.dev",
        "grace@crunch.dev",
        "ada@crunch.dev",
        "linus@crunch.dev",
        "  ada@crunch.dev  ",
        " margaret@crunch.dev",
    ]
    assert dedupe_case_insensitive(SIGNUPS) == [
        "Ada@crunch.dev",
        "grace@crunch.dev",
        "linus@crunch.dev",
        " margaret@crunch.dev",
    ]
    assert first_duplicate(SIGNUPS) == "grace@crunch.dev"
    assert first_duplicate(["a", "b", "c"]) is None
    assert dedupe([]) == []
    assert SIGNUPS[2] == "ada@crunch.dev"  # input list untouched
    print("All checks passed.")
```

**Two containers, two jobs.** `seen` answers one question — *have I met this
before?* — and a set answers it without reading through everything it holds.
`result` answers a different question — *what order did they arrive in?* — and
a list answers that just by being a list. Neither container does both jobs
well, so you use both. One pass over the input, one small extra bag of
strings, done.

**The alternative you were tempted by.** The tidier-looking version drops the
set entirely:

```python
if item not in result:          # reads through everything kept so far
    result.append(item)
```

It gets the right answer, and it turns a program that walks the list once into
a program that walks it again for every single item. See *Under the hood* for
what that costs measured on real data. The short version: two extra lines buy
you a function that still works on a file you have not seen yet.

**Check first, add second.**

```python
if item not in seen:
    seen.add(item)
    result.append(item)
```

That is the only order that works. Swap the two and every item is already in
`seen` by the time the `if` runs, so nothing is ever kept.

**Normalise the key, keep the value.** `dedupe_case_insensitive` differs from
`dedupe` by exactly one idea:

```python
key = item.strip().lower()      # what "the same" means
...
result.append(item)             # what the organisers get back
```

`seen` holds the tidied form, so `"ada@crunch.dev"` and `"  ada@crunch.dev  "`
collide with `"Ada@crunch.dev"`. The result holds the untouched original,
because a human typed that and will want it back. This split — compare on the
tidied version, store what arrived — is the shape of every case-insensitive
lookup and every import of messy rows you will ever write.

**`first_duplicate` returns from inside the loop.** That is what makes it stop
early instead of reading to the end. On `SIGNUPS` it stops at position four.
On a million-row log with a repeat on row two it stops on row two. The return
type is `str | None` because "nothing repeated" is a real answer, not an
error.

**Nothing here changes the input.** `seen` and `result` are new objects and
`items` is only read, which is what the `SIGNUPS[2] == "ada@crunch.dev"`
assert confirms.

**`dedupe([])` needs no special case.** The loop body never runs and `result`
is already `[]`. A guard like `if not items: return []` is a line that can
only ever be wrong.

## Download and run

Download
[exercise-02-deduplicate-solution.py](./exercise-02-deduplicate-solution.py)
and run it:

```bash
python exercise-02-deduplicate-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-02-deduplicate.py`.

## Common bugs to catch

- **`AttributeError: 'set' object has no attribute 'append'`.**

  ```text
  Traceback (most recent call last):
      seen.append(item)
      ^^^^^^^^^^^
  AttributeError: 'set' object has no attribute 'append'
  ```

  Sets take `.add()`; lists take `.append()`. The message always names the
  type you actually built, not the one you meant to.

- **`AttributeError: 'dict' object has no attribute 'add'`.**

  ```text
  Traceback (most recent call last):
      seen.add(item)
      ^^^^^^^^
  AttributeError: 'dict' object has no attribute 'add'
  ```

  You wrote `seen = {}`, which is an empty **dict**. There is no empty-set
  literal in Python — the braces went to dicts first — so an empty set is
  `set()`. Note that your type hint said `set[str]` and Python ran the line
  anyway: hints are a note to the reader, not a rule the interpreter enforces.

- **`exact dedupe:       0`.** You called `seen.add(item)` before the
  `if item not in seen` test, so everything is present by the time you check
  and nothing is ever kept. There is no exception, because there is nothing
  illegal about the code. It just answers the wrong question.

- **A bare `AssertionError` on the `dedupe_case_insensitive` check, with the
  four printed counts all correct.** You appended the normalised key instead
  of the original item:

  ```text
  raw signups:        7
  exact dedupe:       6
  normalised dedupe:  4
  first duplicate:    grace@crunch.dev
  Traceback (most recent call last):
      assert dedupe_case_insensitive(SIGNUPS) == [
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      ...<4 lines>...
      ]
      ^
  AssertionError
  ```

  Stare at that for a second. Every printed number is right. The count is
  right, the order is right, the *only* thing wrong is that
  `"Ada@crunch.dev"` came back as `"ada@crunch.dev"` and
  `" margaret@crunch.dev"` lost its space. Print the list when this bites —
  the counts will keep telling you everything is fine.

- **`first_duplicate` returns `"Ada@crunch.dev"` — the very first entry.** You
  filled `seen` in one loop and checked in a second:

  ```python
  for item in items:
      seen.add(item)
  for item in items:
      if item in seen:
          return item
  ```

  After the first loop everything is in `seen`, so the second loop matches on
  its very first try and returns the first element of the list. It does that
  on *any* non-empty input, whether or not anything repeats. The membership
  test has quietly stopped meaning "seen before now" and started meaning "seen
  at all", and those are different sentences. One pass: check, then add.

- **`first_duplicate` returns `"ada@crunch.dev"`.** You normalised in there
  too. With exact matching, the first repeat is the second plain
  `grace@crunch.dev`.

- **Exact dedupe returns 4 instead of 6.** You normalised inside `dedupe` as
  well. The two functions differ on purpose, so you can see what normalising
  costs and what it buys.

- **`TypeError: unhashable type: 'list'`.**

  ```text
  Traceback (most recent call last):
      seen.add(["a"])
      ~~~~~~~~^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  You ran this on a list of lists. A set can only hold things whose value
  cannot change underneath it — numbers, strings, tuples. Convert each inner
  list to a `tuple` first.

## Under the hood

<details>
<summary>Under the hood — what a hash table is, and why `in` on a set is instant</summary>

**Start with the list.** `x in some_list` has no clever trick available to it.
The list is a row of boxes in whatever order you put them, so Python starts at
box zero and compares, then box one, and so on until it finds `x` or runs out.
If the list holds `n` things, a miss costs `n` comparisons. That is called
**O(n)** — "grows in step with n".

**Now the set.** A set is a **hash table**, and a hash table is a coat check.

You hand your coat over. The attendant does not remember faces; instead they
run your ticket number through a fixed rule and that rule says which peg the
coat goes on. When you come back, they run the same rule on the same ticket
and walk straight to that peg. They never look at the other pegs. It does not
matter whether the cloakroom holds ten coats or ten thousand — it is one
calculation and one look.

Python's version of the ticket rule is `hash()`. Try it — this is one real
run, and **your numbers will be different**, for a reason the end of this
block explains:

```text
>>> hash("ada@crunch.dev")
5357092514651505165
>>> hash("ada@crunch.dev") % 8
5
```

The number is meaningless on its own; what matters is that the *same* string
always produces the *same* number within one run of Python. The set takes that
number, wraps it round to the size of its internal row of slots, and stores
the item there. `in` repeats the calculation and looks at that one slot. One
hash, one look, regardless of size. That is **O(1)** — "does not grow with n".

**What happens when two things land on the same peg.** They can — a hash table
with eight slots will eventually give two different strings the same slot, and
that is called a **collision**. CPython then probes on to another slot by a
fixed rule until it finds the item or an empty slot. Collisions make lookups
slightly slower, which is why the honest claim is "O(1) **on average**" rather
than "always one look". Python keeps the table less than about two-thirds
full, growing it and rehashing everything when it gets fuller than that, so
collisions stay rare in practice.

**Why sets cannot hold lists.** The peg is chosen from the value. If the value
could change after it was filed, the item would be sitting on the wrong peg
and could never be found again. So Python only allows **hashable** things in a
set: numbers, strings, tuples of hashable things, `frozenset`. A list can
change, so `hash([1, 2])` raises `TypeError: unhashable type: 'list'` rather
than letting you file something that will get lost.

**Why the output order of a set is not fixed.** The order you get when you
loop over a set is the order of the pegs, which depends on the hash numbers.
For strings, CPython deliberately mixes a random value into the hash at
startup — this is on by default and can be turned off with
`PYTHONHASHSEED=0` — so the same set can iterate in a different order in two
different runs. That randomisation exists as a defence: without it, an
attacker who can choose the strings your server stores could pick thousands
that all collide and turn every lookup into a linear scan. Fixing an ordering
bug and fixing a security hole happen to be the same change.

**The measurement.** Deduplicating 20,000 unique addresses, CPython 3.13.2:

```text
python     : 3.13.2
n          : 20000 unique addresses
seen set   : 0.0030 s
seen list  : 1.6129 s
ratio      : 536x
```

Reproduce it with `timeit`:

```python
import timeit

SETUP = """
items = [f"user{i}@crunch.dev" for i in range(20_000)]

def dedupe_set(items):
    seen, result = set(), []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def dedupe_list(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result
"""

print(timeit.timeit("dedupe_set(items)",  setup=SETUP, number=5) / 5)
print(timeit.timeit("dedupe_list(items)", setup=SETUP, number=5) / 5)
```

The absolute numbers depend on your machine. The shape does not: double the
input and the set version takes twice as long, while the list version takes
four times as long. That is the difference between O(n) and O(n²), and it is
why the ratio gets *worse* the more data you have, not better.

**Dicts are the same machine.** A dict is a hash table where each peg also
holds a value beside the key. That is why `key in some_dict` is just as fast
as `x in some_set`, why dict keys have the same hashable-only rule, and why
the next exercise's counting dict is cheap. One data structure, two faces.

</details>

## Acceptance checklist

- [ ] `python exercise-02-deduplicate.py` prints four lines then `All checks passed.`
- [ ] Both dedupers use a `set` for the "have I seen this?" test.
- [ ] The word `sort` appears nowhere in the file.
- [ ] `SIGNUPS` is unchanged after every function has run.
- [ ] `dedupe([])` works with no `if not items` special case.
- [ ] `dedupe_case_insensitive` appends `item`, never `key`.
- [ ] Type hints on all three signatures, `str | None` included.
- [ ] Committed to Git with a message like `Add Week 5 exercise 2: deduplicate`.

## Stretch

- **The `dict.fromkeys` one-liner.**

  ```python
  def dedupe_fromkeys(items: list[str]) -> list[str]:
      """Deduplicate preserving first-seen order, using dict key ordering."""
      return list(dict.fromkeys(items))
  ```

  ```text
  fromkeys matches dedupe: True
  ```

  `dict.fromkeys(items)` builds a dict using each item as a key. Duplicate
  keys collapse, and dicts have remembered insertion order since Python 3.7,
  so the keys come back in first-seen order. Same cost, same answer, one line.

  Which should you write? The one-liner when you want an exact-match dedupe
  and nothing else. The explicit loop the moment "the same" stops meaning
  `==`, because `fromkeys` gives you nowhere to put a key function. Reach for
  the one-liner knowing you may have to unfold it later.

- **`dedupe_by(items, key)` — let the caller decide what "the same" means.**

  ```python
  from collections.abc import Callable


  def dedupe_by(
      items: list[str],
      key: Callable[[str], str] = lambda item: item,
  ) -> list[str]:
      """Deduplicate on `key(item)`, keeping the first item of each key."""
      seen: set[str] = set()
      result: list[str] = []
      for item in items:
          marker = key(item)
          if marker not in seen:
              seen.add(marker)
              result.append(item)
      return result
  ```

  ```text
  dedupe_by identity     : True
  dedupe_by normalised   : ['Ada@crunch.dev', 'grace@crunch.dev', 'linus@crunch.dev', ' margaret@crunch.dev']
  ```

  Both of today's functions collapse into this one: `dedupe_by(items)` is
  `dedupe`, and `dedupe_by(items, key=lambda s: s.strip().lower())` is
  `dedupe_case_insensitive`. The default is a function that hands back what it
  was given, so the common case stays a one-argument call — the same design
  `sorted`, `min` and `max` use, and now you know why they use it.

  One note on the signature. `Callable[[str], str]` reads "takes one `str`,
  returns a `str`". Writing a type hint for a parameter that holds a function
  is not something the course has shown you yet, so drop the import and leave
  `key` unannotated if you would rather stay inside what you have been taught.
  The code runs identically either way.

- **`all_duplicates(items)` — every value that appeared more than once, listed
  once each.**

  ```python
  def all_duplicates(items: list[str]) -> list[str]:
      """Return each repeated value once, in the order it was first repeated."""
      seen: set[str] = set()
      reported: set[str] = set()
      result: list[str] = []
      for item in items:
          if item in seen and item not in reported:
              reported.add(item)
              result.append(item)
          seen.add(item)
      return result
  ```

  ```text
  all_duplicates         : ['grace@crunch.dev']
  all_duplicates twice   : ['a', 'b']
  ```

  Two sets, because there are two different questions. `seen` is "has this
  appeared before", `reported` is "have I already listed it". Without the
  second, a value appearing three times gets listed twice. Test it on
  `["a", "b", "a", "a", "b", "c"]`, where `a` appears three times and should
  come back once.

When both dedupers agree with the asserts, move on to
[Exercise 3 — Word Frequency](./exercise-03-word-frequency.md).
