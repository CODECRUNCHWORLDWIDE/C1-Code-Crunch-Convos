"""exercise-01-first-get-request-solution.py — send one GET and read the response.

The exercise calls https://httpbin.org/get, a mirror that answers with a JSON
description of the request it just received, and then prints the parts of the
``Response`` that matter.

This shipped answer does not call httpbin. It replays a **recorded** reply --
a real body captured from that endpoint and pasted in below -- so the download
prints the same six lines on a plane, on a locked-down office network, and on a
day when httpbin is returning 503 to everybody.

The switch is one argument. ``main()`` passes ``send_recorded``; pass
``send_live`` instead and the very same ``probe``, ``describe`` and
``echoed_args`` call the real server::

    response = probe(ECHO_URL, {...}, send=send_live)

Run it with::

    python exercise-01-first-get-request-solution.py
"""

from __future__ import annotations

import io
from datetime import timedelta
from typing import Any, Callable, NamedTuple
from urllib.parse import urlencode

import requests

ECHO_URL = "https://httpbin.org/get"
MISSING_URL = "https://httpbin.org/status/404"
TIMEOUT_SECONDS = 5.0

# Requirement 3: put your own name here.
STUDENT_NAME = "ada"


class Recorded(NamedTuple):
    """One saved reply, kept exactly as the server sent it."""

    status_code: int
    reason: str
    content_type: str
    body: str
    elapsed_seconds: float


#: Real replies captured from httpbin.org. The bodies are byte-for-byte what
#: came back, with two edits that are named rather than hidden: the ``origin``
#: field held this machine's public IP address and now holds the documentation
#: address 203.0.113.7, and the whole document was reformatted with
#: ``json.dumps(indent=2)`` because httpbin pads its output with trailing
#: spaces that a text editor would quietly eat.
RECORDED: dict[str, Recorded] = {
    ECHO_URL: Recorded(
        status_code=200,
        reason="OK",
        content_type="application/json",
        body=(
            "{\n"
            '  "args": {\n'
            '    "student": "ada",\n'
            '    "week": "8"\n'
            "  },\n"
            '  "headers": {\n'
            '    "Accept": "*/*",\n'
            '    "Accept-Encoding": "gzip, deflate",\n'
            '    "Host": "httpbin.org",\n'
            '    "User-Agent": "python-requests/2.32.3"\n'
            "  },\n"
            '  "origin": "203.0.113.7",\n'
            '  "url": "https://httpbin.org/get?student=ada&week=8"\n'
            "}\n"
        ),
        elapsed_seconds=0.412,
    ),
    MISSING_URL: Recorded(
        status_code=404,
        reason="NOT FOUND",
        content_type="text/html; charset=utf-8",
        body="",
        elapsed_seconds=0.208,
    ),
}

#: Anything that can send one GET and hand back a Response. There are two in
#: this file: one that uses the network and one that does not.
Sender = Callable[[str, dict[str, str]], requests.Response]


def send_live(url: str, params: dict[str, str]) -> requests.Response:
    """Send one real GET over the network and return the Response.

    Args:
        url: Absolute https URL to call.
        params: Query-string pairs. requests URL-encodes them for you.

    Returns:
        The Response object, whatever its status code.
    """
    return requests.get(url, params=params, timeout=TIMEOUT_SECONDS)


def send_recorded(url: str, params: dict[str, str]) -> requests.Response:
    """Rebuild a saved reply as a real Response, touching no network.

    Args:
        url: One of the keys of RECORDED.
        params: Query-string pairs, used only to rebuild ``response.url``.

    Returns:
        A genuine requests.Response object holding the recorded reply.
    """
    recorded = RECORDED[url]
    response = requests.Response()
    response.status_code = recorded.status_code
    response.reason = recorded.reason
    response.url = f"{url}?{urlencode(params)}" if params else url
    response.encoding = "utf-8"
    response.headers["content-type"] = recorded.content_type
    response.raw = io.BytesIO(recorded.body.encode("utf-8"))
    response.elapsed = timedelta(seconds=recorded.elapsed_seconds)
    return response


def probe(
    url: str, params: dict[str, str], *, send: Sender = send_live
) -> requests.Response:
    """Send one GET and return the Response, whatever its status code.

    Args:
        url: Absolute https URL to call.
        params: Query-string pairs. requests URL-encodes them for you.
        send: How to send it. Defaults to the real network.

    Returns:
        The Response object. This function does not raise on 4xx or 5xx.
    """
    return send(url, params)


def describe(response: requests.Response) -> None:
    """Print status, content type, elapsed seconds, and the final URL.

    Args:
        response: Any Response, live or replayed.
    """
    print(response.status_code, response.reason)
    print("content-type:", response.headers["content-type"])
    print(f"elapsed: {response.elapsed.total_seconds():.3f}s")
    print("url:", response.url)


def echoed_args(response: requests.Response) -> dict[str, Any]:
    """Return the "args" object httpbin echoed back to us.

    Args:
        response: A Response whose body is httpbin's echo document.

    Returns:
        The parsed ``args`` object. Every value in it is a string.
    """
    return response.json()["args"]


def main() -> None:
    """Probe the echo endpoint, then prove raise_for_status() bites."""
    print("--- replaying recorded replies; pass send=send_live to go online ---")

    response = probe(
        ECHO_URL, {"student": STUDENT_NAME, "week": "8"}, send=send_recorded
    )
    response.raise_for_status()
    describe(response)
    print("echoed args:", echoed_args(response))

    missing = probe(MISSING_URL, {}, send=send_recorded)
    try:
        missing.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        print(exc)


if __name__ == "__main__":
    main()
