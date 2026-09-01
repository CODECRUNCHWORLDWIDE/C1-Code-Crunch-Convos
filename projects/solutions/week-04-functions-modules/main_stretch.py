"""Stretch entry point: the same calculator, driven by CLI flags and CSV files.

Uses `argparse` for flags and `csv` for input files. Both are standard library.
Note that file reading is Week 6 material -- if you have not got there yet, read
`load_csv` as "open the file, hand me one dict per row" and move on.

Examples:
    python main_stretch.py --income sample-income.csv \\
        --expenses sample-expenses.csv --months 12 --rate 0.004
    python main_stretch.py --months 6          # still interactive
"""

import argparse
import csv

import expenses
import income
import main
import report
import report_stretch


def parse_args() -> argparse.Namespace:
    """Return the parsed command-line flags."""
    parser = argparse.ArgumentParser(description="Personal finance calculator.")
    parser.add_argument("--income", help="CSV with label,amount columns")
    parser.add_argument("--expenses", help="CSV with label,amount[,category] columns")
    parser.add_argument("--months", type=int, help="projection horizon in months")
    parser.add_argument(
        "--rate",
        type=float,
        default=0.0,
        help="monthly interest rate as a fraction, e.g. 0.004 for 0.4%%",
    )
    return parser.parse_args()


def load_csv(path: str, add: main.Adder) -> list[dict]:
    """Return entries read from `path`, one per CSV row, built with `add`."""
    entries: list[dict] = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            entries = add(entries, row["label"], float(row["amount"]))
            if row.get("category"):
                entries[-1]["category"] = row["category"]
    return entries


def gather(path: str | None, heading: str, add: main.Adder) -> list[dict]:
    """Return entries from `path` if given, otherwise ask the user for them."""
    if path is None:
        return main.collect(heading, add)
    return load_csv(path, add)


def main_stretch() -> None:
    """Run the calculator with flags, falling back to prompts for anything missing."""
    args = parse_args()
    sources = gather(args.income, main.INCOME_HEADING, income.add_income)
    items = gather(args.expenses, main.EXPENSE_HEADING, expenses.add_expense)
    months = args.months if args.months is not None else main.read_months()
    total_in = income.total_income(sources)
    total_out = expenses.total_expenses(items)
    print()
    print(report.format_report(total_in, total_out, months))
    print(report_stretch.format_categories(items))
    grown = report_stretch.compounded_projection(total_in - total_out, months, args.rate)
    print(f"Compounded at {args.rate * 100:.2f}%/mo: ${grown:.2f}")


if __name__ == "__main__":
    main_stretch()
