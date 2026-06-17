# Challenge 02 — Tiny URL Shortener

Build a tiny URL shortener: the user submits a long URL, your app gives back
a short slug, and visiting the slug 302-redirects to the long URL. Like
`bit.ly`, but in one Python file.

---

## Requirements

Your app must:

1. `GET /` — show a form with a single text input for a URL and a submit
   button. If the user just shortened a URL, also show the resulting short
   link.
2. `POST /shorten` — read the URL from the form, validate it, generate a
   short slug (e.g. 6 random base62 characters), store the mapping, and
   redirect back to `/` with a flash showing the short URL.
3. `GET /<slug>` — look up the slug. If found, **redirect (302)** to the
   long URL. If not found, return **404**.
4. Reject empty submissions and URLs that do not look like an HTTP(S) URL.

In-memory storage (a `dict[str, str]`) is fine. Restarts wipe data.

---

## Suggested data shape

```python
import secrets
import string

ALPHABET = string.ascii_letters + string.digits   # 62 chars

LINKS: dict[str, str] = {}     # slug -> long_url


def new_slug(length: int = 6) -> str:
    """Generate a fresh slug not already in LINKS."""
    while True:
        slug = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if slug not in LINKS:
            return slug
```

`secrets.choice` (not `random.choice`) is the right call here — it draws
from the operating system's cryptographic RNG, so slugs are not guessable
by someone watching your traffic.

---

## URL validation (the easy version)

Use `urllib.parse.urlparse`:

```python
from urllib.parse import urlparse

def looks_like_url(s: str) -> bool:
    if len(s) > 2000:
        return False
    parts = urlparse(s)
    return parts.scheme in {"http", "https"} and bool(parts.netloc)
```

This rejects `not-a-url`, `javascript:alert(1)`, `ftp://example.com`, and
the empty string. It accepts `https://example.com/path?q=1`. Good enough
for our purposes.

---

## Suggested file layout

```text
url-shortener/
├── app.py
└── templates/
    ├── base.html
    └── index.html
```

`index.html` shows the form and (optionally) the most recently shortened
link, passed in via `last_short` in `render_template`.

---

## Skeleton (start here, fill in the gaps)

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

ALPHABET = string.ascii_letters + string.digits
LINKS: dict[str, str] = {}


def new_slug(length: int = 6) -> str:
    while True:
        s = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if s not in LINKS:
            return s


def looks_like_url(s: str) -> bool:
    if not s or len(s) > 2000:
        return False
    parts = urlparse(s)
    return parts.scheme in {"http", "https"} and bool(parts.netloc)


@app.route("/")
def index() -> str:
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
    flash(f"Short URL: {short}", "success")
    return redirect(url_for("index"))


@app.route("/<slug>")
def follow(slug: str):
    long_url = LINKS.get(slug)
    if long_url is None:
        abort(404)
    return redirect(long_url)


if __name__ == "__main__":
    app.run(debug=True)
```

You write the templates. The trickiest bit is making sure your `/<slug>`
route does not swallow `/shorten` — Flask matches more specific routes
first, so listing the routes in the order shown above is correct.

---

## Acceptance checklist

- [ ] Submitting `https://example.com` produces a 6-character slug.
- [ ] Visiting the slug redirects (302) to `https://example.com`.
- [ ] Submitting `not-a-url` flashes an error and does not create a slug.
- [ ] Visiting `/nope404` (a non-existent slug) returns 404.
- [ ] Refreshing after a successful shorten does not duplicate the entry.

---

## Stretch goals

- **Custom slugs**: add an optional `slug` field to the form. Reject if the
  slug already exists.
- **Hit counter**: track how many times each slug has been followed; show
  the counts on a `/stats` page.
- **Persistence**: save `LINKS` to a JSON file on each shorten and load it
  on startup. Restarts no longer lose data.
- **Expiry**: add an "expires in N minutes" option; after that, the slug
  404s. Use `datetime.now() + timedelta(minutes=n)`.
- Render the short URL as a copy-to-clipboard button using one line of
  JavaScript.

---

## References

- `secrets` module — <https://docs.python.org/3/library/secrets.html>
- `urllib.parse` — <https://docs.python.org/3/library/urllib.parse.html>
- `flask.redirect` — <https://flask.palletsprojects.com/en/stable/api/#flask.redirect>
- HTTP redirect status codes — <https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections>
