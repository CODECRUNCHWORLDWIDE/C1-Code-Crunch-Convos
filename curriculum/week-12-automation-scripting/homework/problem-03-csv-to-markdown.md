# Homework 3 — CSV to Markdown converter

> **Topic:** `csv`, padding columns to width, and escaping the pipe
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Beginner
> **Target time:** 45 min
> **Why this one:** you will paste a table into a README or an issue a hundred times, and doing it by hand is miserable. It is also a clean drill in the thing beginners skip — computing a column width from data rather than guessing — and in escaping a character that would otherwise break the output.

## The Brief

Read a CSV file and print a GitHub-flavored Markdown table on stdout. The first
row of the CSV is the header. Pad every column so the pipes line up, escape any
`|` that appears inside a cell (it would start a new column otherwise), and
support an optional alignment flag.

The result is a table you can paste straight into a README and have it render.

## Starter

```python
"""problem-03-csv-to-markdown.py — turn a CSV into a Markdown table.

    python problem-03-csv-to-markdown.py data.csv --align c
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

MIN_WIDTH = 3  # a column narrower than "---" cannot hold a separator


def escape(cell: str) -> str:
    """A pipe inside a cell would start a new column; backslash-escape it."""
    # TODO: replace "|" with "\\|"
    raise NotImplementedError


def render_table(rows: list[list[str]], align: str) -> str:
    """Render rows (header first) as a padded Markdown table."""
    # TODO: escape cells, compute per-column widths, pad, build the separator
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Read the CSV, print the Markdown table. Return an exit code."""
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. Read the CSV with `csv.reader` (or `csv.DictReader`); the first row is the
   header.
2. Right-pad every column to the width of its longest cell so the pipes align.
3. Escape `|` characters inside cells.
4. Support `--align l|c|r`, which sets the separator row's colon markers.
5. Print the table to stdout; exit 1 if the file is missing or empty.

## Constraints

- **Compute widths from the data, do not guess.** The width of a column is the
  longest of its cells (header included), measured *after* escaping — a `\|`
  is two characters, not one, and getting that wrong throws the alignment off by
  a column.
- **Square off ragged rows.** A CSV row with fewer cells than the header would
  otherwise produce a short Markdown row that renders wrong. Pad every row to
  the column count before measuring.
- **The separator markers depend on `--align`.** Left is `:---`, right is
  `---:`, centre is `:---:`, and each must be as wide as its column so the raw
  Markdown stays readable.
- **Enforce a minimum column width of 3.** A one-character column cannot hold a
  centre separator (`:-:` needs three), so pad narrow columns up to it.

## Expected output

The shipped answer, [`problem-03-csv-to-markdown-solution.py`](./problem-03-csv-to-markdown-solution.py),
builds a small CSV in a temp file — with a cell containing a `|`, and an empty
cell — and renders it left-aligned and centered. Real captured output:

```text
$ python problem-03-csv-to-markdown-solution.py
CSV to Markdown — driven headless on a CSV this file builds.

Default (left-aligned):
| Name  | Score | Note         |
| :---- | :---- | :----------- |
| Alice | 95    | top \| marks |
| Bob   | 87    | steady       |
| Carol | 100   |              |
[exit 0]

