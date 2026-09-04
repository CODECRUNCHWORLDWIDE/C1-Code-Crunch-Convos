# Exercise 5 — Find the Prime

> **Topic:** `for` with an `else` clause, and early `return` / `break`
> **Lecture:** [02 — Loops: Doing Things Repeatedly](../lecture-notes/02-loops.md)
> **Difficulty:** Medium
> **Target time:** 30 minutes
> **Why this one:** the loop `else` clause is the one piece of Python almost nobody discovers on their own, and it exists for exactly this shape — "search for a thing; if the search ran out without finding it, do something else". You will write that shape constantly. This exercise also makes you justify a loop's stopping point with an argument instead of a hunch, which is the habit that separates code that happens to work from code you can defend.

## The Brief

A number is **prime** when it is 2 or bigger and nothing divides into it
evenly except 1 and itself. 7 is prime. 9 is not, because 3 goes into it
three times.

The plain way to check is **trial division**: try each possible divisor in
turn and see whether one goes in cleanly. If one does, you are done — not
prime. If you run out of candidates without finding one, it is prime.

You will write that twice, on purpose, because the two versions want
different shapes.

`report_primality()` prints a sentence. It uses the `for`/`else` clause
from [Lecture 2 §8](../lecture-notes/02-loops.md): when it finds a divisor
it prints the reason and `break`s, and when the loop runs out of divisors
without ever breaking, the `else` fires and the number is prime. No flag
variable, nothing to forget to update.

`is_prime()` hands back a `True` or a `False` for somebody else to use. It
uses guard clauses and early returns instead.

Comparing them is the point. A loop `else` suits a loop that *is* the whole
job. An early `return` suits a job whose answer someone is waiting for.

Now the interesting part: **where do you stop looking?**

You do not have to try every number below the one you are testing. You only
have to go as far as the square root. Here is the argument, and you should
be able to say it out loud. Suppose `number = a * b`. If *both* `a` and `b`
were bigger than the square root, then `a * b` would be bigger than
`number` — which cannot be, because `a * b` *is* `number`. So at least one
of the pair is at or below the square root. If a divisor exists, you will
have met it before you get past the root, and everything after that is
wasted work.

## Starter

Create `exercise-05-find-prime.py` in your practice repo, paste this in,
then fill in the two `TODO`s:

```python
"""exercise-05-find-prime.py — trial division, twice.

Once with the for/else clause and once with guard clauses and early
returns, cross-checked against a list of known answers.
"""

import math

CHECK_NUMBERS = [1, 2, 9, 25, 91, 97, 7919]
EXPECTED_PRIME = [False, True, False, False, False, True, True]


def report_primality(number: int) -> None:
    """Print one line explaining whether `number` is prime.

    Uses the for/else clause: the else runs only when no divisor was
    found and the loop was therefore never broken out of.
    """
    if number < 2:
        print(f"{number:>6} is not prime: primes start at 2.")
        return
    # TODO: loop over the candidate divisors from 2 up to and including
    # math.isqrt(number). On the first one that divides evenly, print the
    # reason and break. Attach an else to the FOR (not to the if) that
    # prints the "is prime" line.


def is_prime(number: int) -> bool:
    """Return True when `number` is prime, using guard clauses."""
    if number < 2:
        return False
    if number == 2:
        return True
    # TODO: return False for any other even number, then test only the
    # odd divisors from 3 up to and including math.isqrt(number),
    # returning False on the first hit and True if none of them divide.
    return True


def main() -> None:
    """Report on every check number and confirm both versions agree."""
    prime_count = 0

    for number, expected in zip(CHECK_NUMBERS, EXPECTED_PRIME, strict=True):
        report_primality(number)
        assert is_prime(number) == expected, f"is_prime({number}) is wrong"
        if is_prime(number):
            prime_count += 1

    print(f"{prime_count} of {len(CHECK_NUMBERS)} numbers are prime.")


if __name__ == "__main__":
    main()
```

Three things to read before you start.

**`math.isqrt(n)`** is the integer square root: the largest whole number
whose square is not bigger than `n`. `math.isqrt(9)` is 3.
`math.isqrt(91)` is 9, because 9 × 9 is 81 and 10 × 10 is 100.

