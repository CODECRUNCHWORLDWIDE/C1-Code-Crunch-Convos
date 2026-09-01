# Homework Problem 3 — Two-Sum (classic)

> **Topic:** turning a search into a lookup, and why `if i:` is not the same question as `if i is not None:`
> **Lecture:** [02 — Sets and Dictionaries](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** it is the most-asked interview question in the world, and the reason is not the answer — it is that the obvious solution and the good solution look equally short, so the only thing separating them is whether you noticed that a dict can remember for you. Getting this once rewires how you look at every loop-inside-a-loop you ever write again.

## The Brief

You are given a list of numbers and a target total.

```python
nums = [2, 7, 11, 15]
t = 9
```

Somewhere in that list are two numbers that add up to the target. Here it is the
`2` and the `7`. Find them, and give back **where they were**, not what they
were:

```python
two_sum([2, 7, 11, 15], 9)
# (0, 1)
```

`(0, 1)` means "position 0 and position 1". Positions, because in a real
program the list is usually a row of prices or scores and what you actually need
is which two rows, not which two numbers.

Write one function.

```python
def two_sum(nums: list[int], t: int) -> tuple[int, int] | None:
    ...
```

```python
two_sum([2, 7, 11, 15], 9)    # (0, 1)
two_sum([3, 2, 4], 6)         # (1, 2)
two_sum([1, 2, 3], 100)       # None
```

Three rules:

- The two positions must be **different**, and the smaller one comes first. A
  number is not allowed to pair with itself.
- When no pair reaches the target, return `None`.
- There is at most one answer in any list you are given.

**And one rule that is the actual problem.** The obvious version compares every
number with every other number. On a list of 5,000 that is more than twelve
million comparisons, and on 10,000 it is four times as many again. Your version
must look at each number **once**.

That sounds impossible until you change the question you are asking. Instead of
"do these two numbers add up?", ask, of each number in turn: *"have I already
walked past the number that would finish this pair?"* If you are standing on a
`7` and the target is `9`, the only number that can help you is a `2`. You do
not need to go looking for it. You need to have **remembered** whether you have
seen one.

That memory is a dict. The brief even names it: `seen: dict[int, int]`, mapping
each number to the position you found it at.

## Starter

Save this in your `homework/` folder as part of `week-05-solutions.py` and fill
in the `TODO`s. It runs as pasted — it just never finds anything:

```python
"""Week 5 homework, problem 3: find the two positions that reach a target."""


def two_sum(nums: list[int], t: int) -> tuple[int, int] | None:
    """Return the indices (i, j), i < j, with nums[i] + nums[j] == t.

    Args:
        nums: The numbers to search. May be empty.
        t: The total the two numbers must reach.

    Returns:
        The pair of indices, or None when no pair reaches ``t``.

    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        (0, 1)
    """
    seen: dict[int, int] = {}
    for j, num in enumerate(nums):
        # TODO 1: what number would finish this pair? Look it up in `seen`.
        # TODO 2: if it is there, return its position and this one, in order.
        # TODO 3: only then, remember this number and where it was.
        pass
    return None


def _demo() -> None:
    """Print the brief's three examples."""
    print(two_sum([2, 7, 11, 15], 9))
    print(two_sum([3, 2, 4], 6))
    print(two_sum([1, 2, 3], 100))


if __name__ == "__main__":
    _demo()
```

`enumerate(nums)` hands you the position and the number together, so you never
have to write `nums[j]`. Run this once if you have not met it:

```python
print(list(enumerate([2, 7, 11])))
```

```text
[(0, 2), (1, 7), (2, 11)]
```

The order of TODO 2 and TODO 3 is not a suggestion. Doing them the other way
round is a bug, and *Common bugs to catch* shows what it looks like.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/homework/problem-03-two-sum-classic.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `two_sum(nums, t)` returns a **tuple** `(i, j)` with `i < j` and
   `nums[i] + nums[j] == t`.
2. It returns `None` when no such pair exists, including for an empty list.
3. A number never pairs with itself: `two_sum([3], 6)` is `None`.
4. A repeated value is still two positions: `two_sum([3, 3], 6)` is `(0, 1)`.
5. Each number is looked at once. No nested loops, and no `in` test against the
   list.
6. Type hints on the signature and a docstring on the function.
7. These four asserts pass:

   ```python
   assert two_sum([2, 7, 11, 15], 9) == (0, 1)
   assert two_sum([3, 2, 4], 6) == (1, 2)
   assert two_sum([1, 2, 3], 100) is None
   assert two_sum([], 5) is None
   ```

## Constraints

- **Look up before you record.** The lookup asks "did I see the partner
  *earlier*?", and that is only true while `seen` holds nothing from the current
  turn. Swap the two lines and a lone `3` finds itself.
- **Test with `is not None`, never with `if i:`.** `seen.get(...)` gives back a
  **position**, and position `0` is falsy. `if i:` breaks every case whose
  answer involves the first element — including the brief's own first example.
- **Return a tuple, not a list.** `[0, 1] != (0, 1)`, so the assert fails on an
  answer that prints almost identically.
- **No `nums.index(...)`, no `x in nums`.** Both walk the whole list, so calling
  either inside your loop puts you straight back to comparing everything with
  everything — the thing requirement 5 forbids.
- **`_demo` prints; `two_sum` does not.**

## Expected output

```text
$ python problem-03-two-sum-classic-solution.py
(0, 1)
(1, 2)
None
(0, 1)
None
All 8 asserts passed.
```

The first three lines are the brief's examples. The last two are the ones that
catch the two classic bugs: `two_sum([3, 3], 6)` must find two *positions* even
though the value repeats, and `two_sum([3], 6)` must refuse to pair a number
with itself.

And here is the cost difference, measured rather than asserted. Both versions
were given 5,000 numbers arranged so that the answer is the very last pair, so
neither one can stop early:

```text
python      : 3.13.2
n           : 5000  (only the final pair reaches the target)
naive O(n^2): 0.398 s   (best of 5)
dict  O(n)  : 0.00045 s   (best of 5 x 50)
ratio       : 881x
```

The setup for that measurement is in the first *Under the hood* block, along
with what happens when you double `n`.

## Steps

1. Save the Starter into `week-05-solutions.py` and run it. Three `None`s.
2. Do the trace on paper before you write any code. Target 9, list
   `[2, 7, 11, 15]`:

   | `j` | `num` | needs | seen so far | what happens |
   |---|---|---|---|---|
   | 0 | 2 | 7 | `{}` | not there — record `2 -> 0` |
   | 1 | 7 | 2 | `{2: 0}` | **there, at 0** — return `(0, 1)` |

   Two turns of the loop, one dict lookup each. That is the whole algorithm.
3. Write TODO 1: `i = seen.get(t - num)`.
4. Write TODO 2: `if i is not None: return (i, j)`.
5. Write TODO 3: `seen.setdefault(num, j)`, on the line *after* the `if`.
6. Run it. You want `(0, 1)`, `(1, 2)`, `None`.
7. Add the four required asserts, then add these two, which are the ones that
   matter:

   ```python
   assert two_sum([3, 3], 6) == (0, 1)
   assert two_sum([3], 6) is None
   ```

8. Break it on purpose. Change `if i is not None:` to `if i:` and run the
   asserts again. The first one fails and the second and third still pass —
   which is exactly why this bug survives careless testing.
9. Put it back, compare with **The Solution**, tick the acceptance checklist,
   and commit: `git commit -m "Week 5 homework: two-sum"`.

## The Solution

```python
"""Find the two numbers that add up to a target, in one pass.

Week 5 homework, problem 3, Code Crunch Convos.

Add ``two_sum`` to your own ``week-05-solutions.py``. This file is the published
answer, and the longer name keeps it from landing on top of your work.

The slow way asks, of every pair, "do these two add up?". This way asks one
question per number instead: "have I already walked past the number that would
finish this pair?". That question is a dict lookup, so the whole search is one
pass over the list.
"""


def two_sum(nums: list[int], t: int) -> tuple[int, int] | None:
    """Return the indices (i, j), i < j, with nums[i] + nums[j] == t.

    Args:
        nums: The numbers to search. May be empty.
        t: The total the two numbers must reach.

    Returns:
        The pair of indices, or None when no pair reaches ``t``. When several
        pairs would work, the one that finishes earliest wins.

    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        (0, 1)
    """
    seen: dict[int, int] = {}
    for j, num in enumerate(nums):
        i = seen.get(t - num)
        if i is not None:
            return (i, j)
        seen.setdefault(num, j)
    return None


def _check() -> None:
    """Run the four asserts the brief requires, plus four it implies."""
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert two_sum([1, 2, 3], 100) is None
    assert two_sum([], 5) is None
    assert two_sum([3, 3], 6) == (0, 1)
    assert two_sum([3], 6) is None
    assert two_sum([0, 0], 0) == (0, 1)
    assert two_sum([-3, 4, 3, 90], 0) == (0, 2)


def _demo() -> None:
    """Print the brief's three examples, then the two that catch the bugs."""
    print(two_sum([2, 7, 11, 15], 9))
    print(two_sum([3, 2, 4], 6))
    print(two_sum([1, 2, 3], 100))
    print(two_sum([3, 3], 6))
    print(two_sum([3], 6))
    print("All 8 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
```

**Why it works.**

**The whole idea is that you swapped the question.** "Do these two add up?" has
to be asked of every pair, and there are about `n × n / 2` pairs. "Have I seen
`t - num` already?" is asked once per number, and a dict answers it without
looking at anything else it holds. Same answer, one pass instead of a triangle
of comparisons.

`seen` is the memory that makes the swap possible: it maps each number to the
position it first appeared at. Everything else in those six lines is detail —
but four details are load bearing, and each one is a requirement in disguise.

**1. `i < j` is guaranteed by the shape of the loop, not by a check.** `seen`
only ever contains positions from turns *before* this one, because the recording
happens after the lookup. So the `i` that comes back is always smaller than `j`.
There is no `if i < j` anywhere and there does not need to be — which is a
stronger guarantee than a comparison, because you cannot forget to write it.

**2. Lookup before insert.** Move `seen.setdefault(num, j)` above the `if` and
`two_sum([3], 6)` returns `(0, 0)`: the `3` finds itself and pairs with itself.
The order of those two statements is a correctness requirement, not a style
choice.

**3. `if i is not None`, not `if i`.** `.get()` returns a position, and position
`0` is falsy. `if i:` throws away every answer whose first half lives at the
start of the list, which includes the brief's headline example. See *Common bugs
to catch* — this one is genuinely nasty because it fails on some inputs and not
others.

**4. `setdefault` rather than `seen[num] = j`.** When a value repeats,
`setdefault` keeps the **earliest** position it was seen at. The brief promises
at most one answer, so this rarely shows — but when it does, keeping the
earliest gives you the smaller `i`, which is the answer everybody expects.
`seen[num] = j` overwrites, and on `[5, 5, 3]` with a target of `8` it returns
`(1, 2)` where `(0, 2)` is the natural answer.

**Speed was bought with memory.** In the worst case — no pair at all — `seen`
ends up holding every number in the list. You did not make the work disappear;
you moved it out of the processor and into a hash table. That trade is the
honest description of this algorithm, and it is the trade behind most of the
fast things you will write.

## Download and run

Download [problem-03-two-sum-classic-solution.py](./problem-03-two-sum-classic-solution.py)
and run it:

```bash
python problem-03-two-sum-classic-solution.py
```

Your own copy of `two_sum` belongs in `week-05-solutions.py`, and that is the
file you commit. The longer download name keeps the published answer from
landing on top of your work.

## Common bugs to catch

- **Truthiness instead of `is not None`.** The bug this problem is famous for:

  ```python
  i = seen.get(t - num)
  if i:                       # BUG: position 0 is falsy
      return (i, j)
  ```

  ```text
  truthy      [2,7,11,15] t=9 : None
  truthy      [3,2,4]     t=6 : (1, 2)
  ```

  No exception. The second example passes, so a quick test run looks green — but
  the brief's very first example now returns `None`, because the partner lives
  at position `0`. Any time a dict's *values* can legitimately be `0`, `""`,
  `[]` or `False`, `.get()` plus truthiness is a bug waiting for the right
  input. Use `is not None`, or use `in`:

  ```python
  if (t - num) in seen:
      return (seen[t - num], j)
  ```

- **Recording before looking up.**

  ```python
  for j, num in enumerate(nums):
      seen.setdefault(num, j)     # BUG: inserted before the check
      if t - num in seen:
          return (seen[t - num], j)
  ```

  ```text
  insert-first[3]         t=6 : (0, 0)
  insert-first[2,7,11,15] t=9 : (0, 1)
  ```

  Again no exception, and again the headline example still passes. But
  `two_sum([3], 6)` now returns `(0, 0)` — one number pairing with itself, which
  breaks `i < j`. `assert two_sum([3], 6) is None` is the cheapest possible
  guard against this.
- **Using `nums.index()` to find the partner.**

  ```python
  def two_sum_index(nums, t):
      for i, n in enumerate(nums):
          if (t - n) in nums:
              return (i, nums.index(t - n))
      return None
  ```

  ```text
  (0, 0)
  (0, 0)
  ```

  Two faults at once. `nums.index(x)` returns the **first** occurrence, so on
  `[3, 3]` with a target of `6` both halves come back as position 0 —
  self-pairing again. And `x in nums` walks the list
  ([lecture 03](../lecture-notes/03-comprehensions-and-big-o.md#the-headline-fact)),
  so this version is the slow one with extra steps. It loses the point even when
  it happens to return the right pair.
- **Returning a list.** `return [i, j]` fails
  `assert two_sum([2, 7, 11, 15], 9) == (0, 1)` because `[0, 1] != (0, 1)`. The
  signature says `tuple[int, int] | None`; honour it.
- **Returning something other than `None` for "no answer".** `return ()` or
  `return False` both fail `assert ... is None`, and both make the caller's
  `if result is None:` quietly wrong. A bare `return` and `return None` are the
  same thing, so either is fine.
- **Mistaking a printed `None` for a crash.** At the REPL, an expression that
  evaluates to `None` displays nothing at all:

  ```python
  >>> two_sum([1, 2, 3], 100)
  >>> print(two_sum([1, 2, 3], 100))
  None
  ```

  The first line did not fail. It returned `None`, and the REPL does not show
  `None`. Wrap it in `print()` when you want to see it.

## Under the hood

<details>
<summary>Under the hood — measuring the two versions, and what "one pass" buys you</summary>

The claim is that the dict version does not just win, it wins by more and more
as the list grows. That is worth seeing rather than taking on trust.

The measurement uses 5,000 distinct ascending numbers with the target set so
that **only the last two elements** reach it. Both versions are therefore forced
all the way to the end, which is the fair comparison — pick a target near the
front and the slow version looks fine.

```python
import timeit

SETUP = """
n = 5000
# Distinct and ascending, so the largest two elements are the ONLY pair that
# reaches t -- both algorithms are forced all the way to the end of the list.
nums = list(range(1, n + 1))
t = nums[-1] + nums[-2]

def two_sum_naive(nums, t):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == t:
                return (i, j)
    return None

def two_sum(nums, t):
    seen = {}
    for j, num in enumerate(nums):
        i = seen.get(t - num)
        if i is not None:
            return (i, j)
        seen.setdefault(num, j)
    return None
"""

print(min(timeit.repeat("two_sum_naive(nums, t)", setup=SETUP, repeat=5, number=1)))
print(min(timeit.repeat("two_sum(nums, t)", setup=SETUP, repeat=5, number=50)) / 50)
```

```text
python      : 3.13.2
n           : 5000  (only the final pair reaches the target)
naive O(n^2): 0.398 s   (best of 5)
dict  O(n)  : 0.00045 s   (best of 5 x 50)
ratio       : 881x
```

The absolute numbers depend on your machine. The **ratio** is the part that
travels, and it should be in the high hundreds.

Now the important experiment: double `n` to 10,000 and run it again. The slow
version's time roughly **quadruples**. The dict version's roughly **doubles**.
That is the difference between the two shapes, felt rather than asserted:

- Work that grows with `n × n` — twice the input, four times the work. This is
  written `O(n²)`.
- Work that grows with `n` — twice the input, twice the work. Written `O(n)`.

At 5,000 elements the gap is 881 times. At 50,000 it would be roughly ten times
wider again, because the ratio itself grows with `n`. This is why the shape
matters more than any amount of tuning: a faster processor moves both lines down
by the same factor and changes nothing about which one wins.

Two caveats, so the claim stays honest.

**Dict lookups are `O(1)` on average, not always.** A hash table can, in
principle, put every key in the same slot and degrade to a scan. With ordinary
integer and string keys this does not happen in practice, and Python randomises
string hashing per process specifically so that nobody can arrange it on
purpose.

**`timeit.repeat` and `min` are not decoration.** A single timing measures your
machine's mood as much as your code. Repeating and taking the **minimum** is
the standard trick: interference can only ever make a run slower, so the fastest
run is the one with the least of it.

</details>

<details>
<summary>Under the hood — three ways to ask a dict a question, and when each one lies</summary>

There are three ways to ask whether a key is in a dict, and they differ in ways
that matter exactly once — but that once is this problem.

**`d[key]` — take it or crash.**

```python
>>> seen = {2: 0}
>>> seen[7]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 7
```

Right when a missing key means a bug. Wrong here, where a missing key is the
normal case and half of what you are asking about.

**`key in d` — ask, then take.**

```python
if (t - num) in seen:
    return (seen[t - num], j)
```

Perfectly correct, and the version to reach for if `.get()` keeps tripping you
up. It does cost two lookups instead of one, and it computes `t - num` twice
unless you name it. Neither matters at this size; both are worth noticing.

**`d.get(key)` — take it or get `None`.** One lookup, no exception. The version
above uses this, and it is where the falsy-zero trap lives, because the answer
"the key is missing" and the answer "the value is `0`" come back looking similar
if you test them with `if`.

The general rule is not "always use `.get`". It is: **`.get()` is safe exactly
when `None` cannot be a legitimate value.** Here the values are positions,
`None` is never a position, and `is not None` separates the two cases exactly.

There is a fourth member of the family worth meeting. `.get()` takes a default:

```python
>>> seen.get(7, -1)
-1
```

That is tempting — pick a sentinel that cannot be a real position, and then
`if i >= 0:` works. It is fine, and it is also how you end up with `-1` leaking
into a return value six months later. `None` is the sentinel the language
already provides and every reader already knows.

And `.setdefault(key, default)`, which the answer uses, is the write-side
sibling: it returns the existing value if there is one, and otherwise inserts
the default and returns that. Here it means "remember this number, unless I
already have" — the earliest position wins. Problem 5 uses the same method for
something completely different, because what it returns is a **live** reference
into the dict.

</details>

## Acceptance checklist

- [ ] `two_sum([2, 7, 11, 15], 9)` gives `(0, 1)`.
- [ ] `two_sum([3, 2, 4], 6)` gives `(1, 2)`.
- [ ] `two_sum([1, 2, 3], 100)` gives `None`.
- [ ] `two_sum([], 5)` gives `None` and does not raise.
- [ ] `two_sum([3, 3], 6)` gives `(0, 1)`.
- [ ] `two_sum([3], 6)` gives `None`.
- [ ] `two_sum([0, 0], 0)` gives `(0, 1)` — the falsy-zero check.
- [ ] The answer is a tuple, and the first number is smaller than the second.
- [ ] There is no nested loop, no `nums.index`, and no `x in nums`.
- [ ] The test is written `is not None`.
- [ ] The signature has type hints and the function has a docstring.
- [ ] Committed with a message like `Week 5 homework: two-sum`.

## Stretch

- **Return every pair, not just the first.** Drop the "at most one solution"
  promise and give back a list of all pairs `(i, j)` with `i < j`. The single
  `seen` position is no longer enough — a value can now be needed more than
  once, so `seen` becomes `dict[int, list[int]]`. Decide what to do about
  `[1, 1, 2, 2]` with a target of `3` before you write it: there are four pairs
  there and it is easy to produce two of them twice.
- **Three-Sum.** Find three positions that add to the target. The good version
  sorts the list and then, for each element, walks two pointers inwards from
  both ends of the rest — `O(n²)`, which is the known best for this problem.
  Sorting loses the original positions, so carry them along as
  `sorted(enumerate(nums), key=lambda pair: pair[1])`.
- **Return the values instead of the positions.** A one-character change to the
  return line, and then work out why the brief asked for positions anyway. Hint:
  ask what a caller does next with each answer when the list is a row of prices
  from a database.
- **Handle floats.** `two_sum([0.1, 0.2], 0.3)` returns `None`, because
  `0.1 + 0.2` is not exactly `0.3` in binary floating point and the dict lookup
  is an exact-equality test. There is no clean fix — a hash table cannot do
  "close enough" — which is itself the lesson. `math.isclose` and a sorted
  two-pointer walk is the usual answer.
- **Write it with a set instead of a dict.** If the caller only wants to know
  *whether* a pair exists, a `set` of the numbers seen so far is enough and the
  code loses a line. Then notice what you gave up: you can no longer say where
  the numbers were. Choosing the smaller structure when you need less is a real
  skill, and so is noticing the moment you needed more.

Next: [Homework Problem 4 — Find duplicates](./problem-04-find-duplicates.md).
