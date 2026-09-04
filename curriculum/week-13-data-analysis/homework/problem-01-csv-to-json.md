# Homework 1 — CSV to JSON converter

> **Topic:** `pd.read_csv`, `to_json(orient="records", indent=2)`, and swapping a file's extension with `pathlib`
> **Lecture:** [01 — NumPy & pandas Basics](../lecture-notes/01-numpy-and-pandas-basics.md)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** a spreadsheet and a web page want the same numbers in two
> different shapes, and somebody has to move them across. That somebody is you,
> roughly once a month, forever. This is the smallest honest version of that
> job: read a table, round the money, write it back out as records.

## The Brief

A CSV file is a table drawn on graph paper. There is one header row of column
names at the top, and every row below it is a line of values separated by
commas. It is compact, and a spreadsheet opens it happily.

JSON is a stack of index cards. Each card holds one row, and on the card every
value is written next to its own label — `"product": "Widget"` — so the card
still makes sense if you pick it up on its own. Websites and web APIs almost
always want the stack of cards, because a browser can read a card without
having to remember what the header row said.

Your job is a translator that goes one way: graph paper in, index cards out.
Point it at `data/sales.csv` and it writes `data/sales.json` right beside it,
same name, new extension. It should also accept a `.tsv` file — the same idea
but with tab characters instead of commas as the separator — and it should
round every decimal column to two places before writing, so a price never
lands in the JSON as `9.994999999999999`.

## Starter

Copy this into `problem-01-csv-to-json.py` in your homework folder.

