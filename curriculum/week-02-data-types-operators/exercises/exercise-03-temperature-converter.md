# Exercise 3 — Temperature Converter

> **Topic:** Functions, type hints, and float arithmetic
> **Lecture:** [03 — Reading Input and Type Hints](../lecture-notes/03-input-and-type-hints.md)
> **Difficulty:** Medium
> **Target time:** 30 minutes
> **Why this one:** this is the first exercise where you write functions that hand back an answer instead of printing one. Working something out in one place and showing it in another is the shape of nearly every program you will write from here on. It is also where the strangeness of decimal numbers on a computer stops being a footnote in Lecture 1 and becomes something you have to handle on purpose. Friday's mini-project reuses these three functions word for word, so getting them right now takes work off Friday.

## The Brief

You are building the temperature part of the unit-converter tool you ship
on Friday. Three functions. None of them prints anything and none of them
asks the user anything: Celsius to Fahrenheit, Fahrenheit to Celsius, and
Celsius to kelvin. `main()` uses them to print a reference table of six
well-known temperatures, then does a round-trip check.

The round-trip check is the part worth your attention. Take a
temperature, convert it to Fahrenheit, convert it straight back to
Celsius, and you would expect the number you started with. Sometimes you
get it. Sometimes you get a number that differs in the fifteenth decimal
place, because the values in the middle could not be written down exactly
in the number system a computer uses. Lecture 1 told you that
`0.1 + 0.2` is not `0.3`. This is where that stops being a curiosity and
starts changing how you write a comparison.

Two of the six rows in the table are there specifically to catch a wrong
formula. Minus forty is the one temperature where the Celsius and
Fahrenheit scales agree, so if your row does not read `-40.00` in both
columns, your formula is wrong in a way that a warm-weather test would
never show you. And body temperature, 37 degrees Celsius, is exactly
98.60 Fahrenheit — a whole tenth, which the wrong operator quietly eats.

## Starter

Create `exercise-03-temperature-converter.py` and fill the three `TODO`s:

```python
"""exercise-03-temperature-converter.py — convert between C, F, and K.

Week 2, Exercise 3. Practises writing annotated functions, arithmetic
operators and precedence, and comparing floats with a tolerance.
"""

ABSOLUTE_ZERO_C: float = -273.15
FREEZING_POINT_F: float = 32.0
F_PER_C: float = 9 / 5
TOLERANCE: float = 1e-9

LABEL_WIDTH: int = 16
VALUE_WIDTH: int = 9
TABLE_WIDTH: int = 43

ROUND_TRIP_C: float = 23.3


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: a temperature in degrees Celsius.

    Returns:
        The same temperature in degrees Fahrenheit.
    """
    # TODO: scale by F_PER_C, then shift by FREEZING_POINT_F.
    #       Mind the order — the shift happens after the scale.
    ...


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius.

    Args:
        fahrenheit: a temperature in degrees Fahrenheit.

    Returns:
        The same temperature in degrees Celsius.
    """
    # TODO: undo celsius_to_fahrenheit — shift first, then scale back.
    ...


def celsius_to_kelvin(celsius: float) -> float:
    """Convert a Celsius temperature to kelvin.

    Args:
        celsius: a temperature in degrees Celsius.

    Returns:
        The same temperature in kelvin. Never negative for any real
        temperature, because ABSOLUTE_ZERO_C is the bottom of the scale.
    """
    # TODO: express this using ABSOLUTE_ZERO_C rather than a literal 273.15.
    ...


def table_row(label: str, celsius: float) -> str:
    """Return one reference-table row for the given Celsius temperature."""
    return (f"{label:<{LABEL_WIDTH}}"
            f"{celsius:>{VALUE_WIDTH}.2f}"
            f"{celsius_to_fahrenheit(celsius):>{VALUE_WIDTH}.2f}"
            f"{celsius_to_kelvin(celsius):>{VALUE_WIDTH}.2f}")


def main() -> None:
    """Print the reference table and the round-trip check."""
    print(f"{'Reference point':<{LABEL_WIDTH}}"
          f"{'C':>{VALUE_WIDTH}}{'F':>{VALUE_WIDTH}}{'K':>{VALUE_WIDTH}}")
    print("-" * TABLE_WIDTH)
    print(table_row("Absolute zero", ABSOLUTE_ZERO_C))
    print(table_row("Same in C and F", -40.0))
    print(table_row("Water freezes", 0.0))
    print(table_row("Room temperature", 21.0))
    print(table_row("Body temperature", 37.0))
    print(table_row("Water boils", 100.0))
    print("-" * TABLE_WIDTH)

    there: float = celsius_to_fahrenheit(ROUND_TRIP_C)
    back: float = fahrenheit_to_celsius(there)
    print(f"Round-trip: {ROUND_TRIP_C:.1f} C -> {there:.2f} F -> {back:.6f} C")
    print(f"Exact match? {back == ROUND_TRIP_C}   "
          f"Within {TOLERANCE:g}? {abs(back - ROUND_TRIP_C) < TOLERANCE}")


if __name__ == "__main__":
    main()
```

