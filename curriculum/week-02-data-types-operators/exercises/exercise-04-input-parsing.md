# Exercise 4 — Input Parsing

> **Topic:** `input()`, casting, and error handling
> **Lecture:** [03 — Reading Input and Type Hints](../lecture-notes/03-input-and-type-hints.md)
> **Difficulty:** Medium
> **Target time:** 30 minutes
> **Why this one:** `input()` always hands you back text, never a number, and the moment you forget that your program either falls over or — worse — glues two numbers together instead of adding them and gives you a wrong answer that looks fine. This exercise also produces the `read_int()` helper that Friday's mini-project reuses unchanged, so the half hour you spend here comes straight off Friday's clock. Beyond that, it is the first time you make a program survive something a person did wrong instead of crashing at them.

## The Brief

You are building an arithmetic inspector: a small tool that takes two
whole numbers and prints every arithmetic operator from Lecture 2 applied
to them. Addition through exponentiation, all seven.

The arithmetic is the easy half. The half that takes real thought is
everything a person might type that is not a number. `banana`. An empty
line. `12.0`, which looks like a number and is not a *whole* one. A minus
sign on its own. Your program has to say something useful and ask again,
rather than fall over.

There is one more hazard, and it is not a typing problem at all: division
by zero. `12 / 0` raises `ZeroDivisionError` no matter how carefully you
read the input, because zero is a perfectly good whole number. Three of
your seven operators have to handle it. The other four do not — and
`12 ** 0` is `1`, not an error, which is the kind of detail worth
checking rather than assuming.

## Starter

Create `exercise-04-input-parsing.py` and fill the two `TODO`s:

```python
"""exercise-04-input-parsing.py — read two whole numbers and inspect them.

Week 2, Exercise 4. Practises input(), casting, and recovering from bad
input. The read_int() helper here is reused by the Week 2 mini-project.

Three ways to hand this program its two numbers:

    python exercise-04-input-parsing.py --ask   asks you to type them
    python exercise-04-input-parsing.py 12 0    takes them from the command line
    python exercise-04-input-parsing.py         uses the sample pair below

The sample pair is the default so that a run with nobody at the keyboard
prints the same seven lines every time instead of waiting for typing that
is never coming.
"""

import sys

ASK_FLAG: str = "--ask"
PROMPT_FIRST: str = "First whole number: "
PROMPT_SECOND: str = "Second whole number: "
UNDEFINED: str = "undefined (division by zero)"

SAMPLE_FIRST: int = 17
SAMPLE_SECOND: int = 5
SAMPLE_NOTE: str = (
    f"Using the sample pair {SAMPLE_FIRST} and {SAMPLE_SECOND}. "
    f"Pass two numbers, or {ASK_FLAG}, to choose your own."
)


def parse_int(raw: str) -> int | None:
    """Return the whole number in raw, or None if there isn't one.

    Args:
        raw: exactly what the user typed, unmodified.

    Returns:
        The parsed integer, or None if raw is not a whole number.
        Returning None rather than raising lets the caller decide what
        to do about it.
    """
    # TODO: try int(raw) and return it. Catch ValueError and return None.
    #       Do not print anything here — this function only parses.
    ...


def read_int(prompt: str) -> int:
    """Prompt the user until they type a whole number, then return it.

    Args:
        prompt: the text shown before the cursor.

    Returns:
        The whole number the user eventually typed.
    """
    while True:
        raw: str = input(prompt)
        value: int | None = parse_int(raw)
        if value is not None:
            return value
        print(f"  {raw!r} is not a whole number. Try again.")


def describe(a: int, b: int) -> None:
    """Print every arithmetic operator from Lecture 2 applied to a and b."""
    print(f"{a} + {b}  = {a + b}")
    print(f"{a} - {b}  = {a - b}")
    print(f"{a} * {b}  = {a * b}")
    # TODO: print the / , // and % lines. If b is zero, print UNDEFINED
    #       as the result instead of letting ZeroDivisionError escape.
    #       Keep the '=' signs in the same column as the lines above.
    print(f"{a} ** {b} = {a ** b}")


def numbers_from_argv() -> tuple[int, int] | None:
    """Return the pair typed after the filename, or None if there isn't one."""
    if len(sys.argv) != 3:
        return None
    first: int | None = parse_int(sys.argv[1])
    second: int | None = parse_int(sys.argv[2])
    if first is None or second is None:
        return None
    return first, second


def choose_numbers() -> tuple[int, int]:
    """Return the pair to describe: keyboard, command line, or samples."""
    if ASK_FLAG in sys.argv[1:]:
        try:
            return read_int(PROMPT_FIRST), read_int(PROMPT_SECOND)
        except EOFError:
            print("\nNo input. Using the sample pair.", file=sys.stderr)
            return SAMPLE_FIRST, SAMPLE_SECOND
    from_argv: tuple[int, int] | None = numbers_from_argv()
    if from_argv is not None:
        return from_argv
    print(SAMPLE_NOTE, file=sys.stderr)
    return SAMPLE_FIRST, SAMPLE_SECOND


def main() -> None:
    """Describe whichever pair of whole numbers this run was handed."""
    a, b = choose_numbers()
    describe(a, b)


if __name__ == "__main__":
    main()
```

