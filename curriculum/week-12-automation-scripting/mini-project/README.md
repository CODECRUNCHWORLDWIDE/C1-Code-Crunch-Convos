# Mini-Project — File Organizer Bot

> **Topic:** the whole week in one tool — `argparse`, `pathlib`, `shutil`, `logging`, a config file, a watch loop, and tests
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md) and [03 — Scraping and Scheduling](../lecture-notes/03-scraping-and-scheduling.md)
> **Difficulty:** Medium
> **Target time:** 6–10 hours
> **Why this one:** every habit the week drilled — decide/act/talk layering, dry-run by default, never clobber, log everything, stop cleanly — meets in one tool you will actually keep. It is the smallest thing that feels like real automation, and it is the exact shape a `watchdog`-powered version grows into later.

## The Brief

Build a CLI tool, `organize`, that takes a directory and tidies it into
subfolders by file type: `Images/`, `Documents/`, `Code/`, `Archives/`,
`Music/`, `Video/`, `Other/`. It can run once, or watch a directory and react
when new files appear. Every action is logged. The category-to-extension map is
configurable via a JSON file.

Think of it as the bulk renamer from Exercise 2 and the scheduler from Exercise
5 grown together: it decides where each file belongs (a pure function), moves it
only when you pass `--apply` (the act), and narrates every step to the terminal
and a log file (the talk). Anything that does not match a category goes to the
first category with an empty extension list — `Other` in the sample config.

## Starter

Build your own project — `organize.py`, a `config.json`, and a `tests/` folder —
one function at a time. There is no starter file to copy; the CLI and config
below are the whole contract. The CLI you are aiming for:

```bash
python organize.py ~/Downloads --config config.json            # dry run (default)
python organize.py ~/Downloads --config config.json --apply    # actually move
python organize.py ~/Downloads --config config.json --watch --interval 5 --apply
```

The config is a JSON object mapping each category to the suffixes it claims:

```json
{
  "Images":    [".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"],
  "Documents": [".pdf", ".docx", ".md", ".txt", ".rtf"],
  "Code":      [".py", ".js", ".ts", ".rs", ".go", ".java"],
  "Archives":  [".zip", ".tar", ".gz", ".7z", ".rar"],
  "Music":     [".mp3", ".wav", ".flac", ".ogg"],
  "Video":     [".mp4", ".mov", ".mkv", ".avi"],
  "Other":     []
}
```

The finished answer that ships beside this page,
[`organize.py`](./organize.py), carries this map as a built-in default so it
runs with no config file at all, and it drives itself against a temporary folder
so the download proves itself without touching your `~/Downloads`. Yours reads
`config.json` and points at a real directory.

## Requirements

1. **CLI** (`argparse`): a positional `DIRECTORY`, plus `--config PATH`
   (default `config.json`), `--apply`, `--watch`, `--interval SECONDS`
   (default 10), `--log PATH` (default `<DIRECTORY>/organize.log`), and
   `-v/--verbose`.
2. **Categorise by the config.** The category whose extension list contains the
   file's suffix wins; anything unmatched goes to the first category with an
   empty list.
3. **Dry-run by default.** Without `--apply`, log `would move ...` and touch
   nothing. With `--apply`, move the file and log `moved ...`.
4. **Skip** directories, files already inside a category folder, and the log
   file itself.
5. **Never overwrite.** If the destination exists, append a numeric suffix
   (`name-1.ext`, `name-2.ext`, …), and make the dry run predict the same name.
6. **Log to file and console**, e.g.
   `2026-05-13 10:00:00 INFO  moved beach.jpg -> Images/beach.jpg`.
7. **Exit codes**: 0 success, 1 bad input (missing dir, malformed config),
   2 argparse error.
8. **Type hints** on every public function, `pathlib.Path` everywhere, `logging`
   not `print`, and at least **two** `pytest` tests using `tmp_path`.

## Constraints

- **Decide and act are separate functions.** `categorise()` is a pure decision
  and `organize_once()` builds the destination on its own line *before* the
  `if apply:`. That separation is the only reason a dry run is possible: there
  has to be a moment where the tool knows what it is about to do and has not yet
  done it.
- **Collision-safe naming has to reserve names within the run.** In a dry run
  nothing is created, so `dst.exists()` alone would hand two files the same
  `-1` suffix. Track the names this run has claimed in a `reserved` set — the
  same fix as the `planned` set in Challenge 02.
