"""exercise-02-bulk-rename-solution.py — the bulk renamer, proven headless.

The exercise part is the starter with its TODOs filled in: replace OLD with NEW
in the names of files inside DIRECTORY, previewing by default and moving a byte
only when --apply is passed, never clobbering an existing target.

Your own exercise-02-bulk-rename.py ends in ``raise SystemExit(main())`` and is
run from the shell against a sandbox you build by hand. A published answer
cannot ask you to build a folder first, so this file builds the exact sandbox
the exercise describes inside a temp directory, drives ``main()`` across it —
preview, apply, then a second apply to show the run is idempotent — and deletes
the sandbox on the way out. The renamer being tested is identical either way.

Run it with::

    python exercise-02-bulk-rename-solution.py
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

LABEL_WIDTH = 7


def build_parser() -> argparse.ArgumentParser:
    """Return the parser for the bulk renamer."""
    parser = argparse.ArgumentParser(
        prog="bulk-rename",
        description="Replace OLD with NEW in filenames inside DIRECTORY.",
    )
    parser.add_argument("directory", type=Path, help="Folder to operate on")
    parser.add_argument("old", help="Substring to look for in each filename")
    parser.add_argument("new", help="Replacement substring")
    parser.add_argument("--pattern", default="*",
                        help="Glob to limit the files considered (default: %(default)s)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename. Without this flag, only preview.")
    return parser


def plan_renames(directory: Path, old: str, new: str, pattern: str) -> list[tuple[Path, Path]]:
    """Return (source, target) pairs for files whose name contains old.

    Directories are ignored. Pairs where the name would not change are
    ignored. The list is sorted by source name so repeated runs print the
    same lines in the same order.
    """
    planned: list[tuple[Path, Path]] = []
    for source in sorted(directory.glob(pattern), key=lambda path: path.name):
        if not source.is_file():
            continue
        new_name = source.name.replace(old, new)
        if new_name == source.name:
            continue
        planned.append((source, source.with_name(new_name)))
    return planned


def describe(label: str, source: Path, target: Path, note: str = "") -> str:
    """Format one output line: a fixed-width label, then old -> new."""
    line = f"{label:<{LABEL_WIDTH}}  {source.name} -> {target.name}"
    return f"{line} {note}" if note else line


def main(argv: list[str] | None = None) -> int:
    """Preview or apply the planned renames. Return an exit code."""
    args = build_parser().parse_args(argv)

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    planned = plan_renames(args.directory, args.old, args.new, args.pattern)
    renamed = 0
    skipped = 0

    for source, target in planned:
        if target.exists():
            print(describe("SKIP", source, target, "(target exists)"))
            skipped += 1
            continue
        print(describe("RENAMED" if args.apply else "DRY-RUN", source, target))
        if args.apply:
            source.rename(target)
        renamed += 1

    verb = "renamed" if args.apply else "would be renamed"
    print(f"{renamed} file(s) {verb}, {skipped} skipped")
    if not args.apply:
        print("Re-run with --apply to make these changes.")
    return 1 if skipped else 0


# --------------------------------------------------------------------------- #
# The headless demo — the sandbox from the exercise page, built in a temp
# directory and deleted when the ``with`` block ends. Your own file has no
# demo; you point it at a sandbox you built yourself.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Build the exercise sandbox, drive the renamer over it, then tidy up."""
    print("Bulk Rename — proven headless on a sandbox this file builds and deletes.")
    print()
    with tempfile.TemporaryDirectory(prefix="rename-sandbox-") as tmp:
        sandbox = Path(tmp)
        for name in ("budget draft.txt", "report draft.txt",
                     "report final.txt", "photo.png"):
            (sandbox / name).write_text("", encoding="utf-8")
        (sandbox / "old drafts").mkdir()  # a directory whose name contains 'draft'
        target = str(sandbox)

        print("Preview (the default — nothing on disk is touched):")
        code = main([target, "draft", "final"])
        print(f"[exit {code}]")
        print()

        print("Apply (only --apply moves a byte):")
        code = main([target, "draft", "final", "--apply"])
        print(f"[exit {code}]")
        print()

        print("Apply again — idempotent, the collision is still refused:")
        code = main([target, "draft", "final", "--apply"])
        print(f"[exit {code}]")


if __name__ == "__main__":
    demo()
