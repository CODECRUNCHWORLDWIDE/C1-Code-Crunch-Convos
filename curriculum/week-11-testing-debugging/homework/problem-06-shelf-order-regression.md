# Homework Problem 6 — Shelf order regression

> **Topic:** reproducing a bug with a failing test, then fixing it — regression testing
> **Lecture:** [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md)
> **Difficulty:** Advanced
> **Target time:** 1 hour
> **Why this one:** the most valuable test you ever write is the one that reproduces a real bug, because it is the one that stops the bug coming back.

## The Brief

A member sends in a complaint. On the front-desk shelf list, the shelf `A-10`
shows up **before** `A-2`. That is backwards. Bay 2 comes before bay 10, the
same way page 2 comes before page 10 in a book. Something is putting the shelves
in the wrong order.

Here is why it happens. The current `shelf_order` sorts the codes as plain
words. A word sort walks left to right and compares one letter at a time. It
lines up `A-1` and `A-2`, sees that `1` comes before `2`, and stops right there
— it never notices that `A-10` has a `0` after the `1`. So `A-10` sneaks in
front of `A-2` because `A-1...` looks smaller than `A-2` letter by letter.

What people actually want is called a **natural sort** — the way a person would
do it. A person reads the slot part as a *number*, not a word. As a number,
`2` is plainly less than `10`, so `A-2` comes before `A-10`. That is the whole
fix in one sentence: read the slot as a number.

But you are not just here to fix code. You are here to practice the debugging
discipline, and it has three steps in a strict order:

1. **RED** — write a test that copies the exact complaint (`A-10` before `A-2`)
   and run it against the broken code. Watch it fail. Now you have proof the
   test can catch this bug.
2. **GREEN** — fix `shelf_order` so it reads the slot as a number. Run the test
   again. Watch it pass.
3. **Keep it forever** — never delete that test. A kept test that guards against
   an old bug coming back is called a **regression test**. It stands at the door
   so the same mistake can never walk back in.

## Starter

Two files, side by side in the same folder. First, the buggy module you are
handed. Do not change it yet — you need to watch it fail first.

```python
"""shelving.py — order shelf codes like "A-2" for the front-desk list."""


def shelf_order(codes: list[str]) -> list[str]:
    """Sort shelf codes. BUG: a plain string sort puts "A-10" before "A-2"."""
    return sorted(codes)
```

Then the test file you are here to write. The regression test — the one that
copies the complaint — goes first, because it is the reason this problem exists.

```python
"""test_shelving.py — tests for the front-desk shelf ordering."""

import pytest

from shelving import shelf_order


def test_regression_a10_sorts_after_a2() -> None:
    """The exact bug from the report: A-10 must come after A-2, not before."""
    # TODO: assert shelf_order(["A-10", "A-2"]) == ["A-2", "A-10"]


def test_natural_order_within_an_aisle() -> None:
    """A whole aisle sorts by slot number, not by word."""
    # TODO: assert shelf_order(["A-2", "A-10", "A-1"]) == ["A-1", "A-2", "A-10"]


def test_sorts_across_aisles_then_slots() -> None:
    """Aisle letter first, then slot number."""
    # TODO: assert shelf_order(["B-1", "A-2", "A-10"]) == ["A-2", "A-10", "B-1"]


def test_empty_list_stays_empty() -> None:
    """No codes in, an empty list out — not None."""
    # TODO: assert shelf_order([]) == []


def test_malformed_code_is_rejected() -> None:
    """A code with no numeric slot is bad data, and says so."""
    # TODO: use pytest.raises(ValueError, match="malformed shelf code")
    #       around shelf_order(["A-2", "A-top"])
```

## Requirements

1. Write `test_regression_a10_sorts_after_a2` **first**, and run it against the
   buggy `shelving.py` before you change a single line. It must fail. Read the
   failure — that is your proof the test works.
2. Only after you have seen the red, fix `shelf_order` with a natural-sort key
   that parses the slot part as an `int`.
3. Keep all five tests in `test_shelving.py`. None of them gets deleted, ever.
4. `test_empty_list_stays_empty` asserts `== []`, not just "falsy". An empty
   list and `None` are both falsy, and only one of them is correct.
5. A malformed code — one with no numeric slot, like `"A-top"` — raises
   `ValueError`, and the test uses
   `pytest.raises(ValueError, match="malformed shelf code")`.
