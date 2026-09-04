# Challenge 1 — Recursive Line Counter

> **Topic:** walking a whole folder tree with `pathlib`, and surviving the files you cannot read
> **Lecture:** [01 — Files and `pathlib`](../lecture-notes/01-files-and-pathlib.md)
> **Difficulty:** the counting is a `for` loop; the three `except` clauses in the right order are the work
> **Target time:** 1–2 hours
> **Why this one:** so far every exercise has known the name of its file. Real tools are pointed at a folder and told to go and find things. The moment you do that you meet files you are not allowed to open and files that are not text at all, and a tool that dies on one of them is a tool nobody uses twice.

## The Brief

You are building the small command-line tool that answers "how big is this
project, really". Point it at a folder, and it looks inside that folder, inside
every folder in it, inside every folder in *those*, all the way down. Every
`.py` file it finds gets its lines counted. At the end it prints a tidy table
and a grand total.

**Recursive** is the word for going all the way down like that. `pathlib`
spells it `rglob` — the `r` is for recursive — and it does the descending for
you.

Blank lines do not count. A blank line is a line with nothing on it once you
take the spaces off. This is a rough measure of how much code is here, not a
byte count, and blank lines are punctuation.

Here is the part that makes it a challenge rather than an exercise. Out in a
real tree there are files your program cannot read, and there are two very
different reasons why:

- **You are not allowed.** The operating system says no. That is a
  `PermissionError`.
- **It is not the text you thought it was.** The bytes came back fine and then
  Python could not decode them as UTF-8. That is a `UnicodeDecodeError`, and it
  lives in a completely different part of the exception family from the first
  one. Catching only the first will not save you from the second.

Your tool must say something useful about each skipped file and carry on. One
bad file must never take down the walk. That is the whole challenge, and the
demo tree the shipped answer builds contains a deliberately broken file so you
can watch it happen.

Where the warnings go matters too. The table is the tool's **answer** and goes
to standard output. The warnings are **commentary** and go to standard error
through `logging`. Then `python counter.py src > report.txt` puts the counts in
the file and leaves the warnings on your screen, which is exactly what you
want.

## Starter

Save this as `challenge-01-recursive-line-counter.py` and fill in the `TODO`s:

```python
"""challenge-01-recursive-line-counter.py — count lines of Python in a tree.

Walks a directory recursively, counts the non-blank lines in every .py file,
and prints a sorted table plus a grand total. Files that cannot be read are
logged and skipped.

    python challenge-01-recursive-line-counter.py [DIRECTORY]
"""

import logging
import sys
from pathlib import Path

log = logging.getLogger("linecount")


def count_lines(path: Path) -> int:
    """Return the number of non-blank lines in the UTF-8 text file at *path*."""
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            # TODO: count the line only when line.strip() is truthy
            pass
    return total


def count_python_lines(root: Path) -> dict[Path, int]:
    """Return a dict mapping each .py file under *root* to its line count.

    Files that cannot be read are logged at WARNING level and left out of the
    result. The walk never aborts because of one bad file.
    """
    counts: dict[Path, int] = {}
    for path in root.rglob("*.py"):
        # TODO: skip anything that is not a file
        # TODO: try count_lines(path) and store it
        # TODO: except PermissionError    -> log.warning, skip
        # TODO: except UnicodeDecodeError -> log.warning, skip
        # TODO: except OSError            -> log.warning, skip
        pass
    return counts


def print_report(root: Path, counts: dict[Path, int]) -> None:
    """Print a sorted table of files and line counts, then the grand total."""
    for path in sorted(counts):
        relative = path.relative_to(root).as_posix()
        print(f"{counts[path]:>5} {relative}", flush=True)
    print("-----")
    print(f"{sum(counts.values()):>5} total")


def main() -> None:
    """Count the directory named on the command line, or the current one."""
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print_report(target, count_python_lines(target))


if __name__ == "__main__":
    main()
```

Four names from that starter.

**`rglob("*.py")`.** Hand back every path under this one whose name ends in
`.py`, at any depth. It is lazy: it yields paths as it finds them rather than
building one enormous list first.