You write `parse_int()` and the three missing lines of `describe()`.
Everything else is handed to you finished. Read `read_int()` before you
write anything — it is the shape from Lecture 3 section 8. Loop forever,
ask, try to make sense of the answer, return the moment you succeed.

Notice that it checks `if value is not None`, not `if value:`. Lecture 1
section 7.4 explains why that difference matters, and one of the bugs
below is what happens when you get it wrong.

`sys.argv` is the list of words you typed on the command line.
`sys.argv[0]` is the filename itself, so two numbers after it land in
`sys.argv[1]` and `sys.argv[2]`. That is why `numbers_from_argv()` checks
for a length of exactly three.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/exercises/exercise-04-input-parsing.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `parse_int()` returns an `int` when `raw` holds a whole number, and
   `None` otherwise. It never prints and never raises.
2. `read_int()` keeps prompting until it gets a valid number. Do not
   modify it.
3. `describe()` prints exactly seven lines, one per operator, in the
   order `+ - * / // % **`.
4. When `b` is zero, the `/`, `//` and `%` lines print the value of
   `UNDEFINED` as their result instead of raising. The `**` line still
   prints its real answer, because `a ** 0` is `1`.
5. All seven `=` signs line up in the same column. The one-character
   operators get two spaces before the `=`; `//` and `**` get one.
6. The message for bad input is exactly
   `  {raw!r} is not a whole number. Try again.` — two leading spaces,
   and `!r` so the person can see stray whitespace in what they typed.
7. Keep every type hint, including `int | None` on `parse_int()`.
8. Do not modify `numbers_from_argv()`, `choose_numbers()` or `main()`.

## Constraints

- **The shipped file does not ask for input unless you ask it to, and
  that is deliberate.** A program that waits at a prompt cannot be run
  automatically — by the course's own checker, by a build server, or by
  anybody who just wants to see what it does. So the default is the
  sample pair, `--ask` turns the conversation on, and two numbers on the
  command line skip the conversation while still letting you try any
  input you like. `read_int()` and `input()` are still there, still doing
  the real work, still exactly what the mini-project reuses on Friday.
  This is a habit worth stealing: **make the interactive path opt-in.**
- **Catch `ValueError` by name, not with a bare `except:`.** A bare
  `except` also swallows `KeyboardInterrupt`, which means somebody
  pressing Ctrl+C at the prompt gets treated as a typo and asked again.
  Their only escape is to kill the terminal. It would also swallow
  `SystemExit` and any genuine mistake inside the `try` block. Catch the
  failure you predicted and let everything else through.
- **Return `None` from `parse_int()` instead of printing there.** A
  function that both reads a number and complains about a bad one can
  only ever be used by a program that wants to complain in that exact
  wording, to a terminal. Keeping the parsing pure is what lets the
  mini-project reuse this function on Friday with a different message —
  and what lets `numbers_from_argv()` reuse it right here with no message
  at all.
- **Guard division with `if b == 0`, not with a second `try` / `except`.**
  Both work. The guard is better here because division by zero is not a
  surprise in this program. It is an ordinary input you fully expect and
  have a defined answer for. Save exceptions for the case you could not
  see coming, which is exactly why the *parsing* uses one.
- **Do not call `.strip()` on the input before parsing.** Try it in the
  REPL: `int(" 12 ")` returns `12`. `int()` already tolerates spaces
  around the number, so the strip is a line that does nothing while
  implying it is load-bearing. It also would not fix the case you
  actually care about, `"12.0"`, which fails with or without whitespace.
