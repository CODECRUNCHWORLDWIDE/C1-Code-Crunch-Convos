# Exercise 2 — Sum of Evens

> **Topic:** The accumulator pattern, and `range` with a step
> **Lecture:** [03 — Loop Patterns You Will Use Forever](../lecture-notes/03-loop-patterns.md)
> **Difficulty:** Beginner
> **Target time:** 15 minutes
> **Why this one:** the accumulator — start a total at zero, add to it inside a loop, read it after — is the loop shape you will reuse more than any other. Every running total, word count and price subtotal you ever write is this exercise with different nouns. The second half is the more valuable half, though: it teaches you to check a loop against an independent calculation instead of staring at the output and hoping.

## The Brief

Add up every even number from 2 up to a limit you choose. `sum_evens(10)`
is `2 + 4 + 6 + 8 + 10`, which is 30.

Then do the same sum a second time, with no loop at all.

There is a shortcut. The even numbers up to a limit are `2, 4, 6, …, 2k`,
where `k` is how many of them there are. Their total is always
`k * (k + 1)`. For a limit of 10 there are five of them, so `k` is 5, and
`5 * 6` is 30. Same answer, no counting.

The shortcut is not busywork and it is not showing off. It is your marker.
Your `main()` runs both versions over a spread of limits and stops the
program if they ever disagree. That is a real habit worth forming now: when
you have two independent ways to work out the same answer, you stop having
to squint at output. The loop is what you are practising. The formula is
what proves the loop right.

## Starter

Create `exercise-02-sum-evens.py` in your practice repo, paste this in,
then fill in the two `TODO`s:

```python
"""exercise-02-sum-evens.py — the accumulator pattern, checked by arithmetic.

Adds the even numbers from 2 up to a limit, two different ways, and
asserts that the loop and the closed-form formula agree.
"""

CHECK_LIMITS = [-4, 0, 1, 2, 7, 10, 100]


def sum_evens(limit: int) -> int:
    """Return the sum of every even number from 2 to `limit` inclusive.

    Returns 0 when `limit` is less than 2, because there are no even
    numbers in that range to add.
    """
    total = 0
    # TODO: loop over the even numbers from 2 to limit inclusive and add
    # each one to total. Use range's third argument for the step.
    return total


def sum_evens_formula(limit: int) -> int:
    """Return the same sum using the closed form k * (k + 1)."""
    # TODO: guard against a limit below 2, then compute k and return
    # k * (k + 1). Use // for integer division, not /.
    return 0


def main() -> None:
    """Compare the loop against the formula for every limit in CHECK_LIMITS."""
    for limit in CHECK_LIMITS:
        looped = sum_evens(limit)
        closed = sum_evens_formula(limit)
        status = "ok" if looped == closed else "MISMATCH"
        print(f"limit={limit:>4}  loop={looped:>6}  formula={closed:>6}  {status}")
        assert looped == closed, f"disagreement at limit={limit}"


if __name__ == "__main__":
    main()
```

Three words you need before you start.

**Accumulator.** A variable whose whole job is to hold "the answer so far".
`total` here. You set it before the loop, you change it inside, and you
read it after.

**Step.** `range` takes a third number: how far to jump each time.
`range(2, 11, 2)` gives you 2, 4, 6, 8, 10 and never offers you an odd
number at all.

**`assert`.** A line that says "this had better be true". If it is, nothing
happens and the program carries on. If it is not, the program stops right
there and tells you which check failed. It is a tripwire you leave in your
own code.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/exercises/exercise-02-sum-evens.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `sum_evens()` uses one `for` loop over a `range` with a step of 2. No
   `if` statement inside the loop — the range should never hand you an odd
   number in the first place.
2. `total` starts at `0` **before** the loop and is returned **after** it.
   Nothing else touches it.
3. Both functions return `0` for any limit below 2. Not `None`, not an
   error — zero, because adding up nothing gives you nothing.
4. `sum_evens_formula()` uses `//`, not `/`, to work out `k`.
5. `main()` prints one line per limit and asserts that the two results
   match. All seven lines end in `ok`.