**`for` … `else`** is not "otherwise". The `else` belongs to the `for`, not
to any `if` inside it, and it means one thing only: *the loop finished
without a `break`*. Read it that way every time and it stops being
mysterious.

**`zip(a, b, strict=True)`** walks two lists side by side, handing you one
item from each. The `strict=True` makes it complain if the lists are
different lengths instead of quietly stopping at the shorter one.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/exercises/exercise-05-find-prime.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `report_primality()` uses a `for` loop with an `else` attached to the
   `for`, and a `break` on the divisor it finds. No true-or-false flag
   variable anywhere in the function.
2. When it finds a divisor, the message names the **smallest** one.
   Counting up from 2 gives you that for nothing.
3. `is_prime()` returns `True` or `False` and never prints.
4. Both functions stop at `math.isqrt(number)` **inclusive** — that is,
   `range(..., math.isqrt(number) + 1, ...)`.
5. `is_prime()` deals with 2 correctly *before* it rejects even numbers.
   Two is the only even prime, and an even check placed first is wrong
   about the most famous prime there is.
6. `main()` runs clean: seven report lines, no `AssertionError`, and a
   final summary line.

## Constraints

- **Use `math.isqrt()`, not `math.sqrt()`.** `math.sqrt(25)` gives you
  `5.0`, a float, and `range` refuses floats outright. Beyond the type,
  floats are approximate — for a large enough number, `int(math.sqrt(n))`
  can land one below the true integer square root and quietly skip the very
  divisor that mattered. `math.isqrt` is defined to give the exact answer,
  so there is no rounding to reason about.
- **Stop at the square root, inclusive.** The `+ 1` on the range's stop is
  load-bearing, not decoration. For a perfect square like 9 or 25, the
  *only* divisor at or below the root **is** the root. Drop the `+ 1` and
  every perfect square in your list gets reported prime.
- **In `is_prime()`, step the divisors by 2 after you have handled the even
  numbers.** Once every even number above 2 has been rejected, no even
  divisor can divide what is left, so testing 4, 6 and 8 is guaranteed
  wasted work. `range(3, math.isqrt(number) + 1, 2)` halves the loop.
- **Attach the `else` to the `for`, not to the `if`.** They differ only by
  indentation and Python accepts both, so this is a silent logic bug rather
  than an error. The `else` belongs at the same column as the `f` of `for`.
- **Do not use `break` in `is_prime()`.** Use `return False` directly.
  Breaking out and then working out what to return afterwards needs exactly
  the flag variable the loop `else` was invented to avoid.
- **Keep `report_primality()` printing and `is_prime()` silent.** One
  function that both works something out and prints it cannot be reused by
  anything that wants the answer rather than the paragraph.
- **`def` is Week 4, and these five exercises are the deliberate exception:
  the starter hands you the function headers already written, so you are
  filling in a body someone else declared rather than deciding what a
  function should be.**

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2:

```text
$ python exercise-05-find-prime.py
     1 is not prime: primes start at 2.
     2 is prime.
     9 is not prime: 3 divides it evenly.
    25 is not prime: 5 divides it evenly.
    91 is not prime: 7 divides it evenly.
    97 is prime.
  7919 is prime.
3 of 7 numbers are prime.
```

Every number in that list is doing a job.

- **1** catches a missing lower guard. `math.isqrt(1)` is 1, so the divisor
  loop is empty, so the `else` fires and calls it prime.
- **2** catches an even check placed before the two check.
- **9 and 25** catch a square-root bound that stops one short. They are
  perfect squares, so their only divisor at or below the root *is* the
  root.
- **91** catches a checker that hard-codes a handful of small divisors. It
  survives 2, 3 and 5 and dies at 7.
- **97 and 7919** are genuinely prime, so they are the ones that prove the
  `else` fires at all. 7919 makes you try all 87 candidates from 2 to 88 —
  or 43 of them once you skip the evens.

## Steps

1. Create `exercise-05-find-prime.py` and paste the starter in.
2. Write `report_primality()` first. Get the loop working with just the
   `break` and the "not prime" message, and confirm nothing at all prints
   for 97.
3. Now attach the `else` to the `for` and run again. Line the `else` up
   directly under the `f` of `for`. If your editor auto-indents it under
   the `if`, pull it back.
