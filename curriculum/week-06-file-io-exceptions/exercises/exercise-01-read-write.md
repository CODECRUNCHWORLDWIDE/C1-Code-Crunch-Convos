# Exercise 1 — Read, Clean, Write

> **Topic:** reading a text file one line at a time and writing a tidied copy
> **Lecture:** [01 — Files and `pathlib`](../lecture-notes/01-files-and-pathlib.md)
> **Difficulty:** Beginner
> **Target time:** 15 minutes
> **Why this one:** every other exercise this week is the same three moves — open a file, walk it, write something out. If that loop is not automatic yet, the CSV and JSON exercises will feel like three problems stacked on top of each other instead of one. This is also where you start passing `encoding="utf-8"` every single time, which is the cheapest bug you will ever prevent.

## The Brief

Your community chapter signs people up on a paper sheet by the door. Later,
somebody types the sheet into a text file. What comes out is messy, the way
handwriting-into-a-keyboard always is: some addresses are shouted in capitals,
one line got two extra spaces in front of it, and there is a blank line where
the typist stopped for tea.

Email addresses do not care about capital letters. `Ada.Lovelace@Example.ORG`
and `ada.lovelace@example.org` are the same person, and every mail server on
Earth agrees. No **program** will agree, though, until somebody makes the two
strings actually match. Two strings match in Python only if they are the same
characters in the same order, and `A` is not `a`.

So you are writing the tidier. It reads the messy sheet one line at a time,
trims the spaces off both ends, puts everything in lowercase, throws away the
empty lines, and writes a clean file next to the messy one.

The messy one stays exactly as it was. That is not politeness — it is
insurance. If your tidier has a bug, you want the original still sitting there
so you can fix the bug and run again. A program that eats its own input gets
exactly one attempt.

## Starter

First, the data. Make a folder called `data/` next to your script, and put this
in `data/signups.txt`. Type it exactly. Line 2 starts with two spaces, and line
4 is empty. Those two lines **are** the exercise:

```text
Ada.Lovelace@Example.ORG
  grace.hopper@example.org
KATHERINE.JOHNSON@Example.org

alan.turing@EXAMPLE.org
```

Now the code. Save this as `exercise-01-read-write.py` in the folder that holds
`data/`, and fill in every `TODO`.

```python
"""exercise-01-read-write.py — copy a text file line by line, cleaning as you go.

Reads data/signups.txt, normalises every address, and writes the result to
data/signups-clean.txt. Blank and whitespace-only lines are dropped.
"""

from pathlib import Path

DATA = Path(__file__).parent / "data"
SOURCE = DATA / "signups.txt"
TARGET = DATA / "signups-clean.txt"


def clean(raw_line: str) -> str:
    """Return *raw_line* trimmed of surrounding whitespace and lowercased.

    An empty return value means the line held nothing but whitespace.
    """
    # TODO: strip the line, lowercase it, and return the result
    return raw_line


def copy_clean(source: Path, target: Path) -> tuple[int, int]:
    """Copy *source* to *target* one line at a time, cleaning each line.

    Returns:
        A ``(lines_read, addresses_written)`` pair.
    """
    lines_read = 0
    addresses_written = 0
    with source.open("r", encoding="utf-8") as src, \
         target.open("w", encoding="utf-8") as dst:
        for raw_line in src:
            lines_read += 1
            # TODO: clean the line and skip it when the result is empty
            # TODO: write the cleaned address followed by "\n" to dst
            # TODO: count the address you just wrote
    return lines_read, addresses_written


def main() -> None:
    """Run the copy and report what happened."""
    read, written = copy_clean(SOURCE, TARGET)
    print(f"Read {read} lines from {SOURCE.name}")
    print(f"Wrote {written} addresses to {TARGET.name}")


if __name__ == "__main__":
    main()
```

Five words in that starter you need before you begin.

