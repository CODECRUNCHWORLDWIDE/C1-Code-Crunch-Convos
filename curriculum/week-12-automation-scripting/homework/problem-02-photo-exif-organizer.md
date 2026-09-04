# Homework 2 — Photo-by-EXIF-date organizer

> **Topic:** reading EXIF with Pillow, an mtime fallback, and a dry-run default
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hr
> **Why this one:** a folder of `IMG_0423.jpg` is useless; the same photos in `2023/07/` folders are a library. It teaches reading structured metadata out of a binary file, and — more importantly — what to do when that metadata is missing, which for photos is often.

## The Brief

Walk a folder of photos and move each one into `YYYY/MM/` subfolders based on
when it was taken. The date comes from the photo's EXIF "DateTimeOriginal" tag;
when a photo has no EXIF date — a screenshot, an export, a scan — fall back to
the file's modification time so it still gets filed.

It previews by default and only moves with `--apply`, the same rule as every
file-touching script this week. Non-image files are skipped.

## Starter

```bash
pip install Pillow
```

```python
"""problem-02-photo-exif-organizer.py — sort photos into YYYY/MM/ by EXIF date.

    python problem-02-photo-exif-organizer.py ~/Pictures --apply
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, UnidentifiedImageError

LOGGER = logging.getLogger("photo_organizer")

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp"}
EXIF_DATETIME_ORIGINAL = 36867  # 0x9003, "YYYY:MM:DD HH:MM:SS"


def exif_datetime(path: Path) -> datetime | None:
    """The photo's EXIF DateTimeOriginal, or None if it has none we can read."""
    # TODO: Image.open(path), read tag 36867, strptime "%Y:%m:%d %H:%M:%S"
    raise NotImplementedError


def photo_date(path: Path) -> datetime:
    """The EXIF capture date if present, otherwise the file's modification time."""
    # TODO: return exif_datetime(path) or datetime.fromtimestamp(mtime)
    raise NotImplementedError


def organize(directory: Path, apply: bool) -> int:
    """Move (or preview moving) each image into directory/YYYY/MM/."""
    ...


def main(argv: list[str] | None = None) -> int:
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. For each image, read EXIF tag `36867` (`DateTimeOriginal`), format
   `"YYYY:MM:DD HH:MM:SS"`, and file it under `YYYY/MM/`.
2. If the EXIF date is missing or unreadable, fall back to
   `Path.stat().st_mtime`.
3. Preview by default; `--apply` moves. Log `would move` / `moved`.
4. Skip non-image files (by suffix), and skip images already in a `YYYY/MM/`
   folder.
5. Exit 0 on success, 1 if the directory does not exist.

## Constraints

- **`_getexif()` is JPEG-only; guard for its absence.** A PNG has no `_getexif`
  method, so calling it blindly raises `AttributeError`. Fetch it with `getattr`
  and treat "no EXIF" the same as "no date", which sends the file to the mtime
  fallback.
- **Parse the EXIF string with `strptime`, and catch a bad one.** Cameras
  occasionally write a malformed or zero date (`0000:00:00 00:00:00`).
  `strptime` raises `ValueError` on those; catch it and fall back rather than
  crash.
- **`shutil.move`, not `Path.rename`.** The `YYYY/MM/` folders are created under
  the same directory, but a photo library often lives on an external drive;
  `shutil.move` handles a cross-volume move, `rename` raises on it.
- **Build the destination string with `f"{when:%Y}/{when:%m}/{name}"`.** Forward
  slashes in the log line read the same on every OS, and formatting the datetime
  directly avoids an off-by-one from zero-padding the month by hand.

## Expected output

The shipped answer, [`problem-02-photo-exif-organizer-solution.py`](./problem-02-photo-exif-organizer-solution.py),
builds real images in a temp folder — two with EXIF dates, one with none so the
mtime fallback fires, and a non-image to be skipped — previews, applies, and
checks each file landed. Real captured output:

```text
$ python problem-02-photo-exif-organizer.py
Photo Organizer — driven headless on images this file builds.

Preview (the default — nothing is moved):
INFO    would move img_a.jpg -> 2023/07/img_a.jpg
INFO    would move img_b.jpg -> 2024/01/img_b.jpg
INFO    would move img_c.jpg -> 2022/03/img_c.jpg
INFO    would move 3 photo(s)
[exit 0]

Apply:
INFO    moved img_a.jpg -> 2023/07/img_a.jpg
INFO    moved img_b.jpg -> 2024/01/img_b.jpg
INFO    moved img_c.jpg -> 2022/03/img_c.jpg
INFO    moved 3 photo(s)
[exit 0]

Landed where expected:
  2023/07/img_a.jpg: True
  2024/01/img_b.jpg: True
  2022/03/img_c.jpg: True
  notes.txt left in place: True
