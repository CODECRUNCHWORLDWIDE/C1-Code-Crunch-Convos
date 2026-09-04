# Challenge 3 — Review the parser

> **Topic:** Reading code somebody else wrote — reviewing for correctness and cost, ranking findings by severity, and pinning each one with a failing test
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md) · [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md)
> **Difficulty:** Advanced
> **Target time:** 2 hours
> **Why this one:** every other page this week asks you to test code you just wrote, and you already know what that code was meant to do. Reviewing is the harder half of the job: you are handed a working program by somebody else, you do not know what they meant, and you have to decide whether it is safe to ship. Most of the code you will ever read was written by someone else. This is the drill for it.

## The Brief

A teammate sends you `logdigest.py`. It reads a service log — one line per
request — and hands back a small summary: how many lines, how many errors, how
many lines each server produced, and how busy the window was.

They ran it. It printed a summary. They would like a review before it goes in.

Here is the thing about the code you are about to read: **it works.** It does not
crash. It does not raise. Run it on the sample logs and it prints numbers that
look entirely reasonable. A compiler has no complaint. A linter has almost none.

It is also wrong, and it is wasteful, and the only thing standing between it and
production is a person who reads it carefully. That person is you.

Your job is not "make the tests pass". Your job is to find the defects nobody
told you about, decide which ones matter most, prove each one with a test that
fails today, and hand back a fixed module. That is a code review, and it is what
a reviewer is paid to produce.

There are **four** real findings in the module below. Not style nits — four
things that produce wrong answers or waste real time. Go and find them.

## Starter

Save this as `logdigest.py`. It runs exactly as pasted; run it first and look at
what it prints before you read a single line of it.

```python
"""logdigest.py — read a service log and say what happened in it.

Written by a teammate and sent to you for review. It runs.
"""

from datetime import datetime

MORNING = """# service log, exported 2026-03-01
2026-03-01T09:14:02 web-01 INFO GET /health 12ms
2026-03-01T09:14:07 web-01 INFO GET /orders 88ms
2026-03-01T09:15:31 web-03 ERROR POST /orders 940ms
2026-03-01T09:16:10 web-01 INFO GET /health 11ms
2026-03-01T09:17:44 web-03 WARN GET /orders 610ms
2026-03-01T09:19:02 web-02 INFO GET /health 9ms
"""

MIDDAY = """2026-03-01T11:02:00 web-02 INFO GET /health 10ms
2026-03-01T11:03:00 web-02 ERROR GET /orders 1200ms
2026-03-01T11:04:00 web-04 INFO POST /orders 130ms
2026-03-01T11:06:00 web-04 INFO GET /health 8ms
"""


class Line:
    """One parsed log line."""

    def __init__(self, moment, host, level, path, millis):
        self.moment = moment
        self.host = host
        self.level = level
        self.path = path
        self.millis = millis


def parse(text, records=[]):
    """Turn log text into a list of Line objects."""
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        stamp, host, level, method, path, took = raw.split(" ")
        records.append(
            Line(datetime.fromisoformat(stamp), host, level, path, int(took[:-2]))
        )
    return records


def host_counts(records):
    """How many lines each host produced."""
    counts = {}
    for record in records:
        total = 0
        for other in records:
            if other.host == record.host:
                total += 1
        counts[record.host] = total
    return counts


def lines_per_minute(records):
    """The average number of lines per minute across the window."""
    first = records[0].moment
    last = records[-1].moment
    minutes = int((last - first).total_seconds()) // 60
    return len(records) / minutes


def summarise(text):
    """Summarise one log file."""
    try:
        records = parse(text)
        return {
            "lines": len(records),
            "errors": sum(1 for r in records if r.level == "ERROR"),
            "hosts": host_counts(records),
            "per_minute": lines_per_minute(records),
        }
    except:
        return {"lines": 0, "errors": 0, "hosts": {}, "per_minute": 0.0}


def main():
    """Summarise the two sample files, in the order they arrived."""
    print("morning file:", summarise(MORNING))
    print("midday file: ", summarise(MIDDAY))


if __name__ == "__main__":
    main()
```

The line numbers in this challenge are the line numbers of that file, starting at
line 1 with `"""logdigest.py`. Look at line 35, and at line 78, before you decide
the module is fine.

Your review goes in a `REVIEW.md` beside it. This is the shape reviewers use, and
the shape the worked answer follows:

```text
# Review — logdigest.py

## Summary
<two or three sentences: can this ship, and if not, what is the one thing>

## Findings

### 1. <Blocker|Major|Minor> — <one-line title> (line NN)
**What breaks.** <the behaviour, not the code>
**How to see it.** <the input that shows it>
**Fix.** <the change, in a sentence>

### 2. ...

## Nits
<things not worth a finding, listed briefly>
```

## Requirements

1. **Find all four defects.** Each is a wrong answer or a real waste, not a
   matter of taste. None of them raises on the sample logs.
