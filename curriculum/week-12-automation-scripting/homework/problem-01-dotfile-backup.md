# Homework 1 — Dotfile backup script

> **Topic:** `pathlib`, `shutil.copy2`, `shutil.make_archive`, and a timestamped folder
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Beginner
> **Target time:** 45 min
> **Why this one:** it is the friendliest possible use of `shutil` — copy a handful of files into a dated folder and zip it — and it is genuinely useful the first time you set up a new laptop. It also teaches the habit of *warning and continuing* rather than crashing when one input is missing.

## The Brief

Write a script that backs up your dotfiles — `~/.bashrc`, `~/.gitconfig`,
`~/.vimrc`, and friends — into a timestamped folder, then zips that folder. Run
it before you reinstall your machine and you have a single archive with your
whole shell setup in it.

The list of files to back up lives in a text file, one path per line, `~`
allowed. A file on the list that does not exist is a warning, not a failure —
different machines have different dotfiles, and a missing `.zshrc` should not
stop the `.bashrc` from being saved. The output is a folder like
`dotfile-backups/2026-05-13-1430/` with the originals inside, plus
`2026-05-13-1430.zip` next to it.

## Starter

```python
"""problem-01-dotfile-backup.py — copy the listed dotfiles into a timestamped zip.

    python problem-01-dotfile-backup.py --list dotfiles.txt --dest ~/dotfile-backups
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

LOGGER = logging.getLogger("dotfile_backup")


def read_targets(list_path: Path) -> list[Path]:
    """One path per line, `~` expanded; blank lines and `#` comments skipped."""
    # TODO: read the file, strip each line, expanduser(), skip blanks and comments
    raise NotImplementedError


def run_backup(targets: list[Path], dest_root: Path, stamp: str) -> tuple[int, int]:
    """Copy every existing target into dest_root/<stamp>/, then zip it."""
    # TODO: mkdir the stamped folder; copy2 existing files, warn on missing;
    # TODO: shutil.make_archive(dest_root/stamp, "zip", root_dir=folder)
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Read the list, back up what exists, zip it. Return an exit code."""
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. Read the list of files from a text file (default `dotfiles.txt`), one path
   per line, with `~` expanded.
2. Skip files that do not exist — warn, but do not fail.
3. Copy every existing file into `<dest>/<stamp>/`, where `<stamp>` is
   `YYYY-MM-DD-HHMM`, then create `<dest>/<stamp>.zip` from that folder.
4. Use `logging`, not `print`, for status output.
5. Exit 0 on success, 1 if the list file itself is missing.

## Constraints

- **`shutil.copy2`, not `copy`.** `copy2` preserves the modification time and
  permissions, which is what you want for a backup — a restored `.bashrc` should
  look exactly as it did.
- **`shutil.make_archive` builds the zip; do not assemble it by hand.** One call
  with `root_dir=` pointed at the stamped folder zips its contents. Rolling your
  own with `zipfile` is more code and gets the internal paths wrong.
- **A missing file is `LOGGER.warning`, not a raise.** The whole point is to
  survive a list that does not perfectly match this machine.
- **Read the file list with `Path.read_text().splitlines()`, and skip blank
  lines and `#` comments.** A comment in the list ("# work laptop only") should
  not become a path you try to copy.

## Expected output

The shipped answer, [`problem-01-dotfile-backup-solution.py`](./problem-01-dotfile-backup-solution.py),
threads the clock through `main()` as a seam (defaulting to the real
`datetime.now`, so your own version needs no argument), builds a throwaway home
in a temp directory, injects a fixed time, backs it up, and confirms the archive
landed. Real captured output:

```text
$ python problem-01-dotfile-backup-solution.py
Dotfile Backup — driven headless in a temp home this file builds.

INFO    copied .bashrc
INFO    copied .gitconfig
INFO    copied .vimrc
WARNING skip .zshrc (does not exist)
INFO    wrote 2026-05-13-1430.zip (3 file(s), 1 skipped)
[exit 0]
backup folder 2026-05-13-1430/ created: True
archive 2026-05-13-1430.zip created:   True
```

`.zshrc` is on the list but was never created, so it is a warning and the run
carries on. The stamped folder and its zip both land under the destination.

## Steps

1. Write `read_targets` and print the list it returns, so you can see the `~`
   expansion working before anything is copied.
2. Create a `dotfiles.txt` pointing at two or three real files plus one that
   does not exist.
3. Write `run_backup` and run it. Confirm the stamped folder holds the files
   that existed and the missing one only logged a warning.
4. Confirm the `.zip` appears next to the folder and opens.
5. Run it twice a minute apart and confirm you get two differently-stamped
   backups, neither clobbering the other.

## The Solution

The shipped file is your answer — `read_targets`, `run_backup`, `main` — with a
`clock` seam so the demo can pin the timestamp, plus a `demo()` that builds a
temp home. Your own `main(argv)` needs no `clock`; it uses the real clock.

```python
"""problem-01-dotfile-backup-solution.py — the dotfile backup, proven headless.

