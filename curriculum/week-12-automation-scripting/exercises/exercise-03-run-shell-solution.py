"""exercise-03-run-shell-solution.py — the toolbox doctor, proven headless.

The exercise part is the starter with its TODOs filled in: run each tool's
version command with a *list* of arguments, dig the version number out of
either output stream, and print one row per tool — a missing tool is a row, not
a crash.

Your own exercise-03-run-shell.py ends in ``raise SystemExit(main())`` and is
run from the shell: ``python exercise-03-run-shell.py --tool ...``. This file
drives ``main()`` with a fixed argv list — the three default tools, one that is
not installed, and the injection string from the exercise page — so it prints a
table you can check without typing anything. The probe being tested is
identical either way.

Run it with::

    python exercise-03-run-shell-solution.py
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

VERSION_RE = re.compile(r"\d+(?:\.\d+)+")
ROW = "{name:<12}  {version:<8}  {status}"


def default_tools() -> list[tuple[str, list[str]]]:
    """Return (label, argv) pairs for the tools checked by default."""
    return [
        ("python", [sys.executable, "-V"]),
        ("pip", [sys.executable, "-m", "pip", "--version"]),
        ("git", ["git", "--version"]),
    ]


def probe(argv: list[str], timeout: float) -> str | None:
    """Run argv and return the first version number in its output.

    Returns None if the program is missing, times out, or prints nothing
    that looks like a version.
    """
    try:
        result = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, PermissionError, subprocess.TimeoutExpired):
        return None

    match = VERSION_RE.search(result.stdout + result.stderr)
    return match.group(0) if match else None


def main(argv: list[str] | None = None) -> int:
    """Probe every tool, print the table, return an exit code."""
    parser = argparse.ArgumentParser(
        prog="toolbox-doctor",
        description="Report installed command-line tools and their versions.",
    )
    parser.add_argument("--tool", action="append", default=[], metavar="NAME",
                        help="Extra tool to check, run as `NAME --version`. Repeatable.")
    parser.add_argument("--timeout", type=float, default=10.0,
                        help="Seconds to wait for each tool (default: %(default)s)")
    args = parser.parse_args(argv)

    tools = default_tools()
    tools.extend((name, [name, "--version"]) for name in args.tool)

    print(ROW.format(name="TOOL", version="VERSION", status="STATUS"))
    found = 0
    for label, command in tools:
        version = probe(command, args.timeout)
        if version is None:
            print(ROW.format(name=label, version="-", status="not installed"))
        else:
            found += 1
            print(ROW.format(name=label, version=version, status="ok"))

    print()
    print(f"{found} of {len(tools)} tools available")
    return 0 if found == len(tools) else 1


# --------------------------------------------------------------------------- #
# The headless demo — the default tools, a missing one, and the injection
# string from the exercise page. Your own file has no demo; it reads --tool
# from the shell.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Drive the doctor and show the injection string is inert."""
    print("Run Shell — the toolbox doctor, driven headless.")
    print("Your version numbers will differ; the shape is what matters.")
    print()
    code = main(["--tool", "nosuchtool", "--tool", "echo hi & echo pwned"])
    print(f"[exit {code}]")
    print()
    print("Every call passed a list of arguments, so no shell was ever spawned.")
    print("The injection string became one program name, which does not exist, so")
    print("neither 'hi' nor 'pwned' ran. The safe path is also the default path.")
    needle = "shell=" + "True"
    count = Path(__file__).read_text(encoding="utf-8").count(needle)
    print(f"searching this file for {needle} finds: {count}")


if __name__ == "__main__":
    demo()
