# Homework Problem 3 — Leap Year Function With Tests

> **Topic:** returning a comparison instead of branching on it, and writing a second function whose only job is to check the first one
> **Lecture:** [Lecture Note 1 — Defining Functions](../lecture-notes/01-defining-functions.md)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** you wrote the leap-year rule in Week 3 as a chain of `if`s at the top of a file. Now it becomes a function, which means for the first time you can *ask it a question and check the answer* without running the whole program. That is the entire idea behind testing, and this is the smallest problem that shows it.

## The Brief

You met this rule in Week 3. Here it is again, because now you can do
something with it that you could not do then.

A year is normally 365 days. The Earth actually takes about a quarter of a
day longer than that to go around the Sun, so every fourth year we add a
day. But it is slightly *less* than a quarter, so the correction gets
corrected:

1. If the year divides by 400, it is a leap year.
2. Otherwise, if it divides by 100, it is not.
3. Otherwise, if it divides by 4, it is.
4. Otherwise, it is not.

Read those four lines again. Each one only applies to the years the line
above it did not already claim. That ordering is not style. It is the
answer.

Write `is_leap_year(year: int) -> bool`.

Then write a second function, `_run_tests()`, that asks `is_leap_year` six
questions it already knows the answers to:

| Year | Should be |
|------|-----------|
| 2000 | `True` |
| 1900 | `False` |
| 2024 | `True` |
| 2023 | `False` |
| 2100 | `False` |
| 2400 | `True` |

If every answer matches, it prints `All tests passed`. If one does not, it
says which year, what it got, and what it wanted, and stops.

That second function is the real subject of this problem. In Week 3 you
checked your leap-year code by typing years at a prompt and reading the
screen. That works until you change something, and then you have to do it
all again, and you will not, and a bug will get through. A function that
checks another function runs in a tenth of a second and never gets bored.

## Starter

Save this as `leap.py` in your `homework/` folder and fill in the `TODO`s.
It runs as pasted — it just says every year is a leap year and then claims
success, which is a lie you are about to fix:

```python
"""Gregorian leap-year test, plus a self-check."""

CASES: list[tuple[int, bool]] = [
    (2000, True),
    (1900, False),
    (2024, True),
    (2023, False),
    (2100, False),
    (2400, True),
]


def is_leap_year(year: int) -> bool:
    """Return True if `year` is a leap year in the Gregorian calendar.

    Args:
        year: A year number, for example 2024.

    Returns:
        True for a leap year, False otherwise.

    Example:
        >>> is_leap_year(1900)
        False
    """
    # TODO: divisible by 400 -> True
    # TODO: divisible by 100 -> False
    # TODO: otherwise, divisible by 4
    return True


def _run_tests() -> None:
    """Check every case in CASES and report the first failure, or success."""
    # TODO: for each (year, expected) in CASES, compare is_leap_year(year)
    #       against expected. Print a FAIL line and return on the first
    #       mismatch. Print "All tests passed" only after the loop.
    print("All tests passed")


if __name__ == "__main__":
    _run_tests()
```

`CASES` is given to you complete. It is the brief's table, retyped as
Python. Notice that the table is *data* — a list of pairs — and not part
of the checking code. Adding a seventh case will be one line and will not
touch `_run_tests`.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/homework/problem-03-leap-year-function-with-tests.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `is_leap_year` takes an `int` and returns a `bool`.
2. All six rows of `CASES` come out right.
3. `is_leap_year` prints nothing.
4. `_run_tests` prints `All tests passed` when every case matches, and
   nothing else.
5. On the first mismatch, `_run_tests` prints a line naming the year, the
   answer it got and the answer it wanted, then stops.
6. Type hints and a docstring on both functions.
7. Running the file runs the tests. Importing it prints nothing.

## Constraints

- **Test `% 400` first, then `% 100`, then `% 4`.** The three conditions
  overlap: 2000 satisfies all three. The only thing that decides the
  answer is which test Python reaches first. Most specific first, always.