2. **Write `REVIEW.md`** using the template above. Every finding names the line,
   says what breaks *in terms of behaviour*, gives the input that reveals it, and
   proposes the fix in one sentence.
3. **Rank the findings by severity**, worst first, and use the words `Blocker`,
   `Major` and `Minor`. Be prepared to defend the order — a reviewer who marks
   everything Blocker has ranked nothing.
4. **Write one failing test per finding**, in `test_logdigest.py`. Each test must
   **fail against the module as submitted.** Run them and watch them fail before
   you fix anything.
5. **Write `logdigest_fixed.py`** with all four repaired, and nothing else
   changed. The same four tests must now pass.
6. **Test the cost finding without a stopwatch.** A test that fails when the
   build machine is busy is a test your team will delete within a month.
7. `README.md` says how to run the tests and which finding you would have
   shipped without, if the release were an hour away.

## Constraints

- **No rewrites.** You may not hand back a module you redesigned. A review that
  says "I rewrote it" is not a review — it throws away the author's decisions
  along with their bugs, and it gives them nothing to learn from. Change the four
  things and leave the rest, including the names and the shape of the output.
- **Every finding gets a failing test, no exceptions.** A finding with no test is
  an opinion. A finding with a test that already passes is worse: it is an
  opinion wearing a lab coat. If you cannot make a test fail, you have not
  understood the defect yet.
- **Behaviour, not code, in the findings.** "`parse` has a mutable default" tells
  the author what you read. "Summarising a second file reports the first file's
  lines as well" tells them what their users will see. Write the second, then
  name the cause.
- **Style nits go under `## Nits`, and stay there.** There is at least one in
  the module. Mixing it in with the wrong answers buries the wrong answers.
- **Do not change the log format.** The format is somebody else's; you are
  reviewing the reader, not the writer.

## Expected output

The shipped answer folds the submitted module, the repaired module, the four
tests and a driver into one file so it runs as a plain script. It summarises the
two sample logs with each module, then runs the four tests against each:

```text
$ python challenge-03-review-the-parser.py
The submitted module, on the two sample files, in the order they arrived:
  morning  lines=6   errors=1  per_minute=1.20  hosts={'web-01': 3, 'web-03': 2, 'web-02': 1}
  midday   lines=10  errors=2  per_minute=0.09  hosts={'web-01': 3, 'web-03': 2, 'web-02': 3, 'web-04': 2}
  The midday file has 4 lines. The summary says 10.

The repaired module, same two files, same order:
  morning  lines=6   errors=1  per_minute=1.20  hosts={'web-01': 3, 'web-03': 2, 'web-02': 1}
  midday   lines=4   errors=1  per_minute=1.00  hosts={'web-02': 2, 'web-04': 2}

One failing test per finding, run against the submitted module:
  FAIL  test_parse_does_not_carry_records_between_calls
  FAIL  test_a_one_line_file_is_summarised_not_zeroed
  FAIL  test_a_malformed_line_is_reported_not_swallowed
  FAIL  test_host_counts_does_not_rescan_the_log_for_every_line
  0 passed, 4 failed

The same four tests, run against the repaired module:
  PASS  test_parse_does_not_carry_records_between_calls
  PASS  test_a_one_line_file_is_summarised_not_zeroed
  PASS  test_a_malformed_line_is_reported_not_swallowed
  PASS  test_host_counts_does_not_rescan_the_log_for_every_line
  4 passed, 0 failed
```

The first two blocks are the whole review in six lines. The submitted module says
the midday file has ten lines. Open the midday file and count: there are four.

## Steps

1. Run `logdigest.py` as given. Read the two lines it prints. One of the numbers
   is impossible — find it before you read any code. **That is the review
   starting properly:** compare the output to the input, not the code to your
   taste.
2. Now read the module top to bottom, once, without judging. You are building a
   picture of what the author meant.
3. Read it a second time asking one question of every function: **what input
   makes this wrong?** Try the empty string. Try one line. Try the same text
   twice. Try a line with a field missing.
4. Write each suspicion down as a finding before you fix anything. Fixing first
   loses the finding — you will not remember what the third one was.
5. For each finding, write the test that fails. Run it. **Read the failure
   message and check that it is failing for the reason you think.** A test that
   fails for the wrong reason will pass again for the wrong reason.
6. Rank them. Ask which one, if shipped, would produce a wrong number that nobody
   notices for a month. Those come first — the loud failures are the safe ones.
7. Fix, one finding at a time, running the suite between fixes.
8. Write `REVIEW.md` last, when you know the whole picture, and write the summary
   paragraph first even though it appears at the top.

## The Solution

The whole answer, in three parts: the runnable file first — it carries the
submitted module, the repaired module and one failing test per finding — then
the review as a reviewer would actually send it, then why the findings are
ranked the way they are.

### The finished module and its tests

