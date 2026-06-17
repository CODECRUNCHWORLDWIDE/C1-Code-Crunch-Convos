# Week 7 — Resources

A short, curated reading list. Read the Python docs first — they are the source
of truth. The Real Python articles fill in everyday "how do I actually use this"
gaps, and the essay at the end is a classic that will change how you think
about class design.

---

## Official Python documentation (read first)

- **The official tutorial — Classes**
  <https://docs.python.org/3/tutorial/classes.html>
  The canonical introduction to Python's class model. Covers names and scopes,
  `__init__`, instance vs class attributes, inheritance, private variables,
  iterators, and generators. Short and worth re-reading once a year.

- **`dataclasses` — Data Classes**
  <https://docs.python.org/3/library/dataclasses.html>
  Decorator and functions for automatically adding generated special methods
  (`__init__`, `__repr__`, `__eq__`, ...) to classes. Covers `field()`,
  `default_factory`, `frozen=True`, and `__post_init__`.

- **Python Language Reference — Data model**
  <https://docs.python.org/3/reference/datamodel.html>
  The full reference for every dunder method (`__getitem__`, `__iter__`,
  `__add__`, `__hash__`, descriptors, metaclasses, ...). Long, dense, and the
  most important reference document in all of Python. Skim it once now; come
  back to it when you need a specific dunder.

- **`abc` — Abstract Base Classes**
  <https://docs.python.org/3/library/abc.html>
  Brief reference for `ABC`, `ABCMeta`, and `@abstractmethod`.

- **PEP 8 — Style Guide for Python Code (class section)**
  <https://peps.python.org/pep-0008/#class-names>
  Conventions for class names (`CamelCase`), method names (`snake_case`),
  `_protected` and `__private` underscores.

---

## Real Python articles (practical depth)

- **Object-Oriented Programming (OOP) in Python 3**
  <https://realpython.com/python3-object-oriented-programming/>
  Start here if the official tutorial feels terse.

- **Python Classes: The Power of Object-Oriented Programming**
  <https://realpython.com/python-classes/>
  Longer, deeper companion to the article above.

- **The `@property` Decorator in Python: Its Use Cases, Advantages, and Syntax**
  <https://realpython.com/python-property/>

- **Python's `super()` Considered Super!**
  <https://realpython.com/python-super/>

- **Data Classes in Python 3.7+ (Guide)**
  <https://realpython.com/python-data-classes/>

- **Python `@classmethod` vs `@staticmethod` vs Instance Methods**
  <https://realpython.com/instance-class-and-static-methods-demystified/>

---

## Long-form essay (read once, slowly)

- **"Composition over inheritance"** — Brandon Rhodes
  <https://python-patterns.guide/gang-of-four/composition-over-inheritance/>
  A clear, opinionated essay using the Gang-of-Four design patterns to
  demonstrate when inheritance hurts and composition helps. After Week 7 this
  will make significantly more sense than before — re-read it twice.

---

## Optional further reading

- **Raymond Hettinger — "Beyond PEP 8"** (talk)
  <https://www.youtube.com/watch?v=wf-BqAjZb8M>
  Great taste-builder for "what is *good* Python code, not just *correct*"
  Python code.

- **`functools.total_ordering`**
  <https://docs.python.org/3/library/functools.html#functools.total_ordering>
  Saves you from writing all six comparison dunders by hand.

- **`enum` — Support for enumerations**
  <https://docs.python.org/3/library/enum.html>
  Useful with classes when you have a small fixed set of constants.