## Constraints

- **Do not use the built-in `sum()`.** Real code absolutely should use
  `sum(range(2, limit + 1, 2))` — it is shorter and faster. This exercise
  exists so that when you do reach for `sum()`, you know exactly what it is
  doing on your behalf instead of treating it as a magic word.
- **Do not build a list of the evens first.** `range` hands you one value
  at a time and takes the same tiny amount of memory no matter how large
  the limit ([Lecture 2 §3](../lecture-notes/02-loops.md)). A list of the
  evens up to ten million would be a few hundred megabytes for a total you
  could have carried in one integer.
- **Filter with the step, not with `if number % 2 == 0`.** Walking every
  number and skipping the odd ones does twice the work for the same answer,
  and it puts you one keystroke away from `if number % 2:`, which reads "is
  odd" and quietly totals the wrong half. Let the range express the rule.
- **Use `//`, never `/`, for `k`.** `k` is a count of things, and counting
  is integer work. `/` gives you a float, and a float `k` does not hand you
  the right answer with a decimal point stuck on it — it hands you a
  different number. There is more on this below.
- **A negative limit returns 0. It does not raise.** `range(2, -3, 2)` is
  not an error in Python; it is simply empty, so the loop never runs and
  the `0` you started with is what comes back. The formula has no such
  protection and needs an explicit guard, which is the interesting part of
  this exercise.
- **`def` is Week 4, and these five exercises are the deliberate exception:
  the starter hands you the function headers already written, so you are
  filling in a body someone else declared rather than deciding what a
  function should be.**

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2:

```text
$ python exercise-02-sum-evens.py
limit=  -4  loop=     0  formula=     0  ok
limit=   0  loop=     0  formula=     0  ok
limit=   1  loop=     0  formula=     0  ok
limit=   2  loop=     2  formula=     2  ok
limit=   7  loop=    12  formula=    12  ok
limit=  10  loop=    30  formula=    30  ok
limit= 100  loop=  2550  formula=  2550  ok
```

Two of those lines are earning their place.

**`limit=2` is the sharpest test of the range bound.** If you wrote
`range(2, limit, 2)` and left off the `+ 1`, then `range(2, 2, 2)` is
empty, the one even number in range goes missing, your loop returns 0, the
formula returns 2, and the run stops there. It is the smallest possible
version of the off-by-one, and it fires before any of the bigger limits get
a chance to.

**`limit=-4` catches a formula with no guard.** Without it you get 2 out of
a function that should return 0, on the very first line.

If every line says `ok` on your first run, break it on purpose: change
`limit + 1` to `limit`, run, watch the failure, and put it back. A check
you have never seen fail is a check you do not know is running.

## Steps

1. Create `exercise-02-sum-evens.py` and paste the starter in.
2. Fill in `sum_evens()`. It is two lines: the `for` and the `+=`.
   `total = 0` and `return total` are already written for you, and where
   they sit is half the lesson.
3. Run it. The loop half is now right and the formula half still returns 0,
   so the first `assert` fires at `limit=2`. That is the check doing its
   job, not a problem.
4. Fill in `sum_evens_formula()`: guard first, then `k`, then the return.
5. Run it again. All seven lines should read `ok` and nothing should raise.
6. Check the small cases at the prompt with
   `python -i exercise-02-sum-evens.py`:

   ```text
   >>> sum_evens(1), sum_evens(0), sum_evens(-4)
   (0, 0, 0)
   >>> sum_evens(10), sum_evens_formula(10)
   (30, 30)
   ```

   No decimal points anywhere in that output. Both functions hand back
   whole numbers.
7. Add `1000` to `CHECK_LIMITS` and run once more:

   ```text
   limit=1000  loop=250500  formula=250500  ok
   ```

   It should still be instant. The loop only does 500 additions.

## The Solution