- **Do not write `if condition: return True else: return False`.**
  `year % 4 == 0` is already a `bool`. Return it. The `if`/`else` version
  computes the same answer and then throws it away to build it again by
  hand.
- **`All tests passed` is printed after the loop, not inside it.** A
  message inside the loop prints once per passing case, and — worse —
  prints even when a later case fails. Common bugs to catch has the
  version that always claims success.
- **`_run_tests` stops at the first failure.** With a broken
  `is_leap_year` you get one clear line naming the year, instead of six
  lines you have to compare by eye.
- **No `assert` yet, and no test framework.** A plain `if` and a `print`
  is enough to see the idea. `assert` and `pytest` are Week 6 and beyond;
  what they add is convenience, not concept.

## Expected output

```text
$ python problem-03-leap-year-function-with-tests.py
All tests passed
```

One line. That is what a passing test suite looks like, and it is
supposed to be boring.

But a test you have never seen fail is a test you have not finished
writing. Prove it can fail: swap the first two `if` blocks so the `% 100`
check runs first, and rerun.

```text
FAIL: is_leap_year(2000) -> False, expected True
```

Then put them back. Now try the other classic wrong order — `% 4` first:

```text
FAIL: is_leap_year(1900) -> True, expected False
```

Two different wrong orders, two different years caught. That is why the
table has both 1900 and 2000 in it.

And the docstring example is a real test too:

```bash
python -m doctest leap.py -v
```

The last three lines:

```text
1 test in 3 items.
1 passed.
Test passed.
```

## Steps

1. Activate your Week 4 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `leap.py`. Run it. It prints `All tests passed`,
   which is false — `is_leap_year` returns `True` for everything and
   `_run_tests` never checks anything.
3. Write `_run_tests` first, before you touch `is_leap_year`. Run it. It
   should now fail on 1900, the first year in `CASES` whose answer is
   `False`. A test that fails against broken code is a working test.
4. Now write `is_leap_year`. Three lines: `% 400`, `% 100`, then
   `return year % 4 == 0`.
5. Run it. `All tests passed`.
6. Break it on purpose. Swap the first two `if` blocks, run, read the
   FAIL line, put them back.
7. Run `python -m doctest leap.py -v`.
8. Cross-check against Python's own calendar:
   `python -c "import calendar; print([y for y in (2000, 1900, 2024, 2023, 2100, 2400) if calendar.isleap(y)])"`
   prints `[2000, 2024, 2400]`. Two independent implementations agreeing
   is the cheapest real test there is.
9. Compare against **The Solution**, tick the acceptance checklist, and
   commit: `git add homework/leap.py` then
   `git commit -m "Week 4 homework: leap year function with tests"`.

## The Solution

```python
"""Gregorian leap-year test, plus a self-check that runs with the file.

Week 4 homework, problem 3, Code Crunch Convos.

Save your own copy as ``leap.py`` in your ``homework/`` folder.

``is_leap_year`` answers the question. ``_run_tests`` asks it six times
with answers already known, and says one line about how it went. That
second function is the point of this problem: a function you can check is
worth more than a function you believe.
"""

CASES: list[tuple[int, bool]] = [
    (2000, True),
    (1900, False),
    (2024, True),
    (2023, False),
    (2100, False),
    (2400, True),
]


def is_leap_year(year: int) -> bool:
    """Return True if `year` is a leap year in the Gregorian calendar.

    Args:
        year: A year number, for example 2024.

    Returns:
        True for a leap year, False otherwise.

    Example:
        >>> is_leap_year(1900)
        False
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


def _run_tests() -> None:
    """Check every case in CASES and report the first failure, or success."""
    for year, expected in CASES:
        got = is_leap_year(year)
        if got != expected:
            print(f"FAIL: is_leap_year({year}) -> {got}, expected {expected}")
            return
    print("All tests passed")


if __name__ == "__main__":
    _run_tests()
```

