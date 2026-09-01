# Challenge 1 — Tip Calculator

> **Topic:** turning typed text into numbers, arithmetic that has to be right, and the format mini-language that makes a column of money line up
> **Lecture:** [02 — Operators and Strings](../lecture-notes/02-operators-and-strings.md)
> **Difficulty:** starter, with one formatting detail that has to be exact
> **Target time:** 45–90 minutes
> **Why this one:** it is the first program you write that produces a *report* rather than a sentence. Getting four numbers to line up under each other is the skill, and every table you print for the rest of the course uses the same tool.

## The Brief

Four people share a meal. The bill is `58.75`. They want to leave a 20%
tip and split the whole thing evenly. Nobody wants to do that in their
head at the table.

Write a program that asks for the bill, the tip percentage, and the
number of people, then prints a small report:

```text
--- Bill Summary ---
Bill       :  $   58.75
Tip (20.0%):  $   11.75
Total      :  $   70.50
Per person :  $   23.50
```

The arithmetic is three lines. The interesting part is the shape.

Look down the page at the colons. They are all in the same place. Look
at the dollar signs — same. Look at the decimal points — same. That does
not happen by accident, and it does not happen by typing spaces until it
looks right. It happens because every line is built from the same two
numbers: **labels are padded to 11 characters**, and **amounts are
right-aligned in a field 8 characters wide**.

Count the first line to see where those come from. `Bill` is four
characters, then seven spaces, and that is 11. Then a colon, then two
spaces, then `$`, then `   58.75` — three spaces and five characters,
which is 8.

Why 11 and not 10? Because of the second line. `Tip (20.0%)` is exactly
eleven characters long, and it is the longest label in the report. Every
other label is padded out to match it. Pick a width smaller than your
longest label and that label pushes its own colon out of line.

> **One thing in the original brief does not add up.** It says amounts
> are right-aligned in a *width-7* field, and then shows you an example
> where they clearly sit in a width-8 one. When a written spec and its
> worked example disagree, go with the example. It is the thing a
> grader compares against, and it is what everybody else on the course
> will have produced. So: 8.

## Starter

Save this as `tip.py` and run it before you change anything. It runs as
pasted — it asks all three questions and then prints a heading with
nothing under it, because the four report lines are the part you write.

```python
"""TODO: one line saying what this file does."""

import sys

LABEL_WIDTH: int = 11
AMOUNT_WIDTH: int = 8
CURRENCY: str = "$"
ERROR_MESSAGE: str = "Error: please enter positive numbers only."

DEMO_BILL: str = "58.75"
DEMO_TIP: str = "20"
DEMO_PEOPLE: str = "3"


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or ``demo`` when nobody answers."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


def main() -> None:
    """Read the three inputs, validate them, print the summary."""
    try:
        bill = float(ask("Bill amount in dollars: ", DEMO_BILL))
        tip_percent = float(
            ask("Tip percentage (e.g. 18 for 18%): ", DEMO_TIP)
        )
        people = int(ask("Number of people: ", DEMO_PEOPLE))
    except ValueError:
        print(ERROR_MESSAGE)
        return

    # TODO 1: refuse any value that is zero or negative.
    # TODO 2: work out tip, total, and per_person.
    # TODO 3: build the tip label, so that 20 becomes "Tip (20.0%)".
    # TODO 4: print the four report lines, using the two widths above.
    print("--- Bill Summary ---")


if __name__ == "__main__":
    main()
```

`ask()` is given to you. It writes the question to the *error stream* —
the second way out of a program, the one used for everything that is not
the answer — and then reads a line. If there is nothing to read, it uses
the demo answer instead and prints it, so the file always produces a
whole session. *Constraints* explains why that matters, and *The
Solution* explains how it works.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/challenges/challenge-01-tip-calculator.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Ask for three values, in this order, with these exact prompts:
   `Bill amount in dollars: `, `Tip percentage (e.g. 18 for 18%): `, and
   `Number of people: `.
