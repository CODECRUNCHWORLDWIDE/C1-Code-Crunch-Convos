# Week 6 — Challenges

Two open-ended problems that pull together everything in this week. Unlike the exercises, **the challenges are not handed to you with stubs** — read the spec, design the solution, write the code.

| # | File | Topic | Time |
|---|---|---|---|
| 01 | `challenge-01-recursive-line-counter.md` | `pathlib.rglob`, OSError handling | 1–2 hrs |
| 02 | `challenge-02-config-validator.md` | JSON parsing, custom exceptions, schema-style validation | 2–3 hrs |

---

## Submission format

For each challenge:

1. Create a `.py` file in this folder with your solution (e.g. `challenge-01-solution.py`).
2. Make the script runnable — it should produce sensible output when invoked with `python challenge-01-solution.py`.
3. Add a short note at the top of the file describing your approach and any trade-offs you made.

If you cannot get a challenge fully working, **submit partial code with a written explanation** of where you got stuck and what you tried. That is far more valuable than no submission.

---

## Tips

- **Start with the happy path.** Get a working solution on clean input first, then add error handling.
- **Use the logging module** for any diagnostic output. Reserve `print` for user-facing results.
- **Write small functions.** A 100-line `main()` is a smell. Aim for functions that fit on one screen.
- **Test as you go.** Build up a tiny test directory or test config file and re-run your script after every change.
