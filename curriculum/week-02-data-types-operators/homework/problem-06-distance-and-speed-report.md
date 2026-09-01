# Homework Problem 6 — Distance and Speed Report

> **Topic:** named constants, unit conversion, deriving one value from another, a guard against division by zero, and a two-width report
> **Lecture:** [03 — Reading Input and Type Hints](../lecture-notes/03-input-and-type-hints.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour 45 minutes
> **Why this one:** it is the dress rehearsal for Friday's mini-project. A named conversion constant, one value derived from another instead of computed twice, a guard that refuses impossible input, and a report with two different column widths in it. Every one of those turns up again on Friday, unchanged.

## The Brief

Somebody drove 250 kilometres in three and a half hours. Ask for those two
numbers and print a small report:

```text
--- Trip Report ---
Distance : 250.0 km
Time     :   3.5 hours
Speed    :  71.43 km/h
In miles : 155.34 mi
At MPH   :  44.38 mph
```

Five lines. The first two echo back what was typed. The last three are
worked out:

- **Speed** is distance divided by time.
- **In miles** converts the distance. One international mile is defined as
  exactly 1609.344 metres, so there are exactly `1.609344` kilometres in a
  mile. Put that number in a constant:

  ```python
  KM_PER_MILE: float = 1.609344
  ```

  and then `miles = kilometers / KM_PER_MILE`.
- **At MPH** is the same speed in the other unit.

There is one more requirement, and it is the interesting one. **Check that
the time is greater than zero.** If it is not, print
`Error: time must be positive.` and stop. Dividing by zero raises an
exception and stops the program with a traceback; dividing by a negative
number produces a negative speed and no complaint at all. Both are wrong,
and one guard catches both.

That guard needs `if`, and `if` is Week 3. Problems 2 and 4 banned it on
purpose, to make you find out what comparisons can do on their own. Here the
brief asks for a decision that genuinely cannot be a calculation, so you get
`if` early, in its simplest possible form: check the bad case first, say so,
and get out.

## Starter

Save this as `homework-06-distance-speed.py` and fill in the `TODO`s. It
runs as pasted and prints the heading and the two echo lines:

```python
"""TODO: one line saying what this file does."""

KM_PER_MILE: float = 1.609344
LABEL_WIDTH: int = 9
INPUT_WIDTH: int = 6
RESULT_WIDTH: int = 7


def main() -> None:
    """Read distance and time, then print the trip report."""
    kilometers: float = float(input("Distance in kilometers: "))
    hours: float = float(input("Time in hours: "))

    # TODO: if hours is not positive, print the error and return

    kph: float = 0.0  # TODO: kilometers / hours
    miles: float = 0.0  # TODO: kilometers / KM_PER_MILE
    mph: float = 0.0  # TODO: miles / hours

    print("--- Trip Report ---")
    print(f"{'Distance':<{LABEL_WIDTH}}:{kilometers:>{INPUT_WIDTH}.1f} km")
    print(f"{'Time':<{LABEL_WIDTH}}:{hours:>{INPUT_WIDTH}.1f} hours")
    # TODO: three more lines - Speed, In miles, At MPH


if __name__ == "__main__":
    main()
```

There are two numeric widths, not one. The echoed inputs print with one
decimal in a six-column field. The three computed figures print with two
decimals in a seven-column field. The extra decimal place needs the extra
column, which is why `250.0` sits one column to the left of where `155.34`
sits.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/homework/problem-06-distance-and-speed-report.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks for the distance in kilometres, then the time in hours.
2. If the time is not greater than zero it prints exactly
   `Error: time must be positive.` and nothing else, then stops.
3. Otherwise it prints the heading `--- Trip Report ---` and five report
   lines.
4. The conversion factor is a named constant, spelled out in full as
   `1.609344`.
5. `mph` is worked out from `miles`, not by converting `kph` separately.
6. Your output matches the sample block character for character.
7. `main()` is annotated `-> None`, and every variable carries a type hint.

## Constraints

- **Guard before you divide, not after.** The check has to come before any
  division, because the point of it is that the division never happens.
- **Use `<= 0`, not `== 0`.** Checking only for zero lets `-3.5` through,
  and a negative time gives a negative speed with no error at all.
- **The conversion factor is exact — type all seven digits.** `1.6` is not
  close enough. It is wrong by about 0.6%, which is small enough to look
  right and big enough to matter.
- **Derive `mph` from `miles`.** One conversion, used once. Converting `kph`
  separately gives the same answer and puts the constant in two places, and
  two places is one place too many.
- **Two widths, named.** `INPUT_WIDTH` for the echoed values,
  `RESULT_WIDTH` for the computed ones. Naming them is what makes the
  difference deliberate rather than accidental.
- **No space around the colon in the f-strings.** Look closely: it is
  `}:{`, with nothing between. The value's own right-alignment supplies the
  gap. `Distance ` is nine characters, then `:`, then `250.0` right-aligned
  in six columns gives ` 250.0`.

## Expected output

The downloadable file below uses its built-in example trip when nobody is at
the keyboard, so the run is the same every time:

```text
$ python problem-06-distance-and-speed-report.py
--- Trip Report ---
Distance : 250.0 km
Time     :   3.5 hours
Speed    :  71.43 km/h
In miles : 155.34 mi
At MPH   :  44.38 mph
```

Run the same program in your own terminal and it has the conversation
instead:

```text
Distance in kilometers: 250
Time in hours: 3.5
--- Trip Report ---
Distance : 250.0 km
Time     :   3.5 hours
Speed    :  71.43 km/h
In miles : 155.34 mi
At MPH   :  44.38 mph
```

And the validation path:

```text
Distance in kilometers: 250
Time in hours: 0
Error: time must be positive.
```

## Steps

1. Activate your Week 2 environment and `cd` into your `homework/` folder.
2. Save the Starter as `homework-06-distance-speed.py`.
3. Run it as pasted with `250` and `3.5`. The heading and two echo lines
   appear, correctly aligned.
4. Before you write the conversion, check its direction at the terminal:

   ```bash
   python -c "print(250 / 1.609344, 250 * 1.609344)"
   ```

   ```text
   155.3427980593335 402.336
   ```

   A mile is longer than a kilometre, so the number of miles must be
   *smaller*. Dividing is right.
5. Fill in `kph`, `miles` and `mph`, then add the three remaining print
   lines.
6. Run it and compare against the sample, character for character.
7. Now add the guard, above the divisions. Run it with a time of `0`. You
   should get the error line and nothing else. Run it with `-2`. Same.
8. Take the guard out and run with `0` again, so you have seen the
   `ZeroDivisionError` traceback with your own eyes. Put it back.
9. Check your constant is not rounded:

   ```bash
   python -c "KM_PER_MILE = 1.609344; print(1.609344 / KM_PER_MILE)"
   ```

   ```text
   1.0
   ```

   One mile's worth of kilometres is one mile. A rounded constant prints
   something like `0.9996` and you have found your bug.
10. Commit: `git add homework-06-distance-speed.py` then
    `git commit -m "Add distance and speed trip report"`.

## The Solution

```python
"""Distance and speed trip report.

Week 2 homework, problem 6, Code Crunch Convos. Converts a trip in
kilometers and hours into speed, miles, and miles per hour.

Questions go to the error stream and the report goes to the normal output
stream. When nobody is at the keyboard the script uses the example trip.
Save your own copy as ``homework-06-distance-speed.py``.
"""

import sys

KM_PER_MILE: float = 1.609344
LABEL_WIDTH: int = 9
INPUT_WIDTH: int = 6
RESULT_WIDTH: int = 7

SAMPLE_KILOMETERS: str = "250"
SAMPLE_HOURS: str = "3.5"


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str, fallback: str) -> str:
    """Return the typed line, or ``fallback`` when nobody is at the keyboard."""
    if not someone_is_typing():
        return fallback
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        return fallback


def print_report(kilometers: float, hours: float) -> None:
    """Print the trip report, or the error line when ``hours`` is not positive."""
    if hours <= 0:
        print("Error: time must be positive.")
        return

    kph: float = kilometers / hours
    miles: float = kilometers / KM_PER_MILE
    mph: float = miles / hours

    print("--- Trip Report ---")
    print(f"{'Distance':<{LABEL_WIDTH}}:{kilometers:>{INPUT_WIDTH}.1f} km")
    print(f"{'Time':<{LABEL_WIDTH}}:{hours:>{INPUT_WIDTH}.1f} hours")
    print(f"{'Speed':<{LABEL_WIDTH}}:{kph:>{RESULT_WIDTH}.2f} km/h")
    print(f"{'In miles':<{LABEL_WIDTH}}:{miles:>{RESULT_WIDTH}.2f} mi")
    print(f"{'At MPH':<{LABEL_WIDTH}}:{mph:>{RESULT_WIDTH}.2f} mph")


def main() -> None:
    """Read distance and time, then print the trip report."""
    kilometers: float = float(ask("Distance in kilometers: ", SAMPLE_KILOMETERS))
    hours: float = float(ask("Time in hours: ", SAMPLE_HOURS))
    print_report(kilometers, hours)


if __name__ == "__main__":
    main()
```

**Why it works.**

**Two column widths, and the sample tells you which is which.** The echoed
inputs — `Distance` and `Time` — print with one decimal in a six-column
field. The three computed figures — `Speed`, `In miles` and `At MPH` —
print with two decimals in a seven-column field. Measure the sample and you
will find `250.0` sitting one column to the left of `155.34`, because the
extra decimal place needs the extra column. Two named constants make that
distinction deliberate instead of accidental.

Notice there is no space between the closing `}` of the label and the `:`,
and none after it either. The value's own right-alignment supplies the gap.
`Distance ` is nine characters, then `:`, then `250.0` right-aligned in six
columns gives ` 250.0`.

**`mph` is derived from `miles`, not converted from `kph`.** Both routes
give the same answer — `(km / hours) / KM_PER_MILE` equals
`(km / KM_PER_MILE) / hours` — but computing it from the value you already
have says "same trip, different unit" rather than repeating the constant.
One conversion factor, used once.

**`KM_PER_MILE` is exact, and that is not an accident.** One international
mile has been defined since 1959 as exactly 1609.344 metres, so `1.609344`
is the entire value, not a truncation of something longer. Naming it as a
constant is what the brief asks for and what stops `1.609` from creeping in
somewhere and quietly costing you 0.02%.

**The guard runs before any division.** `hours <= 0` catches both zero —
which would raise `ZeroDivisionError` — and negatives, which would produce a
negative speed and no error at all. `return` ends the function immediately,
so the report never prints. Checking `== 0` alone would let `-3.5` straight
through.

**Why `if` is allowed here.** The brief explicitly asks you to validate and
print `Error: time must be positive.` — a single guard clause, which the
Week 2 material has already shown you in passing and which Week 3
formalises. Problems 2 and 4 ban `if` because their decisions really are
calculations in disguise. This one is not.

**A guard clause returns early instead of nesting.** The shape is: name the
bad case, deal with it, leave. Everything after the guard can then assume
the good case, with no extra indentation and no `else`. That shape scales —
a function with four guards at the top is still flat and still readable,
where four nested `if`s would be a staircase.

**`ask()` is the one piece the brief did not ask for.** It lets the
downloadable file run with nobody present, handing back the example trip
when `sys.stdin.isatty()` says there is no terminal with a person at it,
rather than hanging on an `input()` that will never be answered.

## Download and run

Download [problem-06-distance-and-speed-report-solution.py](./problem-06-distance-and-speed-report-solution.py)
and run it:

```bash
python problem-06-distance-and-speed-report-solution.py
```

Run from a terminal, it asks you the two questions. Run by a script or with
its input redirected, it prints the example report instead of hanging. Save
your own copy as `homework-06-distance-speed.py` in your homework folder,
and commit that.

## Common bugs to catch

- **You multiplied instead of dividing.** `kilometers * KM_PER_MILE` turns
  250 km into 402 miles. Sanity-check the direction: a mile is longer than a
  kilometre, so the number of miles must be *smaller*. Every unit conversion
  has that one-question test, and it catches the mistake faster than
  re-deriving the algebra.
- **You rounded `KM_PER_MILE` to `1.6`.** 250 km then reads `156.25 mi`
  instead of `155.34 mi` — a 0.6% error, small enough to look right and big
  enough to be wrong. Type all seven digits.
- **You skipped the guard because "nobody would type zero".** Delete the
  three guard lines, answer `250` and then `0`, and you get:

  ```text
  Traceback (most recent call last):
    File "homework-06-distance-speed.py", line 31, in <module>
      main()
      ~~~~^^
    File "homework-06-distance-speed.py", line 18, in main
      kph: float = kilometers / hours
                   ~~~~~~~~~~~^~~~~~~
  ZeroDivisionError: float division by zero
  ```

  That is what the brief's error message exists to prevent. Note the exact
  wording: `float division by zero`, because both operands are floats. With
  two integers Python says plain `division by zero`.
- **You wrote `== 0` instead of `<= 0`.** A time of `-2` sails through and
  the report shows a speed of `-125.00 km/h`. Nothing crashes.
- **You assumed non-numeric input is handled.** This brief asks for a
  positive-time check, not full input validation, so typing `abc` still
  crashes:

  ```text
    File "homework-06-distance-speed.py", line 16, in main
      hours: float = float(input("Time in hours: "))
                     ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  ValueError: could not convert string to float: 'abc'
  ```

  Wrapping the casts in `try`/`except ValueError` — as Challenge 1 does — is
  a legitimate improvement, not a requirement here. Knowing which one the
  brief asked for is part of reading a brief.
- **The error line went to the wrong place, or the report kept printing.**
  If you forgot the `return`, the guard prints its message and then divides
  by zero anyway.
- **Your columns are one off.** You used the same width for the echoed
  inputs and the computed figures. Six for one decimal, seven for two.

## Under the hood

<details>
<summary>Under the hood — the three division operators, and what zero does to each</summary>

Python has three ways to divide, and they fail differently.

**`/` is true division** and always gives a float, even when the answer is
whole:

```bash
python -c "print(10 / 2, type(10 / 2))"
```

```text
5.0 <class 'float'>
```

**`//` is floor division**, which rounds *down* towards negative infinity —
not towards zero, which is what most people expect:

```bash
python -c "print(7 // 2, -7 // 2, int(-7 / 2))"
```

```text
3 -4 -3
```

`-7 // 2` is `-4` and `int(-7 / 2)` is `-3`. That gap is a real source of
off-by-one bugs.

**`%` is the remainder**, and it is defined so that
`(a // b) * b + (a % b) == a` always holds. A consequence is that the result
takes the sign of the *divisor*, so `-7 % 3` is `2` in Python where many
languages say `-1`. That is what makes `%` safe for wrapping a value round a
circle.

On zero, all three raise — but the message differs by type:

```bash
python -c "
for a, b in ((1, 0), (1.0, 0.0)):
    try:
        a / b
    except ZeroDivisionError as error:
        print(type(a).__name__, '->', error)
"
```

```text
int -> division by zero
float -> float division by zero
```

Quote the message you actually saw. Two different messages for what looks
like the same mistake is exactly the sort of detail that makes a bug report
useful.

Floats have one more trick: `float('inf')` exists, and dividing a finite
number *by* infinity gives `0.0` with no complaint. `0.0 / 0.0` raises, but
`float('inf') / float('inf')` gives `nan` — "not a number" — which then
poisons every calculation it touches without ever raising anything. Guards
are cheaper than hunting a `nan`.

</details>

<details>
<summary>Under the hood — why 1.609344 is exact and most conversion factors are not</summary>

In 1959 the national standards bodies of six countries agreed to define the
international yard as exactly 0.9144 metres. Everything imperial follows
from that by whole-number multiplication: a foot is a third of a yard, a
mile is 1760 yards, and so

```text
1760 * 0.9144 = 1609.344 metres
```

exactly, by definition, with no measurement involved. That is why
`1.609344` terminates. It is not an approximation of a physical quantity; it
is a definition.

The same is true of `2.54` centimetres to the inch, and of `°F = °C * 9/5 +
32`, which is why the mini-project's temperature conversions are exact too.

Most conversion factors are not like this. The astronomical unit, the
electron-volt, anything involving a measured physical constant — those carry
uncertainty and get revised. When you write a conversion constant, it is
worth knowing which kind you are holding.

There is one catch this problem cannot escape. `1.609344` is exact in
decimal and *not* representable exactly in binary:

```bash
python -c "print(f'{1.609344:.20f}')"
```

```text
1.60934400000000010778
```

So `1.609344 / KM_PER_MILE` gives exactly `1.0` — the same imperfect value
divided by itself — while a chain of conversions can drift in the last few
digits. For a trip report printed to two decimals it never shows. For a
program that adds up millions of conversions it eventually does, which is
what `decimal.Decimal` is for.

</details>

## Acceptance checklist

- [ ] Running the file asks for distance, then time.
- [ ] A time of `0` prints exactly `Error: time must be positive.` and
      nothing else.
- [ ] A negative time does the same.
- [ ] A valid trip prints the heading and five report lines.
- [ ] Your output matches the Expected output block character for
      character.
- [ ] `KM_PER_MILE` is a named constant spelled `1.609344`.
- [ ] `mph` is worked out from `miles`, not from `kph`.
- [ ] The echoed inputs and the computed figures use two different named
      widths.
- [ ] `main()` is annotated `-> None` and every variable carries a type
      hint.
- [ ] Committed with a message like `Add distance and speed trip report`.

## Stretch

- Add the pace as well: minutes per kilometre, which is what runners
  actually use. `60 / kph` gives it — `0.84` minutes for this trip, because
  a car is fast. Turn a pace like `4.2` minutes into `4:12` with `divmod()`
  and it starts reading like a running watch.
- Print the time as hours and minutes — `3.5` hours as `3 h 30 m`. `divmod`
  again, and it is the same shape you would use for seconds, or for making
  change.
- Add a third unit: nautical miles, at exactly 1852 metres. That factor is
  also a definition, and adding it will show you whether your program has
  one conversion constant or one conversion *pattern*.
- Guard the distance too. A negative distance is as impossible as a negative
  time, and adding a second guard is where you will feel why guard clauses
  stack better than nested `if`s.
- Pull the conversion out into a function — `def km_to_mi(km: float) ->
  float:` — and give it a docstring. That is exactly the function Friday's
  mini-project asks for, so doing it now is work you do not repeat.

That is the last of the Week 2 homework. When it is pushed, go on to
[the Week 2 mini-project](../mini-project/README.md) and then take
[the quiz](../quiz.md).