```python
"""challenge-03-review-the-parser-solution.py — the finished code review.

The challenge hands you ``logdigest.py``, a log parser and summariser written by
somebody else. It runs. It never crashes on the sample data. It is still wrong,
and it is still wasteful. The deliverable is what a reviewer is actually paid to
produce: findings ranked by severity, a failing test for each one, and the
repaired module.

This file holds all three so the whole review can be run in one go:

* ``submitted_module()`` — the code exactly as it arrived, wrapped in a function
  only so that both versions can live in one downloadable file.
* ``repaired_module()`` — the same module with every finding fixed.
* four tests, one per finding, each written to fail against the submitted code
  and pass against the repaired code.
* ``main()`` — runs both modules on the sample logs, then runs the four tests
  against each one and prints a plain, same-every-time report.

The written review itself is on the challenge page, under ``The Solution``.

Run it with::

    python challenge-03-review-the-parser-solution.py
"""

from __future__ import annotations

import contextlib
import io
import os
from collections import Counter
from datetime import datetime
from types import SimpleNamespace

import pytest

# --------------------------------------------------------------------------- #
# The sample logs the module was written against
# --------------------------------------------------------------------------- #

MORNING = """# service log, exported 2026-03-01
2026-03-01T09:14:02 web-01 INFO GET /health 12ms
2026-03-01T09:14:07 web-01 INFO GET /orders 88ms
2026-03-01T09:15:31 web-03 ERROR POST /orders 940ms
2026-03-01T09:16:10 web-01 INFO GET /health 11ms
2026-03-01T09:17:44 web-03 WARN GET /orders 610ms
2026-03-01T09:19:02 web-02 INFO GET /health 9ms
"""

MIDDAY = """2026-03-01T11:02:00 web-02 INFO GET /health 10ms
2026-03-01T11:03:00 web-02 ERROR GET /orders 1200ms
2026-03-01T11:04:00 web-04 INFO POST /orders 130ms
2026-03-01T11:06:00 web-04 INFO GET /health 8ms
"""

ONE_LINE = "2026-03-01T09:14:02 web-01 INFO GET /health 12ms\n"

MALFORMED = "2026-03-01T09:14:02 web-01 INFO GET /health\n"


# --------------------------------------------------------------------------- #
# The module as submitted — reproduced verbatim, defects and all
# --------------------------------------------------------------------------- #


def submitted_module() -> SimpleNamespace:
    """Return ``logdigest.py`` exactly as it arrived for review.

    The bodies below are the teammate's, unchanged. The only thing added is the
    wrapper, so this file can hold the before and the after side by side.
    """

    class Line:
        """One parsed log line."""

        def __init__(self, moment, host, level, path, millis):
            self.moment = moment
            self.host = host
            self.level = level
            self.path = path
            self.millis = millis

    def parse(text, records=[]):
        """Turn log text into a list of Line objects."""
        for raw in text.splitlines():
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            stamp, host, level, method, path, took = raw.split(" ")
            records.append(
                Line(datetime.fromisoformat(stamp), host, level, path, int(took[:-2]))
            )
        return records

    def host_counts(records):
        """How many lines each host produced."""
        counts = {}
        for record in records:
            total = 0
            for other in records:
                if other.host == record.host:
                    total += 1
            counts[record.host] = total
        return counts

    def lines_per_minute(records):
        """The average number of lines per minute across the window."""
        first = records[0].moment
        last = records[-1].moment
        minutes = int((last - first).total_seconds()) // 60
        return len(records) / minutes

    def summarise(text):
        """Summarise one log file."""
        try:
            records = parse(text)
            return {
                "lines": len(records),
                "errors": sum(1 for r in records if r.level == "ERROR"),
                "hosts": host_counts(records),
                "per_minute": lines_per_minute(records),
            }
        except:  # noqa: E722 — the finding, left in on purpose
            return {"lines": 0, "errors": 0, "hosts": {}, "per_minute": 0.0}

    return SimpleNamespace(
        Line=Line,
        parse=parse,
        host_counts=host_counts,
        lines_per_minute=lines_per_minute,
        summarise=summarise,
    )


# --------------------------------------------------------------------------- #
# The repaired module — every finding fixed, nothing else changed
# --------------------------------------------------------------------------- #


def repaired_module() -> SimpleNamespace:
    """Return the same module with all four findings fixed."""

    class Line:
        """One parsed log line."""

        def __init__(self, moment, host, level, path, millis):
            self.moment = moment
            self.host = host
            self.level = level
            self.path = path
            self.millis = millis

    def parse(text, records=None):
        """Turn log text into a list of Line objects.

        A fresh list every call unless the caller hands one in. A line that does
        not have the six fields this format promises is a problem worth hearing
        about, so it raises and says which line and what it saw.
        """
        if records is None:
            records = []
        for number, raw in enumerate(text.splitlines(), start=1):
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            fields = raw.split(" ")
            if len(fields) != 6:
                raise ValueError(
                    f"line {number}: expected 6 fields, got {len(fields)}: {raw!r}"
                )
            stamp, host, level, _method, path, took = fields
            if not took.endswith("ms"):
                raise ValueError(
                    f"line {number}: duration {took!r} is not in milliseconds"
                )
            records.append(
                Line(datetime.fromisoformat(stamp), host, level, path, int(took[:-2]))
            )
        return records

    def host_counts(records):
        """How many lines each host produced. One pass, one dictionary."""
        return dict(Counter(record.host for record in records))

    def lines_per_minute(records):
        """Lines per minute across the window, or None when there is no window.

        Fewer than two lines is not a rate of zero. It is a rate nobody can work
        out, and saying so is more honest than inventing a number.
        """
        if len(records) < 2:
            return None
        seconds = (records[-1].moment - records[0].moment).total_seconds()
        if seconds <= 0:
            return None
        return len(records) * 60.0 / seconds

    def summarise(text):
        """Summarise one log file. Bad input raises; it is not rounded down to zero."""
        records = parse(text)
        return {
            "lines": len(records),
            "errors": sum(1 for record in records if record.level == "ERROR"),
            "hosts": host_counts(records),
            "per_minute": lines_per_minute(records),
        }

    return SimpleNamespace(
        Line=Line,
        parse=parse,
        host_counts=host_counts,
        lines_per_minute=lines_per_minute,
        summarise=summarise,
    )


SUBMITTED = submitted_module()
REPAIRED = repaired_module()


def target() -> SimpleNamespace:
    """The module the tests run against, chosen by the REVIEW_TARGET variable.

    The same four tests are run twice: against the submitted code, where all
    four must fail, and against the repaired code, where all four must pass. An
    environment variable is used rather than a plain global because pytest
    imports this file afresh, and a fresh import would not see the global.
    """
    if os.environ.get("REVIEW_TARGET") == "submitted":
        return SUBMITTED
    return REPAIRED


# --------------------------------------------------------------------------- #
# One failing test per finding
# --------------------------------------------------------------------------- #


class CountingHost(str):
    """A host name that counts every equality test made against it.

    Finding 4 is about cost, and a stopwatch makes a flaky test. Counting the
    comparisons the code actually performs does not: the nested scan makes
    ``n * n`` of them, and a single keyed pass makes about ``n``.
    """

    comparisons = 0

    def __eq__(self, other):
        type(self).comparisons += 1
        return str.__eq__(self, other)

    def __hash__(self):
        return str.__hash__(self)


def counting_records(module: SimpleNamespace, count: int) -> list:
    """Build ``count`` records spread over five hosts, each host name counted."""
    moment = datetime(2026, 3, 1, 9, 0, 0)
    return [
        module.Line(moment, CountingHost(f"web-{index % 5:02d}"), "INFO", "/health", 10)
        for index in range(count)
    ]


def test_parse_does_not_carry_records_between_calls() -> None:
    """Finding 1 — the mutable default argument.

    Two calls with the same one-line text must each hand back one record. The
    submitted ``parse`` appends into a list created once, at import, so the
    second call hands back both.
    """
    module = target()
    module.parse(ONE_LINE)
    second = module.parse(ONE_LINE)
    assert len(second) == 1


def test_a_one_line_file_is_summarised_not_zeroed() -> None:
    """Finding 2 — the boundary error on a one-line file.

    One line is a perfectly ordinary log. The summary must say one line, and it
    must say that a rate cannot be worked out — not that the rate is zero.
    """
    summary = target().summarise(ONE_LINE)
    assert summary["lines"] == 1
    assert summary["per_minute"] is None


def test_a_malformed_line_is_reported_not_swallowed() -> None:
    """Finding 3 — the bare except.

    A line missing a field is the one thing the caller most needs to hear about.
    The submitted code turns it into a summary of zeros.
    """
    with pytest.raises(ValueError, match="expected 6 fields"):
        target().summarise(MALFORMED)


def test_host_counts_does_not_rescan_the_log_for_every_line() -> None:
    """Finding 4 — the quadratic scan.

    Counting three hundred lines must not cost ninety thousand comparisons.
    """
    module = target()
    records = counting_records(module, 300)
    CountingHost.comparisons = 0
    counts = module.host_counts(records)
    assert sum(counts.values()) == len(records)
    assert CountingHost.comparisons < 10 * len(records)


# --------------------------------------------------------------------------- #
# The driver — run both modules, then run the tests against each
# --------------------------------------------------------------------------- #


class Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite(which: str) -> list[tuple[str, str]]:
    """Run this file's four tests against one module and hand back the outcomes."""
    os.environ["REVIEW_TARGET"] = which
    collector = Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def show(label: str, summary: dict) -> None:
    """Print one summary on one line, with the rate formatted the same way always."""
    rate = "n/a" if summary["per_minute"] is None else f"{summary['per_minute']:.2f}"
    print(
        f"  {label:<8} lines={summary['lines']:<3} errors={summary['errors']:<2} "
        f"per_minute={rate:<5} hosts={summary['hosts']}"
    )


def report(results: list[tuple[str, str]]) -> None:
    """Print the outcome of each test, then the tally."""
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")
    passed = sum(1 for _, outcome in results if outcome == "passed")
    print(f"  {passed} passed, {len(results) - passed} failed")


def main() -> None:
    """Show both modules on the same input, then the four tests against each."""
    print("The submitted module, on the two sample files, in the order they arrived:")
    show("morning", SUBMITTED.summarise(MORNING))
    show("midday", SUBMITTED.summarise(MIDDAY))
    print("  The midday file has 4 lines. The summary says 10.")

    print()
    print("The repaired module, same two files, same order:")
    show("morning", REPAIRED.summarise(MORNING))
    show("midday", REPAIRED.summarise(MIDDAY))

    print()
    print("One failing test per finding, run against the submitted module:")
    report(run_suite("submitted"))

    print()
    print("The same four tests, run against the repaired module:")
    report(run_suite("repaired"))


if __name__ == "__main__":
    main()
```

