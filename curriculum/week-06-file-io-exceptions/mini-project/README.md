# Mini-project — Log file analyzer

Build a small command-line tool that reads a `.log` file, counts log levels (INFO / WARNING / ERROR), identifies the most common error message, and emits two reports: a JSON summary and a CSV breakdown.

This is the capstone for Week 6. You will use **every topic** from this week's lectures: file I/O, pathlib, regex parsing (light), CSV writing, JSON dumping, exception handling, and logging.

---

## The input format

A log file is a plain-text file with one entry per line. Each entry looks like:

```
2026-05-13 14:30:01 INFO     Connection opened to db-primary
2026-05-13 14:30:02 WARNING  Slow query: SELECT * FROM users (1.2s)
2026-05-13 14:30:03 ERROR    Failed to connect to cache: timeout
```

The fields are:

1. **Date** — `YYYY-MM-DD`
2. **Time** — `HH:MM:SS`
3. **Level** — `INFO`, `WARNING`, `ERROR`, or `DEBUG`
4. **Message** — free-form text, may contain anything

Fields are separated by **whitespace**, but the message itself can contain spaces.

A small `sample.log` is included in this folder for testing.

---

## What your tool should produce

When run as `python analyzer.py sample.log --out-dir reports/`, it should:

1. Parse `sample.log` line by line.
2. **Gracefully skip** lines that do not match the expected format. Log a WARNING for each skipped line (with the line number).
3. Count entries per level (INFO / WARNING / ERROR / DEBUG).
4. Identify the **most common ERROR message** (and how many times it occurred).
5. Write a JSON summary to `reports/summary.json`:

   ```json
   {
     "source_file": "sample.log",
     "total_lines": 30,
     "parsed_lines": 28,
     "skipped_lines": 2,
     "counts": {
       "DEBUG": 0,
       "INFO": 18,
       "WARNING": 6,
       "ERROR": 4
     },
     "most_common_error": {
       "message": "Failed to connect to cache: timeout",
       "count": 2
     }
   }
   ```

6. Write a CSV report to `reports/by-level.csv`:

   ```
   level,count
   DEBUG,0
   ERROR,4
   INFO,18
   WARNING,6
   ```

7. Print a one-line summary to the console.

---

## Constraints

- Pure standard library — no external packages.
- Python 3.10 or newer.
- Use `pathlib.Path` for all file paths (no string concatenation).
- Use the `logging` module for all diagnostic output (not `print`, except for the final summary line).
- Use `csv.writer` for the CSV and `json.dump` for the JSON.
- Catch **specific** exceptions:
  - `FileNotFoundError` when the input file does not exist → print a friendly error and exit with code 1.
  - `re.error` if your regex is malformed → let it crash (it is a programmer bug, not user input).
  - Malformed lines → log a WARNING and continue.

---

## Suggested structure

Look at `starter.py` — it has the imports and function stubs already. Your job is to fill them in. The stubs split the work into:

- `parse_line(line: str) -> dict | None` — return a parsed record, or None for malformed lines.
- `analyze(records: list[dict]) -> dict` — compute the summary stats.
- `write_summary(summary: dict, path: Path) -> None` — write JSON.
- `write_csv(summary: dict, path: Path) -> None` — write CSV.
- `main(args) -> int` — orchestrate everything.

You do not have to follow this structure exactly, but if you are unsure where to start, follow it.

---

## Rubric (25 pts)

| Criterion | Points |
|---|---|
| Reads and parses the log file correctly | 4 |
| Handles missing input file gracefully (exit code 1, friendly message) | 2 |
| Skips malformed lines with a WARNING (not a crash) | 3 |
| Correctly counts entries per level | 3 |
| Correctly identifies most-common error message | 3 |
| Writes valid, pretty-printed JSON summary | 3 |
| Writes valid CSV report | 2 |
| Uses `pathlib` for paths | 1 |
| Uses `logging`, not `print`, for diagnostics | 2 |
| Type hints + docstrings on every function | 2 |

Total: 25.

---

## Stretch goals

If you finish early:

1. **Timestamps in the summary** — record the earliest and latest entry timestamp in the JSON summary.
2. **Per-hour buckets** — write a second CSV with `hour,count` (events per hour).
3. **Multi-file support** — accept multiple log files and aggregate them all.
4. **Filter by level** — accept `--min-level WARNING` to ignore DEBUG/INFO lines entirely.
5. **Gzip support** — if the file ends in `.gz`, open it with the `gzip` module. (Same context-manager protocol.)
6. **`--top-errors N`** — instead of just the single most common error, list the top N.

---

## What "done" looks like

```
$ python analyzer.py sample.log --out-dir reports/
Parsed 28/30 lines. Top error: 'Failed to connect to cache: timeout' (2x).
Reports written to reports/summary.json and reports/by-level.csv.
```

Both report files should exist, be valid (JSON parseable, CSV importable into Excel), and match the counts in your console line.

Good luck — and remember, **error handling is half the work**. A tool that crashes on the first weird line of input is not done; a tool that logs the problem and keeps going is.
