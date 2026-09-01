# Homework Problem 1 — Simple Interest Calculator

> **Topic:** f-string format specs, field width, thousands separators, and casting `input()` to a number
> **Lecture:** [02 — Operators and Strings](../lecture-notes/02-operators-and-strings.md)
> **Difficulty:** Beginner
> **Target time:** 1 hour
> **Why this one:** it is the first program you write where the *shape* of the output is part of the answer. Getting the arithmetic right takes one line. Getting five numbers to line up in a column takes the rest of the hour, and that skill shows up in every report, table and receipt you will ever print.

## The Brief

Simple interest is the easiest kind of interest there is. You lend somebody
money, and every year they pay you the same slice of what you originally
lent. The slice never grows.

```text
interest = principal * (rate / 100) * years
```

Three words to name before you use them:

- **Principal** is the starting money. If you put $1,000 in, the principal
  is 1000.
- **Rate** is the percentage per year. You will type `5` for 5%, so the
  program has to divide by 100 to turn "5 percent" into the fraction
  `0.05`.
- **Years** is how long the money sits there.

Ask the person for those three numbers, then print a five-line report:
principal, rate, years, the interest earned, and the total they end up
with.

The report is the hard part. Look at it:

```text
Principal : $    1,000.00
Rate      :        5.00%
Years     :            3
Interest  : $      150.00
Total     : $    1,150.00
```

Every colon sits in the same column. Every number's last digit sits in the
same column. Nothing in that block is an accident, and you are not allowed
to fake it by typing spaces by hand — Python has to produce it from the
numbers.

## Starter

Save this as `homework-01-simple-interest.py` and fill in the `TODO`s. It
runs as pasted and prints one line of the report:

```python
"""TODO: one line saying what this file does."""

LABEL_WIDTH: int = 10
FIELD_WIDTH: int = 12


def main() -> None:
    """Read principal, rate, and years, then print the five-line report."""
    principal: float = float(input("Principal in dollars: "))
    rate: float = float(input("Annual interest rate in percent: "))
    years: int = int(input("Number of years: "))

    interest: float = 0.0  # TODO: principal * (rate / 100) * years
    total: float = 0.0  # TODO: principal + interest

    print(f"{'Principal':<{LABEL_WIDTH}}: ${principal:>{FIELD_WIDTH},.2f}")
    # TODO: four more lines - rate, years, interest, total


if __name__ == "__main__":
    main()
```

`LABEL_WIDTH` and `FIELD_WIDTH` are the two measurements the whole report is
built from. A label is padded out to ten characters so the colons line up. A
number is padded out to twelve so the digits line up. Everything else is
just choosing which of the two to use.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/homework/problem-01-simple-interest-calculator.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks for the principal, the annual rate in percent, and the
   number of years, in that order.
2. It prints exactly five lines, in the order shown in The Brief.
3. The dollar amounts carry a thousands separator and exactly two decimal
   places — `1,000.00`, not `1000.0`.
4. The rate prints with two decimal places and a trailing `%`.
5. The years print as a whole number with no decimal point.
6. Every column in your output lines up with the sample, character for
   character.
7. `main()` is annotated `-> None`, and every variable you create carries a
   type hint.

## Constraints

- **Cast every `input()` before you do arithmetic with it.** `input()` hands
  back a string, always, even when the person typed digits. `float(...)`
  around the ones that can have decimals, `int(...)` around the years.
- **Use format specs, not `round()`.** `round(total, 2)` changes the
  *number*. `:.2f` changes how the number is *written down*. For a report
  you want the second one, and Common bugs to catch shows what happens when
  you reach for the first.
- **Name the widths.** `LABEL_WIDTH` and `FIELD_WIDTH` at the top, used
  everywhere. Typing `12` and `11` directly into five f-strings means the
  next person has to measure your output with a ruler to work out why those
  numbers.
- **Do not print the `$` inside the number's field.** The dollar sign is a
  plain character in the f-string, sitting outside the braces. The number
  gets its own twelve columns after it.

## Expected output

The downloadable file below uses its built-in example figures when nobody
is at the keyboard, so the run is the same every time:

```text
$ python problem-01-simple-interest-calculator.py
Principal : $    1,000.00
Rate      :        5.00%
Years     :            3
Interest  : $      150.00
Total     : $    1,150.00
```

