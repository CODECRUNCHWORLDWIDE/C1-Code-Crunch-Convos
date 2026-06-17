# Lecture 2 — File System and `subprocess`

In Week 6 we learned the basics of `open()`, `read`, and `write`. This lecture builds on that with three tools that turn Python into a real shell-replacement language:

1. **`pathlib`** — object-oriented filesystem paths (recap + power moves).
2. **`shutil`** — copy, move, archive, and remove entire trees.
3. **`subprocess`** — run external programs from Python and capture their output.

We'll close with a pattern for **watching for file changes** without any third-party libraries.

---

## 1. `pathlib` — your filesystem swiss-army knife

We met `pathlib.Path` in Week 6. Quick refresher:

```python
from pathlib import Path

p = Path("notes") / "2026" / "may.md"   # cross-platform separator
p.parent          # Path('notes/2026')
p.name            # 'may.md'
p.stem            # 'may'
p.suffix          # '.md'
p.with_suffix(".txt")   # Path('notes/2026/may.txt')
```

What you may *not* know yet are these power tools.

### 1.1 `rglob` — recursive glob

`glob` matches a pattern at one level. `rglob` walks the whole tree.

```python
from pathlib import Path

# All Python files under the project (recursive)
for py in Path(".").rglob("*.py"):
    print(py)

# All hidden files at any depth
for h in Path.home().rglob(".*"):
    print(h)
```

Patterns support standard glob syntax: `*` (anything), `?` (one char), `[abc]` (one of), `**` (any depth — implicit in `rglob`).

### 1.2 `parents` — walk upward

```python
p = Path("/Users/jane/code/cc/curriculum/week-12-automation-scripting/lecture-notes/02.md")
list(p.parents)
# [...lecture-notes, ...week-12-automation-scripting, ...curriculum, ...cc, ...code, ...jane, /Users, /]

p.parents[0]      # the immediate folder
p.parents[2]      # two levels up
```

This is the cleanest way to find a project root (look upward until you see a `.git` folder, for example).

### 1.3 `stat` — file metadata

```python
import datetime as dt
from pathlib import Path

s = Path("README.md").stat()
print(s.st_size)               # bytes
print(s.st_mtime)              # last-modified UNIX timestamp
print(dt.datetime.fromtimestamp(s.st_mtime))
print(oct(s.st_mode))          # permissions, e.g. '0o100644'
```

Use this for "files older than 30 days", "files bigger than 1 MB", etc.

### 1.4 `touch`, `mkdir`, `unlink`

```python
from pathlib import Path

Path("logs/today.log").parent.mkdir(parents=True, exist_ok=True)
Path("logs/today.log").touch(exist_ok=True)        # create empty file if missing
Path("logs/yesterday.log").unlink(missing_ok=True) # delete file, no error if absent
```

`parents=True, exist_ok=True` are the magic kwargs you'll use 90% of the time.

### 1.5 Reading and writing in one line

```python
Path("data.txt").write_text("hello\n", encoding="utf-8")
content = Path("data.txt").read_text(encoding="utf-8")

Path("photo.jpg").write_bytes(b"\xff\xd8...")
blob = Path("photo.jpg").read_bytes()
```

For large files keep using `open()` with iteration — these helpers load the whole thing into memory.

---

## 2. `shutil` — high-level file operations

`shutil` (shell-utilities) is the level above `pathlib`. It moves files, copies trees, makes archives.

### 2.1 Copying

```python
import shutil
from pathlib import Path

shutil.copy("a.txt", "b.txt")           # data + permissions
shutil.copy2("a.txt", "b.txt")          # also copies mtime/atime
shutil.copytree("project", "backup")    # whole directory tree
```

`copy2` is what you want for backups — it preserves timestamps.

For partial copies use the `ignore` callback:

```python
def ignore_pyc(_dir, names):
    return [n for n in names if n.endswith(".pyc") or n == "__pycache__"]

shutil.copytree("src", "dist", ignore=ignore_pyc)
```

### 2.2 Moving and renaming

```python
shutil.move("draft.md", "archive/draft.md")
```

`shutil.move` works across filesystems (a `rename` doesn't always — that's an OS limitation). It also accepts `Path` objects.

### 2.3 Deleting

