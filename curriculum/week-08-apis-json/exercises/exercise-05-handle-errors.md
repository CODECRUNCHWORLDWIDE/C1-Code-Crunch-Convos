# Exercise 5 — When the Network Misbehaves

> **Topic:** timeouts, automatic retries, and one custom exception at the boundary
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md) sections 7, 8 and 10, plus [03 — Authentication and Secrets](../lecture-notes/03-authentication-and-secrets.md) section 8
> **Difficulty:** Medium
> **Target time:** 75 minutes
> **Why this one:** the four exercises before this one assumed the network works. It does not. Servers return 503 during a deploy, connections stall, name lookups blink. This is where you build the wrapper you will paste into both challenges and the mini-project — the one that turns every network failure into a single exception type your callers can actually handle.

## The Brief

You are building a **boundary**. On one side of it lives everything that can go
wrong with a network. On the other side lives the rest of your program, which
does not want to know.

The boundary is one function and one exception. `fetch_json(url)` returns
parsed JSON, or it raises `ApiError`. That is the entire contract, and its
value is what it *hides*: callers do not import `requests`, do not learn that a
`503` was retried three times, and do not have to remember that `requests` can
raise at least five different classes for what a person would just call "the
internet did not work".

`httpbin.org` will give you every failure mode on demand:

- `/get` succeeds.
- `/status/404` returns a client error, which should **never** be retried —
  asking again just asks the same wrong question.
- `/status/503` returns a server error, which **should** be retried, because a
  503 usually means "come back in a moment".
- `/delay/5` sleeps for five seconds, so a two-second timeout fires.

Your `main()` runs all four and prints one line for each. No traceback reaches
the terminal.

## Starter

Save this as `exercise-05-handle-errors.py` and fill in every `TODO`.

```python
"""exercise-05-handle-errors.py — turn every network failure into one exception."""

from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 5.0
RETRY_TOTAL = 3
BACKOFF_FACTOR = 0.5


class ApiError(Exception):
    """Raised when a URL could not be turned into JSON.

    The original requests exception stays reachable as __cause__.
    """

    def __init__(self, message: str, *, url: str) -> None:
        super().__init__(message)
        self.url = url


def make_session() -> requests.Session:
    """Return a Session that retries transient failures on GET only."""
    session = requests.Session()
    session.headers.update({"User-Agent": "code-crunch-bootcamp/1.0"})
    retry = Retry(
        total=RETRY_TOTAL,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
        respect_retry_after_header=True,
    )
    # TODO: mount an HTTPAdapter(max_retries=retry) on "https://" and "http://"
    return session


def fetch_json(
    url: str,
    *,
    session: requests.Session | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    """Fetch url and return parsed JSON.

    Pass session=None for a bare, retry-free request.

    Raises:
        ApiError: for every failure. No requests exception ever escapes.
    """
    caller = session or requests
    try:
        response = caller.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    # TODO: except requests.exceptions.Timeout       -> "no response within Xs"
    # TODO: except requests.exceptions.RetryError    -> "gave up after N retries"
    # TODO: except requests.exceptions.HTTPError     -> f"server said {exc}"
    # TODO: except requests.exceptions.RequestException -> "request failed: ..."
    # Each one: raise ApiError(message, url=url) from exc
    raise NotImplementedError


def main() -> None:
    """Run four calls: one success and three different failures."""
    session = make_session()
    cases: list[tuple[str, requests.Session | None, float]] = [
        ("https://httpbin.org/get", session, DEFAULT_TIMEOUT),
        ("https://httpbin.org/status/404", session, DEFAULT_TIMEOUT),
        ("https://httpbin.org/status/503", session, DEFAULT_TIMEOUT),
        ("https://httpbin.org/delay/5", None, 2.0),
    ]
    # TODO: loop with enumerate(cases, start=1); print the header line, then
    # try fetch_json(...) and print the keys, or catch ApiError and print it.
    # TODO: count successes and failures and print the summary line.


if __name__ == "__main__":
    main()
```

Four words before you begin.

**Retry.** Sending the same request again after it failed. Useful when the
failure was temporary and pointless when it was not, which is the whole
judgement call on this page.

**Backoff.** Waiting longer between each retry: nothing, then one second, then
two. Growing the gap is what stops a retry from becoming a stampede.

**Adapter.** The part of `requests` that actually sends bytes. `Session.mount`
lets you replace it for URLs starting with a given prefix, which is how a retry
policy gets attached to a `Session` at all.

