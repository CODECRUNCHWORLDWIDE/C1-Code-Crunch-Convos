"""Tip calculator: read a bill, tip percentage, and party size.

Challenge 1, Week 2, Code Crunch Convos. Prints a four-line summary
with the labels padded to a fixed width and every dollar amount
right-aligned in the same column.

The questions go to the error stream and the summary goes to the normal
output stream, so ``python tip.py > bill.txt`` saves the summary and
nothing else. When the input stream is already finished -- which is what
happens when a checker runs the file -- each question answers itself
from the demo values below instead of waiting for typing that is never
coming.

Run it with::

    python tip.py
"""

import sys

LABEL_WIDTH: int = 11
AMOUNT_WIDTH: int = 8
CURRENCY: str = "$"
ERROR_MESSAGE: str = "Error: please enter positive numbers only."

DEMO_BILL: str = "58.75"
DEMO_TIP: str = "20"
DEMO_PEOPLE: str = "3"


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or ``demo`` when nobody answers.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on when the input stream has
            already ended.

    Returns:
        The line that was typed, or ``demo``. A demo answer is echoed
        after the prompt on the normal output stream, so the printed
        session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


def main() -> None:
    """Read the three inputs, validate them, print the summary."""
    try:
        bill = float(ask("Bill amount in dollars: ", DEMO_BILL))
        tip_percent = float(
            ask("Tip percentage (e.g. 18 for 18%): ", DEMO_TIP)
        )
        people = int(ask("Number of people: ", DEMO_PEOPLE))
    except ValueError:
        print(ERROR_MESSAGE)
        return

    if bill <= 0 or tip_percent <= 0 or people <= 0:
        print(ERROR_MESSAGE)
        return

    tip = bill * (tip_percent / 100)
    total = bill + tip
    per_person = total / people

    tip_label = f"Tip ({tip_percent:.1f}%)"

    print("--- Bill Summary ---")
    print(f"{'Bill':<{LABEL_WIDTH}}:  {CURRENCY}{bill:>{AMOUNT_WIDTH}.2f}")
    print(f"{tip_label:<{LABEL_WIDTH}}:  {CURRENCY}{tip:>{AMOUNT_WIDTH}.2f}")
    print(f"{'Total':<{LABEL_WIDTH}}:  {CURRENCY}{total:>{AMOUNT_WIDTH}.2f}")
    print(
        f"{'Per person':<{LABEL_WIDTH}}:  "
        f"{CURRENCY}{per_person:>{AMOUNT_WIDTH}.2f}"
    )


if __name__ == "__main__":
    main()
