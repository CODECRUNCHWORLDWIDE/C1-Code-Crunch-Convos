# Mini-Project — Unit Converter CLI

> **Topic:** the whole of Week 2 in one program — menus, casting, arithmetic, validation, and formatted output
> **Lecture:** [03 — Reading Input and Type Hints](../lecture-notes/03-input-and-type-hints.md)
> **Difficulty:** the pieces are all familiar; holding six of them in one program is the work
> **Target time:** 2–3 hours, spread over more than one sitting
> **Why this one:** it is your first program with more than one moving part. Up to now every file did one thing from top to bottom. This one has to *decide* what to do, and that changes how you have to think about it.

<!-- no-runnable-file: this page is the project brief, and the project's deliverable is a folder in your own repository with a script, a commit history, and a screenshot of a session. The runnable answer is unit_converter.py, which ships beside this page and is linked from Download and run. A file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

This is the capstone of Week 2. Everything the week taught — variables
and types, casting text to numbers, arithmetic and precedence,
comparisons, `input()`, catching a bad value, f-strings with format
specs, and type hints — comes together in one small program called the
**Code Crunch Unit Converter**.

It converts between three pairs of units:

1. **Celsius and Fahrenheit** — temperature
2. **Kilometers and miles** — distance
3. **US dollars and euros** — currency, at a rate written into the file

It runs once, does one conversion, and exits. Here is the session it
should produce:

```text
================================
   Code Crunch Unit Converter
================================

Categories:
  1) Temperature (C / F)
  2) Distance    (km / mi)
  3) Currency    (USD / EUR)

Pick a category (1-3): 1

Direction:
  a) Celsius     -> Fahrenheit
  b) Fahrenheit  -> Celsius

Choose direction (a/b): a

Value in Celsius: 100

Result: 100.00 C = 212.00 F

Thanks for using the converter!
```

And the same program, going the currency way:

```text
================================
   Code Crunch Unit Converter
================================

Categories:
  1) Temperature (C / F)
  2) Distance    (km / mi)
  3) Currency    (USD / EUR)

Pick a category (1-3): 3

Direction:
  a) USD -> EUR
  b) EUR -> USD

Choose direction (a/b): a

Value in USD: 250

Result: $250.00 USD = €228.50 EUR  (rate: 1 USD = 0.9140 EUR)

Thanks for using the converter!
```

Three categories times two directions is six different endings, and the
program has to pick the right one from two short answers. That is the
new thing here. The arithmetic is six one-line functions you could write
in ten minutes; deciding *which* of them to call, and keeping that
decision readable, is the actual project.

> *As a* learner who has just met `input()` and `float()`,
> *I want* one program that reads a menu answer and does the matching
> conversion,
> *so that* I find out what happens to a program's shape when it has to
> make a choice.

## Starter

The scaffold, with ten `TODO`s to fill in, is on its own page:
**[starter.md](./starter.md)**. Copy the code block from there into a
file called `unit_converter.py` inside your `mini-project/` folder. It
runs before you touch it, so you always have a working program to grow
rather than a broken one to repair.

The plumbing — the banner, both menus, the prompts, and the branching —
is given to you on purpose. What Week 2 taught you is the part that is
missing: the six formulas, one `try` / `except` around a cast, and six
result lines with format specs on them.

**Where the answer on this page differs from the scaffold.** The
scaffold and the answer below are both correct completions of the same
brief, and they make two different decisions:

| | `starter.md` scaffold | The Solution below |
|---|---|---|
| Direction menu | `read_direction(option_a, option_b)` takes the two labels as arguments | each runner prints its own two lines, and `read_direction()` takes nothing |
| Blank lines | separate `print()` calls between the blocks | a leading `\n` on the front of each prompt |
| The farewell | printed at the end of `main()`, always | printed only when a conversion actually happened |

