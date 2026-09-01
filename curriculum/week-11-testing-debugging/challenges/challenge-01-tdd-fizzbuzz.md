# Challenge 1 — TDD FizzBuzz

> **Topic:** Test-Driven Development — the red / green / refactor rhythm, one failing test at a time
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** FizzBuzz is trivial code, which is exactly the point — with the problem out of the way, the only thing left to practise is the *discipline*. TDD is a habit you build on something small so you have it on something large. It is also the single best cure for the classic FizzBuzz bug, and you will watch it steer you away from that bug without ever aiming.

## The Brief

For the numbers 1 to N, return a list of strings. A multiple of 3 is `"Fizz"`, a
multiple of 5 is `"Buzz"`, a multiple of both is `"FizzBuzz"`, and anything else
is just the number as a string. So `fizzbuzz(15)` ends `"13", "14", "FizzBuzz"`.

You already know how to write that. The challenge is to write it a particular
way: **test first, every time.** Test-Driven Development is a three-beat loop.

- **RED** — write one small test for behaviour you have not built yet. Run it.
  Watch it fail. A test you have never seen fail is a test you cannot trust.
- **GREEN** — write the *smallest* code that makes it pass. Not the clever
  version, not the finished version. The smallest.
- **REFACTOR** — with the bar green, tidy the code up. Because the tests still
  pass, you know you did not break anything.

Round and round, one behaviour per lap, until the whole thing is built. The
prize is not FizzBuzz; it is the muscle memory, and one specific lesson about
how the two rules combine that TDD teaches you almost by accident.

## Starter

Four files in a folder. You write `fizzbuzz.py` from empty, driven by
`test_fizzbuzz.py`, which you also grow one test at a time.

```text
challenge-01-tdd-fizzbuzz/
├── fizzbuzz.py         # starts empty; each line is demanded by a test
├── test_fizzbuzz.py    # grows one test at a time
├── pyproject.toml
└── README.md           # how to run + your TDD commit log + a reflection
```

Start `fizzbuzz.py` as an empty file, and `test_fizzbuzz.py` with only the
first test:

```python
"""test_fizzbuzz.py — one test at a time, each watched fail before it passes."""

from fizzbuzz import fizzbuzz


def test_returns_a_list() -> None:
    assert isinstance(fizzbuzz(1), list)
```

The suggested order of tests — not a script, but it leads to a clean design:

1. `test_returns_a_list` — `fizzbuzz(1)` returns a list.
2. `test_length_matches_n` — `fizzbuzz(5)` has length 5.
3. `test_plain_numbers` — `fizzbuzz(2) == ["1", "2"]`.
4. `test_three_is_fizz` — index 2 is `"Fizz"`.
5. `test_five_is_buzz` — index 4 is `"Buzz"`.
6. `test_fifteen_is_fizzbuzz` — index 14 is `"FizzBuzz"`.
7. `test_full_output_to_fifteen` — the whole 15-element list.
8. `test_zero_returns_empty_list` — the edge case.
9. `test_negative_raises_value_error` — negative `n` raises `ValueError`.

A minimal `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-ra -q"
testpaths = ["."]
```

## Requirements

1. **Tests come first.** Every commit message starts with `RED`, `GREEN`, or
   `REFACTOR`. At least **9 commits** in that cadence.
2. **Write only enough production code to make the current failing test pass.**
   No "while I'm here" additions.
3. After each `GREEN`, look for a refactor. If you find one, commit it `REFACTOR`
   — with the tests green before *and* after.
4. The final suite runs in **under one second**. Nothing touches a file, a
   socket, or the clock.
5. `README.md` carries: how to run, the commit log showing the rhythm, and one
   paragraph on whether TDD felt natural or fought you.

## Constraints

- **You may not write a test that already passes.** If you cannot describe the
  failure message a new test would produce, you have not done TDD — you have
  written code and then described it. Delete it and write one that fails first.
- **Resist the list comprehension until the simple tests pass.** The clean
  final shape is a comprehension over a small helper. Reaching for it on test 3
  skips the steps that teach the lesson.
