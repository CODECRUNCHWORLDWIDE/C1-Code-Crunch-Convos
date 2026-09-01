# Week 7 — Exercises

Five small, focused exercises. Each one is a page: read the brief, copy the
starter into a `.py` file of the same name in your practice repo, fill in
the `TODO` markers, and run it until the output matches. So exercise 1
becomes `exercise-01-dog-class.py` on your machine, and you run it with:

```bash
python exercise-01-dog-class.py
```

The starters include type hints, real docstrings, and a demo in `main()`
that you are asked not to edit — that demo is the test. When your classes
are right, the expected output appears without you touching it.

## Index

| # | Exercise | Topics | Difficulty | Est. time |
|---|----------|--------|-----------:|----------:|
| 1 | [exercise-01-dog-class.md](./exercise-01-dog-class.md) | Classes, `__init__`, `self`, methods, per-instance state | Beginner | 30 min |
| 2 | [exercise-02-rectangle.md](./exercise-02-rectangle.md) | `@property`, derived attributes, validation on assignment | Beginner | 45 min |
| 3 | [exercise-03-inheritance-shapes.md](./exercise-03-inheritance-shapes.md) | Inheritance, `super()`, overriding, polymorphism | Easy | 60 min |
| 4 | [exercise-04-dataclass-user.md](./exercise-04-dataclass-user.md) | `@dataclass`, `default_factory`, auto-generated `__eq__` | Easy | 45 min |
| 5 | [exercise-05-bank-account.md](./exercise-05-bank-account.md) | Guarded state, custom exceptions, `__repr__` vs `__str__` | Medium | 90 min |

Recommended order is 1 → 5. Each builds on a concept from the lecture notes:

- 1 and 2 → Lecture 01. (Exercise 2 also borrows `@property` from Lecture 03,
  section 3 — read that one section early; it is four paragraphs.)
- 3 → Lecture 02.
- 4 and 5 → Lecture 03 (and tying everything together).

A solution is a script that runs to completion **with no errors** and prints
output that matches the "Expected output" block on the page, line for line.
Try to do every exercise without peeking at the next lecture — discomfort is
part of learning.

Each page ends with an acceptance checklist and a set of stretch goals. The
checklist is the bar. The stretch goals are optional, and they are where the
interesting arguments live — several of them ask you to write down *why* you
chose one design over another, which is the skill the challenges and the
mini-project will lean on.
