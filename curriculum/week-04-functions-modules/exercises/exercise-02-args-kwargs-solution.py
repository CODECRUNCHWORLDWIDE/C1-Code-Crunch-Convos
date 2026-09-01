"""exercise-02-args-kwargs-solution.py — receipts for the Saturday farmers market.

Three functions, one for each side of the star story. `total_pounds` packs
however many weights arrive. `build_stall` packs however many details arrive.
`receipt_line` puts a keyword-only parameter behind a `*` so a currency code
can never be sold as a vegetable.

The self-checks at the bottom are the starter's, unchanged.
"""


def total_pounds(*weights: float) -> float:
    """Return the combined weight of everything in one basket, in pounds.

    Args:
        *weights: Zero or more individual item weights.

    Returns:
        The total, rounded to two decimals. 0.0 when nothing was passed.
    """
    return round(sum(weights, 0.0), 2)


def build_stall(name: str, **details: object) -> dict[str, object]:
    """Return a stall record with "name" first, then every keyword detail."""
    return {"name": name, **details}


def receipt_line(stall_name: str, *items: str, currency: str = "USD") -> str:
    """Return one receipt line for a stall.

    Args:
        stall_name: The stall's display name.
        *items: Zero or more item names, in the order they were weighed.
        currency: Three-letter currency code. Keyword-only.

    Returns:
        A line like `Sunrise Greens: kale, chard [USD]`.
    """
    listed = ", ".join(items) if items else "(nothing)"
    return f"{stall_name}: {listed} [{currency}]"


if __name__ == "__main__":
    assert total_pounds() == 0.0, total_pounds()
    assert total_pounds(1.5) == 1.5, total_pounds(1.5)
    assert total_pounds(1.5, 2.25, 0.75) == 4.5, total_pounds(1.5, 2.25, 0.75)

    basket = [1.5, 2.25, 0.75]
    assert total_pounds(*basket) == 4.5, "did you unpack the list with *?"

    sunrise = build_stall("Sunrise Greens", produce="kale", price_per_pound=3.5)
    assert sunrise == {
        "name": "Sunrise Greens",
        "produce": "kale",
        "price_per_pound": 3.5,
    }, sunrise
    assert list(sunrise)[0] == "name", "name must be the first key"

    config = {"produce": "figs", "price_per_pound": 6.0}
    orchard = build_stall("Hilltop Orchard", **config)
    assert orchard["name"] == "Hilltop Orchard", orchard
    assert orchard["produce"] == "figs", orchard
    assert config == {"produce": "figs", "price_per_pound": 6.0}, "config was mutated"

    line = receipt_line("Sunrise Greens", "kale", "chard", "spinach")
    assert line == "Sunrise Greens: kale, chard, spinach [USD]", line
    assert receipt_line("Hilltop Orchard", "figs", currency="CAD") == (
        "Hilltop Orchard: figs [CAD]"
    )
    assert receipt_line("Empty Stall") == "Empty Stall: (nothing) [USD]"

    print(line)
    print(receipt_line("Hilltop Orchard", "figs", currency="CAD"))
    print(f"Basket weight: {total_pounds(*basket)} lb")
    print("All checks passed.")
