# Exercise 3 — Table-Driven Tests With Parametrize

> **Topic:** `@pytest.mark.parametrize`, `ids=`, and parametrizing an expected exception
> **Lecture:** [01 — Introduction to `pytest`](../lecture-notes/01-intro-to-pytest.md) (section 8)
> **Difficulty:** Easy
> **Target time:** 25 minutes
> **Why this one:** most real bugs live in the cases nobody bothered to write a separate test for. Parametrize drops the cost of one more case to one more line, so you stop rationing them. It also makes the failure report name the exact input that broke, which is the difference between a five-second fix and a twenty-minute hunt.

## The Brief

The tool library prints a receipt when a member returns something late.
Exercise 1 gave you fees in whole cents; now you render them for a human who
expects `$2.50` and not `250`.

This looks like a one-liner and is not. Five cents must render as `$0.05`, not
`$0.5`. A four-figure amount must group as `$1,234.56`. Zero must render as
`$0.00`, not `$0`. And a negative amount is not a formatting problem at all — it
means whoever called you has a bug, and quietly printing `$-2.50` hides it.

Nine good inputs, three bad ones. As twelve separate test functions that is a
hundred lines of near-identical code. As two parametrized tests — one function
run once per row of a table — it is about twenty lines, and a thirteenth case
costs one more.

## Starter

The module under test:

```python
"""money.py — rendering whole-cent amounts for tool library receipts."""


def format_cents(cents: int) -> str:
    """Render a whole number of cents as a US dollar string.

    Args:
        cents: A non-negative whole number of cents.

    Returns:
        A string like ``"$1,234.56"``, always with two decimal places
        and comma-grouped thousands.

    Raises:
        ValueError: If ``cents`` is negative.
    """
    # TODO: raise ValueError("cents cannot be negative") for a negative input
    # TODO: split with divmod(cents, 100) into dollars and remainder
    # TODO: return f"${dollars:,}.{remainder:02d}"
    return ""
```

The test file:

```python
"""test_money.py — table-driven tests for receipt formatting."""

import pytest

from money import format_cents


@pytest.mark.parametrize(
    "cents, expected",
    [
        (0, "$0.00"),
        (5, "$0.05"),
        (25, "$0.25"),
        (99, "$0.99"),
        (100, "$1.00"),
        (250, "$2.50"),
        (1_000, "$10.00"),
        (123_456, "$1,234.56"),
        (100_000_000, "$1,000,000.00"),
    ],
    ids=[
        "zero",
        "nickel",
        "quarter",
        "under-a-dollar",
        "one-dollar",
        "two-fifty",
        "ten-dollars",
        "four-figures",
        "one-million",
    ],
)
def test_format_cents(cents: int, expected: str) -> None:
    """Every listed amount renders exactly as written."""
    # TODO: one assert, comparing format_cents(cents) to expected


@pytest.mark.parametrize(
    "cents",
    [-1, -25, -100],
    ids=["minus-one-cent", "minus-a-quarter", "minus-a-dollar"],
)
def test_negative_cents_is_rejected(cents: int) -> None:
    """A negative amount is a caller bug, not a credit."""
    # TODO: pytest.raises(ValueError, match="cannot be negative")
```

## Requirements

1. The two decorators stay exactly as given, including every row and every id.
   The table is the specification for this exercise.
2. Each test body is a single statement. If you find yourself writing an `if`
   inside a parametrized test, the branch belongs in the table as another row.
3. `format_cents` uses `divmod`, not float division. The type hints say `int`
   in and `str` out, and no float appears anywhere.
4. The remainder is zero-padded to two digits with `:02d`.
5. Thousands are comma-grouped with the `:,` format spec, not with manual string
   slicing.
6. `pytest -v` reports 12 passed, and each line shows its id in square brackets.

## Constraints

- **Always pass `ids=`.** Without them pytest labels the cases
  `test_format_cents[0-$0.00]` through `[100000000-$1,000,000.00]`, which are
  technically unique and completely unreadable in a CI log. `[nickel]` tells you
  what broke before you open the file.
- **Use `divmod`, never `cents / 100`.** `123456 / 100` produces a float, and
  floats carry rounding error that shows up on amounts you cannot predict in
  advance. Integer division and remainder are exact for every input, forever.
- **Keep the ids stable once written.** `pytest test_money.py::test_format_cents[nickel]`
  reruns exactly one case, and people paste those node ids into bug reports.
  Renaming an id silently breaks every link to it.
