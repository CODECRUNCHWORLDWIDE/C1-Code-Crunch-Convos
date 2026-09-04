# Exercise 2 — Sharing Setup With Fixtures

> **Topic:** `@pytest.fixture`, fixture arguments, `yield` teardown, and the built-in `tmp_path`
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md) (section 7)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** the moment you have more than two tests that need the same sample data, you either copy-paste it or you learn fixtures. Copy-paste rots: you fix the data in four tests and miss the fifth. Fixtures also give you the only clean way to hand a test a real file without leaving junk on disk, which is what the mini-project and both challenges need on Friday.

## The Brief

The tool library keeps its loan roster in a CSV that the volunteer at the front
desk exports every morning. Two things need testing: the loader that turns that
CSV into Python objects, and the filter that answers "what is overdue right
now?"

Both need sample data. Think of a fixture as a recipe pytest re-cooks fresh for
every test: ask for `loans` and you get a brand-new list of four loans; ask for
`roster_csv` and you get a real file written to a scratch folder, then thrown
away when the test ends. Because it is re-cooked each time, one test cannot
spoil the ingredients for the next.

There is a trap in the data, and it is the trap every date filter falls into.
One item is due *today*. Due today is not overdue — the member has until closing
time. If your filter uses `<=` instead of `<`, you bill someone a late fee on
the day they were supposed to return the ladder.

## Starter

The module under test, already written:

```python
"""roster.py — reading and filtering the tool library's loan roster."""

import csv
from datetime import date
from pathlib import Path
from typing import Any

Loan = dict[str, Any]


def load_loans(path: Path) -> list[Loan]:
    """Read a loan roster CSV into a list of loan records.

    The file has three columns: ``item``, ``borrower``, ``due``.
    The ``due`` column is parsed from ISO format into a ``date``.
    """
    loans: list[Loan] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            loans.append(
                {
                    "item": row["item"],
                    "borrower": row["borrower"],
                    "due": date.fromisoformat(row["due"]),
                }
            )
    return loans


def overdue_items(loans: list[Loan], today: date) -> list[str]:
    """Return the names of items due strictly before ``today``, sorted A-Z."""
    return sorted(loan["item"] for loan in loans if loan["due"] < today)
```

The test file you are here to write:

```python
"""test_roster.py — fixture-driven tests for the loan roster."""

from datetime import date
from pathlib import Path

import pytest

from roster import Loan, load_loans, overdue_items

TODAY = date(2026, 3, 10)


@pytest.fixture
def loans() -> list[Loan]:
    """Four loans: two overdue, one due today, one due next week."""
    # TODO: return a list of four dicts with keys item, borrower, due.
    #       circular saw   / Ada   / 2026-03-01
    #       hedge trimmer  / Linus / 2026-03-09
    #       ladder         / Grace / 2026-03-10
    #       pressure washer/ Ada   / 2026-03-15


@pytest.fixture
def roster_csv(tmp_path: Path) -> Path:
    """Write the same four loans to a real CSV and yield its path."""
    path = tmp_path / "roster.csv"
    # TODO: write a header row "item,borrower,due" plus the four data rows
    yield path
    # TODO: delete the file, then assert it is gone


def test_overdue_items_are_sorted_alphabetically(loans: list[Loan]) -> None:
    # TODO: overdue_items(loans, TODAY) == ["circular saw", "hedge trimmer"]


def test_due_today_is_not_overdue(loans: list[Loan]) -> None:
    # TODO: assert "ladder" is not in the result


def test_nothing_overdue_returns_empty_list(loans: list[Loan]) -> None:
    # TODO: call with date(2026, 2, 1) and assert the result == []


def test_mutating_the_fixture_does_not_leak_part_one(loans: list[Loan]) -> None:
    # TODO: pop one loan, then assert len(loans) == 3


def test_mutating_the_fixture_does_not_leak_part_two(loans: list[Loan]) -> None:
    # TODO: assert len(loans) == 4 — proof the fixture was rebuilt


def test_load_loans_reads_every_row(roster_csv: Path) -> None:
    # TODO: assert len(load_loans(roster_csv)) == 4


def test_load_loans_parses_the_due_date(roster_csv: Path) -> None:
    # TODO: assert the first record's "due" == date(2026, 3, 1)
```

## Requirements

1. Both fixtures carry `@pytest.fixture` and are named exactly `loans` and
   `roster_csv`. The name is the wiring — a test asks for a fixture by writing
   its name as a parameter.
2. `loans` **returns** its list. `roster_csv` **yields** its path, then cleans
   up after the `yield`.
3. `roster_csv` takes `tmp_path` as a parameter. Do not build a path by hand.
4. The overdue result is `["circular saw", "hedge trimmer"]` — exactly that
   list, exactly that order.
