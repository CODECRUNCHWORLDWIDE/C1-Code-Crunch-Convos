# Mini-Project — `stringutils`

> **Topic:** A whole small package, tested to 100 %: five pure functions, `pytest`, coverage, and the quality tools
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md) · [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md) · [03 — Quality tools and CI](../lecture-notes/03-quality-tools-and-ci.md)
> **Difficulty:** Medium
> **Target time:** 4-6 hours
> **Why this one:** every skill from the week meets here. You stop reading about `pytest`, coverage, `ruff`, `black`, `mypy`, and CI and use all of them together on one small, real, publishable package.

## The Brief

Ship a tiny Python package called `stringutils` — five small functions that each
take a string and hand back a value. That is the whole library. It is small on
purpose, because the point is not the code; it is everything you wrap around it:
a test for every branch, a coverage report that proves it, formatting and linting
that never argue, type hints a checker accepts, and a robot on GitHub that runs
all of it every time you push.

Think of it like a workshop, not a birdhouse. The birdhouse — the five functions
— takes an afternoon. The workshop — the tests, the tools, the green checkmark a
stranger sees first — is the part you keep and reuse on every project after this
one.

The five functions:

| Function | Signature | Behaviour |
|---|---|---|
| `slugify` | `(text) -> str` | Lowercase; replace runs of non-alphanumeric characters with `-`; trim `-` off the ends. |
| `truncate` | `(text, max_length, suffix="...") -> str` | Short text is unchanged; longer text is cut so the result plus suffix is exactly `max_length`. |
| `word_count` | `(text) -> int` | Count whitespace-separated words; a blank string is `0`. |
| `reverse_words` | `(text) -> str` | Reverse the word order, single spaces between. |
| `is_palindrome` | `(text) -> bool` | Reads the same both ways, ignoring case and punctuation. |

## Starter

Your deliverable is a real package, not one script:

```text
stringutils/
├── pyproject.toml
├── README.md
├── .github/workflows/ci.yml
├── stringutils/
│   ├── __init__.py        # re-exports the five functions
│   └── core.py            # the implementations
└── tests/
    └── test_core.py       # a test for every branch
```

Start `stringutils/core.py` with the five signatures and a `NotImplementedError`
in each, then TDD them one at a time:

```python
"""core.py — five pure string helpers."""


def slugify(text: str) -> str:
    """Lowercase, hyphenate runs of non-alphanumerics, trim the ends."""
    raise NotImplementedError


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Cut text to max_length, ending with suffix; raise if suffix won't fit."""
    raise NotImplementedError


def word_count(text: str) -> int:
    """Count whitespace-separated words."""
    raise NotImplementedError


def reverse_words(text: str) -> str:
    """Reverse the order of the words."""
    raise NotImplementedError


def is_palindrome(text: str) -> bool:
    """True if it reads the same both ways, ignoring case and punctuation."""
    raise NotImplementedError
```

## Requirements

1. **All five functions** behave exactly as the table describes, including the
   edge cases below.
2. **`truncate("Hi", 1)` raises `ValueError`** — the suffix is longer than
   `max_length`, so there is no room for even one character of text.
3. **100 % line *and* branch coverage** on `stringutils/`
   (`pytest --cov=stringutils --cov-branch --cov-fail-under=100`).
4. **`ruff check .` and `black --check .` pass**, and **`mypy --strict`** is
   clean.
5. **A GitHub Actions workflow** runs the tests on every push and pull request,
   and the README shows a green CI badge.
6. The functions are **pure** — a string in, a value out. No globals, no
   logging, no I/O.

Edge cases your tests must cover (not exhaustive): `slugify("Hello, World!")` →
`"hello-world"`; `slugify("   spaced   out   ")` → `"spaced-out"`;
`truncate("Hello", 10)` → `"Hello"`; `truncate("Hello, World!", 8)` →
`"Hello..."`; `truncate("Hello", 3, suffix="…")` → `"He…"`; `word_count("")` →
`0`; `word_count("   ")` → `0`; `reverse_words("the quick brown fox")` →
`"fox brown quick the"`; `is_palindrome("A man, a plan, a canal: Panama")` →
`True`.

