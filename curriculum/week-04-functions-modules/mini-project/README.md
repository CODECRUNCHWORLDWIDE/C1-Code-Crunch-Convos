# Mini-Project — Personal Finance Calculator

> **Topic:** four files that each know one thing, arranged so that the dependencies only ever point one way
> **Lecture:** [04 — Modules and Imports](../lecture-notes/04-modules-and-imports.md)
> **Difficulty:** no single function here is hard; deciding which file each function belongs in is the whole project
> **Target time:** 4–6 hours, spread over more than one sitting
> **Why this one:** it is the first program you cannot hold in your head all at once, and the first time the answer to "where does this code go?" has a real reason behind it rather than a shrug.

<!-- no-runnable-file: this page is the project brief, and the project's deliverable is a folder in your own repository holding four files, a commit history, and a session you can show somebody. The runnable answer is finance_calculator.py, which ships beside this page and is linked from Download and run. It is named after the project rather than the page because a file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

This is the capstone of Week 4. You are building a small program that
asks somebody about their money and tells them what it means:

- what comes in every month,
- what goes out every month,
- what is left over,
- what fraction of the income that leftover is,
- and how much it adds up to over the next N months.

The arithmetic is subtraction, division and multiplication. If the whole
thing were one file it would be about eighty lines and you could write
it this afternoon.

**It is not one file. It is four**, and that is the project.

```text
main.py         talks to a person      prints, asks, validates
income.py       what an income source is, and how to total them
expenses.py     what an expense is, and how to total them
report.py       the arithmetic and the layout
```

The rule those four files obey is one sentence long:

> `main.py` knows about the other three. None of the other three has
> ever heard of `main.py`.

Draw it and it is a fan, not a web:

```text
main.py
    |
    +-- income.py
    +-- expenses.py
    +-- report.py
```

Everything below `main.py` is **pure**: give it numbers, it gives you
numbers or a string back. No printing. No asking. No remembering
anything between calls. Only `main.py` is allowed to touch a keyboard or
a screen.

**Why go to that trouble for eighty lines?** Three payoffs, and you feel
all three before the project is finished.

1. **The interesting code becomes checkable.** You can call
   `savings_rate(2900, 1370)` and look at the answer. You cannot "call"
   a prompt. By pushing every decision that has a right answer out of
   `main.py`, the file you *cannot* check shrinks to something you can
   verify by reading it.
2. **The files cannot tangle.** `report.py` has no reason to reach back
   for anything `main.py` owns, so the two can never end up importing
   each other — which is a real error with a confusing message, and
   *Common bugs to catch* shows it.
3. **The boundaries start meaning something.** `income.py` is not "the
   file where I put income stuff". It is the file that **defines what an
   income source is**. Add a currency later and exactly one file
   changes.

Here is the session the finished program should produce:

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

> *As a* learner who can write functions and import a module,
> *I want* to build something out of four files that each know one
> thing,
> *so that* I find out what "where does this code go?" actually means.

## Starter

Four files, in a folder of your own — `week-04-finance/` beside your
other Week 4 work is fine. Save all four, run all four, and only then
start filling in the TODOs. They run as pasted.

`income.py`:

```python
"""TODO: one line saying what an income source is."""


def add_income(sources: list[dict], label: str, amount: float) -> list[dict]:
    """Return a new list: `sources` plus one more income source."""
    return [*sources, {"label": label, "amount": float(amount)}]


def total_income(sources: list[dict]) -> float:
    """Return the sum of every source's amount, or 0.0 for no sources."""
    # TODO 1: add up the amounts. Start the sum at 0.0, not 0.
    return 0.0


def _demo() -> str:
    """Return a short demonstration of this module's two public functions."""
    sources = add_income([], "salary", 2500)
    return f"sources: {sources}\ntotal_income: {total_income(sources):.2f}"


if __name__ == "__main__":
    print(_demo())
```

`expenses.py`:

```python
"""TODO: one line saying what an expense item is."""


def add_expense(items: list[dict], label: str, amount: float) -> list[dict]:
    """Return a new list: `items` plus one more expense."""
    # TODO 2: the same shape as add_income, with the words changed.
    return items


def total_expenses(items: list[dict]) -> float:
    """Return the sum of every item's amount, or 0.0 for no items."""
    # TODO 3: the same shape as total_income.
    return 0.0


def _demo() -> str:
    """Return a short demonstration of this module's two public functions."""
    items = add_expense([], "rent", 900)
    return f"items: {items}\ntotal_expenses: {total_expenses(items):.2f}"


if __name__ == "__main__":
    print(_demo())
```

`report.py`:

```python
"""TODO: one line saying what this file computes. It must not print or ask."""

RULE = "-" * 30
TITLE = "Personal Finance Report"
LABEL_WIDTH = 17
VALUE_WIDTH = 9


def savings_rate(income: float, expenses: float) -> float:
    """Return savings as a percentage of income (0-100), or 0.0 if income is 0."""
    # TODO 4: guard the zero divisor first, then do the division.
    return 0.0


def project_savings(monthly_savings: float, months: int) -> float:
    """Return the straight-line total saved over `months`, refusing negatives."""
    # TODO 5: raise ValueError("months must be zero or positive") when months < 0.
    return monthly_savings * months


def _row(label: str, value: str) -> str:
    """Return one report line: label padded left, value padded right."""
    return f"{label:<{LABEL_WIDTH}} {value:>{VALUE_WIDTH}}"


def format_report(income: float, expenses: float, months: int) -> str:
    """Return the whole report as one multi-line string, no trailing newline."""
    savings = income - expenses
    # TODO 6: the five _row lines, between the rules and the title.
    return "\n".join([RULE, TITLE, RULE, _row("Income:", f"${income:.2f}"), RULE])


def _demo() -> str:
    """Return the report for the numbers printed in the brief."""
    return format_report(2900.0, 1370.0, 12)


if __name__ == "__main__":
    print(_demo())
```

