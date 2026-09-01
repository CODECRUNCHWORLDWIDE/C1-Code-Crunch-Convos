"""exercise-05-handle-errors-solution.py — turn every network failure into one exception.

The exercise builds one public function and one public exception.
``fetch_json(url)`` returns parsed JSON or raises ``ApiError``. That is the
whole contract, and its value is what it hides: callers never import requests
and never learn that a 503 was retried three times.

This shipped answer does not call httpbin. It replays the **outcomes** -- the
success, the 404, the exhausted retry and the read timeout -- through two
recorded stand-ins, one for a retrying Session and one for a plain get. The
retry adapter in ``make_session`` is real code and is what runs when you pass
``--live``; the recording replays what that adapter produces, without the
waiting.

Recording this one buys two things. It finishes instantly instead of spending
ten to twenty-five seconds in backoff waits and a deliberate timeout. And it
still demonstrates all four outcomes on a day when httpbin -- which is free,
and busy -- is handing out 503 to everybody, which would otherwise turn case 1
into a fifth kind of failure.

Run it with::

    python exercise-05-handle-errors-solution.py
    python exercise-05-handle-errors-solution.py --live
"""

from __future__ import annotations

import io
import sys
from typing import Any, Callable

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 5.0
RETRY_TOTAL = 3
BACKOFF_FACTOR = 0.5

ECHO_URL = "https://httpbin.org/get"
NOT_FOUND_URL = "https://httpbin.org/status/404"
SERVER_ERROR_URL = "https://httpbin.org/status/503"
SLOW_URL = "https://httpbin.org/delay/5"

#: A real body captured from httpbin.org/get, trimmed to its four top-level
#: keys because the four key names are all this program prints. The "origin"
#: field held the capturing machine's public IP address and now holds the
#: documentation address 203.0.113.7.
RECORDED_ECHO = (
    '{"args": {}, "headers": {"Host": "httpbin.org"}, '
    '"origin": "203.0.113.7", "url": "https://httpbin.org/get"}'
)

#: Anything that can send one GET and hand back a Response. requests.get is
#: one. A Session's bound .get method is another. So are the two recorded
#: stand-ins below.
Getter = Callable[..., requests.Response]


class ApiError(Exception):
    """Raised when a URL could not be turned into JSON.

    The original requests exception stays reachable as __cause__.
    """

    def __init__(self, message: str, *, url: str) -> None:
        """Store the message and the URL that produced it.

        Args:
            message: What went wrong, in words a caller can print.
            url: The URL that was being fetched.
        """
        super().__init__(message)
        self.url = url