`TOLERANCE: float = 1e-9` is scientific notation. It means
0.000000001 — a one with nine zeros in front of it. It is the size of
"close enough" that this program will accept.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/exercises/exercise-03-temperature-converter.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `celsius_to_fahrenheit()` returns the Fahrenheit equivalent. Water
   freezes at 0 C and 32 F; water boils at 100 C and 212 F; the two
   scales cross at -40.
2. `fahrenheit_to_celsius()` undoes the function above, built from the
   same two constants — subtract `FREEZING_POINT_F`, then divide by
   `F_PER_C`. Making it mirror the forward function is what lets a reader
   check it by eye.
3. `celsius_to_kelvin()` returns kelvin, worked out from
   `ABSOLUTE_ZERO_C` rather than from a `273.15` typed into the function
   body.
4. All three functions take one `float` and return a `float`. None of
   them prints anything, reads input, or uses any name from outside
   itself other than the module constants.
5. Every function keeps its type hints and its docstring.
6. Do not change `table_row()`, `main()`, or the constants.
7. The `Same in C and F` row must show `-40.00` in both the C and F
   columns, and the `Body temperature` row must show `98.60`.

## Constraints

- **Never use `//`.** That is floor division, and it throws the fraction
  away. It would turn 37 C into 98.00 F instead of 98.60 — a bug that
  hides perfectly at 0 C and 100 C, where the answer happens to be a
  whole number anyway. Those are the two temperatures a beginner checks,
  which is exactly why this bug survives long enough to reach real users.
- **Do not use `round()` inside the functions.** Rounding is a decision
  about *showing* a number, and these functions do not show anything.
  `table_row()` already rounds to two decimals with `.2f` at the moment
  of printing. Round early and you throw away precision the round-trip
  check needs; round late and you keep your options.
- **Compare decimals with `abs(a - b) < TOLERANCE`, never with `==`.**
  The program prints both comparisons side by side so you can see the
  difference for yourself. At 23.3 degrees, `==` says the round trip
  failed and the tolerance check says it succeeded. The tolerance one is
  telling the truth about the temperature; `==` is telling the truth
  about the last bit of a 64-bit number. You almost always want the
  first.
- **Write kelvin as `celsius - ABSOLUTE_ZERO_C`, not `celsius + 273.15`.**
  They give the same number. The first says *why* the number is what it
  is, and if the constant is ever refined there is exactly one place to
  change it. The second is a bare number with no explanation attached,
  which the week's style note tells you to avoid.
- **No `import`.** Nothing here needs a library. `math` has no
  temperature helpers, and reaching for `decimal` to dodge the
  floating-point lesson would defeat the exercise.

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2:

```text
$ python exercise-03-temperature-converter.py
Reference point         C        F        K
-------------------------------------------
Absolute zero     -273.15  -459.67     0.00
Same in C and F    -40.00   -40.00   233.15
Water freezes        0.00    32.00   273.15
Room temperature    21.00    69.80   294.15
Body temperature    37.00    98.60   310.15
Water boils        100.00   212.00   373.15
-------------------------------------------
Round-trip: 23.3 C -> 73.94 F -> 23.300000 C
Exact match? False   Within 1e-09? True
```

