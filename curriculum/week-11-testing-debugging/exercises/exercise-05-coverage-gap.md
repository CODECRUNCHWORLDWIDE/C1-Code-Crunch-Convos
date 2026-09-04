# Exercise 5 — Finding the Missing Branch

> **Topic:** `pytest-cov`, reading the `Missing` column, and why line coverage is not branch coverage
> **Lecture:** [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md) (section 6)
> **Difficulty:** Medium
> **Target time:** 35 minutes
> **Why this one:** you will finish the week with a mini-project that has to hit 100 % coverage, and Friday is a bad day to learn what the coverage report is telling you. More importantly, this exercise shows you the trap: a module can report 100 % line coverage while an entire `if` branch has never been taken. Anyone who trusts the first number without checking the second ships that branch untested.

## The Brief

`holds.py` is the last piece of the tool library system. It decides what to tell
a member about an item — available, reserved, or waitlist — clamps a late fee to
the house maximum, and builds the notification line the front desk sends out.

Three small functions, eighteen statements, and a test file somebody started and
abandoned. Coverage is a tool that watches your tests run and reports which lines
of the module actually executed. You are going to run it over `holds.py`, find
that a fifth of the module never ran, close that gap, and then find that even at
100 % there is still a branch nobody has taken. The work is not writing clever
tests. It is learning to read two tables and act on them.

## Starter

`holds.py`, exactly as given — the line numbers matter, because the coverage
report will point at them:

```python
"""holds.py — shelf status, fee caps, and member notices."""

FEE_CAP_CENTS: int = 1_000


def shelf_status(copies: int, holds: int) -> str:
    """Return the shelf status for an item.

    Raises:
        ValueError: If either count is negative.
    """
    if copies < 0 or holds < 0:
        raise ValueError("counts cannot be negative")
    if copies == 0:
        return "waitlist"
    if holds >= copies:
        return "reserved"
    return "available"


def apply_cap(fee_cents: int) -> int:
    """Clamp a late fee to the house maximum."""
    if fee_cents > FEE_CAP_CENTS:
        fee_cents = FEE_CAP_CENTS
    return fee_cents


def notify(status: str, email: str | None = None) -> str:
    """Build the notice line for a member."""
    message = f"Your item is {status}."
    if email:
        message = f"{message} We emailed {email}."
    return message
```

`test_holds.py`, the abandoned starter. Do not delete these three — add to them:

```python
"""test_holds.py — coverage-driven tests for holds.py."""

import pytest

from holds import FEE_CAP_CENTS, apply_cap, notify, shelf_status


def test_copies_free_and_no_holds_is_available() -> None:
    assert shelf_status(3, 1) == "available"


def test_notify_without_an_email() -> None:
    assert notify("available") == "Your item is available."


def test_cap_clamps_a_big_fee() -> None:
    assert apply_cap(5_000) == FEE_CAP_CENTS


# TODO (round one — close the Missing column):
#   test_zero_copies_is_waitlist
#   test_holds_equal_to_copies_is_reserved
#   test_negative_copies_is_rejected
#   test_notify_with_an_email

# TODO (round two — close the branch gap that survives 100 % line coverage):
#   test_cap_leaves_a_small_fee_alone
```

## Requirements

1. Run coverage **before** writing anything. Record the percentage and the
   contents of the `Missing` column.
2. Add the four round-one tests. Re-run with `--cov-report=term-missing` and
   confirm 100 % with an empty `Missing` column.
3. Re-run with `--cov-branch` added. Confirm the report drops below 100 % and
   names a partial branch in the form `23->25`.
4. Add the single round-two test that closes it, and confirm 100 % with
   `--cov-branch` still on.
5. `test_negative_copies_is_rejected` uses
   `pytest.raises(ValueError, match="cannot be negative")`.
6. `test_holds_equal_to_copies_is_reserved` uses equal counts — three copies,
   three holds — because `>=` is the boundary and `>` is the bug you are
   guarding against.
7. Every new test has at least one `assert`. Eight tests when you are done.

## Constraints

- **Report on `holds` specifically: `--cov=holds`.** A bare `--cov` measures
  every file it can see, including `pytest` itself and your virtual environment,
  and the number it returns is meaningless. Point coverage at code you own.
- **Never write a test purely to move the percentage.** Calling
  `shelf_status(0, 0)` with no assertion covers line 15 and proves nothing. The
  tool cannot tell the difference; a reviewer can, and so can the bug that ships
  anyway.
- **Read the `Missing` column as line numbers, not as a score.** `13, 15, 17,
  32` is a to-do list with four items on it. Open the file at those lines and
  ask what input would get you there. That question is the whole exercise.
- **`23->25` is a branch, not a line.** It means execution never went from line
  23 straight to line 25 — the `if` was never false. Both lines ran, so line
  coverage is satisfied and branch coverage is not. This is why the mini-project
  config sets `branch = true`.
