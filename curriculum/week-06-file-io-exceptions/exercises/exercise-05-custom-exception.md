# Exercise 5 — Custom Exception

> **Topic:** defining a family of exceptions, raising them, and chaining with `raise ... from`
> **Lecture:** [03 — Exceptions and Logging](../lecture-notes/03-exceptions-and-logging.md)
> **Difficulty:** Medium
> **Target time:** 20 minutes
> **Why this one:** built-in exceptions describe Python's problems. `ValueError` tells a caller that something did not parse; it does not tell them which line of whose file was wrong. An exception you define carries your own facts, and a shared base class lets a caller catch everything your code raises with one clause. This is the pattern behind Challenge 02, the mini-project, and every library you will ever import.

## The Brief

Chapters check people in on a tablet at the door. The tablet adds one line to a
plain text file for each check-in: the chapter, the person's email, and how
many sessions they have attended this year, with a `|` between them. At the end
of the month somebody runs your parser over the file.

The tablet is not careful. One line lost its count field entirely. One has an
empty email because a volunteer tapped straight through. One has the word
`zero` where a number belongs. One has a negative count from a botched
correction.

Your parser must reject each bad line with a message precise enough that a
human can open the file, jump to that line number, and fix it — and then keep
going and parse the rest.

To do that you will define three exception types that share one base class.
The parser raises the specific type; `main` catches the base type. That split
is the whole lesson: **the code that knows what went wrong is not the code that
decides what to do about it.**

Three words before you start.

**`raise`.** How you make an exception happen on purpose. `raise
ValueError("nope")` builds the object and throws it.

**Base class and subclass.** `class MalformedLineError(CheckInError):` says
"a MalformedLineError *is a* CheckInError". So `except CheckInError:` catches
it, and so does `except MalformedLineError:`, and one clause can cover a whole
family.

**`super().__init__(...)`.** Calling the parent class's setup. Your class does
its own thing and then hands the rest up to the class it inherits from. Miss it
and the parent's work never happens.

## Starter

First, the data. Create `data/checkins.txt` with exactly these six lines. Line
4 has nothing between the two pipes, and line 5 has only two fields:

```text
lagos|ada.lovelace@example.org|3
manila|grace.hopper@example.org|1
bogota|katherine.johnson@example.org|zero
nairobi||2
quito|alan.turing@example.org
osaka|mary.jackson@example.org|-4
```

Now the code. Save this as `exercise-05-custom-exception.py`:

```python
"""exercise-05-custom-exception.py — parse a check-in log, reject bad lines loudly.

Defines a CheckInError family so callers can catch every parse failure with one
except clause and still learn exactly which line failed and why.
"""

import logging
from pathlib import Path

SOURCE = Path(__file__).parent / "data" / "checkins.txt"
FIELD_COUNT = 3

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s | %(message)s")
log = logging.getLogger(__name__)


class CheckInError(Exception):
    """Base class for every failure while parsing a check-in line."""

    def __init__(self, line_number: int, raw: str, message: str) -> None:
        super().__init__(f"line {line_number}: {message}")
        self.line_number = line_number
        self.raw = raw


class MalformedLineError(CheckInError):
    """Raised when a line does not split into exactly FIELD_COUNT fields."""


class MissingFieldError(CheckInError):
    """Raised when a required field is present but empty."""


class InvalidCountError(CheckInError):
    """Raised when the check-in count is not a non-negative whole number."""


def parse_line(line_number: int, raw: str) -> tuple[str, str, int]:
    """Parse one pipe-delimited check-in line.

    Returns:
        A ``(chapter, email, count)`` triple.

    Raises:
        MalformedLineError: wrong number of fields.
        MissingFieldError: chapter or email is empty.
        InvalidCountError: count is not a whole number, or is negative.
    """
    line = raw.rstrip("\n")
    fields = line.split("|")
    # TODO: raise MalformedLineError unless there are exactly FIELD_COUNT fields
    chapter, email, count_text = fields
    # TODO: raise MissingFieldError when chapter or email is empty
    # TODO: convert count_text with int(); on ValueError raise InvalidCountError
    #       from the original exception
    # TODO: raise InvalidCountError when the count is negative
    return chapter, email, 0


def main() -> None:
    """Parse every line, print the good ones, log the bad ones."""
    accepted = 0
    total = 0
    with SOURCE.open("r", encoding="utf-8") as f:
        for line_number, raw in enumerate(f, start=1):
            total += 1
            # TODO: parse the line; print it on success, log the failure on
            #       CheckInError and carry on to the next line
    print(f"{accepted} of {total} lines accepted; {total - accepted} rejected")


if __name__ == "__main__":
    main()
```

