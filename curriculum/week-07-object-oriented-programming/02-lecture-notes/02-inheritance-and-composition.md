# Lecture 02 — Inheritance and Composition

> **Reading time:** ~40 minutes. **Prerequisites:** Lecture 01.

In lecture 01 you built single classes that stood on their own. Real systems
have *many* related classes: `Manager` and `Engineer` are both `Employee`s;
`Circle` and `Square` are both `Shape`s; a `User` *has a* `Mailbox`. This
lecture covers the two main tools for organizing those relationships:

- **Inheritance** — say "B *is a* A and gets everything A has".
- **Composition** — say "B *has a* A and uses it".

We also touch the **MRO** (the rule Python uses to resolve method calls in a
hierarchy), the **diamond problem**, **polymorphism via duck typing**, and a
preview of **abstract base classes**. By the end you should know not only the
syntax but the much more important question: *which one should I use?*

---

## 1. Inheritance: the "is-a" relationship

Inheritance lets a new class reuse the attributes and methods of an existing
class. The new class is the **subclass** (or *child*), and the existing one is
the **superclass** (or *parent*, or *base class*).

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound."


class Dog(Animal):           # Dog inherits from Animal
    def fetch(self) -> str:
        return f"{self.name} fetches the ball."


fido = Dog("Fido")
print(fido.speak())   # inherited from Animal: "Fido makes a sound."
print(fido.fetch())   # defined on Dog:        "Fido fetches the ball."
```

`Dog` did not define `__init__` or `speak`, but it has both — they were
**inherited** from `Animal`. The rule for using inheritance well is the
**is-a test**: you should be able to say "a Dog *is an* Animal" with a
straight face. If you cannot, you probably want composition (section 5).

### Overriding

A subclass can replace any inherited method by defining its own with the same
name:

```python
class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} meows."

print(Cat("Mittens").speak())   # "Mittens meows."
```

`Cat.speak` **overrides** `Animal.speak`. Lookup still starts at the most
specific class, so `Cat` wins.

---

## 2. `super()` — calling the parent

Often a subclass wants to *extend* the parent's behavior, not replace it. The
standard tool is the built-in `super()`, which gives you a proxy to the parent
class:

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name


class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)    # let Animal set self.name
        self.breed = breed        # then add what's specific to Dog


fido = Dog("Fido", "Border Collie")
print(fido.name, fido.breed)   # "Fido Border Collie"
```

Without `super().__init__(name)`, `self.name` would never be set and the next
attribute access would crash. Calling `super().__init__(...)` from a subclass
`__init__` is the most common use of `super()` you will see.

`super()` is not just for `__init__`. Anywhere you override a method you can
call the parent's version:

```python
class LoggingDog(Dog):
    def fetch(self) -> str:
        print(f"[log] {self.name} is about to fetch")
        return super().fetch() if hasattr(Dog, "fetch") else "no fetch"
```

> Until Python 3.0, `super()` required arguments: `super(Dog, self).__init__(...)`.
> The modern zero-argument form is fine in 99% of cases; the docs cover the
> rare exceptions.

---

## 3. MRO: how Python resolves method calls

Whenever you call `obj.method()`, Python looks for `method` in a specific
order called the **method resolution order**, or **MRO**. For single
inheritance, the MRO is exactly what you would guess: child → parent →
grandparent → `object`.

```python
class A: pass
class B(A): pass
class C(B): pass

print([cls.__name__ for cls in C.__mro__])
# ['C', 'B', 'A', 'object']
```

Every class ultimately inherits from `object`, which is where dunders like
`__repr__` and `__eq__` get their default implementations.

For multiple inheritance the MRO is more interesting. Python uses an algorithm
called **C3 linearization**, which guarantees three properties:

1. A class always appears before its parents.
2. The order parents are listed in the `class C(P1, P2):` line is preserved.
3. The result is *consistent* — there is exactly one MRO per class, or Python
   refuses to create the class.

You will rarely *need* to reason about the MRO manually. When you do, print
`Cls.__mro__` and read it from left to right.