- **Do not raise `fail_under` to 100 everywhere out of habit.** A threshold you
  cannot meet gets lowered, and a threshold that gets lowered teaches the team
  the number is negotiable. `holds.py` reaches 100 because it is eighteen
  statements of pure logic. Real modules land closer to 90.

## Expected output

The shipped answer below writes `holds.py` and `test_holds.py` into a scratch
folder, then runs `pytest --cov` four times — the whole story from 78 % to
100 % — and prints only the stable numbers it parses back:

```text
$ python exercise-05-coverage-gap.py
Coverage measures which lines ran, nothing more. Watch the gap open twice.

Statement coverage, the three starter tests only:
  18 statements, 4 missed, 78%   missing lines 13, 15, 17, 32
Statement coverage, all eight tests:
  18 statements, 0 missed, 100%   missing lines (none)
Branch coverage, all eight tests EXCEPT the small-fee test:
  18 statements, 10 branches, 1 partial, 96%   missing arc 23->25
Branch coverage, all eight tests:
  18 statements, 10 branches, 0 partial, 100%   missing arc (none)

Even at 100% branch coverage, shelf_status never checks whether the
member already holds a copy. Coverage cannot see a rule nobody wrote down.
```

Doing it yourself, you run the `pytest --cov` commands from **Steps** and read
the tables directly. The raw tables are shown under **Under the hood**.

## Steps

1. Install the plugin: `python -m pip install pytest-cov`. Confirm a
   `plugins: cov-...` line appears in the header.
2. Save `holds.py` and `test_holds.py`. Run
   `pytest --cov=holds --cov-report=term-missing` and note the 78 % and the four
   line numbers.
3. Open `holds.py` at lines 13, 15, 17, and 32. For each, write down the
   argument that would reach it *before* you write the test.
4. Add the four round-one tests. Re-run: 100 %, empty `Missing` column.
5. Add `--cov-branch` and re-run. Watch it drop to 96 % with `23->25` listed.
6. Add `test_cap_leaves_a_small_fee_alone` — `apply_cap(250) == 250`. Re-run
   with `--cov-branch`. 100 %, `BrPart` back to 0.
7. Generate the HTML report with `--cov-report=html` and open
   `htmlcov/index.html`. Covered lines are green, missed red, partial branches
   yellow. Delete one of your tests and look again.

## The Solution

