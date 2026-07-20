# Week 7 — Quiz

10 multiple-choice questions. Answer each before scrolling to the answer
key at the bottom. Aim for **8 out of 10** before moving on to Week 8.

---

### 1. What does `__init__` do?

A. It allocates memory for a new object.
B. It runs *after* a new instance has been created, to set it up.
C. It is a static method that returns a new object.
D. It is only required when you inherit from another class.

---

### 2. Inside a method, what is `self`?

A. A keyword reserved by Python.
B. The class object itself.
C. The current instance — Python passes it automatically when you call
   `obj.method()`.
D. The first argument the caller wrote in parentheses.

---

### 3. Which of the following is a **class attribute** (not an instance
attribute)?

```python
class Dog:
    species = "Canis familiaris"

    def __init__(self, name):
        self.name = name
```

A. `species`
B. `name`
C. Both.
D. Neither — they are both local variables.

---

### 4. Why is `tricks = []` directly in the class body usually a bug?

A. Empty lists are not allowed at the class level.
B. The same list is shared by every instance, so mutations leak across
   them.
C. Python silently turns it into a tuple.
D. `[]` is not a valid default in Python.

---

### 5. What is the difference between `__repr__` and `__str__`?

A. They are aliases — Python picks one at random.
B. `__repr__` is for end users; `__str__` is for developers.
C. `__repr__` is for developers (unambiguous); `__str__` is for end users
   (readable). If `__str__` is missing, Python falls back to `__repr__`.
D. `__str__` must return bytes; `__repr__` must return a string.

---

### 6. Given:

```python
class A:
    def greet(self): return "A"
class B(A):
    def greet(self): return "B"
class C(A):
    def greet(self): return "C"
class D(B, C):
    pass

print(D().greet())
```

What is printed?

A. `"A"`
B. `"B"`
C. `"C"`
D. `TypeError` — the class cannot be created.

---

### 7. The phrase "**composition over inheritance**" means:

A. Always inherit from at least two classes.
B. Prefer modeling "has-a" with attributes over modeling "is-a" with
   subclassing — inheritance is for genuine "is-a" relationships only.
C. Replace every `class` with a function.
D. Inheritance was removed in Python 3.

---

### 8. Which decorator turns a method into an **alternative constructor**?

A. `@property`
B. `@staticmethod`
C. `@classmethod`
D. `@dataclass`

---

### 9. What does this code print?

```python
from dataclasses import dataclass

@dataclass
class P:
    x: int
    y: int

a = P(1, 2)
b = P(1, 2)
print(a == b)
```

A. `True` — `@dataclass` generates `__eq__`.
B. `False` — different objects always compare unequal in Python.
C. `True`, but only because integers are interned.
D. `TypeError` — dataclasses do not define `==`.

---

### 10. What does the name-mangled attribute `self.__balance` become inside
a class called `Account`?

A. `self._balance` (single underscore).
B. `self.__balance` exactly — no mangling for regular code.
C. `self._Account__balance`.
D. It is a private keyword and cannot be set on instances.

---

## Answer key

1. **B** — `__init__` is the *initializer*. Allocation is `__new__`'s job;
   you almost never override `__new__`.
2. **C** — `self` is the current instance, passed implicitly. It is a
   convention, not a keyword.
3. **A** — `species` is defined in the class body and shared by all
   instances. `name` is per-instance because it is set on `self`.
4. **B** — mutable class attributes are shared. Use
   `__init__(self): self.tricks = []` or
   `field(default_factory=list)` in a dataclass.
5. **C** — Always implement `__repr__`; add `__str__` only when the
   user-facing form differs.
6. **B** — The MRO is `D → B → C → A → object`. `B.greet` is found first.
7. **B** — Use inheritance only for true "is-a" relationships; otherwise
   compose.
8. **C** — `@classmethod` receives `cls`, so it can construct instances of
   the right (possibly subclassed) type.
9. **A** — `@dataclass` generates `__eq__` from the fields by default.
10. **C** — Name-mangling rewrites `__name` to `_ClassName__name` inside
    the class body, to avoid collisions with subclasses.

---

**Score yourself:** 9–10 ready for Week 8 / 7–8 review the lecture where
you missed / under 7 redo the exercises *and* re-read lecture 01.
