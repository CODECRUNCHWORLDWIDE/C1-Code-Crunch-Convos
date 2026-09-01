# Week 6 — Homework

Six problems, one page each. This is the week your programs stop living
entirely in memory, so every problem here reads or writes something real
and every one of them has to decide what to do when that goes wrong.

Each page carries the brief, a starter you can paste and run, the answer
with an explanation, and a file you can download to compare against.
Read the answer *after* you have written something and run it — the gap
between "this should work" and "why does it print that" is where the
learning happens, and reading first closes it for free.

You are expected to use what you learned this week: `pathlib`, `with`,
`csv`, `json`, custom exceptions, `logging`. Resist the temptation to
copy from the lectures — write the code from memory and go back to the
lectures only when you are stuck.

## The one question behind all six

The six look like unrelated scripts. They are the same decision, six
times. Every one of them hits a failure and has to pick one of three
answers: **skip it and say so**, **stop and explain**, or **let it
crash**.

| # | The failure | The decision | The code shape |
|---|---|---|---|
| 1 | one file of many is unreadable | skip it and say so | `log.warning(...)`; `continue` |
| 2 | the headers disagree | stop and explain | `raise ValueError`; exit 1 |
| 3 | the input will not parse | stop and explain | one diagnostic line; `sys.exit(1)` |
| 4 | a transient call failed | try again, then give up | `except exc_type`; bare `raise` |
| 5 | the file is momentarily gone | skip it and keep going | `log.warning(...)`; `continue` |
| 6 | the write died halfway | leave the world unchanged | `finally`; `Path.replace` |

Ask that question before every `try` you write and the shape of the code
falls out of the answer.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the script
   takes and what it produces before you type anything.
2. Copy the Starter into a file of your own. The page names it — for
   problem 1 that is `word_count.py`, not the `-solution.py` file, which
   is the finished answer.
3. Fill in the `TODO` markers one at a time. Run it after each one.
4. Compare your output with the Expected output block, character for
   character.
5. Only then read The Solution and Why it works.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Word-count CLI](./problem-01-word-count-cli.md) | Carrying on past a file that will not open | Beginner | 45 min |
| 2 | [CSV merger](./problem-02-csv-merger.md) | Validating everything before writing anything | Intermediate | 1 hr |
| 3 | [JSON pretty-printer](./problem-03-json-pretty-printer.md) | Reading facts off an exception object | Intermediate | 50 min |
| 4 | [Retry-on-error decorator](./problem-04-retry-on-error-decorator-preview-of-decorators.md) | Telling a blip apart from a bug | Intermediate | 1 hr |
| 5 | [File watcher (poll-based)](./problem-05-file-watcher-poll-based.md) | A loop that runs forever and still stops politely | Intermediate | 1 hr |
| 6 | [Atomic-save helper](./problem-06-atomic-save-helper.md) | Replacing a file without ever leaving it half-written | Advanced | 1 hr |

Total target time: about 5 hours 35 minutes. The
[week schedule](../README.md) budgets a shorter homework block and both
numbers are honest — the figures here are how long each problem takes
when it goes well, and several of these are the kind of problem where
the first attempt teaches you what the second attempt should have been.

## What you hand in

Your own `homework/` folder should end up holding the six files you
wrote:

```text
homework/
    word_count.py
    csv_merge.py
    json_pretty.py
    retry.py
    watch.py
    atomic.py
```

Those are *your* files. The `-solution.py` files on the problem pages
are the published answers, and they are named differently on purpose so
that the two never land on top of each other.

Each one must be runnable as `python <name>.py ...` and must carry a
module docstring saying what it does, with an example invocation. Type
hints on every signature. `logging` for anything diagnostic. Narrow
`except` clauses — never a bare `except:`.

Due before you start Week 7. Commit with
`feat(week-06): homework problems`. If you are working in a cohort, open
a pull request.

## Checking your work

Every problem page ends with an acceptance checklist. Work down it
before you call a problem done. If your output differs from the page's
Expected output, the difference is the bug — read it rather than
guessing.

Two habits are worth carrying out of this week, and you can check both
by looking rather than running: **not one of these six answers calls
`open()` without a `with`, and not one of them catches `Exception`.**
Neither was a rule imposed from outside. Both fell out of asking, before
each `try`, which of the three things a failure there means.

Then it is on to the [mini-project](../mini-project/README.md), which
uses all of it at once.
