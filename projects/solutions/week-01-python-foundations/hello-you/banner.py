"""banner.py -- print a name centered inside a box of ASCII characters.

This is the Challenge 1 answer, copied into the mini-project unchanged so
that ``hello_you_plus.py`` can import ``build_banner`` instead of owning a
second copy of it. See
``curriculum/week-01-python-foundations/solutions/challenges.md`` for the
line-by-line walkthrough.
"""


def build_banner(name: str, padding: int = 6, border: str = "*") -> str:
    """Return the multi-line banner for ``name`` as one string.

    ``padding`` is the number of spaces on each side of the name, so the
    inside of the box is ``len(name) + 2 * padding`` characters wide.
    """
    inner_width: int = len(name) + 2 * padding
    edge: str = border * (inner_width + 2)
    blank: str = f"{border}{' ' * inner_width}{border}"
    middle: str = f"{border}{name.center(inner_width)}{border}"
    return "\n".join([edge, blank, middle, blank, edge])


def main() -> None:
    """Prompt for a name and print its banner."""
    raw: str = input("Your name: ")
    name: str = raw.strip()
    if not name:
        print("(no name provided)")
        return
    print(build_banner(name))


if __name__ == "__main__":
    main()
