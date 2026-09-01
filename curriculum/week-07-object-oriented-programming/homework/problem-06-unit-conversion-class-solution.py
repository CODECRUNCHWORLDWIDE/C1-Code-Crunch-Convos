"""problem-06-unit-conversion-class-solution.py — a Length that stores metres and speaks five units.

The `-solution` in the name keeps this file from colliding with the `length.py`
you write yourself. Run it with::

    python problem-06-unit-conversion-class-solution.py

One number is stored. Every unit is a property pair over that one number, so
the five views can never disagree with each other.
"""

from __future__ import annotations

import math

# Exact conversion factors, by international agreement since 1959.
METERS_PER_KILOMETER = 1000.0
METERS_PER_MILE = 1609.344
METERS_PER_FOOT = 0.3048
METERS_PER_INCH = 0.0254


class Length:
    """A distance. Internally metres; externally whatever unit you asked for."""

    def __init__(self, meters: float = 0.0) -> None:
        """Store one distance, validated through the `meters` setter."""
        self.meters = float(meters)      # goes through the setter, so it validates

    # --- alternative constructors ----------------------------------------

    @classmethod
    def from_kilometers(cls, value: float) -> "Length":
        """Build a Length from kilometres."""
        return cls(meters=value * METERS_PER_KILOMETER)

    @classmethod
    def from_miles(cls, value: float) -> "Length":
        """Build a Length from miles."""
        return cls(meters=value * METERS_PER_MILE)

    @classmethod
    def from_feet(cls, value: float) -> "Length":
        """Build a Length from feet."""
        return cls(meters=value * METERS_PER_FOOT)

    @classmethod
    def from_inches(cls, value: float) -> "Length":
        """Build a Length from inches."""
        return cls(meters=value * METERS_PER_INCH)

    # --- the one real field ----------------------------------------------

    @property
    def meters(self) -> float:
        """The distance in metres — the only number actually stored."""
        return self._meters

    @meters.setter
    def meters(self, value: float) -> None:
        """Validate, then store. Every other setter routes through here."""
        value = float(value)
        if math.isnan(value):
            raise ValueError("length cannot be NaN")
        if value < 0:
            raise ValueError(f"length cannot be negative, got {value!r}")
        self._meters = value

    # --- the four derived views ------------------------------------------

    @property
    def kilometers(self) -> float:
        """The same distance in kilometres."""
        return self._meters / METERS_PER_KILOMETER

    @kilometers.setter
    def kilometers(self, value: float) -> None:
        """Set the distance from a kilometre figure."""
        self.meters = value * METERS_PER_KILOMETER      # reuse the validation

    @property
    def miles(self) -> float:
        """The same distance in miles."""
        return self._meters / METERS_PER_MILE

    @miles.setter
    def miles(self, value: float) -> None:
        """Set the distance from a mile figure."""
        self.meters = value * METERS_PER_MILE

    @property
    def feet(self) -> float:
        """The same distance in feet."""
        return self._meters / METERS_PER_FOOT

    @feet.setter
    def feet(self, value: float) -> None:
        """Set the distance from a foot figure."""
        self.meters = value * METERS_PER_FOOT

    @property
    def inches(self) -> float:
        """The same distance in inches."""
        return self._meters / METERS_PER_INCH

    @inches.setter
    def inches(self, value: float) -> None:
        """Set the distance from an inch figure."""
        self.meters = value * METERS_PER_INCH

    # --- arithmetic -------------------------------------------------------

    def __add__(self, other: object) -> "Length":
        """Two Lengths add. Anything else declines to NotImplemented."""
        if not isinstance(other, Length):
            # NotImplemented (not a raise) is the idiomatic move: Python then
            # tries other.__radd__ and, finding nothing, raises the TypeError
            # itself — with a better message than we could write.
            return NotImplemented
        return Length(meters=self._meters + other._meters)

    def __sub__(self, other: object) -> "Length":
        """Two Lengths subtract, as long as the result is not negative."""
        if not isinstance(other, Length):
            return NotImplemented
        return Length(meters=self._meters - other._meters)   # may raise on < 0

    def __mul__(self, factor: object) -> "Length":
        """A Length scales by a real number, but never by a bool."""
        if not isinstance(factor, (int, float)) or isinstance(factor, bool):
            return NotImplemented
        return Length(meters=self._meters * factor)

    __rmul__ = __mul__

    # --- comparison and hashing ------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Exact equality on the stored metres. See `is_close` for tolerance."""
        if not isinstance(other, Length):
            return NotImplemented
        return self._meters == other._meters

    def __lt__(self, other: object) -> bool:
        """Order by the stored metres."""
        if not isinstance(other, Length):
            return NotImplemented
        return self._meters < other._meters

    def __hash__(self) -> int:
        """Consistent with the exact `__eq__`, so Lengths work in sets."""
        return hash(self._meters)

    def is_close(self, other: "Length", rel_tol: float = 1e-9) -> bool:
        """Float-tolerant comparison. `==` is exact; unit round trips are not.

        `Length.from_miles(1).miles == 1.0` happens to be exact, but
        `Length.from_miles(0.1) + Length.from_miles(0.9)` lands on
        1609.3440000000003 m while `Length.from_miles(1)` is 1609.344 m — none
        of 0.1, 0.9 or 1609.344 is exactly representable in binary. Use this
        whenever the numbers came out of arithmetic rather than a literal.
        """
        return math.isclose(self._meters, other._meters, rel_tol=rel_tol)

    # --- display ----------------------------------------------------------

    def __repr__(self) -> str:
        """Developer form: always metres, always round-trippable."""
        return f"Length(meters={self._meters!r})"

    def __str__(self) -> str:
        """Reader form: picks km, m or inches by magnitude."""
        if self._meters >= METERS_PER_KILOMETER:
            return f"{self.kilometers:.3f} km"
        if self._meters >= 1:
            return f"{self._meters:.3f} m"
        return f"{self.inches:.2f} in"


