# Homework Problem 2 — Dues ledger

> **Topic:** fixtures over a real CSV — `@pytest.fixture`, `yield` teardown, `tmp_path`
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md) (section 7)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** the moment two tests need the same sample data, you either learn fixtures or you copy-paste it and the copies rot; this problem makes you build both a plain list fixture and a real-file fixture, which is exactly the pair the mini-project needs.

## The Brief

The neighborhood tool library keeps a little money ledger. Every member pays
dues to help buy new drills and ladders. Some members are behind. The library
tracks how far behind each one is in a CSV — one row per member, with how much
they owe.

Two small pieces of code need testing. The first is the **loader**: it opens the
CSV and turns each row into a tidy Python record. The second is the **filter**:
you hand it all the records and a number, the threshold, and it names everyone
who is "in arrears." In arrears means owing **more** than the threshold —
strictly more. A member who owes *exactly* the threshold is caught up enough;
they are **not** in arrears. That one word, "more," is the whole trap in this
problem.

Both pieces need sample data to test against. Rather than type the same four
members into every test, you write a **fixture**. Think of a fixture as a recipe
pytest re-cooks fresh for each test. Ask for `dues` and pytest cooks you a
brand-new list of members. Ask for `dues_csv` and pytest writes a real little
file, hands you the path, and sweeps the file away when the test is done. Because
the recipe is re-cooked every time, one test can never spoil the ingredients for
the next.

## Starter

The module under test, already written for you. This is `ledger.py` — do not
change it:

```python
"""ledger.py — reading and filtering the tool library's dues ledger."""

import csv
from pathlib import Path
from typing import Any

Dues = dict[str, Any]


def load_dues(path: Path) -> list[Dues]:
    """Read a dues CSV (columns: ``member``, ``owed_cents``) into records.

    ``owed_cents`` is parsed from text into an int, so callers never do
    arithmetic on strings.
    """
    dues: list[Dues] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            dues.append({"member": row["member"], "owed_cents": int(row["owed_cents"])})
    return dues


def members_in_arrears(dues: list[Dues], threshold_cents: int) -> list[str]:
    """Names of members owing strictly more than ``threshold_cents``, sorted A-Z."""
    return sorted(row["member"] for row in dues if row["owed_cents"] > threshold_cents)
```

The test file you are here to write. This is `test_ledger.py` — fill in every
`# TODO:`:

```python
"""test_ledger.py — fixture-driven tests for the dues ledger."""

from pathlib import Path

import pytest

from ledger import Dues, load_dues, members_in_arrears

THRESHOLD = 500


@pytest.fixture
def dues() -> list[Dues]:
    """Four members: two over the threshold, one exactly on it, one clear."""
    # TODO: return a list of four dicts with keys member, owed_cents.
    #       Ada      / 1200
    #       Grace    / 500
    #       Linus    / 0
    #       Yukihiro / 750


@pytest.fixture
def dues_csv(tmp_path: Path):
    """Write the same four members to a real CSV and yield its path."""
    path = tmp_path / "dues.csv"
    # TODO: write a header row "member,owed_cents" plus the four data rows
    yield path
    # TODO: delete the file, then assert it is gone


def test_arrears_are_sorted_alphabetically(dues: list[Dues]) -> None:
    # TODO: assert members_in_arrears(dues, THRESHOLD) == ["Ada", "Yukihiro"]


def test_exactly_on_the_threshold_is_not_in_arrears(dues: list[Dues]) -> None:
    # TODO: assert "Grace" is not in the result at THRESHOLD


def test_nobody_over_a_high_threshold_returns_empty_list(dues: list[Dues]) -> None:
    # TODO: call with a huge threshold and assert the result == []


def test_mutation_does_not_leak_part_one(dues: list[Dues]) -> None:
    # TODO: pop one member, then assert len(dues) == 3


def test_mutation_does_not_leak_part_two(dues: list[Dues]) -> None:
    # TODO: assert len(dues) == 4 — proof the fixture was rebuilt


def test_load_dues_reads_every_row(dues_csv: Path) -> None:
    # TODO: assert len(load_dues(dues_csv)) == 4


def test_load_dues_parses_amount_as_int(dues_csv: Path) -> None:
    # TODO: assert the first record's "owed_cents" == 1200 (an int, not "1200")
```

## Requirements

1. Both fixtures carry `@pytest.fixture` and are named exactly `dues` and
   `dues_csv`. The name is the wiring — a test asks for a fixture by writing its
   name as a parameter.
