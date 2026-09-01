# Exercise 1 — Function Basics

> **Topic:** `def`, parameters, default values, type hints, docstrings
> **Lecture:** [01 — Defining Functions](../lecture-notes/01-defining-functions.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** every other exercise this week, both challenges and the mini-project assume you can write a function that takes named values, has a sensible fallback, and hands an answer back. This page also plants one habit that saves you a very confusing afternoon later: never put a list or a dict in a function's default slot. That bug bites people in Week 5, and by then it looks like magic.

## The Brief

The neighborhood tool library lends out drills, wheelbarrows and hedge
trimmers the way a book library lends books. People bring things back late.
The volunteer at the desk needs three small pieces of logic: work out the
fee, say it out loud in plain English, and write it into the day's ledger.

That is three functions, and each one teaches a different thing.

**The fee function is about defaults.** The daily rate and the cap are
policy. Policy has a normal setting that almost everybody wants, and a way
for one caller to say "not this time".

**The summary function is about handing a value back instead of printing
it.** A function that prints has already decided where its answer goes. A
function that returns lets whoever called it decide — screen, file, receipt,
test.

**The ledger function is about a trap.** It has a parameter that can hold a
list, and the obvious way to give it a starting value is broken in a way
that hides for months. You are going to write the version that is not
broken, and by the end of the page you will know exactly why.

One number in the brief matters more than it looks: the cap. A tool returned
forty days late must not generate a ten-dollar bill. No single tool ever
costs more than five dollars. A solution that multiplies days by rate and
stops there passes four of the seven checks, which is exactly how a
half-finished thing gets mistaken for a finished one.

## Starter

Create `exercise-01-function-basics.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""exercise-01-function-basics.py — the tool library's late-fee desk.

Fill in every TODO, then run the file. The self-checks at the bottom
print "All checks passed." when the module is correct.
"""

DAILY_RATE = 0.25
FEE_CAP = 5.00


def late_fee(
    days_late: int,
    daily_rate: float = DAILY_RATE,
    cap: float = FEE_CAP,
) -> float:
    """Return the fee owed for bringing a tool back `days_late` days late.

    Args:
        days_late: Whole days past the due date. Zero or negative is on time.
        daily_rate: Dollars charged per late day.
        cap: The most the library will ever charge for one tool.

    Returns:
        The fee in dollars, rounded to two decimals. Never above `cap`.
    """
    # TODO: return 0.0 when days_late is zero or negative
    # TODO: otherwise charge days_late * daily_rate, but never more than cap
    # TODO: round to two decimals before returning
    raise NotImplementedError


def borrower_summary(name: str, tool: str, days_late: int) -> str:
    """Return one line of plain English describing what `name` owes."""
    # TODO: on time -> f"{name} returned the {tool} on time."
    # TODO: late -> f"{name} owes ${fee:.2f} for the {tool} (N day/days late)."
    raise NotImplementedError


def record_fee(entry: str, ledger: list[str] | None = None) -> list[str]:
    """Append `entry` to `ledger` and return it, starting a new one if needed."""
    # TODO: use the None-sentinel pattern from Lecture 1, section 5
    raise NotImplementedError


if __name__ == "__main__":
    assert late_fee(0) == 0.0, late_fee(0)
    assert late_fee(-2) == 0.0, late_fee(-2)
    assert late_fee(3) == 0.75, late_fee(3)
    assert late_fee(5) == 1.25, late_fee(5)
    assert late_fee(40) == 5.00, late_fee(40)
    assert late_fee(4, daily_rate=0.50) == 2.00, late_fee(4, daily_rate=0.50)
    assert late_fee(3, cap=0.50) == 0.50, late_fee(3, cap=0.50)

    print(borrower_summary("Rosa", "hedge trimmer", 5))
    print(borrower_summary("Ken", "socket set", 1))
    print(borrower_summary("Amina", "cordless drill", 0))
    print(borrower_summary("Marcus", "wheelbarrow", 40))

    assert borrower_summary("Ken", "socket set", 1) == (
        "Ken owes $0.25 for the socket set (1 day late)."
    )
    assert borrower_summary("Amina", "cordless drill", 0) == (
        "Amina returned the cordless drill on time."
    )

    first = record_fee("Rosa $1.25")
    second = record_fee("Ken $0.25")
    assert first == ["Rosa $1.25"], first
    assert second == ["Ken $0.25"], second

    running = record_fee("Marcus $5.00")
    record_fee("Priya $0.50", running)
    assert running == ["Marcus $5.00", "Priya $0.50"], running

    print("All checks passed.")
```

Five words you need before you start.

**Parameter and argument.** The names in the `def` line are **parameters** —
labelled empty boxes. The values you hand over when you call it are
**arguments** — what goes in the boxes.

**Default value.** `daily_rate: float = DAILY_RATE` says "if nobody fills
this box, put `DAILY_RATE` in it". The caller can still pass something else.

**Return.** `return` hands one value back to whoever called the function and
stops the function there. A function that never returns anything hands back
`None`, which is Python's word for "nothing".

**Type hint.** `days_late: int` and `-> float` say what kind of value goes
in and what kind comes out. Python does not enforce them. They are a note to
the next reader, and that reader is usually you.

**Docstring.** The `"""..."""` right under the `def` line. It is not a
comment — Python keeps it, and `help(late_fee)` prints it back to you.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/exercises/exercise-01-function-basics.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `late_fee` returns `0.0` for any `days_late` that is zero or negative. An
   early return is fine and reads better than a nested `if`.
2. `late_fee` never returns more than `cap`, no matter how large `days_late`
   gets.
3. `late_fee` rounds to two decimals with `round(value, 2)`. Money with
   fifteen decimal places is not money.
4. `borrower_summary` returns exactly `"{name} returned the {tool} on time."`
   when the fee is zero.
5. Otherwise `borrower_summary` returns exactly
   `"{name} owes ${fee:.2f} for the {tool} ({n} days late)."` — with the word
   `day`, singular, when `days_late` is `1`.
6. `record_fee` uses `None` as its default and creates a fresh list inside
   the body. Every function keeps its type hints and its docstring.

## Constraints

- **Return strings, do not print them.** `borrower_summary` hands a string
  back; only the `__main__` block prints. A function that prints has nothing
  to assert on, nothing to write to a file, and nothing the mini-project's
  report module can reuse. The self-checks on this page could not exist if
  this function printed.
- **No mutable default — never write `ledger: list[str] = []`.** Python runs
  that `[]` once, at the moment `def` executes, and stores the one list it
  made. Every later call that leaves `ledger` out gets that same list, still
  holding everything the last caller put in it. The `first == ["Rosa $1.25"]`
  check exists to catch exactly this.
- **Cap with `min(...)`, then round.** `min(product, cap)` is one operation
  that reads like the policy sentence: "the smaller of what they owe and what
  we are willing to charge". Rounding first and comparing afterwards is two
  operations that can each nudge the number, in an order you then have to
  think about.
- **Use `DAILY_RATE` and `FEE_CAP` as the defaults, not the numbers `0.25`
  and `5.00`.** The day the org votes to raise the rate, you want to change
  one line at the top of the file, not hunt through signatures.
- **Format money with `f"${fee:.2f}"`, not `str(round(fee, 2))`.** Rounding
  is arithmetic. Formatting is presentation. They are not the same job:

  ```text
  str(round(0.5, 2)) = 0.5
  f"${0.5:.2f}" = $0.50
  ```

  A receipt reading `$0.5` looks broken, because it is.

- **Keep `round(value, 2)` even though today's numbers do not need it.** With
  a rate of `0.25` every product in the checks is already exact, so all seven
  pass with the rounding removed. That is luck, not correctness — `0.25` is a
  quarter, and a quarter is one of the few decimal fractions a computer can
  store perfectly. Change one policy number and the luck runs out:

  ```text
  0.30 rate, 3 days: 0.8999999999999999
  0.30 rate, 3 days rounded: 0.9
  0.10 rate, 3 days: 0.30000000000000004
  0.10 rate, 3 days rounded: 0.3
  ```

  Your tests passing does not mean your reasoning was right. It means today's
  inputs did not expose it.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-function-basics.py
Rosa owes $1.25 for the hedge trimmer (5 days late).
Ken owes $0.25 for the socket set (1 day late).
Amina returned the cordless drill on time.
Marcus owes $5.00 for the wheelbarrow (40 days late).
All checks passed.
```

Read the four lines against each other. Rosa is five days late and pays five
quarters. Ken is one day late and gets the word **day**, singular. Amina owes
nothing and gets a completely different sentence. Marcus is forty days late
and pays five dollars, not ten, because the cap held.

## Steps

1. Create the file and paste the starter. Run it once:
   `python exercise-01-function-basics.py`. You get `NotImplementedError`
   from the first assert. That is the correct starting point, not a problem.
2. Fill in `late_fee`. Run again. Work down the asserts one at a time; the
   first failure names the case you missed.
3. Fill in `borrower_summary`. Call `late_fee(days_late)` from inside it
   instead of redoing the multiplication. That is the whole reason `late_fee`
   is a function. It also means the summary inherits the cap for free —
   Marcus gets `$5.00` without `borrower_summary` knowing a cap exists.
4. Fill in `record_fee` with the `None` sentinel, then run until you see
   `All checks passed.`
5. Open a REPL with `python -i exercise-01-function-basics.py` and try
   `help(late_fee)`. Your docstring should print. If nothing useful comes
   out, you wrote a `#` comment where a `"""` string belongs:

   ```text
   Help on function late_fee:

   late_fee(days_late: int, daily_rate: float = 0.25, cap: float = 5.0) -> float
       Return the fee owed for bringing a tool back `days_late` days late.

       Args:
           days_late: Whole days past the due date. Zero or negative is on time.
           daily_rate: Dollars charged per late day.
           cap: The most the library will ever charge for one tool.

       Returns:
           The fee in dollars, rounded to two decimals. Never above `cap`.
   ```

   Two things to notice. The signature shows `0.25` and `5.0`, not
   `DAILY_RATE` and `FEE_CAP` — Python looked those names up when `def` ran
   and kept the values. And `5.00` printed as `5.0`, because they are the
   same number; the trailing zero only ever existed in your source text.

6. In the same REPL, override one default without touching the other:

   ```text
   >>> late_fee(days_late=6, cap=1.00)
   1.0
   ```

   Six days at the standard rate is `1.50`, and the cap you passed pulled it
   down to `1.0`. You never had to restate `daily_rate` to reach past it.
   That is what naming an argument buys you.

## The Solution

```python
"""exercise-01-function-basics-solution.py — the tool library's late-fee desk.

Three small functions. One works out the fee, one says it in plain English,
one writes it into the day's ledger.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

DAILY_RATE = 0.25
FEE_CAP = 5.00


def late_fee(
    days_late: int,
    daily_rate: float = DAILY_RATE,
    cap: float = FEE_CAP,
) -> float:
    """Return the fee owed for bringing a tool back `days_late` days late.

    Args:
        days_late: Whole days past the due date. Zero or negative is on time.
        daily_rate: Dollars charged per late day.
        cap: The most the library will ever charge for one tool.

    Returns:
        The fee in dollars, rounded to two decimals. Never above `cap`.
    """
    if days_late <= 0:
        return 0.0
    return round(min(days_late * daily_rate, cap), 2)


def borrower_summary(name: str, tool: str, days_late: int) -> str:
    """Return one line of plain English describing what `name` owes."""
    fee = late_fee(days_late)
    if fee == 0.0:
        return f"{name} returned the {tool} on time."
    day_word = "day" if days_late == 1 else "days"
    return f"{name} owes ${fee:.2f} for the {tool} ({days_late} {day_word} late)."


def record_fee(entry: str, ledger: list[str] | None = None) -> list[str]:
    """Append `entry` to `ledger` and return it, starting a new one if needed."""
    if ledger is None:
        ledger = []
    ledger.append(entry)
    return ledger


if __name__ == "__main__":
    assert late_fee(0) == 0.0, late_fee(0)
    assert late_fee(-2) == 0.0, late_fee(-2)
    assert late_fee(3) == 0.75, late_fee(3)
    assert late_fee(5) == 1.25, late_fee(5)
    assert late_fee(40) == 5.00, late_fee(40)
    assert late_fee(4, daily_rate=0.50) == 2.00, late_fee(4, daily_rate=0.50)
    assert late_fee(3, cap=0.50) == 0.50, late_fee(3, cap=0.50)

    print(borrower_summary("Rosa", "hedge trimmer", 5))
    print(borrower_summary("Ken", "socket set", 1))
    print(borrower_summary("Amina", "cordless drill", 0))
    print(borrower_summary("Marcus", "wheelbarrow", 40))

    assert borrower_summary("Ken", "socket set", 1) == (
        "Ken owes $0.25 for the socket set (1 day late)."
    )
    assert borrower_summary("Amina", "cordless drill", 0) == (
        "Amina returned the cordless drill on time."
    )

    first = record_fee("Rosa $1.25")
    second = record_fee("Ken $0.25")
    assert first == ["Rosa $1.25"], first
    assert second == ["Ken $0.25"], second

    running = record_fee("Marcus $5.00")
    record_fee("Priya $0.50", running)
    assert running == ["Marcus $5.00", "Priya $0.50"], running

    print("All checks passed.")
```

**The boring case leaves first.** `if days_late <= 0: return 0.0` is the very
first line of the body. Once it has run, everything below it is dealing with
a genuinely late return and nothing else. The alternative wraps the whole
interesting part inside an `else`, one indent deeper, to say the same thing.
Whenever one branch of a decision is short and final, return from it and let
the real work sit flat at the bottom. You will write this shape thousands of
times.

**`min` does the capping, and it does it before `round`.** Read
`round(min(days_late * daily_rate, cap), 2)` from the inside out: multiply,
clamp, round. The clamp is applied to the exact product, and the rounding
happens once, at the end, to a number that is already final.

**`min` also replaces an `if`.** `if fee > cap: fee = cap` is three more
lines doing what `min` does in one. This is not cleverness — `min(product,
cap)` reads as the policy sentence itself.

**The defaults are names, not numbers.** Python looks up `DAILY_RATE` and
`FEE_CAP` once, when `def` runs, and stores what it found. So the policy
lives in two labelled constants at the top of the file. Type `0.25` into the
signature instead and the rate now exists in two places, which is one place
too many.

**`borrower_summary` calls `late_fee`.** This is the single most important
line on the page. The moment you copy `days_late * DAILY_RATE` into the
summary function, two pieces of code claim to know the fee policy, and one
of them will eventually be wrong.

**It branches on `fee == 0.0`, not on `days_late <= 0`.** The requirement is
written in terms of the fee, so the code is too. They agree today. If the org
later adds a one-day grace period, that change belongs in `late_fee` alone,
and `borrower_summary` keeps working without being touched.

**The singular is computed, not hard-coded.** `"day" if days_late == 1 else
"days"` is a conditional expression — one line that picks between two values.
Giving it a name (`day_word`) instead of jamming it into the f-string keeps
the format string readable. English plurals are a real category of bug, and
the check for Ken exists because of it.

**`record_fee` is the trap, defused.** The default is `None` — a value nobody
can append to — and the list gets made inside the body, on each call that
needs one. That is the `None`-sentinel pattern from
[Lecture 1, section 5](../lecture-notes/01-defining-functions.md). Notice
that `record_fee` still changes a list you *pass in*, and that is correct:
the `running` checks at the bottom depend on it. The rule is not "never
change a list". The rule is "never share a default".

## Download and run

Download
[exercise-01-function-basics-solution.py](./exercise-01-function-basics-solution.py)
and run it:

```bash
python exercise-01-function-basics-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-01-function-basics.py`.

## Common bugs to catch

- **`NotImplementedError`.** You ran the file before filling in a `TODO`.
  Expected on the first run. On later runs it means you missed a function.

- **`AssertionError: 10.0` on the `late_fee(40)` check.**

  ```text
  Traceback (most recent call last):
      assert late_fee(40) == 5.00, late_fee(40)
             ^^^^^^^^^^^^^^^^^^^^
  AssertionError: 10.0
  ```

  You multiplied `40 * 0.25` and returned it. Four of the seven `late_fee`
  checks still pass, which is the dangerous part — a half-built function
  looks like a working one until the input gets large. Wrap the product in
  `min(product, cap)`.

- **`AssertionError: ['Rosa $1.25', 'Ken $0.25']` on the check about
  `first`.** The mutable default:

  ```text
  Traceback (most recent call last):
      assert first == ["Rosa $1.25"], first
             ^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: ['Rosa $1.25', 'Ken $0.25']
  ```

  Look at *which* assert failed. Not the one about `second` — the one about
  `first`, a value that was completely correct at the moment you made it and
  got changed afterwards by a call you made later. That is what a shared list
  does, and it is why this bug is so hard to find in a big program: the damage
  happens nowhere near the line that looks wrong.

- **A bare `AssertionError` with no message, on the Ken check.** You
  hard-coded the word `days`, so the function returned `Ken owes $0.25 for the
  socket set (1 days late).` What Python prints is this and nothing more:

  ```text
  Traceback (most recent call last):
      assert borrower_summary("Ken", "socket set", 1) == (
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          "Ken owes $0.25 for the socket set (1 day late)."
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      )
      ^
  AssertionError
  ```

  That assert has no message after the comma, so Python has nothing to print.
  What it does give you, since Python 3.11, is the caret block showing the
  exact expression that came out false. When you get a message-less
  `AssertionError`, print the call yourself and compare by eye:

  ```bash
  python -c "from exercise_01_function_basics import borrower_summary; print(borrower_summary('Ken', 'socket set', 1))"
  ```

  Use `"day" if days_late == 1 else "days"`.

- **A bare `AssertionError` on the Amina check.** You printed the sentence
  instead of returning it. The line appears on your screen, which feels like
  success, and then the check fails anyway — a function with no `return`
  hands back `None`, and `None` is not equal to a string. The starter's
  `print(borrower_summary(...))` calls would also print an extra `None` on
  the following line. Return the string and let the caller decide what to do
  with it.

- **`help(late_fee)` prints nothing useful.** Your docstring is sitting below
  the first `TODO` comment instead of being the very first thing in the body,
  or you used `#` instead of `"""`. Only a string literal in the first
  statement position becomes the function's documentation.

## Under the hood

<details>
<summary>Under the hood — why a list in a default slot is shared, and what the fix costs</summary>

`def` is not a declaration. It is a statement, and it runs, once, when Python
reaches that line in the file. Running it does three things: evaluate every
default value, build one function object, and bind a name to it.

That first step is the whole story. The defaults are evaluated **then**, at
`def` time, and the results are stapled onto the function object where you
can go and look at them:

```python
def record_fee(entry: str, ledger: list[str] = []) -> list[str]:   # broken
    ledger.append(entry)
    return ledger
```

```text
>>> record_fee.__defaults__
([],)
>>> record_fee("Rosa $1.25")
['Rosa $1.25']
>>> record_fee.__defaults__
(['Rosa $1.25'],)
>>> record_fee("Ken $0.25")
['Rosa $1.25', 'Ken $0.25']
```

The default itself grew. There is one list, made once, living on the function
object for as long as the program runs, and every call that omits `ledger`
appends to it.

The `None` sentinel works for two reasons together. `None` is immutable —
there is no `None.append`, so nothing can accumulate in it. And moving `[]`
into the body moves it from code that runs once to code that runs on every
call.

**What the fix costs.** Two things, and they are worth naming rather than
pretending away.

It costs a line of body and a slightly wider type. `list[str] | None` says
the parameter accepts a list *or* nothing, and a reader has to hold both
possibilities for the two lines it takes to collapse them.

And it costs a small ambiguity: after the sentinel runs, `record_fee(entry)`
and `record_fee(entry, None)` behave identically. Almost always that is what
you want. When it is not — when "no argument" and "explicitly nothing" must
mean different things — the standard move is a private sentinel object of
your own:

```python
_MISSING = object()

def record_fee(entry: str, ledger: list[str] | None = _MISSING) -> list[str]:
    if ledger is _MISSING:
        ledger = []
```

Now `None` is a value a caller can pass, distinct from passing nothing at
all. You will see `_MISSING` and `_SENTINEL` in real libraries for exactly
this reason. You do not need it here.

**Why Python does not just fix it.** Because "evaluate the default fresh on
every call" would mean carrying the unevaluated expression around and running
it at call time — which changes what a default *is*, makes every call
slightly slower, and would break the very common case where the default is
deliberately shared, such as a lookup table computed once. The current rule
is simple and consistent: `def` runs once, and everything in the `def` line
runs with it. Immutable defaults — numbers, strings, tuples, `None` — cannot
notice, which is why they are safe.

</details>

<details>
<summary>Under the hood — why 0.25 is exact and 0.30 is not</summary>

A computer stores fractions in binary, the way you store them in decimal. In
decimal you can write one half as `0.5` exactly, but one third goes
`0.3333...` forever. Binary has the same problem with a different set of
numbers.

Binary fractions are halves, quarters, eighths, sixteenths. So anything you
can build by adding those is exact:

```text
0.25 = 1/4                exact
0.5  = 1/2                exact
0.75 = 1/2 + 1/4          exact
```

That is why every check on this page passes without `round`. The daily rate
is a quarter, and multiplying an exact quarter by a whole number gives an
exact answer, every time.

`0.30` is not a sum of halves. In binary it repeats forever, so Python stores
the nearest value it can hold, and the tiny gap shows up as soon as you
multiply:

```text
0.30 rate, 3 days: 0.8999999999999999
0.10 rate, 3 days: 0.30000000000000004
```

Neither of those is a Python bug. Every language with hardware floating point
does this, because they all use the same standard, IEEE 754, which is what
the chip implements.

Three practical rules follow.

**Round at the boundary, not in the middle.** Do the arithmetic at full
precision, then round once when the number becomes an answer someone reads.
Rounding early and then doing more arithmetic accumulates error instead of
removing it.

**Never compare money with `==` before rounding.** `0.1 + 0.2 == 0.3` is
`False`. For anything that arrived by a different arithmetic path, compare
with `math.isclose`, which you meet in Exercise 5.

**For real money, do not use `float` at all.** Python ships
`decimal.Decimal`, which stores base-ten digits and gets `0.1 + 0.2` exactly
right, and banks and ledgers use it. It is slower and wordier, and it is the
correct choice the moment the numbers are somebody's actual money. This
exercise uses `float` because floats are what you will meet first and the
failure mode is worth seeing up close.

</details>

## Acceptance checklist

- [ ] `python exercise-01-function-basics.py` prints four lines and `All checks passed.`
- [ ] Every function has type hints on all parameters and on the return.
- [ ] Every function has a docstring whose first line is a command ("Return
      the fee", not "Returns the fee").
- [ ] `record_fee` has `None` as its default, not `[]`.
- [ ] `borrower_summary` calls `late_fee` instead of recomputing the fee.
- [ ] `help(late_fee)` prints your docstring in the REPL.
- [ ] `late_fee(days_late=6, cap=1.00)` returns `1.0`.
- [ ] Committed to Git with a message like `Add Week 4 exercise 1: function basics`.

## Stretch

- Add a `waive` parameter to `late_fee` that returns `0.0` when it is set,
  and put a bare `*` in front of it so callers must name it:

  ```python
  def late_fee(
      days_late: int,
      daily_rate: float = DAILY_RATE,
      cap: float = FEE_CAP,
      *,
      waive: bool = False,
  ) -> float:
      """Return the fee owed, or 0.0 when the fee has been waived."""
      if waive or days_late <= 0:
          return 0.0
      return round(min(days_late * daily_rate, cap), 2)
  ```

  ```text
  late_fee(40, waive=True) = 0.0
  late_fee(40) = 5.0
  ```

  Now read the two call sites. `late_fee(40, waive=True)` says what it means.
  `late_fee(40, True)` would have meant "a daily rate of `True`", which
  Python happily computes as `40 * True == 40`. Any parameter whose value at
  the call site is a bare `True` or `False` belongs after a `*`.

- Make `late_fee` reject a fractional `days_late` like `2.5`:

  ```python
      if isinstance(days_late, float):
          raise ValueError("days_late must be a whole number")
  ```

  ```text
  late_fee(2.5) -> ValueError: days_late must be a whole number
  ```

  Then decide whether that is a service or an annoyance, and write your
  reasoning in a comment. Two things to notice while you decide. The guard
  has to go *after* the `days_late <= 0` check, or `late_fee(-2.5)` starts
  raising where it used to return `0.0`. And `isinstance(days_late, float)`
  rejects `2.0` as well as `2.5`, which is probably not what you meant —
  `days_late != int(days_late)` is the test you actually want. Writing the
  guard is easy. Deciding exactly what it forbids is the work.

- Add a `daily_ledger_total(ledger: list[str]) -> float` that pulls the
  dollar amounts back out of the ledger strings and adds them up:

  ```python
  def daily_ledger_total(ledger: list[str]) -> float:
      """Return the sum of the dollar amounts in `ledger`."""
      total = 0.0
      for entry in ledger:
          total += float(entry.rsplit("$", 1)[-1])
      return round(total, 2)
  ```

  ```text
  daily_ledger_total(["Rosa $1.25", "Ken $0.25", "Marcus $5.00", "Priya $0.50"]) = 7.0
  ```

  It works, and you should feel uneasy. You wrote a number into a sentence,
  and now you are picking the sentence apart to get the number back. A
  borrower named `A$AP` breaks it entirely. The instinct that the ledger
  should have stored `("Rosa", 1.25)` all along is correct, and Week 5 is
  where you get the tools to act on it.

Next: [Exercise 2 — `*args` and `**kwargs`](./exercise-02-args-kwargs.md).
