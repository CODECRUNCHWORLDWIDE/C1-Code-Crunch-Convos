"""problem-05-github-releases-solution.py — the releases fetcher, proven offline.

The homework answer hits the public GitHub Releases API and prints the most
recent releases for a repo as TAG  DATE  TITLE, handling 404 and 403 without a
traceback and sending the User-Agent the API requires. Your own
problem-05-github-releases.py ends in ``raise SystemExit(main())`` and calls the
live API.

A published answer must not depend on GitHub's uptime, your rate limit, or which
releases exist the day a test runs, so this file ships a recorded response
(RECORDED_RELEASES, captured from api.github.com/repos/psf/requests) behind a
one-line seam. With USE_LIVE = False it formats the recording and never touches
the network. The formatting and the error handling being tested are identical
either way; set USE_LIVE = True to call the API for real.

Run it with::

    python problem-05-github-releases-solution.py
"""

from __future__ import annotations

import argparse
import os
import sys

import requests

API_URL = "https://api.github.com/repos/{owner}/{repo}/releases"
USER_AGENT = "CodeCrunchBot/0.1 (Week 12 homework; you@example.com)"
TIMEOUT = 10.0

# Flip to True to call api.github.com for real instead of the recording below.
USE_LIVE = False

# A recorded response: the six most recent releases of psf/requests at capture
# time. Only the three fields the report prints are kept.
RECORDED_RELEASES: list[dict[str, object]] = [
    {"tag_name": "v2.34.2", "published_at": "2026-05-14T19:27:15Z", "name": "v2.34.2"},
    {"tag_name": "v2.34.1", "published_at": "2026-05-13T19:23:51Z", "name": "v2.34.1"},
    {"tag_name": "v2.34.0", "published_at": "2026-05-11T19:40:27Z", "name": "v2.34.0"},
    {"tag_name": "v2.33.1", "published_at": "2026-03-30T16:12:09Z", "name": "v2.33.1"},
    {"tag_name": "v2.33.0", "published_at": "2026-03-25T16:38:25Z", "name": "v2.33.0"},
    {"tag_name": "v2.32.5", "published_at": "2025-08-18T20:33:27Z", "name": "v2.32.5"},
]


def fetch_releases(session: requests.Session, owner: str, repo: str) -> tuple[list, int]:
    """Return (releases list, HTTP status). The seam the demo runs offline.

    Both branches return the same shape, so the recording stands in for the API
    with no change to the code that formats it or checks the status.
    """
    if USE_LIVE:
        response = session.get(API_URL.format(owner=owner, repo=repo), timeout=TIMEOUT)
        payload = response.json() if response.status_code == 200 else []
        return payload, response.status_code
    return RECORDED_RELEASES, 200


def format_release(release: dict[str, object]) -> str:
    """One line: tag, publish date (YYYY-MM-DD), and title."""
    tag = str(release.get("tag_name", "?"))
    published = str(release.get("published_at", ""))[:10] or "?"
    title = str(release.get("name") or tag)
    return f"{tag:<10}  {published}  {title}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gh-releases",
        description="Print the most recent GitHub releases for a repo.",
    )
    parser.add_argument("repo", metavar="owner/repo", help="e.g. psf/requests")
    parser.add_argument("--count", type=int, default=5,
                        help="How many releases to show (default: %(default)s)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Fetch and print the releases. Return an exit code."""
    args = build_parser().parse_args(argv)
    if args.repo.count("/") != 1 or args.repo.startswith("/") or args.repo.endswith("/"):
        print(f"error: expected owner/repo, got {args.repo!r}", file=sys.stderr)
        return 1
    owner, repo = args.repo.split("/")

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT  # the API rejects requests without one
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        session.headers["Authorization"] = f"Bearer {token}"  # higher rate limit

    try:
        releases, status = fetch_releases(session, owner, repo)
    except requests.RequestException as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if status == 404:
        print(f"error: repo {args.repo} not found", file=sys.stderr)
        return 1
    if status == 403:
        print("error: rate-limited by GitHub (set GITHUB_TOKEN for a higher limit)",
              file=sys.stderr)
        return 1
    if status != 200:
        print(f"error: GitHub returned HTTP {status}", file=sys.stderr)
        return 1

    for release in releases[: args.count]:
        print(format_release(release))
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — the recorded response, formatted. Your own file has no
# demo; it calls the live API from the shell.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Print the recorded releases the way the live API would be printed."""
    print("GitHub Releases — proven offline against a recorded API response.")
    print()
    code = main(["psf/requests", "--count", "5"])
    print(f"[exit {code}]")
    print()
    print("The recording is injected behind fetch_releases(); set USE_LIVE = True")
    print("to call api.github.com for real — the User-Agent is required, and a")
    print("GITHUB_TOKEN in the environment raises the rate limit.")


if __name__ == "__main__":
    demo()
