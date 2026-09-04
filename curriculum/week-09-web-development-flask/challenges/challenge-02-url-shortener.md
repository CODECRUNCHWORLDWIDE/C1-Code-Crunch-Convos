# Challenge 02 — Tiny URL Shortener

> **Topic:** POST + redirect, secure slug generation with `secrets`, URL validation, dynamic routes, and per-browser state in the session
> **Lecture:** [01 — Flask Hello World](../lecture-notes/01-flask-hello-world.md) · [03 — Forms, Sessions, and Deployment](../lecture-notes/03-forms-sessions-deployment.md)
> **Difficulty:** Intermediate
> **Target time:** 2–4 hours
> **Why this one:** a shortener is the smallest app whose URL *is* the product, which makes it the best drill for the routing questions real apps hit — what happens when a dynamic `/<slug>` rule lives at the root, why a slug must come from a cryptographic RNG, and why "show the user their result after a redirect" needs the session. It is also your first app where validating input is a security boundary, not a politeness: reject `javascript:alert(1)` or you are minting links that run script in your visitors' browsers.

## The Brief

Build a tiny URL shortener: the user submits a long URL, your app gives back
a short slug, and visiting the slug 302-redirects to the long URL. Like
`bit.ly`, but in one Python file.

In-memory storage (a `dict[str, str]` mapping slug to long URL) is fine.
Restarts wipe data.

There is one requirement that looks cosmetic and is not: after a successful
shorten, the index has to *show the resulting short link*. A flash is text —
you cannot click text. Getting a clickable link to survive the redirect,
per-browser, without showing it to anyone else, is the part of this challenge
that teaches you what the session is actually for.

## Starter

Suggested file layout:

```text
url-shortener/
├── app.py
└── templates/
    ├── base.html
    └── index.html
```

Save this as `app.py` and build from it. The slug generator and the URL
validator are given whole, because both have a wrong version that looks
right — the reasons are in the Constraints.

```python
"""Tiny in-memory URL shortener."""
import secrets
import string
from urllib.parse import urlparse

from flask import (
    Flask, abort, flash, redirect, render_template, request, url_for,
)

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

ALPHABET = string.ascii_letters + string.digits   # 62 characters
LINKS: dict[str, str] = {}                        # slug -> long_url


def new_slug(length: int = 6) -> str:
    """Generate a fresh slug not already in LINKS."""
    while True:
        s = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if s not in LINKS:
            return s


def looks_like_url(s: str) -> bool:
    """True for http(s) URLs with a host, under 2000 characters."""
    if not s or len(s) > 2000:
        return False
    parts = urlparse(s)
    return parts.scheme in {"http", "https"} and bool(parts.netloc)


@app.route("/")
def index() -> str:
    # TODO: show the form — and, if the visitor just shortened a URL,
    # their short link. Where does that link live between the redirect
    # and this render? (Hint: not in a global. See the Constraints.)
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form.get("url", "").strip()
    if not looks_like_url(long_url):
        flash("Please enter a valid http:// or https:// URL.", "error")
        return redirect(url_for("index"))

    slug = new_slug()
    LINKS[slug] = long_url
    short = url_for("follow", slug=slug, _external=True)
    # TODO: stash `short` somewhere index() can show it as a clickable link
    flash(f"Short URL: {short}", "success")
    return redirect(url_for("index"))


@app.route("/<slug>")
def follow(slug: str):
    long_url = LINKS.get(slug)
    if long_url is None:
        abort(404)
    return redirect(long_url)


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

You write the templates: `base.html` with the flash widget, and `index.html`
with the form plus the freshly minted link when there is one.

## Requirements

Your app must:

1. `GET /` — show a form with a single text input for a URL and a submit
   button. If the user just shortened a URL, also show the resulting short
   link, clickable, once — a refresh must not repeat it.
2. `POST /shorten` — read the URL from the form, validate it, generate a
   short slug (6 random base62 characters), store the mapping, and redirect
   back to `/` with a flash showing the short URL.
3. `GET /<slug>` — look up the slug. If found, **redirect (302)** to the
   long URL. If not found, return **404**.
4. Reject empty submissions and anything that is not an `http://` or
   `https://` URL — including `javascript:` and `ftp://` schemes.
