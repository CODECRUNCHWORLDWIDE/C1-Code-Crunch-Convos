# Exercise 3 — Sending Data with POST

> **Topic:** sending a JSON body with `json=`, and checking that what came back is what went out
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md)
> **Difficulty:** Easy
> **Target time:** 40 minutes
> **Why this one:** so far you have only read. The moment you write, a whole class of quiet failures opens up — the body went out in the wrong format, the server understood a different value from the one you meant, a Python type did not survive the trip. This exercise makes all three visible against a server that hands your own request straight back to you.

## The Brief

A `GET` asks for something. A `POST` sends something. That is the whole
difference, and it changes what a mistake costs: a bad `GET` gives you a wrong
answer, while a bad `POST` puts a wrong **record** on somebody else's computer,
in a shape you did not intend, where you may not find it for months.

`https://httpbin.org/post` accepts a `POST` and answers with a JSON document
describing what it received — the raw body as text, the body as *it* parsed it,
and the headers your program attached. Nothing is created and nothing is
stored, so you can run it as often as you like.

You are writing a build-report submitter. A pretend CI runner finishes a test
suite and posts a small report: who ran it, which suite, how many tests passed
and failed, whether the run was green, and a couple of tags.

The interesting part is the last line. After the round trip, does the object
that came back compare **equal** to the object you sent?

Sometimes it does not. JSON has six types and Python has many more. Anything
you send that is not one of those six comes back as whatever JSON turned it
into — and `==` is the only thing that will tell you.

## Starter

Save this as `exercise-03-post-data.py` and fill in every `TODO`.

```python
"""exercise-03-post-data.py — POST a JSON body and verify the echo."""

from typing import Any

import requests

POST_URL = "https://httpbin.org/post"
TIMEOUT_SECONDS = 5.0

REPORT: dict[str, Any] = {
    "runner": "ada-laptop",
    "suite": "week-08-smoke",
    "passed": 12,
    "failed": 0,
    "green": True,
    "notes": None,
    "tags": ["python", "http"],
}


def submit_json(payload: dict[str, Any]) -> dict[str, Any]:
    """POST payload as a JSON body; return the parsed echo document."""
    # TODO: requests.post(POST_URL, json=payload, timeout=TIMEOUT_SECONDS)
    # TODO: raise_for_status(), then return .json()
    raise NotImplementedError


def submit_form(payload: dict[str, Any]) -> dict[str, Any]:
    """POST the same payload form-encoded, so you can see the difference."""
    # TODO: same call, but data=payload instead of json=payload
    raise NotImplementedError


def report_round_trip(echo: dict[str, Any], sent: dict[str, Any]) -> None:
    """Print what the server understood, and whether it matches what we sent."""
    # TODO: print echo["headers"]["Content-Type"]
    # TODO: print echo["data"]        -- the raw body as a string
    # TODO: print echo["json"]        -- the body parsed by the server
    # TODO: print whether echo["json"] == sent
    raise NotImplementedError


def main() -> None:
    """Submit the report twice, once as JSON and once form-encoded."""
    print("--- json= ---")
    report_round_trip(submit_json(REPORT), REPORT)

    print("--- data= ---")
    flat = {"runner": REPORT["runner"], "passed": REPORT["passed"]}
    echo = submit_form(flat)
    print("content-type:", echo["headers"]["Content-Type"])
    print("json field:  ", echo["json"])
    print("form field:  ", echo["form"])


if __name__ == "__main__":
    main()
```

Three words to have straight before you start.

**Body.** The parcel attached to a request. A `GET` has none — everything a
`GET` says is in its address. A `POST` has one, and the body is where the data
you are sending actually travels.

**`Content-Type`.** A label on the parcel saying what is inside, so the server
knows how to open it. `application/json` means "this is a JSON document".
`application/x-www-form-urlencoded` means "this is the flat `a=1&b=2` shape a
web form sends".

**`json=` versus `data=`.** Two different parcels. `json=` turns your object
into a JSON document *and* writes the `application/json` label. `data=`
flattens a dictionary into `a=1&b=2` and writes the form label. You will send
the same information both ways and watch it land in two different places on the
server.

## Requirements

1. `submit_json()` uses `json=payload`. Do not call `json.dumps()` yourself and
   do not set `Content-Type` by hand.
2. Every request passes `timeout=TIMEOUT_SECONDS` and calls
   `raise_for_status()` before `.json()`.
3. `report_round_trip()` prints four labelled lines: the content type the
   server saw, the raw body string, the body as the server parsed it, and the
   result of the `==` comparison.
