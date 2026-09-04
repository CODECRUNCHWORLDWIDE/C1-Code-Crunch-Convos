# Exercise 1 — Your First GET Request

> **Topic:** sending one `GET` with `requests`, then reading `.status_code`, `.json()` and `.url`
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** every other exercise this week, both challenges and the mini-project are the same four moves — build a request, send it, check what came back, read the body. Do those four moves once, slowly, against a server whose only job is to tell you the truth about what you sent, and the rest of the week is a variation on a shape you already know.

## The Brief

A **server** is a program on somebody else's computer that waits to be asked
questions. Your program is the **client**: it asks. One question and one answer
is called a **request** and a **response**, and the whole of this week is those
two words.

`httpbin.org` is a mirror. You send it a question and it answers by describing
the question you just asked: which words you put in the address, which extra
notes your program attached without being told to, which IP address it thinks
you came from. It creates nothing and stores nothing, and it needs no password.
That makes it the safest place in the world to learn on, because you cannot
break it and you cannot leak anything into it by accident.

You are building a small **probe** — a program whose whole job is to go and
look. It reports the status code, the kind of content that came back, how long
the round trip took, the exact address `requests` built for you, and the words
the server read out of that address. Then it deliberately asks for something
that is not there, so you can watch the "was that a good answer?" check bite
before you ever depend on it.

## Starter

Save this as `exercise-01-first-get-request.py` and fill in every `TODO`.

```python
"""exercise-01-first-get-request.py — send one GET and read the response.

Calls https://httpbin.org/get, which echoes back a JSON description of the
request it received, then prints the parts of the Response that matter.
"""

from typing import Any

import requests

ECHO_URL = "https://httpbin.org/get"
MISSING_URL = "https://httpbin.org/status/404"
TIMEOUT_SECONDS = 5.0


def probe(url: str, params: dict[str, str]) -> requests.Response:
    """Send one GET and return the Response, whatever its status code.

    Args:
        url: Absolute https URL to call.
        params: Query-string pairs. requests URL-encodes them for you.

    Returns:
        The Response object. This function does not raise on 4xx or 5xx.
    """
    # TODO: return requests.get(url, params=..., timeout=TIMEOUT_SECONDS)
    raise NotImplementedError


def describe(response: requests.Response) -> None:
    """Print status, content type, elapsed seconds, and the final URL."""
    # TODO: print response.status_code and response.reason on one line
    # TODO: print response.headers["content-type"]
    # TODO: print response.elapsed.total_seconds() rounded to 3 places
    # TODO: print response.url
    raise NotImplementedError


def echoed_args(response: requests.Response) -> dict[str, Any]:
    """Return the "args" object httpbin echoed back to us."""
    # TODO: parse the body with .json() and return its "args" key
    raise NotImplementedError


def main() -> None:
    """Probe the echo endpoint, then prove raise_for_status() bites."""
    response = probe(ECHO_URL, {"student": "ada", "week": "8"})
    response.raise_for_status()
    describe(response)
    print("echoed args:", echoed_args(response))

    # TODO: call probe(MISSING_URL, {}), then raise_for_status() inside a
    # try / except requests.exceptions.HTTPError, and print the exception.


if __name__ == "__main__":
    main()
```

Six words in that starter you need before you start.

**URL.** The address. `https://httpbin.org/get` is three parts: `https` says
how to talk, `httpbin.org` says which computer, `/get` says which door on that
computer. Anything after a `?` is the **query string** — extra words you are
handing over with the question.

**`params=`.** A dictionary of those extra words. You give `requests` the plain
dictionary and it builds the query string, punctuation and all.

**`Response`.** What comes back. It is an **object**, not a string: a box with
a dozen labelled compartments you can open by name. `.status_code` holds a
number, `.headers` holds the server's notes about the answer, `.text` holds the
body as one long piece of text, `.json()` turns that text into Python
dictionaries and lists.

**Status code.** A three-digit number the server puts at the top of every
answer. `200` means "here it is". `404` means "no such thing here". You will
meet the families properly in a moment.

**`raise_for_status()`.** One method on the `Response` that says "if that
number was a bad one, stop the program with a clear message". You call it; it
either does nothing at all or it raises.

**`timeout=`.** How many seconds you are willing to wait. You will see in the
Constraints why leaving it out is the worst bug on this page.

## Requirements

