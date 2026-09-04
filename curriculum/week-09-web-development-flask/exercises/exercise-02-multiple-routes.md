# Exercise 2 — Multiple Routes and URL Converters

> **Topic:** Several routes on one app, dynamic URL segments with converters, and one query string
> **Lecture:** [01 — Flask Hello World](../lecture-notes/01-flask-hello-world.md)
> **Difficulty:** Easy
> **Target time:** 40 minutes
> **Why this one:** a URL converter is the cheapest input validation you will ever write. `<int:room_id>` turns "someone typed garbage in the address bar" from a 500-level crash into a free 404, before your function runs. Learn the converters now and you will stop writing the `try: int(x) except: abort(400)` boilerplate that clutters most beginner Flask apps — including, if you skip this, yours in the mini-project.

## The Brief

The study hall from Exercise 1 has grown to three rooms, each with a host and
a topic. You are building the directory: an index of every room, a page per
room, a page per host, and a search that reads a topic out of the query
string.

Everything is still plain text. Templates arrive in Exercise 3, and the ugly
string-building you do here is the argument for them — notice how it feels.

The interesting part is what happens at the edges. `/room/2` should work.
`/room/99` should be a clean `404`, because there is no room 99.
`/room/two` should *also* be a clean `404`, and you should not write a single
line of code to make that happen.

## Starter

Create `exercise-02-multiple-routes.py` and fill in the `TODO`s:

```python
"""exercise-02-multiple-routes.py — a tiny room directory.

Routes:
    GET /                     index of all rooms
    GET /room/<int:room_id>   one room, or 404
    GET /host/<username>      the rooms a person hosts
    GET /search?topic=...     rooms matching a topic
"""

from flask import Flask, abort, request, url_for

app: Flask = Flask(__name__)

ROOMS: dict[int, dict[str, str]] = {
    1: {"name": "Loops and Lists", "host": "ada", "topic": "python"},
    2: {"name": "HTTP by Hand", "host": "grace", "topic": "web"},
    3: {"name": "Reading Tracebacks", "host": "ada", "topic": "python"},
}


@app.route("/")
def index() -> str:
    """List every room, one per line, as `id: name (host: who)`."""
    ...  # TODO


@app.route("/room/<int:room_id>")
def show_room(room_id: int) -> str:
    """Show one room, or abort with 404 if the id is unknown."""
    ...  # TODO


@app.route("/host/<username>")
def show_host(username: str) -> str:
    """List the rooms this person hosts. Match the name case-insensitively."""
    ...  # TODO


@app.route("/search")
def search() -> str:
    """Match rooms by topic, read from the `topic` query parameter."""
    topic: str = request.args.get("topic", default="", type=str).strip().lower()
    ...  # TODO


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

## Requirements

1. `GET /` returns one line per room, in ascending id order, formatted
   exactly `1: Loops and Lists (host: ada)`.
2. `GET /room/2` returns exactly three lines:
   `Room 2: HTTP by Hand`, `Host: grace`, `Topic: web`.
3. `GET /room/99` returns a `404`. Use `abort(404)`, not a hand-written
   "not found" string with a 200 status. A wrong status code lies to every
   client that is not a human.
4. `GET /room/two` returns a `404` with no code of yours involved.
5. `GET /host/ADA` and `GET /host/ada` return the same thing: a first line
   `ada hosts 2 room(s):` followed by `1: Loops and Lists` and
   `3: Reading Tracebacks`. Lower-case the name before you compare.
6. `GET /host/nobody` returns exactly `nobody hosts no rooms.` with status
   `200`. A host with an empty schedule is not an error.
7. `GET /search?topic=python` returns `2 room(s) match topic 'python':`
   followed by the matching room lines. `GET /search` with no query string
   returns exactly `Try /search?topic=python`.
8. Every URL you emit in the index comes from `url_for`, not from an
   f-string with a slash in it.

## Constraints

- **Use `<int:room_id>`, never `<room_id>` plus `int(room_id)` in the body.**
  The manual version turns `/room/two` into an uncaught `ValueError: invalid
  literal for int() with base 10: 'two'` and a `500`. A `500` means "the
  server is broken"; the truth is "that URL does not exist", which is a
  `404`. The converter gets the status code right for free.
- **Separate lines with `"\n"`, and accept that the browser will show them
  on one line.** HTML collapses whitespace. That is not your bug to fix
  today — read the responses with `curl`, where the newlines are real. The
  fix is templates, which is the next exercise.
- **Give every view function a distinct name.** Two functions named `index`
  in one file is not a duplicate-route error, it is
  `AssertionError: View function mapping is overwriting an existing endpoint
  function: index` at import time, and the message rarely lands the first
  time you see it.
- **Read the query string with `request.args.get(..., default=...)`, not
  `request.args["topic"]`.** The bracket form raises on a missing key, and
  Flask turns that into a `400 Bad Request`. A missing optional parameter is
  not a bad request; it is the common case.
- **Do not sort the room ids by hand.** `sorted(ROOMS)` on a dict gives you
  the keys in order. Requirement 1 depends on the order, and dict insertion
  order is a promise about *this* literal, not about a dict you build later.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python exercise-02-multiple-routes.py
GET / -> 200
1: Loops and Lists (host: ada)
2: HTTP by Hand (host: grace)
3: Reading Tracebacks (host: ada)

GET /room/2 -> 200
Room 2: HTTP by Hand
Host: grace
Topic: web

GET /room/99 -> 404

GET /room/two -> 404

GET /host/ADA -> 200
ada hosts 2 room(s):
1: Loops and Lists
3: Reading Tracebacks

GET /host/nobody -> 200
nobody hosts no rooms.

GET /search?topic=python -> 200
2 room(s) match topic 'python':
1: Loops and Lists
3: Reading Tracebacks

GET /search -> 200
Try /search?topic=python
```

