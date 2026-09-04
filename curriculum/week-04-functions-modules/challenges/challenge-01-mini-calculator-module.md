# Challenge 1 — Mini Calculator Module

> **Topic:** your first program made of two files, where one file imports the other, plus a dictionary that holds functions instead of numbers
> **Lecture:** [04 — Modules and Imports](../lecture-notes/04-modules-and-imports.md)
> **Difficulty:** the arithmetic is four one-line functions; the shape of the project is the work
> **Target time:** 2–3 hours
> **Why this one:** up to now a program has been one file. From here on it is a folder. This is the challenge where `import` stops being a magic word you copy from tutorials and starts being something you do to your own code.

## The Brief

You are going to build a pocket calculator that you can type sums into:

```text
> 2 + 3
5.0
```

That is the easy half. The real point is **how the program is split up**.

You write **two** files:

- **`calculator.py`** — four functions that do arithmetic. `add`,
  `subtract`, `multiply`, `divide`. This file never prints anything and
  never asks anybody anything. It just takes numbers and hands numbers
  back.
- **`main.py`** — the part that talks to a person. It asks for a sum,
  works out which of the four functions to call, calls it, and prints
  the answer.

`main.py` gets hold of those four functions with one line:

```python
from calculator import add, subtract, multiply, divide
```

That line is the whole lesson. A **module** is just a `.py` file that
another `.py` file can borrow names from. `calculator.py` is a module
the moment `main.py` imports it. There is no registration step, no
config file, no ceremony — the two files sit in the same folder and
Python finds one from the other.

**Why bother splitting it?** Because of what each half can then do on
its own. `calculator.py` has no keyboard in it, so you can test it
without typing anything. `main.py` has no arithmetic in it, so when a
sum comes out wrong you know which file to open. Every large program you
will ever read is this same trick, repeated: push the part that talks to
humans out to the edge and keep the part that computes in the middle,
where it can be checked.

Here is the session the finished program should produce:

```text
$ python main.py
Mini calculator. Type "quit" to exit.
> 2 + 3
5.0
> 10 / 4
2.5
> 7 * 6
42.0
> 1 / 0
cannot divide by zero
> hello
sorry, I did not understand "hello". Use: <num1> <op> <num2>.
> quit
bye!
```

Two of those lines are the interesting ones. `1 / 0` is a sum nobody can
do, and `hello` is not a sum at all. Neither of them is allowed to end
the program with a traceback — both get a sentence and another prompt.

> *As a* learner who has just met `def`, `return` and `import`,
> *I want* to write one file that another file uses,
> *so that* I find out what a module actually is.

## Starter

Two files, in a new folder called `challenge-01-mini-calculator/`
inside `challenges/`. Save both, then run them before you change
anything. They work as pasted — the arithmetic and the parsing are the
parts you fill in.

`calculator.py`:

```python
"""TODO: one line saying what this file does."""


def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


# TODO 1: subtract, multiply, and divide, in the same shape as add.
# divide must raise ZeroDivisionError("cannot divide by zero") when b is 0.


def _self_test() -> None:
    """Exercise every function and print OK or the first failure."""
    # TODO 2: check all four functions, then check that divide(1, 0) raises.
    print("OK")


if __name__ == "__main__":
    _self_test()
```

`main.py`:

```python
"""TODO: one line saying what this file does."""

import sys

from calculator import add

OPS = {"+": add}
# TODO 3: put the other three functions in OPS. No parentheses after the names.

BANNER = 'Mini calculator. Type "quit" to exit.'
PROMPT = "> "

DEMO_LINES: list[str] = ["2 + 3", "quit"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_LINES.pop(0) if DEMO_LINES else demo
        print(f"{prompt}{answer}".rstrip())
        return answer


def parse(line: str) -> tuple[float, str, float]:
    """Parse '2 + 3' into (2.0, '+', 3.0)."""
    # TODO 4: split the line, check there are exactly three pieces, check the
    #         operator is in OPS, and convert the two numbers.
    return 0.0, "+", 0.0


def main() -> None:
    """Run the REPL until the user quits."""
    print(BANNER)
    while True:
        line = ask(PROMPT, "quit").strip()
        if line == "" or line.lower() == "quit":
            break
        # TODO 5: parse the line, look the operator up in OPS, call it, print
        #         the result. Say something friendly when parse or divide
        #         complains instead of letting the traceback out.
        print(line)
    print("bye!")


if __name__ == "__main__":
    main()
```

Run each of them once:

```text
$ python calculator.py
OK
```