---

## 4. The diamond problem (light touch)

Multiple inheritance can produce a "diamond" shape:

```text
      A
     / \
    B   C
     \ /
      D
```

`D` inherits from both `B` and `C`, which both inherit from `A`. If `B` and
`C` both override a method, which one does `D` get?

```python
class A:
    def greet(self) -> str:
        return "hello from A"

class B(A):
    def greet(self) -> str:
        return "hello from B"

class C(A):
    def greet(self) -> str:
        return "hello from C"

class D(B, C):
    pass

print(D().greet())          # "hello from B"
print([k.__name__ for k in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']
```

C3 picks `B` because it was listed first. If `D` itself overrides `greet`
and uses `super().greet()`, the call walks down the MRO: `D` → `B` → `C` → `A`.

The diamond problem is the textbook reason people preach **composition over
inheritance**. Multiple inheritance is a sharp tool — most professional
Python codebases use it only for very specific patterns (mixins, ABCs).
Beginners should keep to **single inheritance** until they have a strong
reason otherwise.

---

## 5. Composition: the "has-a" relationship

Composition is dramatically simpler: a class **holds another class as an
attribute** and delegates work to it.

```python
class Engine:
    def __init__(self, horsepower: int) -> None:
        self.horsepower = horsepower

    def start(self) -> str:
        return f"Engine ({self.horsepower}hp) starts."


class Car:
    def __init__(self, make: str, engine: Engine) -> None:
        self.make = make
        self.engine = engine          # Car HAS an Engine

    def start(self) -> str:
        return f"{self.make}: " + self.engine.start()


car = Car("Toyota", Engine(150))
print(car.start())   # "Toyota: Engine (150hp) starts."
```

A `Car` is not an `Engine`; it *has* one. Notice the benefits:

- **Loose coupling.** Replace the engine with `ElectricEngine` without
  touching `Car`'s code, as long as the new engine has a compatible `start`.
- **Easy testing.** In a unit test you can pass a fake engine that records
  calls instead of starting anything.
- **No fragile hierarchy.** Adding a `Truck`, a `Boat`, or a `Scooter` does
  not require redesigning a class tree.

### The rule of thumb

> **Use inheritance only for genuine *is-a* relationships; otherwise prefer
> composition.**

This advice is so common it has its own canonical essay (Brandon Rhodes',
linked in `resources.md`). The rough heuristic: if you find yourself
*disabling* features from a parent class (overriding methods to do nothing,
or raising `NotImplementedError`), you have probably misused inheritance —
the relationship was "has-a", not "is-a".

---

## 6. Composition + small inheritance, together

Real systems usually mix both. Here is a tiny banking example:

```python
class TransactionLog:
    def __init__(self) -> None:
        self.entries: list[tuple[str, float]] = []

    def record(self, kind: str, amount: float) -> None:
        self.entries.append((kind, amount))


class Account:
    def __init__(self, holder: str, balance: float = 0.0) -> None:
        self.holder = holder
        self.balance = balance
        self.log = TransactionLog()   # composition

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.log.record("deposit", amount)


class SavingsAccount(Account):        # inheritance: is-a
    def __init__(self, holder: str, balance: float, rate: float) -> None:
        super().__init__(holder, balance)
        self.rate = rate

    def apply_interest(self) -> None:
        interest = self.balance * self.rate
        self.deposit(interest)
```

`SavingsAccount` *is an* `Account` (inheritance), and every `Account` *has a*
`TransactionLog` (composition). Both relationships are honest; the code stays
tidy.

---

## 7. Polymorphism via duck typing

Object-oriented languages let you write code that works on **any object that
supports the right interface**. Java/C# enforce this with explicit interfaces.
Python uses **duck typing**: *"If it walks like a duck and quacks like a duck,
treat it like a duck."*

```python
class Cat:
    def speak(self) -> str:
        return "meow"

class Dog:
    def speak(self) -> str:
        return "woof"

class Duck:
    def speak(self) -> str:
        return "quack"

for animal in [Cat(), Dog(), Duck()]:
    print(animal.speak())
```

