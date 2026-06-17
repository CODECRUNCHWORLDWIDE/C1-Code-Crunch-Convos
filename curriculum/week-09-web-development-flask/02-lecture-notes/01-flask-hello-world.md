# Lecture 1 — Flask Hello World

> **Goal:** by the end of this lecture you can install Flask, write a working
> web app in 10 lines of Python, define multiple routes, capture pieces of the
> URL with converters, and know what is actually happening when a browser hits
> your machine.

---

## 1. The 60-second model of the web

Every web page you have ever opened works the same way:

1. Your **browser** (the *client*) opens a TCP connection to a **server**.
2. The browser sends an HTTP **request** that looks roughly like
   `GET /about HTTP/1.1`.
3. The server sends back an HTTP **response** with a *status code* (e.g.
   `200 OK`, `404 Not Found`), some *headers*, and a *body* (usually HTML).
4. The browser parses the HTML, fetches any extra resources it mentions (CSS
   files, images, JavaScript), and paints pixels.

That is it. There is no magic, just a strict text protocol over a socket. In
Week 8 you played the role of the *client* with the `requests` library. This
week you play the role of the **server**.

The three "languages of the web" each have one job:

- **HTML** is the **structure**: headings, paragraphs, links, forms.
- **CSS** is the **style**: colors, fonts, layout, spacing.
- **JavaScript** is the **behavior**: code that runs *in the browser* after
  the page loads (clicks, animations, fetch calls).

You will write a lot of HTML this week, a little CSS, and zero JavaScript.
Pure server-rendered apps in Flask are a great way to learn — and they are
still a perfectly modern way to ship real software.

---

## 2. What is a web framework? And what is WSGI?

Writing a web server from scratch in Python is possible (`http.server` does it
in the standard library) but tedious. You would have to:

- Parse raw HTTP request text into something usable.
- Look at the URL and dispatch to the right function.
- Format the response correctly with status code, headers, and body.
- Handle errors, sessions, security headers, file uploads, redirects, and a
  long tail of edge cases.

A **web framework** does the boring parts for you. **Flask** is a *micro*
framework: it gives you routing, templating, request/response objects, and a
development server. It deliberately does **not** ship an ORM, an admin panel,
or a user system. You add those when (and only when) you need them.

Flask talks to web servers through a Python standard interface called
**WSGI** (Web Server Gateway Interface, PEP 3333). All you need to know right
now:

- WSGI is a Python convention for "what a web application looks like as a
  callable."
- A WSGI **server** (the Flask dev server, or `gunicorn` in production)
  receives raw HTTP, turns it into a Python dict + a `start_response`
  callable, and calls your WSGI **application** (your Flask `app`).
- Flask wraps all of that so you never see WSGI directly. You just write view
  functions.

If you ever read "Flask is a WSGI framework," that is what the sentence means.

---

## 3. Installing Flask

Make a fresh virtual environment for this week:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install flask
```

Sanity check:

```bash
python -c "import flask; print(flask.__version__)"
```

You should see `3.x.x` (or `2.x.x` — anything from 2.0 onward is fine for
this week).

---

## 4. Hello, Flask

Create a file called `app.py`:

```python
"""Smallest possible Flask app."""
from flask import Flask

app: Flask = Flask(__name__)


@app.route("/")
def hello() -> str:
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
```

Run it:

```bash
python app.py
```

You will see something like:

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open <http://127.0.0.1:5000> in a browser and you should see *Hello, Flask!*.

Congratulations — you are now running a real web server. Two notes about that
output:

- **`127.0.0.1`** (also written `localhost`) is the loopback address. It only
  accepts connections from your own machine. That is exactly what you want
  during development.
- **`Debug mode: on`** means three things:
  1. Code changes auto-reload the server.
  2. Errors show a full interactive traceback in the browser.
  3. The interactive debugger lets anyone with the URL run Python on your
     machine, so **never run with `debug=True` in production**.

### `flask run` vs `python app.py`

Flask ships a CLI:

```bash
export FLASK_APP=app.py            # Windows (PowerShell): $env:FLASK_APP="app.py"
flask run --debug
```

Either approach is fine. `python app.py` is more obvious for beginners; `flask
run` is what you will use in deployment manuals. We will use both
interchangeably.

---

## 5. Routes and view functions

A **route** is a URL pattern. A **view function** is the Python function that
handles requests to that URL. You connect them with the `@app.route`
decorator:

```python
@app.route("/")
def index() -> str:
    return "Home page"


