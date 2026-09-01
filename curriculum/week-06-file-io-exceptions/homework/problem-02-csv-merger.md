# Homework Problem 2 — CSV Merger

> **Topic:** joining several spreadsheets into one, and refusing to start when they do not agree
> **Lecture:** [Lecture 02 — CSV and JSON](../lecture-notes/02-csv-and-json.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** the brief contains three words that decide the whole shape of the program — "before writing anything". This is where you learn that opening a file for writing is itself a destructive act, so the checking has to happen first.

## The Brief

Three spreadsheets, one per quarter, all with the same columns. You want
them as one file for the year.

```text
q1.csv     order_id,customer,amount
q2.csv     order_id,customer,amount
q3.csv     order_id,customer,amount
```

Your tool reads them all and writes one `year.csv` with every row from
every input, in order, under the same header. It adds one column,
`source`, holding the name of the file each row came from — without the
`.csv` on the end, so `q1.csv` becomes `q1`. Without that column, the
moment the rows are mixed together nobody can tell which quarter a row
belonged to.

```text
$ python csv_merge.py q1.csv q2.csv q3.csv --out year.csv
Merged 3 files → year.csv (842 total rows)
```

Now the hard requirement. The inputs are supposed to have the **same
header**. If one of them does not — somebody called the column `total`
instead of `amount` — you raise a `ValueError` with a message that says
which files disagreed and how, and you do it **before writing
anything**.

That last phrase is not decoration. Opening a file with `"w"` empties it
immediately, before a single row is written. If `year.csv` already
existed from a good run this morning, a merge that fails at file three
has already destroyed it. So all the checking happens while the output
path is still untouched.

Use `argparse` for the command line. You have seen it briefly, and the
[docs](https://docs.python.org/3/library/argparse.html) are friendly.

## Starter

Save this as `csv_merge.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it merges nothing and reports zero rows:

```python
"""Concatenate CSV files that share a header, tagging each row with its source."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

SOURCE_COLUMN = "source"


def read_header(path: Path) -> list[str]:
    """Return the header row of `path`, or raise ValueError if there is none."""
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f), None)
    if header is None:
        raise ValueError(f"{path} is empty: no header row to merge")
    return header


def common_header(paths: list[Path]) -> list[str]:
    """Return the shared header, or raise ValueError naming the first mismatch."""
    reference = read_header(paths[0])
    # TODO: refuse if `reference` already contains SOURCE_COLUMN
    for path in paths[1:]:
        header = read_header(path)
        # TODO: raise ValueError if `header` differs from `reference`,
        #       naming both files and both headers
    return reference


def merge(paths: list[Path], out_path: Path) -> int:
    """Merge `paths` into `out_path`. Return the number of data rows written."""
    header = common_header(paths)
    fieldnames = [*header, SOURCE_COLUMN]
    rows_written = 0
    with out_path.open("w", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        # TODO: for each input, read its rows with csv.DictReader, set
        #       row[SOURCE_COLUMN] to the file's stem, write it, and count it
    return rows_written


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Turn the command line into an inputs list and an output path."""
    parser = argparse.ArgumentParser(
        prog="csv_merge.py",
        description="Concatenate CSV files that share a header.",
    )
    parser.add_argument("inputs", nargs="+", type=Path, metavar="CSV")
    parser.add_argument("--out", required=True, type=Path, metavar="PATH")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    """Merge the files named on the command line."""
    parsed = parse_args(argv)
    try:
        rows = merge(parsed.inputs, parsed.out)
    except ValueError as e:
        print(f"csv_merge.py: error: {e}", file=sys.stderr)
        return 1
    print(f"Merged {len(parsed.inputs)} files -> {parsed.out} ({rows} total rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Make three small inputs to try it on:

```bash
python -c "
from pathlib import Path
for n in ('q1', 'q2', 'q3'):
    Path(f'{n}.csv').write_text('order_id,customer,amount\n' + f'{n.upper()}-0001,Ada,10.00\n', encoding='utf-8')
"
python csv_merge.py q1.csv q2.csv q3.csv --out year.csv
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-06-file-io-exceptions/homework/problem-02-csv-merger.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The command line is a list of input CSV paths plus a required `--out`
   path, parsed with `argparse`.
2. Every input's header is compared against the first input's header
   **before** the output file is opened.
3. A disagreement raises `ValueError` with a message naming both files
   and both headers.
4. On success the output holds the shared header plus a `source` column,
   then every data row from every input in order.
5. Each row's `source` is its input file's name without the extension.
6. Every `csv` file is opened with `newline=""`.
7. The summary line reports the number of files and the number of data
   rows.
8. Every function has type hints and a docstring.

## Constraints

- **Validate before you open the output.** `"w"` truncates the instant
  it is called, and there is no undo. Read every header first, compare
  them, and only then open `--out`. This is the requirement that shapes
  the program, and the way to check it is to run a failing merge and
  confirm the output file does not exist afterwards.
- **`newline=""` on every `csv` open, reading and writing.** The `csv`
  module handles line endings itself. Leave it off the reader and a
  quoted field containing a newline gets split into two rows. Leave it
  off the writer and, on Windows, the module's `\r\n` is translated
  again into `\r\r\n`, so every other row comes out blank in a
  spreadsheet.
- **`path.stem`, not `path.name`.** `Path("q1.csv").stem` is `"q1"`;
  `.name` is `"q1.csv"`. The brief says "without extension".
- **`--out` is a named flag, not a positional argument.** With
  `nargs="+"` on the inputs, `argparse` has no way to tell where the
  greedy list of inputs ends and a positional output begins. The flag
  removes the ambiguity, which is exactly why the brief writes the
  command that way.
- **Stream, do not slurp.** Read one row, write one row. Collecting
  every row of the year into a list first is shorter to read and holds
  the entire dataset in memory for no gain.

## Expected output

The shipped answer runs its own demo when you give it no arguments, so
it works from a clean checkout. It builds four CSV files in a scratch
folder — three that agree and one that does not — merges the first
three, prints the header and first row of the result, then tries a merge
that must fail:

```bash
$ python problem-02-csv-merger-solution.py
```

```text
Merged 3 files -> year.csv (842 total rows)
order_id,customer,amount,source
Q1-0000,Customer 0,757.11,q1
exit code 1, year2.csv created: False
```

The brief's example prints a real arrow, `→`, and this answer prints
`->`. That is a deliberate change and it is worth two minutes — the
Under the hood block below shows exactly what the pretty one does on a
console that cannot encode it.

Read the last line as the proof it is. The second merge stopped on the
header mismatch, returned 1, and `year2.csv` was **never created**. That
is the requirement the brief cares about most.

The complaint itself went to stderr, where complaints belong:

```console
csv_merge.py: error: header mismatch: q1.csv has ['order_id', 'customer', 'amount'] but q4-bad.csv has ['order_id', 'customer', 'total']
```

`280 + 300 + 262 = 842`, and the amounts are the same on every machine
because the demo seeds the random number generator before it starts.

## Steps

1. Activate your Week 6 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `csv_merge.py`. Make the three small inputs shown
   under **Starter** and run it. It reports `0 total rows` — the header
   is written and the rows `TODO` is empty.
3. Fill in the loop in `merge`. `csv.DictReader(src)` gives you one dict
   per row keyed by the header names; set `row[SOURCE_COLUMN] =
   path.stem`, `writer.writerow(row)`, and add one to `rows_written`.
4. Run it. Open `year.csv` and check the `source` column says `q1`,
   `q2`, `q3` in the right places.
5. Now break it on purpose. Make a fourth file whose third column is
   called `total`:

   ```bash
   python -c "
   from pathlib import Path
   Path('q4-bad.csv').write_text('order_id,customer,total\nQ4-0001,Bob,9.99\n', encoding='utf-8')
   "
   python csv_merge.py q1.csv q4-bad.csv --out year2.csv
   ```

   With `common_header` still a stub it happily writes a broken file.
6. Fill in the two `TODO`s in `common_header`. Run the same command
   again. You want a one-line complaint, exit code 1, and **no**
   `year2.csv`:

   ```bash
   python csv_merge.py q1.csv q4-bad.csv --out year2.csv
   echo "exit=$?"
   ls year2.csv
   ```

7. Count the merged rows independently, so you are not just trusting
   your own counter:

   ```bash
   python -c "import csv; print(sum(1 for _ in csv.DictReader(open('year.csv', newline='', encoding='utf-8'))))"
   ```

8. Compare against **The Solution**, work down the acceptance checklist,
   and commit: `git add homework/csv_merge.py` then
   `git commit -m "Week 6 homework: CSV merger"`.

## The Solution

```python
"""Homework 2 — CSV merger.

Concatenates several CSV files that share one header into a single output file,
adding a `source` column holding each row's originating filename (no extension).

    python csv_merge.py q1.csv q2.csv q3.csv --out year.csv

Run it with no arguments and it builds its own three quarters of orders in a
scratch folder first, so the download works from a clean checkout with nothing
set up.

Save your own copy as ``csv_merge.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import sys
import tempfile
from pathlib import Path

SOURCE_COLUMN = "source"

#: The spec's example prints U+2192 RIGHTWARDS ARROW here. This answer prints
#: ASCII instead, so the summary line is the same bytes on every console. The
#: page beside this file explains what goes wrong with the pretty one.
ARROW = "->"


def read_header(path: Path) -> list[str]:
    """Return the header row of *path*, or raise ValueError if there is none.

    Args:
        path: The CSV file to inspect.

    Returns:
        The header row as a list of column names.

    Raises:
        ValueError: If the file is empty and so has no header row.
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f), None)
    if header is None:
        raise ValueError(f"{path} is empty: no header row to merge")
    return header


def common_header(paths: list[Path]) -> list[str]:
    """Return the shared header, or raise ValueError naming the first mismatch.

    Runs before the output file is opened, so a mismatch leaves the filesystem
    exactly as it was.

    Args:
        paths: The input files, in the order they will be merged.

    Returns:
        The header every input agrees on.

    Raises:
        ValueError: If two inputs disagree, or the first already has a
            ``source`` column.
    """
    reference = read_header(paths[0])
    if SOURCE_COLUMN in reference:
        raise ValueError(
            f"{paths[0]} already has a {SOURCE_COLUMN!r} column; "
            "merging would produce two columns with the same name"
        )
    for path in paths[1:]:
        header = read_header(path)
        if header != reference:
            raise ValueError(
                f"header mismatch: {paths[0]} has {reference} "
                f"but {path} has {header}"
            )
    return reference


def merge(paths: list[Path], out_path: Path) -> int:
    """Merge *paths* into *out_path*. Return the number of data rows written.

    Args:
        paths: The input files.
        out_path: The file to create.

    Returns:
        How many data rows were written, not counting the header.
    """
    header = common_header(paths)
    fieldnames = [*header, SOURCE_COLUMN]
    rows_written = 0

    with out_path.open("w", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as src:
                for row in csv.DictReader(src):
                    row[SOURCE_COLUMN] = path.stem
                    writer.writerow(row)
                    rows_written += 1
    return rows_written


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Turn the command line into an inputs list and an output path.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        A namespace with ``inputs`` and ``out``.
    """
    parser = argparse.ArgumentParser(
        prog="csv_merge.py",
        description="Concatenate CSV files that share a header.",
    )
    parser.add_argument("inputs", nargs="+", type=Path, metavar="CSV")
    parser.add_argument("--out", required=True, type=Path, metavar="PATH")
    return parser.parse_args(argv)


def _write_quarter(path: Path, prefix: str, rows: int) -> None:
    """Write one sample quarter of orders to *path*.

    Args:
        path: The CSV file to create.
        prefix: The two-letter order-id prefix, such as ``Q1``.
        rows: How many data rows to write.
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "customer", "amount"])
        for i in range(rows):
            writer.writerow(
                [
                    f"{prefix}-{i:04d}",
                    f"Customer {i % 40}",
                    f"{random.randint(500, 90000) / 100:.2f}",
                ]
            )