**The shipped file starts no server** — it drives the same routes with
`app.test_client()` and exits. Your own `exercise-02-multiple-routes.py`
serves on port 5000 and you read it with `curl`, one URL per command:

```console
$ curl http://127.0.0.1:5000/room/2
Room 2: HTTP by Hand
Host: grace
Topic: web

$ curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5000/room/two
404
```

The bodies and status codes are the same either way; only the transport
differs.

## Steps

1. Copy the starter into `exercise-02-multiple-routes.py` and run it.
2. Implement `index()` first. Build a list of strings and `"\n".join(...)`
   it — do not append to one string in a loop.
3. Implement `show_room()`. Check membership with `if room_id not in ROOMS:`
   and `abort(404)` before you touch the dict, so you never index a missing
   key.
4. In a second terminal, ask Flask what it knows:
   `flask --app exercise-02-multiple-routes routes`. Every route you have
   defined should be listed, plus the built-in `static` one. This command
   imports your file; it does not need the server to be running.
5. Implement `show_host()` and `search()`.
6. Test the two failure URLs on purpose: `/room/99` and `/room/two`. Confirm
   both are `404` and neither prints a traceback in your terminal. A
   traceback means your code ran when it should not have.
7. Quote your URLs in the shell when they contain `?` or `&`. Unquoted, your
   shell may eat them and you will debug a query string that was never sent.

## The Solution

