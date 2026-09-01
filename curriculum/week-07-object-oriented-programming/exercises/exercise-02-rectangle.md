# Exercise 2 — Rectangle

> **Topic:** `@property`, values that are worked out instead of stored, and checking a value the moment it arrives
> **Lecture:** [01 — Classes and Instances](../lecture-notes/01-classes-and-instances.md)
> **Also read:** [03 — Dataclasses, Dunder Methods, and Friends](../lecture-notes/03-dataclasses-and-magic-methods.md), section 3, which is where `@property` is taught in full
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** worked-out values are everywhere — an area, a total, a balance, a percentage done. The tempting move is to work one out in `__init__` and store it. That is fine right up until somebody changes an input, and then your object confidently reports a number that stopped being true. `@property` is how Python lets a value stay worked-out while still reading like a plain attribute.

## The Brief

A sign shop quotes jobs by area. Somebody hands you a `Rectangle` class the
last intern wrote. It takes a width and a height, and it stores
`self.area = width * height` in `__init__`. It has already produced one wrong
invoice: a customer resized a poster from 90 by 60 to 60 by 60, and the quote
still said 5400 square centimetres.

Think about what went wrong. The object was holding **three** facts — width,
height, and area — but only two of them are independent. The third is just
the first two multiplied. The moment one changed on its own, the object held
two answers to the same question and no way to tell which was current.

The fix is to stop storing the answer and start working it out on the spot.
Every time somebody asks for the area, multiply. It costs one multiplication
and it can never be stale, because there is nothing to go stale.

Python gives you a way to do that without changing a single call site. It is
called a **property**: a method that you read like a plain attribute. Write
`rect.area` with no parentheses, and behind it a small function runs. The
code that reads it never has to know.

While you are in there, make `width` and `height` refuse nonsense at the
moment of assignment, rather than letting a negative number travel three
functions before it explodes.

Dimensions are in centimetres throughout. The shop does not care about units
in the code, but you should — a class that mixes centimetres and inches is a
bug waiting for a customer.

## Starter

Create `exercise-02-rectangle.py` and fill in the `TODO` markers:

```python
"""exercise-02-rectangle.py — derived values that cannot go stale.

Quotes sign-shop panels by area. Run it with:

    python exercise-02-rectangle.py
"""


def require_positive(label: str, value: float) -> float:
    """Return `value` if it is greater than zero, else raise ValueError.

    The message reads `width must be positive, got -5.0`.
    """
    # TODO: raise ValueError(f"{label} must be positive, got {value}") when
    # value is not greater than zero; otherwise return value
    raise NotImplementedError


class Rectangle:
    """A rectangular panel measured in centimetres."""

    def __init__(self, width: float, height: float) -> None:
        """Set width and height *through the properties* so both are checked."""
        self.width = width
        self.height = height

    @property
    def width(self) -> float:
        """The panel's width in centimetres."""
        # TODO: return the private field
        raise NotImplementedError

    @width.setter
    def width(self, value: float) -> None:
        """Validate, then store the width."""
        # TODO: self._width = require_positive("width", value)

    @property
    def height(self) -> float:
        """The panel's height in centimetres."""
        # TODO
        raise NotImplementedError

    @height.setter
    def height(self, value: float) -> None:
        """Validate, then store the height."""
        # TODO

    @property
    def area(self) -> float:
        """Width times height, computed fresh on every access."""
        # TODO
        raise NotImplementedError

    @property
    def perimeter(self) -> float:
        """Twice the sum of the two sides."""
        # TODO
        raise NotImplementedError

    @property
    def is_square(self) -> bool:
        """True when the two sides are equal."""
        # TODO
        raise NotImplementedError

    def __repr__(self) -> str:
        """Developer form, e.g. `Rectangle(width=90.0, height=60.0)`."""
        # TODO
        raise NotImplementedError


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
```

Three pieces of that starter are new, so here they are before you begin.

**`@property` above a method** turns it into something you read without
parentheses. `rect.area` runs the method and hands you what it returned.
That method is called the **getter**.

**`@width.setter` above a second method with the same name** says what should
happen when somebody *assigns* to it. `rect.width = 60.0` runs that method
with `60.0` as `value`. That method is called the **setter**. A property with
a getter and no setter is read-only, and Python enforces that for you.

