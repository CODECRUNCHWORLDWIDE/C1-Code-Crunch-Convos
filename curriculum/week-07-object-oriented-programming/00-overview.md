# Week 7 — Object-Oriented Programming

Welcome to Week 7 of **Code Crunch Convos**. Up until now you have written Python
as collections of values, functions, and modules. This week you learn to bundle
**state** (data) and **behavior** (functions) together using **classes**. This
mental model — *objects that know things and can do things* — is the foundation
of almost every large Python program you will ever read.

By the end of the week you will refactor your earlier file-handling code from
Week 6 into a clean, testable **Library management system** built from `Book`,
`Member`, and `Library` classes, with JSON save/load.

---

## Learning objectives

After this week you will be able to:

1. Explain what a **class**, an **instance**, an **attribute**, and a **method**
   are, and why OOP is useful for managing related state and behavior.
2. Define classes with `__init__`, `self`, instance attributes, and class
   attributes — and tell those two apart.
3. Implement `__repr__` and `__str__` and explain which is for *developers* and
   which is for *end users*.
4. Use **inheritance** with `super()` and read a class's **MRO**
   (`ClassName.__mro__`).
5. Choose **composition over inheritance** for "has-a" relationships, and use
   inheritance only for genuine "is-a" relationships.
6. Use `@classmethod`, `@staticmethod`, and `@property` correctly.
7. Reduce boilerplate with the **`dataclasses`** module, including `frozen=True`
   and default factories.
8. Write common **dunder methods** (`__eq__`, `__lt__`, `__len__`, `__iter__`)
   to make your classes behave like built-in types.
9. Follow Python's **encapsulation conventions** (`_protected`, `__private`,
   name-mangling) and know they are conventions, not enforcement.
10. Decide when a problem is better solved with simple functions and when OOP
    earns its weight.

---

## Prerequisites

You should be comfortable with everything from Weeks 1–6:

- **Week 1** — variables, the REPL, running scripts.
- **Week 2** — data types, operators, type conversion.
- **Week 3** — `if`/`elif`/`else`, `for` and `while` loops.
- **Week 4** — defining functions, default arguments, keyword arguments, imports.
- **Week 5** — lists, tuples, dictionaries, sets, comprehensions.
- **Week 6** — reading and writing files, JSON, `try`/`except`, context managers.

If any of those feels shaky, revisit that week's exercises **before** you start
the inheritance lecture — OOP layers on top of all of them.

---

## Topics covered

- Classes and instances; what OOP solves
- `__init__`, `self`, instance vs class attributes
- Methods and what `self` really is
- `__repr__` vs `__str__`
- Inheritance, `super()`, and a brief tour of the MRO
- Composition over inheritance
- `@classmethod`, `@staticmethod`, when to reach for each
- Properties with `@property`
- The `dataclasses` module
- Dunder methods overview (`__eq__`, `__lt__`, `__len__`, `__iter__`)
- Encapsulation conventions (`_protected`, `__private`, name-mangling)
- Abstract base classes (`abc`) — brief introduction
- Choosing OOP vs procedural for a given problem

---

## Suggested schedule (~36 hours)

| Day | Focus                                                     | Hours |
|----:|-----------------------------------------------------------|------:|
| 1   | Read `lecture-notes/01-classes-and-instances.md`          |   4   |
| 2   | Exercises 01–02 (Dog, Rectangle)                          |   5   |
| 3   | Read `lecture-notes/02-inheritance-and-composition.md`    |   4   |
| 4   | Exercise 03 + Challenge 01 (deck of cards)                |   5   |
| 5   | Read `lecture-notes/03-dataclasses-and-magic-methods.md`  |   4   |
| 6   | Exercises 04–05 (dataclass user, bank account)            |   4   |
| 7   | Challenge 02, quiz, homework problems                     |   5   |
| 8   | Mini-project: Library management system                   |   5   |

Total: **~36 hours**. Adjust to your pace — if a topic clicks fast, spend the
extra time on the mini-project.

---

## Navigation

```text
week-07-object-oriented-programming/
├── README.md                    <- you are here
├── resources.md
├── quiz.md
├── homework.md
├── lecture-notes/
│   ├── 01-classes-and-instances.md
│   ├── 02-inheritance-and-composition.md
│   └── 03-dataclasses-and-magic-methods.md
├── exercises/
│   ├── README.md
│   ├── exercise-01-dog-class.py
│   ├── exercise-02-rectangle.py
│   ├── exercise-03-inheritance-shapes.py
│   ├── exercise-04-dataclass-user.py
│   └── exercise-05-bank-account.py
├── challenges/
│   ├── README.md
│   ├── challenge-01-deck-of-cards.md
│   └── challenge-02-employee-hierarchy.md
└── mini-project/
    ├── README.md
    └── starter/
        ├── book.py
        ├── member.py
        ├── library.py
        └── main.py
```

**Recommended order:** lecture 01 → exercises 01–02 → lecture 02 → exercise 03 +
challenge 01 → lecture 03 → exercises 04–05 → challenge 02 → quiz → homework →
mini-project.

---

## Stretch goals

If you finish early, pick any of these:

- Add a `Librarian` subclass of `Member` to your mini-project with extra
  permissions (e.g., can register new members).
- Implement an **`Iterable` protocol** for `Library` so you can write
  `for book in library:`.
- Read the `abc` docs and convert one of your hierarchies to use
  `ABC` + `@abstractmethod`.
- Read about **`__slots__`** and benchmark memory use of a class with and
  without it (use `sys.getsizeof` and a list of 1,000,000 instances).
- Replace your hand-written `__init__`/`__eq__` in one exercise with a
  `@dataclass` and compare.

---

## Up next

**Week 8 — APIs & JSON.** You will use the `requests` library to talk to real
HTTP APIs, parse JSON responses into Python dictionaries, and start sketching
small classes that wrap an external service. The skills from this week —
designing small, well-named classes with clear methods — will be exactly the
shape of the "API client" code you build next.

See `../week-08-apis-json/`.