4. Run it. The first report lines should be right, but the assert fires on
   9 — the starter's `is_prime()` still says every number above 2 is prime.
5. Write `is_prime()`: the even guard, then the stepped loop, then
   `return True` at the end. Watch the indentation of that last line.
6. Run it again. Seven lines, no traceback, summary reads `3 of 7`.
7. Check the two functions on their own with
   `python -i exercise-05-find-prime.py`:

   ```text
   >>> is_prime(2), is_prime(1), is_prime(91)
   (True, False, False)
   >>> math.isqrt(91), math.isqrt(7919)
   (9, 88)
   ```

   `math.isqrt(7919)` being 88 is the whole performance claim made
   concrete: 87 candidates in `report_primality`, or 43 in `is_prime` once
   the evens are skipped — against 7,917 if you had looped all the way to
   the number itself.
8. Add `7920` to `CHECK_NUMBERS` and `False` to `EXPECTED_PRIME`, then run
   once more:

   ```text
     7919 is prime.
     7920 is not prime: 2 divides it evenly.
   3 of 8 numbers are prime.
   ```

   `report_primality` names 2 and stops on its first candidate; `is_prime`
   rejects it on the even guard without entering the loop at all. Two
   routes to the same answer, which is the point of having written it
   twice.

## The Solution

```python
"""exercise-05-find-prime-solution.py — trial division, twice.

Once with the for/else clause and once with guard clauses and early
returns, cross-checked against a list of known answers.
"""

import math

CHECK_NUMBERS = [1, 2, 9, 25, 91, 97, 7919]
EXPECTED_PRIME = [False, True, False, False, False, True, True]


def report_primality(number: int) -> None:
    """Print one line explaining whether `number` is prime.

    Uses the for/else clause: the else runs only when no divisor was
    found and the loop was therefore never broken out of.
    """
    if number < 2:
        print(f"{number:>6} is not prime: primes start at 2.")
        return
    for divisor in range(2, math.isqrt(number) + 1):
        if number % divisor == 0:
            print(f"{number:>6} is not prime: {divisor} divides it evenly.")
            break
    else:
        print(f"{number:>6} is prime.")


def is_prime(number: int) -> bool:
    """Return True when `number` is prime, using guard clauses."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for divisor in range(3, math.isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False
    return True


def main() -> None:
    """Report on every check number and confirm both versions agree."""
    prime_count = 0

    for number, expected in zip(CHECK_NUMBERS, EXPECTED_PRIME, strict=True):
        report_primality(number)
        assert is_prime(number) == expected, f"is_prime({number}) is wrong"
        if is_prime(number):
            prime_count += 1

    print(f"{prime_count} of {len(CHECK_NUMBERS)} numbers are prime.")


if __name__ == "__main__":
    main()
```

**`else` on a `for` means "the loop finished without a `break`".** Read it
that way and the mystery evaporates. It is not "otherwise" and it has
nothing to do with the `if` inside the loop; it is attached to the `for`,
and it fires exactly when the loop ran out of items naturally
([Lecture 2 §8](../lecture-notes/02-loops.md)). "Ran out of divisors
without finding one" *is* the definition of prime, so the `else` is not a
trick here. It is the closest Python gets to saying the mathematical
statement out loud. The alternative is a `found = False` flag: three extra
lines and three chances to forget an update.

**The `break` is what makes the `else` mean anything.** Take it out and the
loop always finishes naturally, so the `else` always fires and every number
is declared prime *as well as* whatever the loop already printed:

```text
     9 is not prime: 3 divides it evenly.
     9 is prime.
```

The `break` and the `else` are a matched pair. If you have one without the
other, you have neither.

**Counting up from 2 hands you the smallest divisor for free.**
Requirement 2 wants the message to name the smallest one, and there is
nothing to write for it. The loop starts at the smallest candidate and
`break`s at the first hit, so the divisor in your hand when it stops is by
construction the smallest. Bounds that make a requirement automatic are
worth noticing when you have chosen one.

**The square-root bound, and the `+ 1` that makes it correct.** The
argument is in the Brief: if `number = a * b` and both were bigger than the
root, their product would be bigger than `number`. So any non-prime has a
divisor at or below its square root, and looking past it finds nothing new.

