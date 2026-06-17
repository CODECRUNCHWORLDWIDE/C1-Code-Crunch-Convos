"""
Exercise 01 — List Operations
Goal: practise sorting by a key, finding the max by an attribute,
and manipulating a list via slicing.

Run:
    python exercise-01-list-operations.py
"""

from __future__ import annotations

# ---- Given data ----------------------------------------------------------

# Each book is (title, author, year, pages)
books: list[tuple[str, str, int, int]] = [
    ("Fluent Python",         "Luciano Ramalho",   2022, 1014),
    ("Clean Code",            "Robert Martin",     2008,  464),
    ("The Pragmatic Programmer","Andy Hunt",       1999,  352),
    ("Python Crash Course",   "Eric Matthes",      2019,  544),
    ("Automate the Boring Stuff","Al Sweigart",    2019,  592),
    ("Effective Python",      "Brett Slatkin",     2019,  480),
]


# ---- Task 1: sort by year (ascending) ------------------------------------
# Return a NEW list, do not mutate `books`.
# Hint: sorted(... , key=...).  Use a lambda or operator.itemgetter.

def sort_by_year(books_in: list[tuple]) -> list[tuple]:
    # TODO: replace the next line
    return sorted(books_in, key=lambda b: b[2])


# ---- Task 2: sort by page count (descending) -----------------------------

def sort_by_pages_desc(books_in: list[tuple]) -> list[tuple]:
    # TODO
    return sorted(books_in, key=lambda b: b[3], reverse=True)


# ---- Task 3: find the longest book (max by page count) -------------------
# Return the whole tuple for the longest book.

def longest_book(books_in: list[tuple]) -> tuple:
    # TODO -- use the built-in max() with a key=
    return max(books_in, key=lambda b: b[3])


# ---- Task 4: slice manipulation ------------------------------------------
# Given a list of integers, return a NEW list where:
#   - the first two items are removed
#   - the last item is removed
#   - the middle is reversed
# Example: [1, 2, 3, 4, 5, 6, 7] -> [6, 5, 4, 3]

def middle_reversed(nums: list[int]) -> list[int]:
    # TODO -- one expression using slicing
    return nums[2:-1][::-1]


# ---- Task 5: titles only -------------------------------------------------
# Return a list of just the titles, in the original order.
# Hint: a list comprehension is perfect.

def titles_only(books_in: list[tuple]) -> list[str]:
    # TODO
    return [b[0] for b in books_in]


# ---- Self-check ----------------------------------------------------------

if __name__ == "__main__":
    by_year = sort_by_year(books)
    assert by_year[0][2] == 1999, "Oldest book should be from 1999"
    assert by_year[-1][2] == 2022, "Newest book should be from 2022"

    by_pages = sort_by_pages_desc(books)
    assert by_pages[0][3] == 1014, "Longest book should be 1014 pages"

    longest = longest_book(books)
    assert longest[0] == "Fluent Python"

    assert middle_reversed([1, 2, 3, 4, 5, 6, 7]) == [6, 5, 4, 3]
    assert middle_reversed([10, 20, 30, 40]) == [30]

    titles = titles_only(books)
    assert titles[0] == "Fluent Python"
    assert len(titles) == len(books)

    # books must NOT have been mutated
    assert books[0][0] == "Fluent Python", "Don't mutate the input list!"

    print("All checks passed.")


# ---- STRETCH -------------------------------------------------------------
# 1. Sort books by author last name (alphabetical). Hint: split on space, take [-1].
# 2. Write `books_per_decade(books)` returning a dict like {2020: 1, 2010: 4, 1990: 1}.
# 3. Convert the list of tuples into a list of dicts with named keys.
