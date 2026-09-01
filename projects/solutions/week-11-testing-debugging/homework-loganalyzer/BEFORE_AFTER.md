# BEFORE / AFTER — what changed, and why each change made testing easier

This is the deliverable for **Homework Problem 1**. The starting point is the
Week 6 mini-project reference,
[`projects/solutions/week-06-file-io-exceptions/analyzer.py`](../../week-06-file-io-exceptions/analyzer.py):
one 304-line module that parses, counts, formats, writes, prints and exits.

It worked. It still works — the JSON and CSV this package produces are
byte-for-byte what Week 6 produced. What changed is that you can now get at the
interesting parts without running the program.

---

## Change 1 — one module became five, split by *what they touch*

**Before.** `analyzer.py` held all of it: `LINE_RE`, `parse_line`, `read_records`,
`analyze`, `build_summary`, `hourly_counts`, `filter_min_level`, `write_summary`,
`write_csv`, `write_hourly_csv`, `parse_args`, `main`.

**After.**

| Module | Touches | Cannot touch |
|---|---|---|
| `models.py` | nothing | everything |
| `parsing.py` | the file system (read) | counting, formatting, printing |
| `analysis.py` | nothing | files, `stdout`, `argparse` |
| `reporting.py` | the file system (write) | `stdout`, `argparse` |
| `cli.py` | `sys.argv`, `stdout`, `stderr`, the exit code | — |

The split is not by noun ("posts, users, config"), it is by **side effect**.
That is the axis that matters for testability, because a test's cost is
dominated by the side effects it has to arrange and clean up.

**Why it made testing easier.** `tests/test_analysis.py` — 25 test functions and
28 cases, the largest file in the suite — opens no files, creates no
`tmp_path`, and uses no mock. It
cannot, because nothing it imports can perform I/O. Every test in it is a list
literal, a call, and an equality assertion. In Week 6 the same assertions would
have needed a file on disk, because `analyze` was only reachable through
`read_records`.

The one place a mock still earns its keep is
`test_main_returns_one_when_the_file_cannot_be_read`, which monkeypatches
`cli.read_records` to raise `PermissionError` — because chmod semantics differ
across Windows, macOS and Linux, and root ignores them entirely. One mock in 78
tests is the right number.

---

## Change 2 — hard-coded constants became arguments

**Before.**

```python
LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR")

def analyze(records: list[dict[str, str]]) -> dict:
    counts = {level: 0 for level in LEVELS}     # module global, no way in
    ...

def filter_min_level(records, min_level):
    threshold = LEVELS.index(min_level)          # module global again
    ...

# and, inside main():
summary_path = args.out_dir / "summary.json"     # filename baked into main
csv_path = args.out_dir / "by-level.csv"
```

**After.**

```python
def count_levels(records: Sequence[LogRecord], levels: Sequence[str] = LEVELS) -> dict[str, int]:
def filter_min_level(records: Sequence[LogRecord], min_level: str,
                     levels: Sequence[str] = LEVELS) -> list[LogRecord]:
def write_reports(summary, records, out_dir, *, by_hour=False,
                  summary_name=SUMMARY_FILENAME, level_name=BY_LEVEL_FILENAME,
                  hour_name=BY_HOUR_FILENAME) -> tuple[Path, Path]:
```

`LEVELS` is still the default, so no caller changes. But it is now a *seam*.

**Why it made testing easier.** Two tests exist that could not have been written
before: `test_count_levels_accepts_a_custom_level_tuple` and
`test_filter_min_level_accepts_a_custom_level_ordering`. Both would previously
have required either editing the module or monkeypatching a global — and a
monkeypatched global is a test that passes for a reason you did not intend, the
single most common way a suite goes quietly useless.

`write_reports` returning `tuple[Path, Path]` instead of printing them is the
same move at the output end: `cli.main` decides the wording, and a test asserts
on the paths.

---

## Change 3 — `dict[str, str]` became a frozen dataclass, `dict` became a `TypedDict`

**Before.** A record was `{"date": ..., "time": ..., "level": ..., "message": ...}`
and the summary was a bare `dict`. Both are opaque to `mypy`: nothing stops you
writing `record["mesage"]`, and nothing tells you the summary has a `counts` key
until the program runs and blows up.

**After.** `LogRecord` is a `@dataclass(frozen=True, slots=True)` with two derived
properties (`timestamp`, `hour`) that Week 6 recomputed inline in three places
as f-strings. `Summary` is a `TypedDict(total=False)`, so the optional keys that
only appear with `--timestamps` and `--top-errors` are *typed as* optional
rather than being a comment.

**Why it made testing easier.** Three separate wins:

1. `assert record == LogRecord(date=..., time=..., level=..., message=...)`
   compares the whole record in one line, and the failure diff names the field
   that differs. Comparing dicts gives you the same information more noisily;
   comparing them field by field gives you four assertions and a partial answer.
2. `frozen=True` is what makes the module-scoped `sample_records` fixture safe.
   A wide-scoped fixture is only safe if nothing mutates the shared object, and
   `frozen=True` turns "nothing mutates it" from a convention into a
   `FrozenInstanceError`. `test_logrecord_is_frozen` pins that.
3. `mypy --strict` can now check the summary. `summary["parsed_lines"]` is an
   `int`, `summary["most_common_error"]` is `ErrorSummary | None`, and the
   `if top else "none"` in `cli.main` is *required* rather than defensive.

---

## What did **not** change

The point of Problem 1 is "make the code testable **without changing observable
behavior**". Held constant:

- The JSON key order in `summary.json`, including which optional keys appear.
- The CSV headers, row order (`by-level.csv` alphabetical, `by-hour.csv`
  chronological) and `\r\n` row endings.
- The two lines printed on success, and the warning format for skipped lines.
- Exit code 0 on success, 1 on a missing or unreadable file.
- `.gz` support, multi-file support, and the six flags.

One thing did change, and pretending otherwise would be dishonest: the error
prefix. Week 6 printed `analyzer.py: error: log file not found: x.log` because
the script *was* `analyzer.py`. The entry point is now `python -m loganalyzer`,
so the prefix is `loganalyzer:`. It lives in `cli.PROG`, one constant, one place.

---

## The receipts

```text
$ python -m loganalyzer sample.log --out-dir reports --timestamps --top-errors 3 --by-hour
WARNING  loganalyzer.parsing  sample.log:7: skipping malformed line: -- log rotated by logrotate at 14:30:05 --
WARNING  loganalyzer.parsing  sample.log:23: skipping malformed line: 2026-05-13 14:31:07 TRACE    entering render loop
Parsed 28/30 lines. Top error: 'Failed to connect to cache: timeout' (2x).
Reports written to reports/summary.json and reports/by-level.csv.
```

Identical to what `python analyzer.py sample.log --out-dir reports ...` printed
in Week 6, modulo the logger name on the warning lines and the `PROG` change
above.
