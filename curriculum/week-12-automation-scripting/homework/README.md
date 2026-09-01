# Week 12 — Homework

Six practical problems, one page each — small scripts you will actually reach
for again. They are not tied into one project the way the exercises build toward
the mini-project; each stands alone and drills a different corner of the week:
`shutil` and archives, EXIF, `csv`, image processing, a real HTTP API, and
sockets.

Each shipped answer runs **offline and unattended**. The ones that would
normally touch the network or your files — the photo organizer, the releases
fetcher, the port scanner — build their own sandbox, ship a recorded response
behind a swappable seam, or open their own listener, so `python <name>.py`
finishes on its own and prints the same thing on any machine. Each page shows
the one change that points it back at the real world.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the script reads and
   what it should produce.
2. Copy the Starter into a file of your own — the page names it, and it is
   **not** the `-solution.py` file, which is the finished answer.
3. Fill in the `TODO` markers one at a time, running after each.
4. Compare your output with the Expected output block.
5. Only then read The Solution and why it works.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Dotfile backup](./problem-01-dotfile-backup.md) | `shutil.copy2`, `make_archive`, and a timestamped folder | Beginner | 45 min |
| 2 | [Photo-by-EXIF organizer](./problem-02-photo-exif-organizer.md) | Reading EXIF with Pillow, with an mtime fallback | Intermediate | 1 hr |
| 3 | [CSV to Markdown](./problem-03-csv-to-markdown.md) | `csv`, column padding, and escaping the pipe | Beginner | 45 min |
| 4 | [Batch image resizer](./problem-04-image-resizer.md) | Pillow, aspect ratio, and not touching the originals | Intermediate | 1 hr |
| 5 | [GitHub releases fetcher](./problem-05-github-releases.md) | A real HTTP API, its User-Agent rule, and 404/403 | Intermediate | 1 hr |
| 6 | [Port scanner (localhost only)](./problem-06-port-scanner.md) | Sockets, `connect_ex`, timeouts, and a hard safety rule | Advanced | 1 hr |

Total target time: about 5.5 hours. Problems 2 and 4 need `pip install Pillow`;
problem 5 needs `pip install requests`. The rest are pure standard library.

**Problem 6 carries a safety rule, and it is not decoration.** It scans only
`127.0.0.1` / `localhost` and its CLI refuses any other target. Scanning
machines you do not own is illegal in many places; this is a tool for learning
about sockets in a contained way, nothing else.

## What you hand in

Six scripts of your own, one per problem, named as each page tells you — not the
`-solution.py` names, which belong to the published answers. Each must run as
`python <name>.py`, carry a module docstring with an example invocation, and
put type hints on every signature. Default to **dry-run** for anything that
modifies the filesystem, use `logging` (not `print`) for status, read any secret
from `os.environ` — never a key typed into a committed file — and exit 0 on
success, non-zero on failure. Commit with `feat(week-12): homework problems`.

## Checking your work

Every page ends with an acceptance checklist. Work down it before calling a
problem done. If your output differs from the page's Expected output, that
difference is the bug — read it rather than guessing.
