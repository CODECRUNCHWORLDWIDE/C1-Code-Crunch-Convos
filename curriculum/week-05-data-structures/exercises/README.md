# Week 5 — Exercises

Five guided exercises. Each one is a **page**: read the brief, copy the
starter into your own `.py` file in your practice repo, fill in the `TODO`
blocks, and run it. The page is the prompt; the file you create is the work.

```bash
python exercise-01-list-operations.py
```

You should complete the exercises **in order** — each one reinforces a
concept introduced in the corresponding lecture.

| # | Exercise | Topic | Lecture | Difficulty | Est. time |
|---|---|---|---|---|---:|
| 01 | [exercise-01-list-operations.md](./exercise-01-list-operations.md) | Sort by key, max by attribute, slicing | 01 | Beginner | 60 min |
| 02 | [exercise-02-deduplicate.md](./exercise-02-deduplicate.md) | Remove duplicates (order-preserving) | 01 / 02 | Beginner | 45 min |
| 03 | [exercise-03-word-frequency.md](./exercise-03-word-frequency.md) | Dict-based counting, top-N | 02 | Easy | 60 min |
| 04 | [exercise-04-set-operations.md](./exercise-04-set-operations.md) | Union, intersection, difference | 02 | Beginner | 45 min |
| 05 | [exercise-05-comprehensions.md](./exercise-05-comprehensions.md) | Convert 6 loops to comprehensions | 03 | Easy | 90 min |

---

## How each file is structured

Every starter you copy out has the same anatomy:

```python
"""
Exercise N — Title
Goal: one-line description.
"""

# ---- Given data ----
data = ...

# ---- Your task ----
def my_function(...):
    # TODO: implement
    ...

# ---- Self-check ----
if __name__ == "__main__":
    assert my_function(...) == expected
    print("All checks passed.")
```

When the script prints `All checks passed.`, the exercise is done. Nothing
here needs a `pip install` — every exercise runs on the standard library, and
most of them on nothing but built-ins.

---

## Tips

- **Don't peek at the solutions** in the lecture notes — try yourself first.
- **Use the REPL** to experiment: copy a snippet, mutate it, see what happens.
- **Read error messages**. They tell you exactly what went wrong, and each
  exercise page has a "Common bugs to catch" section keyed to the exact
  exception text you are likely to see.
- **Run before you write.** Every starter fails on the first run. That is the
  baseline that proves the self-check is real.
- **Type hints are part of the exercise**. Keep them; they're documentation.

---

## Stretch versions

After each exercise works, try the stretch variants at the bottom of the
starter (marked `# STRETCH`). Each page's **Stretch** section explains those
same items in order, so keep both open.

Happy crunching!