1. `probe()` passes its parameters through `params=`. No f-string URLs, no `+`
   concatenation.
2. `probe()` passes `timeout=TIMEOUT_SECONDS`. Every request in this course
   carries a timeout.
3. Replace `"ada"` with your own name before you run it.
4. `describe()` prints four lines, in this order: `200 OK`, then
   `content-type: application/json`, then `elapsed: <seconds>s`, then
   `url: <the full URL including the query string>`.
5. `echoed_args()` returns a dict. The line it feeds prints as
   `echoed args: {'student': '<your name>', 'week': '8'}`.
6. The second half prints the `HTTPError` message and the program exits
   normally — status `0`, no traceback.

## Constraints

- **Every request passes `timeout=`.** Without one, `requests` waits forever.
  Not thirty seconds, not two minutes — forever. If the server accepts your
  connection and then never writes a byte back, your script sits there in a
  blocking read with no upper bound, and the only way out is Ctrl-C. A request
  that fails you can handle. A request that hangs you cannot even see.

- **Use `params=`, not string concatenation.** This is a correctness rule, not
  a tidiness one. A query string has punctuation with meaning: `&` separates
  one pair from the next, `=` separates a name from its value. Glue a value
  into the URL yourself and any of those characters inside the value changes
  what the server reads. `params=` escapes them for you. The Under the hood
  block at the bottom shows the exact damage, with real output.

- **`response.headers` is case-insensitive; `response.json()` is not.** Header
  names do not care about capital letters in HTTP, so `requests` hands you a
  special dictionary that does not care either. The parsed body is an ordinary
  dictionary and cares very much: one wrong capital there is a `KeyError`.

- **Do not check `if response.status_code == 200`.** A `201` and a `204` are
  successes too, and that comparison throws them away. `raise_for_status()`
  gets the whole family right and costs one line.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3:

```text
$ python exercise-01-first-get-request.py
--- replaying recorded replies; pass send=send_live to go online ---
200 OK
content-type: application/json
elapsed: 0.412s
url: https://httpbin.org/get?student=ada&week=8
echoed args: {'student': 'ada', 'week': '8'}
404 Client Error: NOT FOUND for url: https://httpbin.org/status/404
```

**The shipped file does not call httpbin.** It replays a reply that was
captured from httpbin earlier and pasted into the file as a constant, which is
why `elapsed: 0.412s` is the same number every single time. Your own
`exercise-01-first-get-request.py` does call it, so your elapsed time will be
your own and your name will be your own. Everything else — the `200 OK`, the
content type, the shape of the lines, the `'8'` in quotes, the 404 message —
is the same for both.

Why the download works that way, and the one-line change that points it at the
real server, is explained under **Download and run**.

## Steps

1. Activate your virtual environment and install the library:
   `python -m pip install requests`.
2. Create `exercise-01-first-get-request.py` and paste the starter in.
3. Fill in `probe()` first. Run it. You should get no traceback until
   `describe()` is reached, which proves the request itself worked.
4. Fill in `describe()` and `echoed_args()`, then run it again.
5. Copy the URL your script printed into a browser and compare. Same server,
   same answer, no Python in between. This is the single most useful debugging
   move of the whole week.
6. Add the `try` / `except requests.exceptions.HTTPError` block for
   `MISSING_URL`, and confirm the message prints instead of a traceback.
7. Print `response.json()["headers"]["User-Agent"]`. That is how the server
   sees you, and you did not set it.

## The Solution

```python
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
```

**`probe()` returns the `Response` and refuses to judge it.** That is what
makes the second half of `main()` possible at all. If `probe()` called
`raise_for_status()` itself, there would be no way to get a `404` response
object back into your hands and decide for yourself what to do with it. Keep
"send it" and "was that good?" as two separate steps and the caller stays in
charge.

**`send` is the seam, and it is the idea to take away from this page.** The
network is the one part of this program you cannot control: it is slow, it
fails, and it gives a different answer tomorrow. So it goes behind a door with
a handle on it. `probe` does not call `requests.get`; it calls whatever
function it was handed, and the default is the real one. Passing a different
function in is called **dependency injection**, and the name is scarier than
the idea — you are passing a function as an argument, which you have been doing
since `sorted(items, key=...)` in Week 5.

