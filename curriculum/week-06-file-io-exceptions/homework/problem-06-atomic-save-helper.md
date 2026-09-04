# Homework Problem 6 — Atomic-Save Helper

> **Topic:** replacing a file so completely that a failure halfway through leaves the old one untouched
> **Lecture:** [Lecture 01 — Files and pathlib](../lecture-notes/01-files-and-pathlib.md)
> **Difficulty:** Advanced
> **Target time:** 1 hour
> **Why this one:** every save you have written so far empties the file first and then fills it. In between those two moments the file is wrong, and if anything goes wrong in that window it stays wrong. This is the pattern that closes the window, and it is four lines.

## The Brief

Look closely at what `path.write_text(new_content)` really does:

1. Open the file for writing, which **empties it immediately**.
2. Write the new content.
3. Close it.

Between step 1 and step 3 the file is not the old version and not the
new version. It is a truncated thing that is neither. If your program
crashes there — or the disk fills, or somebody pulls the power, or the
watcher from problem 5 happens to read it at that exact moment — that is
what is left.

Now the safe version, which is one idea and no cleverness:

1. Write everything to a **different** file, sitting next to the target.
2. When that has finished successfully, **rename** it over the target.

A rename is **atomic**: the filesystem does it in one indivisible step.
At every instant the name refers either to the whole old file or to the
whole new file. There is no moment when it is half of each, and no
moment when it is missing.

Write a script `atomic.py` with one function:

```python
def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write `content` to `path` atomically.

    The write is done to a temporary file first; on success it is renamed
    over `path`. Readers either see the old file or the new file, never
    a half-written one.
    """
```

Then demonstrate it. Overwrite a file successfully. Then **make a write
fail on purpose, partway through**, and show that the original file is
still exactly what it was.

## Starter

Save this as `atomic.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it writes the temp file and never renames
it, so the target never changes:

```python
"""Replace a file's contents without ever leaving it half-written."""

from __future__ import annotations

import logging
from collections.abc import Iterable
from pathlib import Path

log = logging.getLogger("atomic")