```text
$ python main.py
Mini calculator. Type "quit" to exit.
> 2 + 3
2 + 3
> quit
bye!
```

Nothing is broken. `calculator.py` prints `OK` because its self-test
does not check anything yet, and `main.py` echoes your line back
because the parsing is missing on purpose.

**About `ask()`.** It is given to you and you never have to write one.
It asks a question and reads a line. If nobody is there to answer —
because a checker is running the file, or because you piped input in and
the input ran out — it takes the next line out of `DEMO_LINES` instead
and prints it, so the file always produces a whole session. The question
goes to the **error stream** and the answer goes to the **normal output
stream**, and *The Solution* explains why that matters more than it
sounds like it should.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/challenges/challenge-01-mini-calculator-module.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Two files, `calculator.py` and `main.py`, in one folder.
2. `calculator.py` has a module docstring on its first line and exposes
   exactly four public functions: `add`, `subtract`, `multiply`,
   `divide`. Each takes two `float` arguments, returns a `float`, has
   type hints on the parameters and the return, and has a one-line
   docstring.
3. `divide(a, b)` raises `ZeroDivisionError` with the message
   `cannot divide by zero` when `b` is `0`. That exact wording.
4. `calculator.py` has a `_self_test()` that exercises all four
   functions and prints `OK`, or a line naming the first failure. It
   runs under `if __name__ == "__main__":` and nowhere else.
5. `main.py` prints the banner `Mini calculator. Type "quit" to exit.`
   once, before the first prompt.
6. The prompt is `> ` — a greater-than sign and one space.
7. Input is `<number> <operator> <number>`, separated by spaces, where
   the operator is one of `+`, `-`, `*`, `/`.
8. A blank line or the word `quit` ends the program. Accept `QUIT` and
   `  quit  ` too.
9. Anything the program cannot use prints
   `sorry, I did not understand "<what you typed>". Use: <num1> <op> <num2>.`
   and asks again. Dividing by zero prints `cannot divide by zero` and
   asks again. Neither ends the program.
10. On the way out, print `bye!`.
11. `main.py` defines a `main()` function, and the `__main__` guard
    calls it.
12. Say in a comment at the top of `main.py` which import form you chose
    — `from calculator import ...` or `import calculator` — and why.

## Constraints

- **The two files stay in their lanes.** `calculator.py` contains no
  `print` and no `input` outside its `_self_test`. `main.py` contains no
  arithmetic. If you find yourself writing `a + b` in `main.py`, the
  function you want already exists in the other file.
- **Every function gets type hints and a docstring.** `def add(a: float,
  b: float) -> float:` and a one-line `"""Return a + b."""` under it.
  This is the week the habit forms, and it is worth 15 rubric points.
- **Use a dictionary to pick the operator, not an `if`/`elif` chain.**
  `OPS = {"+": add, "-": subtract, ...}` stores the four functions
  themselves. Look one up with `OPS[op]` and call it with
  `OPS[op](left, right)`. *The Solution* explains what is really going
  on there; for now, notice there are **no parentheses** after the
  function names inside the dict.
- **`_self_test()` goes under the `__main__` guard.** Not at the top
  level of the file. If you put it at the top level, `main.py` prints
  `OK` before its banner every single time it starts, because importing
  a module runs everything in it.
- **Standard library only.** `main.py` imports `sys` and your own
  `calculator`. Nothing else.
- **Both files run on a fresh Python 3.10 or newer**, from inside their
  own folder.

## Expected output

The downloadable answer is the two files folded into one, so that it
runs the moment you have it — *Download and run* says why, and *The
Solution* shows where the seam is. Run it with nothing attached to its
input and it answers its own questions and prints a whole session. This
is the real stdout on CPython 3.13.2:

```text
$ python challenge-01-mini-calculator-module.py
OK

Mini calculator. Type "quit" to exit.
> 2 + 3
5.0
> 10 / 4
2.5
> 7 * 6
42.0
> 1 / 0
cannot divide by zero
> hello
sorry, I did not understand "hello". Use: <num1> <op> <num2>.
> quit
bye!
```

The `OK` on the first line is what `python calculator.py` prints on its
own in the two-file version. Everything from the banner down is what
`python main.py` prints. One file, both jobs, because that is the only
way a single download can show you both halves.

Read the session as a checklist. `2 + 3` gives `5.0` and not `5`,
because the functions are typed `-> float`. `10 / 4` gives `2.5`, so
division is real division. `1 / 0` prints your message, not Python's.
`hello` is refused politely. `quit` gets out.

