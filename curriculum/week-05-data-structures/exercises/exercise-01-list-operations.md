# Exercise 1 — List Operations

> **Topic:** putting a list in order with `sorted(key=...)`, picking one winner with `max(key=...)`, and taking the first few with a slice
> **Lecture:** [01 — Lists and Tuples](../lecture-notes/01-lists-and-tuples.md)
> **Difficulty:** Beginner
> **Target time:** 60 minutes
> **Why this one:** almost every program you write from here on ends with the same three questions — put these in order, give me the biggest one, give me the first few. If `sorted` with a key and a slice are not automatic, you will write loops inside loops instead, and loops inside loops are where beginner code gets slow. This page also drills the difference between `list.sort()` and `sorted()`, which is the most common way beginners end up holding `None` and not knowing why.

## The Brief

The Code Crunch community runs short study sessions in three cities. Someone
has been keeping notes in a spreadsheet, and you have been handed the rows.
Each row says four things: what the session was called, which city it ran in,
how many minutes it lasted, and how many people turned up.

Each row arrives as a **record** — a `namedtuple`. Think of a plain tuple as a
row of boxes with no labels, so you have to remember that box number 3 holds
the attendance. A `namedtuple` is the same row of boxes with a **name written
on each one**. You write `s.attendees` and get the attendance. You never have
to remember which box was which.

You are writing the reporting layer. The organisers want three things:

- a **leaderboard** — every session in order, best attended first,
- the **single longest** session, for a note about how much time people will
  actually sit still for,
- the **top three titles**, for the newsletter, plus how many minutes those
  three add up to.

None of that is hard. But each of the three has an obvious wrong way to get
it, and this exercise is built so that the wrong ways fail loudly rather than
quietly.

One detail decides two of the four answers: **the ranking is by attendance,
not by length.** The three best-attended sessions are not the three longest
ones. A function that quietly ranks by the wrong field still returns three
sessions and a plausible number of minutes, which is exactly how a wrong
answer survives a glance.

## Starter

Create `exercise-01-list-operations.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""exercise-01-list-operations.py — the study-session leaderboard.

Rank, search, and slice a list of session records without rearranging the
list you were given.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import namedtuple

# ---- Given data ----
Session = namedtuple("Session", ["title", "city", "minutes", "attendees"])

SESSIONS: list[Session] = [
    Session("Intro to Loops", "Lagos", 90, 42),
    Session("Debugging Clinic", "Nairobi", 60, 17),
    Session("List Comprehensions", "Lagos", 120, 35),
    Session("Git Basics", "Accra", 45, 58),
    Session("Dict Patterns", "Nairobi", 75, 35),
    Session("Reading Tracebacks", "Accra", 30, 23),
]


# ---- Your task ----
def sort_by_attendees(sessions: list[Session]) -> list[Session]:
    """Return a NEW list ordered by attendance, highest first.

    Args:
        sessions: The session records to rank. This list is not modified.

    Returns:
        A new list, most attendees first, ties broken by title A to Z.
    """
    # TODO: sorted() with ONE key that handles both rules
    ...


def longest_session(sessions: list[Session]) -> Session:
    """Return the single session with the most minutes.

    Args:
        sessions: The session records to search.

    Returns:
        The whole record, not just its title or its minutes.
    """
    # TODO: max() with a key. Do not sort.
    ...


def top_three_titles(sessions: list[Session]) -> list[str]:
    """Return the titles of the three best-attended sessions, in rank order.

    Args:
        sessions: The session records to rank.

    Returns:
        Three title strings, best attended first.
    """
    # TODO: rank, slice the first three, then pull out .title
    ...


def total_minutes_of_top(sessions: list[Session], n: int) -> int:
    """Return the combined minutes of the n best-attended sessions.

    Args:
        sessions: The session records to rank.
        n: How many of the top-ranked sessions to add up.

    Returns:
        The sum of those sessions' minutes.
    """
    # TODO: rank, slice, then add up the minutes
    ...


# ---- Self-check ----
if __name__ == "__main__":
    ranked = sort_by_attendees(SESSIONS)
    for s in ranked:
        print(f"{s.attendees:3d}  {s.title} ({s.city})")

    assert [s.title for s in ranked[:3]] == ["Git Basics", "Intro to Loops", "Dict Patterns"]
    assert ranked[-1].title == "Debugging Clinic"
    assert longest_session(SESSIONS).title == "List Comprehensions"
    assert longest_session(SESSIONS).minutes == 120
    assert top_three_titles(SESSIONS) == ["Git Basics", "Intro to Loops", "Dict Patterns"]
    assert total_minutes_of_top(SESSIONS, 3) == 210
    assert SESSIONS[0].title == "Intro to Loops"  # original list untouched
    print("All checks passed.")
```

