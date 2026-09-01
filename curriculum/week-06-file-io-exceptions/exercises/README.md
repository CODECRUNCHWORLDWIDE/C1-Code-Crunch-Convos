# Week 6 — Exercises

Five short, focused exercises. Do them in order — each builds on the previous one.

Each exercise is a **page**, not a file you download. The page gives you:

- A brief describing the task and why anyone would want it.
- The exact contents of the sample input file to create, so nothing has to be
  downloaded and every expected output on the page is reproducible.
- A starter you copy into your own `.py` file: module docstring, type-hinted
  function stubs, `TODO` markers, and an `if __name__ == "__main__":` block.
- The expected terminal session, the bugs to watch for, and an acceptance
  checklist.

Copy the starter into a file named after the exercise, in your own practice
repo, and run it the normal way:

```bash
python exercise-01-read-write.py
```

Every exercise reads and writes inside a `data/` folder next to your script,
and every page tells you what to put in it. Create it once:

```bash
mkdir data
```

---

## Overview

| # | Exercise | Topic | Difficulty | Time |
|---|---|---|---|---|
| 01 | [exercise-01-read-write.md](./exercise-01-read-write.md) | Line-by-line file copy + transform | Beginner | 15 min |
| 02 | [exercise-02-csv-roundtrip.md](./exercise-02-csv-roundtrip.md) | Read CSV, filter rows, write CSV | Easy | 25 min |
| 03 | [exercise-03-json-config.md](./exercise-03-json-config.md) | Load JSON, mutate, save back | Easy | 20 min |
| 04 | [exercise-04-safe-divide.md](./exercise-04-safe-divide.md) | `try`/`except` with logging | Easy | 20 min |
| 05 | [exercise-05-custom-exception.md](./exercise-05-custom-exception.md) | Define and raise a custom exception | Medium | 20 min |

Total: about **2 hours**.

Exercises 01–03 follow `01-files-and-pathlib.md` and `02-csv-and-json.md`.
Exercises 04–05 follow `03-exceptions-and-logging.md`. If you are working
through the week's suggested schedule, do 01 on day 1, 02–03 on day 2, and
04–05 on day 3.

---

## How to work through them

1. Read the brief and the requirements before you write anything.
2. Create the sample input file exactly as the page gives it. The expected
   output on the page depends on that data character for character.
3. Copy the starter into a `.py` file and run it before filling in any `TODO`.
   A starter that runs is a baseline; a starter that does not means the paths
   are wrong and nothing else will work either.
4. Implement one function at a time and run the script after each.
5. Compare your terminal against the page's **Expected output** section. If it
   differs, read **Common bugs to catch** on that page before changing code —
   it is written for that exercise specifically.
6. Work the acceptance checklist at the bottom. The last item is always a Git
   commit.

Solutions are **not** provided in this folder — try every exercise yourself
first. If you are truly stuck after 20 minutes, ask in the bootcamp chat.

---

## Common debugging tips

- **`FileNotFoundError`?** Check that your working directory matches where the file lives. `print(Path.cwd())` to see where Python thinks you are.
- **Weird characters in output?** You forgot `encoding="utf-8"`.
- **CSV rows misaligned?** You forgot `newline=""` when opening for `csv`.
- **JSON `TypeError: Object of type ... is not JSON serializable`?** You tried to dump a `datetime`, `set`, or custom object. Convert to a `str`, `list`, or `dict` first.
- **Bare `except:` silently swallowing your bugs?** Use a specific exception type.

Good luck — and remember, **type-along beats reading**.
