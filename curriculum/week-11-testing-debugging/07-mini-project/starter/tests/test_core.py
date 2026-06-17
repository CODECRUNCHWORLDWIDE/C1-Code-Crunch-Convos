"""Tests for ``stringutils.core``.

This is the skeleton you fill in for the Week 11 mini-project. Each
function gets a small block of tests below. The blocks already include
the most important happy-path assertion and at least one edge case —
your job is to add the remaining tests until ``pytest --cov`` reports
100% line and branch coverage.

Run:

    pytest -v
    pytest --cov=stringutils --cov-branch --cov-report=term-missing
"""

from __future__ import annotations

import pytest

from stringutils import (
    is_palindrome,
    reverse_words,
    slugify,
    truncate,
    word_count,
)


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------


def test_slugify_simple() -> None:
    assert slugify("Hello World") == "hello-world"


def test_slugify_strips_punctuation() -> None:
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_collapses_whitespace() -> None:
    assert slugify("   spaced   out   ") == "spaced-out"


# TODO: add a test for empty input. Expected: ``slugify("") == ""``.
# TODO: add a test that mixed case is lowercased.
# TODO: add a test for an all-punctuation input. Expected: ``""``.


# ---------------------------------------------------------------------------
# truncate
# ---------------------------------------------------------------------------


def test_truncate_short_string_unchanged() -> None:
    assert truncate("Hello", 10) == "Hello"


def test_truncate_long_string_uses_default_suffix() -> None:
    assert truncate("Hello, World!", 8) == "Hello..."


def test_truncate_custom_suffix() -> None:
    assert truncate("Hello", 3, suffix="…") == "He…"


# TODO: assert that the *length* of the truncated string equals
# ``max_length`` whenever truncation actually happens. Try several
# (text, max_length) pairs.
# TODO: assert that a ``max_length`` smaller than the suffix raises
# ``ValueError``. Use ``pytest.raises``.


# ---------------------------------------------------------------------------
# word_count
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected",
    [
        ("one two three", 3),
        ("", 0),
        ("   ", 0),
        ("solo", 1),
        ("  many   spaces   between  ", 3),
    ],
)
def test_word_count(text: str, expected: int) -> None:
    assert word_count(text) == expected


# ---------------------------------------------------------------------------
# reverse_words
# ---------------------------------------------------------------------------


def test_reverse_words_simple() -> None:
    assert reverse_words("the quick brown fox") == "fox brown quick the"


def test_reverse_words_collapses_extra_whitespace() -> None:
    assert reverse_words("  hello   world  ") == "world hello"


def test_reverse_words_empty() -> None:
    assert reverse_words("") == ""


# TODO: add a test for single-word input ("solo" -> "solo").


# ---------------------------------------------------------------------------
# is_palindrome
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected",
    [
        ("racecar", True),
        ("RaceCar", True),
        ("A man, a plan, a canal: Panama", True),
        ("not a palindrome", False),
        ("", True),
        ("a", True),
        ("ab", False),
    ],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) is expected
