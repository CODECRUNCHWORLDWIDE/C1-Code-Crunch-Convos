"""exercise-03-temperature-converter-solution.py — convert between C, F, and K.

Week 2, Exercise 3. Practises writing annotated functions, arithmetic
operators and precedence, and comparing floats with a tolerance.
"""

ABSOLUTE_ZERO_C: float = -273.15
FREEZING_POINT_F: float = 32.0
F_PER_C: float = 9 / 5
TOLERANCE: float = 1e-9

LABEL_WIDTH: int = 16
VALUE_WIDTH: int = 9
TABLE_WIDTH: int = 43

ROUND_TRIP_C: float = 23.3


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: a temperature in degrees Celsius.

    Returns:
        The same temperature in degrees Fahrenheit.
    """
    return celsius * F_PER_C + FREEZING_POINT_F


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius.

    Args:
        fahrenheit: a temperature in degrees Fahrenheit.

    Returns:
        The same temperature in degrees Celsius.
    """
    return (fahrenheit - FREEZING_POINT_F) / F_PER_C


def celsius_to_kelvin(celsius: float) -> float:
    """Convert a Celsius temperature to kelvin.

    Args:
        celsius: a temperature in degrees Celsius.

    Returns:
        The same temperature in kelvin. Never negative for any real
        temperature, because ABSOLUTE_ZERO_C is the bottom of the scale.
    """
    return celsius - ABSOLUTE_ZERO_C


def table_row(label: str, celsius: float) -> str:
    """Return one reference-table row for the given Celsius temperature."""
    return (f"{label:<{LABEL_WIDTH}}"
            f"{celsius:>{VALUE_WIDTH}.2f}"
            f"{celsius_to_fahrenheit(celsius):>{VALUE_WIDTH}.2f}"
            f"{celsius_to_kelvin(celsius):>{VALUE_WIDTH}.2f}")


def main() -> None:
    """Print the reference table and the round-trip check."""
    print(f"{'Reference point':<{LABEL_WIDTH}}"
          f"{'C':>{VALUE_WIDTH}}{'F':>{VALUE_WIDTH}}{'K':>{VALUE_WIDTH}}")
    print("-" * TABLE_WIDTH)
    print(table_row("Absolute zero", ABSOLUTE_ZERO_C))
    print(table_row("Same in C and F", -40.0))
    print(table_row("Water freezes", 0.0))
    print(table_row("Room temperature", 21.0))
    print(table_row("Body temperature", 37.0))
    print(table_row("Water boils", 100.0))
    print("-" * TABLE_WIDTH)

    there: float = celsius_to_fahrenheit(ROUND_TRIP_C)
    back: float = fahrenheit_to_celsius(there)
    print(f"Round-trip: {ROUND_TRIP_C:.1f} C -> {there:.2f} F -> {back:.6f} C")
    print(f"Exact match? {back == ROUND_TRIP_C}   "
          f"Within {TOLERANCE:g}? {abs(back - ROUND_TRIP_C) < TOLERANCE}")


if __name__ == "__main__":
    main()
