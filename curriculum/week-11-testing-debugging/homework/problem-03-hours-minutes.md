# Homework Problem 3 — Hours and minutes

> **Topic:** `@pytest.mark.parametrize`, `ids=`, zero-padding with `:02d`, and a parametrized exception
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md) (section 8)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** the rule fits on a line but hides an off-by-one, and parametrize drops the cost of one more case to one line, so you stop rationing the case that has the bug in it.

## The Brief

The tool library has a front desk. When a member borrows a drill or a saw, a
clock starts. The desk shows how long the tool has been out as `H:MM` — hours,
a colon, then minutes. Think of a scoreboard: the minutes side always shows two
digits, even when there are only a few.

So five minutes must read `0:05`, not `0:5`. That leading zero is the whole
job. Ten hours must read `10:00`, because hours have no ceiling — a tool can be
out all day. And a negative number of minutes is not a display question at all.
Time cannot run backward. If someone hands you a negative, whoever called you
made a mistake, and your job is to say so loudly, not to paper over it.

Now, testing this by hand is boring. You would write one little test for `0`,
another for `5`, another for `60`, and each one looks almost exactly like the
last. A **parametrized test** fixes that. Picture a table with one row per
example: the input on the left, the answer you expect on the right. You write
the test body **once**, and pytest runs it **once per row**. Ten rows, ten
tests, one function. Adding an eleventh example costs one line, not one more
copy-pasted function.

## Starter

The module you are testing, `checkout.py`:

```python
"""checkout.py — showing how long a tool has been out, as H:MM."""


def format_hm(total_minutes: int) -> str:
    """Render a whole number of minutes as ``H:MM``.

    Args:
        total_minutes: A non-negative whole number of minutes.

    Returns:
        A string like ``"1:05"`` — the minutes part always two digits,
        the hours part with no upper bound.

    Raises:
        ValueError: If ``total_minutes`` is negative.
    """
    # TODO: raise ValueError("total_minutes cannot be negative") for a negative input
    # TODO: split with divmod(total_minutes, 60) into hours and minutes
    # TODO: return f"{hours}:{minutes:02d}"
    return ""
```

The test file you write, `test_checkout.py`:

```python
"""test_checkout.py — table-driven tests for the H:MM display."""

import pytest

from checkout import format_hm


@pytest.mark.parametrize(
    "minutes, expected",
    [
        (0, "0:00"),
        (5, "0:05"),
        (59, "0:59"),
        (60, "1:00"),
        (65, "1:05"),
        (600, "10:00"),
        (1_439, "23:59"),
    ],
    ids=[
        "zero",
        "five-minutes",
        "under-an-hour",
        "one-hour",
        "one-hour-five",
        "ten-hours",
        "almost-a-day",
    ],
)
def test_format_hm(minutes: int, expected: str) -> None:
    """Every listed duration renders exactly as written."""
    # TODO: one assert, comparing format_hm(minutes) to expected


@pytest.mark.parametrize(
    "minutes",
    [-1, -60],
    ids=["minus-one", "minus-an-hour"],
)
def test_negative_is_rejected(minutes: int) -> None:
    """A negative duration is a caller bug, not a display problem."""
    # TODO: pytest.raises(ValueError, match="cannot be negative")
```

## Requirements

1. The two decorators stay exactly as given, including every row and every id.
   The table is the specification for this problem.
2. Each test body is a single statement. If you catch yourself writing an `if`
   inside a parametrized test, the branch belongs in the table as another row.
3. `format_hm` uses `divmod`, not float division. The type hints say `int` in
   and `str` out, and no float appears anywhere.
4. The minutes part is zero-padded to two digits with `:02d`.
5. `pytest -v` reports the tests as passed, and each line shows its id in square
   brackets.
6. The negative test uses `pytest.raises(ValueError, match="cannot be negative")`.

## Constraints

- **Always pass `ids=`.** Without them pytest labels the good-input cases
  `test_format_hm[0-0:00]` through `[1439-23:59]` — technically unique and
  completely unreadable in a CI log. `[five-minutes]` tells you what broke
  before you open the file.
- **Use `divmod`, never `total_minutes / 60`.** Float division carries rounding
  error that shows up on inputs you cannot predict in advance. Integer division
  and remainder are exact for every input, forever.
- **Keep the ids stable once written.** `pytest test_checkout.py::test_format_hm[five-minutes]`
  reruns exactly one case, and people paste those node ids into bug reports.
  Renaming an id silently breaks every link to it.
- **Do not merge the good-inputs table and the raises table into one.** A single
  table carrying both "returns this string" and "raises this exception" needs a
  sentinel value and an `if` in the body, and now the test has logic that could
  itself be wrong. Two tables, two shapes, no branching.
- **`match=` is a regular expression, not a substring.** `match="cannot be
  negative"` works because it contains no regex metacharacters. If your message
  ever includes `(`, `.`, or `$`, escape it or the match silently changes
  meaning.

## Expected output

