"""
Exercise 05 — Comprehensions
Goal: convert six explicit for-loops into list, dict, or set comprehensions.

For each "v1" function (the loop) there is a "v2" stub for you to fill in
using a comprehension. The self-check verifies that v1 and v2 return the
same value for the same input.

Run:
    python exercise-05-comprehensions.py
"""

from __future__ import annotations


# =========================================================================
# 1. Squares of the even numbers in a list  ->  list comprehension
# =========================================================================

def even_squares_v1(nums: list[int]) -> list[int]:
    result: list[int] = []
    for n in nums:
        if n % 2 == 0:
            result.append(n * n)
    return result


def even_squares_v2(nums: list[int]) -> list[int]:
    # TODO: replace with a comprehension
    return [n * n for n in nums if n % 2 == 0]


# =========================================================================
# 2. Convert temperatures C -> F  ->  list comprehension with formula
# =========================================================================

def celsius_to_fahrenheit_v1(temps_c: list[float]) -> list[float]:
    out: list[float] = []
    for c in temps_c:
        out.append(c * 9 / 5 + 32)
    return out


def celsius_to_fahrenheit_v2(temps_c: list[float]) -> list[float]:
    # TODO
    return [c * 9 / 5 + 32 for c in temps_c]


# =========================================================================
# 3. Build a {name: len(name)} mapping  ->  dict comprehension
# =========================================================================

def name_lengths_v1(names: list[str]) -> dict[str, int]:
    d: dict[str, int] = {}
    for name in names:
        d[name] = len(name)
    return d


def name_lengths_v2(names: list[str]) -> dict[str, int]:
    # TODO
    return {name: len(name) for name in names}


# =========================================================================
# 4. Unique vowels in a word          ->  set comprehension
# =========================================================================

def vowels_v1(word: str) -> set[str]:
    vowels: set[str] = set()
    for ch in word.lower():
        if ch in "aeiou":
            vowels.add(ch)
    return vowels


def vowels_v2(word: str) -> set[str]:
    # TODO
    return {ch for ch in word.lower() if ch in "aeiou"}


# =========================================================================
# 5. Label each grade as pass/fail    ->  list comp with if/else expression
# =========================================================================

def pass_fail_v1(grades: list[int]) -> list[str]:
    labels: list[str] = []
    for g in grades:
        if g >= 60:
            labels.append("pass")
        else:
            labels.append("fail")
    return labels


def pass_fail_v2(grades: list[int]) -> list[str]:
    # TODO: ternary inside the comprehension
    return ["pass" if g >= 60 else "fail" for g in grades]


# =========================================================================
# 6. Cartesian product of two lists, excluding equal pairs ->  nested comp
# =========================================================================

def cross_pairs_v1(xs: list[int], ys: list[int]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for x in xs:
        for y in ys:
            if x != y:
                pairs.append((x, y))
    return pairs


def cross_pairs_v2(xs: list[int], ys: list[int]) -> list[tuple[int, int]]:
    # TODO: two `for` clauses + an `if`
    return [(x, y) for x in xs for y in ys if x != y]


# ---- Self-check ----------------------------------------------------------

if __name__ == "__main__":
    sample_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sample_temps = [0.0, 100.0, 25.0, -40.0]
    sample_names = ["Ada", "Grace", "Linus"]
    sample_word = "Antidisestablishmentarianism"
    sample_grades = [55, 60, 88, 42, 100]
    sample_xs = [1, 2, 3]
    sample_ys = [2, 3, 4]

    assert even_squares_v1(sample_nums) == even_squares_v2(sample_nums)
    assert celsius_to_fahrenheit_v1(sample_temps) == celsius_to_fahrenheit_v2(sample_temps)
    assert name_lengths_v1(sample_names) == name_lengths_v2(sample_names)
    assert vowels_v1(sample_word) == vowels_v2(sample_word)
    assert pass_fail_v1(sample_grades) == pass_fail_v2(sample_grades)
    assert cross_pairs_v1(sample_xs, sample_ys) == cross_pairs_v2(sample_xs, sample_ys)

    print("All six comprehensions match their loop versions. ")


# ---- STRETCH -------------------------------------------------------------
# 1. Write a generator expression that yields the SAME values as
#    even_squares_v2 but lazily. Sum them with sum(...).
# 2. Convert this nested loop into a single comprehension:
#       result = []
#       for row in matrix:
#           for x in row:
#               if x > 0:
#                   result.append(x * 2)
# 3. When does converting a loop to a comprehension HURT readability?
#    Find one example in your own past code or write one.