**`raise ... from exc`.** A way of raising your own exception while keeping the
original attached to it, so nobody loses the real cause.

## Requirements

1. `make_session()` mounts the adapter on both `https://` and `http://`.
2. `fetch_json()` catches `Timeout`, `RetryError` and `HTTPError` with specific
   messages, and ends with `RequestException` as a final catch-all.
3. Every `raise ApiError(...)` uses `from exc`, so the original exception is
   reachable as `err.__cause__`.
4. `fetch_json()` never lets a `requests` exception escape, and never returns
   `None` on failure. Success returns data; failure raises.
5. `main()` prints a header line per case showing the URL and which mode it is
   using, then either the parsed top-level keys or the `ApiError` message.
6. The summary line reports how many succeeded and how many failed. The whole
   program exits with no traceback.

## Constraints

- **Order the `except` clauses narrowest first.** `Timeout`, `RetryError` and
  `HTTPError` are all subclasses of `RequestException`. Python takes the
  **first** clause that matches, so a `RequestException` handler above them
  swallows all three, and your specific messages become unreachable code — no
  error, no warning, just a generic message forever.

- **Keep `RequestException` last anyway.** It is the safety net and you need
  it. Exactly which class surfaces for a given failure depends on your
  `requests` and `urllib3` versions and on whether a retry adapter is mounted.
  Catch the base class last and that variation cannot hurt you.

- **Case 4 uses a bare get on purpose.** With no retry adapter in the way, the
  timeout surfaces as `requests.exceptions.ReadTimeout` and you see the raw
  behaviour. Put retries in front of it and the same stall is retried three
  times first — correct in production, confusing in a demo.

- **`allowed_methods=["GET", "HEAD"]` — do not add `POST`.** `GET` is
  idempotent, so a repeat is harmless. `POST` is not: a retry after a lost
  reply can submit the same order twice.

- **Retry `5xx` and `429`, never `4xx`.** A `404` means the resource is not
  there. Asking four more times does not create it; it costs four requests and
  several seconds, and it changes which exception your handlers see.

- **`timeout=` on every call, including the retrying ones.** There is no
  default, and the timeout applies per attempt. It is what makes a stalled
  connection fail fast enough for the retry logic to get a turn at all —
  without it, attempt one blocks forever and `total=3` never fires.

- **`ApiError` wraps; it does not replace.** `raise ... from exc` keeps the
  original in `__cause__`, so a log or a debugger still shows the real cause.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3 and urllib3 2.3.0:

```text
$ python exercise-05-handle-errors.py
--- replaying recorded outcomes; pass --live to call httpbin ---
[1/4] https://httpbin.org/get  (retrying session)
      ok - top-level keys: args, headers, origin, url
[2/4] https://httpbin.org/status/404  (retrying session)
      ApiError: server said 404 Client Error: NOT FOUND for url: https://httpbin.org/status/404
[3/4] https://httpbin.org/status/503  (retrying session, waits 0s, 1s, 2s)
      ApiError: gave up after 3 retries on a 5xx or 429 response
[4/4] https://httpbin.org/delay/5  (bare get, timeout=2.0)
      ApiError: no response within 2.0s

1 succeeded, 3 failed - and no traceback reached the terminal.
```

The same file run as `--live`, against the real httpbin, printed those same
lines minus the first — with one difference you cannot see on a page. The
recorded run finished in a twentieth of a second. The live run took
twenty-three, almost all of it spent waiting: the backoff pauses in case 3, and
the deliberate two-second stall in case 4.

Your own program is the live one. Watch its wall clock rather than just its
text. Case 2 should come back instantly — if it pauses, you put `404` in
`status_forcelist`. Case 3 should visibly wait.

## Steps

1. Create `exercise-05-handle-errors.py` and paste the starter in.
2. Mount the adapter in `make_session()` and run case 1 alone. Confirm you get
   the four httpbin keys back.
3. Add the `HTTPError` clause and run case 2. Confirm it returns instantly.
4. Add the `RetryError` clause and run case 3. Watch the clock; you should feel
   the backoff.
5. Add the `Timeout` clause and run case 4. Then, as an experiment, give that
   case the retrying session instead and see what changes. Put it back.
6. In the REPL, catch an `ApiError` and print `err.__cause__`. That is the
   original `requests` exception, still there, still inspectable.
7. Delete `timeout=2.0` from case 4 and run it. It finishes in about five
   seconds, because httpbin does eventually answer. Now imagine a server that
   never does. Put the timeout back.