6. After the fix, all five tests pass together with `pytest -v`.

## Constraints

- **Reproduce the bug BEFORE you fix it.** A test you never watched fail on the
  broken code is a test you cannot trust to catch the bug again. Maybe it passes
  because it is right; maybe it passes because it is asleep. You only know once
  you have seen it wake up and go red.
- **Name the regression test after what it guards:**
  `test_regression_a10_sorts_after_a2`. A year from now someone will read that
  name and know instantly *why the test exists* — so they will not delete it as
  "redundant" and let the old bug back in.
- **Fix the sort KEY, do not hand-roll a sort.** `sorted(...)` already knows how
  to put things in order. You only need to tell it *how to read each code*. A
  home-made sort is more code, more corners, and more places for a new bug to
  hide.
- **A code with no numeric slot is bad data — raise, do not guess.** If the slot
  is not a number, there is no right place to put it. Silently sorting it
  somewhere hides the real problem, which is that a broken code got into the
  list at all. Loud and early beats quiet and wrong.
- **Keep the fixed test forever — that is the entire point of "regression".**
  The word means "sliding back". The test is the guardrail that stops the code
  from sliding back into the same hole it just climbed out of.

## Expected output

The shipped answer prints the broken result right beside the fixed one, so you
can see the bug and the cure together, and then it runs the whole regression
suite and reports it:

```text
$ python problem-06-shelf-order-regression-solution.py
Input: ['A-10', 'A-2', 'A-1', 'B-1']
  broken (plain string sort): ['A-1', 'A-10', 'A-2', 'B-1']
  fixed  (natural-key sort) : ['A-1', 'A-2', 'A-10', 'B-1']
  the bug was A-10 landing before A-2; the fix reads the slot as a number.

The regression suite, run the way pytest runs it:
  PASS  test_regression_a10_sorts_after_a2
  PASS  test_natural_order_within_an_aisle
  PASS  test_sorts_across_aisles_then_slots
  PASS  test_empty_list_stays_empty
  PASS  test_malformed_code_is_rejected

5 passed, 0 failed
```

When you do this for real you will not see that tidy summary. You will see
`pytest`'s own output — red on the first run against the buggy code, green after
the fix.

## Steps

1. Save the buggy `shelving.py` and your new `test_shelving.py` side by side in
   your homework folder.
2. Run `pytest -k regression` and **watch it fail**. Read the line
   `assert ['A-10', 'A-2'] == ['A-2', 'A-10']` — pytest is showing you both
   sides, the wrong order and the right one, with no message from you. That red
   is the deliverable.
3. Write a helper `_natural_key(code)` that splits `"A-10"` into `("A", 10)` —
   the aisle letter, then the slot read as an `int`.
4. Change `shelf_order` to `return sorted(codes, key=_natural_key)`. You are not
   writing a sort; you are handing `sorted` a better pair of glasses.
5. Rerun `pytest -k regression`. It is green now. Then run the whole file with
   `pytest -v` and confirm all five pass.
6. Add the guard: if a code has no dash or the slot is not all digits, raise
   `ValueError("malformed shelf code: ...")`. Add and run
   `test_malformed_code_is_rejected` to prove the guard fires.

## The Solution