@app.route("/about")
def about() -> str:
    return "About page"


@app.route("/contact")
def contact() -> str:
    return "Reach me at hello@example.com"
```

The function name (`index`, `about`, `contact`) is not magic to Flask — but
you will refer to it later by name in `url_for`, so pick descriptive names.

A view function's return value becomes the response body. Flask is helpful:

- Returning a **string** sends an HTTP 200 with `Content-Type: text/html`.
- Returning a **tuple** `(body, status)` lets you set the status code:

```python
@app.route("/teapot")
def teapot() -> tuple[str, int]:
    return "I am a teapot", 418
```

- Returning a **dict** sends JSON automatically:

```python
@app.route("/api/ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}
```

That last one is genuinely useful. You already know how to build JSON APIs;
you just learned the server side in two lines.

---

## 6. The route table and HTTP methods

By default a route accepts only **`GET`** requests. To accept `POST` (or
others) you pass `methods=[...]`:

```python
@app.route("/submit", methods=["GET", "POST"])
def submit() -> str:
    return "this route handles GET and POST"
```

You will use this in lecture 3 for forms. For now, remember:

- `GET` is for *reading*. It should never change server state.
- `POST` is for *creating* or *changing* state.
- `PUT`, `PATCH`, `DELETE` exist and you can use them via `methods=` too, but
  HTML forms can only emit `GET` and `POST` natively.

You can inspect the full route table with `flask routes`:

```bash
flask routes
```

This is gold when an app gets bigger and you forget what is defined.

---

## 7. Dynamic URL parameters

Hard-coded routes are nice but limited. To match `/post/1`, `/post/2`,
`/post/42`, you use a **converter**:

```python
@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    return f"You requested post #{post_id}"
```

Visit <http://127.0.0.1:5000/post/7> and you see *You requested post #7*.
Visit <http://127.0.0.1:5000/post/seven> and Flask returns a `404 Not Found`
*before your function ever runs* — because `"seven"` does not match `int`.
That is the converter doing real work for you.

Built-in converters:

| Converter        | Matches                              | Example          |
|------------------|--------------------------------------|------------------|
| `string` (default) | Any text without a slash           | `/user/<name>`   |
| `int`            | Positive integers                    | `/post/<int:id>` |
| `float`          | Floating-point numbers               | `/temp/<float:c>`|
| `path`           | Like string, but allows slashes      | `/file/<path:p>` |
| `uuid`           | A UUID string                        | `/job/<uuid:j>`  |

You can combine multiple parameters in one URL:

```python
@app.route("/user/<username>/post/<int:post_id>")
def user_post(username: str, post_id: int) -> str:
    return f"Showing post #{post_id} by {username}"
```

Type hints in the function signature are **for you**, not for Flask. Flask
already converts the path segment based on the converter. The hints are there
so that your editor, your future self, and tools like `mypy` know what
`post_id` is.

---

## 8. Query strings

A query string is the part of a URL after the `?`:
`/search?q=flask&page=2`. It is *not* part of the route pattern; you read it
from the `request` object:

```python
from flask import Flask, request

app = Flask(__name__)


@app.route("/search")
def search() -> str:
    query: str = request.args.get("q", default="", type=str)
    page: int = request.args.get("page", default=1, type=int)
    return f"Searching for {query!r} on page {page}"
```

A few things to notice:

- `request.args` is a `MultiDict` — like a `dict`, but each key can hold
  multiple values. `request.args.get("q")` gives you the first value, or
  `None` if the key is missing.
- `default=` is your friend. Use it instead of `if "q" in request.args`.
- `type=int` does the conversion for you and silently returns the default if
  parsing fails. This is the safer way to read numeric query params.

Try it: visit <http://127.0.0.1:5000/search?q=flask&page=3>.

---

## 9. Status codes, redirects, and `abort`

Sometimes you need to send something other than 200:

```python
from flask import Flask, abort, redirect, url_for

app = Flask(__name__)

POSTS: dict[int, str] = {1: "Hello", 2: "Second post"}


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    if post_id not in POSTS:
        abort(404)
    return POSTS[post_id]


@app.route("/latest")
def latest():
    # send the browser to /post/2
    return redirect(url_for("show_post", post_id=2))
```

- **`abort(404)`** raises an exception that Flask converts into a 404
  response. You can also pass `400`, `403`, `500`, etc.
- **`redirect(url)`** returns a 302 response with a `Location:` header.
- **`url_for("show_post", post_id=2)`** builds the URL for the view function
  named `show_post`. **Always prefer `url_for` over hard-coding URLs** — if
  you ever rename a route, every `url_for` call updates automatically.

---

## 10. Putting it all together

Here is a slightly bigger example you can run as-is. It models a tiny "posts"
service with three routes:

```python
"""A minimal blog-like service. Save as `app.py` and run `python app.py`."""
from flask import Flask, abort, request, url_for

app: Flask = Flask(__name__)

POSTS: dict[int, dict[str, str]] = {
    1: {"title": "Hello world", "body": "First post!"},
    2: {"title": "Flask is fun", "body": "Routing is half the framework."},
}


@app.route("/")
def index() -> str:
    links = "<br>".join(
        f'<a href="{url_for("show_post", post_id=pid)}">{post["title"]}</a>'
        for pid, post in POSTS.items()
    )
    return f"<h1>Blog</h1>{links}"


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    if post_id not in POSTS:
        abort(404)
    post = POSTS[post_id]
    return f"<h1>{post['title']}</h1><p>{post['body']}</p>"


@app.route("/search")
def search() -> str:
    q: str = request.args.get("q", "").lower()
    if not q:
        return "Try /search?q=flask"
    matches = [p["title"] for p in POSTS.values() if q in p["title"].lower()]
    return f"Found {len(matches)} match(es): {matches}"


if __name__ == "__main__":
    app.run(debug=True)
```

Run it and visit:

- <http://127.0.0.1:5000/> — the index page with links.
- <http://127.0.0.1:5000/post/1> — the first post.
- <http://127.0.0.1:5000/post/99> — a 404.
- <http://127.0.0.1:5000/search?q=flask> — query-string search.

Notice how ugly the HTML is when you build it with string concatenation. That
is exactly the pain that templates solve, which is lecture 2.

---

## 11. Errors, debugging, and the browser console

When debug mode is on, exceptions raised inside a view function are caught by
Flask and rendered as an interactive traceback in your browser. Take 30
seconds now to deliberately break something:

```python
@app.route("/boom")
def boom() -> str:
    return 1 / 0   # ZeroDivisionError
```

Visit `/boom` and look at the page. You can expand each frame and even open a
Python console scoped to that frame. This is the single most useful Flask
feature for beginners.

Browser DevTools (Cmd-Opt-I on macOS, F12 elsewhere) → **Network** tab is the
other one. It shows you the URL, status code, headers, and body of every
request. When something looks broken, open it before you start guessing.

---

## 12. Recap and what is next

You can now:

- Explain client/server, HTTP request/response, and where Flask sits in WSGI.
- Install Flask and run an app with debug mode on.
- Define routes, including dynamic ones with converters.
- Read query strings, return status codes, and redirect.
- Use `url_for` instead of hard-coding URLs.

What you cannot yet do is build pages that look like *pages*. Returning HTML
as a Python f-string works for two lines and rots after twenty. The fix is
**templates**, and that is exactly where lecture 2 picks up.

> **Practice:** finish `exercises/exercise-01-hello-flask.py` and
> `exercises/exercise-02-multiple-routes.py` before reading lecture 2. You
> should be comfortable starting and stopping a Flask app from the terminal
> without thinking about it.

---

## References

- Flask docs — <https://flask.palletsprojects.com/en/stable/>
- Flask Quickstart — <https://flask.palletsprojects.com/en/stable/quickstart/>
- Flask routing reference — <https://flask.palletsprojects.com/en/stable/api/#url-route-registrations>
- PEP 3333 (WSGI) — <https://peps.python.org/pep-3333/>
- MDN HTTP overview — <https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview>