### Review — logdigest.py

**Summary.** Not yet. The module produces wrong numbers on ordinary input and
hides the evidence when it fails. Two of the four findings are blockers, and they
compound: `parse` quietly carries records from one file into the next, and
`summarise` catches every error there is, so a run that has gone wrong still
prints a summary that looks fine. If only one thing is fixed today, fix the bare
`except` at line 78 — not because it is the most harmful, but because until it is
gone nobody can see the others.

**1. Blocker — `parse` accumulates into a list shared by every call (line 35).**

*What breaks.* Summarise two files in one program and the second summary includes
the first file's lines. In the sample run the midday file has four lines and the
summary says ten, with two errors instead of one and four hosts instead of two.
Nothing raises. The numbers are simply wrong, and they are wrong in the direction
that looks like traffic growth.

*How to see it.* Call `parse` twice with the same one-line text. The first call
returns one record; the second returns two.

*Why it happens.* `records=[]` is evaluated **once**, when `def` runs — not once
per call. Every call that does not pass its own list appends into the same list,
which lives as long as the program does.

*Fix.* Default to `None` and build a fresh list inside the function:

```python
def parse(text, records=None):
    """Build a fresh list every call, unless the caller hands one in."""
    if records is None:
        records = []
    records.extend(line for line in text.splitlines() if line)
    return records


LOG = """one line
"""

print(parse(LOG))
print(parse(LOG))
```