`main.py`:

```python
"""TODO: one line saying what this file does."""

import sys
from collections.abc import Callable

import expenses
import income
import report

BANNER = "== Personal Finance Calculator =="
INCOME_HEADING = "Enter income sources. Blank label to stop."
EXPENSE_HEADING = "Enter expenses. Blank label to stop."
MONTHS_PROMPT = "Project savings over how many months? "

Adder = Callable[[list[dict], str, float], list[dict]]

DEMO_ANSWERS: list[str] = ["salary", "2500", "", "", "12"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        print(f"{prompt}{answer}".rstrip())
        return answer


def read_amount() -> float:
    """Prompt for an amount until the answer is something `float()` accepts."""
    # TODO 7: loop until float(raw) works, complaining in between.
    return float(ask("  Amount: ", "0").strip())


def read_months() -> int:
    """Prompt until the answer is a whole number of months that is >= 0."""
    # TODO 8: loop until int(raw) works AND the answer is not negative.
    return int(ask(MONTHS_PROMPT, "0").strip())


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
    sources = collect(INCOME_HEADING, income.add_income)
    items = collect(EXPENSE_HEADING, expenses.add_expense)
    months = read_months()
    print()
    print(report.format_report(income.total_income(sources), expenses.total_expenses(items), months))


if __name__ == "__main__":
    main()
```

Run each of the four, in that order:

```text
$ python income.py
sources: [{'label': 'salary', 'amount': 2500.0}]
total_income: 0.00
```

```text
$ python expenses.py
items: []
total_expenses: 0.00
```

```text
$ python report.py
------------------------------
Personal Finance Report
------------------------------
Income:            $2900.00
------------------------------
```

```text
$ python main.py
== Personal Finance Calculator ==

Enter income sources. Blank label to stop.
  Label: salary
  Amount: 2500
  Label:

Enter expenses. Blank label to stop.
  Label:

Project savings over how many months? 12

------------------------------
Personal Finance Report
------------------------------
Income:               $0.00
------------------------------
```

Nothing is broken. Every total is `0` and the report has one row,
because those are the TODOs. What already works is the *wiring*: four
files, three imports, one interview, one report. You are filling in
bodies, not building scaffolding.

