# Challenge 01 — Recursive line counter

Build a command-line tool that walks a directory tree recursively, counts the total number of lines of code in every `.py` file, and prints a per-file breakdown plus a grand total.

---

## Specification

Write a script `challenge-01-solution.py` that exposes a function:

```python
def count_python_lines(root: Path) -> dict[Path, int]:
    """Return a dict mapping each .py file under `root` to its line count."""
```

Plus an `if __name__ == "__main__":` block that:

1. Reads the target directory from `sys.argv[1]` (default: the current directory).
2. Calls `count_python_lines(...)`.
3. Prints a sorted table of files and line counts.
4. Prints a final line with the grand total.

### Requirements

- Use `pathlib.Path.rglob("*.py")` for the walk.
- Use `open(..., encoding="utf-8")` to read each file.
- **Handle errors gracefully:**
  - `PermissionError` — log a warning and skip that file. Do not crash.
  - `UnicodeDecodeError` — log a warning and skip that file (some `.py` files might be in a weird encoding).
  - `OSError` (catch-all for other filesystem errors) — log a warning and skip.
- Use the `logging` module for warnings, not `print`.
- Do not count blank lines (use `line.strip()` to test).

### Example output

```
$ python challenge-01-solution.py ../week-06-file-io-exceptions
   12 exercises/exercise-01-read-write.py
   38 exercises/exercise-02-csv-roundtrip.py
   33 exercises/exercise-03-json-config.py
   42 exercises/exercise-04-safe-divide.py
   53 exercises/exercise-05-custom-exception.py
   85 mini-project/starter.py
-----
  263 total
```

### Constraints

- Pure standard library — no `os.walk` (use `pathlib`).
- No external packages.
- Must run on Python 3.10+.

---

## Stretch goals

If the basic version is working, try one or more of:

1. **CLI flags** — accept `--ext .py,.md` to count lines of any extension(s).
2. **Sort by count** — accept `--sort-by-count` to order files largest-first.
3. **Exclude `__pycache__/` and `.venv/`** — common directories you almost never want to count.
4. **Print a histogram** — show a bar chart in the terminal: `████████ 53`.
5. **Add a `--top N` flag** that only shows the N largest files.

---

## Rubric (10 pts)

| Criterion | Points |
|---|---|
| Walks the tree correctly with `pathlib` | 2 |
| Counts non-blank lines accurately | 2 |
| Handles `PermissionError` and `UnicodeDecodeError` without crashing | 3 |
| Uses `logging`, not `print`, for warnings | 1 |
| Clean output (sorted, total line) | 1 |
| Type hints and docstrings on all functions | 1 |
