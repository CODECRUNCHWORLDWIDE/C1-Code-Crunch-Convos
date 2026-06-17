# Challenge 01 — Tip Calculator

Build a small command-line tool that takes a restaurant bill, a tip
percentage, and a party size, then prints a formatted breakdown of the
totals.

## Goal

Help a group split a bill fairly, including a tip, without having to do
the mental arithmetic at the table.

## Specification

### Inputs

Prompt the user for three values, in order:

1. ``Bill amount in dollars: `` — a positive number (may be a float
   such as ``58.75``).
2. ``Tip percentage (e.g. 18 for 18%): `` — a positive number,
   interpreted as a percentage. ``20`` means a 20% tip.
3. ``Number of people: `` — a positive integer.

### Computations

- ``tip = bill * (tip_percent / 100)``
- ``total = bill + tip``
- ``per_person = total / people``

### Output

Print a four-line summary that matches **exactly** this layout (using
``$`` as the currency symbol):

```text
--- Bill Summary ---
Bill       :  $   58.75
Tip (20.0%):  $   11.75
Total      :  $   70.50
Per person :  $   23.50
```

Specifically:

- The labels are left-padded so the colons line up.
- The dollar sign always sits immediately before the number.
- Numbers are right-aligned in a width-7 field with two decimal places.
- The tip percentage in the second label shows one decimal place (so
  ``20`` displays as ``20.0``, and ``18.5`` displays as ``18.5``).
- Two blank lines around the header are fine; the exact whitespace
  inside the lines is what we grade.

### Validation

If the user types something that isn't a number for any prompt, or if
any of the values is ``<= 0``, print:

```text
Error: please enter positive numbers only.
```

and exit without printing the summary.

## Suggested Skeleton

```python
"""Tip calculator: read a bill, tip percentage, and party size."""


def main() -> None:
    try:
        bill = float(input("Bill amount in dollars: "))
        tip_percent = float(input("Tip percentage (e.g. 18 for 18%): "))
        people = int(input("Number of people: "))
    except ValueError:
        print("Error: please enter positive numbers only.")
        return

    if bill <= 0 or tip_percent <= 0 or people <= 0:
        print("Error: please enter positive numbers only.")
        return

    tip = bill * (tip_percent / 100)
    total = bill + tip
    per_person = total / people

    # TODO: print the formatted summary
    ...


if __name__ == "__main__":
    main()
```

## Stretch Goals

Pick one or two to push yourself:

- **Custom currency**: also prompt for a currency symbol (default
  ``$``). Use it in every line.
- **Rounding-up split**: instead of dividing evenly, compute a
  per-person amount rounded *up* to the nearest dollar. Then show how
  much extra tip the group is giving by paying that amount.
- **Service-quality presets**: instead of asking for a percentage,
  accept a single character — ``b`` (bad, 10%), ``g`` (good, 18%),
  ``e`` (excellent, 22%). Print the resulting percentage in the
  summary.

## Grading Rubric (Self-Check)

| Criterion | Points |
|-----------|-------:|
| Reads all three inputs and casts correctly | 2 |
| Validates positive numbers, rejects bad input | 2 |
| Computes tip, total, and per-person correctly | 2 |
| Output matches the required format exactly | 3 |
| Code is readable, uses named constants where appropriate, includes a docstring | 1 |
| **Total** | **10** |
