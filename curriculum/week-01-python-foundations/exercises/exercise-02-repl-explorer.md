# Exercise 2 — REPL Explorer

> **Topic:** Using the REPL to evaluate expressions and arithmetic
> **Lecture:** [01 — Installing Python and Running Your First Program](../lecture-notes/01-installing-python-and-running-your-first-program.md)
> **Difficulty:** Beginner
> **Target time:** 15 minutes
> **Why this one:** the REPL is where you check a guess in four seconds instead of writing a whole script to find out you were wrong. It is also where Python's arithmetic operators stop being trivia and turn into tools. If `/` versus `//` is still fuzzy when you finish, every counting problem for the next fourteen weeks lands one off.

## The Brief

Your community is hosting a Saturday workshop night. Forty-seven people
have signed up. The tables in the room seat six each. You are ordering
pizza: each pizza is cut into eight slices, you are planning three slices
a person, and a pizza costs thirteen dollars fifty.

Three questions. How many tables? How many pizzas? How much does each
person owe?

Answer them at the `>>>` prompt first, one line at a time, before you
write any file. The `>>>` prompt is the **REPL** — you type one line, it
answers, you type the next. It is a conversation. You ask something small,
you get an answer, and the answer changes what you ask next.

Then write the answers into a file that checks them for you.

Underneath the pizza there is one real idea. Dividing and counting are not
the same job. `/` answers "how much each". `//` answers "how many whole
ones". Neither of them answers "how many do I have to buy", because buying
always rounds *up* — half a pizza is not on the menu. Building that
rounding-up by hand is what makes the two operators stop swapping places
in your head.

## Starter

Start the REPL by typing `python` with no filename after it, then type
these lines. The outputs are missing on purpose. Producing them is the
exercise.

```python
>>> attendees = 47
>>> seats_per_table = 6
>>> attendees / seats_per_table      # TODO: note the value and its type
>>> attendees // seats_per_table     # TODO: how does this differ from /?
>>> attendees % seats_per_table      # TODO: what does this leftover mean?
>>> slices_needed = attendees * 3
>>> slices_needed
>>> slices_needed / 8                # TODO: pizzas, if fractions were sold
>>> -(-slices_needed // 8)           # TODO: pizzas you can actually order
>>> _ * 13.50                        # TODO: what is _ holding? the bill
>>> round(_ / attendees, 2)          # TODO: each person's share
>>> 0.1 + 0.2                        # TODO: this one is not a typo
```

Then make `exercise-02-repl-explorer.py` with this content and fill in the
three `TODO` bodies:

```python
"""exercise-02-repl-explorer.py — the answers from my REPL session, checked."""


def tables_needed(people: int, seats: int) -> int:
    """Return how many tables it takes to seat ``people``, ``seats`` each."""
    # TODO: a partly full table is still a table. // floors; you need a ceiling.
    raise NotImplementedError


def pizzas_needed(people: int, slices_each: int, per_pizza: int) -> int:
    """Return how many whole pizzas feed ``people`` at ``slices_each``."""
    # TODO: same ceiling problem, different numbers.
    raise NotImplementedError


def cost_per_person(pizzas: int, price: float, people: int) -> float:
    """Return one person's share of the bill, rounded to whole cents."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    assert tables_needed(47, 6) == 8
    assert tables_needed(48, 6) == 8
    assert pizzas_needed(47, 3, 8) == 18
    assert pizzas_needed(30, 3, 8) == 12
    assert cost_per_person(18, 13.50, 47) == 5.17
    print("All checks passed.")
```

`assert` is a line that says "this had better be true". If it is, nothing
happens and Python moves on. If it is not, the program stops right there
and tells you which line failed. That is the whole checking machine.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-01-python-foundations/exercises/exercise-02-repl-explorer.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Run every line of the starter session at a live prompt. Reading them
   off this page is not the exercise.
2. `tables_needed(47, 6)` returns `8` — not `7`, and not `7.83...`. Seven
   tables leaves five people standing.
3. `pizzas_needed(30, 3, 8)` returns `12`. Thirty people want ninety
   slices, and eleven pizzas is only eighty-eight. And
   `cost_per_person(18, 13.50, 47)` returns exactly `5.17`.
