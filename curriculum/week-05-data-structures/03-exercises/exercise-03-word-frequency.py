"""
Exercise 03 — Word Frequency
Goal: count how often each word appears in a paragraph and print the top 5.

You will implement this WITHOUT collections.Counter first (to build intuition),
then a stretch goal asks you to redo it with Counter.

Run:
    python exercise-03-word-frequency.py
"""

from __future__ import annotations

import string

# ---- Given data ----------------------------------------------------------

PARAGRAPH = """
Python is a programming language that lets you work quickly and integrate
systems more effectively. Python is powerful and easy to learn. Python has
efficient high-level data structures and a simple but effective approach to
object-oriented programming. Python's elegant syntax and dynamic typing,
together with its interpreted nature, make it an ideal language for scripting
and rapid application development in many areas on most platforms.
"""


# ---- Task 1: normalize and tokenize --------------------------------------
# Lowercase the text and strip punctuation, then split on whitespace.
# Return a list of words.
#
# Hint: str.maketrans + str.translate, or a simple comprehension.

def tokenize(text: str) -> list[str]:
    # TODO: lowercase, strip punctuation, split.
    lowered = text.lower()
    # Build a translation table that maps every punctuation char to None.
    translator = str.maketrans("", "", string.punctuation)
    cleaned = lowered.translate(translator)
    return cleaned.split()


# ---- Task 2: count frequencies with a dict -------------------------------

def word_counts(words: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    # TODO: walk `words`, use counts.get(w, 0) + 1 (or setdefault).
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


# ---- Task 3: top N by frequency ------------------------------------------
# Return a list of (word, count) tuples, sorted by count DESC, then word ASC
# (alphabetical tiebreaker). Keep only the top `n` entries.

def top_n(counts: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    # TODO: items(), sort with a 2-part key, slice.
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


# ---- Self-check ----------------------------------------------------------

if __name__ == "__main__":
    words = tokenize(PARAGRAPH)
    assert "python" in words, "Did you lowercase?"
    assert "python," not in words, "Did you strip punctuation?"
    assert "Python" not in words

    counts = word_counts(words)
    assert counts["python"] >= 3, "Expected 'python' to appear several times."
    assert counts["and"] >= 4

    top = top_n(counts, n=5)
    assert len(top) == 5
    assert top[0][1] >= top[1][1] >= top[2][1]   # non-increasing

    # Pretty print for human inspection
    print("Top 5 most common words:")
    for word, count in top:
        print(f"  {word:<12} {count}")

    print("\nAll checks passed.")


# ---- STRETCH -------------------------------------------------------------
# 1. Filter out "stop words" (a, an, the, and, is, to, of, in, ...).
# 2. Re-implement word_counts using collections.Counter and Counter.most_common.
# 3. Read a real text file (paragraph from any book in Project Gutenberg) and
#    show its top 20 words. Preview for next week's file I/O lecture.
