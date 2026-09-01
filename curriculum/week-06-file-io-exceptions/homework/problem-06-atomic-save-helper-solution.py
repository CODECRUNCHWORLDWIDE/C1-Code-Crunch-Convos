"""Homework 6 — atomic-save helper.

`atomic_write_text` writes to a sibling temp file and renames it over the
target, so a reader sees either the whole old file or the whole new one --
never a half-written one -- and a failure mid-write leaves the original intact.

    python atomic.py

The demonstration runs in a scratch folder it creates and deletes, so the
download works from a clean checkout and leaves nothing behind.

Save your own copy as ``atomic.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import logging
import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

log = logging.getLogger("atomic")


def atomic_write_chunks(
    path: Path, chunks: Iterable[str], encoding: str = "utf-8"
) -> None:
    """Write the concatenation of *chunks* to *path* atomically.

    The general form. `atomic_write_text` is the one-string case. Taking an
    iterable means the caller can stream a large document without building it
    in memory -- and it is what makes a genuine mid-write failure possible to
    demonstrate, because the exception can come from the producer.

    Args:
        path: The file to replace.
        chunks: Pieces of text, written in order.
        encoding: The text encoding to write with.
    """
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp_path.open("w", encoding=encoding, newline="") as f:
            for chunk in chunks:
                f.write(chunk)
        # Only reached if every chunk was produced and written. `replace`
        # overwrites an existing target; `rename` would raise FileExistsError
        # on Windows. Same directory, so it never crosses a filesystem.
        tmp_path.replace(path)
    finally:
        # A no-op after a successful replace (the temp file no longer exists),
        # and the cleanup on every failure path, including KeyboardInterrupt.
        tmp_path.unlink(missing_ok=True)


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write `content` to `path` atomically.

    The write is done to a temporary file first; on success it is renamed
    over `path`. Readers either see the old file or the new file, never
    a half-written one.

    Args:
        path: The file to replace.
        content: The complete new contents.
        encoding: The text encoding to write with.
    """
    atomic_write_chunks(path, [content], encoding=encoding)


# --------------------------------------------------------------------------- #
# Demonstration
# --------------------------------------------------------------------------- #
def failing_chunks() -> Iterable[str]:
    """Yield half a document, then blow up -- a simulated disk/producer failure.

    Yields:
        Two replacement lines, before raising.

    Raises:
        RuntimeError: Always, after the second chunk.
    """
    yield "REPLACEMENT LINE 1\n"
    yield "REPLACEMENT LINE 2\n"
    raise RuntimeError("simulated failure halfway through the write")


def _demo() -> int:
    """Overwrite a file safely, then fail mid-write and show it survived.

    The scratch folder is a temporary directory this function makes and
    deletes, so the demo needs nothing placed by hand and leaves nothing
    behind.

    Returns:
        Always 0. The failed write is the point, not an error.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="atomic_") as scratch:
        try:
            os.chdir(scratch)
            target = Path("important.txt")
            target.write_text("ORIGINAL LINE 1\nORIGINAL LINE 2\n", encoding="utf-8")
            print(f"before:            {target.read_text(encoding='utf-8')!r}")

            atomic_write_text(target, "REWRITTEN LINE 1\nREWRITTEN LINE 2\n")
            print(f"after good write:  {target.read_text(encoding='utf-8')!r}")

            try:
                atomic_write_chunks(target, failing_chunks())
            except RuntimeError as e:
                log.warning("write failed: %s", e)

            print(f"after failed write:{target.read_text(encoding='utf-8')!r}")
            leftovers = sorted(p.name for p in target.parent.glob("*.tmp"))
            print(f"temp files left:   {leftovers}")
        finally:
            os.chdir(home)
    return 0


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    raise SystemExit(_demo())
