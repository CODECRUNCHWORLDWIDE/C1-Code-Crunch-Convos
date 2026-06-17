# Week 11 — Challenges

Two larger problems that combine multiple concepts from the week. Pick at least one to complete. Both are excellent portfolio pieces.

| #  | File                               | Approx. time |
|----|------------------------------------|--------------|
| 1  | `challenge-01-tdd-fizzbuzz.md`     | 1 hour       |
| 2  | `challenge-02-flask-api-tests.md`  | 3 hours      |

Challenge 1 teaches the **TDD rhythm**. Challenge 2 teaches **integration testing** of a web app — directly useful if you intend to write Flask, FastAPI, or Django apps for a living.

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