**Why it works.**

**The order of the three checks is the entire problem.** The rules are not
three independent questions you may ask in any order. They are a cascade,
where each later rule only applies to the years the earlier ones did not
claim. Trace all six cases:

| Year | `% 400 == 0` | `% 100 == 0` | `% 4 == 0` | Result | Why |
|------|--------------|--------------|------------|--------|-----|
| 2000 | True | not reached | not reached | `True` | a century, but a 400 one |
| 1900 | False | True | not reached | `False` | a century that is not a 400 |
| 2024 | False | False | True | `True` | ordinary leap year |
| 2023 | False | False | False | `False` | ordinary common year |
| 2100 | False | True | not reached | `False` | same shape as 1900 |
| 2400 | True | not reached | not reached | `True` | same shape as 2000 |

Every row is settled by a different rule, and no row is ever asked a
question a rule above it has already answered. That is what a well-ordered
cascade buys you: you never have to write "divides by 4 **and not** by 100
**unless** by 400", because the lines above have already removed those
years.

**`return year % 4 == 0` returns the comparison itself.** `year % 4 == 0`
evaluates to `True` or `False` on its own. Wrapping it in
`if ...: return True` / `else: return False` computes the boolean, throws
it away, and rebuilds it. Any time you catch yourself returning `True` in
one branch and `False` in the other, delete the branches and return the
condition.

**`CASES` is data and `_run_tests` is the loop that walks it.** The brief
hands you a table; the code holds a table. Adding a case is one line, and
the checking logic never changes. This is the same shape a real test
framework uses underneath — it is just that `pytest` collects the cases
for you instead of you writing them in a list.

**`for year, expected in CASES:` unpacks each pair as it goes.** Each item
of `CASES` is a two-item tuple, and Python spreads it across the two names
in one step. The annotation `list[tuple[int, bool]]` is not required, but
it is what makes that line readable — it says out loud that each item is a
year and a truth value, in that order.

**`_run_tests` returns on the first mismatch.** With a broken
`is_leap_year` that gives you one line naming the guilty year, rather than
six lines to diff by eye. The `print("All tests passed")` sits *after* the
loop, so it is reachable only when the loop ran all the way through
without returning.

## Run it

Copy the worked answer on this page into `problem-03-leap-year-function-with-tests.py` and run it:
and run it:

```bash
python problem-03-leap-year-function-with-tests.py
```

Save your own copy as `leap.py` in your homework folder, and commit that
one. The longer download name keeps it from landing on top of your work.

## Common bugs to catch

- **The classic wrong order.**

  ```python
  def is_leap_year(year: int) -> bool:
      """Return True if year is a leap year. BUGGY."""
      if year % 4 == 0:
          return True
      if year % 100 == 0:
          return False
      return year % 400 == 0
  ```

  This gets 2024, 2023 and 2000 right and fails exactly where the rule is
  interesting:

  ```text
  FAIL: is_leap_year(1900) -> True, expected False
  ```

  1900 divides by 4, so the first branch claims it and the century rule
  never runs. 1900 and 2100 are in the case table specifically to catch
  this.
- **The other wrong order.** Put `% 100` before `% 400` and the mirror
  bug appears:

  ```text
  FAIL: is_leap_year(2000) -> False, expected True
  ```

  2000 divides by 100, gets claimed by the century rule, and never
  reaches the 400 exception that would have rescued it.
- **A self-test that cannot fail.**

  ```python
  for year, expected in CASES:
      if is_leap_year(year) == expected:
          print("All tests passed")     # WRONG
  ```

  This prints once per passing case, and it prints even when a later case
  fails. A test that always says yes is worse than no test at all,
  because it tells you that you are safe. The success message belongs
  after the loop.