Notice what the base class already does for you. Its `__init__` demands three
things — a line number, the raw text, and a message — builds the sentence
`line 3: ...` once, and hands that sentence up to `Exception`. Every raise site
in the file is then *forced* to supply a line number, because the constructor
will not run without one. A rule the language enforces beats a rule in a
docstring.

Notice too that the three subclasses contain a docstring and nothing else. That
is not laziness. They exist to be **names**, so `type(e).__name__` is
informative and so a future caller who wants to treat one kind specially can.

## Requirements

1. All three specific exceptions inherit from `CheckInError`, which inherits
   from `Exception` — never from `BaseException`.
2. `str(error)` is `line <n>: <message>`, because the base `__init__` passes
   that string to `super().__init__`. So
   `str(MissingFieldError(4, "nairobi||2", "email is empty"))` is exactly
   `line 4: email is empty`.
3. Every raised error carries `.line_number` and `.raw`. `.raw` is the original
   line with the trailing newline removed.
4. The four messages are exactly:
   `check-in count 'zero' is not a whole number`,
   `email is empty`,
   `expected 3 fields, found 2`,
   `check-in count -4 is negative`.
5. `InvalidCountError` for the `'zero'` case is raised **`from`** the
   `ValueError` that `int()` produced. The error for the negative count is
   raised with no `from`, because nothing failed underneath it — your rule
   rejected a value that parsed perfectly.
6. `main` has exactly one `except CheckInError as e:` clause. Three separate
   handlers would work and would miss the entire point of the base class.
7. Accepted rows print with `f"{chapter:<8} {email:<32} {count:>3}"`.
8. The last printed line is `2 of 6 lines accepted; 4 rejected`.
9. The script exits normally. Bad data is not a crash.

## Constraints

- **Name every exception class with an `Error` suffix and give it a
  docstring.** The suffix is a convention readers rely on to spot a raisable
  type at a glance, and the docstring is the only place the raising rule gets
  written down.
- **Call `super().__init__(...)` in your base `__init__`.** The message you
  hand to `Exception.__init__` is what `str(e)` returns and what a traceback
  prints. Set `self.message` instead and skip the `super()` call, and your
  handler logs an empty string — the error becomes invisible in the exact
  moment you needed to see it.
- **Raise the specific subclass; catch the base class.** The parser knows the
  precise fault, so it raises `MissingFieldError`. `main` treats all four the
  same way — log it, skip the line — so it catches `CheckInError` once. When a
  fifth failure mode appears next month, `main` needs no edit at all.
- **Use `raise ... from e` when you convert somebody else's exception.** The
  `ValueError` from `int()` is real evidence about the cause. `from e` keeps it
  in the traceback under "the direct cause of the following exception"; leave
  it out and you throw away the only record of what actually broke.
- **Do not catch `ValueError` in `main`.** `InvalidCountError` is not a
  `ValueError` subclass here, and that is deliberate: a caller of your parser
  should not have to know that `int()` is what you happen to use inside it.
- **Number lines with `enumerate(f, start=1)`.** Text editors count from one. A
  parser that reports "line 2" about the third line sends a human to the wrong
  place, which is worse than giving no line number at all, because they will
  believe it.
- **`rstrip("\n")` before splitting.** The trailing newline rides along on the
  last field of every line, so `count_text` would be `"3\n"`. `int("3\n")`
  happens to work, because `int` tolerates surrounding whitespace — which is
  precisely how this bug hides until the day something compares that field to a
  string and gets a `False` nobody can explain. Use `rstrip("\n")` and not
  `.strip()`, so that meaningful spaces inside the first and last fields
  survive.

## Expected output

This program writes to two streams. The accepted rows and the tally go to
standard output; the rejections go to standard error through `logging`.

**Standard output.** Real stdout from the shipped file, captured on CPython
3.13.2:

```text
$ python exercise-05-custom-exception.py > accepted.txt
lagos    ada.lovelace@example.org           3
manila   grace.hopper@example.org           1
2 of 6 lines accepted; 4 rejected
```