Running the shipped answer prints a few durations, then runs every case the way
pytest runs it and reports the count:

```text
$ python problem-03-hours-minutes.py
format_hm(minutes):
      5 minutes -> 0:05
     65 minutes -> 1:05
    600 minutes -> 10:00

The nine cases, run the way pytest runs them:
  PASS  test_format_hm[zero]
  PASS  test_format_hm[five-minutes]
  PASS  test_format_hm[under-an-hour]
  PASS  test_format_hm[one-hour]
  PASS  test_format_hm[one-hour-five]
  PASS  test_format_hm[ten-hours]
  PASS  test_format_hm[almost-a-day]
  PASS  test_negative_is_rejected[minus-one]
  PASS  test_negative_is_rejected[minus-an-hour]

9 passed, 0 failed
```

Doing it for real, you run `pytest -v` and see one `PASSED` line per case, each
with its id in square brackets.

## Steps

1. Save `checkout.py` and `test_checkout.py` side by side in the same folder.
2. Before writing any implementation, run `pytest --collect-only -q` and confirm
   nine node ids. Collection works even though `format_hm` still returns `""`.
3. Fill in the two test bodies. Run `pytest -q`. Everything fails, because
   `format_hm` still returns `""`. That is expected.
4. Implement the `ValueError` guard first. Rerun: the two negative cases go
   green. Then implement the `divmod` and the f-string return. Rerun: all nine
   green.
5. Run one case on its own:
   `pytest -v "test_checkout.py::test_format_hm[ten-hours]"`. Quote it — square
   brackets are glob characters in most shells.
6. Add an eighth row with its own id and watch the count rise without touching
   the test body.

## The Solution

