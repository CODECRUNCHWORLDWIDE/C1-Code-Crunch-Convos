"""Report module for the Personal Finance Calculator.

Pure computation and formatting. This module MUST NOT call `print`,
`input`, or read/write files. All I/O lives in main.py.

Public functions:
    savings_rate(income, expenses) -> float
    project_savings(monthly_savings, months) -> float
    format_report(income, expenses, months) -> str

This file is part of the Week 4 mini-project. See ../README.md.
"""


def savings_rate(income: float, expenses: float) -> float:
    """Return savings as a percentage of income (0..100).

    The formula is:
        rate = (income - expenses) / income * 100

    Edge case: if income is 0, return 0.0 (do not divide by zero).

    Args:
        income: Total monthly income.
        expenses: Total monthly expenses.

    Returns:
        Percentage of income that is saved. Can be negative if expenses
        exceed income.
    """
    # TODO:
    #   1. If income == 0, return 0.0.
    #   2. Otherwise compute and return the rate.
    raise NotImplementedError("savings_rate is not yet implemented")


def project_savings(monthly_savings: float, months: int) -> float:
    """Project total savings over `months` months at the current monthly rate.

    Args:
        monthly_savings: Net savings per month (income minus expenses).
        months: Number of months to project. Must be >= 0.

    Returns:
        `monthly_savings * months`.

    Raises:
        ValueError: If months is negative.
    """
    # TODO:
    #   1. Validate months (must be >= 0).
    #   2. Return monthly_savings * months.
    raise NotImplementedError("project_savings is not yet implemented")


def format_report(income: float, expenses: float, months: int) -> str:
    """Build a multi-line text report describing the current finances.

    The exact format is up to you, but it must include:
        * Income.
        * Expenses.
        * Monthly savings (income - expenses).
        * Savings rate as a percentage.
        * Projected savings over `months` months.

    Args:
        income: Total monthly income.
        expenses: Total monthly expenses.
        months: Projection horizon in months.

    Returns:
        A multi-line string. Currency formatting is up to you, but
        `$1234.56` is a reasonable default.
    """
    # TODO:
    #   1. Compute monthly_savings = income - expenses.
    #   2. Compute rate = savings_rate(income, expenses).
    #   3. Compute projected = project_savings(monthly_savings, months).
    #   4. Build and return a multi-line string with the labels listed above.
    #   Hint: f-strings with the :.2f format spec give two-decimal formatting.
    raise NotImplementedError("format_report is not yet implemented")


def _demo() -> None:
    """Print a small self-demo when this file is run directly."""
    print(format_report(income=2900.0, expenses=1370.0, months=12))


if __name__ == "__main__":
    _demo()
