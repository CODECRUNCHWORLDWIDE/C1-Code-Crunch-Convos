# Homework Problem 1 — Temperature Module

> **Topic:** writing three small functions in one file, giving each a docstring and type hints, and guarding the file's print with `if __name__ == "__main__":`
> **Lecture:** [Lecture Note 1 — Defining Functions](../lecture-notes/01-defining-functions.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** this is the first file you write that is meant to be *used by other files*. That changes one thing and it changes it completely: the file is no longer allowed to shout when somebody imports it. Everything in Week 4 about modules starts from that single rule, and this is the smallest problem that teaches it.

## The Brief

A **module** is a plain `.py` file that other Python files can borrow
things from. That is the whole definition. Nothing special goes at the
top, nothing special goes at the bottom. If you write a file called
`temperature.py` that has a function called `c_to_f` in it, any other
file sitting beside it can say `from temperature import c_to_f` and use
it.

You are building that file.

Three temperatures, three names for the same heat:

- **Celsius** is what most of the world uses for weather. Water freezes
  at 0 and boils at 100.
- **Fahrenheit** is what the United States uses. Water freezes at 32 and
  boils at 212.
- **Kelvin** is what scientists use. It starts at the coldest anything
  can possibly get, which is `-273.15` degrees Celsius. There is no
  colder. Kelvin has no negative numbers because there is nothing below
  the bottom.

Your module holds one function per conversion:

| Function | Turns | Into | Formula |
|----------|-------|------|---------|
| `c_to_f` | Celsius | Fahrenheit | `c * 9 / 5 + 32` |
| `f_to_c` | Fahrenheit | Celsius | `(f - 32) * 5 / 9` |
| `c_to_k` | Celsius | Kelvin | `c + 273.15` |

`c_to_k` has one extra job. If somebody hands it a temperature below
absolute zero, it must refuse — not print a complaint, not return zero,
but **raise `ValueError`**. Raising is how a function says "the thing you
asked for does not exist" in a way the caller cannot accidentally ignore.

Then, at the bottom of the file and only when the file is run directly,
print a small table:

```text
   C       F        K
---------------------
   0    32.00   273.15
 100   212.00   373.15
 -40   -40.00   233.15
```

The `-40` row is not decoration. Minus forty is the one temperature where
Celsius and Fahrenheit agree, which makes it the best row in the table
for catching a formula you typed backwards.

## Starter

Save this as `temperature.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it just gets Fahrenheit and Kelvin wrong on
purpose:

```python
"""Temperature conversions between Celsius, Fahrenheit and Kelvin."""

ABSOLUTE_ZERO_C: float = -273.15

HEADER: str = "   C       F        K"
RULE: str = "---------------------"
SAMPLE_CELSIUS: list[int] = [0, 100, -40]


def c_to_f(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        The same temperature in degrees Fahrenheit.

    Example:
        >>> c_to_f(100)
        212.0
    """
    return 0.0  # TODO: celsius * 9 / 5 + 32


def f_to_c(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius."""
    return 0.0  # TODO: (fahrenheit - 32) * 5 / 9


def c_to_k(celsius: float) -> float:
    """Convert a Celsius temperature to Kelvin."""
    # TODO: raise ValueError when celsius is below ABSOLUTE_ZERO_C
    return 0.0  # TODO: celsius + 273.15


def _table() -> str:
    """Return the sample conversion table as one multi-line string."""
    rows = [HEADER, RULE]
    for celsius in SAMPLE_CELSIUS:
        rows.append(f"{celsius:>4}{c_to_f(celsius):>9.2f}{c_to_k(celsius):>9.2f}")
    return "\n".join(rows)


if __name__ == "__main__":
    print(_table())
```

The row-building line and the `__main__` guard are given to you complete,
because the problem is the three functions. Read them anyway. You write
both from scratch in problem 6.

`f_to_c` and `c_to_k` are missing most of their docstrings. Writing those
is part of the work, and the grading guide charges you a point for each
one you skip.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/homework/problem-01-temperature-module.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `c_to_f`, `f_to_c` and `c_to_k` each take one number and **return** a
   number. None of them prints anything.
2. Every one of the three has type hints on its parameter and on its
   return, and a docstring with an `Args:`, a `Returns:` and an
   `Example:` section.
3. `c_to_k` raises `ValueError` when its argument is below `-273.15`.
   Exactly `-273.15` is allowed and gives `0.0`.
4. Running `python temperature.py` prints the table from The Brief,
   character for character.
5. Importing the module prints nothing at all.

## Constraints

- **The three functions return; they do not print.** A function that
  prints can only ever be watched. A function that returns can be added
  to something, formatted, put in a table, or tested. `_table` is the one
  place a value turns into text, and `print` appears exactly once in the
  whole file.
- **`ABSOLUTE_ZERO_C` is a named constant, not the number `-273.15`
  typed in three places.** The moment a magic number appears twice, one
  of the two copies is going to be wrong later and nobody will notice
  which.
- **The guard is `<`, not `<=`.** Absolute zero is a real, reachable
  temperature — it converts to `0.0 K`. Only *below* it is impossible.
  Getting a boundary right is the entire skill that a validation rule
  teaches.
- **The table prints only under `if __name__ == "__main__":`.** This is
  the rule the whole problem exists for. Without the guard, any file that
  imports your module gets the table dumped into its own output, and it
  will take you an hour to work out where those five lines came from.

## Expected output

```text
$ python problem-01-temperature-module.py
   C       F        K
---------------------
   0    32.00   273.15
 100   212.00   373.15
 -40   -40.00   233.15
```

Two more runs worth doing, because they check the boundary that the table
never touches. Absolute zero itself is legal:

```bash
python -c "from temperature import c_to_k; print(c_to_k(-273.15))"
```

```text
0.0
```

One step below it is not, and the refusal is loud:

```bash
python -c "from temperature import c_to_k; c_to_k(-300)"
```

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from temperature import c_to_k; c_to_k(-300)
                                    ~~~~~~^^^^^^
  File "...\homework\temperature.py", line 71, in c_to_k
    raise ValueError(f"{celsius} C is below absolute zero ({ABSOLUTE_ZERO_C} C)")
ValueError: -300 C is below absolute zero (-273.15 C)
```

And the `Example:` blocks in the docstrings are real, runnable tests:

```bash
python -m doctest temperature.py -v
```

The last three lines:

```text
3 tests in 5 items.
3 passed.
Test passed.
```

## Steps

1. Activate your Week 4 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `temperature.py`. Run it. Every number is `0.00`,
   which is wrong in a way you can see.
3. Fill in `c_to_f`. Run it again. The Fahrenheit column should now read
   `32.00`, `212.00`, `-40.00`.
4. Fill in `c_to_k`, arithmetic first, guard second. Run it. The table is
   complete.
5. Fill in `f_to_c`. Nothing in the table uses it, so check it by hand:
   `python -c "from temperature import f_to_c; print(f_to_c(212))"`
   should print `100.0`.
6. Add the `ValueError` guard to `c_to_k` and try `c_to_k(-300)`. You
   want a traceback here. A traceback you asked for is a feature.
7. Finish the two thin docstrings. Give each an `Args:`, a `Returns:`
   and an `Example:`.
8. Run `python -m doctest temperature.py -v` and read the last three
   lines.
9. Prove the guard works: `python -c "import temperature"` must print
   nothing.
10. Compare against **The Solution**, tick the acceptance checklist, and
    commit: `git add homework/temperature.py` then
    `git commit -m "Week 4 homework: temperature module"`.

## The Solution

```python
"""Temperature conversions between Celsius, Fahrenheit and Kelvin.

Week 4 homework, problem 1, Code Crunch Convos.

This file is a module. A module is just a ``.py`` file that other ``.py``
files are allowed to import. Save your own copy as ``temperature.py`` in
your ``homework/`` folder, because that is the name the import line will
use: ``from temperature import c_to_f``.

Run this file and it prints the sample table. Import it and it prints
nothing, because the printing sits under the ``__main__`` guard at the
bottom.
"""

ABSOLUTE_ZERO_C: float = -273.15

HEADER: str = "   C       F        K"
RULE: str = "---------------------"
SAMPLE_CELSIUS: list[int] = [0, 100, -40]


def c_to_f(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        The same temperature in degrees Fahrenheit.

    Example:
        >>> c_to_f(100)
        212.0
    """
    return celsius * 9 / 5 + 32


def f_to_c(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius.

    Args:
        fahrenheit: Temperature in degrees Fahrenheit.

    Returns:
        The same temperature in degrees Celsius.

    Example:
        >>> f_to_c(212)
        100.0
    """
    return (fahrenheit - 32) * 5 / 9


def c_to_k(celsius: float) -> float:
    """Convert a Celsius temperature to Kelvin.

    Args:
        celsius: Temperature in degrees Celsius, at or above absolute zero.

    Returns:
        The same temperature in kelvin.

    Raises:
        ValueError: If `celsius` is below absolute zero (-273.15 C).

    Example:
        >>> c_to_k(0)
        273.15
    """
    if celsius < ABSOLUTE_ZERO_C:
        raise ValueError(f"{celsius} C is below absolute zero ({ABSOLUTE_ZERO_C} C)")
    return celsius + 273.15


def _table() -> str:
    """Return the sample conversion table as one multi-line string."""
    rows = [HEADER, RULE]
    for celsius in SAMPLE_CELSIUS:
        rows.append(f"{celsius:>4}{c_to_f(celsius):>9.2f}{c_to_k(celsius):>9.2f}")
    return "\n".join(rows)


if __name__ == "__main__":
    print(_table())
```

**Why it works.**

**The row format `{:>4}{:>9.2f}{:>9.2f}` is measured, not guessed.** Copy
the brief's table into a text editor and count characters. Each data row
is 22 characters wide: the Celsius number ends at column 4, Fahrenheit at
column 13, Kelvin at column 22. Three right-aligned fields of width 4, 9
and 9 put every digit exactly where the brief puts it. Inside the braces,
`>` means "push it to the right", the number is the total width including
padding, and `.2f` means "two digits after the point, always". Build the
row with `+` and hand-typed spaces instead and one of the three rows will
be off, because `-40` and `212.00` are different lengths and manual
padding does not adapt.

**The header and the rule are copied out as strings on purpose.** Here is
a real wrinkle in the brief: its header line is 21 characters and its data
rows are 22, so the `F` and the `K` each sit one column to the *left* of
the numbers underneath them. Matching the brief exactly means copying
those two lines verbatim rather than generating them from the same widths
as the rows. That is what `HEADER` and `RULE` are for. If you would rather
have a table that genuinely lines up, write

```python
HEADER = f"{'C':>4}{'F':>9}{'K':>9}"
RULE = "-" * 22
```

and say in a comment that you did. Either choice is defensible. Quietly
producing a third alignment that matches neither is not.

**`c_to_k` checks before it computes.** The comparison is `<`, not `<=`,
so `-273.15` itself passes and returns `0.0`. The error message names the
value it rejected *and* the limit it broke, so the person reading the
traceback does not have to go and look up what absolute zero is.

**`_table()` returns a string and the guard prints it.** The function is
pure — same input, same output, no side effects — so it can be tested by
comparing its return value to text. The one side effect in the file lives
in the two lines that only run when you execute the file directly. The
leading underscore on the name is Python's convention for "this is
private, other modules should not import it".

**The `Example:` blocks use 100 and 212, not -40.** A doctest compares
printed text exactly, and `-40 + 273.15` is not `233.15` in binary
floating point:

```text
>>> -40 + 273.15
233.14999999999998
```

`233.15` is what `.2f` *prints*; it is not what the float *is*. A doctest
written as `c_to_k(-40)` giving `233.15` would fail. Pick examples whose
values land exactly, or format them inside the example.

**Another file can now use this one.** Put a second file beside
`temperature.py` and the module is a module:

```python
"""weather.py - uses the sibling temperature module."""

from temperature import c_to_f

print(f"25 C is {c_to_f(25):.1f} F")
```

```bash
python weather.py
```

```text
25 C is 77.0 F
```

Notice what did *not* happen: the conversion table did not appear. That is
the `__main__` guard earning its place. Problem 6 builds the two-file
version of this idea from scratch.

## Download and run

Download [problem-01-temperature-module-solution.py](./problem-01-temperature-module-solution.py)
and run it:

```bash
python problem-01-temperature-module-solution.py
```

That file *is* the module, under a longer name so it cannot land on top
of your own work. Save your copy as `temperature.py` — the import line
`from temperature import c_to_f` looks the module up by filename, so the
name is part of the answer.

## Common bugs to catch

- **Floor division instead of true division.**

  ```python
  return celsius * 9 // 5 + 32     # WRONG
  ```

  `//` throws away the fractional part. `c_to_f(37)` gives `98` instead
  of `98.6`, and the `-40` row quietly becomes `-41.0`. No error, just
  wrong numbers.
- **Rewriting the formula with your own parentheses.**
  `celsius * 9 / (5 + 32)` is not the formula. Python reads
  `celsius * 9 / 5 + 32` as `((celsius * 9) / 5) + 32`, which is what the
  table wants. Type the formula the way the brief writes it and leave it
  alone.
- **Printing inside `c_to_f` instead of returning.**

  ```python
  def c_to_f(celsius: float) -> float:
      print(celsius * 9 / 5 + 32)     # WRONG: this returns None
  ```

  The annotation promises a `float` and the function hands back `None`.
  The table then dies in the format spec:

  ```text
  TypeError: unsupported format string passed to NoneType.__format__
  ```
- **Printing a complaint instead of raising.**

  ```python
  if celsius < -273.15:
      print("too cold")               # WRONG: the caller cannot see this
      return 0.0
  ```

  Now a caller has no way to tell a genuine `0.0 K` from a failure. The
  brief asks for `ValueError` because that is Python's standard way of
  saying "right type, impossible value".
- **The table at the top level, with no guard.** Drop the
  `if __name__ == "__main__":` line and un-indent the `print`, then run
  the `weather.py` snippet above. The conversion table appears before
  your own first line of output, as a side effect of the import. That is
  precisely the bug the guard exists to prevent.
- **Naming the file something the standard library already uses.** Do not
  call it `math.py`. Your file would shadow Python's own `math` for every
  file in that folder, and the breakage looks unrelated to anything you
  did. `temperature.py` is safe.

## Under the hood

<details>
<summary>Under the hood — parameters and arguments are two different things</summary>

These two words get used as if they meant the same thing. They do not,
and once you see the difference the error messages start making sense.

A **parameter** is the name in the `def` line. It is a label the function
uses for something it has not been given yet.

```python
def c_to_f(celsius: float) -> float:
    ...
```

`celsius` is a parameter. It exists only inside `c_to_f`, and it exists
whether or not anybody ever calls the function.

An **argument** is the actual value at the call site.

```python
c_to_f(100)
```

`100` is an argument. Calling the function binds the argument to the
parameter for the length of that one call, and then the binding is gone.

The slogan: **parameters are in the definition, arguments are in the
call.** A recipe has a parameter that says "flour". The bag on your
counter is the argument.

Why it matters: Python's error messages use these words precisely, and
they will tell you exactly which side of the line you are on.

```bash
python -c "from temperature import c_to_f; c_to_f()"
```

```text
TypeError: c_to_f() missing 1 required positional argument: 'celsius'
```

Read it carefully. It says *argument* missing, and then it names the
*parameter* that has nothing bound to it. It is not complaining about the
`def` line. It is complaining that the call did not supply a value.

Compare with the other direction:

```bash
python -c "from temperature import c_to_f; c_to_f(1, 2)"
```

```text
TypeError: c_to_f() takes 1 positional argument but 2 were given
```

Same distinction, other way round. "Takes 1" is about the parameters,
"2 were given" is about the arguments.

One more piece of vocabulary that hangs off this. An argument can be
passed **positionally** — `c_to_f(100)`, matched by order — or by
**keyword** — `c_to_f(celsius=100)`, matched by name. Both bind the same
argument to the same parameter. The keyword form costs more typing and
buys readability, which is a good trade when a function takes several
numbers and a reader cannot guess which is which.
[Lecture Note 1 §6](../lecture-notes/01-defining-functions.md) has the
ordering rules.

</details>

<details>
<summary>Under the hood — why 0.1 + 0.2 is not 0.3, and what that costs this table</summary>

Computers store fractions in binary — halves, quarters, eighths,
sixteenths. Any fraction that is not a sum of those cannot be stored
exactly, in the same way that one third cannot be written exactly in
decimal however many 3s you type after the point.

`0.1` is one of those. So is `273.15`. So the arithmetic goes slightly
sideways:

```text
>>> 0.1 + 0.2
0.30000000000000004
>>> -40 + 273.15
233.14999999999998
```

Nothing is broken. The nearest storable number to `233.15` is
`233.14999999999998`, and Python is showing you the truth rather than
politely rounding it away.

This costs the table nothing, because `.2f` rounds for display and
`233.14999999999998` rounds to `233.15`. It costs a doctest everything,
because a doctest compares text and those two strings differ.

The rules that follow from this, and they are worth carrying for the rest
of your programming life:

- **Never compare floats with `==`.** `0.1 + 0.2 == 0.3` is `False`.
  Compare with a tolerance instead: `abs(a - b) < 1e-9`, or use
  `math.isclose(a, b)` from the standard library.
- **Round at the edge, not in the middle.** Do the arithmetic in full
  precision and format only when the number becomes text, which is
  exactly what `_table` does.
- **Money is not a float.** Use `decimal.Decimal` or count whole cents as
  integers. Half a cent lost per transaction is a real bug that real
  companies have shipped.

If you want to see the exact value Python is holding, ask for more digits
than a float has:

```bash
python -c "print(f'{-40 + 273.15:.20f}')"
```

```text
233.14999999999997726263
```

That is the number. `233.15` was always the polite summary.

</details>

## Acceptance checklist

- [ ] `python temperature.py` prints the brief's table, character for
      character, including the `-40` row.
- [ ] `python -c "import temperature"` prints nothing.
- [ ] `c_to_f(100)` returns `212.0` and `f_to_c(212)` returns `100.0`.
- [ ] `c_to_k(-273.15)` returns `0.0`.
- [ ] `c_to_k(-300)` raises `ValueError` with a message naming both the
      value and the limit.
- [ ] All three functions have hints on the parameter and the return.
- [ ] All three have a docstring with `Args:`, `Returns:` and
      `Example:`, and `c_to_k` also has `Raises:`.
- [ ] `python -m doctest temperature.py -v` ends with `Test passed.`
- [ ] `-273.15` appears once, as `ABSOLUTE_ZERO_C`.
- [ ] Committed with a message like
      `Week 4 homework: temperature module`.

## Stretch

- **Add `k_to_c` and `f_to_k`.** Write `f_to_k` by calling the two
  functions you already have — `c_to_k(f_to_c(fahrenheit))` — rather than
  deriving a fourth formula. Building new functions out of old ones is
  the whole reason functions exist, and there is nothing to get wrong in
  a line that has no arithmetic in it.
- **Make the table a parameter instead of a constant.** Change `_table`
  to `_table(temperatures: list[float]) -> str` and pass
  `SAMPLE_CELSIUS` from the `__main__` block. Now the same function can
  print any set of rows, and the constant is data the caller chooses
  rather than something buried in the function.
- **Round-trip test every degree from -100 to 100.** For each one, check
  that `f_to_c(c_to_f(c))` comes back to where it started. It will not,
  exactly — the floating-point block above says why — so compare with
  `math.isclose` and watch the first pair that would have failed a plain
  `==`.
- **Guard `f_to_c` too.** Absolute zero is `-459.67 F`. Add the same
  refusal, expressed with a second named constant, and make the two
  error messages read the same shape so they are recognisable when they
  appear.
- **Print the table with aligned headings.** Use the two lines under "Why
  it works" that generate `HEADER` and `RULE` from the field widths.
  Change one width and watch the whole table stay square, which is the
  point of not typing spaces by hand.

Next: [Homework Problem 2 — Password Strength](./problem-02-password-strength.md).
