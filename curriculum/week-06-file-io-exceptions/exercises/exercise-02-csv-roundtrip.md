# Exercise 2 — CSV Roundtrip

> **Topic:** reading a table with `DictReader`, keeping the rows you want, writing them back with `DictWriter`
> **Lecture:** [02 — CSV and JSON](../lecture-notes/02-csv-and-json.md)
> **Difficulty:** Easy
> **Target time:** 25 minutes
> **Why this one:** read a table, keep the rows that matter, write a smaller table. That is a working week of data plumbing squeezed into forty lines. It is also where you learn, permanently, that a value from a CSV file is a piece of text until you turn it into a number yourself.

## The Brief

Your org tracks volunteer mentor hours for each chapter in a spreadsheet, and
somebody exports it to CSV once a month. Mentors who logged ten hours or more
get a certificate. The person who prints the certificates would like a file
holding only those people — same columns, fewer rows.

**CSV** stands for comma-separated values, and it is exactly what it sounds
like: a plain text file where one line is one row and commas divide the
columns. The first line is usually the header, naming the columns.

You are writing the filter. Read the export, keep every row whose `hours` value
is at least ten, and write those rows into a new file with the same header. The
export itself is never touched, so running the script again next month costs
you nothing.

One of the mentors is recorded as `"Chen, Lin"` — a comma inside a name, inside
a file whose whole job is dividing things at commas. That is not a trick
somebody set up to catch you. That is Tuesday. Names contain commas; so do
addresses, job titles and the notes column of every support ticket ever filed.
CSV handles it by putting quote marks around any value that contains the
divider, and a real CSV reader knows to look for them.

That row is why this exercise forbids `.split(",")`.

**Roundtrip** is the word for what you are proving: a value goes out through
the writer, comes back in through the reader, and arrives unchanged. If
`Chen, Lin` is still one name at the end, your filter is genuinely correct
rather than accidentally correct.

## Starter

First, the data. Create `data/mentor-hours.csv` with exactly this content,
quote marks included:

```text
name,chapter,hours,role
Ada Lovelace,Lagos,12,mentor
Grace Hopper,Manila,4,mentor
"Chen, Lin",Lagos,19,lead
Katherine Johnson,Bogota,7,mentor
Alan Turing,Manila,0,observer
Mary Jackson,Bogota,25,lead
```

Open it in a text editor to check it, not in a spreadsheet. A spreadsheet will
open it, decide it knows better, and rewrite the quoting when you save.

Now the code. Save this as `exercise-02-csv-roundtrip.py`:

```python
"""exercise-02-csv-roundtrip.py — filter a CSV export into a smaller CSV.

Reads data/mentor-hours.csv, keeps every mentor with at least MIN_HOURS logged,
and writes the surviving rows to data/mentor-hours-certified.csv.
"""

import csv
from pathlib import Path

DATA = Path(__file__).parent / "data"
SOURCE = DATA / "mentor-hours.csv"
TARGET = DATA / "mentor-hours-certified.csv"
MIN_HOURS = 10


def qualifies(row: dict[str, str], min_hours: int) -> bool:
    """Return True when *row* logged at least *min_hours* hours.

    Every value in *row* is a string, because that is all a CSV holds.
    """
    # TODO: convert row["hours"] to an int and compare it to min_hours
    return False


def filter_rows(source: Path, target: Path, min_hours: int) -> tuple[int, int]:
    """Copy the qualifying rows of *source* into *target*.

    Returns:
        A ``(rows_read, rows_kept)`` pair.
    """
    rows_read = 0
    rows_kept = 0
    with source.open("r", encoding="utf-8", newline="") as src, \
         target.open("w", encoding="utf-8", newline="") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=reader.fieldnames or [])
        # TODO: write the header row
        for row in reader:
            rows_read += 1
            # TODO: write the row when it qualifies, and count it
    return rows_read, rows_kept


def main() -> None:
    """Run the filter and report the counts."""
    read, kept = filter_rows(SOURCE, TARGET, MIN_HOURS)
    print(f"Read {read} rows from {SOURCE.name}")
    print(f"Kept {kept} rows at or above {MIN_HOURS} hours")
    print(f"Wrote {TARGET.name}")


if __name__ == "__main__":
    main()
```

Four names in that starter worth knowing before you begin.

**`csv.DictReader`.** Wrap it around an open file and it hands you one **dict**
per row, where the keys are the column names from the header. `row["hours"]`
instead of `row[2]`.

