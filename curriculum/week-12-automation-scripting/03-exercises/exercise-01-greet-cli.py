"""Exercise 01 — Greet CLI.

A friendly hello-world for argparse. Builds a script that takes a NAME
positional argument and an optional --shout flag.

Run:

    python exercise-01-greet-cli.py Alice
    python exercise-01-greet-cli.py Alice --shout
    python exercise-01-greet-cli.py --help

Stretch (try after the base works):
  1. Add a `--repeat N` integer option that prints the greeting N times.
  2. Add a `--lang` choice between "en", "fr", "es" with appropriate hellos.
  3. Add a `--version` flag that prints "greet 1.0.0" and exits.
"""
from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="greet",
        description="Say hello to NAME. Optionally shout.",
    )
    parser.add_argument("name", help="The name of the person to greet")
    parser.add_argument(
        "--shout",
        action="store_true",
        help="Print the greeting in ALL CAPS",
    )
    return parser


def greet(name: str, shout: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if shout else message


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(greet(args.name, shout=args.shout))
    return 0


if __name__ == "__main__":
    sys.exit(main())
