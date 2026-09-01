"""exercise-01-hello-world-solution.py — first program, first run.

Prints a greeting, the author's name, and the running Python version.
"""

import sys


def main() -> None:
    """Print the three lines described in the module docstring."""
    print("Hello, Code Crunch.")
    print("My name is Ada Lovelace.")
    print(f"Running Python {sys.version_info.major}.{sys.version_info.minor}")


if __name__ == "__main__":
    main()