- **Do not special-case fifteen.** When you get to `test_fifteen_is_fizzbuzz`,
  the temptation is `if n % 15`. Resist it — see the Common bugs section for why
  that road leads straight to the most famous bug in the exercise.
- **Keep the suite fast and pure.** A FizzBuzz test that reads a file or sleeps
  has missed the point twice over.

## Expected output

The shipped answer below folds `fizzbuzz.py`, the nine tests, and a driver into
one file so it runs as a plain script. It prints the finished output, then runs
the suite through pytest:

```text
$ python challenge-01-tdd-fizzbuzz-solution.py
fizzbuzz(15):
  ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']

The nine tests, run the way pytest runs them:
  PASS  test_returns_a_list
  PASS  test_length_matches_n
  PASS  test_plain_numbers
  PASS  test_three_is_fizz
  PASS  test_five_is_buzz
  PASS  test_fifteen_is_fizzbuzz
  PASS  test_full_output_to_fifteen
  PASS  test_zero_returns_empty_list
  PASS  test_negative_raises_value_error

9 passed, 0 failed
```

Doing it for real, you run `pytest` and see nine green dots — but only after you
have watched each of those tests go red first.

## Steps

1. Make the folder, a virtual environment, and `pip install pytest`.
2. Write `test_returns_a_list`. Run `pytest`. It fails with
   `ModuleNotFoundError: No module named 'fizzbuzz'` — that is your first RED.
   Commit it.
3. Make it pass with the smallest thing that works: `def fizzbuzz(n): return []`.
   Commit GREEN.
4. Add `test_length_matches_n` (RED), then `return ["1"] * n` (GREEN). Yes, that
   is deliberately wrong. It is also the smallest thing that passes, and the
   next test is what forces it to become right.
5. Keep going down the list. After each GREEN, ask whether the code wants a
   REFACTOR; the extraction of `_label` is the natural one.
6. At `test_fifteen_is_fizzbuzz`, notice you do **not** need a `% 15` case — two
   independent `if`s that append to a string already produce `"FizzBuzz"`.
7. Finish with the `0` and negative edge cases. Write the reflection paragraph
   while the session is fresh.

## The Solution

```python
"""challenge-01-tdd-fizzbuzz-solution.py — FizzBuzz grown one failing test at a time.

The point of this challenge is not FizzBuzz — it is the rhythm: write a failing
test (RED), write the smallest code that passes it (GREEN), tidy up while the
bar stays green (REFACTOR). Nothing in ``fizzbuzz`` below was written before a
test demanded it. See the exercise page for the full commit log.

You would normally keep ``fizzbuzz.py`` and ``test_fizzbuzz.py`` in two files
and run ``pytest``. A published answer is run as a plain script, so this one
file carries the module, the nine tests, and a ``main()`` that drives pytest
itself and prints a plain, same-every-time report.

Run it with::

    python challenge-01-tdd-fizzbuzz-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# fizzbuzz.py — every line here was demanded by one of the tests below
# --------------------------------------------------------------------------- #


def fizzbuzz(n: int) -> list[str]:
    """Return the FizzBuzz sequence for the numbers 1..n inclusive.

    ``0`` produces an empty list. A negative ``n`` is a caller bug, not an empty
    request, so it raises ``ValueError``.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    return [_label(number) for number in range(1, n + 1)]


def _label(number: int) -> str:
    """Return the FizzBuzz label for a single number."""
    label = ""
    if number % 3 == 0:
        label += "Fizz"
    if number % 5 == 0:
        label += "Buzz"
    return label or str(number)


# --------------------------------------------------------------------------- #
# test_fizzbuzz.py — the nine tests, in the order they were written
# --------------------------------------------------------------------------- #


def test_returns_a_list() -> None:
    assert isinstance(fizzbuzz(1), list)


def test_length_matches_n() -> None:
    assert len(fizzbuzz(5)) == 5


def test_plain_numbers() -> None:
    assert fizzbuzz(2) == ["1", "2"]


def test_three_is_fizz() -> None:
    assert fizzbuzz(3)[2] == "Fizz"


def test_five_is_buzz() -> None:
    assert fizzbuzz(5)[4] == "Buzz"


def test_fifteen_is_fizzbuzz() -> None:
    assert fizzbuzz(15)[14] == "FizzBuzz"


def test_full_output_to_fifteen() -> None:
    assert fizzbuzz(15) == [
        "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz",
        "Buzz", "11", "Fizz", "13", "14", "FizzBuzz",
    ]


def test_zero_returns_empty_list() -> None:
    assert fizzbuzz(0) == []


def test_negative_raises_value_error() -> None:
    with pytest.raises(ValueError, match="must be non-negative"):
        fizzbuzz(-1)


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes."""
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Show the finished output, then run the suite and print the outcomes."""
    print("fizzbuzz(15):")
    print(f"  {fizzbuzz(15)}")

    print()
    print("The nine tests, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
```

