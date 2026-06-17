"""
Exercise 02 — Sum of Even Numbers
=================================

Ask the user for a positive integer `n`, then compute and print the sum
of every even number from 1 to `n` (inclusive).

Examples
--------
    n = 10  ->  2 + 4 + 6 + 8 + 10  = 30
    n = 5   ->  2 + 4               = 6
    n = 1   ->  (no evens)          = 0

Skills practised
----------------
- Reading and converting input with `int(input(...))`
- The accumulator pattern (initialize a total, add to it in the loop)
- `range(start, stop, step)` with a step of 2 OR a `% 2 == 0` filter

Hints
-----
- There are at least three correct approaches:
    a) Loop `for i in range(1, n + 1)` and `if i % 2 == 0: total += i`
    b) Loop `for i in range(2, n + 1, 2)` and `total += i` (no `if`)
    c) Use the built-in `sum(range(2, n + 1, 2))`
  Try the loop versions first, then verify with the built-in.
- Guard against invalid input: if `n` is less than 1, print a friendly
  message and exit.

Run me
------
    python exercise-02-sum-evens.py
"""


def main() -> None:
    raw = input("Enter a positive integer n: ").strip()

    # TODO: Convert `raw` to an int. If it cannot be converted, print a
    # helpful message and `return` from main(). Hint: try/except is
    # taught in Week 6, but for now you can check `raw.isdigit()` first.
    if not raw.isdigit():
        print("Please enter a non-negative whole number.")
        return

    n = int(raw)

    # TODO: Guard clause — handle n < 1 (print a message and return).

    # TODO: Compute the sum of even numbers from 1 through n (inclusive).
    total = 0
    # ... your loop here ...

    print(f"Sum of even numbers from 1 to {n} is {total}.")


if __name__ == "__main__":
    main()
