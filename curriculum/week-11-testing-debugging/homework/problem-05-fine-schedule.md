# Homework Problem 5 — Fine schedule

> **Topic:** `pytest-cov`, the `Missing` column, statement vs branch coverage
> **Lecture:** [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md) (section 6)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** the mini-project has to hit 100 % *branch* coverage, so first watch a tiny module reach 100 % *statement* coverage while a whole `if` branch stays untaken.

## The Brief

A library charges a fine when you bring a tool back late. The fine grows with each
late day, but the house has a rule: it never goes over $20. In the code that $20
is written as `2000` cents. When a fine climbs past the cap, the code pushes it
back down to the cap. That pushing-down step is called a clamp — like a ceiling
the number cannot poke through.

Here is the puzzle. Someone wrote a test file for `fines.py`. Every line of the
module gets run by those tests. And yet one path through the code has never once
happened: the clamp has only ever been asked to *fire*. Nobody has handed it a
small fine and watched it leave that fine alone.

Coverage is a tool that sits and watches your tests run, then tells you which
lines actually executed. You will run it, see a gap, close the gap, then flip on
a second setting called branch coverage — and find one path still open.

## Starter

`fines.py`, given complete. Do not change it — the line numbers matter, because
the coverage report will point right at them:

```python
"""fines.py — the overdue fine schedule."""

CAP_CENTS: int = 2_000


def fine_cents(days_late: int, is_student: bool = False) -> int:
    """Return the overdue fine in whole cents, clamped to the house cap."""
    if days_late < 0:
        raise ValueError("days_late cannot be negative")
    rate = 10 if is_student else 25
    fine = days_late * rate
    if fine > CAP_CENTS:
        fine = CAP_CENTS
    return fine
```

`test_fines.py`, the starter. Two tests are written for you. Do not delete them —
add the three that the `# TODO:` lines name:

```python
"""test_fines.py — coverage-driven tests for fines.py."""

import pytest

from fines import CAP_CENTS, fine_cents


def test_over_cap_standard() -> None:
    assert fine_cents(1_000) == CAP_CENTS


def test_over_cap_student() -> None:
    assert fine_cents(1_000, is_student=True) == CAP_CENTS


# TODO (round one — close the statement gap):
#   test_negative_rejected

# TODO (round two — close the branch gap that survives 100 % statement coverage):
#   test_normal_day_standard   fine_cents(2) == 50
#   test_zero_is_free          fine_cents(0) == 0
```

## Requirements

1. Run coverage **before** you write anything. Write down the percentage and the
   whole `Missing` column.
2. Add `test_negative_rejected`. Re-run with `--cov-report=term-missing` and
   confirm statement coverage reaches 100 % with an empty `Missing` column.
3. Re-run with `--cov-branch` added. Confirm the number drops below 100 % and
   names a partial arc in the form `12->14`.
4. Add the two round-two tests — the under-cap ones — and confirm 100 % with
   `--cov-branch` still on.
5. `test_negative_rejected` uses `pytest.raises(ValueError, match="cannot be negative")`.
6. Report on `fines` specifically with `--cov=fines`, never a bare `--cov`.
7. Every test has at least one `assert`. Five tests when you are done.

## Constraints

- **Use `--cov=fines`, not a bare `--cov`.** A bare `--cov` measures everything it
  can see, including `pytest` itself and your whole virtual environment, and the
  number it hands back means nothing. Point it at code you own.
- **Never write a test just to move the number.** Calling `fine_cents(2)` with no
  `assert` runs the line and proves nothing. The tool cannot tell a real test
  from an empty call — but a reviewer can, and so can the bug that ships anyway.
- **Read the `Missing` column as a to-do list of line numbers, not a score.**
  `9` is one item: open line 9, ask what input reaches it, write that test. That
  question is the whole exercise.
- **`12->14` is a branch, not a line.** It means execution never went from line 12
  straight to line 14 — the `if` was never false. Both lines ran, so statement
  coverage is happy and branch coverage is not. This is why the mini-project sets
  `branch = true`.