4. The finished file prints exactly `All checks passed.` and nothing else.
   An `AssertionError` means a function is wrong. Fix the function, never
   the assertion. Keep every type hint and docstring.

## Constraints

- **Get the rounding-up with `-(-a // b)`, not with `round()` or
  `int()`.** `round(11.25)` is `11` and `int(11.25)` is `11`, and both of
  those send two people home hungry. The minus-sign trick stays in whole
  numbers the entire way, so no decimal error can creep in.
- **Do not import `math`.** `math.ceil` is the readable answer and you
  will use it in real code later. Doing it by hand once is what makes `//`
  and `%` stick, and those two are the operators behind page numbers, grid
  layouts, batching and clock arithmetic for the rest of your life.
- **Round money with `round(value, 2)` once, at the very end.** Rounding
  halfway through means you then do arithmetic on the error, and the total
  you print stops matching the total you would actually pay.
- **Type the REPL lines yourself instead of pasting the block.** Pasting
  swallows the answers in between, and those answers are the entire point.

## Expected output

The file is the easy half. Real output, captured on CPython 3.13.2:

```text
$ python exercise-02-repl-explorer.py
All checks passed.
```

That one line is the whole grade for the file, because every check is an
`assert` that keeps quiet when it is happy.

Getting there means the session first. Here is that session, real, typed
one line at a time:

```text
$ python
Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> attendees = 47
>>> seats_per_table = 6
>>> attendees / seats_per_table
7.833333333333333
>>> attendees // seats_per_table
7
>>> attendees % seats_per_table
5
>>> slices_needed = attendees * 3
>>> slices_needed
141
>>> slices_needed / 8
17.625
>>> -(-slices_needed // 8)
18
>>> _ * 13.50
243.0
>>> round(_ / attendees, 2)
5.17
>>> 0.1 + 0.2
0.30000000000000004
>>> exit()
```

Read down the lines that printed nothing: `attendees = 47`,
`seats_per_table = 6`, `slices_needed = attendees * 3`. Those are
**statements** — they do a job and hand back no value, so the REPL has
nothing to show you. Every other line is an **expression** — it works out
to a value, so the REPL prints it. That difference is the most useful
thing the REPL teaches, and it is the whole subject of Exercise 3.

The three answers in words: **eight tables** (seven full, five people at a
part-filled eighth), **eighteen pizzas**, **five dollars seventeen each**.

## Steps

1. Switch on your Week 1 virtual environment, then start the REPL with
   `python` and no filename.
2. Work through the starter session one line at a time, writing each
   answer down. Stop at `attendees % seats_per_table` and say out loud
   what the `5` means. It is not five tables. It is five people at the
   last table.
3. Leave with `exit()`, or Ctrl+D (Ctrl+Z then Enter on Windows).
4. Make the `.py` file, paste the stub in, and fill the three function
   bodies using the operators you just tested. Run it.
5. On an `AssertionError`, reopen the REPL and call the failing function
   with the failing numbers to see what actually came back. Fail, look,
   fix — that loop is the real lesson here.

## The Solution

```python
"""exercise-02-repl-explorer-solution.py — the answers from my REPL session, checked."""


def tables_needed(people: int, seats: int) -> int:
    """Return how many tables it takes to seat ``people``, ``seats`` each."""
    # A partly full table is still a table, so round up. -(-a // b) is the
    # integer ceiling: // floors, and flipping the sign twice floors the
    # other way.
    return -(-people // seats)


def pizzas_needed(people: int, slices_each: int, per_pizza: int) -> int:
    """Return how many whole pizzas feed ``people`` at ``slices_each``."""
    # Same ceiling, applied to total slices rather than total people.
    return -(-(people * slices_each) // per_pizza)


def cost_per_person(pizzas: int, price: float, people: int) -> float:
    """Return one person's share of the bill, rounded to whole cents."""
    # Multiply first, divide second, round once at the very end.
    return round(pizzas * price / people, 2)


if __name__ == "__main__":
    assert tables_needed(47, 6) == 8
    assert tables_needed(48, 6) == 8
    assert pizzas_needed(47, 3, 8) == 18
    assert pizzas_needed(30, 3, 8) == 12
    assert cost_per_person(18, 13.50, 47) == 5.17
    print("All checks passed.")
```

