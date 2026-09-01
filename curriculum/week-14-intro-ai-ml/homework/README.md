# Week 14 — Homework

Six problems, one page each. They run in order for a reason: fit a model, then
classify with one, then ask which columns it actually leaned on, then tune it,
then find out whether more data would help, and finally check who it gets wrong.
That last question is the one most courses skip, and it is the one that matters
when a model touches people.

Each shipped answer runs **offline and unattended**. Every dataset comes from
scikit-learn or is built in the file, nothing downloads at run time, no chart
window opens, and every seed is pinned — so `python <name>.py` prints the same
numbers on your machine as on the page.

## Setup

Work in the same virtual environment you used for the exercises:

```bash
pip install scikit-learn pandas matplotlib
```

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the model is being
   asked to predict and what it is allowed to look at.
2. Copy the Starter into a file of your own — the page names it, and it is
   **not** the `-solution.py` file, which is the finished answer.
3. Fill in the `TODO` markers one at a time, running after each.
4. Compare your output with the Expected output block.
5. Only then read The Solution and Why it works.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Housing regression](./problem-01-housing-regression.md) | Predicting a quantity, and reading the error in the units of the thing | Intermediate | 45 min |
| 2 | [Churn classification](./problem-02-churn-classification.md) | Predicting a decision, and why accuracy alone can flatter a bad model | Intermediate | 45 min |
| 3 | [Feature importance from a tree](./problem-03-feature-importance.md) | Asking a model which columns it leaned on — and how far to trust the answer | Intermediate | 45 min |
| 4 | [Hyperparameter tuning](./problem-04-grid-search.md) | Searching settings without quietly fitting to the test set | Advanced | 1 hr |
| 5 | [Plot a learning curve](./problem-05-learning-curve.md) | Seeing whether the fix is more data or a different model | Advanced | 1 hr |
| 6 | [Fairness audit](./problem-06-fairness-audit.md) | Checking who the model gets wrong, not just how often it is right | Advanced | 1 hr 15 min |

Total target time: about 5 and a half hours. The [week schedule](../README.md)
leaves more room, and both numbers are honest — the figures here are how long a
problem takes when it goes well, and the schedule allows for getting stuck.

**Two things this week will keep saying, because they are what separates a
result from a claim.**

A score is an estimate, not a verdict. It is measured on one particular split of
one particular dataset, and it moves when the split moves. That is why every page
pins `random_state`: not because one seed is right, but so that when your number
differs from the page's you know the difference is *yours* and worth chasing.

And a model that scores well can still be wrong in ways the score cannot see. One
accuracy figure averages over everybody. Two groups can sit inside that one number
with very different error rates, and the average will never mention it. Problem 6
is where you go looking, and it ends without a certificate on purpose — an audit
is evidence about a model, not a stamp that makes it fair.

## What you hand in

Six programs of your own, one per problem, named as each page tells you — not the
`-solution.py` names, which belong to the published answers — plus one
`report.md` with a short section per problem saying what you found. Keep them
together in a folder called `homework/` inside your fork, along with the
`learning_curve.png` Problem 5 produces.

House rules on every problem:

- **A docstring at the top of every file** naming the problem and showing an
  example invocation.
- **Type hints on every signature.**
- **`random_state` set everywhere reproducibility matters** — the split, the
  model, the search. An unpinned seed makes a number nobody else can check.
- **It runs end-to-end** with `python <name>.py`, from a clean shell, with no
  manual edits.

## Checking your work

Every page ends with an acceptance checklist. Work down it before calling a
problem done. If your numbers differ from the page's Expected output, do not
shrug it off — with the seeds pinned, a difference means something real changed,
and finding out what is the exercise.