- **Do not reflexively set `fail_under = 100`.** A threshold you cannot meet gets
  lowered, and a threshold that gets lowered teaches the team the number is
  negotiable. `fines.py` reaches 100 because it is nine statements of pure logic.
  Real modules land closer to 90.

## Expected output

The shipped answer writes `fines.py` and `test_fines.py` into a scratch folder,
then shells out to `pytest --cov` three times — the whole story from 89 % to
100 % — and prints only the stable numbers it parses back:

```text
$ python problem-05-fine-schedule.py
Statement coverage can be 100% while a branch is never taken.

Statement coverage, the two starter tests only:
  9 statements, 1 missed, 89%   missing lines 9
Branch coverage, after adding the negative-days test:
  9 statements, 0 missed, 4 branches, 1 partial, 92%   missing arc 12->14
Branch coverage, all five tests:
  9 statements, 0 missed, 4 branches, 0 partial, 100%   missing arc (none)

The middle run reached 100% statements while the clamp's 'leave a small
fine alone' branch stayed untested. The last run's under-cap test closes it.
```

Doing it yourself, you run the `pytest --cov` commands from **Steps** and read the
tables directly. The raw tables are shown under **Under the hood**.

## Steps

1. Install the plugin: `python -m pip install pytest-cov`. Confirm a
   `plugins: cov-...` line shows up in the pytest header.
2. Save `fines.py` and `test_fines.py` side by side. Run
   `pytest --cov=fines --cov-report=term-missing` and note the 89 % and the one
   line number in `Missing`.
3. Open `fines.py` at line 9 and read it. It is the `raise` — the sad path when
   `days_late` is negative. No test ever handed it a negative number.
4. Add `test_negative_rejected`. Re-run: 100 % statements, empty `Missing`.
5. Add `--cov-branch` and re-run. Watch it drop to 92 % with `12->14` listed.
6. Add the under-cap tests — `fine_cents(2) == 50` and `fine_cents(0) == 0`.
   Re-run with `--cov-branch`. 100 %, `BrPart` back to 0.

## The Solution

