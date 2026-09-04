# Exercise 3 — Inheritance and Shapes

> **Topic:** inheritance, `super()`, overriding, and one loop that does not care what is in the list
> **Lecture:** [02 — Inheritance and Composition](../lecture-notes/02-inheritance-and-composition.md)
> **Difficulty:** Easy
> **Target time:** 60 minutes
> **Why this one:** Lecture 02 promised this exercise by name. It is the smallest honest demonstration of polymorphism — a list holding three different types, one loop, no type checks anywhere. Once you have written the loop that does not care what is in the list, the reason people organise code into families of classes stops being abstract.

## The Brief

The sign shop from Exercise 2 has outgrown rectangles. A job now mixes
rectangular panels, circular clock faces, and triangular corner gussets, and
the estimator needs one number: total square centimetres of material.

The wrong way to build this is a function full of
`if kind == "circle": ...`. Every new shape means editing that function, and
one day somebody edits it wrong.

The right way needs one new idea. **Inheritance** lets you write a class that
is a more specific version of another class. `Circle` **is a** `Shape`. It
gets everything `Shape` has, and then it changes or adds the bits that are
different. The general class is the **parent** (or base class); the specific
one is the **child** (or subclass).

So: one `Shape` class that knows how to *describe* a shape, and three
subclasses that each know how to work out their own area. Each subclass
**overrides** `area()` — writes its own version, which wins over the
parent's. The estimator then loops over a list of `Shape` and calls `area()`
on each one, and Python picks the right version for each object without
being told.

That last sentence has a name: **polymorphism**, which is Greek for "many
shapes" and here means it literally. Adding a hexagon tomorrow means writing
one new class and touching nothing else.

This is a fresh file. The `Rectangle` here is a different, smaller class than
the one from Exercise 2 — do not import that one.

## Starter

Create `exercise-03-inheritance-shapes.py` and fill in the `TODO` markers:

```python
"""exercise-03-inheritance-shapes.py — one loop, three kinds of panel.

Estimates material for a mixed sign-shop job. Run it with:

    python exercise-03-inheritance-shapes.py
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
        # TODO: return an f-string using self.label and self.area(),
        # formatting the area with :.2f
        raise NotImplementedError

    def __repr__(self) -> str:
        """Developer form, e.g. `Circle(label='Clock face')`."""
        return f"{type(self).__name__}(label={self.label!r})"


class Rectangle(Shape):
    """A rectangular panel."""

    def __init__(self, label: str, width: float, height: float) -> None:
        """Let Shape store the label, then keep the two sides."""
        # TODO: call super().__init__(label), then set self.width/self.height

    def area(self) -> float:
        """Width times height."""
        # TODO
        raise NotImplementedError


class Circle(Shape):
    """A circular panel."""

    def __init__(self, label: str, radius: float) -> None:
        """Let Shape store the label, then keep the radius."""
        # TODO

    def area(self) -> float:
        """Pi times the radius squared."""
        # TODO: use math.pi
        raise NotImplementedError


class RightTriangle(Shape):
    """A right-angled triangular offcut."""

    def __init__(self, label: str, base: float, height: float) -> None:
        """Let Shape store the label, then keep the base and height."""
        # TODO

    def area(self) -> float:
        """Half the base times the height."""
        # TODO
        raise NotImplementedError


def total_area(shapes: Iterable[Shape]) -> float:
    """Sum the areas of every shape given.

    Contains no isinstance checks and no type names. It works because
    every Shape answers area().
    """
    # TODO: one line with sum() and a generator expression
    raise NotImplementedError


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
```

Three pieces of that starter are new.

**`class Rectangle(Shape):`** — the name in the parentheses is the parent.
Anything `Shape` has, `Rectangle` has too, for free.

**`super().__init__(label)`** — "run the parent's version of this method".
It is how a subclass asks the parent to do the parent's own job instead of
copying it. Here the parent's job is storing the label.

**`type(self).__name__`** — the actual class of this object, as a string. It
is resolved when the line runs, not when you write it, so one `__repr__`
written in `Shape` prints `Circle` for a circle and `Rectangle` for a
rectangle.

## Requirements

1. Every subclass `__init__` calls `super().__init__(label)` as its first
   statement, then sets its own attributes.
2. Every subclass overrides `area()` and nothing else. `describe()` and
   `__repr__` are inherited untouched.
3. `describe()` returns `<label>: <area> sq cm` with the area formatted to
   exactly two decimal places.
4. `Circle.area` uses `math.pi`. `Circle("Clock face", 12.0).area()` is
   `452.3893421169302`, which prints as `452.39`.