Five words you need before you start.

**Key function.** `sorted(sessions, key=...)` does not compare the records
themselves. It calls your little function on each record, gets one value back,
and compares *those*. The key is how you say "order these by this bit of
them".

**`lambda`.** A `lambda` is a function with no name, written on one line.
`lambda s: s.minutes` means "given one session, hand back its minutes". You
have already met the idea in Week 4; this is the short spelling for when the
function is one expression long and only used once.

**In place.** A method that works *in place* rearranges the thing you gave it
rather than building you a new one. `list.sort()` is in place. `sorted()` is
not — it leaves the original alone and hands you a new list.

**Slice.** `ranked[:3]` means "a new list holding the first three". The number
after the colon is where to stop. A slice never goes out of range: ask for the
first ninety-nine of six things and you get all six, with no error.

**Stable.** A sort is **stable** when two things that tie stay in the order
they arrived. Python's sort is stable. That sounds helpful, and on this page
it is the trap — see the expected output.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/exercises/exercise-01-list-operations.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `sort_by_attendees` returns a **new** list, highest attendance first, ties
   broken by title A to Z. `SESSIONS` is in its original order afterwards.
2. `longest_session` returns the whole `Session` record — not the minutes,
   not the title.
3. `top_three_titles` returns exactly three strings, in leaderboard order.
4. `total_minutes_of_top(SESSIONS, 3)` returns `210`. That is `45 + 90 + 75`,
   the minutes of the three best **attended** sessions, not the three longest.
5. The printed rows use `f"{s.attendees:3d}  {s.title} ({s.city})"` exactly:
   the number padded to three characters, two spaces, then the title, then the
   city in brackets.
6. Every function keeps its type hints and its docstring.

## Constraints

- **Use `sorted()`, never `sessions.sort()`.** `.sort()` rearranges the
  caller's own list and hands back `None`. Your function was given the list
  the rest of the program is still using, so shuffling it behind the caller's
  back is a bug even when the value you return looks right. The last assert on
  the page exists to catch exactly this.

- **Handle both sort rules in one key: `(-s.attendees, s.title)`.** Python
  compares tuples left to right and stops at the first difference, so that one
  key says the whole rule: most attendees first, and where two sessions tie,
  the earlier title. Sorting twice — once by title, then again by attendance —
  gets the same answer here, but it is two full passes instead of one, and it
  falls apart the day one of your two rules needs the opposite direction.

- **Negate the number you want descending. Leave `reverse` alone.**
  `reverse=True` flips the *whole* key, so it would sort attendance downwards
  **and** titles Z to A, and the tied pair would come out backwards. A minus
  sign on one number lets you mix the two directions in a single pass. Only
  numbers negate, which is why the title stays as it is.

- **Find the maximum with `max()`, not `sorted(...)[0]` and not a loop inside
  a loop.** `max` walks the list once, holding the best it has seen. Sorting
  puts all six in order so you can read one and throw five away. With six
  sessions you cannot feel the difference; with a hundred thousand, sorting
  does roughly seventeen times the work of a single walk, for the same one
  answer. Comparing every session against every other is worse again — a
  hundred thousand sessions would mean ten billion comparisons for something a
  single walk answers.

