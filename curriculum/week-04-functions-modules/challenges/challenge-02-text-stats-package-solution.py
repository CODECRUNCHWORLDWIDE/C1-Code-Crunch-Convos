"""Text statistics: count the words in a paragraph and rank them.

Challenge 2, Week 4, Code Crunch Convos.

The project this answers is two files. ``text_stats.py`` holds ``analyze`` and
its two private helpers; ``main.py`` imports ``analyze`` and prints the demo.
This download folds both halves into one file so that it runs the moment you
save it: everything above the ``main.py half`` banner is what ``text_stats.py``
contains, and everything below it is what ``main.py`` contains. The page beside
this file shows the two-file split, and the package version -- a folder with an
``__init__.py`` in it -- that the challenge's title promises.

Nothing here asks a question, so there is no input handling to arrange. The
whole file is pure computation plus one printing function.

Run it with::

    python challenge-02-text-stats-package-solution.py
"""

import string
from collections import Counter

# --- the text_stats.py half: computation, and nothing else -----------------

_PUNCT = string.punctuation


def _normalize(word: str) -> str:
    """Lowercase and strip leading/trailing punctuation."""
    return word.strip(_PUNCT).lower()


def _tokenize(text: str) -> list[str]:
    """Split `text` into normalized words, dropping empties."""
    return [w for w in (_normalize(raw) for raw in text.split()) if w]


def analyze(text: str) -> dict[str, object]:
    """Return a stats dict for `text`."""
    words = _tokenize(text)
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    total_letters = sum(len(w) for w in words)
    avg = round(total_letters / len(words), 2) if words else 0.0
    return {
        "word_count": len(words),
        "char_count": len(text),
        "avg_word_length": avg,
        "top_3_words": ranked[:3],
    }


def _self_test() -> None:
    """Run a small self-test over the documented edge cases."""
    cases: list[tuple[str, dict[str, object]]] = [
        ("", {"word_count": 0, "char_count": 0, "avg_word_length": 0.0, "top_3_words": []}),
        ("   ", {"word_count": 0, "char_count": 3, "avg_word_length": 0.0, "top_3_words": []}),
        ("hello!!!", {"word_count": 1, "char_count": 8, "avg_word_length": 5.0,
                      "top_3_words": [("hello", 1)]}),
        ("don't", {"word_count": 1, "char_count": 5, "avg_word_length": 5.0,
                   "top_3_words": [("don't", 1)]}),
        ("b b a a c", {"word_count": 5, "char_count": 9, "avg_word_length": 1.0,
                       "top_3_words": [("a", 2), ("b", 2), ("c", 1)]}),
    ]
    for text, expected in cases:
        got = analyze(text)
        if got != expected:
            print(f"FAIL: analyze({text!r})\n  got      {got}\n  expected {expected}")
            return
    print("OK")


# --- the main.py half: printing the demo -----------------------------------

# Import choice. In the two-file version this line reads
# ``from text_stats import analyze``, because the module's whole public surface
# is that one name and repeating ``text_stats.`` in front of it says nothing.

PARAGRAPH = """The quick brown fox jumps over the lazy dog. The dog was not amused.
The fox, however, was delighted. The fox is the fox is the fox."""


def main() -> None:
    """Analyze the demo paragraph and print each statistic."""
    stats = analyze(PARAGRAPH)
    avg = stats["avg_word_length"]
    print(f"Words: {stats['word_count']}")
    print(f"Characters: {stats['char_count']}")
    print(f"Average word length: {avg:.2f}")
    print("Top 3 words:")
    for word, count in stats["top_3_words"]:
        print(f"  {word}: {count}")


if __name__ == "__main__":
    _self_test()
    print()
    main()
