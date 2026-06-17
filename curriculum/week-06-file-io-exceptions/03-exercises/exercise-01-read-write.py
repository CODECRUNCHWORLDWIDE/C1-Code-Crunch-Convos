"""Exercise 01 — Read, transform, write.

Topic: file I/O, the `with` statement, line iteration.
Reference: lecture-notes/01-files-and-pathlib.md sections 2, 4, 5.

Task
----
Write a function `copy_lowercased(src, dst)` that:

  * Reads the file at path `src`, line by line.
  * Writes each line to the file at path `dst`, lowercased.
  * Preserves the line count and line breaks of the source file.
  * Uses utf-8 encoding for both files.
  * Uses the `with` statement (no manual close).

Running this file should:

  1. Create a small sample file `sample-in.txt` with mixed-case lines.
  2. Call `copy_lowercased("sample-in.txt", "sample-out.txt")`.
  3. Print the contents of the output so you can verify it worked.

Expected output (last block):

    --- sample-out.txt ---
    hello world
    python is fun
    code crunch convos

"""

from pathlib import Path


def copy_lowercased(src: Path, dst: Path) -> int:
    """Copy `src` to `dst`, lowercasing every line.

    Returns the number of lines copied.
    """
    # TODO: open `src` for reading and `dst` for writing in utf-8.
    # TODO: iterate line by line, write `line.lower()` to dst.
    # TODO: count the lines and return the count.
    line_count = 0
    with src.open("r", encoding="utf-8") as fin, \
         dst.open("w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line.lower())
            line_count += 1
    return line_count


def _make_sample(path: Path) -> None:
    """Helper: create a small input file with mixed-case text."""
    sample = "Hello WORLD\nPython is FUN\nCode Crunch Convos\n"
    path.write_text(sample, encoding="utf-8")


if __name__ == "__main__":
    here = Path(__file__).parent
    src = here / "sample-in.txt"
    dst = here / "sample-out.txt"

    _make_sample(src)
    n = copy_lowercased(src, dst)
    print(f"Copied {n} line(s) from {src.name} to {dst.name}")

    print("--- sample-out.txt ---")
    print(dst.read_text(encoding="utf-8"), end="")