Feed it your own lines from the shell and the questions vanish, because
they go to the error stream:

```text
$ printf '2 ** 3\n8 / 0\n  QUIT  \n' | python challenge-01-mini-calculator-module.py
OK

Mini calculator. Type "quit" to exit.
sorry, I did not understand "2 ** 3". Use: <num1> <op> <num2>.
cannot divide by zero
bye!
```

Three things checked at once. `**` is not one of the four operators, so
it is refused by the same message as `hello` — requirement 7. `8 / 0` is
caught. And `  QUIT  ` in shouting capitals with spaces around it still
quits, which is requirement 8.

## Steps

1. Make the folder and save both starter files into it. Run
   `python calculator.py` and then `python main.py`. You should see the
   two sessions above. Do not go on until both run.

2. Do **TODO 1**. Write `subtract` and `multiply` by copying `add` and
   changing one character each. Then write `divide`:

   ```python
   def divide(a: float, b: float) -> float:
       """Return a / b, refusing a zero divisor."""
       if b == 0:
           raise ZeroDivisionError("cannot divide by zero")
       return a / b
   ```

   Check it in the REPL — `python -i calculator.py`, then
   `divide(10.0, 4.0)` and `divide(1.0, 0.0)`.

3. Do **TODO 3**: add the other three names to `OPS`. Run `main.py`. It
   still echoes, because the parser is still a stub, but nothing should
   break.

4. Do **TODO 4**, the parser, in three moves. First
   `parts = line.split()`. Then `if len(parts) != 3: raise ValueError(...)`.
   Then unpack, check `op in OPS`, and return
   `float(left), op, float(right)`. Check the length **before** you
   unpack — *Common bugs to catch* shows what happens if you do not.

5. Do **TODO 5**. Call `parse(line)` inside a `try`, catch `ValueError`,
   print the "sorry" message and `continue`. Then, in a second `try`,
   call `OPS[op](left, right)` and print it, catching `ZeroDivisionError`
   and printing the exception itself. Two separate `try` blocks, because
   the two problems deserve two different messages.

6. Do **TODO 2**, the self-test, last — by then you know what to test.
   Check each function against a known answer, then check that
   `divide(1.0, 0.0)` raises with the right message. Print `OK` only if
   everything passed.

7. Run the session from *Expected output* and compare it line by line.

8. Commit:

   ```bash
   git add challenges/challenge-01-mini-calculator/
   git commit -m "Add Challenge 1: mini calculator module"
   ```

## The Solution

```python
"""Mini calculator: four arithmetic functions, and a REPL that uses them.

Challenge 1, Week 4, Code Crunch Convos.

The project this answers is two files. ``calculator.py`` holds the arithmetic
and knows nothing about people; ``main.py`` imports it and does all the talking.
This download folds both halves into one file so that it runs the moment you
save it: everything above the ``main.py half`` banner is what ``calculator.py``
contains, and everything below it is what ``main.py`` contains. The page beside
this file shows the two-file split, which is the thing the challenge is really
about.

Questions go to the error stream and results go to the normal output stream, so
``python challenge-01-mini-calculator-module-solution.py > out.txt`` saves the
answers and none of the questions.

Run it with::

    python challenge-01-mini-calculator-module-solution.py
"""

import sys

# --- the calculator.py half: arithmetic, and nothing else ------------------


def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return a - b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return a * b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return a / b, refusing a zero divisor."""
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def _self_test() -> None:
    """Exercise all four functions and report OK or the first failure."""
    checks = [
        ("add(2, 3)", add(2.0, 3.0), 5.0),
        ("subtract(10, 4)", subtract(10.0, 4.0), 6.0),
        ("multiply(7, 6)", multiply(7.0, 6.0), 42.0),
        ("divide(10, 4)", divide(10.0, 4.0), 2.5),
    ]
    for label, got, want in checks:
        if got != want:
            print(f"FAIL: {label} -> {got!r}, expected {want!r}")
            return
    try:
        divide(1.0, 0.0)
    except ZeroDivisionError as exc:
        if str(exc) != "cannot divide by zero":
            print(f"FAIL: divide by zero message was {str(exc)!r}")
            return
    else:
        print("FAIL: divide(1, 0) did not raise ZeroDivisionError")
        return
    print("OK")


# --- the main.py half: talking to a person ---------------------------------

# Import choice. In the two-file version the line above this table reads
# ``from calculator import add, divide, multiply, subtract``, not
# ``import calculator``. The four names go straight into OPS, and spelling them
# ``calculator.add`` in there would add noise without adding information. For a
# module with a wider surface, ``import calculator`` is the better default.

OPS = {"+": add, "-": subtract, "*": multiply, "/": divide}

BANNER = 'Mini calculator. Type "quit" to exit.'
PROMPT = "> "

# The session this file types for itself when its input stream is finished.
DEMO_LINES: list[str] = ["2 + 3", "10 / 4", "7 * 6", "1 / 0", "hello", "quit"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on once the demo script above has run
            out. Every call site passes ``"quit"``, so this file can never
            loop forever unattended.

    Returns:
        The line that was typed, or the next demo answer. A demo answer is
        echoed after the prompt on the normal output stream, trimmed on the
        right so a question answered with a blank line leaves no stray space
        at the end of a saved transcript.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_LINES.pop(0) if DEMO_LINES else demo
        print(f"{prompt}{answer}".rstrip())
        return answer


def parse(line: str) -> tuple[float, str, float]:
    """Parse '2 + 3' into (2.0, '+', 3.0)."""
    parts = line.split()
    if len(parts) != 3:
        raise ValueError("expected exactly three whitespace-separated fields")
    left, op, right = parts
    if op not in OPS:
        raise ValueError(f"unknown operator {op!r}")
    return float(left), op, float(right)


def main() -> None:
    """Run the REPL until the user quits."""
    print(BANNER)
    while True:
        line = ask(PROMPT, "quit").strip()
        if line == "" or line.lower() == "quit":
            break
        try:
            left, op, right = parse(line)
        except ValueError:
            print(f'sorry, I did not understand "{line}". Use: <num1> <op> <num2>.')
            continue
        try:
            print(OPS[op](left, right))
        except ZeroDivisionError as exc:
            print(exc)
    print("bye!")


if __name__ == "__main__":
    _self_test()
    print()
    main()
```

