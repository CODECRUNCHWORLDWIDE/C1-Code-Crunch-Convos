# Exercise 1 — Your First Pytest Tests

> **Topic:** Writing `test_*.py` files, plain `assert`, `pytest.raises`, and the red-green loop
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** every other exercise, challenge, and the mini-project this week assumes you can create a test file, run `pytest`, and read the failure output. This is also the first time you will watch a test fail *on purpose* and then make it pass. If you skip the red step you never learn to trust a green one, because you never proved the test could catch anything.

## The Brief

The neighborhood tool library lends out circular saws, ladders, and pressure
washers. Members keep them too long. The board voted in a late fee: twenty-five
cents a day, capped at ten dollars, because nobody wanted a returned hedge
trimmer to come with an eighty-dollar bill attached.

You are handed `lending.py`. It computes a fee, and it is wrong in two ways the
author did not notice: it ignores the cap, and it returns a negative fee if you
hand it a negative number of days. Write the tests that expose both bugs, watch
them fail, then fix the module. Every amount here is an integer count of
**cents**, never a float number of dollars, which is why your assertions can be
exact instead of approximately correct.

A test is just a small function that says "if I call this with X, I should get
Y back." You run all of them at once with the `pytest` command, and it tells you
which promises the code kept and which it broke.

## Starter

Two files, side by side in the same folder. First, the module under test:

```python
"""lending.py — late-fee rules for the neighborhood tool library."""

DAILY_FEE_CENTS: int = 25
MAX_FEE_CENTS: int = 1_000


def late_fee_cents(days_late: int) -> int:
    """Return the late fee, in cents, for an item returned late.

    Args:
        days_late: Whole days past the due date. Zero means on time.

    Returns:
        The fee in cents, never greater than ``MAX_FEE_CENTS``.

    Raises:
        ValueError: If ``days_late`` is negative.
    """
    # TODO: reject a negative days_late with
    #       raise ValueError("days_late cannot be negative")
    # TODO: stop the fee at MAX_FEE_CENTS instead of growing forever
    return days_late * DAILY_FEE_CENTS


if __name__ == "__main__":
    for day in (0, 1, 10, 100):
        print(f"{day:>3} days late -> {late_fee_cents(day)} cents")
```

Then the test file you are here to write:

```python
"""test_lending.py — tests for the tool library's late-fee rules."""

import pytest

from lending import MAX_FEE_CENTS, late_fee_cents


def test_on_time_is_free() -> None:
    """Zero days late costs nothing."""
    assert late_fee_cents(0) == 0


def test_one_day_late_costs_a_quarter() -> None:
    """One day late is a single daily charge."""
    # TODO: assert the fee for 1 day is 25


def test_ten_days_late_costs_two_fifty() -> None:
    """Ten days late is ten daily charges, still under the cap."""
    # TODO: assert the fee for 10 days is 250


def test_fee_stops_at_the_cap() -> None:
    """A very late return is billed at the cap, not the raw daily rate."""
    # TODO: assert the fee for 100 days is MAX_FEE_CENTS


def test_negative_days_is_rejected() -> None:
    """A negative day count is a caller bug, not a refund."""
    # TODO: use pytest.raises(ValueError) around late_fee_cents(-3)
```

## Requirements

1. `test_lending.py` contains exactly five test functions, named as in the
   starter. The names are part of the deliverable: `pytest -v` prints them, and
   `test_fee_stops_at_the_cap` tells a reader what broke without opening the
   file.
2. Each test uses a bare `assert`. No `unittest.TestCase`, no
   `self.assertEqual`.
3. `test_fee_stops_at_the_cap` compares against the imported `MAX_FEE_CENTS`,
   not the literal `1000`.
4. `test_negative_days_is_rejected` uses `with pytest.raises(ValueError):` and
   puts **only** the failing call inside the `with` block.
5. Run the suite once *before* touching `lending.py`. Three pass, two fail.
6. Fix `lending.py` so all five pass. The fix is two lines: a guard clause and
   a `min(...)`.

## Constraints

- **Money is stored as whole cents, never as a float.** `0.1 + 0.2` is
  `0.30000000000000004` in Python, so `assert fee == 2.50` can fail for reasons
  that have nothing to do with your logic. Integers make the assertion exact,
  and exactness is the whole point of a test.
- **Compare against `MAX_FEE_CENTS`, not `1000`.** If the board raises the cap,
  a test with a hard-coded `1000` fails even though the code is correct. That is
  a false alarm, and false alarms teach a team to ignore its test suite.
