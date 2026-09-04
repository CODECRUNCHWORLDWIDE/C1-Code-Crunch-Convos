# Homework 5 — GitHub releases fetcher

> **Topic:** a real HTTP API, its required `User-Agent`, JSON, and 404/403 handling
> **Lecture:** [03 — Scraping and Scheduling](../lecture-notes/03-scraping-and-scheduling.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hr
> **Why this one:** it is your first script against a real, public API with real rules — an obligatory `User-Agent`, a rate limit, and error codes you have to handle gracefully. Getting `TAG  DATE  TITLE` out of GitHub is the small win; learning to read an API's rules and respect them is the transferable one.

## The Brief

Hit the public GitHub Releases API and print the most recent releases for a
repository. Given `owner/repo`, fetch
`https://api.github.com/repos/{owner}/{repo}/releases`, and print each release
as `TAG  DATE  TITLE`. No authentication is needed for public repos.

The API has rules. It **requires** a `User-Agent` header and rejects requests
without one. It rate-limits unauthenticated callers, answering 403 when you have
made too many requests. And a repo that does not exist answers 404. Your script
handles all three without a traceback.

## Starter

```bash
pip install requests
```

```python
"""problem-05-github-releases.py — print a repo's recent GitHub releases.

    python problem-05-github-releases.py psf/requests --count 5
"""

from __future__ import annotations

import argparse
import os
import sys

import requests

API_URL = "https://api.github.com/repos/{owner}/{repo}/releases"
USER_AGENT = "CodeCrunchBot/0.1 (Week 12 homework; you@example.com)"
TIMEOUT = 10.0


def format_release(release: dict[str, object]) -> str:
    """One line: tag, publish date (YYYY-MM-DD), and title."""
    # TODO: tag_name, published_at[:10], name or tag
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Fetch and print the releases. Return an exit code."""
    # TODO: parse owner/repo, set the User-Agent, GET the API,
    # TODO: handle 404 and 403, print the first --count releases
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. CLI: `python gh_releases.py owner/repo [--count N]` (default 5).
2. Send a `User-Agent` header — the API requires it.
3. Print each release as `TAG  DATE  TITLE`, the date as `YYYY-MM-DD`.
4. Handle 404 (repo not found) and 403 (rate-limited) with a clear message and
   a non-zero exit, no traceback.
5. Exit 0 on success, 1 on any handled failure, 2 on an argparse error.

## Constraints

- **Send a real `User-Agent`.** GitHub's API returns 403 to requests without
  one. Name your tool and give a contact, exactly as you would for a scraper —
  an API is a server with an operator too.
- **Branch on the status code before reading the body.** A 404 or 403 body is
  not a list of releases; treat those codes explicitly and return a non-zero
  exit with a message, rather than letting `for release in releases` blow up on
  an error payload.
- **Read a token from `os.environ`, never from the source.** The stretch raises
  your rate limit with a `GITHUB_TOKEN`; read it from the environment so a key
  never lands in a committed file.
- **Format the date by slicing, not by parsing.** `published_at` is an ISO
  string like `2026-05-14T19:27:15Z`; the first ten characters are the date.
  You do not need `datetime` for a display string.

## Expected output

The shipped answer, [`problem-05-github-releases-solution.py`](./problem-05-github-releases-solution.py),
ships a recorded API response (captured from
`api.github.com/repos/psf/requests`) behind a one-line `fetch_releases` seam, so
it runs with no network and prints the same releases every time. Real captured
output:

```text
$ python problem-05-github-releases.py
GitHub Releases — proven offline against a recorded API response.

v2.34.2     2026-05-14  v2.34.2
v2.34.1     2026-05-13  v2.34.1
v2.34.0     2026-05-11  v2.34.0
v2.33.1     2026-03-30  v2.33.1
v2.33.0     2026-03-25  v2.33.0
[exit 0]

The recording is injected behind fetch_releases(); set USE_LIVE = True
to call api.github.com for real — the User-Agent is required, and a
GITHUB_TOKEN in the environment raises the rate limit.
```

Set `USE_LIVE = True` and the same code calls the real API; the formatting, the
`--count` cap, and the 404/403 handling are unchanged — only the bytes now come
over the network.

## Steps

1. Build the parser and split `owner/repo`. Reject anything that is not exactly
   one slash.
2. Make the request with the `User-Agent` header, and print the raw status code
   first so you know what you got.
3. Add the 404 and 403 branches, and test them (a made-up repo gives 404).
4. Write `format_release` and print the first `--count` of them.
5. Set `GITHUB_TOKEN` in your environment and confirm the script sends it (and
   that your rate limit goes up).

## The Solution

The shipped file is your answer — `format_release`, `main` — with a
`fetch_releases` seam and a recorded response so it proves itself offline. Your
own file has no recording and no `USE_LIVE`; it always calls the API.

```python
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
```

**The seam is one function, and it returns the same shape either way.**
`fetch_releases` returns `(releases, status)` whether the data came from
`api.github.com` or the recorded constant, so `main` — the parsing, the status
branches, the formatting — is identical offline and online. That is the same
recorded-response pattern as the quotes scraper, and the reason the offline demo
is a faithful test rather than a mock of a different code path.

**The status code is checked before the body is trusted.** A 404's body is a
`{"message": "Not Found"}` object, not a list; iterating it as releases would
raise. So `main` returns early on 404 (repo not found), 403 (rate-limited), and
any other non-200, each with its own message on stderr and a non-zero exit. The
happy path only runs once the status says it is safe to.

**The `User-Agent` is not optional here.** GitHub answers 403 to an API request
with no `User-Agent`, which is easy to miss because a browser and `requests`
usually send one for you — but a bare `requests.get` to this API does not set
one GitHub accepts. Naming the tool and a contact is the same courtesy the
scraper's header showed: it lets an operator tell your script apart from abuse.

**The token is read from the environment, added only if present.** `os.environ.get("GITHUB_TOKEN")`
returns `None` when unset, and the `Authorization` header is added only when a
token is there, so the script works unauthenticated and simply gets a higher
rate limit when a token exists. A key read from the environment never appears in
the file you commit — the one rule about secrets that has no exceptions.

## Run it

Copy the worked answer on this page into `problem-05-github-releases.py` and run it:

```bash
pip install requests
python problem-05-github-releases.py
```

It runs against the recorded response with no network, so you can also
[run it in the online editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-12-automation-scripting/homework/problem-05-github-releases.md).
Set `USE_LIVE = True` in the file to hit the live API.

## Common bugs to catch

- **Every request comes back 403, even for a repo you know exists.** You did not
  send a `User-Agent`. The API requires one.
- **`TypeError: string indices must be integers`** when you format a release.
  You got a 404 and iterated the error object as if it were a list. Branch on
  the status first.
- **The date prints as `2026-05-14T19:27:15Z`.** You printed `published_at`
  whole. Slice the first ten characters.
- **The token is hard-coded in the file.** Never. Read it from `os.environ`.
- **`KeyError: 'name'`** on a release with no title. `name` can be `null`; fall
  back to the tag with `release.get("name") or tag`.
- **`owner/repo` with a slash in the repo name splits wrong.** Split on the
  *first* slash only, or validate that there is exactly one.

## Under the hood

<details>
<summary>Under the hood — rate limits, and why the token multiplies your budget</summary>

GitHub's REST API meters you. Unauthenticated, you get 60 requests per hour, per
IP — fine for trying things, useless for anything that polls. Every response
carries the accounting in its headers: `X-RateLimit-Limit` (your ceiling),
`X-RateLimit-Remaining` (what is left), and `X-RateLimit-Reset` (a Unix
timestamp when the window rolls over). When `Remaining` hits zero the next call
is a 403 whose body explains you are rate-limited — which is exactly the branch
this script handles.

Sending a personal access token in the `Authorization: Bearer` header changes
the accounting from "per IP" to "per token" and raises the ceiling to 5,000
requests an hour. That is why the token is worth reading from the environment
even though the script works without it: the moment you loop over many repos, or
run under CI where you share an IP with everyone else on that runner, 60/hour
runs out in seconds. The professional habit is to read those three headers and,
when `Remaining` is low, sleep until `Reset` rather than hammering into a wall of
403s — the same politeness the scraper showed a website, expressed in the
currency an API meters you in.

</details>

## Acceptance checklist

- [ ] A valid repo prints its recent releases as `TAG  DATE  TITLE`.
- [ ] `--count N` limits how many are shown.
- [ ] A `User-Agent` header is sent on every request.
- [ ] A non-existent repo (404) and a rate limit (403) each print a message and
      exit non-zero, with no traceback.
- [ ] A `GITHUB_TOKEN`, if present in the environment, is sent; none is
      hard-coded.
- [ ] Committed to Git with a message like
      `Add Week 12 homework 5: GitHub releases fetcher`.

## Stretch

- Read `GITHUB_TOKEN` from the environment and send it as
  `Authorization: Bearer <token>` for the higher rate limit (already wired in
  the answer — try it with and without).
- Print the rate-limit headers when `-v` is passed, so you can watch your budget.
- Follow the `Link` header's `rel="next"` to page through *all* releases of a
  long-lived repo, not just the first page.

When 404 and 403 are handled cleanly, move on to
[Homework 6 — Port scanner](./problem-06-port-scanner.md).
