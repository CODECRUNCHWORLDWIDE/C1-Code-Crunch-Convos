# Mini-Project — Personal Finance Calculator

> Time: about 6 hours. Difficulty: this is the main capstone for Week 4.

## Overview

Build a small command-line program that helps a user understand their personal finances. The user enters their monthly income sources and monthly expenses, and your program reports:

- Total monthly income.
- Total monthly expenses.
- Monthly savings (income minus expenses).
- Savings rate (savings as a percentage of income).
- Projected savings over **N** months at the current rate.

The point of this project is **not** to make a beautiful UI — it is to practice splitting a program across multiple files with a clean interface.

## Required file structure

Your finished project must have these four files:

```text
mini-project/
    README.md               # this file
    starter/                # starter code (read-only reference)
    your-solution/          # your work goes here
        main.py             # entry point and CLI
        income.py           # income data and helpers
        expenses.py         # expense data and helpers
        report.py           # formatting and projection
```

You can name the working folder anything you want as long as it contains the four files above.

## What each file is for

### `income.py`

- Owns the concept of "income source".
- Public functions:
  - `add_income(sources: list[dict], label: str, amount: float) -> list[dict]` — append a new source.
  - `total_income(sources: list[dict]) -> float` — sum the amounts.
- Each "source" is a dict with two keys: `"label"` (str) and `"amount"` (float).
- Has a `_demo()` function and the `if __name__ == "__main__":` guard.

### `expenses.py`

- Owns the concept of "expense".
- Public functions:
  - `add_expense(items: list[dict], label: str, amount: float) -> list[dict]` — append a new expense.
  - `total_expenses(items: list[dict]) -> float` — sum the amounts.
- Each "item" is a dict with `"label"` and `"amount"`.
- Has a `_demo()` and the `__main__` guard.

### `report.py`

- Pure computation and formatting. No I/O.
- Public functions:
  - `savings_rate(income: float, expenses: float) -> float` — return savings as a percentage of income (0–100). Return `0.0` if `income == 0`.
  - `project_savings(monthly_savings: float, months: int) -> float` — return `monthly_savings * months`. Raise `ValueError` if `months < 0`.
  - `format_report(income: float, expenses: float, months: int) -> str` — return a multi-line string with the full report.
- Has a `_demo()` and the `__main__` guard.

### `main.py`

- The entry point.
- Imports the other three modules.
- Defines `main()` and guards it with `if __name__ == "__main__":`.
- Drives the user through:
  1. A short banner.
  2. A loop to collect income sources.
  3. A loop to collect expenses.
  4. A prompt for the projection horizon in months.
  5. A printed report from `report.format_report`.

`main.py` is the only file allowed to call `print` and `input`. Everything else should be functions that return values.

## Sample interaction

```text
$ python main.py
== Personal Finance Calculator ==

Enter income sources. Blank label to stop.
  Label: salary
  Amount: 2500
  Label: freelance
  Amount: 400
  Label:

Enter expenses. Blank label to stop.
  Label: rent
  Amount: 900
  Label: food
  Amount: 350
  Label: transport
  Amount: 120
  Label:

Project savings over how many months? 12

------------------------------
Personal Finance Report
------------------------------
Income:            $2900.00
Expenses:          $1370.00
Monthly savings:   $1530.00
Savings rate:        52.76%
Projected (12 mo): $18360.00
------------------------------
```

## Constraints and quality rules

- Every public function has a one-line docstring per [PEP 257](https://peps.python.org/pep-0257/).
- Every parameter and return value has a type hint.
- No function exceeds 25 lines (re-read the [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) tutorial if you are tempted to write a giant function).
- `report.py` must be free of `print` and `input`. It is a pure computation module.
- `main.py` validates user input: if a non-numeric amount is entered, prompt again rather than crashing.
- Use the [`__main__` idiom](https://docs.python.org/3/library/__main__.html) in every file.

## Rubric (out of 100)

| Section | Points | What you have to show |
|---------|--------|-----------------------|
| File structure | 15 | All four files present, named correctly, in one folder. |
| `income.py` | 15 | Functions match the spec; type hints; docstrings; `_demo()` runs. |
| `expenses.py` | 15 | Same as income.py. |
| `report.py` | 20 | Pure computation; `savings_rate`, `project_savings`, `format_report` correct; no I/O. |
| `main.py` | 20 | Full CLI flow; robust to bad input; uses the three modules. |
| Style | 10 | PEP 8 compliance; consistent naming; no wildcard imports. |
| Bonus stretch | +5 | One of the stretch goals below, clearly documented. |

## Stretch goals

- Add a `--income FILE` and `--expenses FILE` CLI flag using [`argparse`](https://docs.python.org/3/library/argparse.html) so the user can load entries from a CSV.
- Add `report.compounded_projection(monthly: float, months: int, monthly_rate: float) -> float` that compounds savings monthly at a given interest rate.
- Add categories to each expense (rent / food / transport / ...) and report totals per category.
- Add unit tests in a `tests/` folder using `pytest`.

## Starter files

A `starter/` folder is provided next to this README. It has the four files with docstrings and TODO comments. **Copy** the folder to `your-solution/` (or any name you like) before editing — do not edit the starter directly. The starter is meant to remain as a reference.

```bash
cp -r starter your-solution
cd your-solution
python main.py
```

## What to learn from this project

- That a multi-file project is not scary once you see the pattern.
- That the entry-point file should be small and orchestration-focused.
- That pure computation modules (`report.py`) are very pleasant to test.
- That a clean separation between "talk to the user" and "compute things" is one of the most important habits in software.

Good luck. Commit often.
