"""exercise-03-word-frequency-solution.py — which words keep coming up.

Three functions, one job each: clean the text into words, count the words
into a dict, rank the dict into a top-N list.

The counting is `counts.get(word, 0) + 1` and nothing else. The ranking is a
two-part sort key, so words that tie on count come out in a fixed order.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
NOTES: str = (
    "Loops are fun. Loops are hard. "
    "Dicts are fast, and dicts are everywhere. "
    " Practice loops, practice dicts, practice sets!"
)

PUNCTUATION: str = ".,!?;:"


# ---- Your task ----
def normalize(text: str) -> list[str]:
    """Split text into lowercase words with edge punctuation removed.

    Empty tokens are dropped.

    Args:
        text: The raw notes.

    Returns:
        The words, lowercased, in the order they appeared.
    """
    words: list[str] = []
    for token in text.split():
        word = token.strip(PUNCTUATION).lower()
        if word:
            words.append(word)
    return words


def count_words(words: list[str]) -> dict[str, int]:
    """Return a dict mapping each word to how many times it appears.

    Args:
        words: The cleaned words, in any order.

    Returns:
        A dict whose values add back up to len(words).
    """
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Return the n most frequent (word, count) pairs.

    Highest count first. Ties are broken by the word, A to Z.

    Args:
        counts: The tally to rank.
        n: How many pairs to return.

    Returns:
        Up to n (word, count) pairs, best first.
    """
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]


# ---- Self-check ----
if __name__ == "__main__":
    words = normalize(NOTES)
    counts = count_words(words)

    print(f"{len(words)} words, {len(counts)} unique")
    for word, count in top_n(counts, 3):
        print(f"{word:<12}{count}")

    assert len(words) == 19
    assert len(counts) == 10
    assert sum(counts.values()) == 19
    assert counts["are"] == 4
    assert counts["practice"] == 3
    assert counts.get("missing", 0) == 0
    assert top_n(counts, 3) == [("are", 4), ("dicts", 3), ("loops", 3)]
    print("All checks passed.")
