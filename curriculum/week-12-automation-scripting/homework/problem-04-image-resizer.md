# Homework 4 — Batch image resizer

> **Topic:** Pillow, preserving aspect ratio, and never touching the originals
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hr
> **Why this one:** shrinking a folder of camera photos before you email or upload them is a chore you will automate once and use forever. It also drills the arithmetic everyone gets wrong the first time — scaling height by the same ratio as width — and the discipline of writing to a new folder so a bug cannot eat your originals.

## The Brief

Resize every image in a folder to a target maximum width, keeping each picture's
aspect ratio, and write the results to a separate output folder so the originals
are untouched. An image already narrower than the target is left alone — there
is no point upscaling it and losing quality.

It previews by default and writes only with `--apply`. It handles `.jpg`,
`.png`, and `.webp`.

## Starter

```bash
pip install Pillow
```

```python
"""problem-04-image-resizer.py — resize images to a max width, keeping ratio.

    python problem-04-image-resizer.py DIR --width 1024 [--output DIR] [--apply]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from PIL import Image

LOGGER = logging.getLogger("image_resizer")

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def new_dimensions(size: tuple[int, int], target_width: int) -> tuple[int, int] | None:
    """The (width, height) to resize to, or None if the image is already small."""
    # TODO: if width <= target, return None; else scale height by target/width
    raise NotImplementedError


def process(directory: Path, target_width: int, output_dir: Path, apply: bool) -> int:
    """Resize (or preview resizing) every image."""
    ...


def main(argv: list[str] | None = None) -> int:
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. CLI: `python resize.py DIR --width N [--output DIR] [--apply]`.
2. Preserve aspect ratio — scale height by the same ratio as width.
3. Write resized copies to `--output` (default `DIR/resized/`), leaving the
   originals in place.
4. Skip images already at or below the target width.
5. Support `.jpg`, `.png`, `.webp`; skip everything else. Exit 0 on success, 1
   if the directory is missing.

## Constraints

- **Output goes to a separate folder.** The whole safety story here is that the
  originals are never modified. Write to `--output` (defaulting to a `resized/`
  subfolder), never back over the source.
- **Scale height by the exact ratio, and round once.** `round(height * target /
  width)` computes the new height from the width ratio in one step. Compute the
  ratio and re-apply it to width and height separately and floating-point drift
  can leave you a pixel off, distorting the image.
- **Skip images already within the target.** Upscaling a 200px image to 320px
  invents pixels and looks worse. `new_dimensions` returns `None` for
  already-small images, and the loop treats `None` as "skip".
- **Dry-run by default.** `--apply` is the only path that opens the output file
  for writing.

## Expected output

The shipped answer, [`problem-04-image-resizer-solution.py`](./problem-04-image-resizer-solution.py),
builds three images of known sizes in a temp folder — one wide, one tall, one
already small — previews the work at `--width 320`, applies it, and reports the
output dimensions. Real captured output:

```text
$ python problem-04-image-resizer.py
Image Resizer — driven headless on images this file builds.

Preview at --width 320 (the default is a dry run):
INFO    skip small.png (200px wide, already within 320px)
INFO    would resize tall.png 400x1000 -> 320x800
INFO    would resize wide.png 800x600 -> 320x240
INFO    would resize 2 image(s)
[exit 0]

Apply:
INFO    skip small.png (200px wide, already within 320px)
INFO    resized tall.png 400x1000 -> 320x800
INFO    resized wide.png 800x600 -> 320x240
INFO    resized 2 image(s)
[exit 0]

Output dimensions:
  resized/wide.png: 320x240
  resized/tall.png: 320x800
  small.png left un-copied: True
