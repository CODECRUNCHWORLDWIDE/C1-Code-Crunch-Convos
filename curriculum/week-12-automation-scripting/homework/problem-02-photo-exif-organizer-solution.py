"""problem-02-photo-exif-organizer-solution.py — the photo organizer, headless.

The homework answer sorts a folder of photos into YYYY/MM/ subfolders by their
EXIF "DateTimeOriginal", falling back to the file's modification time. Your own
problem-02-photo-exif-organizer.py ends in ``raise SystemExit(main())`` and you
point it at a real photo folder.

A published answer needs photos to sort and must not depend on yours, so the
demo builds a few images in a temp folder — two with real EXIF dates, one with
none (so the mtime fallback fires), and a non-image to be skipped — previews the
moves, applies them, and checks each file landed. The organizer being tested is
identical either way.

Needs Pillow: ``pip install Pillow``.

Run it with::

    python problem-02-photo-exif-organizer-solution.py
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from PIL import Image, UnidentifiedImageError

LOGGER = logging.getLogger("photo_organizer")

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp"}
EXIF_DATETIME_ORIGINAL = 36867  # 0x9003, "YYYY:MM:DD HH:MM:SS"


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


def exif_datetime(path: Path) -> datetime | None:
    """The photo's EXIF DateTimeOriginal, or None if it has none we can read."""
    try:
        with Image.open(path) as img:
            getter = getattr(img, "_getexif", None)  # only JPEGs carry it
            exif = getter() if getter is not None else None
    except (UnidentifiedImageError, OSError):
        return None
    raw = (exif or {}).get(EXIF_DATETIME_ORIGINAL)
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        return None


def photo_date(path: Path) -> datetime:
    """The EXIF capture date if present, otherwise the file's modification time."""
    return exif_datetime(path) or datetime.fromtimestamp(path.stat().st_mtime)


def organize(directory: Path, apply: bool) -> int:
    """Move (or preview moving) each image into directory/YYYY/MM/. Return the count."""
    acted = 0
    for path in sorted(directory.iterdir()):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        when = photo_date(path)
        relative = f"{when:%Y}/{when:%m}/{path.name}"
        destination = directory / f"{when:%Y}" / f"{when:%m}" / path.name
        if destination == path:
            continue

        LOGGER.info("%s %s -> %s", "moved" if apply else "would move", path.name, relative)
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(destination))
        acted += 1
    return acted


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photo-organizer",
        description="Sort photos into YYYY/MM/ folders by EXIF date.",
    )
    parser.add_argument("directory", type=Path, help="Folder of photos to sort.")
    parser.add_argument("--apply", action="store_true",
                        help="Actually move files. Without it, dry-run.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Sort the photos, or preview it. Return an exit code."""
    args = build_parser().parse_args(argv)
    configure_logging()

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    acted = organize(args.directory, args.apply)
    verb = "moved" if args.apply else "would move"
    LOGGER.info("%s %d photo(s)", verb, acted)
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — real images with known dates in a temp folder. Your own
# file has no demo; you point it at your camera roll.
# --------------------------------------------------------------------------- #


def write_jpeg(path: Path, taken: str | None) -> None:
    """A tiny JPEG, optionally carrying an EXIF DateTimeOriginal."""
    image = Image.new("RGB", (16, 16), (200, 30, 30))
    if taken is None:
        image.save(path)
        return
    exif = image.getexif()
    exif.get_ifd(0x8769)[EXIF_DATETIME_ORIGINAL] = taken  # the Exif sub-IFD
    image.save(path, exif=exif)


def demo() -> None:
    """Sort a temp folder of images with known dates and confirm each landed."""
    import os

    print("Photo Organizer — driven headless on images this file builds.")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        write_jpeg(folder / "img_a.jpg", "2023:07:14 09:30:00")   # EXIF -> 2023/07
        write_jpeg(folder / "img_b.jpg", "2024:01:02 18:05:00")   # EXIF -> 2024/01
        write_jpeg(folder / "img_c.jpg", None)                    # no EXIF -> mtime
        os.utime(folder / "img_c.jpg",
                 (datetime(2022, 3, 15, 12, 0).timestamp(),) * 2)  # mtime -> 2022/03
        (folder / "notes.txt").write_text("not a photo\n", encoding="utf-8")

        print("Preview (the default — nothing is moved):")
        print(f"[exit {main([str(folder)])}]")
        print()
        print("Apply:")
        print(f"[exit {main([str(folder), '--apply'])}]")
        print()
        print("Landed where expected:")
        for rel in ("2023/07/img_a.jpg", "2024/01/img_b.jpg", "2022/03/img_c.jpg"):
            print(f"  {rel}: {(folder / rel).is_file()}")
        print(f"  notes.txt left in place: {(folder / 'notes.txt').is_file()}")


if __name__ == "__main__":
    demo()
