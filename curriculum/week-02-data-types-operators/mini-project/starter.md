# Mini-Project Starter — Unit Converter CLI

> **Project:** [Mini-Project — Unit Converter CLI](./README.md)
> **Week:** 2
> **What this is:** the scaffold for the Week 2 mini-project. Copy the block
> below into a file called `unit_converter.py` in your Week 2 repository, then
> work the ten `TODO`s. The menus, the prompts and the program flow are
> already written; the arithmetic and the result lines are yours.

The plumbing is given to you on purpose. Menu handling needs branching, and
branching is Week 3. What Week 2 taught you is the part that is missing here:
arithmetic with the right precedence, casting a string to a `float` without
crashing, and formatting a number so a human can read it.

## How to use this page

1. Open a terminal in your Week 2 repository and activate the virtual
   environment. Your prompt should show `(.venv)`.

2. Create the file:

   ```bash
   mkdir -p mini-project
   touch mini-project/unit_converter.py
   ```

   On Windows PowerShell, `New-Item mini-project/unit_converter.py` does the
   same job.

3. Paste in the whole code block from the section below, unchanged.

4. Run it before you edit anything, and answer `1`, then `a`, then `100`:

   ```bash
   python mini-project/unit_converter.py
   ```

   You will get the full banner, both menus, and `Result: not built yet`. That
   is the point — the shell of the program works, so every problem from here
   on is a problem in the ten lines you are about to write.

5. Work the `TODO`s in order. TODO 1 through 6 are the conversions, TODO 7 is
   input validation, and TODO 8 through 10 are the result lines. Test the
   conversions on their own before you run the menu:

   ```bash
   python -i mini-project/unit_converter.py
   ```

   Answer the prompts, and when the program finishes you are left at a `>>>`
   prompt with your functions loaded. Call `c_to_f(0)` and `c_to_f(100)`. You
   should get `32.0` and `212.0`. Ten minutes here saves an hour later.

6. Delete each `# TODO:` comment once it is satisfied.

## The starter

