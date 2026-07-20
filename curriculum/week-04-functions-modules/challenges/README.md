# Week 4 — Challenges

The challenges are larger than the exercises. Each takes 2 to 4 hours. They are graded for design as well as correctness.

## What "passing" means

A challenge passes when:

1. Your code runs without errors on Python 3.10+.
2. The functional requirements in the brief are met.
3. Every function has type hints and a one-line docstring.
4. The code is organized into multiple files where the brief asks for it.
5. A reviewer can run `python main.py` and see the expected output.

## Index

| # | Challenge | Topic | Time | Brief |
|---|-----------|-------|------|-------|
| 1 | Mini calculator module | Multi-file project; clean public interface | 3 h | [challenge-01-mini-calculator-module.md](./challenge-01-mini-calculator-module.md) |
| 2 | Text stats package | Text processing; package layout | 3 h | [challenge-02-text-stats-package.md](./challenge-02-text-stats-package.md) |

## Submission

Each challenge lives in its own folder under `challenges/`. After you finish, your tree should look like this:

```text
challenges/
    README.md
    challenge-01-mini-calculator-module.md
    challenge-02-text-stats-package.md
    challenge-01-mini-calculator/
        calculator.py
        main.py
    challenge-02-text-stats/
        text_stats.py
        main.py
```

Commit each folder separately with a message like `feat(week-04): challenge 01 calculator module`. If you are doing this as part of a cohort, open a pull request and tag a reviewer.

## Tips

- Read the entire brief once before writing any code.
- Sketch your function signatures on paper or in comments first.
- Run `python -i main.py` to drop into the REPL with your modules already imported. Great for poking.
- If a function feels longer than 15 lines, ask whether it should be two functions.
