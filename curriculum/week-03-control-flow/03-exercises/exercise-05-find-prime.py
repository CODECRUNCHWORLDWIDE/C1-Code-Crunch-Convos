"""
Exercise 05 — Prime Checker
===========================

Ask the user for an integer `n` and print whether it is prime.

Definition
----------
A prime number is a whole number greater than 1 whose only positive
divisors are 1 and itself. So 2, 3, 5, 7, 11, 13, ... are prime;
4, 6, 8, 9, 10 are not. 0, 1, and negative numbers are NOT prime.

Examples
--------
    n = 1   ->  "1 is not prime."
    n = 2   ->  "2 is prime."
    n = 17  ->  "17 is prime."
    n = 21  ->  "21 is not prime (divisible by 3)."

Skills practised
----------------
- Guard clauses (handle the small / negative cases first)
- `for` loop + `break` + `else` clause to express "no divisor found"
- The square-root optimization: a non-trivial divisor of `n` is at most
  `sqrt(n)`, so the loop only needs to go that far.

Hints
-----
- After handling n <= 1 and n == 2 specially, loop from 2 to
  `int(n ** 0.5) + 1` (inclusive). If any divisor evenly divides `n`,
  print the not-prime message and `return`. If the loop finishes without
  `break`, n is prime — that's exactly what the `for/else` clause is
  for.
- For extra speed, after handling 2 you can step by 2 starting from 3 to
  skip even divisors. Not required for this exercise.

Run me
------
    python exercise-05-find-prime.py
"""


def main() -> None:
    raw = input("Enter an integer: ").strip()

    # Allow optional leading "-" for negative input.
    if raw.startswith("-") and raw[1:].isdigit():
        n = int(raw)
    elif raw.isdigit():
        n = int(raw)
    else:
        print("Please enter a whole number.")
        return

    # TODO: Guard clauses for n <= 1 (not prime) and n == 2 (prime).

    # TODO: Loop divisors from 2 up to int(n ** 0.5) + 1.
    # If you find one, print "n is not prime (divisible by d)." and return.
    # If the loop finishes naturally, print "n is prime."
    #
    # Use the `for ... else:` clause for a clean structure.

    for divisor in range(2, int(n ** 0.5) + 1):
        # ... check and possibly return/break ...
        pass
    else:
        # ... runs only if the loop was not broken out of ...
        pass


if __name__ == "__main__":
    main()