Read the last line again. `Exact match? False` is the correct output. The
round trip returns `23.299999999999997`, which differs from `23.3` by
about `3.55e-15` — roughly one part in six quadrillion, far smaller than
any thermometer could ever notice, and still more than enough to make
`==` say no.

If your run prints `True` there, do not celebrate. You have almost
certainly rounded inside `fahrenheit_to_celsius()`, and you have hidden
the very thing this exercise exists to show you.

## Steps

1. Turn on your Week 2 virtual environment.
2. Create `exercise-03-temperature-converter.py` and paste the starter in.
3. Write `celsius_to_fahrenheit()` first and run the file. The heading
   and the separator line print, and then the first `table_row()` call
   raises a `TypeError`, because `celsius_to_kelvin()` still hands back
   `None` and `table_row()` builds the whole row in one f-string. That is
   expected at this stage.
4. Write `celsius_to_kelvin()`, then `fahrenheit_to_celsius()`. Run again
   and compare all eleven lines to the Expected output.
5. Check the two trap rows before anything else. `Same in C and F` must
   read `-40.00   -40.00`, and `Body temperature` must read `98.60`.
6. Break it on purpose. Change your formula to
   `(celsius + FREEZING_POINT_F) * F_PER_C` and rerun:

   ```text
   Same in C and F    -40.00   -14.40   233.15
   Water freezes        0.00    57.60   273.15
   ```

   Water still freezes at a perfectly believable `57.60`, and the
   minus-forty row has stopped agreeing with itself. This is what a wrong
   formula looks like from the outside: not a crash, just numbers. Put
   the correct formula back.
7. Break it a second way. Replace `* F_PER_C` with `* 9 // 5` and rerun:

   ```text
   Water freezes        0.00    32.00   273.15
   Room temperature    21.00    69.00   294.15
   Body temperature    37.00    98.00   310.15
   Water boils        100.00   212.00   373.15
   ```

   Freezing and boiling — the two rows most people would check — are
   still perfect, while room temperature and body temperature have
   quietly lost their tenths. Put it back.
8. Run `mypy exercise-03-temperature-converter.py` if you have it
   installed.

## The Solution

```python
"""exercise-03-temperature-converter-solution.py — convert between C, F, and K.

Week 2, Exercise 3. Practises writing annotated functions, arithmetic
operators and precedence, and comparing floats with a tolerance.
"""

ABSOLUTE_ZERO_C: float = -273.15
FREEZING_POINT_F: float = 32.0
F_PER_C: float = 9 / 5
TOLERANCE: float = 1e-9

LABEL_WIDTH: int = 16
VALUE_WIDTH: int = 9
TABLE_WIDTH: int = 43

ROUND_TRIP_C: float = 23.3


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: a temperature in degrees Celsius.

    Returns:
        The same temperature in degrees Fahrenheit.
    """
    return celsius * F_PER_C + FREEZING_POINT_F


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius.

    Args:
        fahrenheit: a temperature in degrees Fahrenheit.

    Returns:
        The same temperature in degrees Celsius.
    """
    return (fahrenheit - FREEZING_POINT_F) / F_PER_C


def celsius_to_kelvin(celsius: float) -> float:
    """Convert a Celsius temperature to kelvin.

    Args:
        celsius: a temperature in degrees Celsius.

    Returns:
        The same temperature in kelvin. Never negative for any real
        temperature, because ABSOLUTE_ZERO_C is the bottom of the scale.
    """
    return celsius - ABSOLUTE_ZERO_C


def table_row(label: str, celsius: float) -> str:
    """Return one reference-table row for the given Celsius temperature."""
    return (f"{label:<{LABEL_WIDTH}}"
            f"{celsius:>{VALUE_WIDTH}.2f}"
            f"{celsius_to_fahrenheit(celsius):>{VALUE_WIDTH}.2f}"
            f"{celsius_to_kelvin(celsius):>{VALUE_WIDTH}.2f}")


def main() -> None:
    """Print the reference table and the round-trip check."""
    print(f"{'Reference point':<{LABEL_WIDTH}}"
          f"{'C':>{VALUE_WIDTH}}{'F':>{VALUE_WIDTH}}{'K':>{VALUE_WIDTH}}")
    print("-" * TABLE_WIDTH)
    print(table_row("Absolute zero", ABSOLUTE_ZERO_C))
    print(table_row("Same in C and F", -40.0))
    print(table_row("Water freezes", 0.0))
    print(table_row("Room temperature", 21.0))
    print(table_row("Body temperature", 37.0))
    print(table_row("Water boils", 100.0))
    print("-" * TABLE_WIDTH)

    there: float = celsius_to_fahrenheit(ROUND_TRIP_C)
    back: float = fahrenheit_to_celsius(there)
    print(f"Round-trip: {ROUND_TRIP_C:.1f} C -> {there:.2f} F -> {back:.6f} C")
    print(f"Exact match? {back == ROUND_TRIP_C}   "
          f"Within {TOLERANCE:g}? {abs(back - ROUND_TRIP_C) < TOLERANCE}")


if __name__ == "__main__":
    main()
```

