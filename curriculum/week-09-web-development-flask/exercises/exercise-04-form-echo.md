# Exercise 4 — Form Echo

> **Topic:** `POST` handling, reading `request.form`, server-side validation, and `flash`
> **Lecture:** [03 — Forms, Sessions, and Deployment](../lecture-notes/03-forms-sessions-deployment.md)
> **Difficulty:** Medium
> **Target time:** 1 hour 15 minutes
> **Why this one:** this is the first exercise where a stranger's typing reaches your code. Everything you have written so far served data you wrote yourself. From here on, the input is hostile until proven otherwise, and the three habits that make it safe — validate on the server, redirect after a successful post, let the template escape — are all in this one page. Both challenges and the mini-project's create-post form are this exercise with more fields.

## The Brief

The study hall has a shout-out board: you type your handle and a short
message, hit the button, and the page echoes it back to you as a
confirmation banner. One page, one form, one route that answers both `GET`
and `POST`.

Nothing is stored. That is deliberate — storing a list of shout-outs is
Challenge 01's job, and leaving it out here keeps the exercise focused on the
round trip: browser posts, server validates, server flashes, browser follows
a redirect and renders the message.

Then you will attack it. You will post to your own server with `curl`, which
ignores every `required` and `maxlength` attribute in your HTML, and you will
watch your server-side checks catch what the browser would have. You will
also post `<script>alert(1)</script>` as a message and watch Jinja2 render it
as text instead of running it.

## Directory layout

```text
exercise-04-form-echo/
├── .env                 <- your real dev secret; NEVER committed
├── .env.example         <- a placeholder; committed
├── .gitignore
├── app.py
└── templates/
    └── form.html
```

`.gitignore`:

```text
.env
.venv/
__pycache__/
```

`.env.example` (committed, so the next person knows what to set):

```text
SECRET_KEY=generate-your-own-with-secrets-token-hex-32
```

Generate your real one and put it in `.env`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Starter

### `app.py`