- **`--watch` must be Ctrl-C-able.** The loop catches `KeyboardInterrupt` and
  exits cleanly, exactly like the scheduler in Exercise 5. A watcher you cannot
  stop is a watcher nobody runs.
- **Move with `shutil.move`, not `Path.rename`.** A destination folder could, in
  principle, be on a different volume; `shutil.move` falls back to copy-then-
  delete across filesystems, where `rename` raises.
- **The config is data, not code.** Read it with `json.loads`; a malformed file
  is exit 1 with a message, never a traceback.

## Expected output

The shipped answer proves itself against a messy folder it builds in a temp
directory rather than starting a real watch loop or touching your `~/Downloads`.
It sorts the folder as a preview, then for real, and prints the resulting tree.
The console format here drops the timestamp so the sample is stable; the live
tool keeps the timestamped audit line and writes it to the log file too. Sample
run:

```text
$ python organize.py
File Organizer Bot — driven headless on a folder this file builds.

Preview (the default — nothing is moved):
INFO  would move backup.zip -> Archives/backup.zip
INFO  would move beach.jpg -> Images/beach.jpg
INFO  would move chart.png -> Images/chart.png
INFO  would move invoice.pdf -> Documents/invoice.pdf
INFO  would move notes.md -> Documents/notes-1.md
INFO  would move script.py -> Code/script.py
INFO  would move song.mp3 -> Music/song.mp3
INFO  would move weird_thing.xyz -> Other/weird_thing.xyz

Apply:
INFO  moved backup.zip -> Archives/backup.zip
INFO  moved beach.jpg -> Images/beach.jpg
INFO  moved chart.png -> Images/chart.png
INFO  moved invoice.pdf -> Documents/invoice.pdf
INFO  moved notes.md -> Documents/notes-1.md
INFO  moved script.py -> Code/script.py
INFO  moved song.mp3 -> Music/song.mp3
INFO  moved weird_thing.xyz -> Other/weird_thing.xyz

Resulting tree:
  Archives/
    backup.zip
  Code/
    script.py
  Documents/
    invoice.pdf
    notes-1.md
    notes.md
  Images/
    beach.jpg
    chart.png
  Music/
    song.mp3
  Other/
    weird_thing.xyz
```

Notice `notes.md -> Documents/notes-1.md`: a `notes.md` already lived in
`Documents/`, so the bot renamed rather than overwrote — and the preview and the
apply agree on the `-1`, because the run reserves each name as it claims it.

## Steps

1. Get `categorise()` right first, as a pure function over a suffix and the
   config. Write the two tests for it before anything moves.
2. Add `unique_path()` with the `reserved` set, and test the collision case.
3. Write `organize_once()` as a dry run only — log `would move`, move nothing.
4. Add the `if apply:` move, and confirm a real run matches the preview file for
   file.
5. Wrap it in the `--watch` loop with `try/except KeyboardInterrupt`.
6. Wire up `logging` to both the console and the log file, and confirm the log
   file accumulates across runs.

## The Solution

The download folds the whole tool into one file and drives itself with a
`demo()` so it runs anywhere; your own build is `organize.py` plus a
`config.json` and a `tests/` folder, and that project is what you hand in. The
sorting is identical.

