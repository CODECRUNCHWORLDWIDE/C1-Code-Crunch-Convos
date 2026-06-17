# Lecture 01 — Files and `pathlib`

> **Read time:** ~30 min. **Type-along time:** ~60 min. Have a REPL open and a scratch directory called `week06_scratch/` ready.

Up until now your programs have lived in RAM. The moment you closed the REPL, every variable you defined evaporated. That is fine for learning, but it is not how real software works. Real programs **read** data from somewhere — configuration files, CSV exports, log files, user input — and **write** results back out. That "somewhere" is almost always the filesystem.

This lecture covers the foundation: how to open files, how to read and write them safely, how to use the modern `pathlib` API for paths, and how to avoid the classic mistakes that bite every beginner (forgetting to close a file, getting an encoding error, hard-coding `/` on Windows).

---

## 1. The `open()` function and file modes

The built-in `open()` function returns a **file object**. The two arguments you will use 99% of the time are the **path** and the **mode**.

```python
f = open("notes.txt", "r", encoding="utf-8")
contents = f.read()
f.close()
print(contents)
```

That works, but it has a serious bug — if `f.read()` raises an exception, `f.close()` never runs and the file stays open. We will fix that in section 2 with the `with` statement. For now, focus on the mode argument.

### Modes

| Mode | Meaning | If file exists | If file missing |
|---|---|---|---|
| `"r"` | Read text (the default) | Open for reading | Raises `FileNotFoundError` |
| `"w"` | Write text | **Truncates to empty** | Creates it |
| `"a"` | Append text | Opens, writes go to end | Creates it |
| `"x"` | Exclusive create | Raises `FileExistsError` | Creates it |
| `"r+"` | Read **and** write text | Opens, cursor at start | Raises `FileNotFoundError` |
| `"rb"` / `"wb"` / `"ab"` | Binary versions | Same as above | Same as above |

Two things to internalize:

1. **`"w"` is destructive.** It silently throws away whatever was in the file. If you want to add to a file, use `"a"`.
2. **The default is text mode.** Python decodes the bytes from disk into `str` for you. If you want raw bytes (images, zip files, anything non-text), add `b`: `"rb"`, `"wb"`, `"ab"`.

You can combine flags: `"r+b"` means "read and write, binary". You almost never need this as a beginner.

### The cursor

A file object has a **position** (sometimes called the "cursor" or "seek pointer"). Reading advances it. You can ask where it is with `f.tell()` and move it with `f.seek(offset)`. In `"r+"` mode the cursor starts at byte 0; in `"a"` mode it starts at the end. This matters for one edge case: if you open in `"r+"` and call `f.write("X")`, the `X` **overwrites** whatever byte was at the cursor — it does not insert. Treat files as a fixed grid of bytes, not as a text editor.

---

## 2. The `with` statement — context managers

The single most important habit in Python file I/O: **always use `with`**.

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    contents = f.read()
# f is automatically closed here, even if an exception was raised inside the block
print(contents)
```

`with` is shorthand for "set up a resource, run a block of code, tear down the resource no matter what happens." The technical name for this pattern is a **context manager**. `open()` returns one; the `with` statement calls its `__enter__` method to get the file object (which we name `f`) and guarantees `__exit__` runs at the end of the block.

Why does this matter?

- **Limited resource.** Operating systems cap the number of open file handles per process. A program that forgets to close files will eventually crash with "Too many open files."
- **Buffering.** Writes are buffered in memory and only flushed to disk when the file is closed (or `.flush()` is called). If you do not close the file properly, the last chunk of data may never reach disk.
- **Exception safety.** If your code between `open()` and `close()` raises, `close()` never runs — unless you wrap it in a `try`/`finally`. `with` does that for you.

You can manage multiple files in one `with`:

```python
with open("input.txt", "r", encoding="utf-8") as src, \
     open("output.txt", "w", encoding="utf-8") as dst:
    for line in src:
        dst.write(line.upper())