**`Path`.** A `Path` is a name for a place on disk. It is not the file itself
and it does not open anything. Think of it as an address written on an
envelope: perfectly useful, and completely separate from the letter inside.

**`open`.** Opening a path hands you a **file object**. That is the letter,
opened, with your finger holding your place in it. `Path` has the address;
the file object has the cursor.

**`"r"` and `"w"`.** The mode. `"r"` is read, and it refuses to run if the file
is not there. `"w"` is write, and it empties the file the instant it opens —
before you have written one character.

**`with`.** `with something as name:` borrows the thing, lets you use it inside
the indented block, and gives it back the moment you leave — whether you left
normally or crashed on the way out. Files that are given back get closed and
flushed. Files that are not given back can lose whatever was still in the
buffer.

**`encoding="utf-8"`.** Files hold numbers, not letters. The encoding is the
codebook that says which number means which letter. UTF-8 is the codebook the
whole internet uses. Say it out loud every time and your file reads the same on
every machine in the org.

## Requirements

1. `clean("  Grace.Hopper@Example.ORG  ")` returns exactly
   `grace.hopper@example.org` — nothing before it, nothing after it, all
   lowercase.
2. `clean("   ")` returns the empty string, `""`. Your loop uses that to decide
   what to throw away.
3. `copy_clean` counts **every** line it reads, blank one included, and counts
   only the addresses it actually wrote. On the sample file that is `5` and
   `4`.
4. Every written line ends with one `"\n"` in your program's view of the file.
   The output holds four lines with no blank lines between them.

   A note so you do not go looking for a bug that is not there: `"\n"` is
   what your program writes, not always what lands on the disk. On Windows,
   Python's text mode turns each `"\n"` into the two bytes `\r\n` on the way
   out, so a hex dump of `data/signups-clean.txt` shows `0d 0a` at the end of
   every line rather than a lone `0a`. On macOS and Linux you get the single
   byte. Nothing on this page depends on which one you get, because the same
   translation runs in reverse when the file is read back. The **Under the
   hood** block further down explains what text mode is doing and how to
   switch the translation off.
5. The two printed lines are exactly `Read 5 lines from signups.txt` and
   `Wrote 4 addresses to signups-clean.txt`.
6. `data/signups.txt` is byte-for-byte unchanged when the run finishes.

## Constraints

- **Walk the file with `for raw_line in src:`. Do not call `.read()` or
  `.readlines()`.** Both of those pull the whole file into memory at once. Five
  lines will not hurt you today. The log files in this week's mini-project are
  not five lines, and the habit is the thing you are actually building here.
- **Build paths from `Path(__file__).parent`, never from a bare string like
  `"data/signups.txt"`.** A bare relative path is measured from wherever your
  terminal happened to be standing when you pressed Enter, which is not
  necessarily where the script lives. `Path(__file__)` is the script's own
  address, so `.parent / "data"` finds the folder beside it from anywhere on
  the machine.
- **Pass `encoding="utf-8"` to both files.** Leave it out and Python picks a
  default that depends on the machine. A name with an accent in it then
  round-trips one way on your laptop and a different way on somebody else's,
  and you find out weeks later from a person whose name your program mangled.
- **Open both files in one `with` statement.** If the write goes wrong halfway
  through, `with` still closes the reader and still flushes the writer. A file
  opened for writing holds your text in a buffer until it is closed, so a
  script that skips `with` and then crashes can leave a half-written file
  behind.
- **Do not sort and do not remove duplicates.** One input line becomes at most
  one output line. That is exactly what makes `5` and `4` numbers you can
  check. De-duplicating is a stretch goal at the bottom, and it needs a
  different tool.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-read-write.py
Read 5 lines from signups.txt
Wrote 4 addresses to signups-clean.txt