**`is_file()`.** True for a real file. False for a folder, and false for a
symbolic link pointing at nothing. `rglob` matches names, and a *folder* can be
named `vendor.py`.

**`relative_to(root)`.** Chop the leading part off a path so the table shows
`pkg/util.py` instead of forty characters of somebody's home directory.

**`as_posix()`.** Render a path with forward slashes whatever machine you are
on. Without it the table reads `pkg\util.py` on Windows and `pkg/util.py`
everywhere else, and a table that changes shape by platform is a table nobody
can diff.

You will also need a tree to point it at. Build one with a deliberately broken
file in it:

```bash
mkdir -p demo/pkg
printf 'import os\n\n\ndef main():\n    print("hi")\n' > demo/app.py
printf '' > demo/pkg/__init__.py
printf 'def a():\n    return 1\n\n\ndef b():\n    return 2\n' > demo/pkg/util.py
python -c "open('demo/pkg/legacy.py','wb').write('# café\nx = 1\n'.encode('latin-1'))"
```

That last line writes a `.py` file whose bytes are Latin-1, not UTF-8. Nothing
about the filename says so, which is precisely the point.

## Requirements

1. `count_python_lines(root)` returns a `dict[Path, int]` mapping each readable
   `.py` file under `root` to its non-blank line count.
2. The walk uses `pathlib.Path.rglob("*.py")`. No `os.walk`, no string paths.
3. Files are read with `open(..., encoding="utf-8")`.
4. Blank lines do not count. A line of three spaces is blank.
5. `PermissionError`, `UnicodeDecodeError` and any other `OSError` each produce
   one `log.warning` naming the file and the reason, and the file is left out
   of the result. The walk continues.
6. The three `except` clauses are in narrowest-first order, so
   `except PermissionError` sits above `except OSError`.
7. Warnings go through `logging`, never `print`.
8. The table is sorted by path, right-aligned in five columns, followed by
   `-----` and a grand-total line.
9. Every function has type hints on all parameters and on the return, and a
   docstring.
10. Standard library only, and it runs on Python 3.10 or newer.

## Constraints

- **`except PermissionError` must come *above* `except OSError`.**
  `PermissionError` is a subclass of `OSError`. Python tries clauses top to
  bottom and takes the first that matches, so putting the broad one first makes
  the narrow one dead code — no error, no warning, just a specific message that
  never prints again.
- **`except OSError` will never catch a `UnicodeDecodeError`.** It is not an
  `OSError`; it sits under `ValueError`, in a different branch of the tree
  entirely. Reading a file is two steps — the operating system hands over bytes,
  and then Python decodes them — and only the first step raises `OSError`. This
  is the single most common way this challenge fails.
- **The `try` has to cover the *reading*, not just the `open`.** Decoding is
  lazy. `open()` on a Latin-1 file succeeds happily; the error only appears when
  you actually pull a line out of it.
- **Never `except:` and never `except Exception:` here.** Both pass the "does
  not crash" test while defeating its purpose: a typo in your own code becomes
  a warning about somebody's file. Name the three types you actually expect.
- **Check `is_file()`, not `exists()`.** `exists()` is True for a directory,
  and then `open()` raises — `IsADirectoryError` on Linux and macOS,
  `PermissionError` on Windows, so you would even get an inconsistent message.
- **Key the dict by the full `Path`, not by `path.name`.** Keying by name
  merges every `__init__.py` in the tree into one entry and your grand total
  comes out low. Only the full path is unique.
- **Count with `for line in f:`, never `len(f.readlines())`.** `readlines`
  counts blank lines, which the spec forbids, and it loads the whole file into
  memory. Iterating never holds more than one line at a time.
- **Formatting belongs in the printer, not in the counter.**
  `count_python_lines` returns full paths and makes no display decisions.
  `relative_to` and `as_posix` happen in `print_report`. Keep them separate and
  the data structure stays useful to whatever you write next.

## Expected output