There is no shared base class. Python does not care — it only checks at call
time that the method exists. This is **ad-hoc polymorphism** and it is at the
heart of why Python feels lightweight: you do not need to plan elaborate
hierarchies just to write a loop like this.

The exercise `exercise-03-inheritance-shapes.py` makes this concrete with a
list of `Shape` objects whose `area()` methods are all called the same way.

---

## 8. Abstract base classes (preview)

Sometimes you *do* want to enforce that subclasses implement certain methods.
The standard library's `abc` module provides this:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


# Shape()    # -> TypeError: Can't instantiate abstract class
# Circle()   # -> requires both methods implemented; works if so
```

Key points:

- `Shape(ABC)` cannot itself be instantiated.
- Any subclass *must* implement every `@abstractmethod`, or it too becomes
  abstract.
- Abstract base classes are most useful when **you ship a library** and want
  to give plugin authors a precise contract.

We treat ABCs as a *preview* this week — they show up properly in Week 11
(testing) and the capstone.

---

## 9. When should I inherit, and when should I compose?

A practical checklist. Choose **inheritance** when **all** of these are true:

- The relationship is a clear "B is a kind of A".
- B reuses most of A's behavior.
- B never needs to *remove* behavior from A.
- A's API is stable; you control it (or it is a well-documented library).

Choose **composition** when **any** of these are true:

- The relationship is "B has an A".
- B uses only a small part of A's behavior.
- You want to swap one A for another at runtime.
- You want to combine behavior from multiple unrelated places.
- You are tempted to reach for multiple inheritance.

When in doubt, **start with composition**. Inheritance is easy to add later
and very painful to remove.

---

## 10. A worked refactor: from bad inheritance to good composition

You will see the antipattern below in many real codebases. It looks fine
until requirements change.

```python
# version 1: inheritance
class List:
    def __init__(self) -> None:
        self.items: list = []
    def add(self, x) -> None:
        self.items.append(x)

class CountedList(List):              # "is-a list that counts adds"
    def __init__(self) -> None:
        super().__init__()
        self.count = 0
    def add(self, x) -> None:
        super().add(x)
        self.count += 1
```

It works. But now your boss says: "Also support a *deduplicating* list, and a
*logging* list, and a list that does both." You quickly end up with
`CountedDedupLoggingList(CountedList, DedupList, LoggingList)` and a tangled
diamond.

Composition rewrites the problem cleanly:

```python
# version 2: composition (Strategy pattern, lightweight)
class Counter:
    def __init__(self) -> None:
        self.value = 0
    def increment(self) -> None:
        self.value += 1

class TrackedList:
    def __init__(self, on_add=None) -> None:
        self.items: list = []
        self.on_add = on_add          # any callable: counter, logger, dedup

    def add(self, x) -> None:
        if self.on_add is not None:
            self.on_add(x)
        self.items.append(x)


counter = Counter()
tracked = TrackedList(on_add=lambda x: counter.increment())
tracked.add("a"); tracked.add("b")
print(counter.value)   # 2
```

Different behaviors are now small, independent objects you can mix and match.
Nothing inherits from anything; the diamond is impossible by construction.

This pattern — passing a small object that customizes behavior — is called
**Strategy**. It is the canonical example of "composition replacing
inheritance".

---

## 11. Recap

- Inheritance models **is-a**; composition models **has-a**.
- Use `super()` to call the parent class — especially from `__init__`.
- Every class has an **MRO**; `Cls.__mro__` shows it.
- The **diamond problem** is one reason to avoid multiple inheritance.
- **Duck typing** gives you polymorphism without shared base classes.
- **Abstract base classes** (`abc`) let you enforce interfaces when you need
  to.
- **Prefer composition** by default. Reach for inheritance only when the
  is-a relationship is undeniable.

**Next lecture:** dataclasses, dunder methods, properties, classmethods and
staticmethods, and encapsulation conventions.
