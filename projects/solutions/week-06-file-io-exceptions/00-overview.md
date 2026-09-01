# Reference implementation — Week 6 mini-project (log file analyzer)

This folder is the working answer to [Week 6's mini-project](../../../curriculum/week-06-file-io-exceptions/mini-project/README.md). It is a real, runnable program, not an excerpt: what you see here is exactly what was executed to produce the transcripts in the [mini-project walkthrough](../../../curriculum/week-06-file-io-exceptions/mini-project/README.md).

Read the walkthrough for the *why*. This file tells you what is here and how to run it.

---

## What is in the folder

| File | What it is |
|---|---|
| `analyzer.py` | The whole tool. One file, standard library only, ~300 lines including docstrings. |
| `sample.log` | 30 lines of realistic log input — 28 well-formed entries plus two lines that are deliberately unparseable. |
| `expected/summary.json` | The JSON summary the tool produces from `sample.log`, byte-for-byte. |
| `expected/by-level.csv` | The CSV report the tool produces from `sample.log`, byte-for-byte. |

`sample.log` is also the file the mini-project spec expects to find next to the assignment. If it is not there, use this copy.

---

## How to run it

Python 3.10 or newer. No `pip install` step — everything it imports (`argparse`, `csv`, `gzip`, `json`, `logging`, `re`, `collections`, `pathlib`) ships with CPython.

```bash
cd projects/solutions/week-06-file-io-exceptions
python analyzer.py sample.log --out-dir reports/
```

Expected output on stdout, with the two skip warnings on stderr:

```
WARNING  analyzer  sample.log:7: skipping malformed line: -- log rotated by logrotate at 14:30:05 --
WARNING  analyzer  sample.log:23: skipping malformed line: 2026-05-13 14:31:07 TRACE    entering render loop
Parsed 28/30 lines. Top error: 'Failed to connect to cache: timeout' (2x).
Reports written to reports/summary.json and reports/by-level.csv.
```

### Check it against the recorded output

```bash
python analyzer.py sample.log --out-dir reports/
diff expected/summary.json reports/summary.json
diff expected/by-level.csv reports/by-level.csv
```

Both `diff`s should print nothing and exit 0. On Windows, `fc expected\summary.json reports\summary.json` does the same job.

---

## The stretch goals

All six of the mini-project's stretch goals are implemented. Every one is **opt-in**, so the default invocation stays byte-identical to the spec.

| Flag / behaviour | Stretch goal |
|---|---|
| `--timestamps` | 1 — adds `first_timestamp` / `last_timestamp` to the JSON summary |
| `--by-hour` | 2 — also writes `<out-dir>/by-hour.csv` with `hour,count` |
| multiple `LOG` arguments | 3 — aggregates several files into one summary |
| `--min-level WARNING` | 4 — drops entries below the given level entirely |
| `.gz` inputs (automatic) | 5 — `gzip.open(..., "rt")` when the suffix is `.gz` |
| `--top-errors N` | 6 — adds a `top_errors` array of the N most common ERROR messages |

```bash
python analyzer.py sample.log --out-dir reports/ --timestamps --by-hour --top-errors 3
python analyzer.py app.log app.log.1.gz --out-dir reports/
python analyzer.py sample.log --out-dir reports/ --min-level WARNING
```

---

## How it maps to the spec

| Spec requirement | Where it lives |
|---|---|
| `parse_line(line) -> dict \| None` | `parse_line`, backed by the module-level `LINE_RE` |
| Skip malformed lines with a WARNING and the line number | `read_records`, the `log.warning("%s:%d: ...")` calls |
| `analyze(records) -> dict` | `analyze` (counts + most common ERROR) |
| `write_summary(summary, path)` | `write_summary` — `json.dump(..., indent=2)` |
| `write_csv(summary, path)` | `write_csv` — `csv.writer`, rows sorted by level |
| `main(args) -> int` | `main`, returning the exit code; `parse_args` holds the CLI |
| `FileNotFoundError` → friendly message, exit 1 | the `except FileNotFoundError` in `main` |
| `re.error` left uncaught | nothing catches it; a bad pattern is a programmer bug |
| `pathlib` everywhere | every path is a `Path`; `argparse` converts with `type=Path` |
| `logging` for diagnostics, `print` for the result | module-level `log`; the only `print`s are the two summary lines and the two error messages |

---

## Reading order

If you are studying the code rather than running it, read it in this order — it is the order the data flows:

1. `LINE_RE` and `parse_line` — one line of text becomes one record dict.
2. `read_records` — a file becomes a list of records plus a line tally.
3. `analyze` and `build_summary` — records become the summary dict.
4. `write_summary` and `write_csv` — the summary becomes two files.
5. `parse_args` and `main` — the glue, read last, because it only makes sense once you know what it is gluing.

That is also a good order to *write* it in, and it is why the file is laid out that way.