```python
"""problem-05-fine-schedule-solution.py — coverage, statement and branch, headless.

``fines.py`` clamps an overdue fine to a house cap. A test file covers every
*statement* and still leaves one *branch* untaken — the clamp has only ever been
asked to fire, never to leave a small fine alone. This script writes the module
and tests to a scratch folder and shells out to ``pytest --cov`` three times to
show the gap, printing only the stable numbers it parses back.

Run it with::

    python problem-05-fine-schedule-solution.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

FINES_PY = '''\
"""fines.py — the overdue fine schedule."""

CAP_CENTS: int = 2_000


def fine_cents(days_late: int, is_student: bool = False) -> int:
    """Return the overdue fine in whole cents, clamped to the house cap."""
    if days_late < 0:
        raise ValueError("days_late cannot be negative")
    rate = 10 if is_student else 25
    fine = days_late * rate
    if fine > CAP_CENTS:
        fine = CAP_CENTS
    return fine
'''

TEST_FINES_PY = '''\
"""test_fines.py — coverage-driven tests for fines.py."""

import pytest

from fines import CAP_CENTS, fine_cents


def test_over_cap_standard() -> None:
    assert fine_cents(1_000) == CAP_CENTS


def test_over_cap_student() -> None:
    assert fine_cents(1_000, is_student=True) == CAP_CENTS


def test_negative_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        fine_cents(-1)


def test_normal_day_standard() -> None:
    assert fine_cents(2) == 50


def test_zero_is_free() -> None:
    assert fine_cents(0) == 0
'''

# The two tests the starter shipped with, versus the rounds you add.
STARTER_ONLY = "over_cap"
ROUND_ONE = "over_cap or negative_rejected"


def run_coverage(folder: Path, branch: bool, select: str | None) -> list[str]:
    """Run pytest --cov in *folder* and return the parsed ``fines.py`` row."""
    cmd = [sys.executable, "-m", "pytest", "--cov=fines",
           "--cov-report=term-missing", "-p", "no:cacheprovider", "-q"]
    if branch:
        cmd.append("--cov-branch")
    if select:
        cmd += ["-k", select]
    result = subprocess.run(cmd, cwd=folder, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    for line in result.stdout.splitlines():
        if line.startswith("fines.py"):
            return line.split()
    return ["fines.py", "(no coverage row — is pytest-cov installed?)"]


def main() -> None:
    """Write the module and tests, then narrate coverage in three runs."""
    print("Statement coverage can be 100% while a branch is never taken.")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        (folder / "fines.py").write_text(FINES_PY, encoding="utf-8")
        (folder / "test_fines.py").write_text(TEST_FINES_PY, encoding="utf-8")

        name, stmts, miss, cover, *missing = run_coverage(folder, False, STARTER_ONLY)
        print("Statement coverage, the two starter tests only:")
        print(f"  {stmts} statements, {miss} missed, {cover}   missing lines "
              f"{' '.join(missing) or '(none)'}")

        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, ROUND_ONE)
        print("Branch coverage, after adding the negative-days test:")
        print(f"  {stmts} statements, {miss} missed, {branch} branches, "
              f"{brpart} partial, {cover}   missing arc {' '.join(missing) or '(none)'}")

        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, None)
        print("Branch coverage, all five tests:")
        print(f"  {stmts} statements, {miss} missed, {branch} branches, "
              f"{brpart} partial, {cover}   missing arc {' '.join(missing) or '(none)'}")

    print()
    print("The middle run reached 100% statements while the clamp's 'leave a small")
    print("fine alone' branch stayed untested. The last run's under-cap test closes it.")


if __name__ == "__main__":
    main()
```

**The `Missing` column is a to-do list, not a score.** `89 %` sounds fine, so it
is tempting to nod and move on. But the column beside it says `9`, and line 9 is
the `raise` — the sad path where someone hands in a negative number of days.
Nobody exercised it. Reading the percentage instead of the column skips the only
useful thing the tool made: a list of exactly where the tests have not been.

**Branch coverage asks a different question, and `12->14` is the shape of the
answer.** That is not a line number, it is an *arc* — execution never went from
line 12 straight to line 14. Line 12 is `if fine > CAP_CENTS:` and line 14 is
`return fine`, so the arc that never happened is the `if` being *false*. Both
lines ran on every test (line 12 on the way in, line 14 on the way out), so
statement coverage was satisfied while the clamp had never once been asked to
*leave a small fine alone*. Every test so far handed it a fine over the cap.

**The under-cap test `fine_cents(2)` is chosen so the `if` is false.** Two late
days at 25 cents is 50 cents — comfortably under the $20 cap. That is what closes
`12->14`. A value *over* the cap, like `fine_cents(3000)`, takes the exact same
true arc the starter tests already took: it adds a test and closes nothing, and
the report stays at 92 %. Pick the input that answers the question the report
actually asked.

**Report on `fines` specifically.** `--cov=fines` points the tool at your one
module. A bare `--cov` sweeps in pytest and your virtual environment, and the
percentage it returns is about their code, not yours. The narrow flag is the one
that tells you something true.

**And 100 % still would not prove the fine amounts are right.** Coverage measures
what *ran*, not what *should have*. You could set the student rate to 10 or to
999 and coverage would say 100 % either way, because every line still executes.
The tool tells you which paths your tests visited. It has nothing to say about
whether the numbers those paths produce match the schedule.

## Run it

Copy the worked answer on this page into `problem-05-fine-schedule.py` and run it:

```bash
python problem-05-fine-schedule.py
```

It needs `pytest` and `pytest-cov` installed. It writes its own throwaway
`fines.py` and `test_fines.py` into a temp folder, so it leaves nothing behind.
Your own work is `fines.py` plus `test_fines.py`, run with the `pytest --cov`
commands above.

