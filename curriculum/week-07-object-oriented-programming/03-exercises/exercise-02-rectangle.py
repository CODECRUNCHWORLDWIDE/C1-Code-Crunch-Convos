"""Exercise 02 — Rectangle with @property.

Goal
----
Define a `Rectangle` class with:

* `__init__(self, width: float, height: float)`,
* a `perimeter()` method that returns ``2 * (width + height)``,
* an `area` *property* (no parentheses on access) that returns
  ``width * height``.

Validate in `__init__` that both dimensions are strictly positive; raise
``ValueError`` if not.

In `main()` build a 3x4 rectangle, print its perimeter and area, then try
to build a rectangle with a negative side inside a ``try`` / ``except`` and
print the error message.

Expected output
---------------
    perimeter = 14
    area = 12
    caught error: dimensions must be positive

Run with:

    python exercise-02-rectangle.py
"""

from __future__ import annotations


class Rectangle:
    """A simple rectangle with a computed `area` property."""

    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("dimensions must be positive")
        self.width = width
        self.height = height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    @property
    def area(self) -> float:
        # TODO: compute width * height. Accessed as `r.area`, no parentheses.
        return self.width * self.height


def main() -> None:
    r = Rectangle(3, 4)
    # `int()` keeps the output tidy when inputs are integers; remove if you
    # prefer to see e.g. 14.0.
    print(f"perimeter = {int(r.perimeter())}")
    print(f"area = {int(r.area)}")

    try:
        Rectangle(-1, 5)
    except ValueError as exc:
        print(f"caught error: {exc}")


if __name__ == "__main__":
    main()
