"""
Exercise 02 — Multiple routes and URL parameters
================================================

Goal
----
Define three routes on one Flask app:

* GET /            -> a tiny home page with HTML links
* GET /about       -> a short "about" page
* GET /greet/<name>  -> personalized greeting for any name

Run it
------
    python exercise-02-multiple-routes.py

Then try:
    http://127.0.0.1:5000/
    http://127.0.0.1:5000/about
    http://127.0.0.1:5000/greet/Ada
    http://127.0.0.1:5000/greet/Grace

What to notice
--------------
* Every route decorator wraps a different view function. The function name
  is the "endpoint" used by `url_for`.
* `<name>` in the URL pattern becomes a keyword argument to the view
  function. Without a converter prefix it defaults to type `str`.
* We use `url_for("greet", name="World")` in the home page rather than
  hard-coding `/greet/World`. If you ever rename the route, the link
  updates automatically.

Stretch
-------
* Add a route `/square/<int:n>` that returns the square of an integer.
  Visit `/square/12` and `/square/abc` to see how the `<int:>` converter
  refuses non-integers with a 404 BEFORE your function runs.
* Add `/random` that returns a different random integer from 1 to 100
  every refresh (hint: `import random`).
* Add a query-string greeting: `/hello?name=Ada` that reads
  `request.args.get("name", "stranger")`.

References
----------
* URL converters: https://flask.palletsprojects.com/en/stable/quickstart/#variable-rules
* `url_for`: https://flask.palletsprojects.com/en/stable/api/#flask.url_for
"""
from flask import Flask, url_for

app: Flask = Flask(__name__)


@app.route("/")
def index() -> str:
    """A tiny home page that links to the other two routes."""
    return (
        "<h1>Exercise 02 — Multiple routes</h1>"
        "<ul>"
        f'<li><a href="{url_for("about")}">About</a></li>'
        f'<li><a href="{url_for("greet", name="World")}">Greet World</a></li>'
        f'<li><a href="{url_for("greet", name="Ada")}">Greet Ada</a></li>'
        "</ul>"
    )


@app.route("/about")
def about() -> str:
    """Static-ish about page."""
    return (
        "<h1>About</h1>"
        "<p>This is Exercise 02 of Week 9 of Code Crunch Convos.</p>"
        f'<p><a href="{url_for("index")}">&larr; Home</a></p>'
    )


@app.route("/greet/<name>")
def greet(name: str) -> str:
    """Greet whatever name was given in the URL path."""
    # `name` came from the URL; treat it as untrusted text. Jinja escaping
    # would handle this in a real template — here we keep it simple but
    # cap the length so a 1MB URL does not crash us.
    safe_name: str = name[:50]
    return (
        f"<h1>Hello, {safe_name}!</h1>"
        f'<p><a href="{url_for("index")}">&larr; Home</a></p>'
    )


if __name__ == "__main__":
    app.run(debug=True)