## The Solution

```python
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
```

**The contract is "data or `ApiError`", and its value is what it hides.** A
caller of `fetch_json` does not import `requests`, does not learn that a `503`
was retried three times, and does not have to know that `requests` can raise
five different classes for one idea. You could swap `requests` for `httpx`
inside this function tomorrow and no caller would change. That is the whole
reason to have a boundary.

**Clause order is narrowest first, and it is not a style preference.**
`Timeout`, `RetryError` and `HTTPError` are all subclasses of
`RequestException`. Python takes the first clause that matches, so putting the
base class above them makes your three specific messages unreachable — no
error, no warning, just a generic message forever.

**`RequestException` stays last anyway.** Which class surfaces for a given
failure depends on your library versions and on whether an adapter is mounted.
A read timeout against a *retrying* session, for instance, can arrive wrapped
in a `ConnectionError` rather than a `Timeout`. The catch-all is what makes
that variation harmless.

**`RetryError` is the clause people leave out.** Once the adapter has spent its
retries it never hands you a `Response` at all — so `raise_for_status()` is
never reached and `HTTPError` never fires. The first "Common bug" below shows
what that looks like uncaught.

**`raise ... from exc`, every time.** It sets `__cause__`, so the original is
still there for a log or a debugger:

```text
ApiError: server said 404 Client Error: NOT FOUND for url: https://httpbin.org/status/404
url attr: https://httpbin.org/status/404
__cause__: HTTPError('404 Client Error: NOT FOUND for url: https://httpbin.org/status/404')
```

A bare `raise ApiError(...)` inside an `except` block chains through
`__context__` instead, and the traceback reads "During handling of the above
exception, another exception occurred" — Python's way of saying "these two may
be unrelated". `from exc` makes it read "The above exception was the direct
cause of the following exception". Say what you mean.

**Failure raises; it never returns `None`.** A function that returns `None` for
failure forces every caller to remember to check, and the crash lands somewhere
else entirely when one forgets. Raising makes forgetting impossible.

**`get` is the seam, and here it is a bound method.** `fetch_json` does not
take a `Session`; it takes *the thing it actually uses*, which is a function
that sends one GET. `requests.get` is one. `session.get` is another —
`make_session().get` is a **bound method**, a function that already knows which
session it belongs to. And so are the two recorded stand-ins. Ask for the
smallest thing that does the job and more things fit through the hole.

**There are two stand-ins because there are two live behaviours.**
`recorded_retrying_get` replays what a Session with the retry adapter produces:
a `RetryError` for the 503, because that is what the adapter raises once its
retries are spent. `recorded_bare_get` replays what a plain `requests.get`
produces: a `503` Response you can call `raise_for_status()` on, because
nothing retried it. Collapsing those into one stand-in would have quietly
erased the distinction case 4 exists to make.

**What the recording does not fake.** `make_session()` is real. The `Retry`
object, the `HTTPAdapter`, the mount on both schemes — all of it is the code
that runs under `--live`, unmodified. What the recording replays is the
*outcome* of that machinery, so the demo finishes instantly instead of sitting
through three backoff waits and a deliberate timeout. The honest way to say it:
this page proves your error handling is right, and `--live` proves the retry
policy is wired up. Run both.

**`replay()` builds a real `Response`.** It does not invent a look-alike with
the right attribute names; it fills in an actual `requests.Response`. That is
why case 2's message is the genuine `requests` error text, produced by the
genuine `raise_for_status()`, rather than a string somebody typed.

## Run it

Copy the worked answer on this page into `exercise-05-handle-errors.py` and run it:

```bash
python exercise-05-handle-errors.py
```

It needs `requests` installed and **no internet**. It finishes in a fraction of
a second.

To run the real thing, pass a flag:

```bash
python exercise-05-handle-errors.py --live
```

That builds the retrying `Session` and calls httpbin four times. Expect it to
take twenty seconds or more, most of it deliberate waiting. And expect it to
fail differently on a bad day: httpbin is a free service that goes down, and
while the answers on this page were being captured it returned
`503 Server Error: Service Temporarily Unavailable` for minutes at a time. If
case 1 fails too, that is them and not you — check
`https://httpbin.org/get` in a browser before you start rewriting code.

The `-solution` in the filename keeps this file from colliding with your own
`exercise-05-handle-errors.py`.

## Common bugs to catch