- **Slice, do not loop and count.** `ranked[:3]` is one expression. The same
  three items built with a counter and a `break` is four lines that can be off
  by one, and slicing already handles "there are only two" without a guard.

- **Read fields by name.** `s.attendees`, never `s[3]`. That is the entire
  reason this data is a `namedtuple` and not a plain tuple. Note what this
  rule does *not* ban: `SESSIONS[0]` and `ranked[-1]` in the self-check are
  picking a record out of a list, which is fine. Reaching into a record by
  position is what you are avoiding.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-list-operations.py
 58  Git Basics (Accra)
 42  Intro to Loops (Lagos)
 35  Dict Patterns (Nairobi)
 35  List Comprehensions (Lagos)
 23  Reading Tracebacks (Accra)
 17  Debugging Clinic (Nairobi)
All checks passed.
```

Look at rows three and four. Both sessions drew 35 people, and `Dict Patterns`
comes first because `D` comes before `L`. If `List Comprehensions` is on top
instead, your key has one part where it needs two — the stable sort left the
tied pair in the order they sat in `SESSIONS`, and that order is the wrong
one.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python exercise-01-list-operations.py`. You get a `TypeError` on the first
   line that uses a result. That is the correct starting point, not a problem
   — it proves the self-check is real.
2. Fill in `sort_by_attendees` first. The other three lean on it.
3. Run again and read the printed table before you read the asserts. Does the
   order match the expected output, line for line?
4. Fill in `longest_session`. Before you add the `key`, try `max(SESSIONS)`
   with no key on purpose, and work out why that particular record came back.
   The answer is in *Common bugs to catch* if you get stuck, but guess first.
5. Fill in `top_three_titles` and `total_minutes_of_top`. Both are "rank,
   slice, then take what you need" — and the ranking function already exists,
   so neither of them should contain the word `sorted`.
6. When `All checks passed.` prints, open a REPL with
   `python -i exercise-01-list-operations.py` and try the same functions on
   records you invent yourself. Two sessions with the same attendance and
   titles you choose is the fastest way to convince yourself the tie-break is
   really doing something.

## The Solution

```python
"""exercise-01-list-operations-solution.py — the study-session leaderboard.

Four small reporting functions over a list of session records. One ranks,
one picks the longest, two slice the ranking down to a headline.

None of them rearranges the list the caller handed in.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import namedtuple

# ---- Given data ----
Session = namedtuple("Session", ["title", "city", "minutes", "attendees"])

SESSIONS: list[Session] = [
    Session("Intro to Loops", "Lagos", 90, 42),
    Session("Debugging Clinic", "Nairobi", 60, 17),
    Session("List Comprehensions", "Lagos", 120, 35),
    Session("Git Basics", "Accra", 45, 58),
    Session("Dict Patterns", "Nairobi", 75, 35),
    Session("Reading Tracebacks", "Accra", 30, 23),
]


# ---- Your task ----
def sort_by_attendees(sessions: list[Session]) -> list[Session]:
    """Return a NEW list ordered by attendance, highest first.

    Args:
        sessions: The session records to rank. This list is not modified.

    Returns:
        A new list, most attendees first, ties broken by title A to Z.
    """
    return sorted(sessions, key=lambda s: (-s.attendees, s.title))


def longest_session(sessions: list[Session]) -> Session:
    """Return the single session with the most minutes.

    Args:
        sessions: The session records to search.

    Returns:
        The whole record, not just its title or its minutes.
    """
    return max(sessions, key=lambda s: s.minutes)


def top_three_titles(sessions: list[Session]) -> list[str]:
    """Return the titles of the three best-attended sessions, in rank order.

    Args:
        sessions: The session records to rank.

    Returns:
        Three title strings, best attended first.
    """
    return [s.title for s in sort_by_attendees(sessions)[:3]]


def total_minutes_of_top(sessions: list[Session], n: int) -> int:
    """Return the combined minutes of the n best-attended sessions.

    Args:
        sessions: The session records to rank.
        n: How many of the top-ranked sessions to add up.

    Returns:
        The sum of those sessions' minutes.
    """
    return sum(s.minutes for s in sort_by_attendees(sessions)[:n])


# ---- Self-check ----
if __name__ == "__main__":
    ranked = sort_by_attendees(SESSIONS)
    for s in ranked:
        print(f"{s.attendees:3d}  {s.title} ({s.city})")

    assert [s.title for s in ranked[:3]] == ["Git Basics", "Intro to Loops", "Dict Patterns"]
    assert ranked[-1].title == "Debugging Clinic"
    assert longest_session(SESSIONS).title == "List Comprehensions"
    assert longest_session(SESSIONS).minutes == 120
    assert top_three_titles(SESSIONS) == ["Git Basics", "Intro to Loops", "Dict Patterns"]
    assert total_minutes_of_top(SESSIONS, 3) == 210
    assert SESSIONS[0].title == "Intro to Loops"  # original list untouched
    print("All checks passed.")
```