Two things fall out of it immediately. The download runs offline, so this page
can promise you an exact output. And `probe`, `describe` and `echoed_args` are
never modified to make that happen — the code you would ship is the code that
ran. Week 11 will call this **mocking** and use it to test programs without a
network. You are doing it now, in the open, where you can see it.

**`send_recorded` builds a real `Response`.** It does not invent a look-alike
object with the right attribute names. It makes an actual
`requests.Response`, fills in the status code, the reason, the headers and the
body bytes, and hands it over. So `describe()` cannot tell the difference, and
neither can `.json()`, and neither can `raise_for_status()` — which is exactly
why the 404 case still prints the genuine requests error message. A stand-in
that behaves differently from the real thing teaches you the stand-in.

**`params=` is a correctness feature.** Look at the `url:` line in the output:
you never typed a `?` or an `&`, and both are there, in the right places, with
your values escaped. Hand-build that string yourself and a value containing an
`&` silently turns one parameter into two. Under the hood has the transcript.

**`raise_for_status()` rather than `status_code == 200`.** A `201 Created` and
a `204 No Content` are successes; an equality test against `200` rejects both.
And when `raise_for_status()` does raise, the message it builds already
contains the status, the reason phrase and the full URL, which is most of what
you need to work out what went wrong.

**`response.elapsed` is the round trip, not your program's runtime.** It is a
`timedelta`, so `.total_seconds()` gives you a float and `:.3f` gives you the
three decimal places requirement 4 asks for.

**Everything in `args` is a string.** You sent `week=8` and the server read
back the one-character string `'8'`. A query string is text on the wire; it has
no types at all. `echoed_args(response)["week"] == 8` is `False` and always
will be. Convert with `int()` at the point where you need a number.

## Run it

Copy the worked answer on this page into `exercise-01-first-get-request.py` and run it:

```bash
python exercise-01-first-get-request.py
```

It needs the `requests` library installed, and nothing else. **It does not need
the internet.** The reply it prints was captured from `https://httpbin.org/get`
and pasted into the file as the `RECORDED` constant, so the download works on a
plane, on a school network that blocks unknown hosts, and on the days when
httpbin — which is free, and busy — hands out `503` to everybody.

To point the same code at the real server, change one argument. In `main()`:

```python
response = probe(ECHO_URL, {"student": STUDENT_NAME, "week": "8"}, send=send_live)
```

That is the whole switch. `send_live` is already in the file, it is four lines
long, and it is the default value of the parameter — so deleting `send=...`
entirely also works.

Two edits were made to the recorded body, and both are marked in the file
rather than hidden. The `origin` field held the capturing machine's real public
IP address, which is not something to publish, so it now holds `203.0.113.7` —
an address reserved for documentation that belongs to nobody. And the document
was reformatted with `json.dumps(indent=2)`, because httpbin pads its output
with trailing spaces that most text editors silently delete.

The `-solution` in the filename keeps this file from colliding with your own
`exercise-01-first-get-request.py`.

## Common bugs to catch

- **`ModuleNotFoundError: No module named 'requests'`.** The library is not
  installed, or it is installed in a different environment from the one your
  terminal is using. Run `python -m pip install requests` — the `python -m`
  prefix guarantees the install lands in the interpreter that will run your
  script.

- **`TypeError: string indices must be integers, not 'str'`.**

  ```text
  Traceback (most recent call last):
    File "exercise-01-first-get-request.py", line 39, in main
      print(response.text["args"])
            ~~~~~~~~~~~~~^^^^^^^^
  TypeError: string indices must be integers, not 'str'
  ```

  You wrote `response.text["args"]`. `.text` is the body as one long string.
  `.json()` is the parsed object, and it is a *method*, so the parentheses are
  not optional. `response.json` without them hands you the method itself, which
  is more confusing still because it does not fail until you try to index it.

- **`KeyError: 'Args'`.** The header lookup two lines above tolerated
  `CONTENT-TYPE` and this one will not tolerate a capital `A`. Both print with
  `{...}` and only one of them ignores case. When a `KeyError` names a key you
  are certain exists, print `sorted(response.json())` and read the real
  spelling.

- **`AssertionError` comparing `args["week"] == 8`.** A query string has no
  types. You sent `week=8` and the server read back the two characters `'8'`.
  Everything in `args` is a string, always.

