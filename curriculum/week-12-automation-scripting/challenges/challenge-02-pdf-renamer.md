# Challenge 02 — PDF renamer

> **Topic:** `pathlib` + `re` + an optional PDF library — safe, batch, dry-run-first
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Medium
> **Target time:** 1.5–3 hours
> **Why this one:** it is the bulk renamer from Exercise 2 grown up — two naming strategies, a real third-party library, and the same non-negotiable habit underneath: preview by default, never clobber. Rename a folder full of `scan_001.pdf` and `Document(7).pdf` into `2024-04-15_Invoice_AcmeCorp.pdf` and you will actually use this.

## The Brief

Rename a folder of poorly-named PDFs into something searchable. You build the
new name one of two ways, and you may use both:

- **`--regex PATTERN`** matches the pattern against the *original filename* and
  rebuilds the name from its named groups. On
  `Invoice_AcmeCorp_2024-04-15.pdf`, a pattern with `vendor` and `date` groups
  yields `2024-04-15_AcmeCorp.pdf` — date first, so the folder sorts
  chronologically.
- **`--from-title`** reads the document title out of the PDF's metadata (using
  [`pypdf`](https://pypdf.readthedocs.io/)), falling back to the first non-empty
  line of page 1, then slugifies it.

Nothing is renamed unless you pass `--apply`; the default is a dry run. A file
whose target already exists is skipped with a warning, never overwritten.

## Starter

`--regex` mode is pure standard library. `--from-title` needs `pip install pypdf`.

```python
"""pdf_renamer.py — rename a folder of PDFs from a filename regex or the title.

    python pdf_renamer.py DIR [--from-title] [--regex PATTERN] [--apply]
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path


def slugify(text: str) -> str:
    """Whitespace -> '_', drop anything not [A-Za-z0-9_.-], cap at 60."""
    ...


def derive_name_from_regex(original: str, pattern: re.Pattern[str]) -> str | None:
    """Rebuild a filename from the pattern's named groups, or None if no match."""
    # TODO: pattern.match(original); pull out `date` first, join the rest with _
    ...


def derive_name_from_title(path: Path) -> str | None:
    """Slugified PDF title, falling back to the first text line of page 1."""
    # TODO: import pypdf lazily; read metadata.title, then page-1 text
    ...


def main(argv: list[str] | None = None) -> int:
    """Preview or apply the renames. Return an exit code."""
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. **CLI** with a positional `DIR`, plus `--from-title`, `--regex PATTERN`, and
   `--apply` (dry-run is the default).
2. **Regex mode** uses named groups. Document the rule you build the new name
   from — this answer puts the `date` group first, then every other non-empty
   group in pattern order, joined by `_`, slugified, capped at 60, plus `.pdf`.
3. **Title mode** reads `pypdf`'s `metadata.title`, falls back to the first
   non-empty line of page 1, slugifies, and truncates to 60 characters.
4. **Refuse to overwrite** an existing target — skip and log a warning.
5. **Exit codes**: 0 on success (including "nothing matched"), 1 on misuse
   (neither mode given, or `DIR` is not a directory), 2 on an argparse error.
6. Use `pathlib.Path`, use `logging`, and type-hint every function.

## Constraints

- **Dry-run is the default; `--apply` is the only write path.** Same rule as the
  bulk renamer, same reason: a rename has no undo, so the safe thing is the
  default.
- **A dry run must predict the real run exactly.** Two PDFs with the same title
  both want one name; in a preview nothing is created, so `target.exists()` is
  `False` for both. Track the names this run has already claimed in a `planned`
  set, or the preview promises two renames and `--apply` performs one.
- **Compile the regex with a `type=` wrapper.** `re.error` is *not* a subclass
  of `ValueError`, so `type=re.compile` hands the user a traceback for a typo'd
  pattern instead of a clean usage error.
- **`derive_name_from_title` must survive a corrupt PDF.** `pypdf` raises a zoo
  of parse errors; a batch renamer that dies on file 40 of 300 is useless. Catch
  broadly *there and only there*, log the file, and move on.
- **Slugify strips trailing separators.** A title ending in a full stop must not
  produce `Report..pdf`. Strip `_.-` from both ends, after truncating.

## Expected output

The shipped answer, [`challenge-02-pdf-renamer-solution.py`](./challenge-02-pdf-renamer-solution.py),
drives the pure-standard-library regex path over sandboxes it builds in temp
directories — a preview, an apply, an idempotent second apply, and two files
that want the same target so the overwrite refusal shows. `--from-title` needs
`pypdf` and real PDFs, so the page walks it below rather than the demo. Real
captured output:

```text
$ python challenge-02-pdf-renamer-solution.py
PDF Renamer — regex mode, driven headless on sandboxes this file builds.

Preview (the default — nothing is renamed):
INFO    would rename Invoice_AcmeCorp_2024-04-15.pdf -> 2024-04-15_AcmeCorp.pdf
INFO    would rename Invoice_Globex_2024-05-02.pdf -> 2024-05-02_Globex.pdf
INFO    would rename Invoice_Initech_2024-06-30.pdf -> 2024-06-30_Initech.pdf
INFO    would rename 3 file(s)
[exit 0]

Apply (date-first, so the folder sorts chronologically):
INFO    renamed Invoice_AcmeCorp_2024-04-15.pdf -> 2024-04-15_AcmeCorp.pdf
INFO    renamed Invoice_Globex_2024-05-02.pdf -> 2024-05-02_Globex.pdf
INFO    renamed Invoice_Initech_2024-06-30.pdf -> 2024-06-30_Initech.pdf
INFO    renamed 3 file(s)
[exit 0]

Apply again — nothing left to match:
INFO    renamed 0 file(s)
[exit 0]

Two files want the same target — the second is refused, and the
dry run agrees with the apply because a 'planned' set reserves the name:
INFO    would rename 2024-01-01_budget.pdf -> 2024-01-01.pdf
WARNING skip 2024-01-01_report.pdf -> 2024-01-01.pdf (target exists)
INFO    would rename 1 file(s)
[exit 0]
INFO    renamed 2024-01-01_budget.pdf -> 2024-01-01.pdf
WARNING skip 2024-01-01_report.pdf -> 2024-01-01.pdf (target exists)
INFO    renamed 1 file(s)
[exit 0]
```

The dry run and the apply agree on the collision — one renamed, one refused —
because a `planned` set reserves each target name the moment it is claimed.

## Steps

1. Write `slugify` and `derive_name_from_regex`, and test them on strings, no
   files needed.
2. Build a folder of sample PDFs whose names match your pattern, and get the
   dry run printing the right new names.
3. Add the `planned` set and the `target.exists()` guard; confirm a preview and
   an `--apply` agree when two files collide.
4. Wire up `--apply` and run it. Re-run to confirm it is idempotent.
5. Add `--from-title` with a lazy `pypdf` import, and try it on a PDF that has a
   real metadata title.
6. Point it at a scanned PDF (an image, no text layer) and confirm it is skipped
   cleanly, not crashed on.

## The Solution

The shipped file is a complete renamer — `slugify`, `derive_name_from_regex`,
`derive_name_from_title`, `plan_rename`, `rename_all`, `compiled_regex`, the
parser, `main` — with a `demo()` that exercises the regex path on temp
sandboxes. `--from-title` is in the file (pypdf is imported only when it runs)
and the page walks it below.

```python
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
```

**The naming rule, stated once so your README can quote it.** The `date` group,
if present, comes first; every other named group with a non-empty value follows
in pattern order, joined by `_`; the result is slugified, capped at 60, and gets
`.pdf`. So `Invoice_AcmeCorp_2024-04-15.pdf` becomes `2024-04-15_AcmeCorp.pdf` —
which sorts chronologically in any file browser, the entire point of the
exercise.

**`plan_rename` is the seam.** It is a pure decision: given a path and the two
modes, what should this file be called? It touches nothing and returns `None`
for "leave it alone". Every policy question — dry run or not, does the target
exist, does the name actually differ — lives in `rename_all` above it. That is
why `--apply` was three lines to add.

**`planned` keeps the dry run honest.** Two different PDFs with the same title
both want one name. In dry-run mode `target.exists()` is `False` for both,
because nothing is created — so without the `planned` set the preview promises
two renames and `--apply` then performs one and warns about the other. A preview
that disagrees with the real run is worse than no preview, because you stopped
reading it. (Same problem, same fix, as the `reserved` set in the mini-project's
`unique_path()`.)

**`compiled_regex` exists because of one inheritance fact.** `argparse` catches
`ArgumentTypeError`, `TypeError`, and `ValueError` from a `type=` callable and
turns them into a clean usage error. `re.error` inherits from `Exception`
directly, so `type=re.compile` would hand your user a traceback for a typo'd
pattern. Wrapping it costs four lines and turns that into
`error: argument --regex: invalid regex: ...`.

**Two levels of "skip", logged differently.** "No rule matched" is normal and
goes to DEBUG, so a run over 300 PDFs where 12 match prints 12 lines, not 300.
"Target exists" is a WARNING, because that one is a real collision you probably
want to resolve by hand. Choosing the level is what makes `-v` useful rather
than decorative.

**The `except Exception` in `derive_name_from_title` is deliberate, and the only
one in the file.** `pypdf` raises `PdfReadError`, `KeyError`, `struct.error`,
and more depending on how a PDF is malformed, and new versions add to the list.
A batch renamer that dies on one corrupt scan out of hundreds is useless; the
type and message are logged so you can still see what happened.

## Download and run

Download
[challenge-02-pdf-renamer-solution.py](./challenge-02-pdf-renamer-solution.py)
and run it:

```bash
python challenge-02-pdf-renamer-solution.py
```

The demo drives the regex path only, which is pure standard library, so it needs
no install and no PDFs. For `--from-title`, `pip install pypdf` and point the
script at a folder of real PDFs.

## Common bugs to catch

- **A traceback instead of a usage error on a bad pattern.** You used
  `type=re.compile`. `re.error` is not a `ValueError`, so argparse does not
  catch it. Wrap compilation in a `type=` callable that re-raises
  `argparse.ArgumentTypeError`.
- **The preview and the apply disagree on a collision.** You checked only
  `target.exists()`. In a dry run nothing is created, so two files claiming the
  same name both pass. Add a `planned` set that reserves each target.
- **`Quarterly_Report..pdf`.** Your slugify truncated but did not strip the
  trailing separator. Strip `_.-` from both ends, after the truncation.
- **The whole run dies on one file.** A scanned PDF is an image with no text
  layer: `extract_text()` returns `""`, `metadata.title` is `None`, and some
  corrupt files raise. Catch broadly in `derive_name_from_title` and skip.
- **`--from-title` renames nothing on your scans and you assume it is broken.**
  It is not — a flatbed scan has no text to read. That is a job for OCR, not
  more parsing code.

## Under the hood

<details>
<summary>Under the hood — why `Path.rename` here and `shutil.move` in the mini-project</summary>

Both files sit in the same directory, so a rename here is a same-filesystem
operation: `Path.rename` maps straight onto the operating system's `rename`
syscall, which just rewrites a directory entry and is atomic on POSIX — the file
is either at the old name or the new one, never in between. That is the exact,
cheapest operation for the job.

The mini-project's file organizer uses `shutil.move` instead, and the difference
is not arbitrary. `shutil.move` is the right call when the destination *might* be
on a different volume — moving from `~/Downloads` to a folder that could,
in principle, be a mounted drive. Across filesystems there is no atomic rename:
the bytes have to be copied and the original deleted, and `shutil.move` handles
that fallback for you while `Path.rename` would raise `OSError: Invalid
cross-device link`. One more caveat worth carrying: on POSIX, `Path.rename`
silently overwrites an existing target, which is precisely why the
`target.exists()` check in this challenge is a hard guard and not a nicety —
the safety cannot be delegated to the syscall.

</details>

## Acceptance checklist

- [ ] Dry-run is the default; `--apply` is the only path that renames.
- [ ] Regex mode rebuilds names date-first from named groups.
- [ ] Title mode works on a PDF with a metadata title, and skips one with no
      text cleanly.
- [ ] A target that already exists is refused with a warning, in both the
      preview and the apply.
- [ ] A typo'd `--regex` gives a usage error and exit 2, not a traceback.
- [ ] Uses `logging` and `pathlib`, with type hints throughout.
- [ ] Committed to Git with a message like
      `Add Week 12 challenge 2: PDF renamer`.

## Stretch

- **OCR fallback**: if `pypdf` finds no text, run `ocrmypdf` over the file via
  `subprocess` (list args, `check=True`, a `timeout`) and retry the title.
- **Date inference**: when the name has no date, take one from
  `Path.stat().st_mtime`.
- **CSV log**: append `original,new,timestamp` for every rename, for an audit
  trail.
- **Undo file**: write a JSON journal that reverses the whole run in one
  command — replayed in reverse, because one rename may free a name a later one
  took.

That is the whole challenge set. Next is the week's capstone:
[Mini-Project — File Organizer Bot](../mini-project/README.md).