2. The bill and the tip percentage are read as `float`. The number of
   people is read as `int`, because a count is a whole number.
3. Compute `tip = bill * (tip_percent / 100)`, then
   `total = bill + tip`, then `per_person = total / people`.
4. Print `--- Bill Summary ---`, then four lines: `Bill`, the tip line,
   `Total`, `Per person`.
5. Every label is left-aligned in 11 characters, followed by `:`, two
   spaces, `$`, and the amount right-aligned in 8 characters with two
   decimal places.
6. The tip label carries the percentage with **one** decimal place, so
   `20` becomes `Tip (20.0%)` and `18.5` stays `Tip (18.5%)`.
7. If any answer is not a number, or if any of the three values is zero
   or negative, print exactly
   `Error: please enter positive numbers only.` and stop without
   printing a summary.
8. Every function has type hints on its parameters and its return, and a
   docstring.
9. The file ends with an `if __name__ == "__main__":` guard.

## Constraints

- **Let the format spec do the counting.** `f"{bill:>8.2f}"` measures the
  number and pads it for you, on every value, forever. Typing the spaces
  yourself works for `58.75` and breaks for `120.00`, and you will not
  notice until somebody runs it on a different bill.
- **The two widths are named constants, used everywhere.** `LABEL_WIDTH`
  and `AMOUNT_WIDTH` appear once each at the top of the file. Widening
  the money column is then one edit instead of four, and the four lines
  cannot drift apart because they all read the same number.
- **Build the tip label first, then pad it.** You cannot format the
  number and pad the finished label in one placeholder: the padding would
  apply to the number, not to the text around it. Two steps, one extra
  variable.
- **Two guards, not one, and in this order.** `try` / `except ValueError`
  catches answers that are not numbers at all. The `if` after it catches
  numbers that parse fine but are nonsense for a bill, like `0` or `-5`.
  The cast has to come first, because you cannot compare `bill` to zero
  until `bill` exists.
- **`int()` for the people, `float()` for the money.** A count is a whole
  number, and `int()` rejects `2.5` for you.
- **The questions answer themselves when nobody is typing.** This is the
  one piece the original brief did not ask for, and it is here so the
  file can be downloaded and run by anybody — you, a classmate, an
  automatic check — and always print the same session. `input()` with
  nothing attached to it raises `EOFError`, or worse, sits there waiting
  for typing that is never coming. `ask()` catches that and falls back to
  the demo answers. Run it in your own terminal and it has the real
  conversation instead. The plain-`input()` version, with no `ask()` at
  all, is under *Stretch* with its own session.
- **Standard library only.** The file imports `sys` and nothing else, so
  it runs on a fresh Python the moment it is downloaded.

## Expected output

Run with nothing attached to its input, the file answers its own
questions from the demo values and prints the report. This is the real
stdout on CPython 3.13.2:

```text
$ python challenge-01-tip-calculator.py
Bill amount in dollars: 58.75
Tip percentage (e.g. 18 for 18%): 20
Number of people: 3
--- Bill Summary ---
Bill       :  $   58.75
Tip (20.0%):  $   11.75
Total      :  $   70.50
Per person :  $   23.50
```

Run it in your own terminal and it asks you instead. A bigger bill and a
tip with a decimal in it, to prove the columns hold:

```text
Bill amount in dollars: 120
Tip percentage (e.g. 18 for 18%): 18.5
Number of people: 4
--- Bill Summary ---
Bill       :  $  120.00
Tip (18.5%):  $   22.20
Total      :  $  142.20
Per person :  $   35.55
```

`120.00` is six characters and `58.75` is five, and both still finish in
the same column, because the field is 8 wide either way.

Both ways of being wrong produce the same message. A bill that is not a
number:

```text
Bill amount in dollars: banana
Error: please enter positive numbers only.
```

And a number that is not a sensible tip:

```text
Bill amount in dollars: 58.75
Tip percentage (e.g. 18 for 18%): 0
Number of people: 3
Error: please enter positive numbers only.
```

