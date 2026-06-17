"""Code Crunch Convos — Week 2 Mini-Project Starter.

A menu-driven command-line unit converter that supports:

* Temperature (Celsius <-> Fahrenheit)
* Distance    (kilometers <-> miles)
* Currency    (USD <-> EUR, at a hardcoded exchange rate)

Run the program with::

    python starter.py

The user is prompted to pick a category, a direction, and a value. The
converted result is printed with two decimal places and the
appropriate unit labels.

See ``README.md`` in this directory for the full specification and
rubric.

Tasks (in suggested order)
--------------------------
1. Implement the six conversion functions below. Each currently
   raises ``NotImplementedError``.
2. Implement ``main()``: print the banner, run the menus, read input,
   call the right conversion, print the result.
3. Test every path by hand (3 categories x 2 directions = 6 paths).
4. Optional: add the stretch goals listed in the README.
"""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USD_TO_EUR: float = 0.9140       # hardcoded exchange rate
KM_PER_MILE: float = 1.609344    # exact, by international agreement


# ---------------------------------------------------------------------------
# Conversion functions
# ---------------------------------------------------------------------------


def c_to_f(celsius: float) -> float:
    """Convert degrees Celsius to degrees Fahrenheit."""
    # TODO: implement F = C * 9 / 5 + 32
    raise NotImplementedError


def f_to_c(fahrenheit: float) -> float:
    """Convert degrees Fahrenheit to degrees Celsius."""
    # TODO: implement C = (F - 32) * 5 / 9
    raise NotImplementedError


def km_to_mi(kilometers: float) -> float:
    """Convert kilometers to miles using ``KM_PER_MILE``."""
    # TODO: miles = kilometers / KM_PER_MILE
    raise NotImplementedError


def mi_to_km(miles: float) -> float:
    """Convert miles to kilometers using ``KM_PER_MILE``."""
    # TODO: kilometers = miles * KM_PER_MILE
    raise NotImplementedError


def usd_to_eur(usd: float) -> float:
    """Convert US dollars to euros using ``USD_TO_EUR``."""
    # TODO: eur = usd * USD_TO_EUR
    raise NotImplementedError


def eur_to_usd(eur: float) -> float:
    """Convert euros to US dollars using ``USD_TO_EUR``."""
    # TODO: usd = eur / USD_TO_EUR
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Program flow
# ---------------------------------------------------------------------------


def print_banner() -> None:
    """Print the welcome banner."""
    print("================================")
    print("   Code Crunch Unit Converter")
    print("================================")
    print()


def main() -> None:
    """Run the unit converter once and exit."""
    print_banner()

    # --- Category menu ---
    print("Categories:")
    print("  1) Temperature (C / F)")
    print("  2) Distance    (km / mi)")
    print("  3) Currency    (USD / EUR)")
    print()
    category: str = input("Pick a category (1-3): ").strip()
    print()

    # TODO: based on the category, print the matching direction menu,
    #       read 'a' or 'b', prompt for the numeric value, cast it
    #       with float() inside a try/except, and print the result in
    #       the format described in mini-project/README.md.
    #
    # Suggested helpers (you don't have to use them):
    #
    #     def prompt_value(label: str) -> float | None:
    #         raw = input(f"Value in {label}: ").strip()
    #         try:
    #             return float(raw)
    #         except ValueError:
    #             print(f"Error: {raw!r} is not a number.")
    #             return None
    #
    # When you have a working version, delete this comment block.

    _ = category  # remove once you've finished the TODO

    print()
    print("Thanks for using the converter!")


if __name__ == "__main__":
    main()