5. `RightTriangle.area` is `0.5 * base * height`, so 30 by 18 is `270.0`.
6. `total_area` contains **zero** `isinstance` calls, zero `type()` calls,
   and no `if` statements. If it has any of those, the family of classes is
   not doing its job.
7. Calling `area()` on a bare `Shape` still raises `NotImplementedError` with
   the message already written in the starter. Do not soften it to a
   `return 0.0` — a shape with no area rule is a bug, and returning zero
   hides it inside a correct-looking total.
8. Do not edit `main()`.

## Constraints

- **Single inheritance only.** Three subclasses, one parent, no mixing in
  extra parents. Lecture 02, section 4 explains what multiple inheritance
  costs; you have no reason to pay it here.
- **`describe()` lives in the base class exactly once.** Copy it into each
  subclass and you now have three places where the `sq cm` suffix and the
  `:.2f` can drift apart, and the estimate stops looking like one document.
  The point of a base class is the code you do *not* repeat.
- **Use `math.pi`, not `3.14` or `3.14159`.** A hard-coded constant is a
  number somebody has to trust. `3.14` gives `452.16` for the clock face —
  wrong by a quarter of a square centimetre on one small part, and it adds up
  across a job. `math.pi` is the closest value the machine can hold, and it
  is one import away.
- **Call `super().__init__(label)`; do not write `self.label = label` in each
  subclass.** Both appear to work today. Only one keeps working the day
  `Shape.__init__` grows a second job — a created-at timestamp, an ID, a
  units check — because with the copied version, three subclasses are still
  doing the parent's old job by hand.
- **Keep `area()` a method here, not a `@property`.** Exercise 2 made `area`
  a property because it was one cheap expression on one concrete class. Here
  `area()` is the promise subclasses have to keep, and the parentheses keep
  the override visible to somebody scanning the file and keep the call in
  `total_area` explicit. The same value can deserve a different shape in a
  different class — the question is always what the reader of the call site
  needs to see.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-inheritance-shapes.py
Back panel: 1000.00 sq cm
Clock face: 452.39 sq cm
Corner gusset: 270.00 sq cm
Total material: 1722.39 sq cm
[Rectangle(label='Back panel'), Circle(label='Clock face'), RightTriangle(label='Corner gusset')]
Base class refused: Shape is abstract; subclasses must implement area()
```

Check the total by hand: 1000 plus 452.39 plus 270 is 1722.39.

Line five is worth a second look. You wrote one `__repr__`, in the base
class, and it printed the correct class name three times — because
`type(self).__name__` asks each object what it actually is rather than
hard-coding `Shape`.

Line six proves the base class still refuses to guess.

## Steps

1. Create the file and run it. The first `NotImplementedError` comes from
   `describe`, which is called before any subclass code runs.
2. Implement `describe()`, then `Rectangle`. Run. You should get one correct
   line and then a failure on `Circle`.
3. Implement `Circle` and `RightTriangle` the same way. Run after each.
4. Implement `total_area` as a single `sum(...)` over a generator expression.
   Check the total by hand: `1000 + 452.39 + 270`.
5. Confirm the last line still prints. If it does not, you weakened the base
   class.
6. Now add a fourth shape without touching `total_area`, `describe`, or
   `main`'s loop body: a `Square(Rectangle)` whose `__init__` takes one side
   and calls `super().__init__(label, side, side)`. Append
   `Square("Logo tile", 20.0)` to `panels`, rerun, and watch the estimator
   absorb it — one new line, and the total climbs by `400.00`. Then take it
   back out of the list so your output matches the block above, but keep the
   class in the file. That two-line class is the whole argument for the
   design.
7. Print `[cls.__name__ for cls in Circle.__mro__]` and read the chain:
   `['Circle', 'Shape', 'object']`. That is the list Python walks to find a
   method, and the Under the hood block below is about how it walks it.

## The Solution

```python
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
```

**The base class holds what is the same; the subclasses hold what differs.**
Every shape on this estimate has a label, prints one line in the same format,
and reprs the same way — so `__init__`, `describe` and `__repr__` are written
once, in `Shape`. What differs is the formula, and only the formula, so
`area()` is the only method any subclass overrides. Look at the three
subclasses: none is longer than six lines, because everything the three have
in common was already paid for once.

**`total_area` never asks what it is holding, and that is the definition of
polymorphism.** `sum(shape.area() for shape in shapes)` works because Python
does the choosing at the moment of the call: `shape.area()` looks up `area`
on the actual object, finds `Circle.area` for a circle and
`RightTriangle.area` for a triangle, and calls that. There is no table, no
registry, no `if`. The payoff is not that this loop is shorter than a chain
of `elif` branches — it is that adding a hexagon tomorrow does not touch this
function at all, so this function cannot be the thing you break.

`Square` in the file is the proof. It is three lines, it does not define
`area`, and dropping `Square("Logo tile", 20.0)` into `panels` gives you
`Logo tile: 400.00 sq cm` and a total that climbs by exactly 400 with no edit
anywhere else. Estimators that grow by "one new class and nothing else" stay
correct. Estimators that grow by "one more branch in the big function" do
not.

**`super().__init__(label)` forwards only the label, because only the label is
the parent's business.** The parent's signature is `(self, label)`; the width
and the height belong to the subclass and are set after the `super()` call.

**`__repr__` uses `type(self).__name__`, not the literal `"Shape"`.** That is
why one method written in the base class prints three different class names
in line five of the output — and the `Square` you add in step 6 reports
`Square` without you writing anything.

**`Shape.area` raises rather than returning `0.0`.** A shape with no area
rule is a programming mistake, and `0.0` is a plausible number that would
slide into the total and make the estimate quietly low. `NotImplementedError`
with a sentence in it fails at the exact line that is wrong, which is the
cheapest place to find out. The base class is not being unhelpful; it is
refusing to guess.

## Run it

Copy the worked answer on this page into `exercise-03-inheritance-shapes.py` and run it:

```bash
python exercise-03-inheritance-shapes.py
```

It imports only `math` and `collections.abc`, both from the standard library.
The `Square` from step 6 is in the file but deliberately not in `panels`, so
the output matches the block above — add it to the list yourself and watch
the total move.

## Common bugs to catch

- **`AttributeError: 'Circle' object has no attribute 'label'`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 16, in <module>
      print(Circle("Clock face", 12.0).describe())
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "<string>", line 8, in describe
      return f"{self.label}: {self.area():.2f} sq cm"
                ^^^^^^^^^^
  AttributeError: 'Circle' object has no attribute 'label'
  ```

  The subclass `__init__` never called `super().__init__(label)`, so nothing
  ever set `self.label`. Note where it failed: not at construction, but later,
  at the first line that reads the missing attribute. Python creates
  attributes on assignment, so an `__init__` that forgets one raises nothing —
  the object simply goes out into the program half-built.

