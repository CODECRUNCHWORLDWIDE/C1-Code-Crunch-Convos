# Challenge 02 — GitHub User Stats

> **Topic:** two endpoints, full pagination, a token that stays out of the URL, and two failure paths that both have to be right
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md) for sessions, and [03 — Authentication and Secrets](../lecture-notes/03-authentication-and-secrets.md) for tokens and rate limits
> **Difficulty:** Intermediate
> **Target time:** 3 hours
> **Why this one:** it is the first program on the week that has to get *two* calls right and combine them. It is also where the pagination bug from Exercise 4 becomes expensive: an account with 130 repositories and a loop that stops at 100 reports a star total that is wrong and looks completely reasonable.

## The Brief

Recruiters, journalists and conference organisers often want a quick snapshot
of somebody's public GitHub footprint. You are building the tool that prints
one.

The public GitHub API needs no key for read-only calls. Two endpoints do the
work:

| Endpoint | What it gives you |
|---|---|
| `GET /users/{login}` | name, bio, location, follower count, public repo count |
| `GET /users/{login}/repos?per_page=100&page=N` | one page of public repositories |

The profile reply, trimmed to the parts you need:

```json
{
  "login": "octocat",
  "name": "The Octocat",
  "bio": null,
  "location": "San Francisco",
  "followers": 23760,
  "public_repos": 8
}
```

Note `"bio": null`. Three of those six fields are nullable, and `null` becomes
Python's `None`, and `None` printed straight out says `None` — which looks like
a bug to whoever reads your output. Every one of them needs a fallback.

Each repository in the second reply carries at least:

```json
{
  "name": "Hello-World",
  "stargazers_count": 3773,
  "description": "My first repository on GitHub!"
}
```

`description` is nullable too.

Your finished tool runs like this:

```bash
$ python ghstats.py octocat
User:         octocat (The Octocat)
Bio:          —
Location:     San Francisco
Followers:    23760
Public repos: 8
Total stars:  22016
Top 5 repos by stars:
  1. Spoon-Knife          (* 13989)  This repo is for demonstration purposes only.
  ...

$ python ghstats.py does-not-exist-9999
Error: GitHub returned 404 for user 'does-not-exist-9999'.
```

## Starter

Save this as `ghstats.py` and fill in every `TODO`.

```python
"""ghstats.py — print a snapshot of one public GitHub profile."""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from typing import Any, NamedTuple

import requests

API_ROOT = "https://api.github.com"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0
PER_PAGE = 100
MAX_PAGES = 20
TOP_N = 5


class GitHubError(Exception):
    """Raised when a lookup cannot be completed, for any reason."""


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


def make_session() -> requests.Session:
    """Return a Session with GitHub's headers, plus a token if one is set."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    # TODO: read GITHUB_TOKEN from os.environ; if it is set, add
    #       session.headers["Authorization"] = f"Bearer {token}"
    return session


def get_json(session: requests.Session, path: str, params: dict[str, Any]) -> Any:
    """GET one path and return the decoded body, or raise GitHubError."""
    # TODO: session.get(f"{API_ROOT}{path}", params=params, timeout=...)
    # TODO: on status >= 400, read body["message"] and raise GitHubError with
    #       a sentence: 404 -> "no such user", 403 + "rate limit" -> advice
    # TODO: wrap RequestException into GitHubError too
    raise NotImplementedError


def fetch_profile(session: requests.Session, login: str) -> Profile:
    """Fetch one account's profile, with fallbacks for the nullable fields."""
    # TODO: get /users/{login} and build a Profile
    # TODO: name falls back to login; bio and location fall back to "—"
    raise NotImplementedError


def fetch_all_repos(session: requests.Session, login: str) -> list[RepoLine]:
    """Walk every page of the account's public repositories."""
    # TODO: the Exercise 4 loop, capped at MAX_PAGES
    raise NotImplementedError


def top_repos(repos: list[RepoLine], count: int = TOP_N) -> list[RepoLine]:
    """Return the most-starred repositories, ties broken by name."""
    # TODO: sorted(..., key=lambda r: (-r.stars, r.name))[:count]
    raise NotImplementedError


def render(profile: Profile, repos: list[RepoLine]) -> str:
    """Format the whole report."""
    raise NotImplementedError  # TODO


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, fetch the account, print the report."""
    parser = argparse.ArgumentParser(description="Summarise a GitHub account.")
    parser.add_argument("login", help="GitHub account name, e.g. octocat")
    args = parser.parse_args(argv)

    # TODO: build the session, render the report, print it
    # TODO: catch GitHubError, print f"Error: {err}" to stderr, return 2
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
```

