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
