"""Public surface of the ``stringutils`` package."""

from __future__ import annotations

from stringutils.core import is_palindrome, reverse_words, slugify, truncate, word_count

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "is_palindrome",
    "reverse_words",
    "slugify",
    "truncate",
    "word_count",
]