Real stdout from the shipped file with no arguments, captured on CPython
3.13.2. With no directory given it builds the demo tree above in a temporary
folder and counts that:

```text
$ python challenge-01-recursive-line-counter.py
    3 app.py
    0 pkg/__init__.py
    4 pkg/util.py
-----
    7 total
```

The warning goes to standard error, so it is not in that block. It looks like
this, with your own temporary path in place of the one here:

```text
WARNING  linecount  skipping C:\...\Temp\tmpxsx_55uz\demo\pkg\legacy.py: not valid UTF-8 (invalid continuation byte)
```

Three things to check in that output.

`legacy.py` is **absent from the table and reported on stderr**. It was not
silently dropped and it did not stop the walk.

`__init__.py` is **present with a count of `0`**. An empty file is a real file
with zero non-blank lines. Skipping it would be a different answer, and a wrong
one.

`3 + 0 + 4 == 7` matches the total line. Check the arithmetic by hand once. A
total that does not match its own table is the classic sign of counting in two
places.

Notice the warning shows backslashes while the table shows forward slashes. The
warning prints a `Path` directly, and `Path.__str__` uses whatever separator
the platform uses. The table goes through `.as_posix()`. That is the split
between "a diagnostic for a human on this machine" and "output another program
might read", and it is worth being deliberate about.

## Steps

1. Build the demo tree with the four commands above, including the Latin-1
   file.
2. Save the starter and run it: `python challenge-01-recursive-line-counter.py
   demo`. With the `TODO`s unfilled you get an empty table and a total of `0`.
   That is a working baseline.
3. Fill in `count_lines`. Run again — you will get a `UnicodeDecodeError`
   traceback, because nothing is catching it yet. Read it before you fix it:

   ```text
   Traceback (most recent call last):
     File "wrong1.py", line 8, in count_python_lines
       counts[path] = sum(1 for line in f if line.strip())
                      ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     File "<frozen codecs>", line 325, in decode
   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
   ```

   Notice where it points: at the line that *reads* the file, not at the
   `open()`. That is the lazy-decoding constraint, demonstrated.
4. Add the three `except` clauses, narrowest first. Run again. The table
   appears and one warning goes to stderr.
5. Add the `is_file()` guard. Prove you need it: `mkdir demo/weird.py`, run,
   and see what happens with and without the guard.
6. Check the total by hand against the table.
7. Prove the two streams are separate:
   `python challenge-01-recursive-line-counter.py demo > report.txt`. The table
   lands in the file; the warning stays on your terminal.
8. Point it at something real — the folder holding this week's material — and
   see whether the number surprises you.

## The Solution

