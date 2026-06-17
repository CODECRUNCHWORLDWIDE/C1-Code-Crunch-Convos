# Week 6 — Exercises

Five short, focused exercises. Do them in order — each builds on the previous one.

Each exercise file contains:

- A docstring describing the task.
- Stub functions with type hints and `TODO` markers where you should write code.
- A `if __name__ == "__main__":` block with a sample run.

You can run each exercise directly:

```bash
python exercise-01-read-write.py
```

---

## Overview

| # | File | Topic | Time |
|---|---|---|---|
| 01 | `exercise-01-read-write.py` | Line-by-line file copy + transform | 15 min |
| 02 | `exercise-02-csv-roundtrip.py` | Read CSV, filter rows, write CSV | 25 min |
| 03 | `exercise-03-json-config.py` | Load JSON, mutate, save back | 20 min |
| 04 | `exercise-04-safe-divide.py` | `try`/`except` with logging | 20 min |
| 05 | `exercise-05-custom-exception.py` | Define and raise a custom exception | 20 min |

Total: about **2 hours**.

---

## How to work through them

1. Read the docstring at the top of the file.
2. Read the `TODO` comments — they describe what each function should do.
3. Implement one function at a time and run the script to check.
4. If you get stuck, re-read the relevant section of the lecture notes (cited in each file).
5. When the `__main__` block prints what the docstring says it should, you are done.

Solutions are **not** provided in this folder — try every exercise yourself first. If you are truly stuck after 20 minutes, ask in the bootcamp chat.

---

## Common debugging tips

- **`FileNotFoundError`?** Check that your working directory matches where the file lives. `print(Path.cwd())` to see where Python thinks you are.
- **Weird characters in output?** You forgot `encoding="utf-8"`.
- **CSV rows misaligned?** You forgot `newline=""` when opening for `csv`.
- **JSON `TypeError: Object of type ... is not JSON serializable`?** You tried to dump a `datetime`, `set`, or custom object. Convert to a `str`, `list`, or `dict` first.
- **Bare `except:` silently swallowing your bugs?** Use a specific exception type.

Good luck — and remember, **type-along beats reading**.