def _demo() -> int:
    """Build four sample CSV files in a scratch folder and merge them.

    Shows both paths the problem cares about: three files that agree merge
    cleanly, and a fourth whose header disagrees stops the run before the
    output file is created. The scratch folder is a temporary directory this
    function makes and deletes, so nothing has to be placed by hand.

    Returns:
        Always 0. Both demonstrated outcomes are the intended ones.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="csv_merge_") as scratch:
        try:
            os.chdir(scratch)
            # A fixed seed makes the amounts the same on every machine, so the
            # sample row printed below is something you can compare against.
            random.seed(6)
            _write_quarter(Path("q1.csv"), "Q1", 280)
            _write_quarter(Path("q2.csv"), "Q2", 300)
            _write_quarter(Path("q3.csv"), "Q3", 262)
            with Path("q4-bad.csv").open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["order_id", "customer", "total"])
                writer.writerow(["Q4-0000", "Customer 1", "10.00"])

            main(["q1.csv", "q2.csv", "q3.csv", "--out", "year.csv"])
            with Path("year.csv").open("r", encoding="utf-8", newline="") as f:
                for line in list(f)[:2]:
                    print(line.rstrip("\r\n"))

            code = main(["q1.csv", "q4-bad.csv", "--out", "year2.csv"])
            print(f"exit code {code}, year2.csv created: {Path('year2.csv').exists()}")
        finally:
            os.chdir(home)
    return 0


def main(argv: list[str] | None = None) -> int:
    """Merge the files named on the command line, or run the demo if there are none.

    Args:
        argv: Command-line arguments, without the program name. ``None`` means
            read them from ``sys.argv``.

    Returns:
        The process exit code.
    """
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return _demo()
    parsed = parse_args(args)
    try:
        rows = merge(parsed.inputs, parsed.out)
    except ValueError as e:
        print(f"csv_merge.py: error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"csv_merge.py: error: no such file: {e.filename}", file=sys.stderr)
        return 1
    print(f"Merged {len(parsed.inputs)} files {ARROW} {parsed.out} ({rows} total rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Why it works.**

**`common_header(paths)` is the first line of `merge`, and that is the
whole design.** Every header is read and compared while the output path
is still untouched. Only then does `out_path.open("w", ...)` run. It
costs a second pass over the first row of each file, and it buys you the
promise the brief made: a failed merge changes nothing on disk.

The alternative — start writing, discover the problem on file three —
leaves a half-merged `year.csv` that looks finished to anybody who did
not read the console.

**`DictReader` plus `DictWriter` do the column matching for you.**
`DictReader` hands you each row as a dict keyed by the header names.
`DictWriter` writes each dict back out in `fieldnames` order. So the
merge lines columns up by *name*, not by position. This answer still
insists the headers match exactly, but if you ever wanted to allow the
same columns in a different order, that is a one-line change to the
comparison and the rows would already come out right.

**`[*header, SOURCE_COLUMN]` appends, so `source` is last.** The
original column order is preserved exactly, and anything that reads the
first three columns by position keeps working.

**The `source`-collision guard.** If an input already has a column
called `source`, adding another gives you a CSV with two identical
headers. `DictReader` reading that file back silently keeps only the
last one, so a column disappears without a word. Three lines to detect
it and refuse is much cheaper than the bug report.

**`newline=""` is on both opens for two different reasons.** On the
reader it stops Python's universal-newline translation from cutting a
quoted, multi-line field into two rows. On the writer it stops Windows
from turning the module's `\r\n` into `\r\r\n`.

**`ARROW` is a constant, and it is ASCII.** The brief's example line has
a real arrow in it. Printing one requires the console you happen to be
attached to to be able to encode it, and plenty of them cannot. A
constant means there is one place to change if you want the pretty
version, and one place to look when somebody asks why it is not there.
The Under the hood block below has the failure in full.

**The demo builds its own data.** `_demo` makes a temporary folder,
changes into it, writes four CSV files, runs both merges, and changes
back out before the folder is deleted. `random.seed(6)` before the
amounts means the sample row is identical on every machine, which is
what lets the page promise a specific number.

## Download and run

Download [problem-02-csv-merger-solution.py](./problem-02-csv-merger-solution.py)
and run it:

```bash
python problem-02-csv-merger-solution.py
```

With no arguments it creates its own quarterly files in a temporary
folder and merges those, so it runs anywhere with nothing set up. Give
it real files and it merges those instead:

```bash
python problem-02-csv-merger-solution.py q1.csv q2.csv q3.csv --out year.csv
```

Save your own copy as `csv_merge.py` in your homework folder, and commit
that one. The longer download name is there so it cannot overwrite your
work.

## Common bugs to catch

- **Opening the output before validating.** This is the direct
  translation of "read each file, write its rows", and it is the most
  likely mistake on this problem:

  ```python
  with out.open("w", encoding="utf-8", newline="") as dst:
      writer = None
      for path in paths:
          with path.open("r", encoding="utf-8", newline="") as src:
              reader = csv.DictReader(src)
              if writer is None:
                  writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
                  writer.writeheader()
              for row in reader:
                  row["source"] = path.stem
                  writer.writerow(row)
  ```

  Two bugs, and the second hides behind the first:

  ```text
  Traceback (most recent call last):
    File "wrong2.py", line 16, in <module>
      writer.writerow(row)
      ~~~~~~~~~~~~~~~^^^^^
    File "...\Lib\csv.py", line 226, in writerow
      return self.writer.writerow(self._dict_to_list(rowdict))
                                  ~~~~~~~~~~~~~~~~~~^^^^^^^^^
    File "...\Lib\csv.py", line 221, in _dict_to_list
      raise ValueError("dict contains fields not in fieldnames: "
                       + ", ".join([repr(x) for x in wrong_fields]))
  ValueError: dict contains fields not in fieldnames: 'source'
  ```

  `fieldnames=reader.fieldnames` forgot to add `source`, and `DictWriter`
  refuses a dict with a key it was not told about — a good default,
  because the alternative is dropping your data in silence. Fix that and
  the deeper bug remains: the output file is already on disk with a
  header in it, written before anything was checked.
- **One `try` around both the checking and the writing.** In the answer
  above that cannot bite, because `common_header` finishes before the
  writer exists. Restructure so both can raise inside the same `try`
  and a genuine `DictWriter` bug reports itself to your user as "header
  mismatch". Keep the checking phase and the writing phase in separate
  scopes.
- **Reading every row into a list first.**

  ```python
  rows = [r for p in paths for r in csv.DictReader(p.open(encoding="utf-8", newline=""))]
  ```

  Correct, shorter, and holds a whole year of orders in memory at once.
  Streaming is two more lines and is flat in memory however big the
  inputs get.
- **Forgetting `newline=""` on the writer.** Nothing crashes. The file
  looks fine in a text editor. Open it in a spreadsheet on Windows and
  there is a blank row between every data row.
- **Using `.name` for the source column.** You get `q1.csv` where the
  brief asked for `q1`. Worth checking, because the header is right and
  the rows are right and only the last column is quietly wrong.

## Under the hood

<details>
<summary>Under the hood — what newline="" actually changes, and why CSV needs it</summary>

There are two separate line-ending translations happening, and
`newline=""` turns off the one that gets in the way.

**Translation one: Python's universal newlines.** When you open a text
file normally, Python converts whatever line ending it finds — `\r\n`,
`\r`, or `\n` — into a plain `\n` on the way in, and converts `\n` back
to the platform's ending on the way out. For ordinary text that is a
kindness. You never have to think about which machine wrote the file.

**Translation two: the `csv` module's own.** `csv` was built to produce
files that a spreadsheet will accept, so it writes `\r\n` itself, by
design, on every platform.

Put those together on Windows and you get the classic bug. `csv` writes
`\r\n`; the file object sees the `\n` and helpfully expands it to
`\r\n`; the file ends up with `\r\r\n`. A spreadsheet reads the extra
`\r` as an empty row.

```text
>>> import csv, io
>>> buf = io.StringIO(newline="")      # no translation, so we see the truth
>>> csv.writer(buf).writerow(["a", "b"])
>>> buf.getvalue()
'a,b\r\n'
```

`newline=""` on the open says "do not translate anything, in either
direction — the `csv` module is handling it".

On the reading side the reason is different and sharper. A CSV field can
legally contain a newline, if it is quoted:

```text
id,note
1,"first line
second line"
```

That is two rows, not three. The `csv` reader knows it, because it
tracks the quoting. But if the *file object* has already chopped the
text into lines before `csv` sees it, the reader is handed the pieces
separately and cannot put them back together. `newline=""` hands the
reader the raw stream and lets it do the splitting.

So the rule is easy to remember and has no exceptions worth learning:
**every `open` you hand to the `csv` module gets `newline=""`, reading
or writing.** It is [quiz question 4](../quiz.md#answer-key) this week
for a reason.

</details>

<details>
<summary>Under the hood — why DictWriter refuses a key it was not told about</summary>

`DictWriter` has a `fieldnames` list, and by default it raises if a row
dict contains a key that is not in it:

```text
ValueError: dict contains fields not in fieldnames: 'source'
```

That looks strict. It is deliberate, and the alternative is worse. A CSV
row is a fixed number of columns in a fixed order. If `DictWriter`
quietly dropped unknown keys, adding a field to your record and
forgetting to add it to `fieldnames` would produce a file that is
perfectly well-formed and missing your data. You would find out weeks
later.

You can ask for the loose behaviour explicitly:

```python
writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
```

Now unknown keys are dropped without complaint. That is occasionally
what you want — writing a summary CSV from records that carry more
fields than you are reporting — and the point is that you had to say so.

The mirror-image setting is for keys that are *missing*:

```python
writer = csv.DictWriter(f, fieldnames=cols, restval="")
```

A row that has no `amount` key writes an empty cell instead of raising.
Without `restval` the default fill is `None`, which lands in the file as
the empty string anyway — but only because `csv` calls `str` on it. Set
`restval` explicitly if the blank matters to whoever reads the file.

And on the reading side, `DictReader` has the same pair of problems in
reverse: a row with more fields than the header collects the leftovers
under the key `None`, and a row with fewer gets `None` as the value.
Neither raises. If your data might be ragged, count the fields yourself.

</details>

<details>
<summary>Under the hood — why the summary line prints -> instead of the arrow</summary>

The brief's example ends with a real arrow:

```text
Merged 3 files → year.csv (842 total rows)
```

That character is U+2192. Writing it to a terminal means encoding it,
and what it gets encoded *into* is not up to your program. It is
whatever the console says it is.

On a Windows console still using the legacy code page, that is cp1252,
and cp1252 has no arrow at all:

```text
>>> "→".encode("cp1252")
UnicodeEncodeError: 'charmap' codec can't encode character '→' in position 0: character maps to <undefined>
```

So the last line of a run that did all its work correctly crashes on the
punctuation. You can force the stream to UTF-8:

```python
sys.stdout.reconfigure(encoding="utf-8")
```

and that fixes the crash — while creating a subtler problem. Now your
program emits UTF-8 bytes at whoever is listening, and if that is
another program decoding with cp1252, the arrow arrives as three
characters:

```text
Merged 3 files â†’ year.csv (842 total rows)
```

Those are the UTF-8 bytes `E2 86 92` read one at a time as cp1252. This
has a name — **mojibake** — and it is what almost every encoding bug
you will ever see looks like.

The general shape of the problem: **a string in memory has no encoding.
Bytes have an encoding. Every time text crosses a boundary — to a file,
to a terminal, to a pipe, over a network — somebody chooses one, and if
the two ends choose differently, you get mojibake.**

That is exactly why every `open` in this week's answers passes
`encoding="utf-8"` explicitly. Left off, Python picks a default from the
machine's settings, so the same program reads the same file correctly on
your laptop and wrongly in the container.

For a *file* you can insist on UTF-8, because you control both ends. For
a *console* you cannot, so a command-line tool whose output must be
identical everywhere sticks to ASCII in the parts it prints. If you want
the arrow, this is the honest version — ask the stream what it can do,
rather than telling it:

```python
def arrow() -> str:
    """Return the nicest arrow this stdout can actually encode."""
    try:
        "→".encode(sys.stdout.encoding or "ascii")
    except (UnicodeEncodeError, LookupError):
        return "->"
    return "→"
```

Prettier on a modern terminal, plain everywhere else, and never a crash.
The cost is that the output is no longer the same on every machine,
which is why the shipped answer does not do it.

</details>

## Acceptance checklist

- [ ] `python csv_merge.py q1.csv q2.csv q3.csv --out year.csv` prints
      one summary line with the file count and the row count.
- [ ] `year.csv` has the original columns plus `source`, in that order.
- [ ] The `source` values are `q1`, `q2`, `q3` — no `.csv`.
- [ ] The data row count in `year.csv` equals the sum of the inputs'
      data rows.
- [ ] A merge with a mismatched header exits 1 and prints one message
      naming both files and both headers.
- [ ] After that failed merge, the output file **does not exist**.
- [ ] Every `csv` open has `newline=""`.
- [ ] `--out` is a required flag and the inputs use `nargs="+"`.
- [ ] Every function has type hints and a docstring.
- [ ] Committed with a message like `Week 6 homework: CSV merger`.

## Stretch

- **Allow the same columns in a different order.** Compare
  `sorted(header) != sorted(reference)` instead, and let `DictWriter`
  put the columns back in the reference's order. It already does. This
  is a one-line change that only works because you used the dict-based
  reader and writer.
- **Add `--dry-run`.** Check every header, report what would be written,
  and touch nothing. Notice that you already have this for free: the
  validating phase is a separate function.
- **Report per-file row counts.** `Merged q1.csv (280), q2.csv (300),
  q3.csv (262) → year.csv (842)`. Keep the counts in a small dict as you
  go.
- **Write to a temporary file and rename it at the end.** Then even a
  crash halfway through leaves the old `year.csv` intact. That is
  problem 6, and this is the program that wants it.
- **Handle a genuinely huge merge.** Generate a million rows across ten
  files and time it. Then try the list-comprehension version from
  **Common bugs to catch** and watch your memory. The difference between
  streaming and slurping stops being theoretical somewhere around here.

Next: [Homework Problem 3 — JSON Pretty-Printer](./problem-03-json-pretty-printer.md).
