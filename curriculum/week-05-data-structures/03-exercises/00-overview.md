# Week 5 — Exercises

Five guided exercises. Each `.py` file is **runnable** as-is: skim the prompts, then fill in the `TODO` blocks. Run with:

```bash
python exercise-01-list-operations.py
```

You should complete the exercises **in order** — each one reinforces a concept introduced in the corresponding lecture.

| # | File | Topic | Lecture |
|---|---|---|---|
| 01 | `exercise-01-list-operations.py` | Sort by key, max by attribute, slicing | 01 |
| 02 | `exercise-02-deduplicate.py` | Remove duplicates (order-preserving) | 01 / 02 |
| 03 | `exercise-03-word-frequency.py` | Dict-based counting, top-N | 02 |
| 04 | `exercise-04-set-operations.py` | Union, intersection, difference | 02 |
| 05 | `exercise-05-comprehensions.py` | Convert 6 loops to comprehensions | 03 |

---

## How each file is structured

Every exercise file has the same anatomy:

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

When the script prints `All checks passed.`, the exercise is done.

---

## Tips

- **Don't peek at the solutions** in the lecture notes — try yourself first.
- **Use the REPL** to experiment: copy a snippet, mutate it, see what happens.
- **Read error messages**. They tell you exactly what went wrong.
- **Type hints are part of the exercise**. Keep them; they're documentation.

---

## Stretch versions

After each exercise works, try the "stretch" variants at the bottom of the file (marked `# STRETCH`). They push the same concept a step further.

Happy crunching!
