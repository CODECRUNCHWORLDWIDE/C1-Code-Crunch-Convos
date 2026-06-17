"""
Exercise 04 — Set Operations
Goal: given two class rosters, answer overlap/exclusivity questions
using set operators (|, &, -, ^).

Run:
    python exercise-04-set-operations.py
"""

from __future__ import annotations

# ---- Given data ----------------------------------------------------------

class_a_students: list[str] = [
    "Ada Lovelace",
    "Grace Hopper",
    "Linus Torvalds",
    "Guido van Rossum",
    "Margaret Hamilton",
    "Barbara Liskov",
]

class_b_students: list[str] = [
    "Linus Torvalds",
    "Guido van Rossum",
    "Donald Knuth",
    "Alan Turing",
    "Margaret Hamilton",
    "Edsger Dijkstra",
]


# ---- Task 1: convert lists to sets ---------------------------------------

def to_set(names: list[str]) -> set[str]:
    # TODO: one-liner
    return set(names)


# ---- Task 2: students in BOTH classes ------------------------------------

def in_both(a: set[str], b: set[str]) -> set[str]:
    # TODO: use the right operator
    return a & b


# ---- Task 3: students in EITHER class (anyone enrolled) ------------------

def in_either(a: set[str], b: set[str]) -> set[str]:
    # TODO
    return a | b


# ---- Task 4: students ONLY in class A ------------------------------------

def only_in_a(a: set[str], b: set[str]) -> set[str]:
    # TODO
    return a - b


# ---- Task 5: students enrolled in EXACTLY one class ----------------------

def exactly_one(a: set[str], b: set[str]) -> set[str]:
    # TODO: symmetric difference
    return a ^ b


# ---- Self-check ----------------------------------------------------------

if __name__ == "__main__":
    A = to_set(class_a_students)
    B = to_set(class_b_students)

    assert in_both(A, B) == {"Linus Torvalds", "Guido van Rossum", "Margaret Hamilton"}
    assert in_either(A, B) == A | B   # trivially true if implemented correctly
    assert len(in_either(A, B)) == 9  # 6 + 6 - 3 overlap
    assert only_in_a(A, B) == {"Ada Lovelace", "Grace Hopper", "Barbara Liskov"}
    assert "Linus Torvalds" not in exactly_one(A, B)
    assert "Ada Lovelace" in exactly_one(A, B)
    assert "Donald Knuth" in exactly_one(A, B)

    # Pretty print
    print(f"Total unique students: {len(in_either(A, B))}")
    print(f"In both classes:        {sorted(in_both(A, B))}")
    print(f"Only in class A:        {sorted(only_in_a(A, B))}")
    print(f"In exactly one class:   {sorted(exactly_one(A, B))}")

    print("\nAll checks passed.")


# ---- STRETCH -------------------------------------------------------------
# 1. Suppose a third class C is added. Find students in ALL three classes,
#    and students in NONE (relative to in_either(A, B, C)). Hint: chain &.
# 2. Read class rosters from two text files (one name per line). Preview of
#    next week's file I/O.
# 3. Given a list of (student, class) tuples, build the per-class rosters
#    yourself using a dict[str, set[str]].
