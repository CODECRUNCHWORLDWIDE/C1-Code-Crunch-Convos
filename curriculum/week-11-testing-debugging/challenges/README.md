# Week 11 — Challenges

Three larger problems that combine multiple concepts from the week. Pick at least one to complete. All three are excellent portfolio pieces.

| #  | File                                 | Approx. time |
|----|--------------------------------------|--------------|
| 1  | `challenge-01-tdd-fizzbuzz.md`       | 1 hour       |
| 2  | `challenge-02-flask-api-tests.md`    | 3 hours      |
| 3  | `challenge-03-review-the-parser.md`  | 2 hours      |

Challenge 1 teaches the **TDD rhythm**. Challenge 2 teaches **integration testing** of a web app — directly useful if you intend to write Flask, FastAPI, or Django apps for a living. Challenge 3 teaches **code review**: you are handed a working module somebody else wrote and asked to say what is wrong with it, rank the findings by severity, and prove every one of them with a test that fails today.

## How to submit

Each challenge has its own deliverable list. When done:

```bash
git add challenges/
git commit -m "Week 11 challenge complete: <name>"
```

Then post the link to your repo (or paste the diff) in `#week-11` for feedback.

## Hints

- Read the whole challenge before you start coding.
- For TDD, **resist** the urge to write more code than the failing test requires.
- For integration tests, the Flask test client lets you skip the network entirely — it calls the view function directly.
- For the review, run the module and compare its output to its input **before** you read any of its code. The fastest finding is usually a number that cannot be true.
