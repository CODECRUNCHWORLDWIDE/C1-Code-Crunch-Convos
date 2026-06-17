# Lecture 03 — Dataclasses, Dunder Methods, and Friends

> **Reading time:** ~35 minutes. **Prerequisites:** Lectures 01 and 02.

You now know how to define classes, instantiate them, and arrange them into
hierarchies. This lecture is about the **everyday tools** that turn a class
from "works" into "good Python". We cover:

- The `dataclasses` module (less boilerplate, more correctness).
- The most-used **dunder methods**: `__eq__`, `__lt__`, `__len__`, `__iter__`.
- **`@property`** for computed attributes that look like fields.
- **`@classmethod`** and **`@staticmethod`** — when each is the right tool.
- Python's **encapsulation conventions**: `_protected`, `__private`, and
  name-mangling.

---

## 1. The `dataclasses` module

Most classes you will ever write are "data holders" — a handful of fields, an
`__init__`, `__repr__`, and `__eq__`. Writing that by hand is tedious:

```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)
```

The `@dataclass` decorator (Python 3.7+) generates all of that for you:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

You get `__init__`, `__repr__`, and `__eq__` for free. The class also looks
like its own documentation — the field list at the top is exactly the shape
of an instance.

```python
a = Point(1.0, 2.0)
b = Point(1.0, 2.0)
print(a)        # Point(x=1.0, y=2.0)
print(a == b)   # True
```

### Defaults and `field()`

Simple defaults work just like function defaults:

```python
@dataclass
class Player:
    name: str
    score: int = 0
    level: int = 1
```

For mutable defaults you **must** use `field(default_factory=...)` — exactly
the same reason `tricks = []` was dangerous in lecture 01:

```python
from dataclasses import dataclass, field

@dataclass
class Inventory:
    items: list[str] = field(default_factory=list)   # one list per instance
```

`default_factory` takes a zero-argument callable. `list`, `dict`, and `set`
are all callable and produce empty collections, which is what you usually
want.

### `frozen=True` — immutable instances

`@dataclass(frozen=True)` makes the resulting object **immutable**. Attempts
to assign to fields raise `FrozenInstanceError`:

```python
@dataclass(frozen=True)
class Money:
    amount: int
    currency: str

m = Money(100, "USD")
# m.amount = 200    # -> dataclasses.FrozenInstanceError
```

Frozen dataclasses are also **hashable** by default, which means you can put
them in sets and use them as dictionary keys — extremely useful for value
objects like coordinates, money, or units.

### Other useful flags

- `order=True` generates `__lt__`, `__le__`, `__gt__`, `__ge__` based on the
  tuple of fields. Combined with `frozen=True`, you get a fully-ordered,
  hashable value type with one decorator.
- `slots=True` (Python 3.10+) generates `__slots__`, which saves memory.
- `kw_only=True` makes every field keyword-only at construction time —
  great when you have many optional fields.

