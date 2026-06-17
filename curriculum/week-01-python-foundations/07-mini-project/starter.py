"""starter.py — Hello, You (Week 1 mini-project starter).

Project
-------
A friendly command-line program that asks the user for their name and
(optionally) their favorite programming language, then prints a
personalized greeting.

How to use this starter
-----------------------
1. Copy this file into a new project folder named ``hello-you``.
2. Rename it to ``hello_you.py``.
3. Inside that folder, create and activate a virtual environment:

   .. code-block:: bash

       python -m venv .venv
       source .venv/bin/activate     # macOS / Linux
       .venv\\Scripts\\Activate.ps1   # Windows PowerShell

4. Implement :func:`prompt_user` and :func:`build_greeting` below so the
   program behaves as described in ``README.md``.
5. Run the program:

   .. code-block:: bash

       python hello_you.py

Acceptance check
----------------
Given the inputs ``Ada`` and ``Python``, the script should print
something like::

    Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
"""

from __future__ import annotations


def prompt_user() -> tuple[str, str]:
    """Ask the user for their name and favorite language.

    Returns
    -------
    tuple[str, str]
        A pair of ``(name, language)``. ``language`` should default to
        ``"Python"`` if the user just presses Enter.
    """
    # TODO: implement two ``input(...)`` calls, strip whitespace, and
    # default the language to "Python" when the answer is empty.
    raise NotImplementedError("prompt_user is not implemented yet.")


def build_greeting(name: str, language: str) -> str:
    """Return the greeting line that includes ``name`` and ``language``.

    The exact wording is up to you, but it must contain both arguments.
    """
    # TODO: return a string built with an f-string, e.g.
    # f"Hello, {name}! Welcome to Code Crunch Convos. May your {language} be readable."
    raise NotImplementedError("build_greeting is not implemented yet.")


def main() -> None:
    """Program entry point. Wire prompt and greeting together."""
    name, language = prompt_user()
    print(build_greeting(name, language))


if __name__ == "__main__":
    main()