Center-aligned (--align c):
| Name  | Score | Note         |
| :---: | :---: | :----------: |
| Alice | 95    | top \| marks |
| Bob   | 87    | steady       |
| Carol | 100   |              |
[exit 0]
```

The `top | marks` cell comes through as `top \| marks`, and the empty cell pads
to its column width rather than collapsing.

## Steps

1. Write `escape` and confirm `"a|b"` becomes `"a\\|b"`.
2. Write `render_table` for the left-aligned case only, and check the pipes line
   up on a two-column CSV.
3. Add the `--align` separator logic and eyeball all three variants.
4. Feed it a CSV with a `|` in a cell and one short row, and confirm neither
   breaks the table.
5. Paste the output into a Markdown preview and confirm it renders.

## The Solution

The shipped file is your answer — `escape`, `render_table`, `main` — with a
`demo()` that builds a CSV and renders it two ways. Your own file has no demo; it
reads a CSV path from the command line.

```python
"""problem-03-csv-to-markdown-solution.py — CSV to a Markdown table, headless.

The homework answer reads a CSV and prints a GitHub-flavored Markdown table:
columns padded to their widest cell, `|` escaped inside cells, and an optional
--align. Your own problem-03-csv-to-markdown.py ends in
``raise SystemExit(main())`` and you point it at a real CSV.

This is pure standard library and already deterministic, so the demo just builds
a small CSV in a temp file — with a cell that contains a `|`, and an empty cell —
and renders it left-aligned and centered. The converter being tested is
identical either way.

Run it with::

    python problem-03-csv-to-markdown-solution.py
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

MIN_WIDTH = 3  # a column narrower than "---" cannot hold a separator

SEPARATORS = {
    "l": lambda width: ":" + "-" * (width - 1),
    "c": lambda width: ":" + "-" * (width - 2) + ":",
    "r": lambda width: "-" * (width - 1) + ":",
}


def escape(cell: str) -> str:
    """A pipe inside a cell would start a new column; backslash-escape it."""
    return cell.replace("|", "\\|")


def render_table(rows: list[list[str]], align: str) -> str:
    """Render rows (header first) as a padded GitHub-flavored Markdown table."""
    grid = [[escape(cell) for cell in row] for row in rows]
    columns = max(len(row) for row in grid)
    grid = [row + [""] * (columns - len(row)) for row in grid]  # ragged rows squared off
    widths = [max(MIN_WIDTH, max(len(row[i]) for row in grid)) for i in range(columns)]

    def line(cells: list[str]) -> str:
        return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)) + " |"

    separator = "| " + " | ".join(SEPARATORS[align](widths[i]) for i in range(columns)) + " |"
    header, *body = grid
    return "\n".join([line(header), separator, *(line(row) for row in body)])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv2md",
        description="Turn a CSV file into a GitHub-flavored Markdown table.",
    )
    parser.add_argument("csv", type=Path, help="The CSV file to read.")
    parser.add_argument("--align", choices=("l", "c", "r"), default="l",
                        help="Column alignment (default: %(default)s)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Read the CSV, print the Markdown table. Return an exit code."""
    args = build_parser().parse_args(argv)
    if not args.csv.is_file():
        print(f"error: no such CSV file: {args.csv}", file=sys.stderr)
        return 1

    with args.csv.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.reader(handle) if row]
    if not rows:
        print(f"error: {args.csv} is empty", file=sys.stderr)
        return 1

    print(render_table(rows, args.align))
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — a small CSV built in a temp file. Your own file has no
# demo; it reads a CSV path from the command line.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Render one small CSV two ways."""
    print("CSV to Markdown — driven headless on a CSV this file builds.")
    print()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = Path(tmp) / "data.csv"
        csv_path.write_text(
            "Name,Score,Note\n"
            "Alice,95,top | marks\n"   # the pipe must be escaped
            "Bob,87,steady\n"
            "Carol,100,\n",            # an empty cell
            encoding="utf-8",
        )
        print("Default (left-aligned):")
        print(f"[exit {main([str(csv_path)])}]")
        print()
        print("Center-aligned (--align c):")
        print(f"[exit {main([str(csv_path), '--align', 'c'])}]")


if __name__ == "__main__":
    demo()
