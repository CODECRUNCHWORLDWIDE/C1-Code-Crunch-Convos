"""Word and character counter.

Week 2 homework, problem 3, Code Crunch Convos. One method call per
statistic, no loops.

The question goes to the error stream and the four statistics go to the
normal output stream. When nobody is at the keyboard the script uses the
example line. Save your own copy as ``homework-03-word-counter.py``.
"""

import sys

LABEL_WIDTH: int = 17

SAMPLE_TEXT: str = "hello there friend"


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


def print_report(text: str) -> None:
    """Print four statistics about ``text``, one per line."""
    print(f"{'Characters':<{LABEL_WIDTH}}: {len(text)}")
    print(f"{'Non-space chars':<{LABEL_WIDTH}}: {len(text.replace(' ', ''))}")
    print(f"{'Words':<{LABEL_WIDTH}}: {len(text.split())}")
    print(f"{'Uppercase':<{LABEL_WIDTH}}: {text.upper()}")


def main() -> None:
    """Read one line and print four statistics about it."""
    text: str = ask("Enter a line: ", SAMPLE_TEXT)
    print_report(text)


if __name__ == "__main__":
    main()
