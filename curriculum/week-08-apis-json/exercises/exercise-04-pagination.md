# Exercise 4 — Walking Every Page

> **Topic:** looping page by page until a page comes back empty
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md) for `params=`, and [03 — Authentication and Secrets](../lecture-notes/03-authentication-and-secrets.md) section 7 for rate limits
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** APIs almost never hand you everything at once. A program that quietly stops at the first slice is one of the most common bugs in professional code, because it never crashes — it just reports a smaller number than the truth, confidently, forever. Challenge 02 is graded on getting this right.

## The Brief

**Pagination** is what a server does when the answer is too big to send in one
go. Instead of the whole list, it sends you a slice and waits to be asked for
the next one. Think of a long book with no chapters: the server hands you
twenty pages, and if you want page twenty-one you have to ask again.

The public GitHub API needs no key for read-only calls.
`GET https://api.github.com/users/{login}/repos` returns a JSON **array** of
one account's public repositories, and it takes two query parameters that
matter here:

- `per_page` — how many items in one slice, up to 100.
- `page` — which slice, counting from 1.

Ask for a page past the end and the server returns an empty array, `[]`. That
empty array is your stop signal.

You are writing a repository counter. Give it an account name and it walks
every page, collects every repository, and reports the total count, the total
number of stars, and how many requests it took — printing one line per request
so you can watch the loop work.

The self-check needs no outside authority, and this is the good part. Run it
twice on the same account with different `--per-page` values. **The number of
requests must change. The number of repositories must not.** If it does, you
dropped a page. You do not need to know the right answer to catch yourself
getting it wrong.

## Starter

Save this as `exercise-04-pagination.py` and fill in every `TODO`.

```python
"""exercise-04-pagination.py — walk a paginated GitHub endpoint to the end."""

import argparse
from typing import Any

import requests

API_ROOT = "https://api.github.com"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0
MAX_PAGES = 50


def make_session() -> requests.Session:
    """Return a Session with the headers GitHub expects from a script."""
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
    """Fetch one page of repos. An empty list means there are no more pages."""
    # TODO: session.get(f"{API_ROOT}/users/{login}/repos", params=..., timeout=...)
    # TODO: params must carry BOTH per_page and page
    # TODO: raise_for_status(), then return .json()
    raise NotImplementedError


def fetch_all_repos(login: str, per_page: int) -> tuple[list[dict[str, Any]], int]:
    """Walk every page until one comes back empty; return (repos, requests)."""
    # TODO: loop page from 1 to MAX_PAGES
    # TODO: fetch, print "page N: M repos", extend the accumulator
    # TODO: break when the page is empty
    # TODO: raise RuntimeError if the loop runs out of pages
    raise NotImplementedError


def main() -> int:
    """Parse arguments, walk the pages, print the summary."""
    parser = argparse.ArgumentParser(description="Count public repos.")
    parser.add_argument("login", help="GitHub account name, e.g. octocat")
    parser.add_argument("--per-page", type=int, default=3, help="page size, 1-100")
    args = parser.parse_args()

    repos, made = fetch_all_repos(args.login, args.per_page)
    stars = sum(repo["stargazers_count"] for repo in repos)
    print(f"{args.login}: {len(repos)} public repos, {stars} stars, {made} requests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**`Session`.** Up to now every call has been `requests.get(...)`, which opens a
connection, uses it once, and throws it away. A `Session` keeps the connection
open between calls and remembers headers you set once. In a loop that makes
several requests to the same host, that is both faster and politer.

**`MAX_PAGES`.** A number you pick that says "if I have not finished by now,
something is wrong". You will see in the Constraints why a loop that depends on
somebody else's server behaving needs one.

## Requirements

1. `fetch_page()` sends `per_page` **and** `page` through `params=`, sets
   `timeout=`, and calls `raise_for_status()`.
2. The loop stops when a page returns an empty list — not when it returns fewer
   items than `per_page`.
3. Results accumulate with `list.extend()`, producing one flat list of repo
   dicts.
4. Each request prints a line: `page 1: 3 repos`. The final empty page prints
   `page 4: 0 repos  (empty -> stop)`.
5. The summary line reports the repository count, the total stars, and the
   request count.
6. If the loop reaches `MAX_PAGES` without an empty page, raise a
   `RuntimeError` naming the login and the cap. Do not return partial data
   silently.

## Constraints

- **Stop on an empty page, not on a short page.** A short page is *usually* the
  last one, and "usually" is not a contract. Some APIs return a short page in
  the middle of a sequence, when items are filtered out on their side after the
  slice has already been cut. The empty page costs exactly one extra request
  and is unambiguous. Take the shortcut only when an API's own documentation
  promises that short means last.

- **`MAX_PAGES` is not optional.** Your loop's normal exit depends on a remote
  server behaving. If a bug on their side serves page 1 forever, an uncapped
  `while True` hammers them until you happen to notice, which might be
  tomorrow. A hard cap turns a runaway into an error message.

- **Every request passes `timeout=`.** In a pagination loop a missing timeout
  is uniquely nasty: pages 1 through 6 succeed, page 7 stalls, and your screen
  is full of output suggesting everything is fine.

- **Set a real `User-Agent`.** GitHub asks every client to identify itself. A
  descriptive one is what lets them contact you instead of blocking you if your
  script misbehaves. It costs one dictionary entry.

- **Never put a token in the query string.** Unauthenticated calls get 60
  requests per hour, which is plenty here, so you need no token at all. When
  you add one in Challenge 02 it travels in the `Authorization` header, loaded
  from a `.env` file — never `?token=...`, which lands in server logs, proxy
  logs, and your own shell history.

- **Use `list.extend()`, not `list.append()`.** `append` adds the whole page as
  one element, so you get a list of lists, `len()` returns the page count, and
  the star sum blows up several lines later with a message that says nothing
  about pages.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3:

```text
$ python exercise-04-pagination.py
--- replaying recorded pages; pass --live to call GitHub ---
page 1: 3 repos
page 2: 3 repos
page 3: 2 repos
page 4: 0 repos  (empty -> stop)
octocat: 8 public repos, 22016 stars, 4 requests