**Standard error:**

```text
WARNING  | rejected InvalidCountError: line 3: check-in count 'zero' is not a whole number
WARNING  | rejected MissingFieldError: line 4: email is empty
WARNING  | rejected MalformedLineError: line 5: expected 3 fields, found 2
WARNING  | rejected InvalidCountError: line 6: check-in count -4 is negative
```

Both together, in one terminal:

```text
$ python exercise-05-custom-exception.py 2>&1
lagos    ada.lovelace@example.org           3
manila   grace.hopper@example.org           1
WARNING  | rejected InvalidCountError: line 3: check-in count 'zero' is not a whole number
WARNING  | rejected MissingFieldError: line 4: email is empty
WARNING  | rejected MalformedLineError: line 5: expected 3 fields, found 2
WARNING  | rejected InvalidCountError: line 6: check-in count -4 is negative
2 of 6 lines accepted; 4 rejected
```

The `flush=True` on the accepted-row print is what makes that interleaving
reproducible. Without it, stdout is held in a buffer whenever it is not a
terminal, and the two accepted rows would appear *after* all four warnings.
`python -u` is the other way to get the same effect. The text of each line is
what matters; the order the two streams land in is a property of buffering.

Four messages, character for character as the spec requires, each naming its
line. Look at the quoting difference between line 3 and line 6: `'zero'` is
quoted because `{count_text!r}` renders a string with its quote marks, while
`-4` is bare because by then it is an `int`. That is not decoration — it tells
the reader whether the parser was looking at text or at a number when it
objected.

Now delete the `except CheckInError` clause from `main` and run it again. Line
3 crashes the script, and the traceback proves your chaining works. Your line
numbers will differ:

```text
lagos    ada.lovelace@example.org           3
manila   grace.hopper@example.org           1
Traceback (most recent call last):
  File "ex5-nocatch.py", line 63, in parse_line
    count = int(count_text)
ValueError: invalid literal for int() with base 10: 'zero'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "ex5-nocatch.py", line 91, in <module>
    main()
    ~~~~^^
  File "ex5-nocatch.py", line 84, in main
    chapter, email, count = parse_line(line_number, raw)
                            ~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "ex5-nocatch.py", line 65, in parse_line
    raise InvalidCountError(
    ...<3 lines>...
    ) from e
InvalidCountError: line 3: check-in count 'zero' is not a whole number
```

Two tracebacks, joined by "the direct cause of". The original `ValueError` on
top, your own error below it, both preserved. A maintainer reading that knows
both that the count was rejected *and* that `int()` is what rejected it. Put
the `except` clause back when you have seen it.

## Steps

1. Create `data/checkins.txt` exactly as given.
2. Save the starter and define nothing new yet — run it once to confirm the
   file loads and six lines are counted.
3. Implement the field-count check and the empty-field checks. Run. Two
   rejections should already appear.
4. Implement the `int()` conversion with `raise InvalidCountError(...) from e`.
   Run.
5. Implement the negative check last, and notice it needs no `try` at all.
   Nothing failed; you are simply refusing a value.
6. Fill in `main`'s single `except CheckInError as e:` and log with
   `log.warning("rejected %s: %s", type(e).__name__, e)`.
7. Remove the `except` clause, run once to read the chained traceback, then put
   it back.
8. Switch `level=logging.INFO` to `level=logging.DEBUG` and add
   `log.debug("raw line: %r", e.raw)` inside the handler. That is what `.raw`
   is for: the message says what is wrong, the attribute lets a maintainer see
   the actual characters.

## The Solution

