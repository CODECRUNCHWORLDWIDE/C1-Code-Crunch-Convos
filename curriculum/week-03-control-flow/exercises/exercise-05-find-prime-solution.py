"""exercise-05-find-prime-solution.py — trial division, twice.

Once with the for/else clause and once with guard clauses and early
returns, cross-checked against a list of known answers.
"""

import math

CHECK_NUMBERS = [1, 2, 9, 25, 91, 97, 7919]
EXPECTED_PRIME = [False, True, False, False, False, True, True]


def report_primality(number: int) -> None:
    """Print one line explaining whether `number` is prime.

    Uses the for/else clause: the else runs only when no divisor was
    found and the loop was therefore never broken out of.
    """
    if number < 2:
        print(f"{number:>6} is not prime: primes start at 2.")
        return
    for divisor in range(2, math.isqrt(number) + 1):
        if number % divisor == 0:
            print(f"{number:>6} is not prime: {divisor} divides it evenly.")
            break
    else:
        print(f"{number:>6} is prime.")


def is_prime(number: int) -> bool:
    """Return True when `number` is prime, using guard clauses."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for divisor in range(3, math.isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False
    return True


def main() -> None:
    """Report on every check number and confirm both versions agree."""
    prime_count = 0

    for number, expected in zip(CHECK_NUMBERS, EXPECTED_PRIME, strict=True):
        report_primality(number)
        assert is_prime(number) == expected, f"is_prime({number}) is wrong"
        if is_prime(number):
            prime_count += 1

    print(f"{prime_count} of {len(CHECK_NUMBERS)} numbers are prime.")


if __name__ == "__main__":
    main()