5. Refreshing after a successful shorten must not create a second entry.

## Constraints

- **`secrets.choice`, not `random.choice`.** `random` is a Mersenne Twister
  seeded from the clock; observe a few hundred outputs and its internal state
  — and every future slug — can be reconstructed. `secrets` draws from the
  operating system's cryptographic RNG. For a shortener the slug *is* the
  access control: anyone who guesses it reads the target. This is not
  paranoia, it is the entire security model.
- **Validate the scheme, not just "is it non-empty".** `looks_like_url`
  rejects `javascript:alert(1)` because the scheme is not in
  `{"http", "https"}`. Skip that check and your app happily mints a short
  link that, when clicked, runs script in the visitor's browser. It also
  rejects `example.com` (no scheme) and `https://` (no host), and caps the
  length at 2000 characters — roughly where browsers and proxies start
  truncating, and because unbounded input into a dict key is how you get a
  memory bug.
- **The "your short link" state goes in the session, nowhere else.** A
  module-level `LAST_SHORT` global shows every visitor the last link *anyone*
  shortened — a privacy bug and a race. A view-function local dies with the
  request. The URL (`/?short=abc`) puts the link in history and logs forever.
  `session["last_short"]`, read back with `pop`, is per-browser, survives the
  redirect, and is consumed exactly once.
- **`POST /shorten` ends in a redirect.** Return `render_template` from it
  instead and every refresh mints a fresh slug for the same URL. Requirement
  5 exists to catch exactly this.
- **Do not route the follow rule as `/s/<slug>` "to be safe" without knowing
  what you are avoiding.** The bare `/<slug>` at the root works — Werkzeug
  ranks the literal `/shorten` above the dynamic rule regardless of source
  order — but it has one subtle consequence, spelled out in Under the hood.
  Meet it, then decide.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0. The slugs are minted by `secrets`, so they differ on every run; the
printout therefore reports facts about the slug rather than the slug itself:

```text
$ python challenge-02-url-shortener.py
GET  /        -> 200 (the form)

POST /shorten url='https://example.com' -> 302  Location: /
  links stored          : 1
  slug length           : 6
  slug is base62        : True
  it maps to the URL    : True
  the flash shows it    : True
  the link is clickable : True
  a refresh repeats it  : False
  ...or mints a new one : False

GET  /<that slug> -> 302  Location: https://example.com
GET  /nope404     -> 404

Garbage in, flash out, nothing stored:
  rejected ''                           -> True
  rejected '   '                        -> True
  rejected 'not-a-url'                  -> True
  rejected 'javascript:alert(1)'        -> True
  rejected 'ftp://example.com'          -> True
  rejected 'https://xxxxxxxxxxxxxxxx'   -> True

Routing edges:
  GET  /shorten -> 404 (matched /<slug>, found no such slug)
  POST /        -> 405

200 more shortens -> 201 links, zero collisions
```

**The shipped file starts no server** — it walks the acceptance checklist
with `app.test_client()` and exits. In your own browser build, the moment
worth seeing by hand is the redirect itself:

```console
$ curl -i http://127.0.0.1:5000/<your-slug>
HTTP/1.1 302 FOUND
Server: Werkzeug/3.1.6 Python/3.13.2
Content-Type: text/html; charset=utf-8
Location: https://example.com
```

The `Location:` header is the entire feature. Everything else is packaging.

## Steps

1. Create the folder, paste the starter into `app.py`, and write `base.html`
   (layout plus flash widget) and `index.html` (the form). Shorten a URL and
   watch the flash appear with the short link as text.
2. Fill in the first `TODO`: in `shorten`, put the short URL in
   `session["last_short"]`. In `index`, pass
   `session.pop("last_short", None)` into the template, and render it as an
   `<a>` when it is not `None`. Confirm the link shows once and a refresh
   clears it.
3. Follow your own slug in the browser. Watch the terminal log the `302` on
   your app and then a request to the target site.