```python
"""exercise-02-sum-evens-solution.py — the accumulator pattern, checked by arithmetic.

Adds the even numbers from 2 up to a limit, two different ways, and
asserts that the loop and the closed-form formula agree.
"""

CHECK_LIMITS = [-4, 0, 1, 2, 7, 10, 100]


def sum_evens(limit: int) -> int:
    """Return the sum of every even number from 2 to `limit` inclusive.

    Returns 0 when `limit` is less than 2, because there are no even
    numbers in that range to add.
    """
    total = 0
    for number in range(2, limit + 1, 2):
        total += number
    return total


def sum_evens_formula(limit: int) -> int:
    """Return the same sum using the closed form k * (k + 1)."""
    if limit < 2:
        return 0
    k = limit // 2
    return k * (k + 1)


def main() -> None:
    """Compare the loop against the formula for every limit in CHECK_LIMITS."""
    for limit in CHECK_LIMITS:
        looped = sum_evens(limit)
        closed = sum_evens_formula(limit)
        status = "ok" if looped == closed else "MISMATCH"
        print(f"limit={limit:>4}  loop={looped:>6}  formula={closed:>6}  {status}")
        assert looped == closed, f"disagreement at limit={limit}"


if __name__ == "__main__":
    main()
```

**The accumulator has one sentence attached to it, and saying that sentence
tells you where every line goes.** The sentence is: *after the loop has run
`k` times, `total` holds the sum of the first `k` even numbers.*

Check it before the loop starts: zero numbers add up to zero, which is
exactly why `total = 0`. Check it after each `+=`: still true. That is why
`total = 0` sits **outside** the loop — inside, it would re-announce "zero
numbers so far" on every single pass and throw away everything you had. And
it is why `return total` sits **after** the loop, because that is the first
moment the sentence covers all of them. Start outside, change inside, read
after ([Lecture 3 §1](../lecture-notes/03-loop-patterns.md)).

**The step is the filter.** `range(2, limit + 1, 2)` counts 2, 4, 6 and
never offers an odd number, so there is nothing to test and no `if` in the
loop body. Every condition you do not write is a condition you cannot get
backwards.

**Small and negative limits need nothing in the loop, and do need a guard
in the formula.** This asymmetry is the point of the exercise.
`range(2, -3, 2)` is simply empty, so `sum_evens(-4)` never enters the body
and returns the `0` it started with. The formula has no such protection,
because `//` rounds **down**, toward negative infinity:

```text
>>> -4 // 2
-2
>>> -2 * (-2 + 1)
2
```

Two, out of a function that should hand back zero, with nothing to warn
you. That is why `if limit < 2: return 0` sits *above* the arithmetic and
not below it. It is a guard clause in exactly the
[Lecture 1 §9](../lecture-notes/01-conditionals.md) sense: refusing to
compute rather than computing something wrong.

**`//` and not `/`, and the reason is not only the type.** Try it with a
limit of 7. `7 // 2` is 3, so `k` is 3, and `3 * 4` is 12 — correct, and
the flooring is doing real work, because it is what discards the odd limit.
`7 / 2` is `3.5`, and `3.5 * 4.5` is `15.75`. A float `k` does not give you
the same number with a decimal point on it. It gives you a different,
wrong number.

**Two implementations are a grader, not duplication.** `sum_evens` and
`sum_evens_formula` share no code and no reasoning — one walks the numbers,
the other uses a fact about them. When two independent methods agree on
seven inputs, the chance that both are wrong in the same direction is
small. That is what the `assert` in `main()` is for, and it is why the
check limits were chosen rather than picked at random: `-4` exercises the
guard, `1` exercises "no evens at all", `2` exercises the boundary where
the range first stops being empty, and `10` exercises the inclusive stop.

**`{limit:>4}` lines the columns up** so a mismatch shows as a ragged row
rather than something you have to read for. `status` is set with the
conditional expression from
[Lecture 1 §8](../lecture-notes/01-conditionals.md) so that the mismatch is
*printed* before the `assert` stops the program. Print first, then fail, or
you lose the evidence.

## Download and run

Download
[exercise-02-sum-evens-solution.py](./exercise-02-sum-evens-solution.py)
and run it:

```bash
python exercise-02-sum-evens-solution.py
```