```python
"""organize.py — the File Organizer Bot, the finished answer to Week 12.

Sort a directory into subfolders by file type — Images/, Documents/, Code/,
Archives/, Music/, Video/, Other/ — from a JSON config. Preview by default;
move only with --apply. Watch a directory and keep sorting with --watch. Every
action is logged to the terminal and to a log file.

Your own deliverable is a small project — organize.py, a config.json, and a
tests/ folder — and that project is what you hand in. This download exists so
the reference answer runs anywhere, so its ``__main__`` block does not start a
real watch loop or touch your Downloads: it builds a messy folder in a temp
directory, sorts it (a dry run, then for real), prints the tree, and shows the
collision-safe rename. The sorting being demonstrated is exactly what runs live.

    python organize.py ~/Downloads --config config.json --apply
    python organize.py ~/Downloads --config config.json          # dry run
    python organize.py ~/Downloads --config config.json --watch --interval 5 --apply

Exit codes: 0 success, 1 bad input (missing dir or malformed config), 2 argparse.

Run the built-in demo with::

    python organize.py
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import time
from pathlib import Path

LOG_NAME = "organize.log"
LOG_FORMAT = "%(asctime)s %(levelname)-5s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGER = logging.getLogger("organize")

DEFAULT_CONFIG: dict[str, list[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"],
    "Documents": [".pdf", ".docx", ".md", ".txt", ".rtf"],
    "Code": [".py", ".js", ".ts", ".rs", ".go", ".java"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Music": [".mp3", ".wav", ".flac", ".ogg"],
    "Video": [".mp4", ".mov", ".mkv", ".avi"],
    "Other": [],
}


class ConfigError(RuntimeError):
    """The config file is missing or the wrong shape."""


def load_config(path: Path) -> dict[str, list[str]]:
    """Read the category-to-extensions map, or raise ConfigError."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"no such config file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or not all(
        isinstance(v, list) for v in data.values()
    ):
        raise ConfigError(f"{path} must map category -> list of extensions")
    return data


def categorise(path: Path, config: dict[str, list[str]]) -> str:
    """The category for *path*: the list holding its suffix, else the empty one.

    A pure decision — no I/O — so it is the piece you can unit-test in a
    millisecond, and the reason a dry run can predict the real run exactly.
    """
    suffix = path.suffix.lower()
    fallback = None
    for name, extensions in config.items():
        if not extensions and fallback is None:
            fallback = name
        if suffix in extensions:
            return name
    if fallback is None:
        raise ConfigError("config has no fallback category (one with an empty list)")
    return fallback


def unique_path(destination: Path, reserved: set[Path]) -> Path:
    """A destination that is free on disk and not already promised this run.

    ``reserved`` is why a dry run agrees with the real run: in a preview nothing
    is created, so ``exists()`` alone would hand two files the same new name.
    Tracking the names this run has already claimed closes that gap — the same
    idea as the ``planned`` set in Challenge 02's PDF renamer.
    """
    candidate = destination
    index = 1
    while candidate.exists() or candidate in reserved:
        candidate = destination.with_name(
            f"{destination.stem}-{index}{destination.suffix}"
        )
        index += 1
    reserved.add(candidate)
    return candidate


def organize_once(directory: Path, config: dict[str, list[str]], apply: bool) -> int:
    """Sort (or preview sorting) every loose file. Return how many were acted on."""
    categories = set(config)
    reserved: set[Path] = set()
    acted = 0
    for path in sorted(directory.iterdir()):
        if not path.is_file() or path.name == LOG_NAME:
            continue
        category = categorise(path, config)
        destination = unique_path(directory / category / path.name, reserved)
        LOGGER.info("%s %s -> %s/%s",
                    "moved" if apply else "would move",
                    path.name, category, destination.name)
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(destination))
        acted += 1
    return acted


def watch(directory: Path, config: dict[str, list[str]], apply: bool,
          interval: float, rounds: int | None = None) -> int:
    """Sort on a loop until Ctrl-C. `rounds` bounds it, for testing.

    Ctrl-C is the supported way to stop a watcher, so it is caught and turned
    into a clean exit rather than a traceback.
    """
    completed = 0
    try:
        while rounds is None or completed < rounds:
            organize_once(directory, config, apply)
            completed += 1
            if rounds is not None and completed >= rounds:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        LOGGER.info("stopped by user after %d round(s)", completed)
    return 0


def configure_logging(log_path: Path, verbose: bool) -> None:
    """Log to the terminal and to *log_path*, with the timestamped audit format."""
    for handler in list(LOGGER.handlers):
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.setLevel(logging.DEBUG if verbose else logging.INFO)
    LOGGER.propagate = False
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    console = logging.StreamHandler(stream=sys.stdout)
    console.setFormatter(formatter)
    LOGGER.addHandler(console)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_file = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    log_file.setFormatter(formatter)
    LOGGER.addHandler(log_file)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="organize",
        description="Sort a directory into subfolders by file type.",
    )
    parser.add_argument("directory", type=Path, help="The folder to organize.")
    parser.add_argument("--config", type=Path, default=Path("config.json"),
                        help="Category -> extensions JSON (default: %(default)s)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually move files. Without it, dry-run.")
    parser.add_argument("--watch", action="store_true",
                        help="Keep running and re-check on an interval.")
    parser.add_argument("--interval", type=float, default=10.0,
                        help="Seconds between checks with --watch (default: %(default)s)")
    parser.add_argument("--log", type=Path, default=None,
                        help="Log file (default: <DIRECTORY>/organize.log)")
    parser.add_argument("-v", "--verbose", action="store_true", help="More logging.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run once or watch. Return an exit code."""
    args = build_parser().parse_args(argv)

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    try:
        config = load_config(args.config) if args.config.exists() else DEFAULT_CONFIG
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    log_path = args.log or (args.directory / LOG_NAME)
    configure_logging(log_path, args.verbose)

    if args.watch:
        return watch(args.directory, config, args.apply, args.interval)

    acted = organize_once(args.directory, config, args.apply)
    LOGGER.info("%s %d file(s)", "moved" if args.apply else "would move", acted)
    return 0


# --------------------------------------------------------------------------- #
# The demo run — a messy folder built in a temp directory, sorted twice. The
# console format here drops the timestamp so the sample is reproducible; the
# live tool keeps the timestamped audit line above, and writes it to the log
# file as well.
# --------------------------------------------------------------------------- #


def _demo_logging() -> None:
    for handler in list(LOGGER.handlers):
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)-5s %(message)s"))
    LOGGER.addHandler(handler)


def _tree(directory: Path, prefix: str = "") -> None:
    for path in sorted(directory.iterdir()):
        print(f"{prefix}{path.name}" + ("/" if path.is_dir() else ""))
        if path.is_dir():
            _tree(path, prefix + "  ")


def demo() -> None:
    """Sort a messy temp folder, first as a preview and then for real."""
    import tempfile

    print("File Organizer Bot — driven headless on a folder this file builds.")
    print()
    _demo_logging()
    with tempfile.TemporaryDirectory() as tmp:
        downloads = Path(tmp)
        for name in ("beach.jpg", "chart.png", "invoice.pdf", "notes.md",
                     "script.py", "backup.zip", "song.mp3", "weird_thing.xyz"):
            (downloads / name).write_bytes(b"x")
        # a name that already exists in its category, to force a -1 rename
        (downloads / "Documents").mkdir()
        (downloads / "Documents" / "notes.md").write_bytes(b"older")

        print("Preview (the default — nothing is moved):")
        organize_once(downloads, DEFAULT_CONFIG, apply=False)
        print()
        print("Apply:")
        organize_once(downloads, DEFAULT_CONFIG, apply=True)
        print()
        print("Resulting tree:")
        _tree(downloads, "  ")


if __name__ == "__main__":
    demo()
```