Three one-line functions. `table_row()`, `main()` and the constants are
exactly as the starter gave them to you.

**The stretch happens before the shift, and Python gets that right on its
own.** `celsius * F_PER_C + FREEZING_POINT_F` needs no brackets, because
`*` is worked out before `+`. Putting brackets in anyway is harmless and
arguably kinder to whoever reads it next. What is *not* harmless is
swapping the two operations round, because the answer stays believable:
at 0 C the wrong version reads `57.60`, and a person could believe that.

**The reverse function mirrors the forward one, and needs brackets to do
it.** `(fahrenheit - FREEZING_POINT_F) / F_PER_C` undoes the two steps in
reverse order: unshift, then unstretch. Here the brackets are doing real
work, because `/` is worked out before `-`. Without them Python computes
`fahrenheit - 17.777...`, which at 212 F gives `194.22` instead of
`100.00`. When one function undoes another, write it as the same two
constants applied backwards. A reader can then check it by looking
instead of by algebra.

**Kelvin is a subtraction because the constant is negative.**
`celsius - ABSOLUTE_ZERO_C` is `celsius - (-273.15)`, which is
`celsius + 273.15`. Naming the constant is what makes the direction
obvious: kelvin counts upward from absolute zero, so you are measuring
the distance from `ABSOLUTE_ZERO_C` up to `celsius`, and a distance is a
subtraction.

**No rounding inside the functions, because rounding is a display
decision.** `table_row()` applies `.2f` at the moment of printing. If a
conversion rounded first, you would have thrown away precision the caller
might need — and in this program the caller does need it, because the
round-trip check exists precisely to expose an error at the fifteenth
decimal place.

**`Exact match? False` is the correct answer, and the tolerance check is
the honest one.** Nothing went wrong. `23.3` cannot be written down
exactly in binary. Neither can the `73.94` in the middle. The two tiny
errors do not cancel out, so the trip back lands on
`23.299999999999997`, which is a different number from `23.3` by
`3.552713678800501e-15`. `abs(back - ROUND_TRIP_C) < TOLERANCE` asks the
question you actually meant — *are these the same temperature?* — rather
than *are these the same pattern of 64 bits?*

**There is no rule for which values survive.** `21.5`, `25.0` and `-40.0`
make the round trip exactly. `23.3`, `37.0` and `18.3` do not, and
nothing about the numbers themselves predicts it:

```text
   23.3  exact=False  repr=23.299999999999997
   21.5  exact=True  repr=21.5
   25.0  exact=True  repr=25.0
  -40.0  exact=True  repr=-40.0
   37.0  exact=False  repr=37.00000000000001
   18.3  exact=False  repr=18.299999999999997
```

That unpredictability is the whole argument. You do not decide this one
value at a time. You use a tolerance, always.

**Nothing here reads input or branches.** Three functions that take a
number and give back a number, and a caller that prints. Separating those
two jobs is the shape of nearly every program you will write after this
week, and it is far easier to see now, while Week 2 has no `if` in it to
tempt you.

## Run it