**The two-`if` accumulator is the whole point.** Every FizzBuzz has to answer one
question: how do the "divisible by 3" and "divisible by 5" rules *combine*? The
naive answer invents a third rule (`% 15`) to paper over the interaction. The
better answer notices there is no third rule at all — `"FizzBuzz"` is simply what
happens when both of the first two fire. `label = ""`, then two independent
`if`s that append, derives that instead of hard-coding it. TDD does not hand you
this shape, but it makes the wrong shape impossible to keep: `test_three_is_fizz`
and `test_five_is_buzz` are already green when you write
`test_fifteen_is_fizzbuzz`, so any change that breaks them is visibly a step
backwards. The accumulator is the cheapest change that keeps all three green.

**`return label or str(number)` leans on truthiness.** An empty string is falsy,
so an empty label means no rule fired and the number is its own label. It reads
as one line of English and it is exactly what a trailing `if not label:` would
have done, minus the extra line.

**`_label` is private and separate because the responsibilities are.**
`fizzbuzz` owns the range and the guard clause; `_label` owns the rules for one
number. That split is the REFACTOR step — done with the tests green before and
after, which is the only time refactoring is safe.

**`n < 0` raises rather than returning `[]`.** `fizzbuzz(-1)` is a caller bug;
`fizzbuzz(0)` is a valid empty request. Collapsing them would hide a typo like
`fizzbuzz(count - 1)` when `count` is `0`.

**The driver is only here because this is a download.** `run_suite()` calls
`pytest.main([__file__])` — the same engine as the `pytest` command — and the
`_Collector` plugin records each result so the printed report never drifts. In
your own folder you just type `pytest`.

## Download and run

Download
[challenge-01-tdd-fizzbuzz-solution.py](./challenge-01-tdd-fizzbuzz-solution.py)
and run it:

```bash
python challenge-01-tdd-fizzbuzz-solution.py
```

It needs `pytest` and nothing else. Your own deliverable is the two separate
files plus a `README.md` with the commit log — the download is the destination,
not the journey, and the journey is the graded part.

The `-solution` in the filename keeps this file from colliding with your own
`fizzbuzz.py` and `test_fizzbuzz.py`.

## Common bugs to catch

- **The unreachable `elif` — the classic FizzBuzz bug.** Written in spec order,
  `if n % 3 / elif n % 5 / elif n % 15`, the `% 15` arm can never run: 15 is
  divisible by 3, so the first arm always wins and `fizzbuzz(15)[14]` is
  `"Fizz"`. `test_fifteen_is_fizzbuzz` catches it, and the failure even names
  the guilty branch — you got `"Fizz"`, not `"Buzz"` and not the number:

  ```text
  $ pytest test_fizzbuzz.py -q
  F                                                                        [100%]
  ================================== FAILURES ===================================
  __________________________ test_fifteen_is_fizzbuzz ___________________________

      def test_fifteen_is_fizzbuzz():
  >       assert fizzbuzz(15)[14] == "FizzBuzz"
  E       AssertionError: assert 'Fizz' == 'FizzBuzz'
  E
  E         - FizzBuzz
  E         + Fizz

  test_fizzbuzz.py:3: AssertionError
  ```

- **Off by one in the range.** `range(n)` instead of `range(1, n + 1)` gives
  `["Fizz", "1", ...]`, because 0 is divisible by 3. `test_plain_numbers`
  catches it — which is exactly the test that step 4's silly `["1"] * n` forced
  into existence.