**The download is one file, and the project is two. Here is why.** Every
page in this course ships one file you can download and run. A two-file
project cannot be one download without a zip, and a zip is a thing you
have to unpack before you can read it. So the answer above is the two
files stacked in one, with a comment banner where the seam is —
everything above `--- the main.py half` is `calculator.py`, everything
below it is `main.py`. Nothing else changed. Split it at that line, put
`from calculator import add, divide, multiply, subtract` at the top of
the lower half, and you have the project the brief asked for. That split
is exactly what the next section shows.

**What the two files look like properly.**

`calculator.py` — the module. It ends at `_self_test`:

```python
"""Tiny arithmetic calculator."""


def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


# ... subtract, multiply, divide, _self_test, exactly as above ...


if __name__ == "__main__":
    _self_test()
```

`main.py` — the program. It starts with the import:

```python
"""Mini calculator REPL."""

import sys

# Import choice: `from calculator import ...` rather than `import calculator`.
# The four names go straight into the OPS dispatch table below, and spelling
# them `calculator.add` in that table would add noise without adding
# information. For a module with a wider surface, `import calculator` wins.

from calculator import add, divide, multiply, subtract

OPS = {"+": add, "-": subtract, "*": multiply, "/": divide}

# ... BANNER, PROMPT, DEMO_LINES, ask, parse, main, exactly as above ...


if __name__ == "__main__":
    main()
```

Run them and you get the two halves of the session separately:

```text
$ python calculator.py
OK
$ python main.py
Mini calculator. Type "quit" to exit.
> 2 + 3
...
```

**`OPS` is a table that holds functions, and that is why there is no
`if`/`elif` chain.** Look closely at
`OPS = {"+": add, "-": subtract, ...}`. There are no parentheses after
`add`. That means nothing is *called* there — the dictionary just
remembers the four functions themselves, the way it would remember four
numbers. A function in Python is a value you can put in a list, pass to
another function, or store in a dict, exactly like `7` or `"hello"`.

Later, `OPS[op]` looks one up and the `(left, right)` after it calls it:

```python
print(OPS[op](left, right))
```

Read that right to left and it is "get the function stored under `op`,
then call it with these two numbers". A four-branch `if`/`elif` would
work identically. The table wins for two reasons you feel straight away:
adding a fifth operator is one line in a dict instead of one more
branch, and `if op not in OPS` gives you operator checking for free in
the parser.

**`divide` raises its own error on purpose.** Python already complains
about `1.0 / 0.0` all by itself — but it says `float division by zero`,
and requirement 3 says the message must be `cannot divide by zero`. So
you check `b == 0` yourself and raise with your own words. This is a
shape you will meet constantly: the language gives you an exception, but
not the one your users need. Catch the condition first and raise
something a human can read.