Copy the worked answer on this page into `exercise-03-temperature-converter.py` and run it:

```bash
python exercise-03-temperature-converter.py
```

## Common bugs to catch

- **`TypeError: unsupported format string passed to NoneType.__format__`.**
  A function still has `...` for a body, so `table_row()` tried to format
  a `None` with `.2f`:

  ```text
  Reference point         C        F        K
  -------------------------------------------
  Traceback (most recent call last):
    File "exercise-03-temperature-converter.py", line 85, in <module>
      main()
      ~~~~^^
    File "exercise-03-temperature-converter.py", line 69, in main
      print(table_row("Absolute zero", ABSOLUTE_ZERO_C))
            ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "exercise-03-temperature-converter.py", line 61, in table_row
      f"{celsius_to_kelvin(celsius):>{VALUE_WIDTH}.2f}")
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: unsupported format string passed to NoneType.__format__
  ```

  The last frame names the function whose answer it tried to format,
  which tells you which `TODO` you skipped. Note that this raises where
  Exercise 2's version of the same mistake did not: there the `None` was
  merely printed, and `print()` prints `None` without complaint. Here the
  `None` is handed a format spec, and that it refuses.

- **The minus-forty row does not match.** You added before you
  multiplied — `(celsius + FREEZING_POINT_F) * F_PER_C`:

  ```text
  Same in C and F    -40.00   -14.40   233.15
  Water freezes        0.00    57.60   273.15
  ```

  The stretch applies to the Celsius value first, and only then do you
  shift by 32.

- **Body temperature shows `98.00` instead of `98.60`.** You used `//`
  somewhere. `37 * 9 // 5 + 32` is `98`; `37 * F_PER_C + 32` is `98.6`.
  Floor division throws the fraction away before the shift ever happens,
  and the rows you would think to check are unharmed:

  ```text
  Room temperature    21.00    69.00   294.15
  Body temperature    37.00    98.00   310.15
  Water boils        100.00   212.00   373.15
  ```

- **Every kelvin value is negative.** You wrote
  `celsius + ABSOLUTE_ZERO_C`:

  ```text
  Absolute zero     -273.15  -459.67  -546.30
  Water freezes        0.00    32.00  -273.15
  ```

  A negative kelvin temperature is physically impossible, so this is the
  friendly bug of the set — it announces itself. Because the constant is
  itself negative, *subtracting* it is what moves the scale up.

- **`fahrenheit_to_celsius()` gives a wrong value that looks close.** You
  wrote `fahrenheit - FREEZING_POINT_F / F_PER_C` and left the brackets
  off. Division is worked out before subtraction, so Python computed
  `fahrenheit - 17.777...`:

  ```text
  Round-trip: 23.3 C -> 73.94 F -> 56.162222 C
  Exact match? False   Within 1e-09? False
  ```

  Notice that the table above this line is completely unharmed, because
  the table never calls the reverse function. Only the last two lines
  give it away.

- **`Exact match?` prints `True`.** You called `round()` inside
  `fahrenheit_to_celsius()`, which rounded away the tiny error the check
  exists to expose:

  ```text
  Round-trip: 23.3 C -> 73.94 F -> 23.300000 C
  Exact match? True   Within 1e-09? True
  ```

  Rounding inside `celsius_to_fahrenheit()` instead changes nothing at
  all, and it is worth knowing why: `celsius_to_fahrenheit(23.3)` already
  lands on exactly the same 64-bit value as `73.94`, so rounding it to
  two decimals rounds it to itself. The run still reads
  `Exact match? False`. The rounding only matters on the way back,
  because that is the value the comparison looks at. Either way, take the
  rounding out.

- **`NameError: name 'ABSOLUTE_ZERO_C' is not defined`.** You retyped the
  constant in lowercase inside a function, or you moved the constants
  into `main()`. Module-level constants live at the top of the file,
  outside every function, so all three converters can see them.