**`csv.DictWriter`.** The mirror image. You tell it the column names once, then
hand it dicts and it writes rows. It puts quote marks in for you whenever a
value needs them.

**`fieldnames`.** The list of column names. The reader learns them from the
header line; the writer needs to be told them, which is why the starter passes
the reader's list straight to the writer.

**`newline=""`.** An instruction to `open` that has nothing to do with
encodings and everything to do with the `csv` module. It is important enough
that it has its own constraint below and its own **Under the hood** block.

## Requirements

1. The output starts with the header row `name,chapter,hours,role` — the same
   column names, in the same order as the input.
2. Exactly three rows follow that header: Ada Lovelace, Chen Lin, Mary Jackson.
3. `"Chen, Lin"` appears in the output **still wrapped in quote marks**. You do
   not type those quotes. `csv` adds them because the value contains the
   divider.
4. `rows_read` counts data rows only — six, not seven. `DictReader` swallows
   the header before your loop ever starts.
5. The boundary is inclusive: a mentor with exactly `10` hours qualifies.
   Nobody in the sample sits on `10`, so add a row with `10` in it, prove it
   qualifies, then take it out again. A boundary you have never watched fire is
   a boundary you have not tested.
6. The three printed lines are exactly `Read 6 rows from mentor-hours.csv`,
   `Kept 3 rows at or above 10 hours` and `Wrote mentor-hours-certified.csv`.
7. `data/mentor-hours.csv` is unchanged when the run finishes.

## Constraints

- **Use the `csv` module. Never `.split(",")`.** The `"Chen, Lin"` row has four
  values, but splitting its text at every comma gives you five pieces, because
  the comma inside the quote marks is *data*. Every column after the name then
  shifts one place to the right, `hours` becomes `Lagos`, and `int("Lagos")`
  raises. The `csv` module knows the quoting rules. `str.split` has never heard
  of them.
- **Pass `newline=""` to `open()` on both files.** The `csv` module writes its
  own line endings. If Python's text layer also translates newlines, Windows
  turns each one into `\r\r\n` and every second line of your output file is
  blank. On the reading side, `newline=""` is what lets a line break *inside* a
  quoted value reach the parser in one piece instead of being mistaken for the
  end of the row. Both are the documented way to open a file for `csv`, and
  both are invisible until they are not.
- **Pass `encoding="utf-8"` to both files.** Mentor names are not all ASCII. A
  CSV that opens perfectly on your laptop and comes out as nonsense on somebody
  else's is the classic sign of a missing `encoding` argument.
- **Use `DictReader` and `DictWriter`, not `reader` and `writer` with numbers.**
  `row["hours"]` still works when somebody reorders the columns in next month's
  export. `row[2]` quietly starts reading the wrong column and tells nobody.
- **Convert with `int(row["hours"])` yourself.** Every value `DictReader` gives
  you is a `str`. Comparing `"7" >= 10` does not compare numbers — it raises
  `TypeError`. Python refuses to guess, and that refusal is a feature: guessing
  is how you end up with a filter that quietly keeps the wrong rows.
- **Write to a different path than you read from.** Opening the source in `"w"`
  mode empties it to zero bytes *before* your reader gets a single row. The
  certificate list is a new file, not an edit of the export.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-csv-roundtrip.py
Read 6 rows from mentor-hours.csv
Kept 3 rows at or above 10 hours
Wrote mentor-hours-certified.csv

--- mentor-hours-certified.csv ---
name,chapter,hours,role
Ada Lovelace,Lagos,12,mentor
"Chen, Lin",Lagos,19,lead
Mary Jackson,Bogota,25,lead

