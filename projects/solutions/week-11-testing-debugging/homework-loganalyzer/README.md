# `loganalyzer` — Week 11 homework reference implementation

![CI](https://github.com/YOUR-USERNAME/loganalyzer/actions/workflows/ci.yml/badge.svg)

The Week 6 log analyzer, refactored until it could be tested, then tested,
type-checked, linted, formatted, hooked and CI'd. This one project is the
answer to **all six** homework problems, because the homework asks you to do all
six to *the same* project.

| Problem | Deliverable | Where it is |
|---|---|---|
| 1 — refactor for testability | `BEFORE_AFTER.md` | [`BEFORE_AFTER.md`](./BEFORE_AFTER.md) |
| 2 — write the tests | `tests/`, coverage report | [`tests/`](./tests) |
| 3 — CI | `.github/workflows/ci.yml` + badge | [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) |
| 4 — `pre-commit` | `.pre-commit-config.yaml` + hook notes | [`.pre-commit-config.yaml`](./.pre-commit-config.yaml) |
| 5 — serious `ruff` config | `[tool.ruff]` in `pyproject.toml` | [`pyproject.toml`](./pyproject.toml) |
| 6 — `mypy --strict` clean | `mypy.txt` | [`mypy.txt`](./mypy.txt) |

## Install

```bash
python -m venv .venv
source .venv/bin/activate          # .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install
```

## Run it

```bash
python -m loganalyzer sample.log --out-dir reports
python -m loganalyzer sample.log --out-dir reports --timestamps --top-errors 3 --by-hour
python -m loganalyzer app.log app.log.1.gz --out-dir reports --min-level WARNING
```

Real output against the shipped `sample.log`:

```text
$ python -m loganalyzer sample.log --out-dir reports --timestamps --top-errors 3 --by-hour
WARNING  loganalyzer.parsing  sample.log:7: skipping malformed line: -- log rotated by logrotate at 14:30:05 --
WARNING  loganalyzer.parsing  sample.log:23: skipping malformed line: 2026-05-13 14:31:07 TRACE    entering render loop
Parsed 28/30 lines. Top error: 'Failed to connect to cache: timeout' (2x).
Reports written to reports/summary.json and reports/by-level.csv.
```

```json
{
  "source_file": "sample.log",
  "total_lines": 30,
  "parsed_lines": 28,
  "skipped_lines": 2,
  "counts": { "DEBUG": 0, "INFO": 18, "WARNING": 6, "ERROR": 4 },
  "most_common_error": { "message": "Failed to connect to cache: timeout", "count": 2 },
  "first_timestamp": "2026-05-13 14:30:01",
  "last_timestamp": "2026-05-13 14:31:21",
  "top_errors": [
    { "message": "Failed to connect to cache: timeout", "count": 2 },
    { "message": "Payment gateway returned 502", "count": 1 },
    { "message": "Unhandled exception in worker 3", "count": 1 }
  ]
}
```

(The JSON above is re-indented for the README; the file itself is
`json.dump(..., indent=2)` with one key per line.)

## Test

```bash
pytest                                                                        # fast loop
pytest -vv                                                                    # per-test listing
pytest --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80
```

```text
$ pytest
........................................................................ [ 92%]
......                                                                   [100%]
78 passed in 0.32s
```

```text
$ pytest --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80
Name                           Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------
src\loganalyzer\__init__.py        4      0      0      0   100%
src\loganalyzer\analysis.py       42      0     14      0   100%
src\loganalyzer\cli.py            51      0      4      0   100%
src\loganalyzer\models.py         30      0      0      0   100%
src\loganalyzer\parsing.py        34      0     10      0   100%
src\loganalyzer\reporting.py      37      0      6      0   100%
--------------------------------------------------------------------------
TOTAL                            198      0     34      0   100%
Required test coverage of 80% reached. Total coverage: 100.00%
78 passed in 0.50s
```

The homework asks for 80 %. The suite lands at 100 % line **and** branch, which
is a consequence of the split rather than an act of heroism: once every function
is small and side-effect-free, there is nowhere for an untested branch to hide.

`__main__.py` is `omit`ted in `[tool.coverage.run]`. It is two lines
(`from ... import main` / `raise SystemExit(main())`) and `coverage` cannot reach
it from a test that imports the package, so counting it would mean either a
permanent 98 % or a fake test that shells out. Omitting it and keeping it
trivial is the honest option.

### What Problem 2 asked for, and where it is

| Requirement | Where |
|---|---|
| 15+ test functions | 70 test functions, 78 cases after parametrization |
| 3+ fixtures | 6 in `tests/conftest.py` — `sample_log`, `sample_facts`, `sample_records`, `out_dir`, `make_records`, `error_records` |
| 1+ `scope="module"` fixture | `sample_log`, `sample_facts` and `sample_records` are all module-scoped |
| 1+ parametrized test with 4+ rows | `test_parse_line_returns_none_for_malformed_input` (6 rows), `test_filter_min_level_keeps_that_level_and_above` (4 rows) |
| 1+ `pytest.raises` | `test_filter_min_level_rejects_an_unknown_level`, `test_read_records_raises_for_a_missing_file`, `test_logrecord_is_frozen`, `test_parser_rejects_an_unknown_min_level` |
| 80 %+ coverage | 100 % line and branch |

## Quality gates

```bash
ruff check .        # All checks passed!
black --check .     # 12 files would be left unchanged.
mypy src            # Success: no issues found in 7 source files
```

CI runs all four again on a clean Ubuntu VM, on Python 3.11 **and** 3.12.

### The `ruff` config, hook by hook

`[tool.ruff.lint] select` is `["E", "W", "F", "I", "B", "UP", "SIM", "C4", "RET"]`:

| Family | What it buys you |
|---|---|
| `E`, `W` | pycodestyle errors and warnings — the pep8 baseline. |
| `F` | pyflakes: unused imports, undefined names, f-strings with no placeholders. |
| `I` | isort: one canonical import order, so imports stop showing up in diffs. |
| `B` | bugbear: real bugs — mutable default arguments, `except:` swallowing everything, loop-variable capture in closures. |
| `UP` | pyupgrade: rewrites to modern syntax for your `target-version`. |
| `SIM` | simplifications — collapsible `if`s, `if x: return True else: return False`. |
| `C4` | comprehension hygiene — `list(x for x in y)` → `[x for x in y]`. |
| `RET` | return hygiene — unnecessary `else` after `return`, assign-then-return. |

`ignore = ["E501"]` because `black` owns line length and having two tools argue
about it is how you end up disabling one of them in anger.

`per-file-ignores` relaxes `S101` (`assert` used) inside `tests/`. `S101` comes
from the `S` (flake8-bandit) family, which is *not* in our `select` list — so
the ignore is currently a no-op. It is here on purpose: the day someone adds
`"S"` to `select`, the test suite would light up with hundreds of `S101`s, and
this line is what stops that from being a reason to back the change out.

### A note on `target-version = "py312"`

Problem 5 specifies `py312`, and that is what this file has. Understand what the
setting means before you copy it: `target-version` is the version `UP` rewrites
*towards*. Set it newer than the oldest interpreter in your CI matrix and `ruff`
will happily suggest syntax that half your matrix cannot parse. The Week 11
challenge-2 blog hits exactly that — `UP047` wants a `TypeVar` rewritten as a
PEP 695 generic, which is a syntax error on 3.11 — and pins `py311` for that
reason. Nothing in this package trips it, so `py312` is safe here.

### `pre-commit`, hook by hook

| Hook | In your own words |
|---|---|
| `trailing-whitespace` | Strips spaces at end of line. They are invisible, they show up in every diff, and no one ever meant to type them. |
| `end-of-file-fixer` | Guarantees exactly one newline at the end of a file, so `git diff` stops printing `\ No newline at end of file`. |
| `check-yaml` | Parses every `.yaml`/`.yml`. Catches the CI workflow you broke with a bad indent *before* you push and wait three minutes to find out. |
| `check-toml` | The same for `pyproject.toml`, which is now the config for five different tools. |
| `check-added-large-files` | Refuses a commit that adds a file over 500 kB. Git never forgets a blob; a stray 200 MB log file is permanent. |
| `ruff --fix` | Lints, and applies the safe autofixes. Runs first because it rewrites imports. |
| `black` | Formats. Runs after `ruff` so it has the last word on layout. |
| `mypy --strict` | Type-checks. `additional_dependencies` is empty because this package has no runtime dependencies — but that key is the one people forget: the hook runs in its own isolated virtualenv and cannot see your project's installs, so every third-party import has to be listed there or `mypy` reports it as missing. |

```bash
pre-commit run --all-files
```

If a hook rewrites a file, the commit aborts and the fix is left in your working
tree. Re-stage, re-commit. That is the loop, not a failure.

### What `mypy --strict` actually forced

See `mypy.txt` for the clean run. The three changes it demanded, and the one
that was genuinely surprising:

1. **`-> None` on every function that returns nothing.** Mechanical.
   `--disallow-untyped-defs` is part of `strict`, and an unannotated function is
   invisible to the checker rather than merely unchecked.
2. **`cast` around `sqlite3`-style dynamic returns.** Not needed here, but the
   equivalent shows up in `parsing.py`: `re.Match.groupdict()` is typed
   `dict[str, str | Any]`, so `LogRecord(**match.groupdict())` type-checks only
   because `LogRecord`'s fields are `str` and `Any` is compatible with anything.
   That is `Any` doing you a favour, and it is worth knowing when it is.
3. **The surprise: `TypedDict(total=False)` changed what "optional" means.**
   `Summary` has `first_timestamp` only when `--timestamps` is passed. Modelling
   that as `total=False` makes `mypy` accept both `summary["first_timestamp"]`
   *and* `"top_errors" not in summary` — because `total=False` says "this key may
   be absent", not "this key is `T | None`". The two are different, and getting
   them mixed up is why `most_common_error` is declared `ErrorSummary | None`
   (always present, sometimes null) while `top_errors` is not (sometimes absent
   entirely). `mypy` will not tell you which one you meant; it will only hold you
   to whichever one you wrote.

## Where to read

1. `BEFORE_AFTER.md` — the three changes and why each one mattered.
2. `src/loganalyzer/models.py` — the shapes. Everything else depends on this.
3. `src/loganalyzer/parsing.py` — reading, and the "return `None`, do not raise" call.
4. `src/loganalyzer/analysis.py` — the pure layer. This is where the tests live.
5. `src/loganalyzer/reporting.py` — writing.
6. `src/loganalyzer/cli.py` — argv in, exit code out.
7. `tests/conftest.py` — the fixtures, and the scope reasoning.
8. `tests/test_analysis.py` — 25 tests, no I/O. The payoff, in one file.
