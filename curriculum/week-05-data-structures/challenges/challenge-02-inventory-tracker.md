# Challenge 02 — Inventory Tracker

**Estimated time:** 90–120 minutes.
**Concepts used:** nested dicts, dict methods, comprehensions, type hints.

---

## The problem

You're writing the backend for a tiny warehouse system. The inventory is organized by **category**, and each category contains **items** with **integer counts**. You'll model it as a nested dictionary:

```python
inventory: dict[str, dict[str, int]] = {
    "fruit": {"apple": 5, "banana": 3, "cherry": 12},
    "tools": {"hammer": 1, "saw": 2},
    "books": {},
}
```

Build a small set of pure functions that operate on this structure.

---

## Required functions

All functions take an `inventory` argument and either return a value or return a new/modified inventory. **Do not** rely on mutating a global; pass the inventory in.

### 1. `add_item(inv, category, item, count=1)`

Add `count` of `item` to `category`. If the category doesn't exist, create it. If the item doesn't exist, create it with the given count. If it does exist, increment.

```python
add_item(inv, "fruit", "kiwi", 4)
# inv["fruit"]["kiwi"] == 4
add_item(inv, "fruit", "kiwi", 3)
# inv["fruit"]["kiwi"] == 7
```

Hint: `inv.setdefault(category, {})` is your friend.

### 2. `remove_item(inv, category, item, count=1)`

Subtract `count` of `item` from `category`. If the result reaches 0 or below, **delete** the item key. If the category becomes empty after the removal, **delete** the category key.

Raise `KeyError` if the category or item doesn't exist.

```python
remove_item(inv, "tools", "hammer", 1)
# "hammer" no longer in inv["tools"]
```

### 3. `category_total(inv, category) -> int`

Return the sum of all counts in `category`. Return `0` if the category doesn't exist (don't raise).

```python
category_total(inv, "fruit")    # e.g. 20
category_total(inv, "missing")  # 0
```

### 4. `grand_total(inv) -> int`

Return the sum of all counts across all categories.

### 5. `find_item(inv, item) -> list[str]`

Return a list of categories that contain `item`. Empty list if not found anywhere.

```python
find_item(inv, "apple")   # ["fruit"]
find_item(inv, "phantom") # []
```

### 6. `top_n_items(inv, n=3) -> list[tuple[str, str, int]]`

Return the `n` highest-count items across the entire inventory, each as a tuple `(category, item, count)`, sorted by count descending. Ties broken by `(category, item)` alphabetical.

```python
top_n_items(inv, 3)
# [("fruit", "cherry", 12), ("fruit", "apple", 5), ("fruit", "banana", 3)]
```

---

## Worked test scaffolding (build your `solution.py` against this)

```python
def run_tests() -> None:
    inv: dict[str, dict[str, int]] = {}

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

    # remove some
    remove_item(inv, "fruit", "banana", 3)      # banana -> 0 -> deleted
    assert "banana" not in inv["fruit"]

    remove_item(inv, "tools", "hammer", 1)      # hammer gone -> category empty -> deleted
    assert "tools" not in inv

    # KeyError on bad path
    try:
        remove_item(inv, "fruit", "phantom", 1)
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError")

    # top_n
    add_item(inv, "fruit", "cherry", 12)
    add_item(inv, "fruit", "date", 2)
    top = top_n_items(inv, 3)
    assert top[0] == ("fruit", "cherry", 12)
    assert len(top) == 3

    print("All checks passed.")

if __name__ == "__main__":
    run_tests()
```

---

## Rubric

| Criterion | Points |
|---|---|
| All 6 functions implemented | 50 (≈8 each) |
| Test scaffolding passes | 20 |
| Correct deletion of empty inner dicts | 10 |
| Type hints throughout | 10 |
| Reflection on design choices (docstring at top) | 10 |
| **Total** | **100** |

---

## Stretch

1. **Persistence** — save and load `inv` to/from `inventory.json`. Use `json.dump`/`json.load`. (Preview of next week.)
2. **`defaultdict` rewrite** — refactor `add_item` to use `collections.defaultdict(lambda: defaultdict(int))`. Compare readability.
3. **`Counter`** — would `Counter` simplify any of the inner dicts? Try replacing `dict[str, int]` with `Counter`. What changes?
4. **Pretty print** — write a `render(inv)` that returns a nicely formatted multi-line string of the whole inventory.
5. **Add a `move_item(inv, from_cat, to_cat, item, count)`** — atomically subtract from one category and add to another, raising if anything is wrong (without leaving the inventory in a broken state).