**`-(-a // b)` rounds up by rounding down backwards.** Take it apart from
the inside. `//` always rounds *down* — toward the smaller number on the
number line. For positive numbers that just means throwing the fraction
away, so `90 // 8` is `11`.

Now flip the sign first. `-90 // 8` really works out to `-11.25`, and
rounding *down* from there means going to `-12`, because on the number
line `-12` is the smaller one. The fraction got thrown away in the other
direction. Flip the sign back and you have `12`, which is exactly the
rounding-up you wanted. Turning the number upside down turns "down" into
"up", so one operator gives you both.

Two things make this the right tool rather than a party trick. It **never
touches a decimal**, so there is nothing to lose precision no matter how
big the numbers get. And it is **exact when the division comes out even**:
`-(-48 // 6)` is `8`, not `9`, because there was no fraction to round.

**Why not `round()` or `int()`.** They answer a different question.
`round(11.25)` is `11` and `int(11.25)` is `11`. Both round *down* here,
and for thirty people that is eighty-eight slices against ninety wanted —
two people looking into an empty box. `round()` also has a habit worth
knowing about now:

```text
>>> round(0.5), round(1.5), round(2.5)
(0, 2, 2)
```

Halves go to the nearest *even* number, not upward. That is on purpose:
always pushing halves upward nudges a long column of numbers upward every
single time, and splitting them between up and down cancels out. Either
way, `round()` is never the right way to say "round up".

**Multiply first, divide second, round once.**
`round(pizzas * price / people, 2)` works out `18 * 13.50` to get `243.0`,
divides by `47` to get `5.170212765957447`, and rounds that once. Do it
the other way — one person's share of *one* pizza, then scale it up — and
you round a number that is about to be multiplied by eighteen, so the
rounding error gets multiplied too:

```text
>>> round(13.50 / 47, 2) * 18
5.22
```

Five cents a head, and the total is off by more than two dollars. **Every
early rounding is an error you then do more arithmetic on.** Keep the full
precision until the last possible moment, which is the moment a human
reads the number.

**Why `0.1 + 0.2` is in the assignment.** It is not a typo and Python is
not broken:

```text
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

A decimal number is stored in binary, and `0.1` in binary goes on forever
the same way one third goes on forever in decimal. It has to be cut off
somewhere, so what gets stored is very slightly not `0.1`. Add two
slightly-wrong numbers and you get a slightly-wrong answer. This is why
the two money rules above exist, and why you should never check two
decimals for being equal with `==`.

**`_` is a REPL thing, not a Python thing.** After the REPL shows you a
value, it also stashes that value under the name `_`, which is how
`_ * 13.50` picked up the `18` from the line before. It only updates on
lines that *show* something, so an assignment leaves it alone:

```text
>>> 2 + 2
4
>>> x = 5
>>> _
4
```

Inside a script `_` is just an ordinary name, and using it before you set
it is a `NameError`. Chaining with `_` is great for exploring and terrible
in a file, because every line then depends on the exact order of the lines
above it.

## Download and run

Download [exercise-02-repl-explorer-solution.py](./exercise-02-repl-explorer-solution.py) and run it:

```bash
python exercise-02-repl-explorer-solution.py
```

## Common bugs to catch

- **A bare `AssertionError` with no message.** You used `//` on its own
  and called it done:

  ```text
  Traceback (most recent call last):
    File "exercise-02-repl-explorer.py", line 25, in <module>
      assert tables_needed(47, 6) == 8
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  That is all `assert` ever gives you, which is why the fix is to go to
  the REPL and call the function yourself. `tables_needed(47, 6)` at the
  prompt prints `7`, and now you can see it.

- **An `AssertionError` that only shows up on the second check.**

  ```text
  Traceback (most recent call last):
    File "exercise-02-repl-explorer.py", line 28, in <module>
      assert pizzas_needed(30, 3, 8) == 12
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  You reached for `round()`. `round(141 / 8)` is `18` and passes;
  `round(90 / 8)` is `round(11.25)`, which is `11`, and fails. An answer
  that works on the number you tried and breaks on the one you did not is
  exactly what the second check in each pair is for. When you add a test
  of your own, pick a case where the division lands *close* to a whole
  number.