```python
import shutil

shutil.rmtree("scratch/")    # recursive delete — be careful!
```

`rmtree` will not ask twice. Treat it like `rm -rf`. Always check the path is what you think it is before calling it, and prefer dry-run mode by default.

### 2.4 Archiving

```python
import shutil

shutil.make_archive("backup-2026-05-13", "zip", "project/")
# -> creates backup-2026-05-13.zip from contents of project/
```

Supported formats out of the box: `zip`, `tar`, `gztar`, `bztar`, `xztar`. Returns the path of the archive it just made.

To unpack:

```python
shutil.unpack_archive("backup-2026-05-13.zip", "restore/")
```

### 2.5 Disk usage

```python
total, used, free = shutil.disk_usage("/")
print(f"{free / 1e9:.1f} GB free")
```

Useful in scripts that need to abort if the disk is nearly full.

---

## 3. `subprocess` — run shell commands from Python

Sometimes the right tool already exists as a CLI. `ffmpeg`, `git`, `pandoc`, `pdftotext`, `rsync` — wrapping them in Python is often easier than re-implementing them.

### 3.1 The one function you need: `subprocess.run`

```python
import subprocess

result = subprocess.run(
    ["git", "log", "-5", "--oneline"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.stdout)
```

Four arguments to remember:

| Argument         | Why                                                           |
|------------------|---------------------------------------------------------------|
| First positional | A **list** of program + args — *not* a string. (See §3.4!)    |
| `capture_output` | Saves stdout/stderr into `result.stdout` and `result.stderr`. |
| `text=True`      | Decodes bytes to `str` using locale encoding (usually UTF-8). |
| `check=True`     | Raises `CalledProcessError` if the command fails.             |

The returned `CompletedProcess` object has `.returncode`, `.stdout`, `.stderr`.

### 3.2 Parsing the output

```python
lines = result.stdout.strip().splitlines()
for line in lines:
    sha, _, message = line.partition(" ")
    print(sha, "→", message)
```

If the output is JSON (many modern CLIs support `--json` or `--format=json`):

```python
import json, subprocess

out = subprocess.run(
    ["gh", "pr", "list", "--json", "number,title"],
    capture_output=True, text=True, check=True,
).stdout
prs = json.loads(out)
```

### 3.3 Passing input on stdin

```python
result = subprocess.run(
    ["grep", "ERROR"],
    input="line1\nERROR oh no\nline3\n",
    capture_output=True, text=True,
)
print(result.stdout)   # "ERROR oh no\n"
```

### 3.4 The `shell=True` warning

Resist the urge to pass a single string with `shell=True`:

```python
# BAD — vulnerable to shell injection
subprocess.run(f"ls {user_input}", shell=True)
```

If `user_input` is `; rm -rf ~`, the shell will happily oblige.

**Rule**: pass a list, leave `shell=False` (the default). The only time `shell=True` makes sense is for genuinely shell-y constructs you control (pipes, redirects, globs):

```python
# OK — no untrusted input in the command string
subprocess.run("ls *.py | wc -l", shell=True, check=True)
```

…and even then, doing the pipe in Python is usually cleaner:

```python
files = list(Path(".").glob("*.py"))
print(len(files))
```

### 3.5 Environment variables

You can override or extend the child process's environment:

```python
import os, subprocess

env = os.environ.copy()
env["LANG"] = "C"          # disable localization for predictable output
env["PATH"] = "/usr/bin"   # be explicit
subprocess.run(["date"], env=env, check=True)
```

Pass `cwd=` to change the working directory of the child process:

```python
subprocess.run(["git", "status"], cwd="/path/to/repo", check=True)
```

### 3.6 Streaming output (`Popen`)

For long-running commands you don't want to buffer the entire output. Use `Popen`:

```python
import subprocess

with subprocess.Popen(
    ["ping", "-c", "5", "example.com"],
    stdout=subprocess.PIPE, text=True,
) as proc:
    assert proc.stdout is not None
    for line in proc.stdout:
        print("ping:", line.rstrip())
```

`run` is `Popen` under the hood — but for 95% of automation work `run` is what you want.

### 3.7 Timeouts

```python
try:
    subprocess.run(["slow-script"], timeout=10, check=True)
except subprocess.TimeoutExpired:
    print("took too long, gave up")
```