```python
"""unit_converter.py — a one-shot, menu-driven unit converter.

Week 2 mini-project for Code Crunch Convos. Converts between Celsius and
Fahrenheit, kilometers and miles, and US dollars and euros. Run it with:
python unit_converter.py
"""

USD_TO_EUR: float = 0.9140
KM_PER_MILE: float = 1.609344

BANNER_RULE: str = "================================"
BANNER_TITLE: str = "   Code Crunch Unit Converter"
NOT_A_NUMBER: str = "That is not a number. Nothing converted."


def c_to_f(c: float) -> float:
    """Return the Celsius temperature c in degrees Fahrenheit."""
    # TODO 1: multiply by 9, divide by 5, then add 32.
    return 0.0


def f_to_c(f: float) -> float:
    """Return the Fahrenheit temperature f in degrees Celsius."""
    # TODO 2: subtract 32 first, then scale by 5/9. Mind the precedence.
    return 0.0


def km_to_mi(km: float) -> float:
    """Return the distance km, in kilometers, expressed in miles."""
    # TODO 3: divide by KM_PER_MILE. Never type 1.609344 inline.
    return 0.0


def mi_to_km(mi: float) -> float:
    """Return the distance mi, in miles, expressed in kilometers."""
    # TODO 4: the inverse of TODO 3.
    return 0.0


def usd_to_eur(usd: float) -> float:
    """Return the amount usd, in US dollars, converted to euros."""
    # TODO 5: multiply by USD_TO_EUR.
    return 0.0


def eur_to_usd(eur: float) -> float:
    """Return the amount eur, in euros, converted to US dollars."""
    # TODO 6: the inverse of TODO 5.
    return 0.0


def parse_float(raw: str) -> float | None:
    """Return the number in raw, or None if raw does not hold one.

    Args:
        raw: exactly what the user typed, unmodified.

    Returns:
        The parsed float, or None when raw is not a number. Returning
        None instead of raising lets the caller choose the wording of
        the complaint.
    """
    # TODO 7: try float(raw) and return it. Catch ValueError and return
    #         None. Do not print anything in here.
    return 0.0


def print_banner() -> None:
    """Print the title block and the numbered category menu."""
    print(BANNER_RULE)
    print(BANNER_TITLE)
    print(BANNER_RULE)
    print()
    print("Categories:")
    print("  1) Temperature (C / F)")
    print("  2) Distance    (km / mi)")
    print("  3) Currency    (USD / EUR)")
    print()


def read_direction(option_a: str, option_b: str) -> str:
    """Print the two directions, then return the letter the user chose."""
    print("Direction:")
    print(f"  a) {option_a}")
    print(f"  b) {option_b}")
    print()
    return input("Choose direction (a/b): ").strip().lower()


def read_value(unit: str) -> float | None:
    """Prompt once for a value in unit and return it, or None if invalid."""
    raw: str = input(f"Value in {unit}: ")
    print()
    return parse_float(raw)


def run_temperature() -> None:
    """Handle the Celsius/Fahrenheit branch, from menu to printed result."""
    direction: str = read_direction("Celsius     -> Fahrenheit",
                                    "Fahrenheit  -> Celsius")
    print()
    if direction == "a":
        value = read_value("Celsius")
        if value is None:
            print(NOT_A_NUMBER)
            return
        # TODO 8a: print   Result: 100.00 C = 212.00 F
        #          using :.2f on the input value and on c_to_f(value).
        print("Result: not built yet")
    elif direction == "b":
        value = read_value("Fahrenheit")
        if value is None:
            print(NOT_A_NUMBER)
            return
        # TODO 8b: the same shape with the units the other way round.
        print("Result: not built yet")
    else:
        print(f"{direction!r} is not a or b. Nothing converted.")


def run_distance() -> None:
    """Handle the kilometers/miles branch, from menu to printed result."""
    direction: str = read_direction("Kilometers -> Miles",
                                    "Miles      -> Kilometers")
    print()
    if direction == "a":
        value = read_value("kilometers")
        if value is None:
            print(NOT_A_NUMBER)
            return
        # TODO 9a: print   Result: 42.00 km = 26.10 mi
        print("Result: not built yet")
    elif direction == "b":
        value = read_value("miles")
        if value is None:
            print(NOT_A_NUMBER)
            return
        # TODO 9b: print   Result: 26.20 mi = 42.16 km
        print("Result: not built yet")
    else:
        print(f"{direction!r} is not a or b. Nothing converted.")


def run_currency() -> None:
    """Handle the USD/EUR branch, from menu to printed result."""
    direction: str = read_direction("USD -> EUR", "EUR -> USD")
    print()
    if direction == "a":
        value = read_value("USD")
        if value is None:
            print(NOT_A_NUMBER)
            return
        # TODO 10a: print
        #   Result: $250.00 USD = €228.50 EUR  (rate: 1 USD = 0.9140 EUR)
        #   Use :,.2f on the money and :.4f on the rate. Two spaces
        #   before the opening parenthesis.
        print("Result: not built yet")
    elif direction == "b":
        value = read_value("EUR")
        if value is None:
            print(NOT_A_NUMBER)
            return
        # TODO 10b: the same line the other way round. The rate note stays
        #           written as 1 USD = ... EUR either way.
        print("Result: not built yet")
    else:
        print(f"{direction!r} is not a or b. Nothing converted.")


def main() -> None:
    """Show the menu, run one conversion, and say goodbye."""
    print_banner()
    category: str = input("Pick a category (1-3): ").strip()
    print()

    if category == "1":
        run_temperature()
    elif category == "2":
        run_distance()
    elif category == "3":
        run_currency()
    else:
        print(f"{category!r} is not 1, 2, or 3. Nothing converted.")

    print()
    print("Thanks for using the converter!")


if __name__ == "__main__":
    main()
```

## What each TODO is asking for

- **TODO 1 — `c_to_f`.** The formula is nine fifths of the Celsius value plus
  thirty-two. Write it so the multiplication and division both happen before
  the addition. `c * 9 / 5 + 32` already does, because `*` and `/` bind tighter
  than `+`; Lecture 2 section 2 has the full table. Check it with the two
  anchors everybody knows: 0 goes to 32, 100 goes to 212.
- **TODO 2 — `f_to_c`.** The inverse, and the one people get wrong. Subtract
  thirty-two *first*, then scale. That means the subtraction needs
  parentheses, because without them Python scales before it subtracts and you
  get a plausible-looking wrong answer. 98.6 must come back as 37.0.
- **TODO 3 — `km_to_mi`.** One mile is `KM_PER_MILE` kilometers, so going from
  kilometers to miles divides. Use the constant, not the literal. If the value
  ever needs correcting you want to fix it in one place, and a named constant
  also tells the next reader what the number is.
- **TODO 4 — `mi_to_km`.** Multiply by the same constant. A useful sanity
  check: `km_to_mi(mi_to_km(5))` should come back as `5.0`, give or take the
  last decimal place.
- **TODO 5 — `usd_to_eur`.** Multiply by `USD_TO_EUR`. That is the whole
  function, and writing it as a function anyway is what lets the rate live in
  exactly one place.
- **TODO 6 — `eur_to_usd`.** Divide by the same rate. Do not add a second
  constant for the reverse direction — two constants can disagree with each
  other, and eventually they will.
- **TODO 7 — `parse_float`.** The exact shape from Lecture 3 section 3: `try`
  the cast, `return` it on success, `except ValueError` and return `None`.
  Catch `ValueError` by name rather than writing a bare `except`, so that a
  user pressing Ctrl+C is not mistaken for a typo. This function must not
  print — its only job is to answer "is this a number, and if so which one".
