"""Temperature conversions between Celsius, Fahrenheit and Kelvin.

Week 4 homework, problem 1, Code Crunch Convos.

This file is a module. A module is just a ``.py`` file that other ``.py``
files are allowed to import. Save your own copy as ``temperature.py`` in
your ``homework/`` folder, because that is the name the import line will
use: ``from temperature import c_to_f``.

Run this file and it prints the sample table. Import it and it prints
nothing, because the printing sits under the ``__main__`` guard at the
bottom.
"""

ABSOLUTE_ZERO_C: float = -273.15

HEADER: str = "   C       F        K"
RULE: str = "---------------------"
SAMPLE_CELSIUS: list[int] = [0, 100, -40]


def c_to_f(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        The same temperature in degrees Fahrenheit.

    Example:
        >>> c_to_f(100)
        212.0
    """
    return celsius * 9 / 5 + 32


def f_to_c(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius.

    Args:
        fahrenheit: Temperature in degrees Fahrenheit.

    Returns:
        The same temperature in degrees Celsius.

    Example:
        >>> f_to_c(212)
        100.0
    """
    return (fahrenheit - 32) * 5 / 9


def c_to_k(celsius: float) -> float:
    """Convert a Celsius temperature to Kelvin.

    Args:
        celsius: Temperature in degrees Celsius, at or above absolute zero.

    Returns:
        The same temperature in kelvin.

    Raises:
        ValueError: If `celsius` is below absolute zero (-273.15 C).

    Example:
        >>> c_to_k(0)
        273.15
    """
    if celsius < ABSOLUTE_ZERO_C:
        raise ValueError(f"{celsius} C is below absolute zero ({ABSOLUTE_ZERO_C} C)")
    return celsius + 273.15


def _table() -> str:
    """Return the sample conversion table as one multi-line string."""
    rows = [HEADER, RULE]
    for celsius in SAMPLE_CELSIUS:
        rows.append(f"{celsius:>4}{c_to_f(celsius):>9.2f}{c_to_k(celsius):>9.2f}")
    return "\n".join(rows)


if __name__ == "__main__":
    print(_table())