The word "at" is where the `+ 1` lives. For a perfect square like 9, the
only divisor at or below the root **is** the root. `range` stops before its
stop value, so `range(2, math.isqrt(9))` is `range(2, 3)` — it tests 2,
never tests 3, and pronounces 9 prime:

```text
>>> import math
>>> math.isqrt(9)
3
>>> list(range(2, math.isqrt(9)))
[2]
```

9 and 25 are in the check list specifically to catch that missing `+ 1`.

**`math.isqrt`, not `math.sqrt`.** `math.sqrt(25)` is `5.0`, and `range`
does not take floats. Even after an `int()` cast the float route stays
wrong in principle: floats are approximate, and for a large enough number
`int(math.sqrt(n))` can come out one below the true integer square root and
skip exactly the divisor that mattered. `math.isqrt` is defined to return
the exact integer square root, so there is no rounding to think about at
all.

**Guard order in `is_prime()`, narrowest claim first.** `number < 2`, then
`number == 2`, then "any other even number", then the odd divisors. Swap
the last two and the most famous prime there is gets rejected for being
even. It is the same rule that orders the chain in Exercise 1 — the
narrowest claim goes first — except here the narrowest claim is about a
single number.

**Stepping by 2 is only safe *because* of the guard above it.**
`range(3, math.isqrt(number) + 1, 2)` skips every even divisor, which
halves the work, and it is correct only because every even number has
already left the function by that point. If a divisor of the survivors were
even, the number itself would have been even. Name that habit: an
optimisation that depends on an earlier guard sits directly below that
guard, so nobody moves one without seeing the other.

**`return False` instead of `break`, in this function only.**
`report_primality` has nothing to hand back, so `break` plus `else` reads
well. `is_prime` owes its caller an answer, and `return False` delivers it
from inside the loop with nothing left to remember. Breaking out and then
working out what to return would need the flag variable both versions were
designed to avoid. Same problem, two shapes, and the shape follows from
whether anyone is waiting for a value.

**`return True` sits after the loop, not inside it.** Inside, it would fire
on the first divisor that *fails* to divide — a yes after one question.
Outside, it means "the candidates are exhausted", which is the only
evidence that justifies it. It is the `else` clause written as an early
return, and putting it one indent too deep is the single most common way to
break this function.

**`zip(..., strict=True)` makes the two lists one source of truth.** Add a
number to `CHECK_NUMBERS` and forget its expected answer, and `strict=True`
raises immediately instead of quietly stopping at the shorter list
([Lecture 2 §5](../lecture-notes/02-loops.md)). Without it, the check that
is supposed to protect you shrinks in silence.

## Run it

Copy the worked answer on this page into `exercise-05-find-prime.py` and run it:

```bash
python exercise-05-find-prime.py
```

It is the same program as the one you are writing, under a name that will
not collide with your own `exercise-05-find-prime.py`.

## Common bugs to catch

- **`AssertionError: is_prime(9) is wrong`, and `9 is prime.` printed one
  line earlier.** Your range stop is `math.isqrt(number)` with no `+ 1`:

  ```text
       1 is not prime: primes start at 2.
       2 is prime.
       9 is prime.
  Traceback (most recent call last):
    File "exercise-05-find-prime.py", line 58, in <module>
      main()
      ~~~~^^
    File "exercise-05-find-prime.py", line 50, in main
      assert is_prime(number) == expected, f"is_prime({number}) is wrong"
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: is_prime(9) is wrong
  ```

  Note that `report_primality` printed the wrong answer *before* the assert
  fired. Both implementations failed the same way for the same reason,
  which is a useful reminder: cross-checking only helps when the two
  versions are genuinely independent. A mistake in shared reasoning slips
  through both.