The `-solution` in the filename keeps this file from colliding with your own
`fines.py` and `test_fines.py`.

## Common bugs to catch

- **`Coverage.py warning: No data was collected. (no-data-collected)` and 0 %.**
  You passed `--cov=fines.py` with the extension. The argument is a module name,
  not a filename — coverage went hunting for a module with a dot in its name and
  found none. Drop the `.py`.
- **The `Missing` column disappears.** You dropped `--cov-report=term-missing` and
  got the plain report, which shows the percentage but not the line numbers. The
  line numbers are the useful part.
- **Branch coverage stays at 92 % after your new test.** Your value is still
  *over* the cap — `fine_cents(3000)` takes the same true arc as the starter
  tests and closes nothing. Pass something clearly under, like `fine_cents(2)`,
  so the `if` is false and execution jumps from 12 to 14.
- **`Failed: DID NOT RAISE <class 'ValueError'>` on the negative test.** Your
  guard reads `days_late > 0` instead of `< 0`, so a negative number slips past.
  If the given `fines.py` is unchanged this should raise; if it does not, you are
  importing a different copy of `fines`.
- **You hit 100 % and assume the code is correct.** It is not necessarily. A
  wrong rate or a wrong cap runs the same lines a right one does. Coverage says
  which paths ran, nothing about whether the fine amounts match the schedule.

## Under the hood

<details>
<summary>Under the hood — the raw tables, and the assertion coverage cannot see</summary>

The script parses these tables down to the stable numbers; here is what pytest
actually prints. The baseline, two starter tests, statement coverage only —
notice the `9` in `Missing`, the `raise` nobody reached:

```text
$ pytest --cov=fines --cov-report=term-missing
..                                                                       [100%]
=============================== tests coverage ================================
Name       Stmts   Miss  Cover   Missing
----------------------------------------
fines.py       9      1    89%   9
----------------------------------------
TOTAL          9      1    89%
2 passed in 0.06s
```

Now add the negative test and turn on `--cov-branch`, but hold back the under-cap
tests — every statement runs, yet one branch arc never does:

```text
$ pytest --cov=fines --cov-branch --cov-report=term-missing
...                                                                      [100%]
=============================== tests coverage ================================
Name       Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------
fines.py       9      0      4      1    92%   12->14
------------------------------------------------------
TOTAL          9      0      4      1    92%
3 passed in 0.08s
```

Now the most important thing about the whole tool. Take a passing test and
replace its `assert fine_cents(2) == 50` with a bare `fine_cents(2)` — a call,
no assertion — and that test still runs the same lines, so the report still reads
**100 %**. Coverage cannot tell a test from a call. A reviewer can, and so can
the bug that ships anyway. The percentage is not the thing; the assertions are.

</details>

## Acceptance checklist

- [ ] You recorded the 89 % baseline and its one line number before writing any test.
- [ ] Statement coverage reaches 100 % with an empty `Missing` column.
- [ ] `--cov-branch` exposed the `12->14` partial arc at 92 %.
- [ ] Branch coverage reaches 100 % with `BrPart` at 0.
- [ ] Five tests, every one with a real `assert`.
- [ ] You reported on `fines` with `--cov=fines`, not a bare `--cov`.

## Stretch

- Move the settings into a `pyproject.toml` here — `branch = true`,
  `show_missing = true` — so plain `pytest --cov=fines` behaves like your full
  command line.
- Delete one assertion, not the test, and re-run. Coverage stays at 100 %. Sit
  with that. It is the most important thing to understand about this tool.
- Install `mutmut` and run it over `fines.py`. It flips `>` to `>=`, `*` to `/`,
  and reports which mutations your suite failed to catch. A surviving mutant is a
  gap 100 % coverage did not find.

---

Next: [Problem 6 — Shelf order regression](./problem-06-shelf-order-regression.md).
