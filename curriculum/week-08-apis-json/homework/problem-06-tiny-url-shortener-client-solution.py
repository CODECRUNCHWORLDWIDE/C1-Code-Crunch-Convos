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
