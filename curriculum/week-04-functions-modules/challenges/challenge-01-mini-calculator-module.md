# Challenge 01 — Mini Calculator Module

> Time: about 3 hours. Difficulty: comfortable.

## Goal

Build a small `calculator` module with four arithmetic functions and a separate `main.py` that uses it as a tiny REPL. This is your first multi-file Python project where one file imports another.

## Functional requirements

Create a folder `challenge-01-mini-calculator/` inside `challenges/`. Inside it, create two files: `calculator.py` and `main.py`.

### `calculator.py`

A module that exposes exactly four public functions:

- `add(a, b)` returns `a + b`.
- `subtract(a, b)` returns `a - b`.
- `multiply(a, b)` returns `a * b`.
- `divide(a, b)` returns `a / b`. If `b == 0`, raise `ZeroDivisionError` with the message `"cannot divide by zero"`.

Each function:

- Accepts two `float` arguments.
- Returns a `float`.
- Has a one-line docstring per [PEP 257](https://peps.python.org/pep-0257/).
- Has type hints on parameters and return value.

The module also has a module-level docstring at the top: `"""Tiny arithmetic calculator."""`.

When run directly (`python calculator.py`), the module should print a small self-test that exercises all four functions and prints either `OK` or a failure message. Use the `if __name__ == "__main__":` idiom.

### `main.py`

A short script that imports your calculator and runs a simple REPL:

1. Prints a one-line welcome banner.
2. In a loop, prompts the user for input in the form `<num1> <op> <num2>`, where `<op>` is one of `+`, `-`, `*`, `/`.
3. Parses the input, calls the right function, prints the result.
4. On a blank line or the word `quit`, exits cleanly.
5. On any error (bad format, bad operator, divide by zero), prints a friendly message and continues the loop.

`main.py` must:

- Import using `from calculator import add, subtract, multiply, divide` OR `import calculator`. Your choice; document the choice in a comment at the top.
- Guard the main entry point with `if __name__ == "__main__":`.
- Define a `main()` function. The guard should call `main()`.

## Example session

```text
$ python main.py
Mini calculator. Type "quit" to exit.
> 2 + 3
5.0
> 10 / 4
2.5
> 7 * 6
42.0
> 1 / 0
cannot divide by zero
> hello
sorry, I did not understand "hello". Use: <num1> <op> <num2>.
> quit
bye!
```

## Suggested structure

```python
# calculator.py
"""Tiny arithmetic calculator."""


def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


# ... subtract, multiply, divide ...


def _self_test() -> None:
    """Run a small self-test."""
    ...


if __name__ == "__main__":
    _self_test()
```

```python
# main.py
"""Mini calculator REPL."""

from calculator import add, subtract, multiply, divide


OPS = {"+": add, "-": subtract, "*": multiply, "/": divide}


def parse(line: str) -> tuple[float, str, float]:
    """Parse '2 + 3' into (2.0, '+', 3.0)."""
    ...


def main() -> None:
    """Run the REPL until the user quits."""
    ...


if __name__ == "__main__":
    main()
```

## Rubric (100 points)

| Section | Points | Criteria |
|---------|--------|----------|
| Module structure | 20 | Two files in their own folder; clean separation. |
| Function correctness | 20 | All four functions work; divide-by-zero handled. |
| Type hints & docstrings | 15 | Present on every function. |
| `__main__` idiom | 10 | Used in both files where appropriate. |
| REPL behavior | 20 | Welcome, loop, quit, robust to bad input. |
| Code style (PEP 8) | 10 | Naming, spacing, line length under 100. |
| Bonus (stretch) | +5 | Support `**` (power) or `%` (modulo); document it. |

## Stretch ideas

- Add a fifth operator like `%` or `**`, and update the parser table.
- Track the last result in a variable named `_` so the user can type `_ + 1`.
- Persist a history list and print it on quit.
- Replace the parser with one that uses `shlex.split` for trickier inputs.

## What to learn from this challenge

- That `import` works automatically across files in the same folder.
- That the entry-point script (`main.py`) should be thin and delegate to a module.
- That input parsing always needs error handling.
- That `if __name__ == "__main__":` lets a module double as a script for testing.

When you are done, commit and move on to [Challenge 02](./challenge-02-text-stats-package.md).