**The whole tool is decide, act, talk.** `categorise()` decides — a pure
function of a suffix and the config, no I/O, testable in a millisecond.
`organize_once()` acts, and only the `shutil.move` line is guarded by
`if apply:`; everything else — scanning, categorising, building the destination,
logging — runs identically in both modes, which is what makes the preview a
truthful prediction. `configure_logging()` and the returned exit code are the
talk. Every Week 12 bug is one of those three layers doing another's job.

**`unique_path()` reserves as it goes.** The collision-safe rename is the
`while candidate.exists() or candidate in reserved:` loop. The `reserved` set is
the non-obvious half: in a dry run nothing is created, so two files that both
want `report.pdf` would both compute `report-1.pdf` from `exists()` alone.
Adding the chosen name to `reserved` the moment it is claimed keeps the preview
honest — the same problem, and the same fix, as Challenge 02's `planned` set.

**`categorise()` finds the fallback in the same pass.** It walks the config once,
remembers the first category with an empty extension list as the fallback, and
returns a real match the moment it finds one. So the "Other" behaviour is not a
special case bolted on — it is the category whose extension list happens to be
empty, chosen by the same loop.

**The watch loop is the scheduler pattern again.** `organize_once` is called on a
`while` loop, `time.sleep(interval)` between rounds, and a `try/except
KeyboardInterrupt` around the whole thing so Ctrl-C logs a clean line and
returns 0 instead of dumping a traceback. `rounds` bounds the loop so a test can
drive it without waiting forever.