- **Use `is not None`, never a truthiness check.** `if value:` treats a
  perfectly valid `0` as a failure and asks the person to type it again,
  forever. Lecture 1 section 7.4 lists `0` among the falsy values; this
  is the exercise where that list earns its keep.

## Expected output

This is the real output of the finished file with no arguments, captured
on CPython 3.13.2:

```text
$ python exercise-04-input-parsing.py
17 + 5  = 22
17 - 5  = 12
17 * 5  = 85
17 / 5  = 3.4
17 // 5 = 3
17 % 5  = 2
17 ** 5 = 1419857
```

In your terminal you also see one more line, before those seven:

```text
$ python exercise-04-input-parsing.py
Using the sample pair 17 and 5. Pass two numbers, or --ask, to choose your own.
17 + 5  = 22
17 - 5  = 12
17 * 5  = 85
17 / 5  = 3.4
17 // 5 = 3
17 % 5  = 2
17 ** 5 = 1419857
```

That note is not missing from the first block. It goes to a different
place. A program has two output streams: **stdout**, for the answer, and
**stderr**, for remarks about the answer. `print(..., file=sys.stderr)`
sends the note down the second one. Both land on your screen, so you see
them together, but `python exercise-04-input-parsing.py > answers.txt`
saves the seven lines and leaves the note on screen where it belongs.

The zero divisor, taken from the command line:

```text
$ python exercise-04-input-parsing.py 12 0
12 + 0  = 12
12 - 0  = 12
12 * 0  = 0
12 / 0  = undefined (division by zero)
12 // 0 = undefined (division by zero)
12 % 0  = undefined (division by zero)
12 ** 0 = 1
```

And a negative number, which is where the interesting arithmetic lives:

```text
$ python exercise-04-input-parsing.py -7 2
-7 + 2  = -5
-7 - 2  = -9
-7 * 2  = -14
-7 / 2  = -3.5
-7 // 2 = -4
-7 % 2  = 1
-7 ** 2 = 49
```

Look hard at the last three lines of that run, because two of them
contradict what most people expect.

- `-7 // 2` is `-4`, not `-3`. Floor division rounds *down*, toward
  negative infinity, not toward zero. `-3.5` rounded down is `-4`.
- `-7 % 2` is `1`, not `-1`. Python's remainder always takes the sign of
  the number on the right. That is a deliberate choice and it is
  different from C, Java and JavaScript.
- `-7 ** 2` prints `49`, and if you typed `-7 ** 2` into the REPL you
  would get `-49`. Both are correct. The printed line is *text*: `a` is
  already the value negative seven, so the program computed `(-7) ** 2`.
  Typed as source code, the minus sign binds more loosely than `**`, so
  `-7 ** 2` means `-(7 ** 2)`. Lecture 2 section 2 has this in its
  precedence examples.

Those first two facts are really one fact. Python promises that
`(a // b) * b + (a % b) == a`. Once `//` rounds down, `%` has to come out
non-negative for a positive divisor, or that promise breaks.

## Steps

1. Turn on your Week 2 virtual environment.
2. Create `exercise-04-input-parsing.py` and paste the starter in.
3. Write `parse_int()` first, then try it from the command line:
   `python exercise-04-input-parsing.py 17 5`. If your numbers come
   through, `parse_int()` works, because `numbers_from_argv()` uses it.
4. Now turn the conversation on: `python exercise-04-input-parsing.py --ask`.
   Type `banana`, then an empty line, then `12.0`, then `-7`. You should
   be sent back three times and accepted on the fourth.
5. Write the three division lines in `describe()`. Run
   `python exercise-04-input-parsing.py 17 5` again and compare to the
   first Expected output block.
6. Run `python exercise-04-input-parsing.py 12 0`. Nothing should
   traceback.
7. Run `python exercise-04-input-parsing.py -7 2`. Check the `//` and `%`
   lines against the notes above. If you predicted `-3` and `-1`, you
   have just learned something that will bite you in Week 3, the first
   time you do arithmetic on a list position.
8. Run `mypy exercise-04-input-parsing.py`. The `int | None` return type
   is the interesting one. `mypy` understands that after
   `if value is not None` the value is definitely an `int`, and it
   complains if you return it without that check.

## The Solution

