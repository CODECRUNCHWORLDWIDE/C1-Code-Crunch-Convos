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