- **`TypeError: unsupported operand type(s) for -: 'float' and 'str'`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print(1.0 - '2')
            ~~~~^~~~~
  TypeError: unsupported operand type(s) for -: 'float' and 'str'
  ```

  Nothing in this exercise reads input, so if you see this you typed
  quotes around a number in a `table_row()` call.

- **`mypy` says `error: Missing return statement  [empty-body]`.** A
  function still has `...` where its body should be. `mypy` finds this
  without running the file at all, which is the whole argument for it in
  Lecture 3 section 7.

## Under the hood

<details>
<summary>Under the hood — why 0.1 + 0.2 is not 0.3</summary>

Write one third as a decimal and you never finish: 0.3333... The number
is perfectly real; the *notation* cannot hold it, because 3 is not a
factor of 10.

A computer has the same problem with a different set of numbers. A
`float` is stored in binary, as a sum of halves, quarters, eighths,
sixteenths and so on. Any fraction whose bottom number is a power of two
fits exactly: 0.5, 0.25, 0.75, 21.5. Everything else repeats forever and
has to be cut off. One tenth is one of the ones that repeats, so `0.1`
was never in your program in the first place. The nearest storable
neighbour was.

You can see the real value by asking the `decimal` module to print it in
full:

```text
>>> from decimal import Decimal
>>> Decimal(0.1)
Decimal('0.1000000000000000055511151231257827021181583404541015625')
>>> Decimal(0.3)
Decimal('0.299999999999999988897769753748434595763683319091796875')
```

Both are wrong by a hair, in different directions. Add the stored `0.1`
to the stored `0.2` and the two errors add up rather than cancel, and the
sum lands one step *above* the stored `0.3`:

```text
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
>>> 0.1 + 0.2 - 0.3
5.551115123125783e-17
```

Nothing is broken. Python is not being sloppy. This is the same
arithmetic your phone, your spreadsheet and every other mainstream
language do, because they all use the same 64-bit format, laid down in
the IEEE 754 standard in 1985.

There is a nice way to see the binary directly. `float.hex()` prints the
stored value in base sixteen, where each digit is four binary digits:

```text
>>> (0.1).hex()
'0x1.999999999999ap-4'
```

Read that as "1.999999999999a, times 2 to the power -4". The `9`s repeat
because one tenth repeats in binary the way one third repeats in decimal,
and the final `a` is the last group rounded up because that is where the
53 available bits ran out.

This is exactly what happens in this exercise. `23.3` is stored slightly
off. `9 / 5` is stored slightly off too:

```text
>>> Decimal(9 / 5)
Decimal('1.8000000000000000444089209850062616169452667236328125')
```

Multiply, add 32, subtract 32, divide, and each of those five steps
rounds to the nearest storable value. Sometimes the roundings cancel and
you land back where you started. At 23.3 they do not, and you land
`3.552713678800501e-15` away.

The rule that falls out of all this is short: **never compare two
computed decimals with `==`.** Ask whether the gap between them is small
enough to ignore. That is what `TOLERANCE` is for, and it is why every
serious numerical library ships a function with a name like `isclose`.
Python has one too, `math.isclose`, and once you meet modules properly it
is what you should reach for.

Integers have none of this trouble. Python's `int` is exact at any size,
so `10**100 + 1` is precisely right. If you need exact decimals — money,
usually — the `decimal` module gives you arithmetic that works in base
ten and gets `0.1 + 0.2 == 0.3` right. Both cost speed. Floats are the
fast default, and knowing when they are the wrong default is a large part
of what separates a working program from a plausible one.

</details>

<details>
<summary>Under the hood — repr, and the shortest string that round-trips</summary>

Here is a puzzle. If `0.1` is really
`0.1000000000000000055511151231257827021181583404541015625`, why does
Python print `0.1`?

```text
>>> 0.1
0.1
>>> repr(0.1)
'0.1'
```

Because `repr()` does not print the value. It prints the **shortest
string of digits that reads back as the same value**. Python asks
itself: what is the fewest digits I can write such that turning that text
back into a float gives me exactly these 64 bits? For this value the
answer is the two characters `0.1`, so that is what you see. The
guarantee is `float(repr(x)) == x`, always. That property is what "round
trips" means: text to number to text and back with nothing lost.

You can check it by hand. Feed Python the long form and it hands back the
short one, because they are the same 64 bits:

```text
>>> float('0.1000000000000000055511151231257827')
0.1
```

Python has not always done this. Up to version 2.7 it printed 17 digits
and `0.1` came out as `0.10000000000000001`, which is honest and
horrible. The shortest-round-trip algorithm gives you honest *and*
readable: the display never lies, because you can always paste it back.

Now look at `0.1 + 0.2` again. It prints `0.30000000000000004` — 17
significant digits, not two. That is not Python suddenly deciding to show
its working. It is the same rule: the sum genuinely is not the same
64-bit value as `0.3`, so the shortest text that reads back as *this*
value needs every one of those digits. The long ugly number is the honest
short answer.

This is why `repr()` is the first tool to reach for when a decimal
comparison surprises you. `print(f"{back:.6f}")` shows you `23.300000`,
which is the format spec being polite — you asked for six decimals and it
gave you six. `print(repr(back))` shows you `23.299999999999997`, which
is the number. The exercise prints `.6f` on purpose, so that the
`Exact match? False` on the next line looks like a contradiction until
you go and ask `repr()` what is really there.

One more consequence, and it catches people. `repr()` and `str()` do the
same thing for floats in Python 3, so `print(x)` and `print(repr(x))`
agree. But an f-string with a format spec does not: `f"{x}"` uses `str()`
and shows you the honest short form, while `f"{x:.2f}"` rounds for
display. Two different jobs. Use the spec when a human is reading a
table, and `repr()` when you are trying to find out what went wrong.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] All eleven lines match the Expected output character for character.
- [ ] The `Same in C and F` row reads `-40.00` in both the C and F columns.
- [ ] The `Body temperature` row reads `98.60`, not `98.00`.
- [ ] The last line reads `Exact match? False   Within 1e-09? True`, with three spaces between the two answers.
- [ ] No conversion function prints, reads input, rounds, or uses `//`.
- [ ] `mypy` reports no issues, if you have it installed.
- [ ] The file is committed to Git with a message like `Add Week 2 exercise 3: temperature converter`.