```python
"""exercise-04-input-parsing-solution.py — read two whole numbers and inspect them.

Week 2, Exercise 4. Practises input(), casting, and recovering from bad
input. The read_int() helper here is reused by the Week 2 mini-project.

Three ways to hand this program its two numbers:

    python exercise-04-input-parsing-solution.py --ask   asks you to type them
    python exercise-04-input-parsing-solution.py 12 0    takes them from the command line
    python exercise-04-input-parsing-solution.py         uses the sample pair below

The sample pair is the default so that a run with nobody at the keyboard
prints the same seven lines every time instead of waiting for typing that
is never coming.
"""

import sys

ASK_FLAG: str = "--ask"
PROMPT_FIRST: str = "First whole number: "
PROMPT_SECOND: str = "Second whole number: "
UNDEFINED: str = "undefined (division by zero)"

SAMPLE_FIRST: int = 17
SAMPLE_SECOND: int = 5
SAMPLE_NOTE: str = (
    f"Using the sample pair {SAMPLE_FIRST} and {SAMPLE_SECOND}. "
    f"Pass two numbers, or {ASK_FLAG}, to choose your own."
)


def parse_int(raw: str) -> int | None:
    """Return the whole number in raw, or None if there isn't one.

    Args:
        raw: exactly what the user typed, unmodified.

    Returns:
        The parsed integer, or None if raw is not a whole number.
        Returning None rather than raising lets the caller decide what
        to do about it.
    """
    try:
        return int(raw)
    except ValueError:
        return None


def read_int(prompt: str) -> int:
    """Prompt the user until they type a whole number, then return it.

    Args:
        prompt: the text shown before the cursor.

    Returns:
        The whole number the user eventually typed.
    """
    while True:
        raw: str = input(prompt)
        value: int | None = parse_int(raw)
        if value is not None:
            return value
        print(f"  {raw!r} is not a whole number. Try again.")


def describe(a: int, b: int) -> None:
    """Print every arithmetic operator from Lecture 2 applied to a and b."""
    print(f"{a} + {b}  = {a + b}")
    print(f"{a} - {b}  = {a - b}")
    print(f"{a} * {b}  = {a * b}")
    if b == 0:
        print(f"{a} / {b}  = {UNDEFINED}")
        print(f"{a} // {b} = {UNDEFINED}")
        print(f"{a} % {b}  = {UNDEFINED}")
    else:
        print(f"{a} / {b}  = {a / b}")
        print(f"{a} // {b} = {a // b}")
        print(f"{a} % {b}  = {a % b}")
    print(f"{a} ** {b} = {a ** b}")


def numbers_from_argv() -> tuple[int, int] | None:
    """Return the pair typed after the filename, or None if there isn't one."""
    if len(sys.argv) != 3:
        return None
    first: int | None = parse_int(sys.argv[1])
    second: int | None = parse_int(sys.argv[2])
    if first is None or second is None:
        return None
    return first, second


def choose_numbers() -> tuple[int, int]:
    """Return the pair to describe: keyboard, command line, or samples."""
    if ASK_FLAG in sys.argv[1:]:
        try:
            return read_int(PROMPT_FIRST), read_int(PROMPT_SECOND)
        except EOFError:
            print("\nNo input. Using the sample pair.", file=sys.stderr)
            return SAMPLE_FIRST, SAMPLE_SECOND
    from_argv: tuple[int, int] | None = numbers_from_argv()
    if from_argv is not None:
        return from_argv
    print(SAMPLE_NOTE, file=sys.stderr)
    return SAMPLE_FIRST, SAMPLE_SECOND


def main() -> None:
    """Describe whichever pair of whole numbers this run was handed."""
    a, b = choose_numbers()
    describe(a, b)


if __name__ == "__main__":
    main()
```

**`parse_int()` reports failure as a value, not as an explosion.** It
returns `int | None`: a number when there is one, `None` when there is
not. That one decision is what makes the function reusable. A
`parse_int()` that printed "please try again" could only ever be used by
a program that wanted to say exactly that, in exactly that wording, to a
terminal. Because this one only parses, `read_int()` can phrase its own
complaint, `numbers_from_argv()` can stay silent, and Friday's
mini-project can say something else entirely.

**`except ValueError`, named, never bare.** `int()` raises `ValueError`
for text it cannot read as a number. It raises `TypeError` only if you
hand it something that is not text at all. Catch the one you predicted.