```python
"""challenge-01-recursive-line-counter-solution.py — count lines of Python in a tree.

Walks a directory recursively, counts the non-blank lines in every .py file it
finds, and prints a sorted table plus a grand total. Files it cannot read are
logged at WARNING level and skipped; one unreadable file never stops the walk.

Give it a directory and it counts that directory::

    python challenge-01-recursive-line-counter-solution.py ../some/folder

Give it nothing and it builds a small demo tree in a throwaway temporary
directory first — four files, one of them deliberately not UTF-8 — and counts
that. The demo exists so the download prints something real on a machine with
nothing set up, and so the UnicodeDecodeError branch is visible rather than
merely claimed.

The table goes to stdout and the warnings go to stderr, so
`python challenge-01-recursive-line-counter-solution.py src > report.txt` puts
the counts in the file and leaves the warnings on your screen.
"""

from __future__ import annotations

import logging
import sys
import tempfile
from pathlib import Path

log = logging.getLogger("linecount")


def count_lines(path: Path) -> int:
    """Return the number of non-blank lines in the UTF-8 text file at *path*.

    Iterates the file object rather than calling ``.readlines()`` so that memory
    stays flat no matter how big the file is.
    """
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                total += 1
    return total


def count_python_lines(root: Path) -> dict[Path, int]:
    """Return a dict mapping each .py file under *root* to its line count.

    Files that cannot be read are logged at WARNING level and left out of the
    result. The walk never aborts because of one bad file.
    """
    counts: dict[Path, int] = {}
    for path in root.rglob("*.py"):
        if not path.is_file():
            # rglob matches directories too; a directory literally named
            # "vendor.py" is rare but it exists, and open() would raise
            # IsADirectoryError on POSIX / PermissionError on Windows.
            continue
        try:
            counts[path] = count_lines(path)
        except PermissionError:
            log.warning("skipping %s: permission denied", path)
        except UnicodeDecodeError as e:
            log.warning("skipping %s: not valid UTF-8 (%s)", path, e.reason)
        except OSError as e:
            log.warning("skipping %s: %s", path, e.strerror or e)
    return counts


def print_report(root: Path, counts: dict[Path, int]) -> None:
    """Print a sorted table of files and line counts, then the grand total."""
    for path in sorted(counts):
        relative = path.relative_to(root).as_posix()
        print(f"{counts[path]:>5} {relative}", flush=True)
    print("-----")
    print(f"{sum(counts.values()):>5} total")


def build_demo_tree(root: Path) -> Path:
    """Create the demo tree under *root* and return the folder to count."""
    package = root / "pkg"
    package.mkdir(parents=True, exist_ok=True)
    (root / "app.py").write_text(
        'import os\n\n\ndef main():\n    print("hi")\n', encoding="utf-8"
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "util.py").write_text(
        "def a():\n    return 1\n\n\ndef b():\n    return 2\n", encoding="utf-8"
    )
    # Latin-1 bytes in a .py file: the operating system hands them over
    # happily and Python's UTF-8 decoder refuses them.
    (package / "legacy.py").write_bytes("# café\nx = 1\n".encode("latin-1"))
    return root


def main() -> None:
    """Count the directory named on the command line, or the demo tree."""
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        print_report(target, count_python_lines(target))
        return
    with tempfile.TemporaryDirectory() as workspace:
        target = build_demo_tree(Path(workspace) / "demo")
        print_report(target, count_python_lines(target))


if __name__ == "__main__":
    main()
```

**The three-clause ladder is the whole challenge.** Everything else is a `for`
loop. Here is the shape that makes the order non-negotiable:

```text
Exception
 ├── OSError
 │    ├── PermissionError          <- an "except OSError" catches this too
 │    └── IsADirectoryError
 └── ValueError
      └── UnicodeError
           └── UnicodeDecodeError  <- NOT an OSError. Different branch entirely.
```

Two consequences fall straight out of it. `except PermissionError` must come
*before* `except OSError`, or the specific message never prints and Python
never warns you that a clause is unreachable. And `except OSError` will never
catch a `UnicodeDecodeError`, so a tree with one Latin-1 file in it takes down
a program that only catches `OSError`.

**The `try` wraps the call, not the loop body.** `count_lines` opens the file
inside a `with`, so the file object is closed on the way out whether it
returned normally or raised. The `try` in the caller is purely about *policy* —
what do we do about a bad file — while `count_lines` is purely about
*mechanism*. That separation is why `count_lines` fits in six lines and can be
tested entirely on its own.

**`is_file()` rather than `exists()`.** `rglob("*.py")` matches names, and a
directory can be named `vendor.py`. `exists()` says True for it and then
`open()` raises. `is_file()` asks the question you meant, and it also returns
False for a broken symbolic link, which is exactly right — there is nothing
there to count.

**`if line.strip():` rather than `if line.strip() != "":`.** The empty string
is falsy, so the shorter form is the same test with less noise. `.strip()` with
no argument removes every kind of leading and trailing whitespace, including
`\n`, `\r`, spaces and tabs, so a line holding three spaces correctly counts as
blank.

**The counter returns data and the printer makes it pretty.**
`count_python_lines` hands back `dict[Path, int]` — full paths, no formatting
decisions at all. `print_report` is where `relative_to(root)` and `.as_posix()`
happen. Keeping the conversion in the printer means the dict is still usable by
the next thing you write, whether that is a sorter, a histogram or a JSON dump.