5. `test_nothing_overdue_returns_empty_list` asserts `== []`, not
   `assert not result`. An empty list and `None` are both falsy; only one is
   correct.
6. Both `..._part_one` and `..._part_two` pass. Together they prove the default
   fixture scope rebuilds the data for every test.
7. All seven tests pass with `pytest -v`.

## Constraints

- **Take `tmp_path`, do not write to the current directory.** A test that writes
  `roster.csv` next to your source files leaves it behind, and the next run
  reads stale data and passes for the wrong reason. `tmp_path` hands every test
  a fresh directory and deletes it afterwards.
- **`loans` returns; `roster_csv` yields.** Use `yield` only when there is
  teardown to do. A `yield` fixture with nothing after the `yield` is a `return`
  fixture in a costume, and it sends the next reader hunting for cleanup that is
  not there.
- **Leave both fixtures at the default `function` scope.** `scope="module"`
  would build the list once and share it, so the test that pops an item would
  break the one after it. Cross-test leakage is the most expensive kind of test
  bug, because the failure lands on an innocent test.
- **The teardown in `roster_csv` is deliberately redundant.** `tmp_path` cleans
  itself. You write the cleanup anyway because the shape is what you need the
  day a fixture creates something pytest does not own — a database row, a queue
  entry, a directory outside `tmp_path`.
- **Use a fixed `TODAY` constant, never `date.today()`.** A test that calls
  `date.today()` gives a different answer tomorrow, and a test that changes its
  mind overnight gets deleted by whoever is on call.

## Expected output

The shipped answer below folds `roster.py`, the seven tests, and a driver into
one file so it runs as a plain script. It prints what the filter returns, then
runs the suite through pytest and reports each test:

```text
$ python exercise-02-fixtures.py
Today is 2026-03-10. Overdue means due strictly before that.
  overdue right now : ['circular saw', 'hedge trimmer']
  the ladder is due today, so it is NOT overdue: True

The seven tests, run the way pytest runs them:
  PASS  test_overdue_items_are_sorted_alphabetically
  PASS  test_due_today_is_not_overdue
  PASS  test_nothing_overdue_returns_empty_list
  PASS  test_mutating_the_fixture_does_not_leak_part_one
  PASS  test_mutating_the_fixture_does_not_leak_part_two
  PASS  test_load_loans_reads_every_row
  PASS  test_load_loans_parses_the_due_date

7 passed, 0 failed
```

Doing it for real, you run `pytest -v` and see seven `PASSED` lines instead.

## Steps

1. Save `roster.py` and `test_roster.py` in your Week 11 folder.
2. Fill in the `loans` fixture first. Run
   `pytest -v -k "sorted or today or nothing"` — the three tests that use it
   should run and pass.
3. Fill in the two mutation tests and rerun. If `part_two` fails with
   `assert 3 == 4`, your fixture is caching instead of rebuilding.
4. Fill in `roster_csv`: header row plus four data rows, via
   `path.write_text(...)` or a `csv.DictWriter`. Then the teardown —
   `path.unlink()` and `assert not path.exists()`.
5. Fill in the last two tests and run `pytest -v`. Seven passed.
6. Run `pytest -q --setup-show test_roster.py::test_load_loans_reads_every_row`
   and read the SETUP/TEARDOWN lines wrapped around your test.
7. Temporarily change `roster.py` to use `<=` instead of `<`. Confirm
   `test_due_today_is_not_overdue` goes red, then change it back.

## The Solution