- **Do not collapse the two parametrized tests into one.** A single table
  carrying both "returns this string" and "raises this exception" needs a
  sentinel value and an `if` in the body, and now the test has logic that could
  itself be wrong. Two tests, two shapes, no branching.
- **`match=` is a regular expression, not a substring.** `match="cannot be
  negative"` works because it contains no regex metacharacters. If your message
  ever includes `(`, `.`, or `$`, escape it or the match silently changes
  meaning.

## Expected output

The shipped answer below folds `money.py`, the two tables, and a driver into one
file so it runs as a plain script. It formats a few amounts, shows the exact
hazard the guard prevents, then runs all twelve cases through pytest:

```text
$ python exercise-03-parametrize-solution.py
A few amounts, formatted:
            5 cents -> $0.05
          250 cents -> $2.50
       123456 cents -> $1,234.56
    100000000 cents -> $1,000,000.00

Why the guard matters — divmod on a negative rounds toward -inf:
  divmod(-1, 100) == (-1, 99)
  with NO guard, format_cents(-1) would return '$-1.99'
  with the guard, format_cents(-1) raises ValueError: cents cannot be negative

The twelve cases, run the way pytest runs them:
  PASS  test_format_cents[zero]
  PASS  test_format_cents[nickel]
  PASS  test_format_cents[quarter]
  PASS  test_format_cents[under-a-dollar]
  PASS  test_format_cents[one-dollar]
  PASS  test_format_cents[two-fifty]
  PASS  test_format_cents[ten-dollars]
  PASS  test_format_cents[four-figures]
  PASS  test_format_cents[one-million]
  PASS  test_negative_cents_is_rejected[minus-one-cent]
  PASS  test_negative_cents_is_rejected[minus-a-quarter]
  PASS  test_negative_cents_is_rejected[minus-a-dollar]

12 passed, 0 failed
```

Doing it for real, you run `pytest -v` and see twelve `PASSED` lines, each with
its id in square brackets.

## Steps

1. Save `money.py` and `test_money.py` side by side.
2. Before writing any implementation, run `pytest --collect-only -q` and confirm
   twelve node ids. Collection works even though the function is empty.
3. Fill in the two test bodies. Run `pytest -q`. Everything fails, because
   `format_cents` still returns `""`. That is expected.
4. Implement the `ValueError` guard. Rerun: the three negative cases go green.
5. Implement the `divmod` and the f-string return. Rerun: all twelve green.
6. Run one case on its own:
   `pytest -v "test_money.py::test_format_cents[four-figures]"`. Quote it —
   square brackets are glob characters in most shells.
7. Add a tenth row with its own id and confirm the count goes to 13 without
   touching the test body.

## The Solution