4. Test the failure paths: `/nope404`, an empty submission, `not-a-url`,
   `javascript:alert(1)`, `ftp://example.com`. Every one is a flash or a
   404 — no traceback, nothing stored. Count `LINKS` before and after to be
   sure.
5. Type `localhost:5000/shorten` straight into the address bar and read the
   404. Then explain it: the path matched `/<slug>` with `slug="shorten"`
   after the literal rule refused the method — Under the hood has the full
   story. Do not "fix" it by adding `GET` to the route.
6. Refresh after a successful shorten and confirm `LINKS` did not grow.

## The Solution

```python
"""challenge-02-url-shortener-solution.py — the URL shortener, proven headless.

The app is the challenge skeleton plus one change: `shorten` also stashes the
short link in the session so `index` can show it as a clickable `<a>`, not
just flash it as text. The two templates are the part you had to write, and
they are here in full — the stylesheet lives in a `<style>` block in
`base.html`, because a two-page app does not need a `static/` folder yet.

Your own build ends in ``app.run(debug=True)`` and you follow slugs in a
browser. This download drives the app with ``app.test_client()`` — Flask's
in-process fake browser — walks the acceptance checklist, prints each round
trip, and exits. The slugs are minted by ``secrets``, so they differ on every
run; the printout therefore reports facts about the slug (length, alphabet)
rather than the slug itself.

Run it with::

    python challenge-02-url-shortener-solution.py
"""

import secrets
import string
from urllib.parse import urlparse

from flask import (
    Flask, abort, flash, redirect, render_template, request, session, url_for,
)
from jinja2 import DictLoader

#: templates/base.html — layout, flash widget, and the whole stylesheet.
BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Crunch Links{% endblock %}</title>
    <style>
      * { box-sizing: border-box; }
      body {
        font-family: system-ui, -apple-system, sans-serif;
        max-width: 40rem; margin: 2rem auto; padding: 0 1rem;
        color: #222; background: #fafafa; line-height: 1.6;
      }
      header h1 a { color: #222; text-decoration: none; }
      form.shorten { display: flex; flex-wrap: wrap; gap: 0.5rem; }
      form.shorten label { flex: 0 0 100%; font-weight: 600; }
      input[type="url"] { flex: 1 1 16rem; padding: 0.5rem; font: inherit; }
      button { padding: 0.4rem 0.75rem; font: inherit; cursor: pointer;
               border: 1px solid #ccc; border-radius: 0.25rem; background: #fff; }
      ul.flashes { list-style: none; padding: 0; }
      .flash { padding: 0.5rem 0.75rem; border-radius: 0.25rem; margin: 0.25rem 0;
               word-break: break-all; }
      .flash-success { background: #d4edda; color: #155724; }
      .flash-error { background: #f8d7da; color: #721c24; }
      .short { font-size: 1.1rem; word-break: break-all; }
      footer { margin-top: 3rem; color: #666; font-size: 0.875rem; }
    </style>
  </head>
  <body>
    <header>
      <h1><a href="{{ url_for('index') }}">Crunch Links</a></h1>
    </header>

    <main>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <ul class="flashes">
            {% for category, message in messages %}
              <li class="flash flash-{{ category }}">{{ message }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}

      {% block content %}{% endblock %}
    </main>

    <footer>
      <small>In memory only. A restart forgets every link.</small>
    </footer>
  </body>
</html>
"""

#: templates/index.html — the form, plus the freshly minted link when there is one.
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block title %}Shorten a URL — Crunch Links{% endblock %}

{% block content %}
  <form class="shorten" method="post" action="{{ url_for('shorten') }}">
    <label for="url">Long URL</label>
    <input type="url" id="url" name="url" maxlength="2000"
           placeholder="https://example.com/a/very/long/path" required autofocus>
    <button type="submit">Shorten</button>
  </form>

  {% if last_short %}
    <p class="short">
      Your short link: <a href="{{ last_short }}">{{ last_short }}</a>
    </p>
  {% endif %}
{% endblock %}
"""

app = Flask(__name__)
app.jinja_loader = DictLoader({"base.html": BASE_HTML, "index.html": INDEX_HTML})
app.secret_key = "dev-only-change-me"

ALPHABET = string.ascii_letters + string.digits
LINKS: dict[str, str] = {}


def new_slug(length: int = 6) -> str:
    """Generate a slug that is not already taken."""
    while True:
        s = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if s not in LINKS:
            return s


def looks_like_url(s: str) -> bool:
    """True for http(s) URLs with a host, under 2000 characters."""
    if not s or len(s) > 2000:
        return False
    parts = urlparse(s)
    return parts.scheme in {"http", "https"} and bool(parts.netloc)


@app.route("/")
def index() -> str:
    # pop, not get: the link is shown once, like a flash. It lives in the
    # session so it is per-browser -- a module-level global would show your
    # link to every other visitor.
    return render_template("index.html", last_short=session.pop("last_short", None))


@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form.get("url", "").strip()
    if not looks_like_url(long_url):
        flash("Please enter a valid http:// or https:// URL.", "error")
        return redirect(url_for("index"))

    slug = new_slug()
    LINKS[slug] = long_url
    short = url_for("follow", slug=slug, _external=True)
    session["last_short"] = short
    flash(f"Short URL: {short}", "success")
    return redirect(url_for("index"))


@app.route("/<slug>")
def follow(slug: str):
    long_url = LINKS.get(slug)
    if long_url is None:
        abort(404)
    return redirect(long_url)


def main() -> None:
    """Walk the acceptance checklist and print what each round trip proved."""
    client = app.test_client()

    response = client.get("/")
    print(f"GET  /        -> {response.status_code} (the form)")

    print()
    response = client.post("/shorten", data={"url": "https://example.com"})
    print(f"POST /shorten url='https://example.com' -> {response.status_code}  Location: {response.headers['Location']}")
    slug, target = next(iter(LINKS.items()))
    body = client.get("/").get_data(as_text=True)
    print(f"  links stored          : {len(LINKS)}")
    print(f"  slug length           : {len(slug)}")
    print(f"  slug is base62        : {all(c in ALPHABET for c in slug)}")
    print(f"  it maps to the URL    : {target == 'https://example.com'}")
    print(f"  the flash shows it    : {f'Short URL: http://localhost/{slug}' in body}")
    print(f"  the link is clickable : {f'href=\"http://localhost/{slug}\"' in body}")
    print(f"  a refresh repeats it  : {f'/{slug}' in client.get('/').get_data(as_text=True)}")
    print(f"  ...or mints a new one : {len(LINKS) != 1}")

    print()
    response = client.get(f"/{slug}")
    print(f"GET  /<that slug> -> {response.status_code}  Location: {response.headers['Location']}")
    print(f"GET  /nope404     -> {client.get('/nope404').status_code}")

    print()
    print("Garbage in, flash out, nothing stored:")
    for bad in ("", "   ", "not-a-url", "javascript:alert(1)", "ftp://example.com",
                "https://" + "x" * 2000):
        before = len(LINKS)
        response = client.post("/shorten", data={"url": bad}, follow_redirects=True)
        rejected = ("Please enter a valid" in response.get_data(as_text=True)
                    and len(LINKS) == before)
        print(f"  rejected {bad[:24]!r:28} -> {rejected}")

    print()
    print("Routing edges:")
    print(f"  GET  /shorten -> {client.get('/shorten').status_code} (matched /<slug>, found no such slug)")
    print(f"  POST /        -> {client.post('/').status_code}")

    print()
    for _ in range(200):
        client.post("/shorten", data={"url": "https://example.org/x"})
    print(f"200 more shortens -> {len(LINKS)} links, zero collisions")


if __name__ == "__main__":
    main()
```