Notice the program stopped before printing any summary, and it did not
crash on the way out.

## Steps

1. Save the Starter as `tip.py` and run `python tip.py`. You should see
   the three questions and the `--- Bill Summary ---` heading. Nothing is
   broken; the report lines are missing on purpose.
2. Fill in **TODO 1**. One `if` with three comparisons joined by `or`:
   if the bill, the percentage, or the head count is `<= 0`, print
   `ERROR_MESSAGE` and `return`. `return` inside `main()` ends the
   program.
3. Fill in **TODO 2**. Three lines, straight from requirement 3. Print
   them raw for a moment — `print(tip, total, per_person)` — and check
   that `58.75` at `20`% gives `11.75`, `70.5`, and `23.5`. Do not move
   on with wrong arithmetic.
4. Fill in **TODO 3**. `f"Tip ({tip_percent:.1f}%)"` gives
   `Tip (20.0%)`. Put it in a variable called `tip_label`.
5. Fill in **TODO 4**, one line at a time. Start with the `Bill` line:

   ```python
   print(f"{'Bill':<{LABEL_WIDTH}}:  {CURRENCY}{bill:>{AMOUNT_WIDTH}.2f}")
   ```

   Run it. Compare it to *Expected output* character by character. When
   that one line is right, the other three are the same shape.
6. Run it again with `120`, `18.5`, `4`. The columns should not move.
7. Test both failure paths: type `banana` at the first question, then
   run again and type `0` for the tip.
8. Commit it:

   ```bash
   git add tip.py
   git commit -m "Add Challenge 1: tip calculator"
   ```

## The Solution

```python
"""Tip calculator: read a bill, tip percentage, and party size.

Challenge 1, Week 2, Code Crunch Convos. Prints a four-line summary
with the labels padded to a fixed width and every dollar amount
right-aligned in the same column.

The questions go to the error stream and the summary goes to the normal
output stream, so ``python tip.py > bill.txt`` saves the summary and
nothing else. When the input stream is already finished -- which is what
happens when a checker runs the file -- each question answers itself
from the demo values below instead of waiting for typing that is never
coming.

Run it with::

    python tip.py
"""

import sys

LABEL_WIDTH: int = 11
AMOUNT_WIDTH: int = 8
CURRENCY: str = "$"
ERROR_MESSAGE: str = "Error: please enter positive numbers only."

DEMO_BILL: str = "58.75"
DEMO_TIP: str = "20"
DEMO_PEOPLE: str = "3"


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or ``demo`` when nobody answers.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on when the input stream has
            already ended.

    Returns:
        The line that was typed, or ``demo``. A demo answer is echoed
        after the prompt on the normal output stream, so the printed
        session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


def main() -> None:
    """Read the three inputs, validate them, print the summary."""
    try:
        bill = float(ask("Bill amount in dollars: ", DEMO_BILL))
        tip_percent = float(
            ask("Tip percentage (e.g. 18 for 18%): ", DEMO_TIP)
        )
        people = int(ask("Number of people: ", DEMO_PEOPLE))
    except ValueError:
        print(ERROR_MESSAGE)
        return

    if bill <= 0 or tip_percent <= 0 or people <= 0:
        print(ERROR_MESSAGE)
        return

    tip = bill * (tip_percent / 100)
    total = bill + tip
    per_person = total / people

    tip_label = f"Tip ({tip_percent:.1f}%)"

    print("--- Bill Summary ---")
    print(f"{'Bill':<{LABEL_WIDTH}}:  {CURRENCY}{bill:>{AMOUNT_WIDTH}.2f}")
    print(f"{tip_label:<{LABEL_WIDTH}}:  {CURRENCY}{tip:>{AMOUNT_WIDTH}.2f}")
    print(f"{'Total':<{LABEL_WIDTH}}:  {CURRENCY}{total:>{AMOUNT_WIDTH}.2f}")
    print(
        f"{'Per person':<{LABEL_WIDTH}}:  "
        f"{CURRENCY}{per_person:>{AMOUNT_WIDTH}.2f}"
    )


if __name__ == "__main__":
    main()
```

