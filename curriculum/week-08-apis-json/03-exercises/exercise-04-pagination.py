"""Exercise 04 — Pagination.

GOAL
----
GitHub returns at most 100 repositories per page. Fetch ALL pages of
public repositories for the user "octocat" and print the total count.

We use page-number pagination (`?per_page=100&page=N`) and stop when the
server returns an empty page. (GitHub also exposes a `Link` header with
explicit `next`/`last` URLs — Homework problem 5 has you parse it.)

API:    https://api.github.com/users/{username}/repos
DOCS:   https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user
LIMITS: 60 unauthenticated requests/hour per IP. octocat has very few
        repos, so we will not come close to the limit.

EXPECTED OUTPUT (numbers may grow over time):

    Page 1: 8 repos (total so far: 8)
    Page 2: 0 repos (total so far: 8)
    octocat has 8 public repos in total.

KEY CONCEPTS
------------
- Looping until the server tells you "no more data".
- Using `params=` for both filters AND the page number.
- A reusable `Session` for many requests to the same host.

EXTENSION
---------
Try changing USERNAME to "torvalds" or your own GitHub username and run
again. You will see the loop walk through many pages.
"""

from __future__ import annotations

from typing import Any

import requests


USERNAME = "octocat"
PER_PAGE = 100  # GitHub max
BASE_URL = "https://api.github.com"


def fetch_all_repos(username: str, *, timeout: float = 10.0) -> list[dict[str, Any]]:
    """Walk every page of public repos for `username`."""
    all_repos: list[dict[str, Any]] = []

    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "code-crunch-bootcamp/1.0",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

        page = 1
        while True:
            response = session.get(
                f"{BASE_URL}/users/{username}/repos",
                params={"per_page": PER_PAGE, "page": page},
                timeout=timeout,
            )
            response.raise_for_status()
            batch: list[dict[str, Any]] = response.json()

            print(f"Page {page}: {len(batch)} repos (total so far: {len(all_repos) + len(batch)})")

            # If we got fewer than PER_PAGE items, this is the last page.
            # (An empty list also satisfies this condition.)
            all_repos.extend(batch)
            if len(batch) < PER_PAGE:
                break

            page += 1

    return all_repos


def main() -> None:
    repos = fetch_all_repos(USERNAME)
    print(f"{USERNAME} has {len(repos)} public repos in total.")


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────────────────────────────────
# Hints
# ─────────────────────────────────────────────────────────────────────────
# 1. The "stop when empty" pattern works for almost any paginated API
#    that uses page numbers. A few APIs return a `null` next-page token
#    instead — same idea, different signal.
# 2. If you hit 403 with "API rate limit exceeded for your IP", wait an
#    hour or set GITHUB_TOKEN in your .env (see lecture 3). The token
#    bumps your limit from 60 to 5000 requests/hour.
# 3. For a tighter stopping condition, check `if len(batch) < PER_PAGE:
#    break` BEFORE the next request — this saves one round-trip on the
#    last page. This file does exactly that.