- **The test file gets no `if __name__ == "__main__":` guard.** You never run a
  test file directly — `pytest` imports it and calls the `test_*` functions
  itself. A guard there would be dead code.
- **Put only the call that should raise inside `pytest.raises`.** If you wrap
  three lines and an earlier one raises `ValueError` by accident, the test
  passes for the wrong reason and you never find out.
- **Do not fix `lending.py` before you have seen the two failures.** A test you
  have never seen fail is a test you have no evidence works.

## Expected output

The shipped answer below is one file that carries the fixed module, the five
tests, and a small driver that runs the suite the way `pytest` would and prints
a plain report. That is what lets a published answer run as an ordinary
script. Run it and you see this, the same on every machine:

```text
$ python exercise-01-first-test-solution.py
The late-fee rules, after the two-line fix:
    0 days late ->    0 cents
    1 days late ->   25 cents
   10 days late ->  250 cents
  100 days late -> 1000 cents  (capped: the raw rate was 2500)
   -3 days late -> ValueError: days_late cannot be negative

The five tests, run the way pytest runs them:
  PASS  test_on_time_is_free
  PASS  test_one_day_late_costs_a_quarter
  PASS  test_ten_days_late_costs_two_fifty
  PASS  test_fee_stops_at_the_cap
  PASS  test_negative_days_is_rejected

5 passed, 0 failed
```

When you do this exercise for real you will not see that tidy summary — you will
see `pytest`'s own output, red the first time and green after the fix. Both of
those runs are shown under **Common bugs to catch** and **Under the hood**, so
you know what you are aiming at.

## Steps

1. Activate your virtual environment and confirm the tool is there:
   `pytest --version` should print `pytest 9.x.x`.
2. Save `lending.py` and `test_lending.py` side by side in your Week 11 folder.
3. Fill in the four `TODO`s in the test file. Leave `lending.py` alone.
4. Run `pytest -v`. You should see the two-failure output shown below. Read the
   `assert 2500 == 1000` line — that is pytest showing you both sides of the
   comparison without you writing a message.
5. Fix `lending.py`: add the `ValueError` guard first, then
   `return min(days_late * DAILY_FEE_CENTS, MAX_FEE_CENTS)`. Rerun. Five passed.
6. Break it on purpose — change `min` to `max` — and rerun. Confirm four tests
   fail, then put `min` back. You have now proved the tests guard the behavior
   you care about.

## The Solution

```python
"""exercise-01-first-test-solution.py — first pytest tests, proven headless.

You normally run tests with the ``pytest`` command, which finds every
``test_*`` function and reports on it. A published answer cannot lean on that,
because the grader runs it as a plain script: ``python this_file.py``. A file
full of ``test_`` functions prints nothing when you do that — pytest is what
calls them, and pytest is not in the room.

So this one file carries three things at once: the fixed ``lending.py`` code,
the five tests from ``test_lending.py``, and a tiny ``main()`` that *drives
pytest itself* and prints a plain, same-every-time report. In your own Week 11
folder you keep the module and the tests in two files and run ``pytest``. Here
they travel together so the download runs on its own.

Run it with::

    python exercise-01-first-test-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# lending.py — the module under test, with the two-line fix applied
# --------------------------------------------------------------------------- #

DAILY_FEE_CENTS: int = 25
MAX_FEE_CENTS: int = 1_000


def late_fee_cents(days_late: int) -> int:
    """Return the late fee, in whole cents, for an item returned late.

    Zero days late is free. Each further day adds ``DAILY_FEE_CENTS``, and the
    total never climbs past ``MAX_FEE_CENTS``. A negative day count is a caller
    bug, not a refund, so it raises.
    """
    if days_late < 0:
        raise ValueError("days_late cannot be negative")
    return min(days_late * DAILY_FEE_CENTS, MAX_FEE_CENTS)


# --------------------------------------------------------------------------- #
# test_lending.py — the five tests, exactly as the exercise asks for them
# --------------------------------------------------------------------------- #


def test_on_time_is_free() -> None:
    """Zero days late costs nothing."""
    assert late_fee_cents(0) == 0


def test_one_day_late_costs_a_quarter() -> None:
    """One day late is a single daily charge."""
    assert late_fee_cents(1) == 25


def test_ten_days_late_costs_two_fifty() -> None:
    """Ten days late is ten daily charges, still under the cap."""
    assert late_fee_cents(10) == 250


def test_fee_stops_at_the_cap() -> None:
    """A very late return is billed at the cap, not the raw daily rate."""
    assert late_fee_cents(100) == MAX_FEE_CENTS


def test_negative_days_is_rejected() -> None:
    """A negative day count is a caller bug, not a refund."""
    with pytest.raises(ValueError):
        late_fee_cents(-3)


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        # The "call" phase is the test body itself; setup/teardown are separate.
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes.

    pytest's own console output is captured and dropped so the report below is
    identical on every machine — no timings, no platform banner, no plugin
    version line to drift.
    """
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Show the fixed fee rules, then run the suite and print the outcomes."""
    print("The late-fee rules, after the two-line fix:")
    for day in (0, 1, 10, 100):
        note = "  (capped: the raw rate was 2500)" if day == 100 else ""
        print(f"  {day:>3} days late -> {late_fee_cents(day):>4} cents{note}")
    try:
        late_fee_cents(-3)
    except ValueError as error:
        print(f"   -3 days late -> ValueError: {error}")

    print()
    print("The five tests, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
```