**The key is a tuple, and the tuple is the whole rule.**

```python
key=lambda s: (-s.attendees, s.title)
```

Read it as one English sentence: *most attendees first, and when two tie, the
earlier title.* Python compares the two tuples box by box and stops the moment
they differ. `Dict Patterns` and `List Comprehensions` both drew 35, so their
first boxes match, so Python moves to the second box, and `"Dict Patterns"
< "List Comprehensions"` settles it.

**The minus sign is the direction switch.** Attendance wants to go downwards
and titles want to go upwards, in one pass. Negating the number flips just
that one comparison. This is the general move and it is worth memorising:
negate the field you want descending, and leave `reverse` alone.

**`sorted` versus `.sort()` is not a style choice.** `sessions.sort(...)`
rearranges the list object you were handed — and you were handed `SESSIONS`
itself, not a copy — then returns `None`. `sorted` builds a new list and
leaves yours alone. The last assert, `SESSIONS[0].title == "Intro to Loops"`,
is there for no other reason.

**`max` needs a key for the same reason `sorted` does.** Without one, Python
compares the records themselves. A `namedtuple` *is* a tuple, so it compares
box by box, and box zero is the title — which is why `max(SESSIONS)` hands
back `Reading Tracebacks`, the alphabetically last title and the *shortest*
session in the list. That is not a bug in `max`. It is `max` answering a
different question perfectly.

**Both slicing functions rank first, then slice.** The order matters, and so
does the fact that neither of them re-does the sorting: they call
`sort_by_attendees`, which already knows the rule. The moment two functions
both claim to know how the leaderboard is ordered, one of them will eventually
be wrong.

**`total_minutes_of_top` puts a generator expression inside `sum`.**
`sum(s.minutes for s in ...)` with no square brackets adds the numbers as they
come. With brackets Python would build a throwaway list of three integers
first. With three items nobody cares; the habit is what you are building, and
Exercise 5 comes back to it.

**A slice never needs a guard.** `[:3]` on a list of two gives you two.
`[:99]` gives you everything. `[:0]` gives you nothing. Compare `ranked[99]`,
which raises `IndexError: list index out of range`. Slices clamp, indexes
raise — which is why the stretch version with a configurable `n` needs no
defensive code.

## Download and run

Download
[exercise-01-list-operations-solution.py](./exercise-01-list-operations-solution.py)
and run it:

```bash
python exercise-01-list-operations-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-01-list-operations.py`.

## Common bugs to catch

- **`TypeError: 'NoneType' object is not iterable`.** You wrote
  `return sessions.sort(...)`:

  ```text
  Traceback (most recent call last):
      for s in ranked:
               ^^^^^^
  TypeError: 'NoneType' object is not iterable
  ```

  `.sort()` sorts in place and hands back `None`, so your function returned
  `None` and the self-check tried to loop over nothing. The message says
  *iterable* because `for s in ranked:` is the first line that touches the
  result. If you slice before you loop you get the sibling message,
  `TypeError: 'NoneType' object is not subscriptable`. Both mean the same
  thing: a method that rearranges gave you `None`, and you kept it. The
  second, quieter half of this bug is that `SESSIONS` really did get
  reordered — even if you patch the return value by adding `return sessions`,
  the caller's list is now wrong.

