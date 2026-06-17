# Lecture Note 3 — Modules and Imports

> Estimated reading time: 35 minutes. Pair this with the [official Python tutorial on modules](https://docs.python.org/3/tutorial/modules.html).

So far every program has lived in a single `.py` file. That works for ten lines, breaks down at a hundred, and is unbearable at a thousand. In this lecture you will learn how to split a Python program across multiple files and how to use code from Python's enormous standard library.

---

## 1. What is a module?

In Python, **any file with a `.py` extension is a module**. That is the entire definition. There is nothing special you have to do to "make" a file into a module — just save it with a `.py` extension and it is one.

The file's **module name** is the file name without `.py`. So `greetings.py` is the module `greetings`. (Keep your module names short, all-lowercase, and use underscores if needed — `data_loader.py` not `DataLoader.py`. See [PEP 8 Naming Conventions](https://peps.python.org/pep-0008/#package-and-module-names).)

When you write a function, class, or top-level variable in a module, other modules can use it by **importing** that module.

---

## 2. The three import forms

Suppose we have a file `geometry.py`:

```python
"""Geometry helpers."""

from math import pi


def circle_area(radius: float) -> float:
    """Return the area of a circle."""
    return pi * radius * radius


def rectangle_area(width: float, height: float) -> float:
    """Return the area of a rectangle."""
    return width * height


PI = pi
```

There are three common ways to import from it.

### Form 1 — `import module`

```python
import geometry

print(geometry.circle_area(3))
print(geometry.PI)
```

You access everything through the module's namespace. This is the most explicit form and the one PEP 8 implicitly prefers. Beginners often skip it, but it has a real advantage: a reader of your code can always tell **where** `circle_area` came from.

### Form 2 — `from module import name`

```python
from geometry import circle_area, PI

print(circle_area(3))
print(PI)
```

You pull specific names into your own namespace. Shorter, but the reader of your code must remember where `circle_area` lives.

Avoid this form:

```python
from geometry import *
```

The wildcard import drags every public name into your namespace. It works but it makes your code hard to read, hides bugs (which import provided `area`?), and shadows built-ins silently. PEP 8 explicitly discourages it.

### Form 3 — `import module as alias`

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

Useful when the module name is long or when there is a community convention. Do not invent your own short aliases for fun. If your team has not agreed on `import foo as f`, do not do it.

You can also alias a `from` import:

```python
from collections import OrderedDict as ODict
```

Same caution applies. Usually overkill.

---

## 3. Where does Python look for modules?

When you write `import geometry`, Python searches a list of directories in order. That list lives in `sys.path`:

```python
import sys
for p in sys.path:
    print(p)
```

Typical contents:

1. The directory of the script you are running. (This is why `import geometry` finds `geometry.py` if both files sit in the same folder.)
2. Directories listed in the `PYTHONPATH` environment variable.
3. Installation-specific default paths.
4. The directories of any installed packages (`pip install ...` puts modules here).

The official explanation is in [The Module Search Path](https://docs.python.org/3/tutorial/modules.html#the-module-search-path).

The practical rule: **if both files are in the same folder, `import sibling_module` just works**. That is all you need for now.

---

## 4. The standard library — Python's batteries

Python ships with a huge **standard library** of modules you can import without installing anything. A short tour of useful ones:

| Module | What it is good for |
|--------|---------------------|
| `math` | `sqrt`, `pi`, `sin`, `log`, etc. |
| `random` | Random numbers, shuffling, sampling. |
| `statistics` | `mean`, `median`, `stdev`. |
| `datetime` | Dates, times, deltas. |
| `os`, `os.path`, `pathlib` | Files, paths, directories. |
| `json` | Read and write JSON. |
| `csv` | Read and write CSV. |
| `collections` | `Counter`, `defaultdict`, `deque`, `namedtuple`. |
| `itertools` | Lazy iteration helpers (`chain`, `groupby`, `combinations`). |
| `functools` | `reduce`, `partial`, `lru_cache`. |
| `re` | Regular expressions. |
| `sys` | Interpreter introspection, `sys.argv`, `sys.exit`. |
| `argparse` | Parse command-line flags. |

A quick example with three of them:

```python
import math
import random
import statistics

print(math.sqrt(2))                # 1.4142...
print(random.choice(["a", "b"]))   # one of "a", "b"
print(statistics.mean([1, 2, 3]))  # 2
```

Browse the full list at the [Python Standard Library docs](https://docs.python.org/3/library/index.html). Whenever you find yourself about to write something tricky, search the standard library first. Odds are it is already there.

---

## 5. Writing your own module

Let us split a program into two files.

`mathy.py`:

```python
"""Math helpers."""


def square(n: float) -> float:
    """Return n squared."""
    return n * n


def cube(n: float) -> float:
    """Return n cubed."""
    return n * n * n


def hypotenuse(a: float, b: float) -> float:
    """Return the hypotenuse of a right triangle with legs a and b."""
    return (square(a) + square(b)) ** 0.5
```

`main.py` (in the same folder):

```python
"""Entry point."""

from mathy import hypotenuse


def main() -> None:
    """Run the demo."""
    print(f"3-4-5 triangle hypotenuse: {hypotenuse(3, 4)}")


if __name__ == "__main__":
    main()
```

From a terminal in that folder:

```bash
python main.py
```

Output: `3-4-5 triangle hypotenuse: 5.0`.

Two files, one import, one demo entry point. That is the basic shape of every multi-file Python project.

---

## 6. The `if __name__ == "__main__":` idiom

When Python imports a module, it **runs every top-level statement in it**. That means if `mathy.py` ended with:

```python
print("hello from mathy")
```

then `from mathy import hypotenuse` in `main.py` would print "hello from mathy" as a side effect. Almost never what you want.

Python has a built-in variable `__name__` that tells you **how** the module is being used:

- If you run `python mathy.py` directly, then `__name__` is `"__main__"`.
- If you `import mathy` from another file, then `__name__` is `"mathy"`.

The idiom uses this to put script-only code behind a guard:

```python
def main() -> None:
    """Run the demo."""
    print(f"3-4-5 triangle hypotenuse: {hypotenuse(3, 4)}")


if __name__ == "__main__":
    main()
```

Now:

- `python main.py` runs `main()`.
- `import main` from another file does **not** run `main()` — it just makes the function available.

This is so common that every project you read will have it somewhere. Read more in the [`__main__` docs](https://docs.python.org/3/library/__main__.html) and in [Real Python's explainer](https://realpython.com/if-name-main-python/).

Style tips:

- Put your "what to do when run as a script" code inside a `main()` function, then guard the call.
- Keep the guarded block short. If it grows, factor it out.
- The guard is the bottom of the file by convention.

---

## 7. Modules expose a public interface

When you write a module, you are designing an **interface** for other code to use. Two conventions help:

### Use `_` for private names

```python
def public_helper() -> int:
    return _internal_helper() + 1


def _internal_helper() -> int:
    return 42
```

Names starting with an underscore are a polite "do not touch from outside". Python does not enforce this, but every Python programmer respects it.

### Use `__all__` if you care about `from x import *`

```python
__all__ = ["public_helper"]
```

`__all__` is a list of names that `from your_module import *` should pull in. Most projects do not bother because they avoid wildcard imports anyway, but you will see it in libraries.

---

## 8. Packages — a brief preview

A **package** is a folder of modules with an `__init__.py` file inside it. The `__init__.py` can be empty; its presence marks the folder as a package.

```text
mypkg/
    __init__.py
    arithmetic.py
    geometry.py
```

You import from a package using dotted paths:

```python
from mypkg.arithmetic import add
from mypkg.geometry import circle_area
```

You can also write `mypkg/__init__.py` so it re-exports a tidy public interface:

```python
# mypkg/__init__.py
from .arithmetic import add, subtract
from .geometry import circle_area, rectangle_area

__all__ = ["add", "subtract", "circle_area", "rectangle_area"]
```

Then users of your package just write:

```python
from mypkg import circle_area
```

We will go deeper into packages later in the bootcamp. For Week 4, you only need to know that **a folder of `.py` files + an `__init__.py` is a package** and that you import with dotted paths. The full reference is in [Packages](https://docs.python.org/3/tutorial/modules.html#packages).

---

## 9. Organizing a multi-file project

Here is a template you can use for the mini-project (and most real projects):

```text
my_project/
    README.md
    main.py
    income.py
    expenses.py
    report.py
```

Rules of thumb for splitting a program into files:

- **One concept per file.** `income.py` deals with income. `expenses.py` deals with expenses. `report.py` knows how to format a report.
- **No "kitchen sink" file.** A file named `utils.py` is a warning sign. If something does not have a clear home, give it one before it becomes a dumping ground.
- **Keep the entry point thin.** `main.py` should mostly orchestrate: read input, call the other modules, print or save output. The interesting logic lives in the other files.
- **Avoid circular imports.** If `income.py` imports from `report.py` and `report.py` imports from `income.py`, you have a design problem. Break the cycle by moving the shared code into a third module.

The mini-project follows this pattern exactly. Use it as a blueprint.

---

## 10. Imports: best practices recap

From PEP 8 and accumulated community wisdom:

1. **Imports at the top of the file.** After the module docstring, before any code.
2. **One module per line.** `import os, sys` is legal but discouraged; `import os` then `import sys` on separate lines is preferred.
3. **Three groups, separated by blank lines, in this order:**
   1. Standard library imports (`os`, `math`).
   2. Third-party imports (`numpy`, `requests`).
   3. Local imports (`from . import income`).
4. **Absolute imports preferred** over relative. `from mypkg.arithmetic import add` is clearer than `from .arithmetic import add`. Both are legal inside a package.
5. **No wildcard imports** in production code (`from module import *`).
6. **Avoid renaming** unless there is a community convention.

A canonical header looks like this:

```python
"""Module docstring."""

import json
import math
from pathlib import Path

import requests

from myapp.income import compute_income
from myapp.expenses import compute_expenses
```

---

## 11. A complete mini-example

Two files in the same folder. Try it yourself.

`temperature.py`:

```python
"""Temperature conversion helpers."""


def c_to_f(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def f_to_c(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


if __name__ == "__main__":
    # Self-test when run directly.
    print(c_to_f(0))    # 32.0
    print(f_to_c(212))  # 100.0
```

`weather_report.py`:

```python
"""A tiny weather report using the temperature module."""

from temperature import c_to_f


def report(city: str, celsius: float) -> str:
    """Return a one-line weather report."""
    fahrenheit = c_to_f(celsius)
    return f"{city}: {celsius:.1f} C ({fahrenheit:.1f} F)"


def main() -> None:
    """Print reports for a few cities."""
    cities = [("Tunis", 24.0), ("Tokyo", 18.5), ("Bogota", 15.0)]
    for city, c in cities:
        print(report(city, c))


if __name__ == "__main__":
    main()
```

Run `python weather_report.py` and you should see three lines of output. Run `python temperature.py` and you should see the self-test results. Run `import temperature` from the REPL and nothing should print. That is the idiom doing its job.

---

## 12. Checklist before you move on

- [ ] You can write a function in one file and call it from another.
- [ ] You can describe the three import forms and when to use each.
- [ ] You can predict whether `import X` will run code at the top level of `X.py`.
- [ ] You can explain what `if __name__ == "__main__":` does and why.
- [ ] You can name three useful standard-library modules and one function from each.
- [ ] You know what a package is and how it differs from a module.

You are ready for the exercises, the challenges, and the multi-file mini-project.

Next steps: [Exercises](../03-exercises/00-overview.md) and the [Mini-project](../07-mini-project/00-overview.md).