**Token.** A long secret string that proves who you are. GitHub lifts the rate
limit from 60 requests an hour to 5,000 when you send one. It travels in the
`Authorization` header, never in a URL — see the Constraints for why that is
not a preference.

**`os.environ`.** The dictionary of environment variables your program was
started with. Reading a secret from there means it is never in your source and
never in your commit history.

## Requirements

1. Accept one positional argument: the GitHub login.
2. Fetch the profile.
3. Fetch **all pages** of the account's public repositories, using the Exercise
   4 pattern.
4. Print the name (or login when `name` is null), bio and location (`—` when
   null), follower count, public repository count, the **sum of
   `stargazers_count` across every repository**, and the top five repositories
   by stars with name, star count and a truncated description.
5. Be polite to the API: a descriptive `User-Agent`, `timeout=` on every
   request, and `Authorization: Bearer <token>` when `GITHUB_TOKEN` is set in
   the environment.
6. Handle failure with no traceback: `404` says the user was not found; `403`
   with a rate-limit message says to wait or set a token; anything else prints
   a short message. All of them exit non-zero.

## Constraints

- **Never put the token in the query string.** Not `?token=...`, not
  `?access_token=...`. A query string is logged by the server, by every proxy
  in between, and by your own shell history, and it lands in the `Referer`
  header of any link somebody clicks from the page. A header is logged by far
  fewer things and redacted by most of them. This is the single most common way
  a real credential leaks.

- **The token comes from the environment, never from the source.** A secret in
  a file is a secret in your commit history forever, even after you delete it,
  because Git keeps every version. If you use a `.env` file, put `.env` in
  `.gitignore` first — in that order.

- **Sum the stars across every page, not just the first.** An account with 130
  repositories and a loop that stops after 100 reports a total that is wrong
  and looks entirely plausible. This is the bug Exercise 4 exists to prevent
  and the one this challenge is graded on.

- **Every nullable field needs a fallback.** `bio`, `location`, `name` and
  `description` can all be `null`. Printing `None` at somebody is a bug you can
  see from across the room.

- **Cap the pagination loop.** Same reason as Exercise 4: your normal exit
  depends on a remote server behaving.

- **Errors go to `stderr`, results to `stdout`, and the exit code is non-zero
  on failure.**

- **Catch narrow exceptions, never bare `except Exception:`.**

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3:

```text
$ python challenge-02-github-user-stats-solution.py
--- replaying an account recorded on 2026-08-24; pass --live for today's ---
User:         octocat (The Octocat)
Bio:          —
Location:     San Francisco
Followers:    23760
Public repos: 8
Total stars:  22016
Top 5 repos by stars:
  1. Spoon-Knife          (* 13989)  This repo is for demonstration purposes only.
  2. Hello-World          (*  3773)  My first repository on GitHub!
  3. octocat.github.io    (*  1148)
  4. hello-worId          (*   790)  My first repository on GitHub.
  5. linguist             (*   758)  Language Savant. If your repository's...

Error: GitHub returned 404 for user 'does-not-exist-9999'.

Error: GitHub rate limit reached. Wait for the hour to roll over, or set GITHUB_TOKEN in your environment to lift the limit.
```

Run with no arguments, the shipped file shows one good account and both failure
paths. Run with a login it is the tool.

Two things in that block reward a second look.

Line 3 of the listing has no description at all, because
`octocat.github.io` has none. It prints as nothing rather than as `None`, and
the trailing spaces are stripped so the line does not end in invisible
whitespace.

And `hello-worId` — fourth place — is not a typo on this page. That repository
really is spelled with a capital letter I where the l should be. Look at it in
a font where they differ and you will see it; in most fonts you will not. It
sits next to the real `Hello-World`, and it is a small, permanent lesson in why
you compare identifiers with `==` rather than with your eyes.