Always pass a `timeout` when the command talks to the network or hits a service you don't control.

---

## 4. Watching for file changes (poll-based)

You don't always need `watchdog` (which uses OS-level events). For small scripts a **polling loop** is fine.

```python
"""watch.py — print a message whenever files in DIR change."""
from __future__ import annotations

import time
from pathlib import Path


def snapshot(root: Path) -> dict[Path, float]:
    """Map each file under root to its modification time."""
    return {p: p.stat().st_mtime for p in root.rglob("*") if p.is_file()}


def diff(old: dict[Path, float], new: dict[Path, float]) -> tuple[list[Path], list[Path], list[Path]]:
    """Return (added, removed, changed)."""
    added = [p for p in new if p not in old]
    removed = [p for p in old if p not in new]
    changed = [p for p in new if p in old and new[p] != old[p]]
    return added, removed, changed


def watch(root: Path, interval: float = 2.0) -> None:
    print(f"watching {root} (Ctrl-C to stop)")
    state = snapshot(root)
    while True:
        time.sleep(interval)
        new = snapshot(root)
        added, removed, changed = diff(state, new)
        for p in added:
            print("ADDED   ", p)
        for p in removed:
            print("REMOVED ", p)
        for p in changed:
            print("CHANGED ", p)
        state = new


if __name__ == "__main__":
    watch(Path("."), interval=2.0)
```

What's nice about polling:

- Zero dependencies.
- Works the same on Linux, macOS, Windows.
- Easy to reason about and test.

What's not nice:

- It misses changes that happen within one cycle (`save`, then `save` again 100 ms later — you see only the second).
- It uses some CPU and disk I/O even when nothing changes.

For more demanding work, install [`watchdog`](https://python-watchdog.readthedocs.io/) which subscribes to OS events.

---

## 5. Worked example: nightly project backup

Let's combine `pathlib`, `shutil`, and `subprocess` in a useful little tool.

```python
"""nightly_backup.py — snapshot a project to a zip, optionally push to git remote."""
from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Snapshot a project directory.")
    p.add_argument("source", type=Path, help="Project folder to back up")
    p.add_argument("dest", type=Path, help="Folder where the .zip will land")
    p.add_argument("--git-push", action="store_true",
                   help="Also run `git push` in the source first")
    return p


def git_push(src: Path) -> None:
    logging.info("running git push in %s", src)
    subprocess.run(["git", "push"], cwd=src, check=True, timeout=60)


def make_archive(src: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    base = dest_dir / f"{src.name}-{stamp}"
    archive = shutil.make_archive(str(base), "zip", root_dir=src)
    return Path(archive)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    args = build_parser().parse_args()

    if not args.source.is_dir():
        logging.error("source %s is not a directory", args.source)
        return 1

    if args.git_push:
        try:
            git_push(args.source)
        except subprocess.CalledProcessError as exc:
            logging.error("git push failed (exit %s)", exc.returncode)
            return exc.returncode

    archive = make_archive(args.source, args.dest)
    size_mb = archive.stat().st_size / 1e6
    logging.info("wrote %s (%.1f MB)", archive, size_mb)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

You could schedule this with cron (`0 2 * * *` for 2 a.m. daily) — we'll cover cron in lecture 3.

---

## 6. Things to remember

1. **Prefer `pathlib.Path` over raw strings.** It does the right thing on every OS.
2. **`shutil` for bulk file operations.** Copy trees, make zips, check disk space.
3. **`subprocess.run(list, capture_output=True, text=True, check=True)`** is the incantation.
4. **Never use `shell=True` with user input.** Pass a list.
5. **Set `timeout=` on commands that touch the network.**
6. **Polling for file changes is fine** for hobby-scale scripts. Reach for `watchdog` when you need OS-level events.
7. **Always default to dry-run** when your script touches the filesystem destructively.

---

## Further reading

- [`pathlib` reference](https://docs.python.org/3/library/pathlib.html)
- [`shutil` reference](https://docs.python.org/3/library/shutil.html)
- [`subprocess` reference](https://docs.python.org/3/library/subprocess.html)
- Real Python: ["An Introduction to subprocess in Python With Examples"](https://realpython.com/python-subprocess/)
- *Automate the Boring Stuff*, Chapter 10 ("Organizing Files").
