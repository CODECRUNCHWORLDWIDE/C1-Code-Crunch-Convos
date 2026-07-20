# Week 2 — Resources

A curated reading list for variables, types, operators, strings, and input.
Skim what looks unfamiliar; bookmark the rest for the next time you forget
a method name.

## Official Python Documentation

These are the authoritative sources. Get used to reading them — they are
shorter and clearer than most tutorials once you adjust to the style.

- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — the
  full reference for numbers, sequences (including `str`), booleans, and
  `None`. The section on **str methods** is the one you'll come back to
  most often this week.
- [Input and Output Tutorial](https://docs.python.org/3/tutorial/inputoutput.html)
  — covers `print()`, `input()`, f-strings, and format specifiers with
  worked examples. Section 7.1 on formatted string literals is required
  reading.
- [Built-in Functions](https://docs.python.org/3/library/functions.html) —
  reference for `int()`, `float()`, `str()`, `bool()`, `type()`,
  `isinstance()`, `input()`, `print()`, and `len()`.
- [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language)
  — the grammar behind format specs like `:.2f`, `:>10`, and `:,`.
- [Operator Precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)
  — the official precedence table. Print it and tape it next to your
  monitor for the next month.

## Python Enhancement Proposals (PEPs)

PEPs are how Python language changes are designed and documented. The two
that matter this week:

- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
  — the style bible. Focus on the **Naming Conventions** section: use
  `snake_case` for variables and functions, `CapWords` for classes, and
  `UPPER_SNAKE_CASE` for constants.
- [PEP 498 — Literal String Interpolation](https://peps.python.org/pep-0498/)
  — the original proposal for f-strings. Useful background for why they
  look the way they do and what they can (and cannot) contain.
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/) — the original
  type-hinting proposal. Skim the introduction; you'll revisit this often.

## Real Python (Free Articles)

Real Python publishes some of the best free Python tutorials on the web.
Recommended reads for this week:

- [Basic Data Types in Python](https://realpython.com/python-data-types/) —
  a long-form tour of `int`, `float`, `complex`, `str`, `bool`, and `None`.
- [Strings and Character Data in Python](https://realpython.com/python-strings/)
  — a thorough chapter-length article on string operations, methods, and
  formatting.
- [Python's f-String for String Interpolation and Formatting](https://realpython.com/python-f-strings/)
  — the most complete f-string guide available for free.
- [Operators and Expressions in Python](https://realpython.com/python-operators-expressions/)
  — covers every operator category with runnable examples.

## Books

- *Automate the Boring Stuff with Python* by Al Sweigart — free online at
  <https://automatetheboringstuff.com/>. For this week, read **Chapter 1
  (Python Basics)** and **Chapter 2 (Flow Control — first half on
  expressions and operators)**. Sweigart's tone is warm and very
  beginner-friendly.
- *Think Python, 3rd Edition* by Allen B. Downey — free at
  <https://allendowney.github.io/ThinkPython/>. Chapters 2 (Variables and
  Statements) and 5 (Expressions and Statements) line up exactly with this
  week.

## Type Checking

- [mypy documentation](https://mypy.readthedocs.io/en/stable/) — the
  reference for the most popular Python type checker. The
  [cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
  is the fastest way in.
- [typing module reference](https://docs.python.org/3/library/typing.html)
  — for when you start needing `list[int]`, `dict[str, float]`, and
  `Optional[T]`.

## Video Walkthroughs

- [Corey Schafer — Python Tutorial: Variables](https://www.youtube.com/watch?v=cQT33yu9pY8)
  — 15 minutes, very clear.
- [mCoding — Strings in Python](https://www.youtube.com/watch?v=ZQzVfvc_qBA)
  — a slightly more advanced take, worth watching after you finish the
  exercises.

## Reference Cards

Keep these open while you work:

- [Python Built-in Types — Quick Reference](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
  — the truthiness table is gold.
- [String Methods — Index](https://docs.python.org/3/library/stdtypes.html#string-methods)
  — every method on `str`, alphabetical.

## A Note on AI Assistants

It's tempting to ask ChatGPT, Claude, or Copilot "what does `:>10` mean?"
Resist the urge for the first few days. Reading the official docs is a
skill, and the only way to build it is to do it. Use AI assistants as a
*last* resort this week, not a first one.
