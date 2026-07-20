# Week 4 — Resources

A curated reading list for functions, modules, and scope. Skim everything; read the items marked **(must-read)** in full.

---

## Official Python documentation

- **(must-read)** [Defining Functions — the official tutorial](https://docs.python.org/3/tutorial/controlflow.html#defining-functions). The clearest single source on `def`, defaults, keyword arguments, `*args`/`**kwargs`, and documentation strings. Read it once before Lecture Note 1 and once after.
- [More on Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions). Continues the tutorial with positional-only, keyword-only, and unpacking argument lists.
- **(must-read)** [Modules — the official tutorial](https://docs.python.org/3/tutorial/modules.html). Covers `import`, `from ... import`, the module search path, packages, and `__main__`.
- [`__main__` — Top-level code environment](https://docs.python.org/3/library/__main__.html). The official explanation of the `if __name__ == "__main__":` idiom.
- [The `math` module](https://docs.python.org/3/library/math.html), [the `random` module](https://docs.python.org/3/library/random.html), and [the `statistics` module](https://docs.python.org/3/library/statistics.html). You will use these in Exercise 05.
- [Built-in Functions](https://docs.python.org/3/library/functions.html). Worth bookmarking. Many "tricks" are just built-ins you have not met yet.

---

## Python Enhancement Proposals (PEPs)

PEPs are the formal design documents of the Python language. They are surprisingly readable.

- **(must-read)** [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/). Naming, indentation, line length. Especially read the "Naming Conventions" section: `snake_case` for functions and variables, `PascalCase` for classes, `UPPER_CASE` for constants.
- **(must-read)** [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/). What goes in a docstring, how to format it, and the difference between one-line and multi-line docstrings.
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/). The original type-hints proposal. Skim the first half; the rest is for tool authors.
- [PEP 3107 — Function Annotations](https://peps.python.org/pep-3107/). The older spec that introduced the `def f(x: int) -> int:` syntax.
- [PEP 328 — Imports: Multi-Line and Absolute/Relative](https://peps.python.org/pep-0328/). Why we usually prefer absolute imports.

---

## Real Python tutorials

[Real Python](https://realpython.com) has high-quality, beginner-friendly tutorials. These are free to read.

- [Defining Your Own Python Function](https://realpython.com/defining-your-own-python-function/). A long, thorough walkthrough of everything we cover in Lecture Note 1.
- [Python args and kwargs: Demystified](https://realpython.com/python-kwargs-and-args/). The single best treatment of `*args`/`**kwargs` for beginners.
- [Python Scope & the LEGB Rule](https://realpython.com/python-scope-legb-rule/). Required reading if Lecture Note 2 leaves you confused.
- [Python Modules and Packages — An Introduction](https://realpython.com/python-modules-packages/). Pairs perfectly with Lecture Note 3.
- [What Does `if __name__ == "__main__"` Do?](https://realpython.com/if-name-main-python/). Explains the idiom we use in the mini-project.
- [Python Type Checking (Guide)](https://realpython.com/python-type-checking/). Optional but valuable.

---

## Books (free or open-licensed)

- **(must-read)** [Think Python (3rd ed.), Chapter 3 — "Functions"](https://greenteapress.com/wp/think-python-3rd-edition/) by Allen Downey. Free online. Beginner-friendly explanation with exercises.
- Think Python, Chapter 6 — "Fruitful Functions". Builds on Chapter 3 with return values, incremental development, and unit tests.
- [Automate the Boring Stuff with Python, Chapter 3 — "Functions"](https://automatetheboringstuff.com/2e/chapter3/) by Al Sweigart. Free online. Very practical tone.
- [Python for Everybody, Chapter 4 — "Functions"](https://www.py4e.com/html3/04-functions) by Charles Severance. Free, with video lectures.

---

## Videos

- [Corey Schafer — Python Tutorial for Beginners 8: Functions](https://www.youtube.com/watch?v=9Os0o3wzS_I). 22 minutes. Excellent pacing.
- [mCoding — `*args` and `**kwargs` in Python](https://www.youtube.com/watch?v=4jBJhCaNrWU). Short and rigorous.
- [ArjanCodes — Why Global Variables Are Bad](https://www.youtube.com/watch?v=NTbGRELYV9I). Reinforces the "avoid `global`" advice from Lecture Note 2.

---

## Going deeper (optional)

- [Python's `inspect` module](https://docs.python.org/3/library/inspect.html). Lets you introspect functions at runtime. Fun once you know the basics.
- [Python's `functools` module](https://docs.python.org/3/library/functools.html). `lru_cache`, `partial`, `reduce`. Builds on what you learn this week.
- [The `dis` module](https://docs.python.org/3/library/dis.html). Disassemble Python bytecode. Useful for understanding how scope is resolved at compile time.
- [Fluent Python (2nd ed.) by Luciano Ramalho](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/). Not free, but the chapters on functions as objects and on decorators are the best treatment in print.

---

## Tooling worth installing this week

- **`ruff`** — a fast linter that catches PEP 8 mistakes. `pip install ruff` then `ruff check .`.
- **`mypy`** — a static type checker. `pip install mypy` then `mypy your_module.py`.
- **`pytest`** — for the testing stretch goals. `pip install pytest`.

None of these are required. They are stretch material if you finish early.

---

## Citation note

When you copy code from Real Python or any tutorial into your own repo, add a short comment crediting the source. Same rule for the books listed above. Crediting sources is a professional habit and shows respect for the people who made the material free.