- **`2 is prime.` disappears, and `97 is prime.` prints eight times.** Your
  `else` is attached to the `if` inside the loop instead of to the `for`.
  Python accepts both, so there is no error — only output that has clearly
  lost its mind:

  ```text
       1 is not prime: primes start at 2.
       9 is prime.
       9 is not prime: 3 divides it evenly.
      25 is prime.
      25 is prime.
      25 is prime.
      25 is not prime: 5 divides it evenly.
  ```

  An `else` on the `if` means "print this every time a candidate does *not*
  divide", which is once per failed candidate. So 97 prints `97 is prime.`
  eight times and 7919 prints it eighty-seven times. Look at the second
  line too: `2 is prime.` has vanished entirely, because for 2 the divisor
  loop is empty and an `else` on the `if` never gets a chance to run. The
  fix is indentation only — the `else` belongs at the same column as the
  `f` of `for`.

- **`AssertionError: is_prime(2) is wrong`.** In `is_prime()`, the
  `number % 2 == 0` guard runs before the `number == 2` check, so two is
  rejected for being even before anyone asks whether it is two:

  ```text
       1 is not prime: primes start at 2.
       2 is prime.
  Traceback (most recent call last):
    File "exercise-05-find-prime.py", line 58, in <module>
      main()
      ~~~~^^
    File "exercise-05-find-prime.py", line 50, in main
      assert is_prime(number) == expected, f"is_prime({number}) is wrong"
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: is_prime(2) is wrong
  ```

  Read that transcript carefully. `2 is prime.` printed correctly, because
  `report_primality` has no even-number shortcut at all. Only `is_prime` is
  wrong, and only the assert knows it. That is exactly the disagreement the
  two-implementation design was built to surface.

- **`TypeError: 'float' object cannot be interpreted as an integer`.** You
  used `math.sqrt()` where `math.isqrt()` belongs:

  ```text
    File "exercise-05-find-prime.py", line 22, in report_primality
      for divisor in range(2, math.sqrt(number) + 1):
                     ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: 'float' object cannot be interpreted as an integer
  ```

  `range` takes whole numbers only, and `math.sqrt` hands back a float even
  for a perfect square. The one-character difference between the two names
  is the whole fix.

- **Every number prints both a "not prime" line and an "is prime" line.**
  You left out the `break`. The `else` on a loop runs whenever the loop was
  *not* broken out of, so without a `break` it always runs.

- **`1 is prime.`** The `number < 2` guard is missing, or it sits after the
  loop instead of before it. One divides only by itself, and a prime has to
  have exactly two different divisors.

- **Every odd number is reported prime.** In `is_prime()` you wrote
  `return True` *inside* the loop instead of after it, so the first divisor
  that does not divide ends the function with a yes. That `return True`
  belongs at the function's own level, after the loop has run out of
  candidates.

- **The program pauses noticeably on a big number.** You are looping all
  the way to `number` instead of to its square root. For 7919 that is 7,917
  divisors instead of 87.

## Under the hood

<details>
<summary>Under the hood — the square-root bound, proved in one line, and what it saves</summary>

**The proof.** Suppose `n = a × b` with both `a` and `b` whole numbers
bigger than 1. If both were strictly greater than `√n`, then
`a × b > √n × √n = n`, which contradicts `a × b = n`. So the smaller of the
pair is at most `√n`.

That is the whole thing. One line, and it is why the loop can stop where it
does: if `n` has any divisor at all, its *smallest* one is at or below
`√n`, and a loop counting upwards from 2 meets the smallest one first.

**Why "at or below" and not "below".** The two are the same except when `n`
is a perfect square, where `a` and `b` are both exactly `√n`. That single
case is the entire reason for the `+ 1`, and it is why 9 and 25 sit in the
check list.

**What it saves.** For 7919 the loop runs 87 times instead of 7,917 — about
90 times less work. And the saving grows: the number of candidates is
roughly `√n` instead of `n`, so ten thousand times bigger a number is only
a hundred times more work.

```text
>>> import math
>>> math.isqrt(7919)
88
>>> len(range(2, math.isqrt(7919) + 1))
87
>>> len(range(3, math.isqrt(7919) + 1, 2))
43
```

Skipping the evens halves it again, to 43.

**Where this stops being good enough.** Trial division is fine for testing
one number of moderate size. For a 300-digit number — the size used in the
keys that protect web traffic — `√n` is still a 150-digit number of
candidates, which is more steps than there are atoms in the observable
universe. Real cryptography uses probabilistic tests such as Miller-Rabin,
which answer "almost certainly prime" in a fraction of a second by a
completely different route. The point of trial division is that it is
*obviously* correct. The point of the fast tests is that they are fast, and
proving them correct is somebody's PhD.

