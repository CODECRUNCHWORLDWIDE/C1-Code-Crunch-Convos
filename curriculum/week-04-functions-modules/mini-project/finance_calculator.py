"""Personal Finance Calculator: money in, money out, savings projected.

Mini-project, Week 4, Code Crunch Convos.

The project you hand in is four files -- ``income.py``, ``expenses.py``,
``report.py`` and ``main.py``. This download folds all four into one file, in
that order, so that it runs the moment you save it. Each half-page banner below
marks where one of the four files starts. The page beside this file shows the
real four-file layout, which is the thing the project is really about.

The dependency rule the four files follow survives the folding: everything
above the ``main.py`` banner is pure -- it takes numbers and returns numbers or
strings, and never prints or asks. Only the ``main.py`` section talks to a
person.

Questions go to the error stream and the report goes to the normal output
stream, so ``python finance_calculator.py > report.txt`` saves the report and
none of the interview.

Run it with::

    python finance_calculator.py
"""

import sys
from collections.abc import Callable

# --- income.py -------------------------------------------------------------
#
# A "source" is a dict with exactly two keys: "label" (str) and "amount"
# (float). A collection of sources is a plain list of those dicts.


def add_income(sources: list[dict], label: str, amount: float) -> list[dict]:
    """Return a new list: `sources` plus one more income source."""
    return [*sources, {"label": label, "amount": float(amount)}]


def total_income(sources: list[dict]) -> float:
    """Return the sum of every source's amount, or 0.0 for no sources."""
    return sum((source["amount"] for source in sources), 0.0)


# --- expenses.py -----------------------------------------------------------
#
# An "item" is the same shape as an income source on purpose. The page beside
# this file argues why the two stay separate anyway.


def add_expense(items: list[dict], label: str, amount: float) -> list[dict]:
    """Return a new list: `items` plus one more expense."""
    return [*items, {"label": label, "amount": float(amount)}]


def total_expenses(items: list[dict]) -> float:
    """Return the sum of every item's amount, or 0.0 for no items."""
    return sum((item["amount"] for item in items), 0.0)


# --- report.py -------------------------------------------------------------
#
# Pure arithmetic and layout. Nothing in this section prints or asks.

RULE = "-" * 30
TITLE = "Personal Finance Report"
LABEL_WIDTH = 17
VALUE_WIDTH = 9


def savings_rate(income: float, expenses: float) -> float:
    """Return savings as a percentage of income (0-100), or 0.0 if income is 0."""
    if income == 0:
        return 0.0
    return (income - expenses) / income * 100


def project_savings(monthly_savings: float, months: int) -> float:
    """Return the straight-line total saved over `months`, refusing negatives."""
    if months < 0:
        raise ValueError("months must be zero or positive")
    return monthly_savings * months


def _row(label: str, value: str) -> str:
    """Return one report line: label padded left, value padded right."""
    return f"{label:<{LABEL_WIDTH}} {value:>{VALUE_WIDTH}}"


def format_report(income: float, expenses: float, months: int) -> str:
    """Return the whole report as one multi-line string, no trailing newline."""
    savings = income - expenses
    return "\n".join(
        [
            RULE,
            TITLE,
            RULE,
            _row("Income:", f"${income:.2f}"),
            _row("Expenses:", f"${expenses:.2f}"),
            _row("Monthly savings:", f"${savings:.2f}"),
            _row("Savings rate:", f"{savings_rate(income, expenses):.2f}%"),
            _row(f"Projected ({months} mo):", f"${project_savings(savings, months):.2f}"),
            RULE,
        ]
    )


# --- main.py ---------------------------------------------------------------
#
# The only section that prints or asks anything.

BANNER = "== Personal Finance Calculator =="
INCOME_HEADING = "Enter income sources. Blank label to stop."
EXPENSE_HEADING = "Enter expenses. Blank label to stop."
MONTHS_PROMPT = "Project savings over how many months? "

# add_income and add_expense have the same shape, so `collect` can take either.
Adder = Callable[[list[dict], str, float], list[dict]]

# The interview this file gives itself when its input stream is finished.
DEMO_ANSWERS: list[str] = [
    "salary",
    "2500",
    "freelance",
    "400",
    "",
    "rent",
    "900",
    "food",
    "350",
    "transport",
    "120",
    "",
    "12",
]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on once the demo interview above has run
            out. Every call site passes something that ends its loop, so this
            file can never run forever unattended.

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
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        print(f"{prompt}{answer}".rstrip())
        return answer


def read_amount() -> float:
    """Prompt for an amount until the answer is something `float()` accepts."""
    while True:
        raw = ask("  Amount: ", "0").strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  {raw!r} is not a number. Try again.")


def read_months() -> int:
    """Prompt until the answer is a whole number of months that is >= 0."""
    while True:
        raw = ask(MONTHS_PROMPT, "0").strip()
        try:
            months = int(raw)
        except ValueError:
            print(f"{raw!r} is not a whole number. Try again.")
            continue
        if months < 0:
            print("Months cannot be negative. Try again.")
            continue
        return months


def collect(heading: str, add: Adder) -> list[dict]:
    """Collect label/amount pairs with `add` until a label comes back blank."""
    print(heading)
    entries: list[dict] = []
    while True:
        label = ask("  Label: ", "").strip()
        if not label:
            break
        entries = add(entries, label, read_amount())
    print()
    return entries


def main() -> None:
    """Run the interview and print the report."""
    print(BANNER)
    print()
    sources = collect(INCOME_HEADING, add_income)
    items = collect(EXPENSE_HEADING, add_expense)
    months = read_months()
    print()
    print(format_report(total_income(sources), total_expenses(items), months))


if __name__ == "__main__":
    main()
