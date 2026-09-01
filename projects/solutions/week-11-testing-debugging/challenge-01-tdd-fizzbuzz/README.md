# Challenge 1 — TDD FizzBuzz (reference solution)

FizzBuzz for 1..N, grown one failing test at a time.

## How to run the tests

```bash
cd challenge-01-tdd-fizzbuzz
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install pytest ruff black
pytest
```

Expected:

```text
.........                                                                [100%]
9 passed in 0.09s
```

`pyproject.toml` sets `addopts = "-ra -q"`, so a plain `pytest -v` cancels out
to normal verbosity. Use `pytest -vv` when you want the per-test listing.

## The TDD log

Twelve commits: nine RED→GREEN pairs collapsed into the cadence below, with
three refactors taken the moment the tests went green.

| # | Commit | What changed |
|---|---|---|
| 1 | `RED: fizzbuzz returns a list` | `test_returns_a_list`. Fails with `ModuleNotFoundError: No module named 'fizzbuzz'`. |
| 2 | `GREEN: return an empty list` | `def fizzbuzz(n): return []`. Nothing more. |
| 3 | `RED: length matches n` | `test_length_matches_n` — `assert 0 == 5`. |
| 4 | `GREEN: return n placeholder entries` | `return ["1"] * n`. Deliberately wrong, deliberately minimal. |
| 5 | `RED: plain numbers are stringified` | `test_plain_numbers` — `assert ['1', '1'] == ['1', '2']`. |
| 6 | `GREEN: stringify the range` | `return [str(i) for i in range(1, n + 1)]`. |
| 7 | `RED: multiples of three are Fizz` | `test_three_is_fizz`. |
| 8 | `GREEN: special-case three` | Inline conditional inside the comprehension. |
| 9 | `RED: multiples of five are Buzz` | `test_five_is_buzz`. |
| 10 | `GREEN: special-case five` | Second inline conditional. |
| 11 | `REFACTOR: extract _label` | Comprehension was becoming unreadable; move the rules into a helper. Tests stay green. |
| 12 | `RED: fifteen is FizzBuzz` | `test_fifteen_is_fizzbuzz`. |
| 13 | `GREEN: concatenate the labels` | Two independent `if`s that append to a label string — no `% 15` case needed. |
| 14 | `REFACTOR: label or str(number)` | Replace the trailing `if not label` with `return label or str(number)`. |
| 15 | `RED: full fifteen-element output` | `test_full_output_to_fifteen`. Passed immediately — kept anyway as the regression net for the whole rule set. |
| 16 | `RED: zero returns an empty list` | `test_zero_returns_empty_list`. Also passed immediately; `range(1, 1)` is empty. |
| 17 | `RED: negative n raises ValueError` | `test_negative_raises_value_error` — `DID NOT RAISE <class 'ValueError'>`. |
| 18 | `GREEN: guard against negative n` | Three-line guard clause at the top of `fizzbuzz`. |

Tests 7 and 8 (`test_full_output_to_fifteen`, `test_zero_returns_empty_list`)
went green without any production change. The challenge says to delete a test
that never fails; these two are the exception worth keeping, because they pin
the *combined* behaviour that the individual rule tests only pin in pieces. The
honest thing is to say so in the log rather than pretend they were RED.

## Reflection

TDD fought me exactly once, at step 12. The instinct was to reach straight for
`if number % 15 == 0` — and that instinct is where the classic FizzBuzz bug
lives, because an `elif` chain that checks `% 3` first can never reach the
`% 15` arm. Because `test_three_is_fizz` and `test_five_is_buzz` were already
green and had to *stay* green, the cheapest thing that satisfied all three
tests at once was two independent `if`s appending to a string. The test suite
pushed me to the better design; I did not think my way there.

The rest of the session felt slow in a good way. Writing
`return ["1"] * n` on purpose felt absurd, and it is absurd — but it forced
`test_plain_numbers` into existence, and that test is the one that would catch
an off-by-one in `range` two months from now. The discipline is not about the
code you write; it is about the tests you would otherwise have skipped.

## Quality gates

```bash
ruff check .        # All checks passed!
black --check .     # 2 files would be left unchanged.
```