## Stretch

- Add `fahrenheit_to_kelvin()` without writing a new formula. Compose the
  two functions you already have:

  ```python
  def fahrenheit_to_kelvin(fahrenheit: float) -> float:
      """Convert a Fahrenheit temperature to kelvin by composing two conversions."""
      return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))
  ```

  There is a closed-form version — `(f - 32) * 5 / 9 + 273.15` — and
  writing it would give you a third place where the same physics is
  written down, and a third place to get it wrong. The composed version
  has one formula, borrowed twice, and it stays correct automatically if
  either underlying conversion is ever corrected.

- Add `kelvin_to_celsius()` — `return kelvin + ABSOLUTE_ZERO_C` — and use
  the tolerance check to confirm that Celsius to kelvin and back is exact
  for every row in the table:

  ```text
   -273.15  K exact True   F exact True   F within tol True
    -40.00  K exact True   F exact True   F within tol True
      0.00  K exact True   F exact True   F within tol True
     21.00  K exact True   F exact False  F within tol True
     37.00  K exact True   F exact False  F within tol True
    100.00  K exact True   F exact True   F within tol True
  ```

  The kelvin trip is one addition and its matching subtraction, so on
  these six values the second operation lands back on exactly the bit
  pattern the first started from. The Fahrenheit trip has a multiply and
  a divide as well, and each of those is another chance to be nudged onto
  a neighbouring value. Do not turn that into a rule, though. Sweep every
  one-decimal Celsius value from -100 to 100 and 1,456 of the 2,001 fail
  the kelvin round trip — more than the 471 that fail the Fahrenheit one.
  Fewer operations means fewer chances to drift, not none.

- Change `ROUND_TRIP_C` to `21.5` and rerun. `Exact match?` flips to
  `True`. Try `25.0` and `-40.0`, both exact, then `37.0` and `18.3`,
  neither of them exact. The table in The Solution has all six.

- Print `repr(back)` instead of `{back:.6f}` and look at the digits the
  format spec was hiding from you.

When your table matches, move on to
[Exercise 4 — Input Parsing](./exercise-04-input-parsing.md).