page 1: 8 repos
page 2: 0 repos  (empty -> stop)
octocat: 8 public repos, 22016 stars, 2 requests

both runs found the same repositories: True
```

Run with no arguments, the shipped file does both walks and then checks them
against each other. Your own program does one walk per invocation; run it twice
and compare the summary lines yourself.

The star total is a snapshot. Stars accumulate every day, and a live run will
give you a bigger number — which is precisely why the last line compares the
two runs with each other rather than against anything written down. **Same
repository count, same star total, different request count.** That invariant is
the deliverable. The number is not.

## Steps

1. Create `exercise-04-pagination.py` and paste the starter in.
2. Write `fetch_page()` first, and call it by hand for page 1 and page 2 with
   `per_page=3`. Confirm the two pages hold different repositories.
3. Now call it for a page far past the end — `page=500`. Confirm you get `[]`
   and not an error. That behaviour is what your whole loop depends on, so see
   it once with your own eyes.
4. Write `fetch_all_repos()` and run it with `--per-page 3`.
5. Run it again with `--per-page 100` and compare the summary lines. Count and
   stars identical, request count different.
6. Print `sorted(repo["name"] for repo in repos)` after each run and compare
   the two lists. Identical sets, or you dropped something.
7. Check your hourly budget: `curl -s https://api.github.com/rate_limit`, or
   read `response.headers["X-RateLimit-Remaining"]` inside `fetch_page()`.

## The Solution

```python
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
```

**A `for` over `range(1, MAX_PAGES + 1)` instead of `while True`.** This is the
central structural choice on the page. The loop's normal exit is the `return`
inside it, on the empty page. The `for` is there so the loop has a *second*
exit that does not depend on a remote server behaving. Fall out of the bottom
and you raise. That is not tidiness: an uncapped loop against an endpoint that
serves page 1 forever will hammer somebody else's server until you notice.

**Stop on empty, not on short.** For this account a short page really is the
last one, and stopping on `len(batch) < per_page` would give the same answer
today. It is still the wrong rule, because "fewer items than I asked for" is a
coincidence of how most APIs implement slicing, not a promise any of them made.
One extra request buys you a stop condition you can defend.

**`extend`, not `append`.** `pages(...)` returns a *list* of repositories.
`append` would add that list as a single element, so `repos` becomes a list of
pages, `len(repos)` becomes the number of requests, and the star sum fails
several lines later with a message about string indices.

**`pages` is the seam.** `fetch_all_repos` does not know where a page comes
from. It asks for `(login, page, per_page)` and gets a list back. `live_pages()`
returns a function that calls GitHub; `recorded_pages()` returns a function
that slices a list already in the file. The loop — the thing this exercise is
actually about — is identical either way, which is the proof that the seam is
in the right place.

**`recorded_pages()` slices the way a server slices.** It skips
`(page - 1) * per_page` rows and takes `per_page` of them. That is not a
convenience: it is what a paginating server does to its database, roughly one
`OFFSET`/`LIMIT` away from the real SQL. So the recording produces genuinely
short pages, genuinely empty pages, and genuinely different request counts at
different page sizes — every behaviour the loop is being tested against.