- **Writing tests that were never red.** Write all nine tests, then the
  implementation, and you have written tests but not done TDD — the log will
  show one lonely `GREEN` at the end. The tell is a test you cannot make fail.
- **A full-list assertion as your *first* test.** `fizzbuzz(15) == [...]` fails
  for fifteen reasons at once and the diff is fifteen lines wide. Big-bang
  assertions are a fine regression net and a useless driver. Drive with the
  narrowest assertion that can only fail one way.

## Under the hood

<details>
<summary>Under the hood — the commit log, and the one place TDD earns its keep</summary>

The reference implementation produced eighteen commits. The rhythm, with the
failure each RED actually produced:

| # | Commit | What changed |
|---|---|---|
| 1 | `RED: fizzbuzz returns a list` | Fails `ModuleNotFoundError: No module named 'fizzbuzz'`. |
| 2 | `GREEN: return an empty list` | `def fizzbuzz(n): return []`. Nothing more. |
| 3 | `RED: length matches n` | `assert 0 == 5`. |
| 4 | `GREEN: return n placeholder entries` | `return ["1"] * n`. Deliberately wrong, deliberately minimal. |
| 5 | `RED: plain numbers are stringified` | `assert ['1', '1'] == ['1', '2']`. |
| 6 | `GREEN: stringify the range` | `return [str(i) for i in range(1, n + 1)]`. |
| 7–10 | `RED`/`GREEN` for Fizz, then Buzz | one inline conditional each. |
| 11 | `REFACTOR: extract _label` | the comprehension was getting unreadable; move the rules into a helper, tests green throughout. |
| 12 | `RED: fifteen is FizzBuzz` | drives the two-`if` accumulator. |
| 13 | `GREEN: concatenate the labels` | two independent `if`s — no `% 15` case. |
| 14 | `REFACTOR: label or str(number)` | replace `if not label` with `return label or str(number)`. |
| 15–16 | `RED` for the full list, then `0` | both passed immediately; kept as a regression net and labelled honestly. |
| 17–18 | `RED`/`GREEN` for the negative guard | three-line guard at the top. |

Two of those RED commits (15 and 16) went green with no production change. The
honest thing is to label them so, because they pin the *combined* behaviour that
the individual rule tests only pin in pieces. And the one place the discipline
actually fought back:

> TDD fought me exactly once, at step 12. The instinct was to reach straight for
> `if number % 15 == 0` — and that instinct is where the classic FizzBuzz bug
> lives. Because `test_three_is_fizz` and `test_five_is_buzz` were already green
> and had to *stay* green, the cheapest thing that satisfied all three at once
> was two independent `if`s appending to a string. The suite pushed me to the
> better design; I did not think my way there. Writing `return ["1"] * n` on
> purpose felt absurd — and it is — but it forced `test_plain_numbers` into
> existence, and that is the test that would catch an off-by-one in `range` two
> months from now. The discipline is not about the code you write; it is about
> the tests you would otherwise have skipped.

</details>

## Acceptance checklist

- [ ] At least nine commits in `RED` → `GREEN` → `REFACTOR` order in `git log`.
- [ ] Every line of `fizzbuzz.py` was demanded by a test you watched fail.
- [ ] No `% 15` special case anywhere.
- [ ] All nine tests pass, and the suite runs in under a second.
- [ ] `README.md` has the commit log and a reflection paragraph.

## Stretch

- Add `ruff` and `black` to your `pyproject.toml` and get both clean. The
  reference `test_full_output_to_fifteen` is written one element per line because
  that is what `black` does to a long list literal.
- Add a tenth test for a large `n` (say 100) and assert only the `FizzBuzz`
  positions. Watch it pass with no production change — a regression net, not a
  driver.
- Rewrite `_label` as a table of `(divisor, word)` pairs and loop over it. Keep
  every test green through the change; that is a REFACTOR, and the tests are
  what make it safe.

When your nine are green, take the rhythm to a whole application:
[Challenge 2 — Integration tests for the Week 9 Flask blog](./challenge-02-flask-api-tests.md).