4. The `json=` round trip must print `round trip equal:  True`.
5. The `data=` section prints the content type, `json field:   None`, and the
   form dict — showing that `data=` and `json=` land in different places.
6. After it all works, change `"tags"` to a tuple `("python", "http")`, run it
   again, and note what happens to the comparison. Leave a one-line comment in
   your file recording the answer, then change it back to a list.

## Constraints

- **Use `json=`, not `data=json.dumps(payload)`.** They produce nearly
  identical bytes, but only `json=` writes the `Content-Type: application/json`
  label. Without that label a strict server tries to read your JSON as a form,
  finds one enormous field name, and answers `400`. The label is the half
  people forget.

- **Set `timeout=` on both calls.** A `POST` that hangs is worse than a `GET`
  that hangs, because you do not know whether the server acted on it before it
  went quiet. You cannot log a failure you never observe.

- **Do not retry this `POST` automatically.** `POST` is not idempotent —
  "idempotent" meaning "doing it twice is the same as doing it once", which is
  true of asking and false of submitting. Two sends mean two reports. Exercise
  5 configures retries for `GET` only, and this is why.

- **Compare with `==` on the whole dict, not field by field.** A per-field
  check only catches the fields you thought to check. Whole-object equality
  catches the one you did not — which here is exactly the one that breaks.

- **Never put credentials in a practice request to a public echo server.**
  `httpbin.org` reflects everything you send, it is not ours, and a practice
  request is still a real request to a real third party. Lecture 3 covers where
  secrets belong.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3:

```text
$ python exercise-03-post-data-solution.py
--- replaying a recorded echo; pass post=post_live to go online ---
--- json= ---
content-type sent: application/json
raw body:          {"runner": "ada-laptop", "suite": "week-08-smoke", "passed": 12, "failed": 0, "green": true, "notes": null, "tags": ["python", "http"]}
parsed by server:  {'failed': 0, 'green': True, 'notes': None, 'passed': 12, 'runner': 'ada-laptop', 'suite': 'week-08-smoke', 'tags': ['python', 'http']}
round trip equal:  True
--- data= ---
content-type: application/x-www-form-urlencoded
json field:   None
form field:   {'passed': '12', 'runner': 'ada-laptop'}
--- json=, with tags as a tuple ---
content-type sent: application/json
raw body:          {"runner": "ada-laptop", "suite": "week-08-smoke", "passed": 12, "failed": 0, "green": true, "notes": null, "tags": ["python", "http"]}
parsed by server:  {'failed': 0, 'green': True, 'notes': None, 'passed': 12, 'runner': 'ada-laptop', 'suite': 'week-08-smoke', 'tags': ['python', 'http']}
round trip equal:  False
```

Your own program prints the first two sections. The shipped file adds the third
because requirement 6 is the whole lesson and a download nobody edits should
still show it.

Four things to read out of that block before you move on.

Python's `True` went out as JSON's lowercase `true` and came back `True`.
`None` made the same trip through `null`. Those two survived because booleans
and null are among the six JSON types.

In the `data=` section the integer `12` came back as the string `'12'`, because
form encoding has no types at all — everything in a form is text.

And the third section is the one to sit with. Look at the `raw body:` line: it
is character-for-character identical to the first section. Look at
`parsed by server:` — identical too. Then `round trip equal:` says `False`.
Nothing errored, nothing warned, and the value you got back is not the value
you sent.

Finally, the keys print in alphabetical order rather than the order you wrote
them. That is httpbin re-serialising its reply with the keys sorted, and it
does not affect `==` at all — dictionaries compare by content, not by order.

## Steps

1. Create `exercise-03-post-data.py` and paste the starter in.
2. Fill in `submit_json()`, then print the whole echo document once. You want
   to see `args`, `data`, `files`, `form`, `headers`, `json`, `origin` and
   `url` with your own eyes before you start reaching into it.
3. Fill in `report_round_trip()` and confirm `round trip equal:  True`.
4. Fill in `submit_form()` and run the second section. Compare where the data
   landed: `json` for one call, `form` for the other, never both.
5. Now do requirement 6. Change `"tags"` to `("python", "http")`, run it, and
   read the failing line before you change it back.

## The Solution

```python
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
```

**`json=` does two things, and people only remember one.** It turns your object
into a JSON document *and* it writes `Content-Type: application/json`. The
label is what tells the server how to open the parcel. You never set a header
in this file; the echo proves one went out anyway.

**`data=` and `json=` land in different places on the server, never both.**
That is what the second section demonstrates. Send a form and `echo["json"]` is
`None` while `echo["form"]` is full; send JSON and it is the other way round.
If you ever cannot find your data on the server side, the first question is
which of the two you used.

