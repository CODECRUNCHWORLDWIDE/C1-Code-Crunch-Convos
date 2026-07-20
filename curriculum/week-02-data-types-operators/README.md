# Week 2 — Variables, Data Types & Operators

Welcome back to **Code Crunch Convos**. With your development environment up
and running from Week 1, you're ready to start writing code that *does
things*. This week is about the raw materials of every Python program:
variables that store values, the built-in data types those values belong to,
and the operators that combine and compare them. You'll learn how to take
input from a user at the command line, format text professionally with
f-strings, and write your first type-annotated functions. By Sunday you'll
ship a small but genuinely useful unit-converter CLI that handles
temperature, distance, and currency conversions through a menu.

Programming languages are essentially three things: data, the operations you
perform on data, and the control flow that decides when to do what. This
week covers the first two pillars in depth. Next week we'll add control
flow.

## Learning Objectives

By the end of this week, you will be able to:

- **Declare** variables in Python and explain what dynamic typing means in
  practice.
- **Identify** Python's core built-in types — `int`, `float`, `str`, `bool`,
  and `None` — and use `type()` and `isinstance()` to inspect them.
- **Convert** values between types safely using `int()`, `float()`, `str()`,
  and `bool()`, and predict the outcome of common casts.
- **Apply** arithmetic, comparison, and logical operators with correct
  precedence to compute values and form boolean expressions.
- **Manipulate** strings using indexing, slicing, common methods, and escape
  sequences, and format output with f-strings and format specifiers.
- **Read** user input with `input()`, cast it to the correct type, and
  defensively handle bad input.
- **Annotate** variables and function signatures with type hints and explain
  why they make code more maintainable.
- **Build** a menu-driven command-line unit converter that ties all of the
  above together.

## Prerequisites

You should have completed [Week 1 — Python Foundations & Dev
Environment](../week-01-python-foundations/README.md). Specifically you
need:

- Python 3.11 or later installed and available as `python` or `python3`.
- Comfort opening a terminal and running a `.py` script from it.
- A working `venv` workflow (create, activate, install).
- A code editor (VS Code recommended) configured for Python.

If any of these are shaky, take an hour to revisit Week 1 before continuing.
The exercises this week assume you can run a script without thinking about
it.

## Topics Covered

- Variables, assignment, and Python's *dynamic typing* model
- Naming conventions — `snake_case`, PEP 8, what to avoid
- Built-in primitive types: `int`, `float`, `str`, `bool`, `None`
- Mutable vs immutable values (a preview; deep dive in Week 5)
- Type casting (`int()`, `float()`, `str()`, `bool()`) and truthiness
- Arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical operators: `and`, `or`, `not`
- Operator precedence and how to read complex expressions
- String basics: indexing, slicing, common methods, escape sequences
- f-strings and format specifications (`:.2f`, `:>10`, `:,`, `:%`)
- Raw strings (`r"..."`) for paths and regex
- Reading input from the terminal with `input()`
- Type hints (`x: int = 5`) and a brief tour of `mypy`

## Weekly Schedule

The schedule below adds up to approximately **36 hours**. It's a guideline;
adjust to your pace.

| Day       | Focus                                       | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----------|---------------------------------------------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday    | Variables, dynamic typing, core types       |    2h    |    1h     |     0h     |    0.5h   |   1h     |     0h       |    0.5h    |     5h      |
| Tuesday   | Operators and string fundamentals           |    2h    |    2h     |     0h     |    0.5h   |   1h     |     0h       |    0.5h    |     6h      |
| Wednesday | f-strings, formatting, escape sequences     |    1h    |    2h     |     1h     |    0.5h   |   1h     |     0h       |    0.5h    |     6h      |
| Thursday  | `input()`, parsing, type hints              |    1h    |    1h     |     1h     |    0.5h   |   1h     |     1h       |    0.5h    |     6h      |
| Friday    | Mini-project: temperature & distance        |    0h    |    1h     |     0h     |    0.5h   |   1h     |     2h       |    0.5h    |     5h      |
| Saturday  | Mini-project: currency & polish             |    0h    |    0h     |     1h     |    0h     |   1h     |     3h       |    0h      |     5h      |
| Sunday    | Quiz, review, push to GitHub                |    0h    |    0h     |     0h     |    1h     |   0h     |     1.5h     |    0h      |     2.5h    |
| **Total** |                                             | **6h**   | **7h**    | **3h**     | **3.5h**  | **6h**   |   **7.5h**   |   **2.5h** |  **36h**    |

## How to Navigate This Week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview (you are here) |
| [resources.md](./resources.md) | Curated readings, Python docs links, PEPs |
| [lecture-notes/01-variables-and-types.md](./lecture-notes/01-variables-and-types.md) | Variables, dynamic typing, the five core types, casting |
| [lecture-notes/02-operators-and-strings.md](./lecture-notes/02-operators-and-strings.md) | Operators, precedence, strings, f-strings, format specs |
| [lecture-notes/03-input-and-type-hints.md](./lecture-notes/03-input-and-type-hints.md) | Reading input, parsing safely, type hints, mypy |
| [exercises/README.md](./exercises/README.md) | Index of short coding exercises |
| [exercises/exercise-01-variable-swap.py](./exercises/exercise-01-variable-swap.py) | Swap two variables without a temporary |
| [exercises/exercise-02-string-formatter.py](./exercises/exercise-02-string-formatter.py) | Build a multi-line aligned f-string |
| [exercises/exercise-03-temperature-converter.py](./exercises/exercise-03-temperature-converter.py) | Celsius to Fahrenheit with type hints |
| [exercises/exercise-04-input-parsing.py](./exercises/exercise-04-input-parsing.py) | Read two numbers and print arithmetic results |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-tip-calculator.md](./challenges/challenge-01-tip-calculator.md) | Tip & per-person split calculator |
| [challenges/challenge-02-mad-libs.md](./challenges/challenge-02-mad-libs.md) | Classic Mad Libs with f-strings |
| [quiz.md](./quiz.md) | 10 multiple-choice questions with answer key |
| [homework.md](./homework.md) | Six practice problems for the week |
| [mini-project/README.md](./mini-project/README.md) | Full spec for the Unit Converter CLI |
| [mini-project/starter.py](./mini-project/starter.py) | Starter file for the mini-project |

## Stretch Goals

Already comfortable with the basics? Try any of these:

- Read [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
  cover to cover and refactor your exercises to match.
- Read [PEP 498 — Literal String Interpolation](https://peps.python.org/pep-0498/)
  for the design rationale behind f-strings.
- Install `mypy` into your virtual environment and run it against every
  exercise this week until you have zero type errors.
- Extend the mini-project with a third conversion category (e.g. kilograms
  to pounds, or 24-hour to 12-hour time).
- Add ANSI color codes to the mini-project menu using raw escape strings
  like `"\033[1;36m"` and reset them with `"\033[0m"`.
- Read the [Python Tutorial — Fancier Output Formatting](https://docs.python.org/3/tutorial/inputoutput.html)
  and try the older `%`-style and `.format()` methods to appreciate why
  f-strings won.

## Up Next

When you've pushed this week's mini-project to GitHub, continue to
[Week 3 — Control Flow](../week-03-control-flow/README.md). That's where
your programs start making decisions and repeating themselves — the third
pillar of programming.
