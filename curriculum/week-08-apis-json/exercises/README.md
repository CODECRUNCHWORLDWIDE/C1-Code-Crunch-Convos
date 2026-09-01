# Week 8 — Exercises

Five small, focused exercises. Do them in order — each one builds a habit you will use in the challenges and mini-project.

**Before you start:**

```bash
python -m pip install requests python-dotenv
```

All exercises hit **free, no-key, public APIs**. You can run them right now without signing up for anything.

---

## Index

Each exercise is a page. It gives you the brief, a starter file to copy into your own `.py`, the exact output to aim for, and the bugs that bite people on that specific task.

| # | Exercise | What you practice | Difficulty | Est. time |
|---|----------|-------------------|-----------:|----------:|
| 01 | [exercise-01-first-get-request.md](./exercise-01-first-get-request.md) | Your first `GET`, reading `.status_code` and `.json()` | Beginner | 40 min |
| 02 | [exercise-02-pokemon-api.md](./exercise-02-pokemon-api.md) | Navigating a nested JSON response with type hints | Easy | 50 min |
| 03 | [exercise-03-post-data.md](./exercise-03-post-data.md) | Sending a JSON body with `json=` and verifying the echo | Easy | 40 min |
| 04 | [exercise-04-pagination.md](./exercise-04-pagination.md) | Looping through pages until a page is empty | Medium | 60 min |
| 05 | [exercise-05-handle-errors.md](./exercise-05-handle-errors.md) | Robust fetcher with timeout, retry, and custom exception | Medium | 75 min |

The times above are hands-on coding time for someone who has already read the relevant lecture. The week's suggested schedule allots larger blocks per exercise because those blocks include re-reading the lecture, experimenting, and debugging. Both numbers are honest; use whichever matches how you are working.

---

## How to run

Each page has a **Starter file** section. Copy that block into a real file in your practice repo, named after the page — `exercise-01-first-get-request.md` becomes `exercise-01-first-get-request.py`. Fill in the `# TODO:` markers, then run it:

```bash
python exercise-01-first-get-request.py
```

Every starter ends with an `if __name__ == "__main__":` guard, so the file runs directly.

If a script fails because `requests` is missing, you forgot the `pip install` above.

---

## Two rules that apply to every exercise this week

1. **Every request passes `timeout=`.** By default `requests` waits forever — not thirty seconds, forever. A script with no timeout does not fail, it hangs, and a hang is far harder to notice than an error.
2. **Every request calls `raise_for_status()` before `.json()`.** Otherwise a `404` error page arrives as HTML and you get a confusing `JSONDecodeError` twenty lines away from the real problem.

You will see both stated again, with their reasons, in each page's **Constraints** section. They are the two habits this week exists to install.

---

## APIs used

| API | Base URL | Key needed |
|---|---|---|
| httpbin | `https://httpbin.org` | none |
| PokeAPI | `https://pokeapi.co/api/v2` | none |
| GitHub REST (public, read-only) | `https://api.github.com` | none — 60 requests/hour unauthenticated |

No key goes in a URL query string anywhere in this week, ever. When Challenge 02 optionally uses a GitHub token, it travels in the `Authorization` header, loaded from a `.env` file. Lecture 3 explains why.

---

## How to check yourself

Every page has an **Expected output** block. Compare your terminal output to it. Where live data changes over time — repository counts, IP addresses, elapsed times — the page says so and tells you which part of the output must still hold. If your output differs:

1. Read the error message carefully — it usually names the line that is wrong.
2. Print intermediate values (`print(repr(response.text[:200]))` is your best friend).
3. Check the page's **Common bugs to catch** section. Your symptom is probably listed there with its cause.
4. Re-read the relevant lecture-note section, which each page links at the top.

Then work the **Acceptance checklist** at the bottom of the page before you move on.

---

## After you finish

Move on to [`../challenges/README.md`](../challenges/README.md). Both challenges assume the patterns from exercises 02, 04, and 05 are in your fingers — nested-JSON navigation, page walking, and the `ApiError` wrapper.