- **`TypeError: Shape.__init__() takes 2 positional arguments but 4 were given`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 10, in <module>
      Rectangle("Back panel", 40.0, 25.0)
      ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<string>", line 8, in __init__
      super().__init__(label, width, height)
      ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  TypeError: Shape.__init__() takes 2 positional arguments but 4 were given
  ```

  You forwarded everything. "Takes 2" counts `self`. `Shape.__init__` accepts
  a label and nothing else — pass it the label, keep the rest.

- **`TypeError: unsupported operand type(s) for +: 'int' and 'method'`.**

  ```text
    File "<string>", line 17, in total_area
      return sum(shape.area for shape in shapes)
  TypeError: unsupported operand type(s) for +: 'int' and 'method'
  ```

  Inside `total_area` you wrote `shape.area` instead of `shape.area()`. The
  `'int'` in that message is `sum`'s starting value of `0`; the `'method'` is
  the function object you handed it instead of a number. This is the mirror
  image of the `@property` bug in Exercise 2 — there a missing decorator made
  a method where a value was wanted; here a missing `()` did.

- **`TypeError: unsupported operand type(s) for ^: 'float' and 'int'`.** In
  `Circle.area` you wrote `self.radius ^ 2`. In Python `^` is bitwise XOR and
  `**` is exponentiation. The error also hides a precedence surprise: `*`
  binds tighter than `^`, so the expression was
  `(math.pi * self.radius) ^ 2`, not `math.pi * (self.radius ^ 2)`. Even had
  the types allowed it, the grouping was wrong.

- **`Clock face: 452.16 sq cm`.** You used `3.14`. Switch to `math.pi` and the
  line becomes `452.39`.

- **`Corner gusset: 540.00 sq cm`.** You forgot the `0.5` and computed a
  rectangle. The triangle is half of it.

- **The last line prints a total instead of an error.** Your `Shape.area`
  returns something — likely `0.0`, or `pass`, which returns `None`. Put the
  `raise NotImplementedError(...)` back.

- **`TypeError: Can't instantiate abstract class Shape without an
  implementation for abstract method 'area'`.** You jumped ahead and made
  `Shape` an `abc.ABC` with `@abstractmethod`. That is a good instinct and it
  is the first stretch goal, but it breaks `main()`'s last block, which
  deliberately builds a bare `Shape`.

## Under the hood

<details>
<summary>Under the hood — how Python finds a method, and what the MRO really is</summary>

When you write `circle.area()`, Python does not search the whole program. It
walks a list, in order, and stops at the first match. That list is stored on
the class and it has a name: the **method resolution order**, or MRO.

```text
>>> [cls.__name__ for cls in Circle.__mro__]
['Circle', 'Shape', 'object']
>>> [cls.__name__ for cls in Square.__mro__]
['Square', 'Rectangle', 'Shape', 'object']
```

Read that as a search path. For `circle.area`, Python checks the instance's
own dictionary first (Exercise 1's Under the hood block), then `Circle`, then
`Shape`, then `object`. `Circle` has an `area`, so the search stops there and
`Shape.area` never runs. That is what "overriding" means, mechanically:
nothing was replaced or deleted; the subclass's version simply sits earlier
in the list.

For `circle.describe`, `Circle` has nothing, so the search continues to
`Shape` and finds it. Same list, different stopping point. Inheritance is not
copying — the parent's method is found, not duplicated.

`object` is on the end of every MRO. It is where the default `__repr__` comes
from, which is why a class you write with no `__repr__` still prints
something like `<__main__.Thing object at 0x000001DC80211440>`.

Now `super()`. It is easy to read as "my parent class", and that reading is
wrong in a way that matters later. `super()` means **the next class after me
in this object's MRO**. Two consequences:

First, the MRO belongs to the *object*, not to the class the code is written
in. Watch what happens with `Square`, which inherits from `Rectangle`:

```text
>>> tile = Square("Logo tile", 20.0)
>>> [cls.__name__ for cls in type(tile).__mro__]
['Square', 'Rectangle', 'Shape', 'object']
```

`Square.__init__` calls `super().__init__(label, side, side)`. The next class
after `Square` is `Rectangle`, so that runs `Rectangle.__init__`, which
itself calls `super().__init__(label)` — and the next class after `Rectangle`
is `Shape`. One `super()` chain, three classes, and none of them had to know
how deep it went.

Second, `super()` with no arguments is doing real work. It needs to know two
things: which class the current method was written in, and which object it
was called on. Python supplies both quietly — the class through a hidden
`__class__` cell that the compiler adds whenever a method body mentions
`super`, and the object through `self`. The long form spells them out:

```text
>>> Square.__init__(tile, "Logo tile", 20.0)   # same as tile.__init__(...)
```

and inside `Rectangle`, `super().__init__(label)` is exactly
`super(Rectangle, self).__init__(label)`.

Where does the ordering come from when a class has more than one parent?
Python builds the MRO with an algorithm called **C3 linearisation**, whose
rules are: a class always comes before its parents, parents stay in the order
you wrote them, and the result must be consistent for every class involved.
When no consistent order exists, Python refuses to create the class at all:

```text
>>> class A: pass
>>> class B(A): pass
>>> class C(A, B): pass
TypeError: Cannot create a consistent method resolution order (MRO) for bases A, B
```

You will not hit that with single inheritance, which is why this exercise
sticks to it. But it is the reason `super()` is defined the way it is: with
one parent, "next in the MRO" and "my parent" are the same thing, so nothing
is lost — and with several, only the MRO version gives every class in the
diamond exactly one turn.

</details>

## Acceptance checklist

- [ ] `python exercise-03-inheritance-shapes.py` runs with no traceback.
- [ ] All six output lines match exactly.
- [ ] Every subclass `__init__` starts with `super().__init__(label)`.
- [ ] `describe()` and `__repr__` appear exactly once in the file, in
      `Shape`.
- [ ] `total_area` has no `isinstance`, no `type()`, and no `if`.
- [ ] `Square(Rectangle)` from step 6 is in the file, and adding it to
      `panels` required no change to `total_area`, `describe`, or the loop.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 3: shape hierarchy`.

## Stretch

- Convert `Shape` to an abstract base class with
  `from abc import ABC, abstractmethod`, then change `main()`'s last block to
  expect `TypeError` at construction instead of `NotImplementedError` at call
  time. Note which failure a teammate would rather get, and why earlier is
  better. Homework problem 2 builds a whole hierarchy that way.
- Add a `perimeter()` method to all three subclasses and a
  `total_edging(shapes)` function that sums it. Notice you added a second
  promise to the same family without disturbing the first.
- Add `__lt__` to `Shape` comparing `self.area() < other.area()`, then print
  `sorted(panels)[0].label`. With the numbers above, the smallest is the
  corner gusset.
- Write a `Hexagon` using the formula `1.5 * math.sqrt(3) * side ** 2` and
  confirm your estimator needs no edits at all.

When one loop handles every shape, move on to
[Exercise 4 — Dataclass User](./exercise-04-dataclass-user.md).