```

> **Rule of thumb:** if you see `open(...)` without a `with` in a code review, ask why.

We will revisit context managers in Week 7 when we learn to build our own.

---

## 3. Encodings — and why you should always pass `encoding="utf-8"`

Text files on disk are sequences of **bytes**. Turning bytes into Python `str` requires picking an **encoding**, a mapping between byte sequences and characters. The most common encodings you will see are:

- **UTF-8** — the modern standard. Variable-width (1–4 bytes per character). Compatible with ASCII. The right answer for almost everything you will write.
- **ASCII** — 7-bit, only English letters/digits/punctuation. A strict subset of UTF-8.
- **Latin-1** (also called `iso-8859-1`) — 1 byte per character, common in older European data.
- **Windows-1252** (often labeled "ANSI") — Microsoft's near-Latin-1 variant. Very common in CSVs exported from Excel.

If you do not pass an `encoding` argument, Python uses the **platform default**, which is *different on different machines* (UTF-8 on macOS/Linux, often cp1252 on Windows). This is the source of "works on my laptop, breaks on the server" bugs.

**Always pass `encoding="utf-8"` explicitly.** Always.

```python
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()
```

If a file is in a different encoding and you read it as UTF-8, you will get `UnicodeDecodeError`. The fix is to figure out the real encoding (often by asking whoever made the file) and pass that. As a last resort, `encoding="utf-8", errors="replace"` will substitute weird bytes with `?` instead of crashing.

See the docs: [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files).

---

## 4. Reading: three patterns

There are three idiomatic ways to read a text file. Pick the right one for the job.

### Pattern A — line-by-line iteration (the default)

```python
with open("big.log", "r", encoding="utf-8") as f:
    for line in f:
        process(line.rstrip("\n"))
```

This is **lazy** — it reads one line at a time and never holds the whole file in memory. Use it for log files, CSVs, anything that might be large. The newline character (`\n`) is included at the end of each line, which is why we usually call `.rstrip("\n")` or `.rstrip()`.

### Pattern B — `.read()` to slurp the whole file

```python
with open("config.toml", "r", encoding="utf-8") as f:
    text = f.read()