## Constraints

- **Pure functions only.** A function that reads a file or prints is one you
  cannot test with a plain `assert result == expected`. Keep the five functions
  free of side effects and the tests stay one line each.
- **Cover the branches, not just the lines.** `truncate` has three paths — suffix
  too long, text short enough, text too long — and 100 % *statement* coverage can
  miss one of them. Turn on `--cov-branch` (Exercise 5's whole lesson) so the
  report tells the truth.
- **`ruff` first with `--fix`, then `black`.** They can disagree on small things;
  running `ruff --fix` and then `black` settles it. Give both the same
  `line-length` in `pyproject.toml`.
- **`target-version` names your *oldest* interpreter.** If CI runs 3.11 and 3.12,
  set `target-version = "py311"`. Naming the newer one lets `ruff` rewrite code
  into syntax the older interpreter cannot parse, turning half your CI matrix red.

## Expected output

The finished answer that ships beside this page,
[stringutils.py](./stringutils.py), folds the five functions and their tests into
one file so it runs anywhere. It drives its own suite through pytest and prints:

```text
$ python stringutils.py
stringutils — five pure functions:
  slugify('Hello, World!')          -> 'hello-world'
  truncate('Hello, World!', 8)      -> 'Hello...'
  word_count('one two three')       -> 3
  reverse_words('the quick brown')  -> 'brown quick the'
  is_palindrome('Panama'-sentence)  -> True

The suite, run the way pytest runs it:
  PASS  test_slugify[punctuated]
  PASS  test_slugify[padded]
  PASS  test_slugify[idempotent]
  PASS  test_slugify[all-symbols]
  PASS  test_truncate[short-unchanged]
  PASS  test_truncate[cut-with-dots]
  PASS  test_truncate[unicode-ellipsis]
  PASS  test_truncate[exact-length]
  PASS  test_truncate_suffix_longer_than_max_raises
  PASS  test_word_count[empty]
  PASS  test_word_count[all-space]
  PASS  test_word_count[three]
  PASS  test_word_count[padded]
  PASS  test_reverse_words
  PASS  test_reverse_words_empty_string
  PASS  test_is_palindrome[classic]
  PASS  test_is_palindrome[plain]
  PASS  test_is_palindrome[empty]
  PASS  test_is_palindrome[another]

19 passed, 0 failed
```

Your own build keeps the functions in `stringutils/core.py` and the tests in
`tests/test_core.py`, and you run `pytest --cov=stringutils --cov-branch`.

## Steps

1. Copy the starter into a repo of your own and make a virtual environment.
2. TDD each function: write a failing test, watch it fail, implement, watch it
   pass, look for a refactor. Repeat for all five.
3. Run `pytest --cov=stringutils --cov-branch --cov-report=term-missing`. Chase
   the `Missing` column and any partial branch to zero.
4. Add `ruff`, `black`, and `mypy --strict` config to `pyproject.toml`; get all
   three clean.
5. Add `.github/workflows/ci.yml` that runs the four checks on 3.11 and 3.12.
6. Push, watch the Actions tab go green, and add the badge to your README.

## The Solution

```python
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
```

**Why it works.** Every function is one small idea. `slugify` lets a single
regular expression do the work: `[^a-z0-9]+` matches any run of "not a letter or
digit" and replaces the whole run with one hyphen, then `.strip("-")` trims the
ends, so `"   spaced   out   "` collapses to `"spaced-out"` in one line.
`truncate` checks the impossible case first — a suffix longer than `max_length`
leaves no room, so it raises before doing anything else — then returns short text
untouched, and otherwise keeps exactly `max_length - len(suffix)` characters and
appends the suffix, so the result is always exactly `max_length` wide.
`word_count` leans on `str.split()` with no argument, which treats any run of
whitespace as one separator and drops empties, so `"   "` counts as zero words
for free. `reverse_words` splits, reverses, and re-joins with single spaces.
`is_palindrome` strips the text down to lowercase letters and digits, then
compares it to its reverse with a slice — `cleaned[::-1]` — so punctuation and
capitals never get a vote.

The tests are table-driven on purpose: each edge case from the spec is a row, so
a new case costs a line, and 100 % branch coverage falls out because every path —
`truncate`'s three, `slugify`'s empty result, `word_count`'s blank string — has a
row that reaches it.

## Download and run

<!-- no-runnable-file: the deliverable is a package in your own repository — stringutils/core.py, tests/, a pyproject.toml, and a CI workflow — not a single script. The finished answer ships as stringutils.py, which folds the module and its tests into one file so it runs on its own, and is linked below. -->

Download [stringutils.py](./stringutils.py) and run it:

```bash
pip install pytest
python stringutils.py
```

It drives its own tests with pytest and prints the run above — no package layout
required. Your own build is the `stringutils/` package plus `tests/`, run with
`pytest --cov=stringutils --cov-branch`.

## Common bugs to catch

- **`slugify` leaves a leading or trailing hyphen.** You replaced the symbols but
  forgot `.strip("-")`. `"Hello, World!"` becomes `"hello-world-"` because the
  trailing `!` turned into a hyphen.
- **`truncate` returns a string longer than `max_length`.** You appended the
  suffix without shortening the text first. Cut to `max_length - len(suffix)`,
  then append.
- **`word_count(" ")` returns `1`.** You wrote `text.split(" ")` with an explicit
  space, which keeps empty strings. Plain `text.split()` collapses whitespace.
- **`is_palindrome` says a punctuated sentence is not a palindrome.** You compared
  the raw text. Strip it to letters and digits and lowercase it first.
- **100 % statements but 96 % branch.** A path exists that no test reaches —
  almost always `truncate`'s "suffix too long" raise or its "already short"
  return. Add the row that hits it. This is Exercise 5, now on your own code.

## Under the hood

<details>
<summary>Under the hood — why these functions are trivial to test, and unicode's last word</summary>

Everything that makes this package easy to test is a choice, not luck. The
functions are **pure**: given the same input they return the same output and
touch nothing else, so a test is `assert f(x) == y` with no setup and no
teardown. There are no fixtures here because there is no state to build.

The one genuinely subtle spot is unicode. `truncate("Hello", 3, suffix="…")`
uses a single ellipsis character `…`, whose `len()` is `1`, not the three of
`...`. The function measures with `len()`, so it treats one visible character as
one character — which is right here, but be warned that `len()` counts Unicode
code points, and some visible glyphs (a flag emoji, an accented letter written as
two code points) are more than one. For ASCII slugs and receipts it is exact; for
arbitrary user text, "one character" is a genuinely hard question that a later
course revisits.

</details>

## Acceptance checklist

- [ ] All five functions match the table and every listed edge case.
- [ ] `truncate("Hi", 1)` raises `ValueError`.
- [ ] `pytest --cov=stringutils --cov-branch` reports 100 %, `BrPart` at 0.
- [ ] `ruff check .`, `black --check .`, and `mypy --strict` are all clean.
- [ ] A GitHub Actions workflow runs on push and PR; the README shows its badge.
- [ ] The functions are pure — no globals, no I/O, no logging.
- [ ] Tagged `v0.1.0` and pushed.

## Stretch

- Add `hypothesis` property tests: `slugify` never raises on any input string,
  and `slugify(slugify(x)) == slugify(x)` (it is idempotent).
- Add doctests to every function and run them with `pytest --doctest-modules`.
- Publish to TestPyPI via a tagged-release workflow, then `pip install` your own
  package into a fresh environment.

That is Week 11. You can now write tests, share setup with fixtures, drive a
table of cases, fake a boundary, read a coverage report, turn a bug into a
regression test, and wrap a package in the quality tools a real team expects.
Next week turns those habits on the command line: `../week-12-automation-scripting/`.
