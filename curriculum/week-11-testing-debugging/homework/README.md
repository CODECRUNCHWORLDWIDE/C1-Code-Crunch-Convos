# Week 11 — Homework

Six problems, one page each. They are not six unrelated puzzles. Each one is a
different testing skill practised on the same imaginary system — a neighborhood
tool library — so the vocabulary carries from one to the next, and together they
rehearse everything the [mini-project](../mini-project/README.md) asks you to do
at once: write tests from a spec, share setup with fixtures, drive a table of
cases, fake a boundary, read a coverage report, and turn a bug into a test that
guards against it forever.

Each shipped answer runs **offline and unattended**. A pytest test file prints
nothing when you run it with `python`, because `pytest` is what calls the tests.
So every answer here bundles the module *and* its tests in one file and, under
`if __name__ == "__main__":`, drives pytest itself and prints a plain report.
That is why `python problem-01-renewal-rules-solution.py` finishes on its own and
prints the same thing on every machine. When you do the work yourself you keep
the module and the tests in separate files and run `pytest` — the normal way.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what goes in and what should
   come back.
2. Copy the Starter into files of your own — the page names them, and they are
   **not** the `-solution.py` file, which is the finished answer.
3. Fill in each `TODO` one at a time, running `pytest` after each. Watch tests
   fail before you make them pass.
4. Compare your output with the Expected output block.
5. Only then read The Solution and the "why it works" notes.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Renewal rules](./problem-01-renewal-rules.md) | Writing a test suite from an English rule, boundary included | Beginner | 40 min |
| 2 | [Dues ledger](./problem-02-dues-ledger.md) | Fixtures over a list and a real CSV, with `tmp_path` and teardown | Intermediate | 1 hr |
| 3 | [Hours and minutes](./problem-03-hours-minutes.md) | Table-driven tests with `parametrize`, `ids=`, and `:02d` padding | Beginner | 40 min |
| 4 | [Overdue notice](./problem-04-overdue-notice.md) | Mocking a POST — asserting on the payload, never touching the network | Intermediate | 1 hr |
| 5 | [Fine schedule](./problem-05-fine-schedule.md) | Coverage: 100 % statements with a branch still untaken | Intermediate | 1 hr |
| 6 | [Shelf order regression](./problem-06-shelf-order-regression.md) | Reproducing a bug with a failing test, then fixing it | Advanced | 1 hr |

Total target time: about 5 hours 20 minutes. Aim to complete at least four; the
last two stretch furthest.

## What you hand in

Six folders of your own, one per problem, each holding the module and its test
file named as the page tells you — **not** the `-solution.py` names, which belong
to the published answers. Each must run its tests with `pytest -v` (problem 5
adds `--cov`). Put type hints on every signature, give each function a one-line
docstring, use a narrow `except` (never a bare `except:`) and a custom exception
where something can fail, and never type a secret into a file you commit.

## Checking your work

Every page ends with an acceptance checklist. Work down it before calling a
problem done. If your output differs from the page's Expected output, that
difference **is** the bug — read it rather than guessing. Nine failures out of
ten are an off-by-one in an assertion or a fixture you forgot to pass in; the
tenth is a mocked boundary you forgot to patch.
