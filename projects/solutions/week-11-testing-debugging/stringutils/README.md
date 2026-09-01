# `stringutils` — Week 11 mini-project reference implementation

![CI](https://github.com/YOUR-USERNAME/stringutils/actions/workflows/ci.yml/badge.svg)

Five small, pure string helpers, tested to 100 % line **and** branch coverage,
formatted by `black`, linted by `ruff`, and type-checked by `mypy --strict`.

This is the reference answer for
`curriculum/week-11-testing-debugging/mini-project/README.md`. Read that page
before you read the code — it carries the walkthrough beside the answer, and it
explains *why* each decision was made.

## Install

```bash
python -m venv .venv
source .venv/bin/activate          # .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

## The five functions

| Function | Signature | Behavior |
|---|---|---|
| `slugify` | `(text: str) -> str` | Lowercase; runs of non-alphanumeric characters collapse to `-`; leading/trailing `-` trimmed. |
| `truncate` | `(text: str, max_length: int, suffix: str = "...") -> str` | Returns `text` unchanged when it fits; otherwise cuts to `max_length - len(suffix)` and appends `suffix`. Raises `ValueError` when the suffix alone would not fit. |
| `word_count` | `(text: str) -> int` | Number of whitespace-separated words. `""` and `"   "` both return `0`. |
| `reverse_words` | `(text: str) -> str` | Words in reverse order, single-space separated. |
| `is_palindrome` | `(text: str) -> bool` | Reads the same both ways, ignoring case and non-alphanumeric characters. |

```python
>>> from stringutils import slugify, truncate, word_count, reverse_words, is_palindrome
>>> slugify("Hello, World!")
'hello-world'
>>> truncate("Hello, World!", 8)
'Hello...'
>>> word_count("one two three")
3
>>> reverse_words("the quick brown fox")
'fox brown quick the'
>>> is_palindrome("A man, a plan, a canal: Panama")
True
```

## Test

```bash
pytest                                                                 # fast loop
pytest --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=100
pytest --doctest-modules src                                           # stretch goal
```

## Quality gates

```bash
ruff check .
black --check .
mypy --strict src
```

All four commands are run again by `.github/workflows/ci.yml` on every push and
pull request, on Python 3.11 and 3.12.

## Layout note

The mini-project brief draws a flat layout (`stringutils/stringutils/core.py`)
but every command in it (`pythonpath = ["src"]`, `pytest --cov=src`,
`mypy src`) assumes a `src/` layout — and Lecture 1 §9 recommends `src/`. This
reference uses `src/` so the commands in the brief work verbatim. If you built
the flat layout instead, drop `pythonpath`/`mypy_path` from `pyproject.toml`
and use `--cov=stringutils` and `mypy stringutils`; nothing else changes.
