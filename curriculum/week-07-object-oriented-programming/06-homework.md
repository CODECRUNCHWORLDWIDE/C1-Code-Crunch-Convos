# Week 7 — Homework

Six problems. Pick **at least four** and submit them as separate `.py` files
in a folder called `week-07-homework/` in your fork of the bootcamp repo.

Each problem is graded on:

1. **Correctness** — runs without errors; outputs match the spec.
2. **Design** — sensible attribute and method choices; good naming.
3. **Style** — type hints, docstrings, PEP 8.

---

## Problem 1 — `BankAccount` with interest

Extend the `BankAccount` from `exercise-05` with a subclass
`SavingsAccount(BankAccount)`.

- Adds a field `interest_rate: float` (e.g. `0.02` for 2% per period).
- Adds a method `apply_interest(self) -> None` that calls `deposit` with
  `balance * interest_rate`.
- Must use `super()` in `__init__`.

Demonstrate in `main()` that depositing, withdrawing, and applying interest
all interact correctly. Catch the overdraw error.

---

## Problem 2 — Polygon hierarchy

Build a `Polygon` hierarchy.

- `Polygon(ABC)` (use `abc.ABC` + `@abstractmethod`) with abstract methods
  `area() -> float` and `perimeter() -> float`.
- `Triangle(Polygon)` — three sides; validate the triangle inequality
  (`a + b > c` for every pair).
- `Rectangle(Polygon)` — width, height; `@property` `area`.
- `RegularPolygon(Polygon)` — `n_sides`, `side_length`; closed-form
  perimeter and area formulas.

In `main()`, build a list of polygons and print the **total area** by
iterating polymorphically.

---

## Problem 3 — `Stack` built on a list

Implement a `Stack` class that wraps a Python list internally and exposes:

- `push(item) -> None`
- `pop() -> Any` (raises `IndexError` on empty)
- `peek() -> Any` (raises `IndexError` on empty)
- `__len__`, `__iter__` (from top to bottom), `__repr__`.
- A property `is_empty: bool`.

Then use your `Stack` to write a function
`is_balanced(s: str) -> bool` that returns `True` iff parentheses, brackets,
and braces in `s` are balanced — `"(a+b)[i]"` is balanced; `"(a+b]"` is not.

---

## Problem 4 — Simple ORM-like model

Write a tiny base class `Model` that subclasses can extend to get a free
`to_dict()` / `from_dict()` / `__repr__`. (No real database, no `sqlite3` —
just the *shape* of an ORM.)

Suggested shape:

```python
class Model:
    """Subclasses declare their fields as class attributes with type hints
    via `__annotations__`. The base class then builds __init__, to_dict,
    from_dict, and __repr__ from those annotations.
    """
```

Then write two subclasses (e.g. `User` and `Post`) and demonstrate
round-tripping them through `json.dumps`/`json.loads` via your `to_dict` /
`from_dict`.

Hint: you can inspect `cls.__annotations__` (a `dict` of field name to
type) in `__init_subclass__` or in `__init__`.

This problem is intentionally open-ended — there is no single right answer.

---

## Problem 5 — Observer pattern (light)

Implement a tiny **observer / event** system.

- `Subject` keeps a list of observer callables.
- `Subject.subscribe(callback) -> None`
- `Subject.unsubscribe(callback) -> None`
- `Subject.notify(event: Any) -> None` calls every subscriber with the
  event.

Then build a `TemperatureSensor(Subject)` whose `set_temperature(value)`
notifies subscribers when the value changes. Wire up two observers in
`main()` — one that prints, one that records the last 5 values in a list —
and demonstrate them firing together.

This is composition, not inheritance: subscribers are just callables.

---

## Problem 6 — Unit-conversion class

Build a `Length` class that stores a value internally in metres but exposes
several units as `@property`:

- `meters`, `kilometers`, `miles`, `feet`, `inches`.

Each property has a **setter** as well, so:

```python
d = Length(meters=1000)
print(d.kilometers)   # 1.0
d.miles = 1.0
print(d.meters)       # ~1609.344
```

Include `__repr__`, `__eq__`, and support addition: `Length(meters=10) +
Length(meters=5)` must return a new `Length` of 15m. Raise `TypeError` for
`Length + 5`.

---

## Submission checklist

- [ ] Each problem in its own file (`problem-1.py`, ...).
- [ ] Type hints throughout.
- [ ] A short `if __name__ == "__main__":` demo at the bottom of each file.
- [ ] No global state apart from the demo.
- [ ] PEP 8 — your editor's auto-formatter (`black` or similar) is your
      friend.