```

`small.png` (200px wide) is already within 320px, so it is skipped and never
copied. The tall and wide images keep their proportions: 800×600 becomes
320×240, 400×1000 becomes 320×800.

## Steps

1. Write `new_dimensions` and test it on paper: 800×600 at width 320 should give
   320×240; 200×150 at width 320 should give `None`.
2. Write `process` as a dry run and confirm the previewed dimensions match.
3. Add `--apply` and run it on a copy of a photo folder. Confirm the originals
   are untouched and the resized copies are in `resized/`.
4. Open a couple of the resized files and confirm they are not squashed.
5. Re-run and confirm already-resized images (if you point at the output) are
   skipped.

## The Solution

The shipped file is your answer — `new_dimensions`, `process`, `main` — plus a
`demo()` that builds images of known sizes. Your own file has no demo; you point
it at a real folder.

```python
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
```

**`new_dimensions` is the pure decision, and it carries the skip.** It takes a
size and a target and returns either the new dimensions or `None`. Returning
`None` for "already small enough" folds the skip rule into the same function
that does the arithmetic, so `process` reads plainly: compute dimensions, and if
there are none, move on. No separate `if width <= target` scattered through the
loop.

**The height is scaled in one expression.** `round(height * target_width /
width)` multiplies before dividing, so the intermediate value keeps its
precision, and rounds exactly once. The tempting two-step version —
`ratio = target / width; new_h = int(height * ratio)` — introduces a float
`ratio` that is then multiplied again, and `int()` truncates rather than rounds,
so a 1000px height can come out a pixel short. One pixel is invisible on one
image and a visible skew once you have resized a hundred.

**The output folder is created lazily, only under `--apply`.** `output_dir.mkdir`
sits inside the `if apply:` block, so a dry run does not litter an empty
`resized/` folder next to a directory it was only ever asked to preview.

**Non-images are filtered by suffix before Pillow ever opens them.** Checking
`path.suffix.lower() in IMAGE_SUFFIXES` first means a `.txt` or a `.zip` in the
folder is skipped without paying for a failed `Image.open`, and without a
`try/except` around every file to swallow the `UnidentifiedImageError` that a
non-image would otherwise raise.

## Run it

Copy the worked answer on this page into `problem-04-image-resizer.py` and run it:

```bash
pip install Pillow
python problem-04-image-resizer.py
```

It builds its own images in a temp folder, so it never touches your photos.

## Common bugs to catch

- **The resized image is squashed or stretched.** You set a fixed height instead
  of scaling it by the width ratio. `round(height * target / width)`.
- **Small images get *bigger*.** You resized unconditionally. Return `None` (and
  skip) when the image is already within the target width.
- **The originals were overwritten.** You saved back to the source path. Write
  to the output folder.
- **`UnidentifiedImageError` on a `.txt` in the folder.** You did not filter by
  suffix before opening. Check the suffix first.
- **An empty `resized/` folder appears after a dry run.** You created the output
  directory outside the `if apply:` guard.
- **`.webp` files are skipped even though you wanted them.** Your suffix set left
  `.webp` out, or you compared suffixes case-sensitively against `.WEBP`.

## Under the hood

<details>
<summary>Under the hood — what `resize` actually does to pixels, and the quality knobs</summary>

Shrinking an image is not just "throw away every other pixel". A good downscale
computes each output pixel from a *neighbourhood* of input pixels, so fine detail
is averaged rather than dropped — otherwise you get aliasing, the jagged edges
and moiré patterns you see when a photo is scaled carelessly. Pillow's
`resize(dimensions)` defaults to a high-quality resampling filter (`BICUBIC` in
recent versions), and you can ask for `Image.Resampling.LANCZOS`, the best for
downscaling, when quality matters more than speed.

There is a second knob at save time. `img.save(dst)` uses the format's default
encoder settings; `img.save(dst, optimize=True, quality=85)` tells the JPEG
encoder to spend a little more effort for a smaller file, and 85 is the usual
sweet spot where the loss is invisible but the file is a fraction of the size.
Those two decisions — how you resample and how you encode — are where "resize a
folder" turns into "resize a folder *well*", and they are worth knowing about
before you batch-process a wedding's worth of photos and discover afterwards that
they are all a bit soft.

</details>

## Acceptance checklist

- [ ] Resized images keep their aspect ratio (no squashing).
- [ ] An image already within the target width is skipped, not upscaled.
- [ ] Originals are untouched; resized copies are in the output folder.
- [ ] Preview writes nothing; `--apply` writes the copies.
- [ ] `.jpg`, `.png`, and `.webp` are handled; other files are skipped.
- [ ] Committed to Git with a message like
      `Add Week 12 homework 4: batch image resizer`.

## Stretch

- Add `--format webp` that converts everything to a chosen format on the way
  out, so you can shrink *and* re-encode in one pass.
- Add `--max-height` as well, and fit each image inside a width×height box
  rather than only capping the width.
- Print a size-saved summary — total bytes before and after — so you can see
  what the run actually bought you.

When your images shrink without distorting, move on to
[Homework 5 — GitHub releases fetcher](./problem-05-github-releases.md).