- **An uncaught `RetryError` for case 3.**

  ```text
  urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='httpbin.org', port=443): Max retries exceeded with url: /status/503 (Caused by ResponseError('too many 503 error responses'))

  During handling of the above exception, another exception occurred:

  Traceback (most recent call last):
    File "exercise-05-handle-errors.py", line 99, in main
      data = fetch_json(url, session=case_session, timeout=timeout)
    File "exercise-05-handle-errors.py", line 65, in fetch_json
      response = caller.get(url, timeout=timeout)
    File "...\site-packages\requests\adapters.py", line 691, in send
      raise RetryError(e, request=request)
  requests.exceptions.RetryError: HTTPSConnectionPool(host='httpbin.org', port=443): Max retries exceeded with url: /status/503 (Caused by ResponseError('too many 503 error responses'))
  ```

  Look at the frame it died in: `caller.get(...)`, not `raise_for_status()`.
  Once the adapter exhausts its retries it never returns a `Response`, so
  `raise_for_status()` is never reached and `HTTPError` never fires. The phrase
  to remember is `too many 503 error responses`.

- **Case 2 pauses for several seconds.** You added `404` to
  `status_forcelist`. Timed side by side against the same URL:

  ```text
  404 through a retrying session
  HTTPError: 404 Client Error: NOT FOUND for url: https://httpbin.org/status/404
  took 0.1s

  404 on the retry list
  RetryError: HTTPSConnectionPool(host='httpbin.org', port=443): Max retries exceeded with url: /status/404 (Caused by ResponseError('too many 404 error responses'))
  took 15.6s
  ```

  Same wrong answer, one hundred and fifty times slower, and the exception type
  changed underneath your handlers.

- **Your specific messages never print, only the generic one.**

  ```text
  ApiError: request failed: 404 Client Error: NOT FOUND for url: https://httpbin.org/status/404
  ```

  You put the `except requests.exceptions.RequestException` clause first.
  Nothing errored and nothing warned; the clauses below it are simply dead. If
  every failure in your program reports the generic message, check clause order
  before you check anything else.

- **`fetch_json` returns `None` and the caller crashes later.**

  ```text
  Traceback (most recent call last):
    File "exercise-05-handle-errors.py", line 69, in <module>
      print(data["url"])
            ~~~~^^^^^^^
  TypeError: 'NoneType' object is not subscriptable
  ```

  You wrote `return None` in an `except` block. The real failure was a `404`
  from a server; what you see is a `TypeError` in your own code, in a different
  function, with the cause thrown away.

- **`requests.exceptions.ReadTimeout: ... Read timed out. (read timeout=2.0)`
  escaping to the terminal.** You caught `ConnectTimeout` instead of `Timeout`.
  `ConnectTimeout` and `ReadTimeout` are two different children of `Timeout`;
  catch the parent and you get both.

- **The retry never happens even though the adapter exists.** You built the
  `Retry` object but never called `session.mount(...)`, or you mounted only
  `"https://"` and then tested against an `http://` URL. `Retry(...)` on its
  own does nothing at all.

- **`AttributeError: module 'requests' has no attribute 'exceptions'` after
  `from requests import get`.** Import the module, not a name out of it:
  `import requests`.

## Under the hood

<details>
<summary>Under the hood — what backoff protects, and it is not you</summary>

The obvious reading of "retry with backoff" is that the waiting is for your
benefit — give the server a moment and it might be ready. That is true and it
is the smaller half.

The larger half is that **backoff protects the server from your clients acting
in unison.**

Picture a service with a thousand clients that goes down for ten seconds. Every
client's request fails at roughly the same moment. Every client retries
immediately. The service comes back up and is hit by a thousand simultaneous
requests, which knocks it over again — and now those thousand clients retry
again, still together, because they all failed together. The outage does not
end; it oscillates. This has a name in the industry: a **thundering herd**, and
its cousin, the **retry storm**.

Growing the gap breaks the first half of that. `backoff_factor=0.5` gives waits
of `0`, `1`, `2` seconds — the formula is `backoff_factor * 2 ** (attempt - 1)`
— so the load from any one client falls off quickly instead of staying
constant. The lecture's `backoff_factor=1.0` gives `0, 2, 4`; this exercise
halves it only so the demo finishes.

But exponential backoff alone does **not** break the second half. A thousand
clients that all failed at the same instant, all waiting exactly one second,
arrive together one second later. They are still a herd; the herd is just
slower. The fix is **jitter** — a random amount added to or subtracted from
each wait, so the clients spread out:

```python
delay = backoff_factor * 2 ** (attempt - 1)
time.sleep(delay * random.uniform(0.5, 1.5))
```

