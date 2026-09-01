"""exercise-01-read-write-solution.py — copy a text file line by line, cleaning as you go.

Reads a sign-up sheet, normalises every address, and writes the result to a
second file. Blank and whitespace-only lines are dropped. The original is never
touched.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact sign-up sheet the page
gives you, so the download runs on any machine with nothing set up beforehand.
The temporary directory is deleted on the way out; ``clean`` and ``copy_clean``
below are the whole exercise and know nothing about it.

Run it with::

    python exercise-01-read-write-solution.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

#: The sign-up sheet exactly as the exercise page gives it. Line 2 starts with
#: two spaces and line 4 is empty; those two lines are the exercise.
SAMPLE_SIGNUPS = (
    "Ada.Lovelace@Example.ORG\n"
    "  grace.hopper@example.org\n"
    "KATHERINE.JOHNSON@Example.org\n"
    "\n"
    "alan.turing@EXAMPLE.org\n"
)


def clean(raw_line: str) -> str:
    """Return *raw_line* trimmed of surrounding whitespace and lowercased.

    An empty return value means the line held nothing but whitespace.
    """
    return raw_line.strip().lower()


def copy_clean(source: Path, target: Path) -> tuple[int, int]:
    """Copy *source* to *target* one line at a time, cleaning each line.

    Returns:
        A ``(lines_read, addresses_written)`` pair.
    """
    lines_read = 0
    addresses_written = 0
    with source.open("r", encoding="utf-8") as src, \
         target.open("w", encoding="utf-8") as dst:
        for raw_line in src:
            lines_read += 1
            address = clean(raw_line)
            if not address:
                continue
            dst.write(address + "\n")
            addresses_written += 1
    return lines_read, addresses_written


def build_sample(folder: Path) -> Path:
    """Write the sample sign-up sheet into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "signups.txt"
    path.write_text(SAMPLE_SIGNUPS, encoding="utf-8")
    return path


def main() -> None:
    """Build the sample data, run the copy, and report what happened."""
    with tempfile.TemporaryDirectory() as workspace:
        data = Path(workspace) / "data"
        source = build_sample(data)
        target = data / "signups-clean.txt"

        read, written = copy_clean(source, target)
        print(f"Read {read} lines from {source.name}")
        print(f"Wrote {written} addresses to {target.name}")

        print()
        print(f"--- {target.name} ---")
        print(target.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
