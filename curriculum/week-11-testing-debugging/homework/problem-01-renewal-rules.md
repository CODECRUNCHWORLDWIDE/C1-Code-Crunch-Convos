# Homework Problem 1 — Renewal rules

> **Topic:** Turning an English rule into a function and the tests that prove it, boundary included
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md) (sections 3–6)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** most bugs are not clever — they are a boundary nobody tested. This problem is small enough that the only real work is choosing the five inputs that pin every clause of the rule, including the exact edge where "one more renewal" becomes "no more."

## The Brief

The tool library lets a member renew a loan, but not forever, and not while
someone else is waiting. The rule, in full: a loan may be renewed up to **two**
times, but never while another member is on the waitlist for that item. A
negative renewal count is not a decision at all — it means whoever called you
has a bug.

Your job is two things at once: write `can_renew`, and write the tests that
prove it obeys every clause. The interesting test is the boundary. "Up to two
times" means two renewals is the *limit* — a member who has already renewed
twice is refused a third. Off-by-one bugs live exactly there, so that is the
input worth writing down.

## Starter

The module you fill in:

```python
"""renewal.py — the loan renewal rule for the tool library."""

MAX_RENEWALS: int = 2


def can_renew(times_renewed: int, someone_waiting: bool) -> bool:
    """Decide whether a member may renew a loan again.

    A loan may be renewed up to ``MAX_RENEWALS`` times, but never while another
    member is waiting for the item. A negative renewal count is a caller bug.
    """
    # TODO: raise ValueError("times_renewed cannot be negative") for a negative count
    # TODO: return False if someone_waiting
    # TODO: otherwise return whether times_renewed is still under MAX_RENEWALS
    return True
```

The test file you write:

```python
"""test_renewal.py — one clause of the rule per test."""

import pytest

from renewal import MAX_RENEWALS, can_renew


def test_fresh_loan_can_renew() -> None:
    # TODO: never renewed, nobody waiting -> True


def test_one_renewal_can_renew_again() -> None:
    # TODO: one renewal used, one still allowed -> True


def test_at_the_limit_cannot_renew() -> None:
    # TODO: MAX_RENEWALS used, nobody waiting -> False  (this is the boundary)


def test_waitlist_blocks_even_a_fresh_loan() -> None:
    # TODO: 0 renewals but someone_waiting=True -> False


def test_negative_count_is_rejected() -> None:
    # TODO: pytest.raises(ValueError, match="cannot be negative") around can_renew(-1, False)
```

## Requirements

1. `test_renewal.py` contains exactly five tests, named as in the starter.
2. `test_at_the_limit_cannot_renew` passes `MAX_RENEWALS`, the imported
   constant, not the literal `2`.
3. Compare booleans with `is True` / `is False`, not `== True`. The function
   promises a bool; `is` notices if it ever returns something merely truthy.
4. `test_negative_count_is_rejected` uses
   `pytest.raises(ValueError, match="cannot be negative")`.
5. All five pass with `pytest -v`.

## Constraints

- **The limit is a boundary, so test the boundary.** `can_renew(2, False)` is
  the one input that tells `<` from `<=` in your implementation. A test at
  `0` and a test at `5` would both pass under either version and prove nothing
  about where the line actually falls.
- **`someone_waiting` outranks the count.** A member owed a renewal still cannot
  have one while somebody waits. Check the waitlist before the count, so the
  more important rule wins.
- **Import `MAX_RENEWALS`; do not hard-code `2`.** If the board raises the limit
  to three next year, correct code keeps working and a test with a literal `2`
  goes red for no reason.
- **A negative count raises; it is never `False`.** Answering `False` politely
  would swallow a caller's bug — a typo like `renewed - 1` when `renewed` is `0`
  — instead of surfacing it.

## Expected output

The shipped answer folds `renewal.py`, the five tests, and a driver into one
file so it runs as a plain script. It prints the decision table, then runs the
suite through pytest:

```text
$ python problem-01-renewal-rules.py
can_renew(times_renewed, someone_waiting):
  renewed=0, waiting=False -> True
  renewed=1, waiting=False -> True
  renewed=2, waiting=False -> False
  renewed=0, waiting=True  -> False
  renewed=-1                 -> ValueError: times_renewed cannot be negative

The five tests, run the way pytest runs them:
  PASS  test_fresh_loan_can_renew
  PASS  test_one_renewal_can_renew_again
  PASS  test_at_the_limit_cannot_renew
  PASS  test_waitlist_blocks_even_a_fresh_loan
  PASS  test_negative_count_is_rejected

5 passed, 0 failed
```

Doing it for real, you run `pytest -v` and see five `PASSED` lines.

## Steps

1. Save `renewal.py` and `test_renewal.py` side by side.
2. Write the five tests first, then run `pytest -v`. They all fail, because the
   starter always returns `True`. That is your red.
3. Fill in the guard clause, then the waitlist check, then the count comparison.
4. Rerun after each change and watch the failures fall one at a time.
5. Break it on purpose: change `<` to `<=` in the count check and confirm
   `test_at_the_limit_cannot_renew` goes red. Put it back.

## The Solution

