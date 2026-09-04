# Exercise 4 — Safe Divide

> **Topic:** `try`/`except` with narrow exception types, and reporting through `logging` instead of `print`
> **Lecture:** [03 — Exceptions and Logging](../lecture-notes/03-exceptions-and-logging.md)
> **Difficulty:** Easy
> **Target time:** 20 minutes
> **Why this one:** a job that dies on row four of six is worse than useless. It did part of the work and told you almost nothing about why it stopped. This is the pattern for every batch job you will ever write: deal with the failure of one item, say clearly which item it was, and keep going. It is also the first time you use `logging` instead of `print`, and once you see the difference you will not go back.

## The Brief

Every chapter of the org reports two numbers at the end of the quarter: how
many people came in total, and how many sessions they held. Average attendance
per session is the first number divided by the second, and the report you are
writing prints it for every chapter.

The data is real data, which means it is dirty. Four different ways, on
purpose:

- **Bogota** registered but has not run a session yet. Its bottom number is
  zero, and dividing by zero is not a hard sum — it is a question with no
  answer.
- **Nairobi** has the word `three` typed into the sessions column, because
  somebody filled the form in by hand.
- **Quito** left the field empty.
- **Osaka** held four sessions and nobody came. Its average is a real, honest
  `0.00`, and it is in the file to catch a specific mistake you are about to be
  warned off.

Your report must print a line for all six chapters, say clearly which ones it
could not work out, and finish with a count of the usable ones. It must never
crash.

Two words before you start.

**Exception.** When Python cannot do what you asked, it stops and raises an
exception — a small object naming what went wrong. If nobody catches it, it
travels up through every function that was waiting, prints a traceback, and
ends the program.

**`try`/`except`.** `try:` marks code that might fail. `except SomeError:`
marks what to do if that particular kind of failure happens. The program
carries on afterwards instead of ending.

## Starter

First, the data. Create `data/chapter-totals.csv`. The trailing comma on the
Quito line is deliberate — that is an empty field, not a typo:

```text
chapter,attendees,sessions
Lagos,180,12
Manila,64,8
Bogota,0,0
Nairobi,45,three
Quito,90,
Osaka,0,4
```

Now the code. Save this as `exercise-04-safe-divide.py`:

```python
"""exercise-04-safe-divide.py — a report that survives bad rows.

Reads data/chapter-totals.csv and prints average attendance per session for
each chapter. Rows that cannot be computed are logged and reported as "--".
"""

import csv
import logging
from pathlib import Path

SOURCE = Path(__file__).parent / "data" / "chapter-totals.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
log = logging.getLogger(__name__)


def safe_divide(numerator: float, denominator: float, label: str) -> float | None:
    """Return numerator / denominator, or None when the division is impossible.

    *label* names the thing being divided so the log line is searchable.
    Logs a warning for a zero denominator and an error for non-numeric input.
    """
    # TODO: try the division
    # TODO: except ZeroDivisionError -> log.warning(...) and return None
    # TODO: except TypeError -> log.error(...) and return None
    return None


def average_attendance(row: dict[str, str]) -> float | None:
    """Return the average attendance for one CSV row, or None if it is unusable."""
    chapter = row["chapter"]
    # TODO: convert row["attendees"] to int; on ValueError log an error, return None
    # TODO: convert row["sessions"] to int; on ValueError log an error, return None
    # TODO: return safe_divide(attendees, sessions, chapter)
    return None


def main() -> None:
    """Print the attendance report and a summary count."""
    with SOURCE.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    log.info("read %d rows from %s", len(rows), SOURCE.name)

    usable = 0
    for row in rows:
        average = average_attendance(row)
        # TODO: count the usable ones and format them to two decimal places;
        #       show "--" for the rest. Careful: 0.00 is a usable result.
        text = "--"
        print(f"{row['chapter']:<10} {text:>6}", flush=True)

    # Deliberate mistake, so you can watch the TypeError branch fire:
    safe_divide("64", 8, "unconverted string")

    log.info("%d of %d chapters had a usable average", usable, len(rows))


if __name__ == "__main__":
    main()
```

Four names from that starter.

**`logging`.** The standard library's way of saying things that are *about* the
program rather than *from* the program. Every message has a level, a timestamp
and a source, and it goes to standard error rather than standard output.