- **One big boolean with no parentheses.**

  ```python
  return year % 4 == 0 and year % 100 != 0 or year % 400 == 0
  ```

  This one is actually correct, because `and` binds tighter than `or`.
  But you have to know that to read it, and the version people write when
  they are tidying up is
  `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`, which says
  1900 is a leap year. If you want the one-expression form, put the
  parentheses in: `(year % 4 == 0 and year % 100 != 0) or year % 400 == 0`.
  The three-branch cascade is easier to defend in review.
- **Testing only the easy years.** 2024 and 2023 are settled by the
  plainest rule in the set. Any of the three wrong orderings passes both.
  Every genuinely useful test in this table is a century.
- **Expecting `%` to be friendly to negative years.** `-4 % 400` is `396`
  in Python, not `-4`, because the result of `%` takes the sign of the
  divisor. The Gregorian calendar has no year `-4` anyway, so it is out
  of scope here — but do not be startled if you go poking.

## Under the hood

<details>
<summary>Under the hood — a docstring is not a comment, and the difference is real</summary>

They look similar on the page. They are not the same kind of thing at all.

A **comment** starts with `#`. Python throws it away while it is reading
the file. It exists only in the source text, for a human who is reading
that source text.

A **docstring** is a string literal that is the very first thing inside a
module, a function or a class. Python keeps it, attaches it to the object,
and hands it out on request.

```python
def is_leap_year(year: int) -> bool:
    """Return True if `year` is a leap year in the Gregorian calendar."""
    # Most specific rule first: 400 beats 100 beats 4.
    if year % 400 == 0:
        return True
```

The first line is a docstring, and it survives:

```bash
python -c "from leap import is_leap_year; print(is_leap_year.__doc__.splitlines()[0])"
```

```text
Return True if `year` is a leap year in the Gregorian calendar.
```

The second line is a comment, and there is no way to reach it from a
running program. It is gone.

That difference drives everything else:

- `help(is_leap_year)` prints the docstring. It has nothing to print for
  a comment.

  ```bash
  python -c "import leap; help(leap.is_leap_year)"
  ```

  ```text
  Help on function is_leap_year in module leap:

  is_leap_year(year: int) -> bool
      Return True if `year` is a leap year in the Gregorian calendar.

      Args:
          year: A year number, for example 2024.
  ```

- Your editor shows the docstring in a tooltip when you hover a call.
- Documentation generators read docstrings and build a website from
  them.
- `doctest` runs the `>>>` lines inside a docstring as real tests. It
  cannot see comments.

The rule of thumb that follows: **a docstring says what the function is
for, from the point of view of somebody calling it. A comment says why
the code inside is written the way it is, for somebody changing it.**

```python
def c_to_k(celsius: float) -> float:
    """Convert Celsius to Kelvin. Raises ValueError below absolute zero."""
    # `<` not `<=`: absolute zero itself is a legal temperature.
    if celsius < ABSOLUTE_ZERO_C:
        ...
```

A caller needs the first sentence and does not care about the second. A
maintainer needs both.

