"""challenge-02-inventory-tracker-solution.py — a tiny warehouse backend.

Reflection on the structure I picked, as the rubric asks for.

I kept the nested dict[str, dict[str, int]] the brief hands me rather than
inventing a flat dict[(category, item), int]. Two reasons. First, the two
questions the app asks most often -- "what is in this category?" and
"how much of this item?" -- are both single O(1) hops in the nested shape,
whereas a flat dict answers the second in O(1) but needs a full O(n) scan
for the first. Second, the brief requires empty categories to disappear,
which is a statement about the inner dict's identity; a flat key space has
no inner dict to be empty. Every function is pure with respect to globals:
the inventory arrives as an argument, so the same code serves a test
fixture, a file-backed store, or a request handler without change.
"""

Inventory = dict[str, dict[str, int]]


def add_item(inv: Inventory, category: str, item: str, count: int = 1) -> None:
    """Add `count` of `item` to `category`, creating either if needed.

    Args:
        inv: The inventory, modified in place.
        category: The shelf the item lives on.
        item: The thing being stocked.
        count: How many to add. Must be positive.

    Raises:
        ValueError: If `count` is zero or negative.
    """
    if count <= 0:
        raise ValueError(f"count must be positive, got {count}")
    bucket = inv.setdefault(category, {})
    bucket[item] = bucket.get(item, 0) + count


def remove_item(inv: Inventory, category: str, item: str, count: int = 1) -> None:
    """Subtract `count` of `item`; prune the item and the category when empty.

    Args:
        inv: The inventory, modified in place.
        category: The shelf to take from.
        item: The thing being removed.
        count: How many to take. Taking more than there is empties the item.

    Raises:
        KeyError: If the category or the item is unknown. Nothing is changed
            when that happens.
    """
    bucket = inv[category]              # KeyError if the category is unknown
    remaining = bucket[item] - count    # KeyError if the item is unknown
    if remaining <= 0:
        del bucket[item]
    else:
        bucket[item] = remaining
    if not bucket:
        del inv[category]


def category_total(inv: Inventory, category: str) -> int:
    """Return the sum of all counts in `category`, or 0 if it does not exist.

    Args:
        inv: The inventory to read.
        category: The shelf to add up.

    Returns:
        The total count on that shelf. An unknown category is 0, not an error.
    """
    return sum(inv.get(category, {}).values())


def grand_total(inv: Inventory) -> int:
    """Return the sum of all counts across every category.

    Args:
        inv: The inventory to read.

    Returns:
        The total number of things in the warehouse.
    """
    return sum(count for bucket in inv.values() for count in bucket.values())


def find_item(inv: Inventory, item: str) -> list[str]:
    """Return the categories that hold `item`.

    Args:
        inv: The inventory to search.
        item: The thing to look for.

    Returns:
        The matching category names, in inventory order. Empty when the item
        is nowhere.
    """
    return [category for category, bucket in inv.items() if item in bucket]


def top_n_items(inv: Inventory, n: int = 3) -> list[tuple[str, str, int]]:
    """Return the n highest-count items in the whole inventory.

    Args:
        inv: The inventory to rank.
        n: How many rows to return. More than there are is not an error.

    Returns:
        Up to n (category, item, count) rows, count descending, ties broken
        by category then item, both A to Z.
    """
    rows = [
        (category, item, count)
        for category, bucket in inv.items()
        for item, count in bucket.items()
    ]
    rows.sort(key=lambda row: (-row[2], row[0], row[1]))
    return rows[:n]


def run_tests() -> None:
    """Run the brief's own scaffolding and report."""
    inv: Inventory = {}

    add_item(inv, "fruit", "apple", 5)
    add_item(inv, "fruit", "banana", 3)
    add_item(inv, "tools", "hammer", 1)
    add_item(inv, "fruit", "apple", 2)        # accumulates

    assert inv == {
        "fruit": {"apple": 7, "banana": 3},
        "tools": {"hammer": 1},
    }, inv

    assert category_total(inv, "fruit") == 10
    assert category_total(inv, "missing") == 0
    assert grand_total(inv) == 11

    assert find_item(inv, "apple") == ["fruit"]
    assert find_item(inv, "ghost") == []

    remove_item(inv, "fruit", "banana", 3)    # banana -> 0 -> deleted
    assert "banana" not in inv["fruit"]

    remove_item(inv, "tools", "hammer", 1)    # hammer gone -> category empty -> deleted
    assert "tools" not in inv

    try:
        remove_item(inv, "fruit", "phantom", 1)
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError")

    add_item(inv, "fruit", "cherry", 12)
    add_item(inv, "fruit", "date", 2)
    top = top_n_items(inv, 3)
    assert top[0] == ("fruit", "cherry", 12)
    assert len(top) == 3

    print("All checks passed.")


def extra_tests() -> None:
    """Check the edge cases the supplied scaffolding does not reach."""
    inv: Inventory = {"fruit": {"apple": 2}, "tools": {"saw": 1}}

    # over-removal clamps to deletion, never a negative count
    remove_item(inv, "fruit", "apple", 99)
    assert inv == {"tools": {"saw": 1}}, inv

    # an unknown category raises before touching anything
    try:
        remove_item(inv, "nope", "saw", 1)
    except KeyError as exc:
        assert exc.args[0] == "nope", exc.args
    else:
        raise AssertionError("Expected KeyError")
    assert inv == {"tools": {"saw": 1}}, inv

    # ties break on (category, item) alphabetical
    inv = {"b": {"x": 5, "a": 5}, "a": {"z": 5}}
    assert top_n_items(inv, 3) == [("a", "z", 5), ("b", "a", 5), ("b", "x", 5)]
    assert len(top_n_items(inv, 99)) == 3      # n larger than the inventory

    # everything survives an empty inventory
    assert top_n_items({}, 3) == []
    assert grand_total({}) == 0
    assert find_item({}, "apple") == []

    print("Extra checks passed.")


if __name__ == "__main__":
    run_tests()
    extra_tests()

    demo: Inventory = {
        "fruit": {"apple": 5, "banana": 3, "cherry": 12},
        "tools": {"hammer": 1, "saw": 2},
    }
    print(top_n_items(demo, 3))
