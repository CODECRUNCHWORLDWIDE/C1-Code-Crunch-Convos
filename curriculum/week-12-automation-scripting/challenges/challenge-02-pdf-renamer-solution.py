"""challenge-02-pdf-renamer-solution.py — the PDF renamer, proven headless.

The challenge answer renames PDFs two ways: from a regex over the filename, or
from the document's title (which needs pypdf). Your own pdf_renamer.py ends in
``raise SystemExit(main())`` and you point it at a real folder.

A published answer must run with no third-party install and no PDFs lying
around, so this file's demo drives the pure-standard-library regex path over a
sandbox it builds in a temp directory: a preview, an apply, an idempotent second
apply, and two files that want the same target so the overwrite refusal shows.
The renamer being tested is identical either way. The --from-title path is right
here in the file — pypdf is imported only when that path runs — and the page
walks it with real PDFs.

Run it with::

    python challenge-02-pdf-renamer-solution.py
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import tempfile
from pathlib import Path

__version__ = "1.0.0"

MAX_STEM = 60

LOGGER = logging.getLogger("pdf_renamer")


def slugify(text: str) -> str:
    """Whitespace -> '_', drop anything that is not [A-Za-z0-9_.-], cap at 60.

    The trailing strip also removes '.', which stops a title ending in a full
    stop from producing 'Report..pdf'.
    """
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"[^A-Za-z0-9_.-]", "", text)
    return text[:MAX_STEM].strip("_.-")


def derive_name_from_regex(original: str, pattern: re.Pattern[str]) -> str | None:
    """Rebuild a filename from the pattern's named groups, or None if no match."""
    match = pattern.match(original)
    if not match:
        return None
    groups = match.groupdict()
    if not groups:
        LOGGER.warning("pattern has no named groups; nothing to build a name from")
        return None
    date = groups.get("date") or ""
    rest = "_".join(slugify(value) for key, value in groups.items()
                    if key != "date" and value)
    stem = f"{date}_{rest}" if date and rest else (date or rest)
    stem = stem[:MAX_STEM].strip("_.-")
    return f"{stem}.pdf" if stem else None


def derive_name_from_title(path: Path) -> str | None:
    """Slugified PDF title, falling back to the first text line of page 1."""
    try:
        from pypdf import PdfReader
    except ImportError:
        LOGGER.error("pypdf is required for --from-title. pip install pypdf")
        return None

    try:
        reader = PdfReader(path)
        title = (reader.metadata.title or "").strip() if reader.metadata else ""
        if not title and reader.pages:
            text = reader.pages[0].extract_text() or ""
            for line in text.splitlines():
                if line.strip():
                    title = line.strip()
                    break
    except Exception as exc:  # pypdf raises a zoo of parse errors
        LOGGER.warning("cannot read %s: %s: %s", path.name, type(exc).__name__, exc)
        return None

    slug = slugify(title)
    return f"{slug}.pdf" if slug else None


def pdf_files(directory: Path) -> list[Path]:
    """Every regular .pdf file directly inside *directory*, case-insensitively."""
    return sorted(p for p in directory.iterdir()
                  if p.is_file() and p.suffix.lower() == ".pdf")


def plan_rename(path: Path, pattern: re.Pattern[str] | None,
                from_title: bool) -> str | None:
    """The new filename for *path*, or None to leave it alone."""
    if pattern is not None:
        new_name = derive_name_from_regex(path.name, pattern)
        if new_name:
            return new_name
    if from_title:
        return derive_name_from_title(path)
    return None


def rename_all(directory: Path, pattern: re.Pattern[str] | None,
               from_title: bool, apply: bool) -> int:
    """Rename (or preview) every PDF in *directory*. Return how many were acted on.

    ``planned`` holds the names this run has already promised to a file. Without
    it, a dry run would happily print two files onto the same target name --
    ``target.exists()`` is False for both, because in a dry run nothing is
    created. That would make the preview disagree with what --apply does.
    """
    planned: set[Path] = set()
    acted = 0
    for path in pdf_files(directory):
        new_name = plan_rename(path, pattern, from_title)
        if new_name is None:
            LOGGER.debug("skip %s (no rule matched)", path.name)
            continue
        if new_name == path.name:
            LOGGER.debug("skip %s (already named correctly)", path.name)
            continue

        target = path.with_name(new_name)
        if target.exists() or target in planned:
            LOGGER.warning("skip %s -> %s (target exists)", path.name, new_name)
            continue
        planned.add(target)

        if apply:
            try:
                path.rename(target)
            except OSError as exc:
                LOGGER.error("could not rename %s: %s", path.name, exc)
                continue
            LOGGER.info("renamed %s -> %s", path.name, new_name)
        else:
            LOGGER.info("would rename %s -> %s", path.name, new_name)
        acted += 1
    return acted