```python
"""problem-01-csv-to-json.py — convert a delimited text file to JSON records.

    python problem-01-csv-to-json.py data/sales.csv    # -> data/sales.json
    python problem-01-csv-to-json.py data/sales.tsv    # -> data/sales.json
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

SEPARATORS = {".csv": ",", ".tsv": "\t"}


def read_table(path: Path) -> pd.DataFrame:
    """Read a .csv or .tsv into a DataFrame, choosing the separator by suffix."""
    # TODO: look up path.suffix.lower() in SEPARATORS.
    # TODO: raise ValueError if the suffix is not one of the two.
    # TODO: return pd.read_csv(path, sep=<the separator you looked up>)
    ...


def round_numeric(df: pd.DataFrame, places: int = 2) -> pd.DataFrame:
    """Return a copy with every float column rounded to `places` decimals."""
    # TODO: df.select_dtypes("float").columns gives you the float columns.
    # TODO: df.round({column: places, ...}) rounds only those.
    ...


def convert(src: Path) -> Path:
    """Write `src` out as JSON records beside it and return the new path."""
    # TODO: read the table, then round it.
    # TODO: dest = src.with_suffix(".json")
    # TODO: df.to_json(dest, orient="records", indent=2)
    # TODO: return dest
    ...


def main(argv: list[str]) -> int:
    """Convert the file named on the command line. Return an exit code."""
    # TODO: expect exactly one argument, so len(argv) == 2.
    # TODO: complain to sys.stderr and return 1 if the file does not exist.
    # TODO: call convert(), print what you wrote, return 0.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

It runs as pasted and does nothing, which is the correct amount of nothing for
a stub. Fill the TODOs one function at a time, bottom of the file upward.

## Requirements

1. Take the path to a delimited file as a **command-line argument**:
   `python problem-01-csv-to-json.py data/sales.csv`.
2. Read it with `pd.read_csv`.
3. Write JSON to the **same folder, same stem, `.json` extension**, using
   `to_json(orient="records", indent=2)`.
4. Accept `.csv` *and* `.tsv`, reading the tab-separated one with `sep="\t"`.
5. Round every float column to two decimals **before** writing.
6. Reject anything else with a clear message on stderr and a non-zero exit
   code. No traceback.
7. Give the file a top-of-file docstring that states the problem, and type
   every function (`def convert(src: Path) -> Path:`).

## Constraints

- **Take the path from the command line, never hard-code it.** A script with
  `pd.read_csv("C:/Users/me/Desktop/sales.csv")` inside it works exactly once,
  on one machine. The moment you share it, the path is wrong. `sys.argv[1]` is
  the difference between a tool and a note to yourself.
- **Build the output path with `with_suffix`, not string surgery.**
  `str(src).replace(".csv", ".json")` looks fine until the folder is called
  `sales.csv.backup/` — then it rewrites the folder name too.
  `src.with_suffix(".json")` only ever touches the last extension.
- **Round before writing, not after.** JSON stores a number, not a printed
  string, so there is no "format it at the end" step the way there is with an
  f-string. Whatever float is in the frame is what lands on disk. Round it in
  the frame.
- **Round only the float columns.** `df.round(2)` on the whole frame is
  harmless here but sloppy in general: it walks every numeric column including
  integer ID columns, and an ID is not a measurement. Naming the columns says
  what you meant.
- **Errors go to stderr, results go to stdout.** They are two different pipes.
  If you print `error: no such file` to stdout, then
  `python problem-01-csv-to-json.py bad.csv > log.txt` files the error away
  where nobody sees it, and the terminal looks like everything worked.
- **Exit codes are the machine-readable answer.** Return `0` for success and
  `1` for failure from `main`, and hand that to `SystemExit`. Any script that
  runs yours — a shell loop, a scheduled job — reads that number and nothing
  else.

## Expected output

The shipped answer,
[`problem-01-csv-to-json-solution.py`](./problem-01-csv-to-json-solution.py),
runs with no argument as well as with one. Given no argument it builds a small
four-row sample sheet in a throwaway temporary folder, converts it, prints the
JSON, and deletes the folder on the way out — so the download works on a
machine with no data files on it at all. Real captured run:

```text
$ python problem-01-csv-to-json.py
wrote sales.json from sales.csv
[
  {
    "order_id":1001,
    "product":"Widget",
    "region":"North",
    "units":3,
    "unit_price":9.99
  },
  {
    "order_id":1002,
    "product":"Gadget",
    "region":"South",
    "units":1,
    "unit_price":24.5
  },
  {
    "order_id":1003,
    "product":"Widget",
    "region":"East",
    "units":12,
    "unit_price":9.99
  },
  {
    "order_id":1004,
    "product":"Doohickey",
    "region":"North",
    "units":7,
    "unit_price":4.33
  }
]
```

Look at the prices. The sample CSV holds `9.995` and `4.333`, three decimals
each. The JSON holds `9.99` and `4.33`. That is the rounding requirement
firing where you can see it. `24.5` stays `24.5` and not `24.50`, because JSON
stores the *number* twenty-four-and-a-half; trailing zeros are a thing printed
text has and numbers do not.

## Steps

1. Paste the starter and run it. Nothing happens, no traceback. Good.
2. Fill in `read_table` first. Test it on its own by adding a temporary
   `print(read_table(Path("some.csv")))` at the bottom, then delete that line.
3. Fill in `round_numeric`. Print `df.dtypes` next to it once so you can see
   which columns pandas decided were floats and which were integers.
4. Fill in `convert`. Run it, then open the `.json` it produced in a text
   editor. It should be a `[` , a list of `{...}` cards, and a `]`.
5. Fill in `main` last: the argument count, the missing-file check, the exit
   codes.
6. Rename your test file from `.csv` to `.tsv`, replace the commas with tabs,
   and run it again. Same JSON.
7. Feed it a `.txt` file on purpose and confirm you get one clear line on
   stderr and exit code 1, not a wall of traceback. On macOS or Linux, check
   with `echo $?`; in PowerShell, `$LASTEXITCODE`.

## The Solution

```python
"""hw-01-csv-to-json.py — convert a delimited text file to JSON records.

Usage:
    python hw-01-csv-to-json.py data/sales.csv        # -> data/sales.json
    python hw-01-csv-to-json.py data/sales.tsv        # -> data/sales.json

Bonus behaviour: .tsv input is read with a tab separator, and every numeric
column is rounded to two decimals before writing.

Run with no argument (as the automated check does) it builds a sample sheet in a
throwaway temporary directory, converts it, prints the JSON, and cleans up — so
the download runs anywhere with nothing set up beforehand.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd

SEPARATORS = {".csv": ",", ".tsv": "\t"}

#: A sample sheet with three-decimal prices, so the rounding bonus visibly fires.
SAMPLE_CSV = (
    "order_id,product,region,units,unit_price\n"
    "1001,Widget,North,3,9.995\n"
    "1002,Gadget,South,1,24.5\n"
    "1003,Widget,East,12,9.995\n"
    "1004,Doohickey,North,7,4.333\n"
)


def read_table(path: Path) -> pd.DataFrame:
    """Read a .csv or .tsv into a DataFrame, choosing the separator by suffix."""
    suffix = path.suffix.lower()
    if suffix not in SEPARATORS:
        raise ValueError(f"expected a .csv or .tsv file, got {path.suffix!r}")
    return pd.read_csv(path, sep=SEPARATORS[suffix])


def round_numeric(df: pd.DataFrame, places: int = 2) -> pd.DataFrame:
    """Return a copy with every float column rounded to `places` decimals."""
    return df.round({c: places for c in df.select_dtypes("float").columns})


def convert(src: Path) -> Path:
    """Write `src` out as JSON records next to it and return the new path."""
    df = round_numeric(read_table(src))
    dest = src.with_suffix(".json")
    df.to_json(dest, orient="records", indent=2)
    return dest


def main(argv: list[str]) -> int:
    if len(argv) == 2:
        src = Path(argv[1])
        if not src.is_file():
            print(f"error: no such file: {src}", file=sys.stderr)
            return 1
        try:
            dest = convert(src)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(f"wrote {dest} ({dest.stat().st_size:,} bytes)")
        return 0

    # No argument: build the sample in a temp dir so the download runs anywhere.
    with tempfile.TemporaryDirectory() as workspace:
        src = Path(workspace) / "sales.csv"
        src.write_text(SAMPLE_CSV, encoding="utf-8")
        dest = convert(src)
        print(f"wrote {dest.name} from {src.name}")
        print(dest.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

**The separator lives in a lookup table, so adding a format is one line.**
`SEPARATORS = {".csv": ",", ".tsv": "\t"}` maps an extension to the character
that splits the columns. `read_table` looks the suffix up, and if it is not in
the table it raises `ValueError` with the suffix in the message. The
alternative — an `if` for CSV, an `elif` for TSV, an `else` that raises — is
three times the code and grows a new branch every time somebody hands you a
semicolon-separated export from a European spreadsheet. With the table, that
export costs you `".csv2": ";"` and nothing else. `path.suffix.lower()` is
there because Windows will happily hand you `SALES.CSV`.

**`with_suffix` swaps the extension and nothing else.**
`Path("data/sales.csv").with_suffix(".json")` gives `data/sales.json` — same
folder, same stem, new tail. It works on the path *object*, so it understands
that `data/` is a folder and `.csv` is an extension, which a `str.replace` call
does not. That is why the output lands beside the input automatically, with no
folder-joining code at all.

**`select_dtypes("float")` picks the columns that can actually hold a
fraction.** `round_numeric` builds `{c: places for c in ...}` — a small
dictionary saying "round this column to 2, and this one" — and hands it to
`df.round`. In the sample, `unit_price` is a float and gets rounded;
`order_id` and `units` are integers and are left alone. `df.round(2)` would
have produced the same JSON here, but it says something you did not mean: that
an order number is a quantity worth rounding.

**`orient="records"` is the shape a web app expects.** It writes a list of
objects, one per row, each with its column names spelled out — the stack of
index cards. `indent=2` makes it readable by a human instead of one enormous
line. Other orientations exist and produce completely different files from the
same frame; there is an Under the hood block below that lays them side by side.

**`main` reads the command line, but the file still runs with nothing on it.**
`len(argv) == 2` means "the script name plus exactly one path". When that
holds, the path is checked with `is_file()`, converted, and the result printed
with its size. When it does not hold, the fallback runs: a
`tempfile.TemporaryDirectory()` block writes `SAMPLE_CSV` to disk, converts it,
prints the JSON, and the `with` block deletes the whole directory when it ends,
whether or not anything went wrong. That is why the download prints something
useful on a fresh machine and still leaves no litter behind.

**Failures return 1 and say why on stderr.** A missing file and a bad extension
each print one line to `sys.stderr` and return `1`, which
`raise SystemExit(main(sys.argv))` turns into the process's exit code. No
traceback, because a traceback is a message to the person who wrote the program
and this message is for the person running it.

## Run it

Copy the worked answer on this page into `problem-01-csv-to-json.py` and run it:

```bash
python -m pip install pandas
python problem-01-csv-to-json.py
```

With no argument it makes its own sample sheet and prints the JSON. With a
path it converts that file:

```bash
python problem-01-csv-to-json.py data/sales.csv
```

The `-solution` suffix keeps it from colliding with your own
`problem-01-csv-to-json.py`. Its docstring still carries the older `hw-01-`
filename from the original brief; the code is what matters and it is unchanged.

## Common bugs to catch

- **`IndexError: list index out of range`.** You reached for `sys.argv[1]`
  before checking that it exists. Check the length first, always.
- **`FileNotFoundError: [Errno 2] No such file or directory: 'sales.csv'`.**
  The path is relative to where you *ran* the command, not to where the script
  lives. `cd` into the folder, or pass the full path.
- **`ParserError: Error tokenizing data. C error: Expected 1 fields in line 2,
  saw 5`.** You read a tab-separated file with the default comma separator, so
  pandas saw one enormous column. Pass `sep="\t"`.
- **The JSON is one unreadable line.** You left out `indent=2`.
- **The JSON is a dictionary of columns, not a list of rows.** You left out
  `orient="records"`, so you got the default `"columns"` shape.
- **`ValueError: Expected object or value` when something else reads your
  JSON.** You wrote to the path but never checked it. Open the file. If it is
  empty, `to_json` was given a path it could not write to.
- **A price reads `9.994999999999999`.** You rounded after writing, or not at
  all. Round the frame before `to_json`.
- **`AttributeError: 'str' object has no attribute 'with_suffix'`.** `sys.argv`
  hands you strings. Wrap it: `src = Path(argv[1])`.
- **The output file lands in the folder you ran the command from, not next to
  the input.** You built the destination from the file *name* instead of from
  the whole path.

## Under the hood

<details>
<summary>Under the hood — the five orient values, and why records won</summary>

`to_json` can write the same frame in several shapes. Take two rows and two
columns and watch what each one does:

| `orient` | What comes out |
|---|---|
| `"records"` | `[{"a":1,"b":"x"},{"a":2,"b":"y"}]` — one object per row |
| `"columns"` | `{"a":{"0":1,"1":2},"b":{"0":"x","1":"y"}}` — the default |
| `"index"` | `{"0":{"a":1,"b":"x"},"1":{"a":2,"b":"y"}}` — keyed by row label |
| `"split"` | `{"columns":[...],"index":[...],"data":[[...],[...]]}` |
| `"values"` | `[[1,"x"],[2,"y"]]` — no names at all |

`"records"` wins for handing data to another program because each row is
self-describing: a reader can take one object and know what every value means
without holding the rest of the file in mind. It is also what nearly every web
API returns, so a JavaScript front end can loop over it directly.

`"split"` is the compact one — column names are stored once instead of once per
row — and it round-trips back into pandas exactly. `"values"` is the smallest
and the most fragile: swap two columns upstream and nothing complains, the
numbers just quietly change meaning.

The trip back is `pd.read_json(path, orient="records")`. Reading with the wrong
orient does not usually raise; it usually gives you a frame that is *shaped*
wrong, which is worse.

</details>

<details>
<summary>Under the hood — what "float column" means, and why 9.995 is not 9.995</summary>

`select_dtypes("float")` asks pandas which columns are stored as `float64` —
64 binary digits split into a sign, an exponent, and a fraction. That format
cannot represent most decimal fractions exactly, in the same way base ten
cannot write one third exactly. `9.995` in a `float64` is really
9.99499999999999957..., very slightly under.

This has a visible consequence: rounding `9.995` to two places gives `9.99`,
not `10.00`, because the stored number genuinely is below the halfway point.
That is not a pandas bug and it is not Python being careless — it is what the
hardware holds. You can see it yourself with `print(f"{9.995:.20f}")`.

If you need decimal arithmetic that behaves the way money is supposed to,
Python has `decimal.Decimal`, which stores digits in base ten and rounds the
way an accountant expects. It is slower and pandas does not vectorise it, so
for analysis work the usual rule holds instead: keep floats, round once, and
never compare two floats with `==`.

</details>

<details>
<summary>Under the hood — TemporaryDirectory, and why the demo leaves nothing behind</summary>

`tempfile.TemporaryDirectory()` makes a real folder in the operating system's
scratch space — `C:\Users\you\AppData\Local\Temp\tmp8f3k2q` on Windows,
`/tmp/tmp8f3k2q` on macOS and Linux — and hands you its path. Used as a
`with` block, it deletes the folder and everything inside it when the block
ends. Not when the program ends; when the *block* ends, including on the way
out of an exception.

That is why the shipped answer can write a CSV, convert it, read the JSON back
and print it, and still leave your disk exactly as it found it. The pattern is
worth stealing for tests: any code that touches the filesystem can be exercised
for real, on real files, without a cleanup step you might forget.

Its sibling `tempfile.NamedTemporaryFile()` does the same for a single file,
with one Windows wrinkle — the file cannot be reopened by name while it is
still open, so on Windows you usually want `delete=False` and a manual unlink,
or a temporary directory like this one.

</details>

## Acceptance checklist

- [ ] `python problem-01-csv-to-json.py data/sales.csv` writes
      `data/sales.json` and prints what it wrote.
- [ ] The JSON opens as a list of objects, one per row, indented.
- [ ] The same script handles a `.tsv` file with tabs.
- [ ] Every float column reads with at most two decimals.
- [ ] A missing file gives one line on stderr and exit code 1, no traceback.
- [ ] There is no hard-coded path anywhere in the file.
- [ ] The file has a docstring at the top and typed function signatures.
- [ ] Committed to Git with a message like
      `Add Week 13 homework 1: CSV to JSON`.

## Stretch

- Add `--indent N` and `--orient records|split|values` with `argparse`, so the
  caller picks the shape instead of you.
- Accept a folder and convert every `.csv` and `.tsv` inside it, printing one
  line per file and a count at the end.
- Add `--lines`, which switches to `to_json(orient="records", lines=True)` —
  one JSON object per line, no surrounding list. That is the JSON Lines format
  log pipelines eat, and it streams: a reader can handle a ten-gigabyte file
  one line at a time.
- Refuse to overwrite an existing `.json` unless `--force` is passed. Silently
  clobbering somebody's file is the one bug that loses work.
- Round-trip it: read your JSON back with `pd.read_json`, compare to the
  original frame with `df.equals(other)`, and find out what the trip cost you.

When your converter handles both extensions, move on to
[Homework 2 — Missing-data report](./problem-02-missing-data-report.md).