- **A traceback ending in `requests.exceptions.HTTPError` for the 404.** You
  called `raise_for_status()` outside the `try` block. Put it inside — catching
  it is the point of the second half.

- **`requests.exceptions.ConnectionError`, with `Failed to resolve` inside it.**

  ```text
  requests.exceptions.ConnectionError: HTTPSConnectionPool(host='httpbin.invalid', port=443): Max retries exceeded with url: /get (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x000001E14F059160>: Failed to resolve 'httpbin.invalid' ([Errno 11001] getaddrinfo failed)"))
  ```

  The name lookup failed: nothing on the internet answers to that host, so
  there was never a connection to time out. Either you are offline, or you
  mistyped the host. Note that a typo does **not** always look like this — see
  the next bug.

- **The script hangs on `httpbin.com` and then times out.** That host is real,
  it resolves, and it does not answer — so you get a `ReadTimeout` after your
  `timeout=` expires, not a name-resolution error. A wrong host that exists is
  slower and more confusing than a wrong host that does not. The host you want
  is `httpbin.org`.

- **The script hangs and never prints anything.** You dropped `timeout=`.
  Ctrl-C, put it back, and read the first constraint again.

## Under the hood

<details>
<summary>Under the hood — what a hand-built URL actually breaks</summary>

The reason to use `params=` is not that string formatting is ugly. It is that
a query string has **punctuation with meaning**, and a value that happens to
contain that punctuation rewrites the question you thought you were asking.

Start with the case that is fine, because knowing which half is safe is part of
knowing the rule. A space inside a hand-built URL is not a disaster:

```text
>>> r = requests.get("https://httpbin.org/get?student=ada grace&week=8", timeout=5)
>>> r.url
'https://httpbin.org/get?student=ada%20grace&week=8'
>>> r.json()["args"]
{'student': 'ada grace', 'week': '8'}
```

`requests` re-encoded the space to `%20` on the way out and the value arrived
whole. A space in a URL is illegal on the wire, but `requests` fixes it for you
before the wire ever sees it.

Now the same URL with an ampersand in the value:

```text
>>> r = requests.get("https://httpbin.org/get?student=ada & grace&week=8", timeout=5)
>>> r.url
'https://httpbin.org/get?student=ada%20&%20grace&week=8'
>>> r.json()["args"]
{' grace': '', 'student': 'ada ', 'week': '8'}
```

Nothing raised. Nothing warned. The spaces were escaped exactly as before — and
the `&` was not, because at that point in the string it is punctuation, and
`requests` has no way to know you meant it as a letter. One parameter became
two. `student` is now `'ada '` with a trailing space, and there is a second
parameter whose *name* is `' grace'` and whose value is empty.

`params=` cannot make that mistake, because you handed it the value separately
from the punctuation:

```text
>>> r = requests.get("https://httpbin.org/get",
...                  params={"student": "ada & grace", "week": "8"}, timeout=5)
>>> r.url
'https://httpbin.org/get?student=ada+%26+grace&week=8'
>>> r.json()["args"]
{'student': 'ada & grace', 'week': '8'}
```

The `&` became `%26`, the spaces became `+`, and the server read back exactly
what you sent. Both `+` and `%20` mean a space in a query string; `requests`
picks one and either is correct.

The failure mode worth fearing here is not the exception. It is the **wrong
answer that does not look wrong**. An exception stops the program and points at
a line. A silently split parameter produces a report with a missing student in
it, six months from now, and nothing in your logs says why.

</details>

<details>
<summary>Under the hood — what a status code actually promises</summary>

The first digit is the whole message; the other two are detail.

| Family | Means | Examples |
|---|---|---|
| `1xx` | "still going" | `100 Continue` |
| `2xx` | it worked | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | look somewhere else | `301 Moved Permanently`, `304 Not Modified` |
| `4xx` | **your** request was wrong | `400 Bad Request`, `404 Not Found`, `429 Too Many Requests` |
| `5xx` | **their** server broke | `500 Internal Server Error`, `503 Service Unavailable` |

The `4xx`/`5xx` split is the useful one and you will lean on it all week. A
`4xx` is a "you" problem: asking again, unchanged, gets the same answer. A
`5xx` is a "them" problem: asking again in two seconds might work. Exercise 5
turns that one sentence into a retry policy.