def compiled_regex(value: str) -> re.Pattern[str]:
    """argparse type: compile the pattern, or fail with a clean message.

    `re.error` is NOT a subclass of ValueError, so without this wrapper argparse
    lets it escape as a traceback instead of a usage error.
    """
    try:
        return re.compile(value)
    except re.error as exc:
        raise argparse.ArgumentTypeError(f"invalid regex: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf_renamer",
        description="Rename PDFs from a filename regex or from the document title.",
    )
    parser.add_argument("directory", metavar="DIR", type=Path,
                        help="Folder containing the PDFs.")
    parser.add_argument("--from-title", action="store_true",
                        help="Build the name from the PDF title (needs pypdf).")
    parser.add_argument("--regex", type=compiled_regex, metavar="PATTERN",
                        help="Regex with named groups, matched against the filename.")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename. Without it, dry-run.")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Show the files that were skipped too.")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    return parser


def configure_logging(verbosity: int) -> None:
    """Root at WARNING so pypdf's own chatter stays out of -v output."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)-7s %(message)s",
        stream=sys.stdout,
    )
    LOGGER.setLevel(logging.DEBUG if verbosity else logging.INFO)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.verbose)

    if not args.regex and not args.from_title:
        print("error: give --regex PATTERN, --from-title, or both", file=sys.stderr)
        return 1
    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    acted = rename_all(args.directory, args.regex, args.from_title, args.apply)
    verb = "renamed" if args.apply else "would rename"
    LOGGER.info("%s %d file(s)", verb, acted)
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — the regex path over a sandbox this file builds and
# deletes. Your own file has no demo; you point it at a real folder.
# --------------------------------------------------------------------------- #


def build_pdfs(directory: Path, names: tuple[str, ...]) -> None:
    """Drop empty .pdf files; regex mode reads only the name, never the bytes."""
    for name in names:
        (directory / name).write_bytes(b"%PDF-1.4\n%%EOF\n")


def demo() -> None:
    """Drive the regex path: preview, apply, idempotent apply, then a collision."""
    print("PDF Renamer — regex mode, driven headless on sandboxes this file builds.")
    print()

    invoice = r"Invoice_(?P<vendor>[A-Za-z]+)_(?P<date>\d{4}-\d{2}-\d{2})\.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        build_pdfs(folder, (
            "Invoice_AcmeCorp_2024-04-15.pdf",
            "Invoice_Globex_2024-05-02.pdf",
            "Invoice_Initech_2024-06-30.pdf",
            "scan_001.pdf",       # no regex match, left alone
            "Document(7).pdf",    # no regex match, left alone
        ))
        d = str(folder)

        print("Preview (the default — nothing is renamed):")
        print(f"[exit {main([d, '--regex', invoice])}]")
        print()
        print("Apply (date-first, so the folder sorts chronologically):")
        print(f"[exit {main([d, '--regex', invoice, '--apply'])}]")
        print()
        print("Apply again — nothing left to match:")
        print(f"[exit {main([d, '--regex', invoice, '--apply'])}]")
        print()

    date_first = r"(?P<date>\d{4}-\d{2}-\d{2})_[a-z]+\.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        build_pdfs(folder, ("2024-01-01_budget.pdf", "2024-01-01_report.pdf"))
        d = str(folder)
        print("Two files want the same target — the second is refused, and the")
        print("dry run agrees with the apply because a 'planned' set reserves the name:")
        print(f"[exit {main([d, '--regex', date_first])}]")
        print(f"[exit {main([d, '--regex', date_first, '--apply'])}]")


if __name__ == "__main__":
    demo()