**The widths are placeholders inside placeholders.** Look closely at
`{bill:>{AMOUNT_WIDTH}.2f}`. There is a `{}` pair *inside* the part after
the colon. Python fills that inner one in first, so at the moment the
line runs it has become `{bill:>8.2f}`. That is why `AMOUNT_WIDTH` can be
a real constant at the top of the file instead of the digit `8` typed out
four times. Change the constant and the whole table re-aligns itself.

**`:<11` and `:>8.2f` are the same little language, in a fixed order.**
Everything after the colon is a *format spec*, and its parts have to come
in the order alignment, width, precision, type. `>8.2f` reads
"right-align, eight columns wide, two digits after the point, print it as
a fixed-point number." Write the pieces in any other order and Python
refuses the whole line — there is a real error message for that in
*Common bugs to catch*.

**The tip label is built, then padded.** `f"Tip ({tip_percent:.1f}%)"`
produces the string `Tip (20.0%)`. Only then does the outer f-string pad
that whole string to eleven characters. Trying to do both in one
placeholder cannot work, because `:<11` would attach to the number, and
the `Tip (` and `%)` around it would not be padded at all.

**`.1f` is what turns `20` into `20.0`.** The user typed `20`, `float()`
made it `20.0`, and `.1f` prints exactly one digit after the point. It
also does the right thing for `18.5`, which stays `18.5`, and for
`20.25`, which becomes `20.2`.

**The validation is two separate nets.** `float("banana")` raises before
you can compare anything, so `try` / `except ValueError` has to catch it.
A bill of `0` parses perfectly well and is still nonsense, so the `if`
catches that. Both print the same message because requirement 7 says so,
and both `return`, which ends `main()` and therefore the program.

**`total / people` is a float even though `people` is an int.** In
Python 3 the `/` operator always hands back a float, whatever you divide.
That is why `per_person` formats cleanly with `.2f` and why you never
have to think about it here.

**`ask()` reads a line, and has an answer ready if there is none.** It
prints the question to `sys.stderr` with `end=""` so the cursor stays on
the same line, and `flush=True` so the text actually appears before the
program starts waiting — the error stream holds unfinished lines in a
buffer otherwise, and a question that shows up after you have answered it
is no use. Then it calls `input()` with no argument, which reads one line
from the input stream. When that stream has already ended, `input()`
raises `EOFError`, and the `except` prints the question and the demo
answer together on the normal output stream and hands the demo answer
back. So the file has a real conversation with a person, reads piped-in
answers when it is given them, and still prints a full session when it is
handed nothing at all.

## Download and run

Download [challenge-01-tip-calculator-solution.py](./challenge-01-tip-calculator-solution.py)
and run it:

```bash
python challenge-01-tip-calculator-solution.py
```

In your own terminal it asks you the three questions. Run by a script,
or with its input closed, it answers itself from the demo values and
prints the same report every time.

You can also feed it the answers from the shell, one per line:

```bash
printf '120\n18.5\n4\n' | python challenge-01-tip-calculator-solution.py
```

Because the questions go to the error stream, `>` captures the report on
its own:

```bash
python challenge-01-tip-calculator-solution.py > bill.txt
```

In your own project, save the same code as `tip.py`.

## Common bugs to catch

**You counted the spaces by hand.** `print("Bill       :  $   " + str(bill))`
reproduces the sample exactly — for `58.75`, and for nothing else:

```text
Bill       :  $   1250.4
```

Six characters instead of five, no trailing zero, column ruined. The
format spec counts on every value; you count once.

**The format spec is backwards.** The single most common formatting
mistake this week. On CPython 3.13.2:

```text
  File "<string>", line 1, in <module>
    x=70.5; print(f"{x:.2f>8}")
                    ^^^^^^^^^
ValueError: Invalid format specifier '.2f>8' for object of type 'float'
```