**`live_pages()` builds its Session once and keeps it.** It returns a small
function that closes over that Session, so every page in a walk shares one
connection. This is a **closure**: a function that remembers a value from where
it was made. You have seen the shape before without the name — it is what
`key=lambda entry: entry["slot"]` was doing in Exercise 2.

**No token, anywhere.** Unauthenticated calls get 60 requests an hour, which is
plenty. When Challenge 02 adds one it goes in the `Authorization` header from a
`.env` file, never in the query string, because query strings land in server
logs, proxy logs, browser history and `Referer` headers.

**The self-check is the deliverable, not the number.** The last line of `demo()`
compares the repository names found by the two walks. That comparison is true
today, was true before the stars moved, and will be true after. A test written
against `22016` would have been wrong by tomorrow morning.

## Run it

Copy the worked answer on this page into `exercise-04-pagination.py` and run it:
and run it:

```bash
python exercise-04-pagination.py
```

It needs `requests` installed and **no internet**. The eight repositories it
pages through were captured from `https://api.github.com/users/octocat/repos`
and pasted into the file as `RECORDED_REPOS`, trimmed to the two fields this
program reads.

There are two reasons this one is recorded rather than live, and both are worth
knowing. Star counts move every day, so a live run cannot promise you the same
output twice. And unauthenticated GitHub allows 60 requests an hour **per IP
address**, which a class sharing one network burns through in minutes.

To call the real API, pass a flag:

```bash
python exercise-04-pagination.py octocat --live --per-page 3
```

`--live` swaps `recorded_pages()` for `live_pages()` and changes nothing else.
Your star total will be larger than the one on this page, and the invariant
will still hold.

The `-solution` in the filename keeps this file from colliding with your own
`exercise-04-pagination.py`.

## Common bugs to catch

- **The loop never ends and every page holds the same repositories.** You built
  `params` once outside the loop, or you left `page` out of it entirely. With
  no `page` parameter GitHub serves page 1 every time, forever:

  ```text
  page 1: 3 repos  first=boysenberry-repo-1
  page 2: 3 repos  first=boysenberry-repo-1
  page 3: 3 repos  first=boysenberry-repo-1
  page 4: 3 repos  first=boysenberry-repo-1
  Traceback (most recent call last):
    File "exercise-04-pagination.py", line 84, in fetch_all_repos
      raise RuntimeError(
      ...<2 lines>...
      )
  RuntimeError: octocat: no empty page after 4 pages; refusing to return partial data
  ```

  Printing the first repository name per page is the quickest way to see it:
  identical names mean identical pages. And note what the program did — it
  stopped and said so. That is `MAX_PAGES` earning its place.

- **`TypeError: list indices must be integers or slices, not str`.**

  ```text
  page 1: 8 repos
  page 2: 0 repos  (empty -> stop)
  Traceback (most recent call last):
    File "exercise-04-pagination.py", line 91, in main
      stars = sum(repo["stargazers_count"] for repo in repos)
                  ~~~~^^^^^^^^^^^^^^^^^^^^
  TypeError: list indices must be integers or slices, not str
  ```

  You used `append` instead of `extend`. The page lines printed perfectly; the
  error surfaces in the star sum, several lines from the mistake, and says
  nothing about pages. Note also that this endpoint's body is a JSON *array*,
  not an object — there is no `["items"]` key to reach into first.

- **`403 Client Error: rate limit exceeded for url: ...`.** You burned through
  60 requests in an hour, most likely from an early version of the loop that
  did not terminate. `X-RateLimit-Reset` is a Unix timestamp telling you when
  the window rolls over.

- **`404 Client Error: Not Found for url: https://api.github.com/users/.../repos`.**
  The account name is wrong. GitHub returns 404 rather than an empty list, and
  the distinction matters: `404` is "no such account", `[]` is "this account
  has nothing". Your loop treats them completely differently, and it should.

- **The two runs disagree by one or two repositories.** Either you stopped on a
  short page, or the account genuinely changed between runs. Run them back to
  back; if they still disagree, it is your loop.

- **`json.decoder.JSONDecodeError` on a later page.** Almost always a
  rate-limit or error page arriving as HTML. Call `raise_for_status()` *before*
  `.json()` and you get a clear `HTTPError` instead of a confusing parse
  failure.

## Under the hood

<details>
<summary>Under the hood — the four ways an API can paginate</summary>

Page numbers are the shape you just wrote. There are three more you will meet,
and knowing which one you are looking at is most of the work.

**Page and size.** `?page=2&per_page=100`. Easy to read, easy to jump around
in, and easy to get wrong: if rows are inserted while you are walking, an item
can slide from page 2 to page 3 and you will never see it. GitHub uses this.