```python
"""exercise-05-custom-exception-solution.py — parse a check-in log, reject bad lines loudly.

Defines a CheckInError family so callers can catch every parse failure with one
except clause and still learn exactly which line failed and why. Accepted rows
go to stdout; rejections go to stderr through the logging module.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact check-in log the page
gives you, so the download runs on any machine with nothing set up beforehand.

Every accepted row is printed with flush=True so that a combined
`python ... 2>&1` transcript interleaves the way the page shows it, instead of
holding the report in a buffer until the program ends.

Run it with::

    python exercise-05-custom-exception-solution.py
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

FIELD_COUNT = 3

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s | %(message)s")
log = logging.getLogger(__name__)

#: The check-in log exactly as the exercise page gives it. Line 4 has nothing
#: between the two pipes and line 5 has only two fields.
SAMPLE_CHECKINS = (
    "lagos|ada.lovelace@example.org|3\n"
    "manila|grace.hopper@example.org|1\n"
    "bogota|katherine.johnson@example.org|zero\n"
    "nairobi||2\n"
    "quito|alan.turing@example.org\n"
    "osaka|mary.jackson@example.org|-4\n"
)


class CheckInError(Exception):
    """Base class for every failure while parsing a check-in line."""

    def __init__(self, line_number: int, raw: str, message: str) -> None:
        super().__init__(f"line {line_number}: {message}")
        self.line_number = line_number
        self.raw = raw


class MalformedLineError(CheckInError):
    """Raised when a line does not split into exactly FIELD_COUNT fields."""


class MissingFieldError(CheckInError):
    """Raised when a required field is present but empty."""


class InvalidCountError(CheckInError):
    """Raised when the check-in count is not a non-negative whole number."""


def parse_line(line_number: int, raw: str) -> tuple[str, str, int]:
    """Parse one pipe-delimited check-in line.

    Returns:
        A ``(chapter, email, count)`` triple.

    Raises:
        MalformedLineError: wrong number of fields.
        MissingFieldError: chapter or email is empty.
        InvalidCountError: count is not a whole number, or is negative.
    """
    line = raw.rstrip("\n")
    fields = line.split("|")
    if len(fields) != FIELD_COUNT:
        raise MalformedLineError(
            line_number,
            line,
            f"expected {FIELD_COUNT} fields, found {len(fields)}",
        )
    chapter, email, count_text = fields
    if not chapter:
        raise MissingFieldError(line_number, line, "chapter is empty")
    if not email:
        raise MissingFieldError(line_number, line, "email is empty")
    try:
        count = int(count_text)
    except ValueError as e:
        raise InvalidCountError(
            line_number,
            line,
            f"check-in count {count_text!r} is not a whole number",
        ) from e
    if count < 0:
        raise InvalidCountError(
            line_number, line, f"check-in count {count} is negative"
        )
    return chapter, email, count


def parse_file(source: Path) -> None:
    """Parse every line of *source*, print the good ones, log the bad ones."""
    accepted = 0
    total = 0
    with source.open("r", encoding="utf-8") as f:
        for line_number, raw in enumerate(f, start=1):
            total += 1
            try:
                chapter, email, count = parse_line(line_number, raw)
            except CheckInError as e:
                log.warning("rejected %s: %s", type(e).__name__, e)
                continue
            accepted += 1
            print(f"{chapter:<8} {email:<32} {count:>3}", flush=True)
    print(f"{accepted} of {total} lines accepted; {total - accepted} rejected")


def build_sample(folder: Path) -> Path:
    """Write the sample check-in log into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "checkins.txt"
    path.write_text(SAMPLE_CHECKINS, encoding="utf-8")
    return path


def main() -> None:
    """Build the sample check-in log and parse it."""
    with tempfile.TemporaryDirectory() as workspace:
        parse_file(build_sample(Path(workspace) / "data"))


if __name__ == "__main__":
    main()
```

**The base class holds the constructor and the subclasses hold nothing but a
docstring.** `CheckInError.__init__` builds the `line <n>: <message>` string
once, hands it to `Exception.__init__`, and stores the two attributes — and all
three subclasses inherit every bit of that. A subclass that defines its own
`__init__` inherits none of it unless it calls `super()`, so the moment you
start writing one, ask what it is adding. Here the answer is nothing.
`MalformedLineError` and `MissingFieldError` differ in no behaviour at all,
only in what they mean.

**`super().__init__(f"line {line_number}: {message}")` is what makes the error
visible.** `str(e)` is not magic and it does not read your attributes. It comes
from the arguments you passed up to `Exception.__init__`. That single call is
why `log.warning("rejected %s: %s", type(e).__name__, e)` prints a sentence
instead of a blank, and why an *unhandled* one prints a useful last line in the
traceback.

**`.line_number` and `.raw` are structured data, not decoration.** The message
string is for a human reading a log. The attributes are for a program: a
handler can sort rejects by line, or write them out as JSON, or print `e.raw`
at `DEBUG` level when somebody needs to see the actual characters. Putting the
same facts in both forms is deliberate — text for the person, fields for the
code — and it costs two assignments.

