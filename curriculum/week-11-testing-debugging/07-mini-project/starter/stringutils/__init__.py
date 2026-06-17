"""``stringutils`` — small, well-tested string helpers.

This package is the Week 11 mini-project of the Code Crunch Convos
bootcamp. The public API is intentionally tiny so that you can reach
100% test coverage in a single afternoon.

Public functions:

- :func:`slugify`
- :func:`truncate`
- :func:`word_count`
- :func:`reverse_words`
- :func:`is_palindrome`
"""

from __future__ import annotations

from stringutils.core import (
    is_palindrome,
    reverse_words,
    slugify,
    truncate,
    word_count,
)

__all__ = [
    "is_palindrome",
    "reverse_words",
    "slugify",
    "truncate",
    "word_count",
]

__version__ = "0.1.0"