```python
"""app.py — a one-page shout-out form that echoes what you typed, safely.

Run from inside exercise-04-form-echo/:
    python app.py
"""

import os

from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

load_dotenv()  # reads .env in development; a no-op if the file is absent

app: Flask = Flask(__name__)

# flash() and session need a signing key. Read it from the environment so the
# real key never lands in Git; fall back to an obviously fake dev value.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")

MAX_MESSAGE_LEN: int = 200


@app.route("/", methods=["GET", "POST"])
def echo() -> str | Response:
    """Show the form on GET; validate, flash, and redirect on POST."""
    if request.method == "POST":
        handle: str = request.form.get("handle", "").strip()
        message: str = request.form.get("message", "").strip()

        errors: list[str] = []
        # TODO: append "Handle is required." when handle is empty
        # TODO: append "Message is required." when message is empty
        # TODO: append f"Message must be {MAX_MESSAGE_LEN} characters or fewer."
        #       when message is longer than MAX_MESSAGE_LEN

        if errors:
            for problem in errors:
                flash(problem, category="error")
            # Re-render with what they typed so nobody has to start over.
            return render_template("form.html", handle=handle, message=message)

        # TODO: flash the echo with category "success", in exactly this form:
        #       @<handle> said: <message>
        # TODO: redirect back to this same route (Post / Redirect / Get)
        ...

    return render_template("form.html", handle="", message="")


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

### `templates/form.html`

Complete; type it or copy it, but read the two commented lines.

```jinja
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Shout-out board — Code Crunch</title>
  </head>
  <body>
    <h1>Study-hall shout-out board</h1>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul class="flashes">
          {% for category, message in messages %}
            <li class="flash flash-{{ category }}">{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <form method="post" action="{{ url_for('echo') }}">
      <label for="handle">Your handle</label>
      {# `name` is what the server sees. `id` only wires up the label. #}
      <input type="text" id="handle" name="handle"
             value="{{ handle }}" maxlength="40" required>

      <label for="message">Shout-out</label>
      {# A textarea's value goes BETWEEN the tags, never in a value="". #}
      <textarea id="message" name="message" rows="4"
                maxlength="200" required>{{ message }}</textarea>

      <button type="submit">Post it</button>
    </form>
  </body>
</html>
```

## Requirements

1. `GET /` returns `200` and shows an empty form.
2. A valid `POST /` flashes exactly `@ada said: nice work` (category
   `success`) and returns a `302` to `/`. The following `GET /` renders the
   message and returns `200`.
3. Refreshing after a successful post does **not** re-submit and does **not**
   show the message a second time. A flash is consumed by the page that
   displays it.
4. An empty handle flashes `Handle is required.` with category `error`, and
   the response is a `200` that re-renders the form with the message the user
   already typed still in the textarea.
5. A message longer than 200 characters flashes
   `Message must be 200 characters or fewer.` The limit comes from
   `MAX_MESSAGE_LEN`, not from a literal typed twice.
6. Posting `<script>alert(1)</script>` as the message echoes it as visible
   text. The page source must show `&lt;script&gt;`, and no dialog appears.
7. Every problem a submission actually has is reported in one response. An
   empty handle *and* an empty message produce two error flashes together —
   and two is the real maximum, because a message that is empty cannot also
   be longer than 200 characters. Report what is wrong all at once; never
   make the user fix one field per round trip.

## Constraints

- **Read the secret key from the environment with a dev fallback, exactly as
  the starter does.** A hard-coded secret is a real defect, not a style
  preference. Flask signs the session cookie with it, and `flash` lives in
  that cookie — so anyone holding the key can mint a cookie your server will
  trust. Commit it once and it is in your Git history forever, recoverable
  from any clone, long after you "removed" it in a later commit. Public repo,
  public key. And a key written in code is the key that quietly ships to
  production, where it is the same one every reader of your repo already has.
  The dev fallback string is deliberately named so that seeing it in a
  production log is an alarm.
- **`debug=True` is for your laptop only.** The debug traceback page includes
  an interactive Python console. On a public host that is remote code
  execution. Deployment runs `gunicorn` with debug off.
- **Validate on the server even though the HTML says `required`.** `required`
  and `maxlength` are conveniences for cooperative browsers. `curl` ignores
  them completely, and so does anyone who opens DevTools and deletes the
  attribute. Client-side validation is a nicety; server-side validation is
  the actual rule.
- **Use `request.form.get("handle", "")`, not `request.form["handle"]`.** The
  bracket form raises `BadRequestKeyError`, which Flask turns into a bare
  `400` page. A missing field is a case you want to handle with your own
  message, not a stack trace.
- **Redirect after a successful POST; re-render after a failed one.** That
  asymmetry is the whole Post/Redirect/Get pattern. Redirecting on success
  makes the destination an idempotent `GET`, so refresh is harmless.
  Re-rendering on failure keeps the user's typing on screen; a redirect would
  throw it away and make them start over.
- **Never put `|safe` on the flashed message.** It is user input, round
  tripped through a cookie. `{{ message }}` escapes it; `{{ message|safe }}`
  is the textbook stored-XSS bug.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python exercise-04-form-echo.py
GET  / -> 200 (the empty form)

A valid shout-out — Post / Redirect / Get:
POST / -> 302  Location: /
GET  / -> 200
  <li class="flash flash-success">@ada said: nice work</li>
refresh once more: the flash is gone -> True

An empty handle — curl would send this; a browser would not:
POST / -> 200 (re-rendered, not redirected)
  <li class="flash flash-error">Handle is required.</li>
the typing survived -> True

A 201-character message:
  <li class="flash flash-error">Message must be 200 characters or fewer.</li>

Two problems in one submission, two flashes in one response:
  <li class="flash flash-error">Handle is required.</li>
  <li class="flash flash-error">Message is required.</li>

The attack — a script tag, echoed as text:
  <li class="flash flash-success">@ada said: &lt;script&gt;alert(1)&lt;/script&gt;</li>
raw <script> reached the page -> False
```

**The shipped file starts no server** — it drives the same route with
`app.test_client()`, whose built-in cookie jar is what lets the flash survive
the redirect, and exits. Your own build serves on port 5000, where one good
submission plus a refresh logs this shape:

```console
127.0.0.1 - - [22/Aug/2026 14:31:08] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [22/Aug/2026 14:31:19] "POST / HTTP/1.1" 302 -
127.0.0.1 - - [22/Aug/2026 14:31:19] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [22/Aug/2026 14:31:33] "GET / HTTP/1.1" 200 -
```

Posting from `curl` proves the same paths over real HTTP. The cookie jar
matters: the flash rides in the session cookie, so without `-c`/`-b` the
message is set and then thrown away.

```console
$ curl -s -c jar.txt -b jar.txt -L \
    --data-urlencode "handle=ada" \
    --data-urlencode "message=nice catch on that <script> bug" \
    http://127.0.0.1:5000/ | grep flash-
<li class="flash flash-success">@ada said: nice catch on that &lt;script&gt; bug</li>
```

The same request with the handle removed — the browser would have blocked
this, and `curl` does not care:

```console
$ curl -s -c jar.txt -b jar.txt \
    --data-urlencode "handle=" \
    --data-urlencode "message=hi" \
    http://127.0.0.1:5000/ | grep flash-
<li class="flash flash-error">Handle is required.</li>
```

## Steps

1. Build the tree. Write `.gitignore` **first**, before `.env` exists, so
   there is no window in which the secret is trackable.
2. Generate a key, put it in `.env`, and confirm `git status` does not list
   `.env`.
3. Fill in the four `TODO`s in `app.py`. Build the whole `errors` list before
   you branch on it, so one submission reports every problem it actually has.
4. Run `python app.py`, submit a valid shout-out in the browser, and watch
   the terminal show `302` then `200`.
5. Refresh. The flash should be gone and no resubmission warning should
   appear. If your browser offers to re-send the form, you returned a
   rendered page on success instead of a redirect.
6. Post `<script>alert(1)</script>` as the message. Read the page source and
   confirm `&lt;script&gt;`.
7. Run both `curl` commands above. The first proves the happy path end to
   end; the second proves your server does not depend on the browser to
   enforce anything.
8. Temporarily comment out the `app.secret_key` line and submit again. Read
   the exception carefully — it is the first entry in the bug list below, and
   it is one you will meet again.

## The Solution

```python
"""exercise-04-form-echo-solution.py — the shout-out form, proven headless.

The exercise part is the starter with its four TODOs filled in: read, validate,
flash, and either redirect (success) or re-render (failure). The template is
the exact `templates/form.html` the exercise page gives you, carried inside
the file in the ``FORM_HTML`` constant and handed to Jinja through a
``DictLoader`` so this one file runs anywhere.

Two deliberate differences from the folder you build yourself:

1. **No `.env`, no `python-dotenv`.** Your build loads the secret key from a
   `.env` file with ``load_dotenv()``. This download reads the environment
   directly and falls back to the same obviously-fake dev value, so it needs
   nothing installed beyond Flask. The rule it teaches is identical: the key
   comes from the environment, never from the source.
2. **No server starts.** Your build ends in ``app.run(debug=True)``. This file
   drives the app with ``app.test_client()`` — Flask's in-process fake
   browser, which also keeps a cookie jar, so flashes survive the redirect
   exactly as they do in a real browser — prints each round trip, and exits.

Run it with::

    python exercise-04-form-echo-solution.py
"""

import os

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from jinja2 import DictLoader

#: templates/form.html, byte for byte as the exercise page gives it.
FORM_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Shout-out board — Code Crunch</title>
  </head>
  <body>
    <h1>Study-hall shout-out board</h1>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul class="flashes">
          {% for category, message in messages %}
            <li class="flash flash-{{ category }}">{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <form method="post" action="{{ url_for('echo') }}">
      <label for="handle">Your handle</label>
      {# `name` is what the server sees. `id` only wires up the label. #}
      <input type="text" id="handle" name="handle"
             value="{{ handle }}" maxlength="40" required>

      <label for="message">Shout-out</label>
      {# A textarea's value goes BETWEEN the tags, never in a value="". #}
      <textarea id="message" name="message" rows="4"
                maxlength="200" required>{{ message }}</textarea>

      <button type="submit">Post it</button>
    </form>
  </body>
</html>
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader({"form.html": FORM_HTML})

# flash() and session need a signing key. Read it from the environment so the
# real key never lands in Git; fall back to an obviously fake dev value.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")

MAX_MESSAGE_LEN: int = 200


@app.route("/", methods=["GET", "POST"])
def echo() -> str | Response:
    """Show the form on GET; validate, flash, and redirect on POST."""
    if request.method == "POST":
        handle: str = request.form.get("handle", "").strip()
        message: str = request.form.get("message", "").strip()

        errors: list[str] = []
        if not handle:
            errors.append("Handle is required.")
        if not message:
            errors.append("Message is required.")
        if len(message) > MAX_MESSAGE_LEN:
            errors.append(f"Message must be {MAX_MESSAGE_LEN} characters or fewer.")

        if errors:
            for problem in errors:
                flash(problem, category="error")
            # Re-render with what they typed so nobody has to start over.
            return render_template("form.html", handle=handle, message=message)

        flash(f"@{handle} said: {message}", category="success")
        return redirect(url_for("echo"))

    return render_template("form.html", handle="", message="")


def flash_lines(page: str) -> list[str]:
    """Pull the rendered flash <li> lines out of a page, stripped."""
    return [line.strip() for line in page.splitlines() if 'class="flash ' in line]


def main() -> None:
    """Drive every round trip the exercise page discusses and print each one."""
    client = app.test_client()

    response = client.get("/")
    print(f"GET  / -> {response.status_code} (the empty form)")

    print()
    print("A valid shout-out — Post / Redirect / Get:")
    response = client.post("/", data={"handle": "ada", "message": "nice work"})
    print(f"POST / -> {response.status_code}  Location: {response.headers['Location']}")
    response = client.get("/")
    print(f"GET  / -> {response.status_code}")
    for line in flash_lines(response.get_data(as_text=True)):
        print(f"  {line}")
    body = client.get("/").get_data(as_text=True)
    print(f"refresh once more: the flash is gone -> {not flash_lines(body)}")

    print()
    print("An empty handle — curl would send this; a browser would not:")
    response = client.post("/", data={"handle": "", "message": "hi"})
    body = response.get_data(as_text=True)
    print(f"POST / -> {response.status_code} (re-rendered, not redirected)")
    for line in flash_lines(body):
        print(f"  {line}")
    print(f"the typing survived -> {'required>hi</textarea>' in body}")

    print()
    print("A 201-character message:")
    response = client.post("/", data={"handle": "ada", "message": "x" * 201})
    for line in flash_lines(response.get_data(as_text=True)):
        print(f"  {line}")

    print()
    print("Two problems in one submission, two flashes in one response:")
    response = client.post("/", data={"handle": "", "message": ""})
    for line in flash_lines(response.get_data(as_text=True)):
        print(f"  {line}")

    print()
    print("The attack — a script tag, echoed as text:")
    client.post("/", data={"handle": "ada", "message": "<script>alert(1)</script>"})
    body = client.get("/").get_data(as_text=True)
    for line in flash_lines(body):
        print(f"  {line}")
    print(f"raw <script> reached the page -> {'<script>' in body}")


if __name__ == "__main__":
    main()
```

**One route, two methods, and the `if` at the top is the whole shape.** `GET`
falls through to the last line and renders an empty form. `POST` reads,
validates, and then does one of two different things. That asymmetry is the
lesson.

**Redirect on success; re-render on failure.** Post/Redirect/Get exists so
that the page a user is looking at was produced by a `GET`. Refresh then
re-issues that `GET`, which is harmless, and the browser never offers to
re-send the form. Success redirects because there is nothing left to show;
failure re-renders because there is — the user's typing, which a redirect
would throw away and make them enter again. Look at what the two paths cost:
success is `POST 302` then `GET 200`, two requests; failure is a single
`POST 200`. That extra hop is what buys the refresh-safety.

**The `errors` list is built completely before anything is flashed.** Three
independent `if`s, no `elif`, no early return. Return on the first problem and
a submission with two mistakes takes two round trips to discover both, which
is exactly the form-filling experience everyone complains about. (As
requirement 7 says, two errors at once is also the ceiling: the "empty" check
and the "too long" check on the same field are mutually exclusive.)

**`request.form.get("handle", "")` never raises; `request.form["handle"]`
does.** The bracket form raises `BadRequestKeyError`, which Flask renders as a
bare `400 Bad Request` page with no explanation for the user and no message of
yours anywhere. A field the browser did not send is a case you want to answer
in your own words.

**`.strip()` at the read, so whitespace is not content.** A message of four
spaces strips to the empty string and is rejected, and a handle typed with a
trailing space matches one typed without. Normalise on the way in, then trust
the value.

**`flash` is a list in the session, and the session is a signed cookie.** That
one sentence explains most of this exercise's surprises. It is why
`app.secret_key` is mandatory — no key, no signature, no session, no flash. It
is why the message survives a redirect but is gone on the next page: reading
the queue empties it. And it is why the shipped file's cookie-jar-equipped
test client shows the same behaviour a browser does. The Under the hood block
below opens a real session cookie up.

**`{{ message }}` escapes, and it must.** The flashed text is user input that
has been round-tripped through a cookie. Jinja escapes it on the way out, so
`<script>alert(1)</script>` renders as visible text. Put `|safe` on it and you
have written the textbook stored-XSS bug.

## Run it

Copy the worked answer on this page into `exercise-04-form-echo.py` and run it:

```bash
python exercise-04-form-echo.py
```

It needs Flask installed and nothing else — no `.env`, no `python-dotenv`,
no `templates/` folder — and it exits on its own. Your own build keeps the
full tree this page teaches, `.env` and `.gitignore` included, because the
secret-handling habit is most of the point.

The `-solution` in the filename keeps this file from colliding with your own
exercise folder.

## Common bugs to catch

- **`RuntimeError: The session is unavailable because no secret key was set.
  Set the secret_key on the application to something unique and secret.`**
  `flash` writes to the session, and the session is a signed cookie. No key,
  no signature, no flash.
- **`405 Method Not Allowed` when you submit.** The route is missing
  `methods=["GET", "POST"]`, so it accepts `GET` only. The page loads fine,
  which is why this one confuses people.
- **The handle is always empty no matter what you type.** Your `<input>` has
  an `id` but no `name`, or the `name` does not match the string in
  `request.form.get(...)`. The server only ever sees `name`.
- **`werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: The browser (or
  proxy) sent a request that this server could not understand. KeyError:
  'handle'`.** You used `request.form["handle"]` on a request that did not
  include the field.
- **The textarea always renders empty on a validation error.** You wrote
  `<textarea value="{{ message }}">`. A textarea has no `value` attribute;
  its content is whatever sits between the opening and closing tags.
- **The textarea gains leading blank space on every re-render.** You put
  `{{ message }}` on its own indented line. Everything between the tags is
  content, indentation included. Keep it tight against the tags.
- **The flash never shows up in the browser.** Either the template is missing
  the `get_flashed_messages` block, or you submitted to `localhost:5000` and
  got redirected to `127.0.0.1:5000` (or the reverse) — those are different
  cookie hosts, so the session cookie does not come back. Pick one spelling
  and stay on it.
- **The form comes back empty after a validation error, wiping the user's
  typing.** You called `render_template("form.html")` with no arguments on
  the failure path. This does *not* raise — `{{ handle }}` on an undefined
  name renders as an empty string under Jinja's default `Undefined`, so the
  page is a clean `200` with blank fields, which on the first `GET` even
  looks correct. The bug only shows when a rejected submission loses the
  draft. Pass `handle=handle, message=message` on the failure re-render, and
  `handle="", message=""` on the plain `GET`, so both paths say what they
  mean.

## Under the hood

<details>
<summary>Under the hood — a session cookie, opened with your own hands</summary>

`flash` stores its queue in `session`, and a Flask session is a **signed
cookie**: the dict is serialised to JSON, base64-encoded, and stamped with an
HMAC computed from `SECRET_KEY`. Here is a real one from the visit-counter
stretch, split at the first dot and base64-decoded:

```text
cookie:  eyJjb3VudCI6M30.aoretQ.CjvxuQvfwmxGdtVAbPnlrZDtXEE
payload: b'{"count":3}'
```

Your data, in plain text, in the browser. **Signed is not encrypted.** Anyone
holding the cookie can read every byte of it; the signature only stops them
*changing* it, because they cannot recompute the HMAC without the key. That
gives you two rules at once:

1. Never put anything in a session you would mind the visitor reading — no
   passwords, no tokens, nothing private. Facts you would print on a postcard
   only: a counter, a locale, an `is_admin` flag.
2. Whoever holds `SECRET_KEY` can mint a cookie your server will trust. That
   is the whole reason the key comes from the environment and never from the
   source: commit it once and it is recoverable from every clone of the repo
   forever, long after a later commit "removed" it.

It also explains the flash lifecycle with no extra machinery. The message
survives the redirect because the cookie rides along on the next request; it
disappears afterwards because rendering the widget reads the queue, and
reading it deletes it from the session — which rewrites the cookie without
it. There is no server-side store to clean up, because there is no
server-side store.

</details>

## Acceptance checklist

- [ ] A valid submission logs `POST 302` followed by `GET 200`, and the flash reads `@ada said: nice work`.
- [ ] Refreshing afterwards shows no message and triggers no resubmission prompt.
- [ ] An empty handle and an empty message reported in one submission produce two error flashes.
- [ ] A 201-character message is rejected with the exact length message.
- [ ] `<script>alert(1)</script>` renders as text; the source shows `&lt;script&gt;`.
- [ ] `git status` never lists `.env`, and `.env.example` is committed in its place.
- [ ] `app.secret_key` reads from `os.environ`, and you can explain in one sentence why a committed key is unfixable by a later commit.
- [ ] The folder is committed to Git with a message like `Add Week 9 exercise 4: form echo`.

## Stretch

- Add a visit counter with `session["count"] = session.get("count", 0) + 1`
  and show it in the template. Then open the cookie in DevTools and decode
  the base64 payload — Flask sessions are *signed*, not *encrypted*, and
  seeing your own data in plain text is the fastest way to remember never to
  put anything sensitive in there.
- Add `pip install flask-wtf` and convert the form to a `FlaskForm` with a
  CSRF token. Then submit with `curl` again and watch it get rejected — that
  rejection is the entire point of CSRF protection.
- Style the two flash categories with a `static/style.css`:
  `.flash-error` red, `.flash-success` green. Two rules, and the page
  suddenly reads as finished.
- Add a `/clear` route that calls `session.clear()` and redirects home.

That is the last exercise for Week 9. The lectures are behind you; now go
build something bigger with them in
[the Week 9 challenges](../challenges/README.md).
