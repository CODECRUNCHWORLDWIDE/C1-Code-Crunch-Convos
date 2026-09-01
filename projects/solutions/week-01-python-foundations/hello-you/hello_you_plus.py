"""hello_you_plus.py -- "Hello, You" with all five stretch goals on.

Week 1 mini-project stretch answer, Code Crunch Convos. Loops until the
user types ``quit``, writes every greeting to ``guests.txt`` with a
timestamp, varies the closing line per language, prints an ASCII banner
around the name, and colorizes the output when ``rich`` is installed.

Run it with::

    python hello_you_plus.py

``rich`` is optional -- without it the script prints the same text in
plain black and white.
"""

from datetime import datetime

from banner import build_banner

try:
    from rich.console import Console

    # Deliberately un-annotated: its type depends on which branch ran.
    # soft_wrap keeps rich from re-wrapping the banner to the terminal
    # width, so the colored output is character-for-character the same
    # as the plain output.
    CONSOLE = Console(soft_wrap=True)
except ImportError:  # rich is optional; plain print is the fallback
    CONSOLE = None

DEFAULT_LANGUAGE: str = "Python"
DEFAULT_NAME: str = "friend"
GUEST_BOOK: str = "guests.txt"
QUIT_WORDS: frozenset[str] = frozenset({"quit"})

LANGUAGE_LINES: dict[str, str] = {
    "python": "May your Python be readable.",
    "javascript": "May your JavaScript never be undefined.",
    "typescript": "May your TypeScript types never widen to any.",
    "rust": "May the borrow checker be gentle with you.",
    "go": "May your goroutines never leak.",
    "c": "May your pointers never dangle.",
    "c++": "May your destructors always fire.",
    "java": "May your stack traces be short.",
    "sql": "May your joins always hit an index.",
    "bash": "May your quotes always match.",
    "ruby": "May your Ruby stay a joy to read.",
}


def closing_line(language: str) -> str:
    """Return the punchy last sentence for ``language``.

    Unknown languages fall back to the mini-project's own wording, with
    the spelling the user typed.
    """
    return LANGUAGE_LINES.get(
        language.lower(), f"May your {language} be readable."
    )


def build_greeting(name: str, language: str) -> str:
    """Return the one-line greeting for ``name`` and ``language``."""
    return (
        f"Hello, {name}! Welcome to Code Crunch Convos. "
        f"{closing_line(language)}"
    )


def record_guest(name: str, language: str, path: str = GUEST_BOOK) -> None:
    """Append one timestamped line about ``name`` to ``path``.

    Uses ``"a"`` so each run adds to the guest book instead of replacing
    it. File modes and ``with`` blocks are Week 6 material -- this is a
    peek ahead.
    """
    stamp: str = datetime.now().isoformat(timespec="seconds")
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"{stamp}\t{name}\t{language}\n")


def show(text: str, style: str = "") -> None:
    """Print ``text``, colored by rich when rich is available.

    ``markup=False`` matters: a name like ``[bold]`` would otherwise be
    read as a rich formatting tag and vanish from the output.
    """
    if CONSOLE is None:
        print(text)
    else:
        CONSOLE.print(text, style=style, markup=False, highlight=False)


def greet_once() -> bool:
    """Prompt, greet, record. Return False when the user asked to quit."""
    try:
        raw_name: str = input("Your name (or 'quit' to stop): ").strip()
    except EOFError:  # piped input ran out; treat it as 'quit'
        print()
        return False
    if raw_name.lower() in QUIT_WORDS:
        return False

    name: str = raw_name or DEFAULT_NAME
    prompt: str = f"Favorite programming language [{DEFAULT_LANGUAGE}]: "
    try:
        language: str = input(prompt).strip() or DEFAULT_LANGUAGE
    except EOFError:
        print()
        return False

    show(build_banner(name), style="bold cyan")
    show(build_greeting(name, language), style="bold green")
    record_guest(name, language)
    return True


def main() -> None:
    """Greet in a loop until the user quits, then say goodbye."""
    show("Hello, You -- Code Crunch Convos, Week 1", style="bold magenta")
    while greet_once():
        pass
    show("Goodbye, and happy crunching.", style="bold magenta")


if __name__ == "__main__":
    main()
