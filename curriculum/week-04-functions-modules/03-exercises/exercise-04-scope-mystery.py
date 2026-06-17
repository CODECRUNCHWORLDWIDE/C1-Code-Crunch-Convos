"""Exercise 04 - Scope mystery.

This file contains FOUR buggy functions, each broken by a scope issue
(LEGB, global, nonlocal, or the mutable-default trap).

Your job:
    1. Run the file. See which tests fail and read the error messages.
    2. Fix each function so that the tests at the bottom pass.
    3. Do NOT change the tests themselves.
    4. Each fix should be small. If you are rewriting a function from
       scratch, you are over-thinking it.

Topics covered:
    - UnboundLocalError caused by assigning to a global.
    - The mutable default argument trap.
    - Confusing reads vs. writes inside nested functions (nonlocal).
    - Accidentally shadowing a built-in.

How to run:
    $ python exercise-04-scope-mystery.py
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# BUG 1
#
# `count_up` is supposed to increment the module-level `counter` and
# return its new value. Instead it raises UnboundLocalError.
#
# Hint: read Lecture Note 2, section on `global`.
# ---------------------------------------------------------------------------
counter = 0


def count_up() -> int:
    """Increment the global counter and return the new value."""
    # FIX: tell Python that `counter` refers to the global name.
    global counter
    counter = counter + 1
    return counter


# ---------------------------------------------------------------------------
# BUG 2
#
# `append_score` should add a score to a player's list of scores and
# return the updated list. It currently SHARES the same default list
# across every caller -- the mutable-default trap.
#
# Hint: use `None` as the default and create a fresh list inside.
# ---------------------------------------------------------------------------
def append_score(score: int, scores: list[int] | None = None) -> list[int]:
    """Append `score` to `scores` (or to a new list) and return it."""
    # FIX: replace the mutable default with None and create a list inside.
    if scores is None:
        scores = []
    scores.append(score)
    return scores


# ---------------------------------------------------------------------------
# BUG 3
#
# `make_adder(step)` should return a function that, when called, adds
# `step` to its own running total and returns the new total. Instead it
# raises UnboundLocalError when `increment` tries to write to `total`.
#
# Hint: `total` lives in the enclosing scope, not the local scope.
# ---------------------------------------------------------------------------
def make_adder(step: int):
    """Return a closure that accumulates a running total in steps of `step`."""
    total = 0

    def increment() -> int:
        # FIX: declare `total` as nonlocal so the assignment updates the
        # enclosing scope's name instead of creating a new local.
        nonlocal total
        total += step
        return total

    return increment


# ---------------------------------------------------------------------------
# BUG 4
#
# `sum_of_squares(values)` shadows the built-in `sum` by using `sum` as a
# loop variable. The accumulated total is wrong (it ends up as just the
# last squared value).
#
# Hint: rename the variable. Never name a local `sum`, `list`, `dict`,
# `type`, or `id`.
# ---------------------------------------------------------------------------
def sum_of_squares(values: list[int]) -> int:
    """Return the sum of the squares of `values`."""
    # FIX: rename `sum` to `total` (or anything except a built-in name).
    total = 0
    for v in values:
        total = total + v * v
    return total


# ---------------------------------------------------------------------------
# Self-tests. Do not modify.
# ---------------------------------------------------------------------------
def _run_tests() -> None:
    failures: list[str] = []

    # Bug 1
    global counter
    counter = 0
    if count_up() != 1:
        failures.append("count_up() first call should return 1")
    if count_up() != 2:
        failures.append("count_up() second call should return 2")
    if counter != 2:
        failures.append("counter should be 2 after two count_up() calls")

    # Bug 2 - each fresh call should NOT see the previous call's list.
    a = append_score(10)
    b = append_score(20)
    if a != [10]:
        failures.append(f"append_score(10) should be [10], got {a}")
    if b != [20]:
        failures.append(f"append_score(20) should be [20], got {b}")
    explicit = append_score(99, [1, 2])
    if explicit != [1, 2, 99]:
        failures.append("append_score(99, [1,2]) should be [1,2,99]")

    # Bug 3
    inc = make_adder(5)
    if inc() != 5:
        failures.append("make_adder(5)(); first call should return 5")
    if inc() != 10:
        failures.append("second call should return 10")
    if inc() != 15:
        failures.append("third call should return 15")

    # Bug 4
    if sum_of_squares([1, 2, 3]) != 14:
        failures.append("sum_of_squares([1,2,3]) should be 1+4+9 = 14")
    if sum_of_squares([]) != 0:
        failures.append("sum_of_squares([]) should be 0")

    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print("All tests passed. You have a feel for scope now.")


if __name__ == "__main__":
    _run_tests()