**About `ask()`.** It is given to you and you never have to write one.
It asks a question and reads a line. If nobody is there to answer, it
takes the next line out of `DEMO_ANSWERS` instead and prints it, so the
file always produces a whole session. The question goes to the **error
stream** and the answer goes to the **normal output stream** — *The
Solution* explains why that split is worth having.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](../../../README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Four files, named exactly `income.py`, `expenses.py`, `report.py` and
   `main.py`, in one folder.
2. `income.py` exposes
   `add_income(sources: list[dict], label: str, amount: float) -> list[dict]`
   and `total_income(sources: list[dict]) -> float`. A source is a dict
   with exactly two keys, `"label"` and `"amount"`.
3. `expenses.py` exposes `add_expense` and `total_expenses`, with the
   same shapes.
4. `report.py` exposes:
   - `savings_rate(income: float, expenses: float) -> float`, returning
     savings as a percentage of income from 0 to 100, and `0.0` when
     income is `0`.
   - `project_savings(monthly_savings: float, months: int) -> float`,
     returning `monthly_savings * months`, and raising `ValueError` when
     `months` is negative.
   - `format_report(income: float, expenses: float, months: int) -> str`,
     returning the whole report as one string.
5. `main.py` imports the other three, prints the banner, collects income
   sources, collects expenses, asks for the horizon in months, and
   prints the report.
6. Both collection loops stop when the label comes back blank.
7. A non-numeric amount prints `  '<what you typed>' is not a number. Try again.`
   and asks for the amount again, without losing the label.
8. A non-numeric month count prints
   `'<what you typed>' is not a whole number. Try again.`; a negative
   one prints `Months cannot be negative. Try again.`. Two problems, two
   messages, and both ask again.
9. Every file has a `_demo()` and an `if __name__ == "__main__":` guard,
   so `python income.py` shows you that module working on its own.
10. Every public function has type hints on the parameters and the
    return, and a one-line docstring.

## Constraints

- **`main.py` is the only file that prints or asks.** The other three
  take values and return values. This is the constraint the whole
  project exists to teach, and it is worth 20 rubric points on
  `report.py` alone.
- **Dependencies point one way.** `main` imports the other three;
  none of them imports `main`, and none of them imports each other.
  There is no clever import order that makes a circle work.
- **No function is longer than 25 lines.** If `main()` starts creeping
  past it, the collection loop wants to be its own function. That is
  exactly how `collect`, `read_amount` and `read_months` came to exist.
- **`report.py` must contain no `print` and no `input`** anywhere a
  caller can reach. Its `_demo()` **returns** the report string; the one
  `print` in the file sits under the `__main__` guard where an import
  can never run it. The brief asks for two things that pull against each
  other here — see *The Solution* for the reasoning.
- **Sum with an explicit float start: `sum(..., 0.0)`.** `sum` starts at
  the integer `0` by default, so an empty list gives you `0`, an `int`,
  and your `-> float` type hint becomes a lie. Three characters fix it.
- **Standard library only**, and only `sys` and `collections.abc`.
- **Runs on Python 3.10 or newer**, from inside its own folder.

## Expected output

The downloadable answer is the four files folded into one — see
*Download and run* for why, and *The Solution* for where the seams are.
Run it with nothing attached to its input and it interviews itself. Real
stdout on CPython 3.13.2:

```text
$ python finance_calculator.py
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

That is the brief's own session, line for line. Check the arithmetic:
`2500 + 400` is `2900`, `900 + 350 + 120` is `1370`, the difference is
`1530`, `1530 / 2900` is `0.5276…` which prints as `52.76%`, and
`1530 × 12` is `18360`.

**Now the part the happy session does not cover.** Feed it three bad
answers and watch it survive all three:

```text
$ printf 'salary\ntwelve hundred\n2500\n\n\nabc\n-3\n6\n' | python finance_calculator.py
== Personal Finance Calculator ==

Enter income sources. Blank label to stop.
  'twelve hundred' is not a number. Try again.

Enter expenses. Blank label to stop.

'abc' is not a whole number. Try again.
Months cannot be negative. Try again.

------------------------------
Personal Finance Report
------------------------------
Income:            $2500.00
Expenses:             $0.00
Monthly savings:   $2500.00
Savings rate:       100.00%
Projected (6 mo): $15000.00
------------------------------
```

The prompts are missing because they go to the error stream, which is
why the complaints stand out so clearly. Read it against the
requirements:

| Input | What should happen | The line it produced |
|---|---|---|
| `twelve hundred` | not a number, ask again, keep `salary` | `'twelve hundred' is not a number. Try again.` |
| *(blank label)* | stop collecting income | moves on to expenses |
| *(blank label)* | stop collecting expenses, with none entered | `Expenses: $0.00`, no crash |
| `abc` | not a whole number of months | `'abc' is not a whole number. Try again.` |
| `-3` | a whole number, but negative — a **different** message | `Months cannot be negative. Try again.` |
| `6` | accepted | `Projected (6 mo): $15000.00` |

Two details in that report are worth staring at. `Expenses: $0.00` is
`sum(..., 0.0)` earning its keep — an empty list totalled cleanly
instead of crashing. And `Projected (6 mo):` is 17 characters, so unlike
the 12-month row it fits the label column exactly and the line is one
character shorter. *The Solution* explains the column arithmetic.

And the promise `project_savings` makes:

```text
$ python -c "import finance_calculator as fc; fc.project_savings(100.0, -1)"
ValueError: months must be zero or positive
```

## Steps

Build it in the order the files depend on each other, and run each one
on its own before you wire it into the next.

1. Save all four starter files into your folder and run all four. You
   should see the four sessions above. Do not go on until they all run.

2. Do **TODO 1** in `income.py`:

   ```python
   return sum((source["amount"] for source in sources), 0.0)
   ```

   Run `python income.py`. You want `total_income: 2500.00`.

3. Do **TODO 2** and **TODO 3** in `expenses.py`. They are `income.py`
   with the words changed. Run `python expenses.py`. You want
   `total_expenses: 900.00`.

   You will be tempted to merge the two files. Read the argument in
   *The Solution* first — it is the most interesting design decision in
   the project, and the answer is not the obvious one.

4. Do **TODO 4**, `savings_rate`. Two lines, and the order matters:

   ```python
   if income == 0:
       return 0.0
   return (income - expenses) / income * 100
   ```

   Check it at the REPL — `python -i report.py`, then
   `savings_rate(2900, 1370)`, `savings_rate(0, 0)` and
   `savings_rate(1000, 1500)`. That last one should give `-50.0`, which
   is correct and means "you overspent by half your income".

5. Do **TODO 5**, `project_savings`. One `if`, one `raise`.

6. Do **TODO 6**, the report body. Five `_row` calls between the title
   and the last rule:

   ```python
   _row("Income:", f"${income:.2f}"),
   _row("Expenses:", f"${expenses:.2f}"),
   _row("Monthly savings:", f"${savings:.2f}"),
   _row("Savings rate:", f"{savings_rate(income, expenses):.2f}%"),
   _row(f"Projected ({months} mo):", f"${project_savings(savings, months):.2f}"),
   ```

   Run `python report.py` and compare it to the block in *Expected
   output* **character by character**, including the spaces. Column
   alignment is the fiddly part of this project and the easiest thing to
   get almost right.

7. Do **TODO 7**, `read_amount`. Wrap the existing line in
   `while True:` with a `try` / `except ValueError` that prints the
   complaint and lets the loop go round again.

8. Do **TODO 8**, `read_months`. Same shape, plus one extra check:
   `int("-3")` succeeds, so a negative horizon gets past the conversion
   and has to be rejected on its own line, with its own message.

9. Run the two sessions from *Expected output* and compare them.

10. Delete `main.py` and write it again from a blank page, with the
    other three files still there. It takes about fifteen minutes the
    second time, and the second time is the one that proves you have
    Week 4.

11. Commit and push:

    ```bash
    git add week-04-finance/
    git commit -m "Week 4 mini-project: personal finance calculator"
    git push
    ```

## The Solution

```python
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
```

**The download is one file, and the project is four. Here is why.**
Every page in this course ships one file you can download and run. A
four-file project cannot be one download without a zip, and a zip is a
thing you have to unpack before you can read it. So the answer above is
the four files stacked in order, with a comment banner where each one
starts. Cut at the banners, add `import expenses`, `import income` and
`import report` to the top of the last piece, and put `income.`,
`expenses.` and `report.` in front of the eight calls that cross a
boundary. Nothing else changes. **The four-file version is what the
brief asks for and what gets graded** — this one is here so you can run
the answer in ten seconds.

Notice what survived the folding. The three pure sections still contain
no `print` and no `input`. The rule is not enforced by the file
boundaries; the file boundaries just make it obvious when you break it.

**`add_income` returns a new list instead of changing the one it was
given.**

```python
return [*sources, {"label": label, "amount": float(amount)}]
```

`[*sources, x]` means "a brand new list: everything in `sources`, then
`x`". The old list is untouched. The alternative — `sources.append(...)`
then `return sources` — is legal too, and the brief allows either.

*The tradeoff.* Appending is instant. Building a new list copies every
existing entry, so on a million entries appending wins easily. On a
personal budget with nine line items that cost is invisible, and what
you buy with it is a guarantee: `add_income` cannot surprise a caller by
changing something the caller is still holding. Same inputs, same
output, nothing else touched. You can call it in any order, from
anywhere, and reason about it without looking anywhere else.

It also closes off a whole family of bugs at the root — see the mutable
default under *Common bugs to catch*, which can only bite a function
that changes things.

Whichever you choose, be consistent. If you append and return the same
list, then `entries = add(entries, ...)` in `collect` is a white lie:
the assignment does nothing, because `entries` was already changed.

**`income.py` and `expenses.py` stay separate even though they are
twins.** Put them side by side and they are the same file with four
words changed. Every instinct you have been taught about not repeating
yourself says merge them into one `entries.py` with `add_entry` and
`total_entries`.

Do not, and here is the reason. The duplication is **coincidental**, not
structural. Income and expenses look alike *today* because both happen
to be a label and an amount. They come apart the moment the program
grows: expenses want a category (that is literally one of the stretch
goals below), income wants a pay frequency, expenses want a due date. A
merged module would grow optional parameters that mean nothing to half
its callers.

The rule of thumb worth keeping: **deduplicate behaviour that must
change together, not code that currently looks similar.** Two functions
that would change for different reasons belong in different files even
when they are identical today.

And notice what the answer *does* deduplicate. `collect` is written once
and takes the adder as a parameter:

```python
Adder = Callable[[list[dict], str, float], list[dict]]


def collect(heading: str, add: Adder) -> list[dict]:
```

That is a function taking a function — the same idea as the dispatch
table in Challenge 1. Here it is right, because the prompting loop
genuinely *is* one behaviour: if you change how the loop stops, you want
it changed for income and expenses at the same time. That is the test.

**`format_report` works out `savings` itself instead of being handed
it.** The signature is fixed at three parameters, so
`savings = income - expenses` happens inside. It could have taken four.

Three is better because four lets a caller pass numbers that disagree —
income 2900, expenses 1370, savings 5 — and the report would print
something impossible without a word of complaint. Three makes that state
impossible to express. **Derive what you can derive; only accept what
you cannot.**

**`format_report` calls `project_savings`, so it inherits the
`ValueError`.**

```python
_row(f"Projected ({months} mo):", f"${project_savings(savings, months):.2f}"),
```

`format_report(2900, 1370, -1)` raises, even though requirement 4 only
attaches that rule to `project_savings`. That is deliberate: there is
exactly one definition of "a valid horizon" in the project, and both
ways in get it for free. Validating again inside `format_report` would
be two places to keep in step, and one of them would eventually be
forgotten.

The cost is that a formatting function can raise. `read_months` pays it
by never letting a negative number reach the report — which is where
validation belongs, at the boundary with the human.

**The column arithmetic, which is most of the fiddly work.**

```python
LABEL_WIDTH = 17
VALUE_WIDTH = 9


def _row(label: str, value: str) -> str:
    """Return one report line: label padded left, value padded right."""
    return f"{label:<{LABEL_WIDTH}} {value:>{VALUE_WIDTH}}"
```

Two things are happening in that f-string. `:<` pads on the right so the
text sits left; `:>` pads on the left so the text sits right. And the
width is itself in braces — `{LABEL_WIDTH}` *inside* the format spec.
That is a **nested replacement field**: Python works out the inner
braces first to get `17`, producing the spec `:<17`. It is how you set a
width from a variable instead of typing `:<17` in six places.

The numbers are not arbitrary. `Monthly savings:` is the longest fixed
label at 16 characters, so 17 guarantees at least one space before the
value. `$18360.00` is 9 characters, so the money column right-aligns
without being cut off.

The last row is the interesting one. `Projected (12 mo):` is **18**
characters — wider than `LABEL_WIDTH`. Python's `<` pads to a *minimum*
width and never truncates, so the label prints in full and that one line
comes out a character wider than the rest. The brief's own sample shows
exactly that. Measure the nine lines of the report and you get
`[30, 23, 30, 27, 27, 27, 27, 28, 30]` — the 28 is that row. If your
numbers differ, you truncated where you should have padded.

**`sum` with an explicit `0.0` start.**

```python
return sum((source["amount"] for source in sources), 0.0)
```

`sum` starts at the integer `0` unless you say otherwise. Total an empty
list and you get `0` — an `int`, not the `float` the type hint promises.
Passing `0.0` makes the hint honest for every input including the empty
one. Three characters, and it is the difference between a type hint that
documents and a type hint that lies.

The thing in the brackets is a **generator expression**, not a list
comprehension: it hands `sum` one amount at a time instead of building a
list first. At nine budget lines that makes no measurable difference.
The habit is what you are practising.

**The zero-income guard, and what it deliberately does not guard.**

```python
if income == 0:
    return 0.0
return (income - expenses) / income * 100
```

Without it, `savings_rate(0, 0)` — a perfectly reasonable thing for
somebody with no income yet to trigger — crashes the program. Note that
the guard checks `income`, which is the divisor, and **not**
`income - expenses`. A negative rate is fine and meaningful:
`savings_rate(1000, 1500)` returns `-50.0`, meaning "you overspent by
half your income". A guard that swallowed that would be hiding the most
important number on the page.

**`report.py` must not print, and must have a `_demo()`. Both.** The
brief asks for two things that pull against each other: `report.py` is a
pure computation module with no I/O, *and* every file needs a `_demo()`
under a `__main__` guard. A demo that cannot print has nothing to
demonstrate.

The resolution is one line:

```python
def _demo() -> str:
    """Return the report for the numbers printed in the mini-project brief."""
    return format_report(2900.0, 1370.0, 12)


if __name__ == "__main__":
    print(_demo())
```

`_demo()` **returns** a string and stays pure. The single `print` sits
under the guard, where an import can never reach it. Everything another
file can call is still completely free of I/O. Spotting a contradiction
in a brief and writing down how you resolved it is worth more than
quietly picking one side.

**`ask()` puts the questions on the other stream.** A program has two
ways to send text out: `stdout`, the normal output stream, for its
results, and `stderr`, the error stream, for everything else. `ask()`
prints the question to `stderr` with `end=""` so the cursor stays on the
line, and `flush=True` so the question appears *before* the program
starts waiting instead of sitting in a buffer. Then it calls `input()`
with **no argument at all**.

That last detail is the one people get wrong. `input("  Amount: ")`
prints its prompt to `stdout`, mixed into the report. Keeping them apart
is what makes this work:

```bash
python finance_calculator.py > report.txt
```

`report.txt` holds the report and none of the interview. That is not a
trick to make a checker happy — it is how every well-behaved
command-line tool on your machine already works, which is why you can
pipe one into another.

## Download and run

Download [finance_calculator.py](./finance_calculator.py) and run it:

```bash
python finance_calculator.py
```

In your own terminal it interviews you. Run by a script, or with its
input closed, it interviews itself from `DEMO_ANSWERS` and prints the
session in *Expected output*.

You can also feed it answers from the shell, one line per question:

```bash
printf 'salary\n2500\n\n\n12\n' | python finance_calculator.py
```

Because the questions go to the error stream, `>` captures the report on
its own:

```bash
python finance_calculator.py > report.txt
```

**One file, four files.** `finance_calculator.py` is the four-file
project stacked into a single download, with a comment banner where each
file starts — a page's answer is one file you can click and run, and a
four-file project cannot be that without a zip. It is named after the
project rather than after this page because a file called `README.py`
would be a strange thing to ask anybody to download.

**What you hand in is the folder, not this file.** `income.py`,
`expenses.py`, `report.py` and `main.py`, in a folder in your own
repository, with the commit history that built them and a session you
can show somebody. *The Solution* shows exactly where to cut.

## Common bugs to catch

**You divided before checking.** The single most common crash in this
project:

```python
def savings_rate(income: float, expenses: float) -> float:
    return (income - expenses) / income * 100
```

```text
Traceback (most recent call last):
  File "report.py", line 12, in <module>
    savings_rate(0, 0)
    ~~~~~~~~~~~~^^^^^^
  File "report.py", line 2, in savings_rate
    return (income - expenses) / income * 100
           ~~~~~~~~~~~~~~~~~~~~^~~~~~~~
ZeroDivisionError: division by zero
```

It passes every test you run by hand, because by hand you always type in
some income. It fails the first time a real person presses Enter on the
income loop without adding anything.

**The mutable default.** Some people reorder the parameters so the list
can have a default value:

```python
def add_income_bad(label, amount, sources=[]):
    sources.append({"label": label, "amount": amount})
    return sources
```

No error. That is what makes it dangerous:

```text
[{'label': 'salary', 'amount': 2500}]
[{'label': 'rent', 'amount': 900}]
```

is what you expected from two separate calls. What you get is:

```text
[{'label': 'salary', 'amount': 2500}]
[{'label': 'salary', 'amount': 2500}, {'label': 'rent', 'amount': 900}]
```

The second call was supposed to start from an empty list. The `[]` in
the signature was created **once**, when the `def` line ran, and every
call that leaves `sources` out shares that same list forever. The brief
makes `sources` a required parameter, which sidesteps the trap entirely
— take the hint.

**Circular imports.** You want the banner in `report.py`, so you reach
for it:

```text
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    from report import format_report
  File "report.py", line 1, in <module>
    from main import BANNER
  File "main.py", line 1, in <module>
    from report import format_report
ImportError: cannot import name 'format_report' from 'report'
```

Read that stack carefully. `main` starts loading, imports `report`,
`report` imports `main`, and `main` is still half-built — it has not
reached the line that defines anything yet. The error blames `report`,
which is the wrong file, and that is why this one costs people an hour.

The fix is never a clever import order. It is the dependency rule from
*The Brief*: arrows point one way. A constant both files need belongs in
the file lower down the stack, or in a third module they both import.

**`ModuleNotFoundError` from the wrong folder.**

```text
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    import income
ModuleNotFoundError: No module named 'income'
```

Python looks for `income.py` next to **the script it was told to run**,
not in the folder you happen to be standing in. `python
week-04-finance/main.py` works from anywhere, because
`week-04-finance/` is what goes on the search path. A `main.py`
somewhere else that expects to find `income.py` in your shell's current
folder does not. `cd` into the project folder first.

**You let `float(input(...))` crash.** A bare
`float(input("  Amount: "))` throws
`ValueError: could not convert string to float: 'twelve hundred'` and
drops the entire session — every label the user has typed so far, gone.
Requirement 7 asks for a loop that re-prompts, which is what
`read_amount` is.

**`read_months` needs a second guard that `read_amount` does not.**
`int("-3")` succeeds. A negative horizon sails past the conversion and
has to be rejected on a line of its own, with its own message.
Requirement 8 asks for two messages precisely because there are two
different problems.

**`report.py` prints at module level.** If your `report.py` has a
top-level `print(format_report(...))` with no guard, then
`import report` in `main.py` dumps a report on the screen before your
banner does. The output looks haunted, and nothing about the traceback
helps, because there is no traceback. The guard is not decoration.

**Your columns are almost right.** One space out somewhere, and the
program is still correct while the report no longer matches. Compare
against *Expected output* character by character, and check the
`Projected (12 mo):` row specifically — it is the one that is
deliberately a character wider than the rest.

**`Expenses: $0` instead of `$0.00`.** You summed with the default start
value, got an `int`, and `f"${0:.2f}"` would still have printed `$0.00`
— so if you are seeing `$0`, you also dropped the `.2f`. Both are worth
fixing: the format string for what the user sees, and `sum(..., 0.0)`
for what the type hint promises.

## Under the hood

<details>
<summary>Under the hood — what import actually does, and why the second one is free</summary>

`import income` sounds like it pastes the text of `income.py` into
`main.py`. It does not. It runs `income.py` once, wraps every name that
file defined into a single **module object**, and hands you that object.

You can look straight at it:

```text
>>> import calculator
>>> type(calculator)
<class 'module'>
>>> calculator
<module 'calculator' from '.../calc/calculator.py'>
>>> sorted(n for n in vars(calculator) if not n.startswith('__'))
['_self_test', 'add', 'divide']
```

A module is a value, like a list or a number. `income.total_income` is
an attribute lookup on that value, the same kind of thing as
`"hello".upper`.

**Python keeps every module it has loaded in one dictionary**, called
`sys.modules`:

```text
>>> import sys
>>> 'calculator' in sys.modules
True
>>> sys.modules['calculator'] is calculator
True
```

`is` there means "the very same object", not "an equal one". There is
exactly one `report` module in a running program, no matter how many
files import it — which is why `main.py` and a future `test_report.py`
are looking at the same thing.

**Which is why the second import is free.** Take a file that says
something out loud when it loads:

```python
"""A module that says something the moment it is imported."""

print("noisy.py is running its top level")
print("__name__ here is", __name__)
```

```text
>>> import noisy
noisy.py is running its top level
__name__ here is noisy
>>> import noisy
>>> print('done')
done
```

The second `import` printed nothing. `import` is not "run this file" —
it is "make sure this file has been run, then give me the module
object". First time, Python finds it, runs it, and files the result.
Every time after, it just reads `sys.modules`.

That has two consequences for this project. A module's top level is a
**one-time setup area**, so `RULE = "-" * 30` in `report.py` is computed
once no matter how often it is used. And a `print` at a module's top
level fires once, the first time somebody imports it, at a moment you do
not control — which is exactly why `_demo()` lives under the guard.

**And it is why the circular import fails the way it does.** When
`main` imports `report`, Python puts a *half-built* `main` module into
`sys.modules` before running `report`. So `report`'s
`from main import BANNER` finds the entry, looks inside, and the name is
not there yet. The module exists; it just is not finished. That is what
`cannot import name 'format_report' from 'report'` is really telling
you.

</details>

<details>
<summary>Under the hood — how __name__ lets one file be both a library and a program</summary>

Every module has a variable called `__name__`, and Python sets it before
the file's first line runs. What it gets depends on **how the file was
started**.

Same file, two ways:

```text
$ python -c "import noisy"
noisy.py is running its top level
__name__ here is noisy
```

```text
$ python noisy.py
noisy.py is running its top level
__name__ here is __main__
```

Imported, `__name__` is the module's name. Run directly, it is the
string `"__main__"` — because the file Python was pointed at *is* the
main program, and Python does not care what it is called.

So this:

```python
if __name__ == "__main__":
    print(_demo())
```

means: "only do this if I am the program somebody started, not a file
somebody borrowed from". One file, two behaviours, decided by the file
itself.

That is what makes all four files in this project able to be two things
at once. To `main.py`, `report.py` is three functions. To you at the
terminal, `python report.py` is a little demo that prints a report. Each
file becomes independently runnable — which is exactly what requirement
9 is buying you, and why step 6 tells you to run `python report.py` and
compare its output before you ever wire it into `main.py`. Debugging one
file at a time is much easier than debugging four.

Watch what the guard is *not* doing. It does not stop the module's top
level running on import — `noisy.py` printed both times it was first
loaded. It only guards what is inside it.

</details>

<details>
<summary>Under the hood — import report versus from report import format_report, and why it matters for tests</summary>

The two forms look like a matter of taste. They differ in one way that
eventually matters, and this project is a good place to see it.

`from report import format_report` copies the *value* out of the module
into your file, once, at import time. `import report` copies a reference
to the module and looks the name up fresh on every call.

Two files that do the same thing:

```python
"""Calls the name it copied at import time."""

from calculator import add


def total() -> float:
    """Return add(2, 3)."""
    return add(2.0, 3.0)
```

```python
"""Calls the name through its module."""

import calculator


def total() -> float:
    """Return calculator.add(2, 3)."""
    return calculator.add(2.0, 3.0)
```

Now replace the function at runtime — which is exactly what a test does
when it wants to check what happens if a dependency misbehaves:

```text
>>> import calculator, uses_from, uses_import
>>> def fake_add(a, b):
...     return 999.0
...
>>> calculator.add = fake_add
>>> uses_from.total()
5.0
>>> uses_import.total()
999.0
```

`uses_from` never noticed. It took its own copy when it was imported and
has held it ever since. `uses_import` goes through the module every
time, so it sees the swap.

This is why `main.py` in this project uses `import income` and calls
`income.add_income`, and why the folded single-file answer keeps the
same call shape. Two more reasons on top of the swappability:
`income.total_income(sources)` says where the function came from at the
point where you read it, and a bare `total_income` next to a bare
`total_expenses` in one function body is one typo away from a bug that
prints a plausible wrong number.

The rule of thumb:

- **`from x import y`** when `y` is small, stable and obvious, and you
  use it a lot — `from collections.abc import Callable`.
- **`import x`** when the name would be ambiguous on its own, when you
  want to be able to swap `x`'s insides in a test, or when you are
  pulling in several names.

Never `from report import *`. It drags every public name into your file,
so a reader cannot tell where anything came from, and a name you did not
expect can quietly replace one of yours.

Week 11 covers testing properly. When you get there, come back to this
block — it is the reason the pure modules in this project are testable
and `main.py` is not.

</details>

<details>
<summary>Under the hood — why the untestable file is the smallest one</summary>

Look again at the fan diagram, and at which file has no tests.

```text
main.py        talks to a human          impure, untestable, thin
    |
    +-- income.py     data shape + totals     pure
    +-- expenses.py   data shape + totals     pure
    +-- report.py     arithmetic + layout     pure
```

A test for `report.py` is three lines and needs nothing but the module:

```python
def test_format_report_matches_the_brief_byte_for_byte() -> None:
    assert report.format_report(2900.0, 1370.0, 12) == BRIEF_REPORT
```

A test for `main.py` needs to pretend to be a keyboard, feed lines in a
particular order, and capture what came out. That is real tooling, and
it is Week 11.

So the design principle is not "write tests for everything". It is:
**make the part you cannot test as small and as boring as you can.**
Every decision with a right answer — how to total a list, what happens
at zero income, how wide a column is — moves out of `main.py` into a
function that can be called directly. What is left in `main.py` is
sequencing: ask this, then that, then print. You verify it by reading
it, and reading it is quick because there is nothing clever in it.

That asymmetry is the entire argument for splitting the project up.
Not tidiness. Not "separation of concerns" as a phrase. This.

**One more thing that falls out of it.** When output format is part of
the spec, assert on the *whole string*, as that test does. Checking
`"2900.00" in output` passes happily on a report with every column
misaligned — which is exactly the bug you were trying to catch.

</details>

## Acceptance checklist

- [ ] Four files, named exactly `income.py`, `expenses.py`, `report.py`
      and `main.py`, in one folder.
- [ ] `python income.py`, `python expenses.py` and `python report.py`
      each run on their own and print their demo.
- [ ] `python report.py` prints the brief's report, character for
      character, including the wider `Projected (12 mo):` row.
- [ ] `savings_rate(2900, 1370)` is `52.758…`, printing as `52.76%`.
- [ ] `savings_rate(0, 0)` returns `0.0` and does not raise.
- [ ] `savings_rate(1000, 1500)` returns `-50.0`.
- [ ] `project_savings(100.0, -1)` raises
      `ValueError: months must be zero or positive`.
- [ ] `total_income([])` returns `0.0` — a float, not `0`.
- [ ] The full session in *Expected output* runs and matches.
- [ ] `twelve hundred` at an amount prompt asks again and keeps the
      label already typed.
- [ ] `abc` at the months prompt and `-3` at the months prompt get two
      **different** messages, and both ask again.
- [ ] Finishing with no expenses at all prints `Expenses: $0.00` rather
      than crashing.
- [ ] No traceback appears for any of those.
- [ ] `report.py`, `income.py` and `expenses.py` contain no `print` or
      `input` outside a `__main__` guard.
- [ ] None of the three imports `main`, and none imports another of the
      three.
- [ ] No function body is longer than 25 lines.
- [ ] Every public function has type hints and a one-line docstring,
      and every file has a module docstring.
- [ ] All four files end with `if __name__ == "__main__":`.
- [ ] No `TODO` comments left.
- [ ] Committed with a message such as
      `Week 4 mini-project: personal finance calculator`.

## Stretch

**Compound the projection.** Straight-line projection assumes the money
sits in a shoebox. Put it somewhere that pays interest and each month's
deposit grows too. Keep this in a `report_stretch.py` so the four graded
files stay exactly as the brief specifies:

```python
def compounded_projection(monthly: float, months: int, monthly_rate: float) -> float:
    """Return the value of `months` monthly deposits compounded at `monthly_rate`.

    `monthly_rate` is a fraction per month, so 0.004 is 0.4% a month. A rate of
    0 gives exactly the same answer as `report.project_savings`.
    """
    if months < 0:
        raise ValueError("months must be zero or positive")
    if monthly_rate == 0:
        return report.project_savings(monthly, months)
    return monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
```

This is the future value of an ordinary annuity: every month you put
`monthly` in, and everything already in there grows by `monthly_rate`.
Rather than loop twelve times, the closed form adds up the whole series
in one expression.

The `monthly_rate == 0` branch is not a speed-up, it is a correctness
guard — at a rate of zero the formula divides by zero. Handing that case
to `project_savings` also states the relationship out loud: compounding
at 0% *is* straight-line projection.

```text
>>> compounded_projection(1530.0, 12, 0.0)
18360.0
>>> compounded_projection(1530.0, 12, 0.004)
18769.354382063193
```

`$18769.35` against `$18360.00` — $409.35 more, from twelve months at a
rate most savings accounts would call modest.

**Give expenses a category and total by category.**

```python
def totals_by_category(items: list[dict]) -> dict[str, float]:
    """Return {category: total} for `items`, defaulting a missing category."""
    totals: dict[str, float] = {}
    for item in items:
        category = item.get("category", DEFAULT_CATEGORY)
        totals[category] = totals.get(category, 0.0) + item["amount"]
    return totals
```

`item.get("category", DEFAULT_CATEGORY)` rather than `item["category"]`
is the load-bearing choice in there. It makes the category **optional**,
so items created by the plain `add_expense` — which has never heard of
categories — still work, landing in `"other"` instead of raising
`KeyError`. That is what lets this bolt onto the graded solution without
editing a line of it.

And this is the moment the "keep income and expenses separate" argument
pays off. Expenses grew a key. Income did not. A merged module would now
have a `category` parameter that means nothing for half its callers.

```text
$ python report_stretch.py
------------------------------
Expenses by category
------------------------------
housing:            $900.00
living:             $470.00
------------------------------
straight-line 12 mo: $18360.00
compounded at 0.4%/mo: $18769.35
```

The sort is `key=lambda pair: (-pair[1], pair[0])` — descending by
total, then alphabetically to break ties. Negating the number is how you
mix two sort directions in one key, since you cannot negate a string.
Exactly the same idiom as the top-three list in Challenge 2.

**Load the entries from CSV files with `argparse`.** Keep it in a
`main_stretch.py` that imports `main` and reuses `collect` and
`read_months`:

```python
def gather(path: str | None, heading: str, add: main.Adder) -> list[dict]:
    """Return entries from `path` if given, otherwise ask the user for them."""
    if path is None:
        return main.collect(heading, add)
    return load_csv(path, add)
```

The design decision worth copying: the flags are **optional overrides**,
not a separate mode. Pass `--income` and it reads the CSV; leave it off
and it asks you. `gather` is a named three-line function rather than an
`if args.income:` buried inside `main_stretch()` because a named
function with one branch is trivially checkable, and because the two
paths converge immediately instead of duplicating everything downstream.

Note that `main_stretch.py` imports `main`, and `main.py` has never
heard of `main_stretch.py`. Dependencies still point one way, so nothing
in here can break the four graded files.

Reading files properly is Week 6, so treat `load_csv` as "open this,
hand me one dict per row" for now. Two details that will bite you if you
skip them: pass `encoding="utf-8"` explicitly, because the default
differs between Windows and Linux and will misbehave on somebody else's
machine; and if a help string contains a percent sign, double it, since
`argparse` runs help text through `%`-formatting.

**Write real tests.** Once `report.py` is pure, testing it needs no
tricks at all. Two idioms worth taking with you.

`pytest.approx` for floats, because
`52.758620689655174 == 52.7586206896` is `False` and exact equality on
binary floating point is a coin flip:

```python
assert report.savings_rate(2900, 1370) == pytest.approx(52.7586206896, rel=1e-9)
```

And `pytest.raises` with `match=`, to assert *which* error, not merely
that something broke — a bare `pytest.raises(ValueError)` would pass
even if the failure came from a typo elsewhere in the function:

```python
with pytest.raises(ValueError, match="months must be zero or positive"):
    report.project_savings(100.0, -1)
```

One more test to write, and it is the one that catches every formatting
mistake on this page at once:

```python
def test_format_report_matches_the_brief_byte_for_byte() -> None:
    assert report.format_report(2900.0, 1370.0, 12) == BRIEF_REPORT
```

Testing is Week 11, so this stretch is a preview. Write the tests
anyway. Watching a change to `_row` turn one assertion red is the
fastest way to understand what the split you just built is for.