**Level.** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`, in that order of
seriousness. You set one level and everything below it goes quiet. That dial is
the whole reason to use `logging` instead of `print`.

**stdout and stderr.** Two separate streams out of every program. Standard
output is the answer; standard error is the commentary. They are separate so
you can save one without the other, which is what `python report.py >
report.txt` is doing.

**`flush=True`.** Force a printed line out immediately instead of letting it
sit in a buffer. It matters here for a reason explained under Expected output.

## Requirements

1. All six chapters get exactly one printed line, in file order.
2. Usable averages print with two decimal places, right-aligned in six columns:
   Lagos `15.00`, Manila `8.00`, Osaka `0.00`.
3. Unusable rows print `--` in the same column.
4. Osaka's `0.00` is a **result**, not a failure. It counts toward `usable`.
5. Bogota logs at `WARNING` — a zero denominator is a fact about the data and
   the program carries on. Nairobi and Quito log at `ERROR` — text where a
   number belongs is a data-entry fault somebody has to go and fix.
6. Each log line names the chapter and quotes the offending value:
   `Nairobi: sessions value 'three' is not a whole number`.
7. The final log line is `3 of 6 chapters had a usable average`.
8. The script exits normally. No traceback, and an exit code of `0`.

## Constraints

- **Catch `ZeroDivisionError` and `TypeError` separately, and never write a
  bare `except:`.** The two mean different things: a zero denominator is a fact
  about the data, a `TypeError` is a bug in your code that has reached runtime.
  A bare `except` also catches `KeyboardInterrupt`, so your script would ignore
  Ctrl-C. Catch the narrowest type that names what you actually expect.
- **Wrap only the risky line in the `try`.** Wrap the whole function and a
  `KeyError` from a misspelled column name gets swallowed and reported as a
  data problem, when it is a code problem.
- **Return `None` for "no result", never `0`.** Zero is a legal average — Osaka
  earned it. If failures also returned `0`, then `0.00` in the report would
  mean either "nobody came" or "the row was broken", and no reader could tell
  which.
- **Test for it with `if average is None:`, not `if not average:`.** `0.0` is
  falsy in Python, so the truthiness test throws Osaka's real answer away
  without a word. This is the single most common way this exercise goes wrong,
  and Osaka exists to catch it.
- **Use `logging` for the failures, not `print`.** The six report lines are the
  program's *result* and belong on stdout. The failure notices are
  *diagnostics*: they need a severity and a timestamp, they belong on stderr,
  and somebody must be able to silence them by turning one dial.
- **Pass log arguments lazily: `log.error("%s: bad value %r", chapter, value)`,
  not an f-string.** The substitution only happens if the message is actually
  emitted, so a `DEBUG` call inside a hot loop costs nothing at `INFO` level.
  It also keeps the message template constant across every call, which is what
  log-searching tools group on.
- **Call `basicConfig` once, at module level, before anything logs.** The first
  log call installs a default handler if none exists, and `basicConfig` does
  nothing at all after that. A late call fails silently.

## Expected output

This program writes to two streams, so there are two things to look at.

**Standard output** — the report itself. Real stdout from the shipped file,
captured on CPython 3.13.2:

```text
$ python exercise-04-safe-divide.py > report.txt
Lagos       15.00
Manila       8.00
Bogota         --
Nairobi        --
Quito          --
Osaka        0.00
```

That is what lands in `report.txt`. Six lines, one per chapter, and nothing
else — no timestamps, no warnings, nothing a spreadsheet would choke on.

**Standard error** — the commentary. Your timestamps will differ:

```text
2026-08-23 23:51:37,184 | INFO     | __main__ | read 6 rows from chapter-totals.csv
2026-08-23 23:51:37,185 | WARNING  | __main__ | Bogota: denominator is zero; average is undefined
2026-08-23 23:51:37,185 | ERROR    | __main__ | Nairobi: sessions value 'three' is not a whole number
2026-08-23 23:51:37,185 | ERROR    | __main__ | Quito: sessions value '' is not a whole number
2026-08-23 23:51:37,185 | ERROR    | __main__ | unconverted string: cannot divide '64' by 8
2026-08-23 23:51:37,185 | INFO     | __main__ | 3 of 6 chapters had a usable average
```

Run it with no redirection and both streams arrive at your terminal together,
interleaved:

```text
$ python exercise-04-safe-divide.py 2>&1
2026-08-23 23:51:50,811 | INFO     | __main__ | read 6 rows from chapter-totals.csv
Lagos       15.00
Manila       8.00
2026-08-23 23:51:50,811 | WARNING  | __main__ | Bogota: denominator is zero; average is undefined
Bogota         --
2026-08-23 23:51:50,811 | ERROR    | __main__ | Nairobi: sessions value 'three' is not a whole number
Nairobi        --
2026-08-23 23:51:50,811 | ERROR    | __main__ | Quito: sessions value '' is not a whole number
Quito          --
Osaka        0.00
2026-08-23 23:51:50,811 | ERROR    | __main__ | unconverted string: cannot divide '64' by 8
2026-08-23 23:51:50,811 | INFO     | __main__ | 3 of 6 chapters had a usable average
```

**That interleaving is the reason the starter has `flush=True` on the print.**
Without it, stdout is *block-buffered* whenever it is not a terminal: Python
collects the report lines in memory and empties them out in one go when the
program ends. `logging` flushes every record immediately. So the two streams
arrive out of order — all six log lines first, then all six report lines in a
block — and the transcript above would be a lie. Adding `flush=True` makes each
report line leave as soon as it is produced, and the interleaving becomes
something you can reproduce.

If you meet this in somebody else's script that does not flush, the other lever
is `python -u`, which turns stdout buffering off for the whole run. Being able
to name the cause is worth more than either fix: the order two streams arrive
in is a property of buffering, not of your code.

Read the report against the log, line by line. Bogota, Nairobi and Quito each
have a log line explaining themselves. Osaka has none — it did not fail. It
just had a very quiet quarter.

## Steps

1. Create `data/chapter-totals.csv` exactly as given, empty Quito field
   included.
2. Save the starter and run it before writing any code. Six `--` lines and one
   `INFO` line prove your wiring works.
3. Implement `safe_divide`. Check both branches in a REPL by calling it with
   `(1, 0, "t")` and `("1", 2, "t")`.
4. Implement `average_attendance`, one conversion at a time. Run after each.
5. Fill in the `main` loop. Format with `f"{average:.2f}"`.
6. Run it and look at Osaka. If Osaka shows `--`, you used a truthiness test.
   Go and fix it now, before the habit sets.
7. Prove the streams are separate:
   `python exercise-04-safe-divide.py > report.txt`. The table lands in the
   file; the log lines stay on your terminal. That split is the practical
   argument for `logging`: the result of the program and the story of the
   program go to different places, so you can capture one without ruining the
   other.
8. Turn the dial. Change `level=logging.INFO` to `level=logging.ERROR` and
   re-run. Bogota's warning disappears, both `INFO` lines disappear, the two
   `ERROR` lines stay, and the six-line table is completely untouched because
   it never went through `logging` at all. One word, and the noise level
   changed. That is what `print` can never give you.

## The Solution

```python
"""exercise-04-safe-divide-solution.py — a report that survives bad rows.

Reads a chapter-totals export and prints average attendance per session for
each chapter. Rows that cannot be computed are logged and reported as "--".
The report goes to stdout; every failure notice goes to stderr through the
logging module.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact export the page gives
you, so the download runs on any machine with nothing set up beforehand.

Every print in the report carries flush=True. Without it stdout is held in a
buffer whenever it is not a terminal, so `python ... 2>&1 | more` would show all
six report lines in a block after all the log lines instead of interleaved with
them. Flushing each line as it is produced makes the combined transcript on the
page reproducible on your machine too.

Run it with::

    python exercise-04-safe-divide-solution.py
"""

