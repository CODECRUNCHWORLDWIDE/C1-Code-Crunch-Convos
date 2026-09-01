"""challenge-02-github-user-stats-solution.py — a snapshot of a public GitHub profile.

Reads the public GitHub REST API -- no token required -- and prints one
account's profile, its total stars across every public repository, and its top
five repositories by stars.

    python challenge-02-github-user-stats-solution.py octocat
    python challenge-02-github-user-stats-solution.py octocat --live

This shipped answer replays a **recorded** account by default: the profile and
all eight repositories of github.com/octocat, captured on 2026-08-24. Star
counts move every day and unauthenticated GitHub allows only 60 requests an
hour per IP address, so a live run can promise neither the same numbers nor
even the same success. Pass ``--live`` and the identical code calls the real
API.

The recording also carries a 404 and a 403, so the two failure paths this tool
has to get right can be exercised without breaking anything.

Run with no arguments at all and it walks through all three.
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from typing import Any, Callable, NamedTuple

import requests

API_ROOT = "https://api.github.com"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0
PER_PAGE = 100
MAX_PAGES = 20
TOP_N = 5


class RecordedReply(NamedTuple):
    """One saved reply: the status GitHub sent, and the body it sent with it."""

    status_code: int
    body: Any


#: Real replies captured from api.github.com on 2026-08-24, keyed by the
#: request that produced them. Repositories are trimmed to the four fields this
#: program reads. The 403 body is a real rate-limit message with the IP address
#: replaced by the documentation address 203.0.113.7.
RECORDED: dict[str, RecordedReply] = {
    "/users/octocat": RecordedReply(
        200,
        {
            "login": "octocat",
            "name": "The Octocat",
            "bio": None,
            "location": "San Francisco",
            "followers": 23760,
            "public_repos": 8,
        },
    ),
    "/users/octocat/repos?page=1&per_page=100": RecordedReply(
        200,
        [
            {
                "name": "boysenberry-repo-1",
                "stargazers_count": 473,
                "description": "Testing",
                "language": None,
            },
            {
                "name": "git-consortium",
                "stargazers_count": 603,
                "description": "This repo is for demonstration purposes only.",
                "language": None,
            },
            {
                "name": "hello-worId",
                "stargazers_count": 790,
                "description": "My first repository on GitHub.",
                "language": None,
            },
            {
                "name": "Hello-World",
                "stargazers_count": 3773,
                "description": "My first repository on GitHub!",
                "language": None,
            },
            {
                "name": "linguist",
                "stargazers_count": 758,
                "description": (
                    "Language Savant. If your repository's language is being "
                    "reported incorrectly, send us a pull request!"
                ),
                "language": "Ruby",
            },
            {
                "name": "octocat.github.io",
                "stargazers_count": 1148,
                "description": None,
                "language": "CSS",
            },
            {
                "name": "Spoon-Knife",
                "stargazers_count": 13989,
                "description": "This repo is for demonstration purposes only.",
                "language": "HTML",
            },
            {
                "name": "test-repo1",
                "stargazers_count": 482,
                "description": None,
                "language": None,
            },
        ],
    ),
    "/users/octocat/repos?page=2&per_page=100": RecordedReply(200, []),
    "/users/does-not-exist-9999": RecordedReply(404, {"message": "Not Found"}),
    "/users/busy-day-demo": RecordedReply(
        403,
        {
            "message": (
                "API rate limit exceeded for 203.0.113.7. (But here's the good "
                "news: Authenticated requests get a higher rate limit. Check "
                "out the documentation for more details.)"
            )
        },
    ),
}

#: Anything that turns (path, query parameters) into a decoded JSON document.
Fetch = Callable[[str, dict[str, Any]], Any]


class GitHubError(Exception):
    """Raised when a lookup cannot be completed, for any reason.

    Everything the user needs to read is in str(exc).
    """


class Profile(NamedTuple):
    """The parts of a GitHub profile this tool displays."""

    login: str
    name: str
    bio: str
    location: str
    followers: int
    public_repos: int


class RepoLine(NamedTuple):
    """One repository, narrowed to what a listing needs."""

    name: str
    stars: int
    description: str


def recorded_key(path: str, params: dict[str, Any]) -> str:
    """Build the RECORDED key for one request.

    Args:
        path: The API path, starting with a slash.
        params: Query parameters, or an empty dict.

    Returns:
        The path with its parameters appended in sorted order.
    """
    if not params:
        return path
    query = "&".join(f"{key}={params[key]}" for key in sorted(params))
    return f"{path}?{query}"


def describe_failure(status_code: int, body: Any, login: str) -> str:
    """Turn a failing status code into a sentence a person can act on.

    Args:
        status_code: The status GitHub answered with.
        body: The decoded body, which GitHub fills with a "message".
        login: The account being looked up.

    Returns:
        One line of plain English.
    """
    message = body.get("message", "") if isinstance(body, dict) else ""
    if status_code == 404:
        return f"GitHub returned 404 for user '{login}'."
    if status_code == 403 and "rate limit" in message.lower():
        return (
            "GitHub rate limit reached. Wait for the hour to roll over, or set "
            "GITHUB_TOKEN in your environment to lift the limit."
        )
    return f"GitHub returned {status_code} for user '{login}': {message}"


def make_session() -> requests.Session:
    """Return a Session with the headers GitHub expects, plus a token if set.

    The token is read from the GITHUB_TOKEN environment variable and travels in
    the Authorization header. It never goes in a URL.

    Returns:
        A Session ready to make authenticated or anonymous calls.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
    return session


