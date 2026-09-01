# Homework Problem 5 — Compound Interest

> **Topic:** the `**` operator, operator precedence, load-bearing parentheses, and floats that are not quite the number you expected
> **Lecture:** [02 — Operators and Strings](../lecture-notes/02-operators-and-strings.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** it looks like Problem 1 with a different formula, and it is not. Two pairs of parentheses are carrying the entire answer, and leaving them out gives you a wrong number that looks completely reasonable. It is also where you meet the fact that `1000 * 1.05 ** 3` is not exactly `1157.625`, and find out that this matters.

## The Brief

Problem 1 computed *simple* interest, where the money you earn is the same
every year. **Compound** interest is what actually happens in a bank
account: the interest you earned last year sits in the account and earns
interest of its own this year. It grows faster, and the longer you leave it
the wider the gap.

```text
final_amount = principal * (1 + rate / 100) ** years
```

Read that from the inside out.

- `rate / 100` turns "5 percent" into the fraction `0.05`.
- `1 + 0.05` is `1.05` — the multiplier for one year. Keep all of it, add a
  twentieth.
- `** years` applies that multiplier once per year. Three years is
  `1.05 * 1.05 * 1.05`.
- Multiply the principal by the result and you have the final amount.

Ask for the principal, the annual rate in percent, and the number of years,
then print a five-line report:

```text
Principal     : $   1,000.00
Rate          :        5.00%
Years         :            3
Final amount  : $   1,157.63
Total interest: $     157.63
```

Compare that with Problem 1's `$150.00` of simple interest over the same
three years. Seven dollars and change. Now run both at thirty years and look
again — that is the whole argument for starting early.

**Do not copy Problem 1's column widths.** The labels are longer here
(`Total interest` is fourteen characters) so every number has moved. Measure
this block, not the last one.

## Starter

Save this as `homework-05-compound-interest.py` and fill in the `TODO`s. It
runs as pasted and prints the first line:

```python
"""TODO: one line saying what this file does."""

LABEL_WIDTH: int = 14
FIELD_WIDTH: int = 11


def main() -> None:
    """Read principal, rate, and years, then print the five-line report."""
    principal: float = float(input("Principal in dollars: "))
    rate: float = float(input("Annual interest rate in percent: "))
    years: int = int(input("Number of years: "))

    final_amount: float = 0.0  # TODO: principal * (1 + rate / 100) ** years
    total_interest: float = 0.0  # TODO: final_amount - principal

    print(f"{'Principal':<{LABEL_WIDTH}}: ${principal:>{FIELD_WIDTH},.2f}")
    # TODO: four more lines - rate, years, final amount, total interest


if __name__ == "__main__":
    main()
```

`LABEL_WIDTH` is 14 because `Total interest` is fourteen characters.
`FIELD_WIDTH` is 11 because the value slot here is twelve columns *including*
the dollar sign, so the number itself gets eleven.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/homework/problem-05-compound-interest.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks for the principal, the annual rate in percent, and the
   number of years, in that order.
2. It prints exactly five lines, in the order shown in The Brief.
3. `Final amount` uses the compound formula, not the simple one.
4. `Total interest` is the final amount minus the principal.
5. Dollar amounts carry a thousands separator and two decimal places; the
   rate carries two decimals and a `%`; the years print as a whole number.
6. Your output matches the sample block character for character.
7. `main()` is annotated `-> None`, and every variable carries a type hint.

## Constraints

- **Parenthesise `(1 + rate / 100)`.** Those brackets are the whole problem.
  Without them the formula means something else entirely and does not
  complain. Common bugs to catch shows what it prints.
- **Derive `total_interest` by subtraction.** `final_amount - principal`,
  not a second formula. Two formulas can disagree; a subtraction cannot.
- **Round once, at the very end, in the format spec.** Do not
  `round(final_amount, 2)` and then also print with `.2f`. Doing both
  changes the answer, and the reason is in Under the hood.
- **Measure this report's widths from this report's sample.** Copying
  Problem 1's `LABEL_WIDTH = 10` makes every line four columns narrow.
  Copying its `FIELD_WIDTH = 12` pushes every dollar amount one column too
  far right.
- **Cast the years with `int()`.** `** ` works fine with a float exponent,
  but the `d` format spec does not, and you want that error.

## Expected output

The downloadable file below uses its built-in example figures when nobody is
at the keyboard, so the run is the same every time:

```text
$ python problem-05-compound-interest.py
Principal     : $   1,000.00
Rate          :        5.00%
Years         :            3
Final amount  : $   1,157.63
Total interest: $     157.63
```

Run the same program in your own terminal and it has the conversation
instead:

```text
Principal in dollars: 1000
Annual interest rate in percent: 5
Number of years: 3
Principal     : $   1,000.00
Rate          :        5.00%
Years         :            3
Final amount  : $   1,157.63
Total interest: $     157.63
```

And the comparison the brief asks for, at a thirty-year horizon:

```text
Principal in dollars: 1000
Annual interest rate in percent: 5
Number of years: 30
Principal     : $   1,000.00
Rate          :        5.00%
Years         :           30
Final amount  : $   4,321.94
Total interest: $   3,321.94
```

Simple interest over the same thirty years earns `$1,500.00`. Compound earns
`$3,321.94`. Same money, same rate, same time.

## Steps

1. Activate your Week 2 environment and `cd` into your `homework/` folder.
2. Save the Starter as `homework-05-compound-interest.py`.
3. Before you write the formula, check the multiplier by hand at the
   terminal:

   ```bash
   python -c "print((1 + 5 / 100) ** 3, 1000 * (1 + 5 / 100) ** 3)"
   ```

   ```text
   1.1576250000000001 1157.6250000000002
   ```

   Note the stray digits on the end. They are not a mistake, and Under the
   hood explains where they come from.
4. Fill in `final_amount` and `total_interest`. Run it. One line, right
   number.
5. Add the `Final amount` and `Total interest` lines. The last one is long
   enough that it reads better split across two f-strings — Python joins
   adjacent string literals for you.
6. Add the `Years` line with `d`, then the `Rate` line last.
7. Diff your output against the sample, character for character.
8. Run it again with 30 years and check against the third block above.
9. Commit: `git add homework-05-compound-interest.py` then
   `git commit -m "Add compound interest calculator"`.

## The Solution

```python
"""Compound-interest calculator.

Week 2 homework, problem 5, Code Crunch Convos.
final_amount = principal * (1 + rate / 100) ** years

Questions go to the error stream and the report goes to the normal output
stream. When nobody is at the keyboard the script uses the example figures.
Save your own copy as ``homework-05-compound-interest.py``.
"""

import sys

LABEL_WIDTH: int = 14
FIELD_WIDTH: int = 11

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
    """Print the five-line compound-interest report."""
    final_amount: float = principal * (1 + rate / 100) ** years
    total_interest: float = final_amount - principal

    print(f"{'Principal':<{LABEL_WIDTH}}: ${principal:>{FIELD_WIDTH},.2f}")
    print(f"{'Rate':<{LABEL_WIDTH}}: {rate:>{FIELD_WIDTH},.2f}%")
    print(f"{'Years':<{LABEL_WIDTH}}: {years:>{FIELD_WIDTH + 1}d}")
    print(f"{'Final amount':<{LABEL_WIDTH}}: ${final_amount:>{FIELD_WIDTH},.2f}")
    print(
        f"{'Total interest':<{LABEL_WIDTH}}: "
        f"${total_interest:>{FIELD_WIDTH},.2f}"
    )


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

**The label width changed, so every number moved.** `Total interest` is
fourteen characters, so the labels pad to fourteen instead of Problem 1's
ten. Put the two expected blocks side by side and you will see the numeric
columns differ as well: here the value slot is twelve columns *including*
the `$`, so the amount itself gets eleven. That is the only reason
`FIELD_WIDTH` is `11` in this file and `12` in Problem 1. Deriving the widths
from the sample instead of copying the previous file is the actual skill
being practised.

**Precedence does the work inside the formula.**
`principal * (1 + rate / 100) ** years` evaluates in this order:

1. `rate / 100` — division beats addition.
2. `1 + that` — but only because the brackets force it.
3. `** years` — the power operator beats multiplication.
4. `principal * that`.

The brackets around `1 + rate / 100` are load-bearing. Take them out and
`1 + rate / 100 ** years` raises `100` to the power of `years` and then
divides, giving an answer about eight orders of magnitude wrong. This is
operator precedence in a formula you can check against a real bank
statement.

**`**` beats a minus sign in front of it, which matters nearby.** Not in
this formula, but in the mistake next door: `-2 ** 2` is `-4`, not `4`,
because the power is applied before the sign. Any time an exponent has a
sign in front of it, put brackets round it.

**Where `1,157.63` comes from, exactly.** The arithmetic result is not the
tidy `1157.625` you get by hand:

```bash
python -c "print(1000 * (1 + 5.0 / 100) ** 3)"
```

```text
1157.6250000000002
```

`0.05` cannot be written exactly in binary, so `1.05 ** 3` lands a hair
above the mathematical value, and `.2f` rounds `1157.6250000000002` up to
`1157.63`. Had the value been exactly `1157.625`, Python's round-half-to-even
rule would have given you `1157.62` instead:

```bash
python -c "print(f'{1157.625:.2f}')"
```

```text
1157.62
```

The sample output says `1,157.63`, which is what the honest formula
produces. It is a very good illustration of why you compute from the inputs
rather than typing a rounded intermediate value into your code.

**`total_interest = final_amount - principal`, not a second formula.**
Deriving it by subtraction guarantees the two figures agree. `157.63` is
also what the subtraction gives, since `1157.6250000000002 - 1000` is
`157.62500000000023`, still above the midpoint.

**The last line is split across two f-strings.** Two string literals sitting
next to each other are joined by Python at compile time, with no `+` and no
cost. It is how you keep a long line under the 79-character limit without
breaking the string in an ugly place.

**`ask()` is the one piece the brief did not ask for.** It lets the
downloadable file run with nobody present, handing back the example figures
when `sys.stdin.isatty()` says there is no terminal with a person at it,
rather than hanging on an `input()` that will never be answered.

## Download and run

Download [problem-05-compound-interest-solution.py](./problem-05-compound-interest-solution.py)
and run it:

```bash
python problem-05-compound-interest-solution.py
```

Run from a terminal, it asks you the three questions. Run by a script or
with its input redirected, it prints the example report instead of hanging.
Save your own copy as `homework-05-compound-interest.py` in your homework
folder, and commit that.

## Common bugs to catch

- **You dropped the brackets.** `principal * 1 + rate / 100 ** years`
  evaluates to `1000.000005` for the sample input and prints
  `$   1,000.00` — the principal, apparently untouched, because
  `5 / 100 ** 3` is `0.000005` and it is being *added* rather than
  compounded. No error. Just a wrong number that looks plausible, which is
  the worst kind.
- **You reused Problem 1's widths.** Copy `LABEL_WIDTH = 10` and the report
  is four columns narrow everywhere. Copy `FIELD_WIDTH = 12` and every
  dollar amount sits one column too far right. The two problems genuinely
  have different layouts.
- **You rounded the intermediate value.**

  ```python
  final_amount = round(principal * (1 + rate / 100) ** years, 2)
  ```

  followed by `.2f` gives `1157.62` here, because `round()` collapses the
  value to the exactly-representable `1157.625` and then the half-to-even
  rule takes it *down*. Round once, at the edge, when you print.
- **You wrote `1 + rate / 100` as `1 + rate // 100`.** `//` is floor
  division. `5 // 100` is `0`, so the multiplier is `1`, and the money never
  grows at all. The report prints the principal five times.
- **You expected compound and simple to differ in year one.** They do not —
  `$1,050.00` both ways. The gap opens at year two and widens from there.
- **`ValueError: Unknown format code 'd' for object of type 'float'`.** You
  cast the years with `float()`. Use `int()`.
- **`OverflowError: (34, 'Result too large')`** from typing something like
  `100000` years. Python integers grow without limit but floats do not, and
  `1.05 ** 100000` is past the largest float there is.

## Under the hood

<details>
<summary>Under the hood — why 1.05 ** 3 is not exactly 1.157625</summary>

A Python float is a binary fraction with 53 bits of precision. Binary can
write halves, quarters and eighths exactly. It cannot write one twentieth
exactly, for the same reason base ten cannot write one third exactly. So
`0.05` is stored as the closest available binary value:

```bash
python -c "print(f'{0.05:.20f}')"
```

```text
0.05000000000000000278
```

That tiny excess is real, and cubing the number magnifies it:

```bash
python -c "print(f'{1.05 ** 3:.20f}')"
```

```text
1.15762500000000012612
```

Multiply by 1000 and the excess climbs into the thirteenth decimal place,
which is exactly where `1157.6250000000002` comes from.

Then `.2f` has to decide. The value is *above* the halfway point between
`1157.62` and `1157.63`, so it rounds up and gives `1157.63`. If the value
had been exactly halfway, Python would apply **round half to even** and pick
`1157.62`, because `2` is the even digit. That rule is not Python being
strange; it is IEEE 754, and it exists because always rounding halves upward
biases a long column of numbers slightly high.

Two consequences worth carrying:

- **Never store money as a float in a real system.** Use `decimal.Decimal`,
  which does arithmetic the way a ledger does, or store whole cents as an
  `int`. For a five-line homework report a float is fine, and knowing why it
  is fine is the point.
- **Never compare floats with `==`.** `0.1 + 0.2 == 0.3` is `False`. Compare
  with a tolerance, or use `math.isclose(a, b)`, which picks a sensible
  tolerance for you.

```bash
python -c "import math; print(0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3))"
```

```text
False True
```

</details>

<details>
<summary>Under the hood — the three things ** does, and the one that surprises people</summary>

`**` is the power operator, and it behaves in three different ways depending
on what you feed it.

**Integer base, non-negative integer exponent** gives an exact integer, of
any size:

```bash
python -c "print(2 ** 100)"
```

```text
1267650600228229401496703205376
```

No overflow, no wrapping. Python integers grow to fit.

**Anything involving a float** gives a float, computed with the same 53 bits
of precision as everything else, which is where this problem's stray digits
come from.

**A negative integer exponent** gives a float even when both operands are
integers, because the answer is a fraction:

```bash
python -c "print(2 ** -1, type(2 ** -1))"
```

```text
0.5 <class 'float'>
```

The surprise is precedence. `**` binds tighter than unary minus, so:

```bash
python -c "print(-2 ** 2, (-2) ** 2)"
```

```text
-4 4
```

And it is **right-associative**, unlike every other operator you have met.
`2 ** 3 ** 2` is `2 ** (3 ** 2)`, which is `2 ** 9`, which is `512` — not
`(2 ** 3) ** 2`, which would be `64`.

```bash
python -c "print(2 ** 3 ** 2)"
```

```text
512
```

That is the mathematical convention, and it is the one place in Python where
a chain of the same operator does not evaluate left to right.

`pow()` is the same operator as a function, with a bonus third argument:
`pow(a, b, m)` computes `a ** b % m` without ever building the enormous
intermediate value. That single feature is what makes public-key
cryptography possible.

</details>

## Acceptance checklist

- [ ] Running the file asks for principal, rate and years, in that order.
- [ ] The output is exactly five lines.
- [ ] `Final amount` for 1000 / 5 / 3 is `$   1,157.63`.
- [ ] `Total interest` is the final amount minus the principal, not a second
      formula.
- [ ] Your output matches the Expected output block character for
      character.
- [ ] `(1 + rate / 100)` is bracketed.
- [ ] Nothing is rounded before the format spec does it.
- [ ] The widths are this report's widths, not Problem 1's.
- [ ] `main()` is annotated `-> None` and every variable carries a type
      hint.
- [ ] Committed with a message like `Add compound interest calculator`.

## Stretch

- Add a fourth question: how many times a year the interest compounds.
  The formula becomes
  `principal * (1 + rate / (100 * n)) ** (n * years)`. Try `n` of 1, 12 and
  365 on the same money and watch the gains shrink as `n` grows — the
  returns are real but they flatten fast.
- Push `n` higher and higher and see what the answer approaches. It converges
  on `principal * math.e ** (rate / 100 * years)`, which is continuous
  compounding, and watching a limit appear in your own output beats reading
  about one.
- Print both the simple and the compound figure side by side and show the
  difference. That is Problem 1 and Problem 5 in one report, and it is the
  comparison the brief keeps pointing at.
- Work out how many years it takes to double the money at 5%. The banker's
  shortcut is "72 divided by the rate", so about 14.4 years. Check it
  against your own program and see how good the shortcut is.
- Rewrite the money handling with `decimal.Decimal` and compare the output.
  `Decimal("1000") * Decimal("1.05") ** 3` gives exactly `1157.625000`, with
  no stray digits on the end, and then the half-to-even rule takes it *down*
  to `1157.62`. The float version and the exact version genuinely disagree by
  a cent, and working out which one a bank would use is a real lesson.

Next: [Homework Problem 6 — Distance and Speed Report](./problem-06-distance-and-speed-report.md).
