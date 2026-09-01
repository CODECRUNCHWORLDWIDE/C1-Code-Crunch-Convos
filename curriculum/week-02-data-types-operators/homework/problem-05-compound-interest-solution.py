"""Compound-interest calculator.

Week 2 homework, problem 5, Code Crunch Convos.
final_amount = principal * (1 + rate / 100) ** years

Questions go to the error stream and the report goes to the normal output
stream. When nobody is at the keyboard the script uses the example figures.
Save your own copy as ``homework-05-compound-interest.py``.
"""

import sys

LABEL_WIDTH: int = 14
FIELD_WIDTH: int = 11

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
    """Print the five-line compound-interest report."""
    final_amount: float = principal * (1 + rate / 100) ** years
    total_interest: float = final_amount - principal

    print(f"{'Principal':<{LABEL_WIDTH}}: ${principal:>{FIELD_WIDTH},.2f}")
    print(f"{'Rate':<{LABEL_WIDTH}}: {rate:>{FIELD_WIDTH},.2f}%")
    print(f"{'Years':<{LABEL_WIDTH}}: {years:>{FIELD_WIDTH + 1}d}")
    print(f"{'Final amount':<{LABEL_WIDTH}}: ${final_amount:>{FIELD_WIDTH},.2f}")
    print(
        f"{'Total interest':<{LABEL_WIDTH}}: "
        f"${total_interest:>{FIELD_WIDTH},.2f}"
    )


def main() -> None:
    """Read principal, rate, and years, then print the five-line report."""
    principal: float = float(ask("Principal in dollars: ", SAMPLE_PRINCIPAL))
    rate: float = float(ask("Annual interest rate in percent: ", SAMPLE_RATE))
    years: int = int(ask("Number of years: ", SAMPLE_YEARS))
    print_report(principal, rate, years)


if __name__ == "__main__":
    main()