--- read back with DictReader ---
'Ada Lovelace' Lagos 12 mentor
'Chen, Lin' Lagos 19 lead
'Mary Jackson' Bogota 25 lead
```

Your own `exercise-02-csv-roundtrip.py` prints the first three lines. The
shipped file prints the file it wrote and then reads it back, so you can see
both halves of the roundtrip in one run.

The last three lines are the point of the exercise. `repr` puts quote marks
around each name, so you can see where the name starts and stops.
`'Chen, Lin'` came back as **one** string with a comma inside it and no quote
characters in it. The writer added the quotes on the way out; the reader took
them off again on the way in. Those two operations are exact opposites, and
that is what the `csv` module is for.

## Steps

1. Create `data/mentor-hours.csv` with the block above.
2. Save the starter, then fill in `qualifies` first.
3. Test `qualifies` before wiring it up:

   ```bash
   python -c "print(int('19') >= 10, int('4') >= 10)"
   ```

   ```text
   True False
   ```

4. Add the `writer.writeheader()` call. It goes before the loop, and it runs
   once.
5. Fill in the loop body and run: `python exercise-02-csv-roundtrip.py`.
6. Open the output in a text editor. Four lines total, with the quote marks
   still around `"Chen, Lin"`.
7. Read your own output back with a throwaway `DictReader` and print
   `row["name"]` for each row:

   ```bash
   python -c "
   import csv, pathlib
   with pathlib.Path('data/mentor-hours-certified.csv').open(encoding='utf-8', newline='') as f:
       for row in csv.DictReader(f):
           print(repr(row['name']))
   "
   ```

   ```text
   'Ada Lovelace'
   'Chen, Lin'
   'Mary Jackson'
   ```

   If the names come back whole, your roundtrip is real.

8. Now break it on purpose, once, so you never wonder again:

   ```bash
   python -c "print('\"Chen, Lin\",Lagos,19,lead'.split(','))"
   ```

   ```text
   ['"Chen', ' Lin"', 'Lagos', '19', 'lead']
   ```

   Five pieces from a four-value row, with the name torn in half.

## The Solution

```python
"""exercise-02-csv-roundtrip-solution.py — filter a CSV export into a smaller CSV.

Reads a mentor-hours export, keeps every mentor with at least MIN_HOURS logged,
and writes the surviving rows to a second CSV with the same header.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact export the page gives
you, so the download runs on any machine with nothing set up beforehand. It
then reads its own output back to prove the roundtrip. ``qualifies`` and
``filter_rows`` are the whole exercise and know nothing about the harness.

Run it with::

    python exercise-02-csv-roundtrip-solution.py
"""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

MIN_HOURS = 10

#: The export exactly as the exercise page gives it, quotes included. The
#: "Chen, Lin" row is the reason this exercise forbids .split(",").
SAMPLE_EXPORT = (
    "name,chapter,hours,role\n"
    "Ada Lovelace,Lagos,12,mentor\n"
    "Grace Hopper,Manila,4,mentor\n"
    '"Chen, Lin",Lagos,19,lead\n'
    "Katherine Johnson,Bogota,7,mentor\n"
    "Alan Turing,Manila,0,observer\n"
    "Mary Jackson,Bogota,25,lead\n"
)


def qualifies(row: dict[str, str], min_hours: int) -> bool:
    """Return True when *row* logged at least *min_hours* hours.

    Every value in *row* is a string, because that is all a CSV holds.
    """
    return int(row["hours"]) >= min_hours


def filter_rows(source: Path, target: Path, min_hours: int) -> tuple[int, int]:
    """Copy the qualifying rows of *source* into *target*.

    Returns:
        A ``(rows_read, rows_kept)`` pair.
    """
    rows_read = 0
    rows_kept = 0
    with source.open("r", encoding="utf-8", newline="") as src, \
         target.open("w", encoding="utf-8", newline="") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=reader.fieldnames or [])
        writer.writeheader()
        for row in reader:
            rows_read += 1
            if qualifies(row, min_hours):
                writer.writerow(row)
                rows_kept += 1
    return rows_read, rows_kept


