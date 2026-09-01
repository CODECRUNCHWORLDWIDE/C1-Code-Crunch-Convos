# Reference Solution — File Organizer Bot (Week 12)

This is the worked reference implementation for the Week 12 mini-project,
[File Organizer Bot](../../../curriculum/week-12-automation-scripting/mini-project/README.md).

Read the mini-project page alongside it — the answer and the reasoning behind it
sit there, beside the brief that asked for them. This file is the operating
manual: what is here, how to run it, and how it maps onto the spec.

Only open this after you have built your own version. The mini-project is where
Week 12 actually lands; reading a finished answer first spends the learning for
nothing.

---

## What's here

```text
week-12-automation-scripting/
├── 00-overview.md           # this file
├── organize.py              # the whole tool — one module, no package needed
├── config.json              # the category map from the spec, verbatim
├── requirements-dev.txt     # pytest only; organize.py itself is stdlib-only
└── tests/
    └── test_organize.py     # 10 tests
```

`organize.py` imports nothing outside the standard library: `argparse`, `json`,
`logging`, `shutil`, `sys`, `time`, `pathlib`. That is deliberate. A tool that
tidies your `~/Downloads` should still work in three years on a fresh machine
with nothing installed.

---

## Running it

From this folder, with any Python 3.10 or newer (`X | None` type syntax and
`dict[str, list[str]]` builtins are used throughout; `from __future__ import
annotations` at the top means they are only strings at runtime, so 3.9 works
too):

```bash
# Preview. This is the default — no --apply, nothing moves.
python organize.py ~/Downloads --config config.json

# Do it for real.
python organize.py ~/Downloads --config config.json --apply

# Sit there and keep tidying as new files land.
python organize.py ~/Downloads --config config.json --watch --interval 5 --apply

# Every knob:
python organize.py --help
```

### Sample run

Seven junk files in a scratch directory, dry-run then apply:

```text
$ python organize.py ./Downloads --config config.json
2026-08-21 01:37:58 INFO  would move backup.zip -> Archives/backup.zip
2026-08-21 01:37:58 INFO  would move beach.jpg -> Images/beach.jpg
2026-08-21 01:37:58 INFO  would move chart.png -> Images/chart.png
2026-08-21 01:37:58 INFO  would move invoice.pdf -> Documents/invoice.pdf
2026-08-21 01:37:58 INFO  would move notes.md -> Documents/notes.md
2026-08-21 01:37:58 INFO  would move script.py -> Code/script.py
2026-08-21 01:37:58 INFO  would move weird_thing.xyz -> Other/weird_thing.xyz
2026-08-21 01:37:58 INFO  would move 7 file(s)

$ python organize.py ./Downloads --config config.json --apply
2026-08-21 01:37:58 INFO  moved backup.zip -> Archives/backup.zip
2026-08-21 01:37:58 INFO  moved beach.jpg -> Images/beach.jpg
2026-08-21 01:37:58 INFO  moved chart.png -> Images/chart.png
2026-08-21 01:37:58 INFO  moved invoice.pdf -> Documents/invoice.pdf
2026-08-21 01:37:58 INFO  moved notes.md -> Documents/notes.md
2026-08-21 01:37:58 INFO  moved script.py -> Code/script.py
2026-08-21 01:37:58 INFO  moved weird_thing.xyz -> Other/weird_thing.xyz
2026-08-21 01:37:58 INFO  moved 7 file(s)
```

Resulting tree:

```text
Downloads/
├── Archives/backup.zip
├── Code/script.py
├── Documents/invoice.pdf
├── Documents/notes.md
├── Images/beach.jpg
├── Images/chart.png
├── Other/weird_thing.xyz
└── organize.log
```

Running the same `--apply` command again moves nothing and logs
`moved 0 file(s)` — the tool is idempotent.

---

## Running the tests

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

Expected:

```text
..........                                                               [100%]
10 passed in 0.26s
```

The tests use pytest's built-in `tmp_path` fixture, so they never touch a real
directory of yours. `tests/test_organize.py` puts the project folder on
`sys.path` before importing `organize`, which is why you can run pytest from
here without installing anything or adding a `conftest.py`.

---

## How it maps to the spec

| Spec requirement | Where it lives in `organize.py` |
|---|---|
| `DIRECTORY` positional, `--config`, `--apply`, `--watch`, `--interval`, `--log`, `-v` | `build_parser()` |
| Config file is JSON, category → extension list | `load_config()` |
| "First category with an empty list" fallback | `fallback_category()` |
| Category whose list contains the suffix wins | `build_extension_map()` + `categorise()` |
| Skip directories | `entry.is_dir()` guard in `organize_once()` |
| Skip files already inside a category folder | `directory.iterdir()` — top level only, so sorted files are never revisited |
| Skip the log file itself | `skip` set in `organize_once()`, compared on `resolve()` |
| Collision-safe `name-1.ext` | `unique_path()` |
| Log to file *and* terminal | `configure_logging()` — two handlers, one formatter |
| `would move ...` in dry-run, `moved ...` with `--apply` | the `if apply:` branch in `organize_once()` |
| Exit 0 / 1 / 2 | `main()` returns 0 or 1; argparse raises `SystemExit(2)` itself |
| Type hints, `pathlib`, `logging`, small functions | throughout — no raw string paths, no `print` except the two pre-logging fatal errors on stderr |
| Two or more pytest tests using `tmp_path` | `tests/test_organize.py`, 10 tests |

Two `print(..., file=sys.stderr)` calls survive in `main()`. They are the errors
that happen *before* logging is configured — a missing directory and an
unopenable log file. You cannot log your way out of "the log file will not
open", so those go straight to stderr, exactly as Lecture 1 §8 describes.

---

## Rubric self-check (25 points)

| Category | Pts | Evidence |
|---|---|---|
| Correctness on the happy path | 5 | sample run above; `test_apply_moves_files_into_categories` |
| Dry-run default + `--apply` | 3 | `test_dry_run_moves_nothing`, `test_main_dry_run_writes_a_log_line` |
| `--watch` polling | 3 | `main()` watch branch; `KeyboardInterrupt` → exit 0 |
| Config loading + `Other` fallback | 2 | `load_config()`, `fallback_category()`, `test_apply_moves_files_into_categories` |
| Collision-safe rename | 2 | `unique_path()`, `test_collision_gets_numeric_suffix` |
| Logging to file + console | 2 | `configure_logging()`; log excerpt above |
| Type hints, `pathlib`, organization | 3 | every public function annotated; no `os.path` anywhere |
| Tests pass and cover non-trivial behavior | 3 | 10 passing, including idempotence and all three exit codes |
| README + sample run output | 2 | this file |

Self-assessed 25/25 against the published rubric. The bar for a pass is 15;
distinction is 21.