**Logging goes to two handlers.** One `StreamHandler` for the terminal and one
`FileHandler` for the audit trail, both with the timestamped format, so the same
line the user watches scroll past is the line written to `organize.log` for
later. The log file is skipped by name in `organize_once`, so the bot never
tries to file its own log under `Documents/`.

## Download and run

<!-- no-runnable-file: the deliverable is a project in your own repository — organize.py plus a config.json, a tests/ folder, and a commit history — not a single script. The finished answer ships as organize.py, which folds the config default and a self-test into one file so it runs on its own, and is linked below. -->

Download [organize.py](./organize.py) and run it:

```bash
python organize.py
```

It builds a messy folder in a temp directory, sorts it, and prints the run
above — it never touches a directory of yours. To sort a real folder, pass one:
`python organize.py ~/Downloads --config config.json` previews, and `--apply`
moves. The file's docstring lists every flag.

## Common bugs to catch

- **The preview and the real run disagree on a `-1` suffix.** You used
  `dst.exists()` without a `reserved` set. In a dry run nothing is created, so
  two files claiming the same name both compute the same suffix. Reserve each
  name as it is chosen.
- **The bot files its own log under `Documents/`.** You did not skip the log
  file by name. `organize.log` matches the `.md`-less "Other" bucket (or
  `Documents` if you list `.log`), so exclude it explicitly.
- **`--watch` cannot be stopped without a traceback.** You did not catch
  `KeyboardInterrupt` around the loop. Wrap it, log a clean line, return 0.
- **`OSError: Invalid cross-device link`.** You used `Path.rename` and the
  destination was on another volume. `shutil.move` handles that; `rename` does
  not.
- **A malformed `config.json` dumps a `JSONDecodeError` traceback.** Catch it,
  print a message, and exit 1 — a bad config is bad input, not a crash.
- **Files already in category folders get moved again on the next run.** You
  iterated recursively, or did not skip subdirectories. Only loose files at the
  top level are candidates.

## Under the hood

<details>
<summary>Under the hood — why this polling watch loop wants to be an event-driven one</summary>

`--watch` here re-scans the whole directory every `interval` seconds. That is
simple, portable, and exactly what Exercise 5 taught — and it is also wasteful:
most of the time nothing has changed, and you are listing a directory over and
over to find that out. It also has latency baked in, up to a full interval
between a file arriving and the bot noticing.

The grown-up version replaces the poll with operating-system file-change events.
The [`watchdog`](https://pypi.org/project/watchdog/) library subscribes to the
kernel's notification API — `inotify` on Linux, `FSEvents` on macOS,
`ReadDirectoryChangesW` on Windows — and calls your handler the instant a file
is created, with no scanning and no interval. The tool reacts immediately and
uses no CPU while idle. The reason to *start* with polling is that it works
everywhere with no dependency and is trivial to reason about and test; the
reason to *graduate* to events is that a real "watch my Downloads forever"
daemon should not burn a scan a second for a folder that changes twice a day.
Same `organize_once` underneath — only the thing that decides *when* to call it
changes, which is exactly the decide/act/talk split paying off again.

</details>

## Acceptance checklist

- [ ] `organize.py` runs from a clean venv, once and with `--watch`.
- [ ] A dry run moves nothing; `--apply` moves and logs `moved ...`.
- [ ] A file whose target exists becomes `name-1.ext`, and the preview predicts
      it.
- [ ] Unmatched files land in the empty-list category (`Other`).
- [ ] Ctrl-C out of `--watch` exits cleanly with no traceback.
- [ ] Logs go to both the console and the log file.
- [ ] At least two `pytest` tests pass, covering `categorise` and the collision
      rename.
- [ ] Committed to Git with a message like
      `feat(week-12): file organizer mini-project`.

## Stretch

- **Watchdog upgrade** — replace the polling loop with the
  [`watchdog`](https://pypi.org/project/watchdog/) library for true OS-level
  file-change events.
- **Notifications** — add a webhook so the bot DMs you on Slack or Discord when
  it files something.
- **Packaging** — wrap it as an installable CLI with `pyproject.toml` and
  `entry_points`, so `organize` runs from anywhere.
- **Undo journal** — write a JSON record of every move so a single command can
  put the folder back, replaying in reverse.

That is Week 12. Next week leaves automation behind (mostly) and turns to data:
[Week 13 — Data Analysis](../../week-13-data-analysis/).
