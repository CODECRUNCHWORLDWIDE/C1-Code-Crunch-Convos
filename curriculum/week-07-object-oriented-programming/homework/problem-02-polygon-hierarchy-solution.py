"""problem-02-polygon-hierarchy-solution.py — a Polygon hierarchy behind an abstract base class.

The `-solution` in the name keeps this file from colliding with the
`polygons.py` you write yourself. Run it with::

    python problem-02-polygon-hierarchy-solution.py

Design note: the brief asks for abstract `area()` / `perimeter()` on `Polygon`
AND a `@property area` on `Rectangle`. Those two only coexist if the whole
hierarchy agrees, so `area` and `perimeter` are abstract *properties* here and
every subclass exposes them as properties. Mixing the two styles is the bug
this file is written to avoid: if `Rectangle.area` is a property while the
others are methods, `sum(p.area() for p in shapes)` dies with
`TypeError: 'float' object is not callable` on the rectangle only (or
`'int'`, depending on the numbers you fed it).
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod


class Polygon(ABC):
    """The contract: every polygon can report an area and a perimeter."""

    @property
    @abstractmethod
    def area(self) -> float:
        """Enclosed area in square units."""

    @property
    @abstractmethod
    def perimeter(self) -> float:
        """Total edge length in units."""

    def describe(self) -> str:
        """Concrete method on an abstract class — subclasses inherit it free."""
        return (
            f"{type(self).__name__}: area={self.area:.4f}, "
            f"perimeter={self.perimeter:.4f}"
        )

    def __repr__(self) -> str:
        """Developer form, naming the actual subclass."""
        return f"{type(self).__name__}(area={self.area:.4f})"


class Triangle(Polygon):
    """Three sides that actually close into a triangle."""

    def __init__(self, a: float, b: float, c: float) -> None:
        """Store three sides, refusing any trio that cannot close."""
        sides = (a, b, c)
        if any(side <= 0 for side in sides):
            raise ValueError(f"every side must be positive, got {sides!r}")
        # Triangle inequality: the two shorter sides must beat the longest.
        # Checking all three pairs is what the brief asks for and costs nothing.
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError(
                f"sides {sides!r} violate the triangle inequality "
                f"(the sum of any two must exceed the third)"
            )
        self.a, self.b, self.c = float(a), float(b), float(c)

    @property
    def perimeter(self) -> float:
        """The three sides added up."""
        return self.a + self.b + self.c

    @property
    def area(self) -> float:
        """Heron's formula: sqrt(s(s-a)(s-b)(s-c)) with s the semi-perimeter."""
        s = self.perimeter / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def __repr__(self) -> str:
        """Developer form, showing the three sides."""
        return f"Triangle(a={self.a!r}, b={self.b!r}, c={self.c!r})"


class Rectangle(Polygon):
    """Width and height; area is the property the brief calls for."""

    def __init__(self, width: float, height: float) -> None:
        """Store two positive sides."""
        if width <= 0 or height <= 0:
            raise ValueError(
                f"width and height must be positive, got {width!r}x{height!r}"
            )
        self.width = float(width)
        self.height = float(height)

    @property
    def area(self) -> float:
        """Width times height."""
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        """Twice the sum of the two sides."""
        return 2 * (self.width + self.height)

    def __repr__(self) -> str:
        """Developer form, showing both sides."""
        return f"Rectangle(width={self.width!r}, height={self.height!r})"


class RegularPolygon(Polygon):
    """n equal sides. Closed-form perimeter and area, no trigonometry per side."""

    def __init__(self, n_sides: int, side_length: float) -> None:
        """Store a side count of at least three and a positive side length."""
        if n_sides < 3:
            raise ValueError(f"a polygon needs at least 3 sides, got {n_sides!r}")
        if side_length <= 0:
            raise ValueError(f"side_length must be positive, got {side_length!r}")
        self.n_sides = n_sides
        self.side_length = float(side_length)

    @property
    def perimeter(self) -> float:
        """Side count times side length."""
        return self.n_sides * self.side_length

    @property
    def area(self) -> float:
        """A = n * s^2 / (4 * tan(pi/n)) — the n triangles from the centre."""
        return (self.n_sides * self.side_length ** 2) / (
            4 * math.tan(math.pi / self.n_sides)
        )

    def __repr__(self) -> str:
        """Developer form, showing the side count and length."""
        return (
            f"RegularPolygon(n_sides={self.n_sides!r}, "
            f"side_length={self.side_length!r})"
        )


def main() -> None:
    """Total a mixed bag of polygons, then show the contract refusing."""
    shapes: list[Polygon] = [
        Triangle(3, 4, 5),
        Rectangle(4, 2.5),
        RegularPolygon(6, 2),
        RegularPolygon(4, 3),          # a square, the long way round
    ]

    for shape in shapes:
        print(shape.describe())

    # The polymorphic line: one expression, four different area formulas.
    total = sum(shape.area for shape in shapes)
    print(f"total area: {total:.4f}")
    print(f"total perimeter: {sum(s.perimeter for s in shapes):.4f}")
    print("largest:", max(shapes, key=lambda s: s.area))

    # --- the contract is enforced ---------------------------------------
    try:
        Polygon()          # type: ignore[abstract]
    except TypeError as exc:
        print("TypeError:", exc)

    class Pentagon(Polygon):
        """Deliberately incomplete: perimeter is missing."""

        @property
        def area(self) -> float:
            """A stand-in area so only `perimeter` is missing."""
            return 1.0

    try:
        Pentagon()         # type: ignore[abstract]
    except TypeError as exc:
        print("TypeError:", exc)

    for bad in [lambda: Triangle(1, 2, 10), lambda: Rectangle(0, 5),
                lambda: RegularPolygon(2, 1)]:
        try:
            bad()
        except ValueError as exc:
            print("ValueError:", exc)


if __name__ == "__main__":
    main()