**The one change to the skeleton, and why it earns its keep.** The skeleton
flashes the short URL as text. Requirement 1 asks the index to *show the
resulting short link*, and a flash is a string — you cannot click a string.
So `shorten` also stashes it in the session and `index` pops it out into a
real `<a>`. The interesting part is *where* it is stored. Four options, one
right answer:

| Where | What happens |
|---|---|
| A module-level `LAST_SHORT` | Every visitor sees the last link *anyone* shortened. A privacy bug and a race. |
| A local in `shorten` | Gone when the function returns, and the redirect starts a whole new request. |
| The URL, `/?short=abc123` | Works, but the link is now in history and in logs, and a refresh re-shows it forever. |
| `session["last_short"]` | Per-browser, survives the redirect, and `pop` consumes it exactly once. |

`session.pop(...)` rather than `session.get(...)` is what makes it behave
like a flash: show once, then forget. That is also why refreshing `/` does
not re-show it — a fact the shipped run asserts.

**`secrets.choice`, not `random.choice`.** The slug is the access control,
so it comes from the OS's cryptographic RNG. 62⁶ is about 5.7 × 10¹⁰
possible slugs; the shipped run mints 201 without a collision, and
`new_slug` loops until it finds a free one anyway.

**`urlparse` is doing more than it looks.** `looks_like_url` rejects
`javascript:alert(1)` because the scheme is not in `{"http", "https"}` —
without that check, your app would hand out a short link that runs script in
the visitor's browser when clicked. It rejects `ftp://example.com` on the
same rule, `example.com` for having no scheme, and `https://` for having no
host.