**`_width` with one leading underscore** is where the real number lives. The
underscore means two things at once. To a reader it means "internal, do not
poke at this from outside". To Python it means a completely different
attribute from `width`, which is what stops the setter from calling itself
forever.

## Requirements

1. `require_positive` raises `ValueError` for zero and for anything negative,
   with the message `<label> must be positive, got <value>`. Zero is not
   positive — a panel with no height is not a panel.
2. `width` and `height` are read/write properties backed by `self._width` and
   `self._height`. Both setters run the value through `require_positive`.
3. `area`, `perimeter`, and `is_square` are **read-only** properties. They
   have getters and no setters.
4. Nothing is cached. `area` recomputes from `self._width` and `self._height`
   every single time it is read.
5. `__repr__` returns `Rectangle(width=90.0, height=60.0)`.
6. `__init__` assigns to `self.width`, not `self._width`, so construction
   goes through the same check as any later assignment. Do not change those
   two lines.
7. Do not edit `report()` or `main()`. They are the test.

## Constraints

- **Store the real values in `_width` and `_height`, with one leading
  underscore.** If the property is named `width` and its setter also stores
  into `self.width`, that assignment goes straight back through the setter,
  which assigns again, forever. `_width` is a different attribute with no
  property watching it, which is what breaks the loop.
- **`area` must be a property, not a method.** The call site in `report()` is
  `rect.area` with no parentheses. Define it as a plain method and that
  expression is the function object itself, and `:.2f` will have nothing
  numeric to format. Read the call site before you choose the shape of the
  thing being called.
- **Do not add a setter for `area`.** There is no sensible answer to "set the
  area to 5000" — which side moved? Read-only is the honest description, and
  Python enforces it for you the moment you leave the setter out.
- **`is_square` may compare the two sides with `==` here**, because both
  numbers came straight from the caller and were never put through
  arithmetic. Be aware that this is the exception, not the rule. Once a
  decimal number has been through a calculation, `==` stops being
  trustworthy — `0.1 + 0.2` is not `0.3` in binary — and `math.isclose(a, b)`
  is the comparison you want. You meet that problem for real in Exercise 5.
- **Validate in the setter, not in `report()`.** Checking at the boundary
  means an invalid `Rectangle` cannot exist at all. Checking in the reporting
  code means it can exist, travel through three more functions, and surface
  somewhere with no useful clue about where it came from.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-rectangle-solution.py
Rectangle(width=90.0, height=60.0)
  area      : 5400.00 sq cm
  perimeter : 300.00 cm
  square?   : no
Rectangle(width=60.0, height=60.0)
  area      : 3600.00 sq cm
  perimeter : 240.00 cm
  square?   : yes