**2. Blocker — `summarise` swallows every error and returns a summary of zeros
(line 78).**

*What breaks.* A malformed line, an unreadable timestamp, a bug in any of the
three helpers — all of it becomes `{"lines": 0, "errors": 0, "hosts": {},
"per_minute": 0.0}`. That is not an error the caller can act on. It is a lie
shaped like an answer, and it is indistinguishable from a genuinely empty log.

*How to see it.* Feed it a line with a field missing. It returns zeros. Delete
the `try`/`except` and the same input raises
`ValueError: not enough values to unpack (expected 6, got 5)` — the message that
would have told the caller exactly what was wrong.

*Why it is worse than it looks.* A bare `except:` catches `BaseException`, which
includes `KeyboardInterrupt` and `SystemExit`. On a long log this module cannot
be stopped with Ctrl-C in the middle of `summarise`; the interrupt is caught and
turned into a summary of zeros.

*Fix.* Delete the `try`/`except` entirely and let the error out. Raise a clear
`ValueError` at the point of the bad line, naming the line number and what was
found, so the caller does not have to guess which of ten thousand lines was the
problem.

**3. Major — `lines_per_minute` breaks on any log shorter than a minute
(lines 62–65).**

*What breaks.* `minutes` is a whole number of minutes between the first and last
line. For a one-line file that is `0`, and `len(records) / 0` raises
`ZeroDivisionError`. For an empty file, `records[0]` raises `IndexError` before
the division is even reached. Both are then eaten by finding 2, so a one-line log
is reported as having zero lines. There is also a quieter version on real data: a
log spanning 90 seconds reports its rate over one minute, overstating it by half.

*How to see it.* Summarise a file with one line in it. The submitted module says
`lines=0`.

*Fix.* Return `None` when there are fewer than two records or the window is zero
seconds long, and divide by seconds rather than truncated minutes:

```python
from datetime import datetime, timedelta


class Line:
    """Just enough of a record to show the fix."""

    def __init__(self, moment):
        self.moment = moment


def lines_per_minute(records):
    """Lines per minute across the window, or None when there is no window."""
    if len(records) < 2:
        return None
    seconds = (records[-1].moment - records[0].moment).total_seconds()
    if seconds <= 0:
        return None
    return len(records) * 60.0 / seconds


start = datetime(2026, 3, 1, 9, 14, 2)
six = [Line(start + timedelta(seconds=count * 60)) for count in range(6)]
print("six lines over five minutes:", lines_per_minute(six))
print("one line:                 ", lines_per_minute(six[:1]))
print("no lines:                 ", lines_per_minute([]))
```

`None` is the honest answer. A rate over a window of no length is not zero — it
is a number nobody can work out, and saying so lets the caller decide what to
print.