**The guard order is forced by what each check needs to already be true.**
`len(fields) != FIELD_COUNT` has to run before
`chapter, email, count_text = fields`, because unpacking a two-item list into
three names raises `ValueError: not enough values to unpack (expected 3, got 2)`
and the entire point of `MalformedLineError` is to produce a useful error
instead of that one. The empty-field checks come next, because they need the
names bound. The `int()` conversion comes after that, because it needs
`count_text`. The negative check comes last, because it needs an actual `int`
to compare. Each guard sits at the first point where it *can* run, which is
also the last point before something worse happens.

**`raise ... from e` on the conversion, and no `from` on the negative check.**
These are two different situations and the difference is the point.
`int("zero")` genuinely failed, and its `ValueError` is real evidence, so
`from e` records it as the cause. The negative count is not like that:
`int("-4")` succeeded perfectly. Nothing failed underneath; your rule rejected
a value that parsed fine. There is no cause to point at, so there is no `from`.
Ask yourself, at every `raise` inside an `except`, whether you are translating
somebody else's failure or reporting your own judgement.

**`InvalidCountError` is not a `ValueError` subclass, on purpose.** It would be
easy to inherit from `ValueError` so that existing handlers catch it. Resist
it. Callers of `parse_line` should not have to know that `int()` is what you
happen to use inside — that is an implementation detail you might replace
tomorrow with a regular expression or a decimal parser. The contract is
`CheckInError`; everything else is yours to change.

**One `except CheckInError` in `main`.** Four distinct failures, one handler,
because `main`'s policy for all four is identical: log it, skip the line, keep
going. Three separate `except` clauses would be three places to edit when the
fifth failure mode arrives, and the base class exists precisely so that it is
zero places. The `continue` after the log is what makes "keep going" literal,
and `accepted += 1` sits after the `try` so that only a line which actually
parsed can be counted.

**About the harness.** `SAMPLE_CHECKINS` and `build_sample` exist so this
download runs on a machine where you have created nothing. `parse_file` is your
`main` with the path passed in as an argument. Everything from `CheckInError`
to `parse_line` is the exercise.

## Run it

Copy the worked answer on this page into `exercise-05-custom-exception.py` and run it:

```bash
python exercise-05-custom-exception.py
```

It needs no `data/` folder: it writes its own copy of the check-in log into a
temporary directory, parses it, and cleans up after itself. The `-solution` in
the name keeps it from colliding with your own
`exercise-05-custom-exception.py`.

## Common bugs to catch

- **The log line reads `rejected MissingFieldError:` with nothing after the
  colon.**

  ```text
  WARNING  | rejected MissingFieldError: 
  ```

  Your class sets `self.message` and calls `super().__init__()` with no
  arguments, so `.args` is empty and `str(e)` is the empty string. An invisible
  error, in the exact moment you needed to see it. Leave the `super()` call out
  entirely and it is only slightly better — `Exception` stores the constructor
  arguments in `.args`, so you get the raw tuple where a sentence belongs:

  ```text
  WARNING  | rejected MissingFieldError: (4, 'nairobi||2', 'email is empty')
  ```

  Pass the formatted message up. `str(e)` is whatever you hand to
  `Exception.__init__`, and nothing else.

- **`TypeError: CheckInError.__init__() missing 2 required positional
  arguments: 'raw' and 'message'`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 9, in <module>
      raise MalformedLineError('expected 3 fields, found 2')
            ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: CheckInError.__init__() missing 2 required positional arguments: 'raw' and 'message'
  ```

  You raised with just a message. Your base class demands three arguments, so
  every raise site has to supply all three. That is the constructor doing its
  job: it is impossible to raise a `CheckInError` that does not know which line
  it came from.

- **`AttributeError: 'InvalidCountError' object has no attribute
  'line_number'`.** A subclass defined its own `__init__` and never called
  `super().__init__(...)`, so the base class never got to set the attributes.
  The handler works fine right up until something touches `.line_number` —
  often weeks later, in the stretch-goal code that writes rejects to JSON.
  These subclasses should contain a docstring and nothing else.

- **`ValueError: not enough values to unpack (expected 3, got 2)` on line 5.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 3, in <module>
      chapter, email, count_text = fields
      ^^^^^^^^^^^^^^^^^^^^^^^^^^
  ValueError: not enough values to unpack (expected 3, got 2)
  ```

  You unpacked before checking the field count, so the guard never runs. Look
  at what that error does not tell you: not which file, not which line of it,
  not what was expected in the org's terms. Turning it into
  `line 5: expected 3 fields, found 2` is the whole reason `MalformedLineError`
  exists.