**Form encoding has no types at all.** The integer `12` came back as `'12'`.
JSON has six types; a form has one, and that one is text. This is why `json=`
is the right default for anything structured, and why `args` in Exercise 1 was
all strings.

**Whole-object `==` catches the field you did not think to check.** One line,
and it tests all of them. The point of this exercise is that the field which
breaks is the field you were not worried about.

**`post` is the seam, and this one is worth looking at closely.** `post_live`
sends the body over the network. `post_recorded` does not — but notice what it
does *not* fake. It calls the real `json.dumps` and the real `json.loads`, the
same two functions `requests` and httpbin use between them. It calls the real
`urlencode` and `parse_qsl` for the form case. Only the wire is missing.

That is what makes the tuple result trustworthy. A stand-in that simply handed
your object back would print `True` for everything, and the exercise would
teach the opposite of the truth. When you fake something, fake the part you
cannot control and keep the part you are trying to learn about.

**The tuple is the planted trap, and it is worth sitting with.** JSON has no
tuple. `json.dumps` wrote it as an array, and `json.loads` read the array back
as a `list`, and `("python", "http") != ["python", "http"]`. The same thing
happens to `set`, `datetime`, `Decimal` and `Path`. The rule to carry forward:
**only the six JSON types survive a round trip unchanged.** Anything else needs
an encoding you write on your side and a decoding you write on the other.

**No retry on this call, deliberately.** If the reply is lost after the server
has already acted, a retry submits the report twice. Exercise 5 restricts
retries to `GET` and `HEAD` for exactly this reason.

## Download and run

Download [exercise-03-post-data-solution.py](./exercise-03-post-data-solution.py)
and run it:

```bash
python exercise-03-post-data-solution.py
```

It needs `requests` installed and **no internet**. The echo document it works
from was captured from `https://httpbin.org/post` and pasted into the file as
`RECORDED_ECHO`; the body fields are filled in per call by `post_recorded`,
which encodes and decodes for real.

To send it to httpbin for real, change one argument at the bottom of the file:

```python
main(post=post_live)
```

`post_live` is already in the file and is the default value of the parameter,
so deleting `post=post_recorded` also works.

Two edits were made to the recorded document and both are named in the file.
The `origin` field held the capturing machine's public IP address and now holds
`203.0.113.7`, an address reserved for documentation. And the per-request
`X-Amzn-Trace-Id` header was dropped, because a stale trace id from somebody
else's request is noise.

The `-solution` in the filename keeps this file from colliding with your own
`exercise-03-post-data.py`.

## Common bugs to catch

- **`round trip equal:  False` after switching `tags` to a tuple.** JSON has no
  tuple. This is the exercise's planted trap, and the same thing happens to
  `set`, `datetime`, `Decimal` and `Path`.

- **`TypeError: Object of type datetime is not JSON serializable`.**

  ```text
  Traceback (most recent call last):
    File "...\site-packages\requests\models.py", line 510, in prepare_body
      body = complexjson.dumps(json, allow_nan=False)
    File "...\Lib\json\encoder.py", line 180, in default
      raise TypeError(f'Object of type {o.__class__.__name__} '
                      f'is not JSON serializable')
  TypeError: Object of type datetime is not JSON serializable
  ```

  You added a timestamp with `datetime.now()`. Read where it raised:
  `prepare_body`, before anything reached the network. That is the good case —
  a loud local failure. Convert timestamps yourself, usually with
  `.isoformat()`, and parse them back on the far side.

- **`json field:   None` in the `json=` section.** You passed `data=payload` by
  mistake. The echo tells you which one you used.

- **`KeyError: 'json'`.** You are reading the echo of a `GET` to
  `httpbin.org/get`, which has no `json` key because a `GET` has no body. Post
  to `/post`.

- **`json.decoder.JSONDecodeError` on `echo["data"]`.** `data` is the raw body
  as a *string*, deliberately — it is what actually went over the wire. If you
  want the object, read `echo["json"]`, which the server already parsed.

- **`405 Client Error: METHOD NOT ALLOWED for url: https://httpbin.org/get`.**
  You sent a `POST` to the `GET` endpoint. `405` always means "right address,
  wrong door": the URL exists, but not for that verb.

- **`400 Bad Request` from a real API when your test server was fine.** You
  built the body yourself with `data=json.dumps(payload)`. httpbin is relaxed
  and takes it; a strict server reads the missing label and refuses. Use
  `json=`.

## Under the hood

<details>
<summary>Under the hood — what actually goes over the wire, byte by byte</summary>