- **A bare `AssertionError` on the `longest_session` check.** You called
  `max(SESSIONS)` with no `key`. There is no traceback from `max` itself,
  because comparing two records is perfectly legal. In a REPL:

  ```text
  >>> max(SESSIONS)
  Session(title='Reading Tracebacks', city='Accra', minutes=30, attendees=23)
  ```

  Thirty minutes is the *shortest* session there is. Any time a `max` or a
  `sorted` over records gives you an answer that looks alphabetical, you
  forgot the `key`.

- **`TypeError: bad operand type for unary -: 'str'`.** You negated the title
  as well as the attendance:

  ```text
  Traceback (most recent call last):
      sorted(sessions, key=lambda s: (-s.attendees, -s.title))
                                                    ^^^^^^^^
  TypeError: bad operand type for unary -: 'str'
  ```

  Only numbers negate. You do not want the title reversed anyway — the rule
  asks for A to Z, which is what an un-negated string already gives you.

- **`AttributeError: 'Session' object has no attribute 'attendee'`.** A
  singular-plural typo. Python 3.13 offers you the fix in the message itself:

  ```text
  AttributeError: 'Session' object has no attribute 'attendee'. Did you mean: 'attendees'?
  ```

  This is the payoff of `namedtuple`. Had the records been plain tuples and
  you had written `s[4]`, you would have got `IndexError: tuple index out of
  range`, which does not tell you what you meant.

- **`AttributeError: can't set attribute`.** You tried `s.attendees = 0`:

  ```text
  Traceback (most recent call last):
      s.attendees = 0
      ^^^^^^^^^^^
  AttributeError: can't set attribute
  ```

  Tuples cannot be changed after they are made, and a `namedtuple` inherits
  that. Use `s._replace(attendees=0)`, which hands you a changed copy and
  leaves the original alone.

- **`total_minutes_of_top` returns `285`.** You added up the three *longest*
  sessions instead of the three *best attended*. Both numbers are the sum of
  three sessions' minutes, so neither looks obviously wrong — which is why the
  assert names the number rather than trusting your eye. "Top" here means top
  of the leaderboard, and the leaderboard is attendance. Rank, slice, add, in
  that order, using the ranking function you already wrote.

- **`List Comprehensions` prints above `Dict Patterns`.** Your key is
  `key=lambda s: s.attendees, reverse=True` and the tie fell where it fell. A
  stable sort keeps tied items in the order they arrived, and in `SESSIONS`
  that order puts `List Comprehensions` first. You got *an* answer; you did
  not get the one the rule asks for.

## Under the hood

<details>
<summary>Under the hood — what a key function really does, and why the sort is stable</summary>

**The key is called once per item, not once per comparison.**

That surprises people, so it is worth seeing. When you write
`sorted(sessions, key=f)`, CPython does not call `f` every time it compares
two records. It walks the list once, calls `f` on each item, and builds an
internal array of `(key, item)` pairs. Then it sorts that array by key alone.
Then it throws the keys away and hands you the items.

The pattern has a name — **decorate, sort, undecorate** — and before `key=`
existed in Python 2.4 you wrote it by hand:

```python
decorated = [(-s.attendees, s.title, s) for s in sessions]
decorated.sort()
result = [s for _, _, s in decorated]
```

Two consequences follow from "once per item", and both matter in real code.

First, an expensive key is fine. If your key has to hit a database or parse a
date, it happens `n` times, not `n log n` times.

Second, the key must be *comparable*, and the item never has to be. That is
why sorting a list of records with no key at all falls back to comparing the
records themselves — and why it works, silently, on `namedtuple`s.

