"""audit.py -- print a summary of the current Python environment.

Challenge 2, Week 1, Code Crunch Convos. Reports the interpreter version,
implementation, platform, executable path, working directory, whether we
are inside a virtual environment, and every installed distribution.

Every line this prints describes the machine and the environment it ran
in, so two people never see the same report.

Run it with::

    python audit.py
"""

import os
import platform
import sys
from importlib.metadata import distributions

RULE_WIDTH: int = 58


def is_in_virtualenv() -> bool:
    """Return True when running inside a venv.

    Returns:
        True when ``sys.prefix`` and ``sys.base_prefix`` differ, which is
        the interpreter's own record of being inside an environment.
    """
    return sys.prefix != sys.base_prefix


def installed_packages() -> list[tuple[str, str]]:
    """Return ``(name, version)`` pairs for every installed distribution.

    Returns:
        One pair per distribution, sorted by name, case-insensitively.
        Duplicates reachable from two places on ``sys.path`` appear once.
    """
    found: dict[str, str] = {}
    for dist in distributions():
        name: str = dist.metadata["Name"] or ""
        if name and name not in found:
            found[name] = dist.version
    return sorted(found.items(), key=lambda pair: pair[0].lower())


def main() -> None:
    """Print the whole audit to standard output."""
    print("=" * RULE_WIDTH)
    print(" Python Environment Audit")
    print("=" * RULE_WIDTH)
    print(f"Python version : {platform.python_version()}")
    print(f"Implementation : {platform.python_implementation()}")
    print(f"Platform       : {platform.platform()}")
    print(f"Executable     : {sys.executable}")
    print(f"Working dir    : {os.getcwd()}")
    print(f"Inside venv    : {'yes' if is_in_virtualenv() else 'no'}")

    packages: list[tuple[str, str]] = installed_packages()
    print()
    print(f"Installed packages ({len(packages)}):")
    if not packages:
        print("  (none)")
    else:
        width: int = max(len(name) for name, _ in packages)
        for name, version in packages:
            print(f"  - {name.ljust(width)}  {version}")
    print("=" * RULE_WIDTH)


if __name__ == "__main__":
    main()