**4. Major — `host_counts` re-reads the whole log once for every line
(lines 48–57).**

*What breaks.* Nothing, on six lines. The cost is `n × n`: the outer loop walks
every record, and for each one the inner loop walks every record again. Three
hundred lines cost about ninety thousand comparisons. Six hundred lines cost
about three hundred and sixty thousand — double the input, four times the work.
A day of logs from a busy service is millions of lines, and this function alone
would run for hours. It also assigns `counts[record.host]` once per record rather
than once per host, doing the same write over and over.

*How to see it.* Count the comparisons rather than timing them. A test that
counts is the same on a fast machine and a loaded one.

*Fix.* One pass, one dictionary:

```python
from collections import Counter


class Line:
    """Just enough of a record to show the fix."""

    def __init__(self, host):
        self.host = host


def host_counts(records):
    """How many lines each host produced. One pass, one dictionary."""
    return dict(Counter(record.host for record in records))


print(host_counts([Line("web-01"), Line("web-03"), Line("web-01")]))
```

**Nits.** `method` at line 41 is unpacked and never used; name it `_method` so a
reader knows it is deliberate. `r` at line 74 is a one-letter name in a module
that otherwise spells things out.

**Why the two blockers are ranked above the two majors.** Findings 3 and 4 fail
loudly or slowly, and both announce themselves — a `ZeroDivisionError` in a
traceback, a function that visibly takes forever. Findings 1 and 2 produce a
plausible wrong answer and print it with total confidence. The reason a wrong
number outranks a crash is that a crash gets fixed on the day it happens, and a
wrong number gets copied into a report, quoted in a meeting, and believed for a
month. Rank by how long the defect can survive undetected, not by how unpleasant
it is when it fires.

**Why finding 2 is the one to fix first even so.** Severity says which finding
does the most damage. Order of work is a different question. While the bare
`except` is in place, every other defect in the module is invisible: finding 3
already fires on a one-line file, and the only reason nobody has noticed is that
its exception is being converted into zeros. Remove the blindfold before you go
looking for anything.

**Why the fixed `parse` raises instead of skipping bad lines.** Skipping is
tempting and it is the wrong default. A parser that silently drops the lines it
cannot read hands you a summary of the part of the file it happened to
understand, with no mark on it saying so. Raising with the line number and the
offending text — `line 1: expected 6 fields, got 5: '...'` — turns a silent
undercount into a five-second fix. If a caller genuinely wants best-effort
parsing, that is a flag they ask for, not a decision the parser makes for them.

**Why the cost test counts comparisons instead of seconds.** `CountingHost` is a
`str` subclass that increments a counter every time it is compared. The nested
scan makes about `n²` comparisons — 90,295 for three hundred records — and the
`Counter` version makes about `2n`, which is 590. Asserting
`comparisons < 10 * len(records)` is true for the repaired code by a wide margin
and false for the submitted code by a factor of thirty. It gives the same answer
on a laptop, on a busy build machine, and in five years on hardware nobody has
built yet. A `time.time()` assertion gives none of those things, and a flaky
performance test gets deleted rather than investigated.

**Why the review says "not yet" rather than listing four fixes.** The first line
of a review is the only line some people read. It has to answer the question the
author asked — can this ship — before it explains anything. Everything after the
summary is evidence for that one sentence.

## Run it

Copy the worked answer on this page into `challenge-03-review-the-parser.py` and run it:

```bash
python challenge-03-review-the-parser.py
```

It needs `pytest` and nothing else. In your own folder the work is four files —
`logdigest.py` as submitted, `logdigest_fixed.py`, `test_logdigest.py` and
`REVIEW.md` — and you run the tests with:

```bash
pytest test_logdigest.py -v
```

The single file here exists because a published answer has to run as one
download. `REVIEW.md` is the graded part, and it is the part no script can check
for you.

## Common bugs to catch

- **You fixed it before you wrote the test, and now you cannot prove anything.**
  The test passes. It would also have passed against the broken module, and you
  will never know. Stash the fix, run the test, watch it fail, then restore the
  fix. Against the module as submitted the four tests fail like this:

  ```text
  $ pytest test_logdigest.py -q
  FFFF                                                                     [100%]
  ================================== FAILURES ===================================
  _______________ test_parse_does_not_carry_records_between_calls _______________

          module.parse(ONE_LINE)
          second = module.parse(ONE_LINE)
  >       assert len(second) == 1
  E       assert 2 == 1

  ________________ test_a_one_line_file_is_summarised_not_zeroed ________________

          summary = target().summarise(ONE_LINE)
  >       assert summary["lines"] == 1
  E       assert 0 == 1

  _______________ test_a_malformed_line_is_reported_not_swallowed _______________

  >       with pytest.raises(ValueError, match="expected 6 fields"):
  E       Failed: DID NOT RAISE <class 'ValueError'>

  ___________ test_host_counts_does_not_rescan_the_log_for_every_line ___________

  >       assert CountingHost.comparisons < 10 * len(records)
  E       assert 90295 < (10 * 300)
  E        +  where 90295 = CountingHost.comparisons

  4 failed in 0.18s
  ```