Randomness making a distributed system *more* reliable is one of the genuinely
surprising results in this area, and it is the reason every serious retry
library ships jitter on by default.

Three more rules that fall out of thinking about it as protection:

**Cap the total, not just the gap.** `total=3` means the whole request costs at
most four attempts. Unbounded retrying with backoff is still unbounded.

**Only retry what might succeed.** Every code on `status_forcelist` — `429`,
`500`, `502`, `503`, `504` — is a "them" problem that may clear on its own. A
`404` is a "you" problem, and retrying it adds load to a server that already
told you the truth.

**Obey `Retry-After` when it is sent.** `respect_retry_after_header=True` makes
urllib3 use the server's own number instead of your schedule. When somebody
tells you exactly how long to wait, guessing is strictly worse.

</details>

<details>
<summary>Under the hood — the requests exception family, and why one is not enough</summary>

Everything `requests` raises descends from `RequestException`, and the shape of
the tree is what makes clause order matter:

```text
RequestException
├── ConnectionError
│   ├── ConnectTimeout        (also a Timeout)
│   ├── ProxyError
│   └── SSLError
├── Timeout
│   ├── ConnectTimeout        (yes, in both places)
│   └── ReadTimeout
├── HTTPError                 (only from raise_for_status)
├── RetryError
├── TooManyRedirects
├── URLRequired
├── MissingSchema
└── JSONDecodeError
```

Four things in there are worth carrying away.

**`ConnectTimeout` inherits from two parents.** It is both a `ConnectionError`
and a `Timeout`, which is exactly right — failing to connect within the time
allowed is both of those things — and it means a `ConnectionError` clause above
a `Timeout` clause will catch it first. Multiple inheritance in an exception
hierarchy is rare and this is a good use of it.

**`HTTPError` is the odd one out.** Every other class here means "the
conversation failed". `HTTPError` means the conversation *succeeded* and the
answer was a bad status code — and it is only ever raised by
`raise_for_status()`, which is to say by you. A `404` is not a network error.
It is a perfectly good reply that you decided to treat as a failure.

**`RetryError` replaces a reply rather than describing one.** When the adapter
gives up you get no `Response` at all, which is why it needs its own clause.

**`JSONDecodeError` is a `RequestException` too**, since requests 2.27. So a
body that is not JSON is caught by your catch-all rather than escaping as a
plain `ValueError`. That is a small kindness worth knowing about, because it
means `fetch_json` really does keep its promise: nothing from the whole
operation escapes uncaught.

And one thing that is *not* in the tree. `requests.get("nonsense")` raises
`MissingSchema`, a subclass of `RequestException`, before any network activity
at all. A programming mistake and a network failure arrive through the same
door. If you want them separated, validate the URL before you call.

</details>

## Acceptance checklist

- [ ] `fetch_json()` raises `ApiError` for all four cases and never returns
      `None`.
- [ ] The `except` clauses run narrowest first with `RequestException` last.
- [ ] Every `raise` uses `from exc`, and `err.__cause__` is the real exception.
- [ ] Case 2 returns immediately; case 3 visibly waits.
- [ ] The adapter is mounted on both schemes, with `POST` excluded from
      `allowed_methods`.
- [ ] The program exits cleanly with the summary line and no traceback.
- [ ] You can say who backoff is protecting, and what jitter adds to it.
- [ ] Committed to Git with a message like `Add Week 8 exercise 5: robust JSON fetcher`.

## Stretch

- Add a `retries_used` counter by subclassing `Retry` and overriding
  `increment` to print each attempt. Seeing the backoff schedule happen in real
  time makes it concrete.

- Add jitter, as in the Under the hood block above, and write a comment
  explaining why four identical clients retrying on the same schedule is worse
  than four clients retrying on random ones.

- Give `ApiError` a `status_code: int | None` attribute, filled in when the
  cause was an `HTTPError`, so callers can special-case `404` without importing
  `requests`.

- Move `ApiError`, `make_session` and `fetch_json` into their own `fetcher.py`
  and import them from a second script. That is the module both challenges
  want, and moving it is the quickest way to find out whether your boundary
  really is a boundary: **if the second script has to `import requests` to
  handle a failure, it is not.**

- Add a fifth case to the recorded stand-ins — a `429` with a `Retry-After`
  header — and prove your handling is right without waiting for a real server
  to rate-limit you.

You now have the whole toolkit for this week. Take it to
[the challenges](../challenges/README.md).
