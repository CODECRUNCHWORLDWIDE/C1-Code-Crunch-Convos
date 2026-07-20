# Week 6 — File I/O & Exception Handling

Welcome to Week 6 of **Code Crunch Convos**, our open-source Python bootcamp. So far your programs have lived entirely in RAM — once you closed the REPL, the data was gone. This week you learn how to make data **persist** by reading and writing files, and how to make your programs **resilient** to the real-world failures that happen when files are missing, encodings are wrong, or numbers are not numbers.

You will leave this week able to read text, CSV, and JSON files; write them safely with context managers; handle exceptions gracefully; and use the `logging` module like a professional Python developer.

---

## Learning objectives

By the end of Week 6 you will be able to:

1. Open files in the correct **mode** (`r`, `w`, `a`, `r+`, `b`) and reason about what each one does.
2. Use the **`with` statement** to guarantee files are closed even when errors occur.
3. Read files line-by-line, all at once with `.read()`, or as a list with `.readlines()` — and pick the right one for the situation.
4. Write data using `.write()`, `.writelines()`, and `print(..., file=...)`.
5. Use **`pathlib.Path`** for modern, cross-platform file paths (joining, globbing, existence checks).
6. Read and write **CSV** files with `csv.reader`, `csv.writer`, `csv.DictReader`, and `csv.DictWriter`.
7. Serialize Python objects to **JSON** with `json.dump`/`json.dumps`, and parse them back with `json.load`/`json.loads`.
8. Use **`try` / `except` / `else` / `finally`** to handle errors deliberately.
9. Understand the **built-in exception hierarchy** and prefer **narrow excepts** over bare `except:`.
10. Use **`raise`** to signal errors and **`raise ... from ...`** for clean exception chaining.
11. Define **custom exception classes** and use them in your own APIs.
12. Use the **`logging` module** instead of `print` for diagnostic output.

---

## Prerequisites

You should be comfortable with everything from Weeks 1–5:

- **Week 1** — running `.py` files, the REPL.
- **Week 2** — strings, slicing, f-strings.
- **Week 3** — `if`, `for`, `while`.
- **Week 4** — defining functions, importing modules, type hints.
- **Week 5** — lists, tuples, sets, dicts, comprehensions. We use lists of dicts heavily this week for CSV/JSON data.

If any of those feel shaky, revisit them — file I/O code is mostly loops over data structures, so weak fundamentals will hurt here.

---

## Topics

| # | Topic | Where |
|---|---|---|
| 1 | `open()`, file modes, encoding | `lecture-notes/01-files-and-pathlib.md` |
| 2 | The `with` statement and context managers | `lecture-notes/01-files-and-pathlib.md` |
| 3 | Reading patterns (line-by-line, `.read()`, `.readlines()`) | `lecture-notes/01-files-and-pathlib.md` |
| 4 | Writing patterns (`.write`, `.writelines`, `print(file=)`) | `lecture-notes/01-files-and-pathlib.md` |
| 5 | `pathlib.Path` — joining, globbing, checks | `lecture-notes/01-files-and-pathlib.md` |
| 6 | CSV — `reader`, `writer`, `DictReader`, `DictWriter` | `lecture-notes/02-csv-and-json.md` |
| 7 | JSON — `load`/`loads`/`dump`/`dumps` | `lecture-notes/02-csv-and-json.md` |
| 8 | `try`/`except`/`else`/`finally` | `lecture-notes/03-exceptions-and-logging.md` |
| 9 | Built-in exception hierarchy | `lecture-notes/03-exceptions-and-logging.md` |
| 10 | Custom exceptions, exception chaining | `lecture-notes/03-exceptions-and-logging.md` |
| 11 | EAFP vs LBYL idioms | `lecture-notes/03-exceptions-and-logging.md` |
| 12 | `logging` module basics | `lecture-notes/03-exceptions-and-logging.md` |

---

## Suggested schedule (~36 hours)

This is a self-paced suggestion. Most learners spend **30–40 hours** on this week.

| Block | Hours | Activity |
|---|---|---|
| Day 1 | 4 | Read `01-files-and-pathlib.md`, type along in REPL |
| Day 1 | 2 | Exercises 01 (file copy with lowercase) |
| Day 2 | 4 | Read `02-csv-and-json.md` |
| Day 2 | 3 | Exercises 02–03 (CSV roundtrip, JSON config) |
| Day 3 | 4 | Read `03-exceptions-and-logging.md` |
| Day 3 | 3 | Exercises 04–05 (safe-divide, custom exception) |
| Day 4 | 4 | Challenge 01 (recursive line counter) |
| Day 4 | 3 | Challenge 02 (config validator) |
| Day 5 | 6 | Mini-project: log file analyzer |
| Day 6 | 2 | Homework problems |
| Day 6 | 1 | Quiz + reflection |

Total: **~36 hours**.

---

## Navigation

- **Lecture notes** — `lecture-notes/01-files-and-pathlib.md` → `02-csv-and-json.md` → `03-exceptions-and-logging.md`
- **Exercises** — `exercises/README.md` (five short, focused tasks)
- **Challenges** — `challenges/README.md` (two longer, open-ended problems)
- **Quiz** — `quiz.md` (10 multiple-choice questions, self-graded)
- **Homework** — `homework.md` (6 problems, due before Week 7)
- **Mini-project** — `mini-project/README.md` (the capstone for this week)
- **Resources** — `resources.md` (official docs, articles, references)

---

## Stretch goals

If you finish early and want to push further:

1. **Encoding deep dive** — read [Joel Spolsky's "The Absolute Minimum Every Software Developer Must Know About Unicode"](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/), then write a tool that converts a file from `latin-1` to `utf-8`.
2. **`logging` config files** — read the [logging.config](https://docs.python.org/3/library/logging.config.html) docs and load your logger config from a YAML or JSON file.
3. **Atomic writes** — implement a context manager `atomic_write(path)` that writes to a temp file and renames on success. We preview this in homework problem 6.
4. **Stream large files** — generate a 1 GB text file and learn why `for line in f:` is the only sane way to process it (don't `.read()` it all).
5. **TOML** — Python 3.11+ ships `tomllib`. Read the [docs](https://docs.python.org/3/library/tomllib.html) and rewrite Exercise 03 to use TOML instead of JSON.

---

## Up next

Once you finish this week, head to **[Week 7 — Object-Oriented Programming](../week-07-object-oriented-programming/)**. We will use the custom exception you wrote here as a stepping stone into classes, inheritance, and the special methods that make Python objects feel native.

---

## Submission checklist

Before marking this week complete:

- [ ] Read all three lecture notes
- [ ] Completed exercises 01–05 (working code, runs without error)
- [ ] Attempted both challenges (write-up in markdown)
- [ ] Passed the quiz (8/10 or higher; retake until you do)
- [ ] Submitted homework problems
- [ ] Mini-project runs end-to-end and outputs both JSON summary and CSV report
- [ ] Pushed everything to your fork of the bootcamp repo

Happy crunching!