--- signups-clean.txt ---
ada.lovelace@example.org
grace.hopper@example.org
katherine.johnson@example.org
alan.turing@example.org
```

Your own `exercise-01-read-write.py` prints the first two lines and stops. The
shipped file prints the tidied file underneath them as well, so you can compare
your `data/signups-clean.txt` against it without opening anything.

Read the two numbers against each other. `5` counts what arrived. `4` counts
what survived. The gap between them is the blank line, and a report that shows
you both numbers is telling you something a report that shows one number cannot.

## Steps

1. Make the folder and the file: `mkdir data`, then create `data/signups.txt`
   with the block above. Check the two spaces on line 2 are really there.
2. Save the starter as `exercise-01-read-write.py` beside `data/`.
3. Fill in `clean` first, and try it on its own before wiring it up:

   ```bash
   python -c "print(repr('  A@B.ORG '.strip().lower()))"
   ```

   ```text
   'a@b.org'
   ```

   `repr` is worth the extra typing here. It shows you the quote marks, so you
   can see there is nothing left outside them. Plain `print` would show
   `a@b.org` whether or not a space was still clinging to the end.
4. Fill in the loop body. Write the address with `dst.write(address + "\n")`.
5. Run it: `python exercise-01-read-write.py`.
6. Open `data/signups-clean.txt` and count the lines. Four, with no gaps.
7. Run the script a second time. The two numbers should not move. Mode `"w"`
   empties the target before writing, so a second run replaces the file rather
   than adding to it. (Mode `"a"` would add, and the file would grow every
   time you ran it — a good thing to know about and the wrong thing here.)

## The Solution

```python
"""exercise-01-read-write-solution.py — copy a text file line by line, cleaning as you go.

Reads a sign-up sheet, normalises every address, and writes the result to a
second file. Blank and whitespace-only lines are dropped. The original is never
touched.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact sign-up sheet the page
gives you, so the download runs on any machine with nothing set up beforehand.
The temporary directory is deleted on the way out; ``clean`` and ``copy_clean``
below are the whole exercise and know nothing about it.

Run it with::

    python exercise-01-read-write-solution.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

#: The sign-up sheet exactly as the exercise page gives it. Line 2 starts with
#: two spaces and line 4 is empty; those two lines are the exercise.
SAMPLE_SIGNUPS = (
    "Ada.Lovelace@Example.ORG\n"
    "  grace.hopper@example.org\n"
    "KATHERINE.JOHNSON@Example.org\n"
    "\n"
    "alan.turing@EXAMPLE.org\n"
)


def clean(raw_line: str) -> str:
    """Return *raw_line* trimmed of surrounding whitespace and lowercased.

    An empty return value means the line held nothing but whitespace.
    """
    return raw_line.strip().lower()


def copy_clean(source: Path, target: Path) -> tuple[int, int]:
    """Copy *source* to *target* one line at a time, cleaning each line.

    Returns:
        A ``(lines_read, addresses_written)`` pair.
    """
    lines_read = 0
    addresses_written = 0
    with source.open("r", encoding="utf-8") as src, \
         target.open("w", encoding="utf-8") as dst:
        for raw_line in src:
            lines_read += 1
            address = clean(raw_line)
            if not address:
                continue
            dst.write(address + "\n")
            addresses_written += 1
    return lines_read, addresses_written


def build_sample(folder: Path) -> Path:
    """Write the sample sign-up sheet into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "signups.txt"
    path.write_text(SAMPLE_SIGNUPS, encoding="utf-8")
    return path


