"""Exercise 03 - Recursion intro.

Goals:
    * Write the same function two ways: iteratively (with a loop) and
      recursively (the function calls itself).
    * Notice that both produce the same answer, and start to feel which
      style suits which problem.
    * See why deep recursion in Python can blow up the stack.

The function:
    factorial(n) = n * (n-1) * (n-2) * ... * 1
    factorial(0) = 1
    factorial(n) for negative n is undefined; raise ValueError.

How to run:
    $ python exercise-03-recursion-intro.py
"""

import sys
import time


# ---------------------------------------------------------------------------
# TASK 1 - iterative factorial
#
# Implement factorial using a `for` loop. Must:
#   - Raise ValueError when n < 0.
#   - Return 1 when n == 0.
# ---------------------------------------------------------------------------
def factorial_iterative(n: int) -> int:
    """Return n! using a loop. Raises ValueError if n < 0."""
    if n < 0:
        raise ValueError("n must be non-negative")
    # TODO: implement with a `for` loop. Hint: start with `result = 1`.
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# ---------------------------------------------------------------------------
# TASK 2 - recursive factorial
#
# Implement factorial recursively. Must:
#   - Raise ValueError when n < 0.
#   - Return 1 when n == 0 (the base case).
#   - Otherwise return n * factorial_recursive(n - 1).
# ---------------------------------------------------------------------------
def factorial_recursive(n: int) -> int:
    """Return n! by calling itself. Raises ValueError if n < 0."""
    if n < 0:
        raise ValueError("n must be non-negative")
    # TODO: implement with recursion.
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


# ---------------------------------------------------------------------------
# Comparison demo.
#
# This is here so you can see both functions produce the same numbers
# AND so you can see a real-world reason iterative is often preferred:
# Python caps the recursion depth around 1000 by default. Try
# factorial_recursive(2000) and it will blow up.
# ---------------------------------------------------------------------------
def _compare() -> None:
    """Show a table comparing iterative and recursive versions."""
    print(f"{'n':>4} | {'iterative':>20} | {'recursive':>20}")
    print("-" * 52)
    for n in [0, 1, 2, 3, 5, 10, 15, 20]:
        a = factorial_iterative(n)
        b = factorial_recursive(n)
        print(f"{n:>4} | {a:>20} | {b:>20}")

    print()
    print("Timing factorial(500):")
    t0 = time.perf_counter()
    factorial_iterative(500)
    t1 = time.perf_counter()
    factorial_recursive(500)
    t2 = time.perf_counter()
    print(f"  iterative: {(t1 - t0) * 1000:.3f} ms")
    print(f"  recursive: {(t2 - t1) * 1000:.3f} ms")

    print()
    print(f"Current recursion limit: {sys.getrecursionlimit()}")
    print("Recursion would fail well below factorial_iterative(10_000).")


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
def _run_tests() -> None:
    failures: list[str] = []

    cases = [(0, 1), (1, 1), (2, 2), (3, 6), (5, 120), (10, 3_628_800)]
    for n, expected in cases:
        if factorial_iterative(n) != expected:
            failures.append(f"factorial_iterative({n}) != {expected}")
        if factorial_recursive(n) != expected:
            failures.append(f"factorial_recursive({n}) != {expected}")

    for f in (factorial_iterative, factorial_recursive):
        try:
            f(-1)
        except ValueError:
            pass
        else:
            failures.append(f"{f.__name__}(-1) should raise ValueError")

    if failures:
        print("FAILED:")
        for msg in failures:
            print(f"  - {msg}")
        raise SystemExit(1)

    print("All tests passed.\n")
    _compare()


if __name__ == "__main__":
    _run_tests()
