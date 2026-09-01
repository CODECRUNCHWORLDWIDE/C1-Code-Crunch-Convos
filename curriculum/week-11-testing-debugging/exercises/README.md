# Week 11 — Exercises

Five focused drills. Each one isolates a single skill. Do them in order — later
exercises assume earlier ones.

Each exercise below is a page, not a file you download. The page gives you the
brief, a starter you copy into your own `.py` files, the exact output to expect,
and the failures most people hit on the way. You create the files in your own
practice repo and run them there.

All five build pieces of the same imaginary system — a neighborhood tool
library — so the vocabulary carries from one drill to the next.

## Setup

Install the three tools this week needs, once, into your activated virtual
environment:

```bash
python -m pip install pytest pytest-mock pytest-cov
pytest --version
```

## How to run

Create a folder for the week, save each exercise's files into it, then from that
folder:

```bash
# Run one test file
pytest test_lending.py -v

# Run everything in the folder
pytest -v

# Run a single test by node id
pytest -v "test_money.py::test_format_cents[four-figures]"
```

Exercise 5 also uses the coverage plugin:

```bash
pytest --cov=holds --cov-branch --cov-report=term-missing
```

## Index

| # | Page | What you'll practice | Difficulty | Est. time |
|---|------|----------------------|-----------:|----------:|
| 1 | [exercise-01-first-test.md](./exercise-01-first-test.md) | Writing `test_*.py`, plain `assert`, `pytest.raises`, the red-green loop | Beginner | 20 min |
| 2 | [exercise-02-fixtures.md](./exercise-02-fixtures.md) | Sharing setup with `@pytest.fixture`, `yield` teardown, `tmp_path` | Easy | 30 min |
| 3 | [exercise-03-parametrize.md](./exercise-03-parametrize.md) | Table-driven tests with `@pytest.mark.parametrize` and `ids=` | Easy | 25 min |
| 4 | [exercise-04-mocking.md](./exercise-04-mocking.md) | Mocking `requests.get` so the suite never touches the network | Medium | 40 min |
| 5 | [exercise-05-coverage-gap.md](./exercise-05-coverage-gap.md) | Finding the missing branch with `pytest-cov` | Medium | 35 min |

Exercises 1–3 follow [Lecture 1](../lecture-notes/01-intro-to-pytest.md). Do
them Monday and Tuesday. Exercises 4 and 5 follow
[Lecture 2](../lecture-notes/02-mocking-coverage-and-debugging.md) — read it
first, on Wednesday.

## Submitting

When all five are done:

```bash
pytest -v
```

Then commit your work:

```bash
git add exercises/
git commit -m "Week 11 exercises complete"
```

## Hints

- Read the whole page before you start typing. The Constraints section explains
  *why* each rule exists, and a rule you understand is a rule you keep.
- Each `TODO` in a starter is one step. Knock them down one at a time and run
  `pytest` after each — five failures at once are five times harder to read than
  one.
- If a test fails, read the *bottom* of the pytest output first. The short test
  summary names what broke; the block above it shows both sides of the
  comparison.
- Watch a test fail before you make it pass. A test you have never seen fail is
  a test you have no evidence works.
- Stuck? Drop into `#week-11` on Discord with the full command you ran and the
  full output, traceback included.