**A different job, a different algorithm.** If you want *all* the primes
below some limit rather than one answer about one number, trial division is
the wrong tool entirely. The Sieve of Eratosthenes writes down every number
up to the limit and crosses out the multiples. Finding the 78,498 primes
below a million took the sieve 0.006 seconds on the machine this page was
written on, against 1.26 seconds for trial division on the same range —
about 220 times faster. "Test one" and "find all" look like the same
problem and are not.

</details>

<details>
<summary>Under the hood — the for/else clause, and why it reads so badly</summary>

`for` … `else` is regularly voted the most confusing thing in Python, and
the reason is the word. `else` here does not mean "otherwise". It means
"and if you got all the way through without breaking out".

It is regularly suggested that the keyword should have been `nobreak`. Read
it as `nobreak` in your head and the confusion disappears:

```python
for divisor in candidates:
    if divides(divisor):
        break
nobreak:                     # not real Python — read the else this way
    print("nothing divided it")
```

**When it fires, exactly:**

| What happened in the loop | Does the `else` run? |
| --- | --- |
| The loop ran out of items | yes |
| The sequence was empty to begin with | yes |
| A `break` was hit | no |
| A `return` left the function | no |
| An exception was raised | no |

The second row is the one that bites. An empty loop counts as "ran out",
so the `else` fires. That is exactly what makes 1 dangerous in this
exercise: `math.isqrt(1)` is 1, so `range(2, 2)` is empty, so the loop body
never runs, so the `else` announces that 1 is prime. The `number < 2` guard
is not tidiness — it is the thing standing between you and a wrong answer.

**`while` has one too**, with the same meaning: the `else` runs when the
condition finally goes false, and not when a `break` got you out.

**When to reach for it.** Only for the search shape: look for something,
and do a different thing if it was never found. If your loop is not a
search, a loop `else` will confuse the next reader for no gain. Even for
searches, many people prefer to put the loop in a function and use `return`
— which is precisely what `is_prime()` does, and why this exercise makes
you write both.

**The flag version, for comparison:**

```python
found = False
for divisor in range(2, math.isqrt(number) + 1):
    if number % divisor == 0:
        found = True
        break
if not found:
    print(f"{number} is prime.")
```

Three extra lines, one extra name, and two places where the two have to
agree. It is not wrong. It is just more surface for a mistake to live on,
and the `else` version says the same thing with nothing left over.

</details>

## Acceptance checklist

- [ ] `python exercise-05-find-prime.py` runs with no traceback.
- [ ] All seven report lines match the expected output exactly.
- [ ] The summary line reads `3 of 7 numbers are prime.`
- [ ] `report_primality()` uses `for`/`else` and contains no flag variable.
- [ ] `is_prime()` contains no `print()` and no `break`.
- [ ] `is_prime(2)` is `True` and `is_prime(1)` is `False`.
- [ ] You can say the square-root argument out loud in one sentence.
- [ ] Committed to Git with a message like `Add Week 3 exercise 5: prime check`.

## Stretch

- Write `next_prime(start: int) -> int`, which returns the first prime at
  or above `start`, using `while True` and an early `return`. Check that
  `next_prime(7920)` is 7927 — and notice that you now have a search loop
  with no fixed stopping point at all, which is where `while True` earns
  its keep.
- Count every prime below 100 with your own `is_prime()`:

  ```text
  >>> sum(1 for n in range(2, 100) if is_prime(n))
  25
  ```

  Twenty-five is the right answer. Getting 26 means 1 slipped past your
  lower guard.
- Look up the Sieve of Eratosthenes and write it for the primes below 1000.
  It crosses out multiples instead of testing divisors, and it is far
  faster for finding *all* the primes in a range — though trial division
  still wins for testing one number on its own.
- Add a divisor counter to `report_primality()` and print how many
  candidates it tried before deciding. Compare 97 against 7919 and watch
  the count grow with the square root rather than with the number.

That is the last exercise for Week 3. The patterns you drilled here — the
retry loop, the accumulator, the nested loop, and the search with a `break`
— are all you need for the two bigger builds in
[this week's challenges](../challenges/README.md).
