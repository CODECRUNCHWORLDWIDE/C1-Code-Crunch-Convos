"""
Exercise 01 — FizzBuzz
======================

The classic interview warm-up. For every integer from 1 to 100
(inclusive), print exactly one line:

- "Fizz"     if the number is divisible by 3 (but not 5)
- "Buzz"     if the number is divisible by 5 (but not 3)
- "FizzBuzz" if the number is divisible by BOTH 3 and 5
- the number itself, otherwise

Expected output (first eight lines):

    1
    2
    Fizz
    4
    Buzz
    Fizz
    7
    8

Skills practised
----------------
- `for` with `range(start, stop)` (remember `stop` is excluded)
- `if`/`elif`/`else`
- The modulo operator `%` to test divisibility

Hints
-----
- The order of your branches matters: check the "both" case (15, 30, 45,
  ...) before the single-divisor cases, OR combine the check with `and`.
- `n % k == 0` is True when `n` is exactly divisible by `k`.

Run me
------
    python exercise-01-fizzbuzz.py
"""


def main() -> None:
    # TODO: Loop through the integers 1 through 100 (inclusive).
    # For each number, print the correct FizzBuzz value.
    #
    # Replace the `pass` below with your loop.
    for number in range(1, 101):
        # TODO: decide what to print for `number`
        pass


if __name__ == "__main__":
    main()