**`logging` and not `print` for the warnings.** `logging` writes to standard
error by default, so redirecting stdout captures the table and nothing else.
`print` would put the warnings in the file too and quietly corrupt the report.

**The `-solution` file takes an argument or builds its own demo.** Given a
directory it counts that directory, exactly like your version. Given nothing it
builds the four-file demo tree — including the deliberately broken Latin-1
file — inside a temporary folder, counts it, and deletes it on the way out.
That is so the download prints something real on a machine with nothing set up,
and so the `UnicodeDecodeError` branch is *demonstrated* rather than claimed.

## Run it

Copy the worked answer on this page into `challenge-01-recursive-line-counter.py` and run it:

```bash
python challenge-01-recursive-line-counter.py
```

With no argument it builds and counts its own demo tree. Give it a folder and
it counts that instead:

```bash
python challenge-01-recursive-line-counter.py ../week-06-file-io-exceptions
```

The `-solution` in the name keeps it from colliding with your own
`challenge-01-recursive-line-counter.py`.

## Common bugs to catch

- **One non-UTF-8 file kills the whole run.**

  ```text
  Traceback (most recent call last):
    File "wrong1.py", line 13, in <module>
      count_python_lines(Path("demo"))
      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
    File "wrong1.py", line 8, in count_python_lines
      counts[path] = sum(1 for line in f if line.strip())
                     ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<frozen codecs>", line 325, in decode
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
  ```

  You caught only `OSError`. Note where the traceback points — inside the
  expression that *consumes* the file, not at the `open()` call. Decoding is
  lazy: `open()` succeeds and the error surfaces on the first read. So
  "I wrapped the `open()` in a `try`" is not enough; the `try` has to cover the
  reading too.

- **A permission failure reports as a generic OS error, forever.**

  ```python
  except OSError as e:
      log.warning("skipping %s: %s", path, e.strerror)
  except PermissionError:               # never reached
      log.warning("skipping %s: permission denied", path)
  ```

  No error and no crash — just a message that can never print, because
  `PermissionError` is an `OSError` and the broad clause matched first. Python
  does not warn about unreachable `except` clauses. Reading the hierarchy is
  your only defence.

- **`IsADirectoryError` (Linux, macOS) or `PermissionError: [Errno 13]`
  (Windows) on a folder.** You skipped the `is_file()` guard and there is a
  directory whose name ends in `.py`. Notice the two platforms give different
  errors for the same situation, which is its own argument for asking
  `is_file()` rather than catching what happens.

- **The grand total is lower than the sum of the table.** You keyed the dict by
  `path.name`, so every `__init__.py` in the tree collapsed into one entry.
  Only the full path is unique, which is why the signature says
  `dict[Path, int]`.

- **Blank lines are being counted.** You used `len(f.readlines())`, which is
  two bugs in six characters: it counts blanks, and it loads the whole file
  into memory.

- **The table prints backslashes on Windows.** You left off `.as_posix()`. Path
  objects render with the platform separator, and a table that changes shape by
  platform cannot be diffed.

- **The warnings end up inside `report.txt`.** You used `print` instead of
  `logging`. `logging` writes to standard error by default, and that default is
  the entire reason to use it here.

## Under the hood

<details>
<summary>Under the hood — what rglob is doing, and what it costs</summary>

`root.rglob("*.py")` looks like magic and is not. It is a **generator**: it
hands you one path at a time, as it finds them, rather than building a list of
everything first. That matters on a big tree — memory stays flat, and the first
result arrives before the walk has finished.

You can see the laziness. Calling it hands back an iterator, not a list:

```text
>>> from pathlib import Path
>>> Path(".").rglob("*.py")
<map object at 0x0000017A669F1390>
```

Nothing has been searched yet. The disk is not touched until you iterate. (The
exact class in that repr is an implementation detail and has changed between
versions; what is promised is that it is lazy.) The signature is worth a look
too:

```text
>>> import inspect
>>> inspect.signature(Path.rglob)
<Signature (self, pattern, *, case_sensitive=None, recurse_symlinks=False)>
```

