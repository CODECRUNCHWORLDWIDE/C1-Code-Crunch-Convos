# Week 11 — Exercises

Five focused drills. Each one isolates a single skill. Do them in order — later exercises assume earlier ones.

## How to run

From this folder:

```bash
# Run a single exercise file
pytest exercise-01-first-test.py -v

# Run them all
pytest -v
```

If `pytest` is not installed:

```bash
python -m pip install pytest pytest-mock pytest-cov
```

## Exercises

| #  | File                              | Topic                                   |
|----|-----------------------------------|-----------------------------------------|
| 1  | `exercise-01-first-test.py`       | Your first pytest tests.                |
| 2  | `exercise-02-fixtures.py`         | Sharing setup with `@pytest.fixture`.   |
| 3  | `exercise-03-parametrize.py`      | Table-driven tests with parametrize.    |
| 4  | `exercise-04-mocking.py`          | Mocking `requests.get` with a mock.     |
| 5  | `exercise-05-coverage-gap.py`     | Find the missing branch with coverage.  |

## Submitting

When all five pass:

```bash
pytest -v
```

Then commit your work:

```bash
git add exercises/
git commit -m "Week 11 exercises complete"
```

## Hints

- Read the docstring at the top of each file before you start.
- Each `TODO` comment is one step. Knock them down one at a time.
- If a test fails, read the *bottom* of the pytest output first — that is where the diff lives.
- Stuck? Drop into `#week-11` on Discord.