Alignment and width come before precision and type. `>8.2f`, never
`.2f>8`.

**You built the line with `+` instead of an f-string.**

```text
  File "<string>", line 1, in <module>
    print("Total: " + 70.5)
          ~~~~~~~~~~^~~~~~
TypeError: can only concatenate str (not "float") to str
```

`+` between a string and a float has no meaning in Python. You could wrap
the number in `str()`, and then you have lost the ability to format it.
Use the f-string.

**You cast the head count with `float()` "to be safe".** Now `2.5 people`
sails past your validation and the report is nonsense. Going the other
way, `int()` on something the user typed as `3.0` gives:

```text
  File "<string>", line 1, in <module>
    print(int("3.0"))
          ~~~^^^^^^^
ValueError: invalid literal for int() with base 10: '3.0'
```

`int()` parses whole-number text only. Your `except ValueError` catches
it and reports "please enter positive numbers only," which is a slightly
misleading message for that input. `int(float("3.0"))` is the two-step
version if you want to be generous about it.

**The printed lines do not add up.** Try `58.75` at `22`%:

```text
Bill       :  $   58.75
Tip (22.0%):  $   12.93
Total      :  $   71.67
```

`58.75 + 12.93` is `71.68`, and the report says `71.67`. Nothing is
broken, and this is worth understanding rather than working around — the
first *Under the hood* block below explains exactly what happened.

**`ValueError: could not convert string to float: 'banana'`** with a
traceback instead of your message. The `float()` call is outside the
`try` block, or your `except` line is indented so that it does not belong
to it. The `try:` and its `except ValueError:` must start in the same
column.

**`NameError: name 'tip_label' is not defined`.** You used the label in a
`print` above the line that builds it. Python reads a function body top
to bottom; a name exists only after the line that made it.

## Under the hood

<details>
<summary>Under the hood — why money in a float goes wrong, and what happens at exactly .5</summary>

**The report that does not add up.** Run the `58.75` at `22`% case and
the tip shows `12.93`, the total shows `71.67`, and `58.75 + 12.93` is
`71.68`. Neither number is rounded wrongly. Ask Python to show you what
it is really holding:

```bash
python -c "from decimal import Decimal; print(Decimal(58.75 * (22.0 / 100))); print(Decimal(58.75 + 58.75 * (22.0 / 100)))"
```

```text
12.925000000000000710542735760100185871124267578125
71.6749999999999971578290569595992565155029296875
```

The tip is a hair *above* `12.925`, so `.2f` rounds it up to `12.93`. The
total is a hair *below* `71.675`, so `.2f` rounds it down to `71.67`. The
two stored numbers fall on opposite sides of their midpoints, and the
display is faithfully reporting that.

Computing the total from the *unrounded* tip, as the answer does, is the
correct behaviour. Rounding each line first and adding the rounded
numbers is how a real accounting system slowly drifts away from reality.

**Why floats are like that.** A `float` stores a number in binary, the
way `1/3` in decimal is `0.3333…` and never finishes. In binary, one
tenth never finishes either. So `0.1` is not really `0.1`:

```bash
python -c "print(0.1 + 0.2)"
```

```text
0.30000000000000004
```

Nothing is broken and no version of Python fixes this; it is what the
hardware in every computer you will ever use does with fractions.
Lecture 1 section 4.2 has the short version.

**What to do about it when cents must be exact.** Use the `decimal`
module, which stores numbers the way a person writes them:

```bash
python -c "from decimal import Decimal; print(Decimal('58.75') * Decimal('0.22'))"
```

```text
12.9250
```

Note the quotes around the numbers. `Decimal(58.75)` takes the broken
float and preserves its brokenness exactly, which is how the first
example in this block worked. `Decimal("58.75")` reads the text and gets
the number you meant. Banks and shops use this. A tip calculator at a
dinner table does not need it, and knowing when you *would* need it is
the point.