Now the part people get wrong. **`200 OK` is a statement about the HTTP
conversation, not about your data.** It says the server understood the request
and is sending a body. It does not say the body contains what you wanted, and
plenty of real APIs answer `200` while telling you, inside the body, that
nothing worked. Two you will meet in this very week:

```text
>>> requests.get("https://is.gd/create.php",
...              params={"format": "json", "url": "notaurl"}, timeout=5).text
'{ "errorcode": 1, "errormessage": "Please enter a valid URL to shorten" }'
```

That came back `200`. The shortener is working perfectly; it is telling you the
URL is bad, in the body, in its own vocabulary.

```text
>>> requests.get("https://geocoding-api.open-meteo.com/v1/search",
...              params={"name": "NotARealPlace", "count": 1}, timeout=5).text
'{"generationtime_ms":0.65505505}'
```

`200` again — and no `results` key at all. "I looked and found nothing" is,
for that API, a completely successful request.

So `raise_for_status()` is necessary and not sufficient. It catches the case
where the conversation went wrong. Checking that the body contains the field
you actually need is a second, separate job, and it is yours.

There is a related trap in the other direction. `response.ok` is `True` for
anything under `400`, which includes the `3xx` family, and it is a plain
attribute rather than a method — so `if response.ok:` is fine but
`if response.ok():` raises `TypeError: 'bool' object is not callable`.

</details>

<details>
<summary>Under the hood — why timeout= has no default, and what happens without it</summary>

`requests.get(url)` with no `timeout=` waits forever. Not a long time —
forever. There is no cap anywhere in the library, and this surprises people so
reliably that the `requests` documentation says so in bold.

The reason is that "forever" is the honest default for a network read. The
library cannot know whether you are fetching a 2 KB JSON document or a 40 GB
backup over a slow link, so it refuses to guess a number and make the second
one fail. That is defensible, and it means the number is your job.

What a hang looks like matters, because it does not look like a bug. There is
no traceback, no error, no output — just a prompt that never comes back. In a
loop it is worse: six pages print, page seven stalls, and the screen is full of
evidence that everything is fine.

The value you pass covers **each phase separately**, not the whole call: up to
`timeout` seconds to connect, then up to `timeout` seconds of silence between
bytes while reading. A slow-but-steady download that keeps trickling data will
happily run past `timeout=5` in wall-clock terms and never fire, because the
gaps between bytes stayed under five seconds. If you need the two limits to
differ, pass a tuple — `timeout=(3.05, 27)` is connect, then read.

And there is one thing `timeout=` cannot cover: name resolution. Looking up
which computer `httpbin.org` refers to happens in the operating system, below
`requests`, and it obeys the system resolver's own limits rather than yours.
That is why a bad hostname can sit for several seconds before failing with a
`ConnectionError` you did not expect to wait for.

</details>

## Acceptance checklist

- [ ] `requests` imports and the script runs with no traceback.
- [ ] Both calls pass `timeout=`.
- [ ] The query string is built by `params=`, and the `url:` line proves it.
- [ ] The four description lines print in the order requirement 4 gives.
- [ ] The 404 is reported as a one-line message, not a traceback.
- [ ] The process exits `0` (`echo $?` on macOS or Linux, `$LASTEXITCODE` in
      PowerShell).
- [ ] You can say, without looking, why `args["week"]` is `'8'` and not `8`.
- [ ] Committed to Git with a message like `Add Week 8 exercise 1: first GET request`.

## Stretch

- Call `https://httpbin.org/status/500` as well. Same `HTTPError`, different
  family — Exercise 5 covers why a `5xx` is worth retrying and a `4xx` is not.

- Print `response.request.headers` to see the full set of headers `requests`
  attached on your behalf. You set none of them:

  ```text
  {'User-Agent': 'python-requests/2.32.3', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
  ```

- Send `params={"tag": ["python", "api"], "unused": None}` and read the echoed
  `args`. A list becomes a repeated key; a `None` disappears before the request
  is built:

  ```text
  url:  https://httpbin.org/get?tag=python&tag=api
  args: {'tag': ['python', 'api']}
  ```

- Add a third recorded reply to `RECORDED` — copy a real body out of your
  browser — and give `main()` a fifth line that probes it. You have just
  written a test fixture, which is most of what Week 11 is about.

Once your probe reports cleanly, move on to
[Exercise 2 — PokeAPI and Nested JSON](./exercise-02-pokemon-api.md).
