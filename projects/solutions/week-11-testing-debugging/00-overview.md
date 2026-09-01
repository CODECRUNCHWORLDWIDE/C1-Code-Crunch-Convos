# Week 11 — reference implementations

Four real projects. Every one of them runs, and every claim made about them in
this folder was produced by running it.

The walkthrough for each one — architecture, tradeoffs, where people get stuck —
lives on the page that set the problem, beside the answer it is explaining. Read
that page first; the code in this folder is the appendix, not the lesson.

| Folder | Answers | Headline |
|---|---|---|
| [`challenge-01-tdd-fizzbuzz/`](./challenge-01-tdd-fizzbuzz) | [Challenge 1](../../../curriculum/week-11-testing-debugging/challenges/challenge-01-tdd-fizzbuzz.md) | 9 tests, 18-commit RED/GREEN/REFACTOR log, `ruff` + `black` clean |
| [`challenge-02-flask-blog-tests/`](./challenge-02-flask-blog-tests) | [Challenge 2](../../../curriculum/week-11-testing-debugging/challenges/challenge-02-flask-api-tests.md) | 39 tests, 100 % branch coverage on `blog/`, `mypy --strict` clean, CI workflow |
| [`stringutils/`](./stringutils) | [Mini-project](../../../curriculum/week-11-testing-debugging/mini-project/README.md) | 47 tests + 5 doctests, 100 % line **and** branch, all four gates green |
| [`homework-loganalyzer/`](./homework-loganalyzer) | [Homework problems 1–6](../../../curriculum/week-11-testing-debugging/homework/README.md) | The Week 6 analyzer refactored: 78 tests, 100 % branch, `pre-commit`, CI matrix |

## Environment

Everything was written and verified on:

| Component | Version |
|---|---|
| CPython | 3.13.2 (Windows 11) |
| `pytest` | 9.1.1 |
| `pytest-cov` | 7.1.0 |
| `coverage` | 7.15.4 |
| `ruff` | 0.16.4 |
| `black` | 26.5.1 |
| `mypy` | 2.3.1 |
| `Flask` / `Werkzeug` | 3.1.3 / 3.1.8 |

The CI workflows target Python 3.11 and 3.12, which is what the lecture notes
specify; nothing in any of the four projects uses syntax newer than 3.11.

If your `pytest` output differs cosmetically — dot counts per line, timings, the
exact wording of a deprecation warning — that is your version, not a broken
answer. If a *count* differs (tests collected, coverage percentage), something
is genuinely different and worth chasing.

## Running any of them

Each folder is self-contained and has its own `README.md` with the exact
commands. The shape is always the same:

```bash
cd <folder>
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -e ".[dev]"        # or: pip install -r requirements-dev.txt
pytest
```

Two of the four (`stringutils`, `homework-loganalyzer`) are installable packages
with a `[project.optional-dependencies] dev` extra. `challenge-01-tdd-fizzbuzz`
is two files and a `pyproject.toml`. `challenge-02-flask-blog-tests` ships a
`requirements-dev.txt` because it is an application, not a library.