def live_fetch(login: str) -> Fetch:
    """Return a fetcher that calls GitHub over one shared Session.

    Args:
        login: The account being looked up, used only in error messages.

    Returns:
        A callable with the Fetch signature.
    """
    session = make_session()

    def fetch(path: str, params: dict[str, Any]) -> Any:
        """Fetch one path from the real API."""
        try:
            response = session.get(
                f"{API_ROOT}{path}", params=params, timeout=TIMEOUT_SECONDS
            )
        except requests.exceptions.RequestException as exc:
            raise GitHubError(f"could not reach GitHub: {exc}") from exc
        if response.status_code >= 400:
            body = response.json() if response.content else {}
            raise GitHubError(describe_failure(response.status_code, body, login))
        return response.json()

    return fetch


def recorded_fetch(login: str) -> Fetch:
    """Return a fetcher that answers from RECORDED, touching no network.

    Args:
        login: The account being looked up, used only in error messages.

    Returns:
        A callable with the Fetch signature.
    """

    def fetch(path: str, params: dict[str, Any]) -> Any:
        """Serve one path out of the recording."""
        key = recorded_key(path, params)
        reply = RECORDED.get(key)
        if reply is None:
            raise RuntimeError(f"no recorded reply for {key}; re-run with --live")
        if reply.status_code >= 400:
            raise GitHubError(describe_failure(reply.status_code, reply.body, login))
        return reply.body

    return fetch


def fetch_profile(login: str, *, fetch: Fetch) -> Profile:
    """Fetch one account's profile and narrow it to a Profile.

    Args:
        login: The account name.
        fetch: How to reach the API.

    Returns:
        The six fields this tool displays. Missing values become an em dash.

    Raises:
        GitHubError: the lookup failed.
    """
    payload = fetch(f"/users/{login}", {})
    return Profile(
        login=payload["login"],
        name=payload.get("name") or payload["login"],
        bio=payload.get("bio") or "—",
        location=payload.get("location") or "—",
        followers=payload["followers"],
        public_repos=payload["public_repos"],
    )


def fetch_all_repos(login: str, *, fetch: Fetch) -> list[RepoLine]:
    """Walk every page of an account's public repositories.

    Args:
        login: The account name.
        fetch: How to reach the API.

    Returns:
        Every public repository, as one flat list.

    Raises:
        GitHubError: the lookup failed.
        RuntimeError: MAX_PAGES pages went by without an empty one.
    """
    repos: list[RepoLine] = []
    for page in range(1, MAX_PAGES + 1):
        batch = fetch(f"/users/{login}/repos", {"per_page": PER_PAGE, "page": page})
        if not batch:
            return repos
        repos.extend(
            RepoLine(
                name=repo["name"],
                stars=repo["stargazers_count"],
                description=repo.get("description") or "",
            )
            for repo in batch
        )
    raise RuntimeError(
        f"{login}: no empty page after {MAX_PAGES} pages; refusing to return "
        f"partial data"
    )


def top_repos(repos: list[RepoLine], count: int = TOP_N) -> list[RepoLine]:
    """Return the *count* most-starred repositories, ties broken by name.

    Args:
        repos: Every repository found.
        count: How many to return.

    Returns:
        The top slice, most stars first.
    """
    return sorted(repos, key=lambda repo: (-repo.stars, repo.name))[:count]


def render(profile: Profile, repos: list[RepoLine]) -> str:
    """Format the whole report.

    Args:
        profile: The account's profile.
        repos: Every public repository found.

    Returns:
        The report as one string, with no trailing newline.
    """
    lines = [
        f"User:         {profile.login} ({profile.name})",
        f"Bio:          {profile.bio}",
        f"Location:     {profile.location}",
        f"Followers:    {profile.followers}",
        f"Public repos: {profile.public_repos}",
        f"Total stars:  {sum(repo.stars for repo in repos)}",
        f"Top {TOP_N} repos by stars:",
    ]
    for rank, repo in enumerate(top_repos(repos), start=1):
        summary = textwrap.shorten(repo.description, width=46, placeholder="...")
        # rstrip so a repository with no description leaves no trailing spaces:
        # invisible whitespace at the end of a line is a real diff nobody can see.
        lines.append(
            f"  {rank}. {repo.name:<20} (* {repo.stars:>5})  {summary}".rstrip()
        )
    return "\n".join(lines)


def report(login: str, *, fetch: Fetch) -> str:
    """Fetch everything for one account and render the report.

    Args:
        login: The account name.
        fetch: How to reach the API.

    Returns:
        The report as one string.

    Raises:
        GitHubError: the lookup failed.
    """
    return render(
        fetch_profile(login, fetch=fetch), fetch_all_repos(login, fetch=fetch)
    )


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, fetch the account, print the report.

    Args:
        argv: Arguments after the program name. None means sys.argv[1:].

    Returns:
        The process exit code. 0 on success, 2 on a handled failure.
    """
    parser = argparse.ArgumentParser(description="Summarise a GitHub account.")
    parser.add_argument("login", help="GitHub account name, e.g. octocat")
    parser.add_argument(
        "--live", action="store_true", help="call the real API instead of replaying"
    )
    args = parser.parse_args(argv)

    fetch = (live_fetch if args.live else recorded_fetch)(args.login)
    try:
        print(report(args.login, fetch=fetch))
    except GitHubError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    return 0


def demo() -> int:
    """Show one good account and both failure paths, all from the recording.

    Returns:
        The process exit code.
    """
    print("--- replaying an account recorded on 2026-08-24; pass --live for today's ---")
    print(report("octocat", fetch=recorded_fetch("octocat")))

    for login in ("does-not-exist-9999", "busy-day-demo"):
        print()
        try:
            print(report(login, fetch=recorded_fetch(login)))
        except GitHubError as err:
            print(f"Error: {err}")
    return 0


if __name__ == "__main__":
    raise SystemExit(demo() if len(sys.argv) == 1 else main())