The visible session is identical for all six working paths. They differ
only when something goes wrong: the scaffold thanks you anyway, the
answer below does not. Either reading is defensible — the brief never
says. Pick one, say which in your README, and be consistent.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](../../../README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

The program:

1. Prints the banner and the three-item category menu, then asks
   `Pick a category (1-3): `.
2. Prints the two directions for that category, then asks
   `Choose direction (a/b): `.
3. Accepts `a` or `b` in any capitalisation, with stray spaces around
   them.
4. Asks for the value with a prompt naming the unit, such as
   `Value in Celsius: `.
5. Converts, and prints one result line carrying both unit labels, with
   **two decimal places** on both numbers.
6. Money carries a thousands separator and the currency symbol, and the
   currency line ends with the rate it used, at four decimal places.
7. Runs once and exits. Looping is a stretch goal.
8. Prints a clear message and exits without a traceback when the
   category, the direction, or the value is not something it understands.

The code:

9. Two module-level constants, and nothing else holds these numbers:

   ```python
   USD_TO_EUR: float = 0.9140
   KM_PER_MILE: float = 1.609344
   ```

10. Six conversion functions, each taking one number and returning one
    number:

    ```python
    def c_to_f(c: float) -> float: ...
    def f_to_c(f: float) -> float: ...
    def km_to_mi(km: float) -> float: ...
    def mi_to_km(mi: float) -> float: ...
    def usd_to_eur(usd: float) -> float: ...
    def eur_to_usd(eur: float) -> float: ...
    ```

11. Type hints on every parameter and every return.
12. A module docstring, and a docstring on every function.
13. The flow inside `main()`, behind an `if __name__ == "__main__":`
    guard.

The project:

14. Saved as `mini-project/unit_converter.py` in your Week 2 repository.
15. Committed with a message that says what it is, and pushed.
16. Linked from your repository README, with a screenshot or a short
    recording of one session. A picture of the thing running is worth
    more to a reader than the source is.

## Constraints

- **The six conversion functions do arithmetic and nothing else.** No
  `input()`, no `print()`, no reaching out to anything. A function that
  takes a number and returns a number can be checked in one line, and
  the "unit tested" stretch goal is only possible because of it.
- **One constant per relationship, used in both directions.** `km_to_mi`
  divides by `KM_PER_MILE` and `mi_to_km` multiplies by it. A second
  constant for "miles per kilometre" would be a second thing that can be
  edited, and two numbers that are supposed to agree eventually do not.
- **Validate next to the `input()` that read the value.** Every check in
  this program lives in the function that does the reading, so no caller
  ever has to wonder whether a value has been checked already.
- **Catch `ValueError` by name.** A bare `except:` also swallows Ctrl+C
  and a `KeyboardInterrupt` is not a typo. Lecture 3 section 3 has the
  shape.
- **No third-party packages.** Standard library only, so the file runs on
  a fresh Python with no install step. The answer imports `sys` and
  nothing else.
- **No loops.** The program runs once. A `while True:` belongs in the
  stretch goal, and if you find yourself writing one before all six
  paths work, you are solving the wrong problem first.
- **The questions answer themselves when nobody is typing.** The
  downloadable answer wraps `input()` in the same `ask()` helper as the
  two Week 2 challenges, so the file can be run by anybody — you, a
  classmate, an automatic check — and always print the same session.
  `input()` with nothing attached to it raises `EOFError`, or sits there
  waiting forever. Your own copy may use plain `input()`; just know that
  it can then only be run by hand.

**And one constraint that needs talking about.** The original brief says:

> **No** `if`/`elif` ladders of more than ~3 branches — Week 3 covers
> cleaner control flow.

Read literally, that is a strange thing to ask of a program that is a
three-category menu crossed with a two-direction menu. Six endings have
to be reached somehow, and Week 2's lectures do hand you `if` — lecture
1 section 7.4 and lecture 2 section 4.1 both use it — and lecture 3
section 3 hands you `try` / `except`. The toolbox is not as empty as the
sentence implies.

So take the rule as what it is protecting against, rather than as a ban
on the keyword. What it is protecting against is a single flat ladder
with six or eight arms in one function, where the reading of the input,
the choice of formula, and the wording of the output are all tangled
together and every new unit means another arm. That function grows
forever and cannot be read in one screen.

The answer below obeys the spirit exactly. `main()` makes a three-way
choice between categories. Each category's runner makes a two-way choice
between directions. No ladder anywhere has more than three arms, each
one fits on a screen, and adding a fourth category is one new function
and one new arm that cannot break the other three.

And the place the rule is really steering you is a table instead of a
ladder: a dictionary that maps the two menu answers to the labels and
the function to call, with no branching at all. That needs dictionaries,
which are Week 5, so it is not required today — but it is written out and
run in the first *Under the hood* block below, because seeing where you
are heading makes the intermediate step make sense.

## Expected output

The downloadable file answers its own questions when nothing is attached
to its input, so the automatic run is the same every time. This is the
real stdout on CPython 3.13.2, and it is the brief's first session line
for line:

```text
$ python unit_converter.py
================================
   Code Crunch Unit Converter
================================

Categories:
  1) Temperature (C / F)
  2) Distance    (km / mi)
  3) Currency    (USD / EUR)

Pick a category (1-3): 1

Direction:
  a) Celsius     -> Fahrenheit
  b) Fahrenheit  -> Celsius

Choose direction (a/b): a

Value in Celsius: 100

Result: 100.00 C = 212.00 F

Thanks for using the converter!
```

Answer it differently and you get one of the other five endings. Feeding
the three answers in from the shell, one per line, is the quickest way to
check all of them:

```bash
printf '3\na\n250\n' | python unit_converter.py
```

Abridged to the answers and the result line, all six paths:

| Category | Direction | Value | Result line |
|---|---|---|---|
| 1 | a | `100` | `Result: 100.00 C = 212.00 F` |
| 1 | b | `212` | `Result: 212.00 F = 100.00 C` |
| 2 | a | `5` | `Result: 5.00 km = 3.11 mi` |
| 2 | b | `5` | `Result: 5.00 mi = 8.05 km` |
| 3 | a | `250` | `Result: $250.00 USD = €228.50 EUR  (rate: 1 USD = 0.9140 EUR)` |
| 3 | b | `250` | `Result: €250.00 EUR = $273.52 USD  (rate: 1 USD = 0.9140 EUR)` |

Every one of those is checkable against something outside the program.
Water freezes at 0 °C and 32 °F and boils at 100 °C and 212 °F. A mile is
*defined* as exactly 1.609344 kilometres. That is what makes them worth
testing against.

All three failure paths, and none of them prints a traceback or a
farewell:

```text
Pick a category (1-3): 9

Error: '9' is not a category. Pick 1, 2, or 3.
```

```text
Choose direction (a/b): z

Error: 'z' is not a direction. Pick a or b.
```

```text
Value in Celsius: abc

Error: 'abc' is not a number.
```

The value in quotes is what you actually typed, which is how you spot a
stray space that would otherwise be invisible.

## Steps

**1. Make the folder and open the scaffold.**

```bash
mkdir -p mini-project
```

Copy the code block from [starter.md](./starter.md) into
`mini-project/unit_converter.py` and run it once, unchanged, answering
`1`, `a`, `100`:

```bash
python mini-project/unit_converter.py
```

You should get the full banner, both menus, and `Result: not built yet`.
That is the point. The shell of the program works, so every problem from
here on is a problem in the lines you are about to write.

**2. Do the six conversions first, and prove them.** They are TODO 1
through 6, and they are the part that has to be right before anything
else matters. Check them without the menus:

```bash
python -c "from unit_converter import c_to_f, f_to_c; print(c_to_f(0), c_to_f(100), f_to_c(98.6))"
```

```text
32.0 212.0 37.0
```

Those three are the anchors everybody can check: water freezes at 0 °C
and 32 °F, boils at 100 °C and 212 °F, and normal body temperature is
98.6 °F and 37 °C. What you are watching for on that last one is 37 and
not 54.78, which is the classic missing-parentheses bug.

The import is silent only because of the `if __name__ == "__main__":`
guard. Without it, importing the file would start a menu.

**3. Do TODO 7, the validation.** `parse_float` is four lines: `try` the
cast, `return` it, `except ValueError`, return `None`. It must not print
anything. Its only job is to answer "is this a number, and if so which
one" — the wording of the complaint belongs to whoever asked.

**4. Do TODO 8 through 10, one result line at a time.** Write the
temperature line, run the program, and compare it to the table above
character by character. When one line is right, the other five are the
same shape.

**5. Test all six paths.** Six runs by hand, or six one-liners:

```bash
for spec in "1 a 100" "1 b 212" "2 a 5" "2 b 5" "3 a 250" "3 b 250"; do
  set -- $spec
  printf "$1\n$2\n$3\n" | python mini-project/unit_converter.py | grep '^Result'
done
```

**6. Test the three failure paths.** A category of `9`, a direction of
`z`, a value of `abc`. Each should print one clear line and stop. No
traceback.

**7. Add the assertions.** This is the last stretch goal and it takes
thirty seconds, and from now on you can change the file without
wondering whether you broke the arithmetic:

```python
import unit_converter as u

assert u.c_to_f(0) == 32
assert u.c_to_f(100) == 212
assert u.f_to_c(32) == 0
assert round(u.f_to_c(212), 10) == 100
assert round(u.km_to_mi(1.609344), 4) == 1.0
assert u.mi_to_km(1) == 1.609344
assert round(u.usd_to_eur(100), 2) == 91.40
print("all assertions passed")
```

```text
$ python check_conversions.py
all assertions passed
```

Note the `round()` calls on the ones that go through a division.
Comparing floats with `==` is a habit that will betray you — lecture 2
section 3 — so round first.

**8. Commit and push.**

```bash
git add mini-project/unit_converter.py
git commit -m "Week 2 mini-project: unit converter CLI"
git push
```

**9. Link it from your repository README**, with a screenshot of one
session. This is the step people skip.

## The Solution

```python
"""Code Crunch Unit Converter -- a one-shot, menu-driven CLI.

Week 2 mini-project, Code Crunch Convos. Converts between Celsius and
Fahrenheit, kilometers and miles, and US dollars and euros. Runs one
conversion and exits.

The questions go to the error stream and the banner, the menus and the
result go to the normal output stream. When the input stream is already
finished -- which is what happens when a checker runs the file -- each
question answers itself from the demo values below, so the file always
prints a complete session instead of waiting for typing that is never
coming.

Run it with::

    python unit_converter.py
"""

import sys

USD_TO_EUR: float = 0.9140  # hardcoded; see the stretch goals
KM_PER_MILE: float = 1.609344

BANNER: str = """================================
   Code Crunch Unit Converter
================================"""

DEMO_CATEGORY: str = "1"
DEMO_DIRECTION: str = "a"
DEMO_VALUE: str = "100"


# --------------------------------------------------------------------
# Asking
# --------------------------------------------------------------------

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


# --------------------------------------------------------------------
# Conversions
# --------------------------------------------------------------------

def c_to_f(c: float) -> float:
    """Return degrees Celsius ``c`` converted to Fahrenheit."""
    return c * 9 / 5 + 32


def f_to_c(f: float) -> float:
    """Return degrees Fahrenheit ``f`` converted to Celsius."""
    return (f - 32) * 5 / 9


def km_to_mi(km: float) -> float:
    """Return kilometers ``km`` converted to miles."""
    return km / KM_PER_MILE


def mi_to_km(mi: float) -> float:
    """Return miles ``mi`` converted to kilometers."""
    return mi * KM_PER_MILE


def usd_to_eur(usd: float) -> float:
    """Return US dollars ``usd`` converted to euros."""
    return usd * USD_TO_EUR


def eur_to_usd(eur: float) -> float:
    """Return euros ``eur`` converted to US dollars."""
    return eur / USD_TO_EUR


# --------------------------------------------------------------------
# Input helpers
# --------------------------------------------------------------------

def read_direction() -> str | None:
    """Return ``"a"`` or ``"b"``, or ``None`` after printing an error."""
    raw: str = ask("\nChoose direction (a/b): ", DEMO_DIRECTION)
    cleaned: str = raw.strip().lower()
    if cleaned == "a" or cleaned == "b":
        return cleaned
    print(f"\nError: {cleaned!r} is not a direction. Pick a or b.")
    return None


def read_value(unit_label: str) -> float | None:
    """Return the number the user typed, or ``None`` if it isn't one."""
    raw: str = ask(f"\nValue in {unit_label}: ", DEMO_VALUE)
    try:
        return float(raw)
    except ValueError:
        print(f"\nError: {raw!r} is not a number.")
        return None


# --------------------------------------------------------------------
# One category each
# --------------------------------------------------------------------

def run_temperature() -> bool:
    """Run the temperature conversion. Return True if it succeeded."""
    print("\nDirection:")
    print("  a) Celsius     -> Fahrenheit")
    print("  b) Fahrenheit  -> Celsius")

    direction: str | None = read_direction()
    if direction is None:
        return False

    if direction == "a":
        value: float | None = read_value("Celsius")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} C = {c_to_f(value):.2f} F")
    else:
        value = read_value("Fahrenheit")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} F = {f_to_c(value):.2f} C")
    return True


def run_distance() -> bool:
    """Run the distance conversion. Return True if it succeeded."""
    print("\nDirection:")
    print("  a) Kilometers -> Miles")
    print("  b) Miles      -> Kilometers")

    direction: str | None = read_direction()
    if direction is None:
        return False

    if direction == "a":
        value: float | None = read_value("kilometers")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} km = {km_to_mi(value):.2f} mi")
    else:
        value = read_value("miles")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} mi = {mi_to_km(value):.2f} km")
    return True


def run_currency() -> bool:
    """Run the currency conversion. Return True if it succeeded."""
    print("\nDirection:")
    print("  a) USD -> EUR")
    print("  b) EUR -> USD")

    direction: str | None = read_direction()
    if direction is None:
        return False

    rate_note: str = f"(rate: 1 USD = {USD_TO_EUR:.4f} EUR)"

    if direction == "a":
        value: float | None = read_value("USD")
        if value is None:
            return False
        print(
            f"\nResult: ${value:,.2f} USD = "
            f"€{usd_to_eur(value):,.2f} EUR  {rate_note}"
        )
    else:
        value = read_value("EUR")
        if value is None:
            return False
        print(
            f"\nResult: €{value:,.2f} EUR = "
            f"${eur_to_usd(value):,.2f} USD  {rate_note}"
        )
    return True


# --------------------------------------------------------------------
# Program flow
# --------------------------------------------------------------------

def main() -> None:
    """Print the menus, run one conversion, and exit."""
    print(BANNER)
    print("\nCategories:")
    print("  1) Temperature (C / F)")
    print("  2) Distance    (km / mi)")
    print("  3) Currency    (USD / EUR)")

    category: str = ask("\nPick a category (1-3): ", DEMO_CATEGORY).strip()

    if category == "1":
        converted: bool = run_temperature()
    elif category == "2":
        converted = run_distance()
    elif category == "3":
        converted = run_currency()
    else:
        print(f"\nError: {category!r} is not a category. Pick 1, 2, or 3.")
        return

    if converted:
        print("\nThanks for using the converter!")


if __name__ == "__main__":
    main()
```

**The program is four layers, and each one only knows the layer below
it.**

```text
main()                  reads the category, picks a runner, says thanks
  run_temperature()     prints its own direction menu, drives one conversion
  run_distance()
  run_currency()
      read_direction()  a validated "a" or "b"
      read_value()      a validated float
          c_to_f() f_to_c() km_to_mi() mi_to_km() usd_to_eur() eur_to_usd()
```

Read it top down and each line is a summary of the line under it. That is
the shape you are after when a program stops fitting in your head.

**One runner per category, instead of one long ladder.** There are six
endings. A single flat `if` / `elif` chain would need six arms, each
containing its own reading and validating and printing, and `main()`
would be four screens long. Splitting by category gives `main()` a
three-way choice and each runner a two-way choice. It also puts each
category's direction menu right next to the code that acts on it, so
adding weights or times is one new function and one new arm, and you
cannot break the three that already work by doing it.

**The runners return `True` or `False`.** Look at the sample sessions:
the farewell prints after a conversion. If you typo the direction, the
program should say what went wrong and stop, not thank you for nothing.
The runner is the only code that knows whether it got that far, so it
reports back and `main()` decides what to print. One line of design that
keeps every error message next to the input that caused it.

**The input helpers return "a value, or nothing".** `read_value()` has
two possible outcomes: a number, or a failure it has already complained
about. `float | None` says exactly that in the signature — the spelling
is straight out of lecture 3 section 6.4 — and the caller's
`if value is None: return False` is the whole of the handling.

It is `is None` and not `== None` because there is only ever one `None`
object in a running Python, so asking "is it *that* object" is both
faster and immune to a type that has redefined `==`. Lecture 1 section
4.5 has the background.

An alternative design raises an exception and catches it in `main()`.
That is cleaner once you have Week 6's material. Returning `None` uses
only what you have today.

**`c * 9 / 5 + 32` gets its order for free.** `*` and `/` bind tighter
than `+`, and they run left to right, so Python reads it as
`((c * 9) / 5) + 32`. Writing `c * (9 / 5) + 32` is the same formula and
a slightly worse program, because `9 / 5` is `1.8`, and `1.8` is one of
the numbers a binary float cannot hold exactly. Multiplying by the
whole number first postpones the rounding:

```bash
python -c "print(37 * 9 / 5 + 32, 37 * (9 / 5) + 32)"
```

```text
98.6 98.60000000000001
```

The reverse function does need its parentheses. `(f - 32) * 5 / 9`
subtracts first; without them Python would scale first and hand you a
plausible-looking wrong answer.

**One constant per relationship.** `km_to_mi` divides by `KM_PER_MILE`,
`mi_to_km` multiplies by it. Two constants would be two things that can
be edited independently, and one day they disagree. The same reasoning
puts a single `USD_TO_EUR` in the file, with `eur_to_usd` dividing rather
than storing a second rate.

**`.strip().lower()` on the menu answers, nothing on the number.**
Requirement 3 asks for case-insensitive letters, and a trailing space
from a fast typist is forgiven for free. The numeric answer is
deliberately *not* stripped, because `float()` already ignores
surrounding whitespace — `float(" 100 ")` is `100.0`. Leaving it raw
means the error message shows exactly what was typed.

**`{value:,.2f}` for money, `{value:.2f}` for everything else.** The
comma earns its place the first time somebody converts `1250000` USD and
reads `€1,142,500.00` instead of a wall of digits. The rate note uses
`.4f` to match the sample's `0.9140` — four decimals, including the
trailing zero that plain `str(0.914)` would drop.

**One thing the brief left open: the rate note on the way back.** The
sample only shows USD to EUR, with `(rate: 1 USD = 0.9140 EUR)`. Going
the other way, this answer prints the *same* note rather than inverting
it to `1 EUR = 1.0941 USD`. The note documents the constant the program
is using, and there is exactly one constant. Inverting it is also
defensible — just be consistent, and do not hide a `1 / USD_TO_EUR`
inside an f-string where a reader cannot see it.

**`ask()` reads a line and has an answer ready if there is none.** It
prints the question to `sys.stderr` with `end=""` so the cursor stays on
the line, and `flush=True` so the text appears before the program starts
waiting. Then `input()` reads a line. When the stream has already ended,
`input()` raises `EOFError`, and the `except` prints the question and the
demo answer together on the normal output stream. So the file talks to a
person, reads piped-in answers, or prints a complete demo session — three
behaviours out of six lines. The same helper appears in both Week 2
challenges.

## Download and run

Download [unit_converter.py](./unit_converter.py) and run it:

```bash
python unit_converter.py
```

In your own terminal it asks you the three questions. Run by a script, or
with its input closed, it answers itself from the demo values and prints
the temperature session above.

Feed it the three answers from the shell to reach any of the six
endings:

```bash
printf '3\na\n250\n' | python unit_converter.py
```

This page has no `.py` of its own on purpose. The deliverable of a
mini-project is the folder in your repository — the script, the commit
history, the README entry, the screenshot — and no single file can stand
in for that. `unit_converter.py` is the part of it that runs, and it is
the file above.

The scaffold you build it from is on [starter.md](./starter.md).

## Common bugs to catch

**`98.6 F = 54.78 C` instead of `37.00 C`.** Missing parentheses in
`f_to_c`. You wrote `f - 32 * 5 / 9`, which multiplies before it
subtracts. It has to be `(f - 32) * 5 / 9`. No error, no traceback, just
a wrong answer that looks like a right one — which is why step 2 checks
the formulas against known values before anything else is built.

**You forgot `float()`, and found out three lines later.**

```text
  File "unit_converter.py", line 3, in c_to_f
    return c * 9 / 5 + 32
           ~~~~~~^~~
TypeError: unsupported operand type(s) for /: 'str' and 'int'
```

`c * 9` succeeded — it repeated the text `"100"` nine times — and only
the division failed. The complaint therefore points one operator past
the mistake. `mypy` catches this before you ever run it, which is the
entire argument for the type hints requirement 11 asks for:

```text
$ mypy unit_converter.py
unit_converter.py:7: error: Argument 1 to "c_to_f" has incompatible type "str"; expected "float"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

**`TypeError: unsupported format string passed to NoneType.__format__`.**

```text
  File "<string>", line 1, in <module>
    v=None; print(f"{v:.2f}")
                    ^^^^^^^
TypeError: unsupported format string passed to NoneType.__format__
```

You applied `:.2f` to the result of `read_value()` without checking it
for `None` first, or you deleted the `if value is None:` guard. The guard
has to come before the formatting, not after.

**`Result: 26.097590073968025 mi`.** You left a format spec off one
placeholder. `{value}` prints the float in full; `{value:.2f}` rounds it
*for display only* and leaves the stored number untouched.

**`Result: $250 USD` with no cents.** No format spec at all, or `:,d`.
Money always shows two decimals, even when they are zeros, because a
column of prices that sometimes has cents and sometimes does not is
unreadable.

**`if raw == "a" and raw == "b":`.** This can never be true — no string
is two different strings at once — so every direction is rejected. You
meant `or`. Once you reach Week 5, `if raw in ("a", "b"):` is the way
this is normally written.

**The direction menu is rejected for a capital `A`.** The `.lower()` is
missing, or it is at the three call sites instead of once inside
`read_direction()`.

**A bad category prints nothing at all.** You wrote the ladder with no
final `else`. Typing `9` shows the banner, the menu, and then silence. A
program that exits without saying anything looks broken even when it is
not.

**`UnicodeEncodeError: 'charmap' codec can't encode character '€'`.**

```text
  File "unit_converter.py", line 139, in run_currency
    print(
    ~~~~~^
        f"\nResult: ${value:,.2f} USD = "
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        f"€{usd_to_eur(value):,.2f} EUR  {rate_note}"
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
UnicodeEncodeError: 'charmap' codec can't encode character '€' in position 24: character maps to <undefined>
```

The euro sign is `U+20AC`, and an old Windows console code page has no
slot for it. Your code is fine; the terminal is the problem. Three ways
out, best first: run `chcp 65001` in that console, set `PYTHONUTF8=1` in
your environment, or print `EUR` instead of `€`. Save your source as
UTF-8 — every modern editor does by default — or the file will not even
parse.

**`NameError: name 'value' is not defined`.** You moved the result line
above the `value = read_value(...)` line while editing. Python reads a
function body top to bottom; a name exists only after the line that
bound it.

## Under the hood

<details>
<summary>Under the hood — a table of conversions instead of a ladder of branches</summary>

The *Constraints* section promised to show where the "no long `if`
ladders" rule is pointing. Here it is.

Look at what the six endings actually differ by. Not much: a label for
the unit going in, a label for the unit coming out, and which function to
call. Three pieces of data. The `if` statements exist only to fetch those
three pieces, and a ladder is a clumsy way to fetch data.

A dictionary fetches data directly. The key is the two menu answers stuck
together — `"1a"`, `"2b"` — and the value is the three things that
ending needs:

```python
from collections.abc import Callable

KM_PER_MILE: float = 1.609344
USD_TO_EUR: float = 0.9140

CONVERSIONS: dict[str, tuple[str, str, Callable[[float], float]]] = {
    "1a": ("C", "F", lambda c: c * 9 / 5 + 32),
    "1b": ("F", "C", lambda f: (f - 32) * 5 / 9),
    "2a": ("km", "mi", lambda km: km / KM_PER_MILE),
    "2b": ("mi", "km", lambda mi: mi * KM_PER_MILE),
    "3a": ("USD", "EUR", lambda usd: usd * USD_TO_EUR),
    "3b": ("EUR", "USD", lambda eur: eur / USD_TO_EUR),
}

for key in ("1a", "2a", "3a"):
    unit_in, unit_out, convert = CONVERSIONS[key]
    print(f"{key}: 100.00 {unit_in} = {convert(100.0):.2f} {unit_out}")

print(CONVERSIONS.get("9z") is None)
```

```text
1a: 100.00 C = 212.00 F
2a: 100.00 km = 62.14 mi
3a: 100.00 USD = 91.40 EUR
True
```

Three lines do the work that six branches were doing, and none of the
three mentions temperature, distance or currency.

Four things are worth noticing.

**Functions are values.** `c_to_f` without the parentheses is not a call
— it is the function itself, and you can put it in a list, hand it to
another function, or store it in a dictionary, exactly like a number.
`convert` then holds whichever one came out of the table, and
`convert(100.0)` calls it. This is the single idea that makes the whole
technique work, and it surprises everybody the first time. (`lambda x:
...` above is just a way of writing a small function without giving it a
name first; six named `def`s in the table would work identically.)

**Adding a unit stops being a code change.** A seventh conversion is one
more line inside the braces. No new branch, no chance of breaking the
six that work, and nothing to forget — you cannot add a row that has a
label but no function, because the shape of the row is fixed.

**The unknown key is free.** `CONVERSIONS.get("9z")` hands back `None`
instead of raising, so the whole of the "that is not a valid choice"
handling is one `if` at the end, not an `else` on every ladder.
`CONVERSIONS["9z"]` would raise `KeyError: '9z'` instead — `.get()` is
the version that asks politely.

**And the price.** The table is data, so a reader can no longer see the
program's behaviour by reading its statements — they have to read the
table too. With six rows that is obviously a win. With two, it is
obviously not, and the honest answer for two branches is two branches.
The skill being learned is noticing when the ladder has stopped being
about *choosing* and started being about *fetching*.

Dictionaries arrive properly in Week 5, and functions-as-values in Week
4. Nothing above is required for this project. It is here so that when
Week 5 hands you `dict`, you already know what it is for.

</details>

<details>
<summary>Under the hood — why the numbers come back with a tail of nines</summary>

Convert 250 US dollars to euros and back and you land exactly where you
started:

```bash
python -c "R = 0.9140; print(250 * R, 250 * R / R)"
```

```text
228.5 250.0
```

Try 21:

```bash
python -c "R = 0.9140; print(21 * R / R)"
```

```text
20.999999999999996
```

Same two operations, and one of them does not come home. Of the whole
numbers from 1 to 1000, seventy-six behave like 21.

The reason is that a `float` stores numbers in binary, and most decimal
fractions do not finish in binary any more than one third finishes in
decimal. `0.9140` is stored as the nearest number the hardware *can*
hold, which is very slightly off. Multiplying rounds to the nearest
storable number again; dividing rounds a third time. Sometimes those tiny
roundings cancel out and you get 250.0 back. Sometimes they do not, and
you get a tail of nines.

The famous one-liner is the same thing:

```bash
python -c "print(0.1 + 0.2)"
```

```text
0.30000000000000004
```

Nothing is broken, no version of Python fixes this, and every language
that uses your computer's floating-point hardware does exactly the same.
Lecture 1 section 4.2 is the short version.

Three practical rules fall out of it, and they are all this project
needs.

**Never compare two floats with `==`.** `f_to_c(212) == 100` is `True`,
and so is `f_to_c(98.6) == 37`. That is luck, not a promise. Take −7 °C
to Fahrenheit and back:

```bash
python -c "from unit_converter import c_to_f, f_to_c; print(f_to_c(c_to_f(-7)))"
```

```text
-7.000000000000001
```

Twenty of the whole numbers between −100 and 100 fail to come home like
that. Round before you compare, which is what the assertions in step 7
do, or compare against a tolerance with `math.isclose(a, b)`.

**Format for display, and keep the full value for arithmetic.**
`{value:.2f}` changes what is printed and nothing else. The stored number
keeps all of its digits, so a second calculation starts from the real
value rather than from a rounded one. Rounding early and then adding the
rounded numbers is how a total stops matching its own rows.

**When cents must be exact, stop using floats.** The `decimal` module
stores numbers the way a person writes them, and a real currency
converter would use it. Compare:

```bash
python -c "from decimal import Decimal; print(0.1 + 0.2); print(Decimal('0.1') + Decimal('0.2'))"
```

```text
0.30000000000000004
0.3
```

Note the quotes. `Decimal("0.1")` reads the text and gets the number you
meant; `Decimal(0.1)` takes the broken float and preserves its brokenness
faithfully. A converter with a hardcoded rate does not need any of this.
Knowing when you *would* need it is the point.

</details>

## Acceptance checklist

- [ ] `python unit_converter.py` prints the banner and the three-item
      category menu.
- [ ] All six paths produce the result lines in the table under
      *Expected output*, character for character.
- [ ] `A` and `a` are both accepted as a direction, and so is ` a `.
- [ ] A category of `9` prints one clear line and exits with no
      traceback.
- [ ] A direction of `z` prints one clear line and exits with no
      traceback.
- [ ] A value of `abc` prints one clear line and exits with no
      traceback.
- [ ] Every number in every result line shows exactly two decimals, and
      money carries a thousands separator and its symbol.
- [ ] The currency line ends with the rate, at four decimals.
- [ ] `USD_TO_EUR` and `KM_PER_MILE` are module-level constants, and
      neither number is typed anywhere else in the file.
- [ ] The six conversion functions contain no `input()` and no `print()`.
- [ ] Every function has type hints on its parameters and its return,
      and a docstring, and no `TODO` comments remain.
- [ ] `main()` sits behind `if __name__ == "__main__":`, and importing
      the file prints nothing.
- [ ] Four-space indentation, `snake_case` names, `UPPER_SNAKE_CASE`
      constants, lines under 80 characters.
- [ ] Saved as `mini-project/unit_converter.py`, committed, and pushed.
- [ ] Linked from your repository README, with a screenshot of a
      session.

The project is worth forty points. These are the same criteria, weighted:

| Criterion | Points | Where it is earned |
|-----------|-------:|--------------------|
| Six conversion functions implemented correctly | 12 | The assertions in step 7 |
| Each function has a docstring and type hints | 4 | Every `def` in the file |
| Banner and menus match the specified layout closely | 4 | Diffed against both sample sessions |
| Reads category, direction, and value from a prompt | 4 | `main()`, `read_direction()`, `read_value()` |
| Validates non-numeric input gracefully | 4 | `try` / `except ValueError`, plus both menu guards |
| Output formatted with two decimals and correct labels | 6 | `:.2f` and `:,.2f`, unit labels in every result line |
| Constants used for exchange rate and km-per-mile | 2 | `USD_TO_EUR`, `KM_PER_MILE` at module top |
| Organised into `main()` with `if __name__ == "__main__":` | 2 | Bottom of the file |
| Clean, readable code; PEP 8 names | 2 | Throughout |
| **Total** | **40** | |

## Stretch

Keep these in a second file, `unit_converter_stretch.py`, so the graded
one stays the small clean thing the checklist grades.

**Loop until quit, take the rate from the environment, and add a fourth
category.** These three fit together in one file. The difference from the
base program is: an `import os`, a `load_rate()` function, a
`while True:` around the menu, a `q` option, and one more runner.

```python
"""Unit converter, stretch edition: loop, quit, env-var rate, weight."""

import os

USD_TO_EUR_DEFAULT: float = 0.9140
KM_PER_MILE: float = 1.609344
KG_PER_POUND: float = 0.45359237


def load_rate() -> float:
    """Return the USD->EUR rate from the environment, or the default."""
    raw: str = os.environ.get("USD_TO_EUR", "")
    try:
        rate: float = float(raw)
    except ValueError:
        return USD_TO_EUR_DEFAULT
    if rate <= 0:
        return USD_TO_EUR_DEFAULT
    return rate


USD_TO_EUR: float = load_rate()


def kg_to_lb(kg: float) -> float:
    """Return kilograms ``kg`` converted to pounds."""
    return kg / KG_PER_POUND


def lb_to_kg(lb: float) -> float:
    """Return pounds ``lb`` converted to kilograms."""
    return lb * KG_PER_POUND


def run_weight() -> None:
    """Run one weight conversion."""
    print("\nDirection:")
    print("  a) Kilograms -> Pounds")
    print("  b) Pounds    -> Kilograms")
    direction: str | None = read_direction()
    if direction is None:
        return
    if direction == "a":
        value: float | None = read_value("kilograms")
        if value is None:
            return
        print(f"\nResult: {value:.2f} kg = {kg_to_lb(value):.2f} lb")
    else:
        value = read_value("pounds")
        if value is None:
            return
        print(f"\nResult: {value:.2f} lb = {lb_to_kg(value):.2f} kg")


def main() -> None:
    """Loop over conversions until the user quits."""
    print(BANNER)
    while True:
        print("\nCategories:")
        print("  1) Temperature (C / F)")
        print("  2) Distance    (km / mi)")
        print("  3) Currency    (USD / EUR)")
        print("  4) Weight      (kg / lb)")
        print("  q) Quit")

        category: str = input("\nPick a category (1-4, q): ").strip().lower()

        if category == "q":
            print("\nThanks for using the converter!")
            return
        if category == "1":
            run_temperature()
        elif category == "2":
            run_distance()
        elif category == "3":
            run_currency()
        elif category == "4":
            run_weight()
        else:
            print(f"\nError: {category!r} is not a category.")


if __name__ == "__main__":
    main()
```

The six original conversion functions, `read_direction()`,
`read_value()`, `BANNER`, and the three original runners are unchanged —
except that in the looping version the runners no longer need to return
`bool`, because the farewell now belongs to the `q` branch.

A real session, with the rate overridden from the shell:

```text
$ USD_TO_EUR=0.8800 python unit_converter_stretch.py
================================
   Code Crunch Unit Converter
================================

Categories:
  1) Temperature (C / F)
  2) Distance    (km / mi)
  3) Currency    (USD / EUR)
  4) Weight      (kg / lb)
  q) Quit

Pick a category (1-4, q): 4

Direction:
  a) Kilograms -> Pounds
  b) Pounds    -> Kilograms

Choose direction (a/b): a

Value in kilograms: 80

Result: 80.00 kg = 176.37 lb

Categories:
  1) Temperature (C / F)
  2) Distance    (km / mi)
  3) Currency    (USD / EUR)
  4) Weight      (kg / lb)
  q) Quit

Pick a category (1-4, q): 3

Direction:
  a) USD -> EUR
  b) EUR -> USD

Choose direction (a/b): a

Value in USD: 250

Result: $250.00 USD = €220.00 EUR  (rate: 1 USD = 0.8800 EUR)

Categories:
  ...
Pick a category (1-4, q): q

Thanks for using the converter!
```

The rate note reads `0.8800`, so you can see the override took effect. In
PowerShell the syntax is `$env:USD_TO_EUR = "0.8800"` before running; in
`cmd` it is `set USD_TO_EUR=0.8800`.

**`load_rate()` is the interesting part.**
`os.environ.get("USD_TO_EUR", "")` gives you the environment variable if
it is set and the empty string if it is not. `float("")` raises
`ValueError`, which the `except` turns into the default — so "not set"
and "set to nonsense" take the same safe path through one `try`. The
`<= 0` check catches a rate of `0` or `-1`, which would parse fine and
then produce either a `ZeroDivisionError` or negative money.

`USD_TO_EUR` is computed once, when the file is loaded, so the rate is
fixed for the whole run. That is what you want: a report where line 1 and
line 3 used different rates is worse than one that is slightly stale.

**The loop moves who owns the farewell.** In the base program `main()`
prints it when the conversion succeeded. Here the only way out is `q`, so
it lives in that branch and `return` ends the program from inside the
loop. An error inside a runner just falls back to the top of the loop and
shows the menu again, which is a better experience — and the reason the
looping version is a stretch goal rather than the default is that it
hides the "runs once and exits" requirement you were asked to satisfy
first.

**`KG_PER_POUND = 0.45359237` is exact.** The international pound is
*defined* as that many kilograms, so `kg_to_lb` divides by it for the
same reason `km_to_mi` divides by `KM_PER_MILE`.

**Twenty-four-hour time to twelve-hour time.** The other suggested
category converts between two *representations* rather than two
magnitudes, which makes it a modulo exercise:

```python
def to_12_hour(time_24: str) -> str:
    """Return ``"HH:MM"`` in 24-hour form as ``"H:MM AM/PM"``."""
    hour_str, minute_str = time_24.strip().split(":")
    hour: int = int(hour_str)
    minute: int = int(minute_str)
    suffix: str = "AM"
    if hour >= 12:
        suffix = "PM"
    hour_12: int = hour % 12
    if hour_12 == 0:
        hour_12 = 12
    return f"{hour_12}:{minute:02d} {suffix}"
```

The two special cases are the whole problem, and both live at `0` and
`12`. `hour % 12` maps 13 to 1 and 23 to 11, which is right, but it also
maps both midnight and noon to `0` — and there is no zero o'clock on a
twelve-hour clock, so both become `12`. The `AM` / `PM` decision is made
*before* the modulo, from the original hour, which is why noon comes out
`12:00 PM` and five past midnight `12:05 AM`. `{minute:02d}` pads the
minute with a leading zero, using the same mini-language as everything
else this week.

```python
assert to_12_hour("00:05") == "12:05 AM"
assert to_12_hour("09:00") == "9:00 AM"
assert to_12_hour("12:00") == "12:00 PM"
assert to_12_hour("13:45") == "1:45 PM"
assert to_12_hour("23:59") == "11:59 PM"
print("all assertions passed")
```

```text
$ python t12.py
all assertions passed
```

`hour_str, minute_str = time_24.strip().split(":")` is tuple unpacking,
from lecture 3 section 4. If somebody types `9` with no colon, it raises
`ValueError: not enough values to unpack (expected 2, got 1)`, so wire it
into the menu behind a `try` / `except`.

**Paint the banner.** ANSI escape codes colour terminal text:

```python
CYAN: str = "\033[1;36m"
RESET: str = "\033[0m"

BANNER: str = f"""{CYAN}================================
   Code Crunch Unit Converter
================================{RESET}"""
```

`\033` is the escape character, decimal 27, written as an octal escape.
`[1;36m` means "bold, foreground cyan," and `[0m` resets everything. The
reset is not optional — leave it out and the colour leaks into your shell
prompt after the program exits. Wrap only the banner, so error messages
stay readable.

Two caveats. Modern Windows Terminal and PowerShell 7 handle ANSI fine;
the legacy `cmd.exe` console may not, and you will see literal
`←[1;36m` garbage. And if you redirect the output to a file the escape
codes go into the file too, which is why real tools check whether they
are writing to a terminal before colouring. That check is
`sys.stdout.isatty()`, and it is worth remembering that it exists.

**Make it pass `mypy --strict`.** The answer above already does:

```bash
$ mypy --strict unit_converter.py
Success: no issues found in 1 source file
```

`--strict` turns on about a dozen separate checks at once. Two of them
bite in a file like this. `--disallow-untyped-defs` insists every
function is annotated, including the `-> None` on `main()`.
`--strict-optional` refuses to let a `float | None` be used where a
`float` is required until you have checked it for `None` — which means
`if value is None: return False` is not merely tidy. Delete it and the
type checker rejects the file:

```text
error: Argument 1 to "c_to_f" has incompatible type "float | None"; expected "float"  [arg-type]
```

It is enforcing the one thing you would otherwise forget.

**Test it with assertions.** The block is in step 7 above. Two notes for
when Week 11 replaces it with pytest. `assert` statements are stripped
out entirely when Python runs with `-O`, so they are a development tool
and never a runtime guarantee. And every assertion up there compares
against a value from *outside* the program — a physical constant, a
definition — never against what the code happens to produce. An
assertion that restates your implementation tests nothing at all.