Run the same program in your own terminal and it has the conversation
instead. Here is a real session:

```text
Principal in dollars: 1000
Annual interest rate in percent: 5
Number of years: 3
Principal : $    1,000.00
Rate      :        5.00%
Years     :            3
Interest  : $      150.00
Total     : $    1,150.00
```

## Steps

1. Activate your Week 2 environment and `cd` into your `homework/` folder.
2. Save the Starter as `homework-01-simple-interest.py`.
3. Fill in `interest` and `total`. Run it. One line appears and the number
   in it is already right.
4. Add the `Interest` and `Total` lines. They are the `Principal` line with
   a different label and a different variable. Run it again.
5. Add the `Years` line. Use `d`, not `f`, and watch the `.00` disappear.
6. Add the `Rate` line last, because it is the awkward one. The `%` takes a
   column of its own, so the number gets `FIELD_WIDTH - 1`.
7. Put your output side by side with the sample and compare the two blocks
   character for character. If a column is off by one, a width is off by
   one.
8. Commit: `git add homework-01-simple-interest.py` then
   `git commit -m "Add simple interest calculator"`.

## The Solution

```python
"""Simple-interest calculator.

Week 2 homework, problem 1, Code Crunch Convos.
interest = principal * (rate / 100) * years

Questions go to the error stream and the report goes to the normal output
stream, so ``python homework-01-simple-interest.py > report.txt`` saves the
report and nothing else. When nobody is at the keyboard the script uses the
example figures rather than waiting for typing that is never coming. Save
your own copy as ``homework-01-simple-interest.py``.
"""

import sys

LABEL_WIDTH: int = 10
FIELD_WIDTH: int = 12

SAMPLE_PRINCIPAL: str = "1000"
SAMPLE_RATE: str = "5"
SAMPLE_YEARS: str = "3"


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


def print_report(principal: float, rate: float, years: int) -> None:
    """Print the five-line simple-interest report."""
    interest: float = principal * (rate / 100) * years
    total: float = principal + interest

    print(f"{'Principal':<{LABEL_WIDTH}}: ${principal:>{FIELD_WIDTH},.2f}")
    print(f"{'Rate':<{LABEL_WIDTH}}: {rate:>{FIELD_WIDTH - 1}.2f}%")
    print(f"{'Years':<{LABEL_WIDTH}}: {years:>{FIELD_WIDTH}d}")
    print(f"{'Interest':<{LABEL_WIDTH}}: ${interest:>{FIELD_WIDTH},.2f}")
    print(f"{'Total':<{LABEL_WIDTH}}: ${total:>{FIELD_WIDTH},.2f}")


def main() -> None:
    """Read principal, rate, and years, then print the five-line report."""
    principal: float = float(ask("Principal in dollars: ", SAMPLE_PRINCIPAL))
    rate: float = float(ask("Annual interest rate in percent: ", SAMPLE_RATE))
    years: int = int(ask("Number of years: ", SAMPLE_YEARS))
    print_report(principal, rate, years)


if __name__ == "__main__":
    main()
```

**Why it works.**

**Read the sample output as a ruler, not as a picture.** Every line is the
same three pieces: a label padded out to ten columns, then a colon and a
space, then a twelve-column slot for the value. What changes is what fills
the slot:

| Line | What goes in the slot | Total line width |
|------|-----------------------|-----------------:|
| Principal | `$` sits outside the slot, then `1,000.00` right-aligned in 12 | 25 |
| Rate | `5.00` right-aligned in 11, then `%` takes the twelfth column | 24 |
| Years | `3` right-aligned in 12 | 24 |

That is why the rate line says `FIELD_WIDTH - 1`. The percent sign is part
of the value, so it claims a column and the number gets the other eleven.
Write the widths as constants and that reasoning stays in the code. Type
`12` and `11` literally and the next reader has to work it out again from
your output.

**`,.2f` is two instructions stacked.** The comma asks for a thousands
separator. The `.2f` asks for a fixed point with exactly two decimals. The
comma has to come before the dot — that is the order Python's format
grammar wants. Together they turn `1000.0` into `1,000.00`.

