"""Exercise 01 - Function basics.

Goals:
    * Define functions with `def`.
    * Add type hints to every parameter and to the return.
    * Write a one-line docstring per PEP 257.
    * Use a default parameter value safely.

How to run:
    $ python exercise-01-function-basics.py

The bottom of this file has self-tests. When the script prints
"All tests passed", you are done.
"""

from math import pi


# ---------------------------------------------------------------------------
# TASK 1
#
# Write `add(a, b)` that returns a + b.
#   - Both parameters are ints.
#   - Return value is an int.
#   - Add type hints and a one-line docstring.
# ---------------------------------------------------------------------------
def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    # TODO: replace the line below with the correct implementation.
    return a + b


# ---------------------------------------------------------------------------
# TASK 2
#
# Write `is_even(n)` that returns True if `n` is even, False otherwise.
#   - Parameter is an int.
#   - Return value is a bool.
#   - Hint: the modulo operator `%` returns the remainder.
# ---------------------------------------------------------------------------
def is_even(n: int) -> bool:
    """Return True if `n` is even, else False."""
    # TODO: replace the line below.
    return n % 2 == 0


# ---------------------------------------------------------------------------
# TASK 3
#
# Write `greet(name, greeting="Hello")` that returns "<greeting>, <name>!".
#   - `greeting` has a default value of "Hello".
#   - Both parameters are strings.
#   - Return value is a string.
# ---------------------------------------------------------------------------
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a friendly greeting string for `name`."""
    # TODO: build and return the greeting using an f-string.
    return f"{greeting}, {name}!"


# ---------------------------------------------------------------------------
# TASK 4
#
# Write `area_of_circle(r)` that returns the area of a circle with radius r.
#   - Use `math.pi` (already imported at the top as `pi`).
#   - Return a float.
#   - Raise `ValueError` if r is negative. The message can be whatever you
#     want, but a useful one is "radius must be non-negative".
# ---------------------------------------------------------------------------
def area_of_circle(r: float) -> float:
    """Return the area of a circle with radius `r`."""
    # TODO: validate r, then compute and return the area.
    if r < 0:
        raise ValueError("radius must be non-negative")
    return pi * r * r


# ---------------------------------------------------------------------------
# Self-tests. Do not edit unless you know why.
# ---------------------------------------------------------------------------
def _run_tests() -> None:
    """Run a small self-test suite and print results."""
    failures: list[str] = []

    # Task 1
    if add(2, 3) != 5:
        failures.append("add(2, 3) should be 5")
    if add(-1, 1) != 0:
        failures.append("add(-1, 1) should be 0")

    # Task 2
    if is_even(4) is not True:
        failures.append("is_even(4) should be True")
    if is_even(7) is not False:
        failures.append("is_even(7) should be False")
    if is_even(0) is not True:
        failures.append("is_even(0) should be True")

    # Task 3
    if greet("Amina") != "Hello, Amina!":
        failures.append('greet("Amina") should be "Hello, Amina!"')
    if greet("Diego", "Hola") != "Hola, Diego!":
        failures.append('greet("Diego", "Hola") should be "Hola, Diego!"')
    if greet("Yuki", greeting="Konnichiwa") != "Konnichiwa, Yuki!":
        failures.append('greet("Yuki", greeting="Konnichiwa") should work')

    # Task 4
    if abs(area_of_circle(0.0)) > 1e-9:
        failures.append("area_of_circle(0) should be 0")
    if abs(area_of_circle(1.0) - pi) > 1e-9:
        failures.append("area_of_circle(1) should be pi")
    if abs(area_of_circle(2.0) - 4 * pi) > 1e-9:
        failures.append("area_of_circle(2) should be 4*pi")

    try:
        area_of_circle(-1.0)
    except ValueError:
        pass  # expected
    else:
        failures.append("area_of_circle(-1) should raise ValueError")

    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print("All tests passed. Nice work.")


if __name__ == "__main__":
    _run_tests()