```

Returns the entire content as one big `str`. Convenient for small files (config, small JSON, README). Dangerous for large files.

### Pattern C — `.readlines()` to get a list

```python
with open("names.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()  # list[str], each ends with "\n"
```

Same memory cost as `.read()`, but you get a list. Useful if you need to index into the file (`lines[42]`) or know the line count up front.

### Which one?

- **Big file, processing each line?** Pattern A.
- **Small file, single string?** Pattern B.
- **Small file, need a list?** Pattern C.

When in doubt, default to Pattern A. It is the most general and the cheapest.

---

## 5. Writing: `.write`, `.writelines`, and `print(..., file=)`

### `.write()`

The basic primitive. Takes a `str`, returns the number of characters written. **Does not add a newline** — you have to include `\n` yourself.

```python
with open("greeting.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.write("World\n")
```

### `.writelines()`

Takes an iterable of strings and writes each one. Confusingly, **also does not add newlines** — the name is a misnomer.

```python
lines = ["one\n", "two\n", "three\n"]
with open("nums.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
```

If your list does not already have `\n` at the end of each element, you need to add them, e.g. `f.writelines(line + "\n" for line in lines)`.

### `print(..., file=...)`

The friendliest option. `print` accepts a `file=` keyword that redirects its output to any file-like object. It **does** add a newline by default.

```python
with open("greeting.txt", "w", encoding="utf-8") as f:
    print("Hello", file=f)
    print("World", file=f)
```

This is great for one-off scripts because you keep the familiar `print` formatting (multiple arguments, `sep=`, `end=`).

---

## 6. `pathlib.Path` — the modern way to handle paths

For decades Python's path handling lived in `os.path`, a module of free functions that take and return strings:

```python
import os.path
config = os.path.join(os.path.dirname(__file__), "config", "app.json")
if os.path.isfile(config):
    ...
```

Python 3.4 introduced **`pathlib`**, which models paths as **objects** with methods. It is cleaner, cross-platform, and what you should use in new code.

```python
from pathlib import Path

config = Path(__file__).parent / "config" / "app.json"
if config.is_file():
    ...
```

The `/` operator joins path segments. It works on any OS — on Windows it produces `\` separators, on macOS/Linux it produces `/`. You never need to think about it.

### Useful `Path` methods

```python
from pathlib import Path

p = Path("/Users/jane/notes/draft.md")

p.name        # 'draft.md'
p.stem        # 'draft'
p.suffix      # '.md'
p.parent      # Path('/Users/jane/notes')
p.parts       # ('/', 'Users', 'jane', 'notes', 'draft.md')

p.exists()    # True / False
p.is_file()   # True if file
p.is_dir()    # True if directory

p.read_text(encoding="utf-8")   # whole file as str — shortcut for open+read
p.write_text("hello\n", encoding="utf-8")  # shortcut for open+write
p.read_bytes()                  # for binary files
p.write_bytes(b"\x00\x01")
```

`read_text` and `write_text` are wonderful for small files — no `with` block needed because `pathlib` opens, reads, and closes for you.

### Globbing

`Path.glob(pattern)` and `Path.rglob(pattern)` find files matching a wildcard. `glob` is shallow, `rglob` is recursive.

```python
for py_file in Path("src").rglob("*.py"):
    print(py_file)
```

### Creating directories

```python
Path("output/reports").mkdir(parents=True, exist_ok=True)
```

`parents=True` creates intermediate directories. `exist_ok=True` makes the call idempotent — no error if it already exists.

Full reference: [`pathlib` docs](https://docs.python.org/3/library/pathlib.html).

---

## 7. Reading binary files (brief)

Not everything is text. Images, zip files, PDFs, audio — all binary. You read them in mode `"rb"` and get `bytes`, not `str`.

```python
with open("photo.jpg", "rb") as f:
    data = f.read()    # bytes
print(len(data), "bytes")
print(data[:4])        # first 4 bytes — JPEGs start with b'\xff\xd8\xff\xe0'
```

You do **not** pass `encoding` in binary mode (it would be meaningless — bytes are bytes). For most beginner projects you will only touch binary mode when copying files or computing checksums.

---

## 8. Common gotchas

A short list of mistakes every Python beginner makes at least once. Recognize them now and save yourself an hour later.

1. **Opening with `"w"` when you meant `"a"`.** You will truncate a file you wanted to add to. There is no undo.
2. **Forgetting to close.** Always use `with`.
3. **Not passing `encoding="utf-8"`.** Works on your Mac, breaks on the Windows server.
4. **Hard-coding path separators.** `"data/users.csv"` works everywhere if you use `Path("data") / "users.csv"`. `"data\\users.csv"` breaks on macOS.
5. **`.readlines()` vs iteration.** `.readlines()` reads the whole file at once. For a 10 GB log this kills your laptop. Use `for line in f:` instead.
6. **Trailing newline confusion.** Lines from `for line in f:` include `\n`. `print(line)` adds **another** `\n`, so your output is double-spaced. Strip with `.rstrip("\n")` or use `print(line, end="")`.
7. **Writing without flushing.** Buffered writes do not appear on disk until `close()` or `.flush()`. If you are watching a file in another terminal, you will not see updates until the program exits.

---

## 9. A worked example

Pulling all of section 1–8 together: a script that reads a text file, counts unique words, and writes a sorted report.

```python
from pathlib import Path
from collections import Counter

INPUT = Path("essay.txt")
OUTPUT = Path("word-counts.txt")

def word_counts(path: Path) -> Counter:
    """Return a Counter of words in the file at *path*."""
    counts: Counter = Counter()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            for word in line.split():
                counts[word.lower().strip(".,!?;:\"'()")] += 1
    return counts

def write_report(counts: Counter, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for word, count in counts.most_common():
            print(f"{count:>6}  {word}", file=f)

if __name__ == "__main__":
    write_report(word_counts(INPUT), OUTPUT)
    print(f"Wrote report with {len(word_counts(INPUT))} unique words.")
```

Note: `path.open(...)` is the `pathlib` shortcut for `open(path, ...)`. Both work; pick one and be consistent.

---

## What's next

You now know how to move plain text in and out of files. But most real data is **structured** — rows and columns, or nested key/value pairs. The next lecture covers the two formats you will encounter most often as a Python developer: **CSV** and **JSON**.

Continue to [`02-csv-and-json.md`](./02-csv-and-json.md).