**And what happens at exactly .5.** Everybody is taught "round half up".
Python does not:

```bash
python -c "print(round(0.5), round(1.5), round(2.5), round(3.5))"
```

```text
0 2 2 4
```

That is **banker's rounding**, also called round-half-to-even: when a
value sits exactly on the midpoint, it goes to whichever neighbour is
even. `0.5` goes down to `0`, `1.5` goes up to `2`, `2.5` goes *down* to
`2`, `3.5` goes up to `4`.

It is not a quirk. Always rounding halves up adds a tiny upward bias to
every total, and over a few million rows of a ledger that bias is real
money. Sending half the ties up and half of them down cancels out. The
IEEE 754 standard that defines floating-point arithmetic makes this the
default, and Python follows it.

`.2f` does the same thing, on values that really are exact midpoints:

```bash
python -c "print(f'{0.125:.2f}', f'{0.375:.2f}')"
```

```text
0.12 0.38
```

`0.125` and `0.375` are two of the rare decimal fractions a binary float
can hold exactly, so both are true ties. `0.125` goes to `0.12` because
`2` is even; `0.375` goes to `0.38` because `8` is even.

Now the trap. This famous "bug" is not banker's rounding at all:

```bash
python -c "print(f'{2.675:.2f}'); print(f'{1.005:.2f}')"
```

```text
2.67
1.00
```

Both look like halves that rounded the wrong way. Neither is a half:

```bash
python -c "from decimal import Decimal; print(Decimal(2.675)); print(Decimal(1.005))"
```

```text
2.67499999999999982236431605997495353221893310546875
1.00499999999999989341858963598497211933135986328125
```

They are both a hair *below* the midpoint, so rounding down is simply
correct. Almost every "Python rounds wrong" report you will ever read is
this, and not the banker's rule. The rule only fires on the handful of
values that a binary float can represent exactly.

</details>

<details>
<summary>Under the hood — the format mini-language, field by field</summary>

Everything after the `:` in a placeholder is a format spec, and it has a
grammar. Written out, with the parts this challenge uses in bold:

```text
[[fill]align][sign][#][0][**width**][,][.**precision**][**type**]
```

The order is fixed. You may leave any part out; you may not shuffle them.

| Piece | What it does | Example |
|---|---|---|
| `fill` | the character to pad with, default a space | `*<11` |
| `align` | `<` left, `>` right, `^` centre, `=` after the sign | `>8` |
| `width` | the smallest number of characters to produce | `8` |
| `,` | group thousands with commas | `,.2f` |
| `.precision` | digits after the decimal point | `.2f` |
| `type` | `f` fixed-point, `d` whole number, `s` text, `%` percent | `f` |

Two of these are worth trying right now:

```bash
python -c "print(f'{1250.4:>12,.2f}|'); print(f'{0.185:.1%}'); print(f'{58.75:*>10.2f}')"
```

```text
    1,250.40|
18.5%
*****58.75
```

The `,` is why a bill of one and a quarter million is readable. The `%`
type multiplies by a hundred and adds the sign, which is another way this
challenge's tip label could have been written. And the fill character is
how a receipt gets its row of dots.

**Nesting.** Any of those pieces can itself be a placeholder, filled in
when the line runs. That is the trick the answer uses:

```bash
python -c "w = 8; print(f'{58.75:>{w}.2f}|'); w = 12; print(f'{58.75:>{w}.2f}|')"
```

```text
   58.75|
       58.75|
```

Same source line, two different widths, because the width came from a
variable.

**This is not f-string-only.** The same mini-language is used by
`str.format` and by the built-in `format`:

```bash
python -c "print(format(58.75, '>8.2f') + '|'); print('{:>8.2f}|'.format(58.75))"
```

```text
   58.75|
   58.75|
```

Under all three spellings the same thing happens: Python calls the
value's own `__format__` method and hands it the spec as a string. Which
is why `f"{None:.2f}"` fails with a message about `NoneType.__format__`
rather than about f-strings — the complaint comes from the value, not
from the syntax.

