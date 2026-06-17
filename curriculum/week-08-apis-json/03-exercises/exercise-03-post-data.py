"""Exercise 03 — POST a JSON body and verify the echo.

GOAL
----
Send a `POST` request to https://httpbin.org/post with a JSON body, then
verify that the response echoes back exactly what we sent.

WHY?
----
This is the foundational pattern for *creating* things in REST APIs:
- "Create a new issue"   -> POST /issues
- "Place an order"       -> POST /orders
- "Submit a form"        -> POST /forms
The body carries the data; the response usually returns the created
resource (httpbin echoes it back for testing purposes).

EXPECTED OUTPUT:

    status_code: 200
    echoed JSON:
    {
      "tags": ["python", "api"],
      "title": "Hello, Code Crunch!"
    }
    round-trip ok: True

KEY CONCEPTS
------------
- `requests.post(url, json=payload)` does three things at once:
    1. serializes `payload` to a JSON string,
    2. sets `Content-Type: application/json`,
    3. sends it as the request body.
- httpbin returns a top-level key `"json"` containing whatever JSON you
  sent. We compare it to our original payload to confirm the round trip.

Reference:
  https://requests.readthedocs.io/en/latest/user/quickstart/#more-complicated-post-requests
"""

from __future__ import annotations

import json
from typing import Any

import requests


URL = "https://httpbin.org/post"


def post_json(payload: dict[str, Any], *, timeout: float = 5.0) -> dict[str, Any]:
    """POST `payload` as JSON. Return the parsed response body."""
    response = requests.post(URL, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def main() -> None:
    payload: dict[str, Any] = {
        "title": "Hello, Code Crunch!",
        "tags": ["python", "api"],
    }

    body = post_json(payload)
    echoed = body["json"]  # httpbin places our JSON here

    print("status_code: 200")
    print("echoed JSON:")
    print(json.dumps(echoed, indent=2, sort_keys=True))
    print(f"round-trip ok: {echoed == payload}")


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────────────────────────────────
# Hints
# ─────────────────────────────────────────────────────────────────────────
# 1. `json=payload` (with the `=`) is keyword-only. Do NOT write
#    `requests.post(URL, payload)` — that would send the dict as
#    form-encoded data, which is a different `Content-Type` and the
#    server would put it under "form" instead of "json".
# 2. To see EVERY field httpbin returns, print the full `body`. You will
#    spot Content-Type, your request headers, your origin IP, and more.
# 3. The check `echoed == payload` uses dict equality, which ignores key
#    order. That is what we want — JSON object key order is not significant.