**`if value is not None`, and this is the bug the exercise is really
about.** `0` is a perfectly valid answer and `0` is falsy. Write
`if value:` and a correct input gets rejected, and because `read_int()`
loops forever the person is asked again, and again, for as long as they
keep typing the right answer. `is not None` asks "did the function give
me a value?" `if value:` asks "is the value interesting?" Those are
different questions, and the second is almost never the one you meant
when a function's contract says it may hand back `None`.

**The zero guard is an `if`, not a second `try` / `except`, because zero
is expected.** Both would work. The difference is what the code says to
the next reader. An exception handler says *this should not happen, and
here is the recovery*. A guard says *this is one of the normal cases, and
here is its answer*. Somebody typing `0` as a divisor is not a surprise.

**All three of `/`, `//` and `%` need the guard; `**` does not.** Zero
divides nothing, floor-divides nothing and leaves no remainder, and each
of those raises with its own wording. But `a ** 0` is `1` for any `a`,
including `0 ** 0`, which Python defines as `1`. Handling `**` with the
other three would be a bug that prints "undefined" for a perfectly
defined answer.

**No `.strip()` before parsing, deliberately.** `int(" 12 ")` returns
`12` on its own. A `.strip()` here would be a line that does nothing
while looking important. What the whitespace tolerance *does* mean is
that the `!r` in the message earns its place: if somebody pastes a
trailing tab into something that genuinely does fail, `'12.0\t'` shows it
and `12.0` does not.

**The `=` signs line up because of the operator lengths, counted once.**
`+`, `-`, `*`, `/` and `%` are one character and get two spaces before
the `=`. `//` and `**` are two characters and get one. This is the one
place in Week 2 where counting spaces by hand is correct, because the
padding sits inside a piece of text whose shape never varies. Everywhere
else — see Exercise 2 — you let a format spec do the counting.

**`choose_numbers()` is three answers to one question, in order of how
specific they are.** Did you explicitly ask to type? Then type. Did you
put two numbers on the command line? Then use them. Neither? Then the
samples, with a note saying so. Reading it top to bottom tells you the
whole story of how the program decides, and there is exactly one place
that decision is made.

## Run it

Copy the worked answer on this page into `exercise-04-input-parsing.py` and run it:

```bash
python exercise-04-input-parsing.py
```

## Common bugs to catch

- **`ValueError: invalid literal for int() with base 10: 'banana'`
  escapes and kills the program.** Your `try` wraps the wrong line, or
  you wrote `except TypeError` instead of `except ValueError`:

  ```text
  Traceback (most recent call last):
    File "<string>", line 9, in <module>
      print(parse_int(raw))
            ~~~~~~~~~^^^^^
    File "<string>", line 4, in parse_int
      return int(raw)
  ValueError: invalid literal for int() with base 10: 'banana'
  ```

  The same `ValueError` covers the other rejected inputs, with the
  offending text quoted in the message: `: ''` for an empty line,
  `: '12.0'` for a decimal, `: '-'` for a lone minus sign. If an empty
  line crashes your program, your `try` block does not wrap the `int()`
  call.

- **Typing `0` as the first number asks you again, forever.** You wrote
  `if value:` instead of `if value is not None`:

  ```text
  First whole number:   '0' is not a whole number. Try again.
  First whole number:   '0' is not a whole number. Try again.
  First whole number:   '0' is not a whole number. Try again.
  ```

  Zero is falsy, so a perfectly valid answer is read as a failure. This
  is the single most common bug in this exercise, and it shows up for
  exactly one input value out of every number a person could type.

- **A `ZeroDivisionError` escapes.** Your guard covers `/` but not `//`
  and `%`:

  ```text
  12 + 0  = 12
  12 - 0  = 12
  12 * 0  = 0
  12 / 0  = undefined (division by zero)
  ```

  ```text
  Traceback (most recent call last):
    File "exercise-04-input-parsing.py", line 113, in <module>
      main()
      ~~~~^^
    File "exercise-04-input-parsing.py", line 109, in main
      describe(a, b)
      ~~~~~~~~^^^^^^
    File "exercise-04-input-parsing.py", line 75, in describe
      print(f"{a} // {b} = {a // b}")
                            ~~^^~~
  ZeroDivisionError: integer division or modulo by zero
  ```

  Three operators, three different messages, and reading the message
  tells you which line you missed: `division by zero` for `/`,
  `integer division or modulo by zero` for `//`, and
  `integer modulo by zero` for `%`.