Lecture 2 section 6.3 is the short reference; the full grammar lives in
the Python documentation under "Format Specification Mini-Language".

</details>

## Acceptance checklist

- [ ] `python tip.py` asks the three questions in the required order,
      with the required wording.
- [ ] Answering `58.75`, `20`, `3` prints the report in *Expected
      output*, character for character.
- [ ] Answering `120`, `18.5`, `4` keeps every colon, dollar sign and
      decimal point in the same column.
- [ ] The tip label shows one decimal place: `Tip (20.0%)`, not
      `Tip (20%)`.
- [ ] `banana` at any prompt prints the error message and no summary.
- [ ] `0` or a negative number at any prompt prints the same error
      message and no summary.
- [ ] Neither failure prints a traceback.
- [ ] `LABEL_WIDTH` and `AMOUNT_WIDTH` are the only places a column
      width appears.
- [ ] No hand-typed run of spaces anywhere in the file.
- [ ] Every function has type hints and a docstring, and no `TODO`
      comments remain.
- [ ] The file ends with the `if __name__ == "__main__":` guard.
- [ ] Four-space indentation, `snake_case` names, lines under 80
      characters.
- [ ] Committed with a message such as `Add Challenge 1: tip calculator`.

## Stretch

**The plain `input()` version.** The graded file uses `ask()` so it can
run with nobody at the keyboard. If you strip that out, the program is
shorter and can only ever be run by hand. Keep it as a second file,
`tip_ask.py`:

```python
"""Tip calculator, keyboard only."""

LABEL_WIDTH: int = 11
AMOUNT_WIDTH: int = 8
CURRENCY: str = "$"
ERROR_MESSAGE: str = "Error: please enter positive numbers only."


def main() -> None:
    """Read the three inputs, validate them, print the summary."""
    try:
        bill = float(input("Bill amount in dollars: "))
        tip_percent = float(input("Tip percentage (e.g. 18 for 18%): "))
        people = int(input("Number of people: "))
    except ValueError:
        print(ERROR_MESSAGE)
        return

    if bill <= 0 or tip_percent <= 0 or people <= 0:
        print(ERROR_MESSAGE)
        return

    tip = bill * (tip_percent / 100)
    total = bill + tip
    per_person = total / people

    tip_label = f"Tip ({tip_percent:.1f}%)"

    print("--- Bill Summary ---")
    print(f"{'Bill':<{LABEL_WIDTH}}:  {CURRENCY}{bill:>{AMOUNT_WIDTH}.2f}")
    print(f"{tip_label:<{LABEL_WIDTH}}:  {CURRENCY}{tip:>{AMOUNT_WIDTH}.2f}")
    print(f"{'Total':<{LABEL_WIDTH}}:  {CURRENCY}{total:>{AMOUNT_WIDTH}.2f}")
    print(
        f"{'Per person':<{LABEL_WIDTH}}:  "
        f"{CURRENCY}{per_person:>{AMOUNT_WIDTH}.2f}"
    )


if __name__ == "__main__":
    main()
```

A real session, typed at a terminal:

```text
$ python tip_ask.py
Bill amount in dollars: 58.75
Tip percentage (e.g. 18 for 18%): 20
Number of people: 3
--- Bill Summary ---
Bill       :  $   58.75
Tip (20.0%):  $   11.75
Total      :  $   70.50
Per person :  $   23.50
```

Identical output, and it hangs the moment nothing is typing at it. That
trade is the whole reason the downloadable file is written the other way.

**All three of the original stretch goals, in one program:** a currency
symbol you can choose, service-quality presets instead of a percentage,
and a per-person amount rounded up to the next whole dollar.

