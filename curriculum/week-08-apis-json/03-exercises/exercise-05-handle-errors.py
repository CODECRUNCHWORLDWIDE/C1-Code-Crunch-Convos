"""Exercise 05 — A robust fetcher with timeouts, retries, and a custom exception.

GOAL
----
Build a `fetch_json(url)` function that behaves correctly under every
common network failure:

  - times out after N seconds,
  - retries idempotent failures (5xx, 429) with exponential backoff,
  - converts every failure into a single, well-named exception
    (`FetchError`) the caller can catch.

WHY?
----
Real-world HTTP code is mostly error handling. This is the function you
will copy/paste into project after project for the rest of your career.

We test against httpbin's `/status/{code}` endpoint, which lets us
trigger any status we want on demand:

  https://httpbin.org/status/200   -> 200 OK (success)
  https://httpbin.org/status/404   -> 404 Not Found (will not retry)
  https://httpbin.org/status/503   -> 503 Service Unavailable (will retry)

EXPECTED OUTPUT (the 503 retries take a few seconds — that is the
exponential backoff doing its job):

    Demo 1: hitting /status/200 (success)
      OK: got status 200
    Demo 2: hitting /status/404 (no retry; permanent client error)
      caught FetchError: 404 Client Error: NOT FOUND for url: ...
    Demo 3: hitting /status/503 (retries with backoff, then fails)
      caught FetchError: HTTPSConnectionPool... Max retries exceeded...

KEY CONCEPTS
------------
- Custom exception classes (week 6 recap).
- `requests.adapters.HTTPAdapter` + `urllib3.util.retry.Retry`.
- Single `try`/`except` at the top of the call stack.

References:
  https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry
  https://requests.readthedocs.io/en/latest/user/advanced/#transport-adapters
"""

from __future__ import annotations

from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class FetchError(Exception):
    """Raised when `fetch_json` cannot get a usable JSON response."""


def make_session(*, total_retries: int = 3, backoff: float = 1.0) -> requests.Session:
    """Build a Session that retries transient failures with backoff."""
    retry = Retry(
        total=total_retries,
        backoff_factor=backoff,           # waits 0, 2, 4, 8, ... seconds
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],  # idempotent only (see lecture 1)
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.headers.update({"User-Agent": "code-crunch-bootcamp/1.0"})
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_json(
    url: str,
    *,
    session: requests.Session | None = None,
    timeout: float = 5.0,
) -> dict[str, Any] | list[Any]:
    """Fetch `url` and return parsed JSON.

    Raises:
        FetchError: on any network failure, timeout, 4xx/5xx, or invalid JSON.
    """
    own_session = session is None
    if own_session:
        session = make_session()

    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        # An empty body would make .json() fail; httpbin /status returns
        # an empty body for non-200, but raise_for_status() already caught
        # those above, so we are safe here for the success path.
        if not response.content:
            return {}
        return response.json()
    except requests.exceptions.RequestException as exc:
        # ConnectionError, Timeout, HTTPError, TooManyRedirects, ...
        raise FetchError(str(exc)) from exc
    except ValueError as exc:
        # JSONDecodeError is a subclass of ValueError
        raise FetchError(f"response was not valid JSON: {exc}") from exc
    finally:
        if own_session:
            session.close()


# ─────────────────────────────────────────────────────────────────────────
# Demos
# ─────────────────────────────────────────────────────────────────────────


def main() -> None:
    # httpbin's /status/{code} returns that code with an empty body.
    # We use /get for the success demo so we have JSON to parse.
    success_url = "https://httpbin.org/get"
    not_found_url = "https://httpbin.org/status/404"
    flaky_url = "https://httpbin.org/status/503"

    print("Demo 1: hitting /get (success)")
    try:
        data = fetch_json(success_url)
        print(f"  OK: got JSON with keys {sorted(data.keys())[:3]} ...")
    except FetchError as exc:
        print(f"  unexpected FetchError: {exc}")

    print("Demo 2: hitting /status/404 (no retry; permanent client error)")
    try:
        fetch_json(not_found_url)
    except FetchError as exc:
        print(f"  caught FetchError: {exc}")

    print("Demo 3: hitting /status/503 (retries with backoff, then fails)")
    print("  (this will take a few seconds — that is exponential backoff)")
    try:
        # Tighten retries so the demo finishes within ~10 seconds.
        fast_session = make_session(total_retries=2, backoff=0.5)
        try:
            fetch_json(flaky_url, session=fast_session)
        finally:
            fast_session.close()
    except FetchError as exc:
        print(f"  caught FetchError: {exc}")


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────────────────────────────────
# Hints
# ─────────────────────────────────────────────────────────────────────────
# 1. Notice that 4xx errors are NOT retried — `status_forcelist` only
#    lists 429 plus the 5xx family. Retrying 404 is pointless (and might
#    be considered abusive by the API owner).
# 2. The `raise ... from exc` form preserves the original traceback, so
#    a debugger / log can see exactly what went wrong underneath.
# 3. The custom `FetchError` class lets callers do:
#        try: data = fetch_json(url)
#        except FetchError: ...
#    without importing `requests.exceptions`. That decoupling matters in
#    big code bases where you may swap requests for httpx later.
