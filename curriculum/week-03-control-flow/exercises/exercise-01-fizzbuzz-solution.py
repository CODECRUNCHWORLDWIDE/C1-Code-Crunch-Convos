"""exercise-01-fizzbuzz-solution.py — branch ordering with an if/elif/else chain.

Prints the counts 1 through 100, replacing multiples of 3 with "Fizz",
multiples of 5 with "Buzz", and multiples of both with "FizzBuzz".
"""

FIRST_COUNT = 1
LAST_COUNT = 100


def fizzbuzz_word(count: int) -> str:
    """Return the word that should be called out for `count`.

    Returns "FizzBuzz" for multiples of 15, "Fizz" for other multiples of
    3, "Buzz" for other multiples of 5, and the count itself as a string
    otherwise.
    """
    if count % 15 == 0:
        return "FizzBuzz"
    elif count % 3 == 0:
        return "Fizz"
    elif count % 5 == 0:
        return "Buzz"
    else:
        return str(count)


def main() -> None:
    """Print one line per count from FIRST_COUNT to LAST_COUNT."""
    for count in range(FIRST_COUNT, LAST_COUNT + 1):
        print(fizzbuzz_word(count))


if __name__ == "__main__":
    main()