```python
"""exercise-05-coverage-gap-solution.py — coverage, statement and branch, headless.

Coverage answers exactly one question — which lines ran — and people read it as
an answer to a different one: is this code tested. This file watches the gap
between those two questions open twice, once at 78 % and once at 96 %.

A coverage run needs a real module and a real test file on disk, so this script
writes ``holds.py`` and ``test_holds.py`` into a throwaway folder, then shells
out to ``pytest --cov`` four times — once per column of the story — and prints
only the stable numbers it parses back. No timings, no banners: the report is
the same on every machine.

Run it with::

    python exercise-05-coverage-gap-solution.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

# --------------------------------------------------------------------------- #
# The two files coverage will measure — written to a temp folder at run time
# --------------------------------------------------------------------------- #

HOLDS_PY = '''\
"""holds.py — shelf status, fee caps, and member notices."""

FEE_CAP_CENTS: int = 1_000


def shelf_status(copies: int, holds: int) -> str:
    """Return the shelf status for an item.

    Raises:
        ValueError: If either count is negative.
    """
    if copies < 0 or holds < 0:
        raise ValueError("counts cannot be negative")
    if copies == 0:
        return "waitlist"
    if holds >= copies:
        return "reserved"
    return "available"


def apply_cap(fee_cents: int) -> int:
    """Clamp a late fee to the house maximum."""
    if fee_cents > FEE_CAP_CENTS:
        fee_cents = FEE_CAP_CENTS
    return fee_cents


def notify(status: str, email: str | None = None) -> str:
    """Build the notice line for a member."""
    message = f"Your item is {status}."
    if email:
        message = f"{message} We emailed {email}."
    return message
'''

TEST_HOLDS_PY = '''\
"""test_holds.py — coverage-driven tests for holds.py."""

import pytest

from holds import FEE_CAP_CENTS, apply_cap, notify, shelf_status


def test_copies_free_and_no_holds_is_available() -> None:
    assert shelf_status(3, 1) == "available"


def test_notify_without_an_email() -> None:
    assert notify("available") == "Your item is available."


def test_cap_clamps_a_big_fee() -> None:
    assert apply_cap(5_000) == FEE_CAP_CENTS


def test_zero_copies_is_waitlist() -> None:
    assert shelf_status(0, 2) == "waitlist"


def test_holds_equal_to_copies_is_reserved() -> None:
    assert shelf_status(3, 3) == "reserved"


def test_negative_copies_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        shelf_status(-1, 0)


def test_notify_with_an_email() -> None:
    assert notify("reserved", "ada@example.org") == (
        "Your item is reserved. We emailed ada@example.org."
    )


def test_cap_leaves_a_small_fee_alone() -> None:
    assert apply_cap(250) == 250
'''

# The three tests the starter shipped with, versus the two rounds you add.
STARTER_ONLY = "available or notify_without_an_email or cap_clamps_a_big_fee"
WITHOUT_ROUND_TWO = "not cap_leaves_a_small_fee_alone"


def run_coverage(folder: Path, branch: bool, select: str | None) -> list[str]:
    """Run pytest --cov in *folder* and return the parsed ``holds.py`` row."""
    cmd = [sys.executable, "-m", "pytest", "--cov=holds",
           "--cov-report=term-missing", "-p", "no:cacheprovider", "-q"]
    if branch:
        cmd.append("--cov-branch")
    if select:
        cmd += ["-k", select]
    result = subprocess.run(cmd, cwd=folder, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    for line in result.stdout.splitlines():
        if line.startswith("holds.py"):
            return line.split()
    return ["holds.py", "(no coverage row — is pytest-cov installed?)"]


def main() -> None:
    """Write the module and tests, then narrate coverage in four runs."""
    print("Coverage measures which lines ran, nothing more. Watch the gap open twice.")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        (folder / "holds.py").write_text(HOLDS_PY, encoding="utf-8")
        (folder / "test_holds.py").write_text(TEST_HOLDS_PY, encoding="utf-8")

        # 1. statement coverage, the three starter tests only
        name, stmts, miss, cover, *missing = run_coverage(folder, False, STARTER_ONLY)
        print("Statement coverage, the three starter tests only:")
        print(f"  {stmts} statements, {miss} missed, {cover}   missing lines "
              f"{' '.join(missing) or '(none)'}")

        # 2. statement coverage, all eight tests
        name, stmts, miss, cover, *missing = run_coverage(folder, False, None)
        print("Statement coverage, all eight tests:")
        print(f"  {stmts} statements, {miss} missed, {cover}   missing lines "
              f"{' '.join(missing) or '(none)'}")

        # 3. branch coverage, everything except the round-two test
        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, WITHOUT_ROUND_TWO)
        print("Branch coverage, all eight tests EXCEPT the small-fee test:")
        print(f"  {stmts} statements, {branch} branches, {brpart} partial, {cover}"
              f"   missing arc {' '.join(missing) or '(none)'}")

        # 4. branch coverage, all eight tests
        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, None)
        print("Branch coverage, all eight tests:")
        print(f"  {stmts} statements, {branch} branches, {brpart} partial, {cover}"
              f"   missing arc {' '.join(missing) or '(none)'}")

    print()
    print("Even at 100% branch coverage, shelf_status never checks whether the")
    print("member already holds a copy. Coverage cannot see a rule nobody wrote down.")


if __name__ == "__main__":
    main()
```

**The `Missing` column is a to-do list, not a score.** `13, 15, 17, 32` is four
line numbers with four names attached. Open the file at each one and ask what
argument gets you there — that question, not the typing of the test, is the
work. Reading the number instead ("78 %, could be worse") skips the only useful
thing the tool produces. And notice: all four of `shelf_status`'s interesting
answers were unreached while the module reported a comfortable-sounding
percentage. Three quarters of a function's behaviour can hide inside a figure
that does not look alarming.

**Branch coverage asks a different question, and `23->25` is the shape of the
answer.** That is not a line number, it is an *arc* — execution never went from
line 23 straight to line 25. Line 23 is `if fee_cents > FEE_CAP_CENTS:` and line
25 is `return fee_cents`, so the arc that never happened is the `if` being
false. Both lines ran (line 23 on every call, line 25 on every way out), so
statement coverage was satisfied while `apply_cap` had never once been asked to
*leave a fee alone*. That is the entire clamp behaviour, untested, at 100 %.

**`apply_cap(250)` is chosen so the `if` is false.** The value has to be
comfortably under the cap. `apply_cap(1_001)` takes the same true branch as
`apply_cap(5_000)`, adds a test, and closes nothing — the report stays at 96 %.
Pick the input that answers the question the report asked.

**`shelf_status(3, 3)` because `>=` is the boundary.** The condition is
`holds >= copies`, and the plausible wrong version is `>`. Only equal counts can
tell them apart: three copies and two holds still leaves one on the shelf, so
`shelf_status(3, 2)` is `"available"` under both versions. Every time you test a
comparison, ask which input distinguishes `>` from `>=` — that is the one to
write down.

**When it says 100 %, believe only what it said.** `holds.py` reaches 100 % on
eighteen statements and is still wrong: `shelf_status` never checks whether the
member already holds a copy, and no coverage tool will ever mention a rule that
nobody wrote down. Coverage measures what ran. It has nothing to say about what
should have.

