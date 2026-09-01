"""Grade-letter assigner with no ``if`` statement in the answer.

Week 2 homework, problem 4, Code Crunch Convos. Counts how many thresholds
the score clears and uses that count to index a string of letters.

The question goes to the error stream and the grade goes to the normal
output stream. When nobody is at the keyboard the script uses the example
score. Save your own copy as ``homework-04-grade-letter.py``.
"""

import sys

LETTERS: str = "FDCBA"

SAMPLE_SCORE: str = "73"


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str, fallback: str) -> str:
    """Return the typed line, or ``fallback`` when nobody is at the keyboard."""
    if not someone_is_typing():
        return fallback
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        return fallback


def grade_for(score: float) -> str:
    """Return the letter grade for ``score`` without branching."""
    index: int = (
        (score >= 60) + (score >= 70) + (score >= 80) + (score >= 90)
    )
    return LETTERS[index]


def main() -> None:
    """Read a percentage score and print its letter grade."""
    score: float = float(ask("Enter your score: ", SAMPLE_SCORE))
    print(f"Grade: {grade_for(score)}")


if __name__ == "__main__":
    main()