```

`img_c.jpg` has no EXIF date, so it is filed by its modification time; the
`notes.txt` is not an image and is left where it is.

## Steps

1. Write `exif_datetime` and test it on one photo from your own phone. Print the
   raw tag value first, before you parse it.
2. Add the mtime fallback in `photo_date`, and confirm a screenshot (no EXIF)
   still gets a date.
3. Write `organize` as a dry run and eyeball the `YYYY/MM/` destinations.
4. Add `--apply` and run it on a copy of a small photo folder. Confirm the
   originals moved and non-images stayed.
5. Run it again and confirm nothing moves the second time — the files are
   already filed.

## The Solution

The shipped file is your answer — `exif_datetime`, `photo_date`, `organize`,
`main` — plus a `demo()` that builds images with known dates. Your own file has
no demo; you point it at a real photo folder.

```python
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
```

**`exif_datetime` returns `None` for "no usable date", and there are three ways
to get there.** The image cannot be opened (`UnidentifiedImageError`), it has no
`_getexif` (a PNG), or the tag is absent or unparseable. All three collapse to
`None`, and `photo_date` reads that as "use the modification time". Keeping the
"why" out of the return value is deliberate: the caller does not care *why*
there is no EXIF date, only that there is not one.

**`_getexif` is fetched with `getattr`, not called directly.** Only Pillow's
JPEG reader defines it; a `PngImageFile` does not, so `img._getexif()` would
raise `AttributeError` on the first screenshot in your folder.
`getattr(img, "_getexif", None)` turns "this format has no EXIF" into a clean
`None` instead of an exception you would have to special-case.

**The mtime fallback is a real answer, not a last resort.** `datetime.fromtimestamp(path.stat().st_mtime)`
gives a genuine date for anything the filesystem tracks, which is everything.
It is a weaker signal than EXIF — copying a file usually resets its mtime — so
EXIF wins when both exist, but a photo with no EXIF still lands in a sensible
folder rather than being skipped.

**The destination is formatted, not built by hand.** `f"{when:%Y}/{when:%m}/..."`
zero-pads the month for free (`07`, not `7`), so `2023/07/` sorts correctly next
to `2023/11/`. Assemble the string with `str(when.month)` and you get `2023/7/`,
which sorts *after* `2023/11/` in a file browser — a bug you would not notice
until December.

## Run it

Copy the worked answer on this page into `problem-02-photo-exif-organizer.py` and run it:

```bash
pip install Pillow
python problem-02-photo-exif-organizer.py
```

It builds its own images in a temp folder, so it never touches your photos.

## Common bugs to catch

- **`AttributeError: 'PngImageFile' object has no attribute '_getexif'`.** You
  called `_getexif()` directly on a non-JPEG. Fetch it with `getattr` and fall
  back on `None`.
- **`ValueError: time data '0000:00:00 00:00:00' does not match format`.** A
  camera wrote a zero date. Catch the `ValueError` from `strptime` and use the
  mtime.
- **`2023/7/` sorts after `2023/11/`.** You built the month without zero-padding.
  Format the datetime (`%m`) instead.
- **Screenshots are skipped instead of filed by date.** Your code returned early
  when EXIF was missing rather than falling back to the mtime.
- **`OSError: Invalid cross-device link`.** The photo folder is on a different
  drive from where you built the destination. Use `shutil.move`.
- **The month folder appears but the file is still in the root.** You logged the
  move but forgot the `if apply:` `shutil.move`, or you created the folder and
  did not move into it.

## Under the hood

<details>
<summary>Under the hood — where DateTimeOriginal actually lives, and why the number is 36867</summary>

EXIF is a set of tagged fields packed into the JPEG's header, organised into
nested tables called IFDs (Image File Directories). The everyday tags —
orientation, resolution — sit in the main IFD, but the camera-specific ones,
including the three date fields, live in a *sub*-directory pointed to by tag
`34665` (`ExifOffset`). `DateTimeOriginal` is tag `36867` (hex `0x9003`) inside
that sub-directory, and there are two siblings that trip people up:
`DateTime` (`306`) is when the file was last *modified*, and
`DateTimeDigitized` (`36868`) is when it was scanned or imported.
`DateTimeOriginal` is the one that means "when the shutter fired", which is what
you want to sort by.

Pillow's private `_getexif()` flattens that nested structure into one dict for
you, which is why `36867` works as a top-level key even though the tag lives in
a sub-IFD. The public, modern API is `img.getexif()`, and to reach
`DateTimeOriginal` through it you go `img.getexif().get_ifd(0x8769)[0x9003]` —
more explicit, and what you would use in code you were not writing for a
one-off. Either way the value is a string like `"2023:07:14 09:30:00"` with
colons in the date, which is why the `strptime` format is `"%Y:%m:%d %H:%M:%S"`
and not the ISO one you might reach for out of habit.

</details>

## Acceptance checklist

- [ ] A photo with EXIF `DateTimeOriginal` lands in `YYYY/MM/` by capture date.
- [ ] A photo with no EXIF is filed by its modification time, not skipped.
- [ ] A non-image file is left where it is.
- [ ] Preview moves nothing; `--apply` moves and logs each move.
- [ ] A second run moves nothing (the photos are already filed).
- [ ] Committed to Git with a message like
      `Add Week 12 homework 2: photo EXIF organizer`.

## Stretch

- Write a `pytest` test with a fake `Image` class (a mock) so the parsing logic
  is tested with no real JPEG on disk.
- Add `--by day` that files into `YYYY/MM/DD/` instead, and `--copy` that copies
  rather than moves, for when you want the originals left in place.
- Detect and skip exact duplicates (same bytes) instead of filing two copies of
  the same photo under the same month.

When photos land in the right folders, move on to
[Homework 3 — CSV to Markdown](./problem-03-csv-to-markdown.md).