It is the same program as the one you are writing, under a name that will
not collide with your own `exercise-02-sum-evens.py`.

## Common bugs to catch

- **`AssertionError: disagreement at limit=2`.** The stop value dropped its
  `+ 1`, so you wrote `range(2, limit, 2)`:

  ```text
  limit=  -4  loop=     0  formula=     0  ok
  limit=   0  loop=     0  formula=     0  ok
  limit=   1  loop=     0  formula=     0  ok
  limit=   2  loop=     0  formula=     2  MISMATCH
  Traceback (most recent call last):
    File "exercise-02-sum-evens.py", line 41, in <module>
      main()
      ~~~~^^
    File "exercise-02-sum-evens.py", line 37, in main
      assert looped == closed, f"disagreement at limit={limit}"
             ^^^^^^^^^^^^^^^^
  AssertionError: disagreement at limit=2
  ```

  `range` stops *before* its stop value. Use `range(2, limit + 1, 2)`.

- **`AssertionError: disagreement at limit=7`, and every total is the last
  even number rather than the sum.** You wrote `total = number` instead of
  `total += number`, so the running total is dropped on the floor and
  rebuilt from scratch every pass:

  ```text
  limit=   2  loop=     2  formula=     2  ok
  limit=   7  loop=     6  formula=    12  MISMATCH
  ```

  Notice it survives `limit=2`, where the last even number and the sum
  happen to be the same value. One `ok` followed by a mismatch is a useful
  signature: it usually means a loop that is right for one pass and wrong
  for two.

- **Every total is 0.** `total = 0` ended up *inside* the loop body, so it
  resets before each addition and the last `+=` is thrown away by the next
  reset. Start outside, change inside.

- **`NameError: name 'total' is not defined`.** The `total = 0` is below
  the loop instead of above it, or it is indented into a different block.

- **`AssertionError: disagreement at limit=-4`, on the very first line.**
  The formula has no guard:

  ```text
  limit=  -4  loop=     0  formula=     2  MISMATCH
  Traceback (most recent call last):
    File "exercise-02-sum-evens.py", line 39, in <module>
      main()
      ~~~~^^
    File "exercise-02-sum-evens.py", line 35, in main
      assert looped == closed, f"disagreement at limit={limit}"
             ^^^^^^^^^^^^^^^^
  AssertionError: disagreement at limit=-4
  ```

  Return 0 before you compute `k`.

- **A decimal point appears in the `formula` column.** You wrote
  `k = limit / 2`:

  ```text
  limit=   2  loop=     2  formula=   2.0  ok
  limit=   7  loop=    12  formula= 15.75  MISMATCH
  ```

  Look hard at the `limit=2` line. It printed `2.0` and still said `ok`,
  because `2 == 2.0` is `True` in Python. The type was already wrong one
  line before the answer was. A float that happens to equal the right
  integer is a bug that has not gone off yet.

- **The odd numbers get totalled instead of the even ones.** You looped
  over every number and used `if number % 2:` as the filter. `number % 2`
  is `1` for odd numbers, and `1` counts as true — so that condition means
  "is odd". The even test is `number % 2 == 0`, and better still, use the
  step and delete the `if`.

- **`TypeError: 'float' object cannot be interpreted as an integer`.** A
  float reached `range`, usually from a `/` somewhere upstream. `range`
  takes whole numbers only.

## Under the hood

<details>
<summary>Under the hood — where k * (k + 1) comes from, and why it has to match the loop</summary>

The formula is not a coincidence and it is not something you have to take
on trust. It falls out in two steps.

**Step one: pull the 2 out.** The even numbers up to `2k` are
`2, 4, 6, …, 2k`, and every one of them is 2 times something:

```text
2 + 4 + 6 + … + 2k  =  2 × (1 + 2 + 3 + … + k)
```

**Step two: add up 1 to k.** There is a very old trick for this. Write the
row forwards, write it again backwards underneath, and add the columns:

```text
   1  +  2  +  3  + … +  k
   k  + k-1 + k-2 + … +  1
  ---------------------------
 k+1  + k+1 + k+1 + … + k+1
```

