"""Exercise 01 — Your first GET request.

GOAL
----
Send a single HTTP GET request to https://httpbin.org/get and print:
  1. The HTTP status code.
  2. The 'url' field of the JSON response body (httpbin echoes back the
     URL you hit, which lets you verify the request worked).

WHY THIS API?
-------------
httpbin.org is a free public service designed for testing HTTP clients.
No signup, no key, no rate limit worth worrying about. Read its docs at
<https://httpbin.org/>.

EXPECTED OUTPUT (yours may differ in the IP shown):

    status_code: 200
    you reached: https://httpbin.org/get

KEY CONCEPTS
------------
- `requests.get(url, timeout=...)` returns a `Response` object.
- `Response.status_code` is the integer HTTP status code (e.g. 200).
- `Response.json()` parses the response body as JSON and returns it.
- Always set `timeout=`; a hung process is worse than a failed one.

Reference: https://requests.readthedocs.io/en/latest/user/quickstart/
"""

from __future__ import annotations

import requests


URL = "https://httpbin.org/get"


def main() -> None:
    # Send the request. timeout=5 means "give up after 5 seconds".
    response = requests.get(URL, timeout=5)

    # Convert any 4xx/5xx into an exception so we fail loudly.
    response.raise_for_status()

    # Pull the parsed JSON body out of the response.
    body: dict = response.json()

    # Print the two things the exercise asks for.
    print(f"status_code: {response.status_code}")
    print(f"you reached: {body['url']}")


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────────────────────────────────
# Hints
# ─────────────────────────────────────────────────────────────────────────
# 1. If you get `ModuleNotFoundError: No module named 'requests'`,
#    run `python -m pip install requests` and try again.
# 2. If `body['url']` raises `KeyError`, print `body` first to inspect
#    the actual shape of the response.
# 3. `requests.get(...)` without `timeout=` will hang forever if the
#    server is unreachable. Get into the habit of always passing it.