**`rglob(p)` is `glob("**/" + p)`.** The `**` means "this folder and every
folder below it", so the pattern is matched at every depth. That also explains
a detail people trip on: the match is against the *name*, so `rglob("*.py")`
happily yields a directory called `vendor.py`. It is a name pattern, not a type
filter. Hence `is_file()`.

**Hidden files are not hidden from it.** Unlike a shell's `*`, `rglob` matches
names beginning with a dot, so `.venv/lib/…/thing.py` is in your results unless
you exclude it. That is the third stretch goal, and it is the difference
between counting your project and counting every library your project
installed.

**Sorting is not promised.** The order comes from the filesystem, and it
differs between machines and even between runs. Any output you want to compare
has to be sorted by you, which is why `print_report` calls `sorted(counts)`
rather than trusting the walk.

**Symlinks and the loop that eats your afternoon.** A symbolic link pointing at
a folder above itself makes an infinite tree. Python has protected you here
since 3.13 — `rglob` no longer follows directory symlinks by default, and takes
`recurse_symlinks=True` if you genuinely want that behaviour. On older
versions, `pathlib` also declined to follow them, while `os.walk` will if you
ask it to. Worth knowing which of your tools would spin.

**The one real alternative.** `os.walk` gives you `(dirpath, dirnames,
filenames)` per folder, and its trick is that you can *edit* `dirnames` in
place to stop it descending into a folder at all:

```python
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in {".venv", "__pycache__"}]
```

That prunes whole subtrees before they are visited. `rglob` cannot do that — it
has already descended by the time you see the path, so you filter results
rather than avoid work. On a tree with a large `.venv` in it, `os.walk` is
genuinely faster. This challenge specifies `pathlib` because the path handling
is cleaner and the scale does not matter; know that the other tool exists and
what it is better at.

Since 3.12 there is also `Path.walk()`, which is `os.walk` with `Path` objects,
and it is the answer when you want both.

</details>

<details>
<summary>Under the hood — why "read a file" has two completely separate ways to fail</summary>

The two errors this challenge asks you to survive feel like one problem —
"cannot read this file" — and they are not. Opening a text file stacks two
layers, and each one fails in its own way at its own moment.

**Layer one: bytes.** The operating system finds the file, checks whether you
are allowed, and hands over raw bytes. Everything that can go wrong here is an
`OSError`: the file is missing, you lack permission, the disk is gone, the
network share timed out, the path is a directory.

**Layer two: characters.** Python takes those bytes and decodes them with an
encoding. Everything that can go wrong here is a `UnicodeDecodeError`, which is
a `ValueError`, because it is a problem with the *value* of the data rather
than with the machine.

The two layers are visible in the traceback:

```text
  File "counter.py", line 8, in count_python_lines
    counts[path] = sum(1 for line in f if line.strip())
  File "<frozen codecs>", line 325, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
```

`<frozen codecs>` is layer two. The bytes arrived perfectly; the codebook
rejected them.

**Why `0xe9` in particular is invalid.** UTF-8 encodes a character in one to
four bytes, and the first byte announces how many follow. A byte in the range
`0xE0`–`0xEF` means "I am the start of a three-byte character", and the next
two bytes must each be **continuation bytes**, which start with the bits `10`.
In Latin-1, `é` is the single byte `0xE9`. So a UTF-8 decoder reads `0xE9`,
expects two continuation bytes, gets the ordinary ASCII `\n` instead, and says
so precisely: *invalid continuation byte*. The error message is not being
obtuse. It is telling you exactly which rule broke.

That self-describing structure is why UTF-8 won. Most malformed text fails
loudly instead of quietly decoding into nonsense.

**The three ways to handle a file that is not what you expected**, in the order
you should consider them:

1. **Skip it and say so.** What this challenge specifies. You cannot count what
   you cannot read, and a warning tells the human something is there.