from __future__ import annotations

import csv
import logging
import tempfile
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
log = logging.getLogger(__name__)

#: The export exactly as the exercise page gives it. Quito's trailing comma is
#: an empty field, and Osaka's real average is 0.00 rather than "no answer".
SAMPLE_TOTALS = (
    "chapter,attendees,sessions\n"
    "Lagos,180,12\n"
    "Manila,64,8\n"
    "Bogota,0,0\n"
    "Nairobi,45,three\n"
    "Quito,90,\n"
    "Osaka,0,4\n"
)


def safe_divide(numerator: float, denominator: float, label: str) -> float | None:
    """Return numerator / denominator, or None when the division is impossible.

    *label* names the thing being divided so the log line is searchable.
    Logs a warning for a zero denominator and an error for non-numeric input.
    """
    try:
        return numerator / denominator
    except ZeroDivisionError:
        log.warning("%s: denominator is zero; average is undefined", label)
        return None
    except TypeError:
        log.error("%s: cannot divide %r by %r", label, numerator, denominator)
        return None


def average_attendance(row: dict[str, str]) -> float | None:
    """Return the average attendance for one CSV row, or None if it is unusable."""
    chapter = row["chapter"]
    try:
        attendees = int(row["attendees"])
    except ValueError:
        log.error(
            "%s: attendees value %r is not a whole number", chapter, row["attendees"]
        )
        return None
    try:
        sessions = int(row["sessions"])
    except ValueError:
        log.error(
            "%s: sessions value %r is not a whole number", chapter, row["sessions"]
        )
        return None
    return safe_divide(attendees, sessions, chapter)