2. `dues` **returns** its list. `dues_csv` **yields** its path, then cleans up
   after the `yield` by deleting the file and asserting it is gone.
3. `dues_csv` takes `tmp_path` as a parameter. Do not build a path by hand.
4. The arrears result is `["Ada", "Yukihiro"]` — exactly that list, exactly that
   order.
5. `test_nobody_over_a_high_threshold_returns_empty_list` asserts `== []`, not
   `assert not result`. An empty list and `None` are both falsy; only one is
   correct.
6. Both `..._part_one` and `..._part_two` pass. Together they prove the default
   fixture scope rebuilds the data for every test.
7. All seven tests pass with `pytest -v`.

## Constraints

- **Take `tmp_path`, do not write to the current folder.** A test that writes
  `dues.csv` next to your source files leaves it behind, and the next run reads
  that stale file and passes for the wrong reason. `tmp_path` hands every test a
  fresh folder and deletes it afterwards.
- **`dues` returns; `dues_csv` yields.** Use `yield` only when there is teardown
  to do. `dues` has nothing to clean up, so it returns. `dues_csv` made a real
  file, so it yields, then deletes it. A `yield` fixture with nothing after the
  `yield` is just a `return` fixture in a costume.
- **Leave both fixtures at the default function scope.** `scope="module"` would
  build the list once and share it, so the test that pops a member would break
  the very next test. That broken test did nothing wrong, and that is exactly why
  shared state is the most expensive kind of test bug.
- **The threshold is strictly greater.** In arrears means owing *more* than the
  threshold. Grace owes exactly 500 and the threshold is 500, so she must not
  appear. Use `>`, never `>=`.
- **Parse the amount to an int at the boundary.** The loader turns `"1200"` into
  `1200` the moment it reads the row, so no caller down the line ever tries to do
  math on a string.

## Expected output

Running the shipped answer prints who is in arrears, then runs the suite and
reports each test. Your build will show the real capture here:

```text
$ python problem-02-dues-ledger.py
Threshold is 500 cents. In arrears = owing strictly more.
  in arrears: ['Ada', 'Yukihiro']
  Grace owes exactly the threshold, so she is NOT in arrears: True

The seven tests, run the way pytest runs them:
  PASS  test_arrears_are_sorted_alphabetically
  PASS  test_exactly_on_the_threshold_is_not_in_arrears
  PASS  test_nobody_over_a_high_threshold_returns_empty_list
  PASS  test_mutation_does_not_leak_part_one
  PASS  test_mutation_does_not_leak_part_two
  PASS  test_load_dues_reads_every_row
  PASS  test_load_dues_parses_amount_as_int

7 passed, 0 failed
```

## Steps

1. Save `ledger.py` and `test_ledger.py` in your Week 11 folder, side by side.
2. Fill in the `dues` fixture first — four dicts, one per member. Run
   `pytest -v -k "sorted or threshold or high"` and watch the three list tests
   go green.
3. Fill in the two mutation tests and rerun. If `part_two` fails with
   `assert 3 == 4`, your fixture is caching instead of re-cooking.
4. Fill in `dues_csv`: a header row plus the four data rows via
   `path.write_text(...)`. Then the teardown — `path.unlink()` and
   `assert not path.exists()`.
5. Fill in the last two loader tests and run `pytest -v`. Seven passed.
6. Run `pytest -q --setup-show test_ledger.py::test_load_dues_reads_every_row`
   once and read the SETUP and TEARDOWN lines wrapped around your test.

## The Solution

