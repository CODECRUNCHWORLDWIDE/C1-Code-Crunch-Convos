"""Homework 1 — Word-count CLI.

Counts whitespace-separated words in each file named on the command line,
prints a right-aligned table and a grand total. Files that cannot be read are
reported as WARNINGs on stderr and do not stop the run.

    python word_count.py essay.txt notes.txt missing.txt

Run it with no arguments and it builds its own sample files in a scratch
folder first, so the download works from a clean checkout with nothing set up.

Save your own copy as ``word_count.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import logging
import os
import sys
import tempfile
from pathlib import Path

log = logging.getLogger("word_count")


def count_words(path: Path) -> int:
    """Return the number of whitespace-separated words in the file at *path*.

    Sums per line rather than splitting the whole file at once, so memory stays
    flat on a large file. The result is identical either way: ``str.split()``
    with no argument treats a run of any whitespace -- including the newline --
    as one separator, so no word can straddle a line boundary.

    Args:
        path: The file to count.

    Returns:
        The number of words in the file.
    """
    total = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            total += len(line.split())
    return total


def report(paths: list[Path]) -> int:
    """Print one line per readable file, then the total. Return the total.

    Args:
        paths: The files to count, in the order given on the command line.

    Returns:
        The sum of the counts of the files that could actually be read.
    """
    grand_total = 0
    for path in paths:
        try:
            words = count_words(path)
        except (OSError, UnicodeDecodeError) as e:
            log.warning("could not read %s: %s", path, type(e).__name__)
            continue
        print(f"{words:>6}  {path}")
        grand_total += words
    print("-----")
    print(f"{grand_total:>6}  total")
    return grand_total


def _demo() -> int:
    """Build two sample files in a scratch folder and report on them.

    The scratch folder is a temporary directory this function creates and
    deletes, so the demo needs no data placed by anybody else and leaves
    nothing behind. It changes into that folder first, which is why the table
    shows plain names like ``essay.txt`` instead of a long temporary path.

    Returns:
        Always 0. The demo cannot fail in a way the caller can act on.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="word_count_") as scratch:
        try:
            os.chdir(scratch)
            Path("essay.txt").write_text(
                " ".join(f"word{i % 17}" for i in range(124)) + "\n",
                encoding="utf-8",
            )
            Path("notes.txt").write_text(
                "\n".join(" ".join(f"n{i}" for i in range(7)) for _ in range(6))
                + "\n",
                encoding="utf-8",
            )
            report([Path("essay.txt"), Path("notes.txt"), Path("missing.txt")])
        finally:
            # Leave the scratch folder before it is deleted. A process whose
            # working directory has been removed is a confusing thing to be.
            os.chdir(home)
    return 0


def main(argv: list[str]) -> int:
    """Count the files named in *argv*, or run the demo when there are none.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The process exit code.
    """
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    if not argv:
        return _demo()
    report([Path(a) for a in argv])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