**`parse` decides nothing about what to say.** It takes a string and
returns a tuple. It touches no globals and prints nothing. When
something is wrong it raises `ValueError` and lets `main` choose the
words. That separation is what lets one `except ValueError` in `main`
handle all three failures — wrong number of pieces, unknown operator,
and "that is not a number", because `float("hello")` raises `ValueError`
too. The user gets one consistent message for all three, and that is not
luck: `parse` raises `ValueError` *specifically* so that it lines up
with the one `float()` already raises.

**Two `try` blocks in `main`, not one.** A bad sum and a division by
zero deserve different sentences, so they get different handlers. One
big `try` would force you to look at the exception's type inside a
single `except`, which is the same code with more nesting.

**Both files have a `__main__` guard, for two different reasons.** In
`calculator.py`, the guard is what lets the module double as its own
test script: `python calculator.py` runs `_self_test()`, and
`from calculator import add` in `main.py` does not. Without it, every
run of `main.py` would print `OK` before its banner, because importing a
module runs every line in it. In `main.py`, the guard stops the REPL
launching if anyone ever imports *it*.

**`ask()` puts the questions on the other stream.** A program has two
ways to send text out: `stdout`, the normal output stream, for its
answers, and `stderr`, the error stream, for everything else. `ask()`
prints the question to `stderr` with `end=""` so the cursor stays on the
line, and `flush=True` so the question appears *before* the program
starts waiting instead of sitting in a buffer. Then it calls `input()`
with **no argument at all**.

That last detail is the one people get wrong. `input("> ")` prints its
prompt to `stdout`, mixed in with your results. Keeping them apart is
what makes this work:

```bash
python challenge-01-mini-calculator-module.py > out.txt
```

`out.txt` holds the answers and none of the questions. You saw the same
effect in the piped session under *Expected output*, where the prompts
simply were not there.

## Run it

Copy the worked answer on this page into `challenge-01-mini-calculator-module.py` and run it:
and run it:

```bash
python challenge-01-mini-calculator-module.py
```

In your own terminal it asks you for sums. Run by a script, or with its
input closed, it types its own session from `DEMO_LINES`.

You can also feed it lines from the shell, one per prompt:

```bash
printf '2 + 3\n10 / 4\nquit\n' | python challenge-01-mini-calculator-module.py
```

One thing to know about that: when the piped lines run out, `ask()` does
not stop — it falls through to `DEMO_LINES` and finishes the demo
session. Pipe a `quit` in at the end if you want it to stop where you
stopped.

Because the questions go to the error stream, `>` captures the answers
on their own:

```bash
python challenge-01-mini-calculator-module.py > out.txt
```

**This one file is the two-file project stacked up.** It is written that
way so the download runs immediately. In your own repository, build the
real thing: a folder `challenges/challenge-01-mini-calculator/` holding
`calculator.py` and `main.py`, split at the `--- the main.py half`
banner, with `from calculator import add, divide, multiply, subtract` at
the top of `main.py`. *The Solution* shows both files. The two-file
version is what the brief asks for and what gets graded.

## Common bugs to catch

**You called the functions inside the dispatch table.** This is the most
common bug in this challenge, by a distance:

```python
OPS = {"+": add(a, b), "/": divide(a, b)}   # WRONG
```

```text
Traceback (most recent call last):
  File "main.py", line 3, in <module>
    OPS = {"+": add(a, b), "/": divide(a, b)}
                    ^
NameError: name 'a' is not defined
```

At the moment that line runs there is no `a` and no `b` — and there
never will be, because the table is built once when the file loads, long
before anybody types a sum. A dispatch table stores functions, not
results. Drop the parentheses.

**You unpacked before checking the length.**

```python
left, op, right = line.split()   # WRONG: crashes on any other count
```

Type `hello`:

```text
Traceback (most recent call last):
  File "main.py", line 3, in <module>
    left, op, right = line.split()
    ^^^^^^^^^^^^^^^
ValueError: not enough values to unpack (expected 3, got 1)
```

Type `1 + 2 + 3`:

```text
Traceback (most recent call last):
  File "main.py", line 3, in <module>
    left, op, right = line.split()
    ^^^^^^^^^^^^^^^
ValueError: too many values to unpack (expected 3)
```

Both are `ValueError`, so a broad `except ValueError` would swallow them
— and then your user gets a message about unpacking instead of a message
about calculator syntax. Check `len(parts) != 3` first and raise your
own error with your own words.

**You let Python's own `ZeroDivisionError` through.**