- **`NotImplementedError`.** You ran the file before filling a body in:

  ```text
  Traceback (most recent call last):
    File "exercise-02-repl-explorer.py", line 25, in <module>
      assert tables_needed(47, 6) == 8
             ~~~~~~~~~~~~~^^^^^^^
    File "exercise-02-repl-explorer.py", line 9, in tables_needed
      raise NotImplementedError
  NotImplementedError
  ```

  Expected, not broken. `raise NotImplementedError` is how a stub says
  "deliberately unfinished" instead of quietly handing back nothing and
  failing somewhere confusing later. Read a traceback bottom-up: the last
  line is where it blew up, the block above is who called it.

- **`SyntaxError: invalid syntax` on a line that looks fine.** You pasted
  the `>>> ` prompt along with the code:

  ```text
  >>> >>> attendees / 6
    File "<stdin>", line 1
      >>> attendees / 6
      ^^
  SyntaxError: invalid syntax
  ```

  `File "<stdin>", line 1` is how the REPL names something you typed
  rather than something from a file. The prompt is Python's output, not
  your input. Copy only what comes after it.

- **`IndentationError: unexpected indent`.** A stray space before your
  expression. The top-level prompt is strict about starting at the very
  first column:

  ```text
  >>>  attendees
    File "<stdin>", line 1
      attendees
  IndentationError: unexpected indent
  ```

- **`TypeError: unsupported operand type(s) for +: 'int' and 'str'`.** You
  wrote `attendees + " people"`:

  ```text
  >>> attendees + " people"
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
      attendees + " people"
      ~~~~~~~~~~^~~~~~~~~~~
  TypeError: unsupported operand type(s) for +: 'int' and 'str'
  ```

  Python will not guess whether you meant text or arithmetic. Use an
  f-string: `f"{attendees} people"`.

- **`48 / 6` prints `8.0`, not `8`.** True division always hands back a
  decimal, even when it divides evenly. Check it yourself with
  `type(48 / 6)`, which says `<class 'float'>`. If you want the whole
  number, use `//`.

- **`NameError: name 'attendees' is not defined` after a restart.** REPL
  variables live in memory and die with the session. That is exactly why
  the second half of this exercise is a file.

## Under the hood

<details>
<summary>Under the hood — what the read-eval-print loop is actually doing</summary>

REPL stands for **read, evaluate, print, loop**, and those are literally
the four steps, in order, forever until you leave.

1. **Read.** It waits for a line, then parses it. If the line is not
   finished — you opened a bracket, or ended with a `:` — it keeps reading
   and shows `...` instead of `>>>`.
2. **Evaluate.** It compiles what you typed and runs it. Your names live
   in one dictionary that stays alive between lines, which is why
   `attendees` is still there three lines later.
3. **Print.** Here is the part people miss. It does not print everything.
   It only prints when the thing you typed was an *expression* — something
   that produces a value — and even then only when that value is not
   `None`. It hands the value to a function called `sys.displayhook`,
   which prints `repr(value)` and then binds it to `_`.
4. **Loop.** Back to step one.

Two consequences fall straight out of step 3.

`attendees = 47` shows nothing because assignment is a statement, not an
expression. It produces no value at all, so there is nothing to hand to
`displayhook`.

`print("hi")` shows `hi` and nothing else, even though `print` is a
function call and function calls are expressions. `print` returns `None`,
and `displayhook` skips `None` on purpose — otherwise every `print` in an
interactive session would be followed by a useless `None`.

`sys.displayhook` is an ordinary variable holding an ordinary function,
and you are allowed to replace it. That is how tools like IPython show
values differently from the plain REPL. You will not need to, but knowing
the printing is a *function call you can see* rather than a built-in
mystery is the point.

</details>

<details>
<summary>Under the hood — floats, 53 bits, and why round() prefers even numbers</summary>

A Python `float` is an IEEE-754 double: one sign bit, eleven bits of
exponent, and fifty-three bits of significand — call it about sixteen
useful decimal digits. Every value has to be a fraction with a power of
two on the bottom. `0.5` is exactly `1/2` and stores perfectly. `0.1` is
`1/10`, and ten is not a power of two, so it stores as the nearest
available binary fraction and stops slightly short.