Both calls in this exercise send the same information. Here is what each one
puts on the wire, with the parts `requests` filled in for you marked.

The `json=` call:

```text
POST /post HTTP/1.1
Host: httpbin.org
User-Agent: python-requests/2.32.3
Accept: */*
Accept-Encoding: gzip, deflate
Content-Type: application/json          <- set by json=
Content-Length: 135                     <- counted by requests

{"runner": "ada-laptop", "suite": "week-08-smoke", "passed": 12, ...}
```

The `data=` call:

```text
POST /post HTTP/1.1
Host: httpbin.org
...
Content-Type: application/x-www-form-urlencoded   <- set by data=
Content-Length: 27

runner=ada-laptop&passed=12
```

Three things worth noticing.

**The blank line is structural.** Headers, then one empty line, then the body.
That empty line is how the server knows the headers have finished, and it is
the same rule in every HTTP message ever sent.

**`Content-Length` is a promise you cannot break.** It says exactly how many
bytes of body follow. Send fewer and the server waits for the rest until it
gives up; send more and the extra bytes get read as the beginning of the next
request. Getting it wrong by hand is a classic way to produce a hang that looks
like a network fault. `requests` counts for you, every time, which is one of
the several reasons not to build requests by hand.

**The form body is flat and has no types.** `runner=ada-laptop&passed=12` is
the same shape as a query string — the identical encoding, just moved from the
address into the body. There is nowhere in it to put a list inside a dictionary
inside a list, which is why `data=` cannot nest and `json=` can.

</details>

<details>
<summary>Under the hood — why "it came back the same" is a stronger check than it looks</summary>

`echo["json"] == sent` is one line, and it is quietly testing four different
things at once.

**That your encoder could represent the value.** A `datetime` fails here
loudly, before the network. That is the easy case.

**That the encoding was lossless.** A tuple encodes fine and decodes into
something else. No exception, no warning — only `==` notices.

**That the server parsed it the way you meant.** If the label were wrong, the
server would have read your JSON as a form and `echo["json"]` would be `None`.

**That nothing in the middle rewrote it.** Proxies, gateways and
"helpful" middleware do sometimes alter bodies. Rare, and infuriating when it
happens, and this line sees it.

Now the limit, because a check you trust too far is worse than no check. Python
dictionaries compare by content and ignore order, so this test cannot see a
reordering — and it should not, because JSON object key order carries no
meaning. It also cannot see anything the server did *after* replying: a real
API that stores your record and then trims a field is beyond the reach of an
echo.

The professional version of this idea is called a **round-trip property**: for
all values `v` of the type you support, `decode(encode(v)) == v`. Week 11 will
show you how to state that as a test and have a machine try it on hundreds of
values you would never have thought of. What you are doing here by hand is the
same idea with one value.

One more caution. This works because `REPORT` contains only JSON-native values.
Add a float like `0.1 + 0.2` and the comparison still passes — JSON numbers go
through as decimal text and Python parses the same double back — but a value
beyond a double's range, or a very long integer, can round-trip through another
language's parser and come back changed. When exact numbers matter, send them
as strings and convert at both ends.

</details>

## Acceptance checklist

- [ ] The `json=` round trip prints `round trip equal:  True`.
- [ ] The content type for the `json=` call is `application/json`, and you did
      not set that header yourself.
- [ ] The `data=` call shows `json field:   None` and a populated form field.
- [ ] The integer `12` comes back as `'12'` in the form section, and you can
      say why.
- [ ] Both calls pass `timeout=` and call `raise_for_status()`.
- [ ] Your file carries a one-line comment recording what the tuple did.
- [ ] You can list the six JSON types without looking them up.
- [ ] Committed to Git with a message like `Add Week 8 exercise 3: POST a JSON body`.

## Stretch

- Send the same report with `requests.put` to `https://httpbin.org/put`. The
  echo is the same shape; the method is what would change a real server's
  behaviour.

- Add a custom header, `headers={"X-Build-Id": "42"}`, and find it in
  `echo["headers"]`. Notice httpbin normalises the capitalisation, because
  header names do not care about case.

- Write a small `assert_round_trip(payload)` helper that raises with a message
  naming the first key whose value changed, instead of just printing `False`.
  Then feed it a payload with a `set` in it.

- Give `post_recorded` a third branch that returns a `500` the way the live
  server would, and prove your error handling works without ever needing a
  server to break. That is the whole argument for the seam, in one experiment.

When the echo matches what you sent — and you know why the tuple does not —
move on to [Exercise 4 — Walking Every Page](./exercise-04-pagination.md).
