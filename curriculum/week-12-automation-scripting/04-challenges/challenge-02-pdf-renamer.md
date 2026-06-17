# Challenge 02 — PDF renamer

Rename a folder full of poorly-named PDFs (think `scan_001.pdf`, `Document(7).pdf`, …) into something searchable like `2024-04-15_Invoice_AcmeCorp.pdf`.

You'll combine `pathlib`, `re`, and an optional PDF library to extract the title from the document itself.

---

## Requirements

### Functional

1. **CLI** built with `argparse`:

   ```text
   python pdf_renamer.py DIR [--from-title] [--regex PATTERN] [--apply]
   ```

   - `DIR`: folder containing PDFs.
   - `--from-title`: read the title from PDF metadata (or the first non-empty line of the first page).
   - `--regex PATTERN`: a Python regex that, when matched against the **original filename**, produces a new filename via its named groups. See "Regex mode" below.
   - `--apply`: actually rename. Otherwise dry-run (default).

2. **Regex mode**: use named groups in the pattern. Example:

   ```text
   --regex 'Invoice_(?P<vendor>[A-Za-z]+)_(?P<date>\d{4}-\d{2}-\d{2})\.pdf'
   ```

   On a file named `Invoice_AcmeCorp_2024-04-15.pdf`, the new name should be derived from the captured groups — at minimum, format `{date}_{vendor}.pdf`. (Document this clearly in your README.)

3. **Title mode** (`--from-title`): use [`pypdf`](https://pypdf.readthedocs.io/) (`pip install pypdf`) to extract the document title. If the title is empty, fall back to the first non-empty text line of page 1.

   - Slugify the title: replace runs of whitespace with `_`, strip non-alphanumeric characters except `_`, `-`, `.`.
   - Truncate to 60 characters.

4. **Refuse to overwrite** an existing file — skip and log a warning.

5. **Exit codes**: 0 on success, 1 on misuse (e.g. neither mode given), 2 on argparse error (default).

### Non-functional

- Use `pathlib.Path`.
- Use the `logging` module.
- Use type hints throughout.

---

## Suggested skeleton

```python
import argparse
import logging
import re
import sys
from pathlib import Path


def derive_name_from_regex(original: str, pattern: re.Pattern) -> str | None:
    match = pattern.match(original)
    if not match:
        return None
    groups = match.groupdict()
    # Order-of-preference template; customize for your use case
    date = groups.get("date", "")
    rest = "_".join(v for k, v in groups.items() if k != "date" and v)
    return f"{date}_{rest}.pdf" if date else f"{rest}.pdf"


def derive_name_from_title(path: Path) -> str | None:
    try:
        from pypdf import PdfReader
    except ImportError:
        logging.error("pypdf is required for --from-title. pip install pypdf")
        return None
    reader = PdfReader(path)
    title = (reader.metadata.title or "").strip() if reader.metadata else ""
    if not title and reader.pages:
        text = reader.pages[0].extract_text() or ""
        for line in text.splitlines():
            if line.strip():
                title = line.strip()
                break
    return slugify(title) + ".pdf" if title else None


def slugify(text: str) -> str:
    import re as _re
    text = _re.sub(r"\s+", "_", text)
    text = _re.sub(r"[^A-Za-z0-9_.-]", "", text)
    return text[:60].strip("_")


def main(argv: list[str] | None = None) -> int:
    ...
```

---

## Stretch goals

1. **OCR fallback**: if `pypdf` returns no text (scanned PDF), call `ocrmypdf` via `subprocess` to OCR it, then retry.
2. **Date inference**: if no date is in the filename, look at `Path.stat().st_mtime`.
3. **CSV log**: append every rename to a CSV (`original,new,timestamp`) for audit.
4. **Undo file**: write a separate JSON that lets you reverse all renames in one command.

---

## Manual test plan

1. Create a folder with 5 sample PDFs named to match a regex.
2. Run with `--regex ...` and confirm the dry-run output looks right.
3. Run again with `--apply` and verify files are renamed.
4. Re-run the same command — should report "no matching files" or "would skip (target exists)".
5. Try `--from-title` against a PDF with a real title in its metadata.

---

## Rubric (10 pts)

| Category                                  | Pts |
|-------------------------------------------|-----|
| Dry-run default + `--apply` works         | 2   |
| Regex mode works with named groups        | 2   |
| Title mode works (or graceful skip)       | 2   |
| Refuses to overwrite existing target      | 1   |
| Uses `logging` and `pathlib`              | 1   |
| Clear README/help text                    | 1   |
| Type hints + structured `main()`          | 1   |