The star totals are a snapshot. Stars accumulate daily, and a `--live` run
tomorrow will give a bigger number.

## Steps

1. Create `ghstats.py` and paste the starter in.
2. Write `make_session()` and `get_json()`, then fetch `/users/octocat` and
   print the raw payload. Find every field you need in it.
3. Write `fetch_profile()`. Test it against an account with a null bio and one
   with a real bio.
4. Write `fetch_all_repos()`. This is Exercise 4's loop; if you solved that
   one, copy your own.
5. Check the pagination the way Exercise 4 taught you: run with `PER_PAGE = 3`
   and again with `PER_PAGE = 100` and confirm the star total does not move.
6. Write `top_repos()` and `render()`.
7. Now the failure paths. Try a login that does not exist. Then, to see the
   403 without burning an hour of your budget, temporarily point the tool at a
   recorded reply — the shipped answer shows how.
8. Check `echo $?` after a failure. It should not be `0`.

## The Solution

```python
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
```

**`fetch` is the seam again, and here it is a closure with the login baked in.**
`live_fetch(login)` and `recorded_fetch(login)` both *return* a function. That
function remembers the login, so `describe_failure` can name the account in its
message without the login being threaded through every call. The rest of the
program takes a `fetch` and never mentions `requests`.

**The recording carries failures on purpose.** A `404` and a `403` are stored
alongside the good account. That is what makes both error paths testable
without breaking a network or waiting an hour to be rate-limited — and error
paths that are hard to reach are exactly the ones that ship broken. Whenever
you build a stand-in, record the failures first; the success case is the one
you were going to test anyway.

**`describe_failure` is shared by both fetchers.** So the recorded 403 produces
character-for-character the sentence the live 403 produces. Duplicate that
formatting in the stand-in and the two drift, and you end up debugging a
message that only exists in the fixture.

**A missing recording raises `RuntimeError`, not `GitHubError`.** They are
different kinds of problem. `GitHubError` means "the API said no", which is
about the account. `RuntimeError` means "this fixture does not cover that",
which is about the fixture. Mapping the second onto the first would tell you an
account does not exist when the truth is that nobody recorded it.

**The token is read once, in `make_session`, and put in a header.** Two
consequences worth naming. It is never in a URL, so it cannot leak through a
log. And it is set on the `Session`, so every request in the walk carries it
without any call site remembering — a secret handled in one place is a secret
you can audit.

**`os.environ.get("GITHUB_TOKEN")` with no default, and an `if`.** An empty or
missing variable means no header at all, rather than `Authorization: Bearer `
with nothing after it, which GitHub answers with `401` and a message that does
not obviously mean "you sent an empty token".

**Nullable fields are handled with `or`, at the boundary.**
`payload.get("bio") or "—"` covers both the missing key and the explicit
`null`, because `None` and `""` are both falsy. Same idea as Exercise 2's unit
conversion: fix the foreign data's shape once, where it arrives, and nothing
downstream has to know it was ever awkward.

**`sorted(repos, key=lambda repo: (-repo.stars, repo.name))`.** The negative
star count sorts descending; `repo.name` breaks ties alphabetically. Sorting on
a tuple sorts on the first element and uses the rest only for ties, and giving
a sort a deterministic tie-break is what stops the output shuffling between
runs for no visible reason.

**`textwrap.shorten` rather than a slice.** A slice can cut a word in half.
`shorten` collapses runs of whitespace, truncates at a word boundary, and adds
the placeholder, and it counts the placeholder inside the width so the result
never overruns.

**`.rstrip()` on each listing line.** A repository with no description would
otherwise leave two spaces at the end of the line. Invisible trailing
whitespace is a real difference that nobody can see, and it will fail a
comparison you are sure should pass.

**`fetch_all_repos` asks for `per_page=100` and still loops.** The largest page
GitHub allows is not the same as "all of them". Asking for the biggest page
reduces the number of requests; it does not remove the need to walk.

## Download and run

Download
[challenge-02-github-user-stats-solution.py](./challenge-02-github-user-stats-solution.py)
and run it:

```bash
python challenge-02-github-user-stats-solution.py
```