See the [`dataclasses` docs](https://docs.python.org/3/library/dataclasses.html)
for the full set of options.

### `__post_init__`

For validation or derived fields, define `__post_init__`:

```python
@dataclass
class Rectangle:
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("dimensions must be positive")
```

`__post_init__` runs at the end of the generated `__init__`. It is the
canonical place for "is this object even valid?" checks.

---

## 2. Dunder methods — making your class feel built-in

Dunder ("double underscore") methods are the hook Python uses to make
operators and built-in functions work on your objects. There are dozens; we
cover the four you will use most.

### `__eq__` — equality

```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))
```

Two rules to remember:

1. Return **`NotImplemented`** (not `False`) when the other operand is not a
   compatible type. This lets Python try the reflected operation on the other
   object.
2. If you implement `__eq__`, you must also implement `__hash__` if you want
   instances to live in sets or dict keys. Or set `__hash__ = None` if your
   objects should be unhashable.

Dataclasses generate both correctly when you ask them to.

### `__lt__` — less-than (and ordering)

```python
class Card:
    def __init__(self, rank: int, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def __lt__(self, other: "Card") -> bool:
        return self.rank < other.rank
```

Implement `__lt__` and you can call `sorted()` on a list of `Card`s. If you
want all six comparisons (`<`, `<=`, `>`, `>=`, `==`, `!=`) consistent, use
`functools.total_ordering`:

```python
from functools import total_ordering

@total_ordering
class Card:
    def __init__(self, rank: int, suit: str) -> None:
        self.rank, self.suit = rank, suit

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Card) and self.rank == other.rank

    def __lt__(self, other: "Card") -> bool:
        return self.rank < other.rank
```

You write `__eq__` and `__lt__`; `total_ordering` fills in the rest.

### `__len__` — the `len()` function

```python
class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def __len__(self) -> int:
        return len(self.cards)
```

Now `len(my_deck)` works. `__len__` must return a non-negative integer.
Anything that has a meaningful "number of items" — collections, queues,
hands, decks, libraries — should implement `__len__`.

### `__iter__` — the `for x in ...` protocol

```python
class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def __iter__(self):
        return iter(self.cards)
```

Returning `iter(self.cards)` is the simplest implementation: delegate to the
underlying list. Once you have `__iter__`, every `for`/`in` construct works
on your object:

```python
for card in deck:
    print(card)

if some_card in deck:   # Python uses __iter__ when there is no __contains__
    print("found it")

ranks = [c.rank for c in deck]   # list comprehensions work too
```

For more advanced cases (lazy streams, infinite sequences) define your own
generator with `yield` inside `__iter__`.

The **full** list of dunders is in the
[Data model](https://docs.python.org/3/reference/datamodel.html). Skim it
once; bookmark it forever.

---

## 3. `@property` — computed attributes that look like fields

Sometimes you want a value that **looks like an attribute** to the caller but
is **computed** behind the scenes:

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        return self.width * self.height
```

Notice the call site:

```python
r = Rectangle(3, 4)
print(r.area)     # 12  -- no parentheses; reads like a field
```

`@property` turns the method `area` into something Python computes on every
access. Use it when:

- The value is **derived** from existing attributes.
- It is **cheap** to compute (otherwise add caching with
  `functools.cached_property`).
- The caller does **not** need to set it directly.

You can also define a **setter** if assignment makes sense:

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self._celsius = (value - 32) * 5 / 9
```

Now `t.fahrenheit = 100` updates the underlying `_celsius`. Properties shine
for **validation on write** — you can reject bad values before they touch
your data.

> **Beginner trap.** Do not overuse properties. If a value is a plain
> attribute, leave it plain. Reach for `@property` only when you actually
> want computation, validation, or read-only semantics.

---

## 4. `@classmethod` and `@staticmethod`

A regular method takes `self` — the instance. The two decorators below change
what (if anything) Python passes as the first argument.

### `@classmethod` — takes the class, often used for alternative constructors

```python
from datetime import date
from dataclasses import dataclass

@dataclass
class User:
    name: str
    birthday: date

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(name=data["name"], birthday=date.fromisoformat(data["birthday"]))


u = User.from_dict({"name": "Ada", "birthday": "1815-12-10"})
```

`cls` is the class itself — so subclasses calling `from_dict` correctly
build instances of the subclass, not of `User`. Classmethods are the
idiomatic way to provide **alternative constructors** (`from_json`,
`from_csv`, `from_dict`).

### `@staticmethod` — takes nothing automatic

A staticmethod is just a function that happens to live inside a class. It
gets no `self` and no `cls`:

```python
class Math:
    @staticmethod
    def clamp(value: float, low: float, high: float) -> float:
        return max(low, min(value, high))


Math.clamp(15, 0, 10)   # 10
```

Use a `@staticmethod` when a helper is **conceptually related** to the class
but does not need the instance or the class itself. If a function has neither
`self` nor `cls` *and* nothing meaningful to do with the class, just write a
plain module-level function — that is usually clearer.

### Quick comparison

| Decorator         | First arg | Sees instance? | Sees class? | Typical use                |
|-------------------|-----------|----------------|-------------|----------------------------|
| (none)            | `self`    | yes            | yes         | normal method              |
| `@classmethod`    | `cls`     | no             | yes         | alternative constructor    |
| `@staticmethod`   | none      | no             | no          | utility tied to the class  |

---

## 5. Encapsulation conventions

Python has **no enforced private attributes**. Instead it relies on
*conventions*. There are three levels.

### `public_name`

No leading underscore. This is the documented, supported API. Other code is
welcome to read and write it.

### `_protected_name`

Single leading underscore. By convention this means **"intended for internal
use; touch at your own risk"**. Python does **not** stop you, but linters,
auto-importers, and other humans will give you side-eye if you reach into it
from outside.

```python
class Account:
    def __init__(self, balance: float) -> None:
        self._balance = balance   # not part of the public API

    @property
    def balance(self) -> float:
        return self._balance
```

### `__double_underscore_name` — name-mangling

If a name **starts with two underscores and does not end with two**, Python
applies **name-mangling**: inside the class body, `self.__x` is rewritten as
`self._ClassName__x`. This makes accidental collisions in subclasses very
unlikely:

```python
class Base:
    def __init__(self) -> None:
        self.__secret = 42       # becomes _Base__secret

class Sub(Base):
    def __init__(self) -> None:
        super().__init__()
        self.__secret = "hi"     # becomes _Sub__secret (different name!)


b = Base()
print(b._Base__secret)           # 42   -- still reachable, just renamed
```

Name-mangling is **not** security. It is collision avoidance, mainly inside
class hierarchies. Use it sparingly — `_single_underscore` is enough 95% of
the time, and `__double` is mostly reserved for the rare case where a parent
class has a field name a subclass might shadow by accident.

> **Never** use `__double__` (dunder) names for your own attributes. Those
> are reserved for Python itself.

---

## 6. Bringing it together: a small but realistic class

Below is a `Book` class you will recognize from the mini-project. It uses
nearly everything in this lecture:

```python
from dataclasses import dataclass, field
from datetime import date

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    copies_total: int = 1
    _copies_loaned: int = field(default=0, repr=False)

    def __post_init__(self) -> None:
        if self.copies_total < 1:
            raise ValueError("a book needs at least one copy")

    @property
    def copies_available(self) -> int:
        return self.copies_total - self._copies_loaned

    def loan_one(self) -> None:
        if self.copies_available == 0:
            raise ValueError(f"no copies of {self.title!r} available")
        self._copies_loaned += 1

    def return_one(self) -> None:
        if self._copies_loaned == 0:
            raise ValueError("no copies are loaned out")
        self._copies_loaned -= 1

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            copies_total=data.get("copies_total", 1),
        )

    def __str__(self) -> str:
        return f"{self.title!r} by {self.author} ({self.copies_available}/{self.copies_total} available)"
```

What is going on:

- A **dataclass** with field defaults and a `_protected` field for the loaned
  count.
- `__post_init__` for **validation**.
- A **`@property`** for `copies_available`, which depends on two other fields.
- Two plain **methods** that mutate state.
- A **`@classmethod`** alternative constructor used to load from JSON later.
- A custom **`__str__`** that overrides the dataclass-generated repr for
  display.

That is most of the OOP vocabulary you need to ship real Python code.

---

## 7. Recap

- `@dataclass` removes the boilerplate of `__init__`, `__repr__`, and
  `__eq__`. Use `default_factory` for mutable defaults. `frozen=True` gives
  you immutable, hashable value objects.
- Implement `__eq__`, `__lt__`, `__len__`, `__iter__` to make your classes
  feel built-in. Return `NotImplemented` for incompatible types.
- `@property` exposes a method as a read-only (or read/write) attribute —
  perfect for derived values and validated setters.
- `@classmethod` for alternative constructors; `@staticmethod` for related
  utilities; plain methods otherwise.
- Underscore conventions: `_protected` is a soft signal; `__private` is
  name-mangling, not security; never invent your own dunders.

You now have the full OOP toolkit. The mini-project at the end of this week
puts every piece of it to work in one realistic system.
