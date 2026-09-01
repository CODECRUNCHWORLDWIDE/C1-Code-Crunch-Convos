"""Five small, pure string helpers.

Every function here takes strings in and returns a value out. No globals, no
logging, no I/O — which is exactly why the test suite for this module runs in
milliseconds and reaches 100 % branch coverage without a single mock.
"""

from __future__ import annotations

__all__ = ["is_palindrome", "reverse_words", "slugify", "truncate", "word_count"]


def slugify(text: str) -> str:
    """Return *text* as a lowercase, hyphen-separated URL slug.

    Runs of non-alphanumeric characters collapse to a single ``-`` and leading
    or trailing separators are dropped.

    >>> slugify("Hello, World!")
    'hello-world'
    """
    normalized = "".join(char if char.isalnum() else " " for char in text.lower())
    return "-".join(normalized.split())


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Shorten *text* to at most *max_length* characters, ending with *suffix*.

    Text that already fits is returned unchanged. Otherwise the text is cut to
    ``max_length - len(suffix)`` characters and *suffix* is appended, so the
    result is exactly *max_length* characters long.

    Raises:
        ValueError: if *text* needs truncating but *suffix* alone would not fit
            inside *max_length*.

    >>> truncate("Hello, World!", 8)
    'Hello...'
    """
    if len(text) <= max_length:
        return text
    if len(suffix) > max_length:
        raise ValueError(f"suffix {suffix!r} is longer than max_length={max_length}")
    return text[: max_length - len(suffix)] + suffix


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in *text*.

    >>> word_count("one two three")
    3
    """
    return len(text.split())


def reverse_words(text: str) -> str:
    """Return *text* with its words in reverse order, separated by single spaces.

    >>> reverse_words("the quick brown fox")
    'fox brown quick the'
    """
    return " ".join(reversed(text.split()))


def is_palindrome(text: str) -> bool:
    """Return True if *text* reads the same both ways.

    Case and non-alphanumeric characters are ignored, so punctuation and
    spacing do not count against a phrase.

    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    """
    cleaned = [char for char in text.lower() if char.isalnum()]
    return cleaned == cleaned[::-1]