**`{years:>12d}` uses `d`, not `f`.** `d` means "write this as a whole
number", so `3` prints as `3` rather than `3.00`. Hand a float to a `d` spec
and Python raises a `ValueError`, which is genuinely useful: it catches the
moment you cast the years with `float()` by mistake.

**`>` means push right.** The number is written into a field of the given
width and padded with spaces on the *left*, so the last digit always lands
in the same column. `<` is the opposite and is what the labels use, so the
text starts at the same column and the colons line up. Right for numbers,
left for words — that is the whole rule.

**The formula is copied out literally.** `principal * (rate / 100) * years`.
The parentheses are not strictly needed, because `*` and `/` have the same
precedence and Python works left to right, so `principal * rate / 100 *
years` computes the same thing. The parentheses are there to say "this
factor is a percentage turned into a fraction", which is the part a reader
has to take on trust.

**`ask()` is the one piece the brief did not ask for.** It exists so the
downloadable file can be run automatically and still finish.
`sys.stdin.isatty()` answers the question "is there a real terminal with a
person attached to it". When there is, the program asks its three questions.
When there is not, calling `input()` would either raise `EOFError` or wait
forever for typing that is never coming, so `ask()` hands back the example
figure instead. The `except EOFError` is a second belt for the same
trousers: some terminals claim somebody is there and then close the input
immediately.

The examples are stored as *strings* — `"1000"`, not `1000` — because that
is what a person would have typed. The automatic run therefore does the same
`float()` and `int()` casts as the real one, and proves they work.

**The prompt goes to the error stream.** Every program has two ways out:
standard output for the answer, standard error for everything else.
`input("prompt")` puts the question on standard output, mixed in with the
report. Sending it to `sys.stderr` keeps them apart, and the payoff is
immediate: `python homework-01-simple-interest.py > report.txt` saves a file
with five clean lines in it while the questions still appear on your screen.
`flush=True` matters because a prompt with no newline on the end would
otherwise sit in a buffer and appear *after* you had already answered it.

## Download and run

Download [problem-01-simple-interest-calculator-solution.py](./problem-01-simple-interest-calculator-solution.py)
and run it:

```bash
python problem-01-simple-interest-calculator-solution.py
```

Run from a terminal, it asks you the three questions. Run by a script or
with its input redirected, it prints the example report instead of hanging.
Save your own copy as `homework-01-simple-interest.py` in your homework
folder, and commit that.

## Common bugs to catch

- **You forgot to cast, and Python did not tell you straight away.**
  `input()` returns a string, always. The bug is nastier than a plain crash,
  because some arithmetic on strings genuinely works:

  ```text
    File "badtypes.py", line 3, in c_to_f
      return c * 9 / 5 + 32
             ~~~~~~^~~
  TypeError: unsupported operand type(s) for /: 'str' and 'int'
  ```

  `"100" * 9` is legal — it repeats the string until it is nine hundred
  characters long — and the failure only surfaces at the `/`. If a traceback
  points at an operator two steps past where you expected trouble, suspect an
  uncast `input()`.
- **You typed `1,000` at the prompt.**
  `float("1,000")` raises
  `ValueError: could not convert string to float: '1,000'`. The comma is an
  output convention, not an input one. Type `1000`.
- **You used `round()` instead of a format spec.** `round(total, 2)` gives
  you a float back, and `print(round(1000.0, 2))` shows `1000.0` — one
  decimal, no separator, no alignment. `round()` changes the value; `.2f`
  changes the rendering. Reports want the rendering.
- **The rate line is one column too wide.** You used `FIELD_WIDTH` on the
  rate instead of `FIELD_WIDTH - 1` and forgot that `%` needs a column of
  its own.
- **`ValueError: Unknown format code 'd' for object of type 'float'`.** You
  cast the years with `float()` and then asked for `d`. Cast with `int()`.
- **The comma and the dot are the wrong way round.** `:.2f,` is a
  `ValueError`. The order in a format spec is fixed: fill, align, sign,
  width, separator, precision, type. Comma before dot, every time.

## Under the hood

<details>
<summary>Under the hood — the format mini-language, one field at a time</summary>

Everything after the `:` inside an f-string's braces is a tiny separate
language with its own grammar. In order, every piece optional:

```text
[[fill]align][sign][#][0][width][grouping][.precision][type]
```