```python
def divide(a: float, b: float) -> float:
    """Return a / b."""
    return a / b        # WRONG: the message will not match the spec
```

The REPL then prints:

```text
float division by zero
```

instead of `cannot divide by zero`. The function still "works". The
requirement still fails. Wherever a brief pins down an error *message*,
you own that message.

**You put `_self_test()` at the top level of `calculator.py`.** No
error, and the program still calculates. But now every run of `main.py`
starts like this:

```text
OK
Mini calculator. Type "quit" to exit.
```

`OK` came from a file you only meant to borrow four functions from.
Importing a module runs every line in it, top to bottom. The
`__main__` guard is the fix, and this is the whole reason it exists.

**`ModuleNotFoundError: No module named 'calculator'`.** You ran
`main.py` from the wrong place:

```text
Traceback (most recent call last):
  File "main.py", line 5, in <module>
    from calculator import add
ModuleNotFoundError: No module named 'calculator'
```

Python looks for `calculator.py` next to the **script it was told to
run**, not in the folder you happen to be standing in. `python
challenge-01-mini-calculator/main.py` works from anywhere.
`python -c "import main"` from the parent folder does not. When in
doubt, `cd` into the project folder first.

**Your results print as `5` instead of `5.0`.** You passed the strings
straight through, or converted with `int()` instead of `float()`. The
functions are typed `-> float` and requirement 7 accepts decimals, so
`float()` is the conversion. `10 / 4` giving `2` instead of `2.5` is the
same bug wearing a different hat.

**`quit` works but `QUIT` does not.** You compared before normalising.
The order is read, `.strip()`, `.lower()`, then test.

## Under the hood

<details>
<summary>Under the hood — what a module actually is once you import it</summary>

`import` sounds like it copies text into your file, the way `#include`
does in C. It does not. It runs the other file once, wraps everything
that file defined into a single **object**, and hands you that object.

You can look at it:

```text
>>> import calculator
>>> type(calculator)
<class 'module'>
>>> calculator
<module 'calculator' from '.../calc/calculator.py'>
>>> calculator.__name__
'calculator'
>>> sorted(n for n in vars(calculator) if not n.startswith('__'))
['_self_test', 'add', 'divide']
```

A module is a value, like a list or a number. `calculator.add` is an
attribute lookup on that value, the same kind of thing as
`"hello".upper`. `vars(calculator)` is the module's own namespace — the
dictionary of every name the file defined. That is all a module is: a
box of names, with a file attached to it.

**Python keeps every module it has loaded in one place.** The place is
`sys.modules`, a plain dictionary from name to module object:

```text
>>> import sys
>>> 'calculator' in sys.modules
True
>>> sys.modules['calculator'] is calculator
True
```

`is` there means "the very same object", not "an equal one". There is
exactly one `calculator` module in a running program, no matter how many
files import it.

**Which is why the second import is free.** Take a file that says
something out loud when it loads:

```python
"""A module that says something the moment it is imported."""

print("noisy.py is running its top level")
print("__name__ here is", __name__)
```

Import it twice:

```text
>>> import noisy
noisy.py is running its top level
__name__ here is noisy
>>> import noisy
>>> print('done')
done
```

The second `import` printed nothing. `import` is not "run this file" —
it is "make sure this file has been run, then give me the module
object". The first time, Python finds the file, runs it, and files the
result in `sys.modules`. Every time after that it just reads
`sys.modules` and hands the same object back. That is why a program with
twenty files that all `import config` reads `config.py` exactly once.

It also means a module's top level is a **one-time setup area**. Put an
expensive thing there and you pay for it once. Put a `print` there and
it fires the first time somebody imports you and never again, at a
moment you do not control — which is why `_self_test()` belongs under
the guard.

</details>

<details>
<summary>Under the hood — how __name__ lets one file be both a library and a program</summary>

Every module has a variable called `__name__`, and Python sets it before
the file's first line runs. What it gets set to depends on **how the
file was started**.

Same file, two ways:

```text
$ python -c "import noisy"
noisy.py is running its top level
__name__ here is noisy
```

```text
$ python noisy.py
noisy.py is running its top level
__name__ here is __main__
```

Imported, `__name__` is the module's name. Run directly, `__name__` is
the string `"__main__"` — because the file Python was pointed at *is*
the main program, and Python does not care what it happens to be called.

So this:

```python
if __name__ == "__main__":
    _self_test()
```

means, in plain English: "only do this if I am the program somebody
started, not a file somebody borrowed from". One file, two behaviours,
and the file itself decides which.

