"""Exercise 05 - Import and use standard library modules.

Goals:
    * Practice all three import forms: `import x`, `from x import y`,
      and `import x as alias`.
    * Use functions from `math`, `random`, and `statistics`.
    * Read the standard library docs.

How to run:
    $ python exercise-05-import-and-use.py
"""

# TODO: complete the imports below.
#   - Import the whole `math` module under the alias `m`.
#   - Import only `mean` and `median` from `statistics`.
#   - Import the whole `random` module (no alias).
import math as m
from statistics import mean, median
import random


# ---------------------------------------------------------------------------
# TASK 1
#
# Write `circle_circumference(radius)` that returns the circumference of
# a circle. Use `m.pi`.
# ---------------------------------------------------------------------------
def circle_circumference(radius: float) -> float:
    """Return the circumference of a circle with `radius`."""
    return 2 * m.pi * radius


# ---------------------------------------------------------------------------
# TASK 2
#
# Write `distance(x1, y1, x2, y2)` that returns the Euclidean distance
# between (x1, y1) and (x2, y2). Use `m.sqrt`.
# ---------------------------------------------------------------------------
def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the Euclidean distance between (x1, y1) and (x2, y2)."""
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# ---------------------------------------------------------------------------
# TASK 3
#
# Write `roll_dice(n=2, sides=6)` that returns a list of `n` rolls of
# a `sides`-sided die. Each roll should be an int in [1, sides].
#
# Note: because the result is random, the self-test below seeds the
# generator first so we get a predictable answer.
# ---------------------------------------------------------------------------
def roll_dice(n: int = 2, sides: int = 6) -> list[int]:
    """Return a list of `n` dice rolls (1..sides)."""
    return [random.randint(1, sides) for _ in range(n)]


# ---------------------------------------------------------------------------
# TASK 4
#
# Write `grade_summary(scores)` that returns a dict with keys
# "mean", "median", and "max" for the given list of numeric scores.
# Use `mean` and `median` from `statistics`. Use the built-in `max`.
#
# If the list is empty, raise ValueError with a helpful message.
# ---------------------------------------------------------------------------
def grade_summary(scores: list[float]) -> dict[str, float]:
    """Return mean/median/max of `scores`."""
    if not scores:
        raise ValueError("scores must not be empty")
    return {
        "mean": float(mean(scores)),
        "median": float(median(scores)),
        "max": float(max(scores)),
    }


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
def _run_tests() -> None:
    failures: list[str] = []

    # Task 1
    if abs(circle_circumference(0) - 0) > 1e-9:
        failures.append("circle_circumference(0) should be 0")
    if abs(circle_circumference(1) - 2 * m.pi) > 1e-9:
        failures.append("circle_circumference(1) should be 2*pi")

    # Task 2
    if abs(distance(0, 0, 3, 4) - 5.0) > 1e-9:
        failures.append("distance((0,0),(3,4)) should be 5")
    if abs(distance(1, 1, 1, 1)) > 1e-9:
        failures.append("distance to self should be 0")

    # Task 3
    random.seed(42)
    rolls = roll_dice(5, sides=6)
    if len(rolls) != 5:
        failures.append("roll_dice(5) should return 5 values")
    if not all(1 <= r <= 6 for r in rolls):
        failures.append("each roll must be in 1..6")

    # Task 4
    summary = grade_summary([10, 20, 30, 40])
    if summary["mean"] != 25.0:
        failures.append("mean of 10,20,30,40 should be 25.0")
    if summary["median"] != 25.0:
        failures.append("median of 10,20,30,40 should be 25.0")
    if summary["max"] != 40.0:
        failures.append("max should be 40.0")

    try:
        grade_summary([])
    except ValueError:
        pass
    else:
        failures.append("grade_summary([]) should raise ValueError")

    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)

    print("All tests passed. The standard library is your friend.")


if __name__ == "__main__":
    _run_tests()