Every column comes to `k + 1`, and there are `k` columns, so the two rows
together total `k × (k + 1)`. One row is half of that, `k(k + 1) / 2`.

Put the steps together:

```text
2 × k(k + 1)/2  =  k(k + 1)
```

The 2 and the ÷2 cancel, which is why the even-number version is the
tidier one — no division survives, so the answer is a whole number by
construction.

**Where `k` comes from.** `k` is *how many* even numbers there are up to
the limit, which is `limit // 2`. For a limit of 10 that is 5, and the
evens are 2, 4, 6, 8, 10 — five of them. For a limit of 7 it is 3, and the
evens up to 7 are 2, 4, 6 — three of them. The flooring is what throws away
the odd limit, and that is exactly the job you want done.

**Why this is a real check and not a circular one.** The loop and the
formula have nothing in common. The loop knows only how to walk and add.
The formula knows only a fact about arithmetic series and never touches an
individual number. If you get the loop's bound wrong, the formula is
unaffected; if you get the formula's guard wrong, the loop is unaffected.
Two wrong answers that agree would have to be wrong in the same direction
by the same amount on all seven inputs, and that essentially does not
happen by accident.

It *can* happen when the two versions share reasoning. Watch for that when
you write your own cross-checks: a second implementation that copies the
first one's assumption tests nothing.

**How big does the loop get?** For a limit of one million, the loop does
500,000 additions and the formula does one multiplication. Both are instant
at these sizes. The formula is `O(1)` — the same work no matter how big the
limit — and the loop is `O(n)`. That difference stops mattering entirely
below about a million and starts mattering a great deal above a billion.

</details>

<details>
<summary>Under the hood — what a range object actually is</summary>

`range(2, 1000001, 2)` does not contain half a million numbers. It contains
three: a start, a stop and a step. It works out the next value only when
something asks for one.

You can see it in the memory footprint:

```text
>>> import sys
>>> sys.getsizeof(range(2, 10_000_001, 2))
48
```

Forty-eight bytes for a range covering five million values. A list of those
same values would be hundreds of megabytes. The number is 48 no matter how
big the range gets, because the object is always just those three numbers
plus Python's per-object bookkeeping.

This is why the constraint against building a list is not fussiness. It is
the difference between a program that works on any limit and one that falls
over on a large one, and the version that works is also the shorter one to
write.

A range is not a generator, though it is easy to lump them together. A
range can be asked its length, indexed, and walked more than once —
`r[500]` is instant, and it computes the value rather than looking it up. A
generator can be walked exactly once and then it is spent. Week 5 draws
that line properly.

</details>

## Acceptance checklist

- [ ] `python exercise-02-sum-evens.py` runs with no traceback.
- [ ] All seven lines print `ok`.
- [ ] `sum_evens()` contains no `if` statement and no call to `sum()`.
- [ ] `sum_evens(1)`, `sum_evens(0)` and `sum_evens(-4)` all return `0`.
- [ ] Both functions return whole numbers, never floats — no decimal point
      appears anywhere in the output.
- [ ] You broke the range on purpose, watched the assert fire, and put it back.
- [ ] Committed to Git with a message like `Add Week 3 exercise 2: sum of evens`.

## Stretch

- Generalise to `sum_multiples(factor: int, limit: int) -> int`, so you can
  total the multiples of 3, or 7, or anything. The shortcut becomes
  `factor * k * (k + 1) // 2` where `k = limit // factor`. Derive it from
  the two steps in the Under the hood block before you trust it, then let
  the assert confirm you were right.
- Print a running total inside the loop so you can watch the accumulator
  grow. It changes nothing about the answer and shows you the pattern
  mid-flight, which is exactly what a debugger would show you.
- Swap the accumulator for a product: multiply the evens instead of adding
  them, starting from `1` rather than `0`. Try a limit of 20 and notice
  that Python integers simply keep growing — no overflow, no wraparound,
  unlike most languages you will meet later.

Once the totals agree, move on to
[Exercise 3 — Password Checker](./exercise-03-password-checker.md).
