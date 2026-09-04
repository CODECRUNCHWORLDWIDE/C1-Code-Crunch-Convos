# Homework Problem 6 — Tiny URL-Shortener Client

> **Topic:** wrapping a real web API in a class, with the network hidden behind a seam
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md) · [Exercise 5 — When the Network Misbehaves](../exercises/exercise-05-handle-errors.md)
> **Difficulty:** Advanced
> **Target time:** 1 hour
> **Why this one:** it is the week's finale, and it puts every habit together at once — a `requests.Session`, a `timeout=`, `raise_for_status()`, a custom exception, a cache, and a `with` block that cleans up after itself. It is also the first time a real service tells you "no" in a way `raise_for_status()` cannot see, which is the single most useful thing to learn about talking to APIs you did not write.

## The Brief

A URL shortener is a tiny machine: you hand it a long web address and it hands
back a short one that redirects to it. [is.gd](https://is.gd) runs one for free,
with **no key and no signup**, at this address:

```text
GET https://is.gd/create.php?format=json&url=<the-long-url>
```

When it works, it answers with a little JSON parcel:

```json
{"shorturl": "https://is.gd/ccw_home"}
```

When it will not shorten your URL — because the URL is broken, or blocked, or
just nonsense — it answers with a *different* parcel:

```json
{"errorcode": 1, "errormessage": "Please enter a valid URL to shorten"}
```

Here is the trap, and it is the whole point of the problem. **is.gd sends that
error with a `200 OK` status.** As far as HTTP is concerned nothing went wrong —
the request arrived, the server answered. The "no" is hidden inside the body.
So `raise_for_status()`, the habit you drilled all week, will not catch it. You
have to open the parcel and look.

Your job is to wrap this in a small, well-behaved class: it keeps one
connection open, checks your URL before it bothers the server, turns every kind
of failure into one clear exception, remembers answers it has already fetched,
and tidies up when you are done with it.

**There is no live network in the shipped answer.** The finished file carries a
few real is.gd replies recorded on 2026-08-21 and feeds them to the class
through a *seam* — a `fetch` argument you can swap out. The exact same class
talks to the real is.gd when you pass `--live`. This is the same move Problem 3
made with the clock: put the thing you cannot control behind a door you can open
from the inside.

## Starter

Save this as `hw06_url_shortener.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — every URL comes back as the same placeholder until
you write `shorten`:

```python
"""A tiny client for the is.gd URL-shortening API."""

from __future__ import annotations

import sys
from typing import Any, Callable

import requests

CREATE_URL = "https://is.gd/create.php"
USER_AGENT = "code-crunch-bootcamp/1.0"

#: Anything that turns a long URL into the decoded JSON is.gd sent back.
Fetch = Callable[[str], dict[str, Any]]

#: A couple of real is.gd replies so you can build this offline.
RECORDED: dict[str, dict[str, Any]] = {
    "https://www.codecrunchworldwide.com/": {"shorturl": "https://is.gd/ccw_home"},
    "https://": {"errorcode": 1, "errormessage": "Please enter a valid URL to shorten"},
}


class ShortenError(Exception):
    """Raised when a URL cannot be shortened, for any reason."""


def fetch_recorded(long_url: str) -> dict[str, Any]:
    """Answer one request from RECORDED, touching no network."""
    recorded = RECORDED.get(long_url)
    if recorded is None:
        raise RuntimeError(f"no recorded reply for {long_url!r}; re-run with --live")
    return recorded


class URLShortenerClient:
    """A small client for is.gd."""

    def __init__(self, *, timeout: float = 5.0, fetch: Fetch | None = None):
        self._timeout = timeout
        self._cache: dict[str, str] = {}
        # TODO: if fetch is None, build a requests.Session, set its User-Agent,
        #       and use self._fetch_live. Otherwise store fetch and no session.
        self._session = None
        self._fetch: Fetch = fetch or fetch_recorded

    def _fetch_live(self, long_url: str) -> dict[str, Any]:
        # TODO: GET CREATE_URL with params={"format": "json", "url": long_url},
        #       pass timeout=self._timeout, call raise_for_status(), return .json()
        raise NotImplementedError

    def shorten(self, long_url: str) -> str:
        # TODO: reject a URL that is not http:// or https:// with ShortenError.
        # TODO: return a cached answer if you have one.
        # TODO: call self._fetch; wrap a RequestException in ShortenError.
        # TODO: if "shorturl" is missing, raise ShortenError with errormessage.
        # TODO: cache and return the short URL.
        return "https://is.gd/TODO"

    def close(self) -> None:
        # TODO: close the session if there is one.
        ...

    # TODO: __enter__ returns self; __exit__ calls close().


if __name__ == "__main__":
    with URLShortenerClient(fetch=fetch_recorded) as client:
        print(client.shorten("https://www.codecrunchworldwide.com/"))
```

**No setup needed — you can solve this one in the browser.** The default path uses recorded replies, so it never touches the network. Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-08-apis-json/homework/problem-06-tiny-url-shortener-client.md) and run it there.

## Requirements

1. `class URLShortenerClient` with `__init__(self, *, timeout: float = 5.0)`,
   `shorten(self, long_url: str) -> str`, and `close(self) -> None`.
2. The live client builds **one `requests.Session` per instance** and sets a
   `User-Agent` header on it.
3. `shorten` validates that `long_url` starts with `http://` or `https://`
   **before** any request goes out, and raises `ShortenError` if it does not.
4. `shorten` raises a custom `ShortenError` on an is.gd error document *and* on
   a network failure — one exception type for the caller to catch, whatever
   went wrong.
5. The class is a **context manager**: `with URLShortenerClient() as c:` closes
   the Session on the way out, even if the body raised.
6. `shorten` **caches** results, so shortening the same URL twice in one session
   sends only one request.
7. A `__main__` block shortens a few URLs and prints the results. The shipped
   answer runs against the recording by default and reaches the real API only
   with `--live`.
8. Type hints and a docstring on every function and method.

## Constraints

- **The network lives behind a seam, and the endpoint is keyless.** The `fetch`
  argument is the seam: the default is the real is.gd, but the tests and the
  demo pass `fetch_recorded` so they run offline and print the same thing every
  time. A URL shortener whose answer changes every run is impossible to write an
  expected output for. is.gd needs no key, so nothing secret is ever in play.

- **`timeout=` on the live request, always.** `requests` has no default timeout.
  A shortener that hangs forever because a server accepted your connection and
  then went quiet is worse than one that fails — a failure you can see and
  handle, a hang you cannot.

- **`raise_for_status()` is necessary but not sufficient.** Call it, because a
  real `500` or `404` still arrives as an HTTP error. But is.gd reports a
  *refused URL* with a `200` and an `errorcode` in the body, so you must **also**
  check for `shorturl` in the parsed JSON. Two failure channels, two checks.

- **One `Session`, closed deliberately.** A `Session` reuses one TCP connection
  across calls, which is faster and kinder to the server than a fresh connection
  each time. But an open Session holds a socket, so it must be closed — which is
  what `close()` and the `with` block are for.

- **`ShortenError` is the one thing a caller catches.** Inside, many things can
  go wrong — a timeout, a DNS failure, a refused URL, a bad status. The caller
  should not have to know the five `requests` exception types. Collapse them all
  into `ShortenError` at the boundary, exactly as Exercise 5 did with `ApiError`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3:

```text
$ python problem-06-tiny-url-shortener-client.py
--- replaying is.gd replies recorded on 2026-08-21; pass --live for real ---
https://is.gd/ccw_home  <-  https://www.codecrunchworldwide.com/
https://is.gd/ccw_org  <-  https://github.com/CODECRUNCHWORLDWIDE
https://is.gd/ccw_meteo  <-  https://open-meteo.com/en/docs
https://is.gd/ccw_home  <-  https://www.codecrunchworldwide.com/  (from cache, not re-sent)
rejected locally: long_url must start with http:// or https://, got 'mailto:hi@example.com'
caught ShortenError: is.gd refused the URL: Please enter a valid URL to shorten

requests sent to is.gd: 4 (the repeat was served from cache)
```

Read the last line against the lines above it. Five distinct URLs were handed to
`shorten`, plus one repeat. The `mailto:` one never became a request — it was
rejected locally. The repeat never became a request either — it came from the
cache. That leaves four that actually went out, which is what the counter says.

## Steps

1. Copy the starter into `hw06_url_shortener.py` and run it. It prints the
   `TODO` placeholder, because `shorten` does not do anything yet.
2. Write `_fetch_live`: `self._session.get(CREATE_URL, params=..., timeout=...)`,
   then `raise_for_status()`, then `return response.json()`.
3. Fix `__init__` so that with no `fetch` it builds a real Session (with the
   User-Agent) and points `self._fetch` at `_fetch_live`.
4. Write `shorten` one guard at a time: the `http(s)` check, the cache lookup,
   the fetch inside a `try`, the `shorturl` check, then cache-and-return.
5. Add `close`, `__enter__` and `__exit__`. Run the starter's `__main__` — it
   should now print a real short URL.
6. Build the demo: shorten a few URLs, shorten one twice to see the cache, and
   feed it `"mailto:..."` and `"https://"` to watch both error paths fire.
7. Only now try `--live` on a URL of your own. The offline path proved your
   logic; the live path proves your wiring.

## The Solution

```python
"""problem-06-tiny-url-shortener-client-solution.py — wrap the is.gd API.

A tiny client for is.gd (https://is.gd), a free, keyless URL shortener. Give it
a long URL and it hands back a short one:

    python problem-06-tiny-url-shortener-client-solution.py
    python problem-06-tiny-url-shortener-client-solution.py https://example.com/a
    python problem-06-tiny-url-shortener-client-solution.py https://example.com/a --live

is.gd's endpoint is::

    GET https://is.gd/create.php?format=json&url=<long-url>

and it answers ``{"shorturl": "https://is.gd/xxxxx"}`` when it succeeds, or
``{"errorcode": N, "errormessage": "..."}`` when it will not shorten the URL --
and it does that with a ``200 OK`` either way, so ``raise_for_status()`` alone
never sees the failure. Reading the *body* is part of the job.

This shipped answer replays **recorded** replies by default -- real is.gd
bodies captured on 2026-08-21 -- so the download prints the same short URLs
every time and needs no network. The seam is the ``fetch`` argument to the
client: swap in ``fetch_recorded`` and the identical class runs offline; leave
it out and it calls the real API with a ``timeout=`` and ``raise_for_status()``.
Pass ``--live`` to shorten URLs for real.

Run it with no arguments and it walks through a worked example.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

import requests

CREATE_URL = "https://is.gd/create.php"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0

#: Anything that turns a long URL into the decoded JSON is.gd sent back.
Fetch = Callable[[str], dict[str, Any]]

#: Real is.gd replies captured on 2026-08-21, keyed by the URL that produced
#: them. Most are success documents; the last is the error document is.gd
#: returns (with a 200 status) when it refuses a URL, so the offline demo can
#: exercise the failure path without a network.
RECORDED: dict[str, dict[str, Any]] = {
    "https://www.codecrunchworldwide.com/": {
        "shorturl": "https://is.gd/ccw_home",
    },
    "https://github.com/CODECRUNCHWORLDWIDE": {
        "shorturl": "https://is.gd/ccw_org",
    },
    "https://open-meteo.com/en/docs": {
        "shorturl": "https://is.gd/ccw_meteo",
    },
    # is.gd answers 200 OK with this body when the URL is unusable.
    "https://": {
        "errorcode": 1,
        "errormessage": "Please enter a valid URL to shorten",
    },
}


class ShortenError(Exception):
    """Raised when a URL cannot be shortened, for any reason.

    Everything the caller needs to read is in ``str(exc)``. The original cause,
    where the failure was a network error, stays reachable as ``__cause__``.
    """


def fetch_recorded(long_url: str) -> dict[str, Any]:
    """Answer one shorten request from RECORDED, touching no network.

    Args:
        long_url: The URL that would have been sent to is.gd.

    Returns:
        The decoded JSON document is.gd returned for it.

    Raises:
        RuntimeError: nothing was recorded for this URL. Nothing is wrong with
            your code; the recording is small. Re-run with --live.
    """
    recorded = RECORDED.get(long_url)
    if recorded is None:
        raise RuntimeError(f"no recorded reply for {long_url!r}; re-run with --live")
    return recorded


class URLShortenerClient:
    """A small client for the is.gd shortening API.

    One ``requests.Session`` is created per client so that repeated calls reuse
    a single TCP connection, and it is closed by :meth:`close` or by leaving a
    ``with`` block. Successful results are cached, so shortening the same URL
    twice in one session sends only one request.

    The ``fetch`` argument is the seam that makes this class testable and lets
    the shipped answer run offline: pass :func:`fetch_recorded` (or any callable
    that maps a URL to a decoded body) and no network is touched. Leave it out
    and the client calls is.gd for real.
    """

    def __init__(self, *, timeout: float = TIMEOUT_SECONDS, fetch: Fetch | None = None):
        """Build a client.

        Args:
            timeout: Seconds to wait on the network before giving up.
            fetch: How to reach is.gd. None means the real API, over a fresh
                Session; anything else is used as-is and no Session is built.
        """
        self._timeout = timeout
        self._cache: dict[str, str] = {}
        if fetch is None:
            self._session: requests.Session | None = requests.Session()
            self._session.headers.update({"User-Agent": USER_AGENT})
            self._fetch: Fetch = self._fetch_live
        else:
            self._session = None
            self._fetch = fetch

    def _fetch_live(self, long_url: str) -> dict[str, Any]:
        """GET is.gd for real and return the decoded body.

        Args:
            long_url: The URL to shorten, sent through params= so it is encoded.

        Returns:
            The decoded JSON document.

        Raises:
            requests.exceptions.RequestException: the request failed at the
                network or HTTP level. shorten() turns this into a ShortenError.
        """
        assert self._session is not None  # the live path always has a session
        response = self._session.get(
            CREATE_URL,
            params={"format": "json", "url": long_url},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()

    def shorten(self, long_url: str) -> str:
        """Return a short URL for *long_url*.

        Args:
            long_url: An ``http://`` or ``https://`` URL.

        Returns:
            The shortened URL is.gd produced.

        Raises:
            ShortenError: the URL is not http(s), is.gd refused it, or the
                network could not be reached.
        """
        if not long_url.startswith(("http://", "https://")):
            raise ShortenError(
                f"long_url must start with http:// or https://, got {long_url!r}"
            )
        if long_url in self._cache:
            return self._cache[long_url]
        try:
            payload = self._fetch(long_url)
        except requests.exceptions.RequestException as exc:
            raise ShortenError(f"could not reach is.gd: {exc}") from exc
        if "shorturl" not in payload:
            message = payload.get("errormessage", "is.gd returned no short URL")
            raise ShortenError(f"is.gd refused the URL: {message}")
        short = payload["shorturl"]
        self._cache[long_url] = short
        return short

    def close(self) -> None:
        """Close the underlying Session, if there is one.

        Safe to call more than once. After close() the client should not be
        used again.
        """
        if self._session is not None:
            self._session.close()
            self._session = None

    def __enter__(self) -> URLShortenerClient:
        """Enter a ``with`` block, returning this client."""
        return self

    def __exit__(self, *exc_info: object) -> None:
        """Leave a ``with`` block, closing the Session."""
        self.close()


def demo() -> int:
    """Walk through a worked example against the recording.

    Returns:
        The process exit code.
    """
    print("--- replaying is.gd replies recorded on 2026-08-21; pass --live for real ---")

    sent = 0

    def counting_fetch(long_url: str) -> dict[str, Any]:
        nonlocal sent
        sent += 1
        return fetch_recorded(long_url)

    urls = [
        "https://www.codecrunchworldwide.com/",
        "https://github.com/CODECRUNCHWORLDWIDE",
        "https://open-meteo.com/en/docs",
    ]
    with URLShortenerClient(fetch=counting_fetch) as client:
        for long_url in urls:
            print(f"{client.shorten(long_url)}  <-  {long_url}")

        # The same URL again: served from the cache, so no second request.
        repeat = client.shorten(urls[0])
        print(f"{repeat}  <-  {urls[0]}  (from cache, not re-sent)")

        # A URL that is not http(s) is rejected before any request goes out.
        try:
            client.shorten("mailto:hi@example.com")
        except ShortenError as err:
            print(f"rejected locally: {err}")

        # is.gd answers 200 with an error document for a URL it will not take.
        try:
            client.shorten("https://")
        except ShortenError as err:
            print(f"caught ShortenError: {err}")

    print()
    print(f"requests sent to is.gd: {sent} (the repeat was served from cache)")
    return 0


def main(argv: list[str] | None = None, *, fetch: Fetch | None = None) -> int:
    """Shorten the URLs named on the command line.

    Args:
        argv: Arguments after the program name. None means sys.argv[1:].
        fetch: How to reach is.gd. None means "decide from --live".

    Returns:
        The process exit code. 0 on success, 2 on a handled failure.
    """
    parser = argparse.ArgumentParser(description="Shorten URLs with the is.gd API.")
    parser.add_argument("urls", nargs="*", help="one or more URLs to shorten")
    parser.add_argument("--live", action="store_true", help="call the real is.gd API")
    args = parser.parse_args(argv)

    get = fetch or (None if args.live else fetch_recorded)

    exit_code = 0
    with URLShortenerClient(fetch=get) as client:
        for long_url in args.urls:
            try:
                print(f"{client.shorten(long_url)}  <-  {long_url}")
            except ShortenError as err:
                print(f"Error: {err}", file=sys.stderr)
                exit_code = 2
    return exit_code


if __name__ == "__main__":
    raise SystemExit(demo() if len(sys.argv) == 1 else main())
```

**The seam is one argument, and it changes everything about testing.** The
client never says `requests.get` in its own body — it says `self._fetch`. When
you build it normally, `self._fetch` is the real network call. When the demo
builds it with `fetch=counting_fetch`, the exact same `shorten` runs against
recorded data. No mock library, no monkey-patching, no network. The rule that
made Problem 3 testable against a fake clock makes this one testable against a
fake internet: **name the thing you cannot control, and let a caller replace
it.**

**Two failure channels, and the code has a check for each.** `raise_for_status()`
handles the HTTP-level failures — a `500`, a `404`, a connection that dropped.
But is.gd reports "I won't shorten this" with a cheerful `200 OK` and an
`errorcode` in the body, so there is a second check: `if "shorturl" not in
payload`. Miss that one and a refused URL sails straight through as a success,
and your caller gets a `KeyError` later when it reaches for a `shorturl` that
was never there. The lesson generalises: an HTTP `200` means "the server
answered", not "the server said yes".

**Everything collapses into one `ShortenError`.** A timeout, a DNS failure, a
dropped connection — `requests` raises five or six different classes for these,
all under `requests.exceptions.RequestException`. `shorten` catches that one
base class and re-raises `ShortenError`, so the caller writes a single
`except ShortenError`. The `from exc` keeps the original exception attached as
`__cause__`, so a traceback still shows the real cause while your callers stay
simple.

**The cache is four lines and it earns them.** A lookup at the top
(`if long_url in self._cache`), a store at the bottom
(`self._cache[long_url] = short`). Errors are never cached — the store comes
*after* every check has passed — so a URL that failed once can be retried, while
a URL that succeeded is never sent twice. The demo's counter proves it: six
calls to `shorten`, four requests actually sent.

**The Session is opened once and closed on purpose.** One `Session` per client
means every `shorten` reuses the same underlying connection instead of dialing
from scratch. That connection is a real operating-system socket, so it has to be
handed back: `close()` does it, and `__enter__`/`__exit__` make `with` do it for
you even if the block raises halfway through. Setting `self._session = None`
after closing makes a second `close()` harmless.

## Run it

Copy the worked answer on this page into `problem-06-tiny-url-shortener-client.py` and run it:

```bash
python problem-06-tiny-url-shortener-client.py
```

It needs nothing installed but `requests`, and by default it never touches the
network — it replays the recorded is.gd replies. Point it at a URL of your own
and add `--live` to shorten it for real:

```bash
python problem-06-tiny-url-shortener-client.py https://example.com/some/long/path --live
```

The `-solution` in the filename keeps it from colliding with your own
`hw06_url_shortener.py`.

## Common bugs to catch

- **Trusting the status code and stopping there.** `raise_for_status()` passes,
  `.json()` succeeds, and then `payload["shorturl"]` raises `KeyError` because
  the body was an error document. The failure lands several lines from its
  cause. The fix is the `if "shorturl" not in payload` check, before you touch
  the key.

- **Building the URL by hand instead of using `params=`.**

  ```python
  self._session.get(f"{CREATE_URL}?format=json&url={long_url}", ...)
  ```

  A long URL almost always contains `&`, `?` or `=` in its own query string, and
  pasted raw into another query string it corrupts the request — is.gd sees a
  truncated or mangled URL. `params={"url": long_url}` lets `requests`
  percent-encode it correctly. This is the same edge that Exercise 1 warned
  about.

- **No `timeout=`.** The one run where is.gd is slow, your program hangs with no
  error and no output. Nothing in the code *looks* wrong, which is exactly why a
  missing timeout is so hard to find later.

- **Catching `Exception` instead of `RequestException`.** A bare
  `except Exception` around the fetch also swallows the `KeyError`, the
  `AttributeError` from a typo, and anything else — turning a bug in your own
  code into a misleading `ShortenError` about the network. Catch the narrow base
  class that means "the request failed".

- **Caching the error.** If you store the result *before* checking for
  `shorturl`, a URL that failed once is remembered as a failure forever in that
  session. Store only after every check has passed.

- **Never closing the Session.** It usually works, then on some runs Python
  prints `ResourceWarning: unclosed <socket.socket ...>` as it shuts down. The
  `with` block is the fix, and it is why the class is a context manager.

## Under the hood

<details>
<summary>Under the hood — why a real API hides "no" inside a 200 body</summary>

It feels wrong that is.gd answers a refused URL with `200 OK`. Surely a refusal
is a `400 Bad Request`? Both designs exist in the wild, and the split is worth
understanding.

The HTTP status code describes **the transport**: did the request reach the
server, was it understood, did the server manage to produce a response. A
`200` means "yes, here is a response." The *content* of that response — whether
the thing you asked for could be done — is the API's own business, and many
APIs choose to report application-level outcomes in the body with a consistent
`200`. That way a client has exactly one place to look for the answer (the body)
and does not have to map a sprawl of status codes onto meanings the HTTP spec
never intended.

Other APIs do the opposite and lean hard on status codes — GitHub returns `404`
for a missing repo, `422` for a validation error, `403` for rate limiting. Both
are defensible. What is *not* defensible is a client that assumes one style. The
robust habit, and the one this problem drills, is to check **both**: let
`raise_for_status()` handle the transport failures, then inspect the body for
the application's own success signal. You cannot know from the outside which
style an API uses until you have read its docs — and sometimes not even then.

The deeper point: an HTTP `200` is the server saying "I heard you and I
answered", which is a smaller promise than "I did what you wanted". Treating the
two as the same is one of the most common ways real integrations break.

</details>

<details>
<summary>Under the hood — what a Session actually reuses, and why it is faster</summary>

`requests.get(url)` and `session.get(url)` look identical, and for one call they
nearly are. The difference shows up on the second call.

Opening an `https://` connection is not free. Before a single byte of your
request is sent, the client and server perform a **TCP handshake** (three
messages back and forth to agree the connection exists) and then a **TLS
handshake** (several more, to agree on encryption keys and check the
certificate). On a connection across the world that can be a hundred
milliseconds or more, spent before your request even starts.

A `Session` keeps that connection open — HTTP calls it *keep-alive* — and reuses
it for the next request to the same host. So the first `shorten` pays for the
handshakes and every one after it does not. For a program shortening a list of
fifty URLs, that is fifty handshakes saved. It is also gentler on the server,
which is not opening and tearing down a connection for each call.

That reuse is exactly why the Session must be closed. The open connection is
backed by a real socket, an operating-system resource with a limited supply. A
program that builds Sessions and drops them without closing leaks sockets, and
on a long-running service that eventually becomes an error you will find very
confusing — "too many open files" — a long way from the code that caused it. A
resource you open, you close; `with` is how Python makes that automatic.

```python
with URLShortenerClient() as client:
    client.shorten("https://example.com")
# the Session's connection is closed here, even if shorten raised
```

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and prints its short URLs.
- [ ] `shorten` rejects a non-`http(s)` URL with `ShortenError`, before any
      request.
- [ ] A refused URL (an is.gd error document) raises `ShortenError`, not
      `KeyError`.
- [ ] The same URL shortened twice sends only one request.
- [ ] `with URLShortenerClient() as c:` closes the Session on exit.
- [ ] Every live request passes `timeout=` and calls `raise_for_status()`.
- [ ] One `Session` per client, with a `User-Agent` set on it.
- [ ] Type hints and a docstring on every method.
- [ ] Committed with a message like `Add Week 8 homework 6: URL shortener`.

## Stretch

- Add an `expand(short_url: str) -> str` method wrapping is.gd's
  `https://is.gd/forward.php?format=json&shorturl=<code>` endpoint, which turns
  a short URL back into the long one. Record a reply for it and test it offline
  first, exactly as `shorten` is tested.

- Make the cache bounded. Right now it grows without limit; a long-running
  program could hold millions of entries. Cap it at, say, 128 entries and evict
  the oldest — or read the source of
  [`functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache)
  and write one sentence on why a method is awkward to decorate with it directly.

- Add a retry with backoff for the *transport* failures only, reusing Exercise
  5's `Retry` policy on an `HTTPAdapter`. Be careful: a retry is safe for a
  timeout, but must never fire on a refused-URL error document, because that is
  not a transient failure — is.gd will refuse it every time.

Week 8 is done. Next is
[Week 9 — Web Development with Flask](../../week-09-web-development-flask/), where
you cross to the other side of every request you made this week and build the
server that answers it.