Take `{principal:>12,.2f}` apart:

| Piece | Value | Meaning |
|-------|-------|---------|
| align | `>` | pad on the left, so the value ends at the right edge |
| width | `12` | make the whole field twelve characters wide |
| grouping | `,` | put a comma every three digits |
| precision | `.2` | exactly two digits after the decimal point |
| type | `f` | fixed point, not scientific, not general |

Because the pieces are positional, the order is not a matter of taste.
`{x:,.2f}` works and `{x:.2f,}` raises `ValueError: Invalid format specifier`.

The nested braces in `{principal:>{FIELD_WIDTH},.2f}` are a second feature.
Any part of the spec can itself be an expression in braces, evaluated first,
and its result pasted into the spec. That is what lets one named constant
drive five lines.

A fill character can come before the alignment:

```bash
python -c "print(f'{42:*>8}')"
```

```text
******42
```

That is `*` as fill, `>` as align, `8` as width. Receipts and cheques pad
with `*` for exactly this reason — so nobody can write extra digits in front
of the number.

The separator has a sibling: `_` groups with underscores instead of commas,
and for `b`, `o` and `x` it groups every four digits, which is how you make a
long binary number readable.

</details>

<details>
<summary>Under the hood — why 0.1 + 0.2 is not 0.3, and why this report is safe anyway</summary>

Python floats are binary fractions. A binary fraction can write halves,
quarters and eighths exactly, and cannot write one tenth exactly, for the
same reason base ten cannot write one third exactly. So `0.1` is stored as
the nearest available binary value, which is very slightly off:

```bash
python -c "print(f'{0.1:.20f}')"
```

```text
0.10000000000000000555
```

Stack a few of those and the error becomes visible:

```bash
python -c "print(0.1 + 0.2)"
```

```text
0.30000000000000004
```

This report is safe from that because the numbers involved — `1000`, `0.05`,
`150.0` — happen to land on values that round cleanly at two decimal places,
and because `.2f` rounds at the last moment, at the edge, when printing.
Problem 5 is where it becomes visible: `1000 * 1.05 ** 3` gives
`1157.6250000000002`, not `1157.625`, and that stray `2` at the end decides
which way the rounding goes.

The rule that follows: **never store money as a float in a real system.**
Use `decimal.Decimal`, which does arithmetic the way a bank ledger does, or
store whole cents as an `int`. For a five-line homework report a float is
fine, and knowing why it is fine is the point.

`.2f` also uses round-half-to-even rather than the round-half-up you were
taught at school, so `f"{2.675:.2f}"` is `'2.67'` — partly because `2.675` is
really `2.67499999...` in binary, and partly by design, because always
rounding halves upward biases a long column of numbers slightly high.

</details>

## Acceptance checklist

- [ ] Running the file asks for principal, rate and years, in that order.
- [ ] The output is exactly five lines.
- [ ] Dollar amounts show a thousands separator and two decimals.
- [ ] The rate shows two decimals and a trailing `%`.
- [ ] The years show as a whole number, with no decimal point.
- [ ] Your output matches the Expected output block character for
      character.
- [ ] The widths are named constants, not numbers typed into five
      f-strings.
- [ ] `main()` is annotated `-> None` and every variable carries a type
      hint.
- [ ] Committed with a message like `Add simple interest calculator`.

## Stretch

- Add a fourth question: how often the interest is paid out — yearly,
  monthly, weekly. Simple interest does not compound, so the total is
  unchanged; only the size of each payment changes. Print that too.
- Print a year-by-year table. One line per year showing the interest earned
  so far and the running total. You do not have loops until Week 4, so write
  it out three times by hand first and notice how much you want the loop.
- Make the report widen itself to fit. Work out the longest label with
  `max(len(label) for label in labels)` and use that as `LABEL_WIDTH`. The
  report then stays lined up no matter what you call the rows.
- Run `python -c "print(f'{1234567.891:,.2f}')"` and then try `_` in place of
  the comma. Two separators, one grammar.
- Read the format spec grammar at
  <https://docs.python.org/3/library/string.html#format-specification-mini-language>.
  It is one page and it is the reference you will come back to for years.

Next: [Homework Problem 2 — BMI Calculator](./problem-02-bmi-calculator.md).