def main() -> None:
    """Build the sample data, run the copy, and report what happened."""
    with tempfile.TemporaryDirectory() as workspace:
        data = Path(workspace) / "data"
        source = build_sample(data)
        target = data / "signups-clean.txt"

        read, written = copy_clean(source, target)
        print(f"Read {read} lines from {source.name}")
        print(f"Wrote {written} addresses to {target.name}")

        print()
        print(f"--- {target.name} ---")
        print(target.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
```

**`clean` returning `""` is the whole design.** A blank line arriving from a
file is not the empty string — it is `"\n"`. A line of nothing but spaces is
`"   \n"`. Both of those are non-empty strings, so both are truthy, so testing
the raw line tells you nothing. But `"\n".strip()` is `""`, and `"   \n".strip()`
is `""`, and the empty string is falsy. So once `clean` has run, `if not
address:` is a complete and correct test for "there was nothing here". One
function decides what a line *means*; the loop only acts on the decision.

**`.strip()` and `.lower()` are chained and returned.** Both hand back a new
string and leave the original alone — strings in Python cannot be edited in
place. Writing `raw_line.lower()` on a line by itself computes a perfectly good
lowercase string and then throws it away, which is the single most common
version of "my code does nothing and I cannot see why".

**`continue` instead of an `else`.** `if address: dst.write(...)` would also be
correct. The `continue` version puts the rejection right next to the reason for
it and leaves the main path flat and unindented. Get used to the shape now —
Exercise 5's loop uses exactly the same one for a far more interesting
rejection.

**The two counters sit in two different places on purpose.** `lines_read += 1`
is at the top of the body, before any decision. `addresses_written += 1` is at
the bottom, after the write actually happened. That placement is what makes `5`
and `4` mean something. Put both at the top and you get `5` and `5`. Put
`lines_read += 1` after the `continue` and you get `4` and `4`, and the blank
line becomes invisible. A count is only useful when you can say exactly which
event it counts, and the place you put the `+= 1` is where you say it.

**The write goes through the file object, not through the `Path`.** `Path` has
`write_text`, which writes a whole file in one go and closes it. It has no
`.write`, because a `Path` is not open. The name you bound in the `with`
statement — `dst` — is the open thing with the cursor in it.

**The source survives because the two paths differ and the source is opened
`"r"`.** Point both names at the same file and `"w"` empties it before the
reader gets a single line. There is no undo.

**About the harness.** Everything from `SAMPLE_SIGNUPS` down to `build_sample`
exists so that this download runs on a machine where you have created nothing.
It writes the same `data/signups.txt` the page gives you, inside a temporary
folder that Python deletes on the way out. Your own version reads the real
`data/` folder beside your script and does not need any of it. `clean` and
`copy_clean` are the exercise, and neither of them knows the harness exists —
which is the point of passing paths in as arguments instead of reaching for
module-level constants inside the function.

## Run it

Copy the worked answer on this page into `exercise-01-read-write.py` and run it:

```bash
python exercise-01-read-write.py
```

It needs no `data/` folder and no setup: it builds its own copy of the sample
sheet in a temporary directory, tidies it, prints the result, and cleans up
after itself. The `-solution` in the name keeps it from colliding with your own
`exercise-01-read-write.py`.

## Common bugs to catch

- **The blank line is still in the output.** You tested the raw line
  (`if raw_line == "":`) instead of the cleaned one. While you are iterating a
  file, `raw_line` is never `""` — the loop simply stops when the file runs
  out, so any line that reaches you carries at least a `"\n"`. Strip first,
  then test.

- **Every other line in the output is blank.**

  ```text
  'ada.lovelace@example.org\n\n  grace.hopper@example.org\n\nkatherine.johnson@example.org\n'
  ```

  You wrote `dst.write(raw_line.lower() + "\n")` using the line that has not
  been stripped. It still carries its own newline, so you added a second one.
  Notice Grace's two leading spaces survived as well, because `.lower()` does
  not remove whitespace. Strip once into a variable, then use the variable
  everywhere below.

- **The output holds one address, and it is the last one.**

  ```text
  'alan.turing@example.org\n'
  ```

  You put `target.open("w", ...)` *inside* the loop. `"w"` empties the file on
  every open, so each pass throws away everything the pass before it wrote.
  Open once, outside the loop, which is what the starter's single `with`
  statement was already doing for you.

- **`TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'`.**

  ```text
  ada.lovelace@example.org
  Traceback (most recent call last):
    File "wrong.py", line 15, in <module>
      dst.write(clean(raw_line) + "\n")
                ~~~~~~~~~~~~~~~~^~~~~~
  TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
  ```

  Read the line above the traceback: the address printed. Your `clean` ends in
  `print(...)` instead of `return ...`, so it computed the right string and
  handed it to your terminal instead of to the caller. A function with no
  `return` hands back `None`. Write it as `dst.write(clean(raw_line))` and the
  wording changes but the cause does not: `TypeError: write() argument must be
  str, not None`.

- **`AttributeError: 'WindowsPath' object has no attribute 'write'. Did you
  mean: 'drive'?`** (`'PosixPath'` on macOS and Linux.) You called
  `TARGET.write(...)`. Use the file object from the `with` block.

- **`FileNotFoundError` on a path that looks correct.**

  ```text
  FileNotFoundError: [Errno 2] No such file or directory: 'data\\signups.txt'
  ```

  Either `data/` does not exist yet, or you replaced the `Path(__file__).parent`
  anchor with a bare string and ran the script from somewhere else. The message
  names the path it tried but not the folder it tried it *from*, which is the
  half you need. Add `print(Path.cwd())` and it resolves in one run.

- **Everything is still in capitals.** `raw_line.lower()` returns a new string.
  You have to return it or assign it; calling it and dropping the result does
  nothing at all.

## Under the hood

<details>
<summary>Under the hood — what text mode really does to your newlines</summary>

Opening a file without `"b"` in the mode gives you **text mode**, and text mode
is not a passive pipe. It does two jobs on every read and every write:
it decodes and encodes characters, and it translates line endings.

The line-ending job exists because operating systems never agreed on how to end
a line. Unix, Linux and modern macOS end it with one byte, `\n`. Windows ends
it with two, `\r\n`. Python's answer is to make `"\n"` the only line ending
your *program* ever sees, and to translate at the edge.

Writing, on Windows:

```text
>>> from pathlib import Path
>>> p = Path("demo.txt")
>>> with p.open("w", encoding="utf-8") as f:
...     f.write("a@b.org\n")
...
8
>>> p.read_bytes()
b'a@b.org\r\n'
```

You wrote eight characters and eight is what `write` reported, but nine bytes
landed on the disk. Reading it back undoes exactly that:

```text
>>> with p.open("r", encoding="utf-8") as f:
...     f.read()
...
'a@b.org\n'
```

That reverse half is called **universal newlines**, and it is why your
`.strip()` works the same on a file a colleague made on a Mac and one a
colleague made on Windows. It also means a hex dump showing `0d 0a` is not
evidence that you wrote two newlines. It is evidence that you are on Windows.

If you want the bytes on disk to be exactly what you wrote, say so:

```text
>>> with p.open("w", encoding="utf-8", newline="\n") as f:
...     f.write("a@b.org\n")
...
8
>>> p.read_bytes()
b'a@b.org\n'
```

`newline="\n"` turns the translation off for that file. Use it when the bytes
themselves are the product — a file another program parses strictly, a file you
are about to hash, a file whose checksum is in a test. Leave it off when the
product is text a human or a text editor will read, which is the normal case
and the case here.

There is a third value, `newline=""`, which turns translation off but keeps
text mode's decoding. That one has its own job, and Exercise 2 is where it
matters.

</details>

<details>
<summary>Under the hood — why encoding="utf-8" is not simply the default</summary>

A file on disk is bytes. `72 101 108 108 111` is not the word "Hello" until
something agrees that 72 means `H`. An **encoding** is that agreement.

For decades every part of the world had its own agreement, and they collided:
byte 233 is `é` in Latin-1, `Ú` in cp437, and half of a character in UTF-8.
UTF-8 settled the argument by covering every writing system at once, and it is
now what the web, Git, JSON and essentially every new format use.

So why does `open()` not just use it? Because when Python 3 was designed, the
safest guess for "a text file on this computer" was "whatever this computer
uses", and on Windows that was — and by default still is — a regional code page
such as cp1252. Changing the default would silently change what millions of
existing scripts read. So `open()` without `encoding=` asks
`locale.getencoding()`, and the answer depends on the machine your code is
running on rather than on your code.

You can see it:

```text
>>> import locale
>>> locale.getencoding()
'cp1252'
```

Here is the failure that follows. Write a name in UTF-8, read it back with the
default on a machine whose default is cp1252, and the bytes are re-interpreted
under the wrong codebook:

```text
>>> "Chidi Okonkwö".encode("utf-8").decode("cp1252")
'Chidi OkonkwÃ¶'
```

Nothing raised. The program carried on and the name is now wrong. That garbled
shape has a name — **mojibake** — and if you have ever seen `Â` or `â€™`
appear in an otherwise normal sentence, you have met it.

Python did not leave it there. **PEP 540** added UTF-8 mode, which you can turn
on for one run with `python -X utf8 script.py` or for a whole machine with the
environment variable `PYTHONUTF8=1`, and it makes UTF-8 the default everywhere.
**PEP 686** commits to UTF-8 mode being on by default in a future release, and
in the meantime **PEP 597** added `python -X warn_default_encoding`, which
prints a warning at every `open()` that did not say. Run this exercise with it
and you will see one line per file you forgot.

None of that helps a colleague running an older interpreter with the old
default. Writing `encoding="utf-8"` is eighteen characters that make the answer
a property of your code instead of a property of somebody's laptop.

</details>

## Acceptance checklist

- [ ] `python exercise-01-read-write.py` runs with no traceback.
- [ ] `data/signups-clean.txt` holds exactly four lowercase addresses, one per line.
- [ ] There are no blank lines anywhere in the output file.
- [ ] Both printed counts match the spec exactly: `5` read, `4` written.
- [ ] `data/signups.txt` is unchanged — same size, same content.
- [ ] Running the script twice in a row gives the same result both times.
- [ ] Both `open` calls pass `encoding="utf-8"`.
- [ ] Committed to Git with a message like `Add Week 6 exercise 1: read, clean, write`.

## Stretch

- Drop duplicate addresses. Keep a `set` of the ones you have already written
  and skip the repeats — add a second copy of `Ada.Lovelace@Example.ORG` to the
  input to prove it works. Notice that the order of the output does not change:
  the set only decides *whether* to write, never *when*.

- Report what you skipped instead of dropping it in silence. Return a third
  value from `copy_clean` — a `list[int]` of the line numbers you rejected —
  and print it. A tidier that says "I threw away line 4" is a tidier somebody
  can trust.

- Swap `dst.write(address + "\n")` for `print(address, file=dst)` and prove the
  file is byte-identical:

  ```bash
  python -c "
  import pathlib
  a = pathlib.Path('data/signups-a.txt'); b = pathlib.Path('data/signups-b.txt')
  with a.open('w', encoding='utf-8') as f:
      f.write('x@y.org' + '\n')
  with b.open('w', encoding='utf-8') as f:
      print('x@y.org', file=f)
  print('identical:', a.read_bytes() == b.read_bytes())
  "
  ```

  ```text
  identical: True
  ```

  `print` writes the value and then writes `end`, which defaults to `"\n"` —
  the same two writes through the same translating text layer.

- Make the script refuse to clobber somebody's work. Open the target with mode
  `"x"` instead of `"w"`. `"x"` creates the file and raises `FileExistsError`
  if it is already there. Catch it and print a clear message. That one letter
  is the difference between a script that is safe to run twice and one that is
  safe to run once.

When your four addresses look right, move on to
[Exercise 2 — CSV Roundtrip](./exercise-02-csv-roundtrip.md).