2. **Decode with a fallback policy.** `open(path, encoding="utf-8",
   errors="replace")` puts `�` — the replacement character — where each bad
   byte was and never raises. `errors="ignore"` drops them silently, which is
   almost always wrong, because it makes corrupt data indistinguishable from
   clean data. `errors="surrogateescape"` is the clever one: it tucks the
   unreadable bytes into a reserved range so that encoding the string back out
   reproduces them exactly. That is what makes it the right choice when you are
   *round-tripping* data you do not need to understand.
3. **Detect the encoding.** There is no reliable way to do this from bytes
   alone, because the same bytes are valid text in several encodings.
   Third-party libraries guess with statistics and are usually right, which is
   not the same as right. This challenge is standard library only, and
   guessing is out of scope for a good reason.

One last thing worth knowing: `.py` files have a rule of their own. A Python
source file may declare its encoding in a comment on the first or second line —
`# -*- coding: latin-1 -*-` — and the interpreter honours it. Your counter does
not, because it is counting lines rather than importing modules. A tool that
claimed to understand Python source would have to read that comment first,
which is a nice illustration of how much specification hides behind the phrase
"just read the file".

</details>

## Acceptance checklist

- [ ] The script runs to the end with a broken file in the tree and no traceback.
- [ ] `except PermissionError` sits above `except OSError` in the file.
- [ ] `except UnicodeDecodeError` exists and is not assumed to be covered by `OSError`.
- [ ] There is no bare `except:` and no `except Exception:` anywhere.
- [ ] The dict is keyed by full `Path`, not by name.
- [ ] Blank lines are not counted; an empty file appears with a count of `0`.
- [ ] The table is sorted, uses forward slashes on every platform, and its
      numbers add up to the grand total.
- [ ] Redirecting stdout to a file leaves the warnings on the terminal.
- [ ] Every function has full type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 challenge 1: recursive line counter`.

## Stretch

Each of these is a small, self-contained addition. Do them one at a time and
run after each.

1. **Count other extensions.** Accept `--ext .py,.md` and count all of them.
   `rglob` takes one pattern, so several extensions means one `rglob` per
   extension writing into the same dict. Duplicates are impossible, since a
   file has one name. Normalise the input so `--ext py,md` and `--ext .py,.md`
   both work.

2. **Sort by count.** Accept `--sort-by-count` and order the table largest
   first. The key you want is `lambda kv: (-kv[1], kv[0])`: negate the count so
   the biggest sorts first, then fall back to the path so equal counts come out
   in a stable order rather than in filesystem order. A tuple sort key is how
   you say "primary key descending, secondary ascending" in one pass.

3. **Exclude `__pycache__/` and `.venv/`.** Check every *directory* component
   of the path against a `frozenset` of excluded names — and use
   `path.relative_to(root).parts[:-1]` so that a *file* honestly named `.venv`
   is not excluded. Membership in a frozenset is a constant-time check, which
   matters when you are walking a real project.

4. **Draw a histogram.** `round(count / largest * width)` scales each bar
   against the largest file *shown*, so the top bar is always full width. Wrap
   it in `max(1, ...)` so a small-but-nonzero file does not render as an empty
   bar, which would read as zero.

   One thing will bite you. Printing `█` (U+2588 FULL BLOCK) on a default
   Windows console gives you this:

   ```text
   UnicodeEncodeError: 'charmap' codec can't encode characters in position 19-38: character maps to <undefined>
   ```

   That is not a bug in your histogram. It is the console's code page refusing
   to represent a character your string legitimately contains — the same family
   of problem as the `encoding="utf-8"` rule from Exercise 1, applied to the
   *output* stream instead of a file. `sys.stdout.reconfigure(encoding="utf-8")`
   fixes it in one line; falling back to `#` when that raises is the polite
   version.

5. **Add `--top N`.** Show only the N largest files. Truncate *after* sorting,
   compute the grand total from everything rather than from the visible slice,
   and print a `... N more file(s) not shown` line so nobody misreads a
   truncated table as the whole tree.

When your counter survives a tree with a broken file in it, move on to
[Challenge 2 — Config Validator](./challenge-02-config-validator.md).
