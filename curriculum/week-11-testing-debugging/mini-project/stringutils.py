"""stringutils.py — the finished answer to Week 11's mini-project.

Five small, pure string functions, plus the test suite that proves them and a
driver that runs it. Your own deliverable is a real package —
``stringutils/core.py``, ``tests/test_core.py``, a ``pyproject.toml`` and a CI
workflow — tested to 100 % coverage, formatted by ``black``, linted by ``ruff``,
and type-checked by ``mypy --strict``. This single file folds the module and its
tests together so the reference answer runs anywhere as a plain script: it drives
its own tests through pytest and prints a plain, same-every-time report.

Run it with::

    python stringutils.py
"""

from __future__ import annotations

import contextlib
import io
import re

import pytest

# --------------------------------------------------------------------------- #
# stringutils/core.py — five pure functions: a string in, a value out
# --------------------------------------------------------------------------- #


def slugify(text: str) -> str:
    """Turn text into a URL slug.

    Lowercase it, replace every run of non-alphanumeric characters with a single
    hyphen, and trim hyphens off the ends. ``"Hello, World!"`` becomes
    ``"hello-world"``.
    """
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Shorten *text* to at most *max_length* characters, ending with *suffix*.

    Text already short enough comes back untouched. Longer text is cut so that
    the result — visible characters plus the suffix — is exactly *max_length*.

    Raises:
        ValueError: If *suffix* is longer than *max_length*, because then there
            is no room for even one character of the text.
    """
    if len(suffix) > max_length:
        raise ValueError("suffix is longer than max_length")
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def word_count(text: str) -> int:
    """Count whitespace-separated words. An empty or blank string is ``0``."""
    return len(text.split())


def reverse_words(text: str) -> str:
    """Reverse the order of the words, joined by single spaces.

    ``"the quick brown fox"`` becomes ``"fox brown quick the"``.
    """
    return " ".join(reversed(text.split()))


def is_palindrome(text: str) -> bool:
    """True if *text* reads the same both ways, ignoring case and punctuation.

    ``"A man, a plan, a canal: Panama"`` is a palindrome; ``"hello"`` is not.
    """
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return cleaned == cleaned[::-1]


# --------------------------------------------------------------------------- #
# tests/test_core.py — the edge cases the spec calls out, table-driven
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello, World!", "hello-world"),
        ("   spaced   out   ", "spaced-out"),
        ("already-a-slug", "already-a-slug"),
        ("!!!", ""),
    ],
    ids=["punctuated", "padded", "idempotent", "all-symbols"],
)
def test_slugify(text: str, expected: str) -> None:
    assert slugify(text) == expected


@pytest.mark.parametrize(
    "text, max_length, suffix, expected",
    [
        ("Hello", 10, "...", "Hello"),
        ("Hello, World!", 8, "...", "Hello..."),
        ("Hello", 3, "…", "He…"),
        ("exact", 5, "...", "exact"),
    ],
    ids=["short-unchanged", "cut-with-dots", "unicode-ellipsis", "exact-length"],
)
def test_truncate(text: str, max_length: int, suffix: str, expected: str) -> None:
    assert truncate(text, max_length, suffix) == expected


def test_truncate_suffix_longer_than_max_raises() -> None:
    with pytest.raises(ValueError, match="longer than max_length"):
        truncate("Hi", 1)


@pytest.mark.parametrize(
    "text, expected",
    [("", 0), ("   ", 0), ("one two three", 3), ("  padded  words  ", 2)],
    ids=["empty", "all-space", "three", "padded"],
)
def test_word_count(text: str, expected: int) -> None:
    assert word_count(text) == expected


def test_reverse_words() -> None:
    assert reverse_words("the quick brown fox") == "fox brown quick the"


def test_reverse_words_empty_string() -> None:
    assert reverse_words("") == ""


@pytest.mark.parametrize(
    "text, expected",
    [
        ("A man, a plan, a canal: Panama", True),
        ("not a palindrome", False),
        ("", True),
        ("Was it a car or a cat I saw?", True),
    ],
    ids=["classic", "plain", "empty", "another"],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) is expected


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes."""
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Show the five functions at work, then run the suite and report."""
    print("stringutils — five pure functions:")
    print(f"  slugify('Hello, World!')          -> {slugify('Hello, World!')!r}")
    print(f"  truncate('Hello, World!', 8)      -> {truncate('Hello, World!', 8)!r}")
    print(f"  word_count('one two three')       -> {word_count('one two three')}")
    print(f"  reverse_words('the quick brown')  -> {reverse_words('the quick brown')!r}")
    print(f"  is_palindrome('Panama'-sentence)  -> {is_palindrome('A man, a plan, a canal: Panama')}")

    print()
    print("The suite, run the way pytest runs it:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
