"""exercise-02-repl-explorer-solution.py — the answers from my REPL session, checked."""


def tables_needed(people: int, seats: int) -> int:
    """Return how many tables it takes to seat ``people``, ``seats`` each."""
    # A partly full table is still a table, so round up. -(-a // b) is the
    # integer ceiling: // floors, and flipping the sign twice floors the
    # other way.
    return -(-people // seats)


def pizzas_needed(people: int, slices_each: int, per_pizza: int) -> int:
    """Return how many whole pizzas feed ``people`` at ``slices_each``."""
    # Same ceiling, applied to total slices rather than total people.
    return -(-(people * slices_each) // per_pizza)


def cost_per_person(pizzas: int, price: float, people: int) -> float:
    """Return one person's share of the bill, rounded to whole cents."""
    # Multiply first, divide second, round once at the very end.
    return round(pizzas * price / people, 2)


if __name__ == "__main__":
    assert tables_needed(47, 6) == 8
    assert tables_needed(48, 6) == 8
    assert pizzas_needed(47, 3, 8) == 18
    assert pizzas_needed(30, 3, 8) == 12
    assert cost_per_person(18, 13.50, 47) == 5.17
    print("All checks passed.")
