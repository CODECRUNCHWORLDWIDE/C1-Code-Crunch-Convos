"""Exercise 03 — Run shell.

Use subprocess to run `git log -5 --oneline` in the current repo and
parse the result into a list of (sha, message) tuples.

Run (must be in a git repo):
    python exercise-03-run-shell.py

Stretch:
  1. Accept a `--count N` flag so the user can ask for the last N commits.
  2. Accept a `--repo PATH` so the command runs in a specific repo.
  3. Print the output as JSON when `--json` is passed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Show the last N commits in a git repo as (sha, message) pairs.",
    )
    p.add_argument("--count", type=int, default=5, help="Number of commits (default: 5)")
    p.add_argument("--repo", type=Path, default=Path("."), help="Path to repo (default: .)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    return p


def fetch_log(repo: Path, count: int) -> list[tuple[str, str]]:
    """Run git log and return (sha, message) tuples."""
    result = subprocess.run(
        ["git", "log", f"-{count}", "--oneline"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    commits: list[tuple[str, str]] = []
    for line in result.stdout.strip().splitlines():
        sha, _, message = line.partition(" ")
        commits.append((sha, message))
    return commits


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        commits = fetch_log(args.repo, args.count)
    except FileNotFoundError:
        print("error: git is not installed or not on PATH", file=sys.stderr)
        return 127
    except subprocess.CalledProcessError as exc:
        print(f"error: git log failed (exit {exc.returncode})", file=sys.stderr)
        print(exc.stderr, file=sys.stderr)
        return exc.returncode

    if args.json:
        print(json.dumps([{"sha": s, "message": m} for s, m in commits], indent=2))
    else:
        for sha, message in commits:
            print(f"{sha}  {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