**`redirect(long_url)` is a 302, deliberately.** A 302 is "temporary" — the
browser asks you again next time, so a hit counter keeps counting and you can
change the target later. A 301 would be cached by the browser possibly
forever, and you would never see the request again. Real shorteners use 302
for exactly this reason.

**Route matching is by specificity, not by source order.** The literal
`/shorten` outranks the dynamic `/<slug>` regardless of the order you wrote
them — move `follow` above `shorten` in the file and nothing changes. The
subtle consequence of a root-level catch-all, and why `GET /shorten` is a
404 rather than a 405, is in Under the hood.

## Run it

Copy the worked answer on this page into `challenge-02-url-shortener.py` and run it:

```bash
python challenge-02-url-shortener.py
```

It needs Flask installed and nothing else, and it exits on its own — the two
templates travel inside the file, and the stylesheet rides in `base.html`'s
`<style>` block. To follow slugs in a real browser, build the folder version;
the Python is identical.

The `-solution` in the filename keeps this file from colliding with your own
`app.py`.

## Common bugs to catch

- **Every refresh mints a new slug for the same URL.** `shorten` returns
  `render_template(...)` instead of `redirect(url_for("index"))`. The page
  the user is looking at was produced by a `POST`, so refresh re-posts.
  Requirement 5 — and the shipped run's `...or mints a new one : False` —
  exist to catch this.

- **A private window shows someone else's "your short link".** You stored
  the last link in a module-level global. Module state is shared by every
  visitor at once; only the session cookie is per-browser. This is the
  single most common Week 9 confusion, and the table in The Solution is the
  cure.

- **The short link prints as `/abc123` instead of a full URL.**
  `url_for("follow", slug=s)` returns a path by default. `_external=True` is
  what produces `http://localhost/abc123` — a link you can paste into a
  chat. (Behind a proxy in production the host also has to be right; that is
  what `ProxyFix` and `SERVER_NAME` are for, and neither is needed here.)

- **`GET /shorten` gives a 404 and you "fix" it with
  `methods=["GET", "POST"]`.** The 404 was correct — you typed a URL into
  the address bar, which is a `GET`, and `/shorten` accepts `POST` only.
  Adding `GET` creates a state-changing `GET` route. Submit the form
  instead, and read Under the hood for why it was a 404 and not a 405.

- **`RuntimeError: The session is unavailable because no secret key was
  set.`** The first `flash()` or `session[...]` write raises this if
  `app.secret_key` is missing. Flash and session are the same mechanism: a
  signed cookie, and signing needs a key.

- **A test searching the page for `'my-link' is already taken.` never
  matches.** Jinja escaped the apostrophes: the HTML contains
  `&#39;my-link&#39; is already taken.` Nothing is broken — the browser
  renders `'` for `&#39;` — but raw-HTML string matching has to search for
  the escaped form. You will meet this again the moment you write tests in
  Week 11.