Rejected: width must be positive, got -5.0
Rejected: height must be positive, got 0
```

The second block is the whole exercise. One attribute was assigned, and all
three worked-out values followed. The intern's cached version would still
print `5400.00` on line six.

The two rejections show the two different value types unchanged in the
message. `-5.0` arrived as a decimal and `0` as a whole number, and the
f-string prints each one exactly as it was given.

## Steps

1. Create the file and run it. The first failure comes from
   `require_positive`, because `__init__` calls the setter immediately.
2. Implement `require_positive` and test it on its own in the REPL:
   `require_positive("width", 3)` returns `3`, and
   `require_positive("width", 0)` raises.
3. Implement the `width` getter and setter. Run again and watch the remaining
   `NotImplementedError`s move down the file — that is a useful progress bar.
4. Implement `height`, then the three read-only properties, then `__repr__`.
5. Compare your output to the block above line by line, including the two
   spaces of indentation on the derived lines.
6. Prove nothing is cached. In the REPL:
   `r = Rectangle(2, 3); r.area` gives `6`, then `r.height = 10; r.area`
   gives `20` with no other call in between.
7. Prove `area` is read-only: `r.area = 99` should raise. Read the message
   carefully — Python tells you exactly what is missing.

## The Solution

```python
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
```

**There are exactly two facts in this object: `_width` and `_height`.
Everything else is arithmetic.** A property is not extra machinery bolted on
for elegance. It is how you make the arithmetic run at read time rather than
at write time, so the wrong answer never gets a chance to exist. The invoice
bug in the brief is not "the intern forgot to update `area`". It is that a
design existed in which `area` *could* need updating.

**The single leading underscore is what stops the setter from calling
itself.** `self.width = value` inside the `width` setter is not a plain
assignment. `width` is a property, so any assignment to `self.width` goes
through the setter — including the one inside the setter. Storing into
`self._width` works because `_width` is an ordinary attribute with no
property watching it. That is the whole trick, and the `RecursionError`
people hit here is Python correctly reporting that they asked for infinity.

**`__init__` assigns to `self.width`, not `self._width`, and that is
deliberate.** It means construction and later assignment take the identical
path through the same check. If `__init__` wrote straight to `_width`, you
would have two ways to set a width and only one of them checked — exactly the
sort of asymmetry that lets an invalid object exist for the twenty minutes it
takes to reach the code that breaks on it. Checking at the boundary means a
`Rectangle` that exists is a `Rectangle` that is valid, everywhere, forever,
with no defensive checks needed downstream.

**`require_positive` is a free function, not a method, because it does not
need the rectangle.** It takes a label and a value and returns a value. That
makes it testable in one REPL line, reusable by the `scale` stretch goal, and
honest about what it depends on. When a helper never touches `self`, taking
`self` anyway is a small lie about what the code needs.

**The guard is `value <= 0`, not `value < 0`.** Zero is the case that catches
people, because "positive" reads like "not negative" until you think about
it. A panel with no height is not a very small panel; it is not a panel. The
demo's second rejection exists precisely to make you get this right.

**`area` and friends have getters and no setters, and Python turns that into
enforcement for free.** Leaving the setter out means an assignment raises
instead of silently doing something arbitrary. Read-only is not a limitation
here; it is the accurate description of the value.

## Download and run

Download
[exercise-02-rectangle-solution.py](./exercise-02-rectangle-solution.py)
and run it:

```bash
python exercise-02-rectangle-solution.py
```

It needs no setup and imports nothing. The `-solution` in the name keeps it
from colliding with your own `exercise-02-rectangle.py`.

## Common bugs to catch

- **`RecursionError: maximum recursion depth exceeded`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 13, in <module>
      Rectangle(90.0, 60.0)
      ~~~~~~~~~^^^^^^^^^^^^
    File "<string>", line 4, in __init__
      self.width = width
      ^^^^^^^^^^
    File "<string>", line 11, in width
      self.width = value
      ^^^^^^^^^^
    File "<string>", line 11, in width
      self.width = value
      ^^^^^^^^^^
    [Previous line repeated 995 more times]
  RecursionError: maximum recursion depth exceeded
  ```

  Your setter body is `self.width = value`. The repeated frame names the
  culprit line for you. Change the body to
  `self._width = require_positive("width", value)`.

- **`TypeError: unsupported format string passed to method.__format__`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 10, in <module>
      print(f"  area      : {rect.area:.2f} sq cm")
                            ^^^^^^^^^^^^^^^
  TypeError: unsupported format string passed to method.__format__
  ```

  `report()` writes `rect.area` with no parentheses, so without `@property`
  that expression is the function object itself, and `:.2f` has nothing
  numeric to format. Put the `@property` line back above `def area`.

- **`AttributeError: 'Rectangle' object has no attribute '_width'`.** The
  getter reads `self._width` but the setter stored something else — usually
  `self.__width` (two underscores, which Python renames to
  `_Rectangle__width`) or a plain local `width` with no `self.` on it.

- **`AttributeError: property 'area' of 'Rectangle' object has no setter`.**
  Something assigned to `area`. That is the error working as intended — find
  the assignment and delete it.

- **The second block still prints `5400.00`.**

  ```text
    area      : 5400.00 sq cm
    area      : 5400.00 sq cm
  ```

  This is the intern's bug, reproduced. You cached the area in `__init__`.
  The poster was resized to 60 by 60 between those two lines and the quote
  did not move. Nothing raised, nothing warned, and the customer was invoiced
  for half a square metre they did not buy. Delete the stored value; the
  property must recompute.

- **`Rejected: height must be positive, got 0` never prints.** Your check is
  `if value < 0`, and zero passes that test:

  ```text
  >>> require_positive("height", 0)
  0
  ```

  No exception, and a zero-height panel quotes at zero square centimetres
  instead of being refused. The rule is "greater than zero", so the guard is
  `if value <= 0`.

- **`ValueError` is raised but the program stops anyway.** You used
  `raise ValueError` with no parentheses and no message, or you raised it
  somewhere `main()` does not guard. Include the message — `Rejected: ` with
  nothing after it helps nobody.

## Under the hood

<details>
<summary>Under the hood — what @property replaces, and why a public attribute is hard to take back</summary>

Start with the version that has no properties at all:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
```

