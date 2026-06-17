# Week 6 — Homework

Six problems. Each problem describes the script to write, the inputs it should handle, and the expected behavior. Submit one `.py` file per problem in a `homework/` folder.

You are expected to use what you learned this week: `pathlib`, `with`, `csv`, `json`, custom exceptions, `logging`. Resist the temptation to copy-paste from the lectures — write the code from memory and check the lectures only when stuck.

---

## Problem 1 — Word-count CLI

Write a script `word_count.py` that:

- Accepts one or more file paths from `sys.argv`.
- For each file, prints a line in the form `   42  notes.txt` (right-aligned word count, then the path).
- After all files, prints a `   total` line.
- If a file cannot be read (missing, permission, decode error), logs a WARNING with the path and the error type, and continues with the remaining files.

```
$ python word_count.py essay.txt notes.txt missing.txt
   124  essay.txt
WARNING  word_count  could not read missing.txt: FileNotFoundError
    42  notes.txt
-----
   166  total
```

---

## Problem 2 — CSV merger

Write a script `csv_merge.py` that:

- Accepts a list of input CSV paths and one output path.
- All input files have the **same header**. (If they do not, raise a `ValueError` with a clear message before writing anything.)
- Concatenates all rows from all inputs into the output file, preserving header order.
- Adds an extra column `source` to each row containing the input filename (without extension).

```
$ python csv_merge.py q1.csv q2.csv q3.csv --out year.csv
Merged 3 files → year.csv (842 total rows)
```

Use `argparse` for the CLI (you have seen it briefly; the [docs](https://docs.python.org/3/library/argparse.html) are friendly).

---

## Problem 3 — JSON pretty-printer

Write a script `json_pretty.py` that:

- Reads JSON from `sys.argv[1]` (the input file).
- Writes a pretty-printed version (indent=2, sort_keys=True) to `sys.argv[2]`.
- If the input is invalid JSON, prints **exactly one** error line that contains the file path, the line number, the column number, and the parser message — then exits with code 1.

```
$ python json_pretty.py messy.json clean.json
$ python json_pretty.py bad.json out.json
ERROR  bad.json:1:17  Expecting property name enclosed in double quotes
$ echo $?
1
```

Hint: `sys.exit(1)` to set the exit code; `json.JSONDecodeError` has `.lineno`, `.colno`, and `.msg`.

---

## Problem 4 — Retry-on-error decorator (preview of decorators)

You have not formally learned decorators yet, but you can copy the syntax. Write a script `retry.py` that defines a decorator:

```python
def retry(exc_type: type[Exception], attempts: int = 3):
    """Decorator: retry the wrapped function up to `attempts` times if `exc_type` is raised."""
```

Behavior:

- Try the wrapped function.
- If it raises an exception of type `exc_type`, log a WARNING and try again, up to `attempts` total tries.
- On the final failure, re-raise the exception.
- Any **other** exception type propagates immediately (no retry).

Demonstrate it with a function that fails the first two times and succeeds on the third. Print the result.

---

## Problem 5 — File watcher (poll-based)

Write a script `watch.py` that:

- Accepts a file path.
- Polls the file's modification time once per second (use `time.sleep(1)` and `Path.stat().st_mtime`).
- When the mtime changes, prints a line `[2026-05-13 14:30:01] file modified` and prints the new contents.
- Handles `FileNotFoundError` gracefully (logs a WARNING and keeps polling).
- Exits cleanly on `KeyboardInterrupt` (Ctrl-C) — do NOT let the traceback show.

This is a simplified version of `tail -f`. It is also a preview of why people use libraries like `watchdog` for the real thing.

---

## Problem 6 — Atomic-save helper

Write a script `atomic.py` exposing one function:

```python
def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write `content` to `path` atomically.

    The write is done to a temporary file first; on success it is renamed
    over `path`. Readers either see the old file or the new file, never
    a half-written one.
    """
```

Behavior:

- Pick a temp file name like `path.with_suffix(path.suffix + ".tmp")`.
- Write the content to that path.
- Use `tmp_path.replace(path)` to atomically replace the original. (`Path.replace` is atomic on POSIX and on modern Windows.)
- If the write fails, the temp file should be cleaned up (use `try/except/finally`).

In `__main__`, demonstrate by overwriting a file, then **simulating a failure mid-write** (raise an exception on purpose) and showing that the original file is still intact.

---

## Submission

- One folder named `homework/` containing six `.py` files.
- Each file runnable as `python <name>.py ...`.
- Each file should have a module docstring describing what it does and an example invocation.
- Use type hints. Use `logging`. Catch narrow exceptions.

Due before you start Week 7.