**The red run is the deliverable, not the green one.** Each failure tells you
something you could not otherwise know. `assert 2500 == 1000` proves the cap
test really reads the function's answer — pytest rewrote your bare `assert` and
printed both sides plus the call that produced the left one, and you wrote no
message to make that happen. `DID NOT RAISE` proves the exception test would
notice if the guard ever vanished. Fix `lending.py` first and watch both go
straight to green, and you have written two lines of code with no evidence
attached to them.

**`min` is the clamp, and the order of the two lines matters.** The guard runs
first because a negative `days_late` is not a fee question at all — it is a
caller with a bug, and answering politely with `0` would hide that bug
somewhere upstream. Once the guard has run, `days_late * DAILY_FEE_CENTS` cannot
be negative, so `min(...)` has one job: stop the growth at the cap. Writing it
as `min` rather than an `if` also removes a second `return` and a second place
to get the boundary wrong.

**Cents, not dollars, is what makes the assertions exact.** `late_fee_cents(10)
== 250` is either true or false. The float version, `fee == 2.50`, compares a
computed binary fraction against a literal one, and those agree right up until
the day they do not. Integers delete a whole category of flaky test from the
file, permanently — which is why real money systems store cents too.

**`MAX_FEE_CENTS` is imported, not retyped.** The cap test asks "does the
function respect the cap", not "is the cap one thousand". Raise the cap to $15
next spring and correct code keeps working while a test with a hard-coded `1000`
goes red for no reason. A team that gets two false alarms learns to ignore the
suite, and then the suite protects nothing.

**Only the failing call goes inside `pytest.raises`.** The block is a claim that
*this one expression* raises. Put three statements in there and a `ValueError`
from the first satisfies the test while the line you meant to check never runs.
One line, one claim.

**The driver is the only unusual part, and it exists only because this is a
download.** `run_suite()` calls `pytest.main([__file__])`, which is the same
engine the `pytest` command uses, pointed at this file; the `_Collector` plugin
records each test's name and result. pytest's own noisy output is captured and
thrown away so the printed report never drifts. In your own folder you skip all
of that and just type `pytest`.

## Download and run

Download
[exercise-01-first-test-solution.py](./exercise-01-first-test-solution.py)
and run it:

```bash
python exercise-01-first-test-solution.py
```

It needs `pytest` installed and nothing else, and it exits on its own. Your own
work is the two separate files — `lending.py` and `test_lending.py` — which you
run with `pytest -v`, not `python`.

The `-solution` in the filename keeps this file from colliding with your own
`lending.py` and `test_lending.py`.

## Common bugs to catch

- **`ModuleNotFoundError: No module named 'lending'`.** The classic cause is a
  `tests/` subfolder: `test_lending.py` lives in `tests/` while `lending.py` sits
  in the parent, so the folder holding `lending.py` is not on the import path.
  For this exercise, keep both files side by side in one folder and run `pytest`
  from there.
- **`collected 0 items`.** Your file is named `lending_test.py`, `tests.py`, or
  `test-lending.py`. Discovery wants `test_*.py` or `*_test.py`, and a hyphen is
  not legal in a Python module name anyway. This line is the most dangerous in
  the whole run, because it is green, not red.
- **A test function is silently skipped.** You named it `check_the_cap` instead
  of `test_the_cap`. `pytest` only collects functions whose name starts with
  `test_`, so yours never ran and the suite still went green.
