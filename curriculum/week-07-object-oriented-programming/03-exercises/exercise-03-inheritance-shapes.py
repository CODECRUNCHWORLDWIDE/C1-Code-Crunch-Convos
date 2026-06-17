"""Exercise 03 — Inheritance and polymorphism with shapes.

Goal
----
Build a small `Shape` hierarchy.

* `Shape` is the parent class.
  - `__init__(self, name: str)` stores ``self.name``.
  - `area(self) -> float` raises ``NotImplementedError``.
    (We will see `abc` later; this is the manual version.)

* `Circle(Shape)` — extra attribute ``radius``. Override ``area()`` to
  return ``math.pi * radius ** 2``.

* `Square(Shape)` — extra attribute ``side``. Override ``area()`` to return
  ``side ** 2``.

Then in `main()`, demonstrate **polymorphism** by putting one of each in a
list and looping over it, printing each shape's name and area.

Expected output (the area values will not be perfectly round)
-------------------------------------------------------------
    Big Circle has area 78.54
    Small Square has area 9.00

Run with:

    python exercise-03-inheritance-shapes.py
"""

from __future__ import annotations

import math


class Shape:
    """Base class for 2D shapes."""

    def __init__(self, name: str) -> None:
        self.name = name

    def area(self) -> float:
        # TODO: raise NotImplementedError -- subclasses must override.
        raise NotImplementedError("subclasses must implement area()")


class Circle(Shape):
    def __init__(self, name: str, radius: float) -> None:
        # TODO: call super().__init__(name) and store the radius.
        super().__init__(name)
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2


class Square(Shape):
    def __init__(self, name: str, side: float) -> None:
        super().__init__(name)
        self.side = side

    def area(self) -> float:
        return self.side ** 2


def main() -> None:
    shapes: list[Shape] = [
        Circle(name="Big Circle", radius=5),
        Square(name="Small Square", side=3),
    ]

    # Polymorphism: same call site, different concrete behavior.
    for shape in shapes:
        print(f"{shape.name} has area {shape.area():.2f}")


if __name__ == "__main__":
    main()