def atomic_write_chunks(
    path: Path, chunks: Iterable[str], encoding: str = "utf-8"
) -> None:
    """Write the concatenation of `chunks` to `path` atomically.

    Args:
        path: The file to replace.
        chunks: Pieces of text, written in order.
        encoding: The text encoding to write with.
    """
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    # TODO: wrap the write in try/finally
    with tmp_path.open("w", encoding=encoding, newline="") as f:
        for chunk in chunks:
            f.write(chunk)
    # TODO: rename the temp file over the target with tmp_path.replace(path)
    # TODO: in `finally`, remove the temp file with unlink(missing_ok=True)


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write `content` to `path` atomically.

    Args:
        path: The file to replace.
        content: The complete new contents.
        encoding: The text encoding to write with.
    """
    atomic_write_chunks(path, [content], encoding=encoding)


def failing_chunks() -> Iterable[str]:
    """Yield half a document, then blow up -- a simulated producer failure."""
    yield "REPLACEMENT LINE 1\n"
    yield "REPLACEMENT LINE 2\n"
    raise RuntimeError("simulated failure halfway through the write")


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    target = Path("important.txt")
    target.write_text("ORIGINAL LINE 1\nORIGINAL LINE 2\n", encoding="utf-8")
    print(f"before:            {target.read_text(encoding='utf-8')!r}")

    atomic_write_text(target, "REWRITTEN LINE 1\nREWRITTEN LINE 2\n")
    print(f"after good write:  {target.read_text(encoding='utf-8')!r}")
    # TODO: call atomic_write_chunks(target, failing_chunks()) inside a
    #       try/except RuntimeError, log the failure, then print the file
    #       again and list any leftover *.tmp files
```

Notice the shape of the helper. The required function takes a single
string, and that is what `atomic_write_text` is. Underneath it,
`atomic_write_chunks` takes an **iterable** of strings — pieces produced
one at a time. That is not extra credit. It is the only honest way to
simulate a failure *during* a write, because a single complete string in
memory has nothing left that can go wrong.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-06-file-io-exceptions/homework/problem-06-atomic-save-helper.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `atomic_write_text(path, content, encoding="utf-8") -> None` writes
   `content` to `path` and returns nothing.
2. The content is written to a temporary file first, named from the
   target — `path.with_suffix(path.suffix + ".tmp")` is the shape the
   brief suggests.
3. The temporary file is renamed over the target with
   `tmp_path.replace(path)` only after the write has finished.
4. On any failure the temporary file is removed, in a `finally`.
5. Running the file demonstrates a successful overwrite, then a write
   that fails partway through, and shows that the original survived it.
6. Every function has type hints and a docstring.

## Constraints

- **`Path.replace`, never `Path.rename`.** On Linux and macOS, `rename`
  quietly overwrites an existing target. On Windows it raises. `replace`
  overwrites on **both**, which is why the brief names it specifically.
- **The temporary file must be a sibling of the target.** An atomic
  rename is an operation on one directory inside one filesystem. Put the
  temporary file in the system temp folder and, whenever that folder
  happens to be on a different drive, `replace` cannot rename — it has to
  copy the bytes and delete the source, which is not atomic at all.
- **Clean up in `finally`, not in `except`.** `finally` runs on every
  way out: success, exception, and Ctrl-C. `except Exception` misses
  `KeyboardInterrupt` and leaves a `.tmp` file behind exactly when the
  person at the keyboard is already annoyed.
- **`unlink(missing_ok=True)`.** After a successful rename the temporary
  file no longer exists, so a plain `unlink` in the `finally` would
  raise `FileNotFoundError` from inside your cleanup — an error while
  handling an error, and the original exception is what gets lost.
- **The `with` block must close before the rename.** Renaming a file
  that still has data sitting in Python's buffer publishes a truncated
  document through the very mechanism designed to prevent that.

## Expected output

The demonstration runs in a scratch folder it creates and deletes, so
the shipped answer works from a clean checkout and leaves nothing
behind:

```bash
$ python problem-06-atomic-save-helper.py
```

```text
before:            'ORIGINAL LINE 1\nORIGINAL LINE 2\n'
after good write:  'REWRITTEN LINE 1\nREWRITTEN LINE 2\n'
after failed write:'REWRITTEN LINE 1\nREWRITTEN LINE 2\n'
temp files left:   []
```

The complaint about the failed write went to stderr:

```console
WARNING  atomic  write failed: simulated failure halfway through the write
```

Read those four lines as the proof they are:

1. The original content is on disk.
2. A successful atomic write replaced it, so the mechanism works at all.
3. The next write got two lines into the temporary file and then raised.
4. **`important.txt` still holds the content from step 2**, character
   for character. The failed write did not touch it. That is the
   property.

And `temp files left: []` says the `finally` ran. Nothing was abandoned.

## Steps

1. Activate your Week 6 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `atomic.py` and run it. Both printed lines show
   the original content — the write went into `important.txt.tmp` and
   was never renamed. Look in the folder and you will see it sitting
   there.
3. Add `tmp_path.replace(path)` after the `with` block, outside it. Run
   again. The second line now shows the rewritten content.
4. Add the `try` / `finally` around both, with
   `tmp_path.unlink(missing_ok=True)` in the `finally`. Run again —
   nothing changes, which is the point: on success the `finally` is a
   no-op because the file has already been renamed away.
5. Fill in the last `TODO`. Call `atomic_write_chunks(target,
   failing_chunks())` inside `try` / `except RuntimeError`, log it, then
   print the file's contents and the list of leftover `*.tmp` files.
6. Run it. You want the failed write to leave the file exactly as step 3
   left it, and no temporary files behind.
7. Prove the mechanism instead of inferring it. Watch the temporary file
   exist while the target is still the old version:

   ```bash
   python -c "
   import importlib.util
   from pathlib import Path
   spec = importlib.util.spec_from_file_location('atomicmod', 'atomic.py')
   m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
   target = Path('important.txt')
   def chunks():
       yield 'A\n'
       print('  mid-write: important.txt =', repr(target.read_text(encoding='utf-8')))
       print('  mid-write: temp exists   =', Path('important.txt.tmp').exists())
       yield 'B\n'
   m.atomic_write_chunks(target, chunks())
   print('  after:      important.txt =', repr(target.read_text(encoding='utf-8')))
   "
   ```

   Halfway through, the temporary file exists and `important.txt` is
   still entirely the old version.
8. Compare against **The Solution**, work down the acceptance checklist,
   and commit: `git add homework/atomic.py` then
   `git commit -m "Week 6 homework: atomic-save helper"`.

## The Solution

```python
"""Homework 6 — atomic-save helper.

