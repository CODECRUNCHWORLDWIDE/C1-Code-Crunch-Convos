"""Simple-interest calculator.

Week 2 homework, problem 1, Code Crunch Convos.
interest = principal * (rate / 100) * years

Questions go to the error stream and the report goes to the normal output
stream, so ``python homework-01-simple-interest.py > report.txt`` saves the
report and nothing else. When nobody is at the keyboard the script uses the
example figures rather than waiting for typing that is never coming. Save
your own copy as ``homework-01-simple-interest.py``.
"""

import sys

LABEL_WIDTH: int = 10
FIELD_WIDTH: int = 12

SAMPLE_PRINCIPAL: str = "1000"
SAMPLE_RATE: str = "5"
SAMPLE_YEARS: str = "3"


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


def print_report(principal: float, rate: float, years: int) -> None:
    """Print the five-line simple-interest report."""
    interest: float = principal * (rate / 100) * years
    total: float = principal + interest

    print(f"{'Principal':<{LABEL_WIDTH}}: ${principal:>{FIELD_WIDTH},.2f}")
    print(f"{'Rate':<{LABEL_WIDTH}}: {rate:>{FIELD_WIDTH - 1}.2f}%")
    print(f"{'Years':<{LABEL_WIDTH}}: {years:>{FIELD_WIDTH}d}")
    print(f"{'Interest':<{LABEL_WIDTH}}: ${interest:>{FIELD_WIDTH},.2f}")
    print(f"{'Total':<{LABEL_WIDTH}}: ${total:>{FIELD_WIDTH},.2f}")


def main() -> None:
    """Read principal, rate, and years, then print the five-line report."""
    principal: float = float(ask("Principal in dollars: ", SAMPLE_PRINCIPAL))
    rate: float = float(ask("Annual interest rate in percent: ", SAMPLE_RATE))
    years: int = int(ask("Number of years: ", SAMPLE_YEARS))
    print_report(principal, rate, years)


if __name__ == "__main__":
    main()