```python
"""exercise-02-fixtures-solution.py — fixture-driven tests, proven headless.

Normally you keep ``roster.py`` and ``test_roster.py`` in two files and run
``pytest``. A published answer is run as a plain script instead, so this one
file carries the module, the tests, and a small ``main()`` that drives pytest
itself and prints a plain, same-every-time report.

The two fixtures are the point of the exercise. ``loans`` is a *factory* —
pytest calls it again for every test, so one test cannot damage the next.
``roster_csv`` writes a real file into pytest's throwaway ``tmp_path`` directory,
hands the test its path, and then cleans it up after the ``yield``.

Run it with::

    python exercise-02-fixtures-solution.py
"""

from __future__ import annotations

import contextlib
import csv
import io
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Any

import pytest

# --------------------------------------------------------------------------- #
# roster.py — the module under test, given complete
# --------------------------------------------------------------------------- #

Loan = dict[str, Any]


def load_loans(path: Path) -> list[Loan]:
    """Read a loan roster CSV into a list of loan records.

    The file has three columns: ``item``, ``borrower``, ``due``. The ``due``
    column is parsed from ISO format (``YYYY-MM-DD``) into a ``date``.
    """
    loans: list[Loan] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            loans.append(
                {
                    "item": row["item"],
                    "borrower": row["borrower"],
                    "due": date.fromisoformat(row["due"]),
                }
            )
    return loans


def overdue_items(loans: list[Loan], today: date) -> list[str]:
    """Return the names of items due strictly before ``today``, sorted A-Z."""
    return sorted(loan["item"] for loan in loans if loan["due"] < today)


# --------------------------------------------------------------------------- #
# test_roster.py — the seven fixture-driven tests
# --------------------------------------------------------------------------- #

TODAY = date(2026, 3, 10)

ROSTER_ROWS: tuple[tuple[str, str, str], ...] = (
    ("circular saw", "Ada", "2026-03-01"),
    ("hedge trimmer", "Linus", "2026-03-09"),
    ("ladder", "Grace", "2026-03-10"),
    ("pressure washer", "Ada", "2026-03-15"),
)


@pytest.fixture
def loans() -> list[Loan]:
    """Four loans: two overdue, one due today, one due next week."""
    return [
        {"item": item, "borrower": borrower, "due": date.fromisoformat(due)}
        for item, borrower, due in ROSTER_ROWS
    ]


@pytest.fixture
def roster_csv(tmp_path: Path) -> Iterator[Path]:
    """Write the same four loans to a real CSV and yield its path."""
    path = tmp_path / "roster.csv"
    rows = ["item,borrower,due"]
    rows.extend(",".join(row) for row in ROSTER_ROWS)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    yield path
    path.unlink()
    assert not path.exists()


def test_overdue_items_are_sorted_alphabetically(loans: list[Loan]) -> None:
    """Both genuinely late items come back, in alphabetical order."""
    assert overdue_items(loans, TODAY) == ["circular saw", "hedge trimmer"]


def test_due_today_is_not_overdue(loans: list[Loan]) -> None:
    """An item due today has until closing time, so it is not late yet."""
    assert "ladder" not in overdue_items(loans, TODAY)


def test_nothing_overdue_returns_empty_list(loans: list[Loan]) -> None:
    """Before every due date the answer is an empty list, not None."""
    assert overdue_items(loans, date(2026, 2, 1)) == []


def test_mutating_the_fixture_does_not_leak_part_one(loans: list[Loan]) -> None:
    """Damage the fixture data on purpose."""
    loans.pop()
    assert len(loans) == 3


def test_mutating_the_fixture_does_not_leak_part_two(loans: list[Loan]) -> None:
    """The damage did not survive: this test gets all four loans back."""
    assert len(loans) == 4


def test_load_loans_reads_every_row(roster_csv: Path) -> None:
    """Four data rows become four records; the header becomes none."""
    assert len(load_loans(roster_csv)) == 4


def test_load_loans_parses_the_due_date(roster_csv: Path) -> None:
    """The due column arrives as a date object, not as a string."""
    assert load_loans(roster_csv)[0]["due"] == date(2026, 3, 1)


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
    """Show what the filter returns, then run the suite and print outcomes."""
    sample = [
        {"item": item, "borrower": borrower, "due": date.fromisoformat(due)}
        for item, borrower, due in ROSTER_ROWS
    ]
    print(f"Today is {TODAY.isoformat()}. Overdue means due strictly before that.")
    print(f"  overdue right now : {overdue_items(sample, TODAY)}")
    print("  the ladder is due today, so it is NOT overdue: "
          f"{'ladder' not in overdue_items(sample, TODAY)}")

    print()
    print("The seven tests, run the way pytest runs them:")
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

**One table, two fixtures.** `ROSTER_ROWS` holds the four loans once, as plain
strings, and both fixtures build from it. If `loans` typed its dates out and
`roster_csv` typed the same dates out again, that would be two copies waiting to
drift apart. From one table, a fifth loan is one row and the two fixtures cannot
disagree about it.

**The `loans` fixture builds new dictionaries every call, and that is load
bearing.** Write the list once at module level and `return` it, and here is what
happens: `part_one` pops an item from that shared list, `part_two` asks for four
and finds three, and the run goes red on a test that did nothing wrong. The
comprehension inside the fixture body gives every test its own list *and* its
own dicts. A fixture is a recipe pytest re-runs, not a value it hands around —
and the two mutation tests exist purely to make that claim checkable.

**`return` for `loans`, `yield` for `roster_csv`.** `yield` exists to let you
run code *after* the test. `loans` has nothing to clean up, so a `yield` there
would promise a teardown that never arrives. `roster_csv` has a real file, so it
yields, then deletes, then asserts the deletion happened. That final `assert`
inside a fixture is unusual and deliberate: a broken teardown then fails loudly
instead of leaving debris for the next run to trip over.

**`tmp_path` instead of a hand-built path.** A test that writes `roster.csv`
next to your source leaves it there, and the next run reads that stale file. If
you later break the fixture's writing code, the test keeps passing on
yesterday's data. `tmp_path` gives every test a fresh, uniquely named directory,
so "the file exists" and "my fixture wrote it" cannot come apart.

**`Iterator[Path]`, not `Path`, on a `yield` fixture.** A function containing
`yield` is a generator, so it does not return a `Path`; it returns something you
iterate. pytest does not care, but a type checker does, and the whole argument of
this week is that the tools should agree with each other.

**`< today`, and a fixture row that proves it.** The ladder is due on the tenth
and `TODAY` is the tenth, so it must not appear. That single row is the whole
difference: with only the saw and the trimmer in the data, `<` and `<=` behave
identically and the off-by-one ships. Choosing input that can tell two plausible
implementations apart is most of the skill in writing tests.

## Run it

Copy the worked answer on this page into `exercise-02-fixtures.py` and run it:

```bash
python exercise-02-fixtures.py
```

It needs `pytest` and nothing else. Your own work is `roster.py` plus
`test_roster.py`, run with `pytest -v`.

The `-solution` in the filename keeps this file from colliding with your own
`roster.py` and `test_roster.py`.

## Common bugs to catch

- **`fixture 'loan' not found`, followed by a list of available fixtures.** You
  defined `loans` but asked for `loan`, or the two live in different files with
  no `conftest.py`. The names must match exactly.
- **`TypeError: object of type 'NoneType' has no len()`.** Your `loans` fixture
  builds the list but has no `return` in front of it, so pytest injected `None`.
  A fixture is a function, and a function that falls off the end returns `None`.
- **`AssertionError: assert 3 == 4` in `part_two`.** You added `scope="module"`
  or `scope="session"` to `loans`. Remove it — the default scope is what keeps
  each test independent, and the failure landing on the *innocent* second test
  is exactly why shared state is so expensive.
- **`ValueError: Invalid isoformat string: '03/01/2026'`.** Your CSV rows use
  US-style dates. `date.fromisoformat` wants `YYYY-MM-DD` and nothing else.
- **`KeyError: 'item'`.** You left the header line out of the CSV, so
  `csv.DictReader` treated your first loan as the column names. Row one must be
  `item,borrower,due`.
- **The overdue result contains `'ladder'`.** Either your fixture gave the
  ladder a due date before the 10th, or `roster.py` is using `<=`. With `<=`,
  two tests catch it at once — the equality test names the extra item for you:

  ```text
  E       AssertionError: assert ['circular sa...er', 'ladder'] == ['circular sa...edge trimmer']
  E
  E         Left contains one more item: 'ladder'
  ```

## Under the hood

<details>
<summary>Under the hood — watching a fixture chain set up and tear down</summary>

`--setup-show` prints the setup and teardown around each test, so you can watch
pytest resolve a fixture chain:

```text
$ pytest -q --setup-show test_roster.py::test_load_loans_reads_every_row