```python
"""problem-03-hours-minutes-solution.py — table-driven tests, proven headless.

The front desk shows how long a tool has been out as ``H:MM``. The rule fits on
one line and still hides an off-by-one: five minutes must render ``0:05``, not
``0:5``. A parametrized test — one function run once per row of a table — makes a
tenth case cost one line, so you stop rationing the cases the bugs hide in.

One file carries the module, the two tables, and a ``main()`` that drives pytest
and prints a plain, same-every-time report.

Run it with::

    python problem-03-hours-minutes-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# checkout.py — the module under test
# --------------------------------------------------------------------------- #


def format_hm(total_minutes: int) -> str:
    """Render a whole number of minutes as ``H:MM``.

    The minutes part is always two digits (``0:05``), the hours part has no
    upper bound (``10:00``). A negative duration is a caller bug.
    """
    if total_minutes < 0:
        raise ValueError("total_minutes cannot be negative")
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}:{minutes:02d}"


# --------------------------------------------------------------------------- #
# test_checkout.py — one table of good inputs, one of bad inputs
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "minutes, expected",
    [
        (0, "0:00"),
        (5, "0:05"),
        (59, "0:59"),
        (60, "1:00"),
        (65, "1:05"),
        (600, "10:00"),
        (1_439, "23:59"),
    ],
    ids=[
        "zero",
        "five-minutes",
        "under-an-hour",
        "one-hour",
        "one-hour-five",
        "ten-hours",
        "almost-a-day",
    ],
)
def test_format_hm(minutes: int, expected: str) -> None:
    """Every listed duration renders exactly as written."""
    assert format_hm(minutes) == expected


@pytest.mark.parametrize(
    "minutes",
    [-1, -60],
    ids=["minus-one", "minus-an-hour"],
)
def test_negative_is_rejected(minutes: int) -> None:
    """A negative duration is a caller bug, not a display problem."""
    with pytest.raises(ValueError, match="cannot be negative"):
        format_hm(minutes)


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each case's id and outcome, in order."""

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
    """Show a few durations, then run the suite and print the outcomes."""
    print("format_hm(minutes):")
    for minutes in (5, 65, 600):
        print(f"  {minutes:>5} minutes -> {format_hm(minutes)}")

    print()
    print("The nine cases, run the way pytest runs them:")
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

**`divmod` splits the number once and exactly.** `divmod(65, 60)` is `(1, 5)` —
the hours and the minutes, both whole numbers, no rounding anywhere. The float
route (`total_minutes / 60` then some rounding) introduces error on inputs you
cannot predict, and a clock that is wrong for one input in ten thousand is worse
than one that is obviously wrong, because nobody finds it until a member does.

**`:02d` is the whole reason `0:05` is not `0:5`.** The format spec
`f"{hours}:{minutes:02d}"` carries the padding: `:02d` means "print this integer
in at least two digit-columns, filling the front with zeros." Drop it and you do
not break one case — you break **every** case whose minutes part is a single
digit. Look at the table: `0:00`, `0:05`, `1:00`, `10:00` all end in a minute
under ten, so all four go red. `0:59`, `1:05` and `23:59` survive only because
their minutes happen to be two digits already. That is exactly why one
hand-picked test would probably have missed the bug — you would have picked a
two-digit case and never seen it.

**`ids=` turn node ids into sentences.** Without them the cases read
`test_format_hm[0-0:00]` through `[1439-23:59]` — unique, technically, and
unreadable in a CI log at two in the morning. `[five-minutes]` names what broke
before you open the file. The ids are also addresses: people paste them into bug
reports, so renaming one silently breaks every link to it.

**One statement per body, and the branch belongs in the table.** The moment a
parametrized test contains an `if`, the test has logic, and logic can be wrong.
The table is data — readable and checkable by someone who does not know Python
well — while a branch inside the body has to be reasoned about.

**Two tables, not one.** A single table carrying both "returns this string" and
"raises this exception" needs a sentinel in the expected column and an `if` in
the body to read it. Two functions with two shapes cost a few extra lines and
remove that whole problem. The `-> str` contract and the `raises ValueError`
contract are genuinely different; keeping them apart keeps the file honest about
that.

## Run it

Copy the worked answer on this page into `problem-03-hours-minutes.py` and run it:

```bash
python problem-03-hours-minutes.py
```

It needs `pytest` and nothing else. Your own work is `checkout.py` plus
`test_checkout.py`, run with `pytest -v`.

The `-solution` in the filename keeps this file from colliding with your own
`checkout.py` and `test_checkout.py`.

## Common bugs to catch

- **`AssertionError: assert '0:5' == '0:05'` — and note it is not alone.**
  Dropping the `:02d` does not take out one case, it takes out **five** of the
  seven: every row whose minute part is under ten loses a character. `[zero]`,
  `[five-minutes]`, `[one-hour]`, `[one-hour-five]` and `[ten-hours]` all go red
  together, while only `[under-an-hour]` and `[almost-a-day]` still pass, because
  their minutes are already two digits (`59`). Do not fix one and move on.
- **`Failed: DID NOT RAISE <class 'ValueError'>` on the two negative ids.** Your
  comparison is backwards — `if total_minutes > 0:` instead of `< 0` — or you
  built the exception without a `raise` in front of it. On pytest 9 the caret
  points at the `with pytest.raises(...)` line.
- **`AssertionError: Regex pattern did not match.`** Your message says "must be
  positive" but the test looks for "cannot be negative". `match=` is searched
  against the exception text, so the two have to agree, and any `.`, `(` or `$`
  in the message needs escaping.
- **`fixture 'minutes' not found`.** You misspelled the argument string in the
  decorator — `"minute, expected"` — so pytest could not find a parameter named
  `minutes` and went looking for a fixture instead. The names in the string and
  in the signature must match.
- **A row or two goes red and you shrug.** Do not. Every red row is one real
  input your code gets wrong. Read the `minutes = 5, expected = '0:05'` header
  pytest prints above the failure; it names the row for you.

## Under the hood

<details>
<summary>Under the hood — what the two parametrize decorators expand into</summary>

Before writing any implementation, you can see what the tables become.
Collection works even though `format_hm` still returns `""`:

```text
$ pytest --collect-only -q
test_checkout.py::test_format_hm[zero]
test_checkout.py::test_format_hm[five-minutes]
test_checkout.py::test_format_hm[under-an-hour]
test_checkout.py::test_format_hm[one-hour]
test_checkout.py::test_format_hm[one-hour-five]
test_checkout.py::test_format_hm[ten-hours]
test_checkout.py::test_format_hm[almost-a-day]
test_checkout.py::test_negative_is_rejected[minus-one]
test_checkout.py::test_negative_is_rejected[minus-an-hour]

9 tests collected in 0.01s
```

Two functions, nine tests: pytest turned each row of each table into its own
independent test, named by its id. Adding an eighth good row plus its id takes
the count to 10 without touching the function body — which is the entire
argument for the shape. Stack a *second* `@pytest.mark.parametrize` on the same
function and pytest takes the cross product, so seven cases become fourteen.

</details>

## Acceptance checklist

- [ ] `pytest --collect-only -q` reports 9 tests from 2 functions.
- [ ] Every case has a human-readable id, no auto-generated labels.
- [ ] Each test body is a single statement.
- [ ] `format_hm` uses `divmod` and contains no float arithmetic.
- [ ] The minutes part is zero-padded with `:02d`, so `5` renders `0:05`.
- [ ] A negative duration raises `ValueError` instead of formatting.
- [ ] You can run one case by node id from the shell.

## Stretch

- Stack a second `@pytest.mark.parametrize` on the same function, over a
  `symbol` or `format` choice. Pytest takes the cross product, so seven cases
  become fourteen. Read the ids it generates.
- Mark one row `pytest.param(90, "1:30", marks=pytest.mark.xfail)` and see how
  an expected failure is reported differently from a real one.
- Write the inverse, `parse_hm("1:05") -> 65`, with its own table over the same
  seven durations. A round-trip check — `parse_hm(format_hm(n)) == n` — is a lot
  of test for very little code.

When your nine are green, move on to
[Problem 4 — Overdue notice](./problem-04-overdue-notice.md).
