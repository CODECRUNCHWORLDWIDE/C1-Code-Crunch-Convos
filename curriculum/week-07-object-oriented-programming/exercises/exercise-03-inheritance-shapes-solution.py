"""exercise-03-inheritance-shapes-solution.py — one loop, three kinds of panel.

Estimates material for a mixed sign-shop job. The `-solution` in the name keeps
this file from colliding with the `exercise-03-inheritance-shapes.py` you write
yourself. Run it with::

    python exercise-03-inheritance-shapes-solution.py
"""

import math
from collections.abc import Iterable


class Shape:
    """Base class for anything with a label and an area."""

    def __init__(self, label: str) -> None:
        """Store the human-readable label used on the estimate."""
        self.label = label

    def area(self) -> float:
        """Area in square centimetres. Subclasses must override this."""
        raise NotImplementedError(
            "Shape is abstract; subclasses must implement area()"
        )

    def describe(self) -> str:
        """One estimate line, e.g. `Back panel: 1000.00 sq cm`.

        Defined once here. No subclass may override it.
        """
        return f"{self.label}: {self.area():.2f} sq cm"

    def __repr__(self) -> str:
        """Developer form, e.g. `Circle(label='Clock face')`."""
        return f"{type(self).__name__}(label={self.label!r})"


class Rectangle(Shape):
    """A rectangular panel."""

    def __init__(self, label: str, width: float, height: float) -> None:
        """Let Shape store the label, then keep the two sides."""
        super().__init__(label)
        self.width = width
        self.height = height

    def area(self) -> float:
        """Width times height."""
        return self.width * self.height


class Circle(Shape):
    """A circular panel."""

    def __init__(self, label: str, radius: float) -> None:
        """Let Shape store the label, then keep the radius."""
        super().__init__(label)
        self.radius = radius

    def area(self) -> float:
        """Pi times the radius squared."""
        return math.pi * self.radius ** 2


class RightTriangle(Shape):
    """A right-angled triangular offcut."""

    def __init__(self, label: str, base: float, height: float) -> None:
        """Let Shape store the label, then keep the base and height."""
        super().__init__(label)
        self.base = base
        self.height = height

    def area(self) -> float:
        """Half the base times the height."""
        return 0.5 * self.base * self.height


class Square(Rectangle):
    """A square panel — a rectangle whose two sides are the same length.

    Step 6 of the exercise: proof that a new shape costs one small class and
    no edit to `total_area`, `describe`, or the loop in `main`.
    """

    def __init__(self, label: str, side: float) -> None:
        """Hand the one side to Rectangle twice."""
        super().__init__(label, side, side)


def total_area(shapes: Iterable[Shape]) -> float:
    """Sum the areas of every shape given.

    Contains no isinstance checks and no type names. It works because
    every Shape answers area().
    """
    return sum(shape.area() for shape in shapes)


def main() -> None:
    """Estimate one mixed job, then show what the base class refuses."""
    panels: list[Shape] = [
        Rectangle("Back panel", 40.0, 25.0),
        Circle("Clock face", 12.0),
        RightTriangle("Corner gusset", 30.0, 18.0),
    ]

    for panel in panels:
        print(panel.describe())

    print(f"Total material: {total_area(panels):.2f} sq cm")
    print(panels)

    try:
        Shape("Blank template").area()
    except NotImplementedError as exc:
        print(f"Base class refused: {exc}")


if __name__ == "__main__":
    main()
