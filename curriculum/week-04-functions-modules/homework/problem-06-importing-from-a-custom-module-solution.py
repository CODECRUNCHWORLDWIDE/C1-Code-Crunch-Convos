"""Small integer helpers, and the script that uses them, in one file.

Week 4 homework, problem 6, Code Crunch Convos.

The brief asks for **two** files - ``mymath.py`` with the helpers, and
``use_mymath.py`` that imports them - and two files is what you should
write. This download is one file for a plain reason: every page here ships
exactly one runnable answer, and a lone ``use_mymath.py`` is not runnable.
On its own it stops on line 3 with ``ModuleNotFoundError: No module named
'mymath'``, because the thing it imports is not there.

So this file is the two halves stacked. ``square``, ``cube`` and
``is_prime`` are the ``mymath.py`` half. ``primes_between`` and ``main``
are the ``use_mymath.py`` half. To get the two files the brief wants, cut
between them and put ``from mymath import cube, is_prime, square`` at the
top of the second half. The page shows both files written out in full.
"""


def square(n: int) -> int:
    """Return `n` squared.

    Args:
        n: Any integer.

    Returns:
        n * n.

    Example:
        >>> square(7)
        49
    """
    return n * n


def cube(n: int) -> int:
    """Return `n` cubed.

    Args:
        n: Any integer.

    Returns:
        n * n * n.

    Example:
        >>> cube(7)
        343
    """
    return n * n * n


def is_prime(n: int) -> bool:
    """Return True if `n` is prime, using trial division.

    Args:
        n: Any integer. Values below 2 are never prime.

    Returns:
        True if n has no divisor other than 1 and itself.

    Example:
        >>> is_prime(29)
        True
    """
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


# Everything below this line is the `use_mymath.py` half.


def primes_between(low: int, high: int) -> list[int]:
    """Return every prime in the inclusive range low..high.

    Args:
        low: Lower bound, inclusive.
        high: Upper bound, inclusive.

    Returns:
        A sorted list of primes.

    Example:
        >>> primes_between(2, 10)
        [2, 3, 5, 7]
    """
    return [n for n in range(low, high + 1) if is_prime(n)]


def main() -> None:
    """Print the squares, cubes and primes the homework asks for."""
    print(f"square(7) = {square(7)}")
    print(f"cube(7)   = {cube(7)}")
    print(f"primes 2..30: {primes_between(2, 30)}")


if __name__ == "__main__":
    main()