- **`assert summary["lines"] == 1` fails with `assert 0 == 1` and you go looking
  in `parse`.** `parse` is fine on one line; the zero comes from the fallback in
  `summarise`. This is what a bare `except` costs you — the failure surfaces
  three functions away from its cause. Delete the `except` first and the real
  error appears where it belongs:

  ```text
  Traceback (most recent call last):
    File "logdigest.py", line 65, in lines_per_minute
      return len(records) / minutes
             ~~~~~~~~~~~~~^~~~~~~~~
  ZeroDivisionError: division by zero
  ```

- **You fix the one-line case and the empty file still misbehaves.** They are
  different lines. `minutes` is only reached when there is at least one record;
  an empty log dies earlier, on line 62:

  ```text
  Traceback (most recent call last):
    File "logdigest.py", line 62, in lines_per_minute
      first = records[0].moment
              ~~~~~~~^^^
  IndexError: list index out of range
  ```

  A `len(records) < 2` guard closes both, which is why it is one fix and not two.

- **Your `pytest.raises` test passes against the submitted module.** It cannot,
  unless you pointed it at the wrong function. `pytest.raises` fails with
  `Failed: DID NOT RAISE <class 'ValueError'>` when the block completes quietly,
  and that is precisely what a bare `except` guarantees. If it passed, you tested
  `parse` directly rather than `summarise` — and `parse` does raise. The whole
  point of the finding is that `summarise` does not let it out.

- **Your performance test uses `time.time()` and passes on the submitted
  module.** Ninety thousand comparisons is roughly ten milliseconds. Any
  threshold loose enough to be reliable is loose enough to miss the defect, and
  any threshold tight enough to catch it will fail on a busy machine. Measure
  work, not wall clock.

- **You reported the unused `method` variable as a finding.** It is a nit. Listing
  it alongside a summary that reports ten lines for a four-line file tells the
  author that you weigh those two things similarly, and the next review you send
  will be skimmed.

- **You rewrote the module.** It is the most common way a first review goes
  wrong. The author gets a diff they cannot read, learns nothing, and has to
  re-verify decisions that were never in question. Four changes, four tests,
  everything else left alone.

## Under the hood

<details>
<summary>Under the hood — why a bare except is worse than except Exception</summary>

Python's exceptions all descend from `BaseException`. Most of what you want to
catch descends from `Exception`, which is one step below it. The handful that do
**not** are the ones that mean "stop the program, right now":

| Class | Raised by |
| --- | --- |
| `KeyboardInterrupt` | Ctrl-C |
| `SystemExit` | `sys.exit()` |
| `GeneratorExit` | a generator being closed |

A bare `except:` catches `BaseException` — all of it. So in the submitted module,
pressing Ctrl-C while `summarise` is running does not stop anything; the
interrupt is caught, discarded, and a summary of zeros is returned. On the
quadratic `host_counts` over a large log, that is a program you cannot get out of
without killing it from another window.

`except Exception:` leaves those three alone. It is the widest catch that is ever
reasonable, and it is still too wide for this module — nothing in `summarise`
knows how to handle a `MemoryError` or an `AttributeError`, so nothing in
`summarise` should be catching them.

The rule underneath: **catch the exception you know how to handle, at the place
you know how to handle it.** Everywhere else, let it go past. A caller that gets
an exception can retry, log it, or stop. A caller that gets zeros can only be
wrong.

When you do catch and re-raise something more useful, chain it, so the original
is still in the traceback:

```python
class LogFormatError(ValueError):
    """A log line that does not match the expected format."""


def parse_stamp(text):
    """Parse one timestamp, and say which text failed if it does not parse."""
    from datetime import datetime

    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise LogFormatError(f"bad timestamp: {text!r}") from exc


print(parse_stamp("2026-03-01T09:14:02"))

try:
    parse_stamp("March 1st")
except LogFormatError as exc:
    print(f"{type(exc).__name__}: {exc}")
    print(f"caused by: {type(exc.__cause__).__name__}")
```

`raise ... from exc` sets `__cause__`, and the printed traceback then says
`The above exception was the direct cause of the following exception`. You get
your clearer message *and* the original.

</details>

<details>
<summary>Under the hood — what the nested scan actually costs, measured</summary>

`host_counts` as submitted has a loop inside a loop over the same list, so the
number of comparisons grows with the square of the input. Counted, using the
`CountingHost` class from the answer:

| Records | Submitted | Repaired |
| --- | --- | --- |
| 300 | 90,295 | 590 |
| 600 | 360,595 | 1,190 |

Double the input and the submitted version does **four** times the work; the
repaired version does twice. That is the difference between `O(n²)` and `O(n)`,
and it is why the fix matters on real logs and is invisible on six lines.

Two details worth knowing:

