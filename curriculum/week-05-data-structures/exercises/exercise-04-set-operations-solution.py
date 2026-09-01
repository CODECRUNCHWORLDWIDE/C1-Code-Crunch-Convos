"""exercise-04-set-operations-solution.py — the coverage report.

Five questions the organisers ask in English, five set operations that mean
exactly those questions. Every body is one expression, and none of them
changes the rosters it was handed.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
MORNING: set[str] = {"lists", "tuples", "slicing", "dicts", "big-o"}
EVENING: set[str] = {"dicts", "sets", "comprehensions", "big-o", "slicing"}
REQUIRED: set[str] = {"lists", "dicts", "big-o"}


# ---- Your task ----
def covered_by_either(a: set[str], b: set[str]) -> set[str]:
    """Return every topic covered by at least one circle.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding the topics in a, in b, or in both.
    """
    return a | b


def covered_by_both(a: set[str], b: set[str]) -> set[str]:
    """Return the topics covered by both circles.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding only the topics that appear in both.
    """
    return a & b


def only_in_first(a: set[str], b: set[str]) -> set[str]:
    """Return the topics in `a` that `b` has not covered.

    Swapping the arguments gives a different answer.

    Args:
        a: The circle being reported on.
        b: The circle being compared against.

    Returns:
        A new set holding the topics in a and not in b.
    """
    return a - b


def covered_exactly_once(a: set[str], b: set[str]) -> set[str]:
    """Return the topics covered by exactly one of the two circles.

    Args:
        a: One circle's topics.
        b: The other circle's topics.

    Returns:
        A new set holding the topics in one circle but not the other.
    """
    return a ^ b


def is_fully_covered(required: set[str], covered: set[str]) -> bool:
    """Return True if every required topic appears in `covered`.

    Args:
        required: The core topics that must be taught.
        covered: What one circle has actually taught.

    Returns:
        True when nothing required is outstanding, otherwise False.
    """
    return required <= covered


# ---- Self-check ----
if __name__ == "__main__":
    print(f"{'either:':<15}{len(covered_by_either(MORNING, EVENING))} topics")
    print(f"{'both:':<15}{', '.join(sorted(covered_by_both(MORNING, EVENING)))}")
    print(f"{'morning only:':<15}{', '.join(sorted(only_in_first(MORNING, EVENING)))}")
    print(f"{'evening only:':<15}{', '.join(sorted(only_in_first(EVENING, MORNING)))}")
    print(f"{'exactly once:':<15}{len(covered_exactly_once(MORNING, EVENING))} topics")

    assert covered_by_either(MORNING, EVENING) == {
        "lists", "tuples", "slicing", "dicts", "big-o", "sets", "comprehensions",
    }
    assert covered_by_both(MORNING, EVENING) == {"slicing", "dicts", "big-o"}
    assert only_in_first(MORNING, EVENING) == {"lists", "tuples"}
    assert only_in_first(EVENING, MORNING) == {"sets", "comprehensions"}
    assert covered_exactly_once(MORNING, EVENING) == {
        "lists", "tuples", "sets", "comprehensions",
    }
    assert is_fully_covered(REQUIRED, MORNING) is True
    assert is_fully_covered(REQUIRED, EVENING) is False
    assert len(MORNING) == 5 and len(EVENING) == 5  # inputs untouched
    print("All checks passed.")