## Run it

Copy the worked answer on this page into `exercise-05-coverage-gap.py` and run it:

```bash
python exercise-05-coverage-gap.py
```

It needs `pytest` and `pytest-cov` installed. It writes its own throwaway
`holds.py` and `test_holds.py` into a temp folder, so it leaves nothing behind.
Your own work is `holds.py` plus `test_holds.py`, run with the `pytest --cov`
commands above.

The `-solution` in the filename keeps this file from colliding with your own
`holds.py` and `test_holds.py`.

## Common bugs to catch

- **`Coverage.py warning: No data was collected. (no-data-collected)` and 0 %.**
  You passed `--cov=holds.py` with the extension. The argument is a module or
  package name, not a filename — coverage went looking for a module with a dot
  in its name and found none.
- **The `Missing` column disappears.** You dropped `--cov-report=term-missing`
  and got the plain report, which shows the percentage but not the line numbers.
  The line numbers are the useful part.
- **`AssertionError: assert 'available' == 'reserved'`.** You wrote
  `shelf_status(3, 2)` for the reserved test. Two holds against three copies
  leaves one on the shelf. The boundary is equal counts — `shelf_status(3, 3)`.
- **`Failed: DID NOT RAISE <class 'ValueError'>` on the negative test.** You
  passed `shelf_status(0, -1)` and assumed the `copies == 0` check wins. The
  guard on line 12 runs first and covers *both* arguments, so this should raise.
  If it does not, you are importing a different copy of `holds`.
- **Branch coverage stays at 96 % after the small-fee test.** Your new value is
  still above the cap — `apply_cap(1_001)` takes the same true branch as
  `apply_cap(5_000)` and closes nothing. Pass something clearly under, like 250,
  so the `if` is false and execution jumps from 23 to 25.
- **You hit 100 % and assume the module is correct.** It is not. `shelf_status`
  never checks whether a member already holds a copy, and no coverage tool will
  ever tell you about a rule nobody wrote down. Coverage measures what ran, not
  what should have.

## Under the hood

<details>
<summary>Under the hood — the raw tables, and the assertion coverage cannot see</summary>

The script parses these tables down to the stable numbers; here is what pytest
actually prints. The baseline, three tests, statement coverage only:

```text
$ pytest --cov=holds --cov-report=term-missing
...                                                                      [100%]
=============================== tests coverage ================================
Name       Stmts   Miss  Cover   Missing
----------------------------------------
holds.py      18      4    78%   13, 15, 17, 32
----------------------------------------
TOTAL         18      4    78%
3 passed, 5 deselected in 0.08s
```

The same suite once you add `--cov-branch`, with the round-two test still held
back — every statement ran, but one branch arc never did:

```text
$ pytest --cov=holds --cov-branch --cov-report=term-missing
.......                                                                  [100%]
=============================== tests coverage ================================
Name       Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------
holds.py      18      0     10      1    96%   23->25
------------------------------------------------------
TOTAL         18      0     10      1    96%
7 passed, 1 deselected in 0.10s
```

Now the most important thing about the whole tool. Replace
`assert apply_cap(250) == 250` with a bare `apply_cap(250)` — a call, no
assertion — and the eighth test still runs the same lines, so the report still
reads **100 % branch coverage**. Coverage cannot tell a test from a call. A
reviewer can, and so can the bug that ships anyway. The percentage is not the
thing; the assertions are.

</details>

## Acceptance checklist

- [ ] You recorded the 78 % baseline and its four line numbers before writing
      any test.
- [ ] Statement coverage reaches 100 % with an empty `Missing` column.
- [ ] `--cov-branch` exposed the `23->25` partial branch at 96 %.
- [ ] Branch coverage reaches 100 % with `BrPart` at 0.
- [ ] Eight tests, every one with a real assertion.
- [ ] You opened `htmlcov/index.html` and read the colored source view.
- [ ] Committed with a message like
      `Add Week 11 exercise 5: close the coverage and branch gaps in holds.py`.

## Stretch

- Move the settings into a `pyproject.toml` here — `branch = true`,
  `show_missing = true`, `fail_under = 100` — so plain `pytest --cov=holds`
  behaves like your full command line.
- Delete one assertion, not the test, and re-run. Coverage stays at 100 %. Sit
  with that. It is the most important thing to understand about this tool.
- Install `mutmut` and run it over `holds.py`. It flips `>=` to `>`, `+` to `-`,
  and reports which mutations your suite failed to catch. A surviving mutant is
  a gap 100 % coverage did not find.

That is Week 11's drills done. You can now write tests, share setup with
fixtures, drive a table of cases, fake a network boundary, and read a coverage
report. Take those into the bigger problems:
[Week 11 Challenges](../challenges/README.md).