## Under the hood

<details>
<summary>Under the hood — what a root-level /&lt;slug&gt; rule quietly absorbs</summary>

Ask Flask for its route table:

```text
$ flask --app app routes
Endpoint  Methods  Rule
--------  -------  -----------------------
follow    GET      /<slug>
index     GET      /
shorten   POST     /shorten
static    GET      /static/<path:filename>
```

Werkzeug sorts rules by how constrained they are, so the literal `/shorten`
outranks the dynamic `/<slug>` no matter which you wrote first. So far, so
reassuring.

Now the subtle part, which the shipped run pins: **`GET /shorten` returns
404, not 405.** Walk it through. Werkzeug tries `/shorten` — the path
matches, the method does not. Normally that ends as a `405 Method Not
Allowed`. But the router keeps looking, and `/<slug>` matches the path *and*
the method, with `slug="shorten"`. So `follow` runs, finds no such slug in
`LINKS`, and aborts 404.

A catch-all dynamic rule at the root quietly absorbs the method mismatches
of every literal route beside it. That is the price of `/<slug>` at the top
level, and it is worth knowing you are paying it:

- It is why the "helpful" fix of adding `GET` to `/shorten` changes more
  than it looks like it changes.
- It is why a real build with more pages keeps a `RESERVED` set of slugs
  (`{"shorten", "stats", "static"}`): if a user claims the slug `stats`,
  the literal `/stats` rule will always win, and their link is permanently
  dead. Refuse it at creation rather than shipping a link that silently
  does the wrong thing.
- The alternative design — prefixing the follow route as `/s/<slug>` —
  makes every short link two characters longer and removes the whole class
  of problem. Real shorteners pay the two characters more often than not.

One more routing fact from the table: `POST /` is a 405, because `/` is
`GET`-only and nothing else matches the bare path. The 404/405 pair in the
shipped run is the two failure modes side by side: 404 means "no rule and no
resource"; 405 means "rule found, wrong verb".

</details>

## Acceptance checklist

- [ ] Submitting `https://example.com` produces a 6-character slug.
- [ ] Visiting the slug redirects (302) to `https://example.com`.
- [ ] The index shows the short link as a clickable `<a>` once; a refresh
      does not repeat it.
- [ ] Submitting `not-a-url`, `javascript:alert(1)`, or `ftp://example.com`
      flashes an error and does not create a slug.
- [ ] Visiting `/nope404` (a non-existent slug) returns 404.
- [ ] Refreshing after a successful shorten does not duplicate the entry.
- [ ] You can say why `GET /shorten` is a 404 and `POST /` is a 405.

## Stretch

- **Custom slugs**: add an optional `slug` field to the form. Validate it
  against a regex like `^[A-Za-z0-9_-]{1,32}$`, reject slugs that already
  exist — and reject a `RESERVED` set (`shorten`, `stats`, `static`), for
  the reason Under the hood explains.
- **Hit counter**: track how many times each slug has been followed; show
  the counts on a `/stats` page. The 302 (not 301) is what keeps the counter
  honest.
- **Persistence**: save `LINKS` to a JSON file on each shorten and load it
  on startup. Restarts no longer lose data.
- **Expiry**: add an "expires in N minutes" option; after that, the slug
  404s. Reap on read — check the deadline inside `follow` and delete there —
  rather than running a background timer. Use
  `datetime.now() + timedelta(minutes=n)`.
- Render the short URL as a copy-to-clipboard button with one line of
  JavaScript that reads the DOM:
  `navigator.clipboard.writeText(document.getElementById('short-link').href)`.
  Never interpolate a template variable into inline JS — Jinja's HTML
  escaping does not protect you inside a script string.

References:

- `secrets` module — <https://docs.python.org/3/library/secrets.html>
- `urllib.parse` — <https://docs.python.org/3/library/urllib.parse.html>
- `flask.redirect` — <https://flask.palletsprojects.com/en/stable/api/#flask.redirect>
- HTTP redirect status codes — <https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections>