- The repaired count is about `2n`, not `n`. `Counter` compares once per record
  when it finds an existing key, and building `dict(...)` from it touches the
  five keys again. Constant factors are real; they are just not what changes when
  the input grows.
- The submitted count is 90,295 rather than exactly 90,000. `str.__eq__` short
  circuits on identity for interned strings and the counter fires slightly
  differently at the boundaries. The shape is what matters — 300 records to 600
  records multiplied the work by 3.99.

The `Counter` version is faster for a reason worth naming. Looking a key up in a
dictionary hashes it once and jumps straight to a slot; it does not walk the
other keys. So counting `n` items over `h` distinct hosts costs about `n` steps
instead of `n²`, and `h` never enters the sum at all. That trade — spend memory
on a dictionary, stop scanning — is the single most common performance fix you
will ever make to somebody else's loop.

Run it yourself:

```python
from collections import Counter
import time

hosts = [f"web-{index % 5:02d}" for index in range(4000)]

start = time.perf_counter()
slow = {}
for host in hosts:
    total = 0
    for other in hosts:
        if other == host:
            total += 1
    slow[host] = total
slow_seconds = time.perf_counter() - start

start = time.perf_counter()
fast = dict(Counter(hosts))
fast_seconds = time.perf_counter() - start

print(f"same answer: {slow == fast}")
print(f"nested scan: {slow_seconds:.4f}s")
print(f"Counter:     {fast_seconds:.4f}s")
```

</details>

<details>
<summary>Under the hood — how a mutable default actually behaves</summary>

`def parse(text, records=[])` does not mean "an empty list each time". It means
"this exact list", created once, when the `def` statement runs — which happens
when the module is imported, not when the function is called. The list is stored
on the function object itself and you can look at it:

```python
def collect(item, bucket=[]):
    """Append to the default bucket and return it."""
    bucket.append(item)
    return bucket


print(collect("a"))
print(collect("b"))
print(collect("c"))
print("the default itself:", collect.__defaults__)
```

That prints `['a']`, then `['a', 'b']`, then `['a', 'b', 'c']`, and finally the
default tuple holding the same three-item list. The function has grown state
nobody declared.

The same trap applies to `{}`, `set()`, and any object you can change in place. It
does **not** apply to `0`, `None`, `""`, or a tuple, because there is no way to
change those in place — which is exactly why `None` is the conventional sentinel:

```python
def collect(item, bucket=None):
    """Append to the caller's bucket, or to a fresh one."""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


print(collect("a"))
print(collect("b"))
print("shared?", collect("c", collect("d")))
```

Now each default call gets its own list, and a caller who wants to accumulate can
still pass one in — the flexibility the original was reaching for, without the
surprise.

The reason this defect is so hard to spot in review is that it is invisible in
any single call. `parse` is correct the first time, correct in isolation, and
correct in a test file that calls it once. It only misbehaves in the second call
of a real program, which is the first place nobody is looking.

</details>

## Acceptance checklist

- [ ] `REVIEW.md` exists, with a summary paragraph and four findings.
- [ ] Every finding names a line, describes the broken **behaviour**, gives the
      input that reveals it, and proposes a fix.
- [ ] The findings are ranked `Blocker` / `Major` / `Minor`, worst first, and you
      can say why in one sentence.
- [ ] Style nits are under `## Nits`, not among the findings.
- [ ] Four tests in `test_logdigest.py`, each of which you have watched fail
      against the submitted module.
- [ ] The cost test measures work, not wall-clock time.
- [ ] `logdigest_fixed.py` passes all four, and differs from the original in four
      places and no more.
- [ ] `README.md` says which finding you would have shipped without, and why.

## Stretch

- **Review a real one.** Open the oldest file in your own Week 5 or Week 9 work
  and review it with this template as if a stranger wrote it. Time yourself; a
  first pass on a hundred lines should take about twenty minutes. Whatever you
  find, write the failing test before the fix.
- **Add the fifth defect on purpose.** Give the log a second duration format —
  `1.2s` alongside `412ms` — and watch `int(took[:-2])` turn `1.2s` into a crash
  and `took.rstrip("ms")` turn it into `1.2`, which is silently 1,198 milliseconds
  short. Write the test that catches it, then fix the parser to accept both units.
- **Make the review reproducible.** Wire `ruff` and `mypy` over `logdigest.py` and
  see which of your four findings a tool would have caught for free. `ruff` flags
  the bare `except` (E722) and the mutable default (B006); nothing flags the
  boundary error or the quadratic scan. That gap is the argument for human review
  in one line, and it belongs in your `README.md`.
- **Turn the tests into a regression suite.** Add `pytest --cov=logdigest_fixed
  --cov-branch` and find the branches your four tests never reach. Each uncovered
  branch is a defect nobody has found yet.

You have now read code you did not write and said, in writing, what is wrong with
it. That is the half of the job the other pages this week do not ask for. Take
the [quiz](../quiz.md), then build the week's
[mini-project](../mini-project/README.md) — and review your own module with this
template before you call it done.