- **`ValueError: invalid literal for int() with base 10: 'zero'` reaches the
  terminal.** Your `except ValueError` is missing, or it is around the wrong
  line, or you wrote `raise InvalidCountError(...)` outside the `except` block
  so there was nothing to chain from.

- **The traceback says "During handling of the above exception, another
  exception occurred" instead of "the direct cause of".** You raised inside the
  `except` block but left off `from e`. Both chain — Python keeps the original
  either way — but the first is Python's careful way of saying "these two
  happened near each other and I do not know whether that is related". `from e`
  states that the first *caused* the second. On a two-line function the
  difference is cosmetic. In a handler with twenty lines of cleanup, where the
  second exception might be an unrelated bug in your cleanup code, it is the
  difference between a five-minute diagnosis and an hour of one.

- **`osaka` is accepted with a count of `-4`.** You tested
  `count_text.startswith("-")` on the string instead of `count < 0` on the
  integer. It happens to work on `"-4"` and fails on `" -4"`, which `int`
  accepts as `-4` while `startswith` says `False`. Convert first, then compare
  numbers. A rule about a *quantity* belongs after the value is a quantity.

- **Every line number is one too low.** `enumerate(f)` starts at `0`. Pass
  `start=1`. The rejection messages then become confidently wrong, which is
  worse than being absent: a human opens line 2, finds a perfectly good record,
  and concludes your parser is broken.

## Under the hood

<details>
<summary>Under the hood — the exception tree, and where your family hangs off it</summary>

Every exception in Python is an object, and every one of them inherits from
`BaseException`. The tree matters because `except` matches by inheritance: a
clause catches its type and everything below it.

The top of the tree:

```text
BaseException
 ├── SystemExit                 <- sys.exit() raises this
 ├── KeyboardInterrupt          <- Ctrl-C raises this
 ├── GeneratorExit
 └── Exception                  <- everything you should normally catch
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── KeyError
      │    └── IndexError
      ├── OSError
      │    ├── FileNotFoundError
      │    └── PermissionError
      └── ValueError
           └── UnicodeError
                └── UnicodeDecodeError
```

Three facts fall straight out of that shape.

**Why `except Exception:` and not `except BaseException:`.** The three types
above `Exception` are not errors. They are control flow — the interpreter
saying "stop now" on the user's behalf. Catching them means your program
ignores Ctrl-C and ignores `sys.exit()`. `Exception` was deliberately put one
level down so that "catch everything that went wrong" and "catch everything"
could be different requests.

**Why clause order matters.** Python tries clauses top to bottom and takes the
first that matches, so a broad clause above a narrow one makes the narrow one
dead code that never runs and never warns you:

```python
except OSError as e:              # matches PermissionError too
    log.warning("filesystem: %s", e)
except PermissionError:           # never reached
    log.warning("permission denied")
```

Challenge 01 is built on exactly this, and it is the most common way that
challenge fails.

**Why `UnicodeDecodeError` is not an `OSError`.** Look where it sits: under
`ValueError`, in a completely different branch. Reading a file is two steps —
the operating system hands over bytes, then Python decodes them — and only the
first can raise `OSError`. A `.py` file full of Latin-1 bytes opens perfectly
and fails on the read. Catch `OSError` alone and one such file takes down your
whole walk.

**Where your family goes.** `CheckInError` inherits from `Exception` directly,
which is right: it is not a kind of `ValueError`, not a kind of `OSError`, it
is a kind of *your problem*. That is the same shape every library uses.
`requests` has `RequestException` with `HTTPError` and `ConnectionError` under
it. `json` has `JSONDecodeError`, and that one *does* inherit from
`ValueError` — because it was added to a module whose users had been catching
`ValueError` around `json.loads` for years, and breaking them was not worth it.
Inheriting from a built-in is a compatibility decision, and if you have no
existing callers to keep happy, `Exception` is the honest parent.

**One more thing you can do with a base class**, which is worth knowing before
you need it:

