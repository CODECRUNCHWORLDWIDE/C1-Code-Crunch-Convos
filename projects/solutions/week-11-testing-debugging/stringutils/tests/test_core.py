"""Tests for :mod:`stringutils.core`.

The suite is deliberately table-driven: one parametrized test per function,
with the edge cases the mini-project spec calls out plus the ones that keep
branch coverage at 100 %.
"""

from __future__ import annotations

import pytest

from stringutils import is_palindrome, reverse_words, slugify, truncate, word_count

# ---------------------------------------------------------------- slugify ---


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, World!", "hello-world"),
        ("   spaced   out   ", "spaced-out"),
        ("already-a-slug", "already-a-slug"),
        ("Code Crunch Worldwide", "code-crunch-worldwide"),
        ("snake_case_name", "snake-case-name"),
        ("Python 3.12 Release", "python-3-12-release"),
        ("---leading and trailing---", "leading-and-trailing"),
        ("", ""),
        ("   ", ""),
        ("!!!", ""),
        ("Café Crunch", "café-crunch"),
    ],
    ids=[
        "punctuation",
        "collapses-whitespace",
        "idempotent",
        "org-name",
        "underscore-is-not-alnum",
        "digits-survive-dots-do-not",
        "trims-both-ends",
        "empty",
        "all-whitespace",
        "all-punctuation",
        "unicode-letters-survive",
    ],
)
def test_slugify(text: str, expected: str) -> None:
    assert slugify(text) == expected


def test_slugify_is_idempotent() -> None:
    """Slugifying a slug must not change it — a property worth locking down."""
    once = slugify("Hello, World! Again")
    assert slugify(once) == once


# --------------------------------------------------------------- truncate ---


@pytest.mark.parametrize(
    ("text", "max_length", "suffix", "expected"),
    [
        ("Hello", 10, "...", "Hello"),
        ("Hello", 5, "...", "Hello"),
        ("Hello, World!", 8, "...", "Hello..."),
        ("Hello", 3, "…", "He…"),
        ("Hello", 3, "...", "..."),
        ("", 0, "...", ""),
        ("abcdef", 6, "...", "abcdef"),
        ("abcdef", 5, "..", "abc.."),
    ],
    ids=[
        "already-short",
        "exactly-max-length",
        "spec-example",
        "custom-unicode-suffix",
        "suffix-fills-the-budget",
        "empty-text-zero-budget",
        "boundary-fits",
        "boundary-one-over",
    ],
)
def test_truncate(text: str, max_length: int, suffix: str, expected: str) -> None:
    assert truncate(text, max_length, suffix=suffix) == expected


def test_truncate_result_never_exceeds_max_length() -> None:
    assert len(truncate("Hello, World!", 8)) == 8


def test_truncate_uses_ellipsis_by_default() -> None:
    assert truncate("Hello, World!", 8) == "Hello..."


def test_truncate_raises_when_suffix_does_not_fit() -> None:
    with pytest.raises(ValueError, match=r"longer than max_length=1"):
        truncate("Hi", 1)


def test_truncate_raises_on_negative_max_length() -> None:
    with pytest.raises(ValueError, match=r"longer than max_length=-1"):
        truncate("Hi", -1)


# ------------------------------------------------------------- word_count ---


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("   ", 0),
        ("one", 1),
        ("one two three", 3),
        ("  padded   words  ", 2),
        ("tabs\tand\nnewlines\rcount", 4),
    ],
    ids=["empty", "whitespace-only", "single", "three", "padded", "mixed-whitespace"],
)
def test_word_count(text: str, expected: int) -> None:
    assert word_count(text) == expected


# ---------------------------------------------------------- reverse_words ---


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("the quick brown fox", "fox brown quick the"),
        ("solo", "solo"),
        ("", ""),
        ("   ", ""),
        ("  double   spaced  words ", "words spaced double"),
    ],
    ids=["spec-example", "single-word", "empty", "whitespace-only", "normalizes-spacing"],
)
def test_reverse_words(text: str, expected: str) -> None:
    assert reverse_words(text) == expected


def test_reverse_words_twice_is_identity_for_normalized_text() -> None:
    text = "code crunch worldwide"
    assert reverse_words(reverse_words(text)) == text


# ---------------------------------------------------------- is_palindrome ---


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("A man, a plan, a canal: Panama", True),
        ("not a palindrome", False),
        ("racecar", True),
        ("RaceCar", True),
        ("No 'x' in Nixon", True),
        ("", True),
        ("   ", True),
        ("a", True),
        ("ab", False),
        ("12321", True),
        ("12345", False),
    ],
    ids=[
        "classic-phrase",
        "plain-false",
        "single-word",
        "case-insensitive",
        "punctuation-ignored",
        "empty-is-vacuously-true",
        "whitespace-only",
        "one-char",
        "two-different-chars",
        "digits-true",
        "digits-false",
    ],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) is expected
