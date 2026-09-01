"""exercise-02-deduplicate-solution.py — one entry per human, order kept.

Three functions over a sign-up list. Two of them remove duplicates while
keeping the order people first appeared; the third reports the first repeat
it meets and stops there.

All three keep a `set` beside a `list` and use each for the one job it is
good at: the set answers "have I seen this?", the list remembers the order.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
SIGNUPS: list[str] = [
    "Ada@crunch.dev",
    "grace@crunch.dev",
    "ada@crunch.dev",
    "linus@crunch.dev",
    "grace@crunch.dev",
    "  ada@crunch.dev  ",
    " margaret@crunch.dev",
]


# ---- Your task ----
def dedupe(items: list[str]) -> list[str]:
    """Return a new list with exact duplicates removed, first-seen order kept.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        A new list holding the first sighting of each exact string.
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def dedupe_case_insensitive(items: list[str]) -> list[str]:
    """Return a new list deduplicated after stripping and lowercasing.

    The output keeps the ORIGINAL spelling of the first occurrence, not the
    normalised form used for comparison.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        A new list holding the first sighting of each normalised address,
        spelled the way it arrived.
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.strip().lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def first_duplicate(items: list[str]) -> str | None:
    """Return the first item that appears twice (exact match), or None.

    Args:
        items: The raw entries. This list is not modified.

    Returns:
        The repeated string, or None when nothing repeats.
    """
    seen: set[str] = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print(f"raw signups:        {len(SIGNUPS)}")
    print(f"exact dedupe:       {len(dedupe(SIGNUPS))}")
    print(f"normalised dedupe:  {len(dedupe_case_insensitive(SIGNUPS))}")
    print(f"first duplicate:    {first_duplicate(SIGNUPS)}")

    assert dedupe(SIGNUPS) == [
        "Ada@crunch.dev",
        "grace@crunch.dev",
        "ada@crunch.dev",
        "linus@crunch.dev",
        "  ada@crunch.dev  ",
        " margaret@crunch.dev",
    ]
    assert dedupe_case_insensitive(SIGNUPS) == [
        "Ada@crunch.dev",
        "grace@crunch.dev",
        "linus@crunch.dev",
        " margaret@crunch.dev",
    ]
    assert first_duplicate(SIGNUPS) == "grace@crunch.dev"
    assert first_duplicate(["a", "b", "c"]) is None
    assert dedupe([]) == []
    assert SIGNUPS[2] == "ada@crunch.dev"  # input list untouched
    print("All checks passed.")