`atomic_write_text` writes to a sibling temp file and renames it over the
target, so a reader sees either the whole old file or the whole new one --
never a half-written one -- and a failure mid-write leaves the original intact.

    python atomic.py

The demonstration runs in a scratch folder it creates and deletes, so the
download works from a clean checkout and leaves nothing behind.

Save your own copy as ``atomic.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import logging
import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

log = logging.getLogger("atomic")


def atomic_write_chunks(
    path: Path, chunks: Iterable[str], encoding: str = "utf-8"
) -> None:
    """Write the concatenation of *chunks* to *path* atomically.

    The general form. `atomic_write_text` is the one-string case. Taking an
    iterable means the caller can stream a large document without building it
    in memory -- and it is what makes a genuine mid-write failure possible to
    demonstrate, because the exception can come from the producer.

    Args:
        path: The file to replace.
        chunks: Pieces of text, written in order.
        encoding: The text encoding to write with.
    """
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp_path.open("w", encoding=encoding, newline="") as f:
            for chunk in chunks:
                f.write(chunk)
        # Only reached if every chunk was produced and written. `replace`
        # overwrites an existing target; `rename` would raise FileExistsError
        # on Windows. Same directory, so it never crosses a filesystem.
        tmp_path.replace(path)
    finally:
        # A no-op after a successful replace (the temp file no longer exists),
        # and the cleanup on every failure path, including KeyboardInterrupt.
        tmp_path.unlink(missing_ok=True)


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write `content` to `path` atomically.

    The write is done to a temporary file first; on success it is renamed
    over `path`. Readers either see the old file or the new file, never
    a half-written one.

    Args:
        path: The file to replace.
        content: The complete new contents.
        encoding: The text encoding to write with.
    """
    atomic_write_chunks(path, [content], encoding=encoding)


# --------------------------------------------------------------------------- #
# Demonstration
# --------------------------------------------------------------------------- #
def failing_chunks() -> Iterable[str]:
    """Yield half a document, then blow up -- a simulated disk/producer failure.

    Yields:
        Two replacement lines, before raising.

    Raises:
        RuntimeError: Always, after the second chunk.
    """
    yield "REPLACEMENT LINE 1\n"
    yield "REPLACEMENT LINE 2\n"
    raise RuntimeError("simulated failure halfway through the write")


def _demo() -> int:
    """Overwrite a file safely, then fail mid-write and show it survived.

    The scratch folder is a temporary directory this function makes and
    deletes, so the demo needs nothing placed by hand and leaves nothing
    behind.

    Returns:
        Always 0. The failed write is the point, not an error.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="atomic_") as scratch:
        try:
            os.chdir(scratch)
            target = Path("important.txt")
            target.write_text("ORIGINAL LINE 1\nORIGINAL LINE 2\n", encoding="utf-8")
            print(f"before:            {target.read_text(encoding='utf-8')!r}")

            atomic_write_text(target, "REWRITTEN LINE 1\nREWRITTEN LINE 2\n")
            print(f"after good write:  {target.read_text(encoding='utf-8')!r}")

            try:
                atomic_write_chunks(target, failing_chunks())
            except RuntimeError as e:
                log.warning("write failed: %s", e)

            print(f"after failed write:{target.read_text(encoding='utf-8')!r}")
            leftovers = sorted(p.name for p in target.parent.glob("*.tmp"))
            print(f"temp files left:   {leftovers}")
        finally:
            os.chdir(home)
    return 0


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    raise SystemExit(_demo())
```

**Why it works.**

**What "atomic" actually promises.** The filesystem guarantees that a
rename-over is one indivisible operation. At every instant, the name
refers either to the old file or to the new one. There is no window in
which it is half of each, and no window in which it does not exist. That
is the *only* guarantee, and it is exactly the one you want, because the
failure it removes — somebody reading the file while a writer is partway
through — is the common one.

Compare the naive version. `path.write_text(content)` truncates the file
to zero bytes and then writes. Between those two steps, which can be
milliseconds apart on a large document, any reader sees an empty or
truncated file. Your watcher from problem 5 prints garbage; a config
loader raises `JSONDecodeError` on a file that is perfectly valid one
tick later.

**`replace`, never `rename`.** This is the Windows detail that catches
everybody:

```text
>>> tmp.rename(target)          # target already exists
FileExistsError: [WinError 183] Cannot create a file when that file already exists: 'rn.txt.tmp' -> 'rn.txt'
```

The whole point of the operation is overwriting, so the target always
exists. `replace` is the portable one.

**The temporary file has to be a sibling.**
`path.with_suffix(path.suffix + ".tmp")` puts it in the same directory
as the target, and that is load-bearing rather than tidy. An atomic
rename is a directory-entry operation within one filesystem. Move the
temporary file to the system temp folder and, whenever that happens to
be on a different volume, `replace` cannot rename at all — on Linux you
get `OSError: [Errno 18] Invalid cross-device link`.

**`finally`, because it is the only clause that always runs.**

| Exit path | What `finally` does |
|---|---|
| Success | the temp file was renamed away, so `unlink(missing_ok=True)` does nothing |
| The producer raises | the temp file holds a partial document; it is deleted; the exception carries on |
| The disk fills during `f.write` | the same |
| Ctrl-C | the same — `finally` runs for `BaseException` too |

`except Exception: cleanup; raise` misses `KeyboardInterrupt`.
`missing_ok=True` is what makes the success case a no-op instead of a
`FileNotFoundError` thrown from inside your own cleanup.

**The `with` closes before the rename.** The rename is written *after*
the `with` block ends, so the file object is closed and its buffer
flushed to disk first. Put `tmp_path.replace(path)` inside the `with` and
you have built an elaborate way to do the unsafe thing.

**Why the general function takes chunks.** The required signature takes
a `str`, and `atomic_write_text` provides exactly that. But "simulate a
failure mid-write", which the brief explicitly asks for, is impossible
if the content is already a complete string in memory — there is nothing
left to fail. Consuming an iterable means the demonstration can hand it
a generator that yields two lines and then raises, which is a genuine
failure partway through, with real bytes already in the temporary file.
No test hooks and no duplicated function. The streaming version is
independently useful for documents too large to build in memory.

## Run it

Copy the worked answer on this page into `problem-06-atomic-save-helper.py` and run it:
and run it:

```bash
python problem-06-atomic-save-helper.py
```

It creates its own file in a temporary folder, overwrites it once
successfully and once with a deliberate failure, and deletes the folder
on the way out, so it runs anywhere with nothing set up and leaves
nothing behind.

Save your own copy as `atomic.py` in your homework folder, and commit
that one. The longer download name is there so it cannot overwrite your
work.

## Common bugs to catch

- **`tmp_path.rename(path)`.** Passes every test on macOS and Linux.
  Fails on Windows the first time the target already exists — which is
  always, because overwriting is the entire job:

  ```text
  FileExistsError: [WinError 183] Cannot create a file when that file already exists: 'rn.txt.tmp' -> 'rn.txt'
  ```

- **Putting the temporary file in the system temp folder.**
  `tempfile.NamedTemporaryFile()` feels like exactly the right tool, and
  it defaults to a directory that may be on another drive. When it is:

  ```text
  OSError: [Errno 18] Invalid cross-device link
  ```

  Worse, it only happens on *some* machines, so it passes on your laptop
  and fails in the container. If you want `tempfile`, use
  `tempfile.NamedTemporaryFile(dir=path.parent, delete=False)`. The
  `dir=` is the part that matters.
- **Cleaning up in `except` instead of `finally`.**

  ```python
  except Exception:
      tmp_path.unlink(missing_ok=True)
      raise
  ```

  Leaves the `.tmp` file behind on `KeyboardInterrupt` and `SystemExit`,
  because neither of those is an `Exception`. And without
  `missing_ok=True` you can raise `FileNotFoundError` from inside your
  own cleanup, which replaces the original error with a confusing one.
- **Calling `replace` inside the `with`.** The file is still open and
  its buffer is unflushed, so you publish a partial document through the
  mechanism designed to prevent that.
- **"Simulating" the failure by deleting the target first.** Some
  answers demonstrate safety by removing `important.txt` and showing
  that the write recreates it. That demonstrates nothing. The claim
  under test is that the *original survives a failed write*, so the
  original has to be there, with known contents, both before and after.
- **Forgetting that `with_suffix` needs a name.**
  `Path("archive.tar.gz").suffix` is `".gz"`, so the temp file is
  `archive.tar.gz.tmp` — fine. `Path("notes")` has an empty suffix, so
  you get `notes.tmp` — fine. `Path(".gitignore")` also has an empty
  suffix, because a leading dot is not a suffix, giving
  `.gitignore.tmp` — still fine. The one input that raises is a path
  with no name at all, like `Path(".")`, and a caller asking to
  atomically write to `.` has a larger problem than this function.

## Under the hood

<details>
<summary>Under the hood — what happens to an open file when the process dies</summary>

There are three different deaths and they do not have the same
consequences. Knowing which is which is what tells you when `with` is
enough and when it is not.

**The exception you catch, and the `with` block.** An exception
propagating out of a `with` runs the file object's exit handler on the
way past. The buffer is flushed, the file is closed, the operating
system is told. Nothing is lost. This is the whole reason `with` exists,
and it covers the overwhelming majority of failures.

```python
with path.open("w", encoding="utf-8") as f:
    f.write("half")
    raise RuntimeError("boom")     # "half" is still flushed and closed
