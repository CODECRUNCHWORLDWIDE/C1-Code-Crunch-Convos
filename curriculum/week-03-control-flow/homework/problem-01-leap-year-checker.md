# Homework Problem 1 — Leap Year Checker

> **Topic:** an ordered `if`/`elif`/`else` chain, the `%` operator, and validating input before you convert it
> **Lecture:** [01 — Conditionals: Deciding What Runs](../lecture-notes/01-conditionals.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** the leap-year rule is three rules that overlap, and the *order* you test them in is the entire answer. Put them in the wrong order and the program is right three times out of four and wrong on 1900 — no error, no warning, just a quietly incorrect calendar. Every bug you meet for the rest of the course that looks like "it works on my examples" is this bug wearing a different coat.

## The Brief

Most years have 365 days. A year on Earth is actually a bit longer than
that — about a quarter of a day longer — so every four years we add a
day and call it a leap year. February gets 29 days.

But a quarter of a day is not exactly right either. It is slightly less.
So the calendar we use, the **Gregorian calendar**, corrects the
correction:

1. If the year divides by 4, it is a leap year.
2. **Except** if it divides by 100 — then it is not.
3. **Except** if it also divides by 400 — then it is, after all.

Read those three lines again and notice that each one overrules the one
above it. That is not decoration. It is the structure of the code you are
about to write.

| Year | Divides by 4? | Divides by 100? | Divides by 400? | Leap? |
|------|---------------|-----------------|-----------------|-------|
| 2024 | yes | no | no | **yes** |
| 2023 | no | no | no | **no** |
| 1900 | yes | yes | no | **no** |
| 2000 | yes | yes | yes | **yes** |

Your program asks for a year and prints one of two sentences:

```text
2024 is a leap year.
1900 is not a leap year.
```

Those four rows are your test set. A program that gets 2024 and 2023
right has proved nothing. A program that gets 1900 and 2000 right has
proved it understands the rule.

## Starter

Save this as `homework-01-leap-year.py` and fill in the `TODO`s. It runs
as pasted — it just says every year is a leap year, which is wrong on
purpose:

```python
"""Homework 1 - Leap year checker.

Asks for a year and reports whether it is a leap year under the
Gregorian rule.
"""

DIGITS = "0123456789"

# --- read a year, refusing anything that is not a whole number ---
while True:
    raw = input("Enter a year: ").strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number:
        year = int(raw)
        break
    print("Please type a year as a whole number, like 2024.")

# --- the Gregorian rule, most specific test first ---
is_leap = True  # TODO: replace with an if / elif / elif / else chain

if is_leap:
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")
```

The reading loop is given to you complete, because this problem is about
the decision, not about the typing. Read it anyway — you will write it
yourself in problem 3, and by problem 4 you will be sick of it, which is
exactly the point.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/homework/problem-01-leap-year-checker.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks for a year with the prompt `Enter a year: `.
2. It prints `<year> is a leap year.` or `<year> is not a leap year.`,
   with the year spelled the way the person typed it.
3. All four rows of the table in The Brief come out right.
4. A typed word, or an empty line, produces a message and another
   question — never a crash.
5. The decision is a single `if` / `elif` / `elif` / `else` chain, not a
   nest of `if`s inside `if`s.

## Constraints

- **No functions.** `def` is Week 4. Everything sits at the top level of
  the file, in the order it runs.
- **No `try` / `except`.** Exceptions are Week 6. Check the characters
  *before* you hand the string to `int()`. That is not a workaround —
  refusing bad input before you convert it is a habit that outlives the
  day you learn `try`.
- **Test the most specific rule first.** `% 400`, then `% 100`, then
  `% 4`, then everything else. Common bugs to catch shows what the other
  order does to the year 1900.
- **`year % 4` means "the remainder after dividing by 4".** `2024 % 4` is
  `0`, so 2024 divides evenly. `2023 % 4` is `3`, so it does not.
  "Divides by 4" and "`% 4 == 0`" are the same sentence in two
  languages.

## Expected output

The downloadable file below types its own answer — `1900`, the
interesting one — when nobody is at the keyboard, so the run is the same
every time:

```text
$ python problem-01-leap-year-checker.py
Enter a year: 1900
1900 is not a leap year.
```

Run it in your own terminal and it asks you instead. Here is the same
program fed the four table rows, one run each, from Git Bash:

```bash
for y in 2024 2023 1900 2000; do printf "$y\n" | python -u problem-01-leap-year-checker.py 2>&1; done
```

```text
Enter a year: 2024 is a leap year.
Enter a year: 2023 is not a leap year.
Enter a year: 1900 is not a leap year.
Enter a year: 2000 is a leap year.
```

The prompt and the answer run together on one line because piped input
is never echoed back. Nothing was typed between them, so nothing appears
between them.

## Steps

1. Activate your Week 3 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `homework-01-leap-year.py`. Run it. Type `2024`.
   It says leap, which is right by accident.
3. Type `2023`. It still says leap, which is wrong. Now you have
   something to fix.
4. Replace the `is_leap = True` line with the chain. Write the `% 400`
   test first, then `% 100`, then `% 4`, then `else`.
5. Run all four table rows. Do not stop at 2024 and 2023 — 1900 is the
   row that catches the ordering bug and it is the only one that does.
6. Type a word at the prompt. You should get a polite message and
   another question, not a traceback.
7. Compare against **The Solution**, then tick every box in the
   acceptance checklist.
8. Commit: `git add homework/homework-01-leap-year.py` then
   `git commit -m "Week 3 homework: leap year checker"`.

## The Solution

```python
"""Leap year checker.

Week 3 homework, problem 1, Code Crunch Convos.

A year is a leap year when it divides by 4, except centuries, which are
leap years only when they divide by 400.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-01-leap-year.py``, write ``input("Enter a year: ")`` instead.

Questions go to the error stream and the verdict goes to the normal
output stream, so ``python homework-01-leap-year.py > verdict.txt`` saves
the answer and not the questions.
"""

import sys

DIGITS: str = "0123456789"
DEMO_YEAR: str = "1900"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


# Read a year, refusing anything that is not a whole number.
while True:
    raw = ask("Enter a year: ", DEMO_YEAR).strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number:
        year = int(raw)
        break
    print("Please type a year as a whole number, like 2024.")

# The Gregorian rule, most specific test first.
if year % 400 == 0:
    is_leap = True
elif year % 100 == 0:
    is_leap = False
elif year % 4 == 0:
    is_leap = True
else:
    is_leap = False

if is_leap:
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")
```

**Why it works.**

**The order of the chain *is* the algorithm.** The three rules overlap:
every year that divides by 400 also divides by 100 and by 4. All three
tests are true for the year 2000. The only thing that decides the answer
is which test Python reaches first, and an `elif` chain stops at the
first true one and never looks at the rest.

| Year | `% 400 == 0` | `% 100 == 0` | `% 4 == 0` | First branch reached | Answer |
|---|---|---|---|---|---|
| 2000 | true | true | true | `% 400` | leap |
| 1900 | false | true | true | `% 100` | not leap |
| 2024 | false | false | true | `% 4` | leap |
| 2023 | false | false | false | `else` | not leap |

Read down the "first branch reached" column. Every row is caught by a
*different* rule, and no row is ever asked a question that a rule above
it has already settled. That is what a well-ordered chain buys you. You
never have to write "divides by 4 **and not** by 100 **unless** by 400",
because the branches above have already removed those cases.

**The one-expression version, if you prefer it.** The same rule fits on
one line:

```python
is_leap = year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
```

That is correct, and it is what the range extension under **Stretch**
uses, because inside a loop body one expression reads better than four
branches. Keep the parentheses even though `and` binds tighter than `or`
and they change nothing. Without them a reader has to remember Python's
precedence table to check your logic, and code that needs a precedence
table to read is code that will be misread.

**Why validate at all, when the brief did not ask?** Because
`int("twenty")` raises `ValueError` and killing the program is a worse
answer than asking again. The loop strips whitespace, rejects the empty
string with `raw != ""`, then walks the characters and `break`s out of
the *inner* `for` the moment it finds one that is not a digit. There is
no reason to check the rest once one has failed. That `break` leaves the
`for`, not the `while` — `break` only ever exits the innermost loop
([Lecture 2 §11](../lecture-notes/02-loops.md)).

**`ask()` is the one piece the brief did not ask for**, and it is the one
`def` in the file. It exists so this download can be run automatically
and still finish. `input()` with nothing to read raises `EOFError`, so
`ask()` catches that and hands back the example answer instead. Your own
`homework-01-leap-year.py` should call `input("Enter a year: ")`
directly — you have not met `def` or `except` yet, and you do not need
either to answer this question.

**The prompt goes to the error stream.** A program has two ways out:
standard output for the answer, standard error for everything else.
`input("Enter a year: ")` puts the question on standard output, mixed in
with the answer. `print(prompt, end="", file=sys.stderr, flush=True)`
keeps them apart, and the payoff shows up the moment you redirect:
`python homework-01-leap-year.py > verdict.txt` gives you a file with one
clean sentence in it while the question still appears on your screen.
`flush=True` matters because a prompt with no newline on the end would
otherwise sit in a buffer and appear *after* you had already answered
it.

## Run it

Copy the worked answer on this page into `problem-01-leap-year-checker.py` and run it:
and run it:

```bash
python problem-01-leap-year-checker.py
```

Run from a terminal, it asks you for a year. Run by a script, or with its
input redirected, it uses `1900` instead of hanging. Save your own copy
as `homework-01-leap-year.py` in your homework folder, and commit that
one.

## Common bugs to catch

- **The chain runs from most general to most specific.** This is the bug
  the whole problem is built to catch:

  ```python
  if year % 4 == 0:            # WRONG - too general to go first
      is_leap = True
  elif year % 100 == 0:
      is_leap = False
  elif year % 400 == 0:
      is_leap = True
  else:
      is_leap = False
  ```

  There is no error message. It gets three of the four rows right, which
  is exactly why people ship it:

  ```text
  2024 True
  2023 False
  1900 True     <- wrong, 1900 was not a leap year
  2000 True
  ```

  `1900 % 4` is `0`, so the first branch fires and the century rule below
  it is never consulted. Whenever your conditions overlap, the most
  restrictive one goes first.
- **The parentheses go missing in the one-line version.**
  `year % 400 == 0 or year % 4 == 0 and year % 100 != 0` happens to be
  correct, because `and` binds tighter than `or`. The version people
  write when they are trying to be tidy is
  `(year % 400 == 0 or year % 4 == 0) and year % 100 != 0`, which moves
  the century test outside and now reports 2000 as *not* a leap year. If
  you use one expression, group it explicitly and test it on all four
  rows before you trust it.
- **`int(input(...))` with no validation.** Type a word and the program
  dies:

  ```text
  Enter a year: Traceback (most recent call last):
    File "homework-01-leap-year.py", line 3, in <module>
      year = int(input("Enter a year: "))
  ValueError: invalid literal for int() with base 10: 'twenty'
  ```
- **`raw.isdigit()` as the validator.** It is the obvious method and it
  is subtly wrong. `'²'.isdigit()` is `True`, but `int('²')` raises the
  same `ValueError` above. Comparing each character against the literal
  `"0123456789"` asks the question `int()` actually cares about.
- **`if year % 4 == 0 or year % 400 == 0:` with no century branch.** The
  `or` makes the second test pointless — anything divisible by 400 is
  already divisible by 4 — so this is the "divides by 4" rule with extra
  words, and 1900 comes out leap again.

## Under the hood

<details>
<summary>Under the hood — why 1900 was not a leap year and 2000 was</summary>

The rule is not arbitrary. It is arithmetic about the length of a year.

One orbit of the Sun takes about **365.2422** days. A calendar year of
365 days is therefore about `0.2422` days short, and after four years the
calendar has drifted almost a full day behind the sky. Adding one day
every fourth year — the plain "divides by 4" rule — is the fix Julius
Caesar's calendar used from 45 BC.

But `0.2422` is not `0.25`. The Julian rule adds `0.25` days per year and
the sky only needs `0.2422`, so the calendar now runs **fast** by about
`0.0078` days a year. That is one day every 128 years, and by the 1500s
the drift had reached ten days: the spring equinox, which the Church used
to date Easter, had slid from 21 March to 11 March.

The Gregorian reform of 1582 fixed it with two changes. It deleted ten
days once, and it changed the leap rule so the drift could not come back:
**skip the leap day in three centuries out of every four.**

Count what that buys you. In 400 years the Julian rule gives 100 leap
days. The Gregorian rule gives 97 — it skips 1700, 1800 and 1900, and
keeps 2000, because 2000 divides by 400.

```text
Julian    : 400 * 365 + 100 = 146,100 days   -> 365.25    days per year
Gregorian : 400 * 365 +  97 = 146,097 days   -> 365.2425  days per year
Reality   :                                     365.2422  days per year
```

`365.2425` against `365.2422` is an error of `0.0003` days a year, which
is one day roughly every 3,300 years. That is why 1900 was an ordinary
year, why 2000 was a leap year, and why almost nobody alive has seen the
century rule actually fire — the last time it did was 1900, and the next
time will be 2100.

There is a footnote to the footnote. The length of the year is itself
changing slowly, because the Earth's rotation is gradually slowing under
tidal friction. The Gregorian rule has no correction for that. Instead
timekeepers insert **leap seconds** by hand, announced a few months in
advance, which is why no formula can tell you how many seconds there were
in 2016 — you have to look it up.

</details>

<details>
<summary>Under the hood — what % actually computes, and what it does with negatives</summary>

`%` is the remainder operator, and Python defines it so that this
identity always holds for integers:

```text
a == (a // b) * b + (a % b)
```

`//` is floor division: it divides and rounds **down**, towards negative
infinity, not towards zero. Everything surprising about `%` follows from
that one choice.

```bash
python -c "print(7 // 2, 7 % 2, -7 // 2, -7 % 2)"
```

```text
3 1 -4 1
```

`-7 // 2` is `-4`, not `-3`, because `-3.5` rounds *down* to `-4`. Push
that through the identity and `-7 % 2` has to be `1`, not `-1`.

The rule that falls out: **in Python the result of `%` always takes the
sign of the divisor.** `-7 % 2` is `1`; `7 % -2` is `-1`. In C, Java and
JavaScript the result takes the sign of the *dividend* instead, so `-7 %
2` is `-1` there. Same symbol, different answer, and it is a real source
of bugs when you port code.

For this program it means the leap-year test would still work on negative
years — `-400 % 400` is `0` — although the validator rejects the `-`
before the question can come up. Python's choice is the more useful one
in general: `index % length` is always a valid index into a list of that
length, however negative `index` gets, which is exactly what you want for
wrapping a clock face, a ring buffer, or the alphabet in a Caesar cipher.

</details>

## Acceptance checklist

- [ ] Running the file asks `Enter a year: ` and waits.
- [ ] `2024` reports a leap year.
- [ ] `2023` reports not a leap year.
- [ ] `1900` reports **not** a leap year.
- [ ] `2000` reports a leap year.
- [ ] Typing `twenty` prints the retry message and asks again, with no
      traceback.
- [ ] Pressing Enter on an empty line does the same.
- [ ] The decision is one `if` / `elif` / `elif` / `else` chain, most
      specific test first.
- [ ] There is no `def` and no `try` in your own file.
- [ ] Committed with a message like
      `Week 3 homework: leap year checker`.

## Stretch

- **List the leap years in a range.** Ask for a start year and an end
  year and print every leap year between them, inclusive. Three things in
  this version are worth stealing: `for prompt in (...)` runs the same
  validator twice with a different question, which is the closest you can
  get to a function before Week 4; `range(start, end + 1)` is inclusive,
  because `range`'s stop value is not
  ([Lecture 2 §3](../lecture-notes/02-loops.md)); and
  `start, end = end, start` swaps two variables in one line, the same
  tuple move problem 5 uses on the Fibonacci pair.

  ```python
  """Homework 1 extension - list every leap year in a range."""

  DIGITS = "0123456789"

  years = []
  for prompt in ("Start year: ", "End year: "):
      while True:
          raw = input(prompt).strip()
          is_whole_number = raw != ""
          for ch in raw:
              if ch not in DIGITS:
                  is_whole_number = False
                  break
          if is_whole_number:
              years.append(int(raw))
              break
          print("Please type a year as a whole number, like 2024.")

  start, end = years
  if start > end:
      start, end = end, start

  found = 0
  for year in range(start, end + 1):
      if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
          print(year)
          found += 1

  if found == 0:
      print(f"No leap years between {start} and {end}.")
  else:
      print(f"{found} leap year(s) between {start} and {end}.")
  ```

  Test it across a century boundary — 1900 must be missing from the
  middle. `printf '1896\n1910\n' | python homework-01-leap-year-range.py`
  prints `1896`, `1904`, `1908` and then
  `3 leap year(s) between 1896 and 1910.`. Then test a range with no leap
  years at all, `2021` to `2023`, which is the only input that exercises
  the `found == 0` branch.
- **Print how many days are in the year.** 366 or 365, straight off the
  same flag. Then print how many days are in February.
- **Check your program against Python's own calendar.** The standard
  library already knows:
  `python -c "import calendar; print([y for y in (2024, 2023, 1900, 2000) if calendar.isleap(y)])"`
  prints `[2024, 2000]`. Two independent implementations agreeing is the
  cheapest real test there is.
- **Find the next leap year after a given year.** A `while` loop that
  adds one and tests, stopping at the first hit. Try it with 2096 and
  watch it skip 2100.

Next: [Homework Problem 2 — Count Vowels in a String](./problem-02-count-vowels-in-a-string.md).