- **A string escapes `parse_int()` and the addition still works.** You
  returned `raw` instead of `int(raw)`. Watch what happens with `12` and
  `5`:

  ```text
  12 + 5  = 125
  ```

  `+` between two strings glues them together, so `"12" + "5"` is
  `"125"`, and nothing raises until the next line tries to subtract:

  ```text
  TypeError: unsupported operand type(s) for -: 'str' and 'str'
  ```

  If only *one* of the two escapes, `+` fails immediately, and the
  wording depends on which side the string is. These are the last lines
  of two separate tracebacks:

  ```text
  TypeError: can only concatenate str (not "int") to str
  ```

  ```text
  TypeError: unsupported operand type(s) for +: 'int' and 'str'
  ```

  The first is `"12" + 5`, with the text on the left. The second is
  `12 + "5"`, with the text on the right.

  Same mistake, two different sentences, because Python asks the value on
  the left first. `mypy` catches all of this before you run anything:

  ```text
  exercise-04-input-parsing.py:47: error: Incompatible return value type (got "str", expected "int | None")  [return-value]
  Found 1 error in 1 file (checked 1 source file)
  ```

- **`mypy` complains about the `return` inside `read_int()`.** You
  deleted the `if value is not None` check:

  ```text
  exercise-04-input-parsing.py:61: error: Incompatible return value type (got "int | None", expected "int")  [return-value]
  ```

  That is `mypy` refusing to let an `int | None` out of a function that
  promised an `int`. Put the check back and `mypy` narrows the type to
  `int` on the line after it, and the same `return` is accepted. The
  check you need for correctness and the check the type checker wants are
  the same check.

- **You left `...` in `parse_int()` and got no error from anywhere.**
  `mypy` does not flag this one, because a body of `...` is compatible
  with a return type that includes `None`. At run time `parse_int()` now
  always says `None`, so `--ask` rejects everything you type and command
  line numbers are silently ignored in favour of the samples. If your
  numbers are not getting through and nothing is complaining, this is
  where to look.

- **`12.0` is accepted and becomes `12`.** You wrapped the cast:
  `int(float(raw))`. That is a real technique from Lecture 1 section 7.1
  and it is not what this exercise asks for. `12.0` is not a whole number
  *as typed*, and silently chopping somebody's decimal off is how a
  program loses money. If you want to accept it, accept it loudly.

- **The `=` signs do not line up.** `17 + 5` is six characters and
  `17 // 5` is seven, so the short operators need two spaces before the
  `=` and the long ones need one. Count them rather than eyeballing.

- **`1_000` is accepted as `1000` and you did not expect it.** Not a bug.
  `int()` accepts underscore separators in text, the same ones Lecture 1
  section 4.1 uses in source code.

- **The prompt and the typed value end up on separate lines.** You wrote
  `print(PROMPT_FIRST)` and then `input()`. Hand the prompt *to*
  `input()`. That is what the argument is for, and it keeps the cursor on
  the same line.

## Under the hood

<details>
<summary>Under the hood — what int() accepts, and what it turns down</summary>

`int(text)` is fussier than most people assume in one direction and much
more relaxed in another. Here is the whole picture, run on CPython
3.13.2.

**Accepted, and some of these surprise people:**

```text
>>> int("12")
12
>>> int(" 12 ")
12
>>> int("+12")
12
>>> int("-12")
-12
>>> int("1_000")
1000
>>> int(" \n 42 \n ")
42
>>> int("12\t")
12
```

Whitespace on either end is stripped for you — spaces, tabs and newlines
alike. A leading sign is fine. Underscores are fine *between* digits,
exactly as they are in source code.

**Turned down, all with `ValueError`. Each of these really prints a full
traceback; only the last line is shown here:**

```text
>>> int("12.0")
ValueError: invalid literal for int() with base 10: '12.0'
>>> int("")
ValueError: invalid literal for int() with base 10: ''
>>> int("-")
ValueError: invalid literal for int() with base 10: '-'
>>> int("banana")
ValueError: invalid literal for int() with base 10: 'banana'
>>> int("1__0")
ValueError: invalid literal for int() with base 10: '1__0'
>>> int("_12")
ValueError: invalid literal for int() with base 10: '_12'
>>> int("12_")
ValueError: invalid literal for int() with base 10: '12_'
```