It needs `requests` installed and **no internet**. The profile, all eight
repositories, a `404` and a `403` were captured from `api.github.com` on
2026-08-24 and pasted into the file as `RECORDED`.

There are two reasons this one is recorded. Star counts move every day, so a
live run cannot promise the same output twice. And unauthenticated GitHub
allows 60 requests an hour **per IP address**, which a class sharing one
network exhausts in minutes — the very failure the tool is supposed to explain
politely.

To call the real API:

```bash
python challenge-02-github-user-stats-solution.py octocat --live
```

`--live` swaps `recorded_fetch` for `live_fetch` and changes nothing else. If
you have a token, set it first and the limit stops being a problem:

```bash
# macOS or Linux
export GITHUB_TOKEN=ghp_your_token_here
# PowerShell
$env:GITHUB_TOKEN = "ghp_your_token_here"
```

Setting it in your shell rather than in a file means it is never at risk of
being committed. A token for this needs no scopes at all — public data is
public — so create one with everything switched off.

One edit was made to the recording: the rate-limit message contains the IP
address it was measured against, and that now reads `203.0.113.7`, an address
reserved for documentation.

The `-solution` in the filename keeps this file from colliding with your own
`ghstats.py`.

## Common bugs to catch

- **`Bio:          None`.** You printed the field without a fallback. `null`
  becomes `None`, and `None` in an f-string becomes the four characters `None`.

- **The star total is too low, and everything else is right.**

  ```text
  Public repos: 137
  Total stars:  4102
  ```

  Read those two numbers together: the profile says 137 repositories and your
  loop found the stars of 100. You stopped after the first page. Comparing
  `len(repos)` against `profile.public_repos` is a free self-check and worth
  printing while you develop.

- **`TypeError: unsupported operand type(s) for -: 'str' and 'int'`.** Your
  sort key is `-repo["stargazers_count"]` on a dict where you meant the
  narrowed `RepoLine`, or the field name is wrong and you are negating a
  string.

- **`403 Client Error: rate limit exceeded for url: ...` as a traceback.** You
  called `raise_for_status()` and did not catch `HTTPError`, or you checked
  only for `404`. Read the `message` field in the body — GitHub says
  `API rate limit exceeded for <ip>` in plain English, and matching on
  `"rate limit"` is how you tell it apart from a genuine permissions problem,
  which is also a `403`.

- **`401 Bad credentials`.** Your `GITHUB_TOKEN` is set but wrong, expired, or
  empty. An empty one is the sneaky case: `Authorization: Bearer ` with nothing
  after it is not the same as sending no header at all.

- **`KeyError: 'message'` while handling an error.** Not every failing reply
  has a JSON body — some proxies return HTML — so read it with `.get()` and a
  default rather than with `[...]`.

- **The description column is ragged, or a word is cut in half.** You sliced
  with `[:46]` instead of using `textwrap.shorten`.

- **Two runs list the top five in a different order.** You sorted on stars
  alone and two repositories are tied. Add the name as a tie-break.

## Under the hood

<details>
<summary>Under the hood — where a secret is safe, and where it only looks safe</summary>

Rank the places a token can live, worst first.

**In the source code.** The worst, and it is worse than it looks, because Git
never forgets. Deleting the line in a later commit leaves the token in the
history of every clone, on every laptop, and in every fork. The fix is not a
commit; it is revoking the token.

**In a URL.** Almost as bad, for reasons that are easy to miss. Web servers log
the full path and query of every request by default, as does every proxy and
load balancer along the way. It is in your shell history. It goes into the
browser's address bar if the URL is ever opened. And it is sent in the
`Referer` header to any third-party site linked from a page fetched that way.
Multiply that by everyone who can read a log file.

**In an environment variable.** Much better and where this tool reads from. It
is not in your code, not in your history, and not in the URL. It is not
perfect: on many systems any process running as you can read another process's
environment, and it is easy to leak by printing `os.environ` in a debug dump or
a crash report.

**In a `.env` file that is gitignored.** The same protection with better
ergonomics, and one sharp edge worth stating: add `.env` to `.gitignore`
**before** you create the file. Do it the other way round and you have a window
in which `git add .` sweeps it in.

**In a secrets manager or the OS keychain.** What production uses. Encrypted at
rest, access-controlled, and it records who read what and when.