```python
"""Tip calculator, stretch edition: presets, custom currency, round-up split."""

LABEL_WIDTH: int = 11
AMOUNT_WIDTH: int = 8
ERROR_MESSAGE: str = "Error: please enter positive numbers only."
PRESETS: dict[str, float] = {"b": 10.0, "g": 18.0, "e": 22.0}


def round_up_to_dollar(amount: float) -> float:
    """Return ``amount`` rounded up to the next whole dollar."""
    return -(-amount // 1)


def main() -> None:
    """Read inputs (with a service preset), print the padded summary."""
    currency = input("Currency symbol [$]: ").strip() or "$"
    quality = input("Service (b=bad, g=good, e=excellent): ").strip().lower()
    tip_percent = PRESETS.get(quality, 0.0)

    try:
        bill = float(input("Bill amount in dollars: "))
        people = int(input("Number of people: "))
    except ValueError:
        print(ERROR_MESSAGE)
        return

    if bill <= 0 or tip_percent <= 0 or people <= 0:
        print(ERROR_MESSAGE)
        return

    tip = bill * (tip_percent / 100)
    total = bill + tip
    per_person = total / people
    rounded_share = round_up_to_dollar(per_person)
    extra = rounded_share * people - total

    tip_label = f"Tip ({tip_percent:.1f}%)"

    print("--- Bill Summary ---")
    print(f"{'Bill':<{LABEL_WIDTH}}:  {currency}{bill:>{AMOUNT_WIDTH}.2f}")
    print(f"{tip_label:<{LABEL_WIDTH}}:  {currency}{tip:>{AMOUNT_WIDTH}.2f}")
    print(f"{'Total':<{LABEL_WIDTH}}:  {currency}{total:>{AMOUNT_WIDTH}.2f}")
    print(
        f"{'Per person':<{LABEL_WIDTH}}:  "
        f"{currency}{per_person:>{AMOUNT_WIDTH}.2f}"
    )
    print(
        f"{'Rounded up':<{LABEL_WIDTH}}:  "
        f"{currency}{rounded_share:>{AMOUNT_WIDTH}.2f}"
    )
    print(f"{'Extra tip':<{LABEL_WIDTH}}:  {currency}{extra:>{AMOUNT_WIDTH}.2f}")


if __name__ == "__main__":
    main()
```

A real session:

```text
Currency symbol [$]:
Service (b=bad, g=good, e=excellent): e
Bill amount in dollars: 58.75
Number of people: 3
--- Bill Summary ---
Bill       :  $   58.75
Tip (22.0%):  $   12.93
Total      :  $   71.67
Per person :  $   23.89
Rounded up :  $   24.00
Extra tip  :  $    0.33
```

**Custom currency in one line.** `input(...).strip() or "$"` uses the
truthiness rule from lecture 2 section 4.2: `or` gives back the first
operand that counts as yes, and the empty string counts as no. Pressing
Enter therefore gives you `"$"`. The `.strip()` has to come first,
because a string of three spaces is *not* empty and would sail through.

**Service presets in one lookup.** `PRESETS.get(quality, 0.0)` finds the
letter and falls back to `0.0` when the user types something else — and
`0.0` is caught by the `tip_percent <= 0` guard you already wrote, so a
bad answer is rejected for free with no extra code. Dictionaries are
officially Week 5. If you would rather stay inside Week 2's toolbox, the
`if` / `elif` version is three branches and equally correct. Either way,
`.strip().lower()` first, so `" E "` works.

**Rounding up, built out of rounding down.** `-(-amount // 1)` looks like
a magic spell and is not. `//` rounds *toward negative infinity*, which
is lecture 2 section 1.2. So negate, floor, and negate again, and you
have rounded away from negative infinity — that is, up. Follow `23.89`
through it: negate to `-23.89`, floor to `-24.0`, negate to `24.0`.
`extra` is then what the group over-pays, `rounded_share * people -
total`.

That last summary is the float-rounding example from *Under the hood*
wearing a hat: `12.93 + 58.75` does not visibly equal `71.67`, and
`24.00 * 3 - 71.675` is `0.325`, shown as `0.33`.
