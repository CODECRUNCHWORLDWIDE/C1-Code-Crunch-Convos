# Homework Problem 1 — Word-count CLI

> **Topic:** counting words in several files at once, and carrying on when one of them cannot be read
> **Lecture:** [Lecture 01 — Files and pathlib](../lecture-notes/01-files-and-pathlib.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** this is the first program you write that is handed a list of things and has to survive one of them being broken. The interesting line is not the counting. It is the `continue`.

## The Brief

You are writing the tool that answers "how long is this?" for a pile of
files at once.

Give it some file names. For each one it prints the number of words and
the name, lined up in a column. At the end it prints the total.

```text
   124  essay.txt
    42  notes.txt
-----
   166  total
```

Now the part that makes it a real program. One of those files will not
open. It was deleted, or you spelled it wrong, or it is not text at all.
When that happens the tool must **not** stop. It says so, out loud, and
moves on to the next file.

```text
WARNING  word_count  could not read missing.txt: FileNotFoundError
```

That warning is a complaint, not a result. So it goes to a different
place from the table — you will see exactly what that means in a moment.

A **word** here is whatever `"some text".split()` gives you back: any run
of spaces, tabs or newlines separates one word from the next.

Write a script called `word_count.py` that takes its file names from the
command line.

## Starter

Save this as `word_count.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it just says every file has zero words:

```python
"""Count the words in each file named on the command line."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

log = logging.getLogger("word_count")


def count_words(path: Path) -> int:
    """Return the number of whitespace-separated words in the file at `path`.

    Args:
        path: The file to count.

    Returns:
        The number of words in the file.
    """
    total = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            # TODO: add this line's word count to `total`
            pass
    return total


def report(paths: list[Path]) -> int:
    """Print one line per readable file, then the total. Return the total."""
    grand_total = 0
    for path in paths:
        # TODO: call count_words in a try, and on failure log a WARNING
        #       naming the path and the exception type, then `continue`
        words = 0
        print(f"{words:>6}  {path}")
        grand_total += words
    print("-----")
    print(f"{grand_total:>6}  total")
    return grand_total


def main(argv: list[str]) -> int:
    """Count the files named in `argv`."""
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    if not argv:
        print("usage: word_count.py FILE [FILE ...]", file=sys.stderr)
        return 2
    report([Path(a) for a in argv])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Make two files to try it on before you write anything:

```bash
python -c "from pathlib import Path; Path('essay.txt').write_text('one two three\n', encoding='utf-8')"
python -c "from pathlib import Path; Path('notes.txt').write_text('four five\n', encoding='utf-8')"
python word_count.py essay.txt notes.txt missing.txt
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-06-file-io-exceptions/homework/problem-01-word-count-cli.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The script accepts one or more file paths from `sys.argv`.
2. For each readable file it prints the word count right-aligned in a
   six-character column, then two spaces, then the path.
3. After the last file it prints `-----` and then the grand total in the
   same shape, labelled `total`.
4. A file that cannot be read logs a WARNING naming the path and the
   **type** of the exception, and the run continues with the next file.
5. The grand total counts only the files that were actually read.
6. Every function has type hints and a docstring.

## Constraints

- **Catch `(OSError, UnicodeDecodeError)`, not `Exception`.** Those two
  cover every failure the brief names, and nothing else. A missing file,
  a locked file and a directory handed in by mistake are all kinds of
  `OSError`. A file full of bytes that are not valid UTF-8 is not — by
  the time decoding fails the operating system has already handed you
  the bytes successfully, so that one is a `ValueError` underneath.
  Catching `Exception` instead would also swallow the typo in your own
  code and report it as an unreadable file.
- **Report `type(e).__name__`, not `str(e)`.** The brief's line ends
  `: FileNotFoundError` — the name of the exception type. `str(e)` would
  give you `[Errno 2] No such file or directory: 'missing.txt'`, which
  repeats the path you already printed.
- **Use `logging` for the warning, not `print`.** `logging` writes to
  stderr and `print` writes to stdout, which is what lets
  `python word_count.py *.txt > counts.txt` put the table in the file
  and the complaints on your screen. With `print` the warning lands in
  the middle of `counts.txt` and the next tool to read it chokes.
- **Count with `.split()`, never `.split(" ")`.** `"a  b".split(" ")` is
  `['a', '', 'b']` — three pieces, because splitting on one literal
  space does not collapse runs and does not treat a newline as a
  separator at all.
- **Sum per line, do not read the whole file at once.** Both give the
  same number. Only one of them still works on a file bigger than your
  memory.

## Expected output

The shipped answer runs its own demo when you give it no file names, so
it works from a clean checkout. It creates `essay.txt` and `notes.txt` in
a scratch folder, then counts those two plus a `missing.txt` that was
never created:

```bash
$ python problem-01-word-count-cli-solution.py
```

```text
   124  essay.txt
    42  notes.txt
-----
   166  total
```

`124 + 42 == 166`, and `missing.txt` contributes nothing.

The warning is not in that block, and that is the lesson rather than an
omission. It went to stderr:

```console
WARNING  word_count  could not read missing.txt: FileNotFoundError
```

Prove the split to yourself. Throw stderr away and you keep the table;
throw stdout away and you keep the complaint:

```bash
python problem-01-word-count-cli-solution.py 2>/dev/null
python problem-01-word-count-cli-solution.py 2>&1 >/dev/null
```

## Steps

1. Activate your Week 6 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `word_count.py`. Make the two sample files shown
   under **Starter** and run it. Every count is `0`, because the counting
   `TODO` is still a `pass`.
3. Fill in `count_words`: `total += len(line.split())`. Run it again.
   The two real files now have counts and `missing.txt` crashes the
   program with a traceback. That crash is the problem you are here to
   solve.
4. Wrap the `count_words` call in `try` / `except (OSError,
   UnicodeDecodeError) as e`. In the `except`, call
   `log.warning("could not read %s: %s", path, type(e).__name__)` and
   then `continue`.
5. Run it a third time. Two rows, one warning, and a total of the two
   rows.
6. Check the column widths against **Expected output** character by
   character. Six wide, then two spaces.
7. Try it on a file that is not UTF-8 to see the second half of the
   exception tuple earn its place:

   ```bash
   python -c "from pathlib import Path; Path('latin.txt').write_bytes(b'caf\xe9 au lait\n')"
   python word_count.py latin.txt
   ```

8. Compare against **The Solution**, work down the acceptance checklist,
   and commit: `git add homework/word_count.py` then
   `git commit -m "Week 6 homework: word-count CLI"`.

## The Solution

```python
"""Homework 1 — Word-count CLI.

Counts whitespace-separated words in each file named on the command line,
prints a right-aligned table and a grand total. Files that cannot be read are
reported as WARNINGs on stderr and do not stop the run.

    python word_count.py essay.txt notes.txt missing.txt

Run it with no arguments and it builds its own sample files in a scratch
folder first, so the download works from a clean checkout with nothing set up.

Save your own copy as ``word_count.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import logging
import os
import sys
import tempfile
from pathlib import Path

log = logging.getLogger("word_count")


def count_words(path: Path) -> int:
    """Return the number of whitespace-separated words in the file at *path*.

    Sums per line rather than splitting the whole file at once, so memory stays
    flat on a large file. The result is identical either way: ``str.split()``
    with no argument treats a run of any whitespace -- including the newline --
    as one separator, so no word can straddle a line boundary.

    Args:
        path: The file to count.

    Returns:
        The number of words in the file.
    """
    total = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            total += len(line.split())
    return total


def report(paths: list[Path]) -> int:
    """Print one line per readable file, then the total. Return the total.

    Args:
        paths: The files to count, in the order given on the command line.

    Returns:
        The sum of the counts of the files that could actually be read.
    """
    grand_total = 0
    for path in paths:
        try:
            words = count_words(path)
        except (OSError, UnicodeDecodeError) as e:
            log.warning("could not read %s: %s", path, type(e).__name__)
            continue
        print(f"{words:>6}  {path}")
        grand_total += words
    print("-----")
    print(f"{grand_total:>6}  total")
    return grand_total


def _demo() -> int:
    """Build two sample files in a scratch folder and report on them.

    The scratch folder is a temporary directory this function creates and
    deletes, so the demo needs no data placed by anybody else and leaves
    nothing behind. It changes into that folder first, which is why the table
    shows plain names like ``essay.txt`` instead of a long temporary path.

    Returns:
        Always 0. The demo cannot fail in a way the caller can act on.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="word_count_") as scratch:
        try:
            os.chdir(scratch)
            Path("essay.txt").write_text(
                " ".join(f"word{i % 17}" for i in range(124)) + "\n",
                encoding="utf-8",
            )
            Path("notes.txt").write_text(
                "\n".join(" ".join(f"n{i}" for i in range(7)) for _ in range(6))
                + "\n",
                encoding="utf-8",
            )
            report([Path("essay.txt"), Path("notes.txt"), Path("missing.txt")])
        finally:
            # Leave the scratch folder before it is deleted. A process whose
            # working directory has been removed is a confusing thing to be.
            os.chdir(home)
    return 0


def main(argv: list[str]) -> int:
    """Count the files named in *argv*, or run the demo when there are none.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The process exit code.
    """
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    if not argv:
        return _demo()
    report([Path(a) for a in argv])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

**Why it works.**

**The exception tuple is exactly the right width.** The three failures
the brief names live in two different families:

```text
Exception
 ├── OSError
 │    ├── FileNotFoundError      <- the file is not there
 │    ├── PermissionError        <- you are not allowed to open it
 │    └── IsADirectoryError      <- somebody handed you a folder
 └── ValueError
      └── UnicodeError
           └── UnicodeDecodeError  <- the bytes are not UTF-8
```

`OSError` covers the first three because they are its children. The
fourth is not one of them and never will be. Catching only `OSError`
gets you past the missing file and then dies on the first spreadsheet
somebody exported from an old copy of Excel.

**`continue` is the whole point.** A word counter over five files should
give you four counts and one complaint, not nothing. The total is
deliberately the total of what was *readable*, and the run is honest
about being partial because the warning is right there beside it.

**Counting per line gives the same answer as counting the whole file.**
`str.split()` with no argument splits on *runs* of whitespace and throws
away the empty pieces at the ends. A newline is whitespace. So no word
can be cut in half at a line boundary and no empty string is ever
counted. `len(path.read_text().split())` would agree — and would also
build a list of every word in the file, all at once, in memory.

**`{words:>6}` is six columns, then two literal spaces.** Count the
characters in the brief's example: `   124  essay.txt` is three spaces,
then `124`, then **two** spaces. Both numbers sit in a six-wide
right-aligned field. The separator line is five dashes.

**The demo builds its own data.** `_demo` makes a temporary folder,
changes into it, writes the two sample files, and changes back out
before the folder is deleted. That is why you can download this file to
an empty directory and run it. It also means the paths in the table are
short names rather than a long temporary path, so the output is the same
on every machine.

## Download and run

Download [problem-01-word-count-cli-solution.py](./problem-01-word-count-cli-solution.py)
and run it:

```bash
python problem-01-word-count-cli-solution.py
```

With no arguments it creates its own sample files in a temporary folder
and counts those, so it runs anywhere with nothing set up. Give it real
file names and it counts those instead:

```bash
python problem-01-word-count-cli-solution.py essay.txt notes.txt missing.txt
```

Save your own copy as `word_count.py` in your homework folder, and commit
that one. The longer download name is there so it cannot overwrite your
work.

## Common bugs to catch

- **Catching only `FileNotFoundError`.** The most common version of this
  answer, and it survives right up until a file is not UTF-8:

  ```python
  try:
      words = len(path.read_text(encoding="utf-8").split())
  except FileNotFoundError:
      print(f"skipping {path}")
      continue
  ```

  ```text
     124  essay.txt
  Traceback (most recent call last):
    File "wrong1.py", line 7, in <module>
      words = len(p.read_text(encoding="utf-8").split())
                  ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
    File "...\Lib\pathlib\_local.py", line 546, in read_text
      return PathBase.read_text(self, encoding, errors, newline)
             ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "...\Lib\pathlib\_abc.py", line 633, in read_text
      return f.read()
             ~~~~~~^^
    File "<frozen codecs>", line 325, in decode
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte
  ```

  Look at the first line: `essay.txt` was counted, and *then* the run
  died. Partial output plus a traceback is the worst of both worlds,
  because whoever reads `counts.txt` later cannot tell a complete answer
  from a truncated one.
- **`except Exception:` to make the traceback go away.** It does make it
  go away. It also swallows the `NameError` from the variable you
  misspelled inside `count_words`, which now reports as
  `could not read essay.txt: NameError` and sends you hunting through the
  filesystem for a bug that is in your own function.
- **Counting with `.split(" ")`.**

  ```text
  >>> "a  b".split(" ")
  ['a', '', 'b']
  >>> "a  b".split()
  ['a', 'b']
  ```

  Any file with two spaces after a full stop inflates your count, and
  every line-ending is missed entirely.
- **Printing the warning with `print`.** It compiles, it looks identical
  on screen, and it quietly corrupts every redirect of the script
  forever.
- **Adding the count before the read succeeds.** If `grand_total +=
  words` sits above the `try`, or the `continue` is forgotten, an
  unreadable file contributes whatever `words` held from the previous
  loop. Add to the total only after a successful count.

## Under the hood

<details>
<summary>Under the hood — what pathlib gives you that a string path does not</summary>

You could write this whole program with strings and `os.path`. It would
work. `pathlib` is worth the swap anyway, and here is what you actually
get.

**A path stops being text.** `"reports" + "/" + name` is string
concatenation, and string concatenation has no opinion about whether the
result is a sensible path. `Path("reports") / name` is a path operation,
and `/` on a `Path` is defined to be "join these with the right
separator for this machine".

```text
>>> from pathlib import Path
>>> Path("reports") / "2026" / "may.csv"
WindowsPath('reports/2026/may.csv')
>>> str(Path("reports") / "2026" / "may.csv")
'reports\\2026\\may.csv'
```

The same source line produced `reports\2026\may.csv` on Windows and
would produce `reports/2026/may.csv` on Linux. You never typed a
separator, so you never typed the wrong one.

**The pieces of a name have names.**

```text
>>> p = Path("data/q1.csv")
>>> p.name
'q1.csv'
>>> p.stem
'q1'
>>> p.suffix
'.csv'
>>> p.parent
WindowsPath('data')
>>> p.with_suffix(".json")
WindowsPath('data/q1.json')
```

Problem 2 needs `.stem` and problem 6 needs `.with_suffix`. Done with
string slicing, both are a small pile of `rfind` calls that get the
edge cases wrong. `Path("archive.tar.gz").suffix` is `'.gz'`, not
`'.tar.gz'`, and that is a decision somebody made carefully rather than
an accident of where the first dot fell.

**Reading and writing are methods on the thing itself.**

```python
text = Path("notes.txt").read_text(encoding="utf-8")
Path("out.txt").write_text(text.upper(), encoding="utf-8")
```

Each of those opens the file, does the one operation, and closes it,
even if something goes wrong in between. For a whole small file that is
the shortest correct thing you can write. For a large file you still
want `with path.open(...)` and a loop, which is what `count_words` does.

**Asking questions is a method call, not a module function.**

```text
>>> Path("notes.txt").exists()
True
>>> Path("data").is_dir()
False
>>> sorted(Path(".").glob("*.txt"))
[WindowsPath('essay.txt'), WindowsPath('notes.txt')]
```

`glob` is the one that changes how you write programs. Getting every CSV
in a folder, in sorted order, is one line.

**Where it does not help.** A `Path` is not a file. Making one touches
the disk not at all — `Path("nonsense/../../etc/passwd")` is a perfectly
happy object. And `path.exists()` is a question about one instant in
time; by the time you act on the answer it can be false. That is why
`count_words` opens the file and catches the failure instead of asking
first. More on that in problem 5.

</details>

<details>
<summary>Under the hood — why stdout and stderr are two streams, and what that buys you</summary>

Every program starts life with two output pipes, not one.

| Stream | Number | What belongs in it |
|---|---|---|
| stdout | 1 | the answer — the thing the next program wants |
| stderr | 2 | everything about how the run went — progress, warnings, errors |

`print` writes to stdout. `logging` writes to stderr. That is the entire
mechanism behind this problem's warning behaviour, and it is why the
brief insists on `logging` rather than a `print` that looks the same on
screen.

The payoff is that either stream can be redirected without disturbing
the other:

```bash
python word_count.py *.txt > counts.txt      # table to the file, warnings to the screen
python word_count.py *.txt 2> problems.txt   # table to the screen, warnings to the file
python word_count.py *.txt 2>/dev/null       # table only
python word_count.py *.txt 2>&1 >/dev/null   # warnings only
```

That last one reads backwards to most people. `2>&1` says "send stderr
wherever stdout is currently going" — the screen, at that moment,
because the redirections are applied left to right. Then `>/dev/null`
moves stdout to the bin. stderr is already pointed at the screen and
stays there.

**The buffering wrinkle.** When stdout is a terminal, Python flushes it
line by line. When stdout is a file or a pipe, Python switches to
flushing in large blocks, because that is much faster. stderr is never
buffered that way. So in a captured transcript the warnings can appear
in a surprising place — before table rows that were actually printed
first.

```bash
python word_count.py essay.txt notes.txt missing.txt | cat
```

If that looks scrambled, nothing is wrong with your program. `python -u`
turns the buffering off and restores the intuitive order, and it is why
several transcripts in this week use it.

This is also the reason a well-behaved command-line tool never prints
progress messages to stdout. Somebody, eventually, will pipe your
output into something else.

</details>

## Acceptance checklist

- [ ] `python word_count.py essay.txt notes.txt missing.txt` prints two
      table rows, a separator, and a total.
- [ ] The missing file produces one WARNING naming the path and
      `FileNotFoundError`.
- [ ] The run does not stop at the missing file.
- [ ] The total is the sum of the files that were read, not of all the
      arguments.
- [ ] `python word_count.py essay.txt 2>/dev/null` still prints the
      table.
- [ ] `python word_count.py missing.txt 2>&1 >/dev/null` prints only the
      warning.
- [ ] Counts are made with `.split()`, not `.split(" ")`.
- [ ] The `except` names `(OSError, UnicodeDecodeError)`, not
      `Exception` and not a bare `except:`.
- [ ] Every function has type hints and a docstring.
- [ ] Committed with a message like `Week 6 homework: word-count CLI`.

## Stretch

- **Add a `--chars` flag.** Print characters as well as words, in a
  second column. `len(line)` per line, and decide out loud whether the
  newline counts.
- **Sort the table by count.** Collect the `(count, path)` pairs first,
  then sort and print. Notice what that costs you: nothing prints until
  every file has been read, so a slow file now delays the whole report.
  Streaming and sorting are a genuine trade, not a style choice.
- **Make the column width fit the data.** Six is a guess. Compute the
  width from the largest count and use `f"{words:>{width}}"`. The nested
  braces are real f-string syntax.
- **Count the lines and bytes too, like `wc`.** Then run the real `wc`
  on the same files and compare. Where you disagree, work out which of
  you is right — `wc -w` and `str.split()` do not agree about every
  possible file, and finding one is the exercise.
- **Handle a directory politely.** Right now handing it a folder logs
  `IsADirectoryError`, which is honest but unhelpful. Detect it with
  `path.is_dir()` and count every `*.txt` inside instead. Then think
  about whether that surprise is a feature or a bug.

Next: [Homework Problem 2 — CSV Merger](./problem-02-csv-merger.md).
