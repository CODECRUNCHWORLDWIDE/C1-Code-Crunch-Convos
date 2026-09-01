"""Homework 3 — JSON pretty-printer.

Reads a JSON document and rewrites it with indent=2 and sorted keys. On a
parse error it emits exactly one diagnostic line and exits 1, leaving the
output file untouched.

    python json_pretty.py messy.json clean.json

Run it with no arguments and it builds its own good and bad input files in a
scratch folder first, so the download works from a clean checkout with nothing
set up.

Save your own copy as ``json_pretty.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import tempfile
from pathlib import Path

# "%(levelname)s  %(message)s" -- deliberately NOT the %(levelname)-8s format
# used elsewhere this week, because the spec's example line is
#     ERROR  bad.json:1:17  Expecting property name enclosed in double quotes
# with exactly two spaces after the level.
log = logging.getLogger("json_pretty")


def pretty(src: Path, dst: Path) -> int:
    """Rewrite *src* into *dst*, pretty-printed. Return a process exit code.

    Parsing happens in full before *dst* is opened, so a bad input never
    truncates a good output file.

    Args:
        src: The JSON file to read.
        dst: The file to write the pretty-printed version to.

    Returns:
        0 on success, 1 if the input could not be read or parsed.
    """
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except FileNotFoundError:
        log.error("%s: no such file", src)
        return 1
    except UnicodeDecodeError as e:
        log.error("%s: not valid UTF-8 (%s)", src, e.reason)
        return 1
    except json.JSONDecodeError as e:
        log.error("%s:%d:%d  %s", src, e.lineno, e.colno, e.msg)
        return 1

    text = json.dumps(data, indent=2, sort_keys=True)
    dst.write_text(text + "\n", encoding="utf-8")
    return 0


def _demo() -> int:
    """Pretty-print one good file and one broken one in a scratch folder.

    The scratch folder is a temporary directory this function makes and
    deletes, so the demo needs nothing placed by hand and leaves nothing
    behind. It changes into that folder first so the diagnostic line names
    ``bad.json`` rather than a long temporary path.

    Returns:
        Always 0. Both demonstrated outcomes are the intended ones.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="json_pretty_") as scratch:
        try:
            os.chdir(scratch)
            Path("messy.json").write_text(
                '{"name":"Alice","tags":["b","a"],"active":true,'
                '"age":30,"manager":null}\n',
                encoding="utf-8",
            )
            Path("bad.json").write_text('{"name": "Alice",}\n', encoding="utf-8")

            code = pretty(Path("messy.json"), Path("clean.json"))
            print(f"messy.json -> clean.json: exit {code}")
            print(Path("clean.json").read_text(encoding="utf-8"), end="")

            code = pretty(Path("bad.json"), Path("out.json"))
            print(f"bad.json -> out.json: exit {code}")
            print(f"out.json exists: {Path('out.json').exists()}")
        finally:
            os.chdir(home)
    return 0


def main(argv: list[str]) -> int:
    """Pretty-print the files named in *argv*, or run the demo when empty.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The process exit code.
    """
    logging.basicConfig(format="%(levelname)s  %(message)s")
    if not argv:
        return _demo()
    if len(argv) != 2:
        print("usage: json_pretty.py INPUT.json OUTPUT.json", file=sys.stderr)
        return 2
    return pretty(Path(argv[0]), Path(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