**Timsort, and why stability is free here.**

Python's sort is **Timsort**, written for CPython in 2002 by Tim Peters. It
looks for stretches that are already in order — real data is full of them —
and merges those stretches together. On a list that is already sorted it does
a single pass and stops. In the worst case it is `O(n log n)`, the same as any
good sort, and it never degrades the way a naive quicksort can.

**Stable** means: when two items compare equal, the one that was earlier in
the input stays earlier in the output. Timsort gets this by only ever merging
adjacent runs and always preferring the left side on a tie. It is not an extra
step; it falls out of how the merge works.

Stability is genuinely useful. It is what lets you sort by one thing, then by
another, and keep the first ordering inside groups of the second:

```python
sessions.sort(key=lambda s: s.title)        # then
sessions.sort(key=lambda s: -s.attendees)   # ties keep title order
```

That gives the same answer as the tuple key on this page. So why does the page
forbid it? Because it is two full sorts instead of one, and because it reads
backwards — the *last* sort you write is the *first* rule that applies, which
is a fact you have to remember rather than read. And it stops working the
moment one of the two rules needs the opposite direction, since the earlier
sort cannot be flipped independently. One key says the whole rule in one
place, in the order you would say it out loud.

**`min` and `max` are the same function with the comparison flipped.** Both
take the same `key` argument, both make one pass, both hold a single current
best. Learning one teaches you the other. Both also raise
`ValueError: max() iterable argument is empty` on an empty list — worth
knowing before you call `max` on something a file gave you.

</details>

## Acceptance checklist

- [ ] `python exercise-01-list-operations.py` prints six rows then `All checks passed.`
- [ ] The table matches the expected output character for character.
- [ ] `SESSIONS` is in its original order after every function has run.
- [ ] `longest_session` uses `max()` with a key — no sort, no loop.
- [ ] No record is read by position anywhere in your four functions.
- [ ] `top_three_titles` and `total_minutes_of_top` call `sort_by_attendees`
      instead of sorting again.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 5 exercise 1: list operations`.

## Stretch

- **Sort by city, then by attendance inside each city.**

  ```python
  def sort_by_city_then_attendees(sessions: list[Session]) -> list[Session]:
      """Return a new list grouped by city A to Z, best attended first within each."""
      return sorted(sessions, key=lambda s: (s.city, -s.attendees))
  ```

  ```text
  Accra    58  Git Basics
  Accra    23  Reading Tracebacks
  Lagos    42  Intro to Loops
  Lagos    35  List Comprehensions
  Nairobi  35  Dict Patterns
  Nairobi  17  Debugging Clinic
  ```

  Same tuple trick, different fields — and notice the minus sign moved. City
  upwards, attendance downwards, one pass. Nothing about the mechanism
  changed, which is the sign you learned a pattern rather than an answer.

- **Add `shortest_session` with `min()`.**

  ```python
  def shortest_session(sessions: list[Session]) -> Session:
      """Return the single session with the fewest minutes."""
      return min(sessions, key=lambda s: s.minutes)
  ```

  ```text
  shortest: Reading Tracebacks 30
  ```

  Confirm for yourself that `min` takes exactly the same `key` argument as
  `max` and is exactly as cheap.

- **Give the top-titles function a configurable `n`, and find out what a slice
  does when `n` is too big.**

  ```python
  def top_titles(sessions: list[Session], n: int = 3) -> list[str]:
      """Return the titles of the n best-attended sessions, in rank order."""
      return [s.title for s in sort_by_attendees(sessions)[:n]]
  ```

  ```text
  top 2   : ['Git Basics', 'Intro to Loops']
  top 99  : 6 titles
  top 0   : []
  ```

  No guard needed, and that is the finding. Then try `ranked[99]` in the REPL
  and read the `IndexError`. Slices clamp; indexes raise. That difference is
  worth one line of your notes.

When your leaderboard is right, move on to
[Exercise 2 — Deduplicate](./exercise-02-deduplicate.md).