```python
"""problem-02-dues-ledger-solution.py — fixtures over a real CSV, proven headless.

Two fixtures share the sample data: one hands back a list of dues records, the
other writes those same records to a real CSV in pytest's throwaway ``tmp_path``
and cleans it up afterwards. Building the data from one table keeps the two
fixtures from drifting apart.

One file carries the module, the tests, and a ``main()`` that drives pytest and
prints a plain, same-every-time report.

Run it with::

    python problem-02-dues-ledger-solution.py
"""

from __future__ import annotations

import contextlib
import csv
import io
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

# --------------------------------------------------------------------------- #
# ledger.py — the module under test, given complete
# --------------------------------------------------------------------------- #

Dues = dict[str, Any]


def load_dues(path: Path) -> list[Dues]:
    """Read a dues CSV (columns: ``member``, ``owed_cents``) into records.

    ``owed_cents`` is parsed from text into an int, so callers never do
    arithmetic on strings.
    """
    dues: list[Dues] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            dues.append({"member": row["member"], "owed_cents": int(row["owed_cents"])})
    return dues


def members_in_arrears(dues: list[Dues], threshold_cents: int) -> list[str]:
    """Names of members owing strictly more than ``threshold_cents``, sorted A-Z."""
    return sorted(row["member"] for row in dues if row["owed_cents"] > threshold_cents)


# --------------------------------------------------------------------------- #
# test_ledger.py — fixture-driven tests
# --------------------------------------------------------------------------- #

THRESHOLD = 500

DUES_ROWS: tuple[tuple[str, str], ...] = (
    ("Ada", "1200"),
    ("Grace", "500"),
    ("Linus", "0"),
    ("Yukihiro", "750"),
)


@pytest.fixture
def dues() -> list[Dues]:
    """Four members: two over the threshold, one exactly on it, one clear."""
    return [{"member": member, "owed_cents": int(owed)} for member, owed in DUES_ROWS]


@pytest.fixture
def dues_csv(tmp_path: Path) -> Iterator[Path]:
    """Write the same four rows to a real CSV and yield its path."""
    path = tmp_path / "dues.csv"
    rows = ["member,owed_cents"]
    rows.extend(",".join(row) for row in DUES_ROWS)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    yield path
    path.unlink()
    assert not path.exists()


def test_arrears_are_sorted_alphabetically(dues: list[Dues]) -> None:
    """Only the two who owe more than the threshold, in order."""
    assert members_in_arrears(dues, THRESHOLD) == ["Ada", "Yukihiro"]


def test_exactly_on_the_threshold_is_not_in_arrears(dues: list[Dues]) -> None:
    """Owing exactly the threshold is not owing *more* than it."""
    assert "Grace" not in members_in_arrears(dues, THRESHOLD)


def test_nobody_over_a_high_threshold_returns_empty_list(dues: list[Dues]) -> None:
    """The answer is an empty list, not None."""
    assert members_in_arrears(dues, 100_000) == []


def test_mutation_does_not_leak_part_one(dues: list[Dues]) -> None:
    """Damage the fixture data on purpose."""
    dues.pop()
    assert len(dues) == 3


def test_mutation_does_not_leak_part_two(dues: list[Dues]) -> None:
    """The damage did not survive: this test gets all four rows back."""
    assert len(dues) == 4


def test_load_dues_reads_every_row(dues_csv: Path) -> None:
    """Four data rows become four records; the header becomes none."""
    assert len(load_dues(dues_csv)) == 4


def test_load_dues_parses_amount_as_int(dues_csv: Path) -> None:
    """The owed column arrives as an int, not as a string."""
    assert load_dues(dues_csv)[0]["owed_cents"] == 1200


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
    """Show who is in arrears, then run the suite and print the outcomes."""
    sample = [{"member": m, "owed_cents": int(o)} for m, o in DUES_ROWS]
    print(f"Threshold is {THRESHOLD} cents. In arrears = owing strictly more.")
    print(f"  in arrears: {members_in_arrears(sample, THRESHOLD)}")
    print("  Grace owes exactly the threshold, so she is NOT in arrears: "
          f"{'Grace' not in members_in_arrears(sample, THRESHOLD)}")

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

**One table, two fixtures.** The four members live in one small table of rows,
and both fixtures build from that one table. If `dues` typed the amounts out and
`dues_csv` typed the same amounts out again, you would have two copies waiting to
drift apart — fix one, forget the other. From a single table, a fifth member is
one new row, and the two fixtures cannot disagree about it.

**The `dues` fixture builds new dictionaries every call, and that is load
bearing.** Write the list once at the top of the file and hand the same list to
every test, and here is what happens: `part_one` pops a member off that shared
list, `part_two` asks for four and finds three, and the run goes red on a test
that did nothing wrong. Building the list fresh inside the fixture body gives
every test its own list *and* its own dicts. A fixture is a recipe pytest
re-cooks, not one bowl it passes around — and the two mutation tests exist purely
to make that claim checkable. Function scope is what keeps the recipe getting
re-cooked, so it is doing real work here even though you never see it.

**`return` for `dues`, `yield` for `dues_csv`, and the final assert.** `yield`
exists so you can run cleanup code *after* the test finishes. `dues` has nothing
to clean up, so a `yield` there would promise a teardown that never comes.
`dues_csv` made a real file, so it yields the path, then deletes the file, then
asserts the deletion actually happened. That last `assert not path.exists()`
inside a fixture is deliberate: a broken teardown fails loudly instead of leaving
junk behind for the next run to trip over.

**`tmp_path` instead of a path you build yourself.** A test that writes
`dues.csv` next to your source leaves it sitting there, and the next run reads
that old file. If you later break the code that writes the file, the test keeps
passing on yesterday's data and you never notice. `tmp_path` gives every test a
fresh, uniquely named folder, so "the file exists" and "my fixture wrote it"
cannot quietly come apart.

**Strictly `>`, with a member sitting exactly on the line to prove it.** Grace
owes exactly 500 and the threshold is 500, so she must not show up in the
answer. That single row is the whole point of the test: with only Ada and
Yukihiro in the data, `>` and `>=` behave identically and the bug ships unseen.
Grace is the row that can tell the two apart. And the empty-case test asserts
`== []`, not `assert not result`, because `None` is also falsy — checking for the
exact empty list is the only way to know the filter returned a real, empty
answer.

## Run it

Copy the worked answer on this page into `problem-02-dues-ledger.py` and run it:

```bash
python problem-02-dues-ledger.py
```

It needs `pytest` and nothing else. Your own work is `ledger.py` plus
`test_ledger.py`, run with `pytest -v`. The `-solution` in the filename keeps
this shipped answer from colliding with the `ledger.py` and `test_ledger.py` you
write yourself.

## Common bugs to catch

- **`fixture 'due' not found`, followed by a list of available fixtures.** You
  defined `dues` but asked for `due`. The names must match exactly — the
  parameter name is how pytest wires the fixture in.
- **`TypeError: object of type 'NoneType' has no len()`.** Your `dues` fixture
  builds the list but has no `return` in front of it, so pytest handed the test
  `None`. A fixture is a function, and a function that falls off the end returns
  `None`.
- **`AssertionError: assert 3 == 4` in the second mutation test.** You added
  `scope="module"` to `dues`. Remove it — the default function scope is what
  rebuilds the data for each test, and the failure landing on the *innocent*
  second test is exactly why shared state is so expensive.
- **`KeyError: 'owed_cents'`.** You left the header line out of the CSV, so
  `csv.DictReader` read your first member as the column names. Row one must be
  `member,owed_cents`.
- **`ValueError: invalid literal for int() with base 10`.** A CSV amount is not
  a plain number — a stray letter, a dollar sign, or a blank cell. `int()` wants
  digits and nothing else.
- **Grace shows up in arrears.** You used `>=` instead of `>`, so owing exactly
  the threshold now counts. Change it back to `>` — in arrears means owing
  *more*.

## Under the hood

<details>
<summary>Under the hood — why function scope re-runs the fixture body every test</summary>

You can skip this and still get every test green; it is here for the curious.

The default scope for a fixture is `function`. That word means pytest runs the
fixture's body again for each test function that asks for it. So `dues` is not
one list that all seven tests share — it is a fresh list, cooked from scratch,
handed to each test that names it. That is why `part_one` can pop a member and
`part_two` still sees all four: they were never holding the same list.

`scope="module"` would run the body just once and share the single result across
every test in the file. You would trade safety for speed. It is worth it when
the setup is genuinely expensive — spinning up a database, loading a big model —
and every test only reads the data, never changes it. The moment one test
mutates the shared thing, module scope turns into the leak this problem is built
to warn you about. Cheap setup like ours has nothing to gain from it, so leave
the scope alone.

</details>

## Acceptance checklist

- [ ] Both fixtures carry the `@pytest.fixture` decorator.
- [ ] `dues` returns its list; `dues_csv` yields its path.
- [ ] `dues_csv` takes `tmp_path` and never writes to the working folder.
- [ ] `dues_csv` deletes the file after the `yield` and asserts it is gone.
- [ ] `members_in_arrears` returns `["Ada", "Yukihiro"]` for THRESHOLD 500.
- [ ] The empty case asserts `== []`, not a falsy check.
- [ ] Both mutation tests pass, proving per-test fixture rebuild.
- [ ] `pytest -v` reports 7 passed.

## Stretch

- Move the `dues` fixture into a `conftest.py` next to your test file and delete
  it from `test_ledger.py`. Nothing else changes — that is how one fixture gets
  shared across many test files.
- Add a member whose `owed_cents` cell is blank in the CSV, decide what
  `load_dues` should do about it, and write a test that pins that behavior down.
- Parametrize the threshold: feed `members_in_arrears` several thresholds in one
  table-driven test and assert the arrears list for each.

---

Next: [Problem 3 — Hours and minutes](./problem-03-hours-minutes.md)