The layout convention this course uses — a one-line summary, a blank
line, then `Args:`, `Returns:`, `Raises:` and `Example:` — is Google
style, and [Lecture Note 1 §8](../lecture-notes/01-defining-functions.md)
picked it. [PEP 257](https://peps.python.org/pep-0257/) is the rule that
says the summary line is a sentence ending in a full stop, written as a
command — "Return the total", not "Returns the total" and not "This
function returns the total".

One last thing worth knowing. A comment that restates the code is noise:

```python
score = score + 1   # add one to score
```

A docstring that restates the signature is the same noise:

```python
def add(a: int, b: int) -> int:
    """Add a and b."""     # says nothing the signature did not
```

The useful version says something the code cannot: what the units are,
what happens at the edges, what it does when the input is wrong.

</details>

<details>
<summary>Under the hood — what doctest actually does with those Example: blocks</summary>

Every `Example:` block in this week's answers is a real, runnable test,
and it costs nothing extra to write because it was going in the docstring
anyway.

```python
    Example:
        >>> is_leap_year(1900)
        False
```

`doctest` reads the docstring, finds every line starting with `>>> `,
runs it, and compares what came back against the lines underneath.

```bash
python -m doctest leap.py
```

Silence. That is a pass, and it is unnerving the first time. Ask for the
count instead:

```bash
python -m doctest leap.py -v
```

The last three lines:

```text
1 test in 3 items.
1 passed.
Test passed.
```

"3 items" is the module plus the two functions — the three places a
docstring could live. "1 test" is the one `>>>` line among them.

The comparison is **textual**, and that is the whole character of the
tool. Whatever the expression evaluates to is turned into text with
`repr` and matched character for character against what you wrote. Which
means:

- `'strong'` needs its quotes, because that is how a string reprs.
- `212.0` is not `212`, because a float reprs with its point.
- `233.15` fails for `c_to_k(-40)`, because the true value is
  `233.14999999999998`. Problem 1's block on floating point says why.
- Dict order matters, because dicts print in insertion order.

That strictness is the trade. `doctest` is the cheapest possible way to
keep an example honest — an example that drifts out of date turns into a
failing test the moment anybody runs it — and it is the wrong tool for
anything with a fiddly output format. For those, you want the real thing:
`assert`, and eventually `pytest`.

Which is where `_run_tests` is heading. Written with `assert`, it is
three lines:

```python
def _run_tests() -> None:
    """Check every case in CASES."""
    for year, expected in CASES:
        assert is_leap_year(year) == expected, f"{year} should be {expected}"
    print("All tests passed")
```

`assert` raises `AssertionError` when its condition is false, and the
message after the comma goes into the traceback. That is genuinely
better — it stops the program, so a failing test cannot be ignored. It is
held back to Week 6 only because exceptions are Week 6, and there is
nothing in the idea of testing that needs them.

</details>

## Acceptance checklist

- [ ] `python leap.py` prints exactly `All tests passed`.
- [ ] You have seen it print a `FAIL:` line at least once, on purpose.
- [ ] `is_leap_year(2000)` is `True` and `is_leap_year(1900)` is `False`.
- [ ] `is_leap_year(2100)` is `False` and `is_leap_year(2400)` is `True`.
- [ ] `is_leap_year` contains no `print`.
- [ ] The last line of `is_leap_year` returns a comparison, not `True` or
      `False` from an `if`/`else`.
- [ ] `All tests passed` is printed after the loop, not inside it.
- [ ] Both functions have type hints and a docstring.
- [ ] `python -m doctest leap.py -v` ends with `Test passed.`
- [ ] `python -c "import leap"` prints nothing.
- [ ] Committed with a message like
      `Week 4 homework: leap year function with tests`.

## Stretch

- **Report every failure, not just the first.** Count the mismatches in
  the loop and print `3 of 6 cases failed` at the end. Stopping early is
  right when you are fixing one bug; a full report is right when you have
  just rewritten the function and want the whole picture.
- **Check yourself against the standard library.** `calendar.isleap` has
  been in Python since 1994 and is certainly correct. Add a second loop
  that compares your answer to `calendar.isleap(year)` for every year
  from 1583 to 2400 and prints how many disagreed. The answer should be
  zero, across 818 years, in well under a second.
- **Add `days_in_year(year: int) -> int`.** Return `366` or `365`
  straight off `is_leap_year`. Then `days_in_february`. Two-line functions
  built out of a function you already trust are the cheapest code you
  will ever write.
- **Rewrite `_run_tests` with `assert`.** The version is in the second
  Under the hood block. Then make one case wrong and read the traceback —
  notice that the program *stops*, which is the difference between a test
  and a print.
- **Find the leap years in a century.** Print every leap year from 1900
  to 2000 inclusive, using a list comprehension over
  `range(1900, 2001)`. Count them. The answer is 25 and not 26, and the
  missing one is 1900 itself, which is the century rule visible in a
  single number.

Next: [Homework Problem 4 — Recursive Sum](./problem-04-recursive-sum.md).