The homework answer reads a list of dotfiles, copies the ones that exist into a
timestamped folder, and zips it. Your own problem-01-dotfile-backup.py ends in
``raise SystemExit(main())`` and points at your real ``~`` and a real
``dotfiles.txt``.

A published answer cannot touch your home directory or stamp a folder with the
real clock and still match a recording, so this file threads the clock through
``main`` as a seam (it defaults to the real ``datetime.now``, so your own
version needs no argument) and the demo builds a throwaway home in a temp
directory, injects a fixed time, backs it up, and checks the archive landed. The
backup being tested is identical either way.

Run it with::

    python problem-01-dotfile-backup-solution.py
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
import tempfile
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

LOGGER = logging.getLogger("dotfile_backup")


def configure_logging() -> None:
    """Log INFO and up to stdout, with no timestamp of its own."""
    for handler in list(LOGGER.handlers):
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)-7s %(message)s"))
    LOGGER.addHandler(handler)


def read_targets(list_path: Path) -> list[Path]:
    """One path per line, `~` expanded; blank lines and `#` comments skipped."""
    targets: list[Path] = []
    for line in list_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            targets.append(Path(line).expanduser())
    return targets


def run_backup(targets: list[Path], dest_root: Path, stamp: str) -> tuple[int, int]:
    """Copy every existing target into dest_root/<stamp>/, then zip it.

    Returns (copied, skipped). A target that does not exist is a warning, not a
    failure — a machine that never had a ``.zshrc`` should still back up the
    rest.
    """
    folder = dest_root / stamp
    folder.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0
    for source in targets:
        if not source.exists():
            LOGGER.warning("skip %s (does not exist)", source.name)
            skipped += 1
            continue
        shutil.copy2(source, folder / source.name)
        LOGGER.info("copied %s", source.name)
        copied += 1

    archive = shutil.make_archive(str(dest_root / stamp), "zip", root_dir=folder)
    LOGGER.info("wrote %s (%d file(s), %d skipped)", Path(archive).name, copied, skipped)
    return copied, skipped


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dotfile-backup",
        description="Copy the dotfiles listed in a file into a timestamped zip.",
    )
    parser.add_argument("--list", type=Path, default=Path("dotfiles.txt"),
                        help="File of paths to back up, one per line (default: %(default)s)")
    parser.add_argument("--dest", type=Path, default=Path.home() / "dotfile-backups",
                        help="Where the timestamped folder and zip go (default: %(default)s)")
    return parser


def main(argv: list[str] | None = None, *,
         clock: Callable[[], datetime] = datetime.now) -> int:
    """Read the list, back up what exists, zip it. Return an exit code."""
    args = build_parser().parse_args(argv)
    configure_logging()

    if not args.list.is_file():
        print(f"error: no such list file: {args.list}", file=sys.stderr)
        return 1

    stamp = clock().strftime("%Y-%m-%d-%H%M")
    run_backup(read_targets(args.list), args.dest, stamp)
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — a throwaway home in a temp directory and a fixed clock.
# Your own file has no demo; it reads your real dotfiles.txt and writes under ~.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Back up a temp home at a fixed time, then confirm the archive exists."""
    print("Dotfile Backup — driven headless in a temp home this file builds.")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        (home / ".bashrc").write_text("export EDITOR=vim\n", encoding="utf-8")
        (home / ".gitconfig").write_text("[user]\n\tname = You\n", encoding="utf-8")
        (home / ".vimrc").write_text("set number\n", encoding="utf-8")
        listing = home / "dotfiles.txt"
        listing.write_text(
            f"{home / '.bashrc'}\n"
            f"{home / '.gitconfig'}\n"
            f"{home / '.vimrc'}\n"
            f"{home / '.zshrc'}\n",  # listed but never created -> a skip
            encoding="utf-8",
        )
        dest = home / "dotfile-backups"

        code = main(["--list", str(listing), "--dest", str(dest)],
                    clock=lambda: datetime(2026, 5, 13, 14, 30))
        print(f"[exit {code}]")

        stamp = "2026-05-13-1430"
        print(f"backup folder {stamp}/ created: {(dest / stamp).is_dir()}")
        print(f"archive {stamp}.zip created:   {(dest / f'{stamp}.zip').is_file()}")


