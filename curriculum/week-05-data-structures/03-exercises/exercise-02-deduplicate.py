"""
Exercise 02 — Deduplicate
Goal: remove duplicate items from a list. Two flavours:
  1. Preserve original order (the "first occurrence wins").
  2. Don't care about order — just be fast.

Run:
    python exercise-02-deduplicate.py
"""

from __future__ import annotations


# ---- Task 1: order-preserving deduplication ------------------------------
# Return a new list with duplicates removed, keeping the order of first occurrence.
# Example: ["a", "b", "a", "c", "b", "d"]  ->  ["a", "b", "c", "d"]
#
# Hint: keep a `seen` set and walk the list once.

def dedupe_ordered(items: list) -> list:
    seen: set = set()
    result: list = []
    # TODO: loop over items; if not seen, add to result and to seen.
    for x in items:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result


# ---- Task 2: fast deduplication, order not required ----------------------
# Use the set() trick. Note: the resulting order is NOT guaranteed.

def dedupe_fast(items: list) -> list:
    # TODO: one expression
    return list(set(items))


# ---- Task 3: deduplicate by KEY ------------------------------------------
# Given a list of dicts, keep only the first occurrence per `key` value.
# Example: dedupe_by([{"id": 1, ...}, {"id": 2, ...}, {"id": 1, ...}], "id")
#          -> [first dict, second dict]   (the third is dropped)

def dedupe_by(records: list[dict], key: str) -> list[dict]:
    seen: set = set()
    result: list[dict] = []
    # TODO: loop, check if record[key] is in seen, add otherwise.
    for r in records:
        k = r[key]
        if k not in seen:
            seen.add(k)
            result.append(r)
    return result


# ---- Self-check ----------------------------------------------------------

if __name__ == "__main__":
    # Task 1
    assert dedupe_ordered(["a", "b", "a", "c", "b", "d"]) == ["a", "b", "c", "d"]
    assert dedupe_ordered([1, 1, 1, 1]) == [1]
    assert dedupe_ordered([]) == []
    assert dedupe_ordered([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [3, 1, 4, 5, 9, 2, 6]

    # Task 2 — order not checked, but contents must match
    out = dedupe_fast([1, 2, 2, 3, 3, 3])
    assert sorted(out) == [1, 2, 3]

    # Task 3
    people = [
        {"id": 1, "name": "Ada"},
        {"id": 2, "name": "Grace"},
        {"id": 1, "name": "Ada Lovelace"},   # duplicate id, dropped
        {"id": 3, "name": "Linus"},
    ]
    cleaned = dedupe_by(people, "id")
    assert len(cleaned) == 3
    assert cleaned[0]["name"] == "Ada"        # FIRST occurrence kept

    print("All checks passed.")


# ---- STRETCH -------------------------------------------------------------
# 1. Implement dedupe_ordered using `dict.fromkeys(items)` -- a one-liner trick
#    that works because dicts preserve insertion order since 3.7.
# 2. Add a `case_insensitive` flag to dedupe_ordered for strings.
# 3. Benchmark dedupe_ordered vs dedupe_fast on a list of 100,000 random ints
#    using `timeit`. Which is faster? Why?
