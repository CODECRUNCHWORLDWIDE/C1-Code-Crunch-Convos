"""Mini calculator: four arithmetic functions, and a REPL that uses them.

Challenge 1, Week 4, Code Crunch Convos.

The project this answers is two files. ``calculator.py`` holds the arithmetic
and knows nothing about people; ``main.py`` imports it and does all the talking.
This download folds both halves into one file so that it runs the moment you
save it: everything above the ``main.py half`` banner is what ``calculator.py``
contains, and everything below it is what ``main.py`` contains. The page beside
this file shows the two-file split, which is the thing the challenge is really
about.

Questions go to the error stream and results go to the normal output stream, so
``python challenge-01-mini-calculator-module-solution.py > out.txt`` saves the
answers and none of the questions.

Run it with::

    python challenge-01-mini-calculator-module-solution.py
"""

import sys

# --- the calculator.py half: arithmetic, and nothing else ------------------


def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return a - b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return a * b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return a / b, refusing a zero divisor."""
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def _self_test() -> None:
    """Exercise all four functions and report OK or the first failure."""
    checks = [
        ("add(2, 3)", add(2.0, 3.0), 5.0),
        ("subtract(10, 4)", subtract(10.0, 4.0), 6.0),
        ("multiply(7, 6)", multiply(7.0, 6.0), 42.0),
        ("divide(10, 4)", divide(10.0, 4.0), 2.5),
    ]
    for label, got, want in checks:
        if got != want:
            print(f"FAIL: {label} -> {got!r}, expected {want!r}")
            return
    try:
        divide(1.0, 0.0)
    except ZeroDivisionError as exc:
        if str(exc) != "cannot divide by zero":
            print(f"FAIL: divide by zero message was {str(exc)!r}")
            return
    else:
        print("FAIL: divide(1, 0) did not raise ZeroDivisionError")
        return
    print("OK")


# --- the main.py half: talking to a person ---------------------------------

# Import choice. In the two-file version the line above this table reads
# ``from calculator import add, divide, multiply, subtract``, not
# ``import calculator``. The four names go straight into OPS, and spelling them
# ``calculator.add`` in there would add noise without adding information. For a
# module with a wider surface, ``import calculator`` is the better default.

OPS = {"+": add, "-": subtract, "*": multiply, "/": divide}

BANNER = 'Mini calculator. Type "quit" to exit.'
PROMPT = "> "

# The session this file types for itself when its input stream is finished.
DEMO_LINES: list[str] = ["2 + 3", "10 / 4", "7 * 6", "1 / 0", "hello", "quit"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on once the demo script above has run
            out. Every call site passes ``"quit"``, so this file can never
            loop forever unattended.

    Returns:
        The line that was typed, or the next demo answer. A demo answer is
        echoed after the prompt on the normal output stream, trimmed on the
        right so a question answered with a blank line leaves no stray space
        at the end of a saved transcript.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_LINES.pop(0) if DEMO_LINES else demo
        print(f"{prompt}{answer}".rstrip())
        return answer


def parse(line: str) -> tuple[float, str, float]:
    """Parse '2 + 3' into (2.0, '+', 3.0)."""
    parts = line.split()
    if len(parts) != 3:
        raise ValueError("expected exactly three whitespace-separated fields")
    left, op, right = parts
    if op not in OPS:
        raise ValueError(f"unknown operator {op!r}")
    return float(left), op, float(right)


def main() -> None:
    """Run the REPL until the user quits."""
    print(BANNER)
    while True:
        line = ask(PROMPT, "quit").strip()
        if line == "" or line.lower() == "quit":
            break
        try:
            left, op, right = parse(line)
        except ValueError:
            print(f'sorry, I did not understand "{line}". Use: <num1> <op> <num2>.')
            continue
        try:
            print(OPS[op](left, right))
        except ZeroDivisionError as exc:
            print(exc)
    print("bye!")


if __name__ == "__main__":
    _self_test()
    print()
    main()
