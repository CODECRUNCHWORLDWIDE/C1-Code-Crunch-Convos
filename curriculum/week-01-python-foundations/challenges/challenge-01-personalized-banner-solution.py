"""banner.py -- print a name centered inside a box of ASCII characters.

Challenge 1, Week 1, Code Crunch Convos. Takes a name from the command
line, trims the whitespace around it, and prints a rectangular banner
whose width grows with the name.

Run it with::

    python banner.py Ada
"""

import sys

DEMO_NAME: str = "Ada"


def build_banner(name: str, padding: int = 6, border: str = "*") -> str:
    """Return the multi-line banner for a name as one string.

    ``padding`` is the number of spaces on each side of the name, so the
    inside of the box is ``len(name) + 2 * padding`` characters wide.

    Args:
        name: the text to centre, already trimmed.
        padding: spaces between the name and each border column.
        border: the single character the box is drawn with.

    Returns:
        Five lines joined by newlines: edge, blank, name, blank, edge.
    """
    inner_width: int = len(name) + 2 * padding
    edge: str = border * (inner_width + 2)
    blank: str = f"{border}{' ' * inner_width}{border}"
    middle: str = f"{border}{name.center(inner_width)}{border}"
    return "\n".join([edge, blank, middle, blank, edge])


def read_name(argv: list[str]) -> str:
    """Return the name to draw, trimmed of the spaces around it.

    Args:
        argv: the words typed after the script name, usually
            ``sys.argv[1:]``.

    Returns:
        Those words joined by single spaces and stripped. When nothing
        was given, ``DEMO_NAME``, so the file always prints a banner.
    """
    return " ".join(argv).strip() or DEMO_NAME


def main() -> None:
    """Read one name from the command line and print its banner."""
    print(build_banner(read_name(sys.argv[1:])))


if __name__ == "__main__":
    main()