- **TODO 8a and 8b — the temperature result lines.** One f-string each, two
  `:.2f` placeholders in each. The value the user typed goes on the left of
  the `=`, the converted value on the right, and each carries its unit letter.
- **TODO 9a and 9b — the distance result lines.** Same shape, `km` and `mi`
  as the labels. Distance uses two decimals too, even though nobody measures
  a road that precisely — a consistent format is easier to read down a column
  than a clever one.
- **TODO 10a and 10b — the currency result lines.** These carry three things:
  the amount with a thousands separator (`:,.2f`, so 1250 prints as
  `1,250.00`), the currency symbol in front of it, and the rate in
  parentheses at four decimals. Printing the rate you used is not decoration.
  It is the difference between a number a person can check and a number they
  have to trust.

## Expected output when you are done

A temperature session:

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

A currency session:

```text
$ python unit_converter.py
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

And the four other paths, trimmed to their result lines so you can check your
arithmetic without running six full sessions:

```text
Value in Fahrenheit: 98.6
Result: 98.60 F = 37.00 C

Value in kilometers: 42
Result: 42.00 km = 26.10 mi

Value in miles: 26.2
Result: 26.20 mi = 42.16 km

Value in EUR: 100
Result: €100.00 EUR = $109.41 USD  (rate: 1 USD = 0.9140 EUR)
```

Bad input, and a category that does not exist:

```text
Value in USD: banana

That is not a number. Nothing converted.

Thanks for using the converter!
```

```text
Pick a category (1-3): 9

'9' is not 1, 2, or 3. Nothing converted.

Thanks for using the converter!
```

Note that the program still says goodbye in both failure cases. Exiting
cleanly on bad input is a requirement, not a nicety — a program that vanishes
mid-sentence leaves the user unsure whether anything happened.

## Common bugs to catch

- **`ValueError: could not convert string to float: 'banana'`.** TODO 7 is
  still a placeholder, so the cast is running unprotected somewhere. Put the
  `float(raw)` call inside the `try` block, and make sure the `except
  ValueError:` line lines up with the `try:` above it.
- **`98.6 F = 54.78 C` instead of `37.00 C`.** Missing parentheses in
  `f_to_c`. You wrote `f - 32 * 5 / 9`, which multiplies before it subtracts.
  It has to be `(f - 32) * 5 / 9`.
- **`TypeError: unsupported format string passed to NoneType.__format__`.**
  You applied `:.2f` to the result of `read_value()` without checking it for
  `None` first, or you deleted the `if value is None:` guard. The guard has to
  come before the formatting, not after.
- **`Result: 26.0975... mi` with fifteen decimals.** You left the `:.2f` off
  one of the placeholders. `{value}` prints the float in full; `{value:.2f}`
  rounds it for display only and leaves the stored number untouched.
- **`Result: $250 USD` with no cents.** You used `:,d` or no format spec at
  all. Money always shows two decimals, even when they are zeros, because a
  column of prices that sometimes has cents and sometimes does not is
  unreadable.
- **`UnicodeEncodeError: 'charmap' codec can't encode character '€'`.**
  Your Windows console is on a code page that has no euro sign. Run
  `chcp 65001` in that terminal first, or set `PYTHONIOENCODING=utf-8`. Your
  code is fine; the terminal is the problem.
- **`NameError: name 'value' is not defined`.** You moved the result line
  above the `value = read_value(...)` line while editing. Python reads a
  function body top to bottom; a name has to be bound before it is used.

## When you are done

The rubric in the mini-project README is worth forty points. These are the
same criteria, phrased as things you can check.

- [ ] All six conversion functions return the right numbers — verify 0 C, 100
      C, 98.6 F, 42 km, 26.2 mi, 250 USD, and 100 EUR against the block above.
- [ ] Every function has type hints and a docstring, and no `TODO` comments
      remain.
- [ ] The banner and both menus match the layout in the project README.
- [ ] Category, direction, and value all come from `input()`.
- [ ] A non-numeric value prints the error and exits without a traceback.
- [ ] Every number is formatted to two decimals with the right unit label, and
      money carries a thousands separator.
- [ ] `USD_TO_EUR` and `KM_PER_MILE` are module-level constants, used
      everywhere, typed nowhere as literals.
- [ ] The flow lives in `main()` behind `if __name__ == "__main__":`.
- [ ] Names are `snake_case` and lines stay under 80 characters.
- [ ] Saved as `mini-project/unit_converter.py`, then committed and pushed:

      ```bash
      git add mini-project/unit_converter.py
      git commit -m "Week 2 mini-project: unit converter CLI"
      git push
      ```

Link it from your repository README and add a screenshot of one session. A
picture of the thing running is worth more to a reader than the source is.