That is what makes `calculator.py` able to be two things at once. To
`main.py` it is four arithmetic functions and nothing else. To you at
the terminal it is a little test script. Neither gets in the other's
way, and the entire mechanism is one `if` statement comparing a string.

Watch what the guard is *not*. It does not stop the module's top level
running on import — `noisy.py` printed both times it was first loaded.
It only guards what is inside it. Anything you want to happen on import,
put outside the guard on purpose; anything you want only when the file
is run, put inside.

</details>

<details>
<summary>Under the hood — import calculator versus from calculator import add</summary>

The two forms look like a matter of taste. They differ in one way that
eventually matters.

`from calculator import add` copies the *value* of `calculator.add` into
your file's namespace, right now, once. `import calculator` copies a
reference to the module and looks `add` up fresh on every call.

Most of the time that difference is invisible. Here is where it is not.
Two files that do the same thing:

```python
"""Calls the name it copied at import time."""

from calculator import add


def total() -> float:
    """Return add(2, 3)."""
    return add(2.0, 3.0)
```

```python
"""Calls the name through its module."""

import calculator


def total() -> float:
    """Return calculator.add(2, 3)."""
    return calculator.add(2.0, 3.0)
```

Now replace `calculator.add` at runtime — which is exactly what a test
does when it wants to check what happens if a dependency misbehaves:

```text
>>> import calculator, uses_from, uses_import
>>> def fake_add(a, b):
...     return 999.0
...
>>> calculator.add = fake_add
>>> uses_from.total()
5.0
>>> uses_import.total()
999.0
```

`uses_from` never noticed. It took its own copy of the function when it
was imported and has held it ever since. `uses_import` goes through the
module every time, so it sees the swap.

The rule of thumb that falls out of this:

- **`from x import y`** when `y` is a small, stable, obvious thing you
  will use a lot — `from collections import Counter`. Shorter at every
  call site.
- **`import x`** when you might want to swap `x`'s insides in a test,
  when the name would be ambiguous on its own (`report.total` reads
  better than a bare `total`), or when you are importing many names.

This answer uses `from calculator import ...` because the four names go
straight into `OPS` and `calculator.add` in there would be noise. That
is a real, small tradeoff, made on purpose — which is why requirement 12
asks you to write your choice down. Week 11 covers testing, and this is
the paragraph you will come back to.

Never use `from calculator import *`. It drags every public name in the
module into your file, so a reader cannot tell where anything came from,
and a name you did not expect can quietly replace one of yours.

</details>

## Acceptance checklist

- [ ] Two files, `calculator.py` and `main.py`, in a folder of their
      own under `challenges/`.
- [ ] `python calculator.py` prints `OK` and nothing else.
- [ ] `python main.py` prints the banner, then prompts with `> `.
- [ ] `2 + 3` gives `5.0`. `10 - 4` gives `6.0`. `7 * 6` gives `42.0`.
      `10 / 4` gives `2.5`.
- [ ] `1 / 0` prints `cannot divide by zero` and asks again.
- [ ] `hello` prints
      `sorry, I did not understand "hello". Use: <num1> <op> <num2>.`
      and asks again.
- [ ] `2 ** 3` is refused the same way, because `**` is not one of the
      four operators.
- [ ] `1 + 2 + 3` is refused, not crashed on.
- [ ] `quit`, `QUIT`, `  quit  ` and a blank line all print `bye!` and
      stop.
- [ ] No traceback appears for any of those.
- [ ] `calculator.py` has no `print` or `input` outside `_self_test`,
      and `main.py` has no arithmetic.
- [ ] `OPS` is a dict of functions with no parentheses after the names.
- [ ] Every function has type hints and a one-line docstring, and both
      files have a module docstring.
- [ ] Both files end with `if __name__ == "__main__":`.
- [ ] A comment at the top of `main.py` says which import form you chose
      and why.
- [ ] No `TODO` comments left.
- [ ] Committed with a message such as
      `Add Challenge 1: mini calculator module`.

## Stretch

**Two more operators, a memory, and a history.** `**` for powers and `%`
for remainders both take two numbers and return one, so they drop into
the table with no other change. `_` remembers the last answer, so you
can type `_ + 1`. And the history prints on the way out.

`calculator_stretch.py` imports the four you already have and adds two:

```python
"""Tiny arithmetic calculator (stretch: power and modulo)."""

from calculator import add, divide, multiply, subtract


def power(a: float, b: float) -> float:
    """Return a raised to the power b."""
    return a ** b


def modulo(a: float, b: float) -> float:
    """Return the remainder of a / b, refusing a zero divisor."""
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a % b


OPS = {"+": add, "-": subtract, "*": multiply, "/": divide, "**": power, "%": modulo}
```