```

**The process being killed — `SIGKILL`, Task Manager, `kill -9`.** Your
`finally` does not run. Your `with` does not run. Python does not get a
say. But the file is not lost either, and this surprises people: an open
file is an object held by the **kernel**, not by your program. When a
process dies for any reason, the kernel closes every file it had open
and flushes what was in *its* buffers.

What you lose is only what was still in **Python's** buffer and had not
reached the kernel yet. `f.write("hello")` normally copies into a
user-space buffer of a few kilobytes and only calls the operating system
when that fills up, or on close.

```python
f.write("important")
f.flush()          # now the kernel has it; a killed process cannot lose it
```

So the ladder is: **Python buffer → kernel page cache → the actual
disk.** `flush()` moves you from the first to the second and protects
against your process dying. It does *not* protect against the machine
losing power.

**The machine losing power.** The kernel's page cache is in RAM. Data
that reached the kernel but not the platter is gone. That is what
`os.fsync` is for:

```python
f.flush()
os.fsync(f.fileno())        # the file's bytes are physically stored
```

And on POSIX, for a rename like this problem's, the *directory entry*
needs the same treatment, because it is a separate piece of metadata:

```python
dir_fd = os.open(path.parent, os.O_RDONLY)
os.fsync(dir_fd)
os.close(dir_fd)
```

This is where the distinction that matters lives:

| Property | What it promises | What buys it |
|---|---|---|
| **Atomic** | a reader sees the whole old file or the whole new one | `replace` over a fully-written sibling |
| **Durable** | the new file survives a power cut | `fsync` on the file, and on the directory |

This problem asks for atomicity, and gets it. Durability costs real
performance — `fsync` waits for the hardware — and databases pay it on
every commit because that is their job. Most programs do not need it.
Knowing which one you have is the difference between somebody who copied
the pattern and somebody who understands it.

**One last case: the file nobody closed.** If you open a file and never
close it and never use `with`, CPython usually closes it anyway, when
the object's last reference goes away and it is collected. Usually. You
get a warning if you are running with them enabled:

```text
ResourceWarning: unclosed file <_io.TextIOWrapper name='out.txt' mode='w' encoding='utf-8'>
```

Do not rely on it. It is a CPython implementation detail rather than a
language promise, the timing is not something you can predict, and on
other Python implementations the collection may not happen for a long
time. `with` is the promise; garbage collection is a safety net with
holes in it.

</details>

<details>
<summary>Under the hood — where atomic replace is used, and where it is not enough</summary>

Once you have seen this pattern you start seeing it everywhere.

**Editors.** Many text editors save by writing a new file and renaming
it over the old one. That is why a file's inode number can change when
you save it, and why file watchers that follow an inode rather than a
name lose track of the file after a save. Problem 5's watcher follows
the *name*, so it copes.

**Package managers and build tools.** Downloading to `thing.partial` and
renaming to `thing` on completion is how you can interrupt a download
and know the cache is not poisoned.

**Configuration.** Anything that reads a config file at intervals — a
web server, a monitoring agent — is a reader that must never see a
half-written file. The writer using an atomic replace is what makes the
reader's job possible.

**Where it is not enough:**

**More than one file has to change together.** Atomic replace gives you
one file at a time. If `index.json` and `data.csv` must agree, replacing
each atomically still leaves a moment where one is new and the other is
old. Fixing that needs either a single file holding both, or a
directory-level swap, or a real database and a transaction.

**Two writers at once.** Both write their own temp file, both rename.
The second rename wins, completely, and the first writer's changes
vanish without an error. Atomicity says nobody sees a *torn* file; it
does not say nobody loses. That needs a lock, or a compare-and-swap on a
version number.

**Appending.** This pattern rewrites the whole file. For a log file that
grows forever it is exactly wrong — you would rewrite gigabytes to add a
line. Appends have their own guarantee: a single `write` to a file
opened in append mode is atomic up to a size limit, which is why several
processes can share one log file without interleaving mid-line.

**Directories.** There is no atomic "replace this directory with that
one". The usual trick is a symbolic link that points at a versioned
directory, and replacing the *link* atomically — which is the same idea
one level up.

</details>

## Acceptance checklist

- [ ] `python atomic.py` prints four lines showing before, after a good
      write, after a failed write, and the leftover temp files.
- [ ] The content after the failed write is identical to the content
      after the good write.
- [ ] `temp files left:` is an empty list.
- [ ] The rename uses `Path.replace`, not `Path.rename`.
- [ ] The temporary file is a sibling of the target, not in the system
      temp folder.
- [ ] The cleanup is in a `finally`, with `missing_ok=True`.
- [ ] `tmp_path.replace(path)` is outside the `with` block.
- [ ] The failure is a real failure during the write, not a deleted
      target.
- [ ] Every function has type hints and a docstring.
- [ ] Committed with a message like
      `Week 6 homework: atomic-save helper`.

## Stretch

- **Make it a context manager.** `with atomic_write(path) as f:` where
  `f` is the temporary file, and leaving the block does the rename. The
  week's own [stretch goals](../README.md#stretch-goals) suggest exactly
  this, and it is what Week 7's `__enter__` and `__exit__` are for.
- **Add a `durable=False` option.** When `True`, `flush` and `fsync` the
  file before the rename, and `fsync` the parent directory after it on
  POSIX. Time a thousand writes with it on and off, and you will
  understand why it is not the default.
- **Preserve the target's permissions.** A brand-new temporary file gets
  default permissions, so replacing a file that somebody had made
  read-only, or group-writable, quietly changes that. Copy the mode
  across with `os.chmod` before the rename. Real implementations of this
  pattern all do.
- **Add a binary version.** `atomic_write_bytes`. Almost the same
  function with `"wb"` and no encoding — which is itself worth noticing,
  because it shows exactly how much of the text machinery is about
  encoding and how little is about safety.
- **Break it four ways and watch each one.** Use `rename` and run it on
  Windows. Put the temp file in `tempfile.gettempdir()` and try it
  across drives. Move the cleanup into an `except Exception` and press
  Ctrl-C mid-write. Move `replace` inside the `with` and read the
  result. Each failure is more memorable than the rule that prevents it.

Next: the [Mini-Project — Log File Analyzer](../mini-project/README.md),
which brings this week's whole toolkit together.
