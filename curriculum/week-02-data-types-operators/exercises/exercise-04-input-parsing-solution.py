"""exercise-04-input-parsing-solution.py — read two whole numbers and inspect them.

Week 2, Exercise 4. Practises input(), casting, and recovering from bad
input. The read_int() helper here is reused by the Week 2 mini-project.

Three ways to hand this program its two numbers:

    python exercise-04-input-parsing-solution.py --ask   asks you to type them
    python exercise-04-input-parsing-solution.py 12 0    takes them from the command line
    python exercise-04-input-parsing-solution.py         uses the sample pair below

The sample pair is the default so that a run with nobody at the keyboard
prints the same seven lines every time instead of waiting for typing that
is never coming.
"""

import sys

ASK_FLAG: str = "--ask"
PROMPT_FIRST: str = "First whole number: "
PROMPT_SECOND: str = "Second whole number: "
UNDEFINED: str = "undefined (division by zero)"

SAMPLE_FIRST: int = 17
SAMPLE_SECOND: int = 5
SAMPLE_NOTE: str = (
    f"Using the sample pair {SAMPLE_FIRST} and {SAMPLE_SECOND}. "
    f"Pass two numbers, or {ASK_FLAG}, to choose your own."
)


def parse_int(raw: str) -> int | None:
    """Return the whole number in raw, or None if there isn't one.

    Args:
        raw: exactly what the user typed, unmodified.

    Returns:
        The parsed integer, or None if raw is not a whole number.
        Returning None rather than raising lets the caller decide what
        to do about it.
    """
    try:
        return int(raw)
    except ValueError:
        return None


def read_int(prompt: str) -> int:
    """Prompt the user until they type a whole number, then return it.

    Args:
        prompt: the text shown before the cursor.

    Returns:
        The whole number the user eventually typed.
    """
    while True:
        raw: str = input(prompt)
        value: int | None = parse_int(raw)
        if value is not None:
            return value
        print(f"  {raw!r} is not a whole number. Try again.")


def describe(a: int, b: int) -> None:
    """Print every arithmetic operator from Lecture 2 applied to a and b."""
    print(f"{a} + {b}  = {a + b}")
    print(f"{a} - {b}  = {a - b}")
    print(f"{a} * {b}  = {a * b}")
    if b == 0:
        print(f"{a} / {b}  = {UNDEFINED}")
        print(f"{a} // {b} = {UNDEFINED}")
        print(f"{a} % {b}  = {UNDEFINED}")
    else:
        print(f"{a} / {b}  = {a / b}")
        print(f"{a} // {b} = {a // b}")
        print(f"{a} % {b}  = {a % b}")
    print(f"{a} ** {b} = {a ** b}")


def numbers_from_argv() -> tuple[int, int] | None:
    """Return the pair typed after the filename, or None if there isn't one."""
    if len(sys.argv) != 3:
        return None
    first: int | None = parse_int(sys.argv[1])
    second: int | None = parse_int(sys.argv[2])
    if first is None or second is None:
        return None
    return first, second


def choose_numbers() -> tuple[int, int]:
    """Return the pair to describe: keyboard, command line, or samples."""
    if ASK_FLAG in sys.argv[1:]:
        try:
            return read_int(PROMPT_FIRST), read_int(PROMPT_SECOND)
        except EOFError:
            print("\nNo input. Using the sample pair.", file=sys.stderr)
            return SAMPLE_FIRST, SAMPLE_SECOND
    from_argv: tuple[int, int] | None = numbers_from_argv()
    if from_argv is not None:
        return from_argv
    print(SAMPLE_NOTE, file=sys.stderr)
    return SAMPLE_FIRST, SAMPLE_SECOND


def main() -> None:
    """Describe whichever pair of whole numbers this run was handed."""
    a, b = choose_numbers()
    describe(a, b)


if __name__ == "__main__":
    main()