def report(source: Path) -> None:
    """Print the attendance report for *source* and log a summary count."""
    with source.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    log.info("read %d rows from %s", len(rows), source.name)

    usable = 0
    for row in rows:
        average = average_attendance(row)
        if average is None:
            text = "--"
        else:
            usable += 1
            text = f"{average:.2f}"
        print(f"{row['chapter']:<10} {text:>6}", flush=True)

    # Deliberate mistake, so you can watch the TypeError branch fire:
    safe_divide("64", 8, "unconverted string")

    log.info("%d of %d chapters had a usable average", usable, len(rows))


def build_sample(folder: Path) -> Path:
    """Write the sample chapter-totals export into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "chapter-totals.csv"
    path.write_text(SAMPLE_TOTALS, encoding="utf-8", newline="")
    return path


def main() -> None:
    """Build the sample data and run the report over it."""
    with tempfile.TemporaryDirectory() as workspace:
        report(build_sample(Path(workspace) / "data"))


if __name__ == "__main__":
    main()
```

**`None` means "no result" and `0.0` means "the result is zero", and the two
are never confused.** This is the whole exercise. Osaka held four sessions and
nobody came: `0 / 4` is `0.0`, a perfectly good average somebody would want to
see. Bogota has run no sessions at all, so its average does not exist — there
is no number that answers the question. If both came back as `0`, the `0.00` in
the report would be ambiguous and no reader could tell the sad turnout from the
missing data. `float | None` is the type that can say both things.

**And that is why the test is `if average is None:`.** `0.0` is falsy in
Python, along with `0`, `""`, `[]`, `{}` and `None`. So `if not average:`
treats Osaka's real answer exactly like Bogota's non-answer, prints `--`, and
reports `2 of 6`. No error, no warning, nothing in the log — just a wrong
number in a report somebody makes a decision from. `is None` asks the question
you actually mean: not "is this value unimportant" but "is this value absent".
Reach for `is None` every single time a function can legitimately return a
falsy value, which is most of them.

**Two `except` clauses, two meanings, two different levels, on purpose.**
`ZeroDivisionError` from Bogota is a fact about the data that stays true until
Bogota runs a session: expected, not urgent, `WARNING`, carry on. `TypeError`
means something reached the division that was never a number, which is a
mistake in *your* code and not in the spreadsheet. `ERROR` says so out loud.

**Each `try` wraps one line.** `try: attendees = int(row["attendees"])` and
nothing else. The narrower the block, the more precisely the handler can
describe what went wrong, because there is only one thing inside it that can go
wrong. That is what lets the message say `sessions value 'three' is not a whole
number` instead of `something failed on this row`.

**The conversions live in `average_attendance` and the division lives in
`safe_divide`.** `safe_divide` knows nothing about CSV files or chapters; it
takes two numbers and a label. `average_attendance` knows the row shape and the
column names. That split is exactly why the `label` parameter exists: the
function that *detects* the failure is not the function that knows what to
*call* the thing that failed, so the caller passes the name down. Every log
line then names a chapter and can be searched for.

**Lazy `%` arguments, not f-strings.** `log.error("%s: sessions value %r is not
a whole number", chapter, value)` hands the template and the values over
separately, and the substitution happens only if the record is actually
emitted. It also keeps the template identical across every call, so
`Nairobi: ...` and `Quito: ...` are visibly the same event with different
parameters rather than two unrelated strings.

**`%r` rather than `%s` for the offending value.** Quito's sessions field is
empty. `%s` renders it as nothing at all, so the message reads
`Quito: sessions value  is not a whole number` and the reader cannot tell
whether the value was empty, a space, or a bug in the message. `%r` renders it
as `''` — visible and unambiguous — and quotes `'three'` in the same style for
free. When you log a value that came from outside your program, `%r` is almost
always right.

**`list(csv.DictReader(f))` inside the `with`, and the report outside it.** The
reader is lazy and stops working the moment the file closes, so turning it into
a list inside the block is what lets `len(rows)` appear in the opening log line
and the loop run after the file is shut. Six rows is nothing. On a file too big
to hold in memory you would keep the loop inside the `with` and count as you
go.

**About the harness.** `SAMPLE_TOTALS` and `build_sample` exist so this
download runs on a machine where you have created nothing. `report` is your
`main` with the path passed in as an argument. `safe_divide` and
`average_attendance` are the exercise.

## Run it

Copy the worked answer on this page into `exercise-04-safe-divide.py` and run it:

```bash
python exercise-04-safe-divide.py
```

It needs no `data/` folder: it writes its own copy of the export into a
temporary directory, runs the report, and cleans up after itself. Redirect
stdout with `> report.txt` to see the two streams part company. The `-solution`
in the name keeps it from colliding with your own
`exercise-04-safe-divide.py`.

## Common bugs to catch

- **Osaka shows `--`.** You wrote `if average:` or `if not average:` instead of
  `if average is None:`. Here is what it looks like — no traceback, no log
  line, nothing to search for:

  ```text
  Lagos       15.00
  Manila       8.00
  Bogota         --
  Nairobi        --
  Quito          --
  Osaka          --
  ```

  and the summary quietly says `2 of 6` instead of `3 of 6`. The only way to
  catch this is to have a genuine zero in your test data and to know what it
  should print, which is exactly why Osaka is in the sample file.

- **`ValueError: invalid literal for int() with base 10: 'three'` kills the
  script.**

  ```text
  Lagos       15.00
  Manila       8.00
  Bogota       0.00
  Traceback (most recent call last):
    File "<string>", line 5, in <module>
      ...
  ValueError: invalid literal for int() with base 10: 'three'
  ```

  Your conversion is outside a `try`, so the run dies at Nairobi and Quito and
  Osaka never happen. Three rows printed and then nothing — which is worse than
  never starting, because now you have partial output and no way to tell it is
  partial.

- **`ZeroDivisionError: division by zero` escapes anyway.** You caught
  `ValueError`, thinking a zero denominator is a value problem. It is not.
  `ZeroDivisionError` sits under `ArithmeticError`, and `ValueError` is a
  completely different branch of the tree. Two failures, two branches, two
  handlers.

- **The `TypeError` branch never fires.** It cannot, on real data — every value
  reaching `safe_divide` has already been through `int()`, so there is nothing
  left to fail. That is exactly why the starter ends with a deliberate
  `safe_divide("64", 8, "unconverted string")` call. Here is what it is
  protecting you from, unhandled:

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print('64' / 8)
            ~~~~~^~~
  TypeError: unsupported operand type(s) for /: 'str' and 'int'
  ```

- **Log lines have no timestamp and read `WARNING:root:Bogota: ...`.** Either
  `basicConfig` never ran, or something logged before it did, or you called the
  module-level `logging.warning(...)` function instead of a method on your
  `log = logging.getLogger(__name__)` object. Those module-level functions go
  to the root logger, which is why the name reads `root`.

- **The `INFO` lines do not appear at all.** `basicConfig` defaults to
  `WARNING`. Without `level=logging.INFO` you only ever see warnings and
  errors.

- **`--- Logging error ---` followed by `TypeError: not enough arguments for
  format string`.**

  ```text
  --- Logging error ---
  Traceback (most recent call last):
    File "...\Lib\logging\__init__.py", line 400, in getMessage
      msg = msg % self.args
            ~~~~^~~~~~~~~~~
  TypeError: not enough arguments for format string
  Call stack:
    File "<string>", line 5, in <module>
      log.error('%s: sessions value %r is not a whole number', 'Nairobi')
  Message: '%s: sessions value %r is not a whole number'
  Arguments: ('Nairobi',)
  ```

  Two `%` placeholders, one argument. Notice the program did not die: `logging`
  catches errors raised while formatting a record, because a broken log call
  must never take down the program it is watching. That is the right behaviour,
  and it is also why this one is easy to miss — it scrolls past and nothing
  exits non-zero. The block hands you `Message:` and `Arguments:` so you can
  see exactly what it had.

- **The summary says `6 of 6`.** Your failure path returns `0` instead of
  `None`, or you increment `usable` before checking the result.

## Under the hood

<details>
<summary>Under the hood — an exception you catch, and one you let through</summary>

`try`/`except` is easy to write and easy to overuse. The question worth asking
at every one is not "could this line fail" but **"do I know what to do if it
does?"** If the answer is no, letting it through is the right move, and it is a
decision rather than a lapse.

**What "letting it through" actually does.** An uncaught exception does not
just stop the current function. It travels up through every function that was
waiting on it, and each one stops too. When it reaches the top with nobody left
to catch it, Python prints the traceback and exits with a non-zero code. That
non-zero code is not a failure to handle something — it is a message to
whatever ran your script, and a scheduler, a CI job or a shell script can read
it and act.

**What this exercise catches, and why each one earns it.**

- `ValueError` from `int("three")` — you know exactly what to do: name the
  chapter, name the bad value, skip the row. The whole point is that row four
  cannot take down rows five and six.
- `ZeroDivisionError` from Bogota — the same. It is a known, expected shape of
  real data.

**What this exercise does not catch, on purpose.**

- `KeyError` from a misspelled column name. That is a bug in your code. If you
  swallowed it, your program would report a data problem that does not exist,
  the log would blame the chapter, and the real fault would be invisible. Let
  it crash. It crashes on the first row, on your machine, while you are
  looking.
- `FileNotFoundError` from a missing CSV. There is no report to produce. A
  traceback naming the path is the most useful thing this program can do.

**Three habits that follow.**

**Never write a bare `except:`.** It catches `BaseException`, which includes
`KeyboardInterrupt` and `SystemExit`. Your script would ignore Ctrl-C:

```text
>>> while True:
...     try:
...         pass
...     except:
...         pass
...
```

That loop cannot be stopped with Ctrl-C. `except Exception:` is better, because
`Exception` deliberately excludes those two — but it is still very broad, and
in a batch loop it is the reason a program can run for an hour "successfully"
having silently skipped everything.

**Use `else` for the part that must only run on success.** `try`/`except` has
two more clauses that get forgotten:

```python
try:
    sessions = int(row["sessions"])
except ValueError:
    log.error("%s: sessions value %r is not a whole number", chapter, row["sessions"])
    return None
else:
    log.debug("%s: parsed %d sessions", chapter, sessions)
finally:
    log.debug("%s: conversion attempted", chapter)
```

`else` runs only when the `try` block raised nothing. `finally` runs either
way, even if you `return` out of the handler, which is what makes it the right
place for cleanup. Moving the success path into `else` keeps the `try` block
down to the one line that can actually fail, which is the constraint at the top
of this page, enforced by the shape of the code instead of by discipline.

**Re-raise when you have logged but not solved.** Logging an exception and
carrying on as if nothing happened is the most expensive habit in this whole
area. If you cannot recover, log it and put it back:

```python
try:
    config = load_config(path)
except OSError:
    log.exception("cannot read %s", path)
    raise
```

A bare `raise` inside an `except` block re-raises the exception you are
handling, with its original traceback intact. And `log.exception(...)` is
`log.error(...)` with the traceback attached — use it inside a handler and you
never have to format one by hand.

</details>

<details>
<summary>Under the hood — what logging is doing between your call and the screen</summary>

`log.warning("...")` looks like a fancy `print`. It is a small pipeline, and
knowing the four parts explains every confusing thing `logging` ever does.

**Logger → Record → Handler → Formatter.**

1. **The logger** is the object you call. `logging.getLogger(__name__)` returns
   the one named after your module — and calling it twice returns the *same*
   object, because loggers are cached by name. That is why you can call
   `getLogger` in every file without making a mess.
2. **The record** is built if the level passes. It carries the raw template,
   the arguments you passed, the level, the time, the module and the line
   number. Your `%s` substitution has not happened yet, which is the whole
   point of passing arguments lazily.
3. **The handler** decides where it goes. `basicConfig` with no `filename`
   installs a `StreamHandler` pointed at `sys.stderr`. That is why redirecting
   stdout does not capture your logs.
4. **The formatter** turns the record into the line you read. That is what your
   `format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"` string is
   configuring.

**The bit that surprises everyone: names are a tree.** A logger called
`report.csv.reader` has `report.csv` as its parent, `report` as its
grandparent, and the root logger above that. A record travels *up* through
every ancestor's handlers, which is why configuring the root logger once
configures your whole program. It is also why a message can appear twice: add a
handler to your own logger and leave the root's in place, and both print it.

**Levels are just numbers**, and the comparison is `>=`:

```text
>>> import logging
>>> logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
(10, 20, 30, 40, 50)
```

`basicConfig(level=logging.INFO)` sets 20, so a `DEBUG` call at 10 is dropped
before a record is even built. That is the cost argument for lazy arguments,
made concrete: below the level, your `%s` substitution never runs at all.

**Why `basicConfig` seems to ignore you.** It is a convenience function with
one rule: **if the root logger already has handlers, it does nothing.** And
calling `logging.warning(...)` at module level installs a handler as a side
effect. So this sequence silently fails:

```python
import logging
logging.warning("starting")                    # installs a default handler
logging.basicConfig(level=logging.INFO)        # does nothing at all
```

You then get `WARNING:root:starting` with no timestamp, and your `INFO` lines
never appear, and nothing tells you why. Two defences: call `basicConfig` at
the top of your module before anything logs, and use
`log = logging.getLogger(__name__)` rather than the module-level functions.
Since Python 3.8, `basicConfig(force=True)` will tear down existing handlers
and reconfigure — useful in a notebook, and a bad habit in a program.

**And the rule for libraries, which you will need the first time you write
one.** A library never calls `basicConfig` and never adds a handler. It calls
`logging.getLogger(__name__)` and logs. The application that imports it decides
where the output goes. A library that configures logging is a library that
overrides its user's decisions.

</details>

## Acceptance checklist

- [ ] All six chapters print, in file order, and the script exits cleanly.
- [ ] Lagos `15.00`, Manila `8.00`, Osaka `0.00`; the other three show `--`.
- [ ] Bogota logs `WARNING`; Nairobi and Quito log `ERROR`.
- [ ] Every log message names the chapter and quotes the bad value with `%r`.
- [ ] The final log line reads `3 of 6 chapters had a usable average`.
- [ ] Redirecting stdout to a file leaves the log lines on the terminal.
- [ ] There is no bare `except:` anywhere in the file.
- [ ] The exit code is `0`. Check it with `echo $?`, or `$LASTEXITCODE` in PowerShell.
- [ ] Committed to Git with a message like `Add Week 6 exercise 4: safe divide with logging`.

## Stretch

- Add `log.debug("computing %s: %d / %d", chapter, attendees, sessions)` to
  `average_attendance` and switch the level to `logging.DEBUG`. You now have a
  trace of every calculation, and turning it off is a one-word change.

- Send the log to a file as well as the terminal by passing
  `filename="report.log"` to `basicConfig` — then find out from the docs why
  that *replaces* the console handler instead of adding to it, and what
  `handlers=[...]` is for.

- Give `safe_divide` a `default: float | None = None` parameter so a caller can
  choose to get `0.0` back instead of `None`. Then write a comment naming which
  callers should ever use it. If you cannot name one, that is a useful answer
  too.

- Reject a negative session count with your own `raise ValueError(...)`, and
  catch it in the same place you catch the conversion failure. That is the
  bridge into the next exercise, which is about raising exceptions you designed
  yourself.

When your report survives all six rows, move on to
[Exercise 5 — Custom Exception](./exercise-05-custom-exception.md).
