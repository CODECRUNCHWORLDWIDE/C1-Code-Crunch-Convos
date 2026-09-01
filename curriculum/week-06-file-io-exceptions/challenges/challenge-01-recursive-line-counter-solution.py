"""challenge-01-recursive-line-counter-solution.py — count lines of Python in a tree.

Walks a directory recursively, counts the non-blank lines in every .py file it
finds, and prints a sorted table plus a grand total. Files it cannot read are
logged at WARNING level and skipped; one unreadable file never stops the walk.

Give it a directory and it counts that directory::

    python challenge-01-recursive-line-counter-solution.py ../some/folder

Give it nothing and it builds a small demo tree in a throwaway temporary
directory first — four files, one of them deliberately not UTF-8 — and counts
that. The demo exists so the download prints something real on a machine with
nothing set up, and so the UnicodeDecodeError branch is visible rather than
merely claimed.

The table goes to stdout and the warnings go to stderr, so
`python challenge-01-recursive-line-counter-solution.py src > report.txt` puts
the counts in the file and leaves the warnings on your screen.
"""

from __future__ import annotations

import logging
import sys
import tempfile
from pathlib import Path

log = logging.getLogger("linecount")


def count_lines(path: Path) -> int:
    """Return the number of non-blank lines in the UTF-8 text file at *path*.

    Iterates the file object rather than calling ``.readlines()`` so that memory
    stays flat no matter how big the file is.
    """
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                total += 1
    return total


def count_python_lines(root: Path) -> dict[Path, int]:
    """Return a dict mapping each .py file under *root* to its line count.

    Files that cannot be read are logged at WARNING level and left out of the
    result. The walk never aborts because of one bad file.
    """
    counts: dict[Path, int] = {}
    for path in root.rglob("*.py"):
        if not path.is_file():
            # rglob matches directories too; a directory literally named
            # "vendor.py" is rare but it exists, and open() would raise
            # IsADirectoryError on POSIX / PermissionError on Windows.
            continue
        try:
            counts[path] = count_lines(path)
        except PermissionError:
            log.warning("skipping %s: permission denied", path)
        except UnicodeDecodeError as e:
            log.warning("skipping %s: not valid UTF-8 (%s)", path, e.reason)
        except OSError as e:
            log.warning("skipping %s: %s", path, e.strerror or e)
    return counts


def print_report(root: Path, counts: dict[Path, int]) -> None:
    """Print a sorted table of files and line counts, then the grand total."""
    for path in sorted(counts):
        relative = path.relative_to(root).as_posix()
        print(f"{counts[path]:>5} {relative}", flush=True)
    print("-----")
    print(f"{sum(counts.values()):>5} total")


def build_demo_tree(root: Path) -> Path:
    """Create the demo tree under *root* and return the folder to count."""
    package = root / "pkg"
    package.mkdir(parents=True, exist_ok=True)
    (root / "app.py").write_text(
        'import os\n\n\ndef main():\n    print("hi")\n', encoding="utf-8"
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "util.py").write_text(
        "def a():\n    return 1\n\n\ndef b():\n    return 2\n", encoding="utf-8"
    )
    # Latin-1 bytes in a .py file: the operating system hands them over
    # happily and Python's UTF-8 decoder refuses them.
    (package / "legacy.py").write_bytes("# café\nx = 1\n".encode("latin-1"))
    return root


def main() -> None:
    """Count the directory named on the command line, or the demo tree."""
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        print_report(target, count_python_lines(target))
        return
    with tempfile.TemporaryDirectory() as workspace:
        target = build_demo_tree(Path(workspace) / "demo")
        print_report(target, count_python_lines(target))


if __name__ == "__main__":
    main()
