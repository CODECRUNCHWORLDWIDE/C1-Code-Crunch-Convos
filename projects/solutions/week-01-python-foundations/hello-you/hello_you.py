"""hello_you.py -- greet the user by name.

Week 1 mini-project, Code Crunch Convos. Asks for a name and, optionally,
a favorite programming language, then prints one personalized greeting.

Run it with::

    python hello_you.py
"""

DEFAULT_LANGUAGE: str = "Python"
DEFAULT_NAME: str = "friend"


def prompt_user() -> tuple[str, str]:
    """Return ``(name, language)``, both stripped of outer whitespace.

    An empty name becomes ``DEFAULT_NAME`` and an empty language becomes
    ``DEFAULT_LANGUAGE``, so neither answer can be blank downstream.
    """
    name: str = input("Your name: ").strip() or DEFAULT_NAME
    prompt: str = f"Favorite programming language [{DEFAULT_LANGUAGE}]: "
    language: str = input(prompt).strip() or DEFAULT_LANGUAGE
    return name, language


def build_greeting(name: str, language: str) -> str:
    """Return the one-line greeting for ``name`` and ``language``."""
    return (
        f"Hello, {name}! Welcome to Code Crunch Convos. "
        f"May your {language} be readable."
    )


def main() -> None:
    """Prompt once, greet once."""
    name, language = prompt_user()
    print(build_greeting(name, language))


if __name__ == "__main__":
    main()
