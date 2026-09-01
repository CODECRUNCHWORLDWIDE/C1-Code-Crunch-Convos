"""organize.py — File Organizer Bot (Week 12 mini-project reference solution).

Tidy a directory into subfolders by file type, using a JSON category map.

Usage
-----
    # Preview what would happen (dry-run is the default)
    python organize.py ~/Downloads --config config.json

    # Actually move the files
    python organize.py ~/Downloads --config config.json --apply

    # Keep running and re-check every 5 seconds
    python organize.py ~/Downloads --config config.json --watch --interval 5 --apply

Exit codes
----------
    0   success (including a clean Ctrl-C out of --watch)
    1   bad input: directory missing, config missing/malformed, log unwritable
    2   bad command-line arguments (argparse supplies this)
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import time
from pathlib import Path

__version__ = "1.0.0"

LOG_FORMAT = "%(asctime)s %(levelname)-5s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGER = logging.getLogger("organize")


class ConfigError(ValueError):
    """Raised when config.json is missing, unreadable, or the wrong shape."""


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #


def load_config(path: Path) -> dict[str, list[str]]:
    """Read and validate the category map.

    Extensions are normalised to lowercase and forced to start with a dot, so
    both ``"jpg"`` and ``".JPG"`` in the config match a file named ``photo.JPG``.
    """
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"config file not found: {path}") from exc
    except OSError as exc:
        raise ConfigError(f"cannot read config file {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"config file {path} is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError(f"config file {path} must contain a JSON object")

    config: dict[str, list[str]] = {}
    for category, extensions in raw.items():
        if not isinstance(extensions, list) or not all(
            isinstance(item, str) for item in extensions
        ):
            raise ConfigError(
                f"category {category!r} must map to a list of extension strings"
            )
        config[category] = [_normalise_extension(item) for item in extensions]
    return config


def _normalise_extension(extension: str) -> str:
    extension = extension.strip().lower()
    return extension if extension.startswith(".") else f".{extension}"


def build_extension_map(config: dict[str, list[str]]) -> dict[str, str]:
    """Invert the config into ``{".jpg": "Images", ...}``.

    If two categories claim the same extension the first one in the file wins;
    ``setdefault`` keeps that rule explicit instead of silently last-write-wins.
    """
    mapping: dict[str, str] = {}
    for category, extensions in config.items():
        for extension in extensions:
            if extension in mapping:
                LOGGER.warning(
                    "extension %s claimed by both %s and %s; keeping %s",
                    extension,
                    mapping[extension],
                    category,
                    mapping[extension],
                )
                continue
            mapping[extension] = category
    return mapping


def fallback_category(config: dict[str, list[str]]) -> str | None:
    """The first category with an empty extension list, or None."""
    for category, extensions in config.items():
        if not extensions:
            return category
    return None


def categorise(
    path: Path, extension_map: dict[str, str], fallback: str | None
) -> str | None:
    """Return the destination category for ``path``, or None to leave it alone."""
    return extension_map.get(path.suffix.lower(), fallback)


# --------------------------------------------------------------------------- #
# Filesystem
# --------------------------------------------------------------------------- #


def unique_path(dst: Path, reserved: set[Path] | None = None) -> Path:
    """Return ``dst``, or ``name-1.ext`` / ``name-2.ext`` … if it is taken.

    ``reserved`` holds paths this run has already promised to something else.
    It matters in dry-run mode, where nothing is created on disk and
    ``dst.exists()`` alone would hand the same name to two different files.
    """
    reserved = reserved or set()
    if not dst.exists() and dst not in reserved:
        return dst
    stem, suffix = dst.stem, dst.suffix
    index = 1
    while True:
        candidate = dst.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists() and candidate not in reserved:
            return candidate
        index += 1


def organize_once(
    directory: Path,
    config: dict[str, list[str]],
    *,
    apply: bool = False,
    log_path: Path | None = None,
) -> int:
    """Sort every top-level file in ``directory``. Return the number acted on."""
    extension_map = build_extension_map(config)
    fallback = fallback_category(config)
    skip = {log_path.resolve()} if log_path is not None else set()
    reserved: set[Path] = set()
    acted = 0

    for entry in sorted(directory.iterdir()):
        if entry.is_dir():
            LOGGER.debug("skip %s (directory)", entry.name)
            continue
        if not entry.is_file():
            LOGGER.debug("skip %s (not a regular file)", entry.name)
            continue
        if entry.resolve() in skip:
            LOGGER.debug("skip %s (log file)", entry.name)
            continue

        category = categorise(entry, extension_map, fallback)
        if category is None:
            LOGGER.debug("skip %s (no category and no fallback)", entry.name)
            continue

        destination = unique_path(directory / category / entry.name, reserved)
        reserved.add(destination)
        relative = f"{category}/{destination.name}"

        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(entry), str(destination))
            except OSError as exc:
                LOGGER.error("could not move %s: %s", entry.name, exc)
                continue
            LOGGER.info("moved %s -> %s", entry.name, relative)
        else:
            LOGGER.info("would move %s -> %s", entry.name, relative)
        acted += 1

    return acted


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(f"must be > 0, got {number}")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="organize",
        description="Tidy a directory into subfolders by file type.",
    )
    parser.add_argument(
        "directory", metavar="DIRECTORY", type=Path, help="The folder to organize."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.json"),
        help="Path to config.json (default: %(default)s)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files. Without it, dry-run.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Keep running and re-check the directory every --interval seconds.",
    )
    parser.add_argument(
        "--interval",
        type=positive_float,
        default=10.0,
        metavar="SECONDS",
        help="Poll interval, only with --watch (default: %(default)s)",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        metavar="PATH",
        help="Append-only log file (default: <DIRECTORY>/organize.log)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v for DEBUG)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


def configure_logging(log_path: Path, verbosity: int) -> None:
    """Send the same formatted records to the console and to ``log_path``."""
    for handler in list(LOGGER.handlers):
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.setLevel(logging.DEBUG if verbosity else logging.INFO)
    LOGGER.propagate = False
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    console = logging.StreamHandler(stream=sys.stdout)
    console.setFormatter(formatter)
    LOGGER.addHandler(console)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    directory: Path = args.directory.expanduser()
    if not directory.is_dir():
        print(f"error: {directory} is not a directory", file=sys.stderr)
        return 1

    log_path: Path = (args.log or directory / "organize.log").expanduser()
    try:
        configure_logging(log_path, args.verbose)
    except OSError as exc:
        print(f"error: cannot open log file {log_path}: {exc}", file=sys.stderr)
        return 1

    try:
        config = load_config(args.config.expanduser())
    except ConfigError as exc:
        LOGGER.error("%s", exc)
        return 1

    if not args.watch:
        acted = organize_once(directory, config, apply=args.apply, log_path=log_path)
        verb = "moved" if args.apply else "would move"
        LOGGER.info("%s %d file(s)", verb, acted)
        return 0

    LOGGER.info(
        "watching %s every %gs (Ctrl-C to stop)%s",
        directory,
        args.interval,
        "" if args.apply else " [dry-run]",
    )
    try:
        while True:
            organize_once(directory, config, apply=args.apply, log_path=log_path)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        LOGGER.info("stopped by user")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
