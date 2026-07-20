# Week 4 — Functions, Modules & Scope

Welcome to Week 4 of **Code Crunch Convos**, a global, open-source Python bootcamp run out of Code Crunch Club. By the end of this week you will know how to package logic into reusable functions, split a program across multiple files, and reason confidently about which variables are visible where.

This is the week your programs stop being "scripts" and start being **software**.

---

## Why this week matters

In Weeks 1 to 3 you wrote linear scripts: read input, branch on it, loop until done. That works for tiny problems, but it falls apart fast. The moment you copy and paste the same five lines into three different `if` branches, you have a maintenance problem.

Functions are the cure. A function is a named, parameterized block of behavior you can call from anywhere. Once you can write good functions, you can:

- Reuse the same logic in many places without copy-paste.
- Test a small piece of code in isolation.
- Name a concept (`is_palindrome`, `tax_due`) so your code reads like prose.
- Split a big program into many small files, each focused on one job.

Modules take that one step further. A module is just a `.py` file that other Python files can import. Packages are folders of modules. The Python standard library itself is a giant package, and by the end of this week you will both **use** it and **add to it** by writing your own modules.

---

## Learning objectives

By the end of Week 4 you will be able to:

1. Define a function with `def`, including parameters, return values, type hints, and a PEP 257 docstring.
2. Distinguish parameters from arguments, and positional from keyword arguments.
3. Use default parameter values safely and explain the mutable-default pitfall.
4. Accept variable numbers of arguments using `*args` and `**kwargs`, and unpack iterables and dicts at the call site.
5. Apply the LEGB scope rule (Local, Enclosing, Global, Built-in) to predict which name a lookup finds.
6. Use `global` and `nonlocal` correctly, and explain why both should be rare.
7. Write a pure function and articulate the difference between a return value and a side effect.
8. Use a `lambda` for a small inline function and know when *not* to.
9. Import from the standard library using `import`, `from ... import`, and aliases.
10. Write your own module, import it from a sibling file, and protect script-only code with `if __name__ == "__main__":`.
11. Organize a multi-file Python project around a clear public interface.

---

## Prerequisites

You should be comfortable with everything from Weeks 1 to 3:

- **Week 1 — Python Foundations**: running scripts, `print`, variables, basic I/O.
- **Week 2 — Data Types & Operators**: `int`, `float`, `str`, `bool`, `list`, `dict`, slicing, f-strings.
- **Week 3 — Control Flow**: `if/elif/else`, `for`, `while`, `break`, `continue`, basic boolean logic.

If any of those feel shaky, do not skip ahead. Functions are easier when the body of the function is already familiar.

---

## Topics covered

- Defining functions with `def`
- Parameters vs arguments; positional vs keyword
- Return values vs side effects
- Default parameter values (and the mutable-default gotcha)
- `*args` and `**kwargs`
- Type hints on parameters and return values (PEP 484)
- Docstrings (PEP 257)
- The LEGB scope rule
- `global` and `nonlocal`
- Pure functions
- `lambda` expressions
- Importing from the standard library
- Writing your own module
- Multi-file projects and the `if __name__ == "__main__":` idiom

---

## Schedule (roughly 36 hours of work)

| Day | Activity | Time | Deliverable |
|-----|----------|------|-------------|
| Mon | Read lecture note 1 (defining functions) | 2 h | Notes in your journal |
| Mon | Exercise 01 (function basics) | 1.5 h | `exercise-01-function-basics.py` |
| Tue | Read lecture note 2 (`*args`/`**kwargs`, scope) | 2.5 h | Notes |
| Tue | Exercise 02 (`*args`/`**kwargs`) | 1.5 h | `exercise-02-args-kwargs.py` |
| Wed | Exercise 03 (recursion intro) | 2 h | `exercise-03-recursion-intro.py` |
| Wed | Exercise 04 (scope mystery) | 1.5 h | Fixed script |
| Thu | Read lecture note 3 (modules & imports) | 2 h | Notes |
| Thu | Exercise 05 (stdlib imports) | 1.5 h | `exercise-05-import-and-use.py` |
| Fri | Challenge 01 (calculator module) | 3 h | Module + `main.py` |
| Fri | Challenge 02 (text stats package) | 3 h | Package + demo |
| Sat | Mini-project: personal finance calculator | 6 h | 4-file project |
| Sun | Homework problems 1–6 | 5 h | 6 short scripts |
| Sun | Quiz (10 MCQs) | 30 min | Submitted answers |
| Sun | Review, polish, commit | 1.5 h | Clean repo |
| **Total** | | **~36 h** | |

If you have less than 36 hours, prioritize: lecture notes, exercises 1 and 2, and the mini-project. The challenges are stretch material if you are time-boxed.

---

## Navigation

- [Lecture note 1 — Defining functions](./lecture-notes/01-defining-functions.md)
- [Lecture note 2 — `*args`, `**kwargs`, and scope](./lecture-notes/02-args-kwargs-and-scope.md)
- [Lecture note 3 — Modules and imports](./lecture-notes/03-modules-and-imports.md)
- [Exercises index](./exercises/README.md)
- [Challenges index](./challenges/README.md)
- [Quiz](./quiz.md)
- [Homework](./homework.md)
- [Mini-project — Personal finance calculator](./mini-project/README.md)
- [Resources](./resources.md)

---

## Stretch goals

If the core material feels easy, push further:

1. **Add `typing` generics** to your functions: `list[int]`, `dict[str, float]`, `Optional[str]`. Read [PEP 484](https://peps.python.org/pep-0484/).
2. **Write doctests** inside your docstrings and run them with `python -m doctest your_module.py -v`.
3. **Refactor an old script** from Week 3 into functions in a separate module, then import and call them from a thin entry-point script.
4. **Profile a recursive function** with `time` from the standard library and compare against the iterative version.
5. **Read the `functools` docs** and try `functools.reduce` and `functools.lru_cache` on your recursive `factorial`.
6. **Explore `argparse`** and turn your mini-project into a real CLI with flags.

---

## How to get help

- Open a discussion in the Code Crunch Convos GitHub org.
- Post in the `#week-04` Discord channel.
- Pair with another learner. Functions are great practice for code review.

If you are stuck for more than 30 minutes on a single bug, ask. The bootcamp is a community, not a solo sprint.

---

## Up next

[Week 5 — Data Structures](../week-05-data-structures/README.md): we will go deeper on lists, tuples, sets, and dictionaries, including comprehensions, when to pick which structure, and the time-complexity trade-offs that come with each.

Bring your function skills with you — Week 5 leans on them heavily.
