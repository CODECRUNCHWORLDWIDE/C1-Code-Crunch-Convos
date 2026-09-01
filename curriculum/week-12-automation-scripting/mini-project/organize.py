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