A decimal point is not a whole number, so `"12.0"` is out. Empty text is
out. A sign with nothing after it is out. Underscores must sit between
two digits — doubled, leading or trailing, they are out. Every one of
these quotes the offending text back at you, which is why the `!r` in the
error message is worth having.

**A different error, for a different mistake:**

```text
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

That is what `int(None)` says.

`TypeError`, not `ValueError`. `ValueError` means "right kind of thing,
wrong contents". `TypeError` means "wrong kind of thing entirely". That
is exactly why `except ValueError` is the correct catch here: if a
`TypeError` ever fires in `parse_int()`, something is broken upstream and
you want to hear about it, not quietly get a `None` back.

**Two more corners worth knowing.**

`int()` takes a second argument, the base. `int("ff", 16)` is `255` and
`int("1010", 2)` is `10`. Pass `0` and it reads the prefix and works it
out: `int("0x1f", 0)` is `31`. Without a base, `int("0b1010")` is a
`ValueError`, because base 10 does not know what `0b` means.

And a genuinely modern surprise:

```text
ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use sys.set_int_max_str_digits() to increase the limit
```

That is `int("1" * 5000)`, five thousand ones.

Python 3.11 added a cap on how many digits `int()` will read from text.
Converting text to a very large number takes time proportional to the
*square* of the digit count, so a web form that let somebody paste a
million digits was a way to make a server sit there and think. The limit
is a security fix, not a limit on how big an `int` can be. Python's
integers themselves are still unbounded — `10 ** 100` is exact and fine.

**One thing `int()` accepts that has nothing to do with English.**
Digits from other writing systems work too, because Python asks Unicode
whether a character is a digit rather than checking whether it is between
`0` and `9`. The Arabic-Indic numerals for one and two parse as `12`.
Charming, and worth knowing if you ever validate input for a worldwide
audience.

</details>

<details>
<summary>Under the hood — why the guard beats the clever one-liner</summary>

Week 2 has no `if` in its lecture material, so you might reasonably ask
whether the zero guard could be written with the week's own tools. It
can, using the short-circuit behaviour of `and` and `or` from
[Lecture 2 section 4](../lecture-notes/02-operators-and-strings.md):

```python
print(f"{a} / {b}  = {b and a / b or UNDEFINED}")
```

Read it as: if `b` is falsy, `and` stops and gives you `b` — which is `0`
— so `or` takes over and gives you `UNDEFINED`. If `b` is truthy, `and`
gives you the division, and `or` leaves a truthy result alone. It works.
Try it with `a = 0` and `b = 3`:

```text
0 + 3  = 3
0 - 3  = -3
0 * 3  = 0
0 / 3  = undefined (division by zero)
0 // 3 = undefined (division by zero)
0 % 3  = undefined (division by zero)
0 ** 3 = 0
```

Three is not zero. Nothing was divided by zero. But `b and a / b`
evaluated to `0.0`, and `0.0` is falsy, so `or UNDEFINED` fired anyway.
The construction cannot tell "there was no answer" apart from "the answer
was zero", which is the exact same confusion as `if value:` versus
`if value is not None` in `read_int()`. One bug, two costumes.

Wrapping the division in `str()` happens to fix it, because `"0.0"` is
non-empty text and therefore truthy. That is not a fix. That is the bug
being hidden by an accident of what `str()` returns.

`if b == 0` says what you mean, cannot be broken by a value that happens
to be falsy, and reads correctly to somebody who has never seen the
trick. Wait a week for `if`. It is worth it.

There is a second reason the guard is right here, and it is about
vocabulary rather than correctness. `try` / `except` and `if` say
different things to a reader. An exception handler means *this was not
supposed to happen*. A guard means *this is one of the cases I planned
for*. Somebody typing `banana` is the first. Somebody typing `0` is the
second. Matching the tool to the meaning is most of what makes code
readable to the next person, and that person is usually you in three
months.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback for any input, including `banana`, an empty line, and `0`.
- [ ] Every run in Expected output reproduces exactly, including the alignment of the `=` signs.
- [ ] `0` as either number is accepted, not re-prompted.
- [ ] `parse_int()` neither prints nor raises, and catches `ValueError` by name.
- [ ] `read_int()`, `numbers_from_argv()`, `choose_numbers()` and `main()` are unmodified.
- [ ] You can explain in one sentence why `-7 % 2` is `1`.
- [ ] `mypy` reports no issues, if you have it installed.
- [ ] The file is committed to Git with a message like `Add Week 2 exercise 4: input parsing`.

## Stretch

- **Run the conversation for real.** The shipped file keeps `input()`
  behind `--ask` so that an automatic run cannot hang, but the
  conversation is the point of the exercise, so go and have it:

  ```bash
  python exercise-04-input-parsing.py --ask
  ```

  Type `seven`, then `12.0`, then `12`, then `0`. Here is that exact
  session, captured by feeding the four answers in from a file rather
  than a keyboard:

  ```text
  First whole number:   'seven' is not a whole number. Try again.
  First whole number:   '12.0' is not a whole number. Try again.
  First whole number: Second whole number: 12 + 0  = 12
  12 - 0  = 12
  12 * 0  = 0
  12 / 0  = undefined (division by zero)
  12 // 0 = undefined (division by zero)
  12 % 0  = undefined (division by zero)
  12 ** 0 = 1
  ```

  The two prompts run into each other on the third line because nothing
  was typed between them — text fed in from a file is not echoed back to
  the screen the way your own typing is. Type the same four answers by
  hand and you will see `12` and `0` sitting after their prompts, each on
  its own line. Same program, same output, different-looking transcript.

  If you want to reproduce the captured version yourself, this works in
  Git Bash, macOS and Linux:

  ```bash
  printf 'seven\n12.0\n12\n0\n' | python exercise-04-input-parsing.py --ask
  ```

  Piping into a Python `input()` loop from Windows PowerShell 5.1 did not
  work in testing, so on Windows either use Git Bash or just type.

- **Simplify `main()` back to the shape the lecture gives you** and see
  the trade-off for yourself:

  ```python
  def main() -> None:
      """Read two whole numbers and describe them."""
      a: int = read_int(PROMPT_FIRST)
      b: int = read_int(PROMPT_SECOND)
      describe(a, b)
  ```

  Shorter, clearer, and it hangs the moment nobody is at the keyboard.
  For a tool a person runs by hand, that is fine. For a tool a script
  runs at three in the morning, it is a job that never finishes. Decide
  on purpose which one you are writing.

- **Add a retry limit.** After three bad attempts, give up and say so
  rather than asking forever. Notice what this does to the type: a
  `read_int()` that never gives up can promise an `int`, but a
  `read_int_limited()` that can give up has to promise `int | None`, and
  every caller now has to deal with the `None`. `mypy --strict` will not
  let you forget.

  ```text
  $ printf 'x\n2000000\ny\n' | python exercise-04-stretch.py
  Whole number (max 1000000):   'x' is not a whole number. Try again.
  Whole number (max 1000000):   '2000000' is not a whole number. Try again.
  Whole number (max 1000000):   'y' is not a whole number. Try again.
  Giving up after three bad attempts.
  ```

- **Reject numbers outside a sensible range** by having `parse_int()`
  return `None` for anything above a million. Notice that `read_int()`
  does not change at all. That is the payoff for keeping parsing pure:
  the loop's contract is "keep asking until `parse_int()` gives me
  something", and it does not care *why* a parse failed. Adding a rule
  meant editing one function.

- **Write `parse_float()` and a matching `read_float()`.** You will see
  immediately that they are the same two functions again with one word
  changed, and you cannot fix that yet — the fix is to pass the converter
  in as an argument, which needs Week 4's material on functions as
  values. Notice the smell now; the cure is two weeks away.

- **Find out what `0 ** 0` gives, then what `0 % 0` gives.** One is a
  number and one is an exception:

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print(0%0)
            ~^~
  ZeroDivisionError: integer modulo by zero
  ```

  `0 ** 0` is `1`, by a convention that holds across essentially all of
  mathematics and computing, because it makes the exponent rules work
  without special cases. Remainder by zero has no such convention
  available — there is no leftover when you divide nothing into
  something — so it refuses. One of them is a decision the language made
  for your convenience; the other is arithmetic saying no.

That is all four exercises. When your arithmetic inspector survives
everything you can throw at it, move on to the
[Week 2 challenges](../challenges/README.md).
