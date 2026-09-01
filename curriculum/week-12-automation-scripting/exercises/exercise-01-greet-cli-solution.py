"""exercise-01-greet-cli-solution.py — the greet CLI, proven headless.

The exercise part is the starter with its TODOs filled in: a check-in desk
greeter built with argparse — a required name, a positive --times, a --greeting
from a fixed set, --shout, and --version.

Your own exercise-01-greet-cli.py ends in ``raise SystemExit(main())`` and is
run from the shell: ``python exercise-01-greet-cli.py Ada --times 3``. A
published answer cannot sit waiting for command-line arguments, so this file
proves the parser by calling ``main()`` with fixed argv lists itself and
printing what each one does — the good runs and the ones argparse rejects. The
parser being tested is identical either way.

Run it with::

    python exercise-01-greet-cli-solution.py
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys

GREETINGS: tuple[str, ...] = ("hello", "welcome", "howdy")


def positive_int(value: str) -> int:
    """Parse a command-line string as a whole number greater than zero.

    Raises:
        argparse.ArgumentTypeError: if the value is zero or negative.
    """
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"must be a positive whole number, got {number}"
        )
    return number


def build_parser() -> argparse.ArgumentParser:
    """Return the fully configured parser for the greet CLI."""
    parser = argparse.ArgumentParser(
        prog="greet",
        description="Greet a volunteer at the Code Crunch check-in desk.",
    )
    parser.add_argument("name", help="Name to print on the badge line")
    parser.add_argument(
        "-n", "--times",
        type=positive_int,
        default=1,
        help="How many badge lines to print (default: %(default)s)",
    )
    parser.add_argument(
        "--greeting",
        choices=GREETINGS,
        default="hello",
        help="Which word to open with (default: %(default)s)",
    )
    parser.add_argument(
        "--shout",
        action="store_true",
        help="Print the whole line in capitals, counter included",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    return parser


def badge_line(name: str, greeting: str, index: int, total: int) -> str:
    """Build a single badge line, e.g. 'Hello, Ada. (1 of 3)'."""
    return f"{greeting.capitalize()}, {name}. ({index} of {total})"


def main(argv: list[str] | None = None) -> int:
    """Parse argv, print the badge lines, and return an exit code."""
    args = build_parser().parse_args(argv)
    for index in range(1, args.times + 1):
        line = badge_line(args.name, args.greeting, index, args.times)
        print(line.upper() if args.shout else line)
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — the same argv lists the exercise page walks through.
# Your own file has no demo; it ends in ``raise SystemExit(main())`` and reads
# its arguments from the shell.
# --------------------------------------------------------------------------- #


def show(argv: list[str]) -> None:
    """Run the CLI once with *argv*, echoing the command, its output, exit code.

    argparse writes to stdout for --version and to stderr for a bad flag, and
    exits the process itself; capturing both streams and catching SystemExit is
    what lets one file demonstrate the success and the failure paths together.
    """
    print(f"greet {' '.join(argv)}")
    captured = io.StringIO()
    try:
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            code = main(argv)
    except SystemExit as exc:
        code = exc.code
    text = captured.getvalue()
    if text and not text.endswith("\n"):
        text += "\n"
    sys.stdout.write(text)
    print(f"[exit {code}]")
    print()


def demo() -> None:
    """Drive the parser with fixed argv lists and print the whole session."""
    os.environ["COLUMNS"] = "80"  # fixed width, so the usage block wraps the same everywhere
    print("Greet CLI — driving the parser headless with fixed argv lists.")
    print()
    show(["Ada"])
    show(["Ada", "--times", "3", "--greeting", "welcome"])
    show(["Grace H", "--shout"])
    show(["--version"])
    show(["Ada", "--times", "0"])
    show(["Ada", "--times", "two"])
    show(["Ada", "--greeting", "hi"])


if __name__ == "__main__":
    demo()