def build_sample(folder: Path) -> Path:
    """Write the sample mentor-hours export into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "mentor-hours.csv"
    path.write_text(SAMPLE_EXPORT, encoding="utf-8", newline="")
    return path


def read_back(path: Path) -> None:
    """Parse *path* again and print each row, so the roundtrip is visible."""
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            print(repr(row["name"]), row["chapter"], row["hours"], row["role"])


def main() -> None:
    """Build the sample export, filter it, and read the result back."""
    with tempfile.TemporaryDirectory() as workspace:
        data = Path(workspace) / "data"
        source = build_sample(data)
        target = data / "mentor-hours-certified.csv"

        read, kept = filter_rows(source, target, MIN_HOURS)
        print(f"Read {read} rows from {source.name}")
        print(f"Kept {kept} rows at or above {MIN_HOURS} hours")
        print(f"Wrote {target.name}")

        print()
        print(f"--- {target.name} ---")
        print(target.read_text(encoding="utf-8"), end="")

        print()
        print("--- read back with DictReader ---")
        read_back(target)


if __name__ == "__main__":
    main()
```

**`DictReader` eats the header, and that is why `rows_read` is 6.** Building
the reader consumes nothing. The first time you iterate it, it pulls one line
off the file to learn the column names, then hands you the *second* line as
your first row. So the loop body runs six times over a seven-line file, and
`rows_read` counts mentors — which is what a person means by "how many are in
this export". You never write a "skip the header" line, and you never
accidentally test the header against `min_hours`.

**`reader.fieldnames` is what makes it a roundtrip.** The writer's column names
come from the reader, not from a list you typed out. So the output header *is*
the input header — same names, same order — because of how it is built, not
because you were careful. When somebody adds a `region` column to next month's
export, this script keeps working and keeps the new column.

**The `or []` is not decoration.** `reader.fieldnames` is `None` for a
completely empty file, and `DictWriter` with `fieldnames=None` raises when you
try to write. `or []` turns that into a valid empty header, so an empty input
produces an empty output instead of a traceback. It is a two-character guard
that only matters on the day the upstream export fails, which is the day you
least want to be reading a stack trace.

**`int(row["hours"])`, every single time, because a CSV has exactly one type.**
A CSV file is characters. There is no column type, no schema, no hidden
metadata. The `12` in the file is the two characters `1` and `2`, and
`DictReader` hands it over as the string `"12"`. And strings compare
alphabetically, which is where the damage comes from:

```text
>>> "9" > "10"
True
```

Nine is not greater than ten. `"9"` sorts after `"1"`, so as *text* it is.
Every "my filter kept the wrong rows" bug in a CSV script is that comparison
happening somewhere nobody looked. Convert once, at a named boundary, and the
rest of the function can trust its own numbers.

**`>=` gives the inclusive boundary the brief asked for.** "At least ten hours"
means ten counts.

**`writeheader()` outside the loop, `writerow` inside it.** `DictWriter` knows
the column names from the moment you build it, but it never writes them unless
you ask — because plenty of real pipelines add rows to a file that already has
a header. Call it once, before the loop, and the shape of the code matches the
shape of the file.

**The two paths differ, and that is load-bearing.** Both files are opened by
the same `with` statement, so `"w"` empties the target *before* the reader has
read a byte. Point them at the same file and you have not filtered your export;
you have deleted it.

**About the harness.** `SAMPLE_EXPORT`, `build_sample` and `read_back` exist so
this download runs on a machine where you have created nothing. `build_sample`
writes the same `data/mentor-hours.csv` the page gives you, inside a temporary
folder Python deletes on the way out, and it passes `newline=""` for the same
reason the exercise does — the sample text already contains exactly the line
endings it should have, and translation would add to them. `qualifies` and
`filter_rows` are the exercise and know nothing about any of it.

## Run it

Copy the worked answer on this page into `exercise-02-csv-roundtrip.py` and run it:

```bash
python exercise-02-csv-roundtrip.py
```

It needs no `data/` folder: it writes its own copy of the export into a
temporary directory, filters it, prints the result, reads it back, and cleans
up after itself. The `-solution` in the name keeps it from colliding with your
own `exercise-02-csv-roundtrip.py`.

## Common bugs to catch

- **`TypeError: '>=' not supported between instances of 'str' and 'int'`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 5, in <module>
      if row['hours'] >= 10:
         ^^^^^^^^^^^^^^^^^^
  TypeError: '>=' not supported between instances of 'str' and 'int'
  ```

  You compared `row["hours"] >= min_hours` without `int(...)`. This error is a
  gift: it fires on the first row, loudly, instead of giving you a quietly
  wrong answer later. Compare `row["hours"] >= "10"` — two strings — and there
  is no error at all, `"9"` no longer qualifies, and you lose an afternoon.

- **`ValueError: invalid literal for int() with base 10: 'Lagos'`.**

  ```text
  Ada Lovelace
  Traceback (most recent call last):
    File "wrong.py", line 10, in <module>
      if int(row["hours"]) >= 10:
         ~~~^^^^^^^^^^^^^^
  ValueError: invalid literal for int() with base 10: 'Lagos'
  ```

  You used `.split(",")`. Read what the error says: it tried to turn `'Lagos'`
  into a number, so the chapter ended up in the hours column. Notice that Ada
  printed first — the bug is completely invisible for every row without a comma
  in it, which is exactly how it survives into production.

- **A blank line between every row of the output.**

  ```text
  b'name,chapter,hours,role\r\r\nAda Lovelace,Lagos,12,mentor\r\r\n'
  ```

  You left `newline=""` off the target. `\r\r\n` — the `csv` module wrote
  `\r\n`, and the text layer translated the `\n` inside it into another `\r\n`.
  Seven lines where the checklist wants four. This is the most common `csv` bug
  on Windows and it never announces itself.

- **The output has no header.** You forgot `writer.writeheader()`. `DictWriter`
  knows the field names and still will not write them until you say so.

- **`ValueError: dict contains fields not in fieldnames: 'certified'`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 12, in <module>
      w.writerow(row)
      ~~~~~~~~~~^^^^^
    File "...\Lib\csv.py", line 221, in _dict_to_list
      raise ValueError("dict contains fields not in fieldnames: "
                       + ", ".join([repr(x) for x in wrong_fields]))
  ValueError: dict contains fields not in fieldnames: 'certified'
  ```

  You added a computed key to the row before writing it. `DictWriter` checks
  that a row's keys are all declared columns, which is the check that stops a
  typo'd key from vanishing into nothing. If you want the column, declare it:
  `fieldnames=[*reader.fieldnames, "certified"]`. If you do not, keep it out of
  the dict — and remember that `row` is a real dict you are changing, so the
  extra key stays there for the rest of that row's life.

- **`AttributeError: 'list' object has no attribute 'keys'`.** You built a
  `DictWriter` and handed `writerow` a list. `DictWriter` wants dicts;
  `csv.writer` wants lists. Pick one pair and stay inside it.

- **Four rows kept instead of three.** You compared the length of the string,
  or filtered on `role` instead of `hours`, or counted the header. Print each
  row inside the loop and read the four you actually kept.

- **The input file is now empty.** You opened `SOURCE` in `"w"` mode somewhere.
  There is no undo. Recreate it from the block above and keep the two paths
  distinct.

## Under the hood

<details>
<summary>Under the hood — why csv needs newline="" and nothing else will do</summary>

Text mode does two jobs: it translates characters to and from bytes, and it
translates line endings. The `csv` module wants the first job and absolutely
not the second, and `newline=""` is how you ask for that split.

**Why `csv` writes `\r\n` itself.** The CSV format is written down, in RFC
4180, and the record separator it specifies is `\r\n`. The `csv` module obeys
the format rather than the operating system, so `csv.writer` emits `\r\n`
whatever machine you are on. That is deliberate: a CSV is usually a file you
hand to somebody else.

Now watch what happens when the text layer helps:

```text
>>> import csv, io
>>> buffer = io.StringIO()
>>> csv.writer(buffer).writerow(["a", "b"])
5
>>> buffer.getvalue()
'a,b\r\n'
```

That `\r\n` is one string containing a `\n`. Send it through a file opened in
default text mode on Windows and the translation fires on the `\n` inside it:

```text
\r  +  \n   ->   \r  +  \r\n
```

Which is exactly what lands on the disk:

```text
>>> from pathlib import Path
>>> p = Path("nonewline.csv")
>>> with p.open("w", encoding="utf-8") as f:
...     w = csv.writer(f)
...     w.writerow(["name", "chapter"])
...     w.writerow(["Ada Lovelace", "Lagos"])
...
14
20
>>> p.read_bytes()
b'name,chapter\r\r\nAda Lovelace,Lagos\r\r\n'
```

Every record now ends in three bytes, and every reader that splits on `\r\n`
finds an empty line between your rows. `newline=""` turns the translation off
while leaving encoding on, so what the module wrote is what lands.

**Why the reader needs it too, for a completely different reason.** A CSV value
is allowed to contain a line break, as long as it is inside quote marks:

```text
name,note
Ada,"first line
second line"
```

That is three lines of text and two rows of data. The `csv` parser is built to
handle it — it knows it is inside a quoted value and keeps going. But it can
only do that if it is handed the line breaks as they really are. With universal
newlines switched on, the file object splits and rewrites lines before the
parser ever sees them, and a `\r` inside a quoted value can be turned into a
`\n`, silently editing somebody's data.

Watch the difference. The file below holds a note with a bare `\r` inside a
quoted value:

```text
>>> from pathlib import Path
>>> p = Path("quoted-newline.csv")
>>> p.write_bytes(b'name,note\r\nAda,"first\rsecond"\r\n')
31
>>> with p.open(encoding="utf-8", newline="") as f:
...     list(csv.reader(f))
...
[['name', 'note'], ['Ada', 'first\rsecond']]
>>> with p.open(encoding="utf-8") as f:
...     list(csv.reader(f))
...
[['name', 'note'], ['Ada', 'first\nsecond']]
```

Same file, same parser, one character of somebody's note quietly changed.

So the rule, and it is worth memorising as one sentence: **any file you open
for the `csv` module gets `newline=""`, reading or writing, on every operating
system.** The Python documentation says the same thing, and this is the one
place where "it works on my machine" is guaranteed for anyone on Linux and
guaranteed to break for somebody on Windows.

A last detail for completeness. `newline=""` and `newline="\n"` are not the
same request. `newline="\n"` says "no translation, and `\n` is the line
terminator". `newline=""` says "no translation, and *recognise* any of `\n`,
`\r` or `\r\n` as a line ending when splitting". The `csv` module needs the
recognising part, so `""` is the one to use.

</details>

<details>
<summary>Under the hood — what the quoting rules actually are</summary>

The `csv` module is not doing anything you could not do by hand. It is doing
four small things consistently, which is the part people get wrong.

**When a value gets quotes.** By default (`csv.QUOTE_MINIMAL`) a value is
wrapped in `"` only when it has to be: when it contains the delimiter, a quote
character, `\r`, or `\n`. That is why `Lagos` comes out bare and `Chen, Lin`
comes out quoted, in the same file, on the same run.

**How a quote inside a value is written.** By doubling it. A mentor called
`Lin "Chen"` is written like this:

```text
>>> import csv, io
>>> b = io.StringIO()
>>> csv.writer(b).writerow(['Lin "Chen"', "Lagos"])
22
>>> b.getvalue()
'"Lin ""Chen""",Lagos\r\n'
```

Read the outside pair as the wrapper and each doubled pair as one literal quote
character. The reader undoes it exactly:

```text
>>> next(csv.reader(io.StringIO('"Lin ""Chen""",Lagos')))
['Lin "Chen"', 'Lagos']
```

**What the module does not do.** It does not know types, it does not trim
spaces, and it does not care what your columns mean. ` 12` with a leading space
comes back as `' 12'`. `int(' 12')` happens to work, because `int` tolerates
surrounding whitespace — which is exactly the kind of luck that hides a
whitespace problem until the day you compare that value to a string.

**The four quoting modes**, since you will meet them in other people's code:
`QUOTE_MINIMAL` (the default, above), `QUOTE_ALL` (quote everything — useful
when a downstream tool is fussy), `QUOTE_NONNUMERIC` (quote everything that is
not a number, and *convert* unquoted values to `float` on read), and
`QUOTE_NONE` (never quote, and raise if a value contains the delimiter).
`QUOTE_NONNUMERIC` is the interesting one: it is the only setting that gives
you back something other than a string, and it gives you `float`, so `12`
returns as `12.0`. That is rarely what you want, and it is why explicit
`int(...)` is still the advice.

**And the thing CSV genuinely cannot do.** There is no way to say "this value
is missing" as distinct from "this value is the empty string" — Quito's empty
field in Exercise 4 is the same two characters either way. There is no type
information, no character-set declaration inside the file, and no agreement
about whether the first row is a header. Every one of those is a reason JSON
exists, and JSON is Exercise 3.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] `data/mentor-hours-certified.csv` has exactly four lines: header plus three rows.
- [ ] The `"Chen, Lin"` value is intact and still quoted in the output.
- [ ] Reading the output back with `DictReader` gives three complete rows, and
      `repr(row["name"])` shows `'Chen, Lin'` as one string.
- [ ] The three printed lines match the spec exactly.
- [ ] Both `open` calls pass `newline=""` and `encoding="utf-8"`.
- [ ] `data/mentor-hours.csv` is unchanged.
- [ ] A row with exactly `10` hours qualifies when you add one.
- [ ] Committed to Git with a message like `Add Week 6 exercise 2: CSV roundtrip filter`.

## Stretch

- Add a `total_hours` line to the output — the sum of the `hours` column across
  the kept rows only. Watch the `int` conversion happen twice and decide
  whether to convert once per row instead, into a local variable.

- Write one file per chapter — `data/certified-lagos.csv` and friends — using a
  dict of open writers. Notice how quickly "one open file per key" gets awkward,
  and remember the feeling for Week 7.

- Sort the output by hours, largest first. You cannot sort a reader that is
  still reading; you have to collect the rows into a list first. Say out loud
  why that is a memory trade-off before you write it.

- Change the *output* delimiter to a tab with
  `csv.DictWriter(dst, fieldnames=..., delimiter="\t")` and look at the result.
  `Chen, Lin` no longer needs quote marks, because the comma is no longer
  special. Then ask yourself what a name containing a tab would do, and you
  have understood quoting.

When your roundtrip holds, move on to
[Exercise 3 — JSON Config](./exercise-03-json-config.md).
