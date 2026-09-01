"""exercise-03-post-data-solution.py — POST a JSON body and verify the echo.

The exercise posts a small build report to https://httpbin.org/post, which
answers with a JSON description of the request it just received, and then asks
the only question that matters: did the object come back equal to the object
that went out?

This shipped answer does not call httpbin. It replays a **recorded** echo -- a
real document captured from that endpoint -- and fills in the body fields the
way httpbin fills them in: by encoding what it was handed and decoding it
again. So the round trip on this page is a real round trip through JSON. The
only thing missing is the wire.

The switch is one argument. ``main()`` passes ``post=post_recorded``; pass
``post=post_live``, or leave the argument off, and the very same
``submit_json``, ``submit_form`` and ``report_round_trip`` call httpbin.

Run it with::

    python exercise-03-post-data-solution.py
"""

from __future__ import annotations

import json
from typing import Any, Callable
from urllib.parse import parse_qsl, urlencode

import requests

POST_URL = "https://httpbin.org/post"
TIMEOUT_SECONDS = 5.0

# Requirement 6: with "tags" as a tuple the round trip printed False. JSON has
# no tuple type, so ("python", "http") went out as an array and came back a
# list, and ("python", "http") != ["python", "http"]. The third section of
# main() below runs that experiment rather than describing it.
REPORT: dict[str, Any] = {
    "runner": "ada-laptop",
    "suite": "week-08-smoke",
    "passed": 12,
    "failed": 0,
    "green": True,
    "notes": None,
    "tags": ["python", "http"],
}

#: A real echo document captured from httpbin.org/post, with two named edits:
#: the "origin" field held this machine's public IP address and now holds the
#: documentation address 203.0.113.7, and the per-request X-Amzn-Trace-Id
#: header was dropped because a stale trace id means nothing. The body fields
#: -- data, json, form -- are filled in per call by post_recorded, exactly as
#: the real server fills them in.
RECORDED_ECHO = (
    '{"args": {}, "data": "", "files": {}, "form": {}, '
    '"headers": {"Accept": "*/*", "Accept-Encoding": "gzip, deflate", '
    '"Content-Length": "0", "Content-Type": "", "Host": "httpbin.org", '
    '"User-Agent": "python-requests/2.32.3"}, '
    '"json": null, "origin": "203.0.113.7", '
    '"url": "https://httpbin.org/post"}'
)

#: Anything that can POST one body and hand back the parsed echo document. The
#: two body arguments are exclusive: exactly one of them is not None, which is
#: the whole point the exercise is making.
Poster = Callable[[str, dict[str, Any] | None, dict[str, Any] | None], dict[str, Any]]


def post_live(
    url: str,
    json_body: dict[str, Any] | None,
    form_body: dict[str, Any] | None,
) -> dict[str, Any]:
    """POST one body over the network and return the parsed reply.

    Args:
        url: Absolute https URL to post to.
        json_body: An object to send as a JSON document, or None.
        form_body: Flat pairs to send form-encoded, or None.

    Returns:
        The decoded reply body.

    Raises:
        requests.HTTPError: the server answered 4xx or 5xx.
    """
    response = requests.post(
        url, json=json_body, data=form_body, timeout=TIMEOUT_SECONDS
    )
    response.raise_for_status()
    return response.json()


def post_recorded(
    url: str,
    json_body: dict[str, Any] | None,
    form_body: dict[str, Any] | None,
) -> dict[str, Any]:
    """Answer from RECORDED_ECHO, encoding and decoding the body for real.

    The encoding is not faked. A JSON body goes through json.dumps and comes
    back through json.loads, which is what requests and httpbin do between
    them, so a value JSON cannot represent still changes on the way through. A
    form body goes through urlencode and parse_qsl, which is why every value
    comes back as text.

    Args:
        url: Ignored; present so the signature matches post_live.
        json_body: An object to send as a JSON document, or None.
        form_body: Flat pairs to send form-encoded, or None.

    Returns:
        The echo document, key-sorted the way httpbin sorts it.
    """
    echo = json.loads(RECORDED_ECHO)
    if json_body is not None:
        raw = json.dumps(json_body, allow_nan=False)
        echo["data"] = raw
        echo["json"] = json.loads(raw)
        echo["headers"]["Content-Type"] = "application/json"
    else:
        raw = urlencode(form_body or {})
        echo["form"] = dict(parse_qsl(raw))
        echo["headers"]["Content-Type"] = "application/x-www-form-urlencoded"
    echo["headers"]["Content-Length"] = str(len(raw))
    # httpbin re-serialises its reply with the keys sorted; do the same so the
    # printed dicts match what the live server would have shown you.
    return json.loads(json.dumps(echo, sort_keys=True))


def submit_json(payload: dict[str, Any], *, post: Poster = post_live) -> dict[str, Any]:
    """POST payload as a JSON body; return the parsed echo document.

    Args:
        payload: Any object made only of JSON-native types.
        post: How to send it. Defaults to the real network.

    Returns:
        httpbin's description of the request it received.
    """
    return post(POST_URL, payload, None)


def submit_form(payload: dict[str, Any], *, post: Poster = post_live) -> dict[str, Any]:
    """POST the same payload form-encoded, so you can see the difference.

    Args:
        payload: Flat key/value pairs; form encoding cannot nest.
        post: How to send it. Defaults to the real network.

    Returns:
        httpbin's description of the request it received.
    """
    return post(POST_URL, None, payload)


def report_round_trip(echo: dict[str, Any], sent: dict[str, Any]) -> None:
    """Print what the server understood, and whether it matches what we sent.

    Args:
        echo: The parsed echo document.
        sent: The object we handed to json=.
    """
    print("content-type sent:", echo["headers"]["Content-Type"])
    print("raw body:         ", echo["data"])
    print("parsed by server: ", echo["json"])
    print("round trip equal: ", echo["json"] == sent)


def main(*, post: Poster = post_live) -> None:
    """Submit the report three ways: as JSON, form-encoded, and with a tuple.

    Args:
        post: How to send each request. Defaults to the real network.
    """
    print("--- json= ---")
    report_round_trip(submit_json(REPORT, post=post), REPORT)

    print("--- data= ---")
    flat = {"runner": REPORT["runner"], "passed": REPORT["passed"]}
    echo = submit_form(flat, post=post)
    print("content-type:", echo["headers"]["Content-Type"])
    print("json field:  ", echo["json"])
    print("form field:  ", echo["form"])

    print("--- json=, with tags as a tuple ---")
    tupled = {**REPORT, "tags": ("python", "http")}
    report_round_trip(submit_json(tupled, post=post), tupled)


if __name__ == "__main__":
    print("--- replaying a recorded echo; pass post=post_live to go online ---")
    main(post=post_recorded)