**Offset and limit.** `?offset=100&limit=50`. The same idea with the arithmetic
exposed — skip this many, take that many. It has the same drift problem, and it
gets slow on large tables, because a database asked for `OFFSET 500000` has to
count through half a million rows before it can start returning any.

**Cursor, sometimes called keyset.** The server hands back an opaque token and
you send it next time: `?cursor=eyJpZCI6NDIxfQ`. Immune to drift, because the
token means "after this exact record" rather than "past this many records", and
fast at any depth. The cost is that you cannot jump to page 40, and you must
not try to decode the token — it is theirs, and its format can change.

**A `next` link.** The server tells you the whole next URL, either in the body
or in a `Link` header. This is the friendliest of the four, because there is no
arithmetic to get wrong at all.

GitHub sends the `Link` header alongside page numbers, and `requests` parses it
for you into `response.links`:

```text
Link: <https://api.github.com/user/583231/repos?per_page=3&page=2>; rel="next",
      <https://api.github.com/user/583231/repos?per_page=3&page=3>; rel="last"
```

```text
>>> response.links["next"]["url"]
'https://api.github.com/user/583231/repos?per_page=3&page=2'
```

Loop `while "next" in response.links` and you stop when the *server* stops
offering a next page — its own opinion about whether there is more, instead of
your inference from a page length. It also saves the extra empty-page request.
Homework problem 5 has you write that parser by hand.

One trap that spans all four. Sorting is not optional if you want a stable
walk. An endpoint with no defined order is free to return rows in a different
arrangement on every request, and then no pagination scheme on earth can
promise you saw everything exactly once.

</details>

<details>
<summary>Under the hood — what a rate limit is, and why it is not about you</summary>

GitHub allows an unauthenticated client 60 requests an hour. Authenticate and
it becomes 5,000. Those numbers are not a punishment; they are how a service
stays up when one badly-written loop finds it.

The rules travel in the headers, so your program can read them:

```text
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 54
X-RateLimit-Reset: 1787488575
X-RateLimit-Used: 6
```

`Reset` is a Unix timestamp — seconds since the start of 1970 — so
`datetime.fromtimestamp(1787488575)` turns it into a time you can read. When
you run out, the answer is `403` (GitHub's choice) or `429 Too Many Requests`
(the standard one), and both mean the same thing: come back later.

Some services also send `Retry-After`, which is either a number of seconds or
an actual date. When it is there, honour it. It is the server telling you the
exact answer to "how long?", and guessing is strictly worse than being told.

The important reframe: **a rate limit is a shared resource, not a personal
quota.** A limit is applied per IP address, so an entire classroom or office
usually shares one. When your loop misbehaves, the person who cannot work is
the person sitting next to you.

Which is why the two habits on this page are habits and not preferences. Cap
the loop, so a bug costs 50 requests instead of 50,000. And identify yourself
in the `User-Agent`, so that when your script does misbehave the operator has
somebody to email instead of a subnet to block.

</details>

## Acceptance checklist

- [ ] `per_page` and `page` both travel through `params=`, never in an f-string.
- [ ] The loop stops on an empty page and prints the `(empty -> stop)` line.
- [ ] `MAX_PAGES` is enforced and raises rather than returning partial data.
- [ ] Two runs with different `--per-page` values agree on the repository count
      and the star total, and disagree on the request count.
- [ ] Every request has a `timeout=` and a descriptive `User-Agent`.
- [ ] No token appears anywhere in the file or in a URL.
- [ ] You can say what the difference is between a `404` and an empty array.
- [ ] Committed to Git with a message like `Add Week 8 exercise 4: paginate GitHub repos`.

## Stretch

- Switch to the `Link` header instead of counting pages. Loop while
  `"next" in response.links`, following `response.links["next"]["url"]`. Notice
  that you no longer build a URL at all.

- Turn `fetch_all_repos` into a generator that `yield`s one repository at a
  time, so a caller can stop early without downloading every page. The change
  is small; the difference for a caller who wanted the first five results of
  four hundred is not.

- Try the same loop against
  `https://pokeapi.co/api/v2/pokemon?limit=20&offset=0`. That API uses
  offset/limit and returns a `next` URL inside the body rather than an empty
  array — two more of the four strategies, in one endpoint.

- Add a second account to `RECORDED_REPOS` — capture a real listing from any
  public profile — and make `recorded_pages()` serve both. You now have a
  fixture you can point every future version of this loop at, for free, in
  under a second.

When both runs agree, move on to
[Exercise 5 — When the Network Misbehaves](./exercise-05-handle-errors.md).
