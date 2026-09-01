"""problem-04-image-resizer-solution.py — the batch resizer, proven headless.

The homework answer resizes every image in a folder to a maximum width, keeping
the aspect ratio, writing to an output folder so the originals are untouched,
and skipping images already within the target. Your own
problem-04-image-resizer.py ends in ``raise SystemExit(main())`` and you point
it at a real folder.

A published answer needs images and must not depend on yours, so the demo builds
three in a temp folder — one wide, one tall, one already small — previews the
work, applies it, and checks the output dimensions. The resizer being tested is
identical either way.

Needs Pillow: ``pip install Pillow``.

Run it with::

    python problem-04-image-resizer-solution.py
"""

from __future__ import annotations

import argparse
import logging
import sys
import tempfile
from pathlib import Path

from PIL import Image

LOGGER = logging.getLogger("image_resizer")

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


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


def new_dimensions(size: tuple[int, int], target_width: int) -> tuple[int, int] | None:
    """The (width, height) to resize to, or None if the image is already small.

    The height is scaled by the same ratio as the width, so the picture keeps
    its shape instead of stretching.
    """
    width, height = size
    if width <= target_width:
        return None
    return target_width, round(height * target_width / width)


def process(directory: Path, target_width: int, output_dir: Path, apply: bool) -> int:
    """Resize (or preview resizing) every image. Return how many were acted on."""
    acted = 0
    for path in sorted(directory.iterdir()):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        with Image.open(path) as image:
            width, height = image.size
            dimensions = new_dimensions(image.size, target_width)
            if dimensions is None:
                LOGGER.info("skip %s (%dpx wide, already within %dpx)",
                            path.name, width, target_width)
                continue
            LOGGER.info("%s %s %dx%d -> %dx%d",
                        "resized" if apply else "would resize",
                        path.name, width, height, dimensions[0], dimensions[1])
            if apply:
                output_dir.mkdir(parents=True, exist_ok=True)
                image.resize(dimensions).save(output_dir / path.name)
        acted += 1
    return acted


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resize",
        description="Resize images to a maximum width, keeping aspect ratio.",
    )
    parser.add_argument("directory", type=Path, help="Folder of images.")
    parser.add_argument("--width", type=int, default=1024,
                        help="Maximum width in pixels (default: %(default)s)")
    parser.add_argument("--output", type=Path, default=None,
                        help="Where resized copies go (default: DIR/resized/)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write files. Without it, dry-run.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Resize the folder, or preview it. Return an exit code."""
    args = build_parser().parse_args(argv)
    configure_logging()

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    output_dir = args.output or (args.directory / "resized")
    acted = process(args.directory, args.width, output_dir, args.apply)
    verb = "resized" if args.apply else "would resize"
    LOGGER.info("%s %d image(s)", verb, acted)
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — three images of known sizes in a temp folder. Your own
# file has no demo; you point it at a real folder.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Resize a temp folder to 320px wide and confirm the output dimensions."""
    print("Image Resizer — driven headless on images this file builds.")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        Image.new("RGB", (800, 600), (30, 120, 200)).save(folder / "wide.png")
        Image.new("RGB", (400, 1000), (200, 120, 30)).save(folder / "tall.png")
        Image.new("RGB", (200, 150), (30, 200, 120)).save(folder / "small.png")
        (folder / "notes.txt").write_text("not an image\n", encoding="utf-8")
        output = folder / "resized"

        print("Preview at --width 320 (the default is a dry run):")
        print(f"[exit {main([str(folder), '--width', '320'])}]")
        print()
        print("Apply:")
        print(f"[exit {main([str(folder), '--width', '320', '--apply'])}]")
        print()
        print("Output dimensions:")
        for name in ("wide.png", "tall.png"):
            with Image.open(output / name) as resized:
                print(f"  resized/{name}: {resized.size[0]}x{resized.size[1]}")
        print(f"  small.png left un-copied: {not (output / 'small.png').exists()}")


if __name__ == "__main__":
    demo()