if __name__ == "__main__":
    demo()
```

**The clock is a seam so the demo is reproducible.** A backup folder named after
the current minute cannot match a recorded run, so `main` takes an optional
`clock` that defaults to `datetime.now`. Your own version never passes it; the
demo passes a fixed `datetime(2026, 5, 13, 14, 30)` so the stamp — and the log
line naming the zip — is the same every run. It is the same trick the scheduler
in Exercise 5 uses for its timestamps.

**A missing file warns and the loop continues.** `run_backup` checks
`source.exists()` and, when it is false, logs a warning and moves to the next
target rather than raising. That is the whole reliability idea of the script: a
list written for one machine should still do useful work on another, backing up
what it can and telling you what it could not.

**`shutil.make_archive` does the zip in one line.** Given a `base_name`
(`dest_root/stamp`), a format (`"zip"`), and `root_dir=folder`, it walks the
folder and writes `stamp.zip` beside it. Because `root_dir` is the stamped
folder and the zip is written to its *parent*, the archive never tries to
include itself.

**`copy2`, not `copy`.** `copy2` carries the file's modification time and
permission bits across, so a restored dotfile looks byte-for-byte and
metadata-for-metadata like the original. For a backup that matters — a `.ssh`
config restored world-readable would be a problem.

## Download and run

Download
[problem-01-dotfile-backup-solution.py](./problem-01-dotfile-backup-solution.py)
and run it:

```bash
python problem-01-dotfile-backup-solution.py
```

It needs nothing but the standard library and builds its own temp home, so it
never touches your real `~`. Because it is pure stdlib, you can also
[run it in the online editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-12-automation-scripting/homework/problem-01-dotfile-backup.md).

## Common bugs to catch

- **The whole script dies on the first missing file.** You raised instead of
  warning. Check `source.exists()` and `LOGGER.warning(...)` on the miss.
- **The zip contains the full absolute path to each file.** You built it by hand
  with `zipfile` and wrote `arcname`s wrong. `make_archive` with `root_dir=`
  stores paths relative to that folder.
- **`shutil.SameFileError` or the zip includes itself.** You wrote the archive
  *inside* the folder you were zipping. Write it to the parent, which
  `make_archive(dest_root/stamp, ...)` does.
- **Every run overwrites the last backup.** Your stamp has no time in it, only a
  date, so two runs the same day collide. Include `HHMM`.
- **`~` shows up literally in a path.** You forgot `Path(line).expanduser()`.
  The shell expands `~`; Python does not, until you ask it to.

## Under the hood

<details>
<summary>Under the hood — what a zip actually stores, and why paths inside it are relative</summary>

A zip file is a flat list of entries, each with a *name* that is a path, plus
the compressed bytes and a little metadata. Nothing in the format says those
names have to be relative — you *can* store `C:\Users\you\.bashrc` as an
entry name — but if you do, unzipping it either dumps files in absurd places or,
on a careless extractor, escapes the target directory entirely (the classic
"zip slip" vulnerability). So the convention, and what `make_archive` does, is to
store names relative to a chosen root.

That is what `root_dir=` sets: the folder those names are measured from. Point it
at your stamped backup folder and the entries become `.bashrc`, `.gitconfig`,
`.vimrc` — clean names that extract into whatever folder the user is standing in.
`make_archive` also has a `base_dir` argument for the case where you want the
archive to contain a top-level folder (so everything unzips into
`2026-05-13-1430/` rather than scattering into the current directory); worth
knowing when you decide how you want a restore to feel.

</details>

## Acceptance checklist

- [ ] The list is read with `~` expanded and comments skipped.
- [ ] A file on the list that does not exist warns and does not stop the run.
- [ ] Existing files land in `<dest>/<stamp>/`, and `<dest>/<stamp>.zip` is
      created next to it.
- [ ] Two runs a minute apart produce two backups, neither overwriting the
      other.
- [ ] Status goes through `logging`, and a missing list file exits 1.
- [ ] Committed to Git with a message like
      `Add Week 12 homework 1: dotfile backup`.

## Stretch

- Add `--keep N` that deletes all but the newest N backups after writing a new
  one, so the folder does not grow forever.
- Add a `--restore STAMP` that unzips a chosen backup into a folder you name, so
  the tool is round-trippable.
- Record a small manifest (`files.json`) inside each backup listing what was and
  was not captured, with sizes, so a restore can warn about anything missing.

When your backup survives a missing file, move on to
[Homework 2 — Photo-by-EXIF organizer](./problem-02-photo-exif-organizer.md).
