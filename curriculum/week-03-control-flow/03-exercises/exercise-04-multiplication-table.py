"""
Exercise 04 — Multiplication Table
==================================

Ask the user for a positive integer `n` and print an `n x n`
multiplication table.

Example for n = 5:

       1   2   3   4   5
       2   4   6   8  10
       3   6   9  12  15
       4   8  12  16  20
       5  10  15  20  25

Each cell should be right-aligned in a field 4 characters wide so the
columns line up nicely no matter how big the numbers get (up to roughly
n = 30).

Skills practised
----------------
- Nested `for` loops
- f-string format specifiers: `f"{value:4d}"` pads an integer to width 4
- The `end=""` argument to `print(...)` so a row stays on one line

Hints
-----
- Outer loop: rows from 1 to n. Inner loop: columns from 1 to n.
- Inside the inner loop, print `row * col` with `end=" "` (or use a
  width-aligned field).
- After the inner loop finishes, call `print()` with no arguments to
  start a new line.

Run me
------
    python exercise-04-multiplication-table.py
"""


def main() -> None:
    raw = input("Enter table size n (1-20 recommended): ").strip()

    if not raw.isdigit():
        print("Please enter a positive whole number.")
        return

    n = int(raw)
    if n < 1:
        print("n must be at least 1.")
        return

    # TODO: Nested loops to print the n x n table.
    # Each cell: print(f"{row * col:4d}", end="")
    # After each row: print()
    for row in range(1, n + 1):
        # ... inner loop ...
        pass


if __name__ == "__main__":
    main()