```python
"""problem-01-renewal-rules-solution.py — a decision function, fully tested.

You are handed a rule in English and asked to turn it into a function *and* the
tests that prove it. The skill is choosing inputs that pin every clause of the
rule — including the boundary, where off-by-one bugs live.

One file carries the module, the tests, and a ``main()`` that drives pytest and
prints a plain, same-every-time report. In your own folder you keep the module
and the tests in two files and run ``pytest``.

Run it with::

    python problem-01-renewal-rules-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# renewal.py — the module under test
# --------------------------------------------------------------------------- #

MAX_RENEWALS: int = 2


def can_renew(times_renewed: int, someone_waiting: bool) -> bool:
    """Decide whether a member may renew a loan again.

    A loan may be renewed up to ``MAX_RENEWALS`` times, but never while another
    member is waiting for the item. A negative renewal count is a caller bug.
    """
    if times_renewed < 0:
        raise ValueError("times_renewed cannot be negative")
    if someone_waiting:
        return False
    return times_renewed < MAX_RENEWALS


# --------------------------------------------------------------------------- #
# test_renewal.py — one clause of the rule per test
# --------------------------------------------------------------------------- #


def test_fresh_loan_can_renew() -> None:
    """Never renewed, nobody waiting: yes."""
    assert can_renew(0, someone_waiting=False) is True


def test_one_renewal_can_renew_again() -> None:
    """One renewal used, one still allowed."""
    assert can_renew(1, someone_waiting=False) is True


def test_at_the_limit_cannot_renew() -> None:
    """Two renewals used is the limit, so a third is refused."""
    assert can_renew(MAX_RENEWALS, someone_waiting=False) is False


def test_waitlist_blocks_even_a_fresh_loan() -> None:
    """Someone waiting outranks a renewal you would otherwise be owed."""
    assert can_renew(0, someone_waiting=True) is False


def test_negative_count_is_rejected() -> None:
    """A negative renewal count is a caller bug, not a decision."""
    with pytest.raises(ValueError, match="cannot be negative"):
        can_renew(-1, someone_waiting=False)


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes."""
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Show the decision table, then run the suite and print the outcomes."""
    print("can_renew(times_renewed, someone_waiting):")
    for renewed, waiting in [(0, False), (1, False), (2, False), (0, True)]:
        print(f"  renewed={renewed}, waiting={waiting!s:<5} -> "
              f"{can_renew(renewed, waiting)}")
    try:
        can_renew(-1, someone_waiting=False)
    except ValueError as error:
        print(f"  renewed=-1                 -> ValueError: {error}")

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

**The waitlist check comes before the count check, on purpose.** The rule has a
priority: someone waiting beats a renewal you would otherwise be owed. Writing
the checks in priority order means the code reads like the rule, and the more
important condition can never be skipped.

**`times_renewed < MAX_RENEWALS` is the whole boundary.** Two renewals used is
the limit, so a member at the limit must be refused — `2 < 2` is `False`, which
is exactly right. The plausible bug is `<=`, which would allow a third renewal;
`test_at_the_limit_cannot_renew` is the single test that can tell the two apart.

**The guard raises rather than returning `False`.** `can_renew(-1, False)` is not
a member who cannot renew — it is a caller who computed a nonsense number.
Raising turns that into a loud failure at the source instead of a quiet wrong
answer downstream.

**`is True` / `is False`, not `== True`.** The function's contract is a real
bool. Comparing with `is` means a future version that accidentally returns a
truthy string or a `1` fails the test instead of sliding by.

## Run it

Copy the worked answer on this page into `problem-01-renewal-rules.py` and run it:

```bash
python problem-01-renewal-rules.py
```

It needs `pytest` and nothing else. Your own work is `renewal.py` plus
`test_renewal.py`, run with `pytest -v`.

The `-solution` in the filename keeps this file from colliding with your own
`renewal.py` and `test_renewal.py`.

## Common bugs to catch

- **`test_at_the_limit_cannot_renew` fails with `assert True is False`.** You
  wrote `<=` where the rule needs `<`. Two renewals is the limit, not one past it.
- **`test_waitlist_blocks_even_a_fresh_loan` fails.** You checked the count
  before the waitlist and returned early, so the waitlist never got a say. Check
  `someone_waiting` first.
- **`Failed: DID NOT RAISE <class 'ValueError'>`.** Your guard is `> 0` instead
  of `< 0`, or you built the exception without a `raise` in front of it. On
  pytest 9 the caret points at the `with pytest.raises(...)` line.
- **The suite passes with the literal `2` in the test.** It will — until the
  limit changes. Requirement 2 exists so a config change does not create a false
  alarm.

## Under the hood

<details>
<summary>Under the hood — why the boundary case is the only one that earns its keep</summary>

Five tests, but they are not equally valuable. `test_fresh_loan_can_renew` and
`test_waitlist_blocks_even_a_fresh_loan` both use `times_renewed = 0`, so neither
can tell `<` from `<=` — under either implementation they pass. The same is true
of any input comfortably away from the limit.

Only `can_renew(2, False)` sits *on* the boundary, where the two plausible
implementations disagree: `2 < 2` is `False` (correct) and `2 <= 2` is `True`
(the bug). This is the general shape of testing a comparison — for every `<`,
`<=`, `>`, `>=` in your code, there is exactly one input that distinguishes it
from its neighbour, and that input is the one worth writing down. The others are
reassurance; this one is a test.

</details>

## Acceptance checklist

- [ ] Five tests, named as in the starter, all passing.
- [ ] The limit test uses `MAX_RENEWALS`, not the literal `2`.
- [ ] Booleans compared with `is True` / `is False`.
- [ ] Swapping `<` for `<=` turns the boundary test red.
- [ ] Committed with a message like
      `Add Week 11 homework 1: renewal rules with a boundary test`.

## Stretch

- Add `can_renew` overloads for a `VIP` member who gets three renewals, driven
  by a new argument, and a parametrized test over `(renewed, vip, expected)`.
- Tighten the exception test's `match=` to the full message and watch it still
  pass — then change the message by one word and watch it fail.
- Write a property: for any non-negative `times_renewed`, if `someone_waiting`
  is `True` the answer is always `False`. Test it over a handful of counts.

When your five are green, move on to
[Problem 2 — Dues ledger](./problem-02-dues-ledger.md).