- **`Failed: DID NOT RAISE <class 'ValueError'>` after you added the guard.**
  You wrote `if days_late > 0:` instead of `< 0`, or you built the exception
  without raising it — `ValueError("...")` alone on a line creates an object and
  throws it away. On pytest 9 the caret points at the `with pytest.raises(...)`
  line:

  ```text
  $ pytest -q
  ...FF                                                                    [100%]
  ================================== FAILURES ===================================
  __________________________ test_fee_stops_at_the_cap __________________________

      def test_fee_stops_at_the_cap() -> None:
  >       assert late_fee_cents(100) == MAX_FEE_CENTS
  E       assert 2500 == 1000
  E        +  where 2500 = late_fee_cents(100)

  test_lending.py:10: AssertionError
  _______________________ test_negative_days_is_rejected ________________________

      def test_negative_days_is_rejected() -> None:
  >       with pytest.raises(ValueError):
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  E       Failed: DID NOT RAISE <class 'ValueError'>

  test_lending.py:12: Failed
  =========================== short test summary info ===========================
  FAILED test_lending.py::test_fee_stops_at_the_cap - assert 2500 == 1000
  FAILED test_lending.py::test_negative_days_is_rejected - Failed: DID NOT RAIS...
  2 failed, 3 passed in 0.04s
  ```

- **`assert 2500 == 1000` still appears after the fix.** You edited a second
  copy of `lending.py` in another folder. Run
  `python -c "import lending; print(lending.__file__)"` to see which one is
  actually imported.
- **All five pass on the very first run.** You fixed `lending.py` before writing
  the tests. Revert the module and watch the red. The red is the part that
  proves the test works.

## Under the hood

<details>
<summary>Under the hood — what "min swapped for max" actually breaks, and why four tests catch it</summary>

Step 6 asks you to swap `min` for `max` on purpose. It is worth reading the whole
report rather than just noting that something went red:

```text
$ pytest -q
FFFF.                                                                    [100%]
================================== FAILURES ===================================
____________________________ test_on_time_is_free _____________________________

    def test_on_time_is_free() -> None:
>       assert late_fee_cents(0) == 0
E       assert 1000 == 0
E        +  where 1000 = late_fee_cents(0)

test_lending.py:4: AssertionError
...
=========================== short test summary info ===========================
FAILED test_lending.py::test_on_time_is_free - assert 1000 == 0
FAILED test_lending.py::test_one_day_late_costs_a_quarter - assert 1000 == 25
FAILED test_lending.py::test_ten_days_late_costs_two_fifty - assert 1000 == 250
FAILED test_lending.py::test_fee_stops_at_the_cap - assert 2500 == 1000
4 failed, 1 passed in 0.05s
```

Four failures, not one. `max(0, 1000)` is `1000`, so an on-time return is now
billed ten dollars — a much worse bug than the one you started with, and the
suite catches it four different ways. That overlap is a feature: overlapping
tests are how a suite survives a change nobody thought carefully about. The one
test that still passes is the negative-days one, because swapping `min` for `max`
never touched the guard clause.

A note on wording, since search engines have not caught up. pytest 8 printed
`Failed: DID NOT RAISE <class 'ValueError'>` and pointed the `>` marker at the
call *inside* the `with`. pytest 9 keeps that same message but points the caret
at the `with pytest.raises(...)` line itself. Same failure, slightly different
picture; both mean "the block finished without the exception you promised".

</details>

## Acceptance checklist

- [ ] `pytest -v` collects exactly five tests from `test_lending.py`.
- [ ] You saw the two-failure run before you touched `lending.py`.
- [ ] All five pass after a two-line change to `lending.py`.
- [ ] The cap test references `MAX_FEE_CENTS`, not the literal `1000`.
- [ ] Swapping `min` for `max` turns four of the five tests red.
- [ ] Both files are committed with a message like
      `Add Week 11 exercise 1: first pytest tests for late fees`.

## Stretch

- Tighten the exception test with
  `pytest.raises(ValueError, match="cannot be negative")`. `match=` is a regex,
  so a literal `.` or `(` in your message needs escaping.
- Add a failure message to one assertion:
  `assert late_fee_cents(100) == MAX_FEE_CENTS, f"got {late_fee_cents(100)}"`.
  Force it to fail, compare it to the bare version, and decide for yourself when
  the message earns its keep.
- Run `pytest -x -q`, then `pytest --lf`. The first stops at the first failure;
  the second reruns only what failed last time.

When your five tests are green, move on to
[Exercise 2 — Sharing Setup With Fixtures](./exercise-02-fixtures.md).
