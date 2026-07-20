# Challenge 02 — Text Stats Module

> Time: about 3 hours. Difficulty: slightly harder than Challenge 01.

## Goal

Build a `text_stats` module that, given a string, returns a dictionary of summary statistics: word count, character count, average word length, and the top three most common words.

You will write the module, a `main.py` to demo it, and a small set of self-tests.

## Functional requirements

Create a folder `challenge-02-text-stats/` inside `challenges/`. Inside, create:

- `text_stats.py` — the module.
- `main.py` — a demo script.

### `text_stats.py`

The public interface must expose exactly **one** function:

```python
def analyze(text: str) -> dict[str, object]:
    """Return a stats dict for `text`."""
```

The dict it returns must have **exactly** these keys:

| Key | Type | Description |
|-----|------|-------------|
| `word_count` | `int` | Number of words in `text`. |
| `char_count` | `int` | Number of characters in `text`, including spaces. |
| `avg_word_length` | `float` | Mean length of words, rounded to 2 decimals. 0.0 if no words. |
| `top_3_words` | `list[tuple[str, int]]` | The three most common words, with counts. |

Rules for word-counting:

- Split on whitespace.
- Lowercase each word before counting.
- Strip leading and trailing punctuation: `.,!?;:()"'`. Use `str.strip(...)` with a string of those characters, or import `string.punctuation`.
- Ignore empty strings that result from the strip step.

Rules for `top_3_words`:

- The list is ordered by count, descending.
- If two words tie on count, sort them alphabetically as a tiebreaker.
- If there are fewer than three distinct words, return as many as there are (do not pad).
- Return a list of `(word, count)` tuples.

The module **must**:

- Use [`collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) to count words. (Hint: `Counter(words).most_common()` is your friend, but you must apply the alphabetical tiebreaker yourself for stable ordering.)
- Have type hints and docstrings on every function (public and private).
- Use a private helper `_normalize(word: str) -> str` to lowercase and strip punctuation from one word.
- Use a private helper `_tokenize(text: str) -> list[str]` that returns the cleaned list of words.
- Include a `_self_test()` function and run it under `if __name__ == "__main__":`.

### `main.py`

A demo script that:

1. Defines a multi-line paragraph (use a triple-quoted string).
2. Imports `analyze` from your module.
3. Prints each stat on its own line, formatted neatly.
4. Has a `main()` function and the `if __name__ == "__main__":` guard.

Use this paragraph in the demo (or a longer one of your choice):

```text
The quick brown fox jumps over the lazy dog. The dog was not amused.
The fox, however, was delighted. The fox is the fox is the fox.
```

Expected output (formatting up to you, contents must match):

```text
Words: 27
Characters: 142
Average word length: 3.59
Top 3 words:
  the: 7
  fox: 4
  is: 2
```

(Exact numbers depend on the paragraph and your stripping rules. The numbers above match the stripping rules listed above.)

## Suggested skeleton

```python
# text_stats.py
"""Compute summary statistics for a piece of text."""

import string
from collections import Counter


_PUNCT = string.punctuation


def _normalize(word: str) -> str:
    """Lowercase and strip leading/trailing punctuation."""
    return word.strip(_PUNCT).lower()


def _tokenize(text: str) -> list[str]:
    """Split `text` into normalized words, dropping empties."""
    ...


def analyze(text: str) -> dict[str, object]:
    """Return a stats dict for `text`."""
    ...


def _self_test() -> None:
    """Run a small self-test."""
    ...


if __name__ == "__main__":
    _self_test()
```

## Rubric (100 points)

| Section | Points | Criteria |
|---------|--------|----------|
| `analyze` correctness | 25 | All four keys present and computed correctly. |
| Top-3 tiebreaking | 10 | Counts descending; ties broken alphabetically. |
| Tokenization | 15 | Lowercased, punctuation stripped, empties dropped. |
| Module structure | 15 | Private helpers; clean public surface. |
| Type hints & docstrings | 10 | Present everywhere. |
| Self-tests | 10 | `_self_test()` exists and covers edge cases. |
| `main.py` | 10 | Imports module, prints the demo cleanly. |
| Bonus (stretch) | +5 | Add a `--file PATH` flag in `main.py` using `argparse`. |

## Edge cases to handle

- Empty string `""` → `{"word_count": 0, "char_count": 0, "avg_word_length": 0.0, "top_3_words": []}`.
- Whitespace only `"   "` → same as empty.
- Trailing punctuation `"hello!!!"` → counts as one word `"hello"`.
- Single quotes inside a word `"don't"` should stay intact; only **leading and trailing** punctuation is stripped.

## Stretch ideas

- Add a `top_n` parameter to `analyze` that defaults to 3 but can be overridden.
- Add a `--file PATH` flag to `main.py` and read text from a file.
- Add a basic stop-words filter (a small set of words like "the", "and", "a") and expose a `remove_stopwords: bool = False` flag.
- Compute the longest word and add it as a fifth key, behind a flag.

## What to learn from this challenge

- That a tiny module can have a clean public interface (`analyze`) and a tidy private interior (`_normalize`, `_tokenize`).
- That `collections.Counter` is much nicer than building a count dict by hand.
- That sorting with a tuple key (`key=lambda x: (-count, word)`) is how you do "descending by count, ascending by name".

When you finish, commit and move on to the [mini-project](../mini-project/README.md).