That explains the wrongness. It does not yet explain the *display*, and
the display is its own story. Since Python 3.1, printing a float shows the
**shortest decimal string that would read back as the same stored value**.
So `0.1` alone prints as `0.1` — that short string does round-trip. But
`0.1 + 0.2` lands on a stored value one notch away from the one `0.3`
gives you, and the shortest string that round-trips to *that* value is
`0.30000000000000004`. Python is not adding noise. It is refusing to hide
a difference that is really there.

Now `round()`. It uses **banker's rounding**: exact halves go to the
nearest even number, so `round(0.5)` is `0` and `round(2.5)` is `2`.
Always rounding halves upward biases a long column of numbers upward,
because you nudge in one direction every single time. Splitting halves
between up and down cancels out across a batch. This is why accountants
have done it this way for a very long time, and it is baked into the
IEEE-754 standard as the default.

There is one more twist. `round(2.675, 2)` gives `2.67`, not `2.68`, and
banker's rounding is not to blame — `2.675` was never exactly `2.675` in
the first place. It stored a hair below, so rounding down is correct for
the number that is actually there.

If you ever need money arithmetic that behaves the way a cashier expects,
the standard library has `decimal.Decimal`, which works in base ten and
lets you choose the rounding rule. It is slower, and for this exercise the
one `round(x, 2)` at the end is the right call.

The assertion `cost_per_person(18, 13.50, 47) == 5.17` gets away with `==`
on a float only because `round(x, 2)` happens to land on exactly the same
stored value as the literal `5.17`. That is a property of this particular
number, not a general licence to compare floats with `==`.

</details>

<details>
<summary>Under the hood — where math.ceil and -(-a // b) actually disagree</summary>

For numbers you can read off a page they agree every time. Make the
numbers big enough and they part company:

```text
>>> a = 10 ** 17 + 1
>>> b = 2
>>> -(-a // b)
50000000000000001
>>> import math
>>> math.ceil(a / b)
50000000000000000
>>> a / b
5e+16
```

`math.ceil` is not wrong. It was handed a wrong number. `a / b` converts
to a float first, and a float has about sixteen useful decimal digits.
`50000000000000000.5` needs seventeen, so it gets rounded to `5e+16`
*before* `ceil` ever sees it, and by then there is no fraction left to
round up.

`-(-a // b)` stays in whole numbers the whole way, and Python's whole
numbers have no size limit at all — they grow as many digits as they need.

The rule: **`math.ceil(a / b)` for numbers you can see, `-(-a // b)` for
numbers you cannot.**

Worth knowing too: `math.ceil` on a float and `//` on integers are not
just different in precision, they are different *machines*. `//` on two
integers is exact integer arithmetic. `math.ceil(a / b)` is float
division, which is one rounding, followed by a ceiling, which cannot
recover what the rounding lost.

</details>

## Acceptance checklist

- [ ] You ran the whole starter session at a live `>>>` prompt.
- [ ] You can say in one sentence each what `/`, `//`, and `%` do.
- [ ] `python exercise-02-repl-explorer.py` prints `All checks passed.`
- [ ] No assertion was edited to make the file pass.
- [ ] Neither `math` nor any third-party package is imported.
- [ ] The file is committed to Git with a message like `Add Week 1 exercise 2: REPL explorer`.

## Stretch

- Add `leftover_slices(people, slices_each, per_pizza)`. For forty-seven
  people it returns `3`: eighteen pizzas is one hundred forty-four slices
  against one hundred forty-one wanted. Have it call `pizzas_needed`
  rather than repeating the rounding-up expression, so that if you later
  decide a half-eaten pizza counts, you change one function and both
  answers follow. Notice the leftover can never reach a whole pizza —
  you would not have bought it.
- Compare `-(-a // b)` with `math.ceil(a / b)` for `a = 10 ** 17 + 1` and
  `b = 2`. They disagree, because `a / b` turns the numbers into decimals
  first and decimals run out of digits at that size, while the whole-number
  version never runs out.
- Explore `divmod(47, 6)`. It gives you `(7, 5)` — the `//` answer and the
  `%` answer as one pair, from one division instead of two. It is the
  idiomatic way to ask "how many whole ones, and what is left", which is
  the exact shape you want for turning seconds into minutes and seconds.

When your checks pass, move on to
[Exercise 3 — Script vs REPL](./exercise-03-script-vs-repl.md).
