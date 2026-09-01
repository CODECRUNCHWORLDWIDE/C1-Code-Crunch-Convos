"""exercise-04-pagination-solution.py — walk a paginated GitHub endpoint to the end.

The exercise walks GET https://api.github.com/users/{login}/repos one page at a
time until a page comes back empty, then reports how many repositories it found
and how many requests that took.

This shipped answer does not call GitHub. It replays a **recorded** listing --
the eight public repositories of the ``octocat`` account, captured from that
endpoint -- and slices it into pages the way a real server does. So the loop
under test is the real loop, and its stop condition is exercised for real.

Two reasons this one is recorded rather than live. Star counts move, so a live
run cannot promise the same output twice. And unauthenticated GitHub allows 60
requests an hour, which a class of thirty people share badly.

Run it with::

    python exercise-04-pagination-solution.py                 # the two-run demo
    python exercise-04-pagination-solution.py octocat --per-page 5
    python exercise-04-pagination-solution.py octocat --live  # the real API
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

import requests

API_ROOT = "https://api.github.com"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0
MAX_PAGES = 50

#: The public repositories of github.com/octocat, captured from
#: /users/octocat/repos and trimmed to the two fields this program reads. Star
#: counts drift upward every day, so these are a snapshot -- which is exactly
#: why the check at the end of the demo compares two runs with each other
#: rather than against a number written down here.
RECORDED_REPOS: list[dict[str, Any]] = [
    {"name": "boysenberry-repo-1", "stargazers_count": 473},
    {"name": "git-consortium", "stargazers_count": 603},
    {"name": "hello-worId", "stargazers_count": 790},
    {"name": "Hello-World", "stargazers_count": 3773},
    {"name": "linguist", "stargazers_count": 758},
    {"name": "octocat.github.io", "stargazers_count": 1148},
    {"name": "Spoon-Knife", "stargazers_count": 13989},
    {"name": "test-repo1", "stargazers_count": 482},
]

#: Anything that can hand back one page of repositories for one account.
#: Signature: (login, page, per_page) -> that page, possibly empty.
FetchPage = Callable[[str, int, int], list[dict[str, Any]]]


def make_session() -> requests.Session:
    """Return a Session with the headers GitHub expects from a script.

    Returns:
        A Session whose headers identify this program and pin the API version.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return session


def fetch_page(
    session: requests.Session, login: str, page: int, per_page: int
) -> list[dict[str, Any]]:
    """Fetch one page of repos. An empty list means there are no more pages.

    Args:
        session: A Session carrying the GitHub headers.
        login: The account name whose public repos we are listing.
        page: 1-based page number.
        per_page: Items per page, 1 to 100.

    Returns:
        The decoded JSON array for that page, possibly empty.

    Raises:
        requests.HTTPError: GitHub answered 4xx or 5xx.
    """
    response = session.get(
        f"{API_ROOT}/users/{login}/repos",
        params={"per_page": per_page, "page": page},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def live_pages() -> FetchPage:
    """Return a page fetcher that calls GitHub over one shared Session.

    Returns:
        A callable with the FetchPage signature. One Session is built here and
        reused for every page, so the connection is opened once.
    """
    session = make_session()

    def fetch(login: str, page: int, per_page: int) -> list[dict[str, Any]]:
        """Fetch one page from the real API."""
        return fetch_page(session, login, page, per_page)

    return fetch


def recorded_pages() -> FetchPage:
    """Return a page fetcher that slices RECORDED_REPOS, touching no network.

    Returns:
        A callable with the FetchPage signature. It slices the recording the
        way a paginating server slices its database: skip (page - 1) * per_page
        rows, then take per_page of them.
    """

    def fetch(login: str, page: int, per_page: int) -> list[dict[str, Any]]:
        """Serve one page out of the recording."""
        if login != "octocat":
            raise requests.HTTPError(
                f"404 Client Error: Not Found for url: "
                f"{API_ROOT}/users/{login}/repos"
            )
        start = (page - 1) * per_page
        return RECORDED_REPOS[start : start + per_page]

    return fetch


def fetch_all_repos(
    login: str, per_page: int, *, pages: FetchPage
) -> tuple[list[dict[str, Any]], int]:
    """Walk every page until one comes back empty; return (repos, requests).

    Args:
        login: The account name to walk.
        per_page: Page size to request.
        pages: How to get one page. live_pages() or recorded_pages().

    Returns:
        A flat list of every repo dict, and the number of requests made.

    Raises:
        RuntimeError: MAX_PAGES pages went by without an empty one.
    """
    repos: list[dict[str, Any]] = []
    requests_made = 0

    for page in range(1, MAX_PAGES + 1):
        batch = pages(login, page, per_page)
        requests_made += 1
        if not batch:
            print(f"page {page}: 0 repos  (empty -> stop)")
            return repos, requests_made
        print(f"page {page}: {len(batch)} repos")
        repos.extend(batch)

    raise RuntimeError(
        f"{login}: no empty page after {MAX_PAGES} pages; refusing to return "
        f"partial data"
    )


def summarise(login: str, per_page: int, *, pages: FetchPage) -> list[dict[str, Any]]:
    """Walk every page, print the summary line, and return the repos.

    Args:
        login: The account name to walk.
        per_page: Page size to request.
        pages: How to get one page.

    Returns:
        Every repository found, as one flat list.
    """
    repos, made = fetch_all_repos(login, per_page, pages=pages)
    stars = sum(repo["stargazers_count"] for repo in repos)
    print(f"{login}: {len(repos)} public repos, {stars} stars, {made} requests")
    return repos


def demo() -> int:
    """Run the same account at two page sizes and check they agree.

    Returns:
        The process exit code. Non-zero if the two runs disagree.
    """
    print("--- replaying recorded pages; pass --live to call GitHub ---")
    small = summarise("octocat", 3, pages=recorded_pages())
    print()
    large = summarise("octocat", 100, pages=recorded_pages())
    print()
    agree = sorted(repo["name"] for repo in small) == sorted(
        repo["name"] for repo in large
    )
    print(f"both runs found the same repositories: {agree}")
    return 0 if agree else 1


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, walk the pages, print the summary.

    Args:
        argv: Arguments after the program name. None means sys.argv[1:].

    Returns:
        The process exit code.
    """
    parser = argparse.ArgumentParser(description="Count public repos.")
    parser.add_argument("login", help="GitHub account name, e.g. octocat")
    parser.add_argument("--per-page", type=int, default=3, help="page size, 1-100")
    parser.add_argument(
        "--live", action="store_true", help="call the real API instead of replaying"
    )
    args = parser.parse_args(argv)

    pages = live_pages() if args.live else recorded_pages()
    summarise(args.login, args.per_page, pages=pages)
    return 0


if __name__ == "__main__":
    # No arguments means "show me what this does": run the two-page-size demo.
    # Any arguments at all means "I know what I want": run the real CLI.
    raise SystemExit(demo() if len(sys.argv) == 1 else main())