def main() -> None:
    """Convert one distance five ways, then add, compare and break it."""
    d = Length(meters=1000)
    print(repr(d), "|", d)
    print("kilometers:", d.kilometers)     # 1.0
    print("miles:", d.miles)
    print("feet:", d.feet)
    print("inches:", d.inches)

    d.miles = 1.0
    print("after d.miles = 1.0 ->", repr(d))   # 1609.344 m
    print("round trip miles:", d.miles)

    d.feet = 5280
    print("5280 feet ->", repr(d), "=", d.miles, "miles")

    # --- addition ---------------------------------------------------------
    total = Length(meters=10) + Length(meters=5)
    print("10m + 5m =", repr(total))
    print("mixed units:", repr(Length(meters=100) + Length.from_feet(10)))
    print("scaled:", repr(3 * Length(meters=2.5)))

    try:
        Length(meters=10) + 5
    except TypeError as exc:
        print("TypeError:", exc)

    # --- equality ---------------------------------------------------------
    print("equal:", Length(meters=1609.344) == Length.from_miles(1))
    tenth = Length.from_miles(0.1) + Length.from_miles(0.9)
    print("float noise:", repr(tenth), "==", repr(Length.from_miles(1)),
          "->", tenth == Length.from_miles(1))
    print("is_close:", tenth.is_close(Length.from_miles(1)))
    print("sorted:", sorted([Length.from_miles(1), Length(meters=5),
                             Length.from_feet(100)]))
    print("hashable:", len({Length(meters=1), Length(meters=1.0)}))

    try:
        Length(meters=-1)
    except ValueError as exc:
        print("ValueError:", exc)
    try:
        Length(meters=1) - Length(meters=2)
    except ValueError as exc:
        print("ValueError:", exc)


if __name__ == "__main__":
    main()