Notice that the new module imports the old one and re-exports `OPS`.
Three files now, and the dependencies still point one way:
`main_stretch.py` → `calculator_stretch.py` → `calculator.py`. Nothing
points back.

`main_stretch.py`:

```python
"""Mini calculator REPL (stretch: ** and %, an `_` last-result name, history)."""

from calculator_stretch import OPS

BANNER = 'Mini calculator. Type "quit" to exit. `_` is the last result.'
PROMPT = "> "


def parse(line: str, last: float | None) -> tuple[float, str, float]:
    """Parse '2 + 3' into (2.0, '+', 3.0), resolving `_` to the last result."""
    parts = line.split()
    if len(parts) != 3:
        raise ValueError("expected exactly three whitespace-separated fields")
    left, op, right = parts
    if op not in OPS:
        raise ValueError(f"unknown operator {op!r}")
    return _number(left, last), op, _number(right, last)


def _number(token: str, last: float | None) -> float:
    """Turn one token into a float, treating `_` as the previous result."""
    if token == "_":
        if last is None:
            raise ValueError("no previous result yet")
        return last
    return float(token)


def main() -> None:
    """Run the REPL, remembering the last result and the full history."""
    print(BANNER)
    history: list[str] = []
    last: float | None = None
    while True:
        try:
            line = input(PROMPT).strip()
        except EOFError:
            print()
            break
        if line == "" or line.lower() == "quit":
            break
        try:
            left, op, right = parse(line, last)
            last = OPS[op](left, right)
        except ValueError:
            print(f'sorry, I did not understand "{line}". Use: <num1> <op> <num2>.')
            continue
        except ZeroDivisionError as exc:
            print(exc)
            continue
        history.append(f"{line} = {last}")
        print(last)
    if history:
        print("history:")
        for entry in history:
            print(f"  {entry}")
    print("bye!")


if __name__ == "__main__":
    main()
```

Two things worth sitting with. `last` is a plain local variable passed
into `parse` as a parameter — there is no `global` anywhere. A function
whose behaviour depends on something its callers cannot see is a
function you cannot reason about, and this is that argument at REPL
scale. And this version uses plain `input()` with its own `EOFError`
handler instead of `ask()`, which makes it shorter and means it can only
be run by hand. That trade is why the downloadable answer is written the
other way.

Verify:

```bash
printf '2 ** 10\n_ + 1\n17 %% 5\n_ / 0\nquit\n' | python main_stretch.py
```

```text
Mini calculator. Type "quit" to exit. `_` is the last result.
> 1024.0
> 1025.0
> 2.0
> cannot divide by zero
> history:
  2 ** 10 = 1024.0
  _ + 1 = 1025.0
  17 % 5 = 2.0
bye!
```

The `>` characters bunch up against the results because `input()` writes
its prompt with no trailing newline and piped input is never echoed
back. Type the same lines by hand and it looks normal. (The doubled `%%`
is `printf` needing an escape for a literal percent sign — the program
itself sees a single `%`.)

**Accepting `2+3` with no spaces — a stretch worth attempting and then
abandoning.** The brief's original suggestion was `shlex.split`. Try it
in the REPL before you rewrite anything:

```text
>>> import shlex
>>> shlex.split("2 + 3")
['2', '+', '3']
>>> shlex.split("2+3")
['2+3']
```

Identical to `str.split()` on the first, and useless on the second.
`shlex` splits shell-style quoted strings; it knows nothing about
arithmetic. If you really want `2+3`, the tool is `re`:

```python
import re

PATTERN = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*(\*\*|[-+*/%])\s*(-?\d+(?:\.\d+)?)\s*$")
```

Verified behaviour:

| input | groups |
|-------|--------|
| `2+3` | `('2', '+', '3')` |
| `  10 / 4 ` | `('10', '/', '4')` |
| `2**10` | `('2', '**', '10')` |
| `-3 * -4` | `('-3', '*', '-4')` |
| `1.5+2.25` | `('1.5', '+', '2.25')` |
| `17%5` | `('17', '%', '5')` |
| `hello` | no match |
| `2 ^ 3` | no match |

Regular expressions are Week 12, so this one is genuinely optional. The
part to take away now is the method: "use library X" is a guess, and the
way you check a guess is three lines in the REPL, before you rewrite
your parser around it.

When you are done, commit and move on to
[Challenge 2](./challenge-02-text-stats-package.md).