```

**Widths are measured after escaping, over a squared-off grid.** The code
escapes every cell first, then pads short rows out to the column count, and only
then computes `widths` as the longest cell per column. Order matters: measure
before escaping and a `|` cell reports width 1 while it prints as 2, and the
whole column is a character short. Squaring off the rows first means a CSV row
that is missing its last field still produces a full-width Markdown row.

**One `line()` helper renders the header and every body row.** It left-justifies
each cell to its column width and joins with ` | `. Because the header, the body
rows, and the width calculation all go through the same escaped grid, they
cannot disagree about how wide a column is — the classic bug where the header
lines up and the third data row does not simply cannot happen.

**The separator is data-driven, not hand-typed.** `SEPARATORS[align](width)`
builds `:---`, `---:`, or `:---:` at exactly the column's width, so the raw
Markdown is as readable as the rendered table. A hand-typed `:---:` that does not
match the column width still *renders* — Markdown does not care — but the source
looks ragged, and this file is a tool for producing source you paste and read.

**`MIN_WIDTH = 3` guards the narrow-column case.** A column whose widest cell is
one character (a `y`/`n` flag, say) cannot hold a centre separator, which needs
`:-:`. Clamping every width up to 3 keeps every alignment legal without a special
case.

## Download and run

Download
[problem-03-csv-to-markdown-solution.py](./problem-03-csv-to-markdown-solution.py)
and run it:

```bash
python problem-03-csv-to-markdown-solution.py
```

It is pure standard library and builds its own CSV, so you can also
[run it in the online editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-12-automation-scripting/homework/problem-03-csv-to-markdown.md).

## Common bugs to catch

- **A `|` in a cell splits it into two columns.** You did not escape it. Replace
  `|` with `\|` in every cell.
- **The header lines up but a data row does not.** You measured widths on the
  raw cells and padded the escaped ones (or vice versa). Do both on the same
  escaped grid.
- **A short CSV row renders with too few cells.** You did not pad ragged rows to
  the column count before rendering.
- **`--align c` produces `:-:` on a wide column.** Your separator was a fixed
  string instead of one built to the column's width.
- **`csv` splits a quoted field with a comma inside it wrongly.** You split on
  `,` by hand instead of using the `csv` module, which understands quoting.
- **A blank trailing line in the CSV becomes an empty table row.** Filter out
  empty rows when you read.

## Under the hood

<details>
<summary>Under the hood — why you use the csv module instead of split(",")</summary>

`line.split(",")` looks like it parses CSV, and it does, right up until a cell
contains a comma. Real CSV handles that by quoting: `Smith, John` is written
`"Smith, John"`, and a quote inside a quoted field is doubled (`""`). A field can
even contain a newline if it is quoted, so a single logical row can span several
lines of the file. `split(",")` knows none of this — it would turn
`"Smith, John",42` into three fields and mangle every address, price, or
free-text column you ever feed it.

The `csv` module implements the actual grammar (RFC 4180, plus the dialects real
programs emit), so `csv.reader` hands you the fields a spreadsheet would, quotes
and embedded commas resolved. It also has `csv.writer` for the reverse trip, and
`csv.Sniffer` to guess whether a file is comma- or tab- or semicolon-separated.
The rule worth keeping past this exercise: whenever a format has an escaping or
quoting scheme — CSV, JSON, HTML, URLs, shell arguments — reach for the library
that knows the scheme rather than the `str` method that looks close enough. The
`str` method is the one that fails on the row you did not test.

</details>

## Acceptance checklist

- [ ] The pipes align in the raw output, header and every row.
- [ ] A `|` inside a cell is escaped and does not break the table.
- [ ] `--align l|c|r` all produce valid separator rows.
- [ ] A short CSV row still renders full-width.
- [ ] The output pastes into Markdown and renders as a table.
- [ ] Committed to Git with a message like
      `Add Week 12 homework 3: CSV to Markdown`.

## Stretch

- Add `--align` *per column*, e.g. `--align l,c,r`, so a numbers column can be
  right-aligned while text stays left.
- Read from stdin when no file is given, so you can pipe into it:
  `cat data.csv | python problem-03-csv-to-markdown.py`.
- Add `--max-width N` that truncates long cells with an ellipsis, so one giant
  cell does not stretch the whole table.

When your tables line up, move on to
[Homework 4 — Batch image resizer](./problem-04-image-resizer.md).