```python
"""exercise-02-multiple-routes-solution.py — a tiny room directory, proven headless.

The four view functions are the exercise, unchanged in meaning from the
starter. Your own exercise-02-multiple-routes.py ends in
``app.run(debug=True)`` and you read the routes with curl; that is the right
way to work interactively. This shipped answer has to prove all four routes
work and then exit, so instead of binding a port it drives the app with
``app.test_client()`` — Flask's in-process fake browser — and prints each
status code and body. Same routes, same answers, no server.

Run it with::

    python exercise-02-multiple-routes-solution.py
"""

from flask import Flask, abort, request, url_for

app: Flask = Flask(__name__)

ROOMS: dict[int, dict[str, str]] = {
    1: {"name": "Loops and Lists", "host": "ada", "topic": "python"},
    2: {"name": "HTTP by Hand", "host": "grace", "topic": "web"},
    3: {"name": "Reading Tracebacks", "host": "ada", "topic": "python"},
}


@app.route("/")
def index() -> str:
    """List every room, one per line, as `id: name (host: who)`."""
    lines: list[str] = [
        f"{room_id}: {ROOMS[room_id]['name']} (host: {ROOMS[room_id]['host']})"
        for room_id in sorted(ROOMS)
    ]
    return "\n".join(lines)


@app.route("/room/<int:room_id>")
def show_room(room_id: int) -> str:
    """Show one room, or abort with 404 if the id is unknown."""
    if room_id not in ROOMS:
        abort(404)
    room: dict[str, str] = ROOMS[room_id]
    return "\n".join(
        [
            f"Room {room_id}: {room['name']}",
            f"Host: {room['host']}",
            f"Topic: {room['topic']}",
        ]
    )


@app.route("/host/<username>")
def show_host(username: str) -> str:
    """List the rooms this person hosts. Match the name case-insensitively."""
    who: str = username.strip().lower()
    hosted: list[int] = [
        room_id for room_id in sorted(ROOMS) if ROOMS[room_id]["host"] == who
    ]
    if not hosted:
        return f"{who} hosts no rooms."
    lines: list[str] = [f"{who} hosts {len(hosted)} room(s):"]
    lines += [f"{room_id}: {ROOMS[room_id]['name']}" for room_id in hosted]
    return "\n".join(lines)


@app.route("/search")
def search() -> str:
    """Match rooms by topic, read from the `topic` query parameter."""
    topic: str = request.args.get("topic", default="", type=str).strip().lower()
    if not topic:
        return f"Try {url_for('search', topic='python')}"
    matches: list[int] = [
        room_id for room_id in sorted(ROOMS) if ROOMS[room_id]["topic"] == topic
    ]
    lines: list[str] = [f"{len(matches)} room(s) match topic '{topic}':"]
    lines += [f"{room_id}: {ROOMS[room_id]['name']}" for room_id in matches]
    return "\n".join(lines)


#: Every URL the exercise page discusses, happy paths and failure paths alike.
REQUESTS: tuple[str, ...] = (
    "/",
    "/room/2",
    "/room/99",
    "/room/two",
    "/host/ADA",
    "/host/nobody",
    "/search?topic=python",
    "/search",
)


def main() -> None:
    """Hit every URL and print the status plus the body for the 200s."""
    client = app.test_client()
    for path in REQUESTS:
        response = client.get(path)
        print(f"GET {path} -> {response.status_code}")
        if response.status_code == 200:
            print(response.get_data(as_text=True))
        print()


if __name__ == "__main__":
    main()
```

**`<int:room_id>` is validation that runs before your function exists.** The
converter compiles into the URL rule's pattern, so `/room/two` does not match
`/room/<int:room_id>` at all. Werkzeug looks for another rule, finds none, and
raises `NotFound` — a 404 — while `show_room` sits untouched. Your function is
therefore free to assume `room_id` is an `int`, and the type hint on the
parameter is the truth rather than a hope.

**`abort(404)` before the lookup, never after.** The guard runs first so that
`ROOMS[room_id]` on the next line cannot raise `KeyError`. `flask.abort`
raises `werkzeug.exceptions.NotFound`; Flask catches it at the top of the
request and turns it into the 404 response. Nothing after the `abort` runs.

**A room that does not exist is a 404; a host with an empty schedule is a
200.** These feel similar and are not. `/room/99` names a resource that is not
there, so "not found" is the honest answer. `/host/nobody` asks a question
that has an answer — nobody hosts nothing — and an empty result set is a
perfectly good answer to a perfectly good question. Return a 404 there and
every script that talks to you will treat "this person is free" as "your
server is broken".

**Lower-case once, at the boundary.** `who = username.strip().lower()` happens
on the way in, and everything downstream compares and prints `who`. That is
why `/host/ADA` and `/host/ada` produce byte-identical responses. The
alternative is a `.lower()` sprinkled at every comparison, and the one you
forget is the bug.

**`sorted(ROOMS)` sorts the keys, and the output depends on it.** Iterating a
dict gives you insertion order, which happens to be 1, 2, 3 for this literal
and is a promise about *this* literal only. Requirement 1 pins the order, so
say what you mean.

**`request.args.get(..., default="", type=str)` cannot raise.** The bracket
form, `request.args["topic"]`, raises `BadRequestKeyError` on a missing key,
and Flask renders that as a bare `400 Bad Request` page. A missing optional
parameter is not a malformed request; it is the common case.