```text
>>> try:
...     raise MissingFieldError(4, "nairobi||2", "email is empty")
... except CheckInError as e:
...     print(type(e).__name__, "|", e, "|", e.line_number)
...
MissingFieldError | line 4: email is empty | 4
```

One clause, and the handler still has the specific class name and the
structured fields. You did not have to give up precision to gain simplicity —
that is the trade this design refuses to make.

</details>

<details>
<summary>Under the hood — how chaining is stored, and how to switch it off</summary>

"Chaining" is not a formatting trick in the traceback printer. It is two real
attributes on the exception object, and you can look at them.

**`__context__` is set automatically.** Raise anything inside an `except`
block and Python quietly records what you were handling:

```text
>>> try:
...     try:
...         int("zero")
...     except ValueError:
...         raise RuntimeError("could not parse")
... except RuntimeError as e:
...     print("context:", repr(e.__context__))
...     print("cause:  ", repr(e.__cause__))
...
context: ValueError("invalid literal for int() with base 10: 'zero'")
cause:   None
```

`__context__` is filled in; `__cause__` is empty. That is what produces
**"During handling of the above exception, another exception occurred"** — a
careful, non-committal sentence, because Python genuinely does not know whether
the second error was caused by the first or was an unrelated bug in your
handler.

**`from e` sets `__cause__`, and that is a claim you are making:**

```text
>>> try:
...     try:
...         int("zero")
...     except ValueError as err:
...         raise RuntimeError("could not parse") from err
... except RuntimeError as e:
...     print("cause:  ", repr(e.__cause__))
...
cause:   ValueError("invalid literal for int() with base 10: 'zero'")
```

Now the traceback says **"The above exception was the direct cause of the
following exception"**. Same two objects, same information — a different
sentence to the person reading it at two in the morning.

**And `from None` deliberately hides the cause.** Setting `__suppress_context__`
stops the printer showing the original entirely:

```text
>>> try:
...     try:
...         int("zero")
...     except ValueError:
...         raise RuntimeError("could not parse") from None
... except RuntimeError as e:
...     print("suppressed:", e.__suppress_context__)
...
suppressed: True
```

That is a real tool, not vandalism, and the standard library uses it. The
`json` module raises its `JSONDecodeError` with `from None` so that you see the
message that helps you — `Expecting value: line 1 column 1 (char 0)` — instead
of the internal `StopIteration` that happened to be underneath. Use it when the
underlying exception is an implementation detail of your own code that would
only mislead a reader. Never use it to make a traceback look tidier.

**A note on the newer piece.** Since Python 3.11 there is also
`ExceptionGroup`, and `except*` to match inside one, for when several things
fail at once — the shape you get from concurrent code where four tasks each
raised something different. You will not need it this week. It is worth knowing
the name so that the syntax `except*` is not a mystery when you meet it.

</details>

## Acceptance checklist

- [ ] Three exception classes, all inheriting from one `CheckInError` base.
- [ ] `main` catches `CheckInError` exactly once and never crashes.
- [ ] All four rejection messages match the spec character for character.
- [ ] The `'zero'` failure is chained with `from` and shows a two-part traceback.
- [ ] `e.line_number` and `e.raw` are populated on every raised error.
- [ ] The final line reads `2 of 6 lines accepted; 4 rejected`.
- [ ] Adding a seventh bad line to the file needs no change to `main` at all.
- [ ] The exit code is `0`.
- [ ] Committed to Git with a message like `Add Week 6 exercise 5: custom exception family`.

## Stretch

- Add a `to_dict()` method on `CheckInError` returning
  `{"line": ..., "error": type(self).__name__, "message": str(self)}`, collect
  the rejects in a list, and write them to `data/rejects.json` with
  `json.dump`. You now have a machine-readable error report, which is what
  Exercise 3 was preparing you for.

- Add a `DuplicateCheckInError` for an email that appears twice in the file.
  Then confirm that `main` handles it with no edits at all. That confirmation
  is the payoff for everything on this page.

- Write the parser's failure cases as a `test_parse_line()` function using
  `try`/`except`/`else` — raise `AssertionError` in the `else` branch when the
  expected exception did not happen. Week 11 replaces that shape with
  `pytest.raises`, and you will recognise it immediately.

That is Week 6's exercises. Take the two longer problems next:
[Challenges](../challenges/README.md).
