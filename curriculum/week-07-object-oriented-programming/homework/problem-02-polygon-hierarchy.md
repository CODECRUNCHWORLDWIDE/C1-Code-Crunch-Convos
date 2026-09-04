# Problem 2 — Polygon hierarchy

> **Topic:** abstract base classes, `@abstractmethod`, and making "you must implement this" a real rule
> **Lecture:** [02 — Inheritance and Composition](../lecture-notes/02-inheritance-and-composition.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** Exercise 3's base class refused to guess by raising when somebody called `area()`. That is late. This is the same idea, moved earlier: a class that cannot even be built until it has kept its promises. It is also where you find out that a promise has to be kept *the same way* by everybody, or the polymorphic loop breaks in a way no base class can catch.

## The Brief

Build a family of polygons.

At the top is `Polygon`, and it is **abstract** — a class you cannot make an
object out of, because it is only a promise. The promise is two names: every
polygon can report its `area` and its `perimeter`. `Polygon` itself has no
idea how; the subclasses do.

Exercise 3 made the same promise with `raise NotImplementedError`, which
works but fires late — a shape with no `area` is a perfectly buildable
object right up until somebody calls the method, possibly three hours into a
batch job. Python's `abc` module moves the failure to construction time:

```python
from abc import ABC, abstractmethod

class Polygon(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        """Enclosed area in square units."""
```

Inherit from `ABC`, mark a method `@abstractmethod`, and Python refuses to
build **any** class that has not supplied it. Not when it is called. When you
try to make one.

Three subclasses:

- **`Triangle`** — three sides, and they have to actually close into a
  triangle.
- **`Rectangle`** — width and height.
- **`RegularPolygon`** — `n` equal sides, with closed-form formulas rather
  than a loop.

Then a `main()` that puts all four objects in one list and prints the total
area by looping over them, without asking any of them what they are.

**One thing about the wording, before you start.** The brief above asks for
abstract *methods* `area()` and `perimeter()`, and also for a `@property`
`area` on `Rectangle`. Taken literally those two conflict. If `Rectangle.area`
is a property while `Triangle.area` is a method, then
`sum(p.area for p in shapes)` adds a number to two bound methods, and
`sum(p.area() for p in shapes)` blows up on the rectangle. There is no
arrangement in which both spellings work.

The honest resolution is to make the whole family agree. This answer declares
`area` and `perimeter` as **abstract properties** — `@property` stacked over
`@abstractmethod` — and implements them as properties everywhere. That
satisfies both halves of the request (a property *is* a method, and
`Rectangle.area` is a property) and keeps the loop working. Making them all
plain methods instead is equally correct. What is not correct is mixing the
two, and the abstract base class will not save you from it — which is the
sharpest lesson on this page.

## Starter

Save this as `polygons.py` and fill in the `TODO` markers.

```python
"""polygons.py — a Polygon hierarchy behind an abstract base class.

    python polygons.py
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
        # TODO: f"{type(self).__name__}: area={...:.4f}, perimeter={...:.4f}"
        raise NotImplementedError

    def __repr__(self) -> str:
        """Developer form, naming the actual subclass."""
        return f"{type(self).__name__}(area={self.area:.4f})"


class Triangle(Polygon):
    """Three sides that actually close into a triangle."""

    def __init__(self, a: float, b: float, c: float) -> None:
        """Store three sides, refusing any trio that cannot close."""
        # TODO: refuse a non-positive side.
        # TODO: refuse sides that break the triangle inequality —
        #       a + b > c AND a + c > b AND b + c > a. All three.
        # TODO: store self.a, self.b, self.c as floats

    @property
    def perimeter(self) -> float:
        """The three sides added up."""
        # TODO
        raise NotImplementedError

    @property
    def area(self) -> float:
        """Heron's formula: sqrt(s(s-a)(s-b)(s-c)) with s the semi-perimeter."""
        # TODO: s is half the perimeter
        raise NotImplementedError


class Rectangle(Polygon):
    """Width and height; area is the property the brief calls for."""

    def __init__(self, width: float, height: float) -> None:
        """Store two positive sides."""
        # TODO

    @property
    def area(self) -> float:
        """Width times height."""
        # TODO
        raise NotImplementedError

    @property
    def perimeter(self) -> float:
        """Twice the sum of the two sides."""
        # TODO
        raise NotImplementedError


class RegularPolygon(Polygon):
    """n equal sides. Closed-form perimeter and area, no trigonometry per side."""

    def __init__(self, n_sides: int, side_length: float) -> None:
        """Store a side count of at least three and a positive side length."""
        # TODO

    @property
    def perimeter(self) -> float:
        """Side count times side length."""
        # TODO
        raise NotImplementedError

    @property
    def area(self) -> float:
        """A = n * s^2 / (4 * tan(pi/n)) — the n triangles from the centre."""
        # TODO: math.tan takes RADIANS, so it is math.pi / n
        raise NotImplementedError


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

    total = sum(shape.area for shape in shapes)
    print(f"total area: {total:.4f}")
    print(f"total perimeter: {sum(s.perimeter for s in shapes):.4f}")
    print("largest:", max(shapes, key=lambda s: s.area))

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
```

Two formulas you may not have met.

**Heron's formula.** You know three sides and nothing else — no height, no
angles. Heron gives you the area from the sides alone. Let `s` be half the
perimeter; then the area is `sqrt(s(s-a)(s-b)(s-c))`.

**The regular-polygon area.** Cut an `n`-sided shape into `n` identical
triangles meeting at the centre. Each has base `s` and height
`s / (2·tan(π/n))`, so the whole thing is `n·s² / (4·tan(π/n))`.
`math.tan` takes radians, which is why it is `math.pi / n` and not `180 / n`
— degrees here is a silent wrong answer, not an error.

## Requirements

1. `Polygon(ABC)` declares `area` and `perimeter` as abstract properties, and
   provides a concrete `describe()` and `__repr__` that every subclass
   inherits untouched.
2. `Polygon()` raises `TypeError` at construction. So does any subclass that
   fails to supply both names.
3. `Triangle(a, b, c)` refuses a non-positive side and refuses a trio that
   breaks the triangle inequality, with a message naming the sides.
4. `Triangle.area` uses Heron's formula. A 3-4-5 triangle is area `6`,
   perimeter `12`.
5. `Rectangle(width, height)` refuses a non-positive side. `area` is a
   `@property`.
6. `RegularPolygon(n_sides, side_length)` refuses fewer than three sides and
   a non-positive side length, and uses the closed-form formulas.
7. `main()` builds a `list[Polygon]` and totals it with one expression
   containing no `isinstance` and no branching.
8. Every polygon exposes `area` and `perimeter` **the same way**. Do not mix
   properties and methods.

## Constraints

- **`@property` goes on the outside, always.** Decorators apply bottom-up:
  `abstractmethod` marks the plain function, then `property` wraps the marked
  function and carries the abstract flag through. Reverse them and the flag
  ends up in the wrong layer, `ABCMeta` never sees it, and the class becomes
  buildable with no implementation at all. Remember it as "`@property` is
  always outermost".
- **Check all three pairs of the triangle inequality.** `a + b > c` alone is
  enough only if you already know `c` is the longest side, and the
  constructor accepts them in any order. (The compact alternative is to
  `sorted()` the sides and do one comparison — same result, one more line.)
- **Validate before Heron, not after.** Skip the check and a trio like
  `1, 2, 10` makes one factor negative, the product negative, and
  `math.sqrt` raises `ValueError: math domain error` — the right exception
  type with a useless message about arithmetic, for what is really bad input.
- **`math.tan(math.pi / n)`, in radians.** `math.tan(180 / n)` runs happily
  and returns nonsense.
- **`float(...)` the stored sides.** `RegularPolygon(6, 2)` then reprs as
  `side_length=2.0`, so an `int` argument and a `float` argument behave
  identically downstream.
- **Never compare a computed area with `==`.** `RegularPolygon(4, 3)` prints
  `area=9.0000` and is really `9.000000000000002`, because
  `math.tan(math.pi/4)` is `0.9999999999999999` rather than 1. Use
  `math.isclose` in any test you write on derived geometry.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-polygon-hierarchy.py
Triangle: area=6.0000, perimeter=12.0000
Rectangle: area=10.0000, perimeter=13.0000
RegularPolygon: area=10.3923, perimeter=12.0000
RegularPolygon: area=9.0000, perimeter=12.0000
total area: 35.3923
total perimeter: 49.0000
largest: RegularPolygon(n_sides=6, side_length=2.0)
TypeError: Can't instantiate abstract class Polygon without an implementation for abstract methods 'area', 'perimeter'
TypeError: Can't instantiate abstract class Pentagon without an implementation for abstract method 'perimeter'
ValueError: sides (1, 2, 10) violate the triangle inequality (the sum of any two must exceed the third)
ValueError: width and height must be positive, got 0x5
ValueError: a polygon needs at least 3 sides, got 2
```

Every number is checkable by hand. The 3-4-5 triangle is the classic right
triangle: area 6, perimeter 12. The 4 × 2.5 rectangle: area 10, perimeter 13.
The regular hexagon with side 2: perimeter 12, and area
`6·4 / (4·tan(30°)) = 6/tan(30°) ≈ 10.3923`. The regular 4-gon with side 3 is
a 3 × 3 square: area 9, perimeter 12.

The two `TypeError`s are the whole reason for `abc`. Read them: each one
names exactly which methods are missing. That is one of the more useful error
messages in the language — read it rather than guessing.

(The wording is Python 3.12 and later. Python 3.11 and earlier said
`Can't instantiate abstract class Polygon with abstract methods area, perimeter`.)

## Steps

1. Save the starter and run it. It fails in `describe`, which is called
   before anything else.
2. Write `describe`, then `Rectangle` — the easiest subclass. Run and check
   line two.
3. Write `Triangle`, checks first, then `perimeter`, then `area`. Verify the
   3-4-5 gives exactly `6.0` before moving on.
4. On purpose, comment out the triangle-inequality check and build
   `Triangle(1, 2, 10)`. Read the `math domain error` and note how little it
   tells you. Put the check back.
5. Write `RegularPolygon`. Check the hexagon against
   `6 / math.tan(math.pi / 6)` in a REPL.
6. Run the whole file. Both `TypeError`s should print.
7. Now try the thing the design note warns about, in a scratch file: make
   `Rectangle.area` a property and `Triangle.area` a plain method, then run
   `sum(p.area() for p in shapes)`. Note that `ABC` said nothing, and note
   which shape it died on.

## The Solution

```python
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
```

**`ABC` plus `@abstractmethod` turns "you must implement this" into a rule the
interpreter keeps.** `abc.ABC` installs a special metaclass that collects the
names of every method marked `@abstractmethod` into `__abstractmethods__`.
Building a class whose `__abstractmethods__` is not empty raises `TypeError`
*at construction*, before any of your code runs. That is a much better place
to find out than in the middle of a report, three hours into a batch job, on
the one shape whose `area` you forgot.

**The decorator order `@property` then `@abstractmethod` is not arbitrary.**
Decorators apply bottom-up: `abstractmethod` marks the plain function, then
`property` wraps the marked function into a descriptor and carries the
abstract flag through.

**`describe()` shows why an abstract base class is more than an interface.**
It is a *concrete* method on the abstract class that reads `self.area` and
`self.perimeter` — names that do not exist yet at the point the base class is
written. Every subclass inherits it, and it works because Python resolves
`self.area` against the actual object's class at call time. That shape has a
name: the base class writes the algorithm, the subclasses supply the pieces.

**Heron's formula is the right area formula for three sides.** You do not
know the height, and computing one would mean choosing a base and doing
trigonometry. Notice that the validation earns its keep here: if the triangle
inequality is broken, one of those factors goes negative, the product goes
negative, and `math.sqrt` raises. Checking up front turns that into a
sentence that names the actual problem.

**Checking all three pairs is necessary, not paranoid.** Since the
constructor accepts the sides in any order, you cannot assume which is
longest.

**The regular-polygon area is one formula, not a loop.** The perimeter is
just `n · s`, and the area falls out of the `n` triangles meeting at the
centre.

**`RegularPolygon(4, 3)` prints `area=9.0000`, and it is really
`9.000000000000002`.** The `:.4f` formatting hides it. This is worth knowing
before you write `assert square.area == 9`.

## Run it

Copy the worked answer on this page into `problem-02-polygon-hierarchy.py` and run it:

```bash
python problem-02-polygon-hierarchy.py
```

It imports only `math` and `abc` from the standard library. Save your own
version as `polygons.py`.

## Common bugs to catch

- **Mixing properties and methods across the family.** This is the exact
  failure the design note warns about, and it is the reason to read this
  section before you start:

  ```python
  class Polygon(ABC):
      @abstractmethod
      def area(self) -> float: ...

  class Rectangle(Polygon):
      def __init__(self, w, h): self.w, self.h = w, h
      @property
      def area(self) -> float: return self.w * self.h

  class Square(Polygon):
      def __init__(self, s): self.s = s
      def area(self) -> float: return self.s ** 2

  print(sum(p.area() for p in [Square(2), Rectangle(3, 4)]))
  ```

  ```text
  TypeError: 'int' object is not callable
  ```

  The abstract base class does **not** catch this. `Rectangle` has *something*
  named `area`, so `__abstractmethods__` is satisfied and the class builds
  happily. The failure waits until the call site, and it fires on the
  rectangle only — so a loop over shapes produces several correct answers
  before it dies. An ABC checks that a name exists. It cannot check that
  everybody spelled it the same way.

- **Reversing the decorators.**

  ```python
  @abstractmethod
  @property
  def area(self) -> float: ...
  ```

  No error at definition time, no error at construction time. The class is
  simply no longer abstract in the way you wanted, and a subclass that
  forgets `area` gets a confusing failure much later. `@property` on the
  outside, always.

- **`ValueError: math domain error`.** You skipped the triangle-inequality
  check and Heron's formula took the square root of a negative number. Same
  exception type as the good version, useless message. Validate at the
  boundary and say what is actually wrong.

- **`AttributeError: 'Triangle' object has no attribute 'a'`.** Your
  `__init__` body is only comments, so it sets nothing. The starter is
  written that way on purpose.

- **The hexagon comes out as `2.4022` or some other small number.** You used
  degrees: `math.tan(180 / n)` instead of `math.tan(math.pi / n)`. No error,
  just a wrong answer. Every trigonometric function in `math` takes radians.

- **`TypeError: unsupported operand type(s) for +: 'int' and 'property'`.**
  You wrote `sum(Polygon.area for ...)` or otherwise reached for the property
  on the *class* rather than on an instance. `Polygon.area` is the property
  object itself; `shape.area` runs it.

- **`Polygon()` builds without complaint.** Either you forgot `(ABC)` on the
  class line, or none of your methods is actually marked. Check that
  `sorted(Polygon.__abstractmethods__)` is `['area', 'perimeter']`.

## Under the hood

<details>
<summary>Under the hood — what abc actually checks, and the three ways to say "this type will do"</summary>

`abc` is not a language feature. It is a module, and you can watch it work.

`class Polygon(ABC)` sets the class's **metaclass** to `ABCMeta`. A metaclass
is the thing that builds classes, the way a class builds objects — so
`ABCMeta` gets a chance to run code every time a class in this family is
created. What it does is collect names:

```text
>>> sorted(Polygon.__abstractmethods__)
['area', 'perimeter']
>>> Rectangle.__abstractmethods__
frozenset()
>>> type(Polygon)
<class 'abc.ABCMeta'>
```

`object.__new__` then refuses to build an instance of any class whose
`__abstractmethods__` is non-empty. That is the entire mechanism: one
frozenset, checked at construction.

Two consequences fall straight out of it.

**The check is on the name, not on the shape.** `ABCMeta` asks "is there
something called `area` anywhere in this class's MRO that is not still
marked abstract?" It cannot ask "is it a property?", "does it take the right
arguments?", or "does it return a float?". That is why the property/method
mix-up at the top of the bugs list sails past it.

**The check happens at construction, not at class definition.** Defining an
incomplete subclass is fine and raises nothing. You find out when somebody
tries to build one:

```text
>>> class Pentagon(Polygon):
...     @property
...     def area(self) -> float:
...         return 1.0
...
>>> sorted(Pentagon.__abstractmethods__)
['perimeter']
>>> Pentagon()
TypeError: Can't instantiate abstract class Pentagon without an implementation for abstract method 'perimeter'
```

Now the wider question: `abc` is one of **three** ways Python lets you say "a
value of this shape will do", and knowing when to reach for which is the real
skill.

**1. Duck typing.** Write no base class at all. `total_area` in Exercise 3
worked on anything with an `area()`, and `Subject` in homework problem 5
works on anything callable. Cheapest, most flexible, and completely silent
about its expectations — a wrong object fails at the call, with an
`AttributeError` that names the method rather than the promise.

**2. An abstract base class.** What this problem uses. The promise is written
down in one place, the failure moves to construction time, and a reader can
see the whole contract in six lines. The cost is that a class has to
*inherit* from `Polygon` to count — which is fine when you own all the
classes, and awkward when the shape you want already exists somewhere else.

There is a hatch for that last case, and it is worth knowing:

```text
>>> class Blob:                      # inherits nothing
...     @property
...     def area(self): return 1.0
...     @property
...     def perimeter(self): return 4.0
...
>>> Polygon.register(Blob)
<class '__main__.Blob'>
>>> isinstance(Blob(), Polygon)
True
```

`register` makes `isinstance` say yes without any inheritance. It checks
nothing at all — you are asserting the relationship, not proving it — which
is how `collections.abc` can claim that `list` is a `MutableSequence` even
though `list` predates the whole module.

**3. A `typing.Protocol`.** Structural typing: a class counts if it has the
right methods, whether or not it has ever heard of your protocol.

```python
from typing import Protocol

class HasArea(Protocol):
    @property
    def area(self) -> float: ...
```

Now a type checker will accept any object with an `area` property, with no
inheritance and no `register` call. That is duck typing that a tool can
verify, and it is usually the right answer for a shape you do not own. The
cost is that it is checked by `mypy`, not by Python — nothing raises at
runtime unless you also add `@runtime_checkable`, and even then `isinstance`
only checks that the names exist.

The rule of thumb: **`abc` when you own the family and want the failure
early; `Protocol` when you are describing somebody else's objects; plain duck
typing when the promise is one method wide and the code is small.** This
problem is squarely the first case, which is why it is the one you build.

</details>

## Acceptance checklist

- [ ] `python polygons.py` runs with no traceback.
- [ ] All thirteen output lines match exactly.
- [ ] `Polygon()` raises `TypeError`, and the message names both missing
      methods.
- [ ] An incomplete subclass raises `TypeError` naming just the one it is
      missing.
- [ ] `area` and `perimeter` are properties on *every* class, with
      `@property` outermost.
- [ ] `Triangle(1, 2, 10)` raises `ValueError`, not `math domain error`.
- [ ] The total is computed with one expression containing no `isinstance`
      and no `if`.
- [ ] Every signature is type-hinted.
- [ ] Committed to Git with a message like
      `Add Week 7 homework 2: polygon hierarchy`.

## Stretch

- Add a `Square(RegularPolygon)` that takes one side, and confirm it needs no
  `area` or `perimeter` of its own. Then decide whether it earns its place in
  the file at all, given that `RegularPolygon(4, s)` already exists, and write
  one sentence either way.
- Add `__eq__` and `__lt__` comparing area, so `sorted(shapes)` works. Use
  `math.isclose` in `__eq__` and then explain, in a comment, why that makes
  the class unsafe to put in a set. (Exercise 4's second Under the hood block
  has the answer.)
- Make `describe()` accept a unit string — `describe("cm")` — with a sensible
  default, and note that you changed one method in one place and every
  subclass got it.
- Write a `Protocol` version of the contract and re-point `main`'s type hints
  at it. Run `mypy` on both and compare what each one catches. The
  interesting case is a class that satisfies the protocol without inheriting
  from anything.

Next: [Problem 3 — `Stack` built on a list](./problem-03-stack-built-on-a-list.md).