**`url_for` is doing real work in exactly one place here.** The one URL this
app prints is the search hint: `url_for('search', topic='python')` builds
`/search` from the endpoint name, and any keyword that is not a route variable
becomes a query parameter, so the whole string comes out as
`/search?topic=python` — with no slash typed by hand anywhere in the file.
Type the path as a literal instead and it keeps working right up until the app
is mounted under a prefix, at which point every hand-written path is wrong and
every `url_for` is still right.

## Run it

Copy the worked answer on this page into `exercise-02-multiple-routes.py` and run it:

```bash
python exercise-02-multiple-routes.py
```

It needs Flask installed and nothing else, and it exits on its own — the
`REQUESTS` tuple at the bottom walks every URL this page discusses, happy
paths and failure paths alike. To click around instead, run your own
`exercise-02-multiple-routes.py` and read it with `curl`.

The `-solution` in the filename keeps this file from colliding with your own
`exercise-02-multiple-routes.py`.

## Common bugs to catch

- **`werkzeug.routing.exceptions.BuildError: Could not build url for
  endpoint 'show_rooms'. Did you mean 'show_room' instead?`** `url_for` takes
  the *view function's* name, not the URL. The "did you mean" hint is
  usually right.
- **`TypeError: show_room() got an unexpected keyword argument 'id'`.** The
  name inside `<int:room_id>` must match the parameter name in the function
  signature exactly. Flask passes it as a keyword argument.
- **`/room/2` works but `/room/2/` gives a 404.** A route defined without a
  trailing slash matches only the exact path. Defined *with* one
  (`/rooms/`), Flask helpfully redirects `/rooms` to `/rooms/` with a `308`.
  The behaviour is asymmetric on purpose; pick one form and be consistent.
- **`/room/-1` is a 404, not a 400.** The `int` converter matches digits
  only, so the minus sign never matches. This is fine — just do not spend
  twenty minutes looking for the code that "rejected" it.
- **`404` on `/search` AND on `/search?topic=python`.** You wrote
  `@app.route("/search?topic=<topic>")`. Nothing raises — the rule registers
  with a literal `?` in it, and no URL can ever match it, because routing
  matches the *path* and the path stops at the `?`. Both requests 404, which
  is the tell: if adding a parameter broke the URL you already had, the
  parameter is in the wrong place. Query strings are never part of a route
  pattern. They live in `request.args`.
- **`AssertionError: View function mapping is overwriting an existing
  endpoint function`.** Two view functions share a name. Rename one.
- **Everything renders on one line in the browser and you conclude your
  join is broken.** It is not. Check with `curl` before you change code.
- **`RuntimeError: Working outside of request context`.** You called
  `request.args` at module level or inside a helper that runs at import
  time. `request` only exists while a request is being handled.

## Acceptance checklist

- [ ] All four routes respond, and `flask --app exercise-02-multiple-routes routes` lists them.
- [ ] `/room/99` and `/room/two` both return `404` with no traceback in the terminal.
- [ ] `/host/ADA` and `/host/ada` return identical output.
- [ ] `/host/nobody` returns `200`, not `404`.
- [ ] `/search` with no query string returns the hint line.
- [ ] No URL in your code is a hand-written string with a slash in it.
- [ ] The file is committed to Git with a message like `Add Week 9 exercise 2: multiple routes`.

## Stretch

- Add `/room/<int:room_id>/host` that `redirect`s to
  `url_for("show_host", username=...)`. Watch the `302` and then the `200` in
  the two log lines it produces.
- Add a second query parameter, `?limit=2`, read with
  `request.args.get("limit", default=10, type=int)`. Feed it `?limit=abc` and
  note that you get the default back rather than an exception — `type=` fails
  quietly by design.
- Add `/room/new` as a static route alongside `/room/<int:room_id>`. It works,
  and the ordering of the two decorators does not matter: Werkzeug ranks the
  more specific rule first. Confirm that yourself rather than taking it on
  faith.

When your directory answers all four routes, move on to
[Exercise 3 — Template Loop](./exercise-03-template-loop.md).
