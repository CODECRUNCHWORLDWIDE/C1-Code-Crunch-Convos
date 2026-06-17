# Week 8 — Exercises

Five small, focused exercises. Do them in order — each one builds a habit you will use in the challenges and mini-project.

**Before you start:**

```bash
python -m pip install requests python-dotenv
```

All exercises hit **free, no-key, public APIs**. You can run them right now without signing up for anything.

---

## Index

| # | File | What you practice |
|---|---|---|
| 01 | `exercise-01-first-get-request.py` | Your first `GET`, reading `.status_code` and `.json()` |
| 02 | `exercise-02-pokemon-api.py` | Navigating a nested JSON response with type hints |
| 03 | `exercise-03-post-data.py` | Sending a JSON body with `json=` and verifying the echo |
| 04 | `exercise-04-pagination.py` | Looping through pages until a page is empty |
| 05 | `exercise-05-handle-errors.py` | Robust fetcher with timeout, retry, and custom exception |

---

## How to run

Each file has a `__main__` block. Run with:

```bash
python exercise-01-first-get-request.py
```

If a script fails because `requests` is missing, you forgot the `pip install` above.

---

## How to check yourself

Each exercise's docstring lists explicit "expected output" examples. Compare your terminal output to those. If your output differs:

1. Read the error message carefully — it usually tells you which line is wrong.
2. Print intermediate values (`print(repr(r.text[:200]))` is your best friend).
3. Re-read the relevant lecture-note section.

If you are stuck for more than 30 minutes on one exercise, scroll to the bottom of the file — every script has a `# Hints` comment block.

---

## After you finish

Move on to `challenges/README.md`. Both challenges assume the patterns from exercises 02, 04, and 05 are in your fingers.