There is nothing wrong with that. It is the right amount of code for the job
it does. The question is what happens when the job changes.

Suppose six months later you need widths to be checked. In a language where
fields are fields, `rect.width` is a raw memory read and there is no place to
put a check — so those languages tell you to write `getWidth()` and
`setWidth()` on day one, for every field, just in case. That is why so much
Java looks the way it does.

Python does not need that, because `rect.width` is not a raw read. It is an
**attribute lookup**, and attribute lookup is a thing you can intercept. A
property is the interception:

```text
>>> Rectangle.width
<property object at 0x0000023E0A5A4D60>
>>> Rectangle.width.fget
<function Rectangle.width at 0x0000023E0A5B2340>
>>> Rectangle.width.fset
<function Rectangle.width at 0x0000023E0A5B23E0>
```

`Rectangle.width` is not a number. It is an object holding up to three
functions — `fget`, `fset`, `fdel` — and it lives on the **class**, not on
the instance. When Python looks up `rect.width` it finds that object on the
class, notices it knows how to be got, and calls `fget(rect)`. When you
assign, it calls `fset(rect, value)`. Leave `fset` as `None` and the
assignment raises. That is the whole mechanism, and it is called the
**descriptor protocol**.

The practical consequence is the one that matters: **you can start with a
plain attribute and add a property later without changing a single line of
calling code.** `rect.width` reads the same either way. Nobody who uses your
class has to know it changed. That is why "write getters and setters just in
case" is bad advice in Python — the "just in case" already works.

The reverse is not true, and this is the part worth remembering. Once
`_width` is public as `width`, taking it back is a breaking change. Every
caller doing `rect.width = -5` keeps working, and if you later add the check,
their code starts raising. The underscore is how you say, up front, "this one
is mine". It buys nothing from Python — `rect._width = -5` works fine — but
it moves the conversation from "you broke my code" to "you were poking at
something marked private".

Two more properties in the standard library are worth meeting now:

- **`functools.cached_property`** computes once and stores the answer on the
  instance, so later reads are free. That is the *right* tool when the input
  never changes and the computation is expensive, and exactly the *wrong*
  tool here — it reintroduces the intern's bug on purpose. The third stretch
  goal asks you to try it and write down why.
- **`@width.deleter`** handles `del rect.width`. You will rarely want it, but
  it is the third slot on the property object, and now you know what `fdel`
  is for.

</details>

## Acceptance checklist

- [ ] `python exercise-02-rectangle.py` runs with no traceback.
- [ ] All ten output lines match exactly.
- [ ] `area`, `perimeter`, and `is_square` are properties with no setters.
- [ ] No derived value is stored anywhere.
- [ ] `Rectangle(0, 5)` raises `ValueError` at construction time.
- [ ] Assigning to `rect.area` raises `AttributeError`.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 2: Rectangle properties`.

## Stretch

- Add a `scale(self, factor: float) -> None` method that multiplies both
  sides. Validate the factor with the same `require_positive` helper, and
  confirm the derived values follow with no extra work.
- Add a `diagonal` property using `math.hypot(self._width, self._height)`.
  For 90 by 60 it is about `108.17`. Check it against
  `math.sqrt(90**2 + 60**2)` and note that `hypot` is the one that will not
  overflow on huge inputs.
- Convert `area` to `functools.cached_property` and then write a short
  comment explaining why that is the wrong choice for this class. The answer
  is in the first paragraph of the brief.

When your panel quotes correctly, move on to
[Exercise 3 — Inheritance and Shapes](./exercise-03-inheritance-shapes.md).
