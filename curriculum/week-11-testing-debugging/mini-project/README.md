# Mini-project — `stringutils`

Ship a small, tested, type-checked, CI-verified Python package called `stringutils`. This is the project where you stop reading about quality tools and start using all of them together.

By Friday evening you should have a repository that:

- Implements five string utility functions.
- Has **100 %** line and branch coverage.
- Passes `ruff check .`, `black --check .`, and `mypy --strict src/`.
- Runs a green GitHub Actions workflow on every push.
- Carries a "CI passing" badge in its README.

---

## What you're building

A package with this public surface:

```python
from stringutils import (
    slugify,
    truncate,
    word_count,
    reverse_words,
    is_palindrome,
)
```

The five functions:

| Function        | Signature                                                  | Behavior                                                                                                        |
|-----------------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| `slugify`       | `(text: str) -> str`                                       | Lowercase, replace runs of non-alphanumeric chars with `-`, trim leading/trailing `-`.                          |
| `truncate`      | `(text: str, max_length: int, suffix: str = "...") -> str` | If `len(text) <= max_length`, return unchanged; otherwise cut to `max_length - len(suffix)` and append `suffix`.|
| `word_count`    | `(text: str) -> int`                                       | Count whitespace-separated words. Empty strings return 0.                                                       |
| `reverse_words` | `(text: str) -> str`                                       | Reverse the order of the words, preserving single-space separators.                                             |
| `is_palindrome` | `(text: str) -> bool`                                      | True if the text reads the same forwards and backwards, ignoring case and non-alphanumeric characters.          |

Edge cases your tests must cover (this list is not exhaustive):

- `slugify("Hello, World!")` → `"hello-world"`
- `slugify("   spaced   out   ")` → `"spaced-out"`
- `truncate("Hello", 10)` → `"Hello"`
- `truncate("Hello, World!", 8)` → `"Hello..."`
- `truncate("Hello", 3, suffix="…")` → `"He…"`
- `truncate("Hi", 1)` raises `ValueError` (suffix longer than max_length).
- `word_count("")` → `0`
- `word_count("   ")` → `0`
- `word_count("one two three")` → `3`
- `reverse_words("the quick brown fox")` → `"fox brown quick the"`
- `is_palindrome("A man, a plan, a canal: Panama")` → `True`
- `is_palindrome("not a palindrome")` → `False`

---

## Project layout (when finished)

```text
stringutils/
├── pyproject.toml
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── stringutils/
│   ├── __init__.py
│   └── core.py
└── tests/
    └── test_core.py
```

The `starter/` folder in this directory contains a working skeleton — copy it to your own repo and fill in the `NotImplementedError`s. You can move to a `src/stringutils/` layout later if you wish; the starter uses the flat layout for simplicity.

---

## Step-by-step

1. **Copy the starter.** `cp -r starter ~/projects/stringutils && cd ~/projects/stringutils`.
2. **Make a virtualenv and install dev deps.**

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. **Run the (failing) tests** to confirm pytest works:

   ```bash
   pytest
   ```

4. **TDD each function.** Add a test, watch it fail, implement, watch it pass, refactor. Repeat for all five.
5. **Check coverage.**

   ```bash
   pytest --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=100
   ```

6. **Lint and format.**

   ```bash
   ruff check .
   black --check .
   ```

7. **Type-check.**

   ```bash
   mypy src
   ```

8. **Push to GitHub.** Initialize a public repo, push, watch the Actions tab go green.
9. **Add the CI badge** to your README.
10. **Tag `v0.1.0`** to mark your first release.

---

## Rubric

| Criterion                                                  | Points |
|------------------------------------------------------------|--------|
| All five functions implemented with correct behavior       | 3      |
| 100 % line **and** branch coverage                         | 3      |
| `ruff check .` and `black --check .` pass                  | 1      |
| `mypy --strict src` is clean                               | 1      |
| GitHub Actions workflow passes on push & PR                | 1      |
| CI badge in README                                         | 1      |
| **Total**                                                  | **10** |

Stretch (do any *one* for an extra +2):

- Add `hypothesis` property-based tests for `slugify` (no exceptions on any input).
- Publish to TestPyPI via a tagged release workflow.
- Add doctests to every function and run them with `pytest --doctest-modules`.

---

## What "good" looks like

- Functions are **pure** — they take a string in and return a string out. No globals, no logging, no I/O.
- Tests live in `tests/` and mirror the module under test.
- Edge cases (empty string, all whitespace, unicode) are tested explicitly.
- The README explains how to install, how to test, and what each function does.
- Commit history is small and incremental. Each commit moves one assertion or fixes one mypy error.
- The CI badge is the first thing a stranger sees on the README.

---

## Where you'll get stuck

- **Import errors in tests.** Make sure `pythonpath = ["src"]` is in `[tool.pytest.ini_options]`.
- **`black` and `ruff` disagree.** Set the same `line-length` for both. Run `ruff` first (with `--fix`), then `black`.
- **CI passes locally but fails on GitHub.** Your local env has packages the CI doesn't. Pin versions in `pyproject.toml`.
- **`mypy --strict` rejects `*args` and `**kwargs`.** Type them: `*args: str`, `**kwargs: Any`.

When in doubt, read the test failure message *before* googling. Nine times out of ten it tells you exactly what is wrong.