Three habits that matter more than the ranking:

**Scope the token to nothing you do not need.** This tool reads public data, so
a token with every permission switched off works perfectly. A leaked token that
can do nothing is an inconvenience; a leaked token that can push is an
incident.

**Rotate on suspicion, not on proof.** Revoking and reissuing takes a minute.
Establishing that a leaked token was definitely never used takes considerably
longer and rarely succeeds.

**Never log the token, and be careful what you log around it.**
`print(response.request.headers)` — which Exercise 1 suggested as a way to see
what `requests` sends — will happily print your `Authorization` header. That is
fine on httpbin with no token and a bad habit to carry into a program that has
one.

</details>

<details>
<summary>Under the hood — why 200 does not mean your answer is correct</summary>

This tool checks `status_code >= 400` and treats everything else as success.
That is necessary and it is not sufficient, and the gap is worth seeing plainly
because it is where a whole class of quiet bugs lives.

A status code describes the **HTTP conversation**. `200 OK` means: the server
understood the request, and here is a body. It says nothing about whether the
body contains what you wanted.

Plenty of real APIs answer `200` while telling you, inside the body, that
nothing worked. Two you meet elsewhere in this very week:

```text
>>> requests.get("https://is.gd/create.php",
...              params={"format": "json", "url": "notaurl"}, timeout=5)
<Response [200]>
>>> _.json()
{'errorcode': 1, 'errormessage': 'Please enter a valid URL to shorten'}
```

```text
>>> requests.get("https://geocoding-api.open-meteo.com/v1/search",
...              params={"name": "NotARealPlace", "count": 1}, timeout=5).json()
{'generationtime_ms': 0.65505505}
```

The first is a working shortener refusing a bad URL. The second is a working
geocoder saying it found nothing — with no `results` key at all, so
`payload["results"]` raises `KeyError` several lines from the cause.

GitHub is well behaved and uses status codes properly, which is exactly why
this tool can be as short as it is. But "well behaved" is an observation about
one API, not a property of HTTP, and the habit that survives contact with the
next API is:

1. `raise_for_status()`, or an equivalent check, for the conversation.
2. A check that the field you actually need is present, for the answer.

The second one is yours, and nothing can do it for you, because only you know
what you asked for. `payload.get("results") or raise` is often the whole of it.

There is a mirror-image trap on the other side. A `404` is not always "you
asked wrongly" — GitHub returns `404` rather than `403` for a private
repository you cannot see, deliberately, so that the response does not confirm
the repository exists. A status code is a summary written by somebody with
their own priorities, and reading the body is how you find out what they
actually meant.

</details>

## Acceptance checklist

- [ ] The profile lookup works and every nullable field has a fallback.
- [ ] The repository walk fetches **every** page, and `len(repos)` matches
      `public_repos`.
- [ ] The star total is the sum across all pages.
- [ ] The top five are sorted by stars descending, with ties broken by name.
- [ ] `GITHUB_TOKEN` is used when set, from the environment, in a header.
- [ ] No token appears in any URL, in the source, or in any printed output.
- [ ] `404` and rate-limited `403` each produce one helpful line and a non-zero
      exit.
- [ ] Every request passes `timeout=` and a descriptive `User-Agent`.
- [ ] No bare `except Exception:` anywhere in the file.
- [ ] Committed to Git with a message like `Add Week 8 challenge 2: GitHub user stats`.

## Stretch

- Add `--json`, which prints the whole result as a JSON document instead of
  formatted text, so another program can consume it. Then pipe it into
  `python -m json.tool` and confirm it parses.

- Add `--save FILE`, appending each result to a JSON history file using Week
  6's patterns. Decide what happens when the file already exists and is
  malformed, and write the reason down.

- Show each repository's `language` next to the star count, with a fallback for
  the ones that have none. The recording already carries the field.

- Print `X-RateLimit-Remaining` after each live request while you develop. It
  turns "am I about to be blocked?" from a guess into a number.

- Record a second account of your own — capture the two replies with `curl` —
  and add it to `RECORDED`. An account with more than 100 repositories is the
  one worth capturing, because it is the only one that can catch the
  pagination bug.

When both failure paths print one clean line, take everything to
[the mini-project](../mini-project/README.md).
