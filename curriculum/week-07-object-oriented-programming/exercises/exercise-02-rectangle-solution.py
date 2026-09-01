"""exercise-02-rectangle-solution.py — derived values that cannot go stale.

Quotes sign-shop panels by area. The `-solution` in the name keeps this file
from colliding with the `exercise-02-rectangle.py` you write yourself. Run it
with::

    python exercise-02-rectangle-solution.py
"""


def require_positive(label: str, value: float) -> float:
    """Return `value` if it is greater than zero, else raise ValueError.

    The message reads `width must be positive, got -5.0`.
    """
    if value <= 0:
        raise ValueError(f"{label} must be positive, got {value}")
    return value


class Rectangle:
    """A rectangular panel measured in centimetres."""

    def __init__(self, width: float, height: float) -> None:
        """Set width and height *through the properties* so both are checked."""
        self.width = width
        self.height = height

    @property
    def width(self) -> float:
        """The panel's width in centimetres."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Validate, then store the width."""
        self._width = require_positive("width", value)

    @property
    def height(self) -> float:
        """The panel's height in centimetres."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Validate, then store the height."""
        self._height = require_positive("height", value)

    @property
    def area(self) -> float:
        """Width times height, computed fresh on every access."""
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        """Twice the sum of the two sides."""
        return 2 * (self._width + self._height)

    @property
    def is_square(self) -> bool:
        """True when the two sides are equal."""
        return self._width == self._height

    def __repr__(self) -> str:
        """Developer form, e.g. `Rectangle(width=90.0, height=60.0)`."""
        return f"Rectangle(width={self._width!r}, height={self._height!r})"


def report(rect: Rectangle) -> None:
    """Print one panel and its three derived values."""
    print(repr(rect))
    print(f"  area      : {rect.area:.2f} sq cm")
    print(f"  perimeter : {rect.perimeter:.2f} cm")
    print(f"  square?   : {'yes' if rect.is_square else 'no'}")


def main() -> None:
    """Quote a poster, resize it, then try two illegal dimensions."""
    poster = Rectangle(90.0, 60.0)
    report(poster)

    poster.width = 60.0
    report(poster)

    for label, value in (("width", -5.0), ("height", 0)):
        try:
            setattr(poster, label, value)
        except ValueError as exc:
            print(f"Rejected: {exc}")


if __name__ == "__main__":
    main()