```python
"""problem-06-shelf-order-regression-solution.py — reproduce a bug, then fix it.

A bug report says shelf ``A-10`` is listed before ``A-2``. The discipline is:
write a test that *reproduces* the report and fails on the broken code (RED),
then fix the code so the test passes (GREEN), and keep that test forever so the
bug can never sneak back. That kept test is a *regression test*.

This file ships the fixed ``shelf_order`` plus the regression suite, and its
``main()`` shows the broken behaviour beside the fixed one before running the
suite. One file, driven by pytest, printing a plain, same-every-time report.

Run it with::

    python problem-06-shelf-order-regression-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# shelving.py — the FIXED module: a natural sort key, not a plain string sort
# --------------------------------------------------------------------------- #


def shelf_order(codes: list[str]) -> list[str]:
    """Sort shelf codes like ``"A-2"`` in natural order (``A-2`` before ``A-10``).

    A plain string sort puts ``"A-10"`` before ``"A-2"``, because ``"1"`` sorts
    before ``"2"`` character by character. The fix is a key that reads the slot
    as a number.
    """
    return sorted(codes, key=_natural_key)


def _natural_key(code: str) -> tuple[str, int]:
    """Split ``"A-10"`` into ``("A", 10)`` so the slot sorts numerically."""
    aisle, dash, slot = code.partition("-")
    if not dash or not slot.isdigit():
        raise ValueError(f"malformed shelf code: {code!r}")
    return aisle, int(slot)


def _broken_shelf_order(codes: list[str]) -> list[str]:
    """The original, buggy version — a plain string sort. Kept only for the demo."""
    return sorted(codes)


# --------------------------------------------------------------------------- #
# test_shelving.py — the regression test plus the rest of the contract
# --------------------------------------------------------------------------- #


def test_regression_a10_sorts_after_a2() -> None:
    """The exact bug from the report: A-10 must come after A-2, not before."""
    assert shelf_order(["A-10", "A-2"]) == ["A-2", "A-10"]


def test_natural_order_within_an_aisle() -> None:
    """A whole aisle sorts by slot number, not by string."""
    assert shelf_order(["A-2", "A-10", "A-1"]) == ["A-1", "A-2", "A-10"]


def test_sorts_across_aisles_then_slots() -> None:
    """Aisle letter first, then slot number."""
    assert shelf_order(["B-1", "A-2", "A-10"]) == ["A-2", "A-10", "B-1"]


def test_empty_list_stays_empty() -> None:
    """No codes in, an empty list out — not None."""
    assert shelf_order([]) == []


def test_malformed_code_is_rejected() -> None:
    """A code with no numeric slot is bad data, and says so."""
    with pytest.raises(ValueError, match="malformed shelf code"):
        shelf_order(["A-2", "A-top"])


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
    """Show the bug beside the fix, then run the regression suite."""
    codes = ["A-10", "A-2", "A-1", "B-1"]
    print(f"Input: {codes}")
    print(f"  broken (plain string sort): {_broken_shelf_order(codes)}")
    print(f"  fixed  (natural-key sort) : {shelf_order(codes)}")
    print("  the bug was A-10 landing before A-2; the fix reads the slot as a number.")

    print()
    print("The regression suite, run the way pytest runs it:")
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

**The regression test is the real deliverable, not the fix.** Anyone can change
`sorted(codes)` into something else. The thing that has *value* is the proof that
your change fixes the reported bug and keeps it fixed. That proof only exists if
you watched `test_regression_a10_sorts_after_a2` fail on the buggy code first. A
green test that has never been red is a promise nobody has checked.

**The fix is a sort key, not a hand-rolled sort.** `sorted(codes, key=_natural_key)`
keeps Python's fast, correct sorting and only changes *what each code looks like*
while it is being compared. The key turns `"A-2"` into `("A", 2)` and `"A-10"`
into `("A", 10)`, and now `2` really is less than `10` because they are numbers,
so `A-2` lands before `A-10`. You wrote no loops and no swaps — you just taught
`sorted` how to read a shelf code.

**`code.partition("-")` splits once, and the guard catches bad data.**
`partition` cuts the string at the *first* dash and hands back three pieces: the
part before, the dash itself, and everything after. If there is no dash, or the
part after is not all digits, the code is broken — there is no slot number to
sort by — so `_natural_key` raises `ValueError` instead of quietly shoving it
somewhere. Bad data stops at the door; it does not get sorted into the wrong
bay.

**The tuple key `(aisle, int(slot))` is the shelf order, spelled out.** Python
compares tuples piece by piece: it looks at the aisle letter first, and only if
two codes share the same aisle does it look at the slot number. That is exactly
how a person walks the shelves — find aisle `A`, then count up the bays `1, 2,
10`. Letter first, number second, and the tuple says both in one small object.

**Naming it `test_regression_...` is how it survives.** Tests get deleted when a
future reader cannot tell why they are there. A vague name invites a cleanup
that quietly removes the guardrail. `test_regression_a10_sorts_after_a2` tells
that reader, in the name alone, "I exist because `A-10` once jumped in front of
`A-2`, and I am here so it never does again." Nobody deletes a guardrail once
they can see the cliff.

## Download and run

Download
[problem-06-shelf-order-regression-solution.py](./problem-06-shelf-order-regression-solution.py)
and run it:

```bash
python problem-06-shelf-order-regression-solution.py
```

It shows the broken result beside the fixed one, then runs the regression suite
and prints a plain report. It needs `pytest` installed and nothing else, and it
exits on its own.

Your own work is the two separate files — the fixed `shelving.py` and your
`test_shelving.py` — which you run with `pytest -v`, not `python`. The
`-solution` in the filename keeps the download from colliding with your own
`shelving.py`.

## Common bugs to catch

- **The regression test passes on the very first run, before you fixed
  anything.** That is not good news — it means your evidence is missing. Either
  you wrote the test against already-fixed code, or the assertion is backwards
  (`["A-10", "A-2"]` on the right side instead of `["A-2", "A-10"]`). Revert to
  the buggy `shelving.py` and make sure you see the red. No red, no proof.
- **`ValueError: invalid literal for int() with base 10`.** A slot that is not
  digits reached `int()`. That is the crash the guard is supposed to prevent —
  check the slot part with `.isdigit()` *before* you call `int()`, and raise your
  own clear `ValueError` instead.
- **`AttributeError`, or a code splitting into too many pieces.** You used
  `.split("-")`, and a code with two dashes handed you three parts and a
  surprise. `partition("-")` splits at the *first* dash only and always returns
  exactly three pieces, which is why the solution uses it.
- **The malformed test does not raise.** Your guard is checking the wrong thing
  — maybe it only checks that a dash exists, not that the slot is all digits.
  `"A-top"` has a dash. Check that the slot part passes `.isdigit()`.
- **The across-aisle order comes out wrong.** You keyed on the slot number only
  and dropped the aisle letter, so `B-1` and `A-2` got compared by `1` versus
  `2`. Key on the whole tuple `(aisle, int(slot))` so the letter is compared
  first.

## Under the hood

<details>
<summary>Under the hood — why a plain string sort puts "A-10" before "A-2"</summary>

A string sort in Python is a letter-by-letter race. It lines up two codes and
compares the first character of each, then the second, then the third, and it
stops the instant it finds a difference. For `"A-10"` and `"A-2"` it checks
`'A'` against `'A'` (a tie), then `'-'` against `'-'` (a tie), then `'1'`
against `'2'`. There it stops: `'1'` comes before `'2'` in the character order,
so `"A-10"` is declared "smaller" and goes first. The `'0'` hiding in `"A-10"`
is never even looked at — the race was already over.

You can see it for yourself:

```python
>>> sorted(["A-10", "A-2"])
['A-10', 'A-2']
```

That is not a Python bug. It is doing exactly what a word sort does, which is
compare characters, not read numbers. The trouble is that `"1"` the character
and `1` the number sort differently, and shelf codes want the number.

This exact problem has a name — **natural sort** — and you have seen it
everywhere. It is why a file manager can show `img2` before `img10` only if
someone taught it to read the digits as a number; the naive version shows
`img10` before `img2` for the same reason our shelves went wrong. Our
`_natural_key` is just the "read the digits as a number" fix, applied to shelf
codes.

</details>

## Acceptance checklist

- [ ] You watched `test_regression_a10_sorts_after_a2` **fail** on the buggy
      `shelving.py` before you changed anything.
- [ ] `shelf_order` is fixed with a natural-sort key that parses the slot as an
      `int` — not a hand-rolled sort.
- [ ] All five tests are still in the file, and `pytest -v` shows all five pass.
- [ ] `test_empty_list_stays_empty` asserts `== []`, not just falsy.
- [ ] A malformed code raises `ValueError`, and the test checks the message with
      `match="malformed shelf code"`.
- [ ] The regression test's name says what it guards, so a future reader knows
      why it must not be deleted.

## Stretch

- Support three-part codes like `"A-2-3"` (aisle, bay, then shelf-within-bay).
  Extend `_natural_key` to return a longer tuple, and add a test that proves
  `A-2-3` sorts before `A-2-10`.
- Build a list of 50 shuffled codes, run `shelf_order` on it, and assert only
  the first and last elements. It is a cheap way to check the whole ordering
  holds at scale without listing all 50 by hand.
- Add a `hypothesis`-style property test: for any list of valid codes,
  `shelf_order` never changes the *multiset* of codes — sorting reorders, it
  never adds, drops, or duplicates. Assert `sorted(result) == sorted(codes)`.

---

Back to the [homework index](./README.md), or on to the
[mini-project](../mini-project/README.md).
