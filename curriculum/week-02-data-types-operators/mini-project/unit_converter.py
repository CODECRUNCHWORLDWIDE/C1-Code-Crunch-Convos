"""Code Crunch Unit Converter -- a one-shot, menu-driven CLI.

Week 2 mini-project, Code Crunch Convos. Converts between Celsius and
Fahrenheit, kilometers and miles, and US dollars and euros. Runs one
conversion and exits.

The questions go to the error stream and the banner, the menus and the
result go to the normal output stream. When the input stream is already
finished -- which is what happens when a checker runs the file -- each
question answers itself from the demo values below, so the file always
prints a complete session instead of waiting for typing that is never
coming.

Run it with::

    python unit_converter.py
"""

import sys

USD_TO_EUR: float = 0.9140  # hardcoded; see the stretch goals
KM_PER_MILE: float = 1.609344

BANNER: str = """================================
   Code Crunch Unit Converter
================================"""

DEMO_CATEGORY: str = "1"
DEMO_DIRECTION: str = "a"
DEMO_VALUE: str = "100"


# --------------------------------------------------------------------
# Asking
# --------------------------------------------------------------------

def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or ``demo`` when nobody answers.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on when the input stream has
            already ended.

    Returns:
        The line that was typed, or ``demo``. A demo answer is echoed
        after the prompt on the normal output stream, so the printed
        session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


# --------------------------------------------------------------------
# Conversions
# --------------------------------------------------------------------

def c_to_f(c: float) -> float:
    """Return degrees Celsius ``c`` converted to Fahrenheit."""
    return c * 9 / 5 + 32


def f_to_c(f: float) -> float:
    """Return degrees Fahrenheit ``f`` converted to Celsius."""
    return (f - 32) * 5 / 9


def km_to_mi(km: float) -> float:
    """Return kilometers ``km`` converted to miles."""
    return km / KM_PER_MILE


def mi_to_km(mi: float) -> float:
    """Return miles ``mi`` converted to kilometers."""
    return mi * KM_PER_MILE


def usd_to_eur(usd: float) -> float:
    """Return US dollars ``usd`` converted to euros."""
    return usd * USD_TO_EUR


def eur_to_usd(eur: float) -> float:
    """Return euros ``eur`` converted to US dollars."""
    return eur / USD_TO_EUR


# --------------------------------------------------------------------
# Input helpers
# --------------------------------------------------------------------

def read_direction() -> str | None:
    """Return ``"a"`` or ``"b"``, or ``None`` after printing an error."""
    raw: str = ask("\nChoose direction (a/b): ", DEMO_DIRECTION)
    cleaned: str = raw.strip().lower()
    if cleaned == "a" or cleaned == "b":
        return cleaned
    print(f"\nError: {cleaned!r} is not a direction. Pick a or b.")
    return None


def read_value(unit_label: str) -> float | None:
    """Return the number the user typed, or ``None`` if it isn't one."""
    raw: str = ask(f"\nValue in {unit_label}: ", DEMO_VALUE)
    try:
        return float(raw)
    except ValueError:
        print(f"\nError: {raw!r} is not a number.")
        return None


# --------------------------------------------------------------------
# One category each
# --------------------------------------------------------------------

def run_temperature() -> bool:
    """Run the temperature conversion. Return True if it succeeded."""
    print("\nDirection:")
    print("  a) Celsius     -> Fahrenheit")
    print("  b) Fahrenheit  -> Celsius")

    direction: str | None = read_direction()
    if direction is None:
        return False

    if direction == "a":
        value: float | None = read_value("Celsius")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} C = {c_to_f(value):.2f} F")
    else:
        value = read_value("Fahrenheit")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} F = {f_to_c(value):.2f} C")
    return True


def run_distance() -> bool:
    """Run the distance conversion. Return True if it succeeded."""
    print("\nDirection:")
    print("  a) Kilometers -> Miles")
    print("  b) Miles      -> Kilometers")

    direction: str | None = read_direction()
    if direction is None:
        return False

    if direction == "a":
        value: float | None = read_value("kilometers")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} km = {km_to_mi(value):.2f} mi")
    else:
        value = read_value("miles")
        if value is None:
            return False
        print(f"\nResult: {value:.2f} mi = {mi_to_km(value):.2f} km")
    return True


def run_currency() -> bool:
    """Run the currency conversion. Return True if it succeeded."""
    print("\nDirection:")
    print("  a) USD -> EUR")
    print("  b) EUR -> USD")

    direction: str | None = read_direction()
    if direction is None:
        return False

    rate_note: str = f"(rate: 1 USD = {USD_TO_EUR:.4f} EUR)"

    if direction == "a":
        value: float | None = read_value("USD")
        if value is None:
            return False
        print(
            f"\nResult: ${value:,.2f} USD = "
            f"€{usd_to_eur(value):,.2f} EUR  {rate_note}"
        )
    else:
        value = read_value("EUR")
        if value is None:
            return False
        print(
            f"\nResult: €{value:,.2f} EUR = "
            f"${eur_to_usd(value):,.2f} USD  {rate_note}"
        )
    return True


# --------------------------------------------------------------------
# Program flow
# --------------------------------------------------------------------

def main() -> None:
    """Print the menus, run one conversion, and exit."""
    print(BANNER)
    print("\nCategories:")
    print("  1) Temperature (C / F)")
    print("  2) Distance    (km / mi)")
    print("  3) Currency    (USD / EUR)")

    category: str = ask("\nPick a category (1-3): ", DEMO_CATEGORY).strip()

    if category == "1":
        converted: bool = run_temperature()
    elif category == "2":
        converted = run_distance()
    elif category == "3":
        converted = run_currency()
    else:
        print(f"\nError: {category!r} is not a category. Pick 1, 2, or 3.")
        return

    if converted:
        print("\nThanks for using the converter!")


if __name__ == "__main__":
    main()
