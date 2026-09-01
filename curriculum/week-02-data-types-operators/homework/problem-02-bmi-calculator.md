# Homework Problem 2 — BMI Calculator

> **Topic:** comparison operators, chained comparisons, booleans as ordinary values, and `**`
> **Lecture:** [02 — Operators and Strings](../lecture-notes/02-operators-and-strings.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** it takes away the tool you would reach for and hands you a better idea. You do not have `if` yet, so you cannot branch. What you discover instead is that a comparison like `bmi < 18.5` is not a question waiting for an `if` — it is already a value, `True` or `False`, that you can name, store and print. Once you see that, Problem 4 becomes possible.

## The Brief

Body Mass Index is a single number that compares somebody's weight to their
height:

```text
BMI = weight_kg / (height_m ** 2)
```

`**` is Python's power operator. `height_m ** 2` is the height multiplied by
itself. So a person 1.74 m tall weighing 70 kg has a BMI of
`70 / (1.74 * 1.74)`, which is about 23.1.

Health guidelines sort that number into four bands:

| Band | Range |
|------|-------|
| Underweight | below 18.5 |
| Normal | 18.5 up to but not including 25 |
| Overweight | 25 up to but not including 30 |
| Obese | 30 and above |

Ask for a weight in kilograms and a height in metres. Print the BMI to one
decimal place, then print all four band names with `True` or `False` beside
each one:

```text
BMI: 23.1
Underweight : False
Normal      : True
Overweight  : False
Obese       : False
```

**You may not use `if`.** That is not an arbitrary hoop. `if` is Week 3, and
doing without it here is what forces you to notice that comparisons produce
values. Printing all four flags is not a workaround — it is the answer this
week wants.

One caution about the numbers themselves: BMI is a rough population
statistic, not a diagnosis. It knows nothing about muscle, bone or build.
Treat it here as a formula to practise on.

## Starter

Save this as `homework-02-bmi.py` and fill in the `TODO`s. It runs as pasted
and prints the BMI line:

```python
"""TODO: one line saying what this file does."""

LABEL_WIDTH: int = 12
UNDERWEIGHT_MAX: float = 18.5
NORMAL_MAX: float = 25.0
OVERWEIGHT_MAX: float = 30.0


def main() -> None:
    """Read weight and height, print the BMI and four category flags."""
    weight_kg: float = float(input("Weight in kilograms: "))
    height_m: float = float(input("Height in meters: "))

    bmi: float = weight_kg / (height_m ** 2)

    underweight: bool = bmi < UNDERWEIGHT_MAX
    # TODO: normal, overweight, obese - one bool each

    print(f"BMI: {bmi:.1f}")
    print(f"{'Underweight':<{LABEL_WIDTH}}: {underweight}")
    # TODO: three more flag lines


if __name__ == "__main__":
    main()
```

The three boundary numbers are constants at the top because each one is used
by *two* bands — 18.5 ends `Underweight` and starts `Normal`. Naming it once
is what keeps the two bands glued together when you change it.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/homework/problem-02-bmi-calculator.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks for weight in kilograms, then height in metres.
2. It prints the BMI rounded to one decimal place, on its own line, in the
   form `BMI: 23.1`.
3. It then prints four lines, one per band, each showing `True` or `False`.
4. The four labels are padded so the colons line up.
5. Exactly one of the four flags is `True` for any sensible BMI.
6. There is no `if`, `elif` or `else` anywhere in the part that works out
   the bands.
7. `main()` is annotated `-> None`, and every variable carries a type hint.

## Constraints

- **No `if` in the answer.** Use comparison operators and store their
  results. If your program branches, you have skipped the lesson this
  problem exists to teach. (The downloadable file below has exactly one
  `if`, inside the helper that decides whether anybody is at the keyboard.
  It is plumbing so the file can run unattended, and it is not part of the
  answer. Your own copy does not need it.)
- **Parenthesise the denominator.** Write `weight_kg / (height_m ** 2)`,
  even though `**` already binds tighter than `/` so the parentheses change
  nothing. They mean a reader never has to check, and they mean a one-key
  typo cannot silently turn the formula into something else.
- **Use chained comparisons for the middle two bands.**
  `UNDERWEIGHT_MAX <= bmi < NORMAL_MAX`, not two comparisons joined with
  `and`. Both are correct; the chain is the one Python was designed for.
- **`<=` on the low end, `<` on the high end, every time.** Mix them and a
  BMI that lands exactly on a boundary either lights up two flags or none.
- **Name the boundaries.** `18.5` typed twice is two places to change and
  one place to forget.

## Expected output

The downloadable file below uses its built-in example figures when nobody is
at the keyboard, so the run is the same every time:

```text
$ python problem-02-bmi-calculator.py
BMI: 23.1
Underweight : False
Normal      : True
Overweight  : False
Obese       : False
```

Run the same program in your own terminal and it has the conversation
instead:

```text
Weight in kilograms: 70
Height in meters: 1.74
BMI: 23.1
Underweight : False
Normal      : True
Overweight  : False
Obese       : False
```

Now the run that separates a correct answer from a lucky one — a weight of
`50` and a height of `1.645` give a BMI of `18.477...`, which *displays* as
`18.5` and is still flagged `Underweight`, because the comparison sees the
full value and not the label:

```text
Weight in kilograms: 50
Height in meters: 1.645
BMI: 18.5
Underweight : True
Normal      : False
Overweight  : False
Obese       : False
```

## Steps

1. Activate your Week 2 environment and `cd` into your `homework/` folder.
2. Save the Starter as `homework-02-bmi.py`.
3. Run it as pasted with weight `70` and height `1.74`. You should see
   `BMI: 23.1` and one flag line.
4. Before you write the other three flags, prove to yourself that a
   comparison is a value:

   ```bash
   python -c "bmi = 23.1; print(bmi < 18.5, type(bmi < 18.5))"
   ```

   ```text
   False <class 'bool'>
   ```

5. Add `normal`, `overweight` and `obese`. The two middle ones are chains;
   the last one is a single `>=`.
6. Add the three remaining `print()` lines.
7. Test every boundary: `18.5`, `25`, `30`. At each one, exactly one flag
   must be `True`, and it must be the *upper* band, because the low end is
   inclusive.
8. Commit: `git add homework-02-bmi.py` then
   `git commit -m "Add BMI calculator with boolean flags"`.

## The Solution

```python
"""BMI calculator with no ``if`` statement in the answer.

Week 2 homework, problem 2, Code Crunch Convos.
BMI = weight_kg / (height_m ** 2)

The four categories are printed as plain True/False flags, because ``if`` is
a Week 3 topic. Questions go to the error stream so the flags on the normal
output stream stay clean enough to redirect into a file. When nobody is at
the keyboard the script uses the example figures. Save your own copy as
``homework-02-bmi.py``.
"""

import sys

LABEL_WIDTH: int = 12
UNDERWEIGHT_MAX: float = 18.5
NORMAL_MAX: float = 25.0
OVERWEIGHT_MAX: float = 30.0

SAMPLE_WEIGHT_KG: str = "70"
SAMPLE_HEIGHT_M: str = "1.74"


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


def print_report(weight_kg: float, height_m: float) -> None:
    """Print the BMI and one True/False flag per category."""
    bmi: float = weight_kg / (height_m ** 2)

    underweight: bool = bmi < UNDERWEIGHT_MAX
    normal: bool = UNDERWEIGHT_MAX <= bmi < NORMAL_MAX
    overweight: bool = NORMAL_MAX <= bmi < OVERWEIGHT_MAX
    obese: bool = bmi >= OVERWEIGHT_MAX

    print(f"BMI: {bmi:.1f}")
    print(f"{'Underweight':<{LABEL_WIDTH}}: {underweight}")
    print(f"{'Normal':<{LABEL_WIDTH}}: {normal}")
    print(f"{'Overweight':<{LABEL_WIDTH}}: {overweight}")
    print(f"{'Obese':<{LABEL_WIDTH}}: {obese}")


def main() -> None:
    """Read weight and height, print the BMI and four category flags."""
    weight_kg: float = float(ask("Weight in kilograms: ", SAMPLE_WEIGHT_KG))
    height_m: float = float(ask("Height in meters: ", SAMPLE_HEIGHT_M))
    print_report(weight_kg, height_m)


if __name__ == "__main__":
    main()
```

**Why it works.**

**A comparison *is* a value.** This is the whole point of the problem.
`bmi < 18.5` does not need an `if` around it to be useful. On its own it
produces `True` or `False`, and `True` and `False` are ordinary values you
can put in a variable, pass to a function, or print. Once you see booleans
that way, `if` stops looking like the only way to make a decision.

**Chained comparisons are the trick that makes the middle bands easy.**
`UNDERWEIGHT_MAX <= bmi < NORMAL_MAX` is Python reading like mathematics. It
means "18.5 is less than or equal to bmi, *and* bmi is less than 25", and it
evaluates `bmi` only once. Most languages make you write the `and` yourself.

**The four flags cannot overlap, by construction.** Each band starts exactly
where the one before it ends, with `<=` on the low end and `<` on the high
end. For any finite BMI, exactly one flag is `True`. Write `bmi > 18.5` for
`normal` instead and a BMI of exactly `18.5` lights up nothing at all — the
classic boundary bug, and the reason the boundary is a named constant used
by two bands rather than a number typed twice.

**`{bmi:.1f}` rounds the label, not the value.** The stored `bmi` keeps its
full precision for the comparisons, so a BMI of `24.97` displays as `25.0`
and is still classified `Normal`. That is correct — the bands are defined on
the number, not on its label — but it looks wrong at a glance, which is
exactly why the second sample session on this page exists.

**`print(f"... {underweight}")` shows `True` and `False`** with capital
letters, because an f-string calls `str()` on the value and `str(True)` is
the string `"True"`.

**`ask()` is the one piece the brief did not ask for.** It lets the
downloadable file run without a person present. `sys.stdin.isatty()` asks
"is there a real terminal with somebody at it". When there is, the program
asks its questions; when there is not, `ask()` hands back the example value
instead of hanging on an `input()` that will never be answered. The
`except EOFError` covers the case where a terminal claims somebody is there
and then closes the input. That single `if` is plumbing, not part of the
BMI answer — `print_report` has no branch in it at all.

## Download and run

Download [problem-02-bmi-calculator-solution.py](./problem-02-bmi-calculator-solution.py) and
run it:

```bash
python problem-02-bmi-calculator-solution.py
```

Run from a terminal, it asks you the two questions. Run by a script or with
its input redirected, it prints the example report instead of hanging. Save
your own copy as `homework-02-bmi.py` in your homework folder, and commit
that.

## Common bugs to catch

- **You used `if` anyway.** The output looks right and the exercise is
  wasted. Delete the branch and store the comparison instead.
- **You wrote `weight_kg / height_m * 2`.** One character away from the
  right answer and completely wrong: that is `(weight_kg / height_m) * 2`.
  With the parentheses in place — `weight_kg / (height_m ** 2)` — the typo
  is much harder to make and much easier to see.
- **You borrowed `&&` from another language.**

  ```text
    File "<string>", line 1
      print(True && False)
                  ^
  SyntaxError: invalid syntax
  ```

  Python spells them `and`, `or`, `not`.
- **You wrote a chain that is not one.** `18.5 <= bmi and < 25` is
  `SyntaxError: invalid syntax`. Each side of an `and` has to be a complete
  comparison. Either write the chain — `18.5 <= bmi < 25` — or write both
  halves out: `bmi >= 18.5 and bmi < 25`.
- **You typed the height in centimetres.** `170` metres gives a BMI of `0.0`
  and four `False` flags. Nothing crashes, nothing warns. A program that
  accepts any number will happily compute nonsense, and there is no
  validation here to catch it.
- **Two flags are `True` at once.** You used `<=` on both ends of a band.
  Low end inclusive, high end exclusive, all four times.
- **`ZeroDivisionError: float division by zero`.** Somebody typed `0` for
  the height. Week 3's `if` is where you learn to refuse that politely.

## Under the hood

<details>
<summary>Under the hood — how a chained comparison is really evaluated</summary>

`a <= b < c` is not `(a <= b) < c`. If it were, Python would compare a
boolean against `c` and give you nonsense. What actually happens is that the
chain expands to `(a <= b) and (b < c)`, with one important extra promise:
**`b` is evaluated only once.**

That promise matters the moment the middle term has a side effect or costs
something:

```bash
python -c "
def bmi():
    print('computing')
    return 23.1
print(18.5 <= bmi() < 25)
"
```

```text
computing
True
```

`computing` appears once, not twice. Written by hand as
`18.5 <= bmi() and bmi() < 25`, the function would run twice.

The chain also short-circuits. If the first comparison is `False`, the
second is never evaluated at all — the answer cannot change, so Python does
not bother.

Chains are not limited to two links. `0 <= score <= 100` is the idiomatic
range check, and `a < b < c < d` is legal. What chains are bad at is mixing
directions: `a < b > c` is legal and almost always a mistake, because it
reads like a shape and means something quite different.

</details>

<details>
<summary>Under the hood — bool is a kind of int, and what that buys you</summary>

`bool` is a subclass of `int`. This is not a quirk, it is the language
definition:

```bash
python -c "print(isinstance(True, int), True == 1, True + True)"
```

```text
True True 2
```

`True` *is* `1` and `False` *is* `0` wherever a number is wanted. The only
difference is how they print.

That is what makes counting flags possible without a branch:

```bash
python -c "bmi = 23.1; print((bmi >= 18.5) + (bmi >= 25) + (bmi >= 30))"
```

```text
1
```

One threshold cleared. Problem 4 turns exactly that count into a letter
grade.

Two related facts worth carrying:

- **`sum()` counts `True`s.** `sum([True, False, True])` is `2`, which is
  how you count how many things in a list satisfy a condition, once you have
  loops.
- **`==` and `is` are different questions.** `True == 1` is `True` because
  they compare equal as numbers. `True is 1` is `False` because they are
  different objects. Use `==` for values and `is` only for `None`, `True`
  and `False` themselves.

Python's `int` is also unbounded — it grows to fit, with no overflow — which
is why `2 ** 1000` just works and why you never worry about a counter
wrapping round to a negative number.

</details>

## Acceptance checklist

- [ ] Running the file asks for weight, then height.
- [ ] The BMI prints on its own line with exactly one decimal place.
- [ ] Four flag lines follow, with the colons lined up.
- [ ] Exactly one flag is `True` for any sensible BMI.
- [ ] There is no `if`, `elif` or `else` in the part that works out the
      bands.
- [ ] The middle two bands use chained comparisons, not `and`.
- [ ] The three boundaries are named constants, each used by two bands.
- [ ] `18.5`, `25` and `30` each land in the upper band.
- [ ] Committed with a message like `Add BMI calculator with boolean flags`.

## Stretch

- Print the flags as `yes`/`no` instead of `True`/`False`, still without an
  `if`. `"no yes".split()[underweight]` works because a boolean is an index.
  It is the same trick Problem 4 is built on.
- Print the category name on a single line, still without an `if`. Add the
  three `>=` comparisons to get a number from 0 to 3, then use it to index a
  tuple of the four band names.
- Add pounds and inches. The imperial formula is
  `703 * weight_lb / (height_in ** 2)`, and `703` is exactly the constant
  that converts one formula into the other. Work out where it comes from.
- Come back after Week 3 and rewrite the whole thing with `if`/`elif`.
  Compare the two versions side by side. Notice what got shorter, and notice
  what you can no longer see at a glance.
- Find out what happens at a BMI of exactly `18.5`, `25.0` and `30.0` by
  running the program three times, and write the answers into your commit
  message. Boundaries are where bugs live.

Next: [Homework Problem 3 — Word and Character Counter](./problem-03-word-and-character-counter.md).