def make_session() -> requests.Session:
    """Return a Session that retries transient failures on GET only.

    Returns:
        A Session with a retry policy mounted on both http and https.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "code-crunch-bootcamp/1.0"})
    retry = Retry(
        total=RETRY_TOTAL,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def replay(url: str, status_code: int, reason: str, body: str) -> requests.Response:
    """Build a real Response object holding a recorded reply.

    Args:
        url: The URL this reply is pretending to have come from.
        status_code: The status code the server sent.
        reason: The reason phrase beside it, such as "NOT FOUND".
        body: The response body, as text.

    Returns:
        A genuine requests.Response. raise_for_status() and .json() work on it
        exactly as they would on one that arrived over the network.
    """
    response = requests.Response()
    response.status_code = status_code
    response.reason = reason
    response.url = url
    response.encoding = "utf-8"
    response.headers["content-type"] = "application/json"
    response.raw = io.BytesIO(body.encode("utf-8"))
    return response


def recorded_retrying_get(url: str, timeout: float = DEFAULT_TIMEOUT) -> requests.Response:
    """Stand in for a retrying Session.get, replaying the outcome for *url*.

    The 503 case raises immediately rather than waiting through the real
    backoff schedule. The exception it raises is the one the real adapter
    raises once its retries are spent.

    Args:
        url: One of the four URLs this exercise uses.
        timeout: Accepted and ignored; present so the signature matches.

    Returns:
        A recorded Response for the URLs that answer.

    Raises:
        requests.exceptions.RetryError: for the 503 URL.
        requests.exceptions.ReadTimeout: for the slow URL.
    """
    if url == ECHO_URL:
        return replay(url, 200, "OK", RECORDED_ECHO)
    if url == NOT_FOUND_URL:
        return replay(url, 404, "NOT FOUND", "")
    if url == SERVER_ERROR_URL:
        raise requests.exceptions.RetryError(
            "HTTPSConnectionPool(host='httpbin.org', port=443): Max retries "
            "exceeded with url: /status/503 (Caused by ResponseError('too many "
            "503 error responses'))"
        )
    raise requests.exceptions.ReadTimeout(
        f"HTTPSConnectionPool(host='httpbin.org', port=443): Read timed out. "
        f"(read timeout={timeout})"
    )


def recorded_bare_get(url: str, timeout: float = DEFAULT_TIMEOUT) -> requests.Response:
    """Stand in for a plain requests.get, with no retry adapter in the way.

    Args:
        url: One of the four URLs this exercise uses.
        timeout: Used in the timeout message, as the real one does.

    Returns:
        A recorded Response for the URLs that answer.

    Raises:
        requests.exceptions.ReadTimeout: for the slow URL.
    """
    if url == SLOW_URL:
        raise requests.exceptions.ReadTimeout(
            f"HTTPSConnectionPool(host='httpbin.org', port=443): Read timed "
            f"out. (read timeout={timeout})"
        )
    if url == SERVER_ERROR_URL:
        return replay(url, 503, "SERVICE UNAVAILABLE", "")
    return recorded_retrying_get(url, timeout)


def fetch_json(
    url: str,
    *,
    get: Getter = requests.get,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    """Fetch url and return parsed JSON.

    Args:
        url: Absolute URL to GET.
        get: How to send it. requests.get, a Session's .get, or a stand-in.
        timeout: Seconds to wait per attempt.

    Returns:
        The decoded JSON body.

    Raises:
        ApiError: for every failure. No requests exception ever escapes.
    """
    try:
        response = get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as exc:
        raise ApiError(f"no response within {timeout}s", url=url) from exc
    except requests.exceptions.RetryError as exc:
        raise ApiError(
            f"gave up after {RETRY_TOTAL} retries on a 5xx or 429 response",
            url=url,
        ) from exc
    except requests.exceptions.HTTPError as exc:
        raise ApiError(f"server said {exc}", url=url) from exc
    except requests.exceptions.RequestException as exc:
        raise ApiError(f"request failed: {exc}", url=url) from exc


def main(*, live: bool = False) -> None:
    """Run four calls: one success and three different failures.

    Args:
        live: True to call httpbin for real. False replays recorded outcomes.
    """
    if live:
        retrying: Getter = make_session().get
        bare: Getter = requests.get
    else:
        retrying = recorded_retrying_get
        bare = recorded_bare_get

    cases: list[tuple[str, Getter, float, str]] = [
        (ECHO_URL, retrying, DEFAULT_TIMEOUT, "retrying session"),
        (NOT_FOUND_URL, retrying, DEFAULT_TIMEOUT, "retrying session"),
        (
            SERVER_ERROR_URL,
            retrying,
            DEFAULT_TIMEOUT,
            "retrying session, waits 0s, 1s, 2s",
        ),
        (SLOW_URL, bare, 2.0, "bare get, timeout=2.0"),
    ]

    succeeded = 0
    failed = 0
    for number, (url, getter, timeout, mode) in enumerate(cases, start=1):
        print(f"[{number}/{len(cases)}] {url}  ({mode})")
        try:
            data = fetch_json(url, get=getter, timeout=timeout)
        except ApiError as err:
            failed += 1
            print(f"      ApiError: {err}")
        else:
            succeeded += 1
            print(f"      ok - top-level keys: {', '.join(sorted(data))}")

    print()
    print(
        f"{succeeded} succeeded, {failed} failed "
        f"- and no traceback reached the terminal."
    )


if __name__ == "__main__":
    going_live = "--live" in sys.argv[1:]
    if not going_live:
        print("--- replaying recorded outcomes; pass --live to call httpbin ---")
    main(live=going_live)
