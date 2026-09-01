"""Pure computation and formatting for the finance report.

Every public function here takes numbers and returns a number or a string.
Nothing in this module calls `input`, opens a file, or keeps state between
calls. The one `print` in the file sits under the `__main__` guard, so it never
runs on import -- see 00-overview.md, "The report.py print rule".
"""

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


def _demo() -> str:
    """Return the report for the numbers printed in the mini-project brief."""
    return format_report(2900.0, 1370.0, 12)


if __name__ == "__main__":
    print(_demo())
