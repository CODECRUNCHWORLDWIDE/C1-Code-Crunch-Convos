"""File Organizer Bot — starter skeleton.

Fill in the TODOs to complete the mini-project. The skeleton handles
argument parsing, config loading, logging setup, and the main dispatch
between run-once and watch modes. The interesting bits — categorizing
and moving files — are left for you.

Run:

    python starter.py ~/Downloads --config sample-config.json
    python starter.py ~/Downloads --config sample-config.json --apply
    python starter.py ~/Downloads --config sample-config.json --watch --apply

See README.md for the full specification and rubric.
"""
from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import time
from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="organize",
        description="Sort files into subfolders by extension.",
    )
    parser.add_argument("directory", type=Path, help="Folder to organize")
    parser.add_argument(
        "--config", type=Path, default=Path("config.json"),
        help="Path to the JSON config (default: ./config.json)",
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually move files (default: dry-run)")
    parser.add_argument("--watch", action="store_true",
                        help="Keep watching the directory")
    parser.add_argument("--interval", type=float, default=10.0,
                        help="Seconds between polls in watch mode (default: 10)")
    parser.add_argument("--log", type=Path, default=None,
                        help="Log file path (default: <DIR>/organize.log)")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increase verbosity (-v, -vv)")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    return parser


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config(path: Path) -> dict[str, list[str]]:
    """Load the JSON category-to-extensions mapping."""
    if not path.is_file():
        raise FileNotFoundError(f"config file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("config must be a JSON object {category: [exts]}")
    for category, exts in data.items():
        if not isinstance(exts, list):
            raise ValueError(f"category {category!r}: extensions must be a list")
    return data


def find_other_category(config: dict[str, list[str]]) -> str:
    """Return the first category with an empty extension list (the fallback)."""
    for category, exts in config.items():
        if not exts:
            return category
    # No explicit fallback in config — default to "Other"
    return "Other"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(log_file: Path, verbosity: int) -> None:
    level = logging.WARNING - (verbosity * 10)
    level = max(level, logging.DEBUG)
    fmt = "%(asctime)s %(levelname)-5s %(message)s"

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    except OSError as exc:
        # We can still log to stdout — just warn about the file.
        print(f"warning: could not open log file {log_file}: {exc}",
              file=sys.stderr)

    logging.basicConfig(level=level, format=fmt, handlers=handlers, force=True)


# ---------------------------------------------------------------------------
# Core logic — TODO: implement these
# ---------------------------------------------------------------------------

def categorize(path: Path, config: dict[str, list[str]], fallback: str) -> str:
    """Return the category folder name for a given file path.

    TODO:
      - Compare path.suffix (lowercased) against each category's extension list.
      - Return the matching category, else return `fallback`.
    """
    suffix = path.suffix.lower()
    for category, exts in config.items():
        if suffix in (e.lower() for e in exts):
            return category
    return fallback


def unique_path(dst: Path) -> Path:
    """Return a non-clashing destination by appending -1, -2, ... if needed."""
    if not dst.exists():
        return dst
    stem, suffix = dst.stem, dst.suffix
    i = 1
    while True:
        candidate = dst.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def iter_loose_files(directory: Path, category_names: Iterable[str],
                     log_file: Path) -> Iterable[Path]:
    """Yield files in `directory` that are not already inside a category folder."""
    category_set = set(category_names)
    for path in directory.iterdir():
        if path.is_dir():
            continue
        if path.resolve() == log_file.resolve():
            continue
        if path.parent.name in category_set:
            continue
        yield path


def organize_once(directory: Path, config: dict[str, list[str]],
                  apply: bool, log_file: Path) -> int:
    """Run the organizer one time. Return the number of files moved (or planned)."""
    fallback = find_other_category(config)
    moved = 0
    for src in iter_loose_files(directory, config.keys(), log_file):
        category = categorize(src, config, fallback)
        target_dir = directory / category
        # TODO: ensure target_dir exists if apply is True
        target = unique_path(target_dir / src.name)
        if apply:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(target))
            logging.info("moved %s -> %s", src.name, target.relative_to(directory))
        else:
            logging.info("would move %s -> %s", src.name,
                         target.relative_to(directory))
        moved += 1
    return moved


def watch(directory: Path, config: dict[str, list[str]], apply: bool,
          interval: float, log_file: Path) -> None:
    """Run organize_once on an interval. Stop on Ctrl-C."""
    logging.info("watching %s every %ss (Ctrl-C to stop)", directory, interval)
    try:
        while True:
            organize_once(directory, config, apply, log_file)
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("stopped by user")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    log_file = args.log or (args.directory / "organize.log")
    setup_logging(log_file, args.verbose)

    try:
        config = load_config(args.config)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: invalid config — {exc}", file=sys.stderr)
        return 1

    if args.watch:
        watch(args.directory, config, args.apply, args.interval, log_file)
    else:
        count = organize_once(args.directory, config, args.apply, log_file)
        verb = "Moved" if args.apply else "Would move"
        logging.info("%s %d file(s).", verb, count)
        if not args.apply:
            logging.info("Re-run with --apply to make changes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
