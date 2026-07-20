# Week 12 — Homework

Six practical problems. Pick **at least four** and submit. If you have time, do all six — they are mostly small and very useful in real life.

Every solution must:

- Have a top-of-file docstring explaining what it does and how to run it.
- Use `argparse` (or, where impractical, accept inputs via env vars).
- Default to **dry-run** for anything that modifies the filesystem.
- Use `logging`, not `print`, for status output.
- Exit 0 on success, non-zero on failure.

---

## Problem 1 — Dotfile backup script

Write a script that copies a list of "dotfiles" (e.g. `~/.bashrc`, `~/.zshrc`, `~/.gitconfig`, `~/.vimrc`) into a timestamped folder, then zips it up.

**Requirements**

- Read the list of files from `dotfiles.txt` (one path per line, `~` allowed).
- Skip files that don't exist (warn but don't fail).
- Output: `~/dotfile-backups/2026-05-13-1430/` with the originals inside, plus `2026-05-13-1430.zip` next to it.

**Useful tools**: `pathlib.Path.expanduser`, `shutil.copy2`, `shutil.make_archive`, `datetime.datetime.now().strftime`.

---

## Problem 2 — Photo-by-EXIF-date organizer

Walk a folder of photos and move each one into `YYYY/MM/` subfolders based on the EXIF "DateTimeOriginal" tag.

**Requirements**

- Use `Pillow` (`pip install Pillow`) to read EXIF data:

  ```python
  from PIL import Image
  img = Image.open(path)
  exif = img._getexif() or {}
  ```

  EXIF tag `36867` is `DateTimeOriginal` (format `"YYYY:MM:DD HH:MM:SS"`).

- If the EXIF date is missing, fall back to `Path.stat().st_mtime`.
- Defaults to dry-run; `--apply` actually moves.
- Skip non-image files.

**Bonus**: write a small `pytest` test using a fake `Image` class (mock).

---

## Problem 3 — CSV → Markdown converter

Read a CSV file and emit a GitHub-flavored Markdown table on stdout.

**Requirements**

- Use `csv.DictReader`.
- First row of the CSV is the header.
- Right-pad columns to the longest entry per column.
- Escape `|` characters inside cells.
- Optional `--align l|c|r` flag that controls column alignment.

Example:

```text
$ python csv2md.py data.csv --align c
| Name    | Score |
| :-----: | :---: |
| Alice   | 95    |
| Bob     | 87    |
```

---

## Problem 4 — Batch image resizer

Resize every image in a folder to a target max-width while preserving aspect ratio.

**Requirements**

- `pip install Pillow`.
- CLI: `python resize.py DIR --width 1024 [--output DIR] [--apply]`.
- Output goes to `--output` (default: `DIR/resized/`), so originals are untouched.
- Supports `.jpg`, `.png`, `.webp`.
- Skips images already smaller than the target width.

**Helpful Pillow API**:

```python
from PIL import Image
img = Image.open(src)
if img.width > target:
    ratio = target / img.width
    img = img.resize((target, int(img.height * ratio)))
img.save(dst, optimize=True, quality=85)
```

---

## Problem 5 — GitHub releases fetcher

Hit the public GitHub Releases API and print the 5 most recent releases for a repo.

**Requirements**

- CLI: `python gh_releases.py owner/repo [--count N]`.
- Use the API at `https://api.github.com/repos/{owner}/{repo}/releases` — no auth needed for public repos.
- Print each release as `TAG  DATE  TITLE`.
- Handle 404 (repo not found) and 403 (rate-limited) gracefully.
- Set a `User-Agent` header (the API requires it).

**Stretch**: read a `GITHUB_TOKEN` env var; if present, send it as `Authorization: Bearer <token>` for higher rate limits.

---

## Problem 6 — Educational port scanner (localhost only)

Write a script that scans TCP ports 1–1024 on `127.0.0.1` and reports which are open.

> **Hard rule**: only scan `127.0.0.1` or `localhost`. Scanning other hosts without permission is illegal in many jurisdictions. The CLI must refuse any other target.

**Requirements**

- Use `socket.socket(AF_INET, SOCK_STREAM)` and `connect_ex((host, port))`.
- A return value of `0` from `connect_ex` means the port accepted the connection.
- Use `socket.setdefaulttimeout(0.2)` (or set per-socket) so the scan is fast.
- CLI: `python scan_local.py [--start 1] [--end 1024]`. Refuse any `--host` other than `127.0.0.1`/`localhost`.
- Bonus: use `concurrent.futures.ThreadPoolExecutor` for parallelism.

**Why this is useful**: it teaches you about sockets, timeouts, and exit conditions in a contained way. It is *not* for use against other people's machines.

---

## Submission checklist

- [ ] Each script lives in its own file with a docstring.
- [ ] All scripts run from a clean venv with the dependencies you listed.
- [ ] No secrets committed; if any script needs one, it reads from env vars.
- [ ] At least one script has a unit test.
- [ ] You wrote *one* paragraph reflecting on which homework problem you'd actually use in your daily workflow, and why.