SETUP    S tmp_path_factory
        SETUP    F tmp_path (fixtures used: tmp_path_factory)
        SETUP    F roster_csv (fixtures used: tmp_path)
        test_roster.py::test_load_loans_reads_every_row (fixtures used: request, roster_csv, tmp_path, tmp_path_factory).
        TEARDOWN F roster_csv
        TEARDOWN F tmp_path
TEARDOWN S tmp_path_factory
1 passed in 0.06s
```

The letter is the scope: `F` for function, `S` for session. You asked for one
fixture, `roster_csv`, and pytest resolved a chain of three — `roster_csv`
pulled in `tmp_path`, which pulled in `tmp_path_factory` — setting them up in
order and tearing them down in reverse. (pytest 9 also lists `request` among the
fixtures used and indents the function-scoped lines; pytest 8 did neither. The
structure is identical.)

</details>

## Acceptance checklist

- [ ] Both fixtures carry the `@pytest.fixture` decorator.
- [ ] `roster_csv` takes `tmp_path` and never writes to the working directory.
- [ ] `roster_csv` yields, then deletes the file and asserts it is gone.
- [ ] Both mutation tests pass, proving per-test fixture rebuild.
- [ ] `pytest -v` reports 7 passed.
- [ ] `--setup-show` shows `roster_csv` pulling in `tmp_path`.
- [ ] Committed with a message like
      `Add Week 11 exercise 2: fixtures for the loan roster`.

## Stretch

- Move the `loans` fixture into a `conftest.py` next to your test file and
  delete it from `test_roster.py`. Nothing else changes — that is how fixtures
  get shared across many test files.
- Add a `scope="module"` fixture that builds ten thousand loans and time the
  suite with `pytest --durations=5` before and after. Feel the trade.
- Make `load_loans` print a warning on a blank `borrower` field, then assert on
  `capsys.readouterr().out` in a new test.

When all seven are green, move on to
[Exercise 3 — Table-Driven Tests With Parametrize](./exercise-03-parametrize.md).
