# Problem 6 — Unit-conversion class

> **Topic:** one stored number, five live views of it — property pairs, and operators that refuse politely
> **Lecture:** [03 — Dataclasses, Dunder Methods, and Friends](../lecture-notes/03-dataclasses-and-magic-methods.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** it is `@property` with the setter half finally added, and it forces the week's central design question at the smallest possible scale: which facts do you *store*, and which do you *derive*? Store one number and the object can never disagree with itself. Store five and one day two of them will quietly differ, with no error anywhere. It is also your first meeting with `NotImplemented` — the polite way an operator says "not my job" — which is how every numeric type in Python actually works.

## The Brief

Build a `Length` class that stores a distance internally in **metres** but
speaks four other units as if they were real attributes:

- `meters`, `kilometers`, `miles`, `feet`, `inches` — each one a `@property`.

Each property has a **setter** as well, so both directions work:

```python
d = Length(meters=1000)
print(d.kilometers)   # 1.0
d.miles = 1.0
print(d.meters)       # ~1609.344
```

Think of the object as one ruler with five scales printed on it. There is
only one length — the ruler's — and each scale is just a different way of
reading the same mark. Ask for `kilometers` and the getter divides; assign
to `miles` and the setter multiplies back into metres. Nothing is ever
stored except the metres, so the five readings cannot drift apart: they are
computed from the same fact every time you look.

Include `__repr__`, `__eq__`, and support addition:
`Length(meters=10) + Length(meters=5)` must return a **new** `Length` of
15 m. `Length + 5` must raise `TypeError` — a length plus a bare number is
a question with no honest answer (5 what? metres? miles?).

The shipped answer goes a little further, and the page explains why each
step earns its place: subtraction and scaling (`3 * Length(meters=2.5)`),
ordering so `sorted()` works, `__hash__` so lengths can live in sets, a
tolerant `is_close` beside the exact `==`, and four `from_*` alternative
constructors so `Length.from_miles(1)` reads the way you would say it.

## Starter

Save this as `length.py` and fill in the `TODO` markers. The `meters`
property pair is given complete — it is the pattern every other unit
copies — and so is the `kilometers` pair, as a worked example one line
long on each side.

```python
"""length.py — a Length that stores metres and speaks five units.

    python length.py
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

    # TODO: the miles property pair — getter divides by METERS_PER_MILE,
    # setter assigns self.meters (NOT self._meters) so validation runs.

    # TODO: the feet property pair.

    # TODO: the inches property pair.

    # --- arithmetic -------------------------------------------------------

    def __add__(self, other: object) -> "Length":
        """Two Lengths add. Anything else declines to NotImplemented."""
        # TODO: if `other` is not a Length, return NotImplemented (return,
        # not raise!) and let Python raise the TypeError itself. Otherwise
        # return a NEW Length holding the sum of the two _meters.

    def __sub__(self, other: object) -> "Length":
        """Two Lengths subtract, as long as the result is not negative."""
        # TODO: same shape as __add__. The Length constructor already
        # refuses a negative result — do not check twice.

    def __mul__(self, factor: object) -> "Length":
        """A Length scales by a real number, but never by a bool."""
        # TODO: accept int and float but explicitly refuse bool —
        # isinstance(True, int) is True in Python. NotImplemented otherwise.

    # TODO: make 3 * Length(...) work too. One line, no new function.

    # --- comparison and hashing ------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Exact equality on the stored metres. See `is_close` for tolerance."""
        # TODO: NotImplemented for a non-Length, else compare _meters.

    def __lt__(self, other: object) -> bool:
        """Order by the stored metres."""
        # TODO: same shape as __eq__. This is what sorted() calls.

    def __hash__(self) -> int:
        """Consistent with the exact `__eq__`, so Lengths work in sets."""
        # TODO: hash the one stored number.

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
        # TODO: f"Length(meters={...!r})"

    def __str__(self) -> str:
        """Reader form: picks km, m or inches by magnitude."""
        # TODO: >= 1 km -> "1.000 km"; >= 1 m -> "1.000 m"; else inches
        # to two decimal places, "39.37 in".


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
```

Two details in the given half worth a second look before you start.

**`__init__` assigns `self.meters`, not `self._meters`.** That single line
routes construction through the property setter, so `Length(meters=-1)`
is refused at birth instead of becoming a negative distance that fails
somewhere else later. Every setter you write should pull the same trick.

**The conversion constants are exact.** Since the 1959 international yard
and pound agreement, one inch is *defined* as exactly 0.0254 m, a foot as
0.3048 m, and a mile as 1609.344 m. They are not measurements with error
bars — which is why `Length.from_feet(5280).miles` can come back as exactly
`1.0`.

## Requirements

1. Exactly one number is stored: `_meters`. Every other unit is derived.
2. `meters`, `kilometers`, `miles`, `feet` and `inches` are each a
   `@property` with both a getter and a setter.
3. Every unit setter assigns `self.meters` — never `self._meters` — so the
   validation runs exactly once, in one place.
4. A negative or NaN length raises `ValueError`, whatever unit it arrived in.
5. `Length + Length` and `Length - Length` return a **new** `Length`;
   `Length + 5` raises `TypeError`, produced by returning `NotImplemented`.
6. `Length * 3` and `3 * Length` both scale; multiplying by a `bool` is
   refused.
7. `__eq__` is exact, `__hash__` agrees with it, `__lt__` makes `sorted()`
   work, and `is_close` exists for numbers that came out of arithmetic.
8. `__repr__` always shows metres; `__str__` picks a readable unit by
   magnitude.
9. Do not edit `main()`.

## Constraints

- **Store one number, derive four.** Storing all five units means five
  copies of one fact that must be kept in agreement by hand, forever. Set
  `feet` and forget to update `inches`, and the object now disagrees with
  itself — with no exception anywhere, which is the worst kind of wrong.
- **Route every setter through `self.meters`.** The `meters` setter is
  where the NaN and negativity checks live. Write `self._meters = ...` in
  the other four setters and you have four validation holes.
- **Return `NotImplemented`; never raise `TypeError` yourself.**
  `NotImplemented` (a value, not an exception) tells Python "I do not
  handle this operand". Python then tries the other side's reflected
  method, and only when both decline does it raise — with a message naming
  both types, better than anything you would write by hand. Raising
  directly satisfies the letter of the spec and breaks the protocol for
  every future type that *could* have handled the mix.
- **Refuse `bool` in `__mul__`.** `isinstance(True, int)` is `True` in
  Python, so without the guard `Length(meters=10) * True` silently gives
  10 metres. A distance times a boolean is a bug at the call site every
  time; refusing turns a wrong answer into a `TypeError`.
- **`==` stays exact, and `is_close` lives beside it.** A tolerant `==`
  would be friendlier and would break hashing: `math.isclose` is not
  transitive, so `a == b` and `b == c` would not imply `a == c`, and no
  hash function can be consistent with that. Exact `==`, consistent
  `__hash__`, tolerant `is_close` — each doing the one job it can do
  honestly.
- **`__repr__` never picks a unit.** It is the developer form: always
  metres, unambiguous, round-trippable. `__str__` is for a human and may
  choose km, m or inches by magnitude. Straight out of lecture 01:
  unambiguous versus readable.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-06-unit-conversion-class.py
Length(meters=1000.0) | 1.000 km
kilometers: 1.0
miles: 0.621371192237334
feet: 3280.839895013123
inches: 39370.078740157485
after d.miles = 1.0 -> Length(meters=1609.344)
round trip miles: 1.0
5280 feet -> Length(meters=1609.344) = 1.0 miles
10m + 5m = Length(meters=15.0)
mixed units: Length(meters=103.048)
scaled: Length(meters=7.5)
TypeError: unsupported operand type(s) for +: 'Length' and 'int'
equal: True
float noise: Length(meters=1609.3440000000003) == Length(meters=1609.344) -> False
is_close: True
sorted: [Length(meters=5.0), Length(meters=30.48), Length(meters=1609.344)]
hashable: 1
ValueError: length cannot be negative, got -1.0
ValueError: length cannot be negative, got -1.0
```

The first four value lines are the brief's own example: `Length(meters=1000)`
reports `1.0` kilometres, and after `d.miles = 1.0` the internal value is
`1609.344` m — the "~1609.344" the spec predicts, exactly.
`5280 feet -> ... = 1.0 miles` is the sanity check that two conversion
factors agree with each other. The `float noise` line is the one to sit
with: two objects that represent the same distance, that are not `==`, and
that `is_close` correctly calls equal.

## Steps

1. Save the starter and run it. It fails with
   `TypeError: __repr__ returned non-string (type NoneType)` — `__repr__`
   is still only a comment, and a method whose body is only a comment
   returns `None`. Write `__repr__` and `__str__` first; now the first line
   prints.
2. Write the three missing property pairs. Each is two tiny methods: the
   getter divides `self._meters` by the constant, the setter multiplies and
   assigns `self.meters`. Check the four conversion lines against a REPL:

   ```bash
   python -c "print(1000 / 1609.344, 1000 / 0.3048)"
   ```

   ```text
   0.621371192237334 3280.839895013123
   ```

3. Check the setter direction: `after d.miles = 1.0` must show
   `Length(meters=1609.344)`, and the round trip must come back as exactly
   `1.0`.
4. Write `__add__`, `__sub__`, `__mul__` and the reflected multiply. Run —
   the `TypeError:` line should now appear, and notice you never wrote that
   message: Python composed it after your `NotImplemented`.
5. Write `__eq__`, `__lt__` and `__hash__`. The `sorted:` line proves
   ordering, and `hashable: 1` proves that two equal lengths collapse to
   one set member.
6. Now break it on purpose. Change the `meters` getter to
   `return self.meters` and run. Read the `RecursionError` — the property
   *is* the attribute named `meters`, so reading it inside itself re-enters
   the property forever. Put `self._meters` back. Everyone writes this bug
   exactly once; better here than in review.

## The Solution

```python
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
```

**There is exactly one number in the object.** `_meters`. Every other unit
is a pair of tiny functions over it: the getter divides, the setter
multiplies. Store all five and you have five numbers that must be kept in
agreement forever, which they will not be — set `feet` and forget to update
`inches` and the object now disagrees with itself with no error anywhere.
One stored fact, four derived views, and inconsistency becomes structurally
impossible.

**Every setter routes through `self.meters`, not `self._meters`.**
`miles.setter` writes `self.meters = value * METERS_PER_MILE`, which invokes
the `meters` setter, which runs the NaN and negativity checks. Write
`self._meters = ...` directly in each of the four and you have four copies
of the validation — or, more likely, one copy and three holes. This is the
same "one place for the rule" move as `super().__init__` in Problem 1.

**`__init__` assigns `self.meters`, not `self._meters`, for the same
reason.** The constructor gets the validation free, so `Length(meters=-1)`
raises rather than creating a negative distance that fails somewhere else
later.

**`__add__` returns `NotImplemented` and Python raises the `TypeError` for
you.** The spec says "raise `TypeError` for `Length + 5`", and this is how
Python wants you to do it. `NotImplemented` tells the interpreter "I do not
handle this operand"; it then tries `(5).__radd__(length)`, which also
declines, and only then raises:

```text
TypeError: unsupported operand type(s) for +: 'Length' and 'int'
```

That message is better than anything you would write by hand, it names both
types, and it is the message every other Python type produces for the same
mistake. Raising `TypeError` yourself inside `__add__` also satisfies the
letter of the spec, but it breaks the protocol — a future `Distance` class
with an `__radd__` that *could* have handled `Length + Distance` never gets
asked.

**`__mul__` explicitly excludes `bool`.** `isinstance(True, int)` is `True`
in Python, so without the guard `Length(meters=10) * True` silently gives
10 metres and `* False` gives 0. Multiplying a distance by a boolean is a
bug at the call site every time; refusing it turns a wrong answer into a
`TypeError`.

**`__rmul__ = __mul__` makes `3 * length` work.** Python tries
`(3).__mul__(length)` first, gets `NotImplemented` back from `int`, then
tries the reflected `length.__rmul__(3)`. Since scalar multiplication
commutes, assigning the same function to both names is correct and honest.
(Note `__radd__` is deliberately *not* defined: `5 + Length` should fail
exactly as `Length + 5` does.)

**`__eq__` is exact, and `is_close` exists alongside it.** This is a real
trade and the code takes a position. Exact `==` lets `__hash__` be
consistent (equal objects hash equal, so `Length` works in sets and as dict
keys). A tolerant `==` using `math.isclose` would be friendlier at the call
site and would break hashing — `isclose` is not transitive, so `a == b` and
`b == c` would not imply `a == c`, and no hash function can be consistent
with that. So: `==` is exact, `is_close` is available when the numbers came
out of arithmetic, and the docstring says which to use when. The demo shows
a real case where they differ.

**`__str__` picks a unit; `__repr__` never does.** `repr` is the developer
form and always shows metres, unambiguously and round-trippably. `str` is
for a human and chooses km, m, or inches by magnitude. Straight out of
lecture 01: unambiguous versus readable.

**The conversion constants are exact by definition.** Since the 1959
international yard and pound agreement, one inch is *defined* as exactly
0.0254 m, a foot as 0.3048 m, and a mile as 1609.344 m. These are not
measurements with error bars, which is why `Length.from_feet(5280).miles`
comes back as exactly `1.0`.

## Run it

Copy the worked answer on this page into `problem-06-unit-conversion-class.py` and run it:

```bash
python problem-06-unit-conversion-class.py
```

It imports only `math` and needs no setup. Save your own version as
`length.py`; the longer download name is there so it cannot overwrite your
work.

## Common bugs to catch

- **`RecursionError: maximum recursion depth exceeded` — the classic.**

  ```python
  @property
  def meters(self):
      return self.meters          # calls itself

  @meters.setter
  def meters(self, value):
      self.meters = value         # calls itself
  ```

  The property *is* the attribute named `meters`, so reading or writing
  `self.meters` inside it re-enters the property. The storage must have a
  different name — conventionally the same name with a leading underscore.

- **`AttributeError: property 'meters' of 'Length' object has no setter`.**

  ```python
  class Length:
      def __init__(self, meters=0.0):
          self.meters = meters
      @property
      def meters(self):
          return self._meters
  ```

  A getter-only property, assigned in `__init__`. Either add the setter
  (what this solution does) or assign `self._meters` directly in the
  constructor.

- **Storing all five units.** Five fields, five places to update, and a
  `__str__` that reports whichever one was updated most recently. Works in
  the demo, drifts in production, and never raises. Store one, derive four.

- **Raising `TypeError` by hand inside `__add__`.** It satisfies the spec's
  letter and breaks the reflected-operation protocol. `return
  NotImplemented` gets you the same exception with a better message and
  keeps the door open for other types.

- **Setters that write `self._meters` directly.** The conversions still
  work, so nothing fails today — but `d.miles = -1.0` now creates a
  negative distance the `meters` setter would have refused. One validation,
  four holes.

- **Expecting float arithmetic to be exact.**
  `Length.from_miles(0.1) + Length.from_miles(0.9) == Length.from_miles(1)`
  is `False`, and that is not a bug in the class — it is IEEE 754. Any test
  on derived units needs `math.isclose` or a rounded comparison. The
  `float noise` line in the demo exists to make you meet this on purpose.

## Under the hood

<details>
<summary>Under the hood — NotImplemented, reflected operations, and why a tolerant == would break sets</summary>

`a + b` is not one call; it is a small negotiation. Python asks up to two
questions:

1. `type(a).__add__(a, b)` — "left side, can you do this?"
2. If that returned `NotImplemented`: `type(b).__radd__(b, a)` — "right
   side, can *you*?" (the `r` is for *reflected*)
3. If both declined: `TypeError: unsupported operand type(s) for +: ...`

`NotImplemented` is a real value — a singleton, like `None` — not an
exception. It exists precisely so a class can decline an operand *without*
slamming the door on the whole expression. This is how `int` and `float`
cooperate: `(3).__add__(3.5)` returns `NotImplemented` because `int` does
not know floats, then `(3.5).__radd__(3)` says "I do", and you get `6.5`.
Your `Length` is joining that same protocol, which is why it must play by
the same rule.

The name collision to avoid: `NotImplementedError` is an *exception* meant
for abstract methods that a subclass should have overridden. Returning the
exception class from `__add__`, or raising `NotImplemented`, are both
category errors Python will let you make. The value is returned; the error
is raised; they are unrelated.

One subtlety the solution exploits without saying so: when the two operands
are the *same type*, Python skips the reflected call — there is no point
asking the same class twice. And when the right operand is a *subclass* of
the left, Python asks the subclass **first**, so `Length + NauticalLength`
gives the more specific class the first refusal. The protocol was designed
so inheritance hierarchies extend operators without editing the parent —
the same open-for-extension idea as `NotImplemented` itself.

**Why exact `==` is load-bearing for `__hash__`.** Python's one hard rule:
objects that compare equal must have equal hashes. Sets and dicts find an
object by hashing it first, then confirming with `==` — if two "equal"
objects landed in different hash buckets, a set could hold both and
`hashable: 1` would print `2`. Now suppose `==` used `math.isclose`.
Tolerant equality is not transitive — `a` close to `b`, `b` close to `c`,
`a` not close to `c` — so there is no way to assign buckets that keeps the
rule. Any hash you write will be wrong for *some* triple. Which is why the
tolerant comparison must be a named method, not the operator: the operator
carries obligations `isclose` cannot meet.

Defining `__eq__` also has a quiet side effect worth knowing: it sets your
class's `__hash__` to `None`, making instances unhashable, unless you
define `__hash__` yourself. That is Python protecting the invariant — a
class that redefined equality but kept identity-based hashing would break
sets silently. The solution defines both, together, on the same stored
number, which is the only arrangement that keeps them consistent.

</details>

## Acceptance checklist

- [ ] `python length.py` runs with no traceback.
- [ ] Every output line matches the transcript exactly.
- [ ] The class stores exactly one number, `_meters`.
- [ ] Every unit setter assigns `self.meters`, never `self._meters`.
- [ ] `Length(meters=10) + 5` raises `TypeError` naming both types — and
      you did not write that message.
- [ ] `3 * Length(meters=2.5)` works.
- [ ] `Length(meters=-1)` and `d.miles = -1.0` both raise `ValueError`.
- [ ] `hashable:` prints `1` — equal lengths collapse in a set.
- [ ] The `float noise` line prints `False` and the `is_close` line `True`,
      and you can say why in one sentence.
- [ ] Every signature is type-hinted.
- [ ] Committed to Git with a message like
      `Add Week 7 homework 6: unit conversion class`.

## Stretch

- Add `yards`. Count the lines it costs — one constant and one property
  pair — and notice that none of the arithmetic, comparison or display code
  changes. That is the store-one-derive-many design paying rent.
- Build a `Temperature` class with `celsius`, `fahrenheit` and `kelvin`
  properties. The conversions are now *affine* — multiply **and add** —
  and `Temperature(20) + Temperature(5)` is physically meaningless while
  `Temperature(20) - Temperature(5)` arguably is not. Write one sentence on
  which operators you kept and why. Not every quantity is a `Length`.
- Decorate the class with `functools.total_ordering` and delete nothing.
  Then check what `<=` and `>` do, and read the docs for what the decorator
  costs at call time compared to writing all four by hand.
- Add `__format__` so `f"{d:mi}"` renders miles and `f"{d:km}"` kilometres,
  falling back to `str(d)` for an empty spec. Decide what an unknown unit
  spec should do — silently fall back, or raise — and defend the choice in
  the docstring.

Next up: the [mini-project](../mini-project/README.md), which uses
everything this week taught at once.
