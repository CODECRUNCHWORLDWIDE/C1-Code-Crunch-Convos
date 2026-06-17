"""Exercise 02 — Bulk rename.

Rename every file in DIR whose name contains OLD, replacing OLD with NEW.
Defaults to dry-run (no changes); pass --apply to actually rename.

Run (preview):
    python exercise-02-bulk-rename.py ./testdata "IMG_" "Photo_"

Run (apply):
    python exercise-02-bulk-rename.py ./testdata "IMG_" "Photo_" --apply

Stretch:
  1. Add --pattern (glob) so only files matching it are considered.
  2. Add --recursive to descend into subdirectories.
  3. Refuse to overwrite an existing file; warn instead and skip.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="bulk_rename",
        description="Replace OLD with NEW in filenames inside DIR.",
    )
    p.add_argument("directory", type=Path, help="Folder to process")
    p.add_argument("old", help="Substring to find in filenames")
    p.add_argument("new", help="Replacement substring")
    p.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files. Without it, just preview.",
    )
    return p


def plan_renames(directory: Path, old: str, new: str) -> list[tuple[Path, Path]]:
    """Return a list of (source, target) pairs that would be renamed."""
    plans: list[tuple[Path, Path]] = []
    for path in directory.iterdir():
        if path.is_file() and old in path.name:
            target = path.with_name(path.name.replace(old, new))
            plans.append((path, target))
    return plans


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    plans = plan_renames(args.directory, args.old, args.new)
    if not plans:
        print("no matching files found")
        return 0

    for src, dst in plans:
        if args.apply:
            src.rename(dst)
            print(f"renamed  {src.name} -> {dst.name}")
        else:
            print(f"would rename  {src.name} -> {dst.name}")

    verb = "Renamed" if args.apply else "Would rename"
    print(f"\n{verb} {len(plans)} file(s).")
    if not args.apply:
        print("Re-run with --apply to actually make changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
