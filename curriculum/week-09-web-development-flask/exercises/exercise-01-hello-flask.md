# Exercise 1 — Hello, Flask

> **Topic:** A minimal Flask app with a single route, started and stopped from the terminal
> **Lecture:** [01 — Flask Hello World](../lecture-notes/01-flask-hello-world.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** every other Flask exercise, challenge, and the mini-project all start by running a server and hitting it from a browser. If starting and stopping a server is still fiddly for you, every later bug will look like a Flask bug when it is really a "the server was not running" bug. Do the loop once, deliberately, on an app small enough that nothing else can be wrong.

## The Brief

The Code Crunch community runs a weekly study hall. Right now, whether it is
open is announced in chat and scrolls away. You are going to serve that one
fact over HTTP instead, so that a browser — or a script, or a phone — can ask
the question directly.

The whole app is one route that returns one sentence. That is deliberate. The
point of this exercise is not the sentence; it is the loop around it: start
the server, read what it printed, make a request, watch the log line appear,
stop the server. You will run that loop several hundred times before this
bootcamp ends.

## Starter

Create `exercise-01-hello-flask.py` in your practice repo with this content,
then fill in the `TODO`s:

```python
"""exercise-01-hello-flask.py — the smallest useful Flask app.

Serves one route, GET /, which reports whether the Code Crunch study
hall is open. Run with: python exercise-01-hello-flask.py
"""

from flask import Flask

app: Flask = Flask(__name__)

STUDY_HALL_OPEN: bool = True


@app.route("/")
def index() -> str:
    """Return the study hall status as a single line of text."""
    # TODO: return "Code Crunch study hall is open." when STUDY_HALL_OPEN
    # is True, and "Code Crunch study hall is closed." when it is False.
    ...


if __name__ == "__main__":
    # debug=True is for your laptop only. See the Constraints section.
    app.run(debug=True)
```

## Requirements

1. The module has a docstring on the first line, and `index()` has one too.
2. `GET /` returns exactly `Code Crunch study hall is open.` when
   `STUDY_HALL_OPEN` is `True` — capital C, capital C, trailing period, no
   HTML tags.
3. Flipping `STUDY_HALL_OPEN` to `False` and saving the file makes `GET /`
   return exactly `Code Crunch study hall is closed.` You should not have to
   restart the server by hand to see the change.
4. The app runs with `python exercise-01-hello-flask.py` and serves on
   `http://127.0.0.1:5000`.
5. The `if __name__ == "__main__":` guard stays. It is what lets you later
   run the same file under `gunicorn` without the dev server also firing up.

## Constraints

- **Return one string, not HTML.** A view function that returns a `str` gets
  a `200` with `Content-Type: text/html`. You do not need tags yet, and
  leaving them out keeps the response small enough to read in full in your
  terminal with `curl`.
- **Do not build the sentence with string concatenation across an `if`.**
  Write two complete literal sentences and pick one. Requirement 2 compares
  the output character for character, and concatenation is where a missing
  space or a doubled period sneaks in.
- **`debug=True` is for your laptop and nowhere else.** Debug mode gives you
  auto-reload and an in-browser traceback, and the traceback page includes an
  interactive Python console. Anyone who can load that page can run arbitrary
  code on the machine hosting it. Shipping `debug=True` to a public host is
  not a style problem, it is a remote-code-execution hole. Production runs
  under `gunicorn` with debug off — lecture 3, section 8.
- **Bind to `127.0.0.1` (the default). Do not pass `host="0.0.0.0"` yet.**
  `0.0.0.0` accepts connections from your whole network, and with debug on
  that means handing the console to everyone on the coffee-shop wifi.
- **Stop the server with Ctrl-C, not by closing the terminal tab.** A closed
  tab can leave the port held, and then your next run fails with a confusing
  "address already in use" instead of starting.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python exercise-01-hello-flask.py
GET /      -> 200 text/html; charset=utf-8
Code Crunch study hall is open.

Flip STUDY_HALL_OPEN to False and ask again:
GET /      -> 200
Code Crunch study hall is closed.

A URL nobody registered:
GET /index -> 404
```

**The shipped file starts no server.** It proves the route with
`app.test_client()` — Flask's in-process fake browser — and exits, which is
what lets it print the same lines every time. Your own
`exercise-01-hello-flask.py` ends in `app.run(debug=True)` instead, so it
serves until you Ctrl-C, and what you see is a two-terminal session. Terminal
one, the server:

```console
$ python exercise-01-hello-flask.py
 * Serving Flask app 'exercise-01-hello-flask'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 140-627-828
127.0.0.1 - - [22/Aug/2026 09:14:02] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [22/Aug/2026 09:14:02] "GET /favicon.ico HTTP/1.1" 404 -
```

Terminal two, a client:

```console
$ curl http://127.0.0.1:5000/
Code Crunch study hall is open.
```

Your line 6 may read `* Restarting with watchdog (windowsapi)` instead of
`* Restarting with stat`. Both are the reloader; Werkzeug uses the faster
file-system-event backend when the `watchdog` package is installed and falls
back to polling timestamps when it is not.

## Steps

1. Activate your Week 9 virtual environment and confirm Flask is there:
   `python -c "import flask; print(flask.__version__)"`.
2. Create `exercise-01-hello-flask.py`, paste the starter, fill in the `TODO`.
3. Run it: `python exercise-01-hello-flask.py`. Read every line it printed
   before you touch the browser.
4. Open <http://127.0.0.1:5000> and look back at the terminal. You should see
   a new `"GET / HTTP/1.1" 200 -` line. No line means the request never
   reached this server.
5. With the server still running, change `STUDY_HALL_OPEN` to `False` and
   save. Watch the terminal print `* Detected change in ...`, then refresh
   the browser. That is the reloader earning its keep.
6. Set it back to `True`, then stop the server with Ctrl-C and refresh once
   more. The browser should now fail to connect — that is what "the server is
   not running" looks like, and it is worth seeing on purpose once.

## The Solution

```python
"""exercise-01-hello-flask-solution.py — the smallest useful Flask app, proven headless.

The exercise part is the starter with its one TODO filled in: one route,
GET /, which reports whether the Code Crunch study hall is open.

Your own exercise-01-hello-flask.py ends in ``app.run(debug=True)`` and sits
serving http://127.0.0.1:5000 until you press Ctrl-C — the right tool for
working interactively. A shipped answer cannot sit waiting for a browser, so
this file proves the route works and then exits: it drives the app with
``app.test_client()``, Flask's in-process fake browser, which calls your app
directly with no port, no second terminal, and no Ctrl-C. The route being
tested is identical either way.

Run it with::

    python exercise-01-hello-flask-solution.py
"""

from flask import Flask

app: Flask = Flask(__name__)

STUDY_HALL_OPEN: bool = True


@app.route("/")
def index() -> str:
    """Return the study hall status as a single line of text."""
    if STUDY_HALL_OPEN:
        return "Code Crunch study hall is open."
    return "Code Crunch study hall is closed."


def main() -> None:
    """Fire the requests the exercise page discusses and print what came back."""
    global STUDY_HALL_OPEN
    client = app.test_client()

    response = client.get("/")
    print(f"GET /      -> {response.status_code} {response.headers['Content-Type']}")
    print(response.get_data(as_text=True))

    print()
    print("Flip STUDY_HALL_OPEN to False and ask again:")
    STUDY_HALL_OPEN = False
    response = client.get("/")
    print(f"GET /      -> {response.status_code}")
    print(response.get_data(as_text=True))
    STUDY_HALL_OPEN = True

    print()
    print("A URL nobody registered:")
    response = client.get("/index")
    print(f"GET /index -> {response.status_code}")


if __name__ == "__main__":
    main()
```

**Two complete sentences, and the `if` picks one.** The constraint above
forbids building the string across the branch, and it is worth seeing why. The
tempting version is one line shorter:

```python
state = "open" if STUDY_HALL_OPEN else "closed"
return "Code Crunch study hall is" + " " + state + " ."
```

and it produces `'Code Crunch study hall is open .'` — a space before the
period. Requirement 2 compares character for character, so that fails, and
when it fails you will be staring at the `if`, which is fine, rather than at
the four string fragments, which is where the bug is. Write the sentence you
want to see.

**No `else` after the `return`.** Both branches return, so nothing can fall
off the end of the function — and falling off the end is exactly what produces
the most common error in this exercise, listed below.

**`STUDY_HALL_OPEN` is read when the request arrives, not when the file is
imported.** The name is looked up inside `index()` every time the function
runs. That is what makes step 5 work: change the constant, save, and the next
request answers differently. Freeze the sentence into a module-level constant
instead and it would *appear* to work too — but only because the reloader
restarts the whole process on every save, which is a crutch a production
server does not have.

**A view function that returns a `str` becomes a 200 response** with
`Content-Type: text/html; charset=utf-8`, which is what the first output line
proves. Flask wraps the string for you; a `dict` would become JSON and a
`(body, status)` tuple sets the code — both show up in the stretch.

**`app.test_client()` is how the shipped answer runs without a server.** It
is a real client for your WSGI app that skips the network entirely: no port,
no socket, no Ctrl-C, and the `404` for `/index` at the end is produced by
exactly the same routing that a browser request would hit. Your own file keeps
`app.run(debug=True)` because *you* need a server to click around; a published
answer needs to prove itself and exit. Week 11 builds its whole testing story
on this object.

## Run it

Copy the worked answer on this page into `exercise-01-hello-flask.py` and run it:

```bash
python exercise-01-hello-flask.py
```

It needs Flask installed and nothing else, and it exits on its own — no
server, no Ctrl-C. To click around instead, run your own
`exercise-01-hello-flask.py`, which ends in `app.run(debug=True)` and serves
until you stop it.

The `-solution` in the filename keeps this file from colliding with your own
`exercise-01-hello-flask.py`.

## Common bugs to catch

- **The browser shows the page but the terminal shows no log line.** You are
  looking at a cached response, or at a second copy of the server you started
  earlier and forgot. Hard-refresh, and check for stray Python processes.
- **`OSError: [Errno 48] Address already in use`** (Windows:
  `[WinError 10048]`). Something is already on port 5000 — usually a previous
  run you did not Ctrl-C. Kill it, or run on another port with
  `app.run(debug=True, port=5001)`.
- **On macOS, port 5000 answers with an unexpected 403 or an AirPlay page.**
  AirPlay Receiver listens on 5000. Turn it off in System Settings, or use
  `port=5001`.
- **`TypeError: The view function for 'index' did not return a valid
  response. The function either returned None or ended without a return
  statement.`** You left the `...` in place, or your `if` has a branch that
  falls off the end without returning.
- **`404 Not Found` at `/`.** You wrote `@app.route("index")` or
  `@app.route("/index")`. The root route pattern is the single character `/`.
- **A `"GET /favicon.ico HTTP/1.1" 404 -` line appears and worries you.** It
  should not. Every browser asks for a site icon; you have not made one. It
  is noise, not a bug. `curl` never asks for it, which is one reason `curl`
  is the cleaner way to read a response.
- **`jinja2` or `werkzeug` errors on import, or `ModuleNotFoundError: No
  module named 'flask'`.** Your virtual environment is not active, so
  `python` is a different interpreter than the one you `pip install`ed into.
- **Ctrl-C prints a traceback ending in `KeyboardInterrupt`.** That is normal
  and means the shutdown worked. It is not a crash.

## Acceptance checklist

- [ ] `python exercise-01-hello-flask.py` starts a server with no traceback.
- [ ] `curl http://127.0.0.1:5000/` prints the open sentence exactly.
- [ ] The terminal logs a `200` line for each request you make.
- [ ] Flipping `STUDY_HALL_OPEN` to `False` changes the response without a manual restart.
- [ ] Ctrl-C stops the server, and the browser then fails to connect.
- [ ] You can state, in one sentence, why `debug=True` must not ship.
- [ ] The file is committed to Git with a message like `Add Week 9 exercise 1: hello flask`.

## Stretch

- Add a `/healthz` route that returns the tuple `("OK", 200)`. Hosts use a
  route like this to decide whether your app is alive; you will want it when
  you deploy in lecture 3.
- Return a `dict` from a new `/api/status` route, such as
  `{"open": STUDY_HALL_OPEN}`. Flask serialises dicts to JSON for you. Hit it
  with `curl` and compare the `Content-Type` header to the one `/` sends
  (`curl -i` shows headers).
- Run the same file under a production server. On macOS or Linux:
  `pip install gunicorn` then
  `gunicorn "exercise-01-hello-flask:app" --bind 127.0.0.1:8000`. Gunicorn
  does not run on Windows; use `pip install waitress` and
  `waitress-serve --port=8000 exercise-01-hello-flask:app` instead. Either
  way, edits no longer reload and no debugger appears. That is the point.

When your one route answers reliably, move on to
[Exercise 2 — Multiple Routes](./exercise-02-multiple-routes.md).