```python
"""exercise-03-parametrize-solution.py — table-driven tests, proven headless.

Normally you keep ``money.py`` and ``test_money.py`` in two files and run
``pytest``. A published answer is run as a plain script, so this one file
carries the module, the two parametrized tests, and a ``main()`` that drives
pytest itself and prints a plain, same-every-time report.

A parametrized test is one function run once per row of a table. Twelve rows,
twelve tests, one body — and when a row fails, the report names that row so you
know exactly which input broke.

Run it with::

    python exercise-03-parametrize-solution.py
"""

from __future__ import annotations

import contextlib
import io

import pytest

# --------------------------------------------------------------------------- #
# money.py — the module under test, three lines of body
# --------------------------------------------------------------------------- #


def format_cents(cents: int) -> str:
    """Render a whole number of cents as a US dollar string.

    Always two decimal places, always comma-grouped thousands, e.g.
    ``"$1,234.56"``. A negative amount is a caller bug, not a credit, so it
    raises rather than printing ``"$-1.99"``.
    """
    if cents < 0:
        raise ValueError("cents cannot be negative")
    dollars, remainder = divmod(cents, 100)
    return f"${dollars:,}.{remainder:02d}"


# --------------------------------------------------------------------------- #
# test_money.py — one table of good inputs, one table of bad inputs
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "cents, expected",
    [
        (0, "$0.00"),
        (5, "$0.05"),
        (25, "$0.25"),
        (99, "$0.99"),
        (100, "$1.00"),
        (250, "$2.50"),
        (1_000, "$10.00"),
        (123_456, "$1,234.56"),
        (100_000_000, "$1,000,000.00"),
    ],
    ids=[
        "zero",
        "nickel",
        "quarter",
        "under-a-dollar",
        "one-dollar",
        "two-fifty",
        "ten-dollars",
        "four-figures",
        "one-million",
    ],
)
def test_format_cents(cents: int, expected: str) -> None:
    """Every listed amount renders exactly as written."""
    assert format_cents(cents) == expected


@pytest.mark.parametrize(
    "cents",
    [-1, -25, -100],
    ids=["minus-one-cent", "minus-a-quarter", "minus-a-dollar"],
)
def test_negative_cents_is_rejected(cents: int) -> None:
    """A negative amount is a caller bug, not a credit."""
    with pytest.raises(ValueError, match="cannot be negative"):
        format_cents(cents)


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


def _unguarded(cents: int) -> str:
    """What format_cents would return with the guard deleted — for the demo."""
    dollars, remainder = divmod(cents, 100)
    return f"${dollars:,}.{remainder:02d}"


def main() -> None:
    """Show the formatter, the hazard the guard prevents, then run the suite."""
    print("A few amounts, formatted:")
    for cents in (5, 250, 123_456, 100_000_000):
        print(f"  {cents:>11} cents -> {format_cents(cents)}")

    print()
    print("Why the guard matters — divmod on a negative rounds toward -inf:")
    print(f"  divmod(-1, 100) == {divmod(-1, 100)}")
    print(f"  with NO guard, format_cents(-1) would return {_unguarded(-1)!r}")
    try:
        format_cents(-1)
    except ValueError as error:
        print(f"  with the guard, format_cents(-1) raises ValueError: {error}")

    print()
    print("The twelve cases, run the way pytest runs them:")
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

**`divmod` splits the number once and exactly.** `divmod(123456, 100)` is
`(1234, 56)` — the dollars and the cents, both whole numbers, no rounding
anywhere. The float route (`cents / 100` then some rounding) introduces error on
amounts you cannot predict, and money code that is wrong for one input in ten
thousand is worse than money code that is obviously wrong, because nobody finds
it until a customer does.

**The format spec does all the presentation.** `f"${dollars:,}.{remainder:02d}"`
carries two instructions. `:,` groups thousands, which is why `1000000` becomes
`1,000,000` with no string slicing. `:02d` pads the remainder to two digits,
which is why five cents is `$0.05` and not `$0.5`. Both live inside the braces,
after the colon — that is the whole syntax, and it replaces the fifteen lines of
manual padding people write when they do not know it exists.

**The guard is not about *where* it sits — it is about *existing at all*.** A
common half-truth is that the `if` must run before the `divmod` or the negative
"slips through". Not so: the guard raises wherever you put it, because it raises
before anything is formatted either way. The real hazard is deleting the guard,
and it is worth seeing because it is not what anyone expects. `divmod(-1, 100)`
is `(-1, 99)`, not `(0, -1)`, because Python's floor division rounds toward
negative infinity — so an *unguarded* `format_cents(-1)` cheerfully returns
`"$-1.99"`, one cent owed the other way rendered as nearly two dollars. Keep the
guard so that surprise can never reach a receipt.

**`ids=` turn node ids into sentences.** Without them the cases read
`test_format_cents[0-$0.00]` through `[100000000-$1,000,000.00]` — unique,
technically, and unreadable in a CI log at two in the morning. `[nickel]` names
what broke before you open the file. The ids are also addresses: people paste
them into bug reports, so renaming one silently breaks every link to it.

**One statement per body, and the branch belongs in the table.** The moment a
parametrized test contains an `if`, the test has logic, and logic can be wrong.
The table is data — readable and checkable by someone who does not know Python
well — while a branch inside the body has to be reasoned about.

**Two tests, not one.** A single table carrying both "returns this string" and
"raises this exception" needs a sentinel in the expected column and an `if` in
the body to read it. Two functions with two shapes cost four extra lines and
remove that whole problem. The `-> str` contract and the `raises ValueError`
contract are genuinely different; keeping them apart keeps the file honest about
that.

## Download and run

Download
[exercise-03-parametrize-solution.py](./exercise-03-parametrize-solution.py)
and run it:

```bash
python exercise-03-parametrize-solution.py
```

It needs `pytest` and nothing else. Your own work is `money.py` plus
`test_money.py`, run with `pytest -v`.

The `-solution` in the filename keeps this file from colliding with your own
`money.py` and `test_money.py`.

## Common bugs to catch

- **`AssertionError: assert '$0.5' == '$0.05'` — and note it is not alone.**
  Dropping the `:02d` does not take out one case, it takes out *five* of the
  nine: every amount whose cents part is `0` or a single digit loses a
  character. `[quarter]`, `[under-a-dollar]`, `[two-fifty]` and `[four-figures]`
  still pass because they all happen to have a two-digit cents part — which is
  exactly why one hand-picked test case would probably have missed the bug:

  ```text
  $ pytest -q
  FF..F.F.F                                                                [100%]
  =========================== short test summary info ===========================
  FAILED test_money.py::test_format_cents[zero] - AssertionError: assert '$0.0'...
  FAILED test_money.py::test_format_cents[nickel] - AssertionError: assert '$0....
  FAILED test_money.py::test_format_cents[one-dollar] - AssertionError: assert ...
  FAILED test_money.py::test_format_cents[ten-dollars] - AssertionError: assert...
  FAILED test_money.py::test_format_cents[one-million] - AssertionError: assert...
  5 failed, 4 passed in 0.05s
  ```

- **`AssertionError: assert '$1234.56' == '$1,234.56'`.** You dropped the comma
  from the format spec. It is `{dollars:,}` — the comma goes inside the braces,
  after the colon. Only the two large amounts notice, which is why the table has
  two large amounts.
- **`Failed: DID NOT RAISE <class 'ValueError'>` on all three negative ids.**
  Your comparison is backwards — `if cents > 0:` instead of `if cents < 0:` — or
  you built the exception without a `raise` in front of it. On pytest 9 the
  caret points at the `with pytest.raises(...)` line. And it is worth seeing what
  the unguarded function actually produces: `format_cents(-1)` returns
  `'$-1.99'`, which is the whole reason the guard exists.
- **`AssertionError: Regex pattern did not match.`** Your message says "must be
  positive" but the test looks for "cannot be negative". `match=` is searched
  against the exception text, so the two have to agree, and any `.`, `(` or `$`
  in the message needs escaping.
- **`fixture 'cents' not found`.** You misspelled the argument string in the
  decorator — `"cent, expected"` — so pytest could not find a parameter named
  `cents` and went looking for a fixture instead. On pytest 9 this is a
  collection error. The names in the string and in the signature must match.
- **Eleven of twelve pass and you shrug.** Do not — see the first bug above.
  Any red row is one real input your code gets wrong. Read the
  `cents = 5, expected = '$0.05'` header pytest prints above the failure; it
  names the row for you.

## Under the hood

<details>
<summary>Under the hood — what one parametrize decorator expands into</summary>

Before writing any implementation, you can see what the table becomes.
Collection works even though `format_cents` still returns `""`:

```text
$ pytest --collect-only -q
test_money.py::test_format_cents[zero]
test_money.py::test_format_cents[nickel]
test_money.py::test_format_cents[quarter]
test_money.py::test_format_cents[under-a-dollar]
test_money.py::test_format_cents[one-dollar]
test_money.py::test_format_cents[two-fifty]
test_money.py::test_format_cents[ten-dollars]
test_money.py::test_format_cents[four-figures]
test_money.py::test_format_cents[one-million]
test_money.py::test_negative_cents_is_rejected[minus-one-cent]
test_money.py::test_negative_cents_is_rejected[minus-a-quarter]
test_money.py::test_negative_cents_is_rejected[minus-a-dollar]

12 tests collected in 0.01s
```

Two functions, twelve tests: pytest turned each row of each table into its own
independent test, named by its id. Adding a tenth row plus its id takes the
count to 13 without touching the function body — which is the entire argument
for the shape. Stack a *second* `@pytest.mark.parametrize` on the same function
and pytest takes the cross product, so twelve cases become twenty-four.

</details>

## Acceptance checklist

- [ ] `pytest --collect-only -q` reports 12 tests from 2 functions.
- [ ] Every case has a human-readable id, no auto-generated labels.
- [ ] Each test body is a single statement.
- [ ] `format_cents` uses `divmod` and contains no float arithmetic.
- [ ] A negative amount raises `ValueError` instead of formatting to `$-1.99`.
- [ ] You can run one case by node id from the shell.
- [ ] Committed with a message like
      `Add Week 11 exercise 3: parametrized receipt formatting tests`.

## Stretch

- Stack a second `@pytest.mark.parametrize` on the same function, over
  `symbol` in `["$", "£"]`. Pytest takes the cross product, so twelve cases
  become twenty-four. Read the ids it generates.
- Mark one row `pytest.param(1, "$0.01", marks=pytest.mark.xfail)` and see how
  an expected failure is reported differently from a real one.
- Write the inverse, `parse_dollars("$1,234.56") -> 123456`, with its own table
  over the same nine amounts. A round-trip check —
  `parse_dollars(format_cents(n)) == n` — is a lot of test for very little code.

When your twelve are green, move on to
[Exercise 4 — Mocking a Network Call](./exercise-04-mocking.md).
