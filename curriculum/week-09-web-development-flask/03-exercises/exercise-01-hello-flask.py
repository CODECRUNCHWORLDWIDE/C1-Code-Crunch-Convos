"""
Exercise 01 — Hello, Flask
==========================

Goal
----
Write the smallest Flask app that can run: one route, one view function,
returning a plain-text greeting.

Run it
------
    python exercise-01-hello-flask.py

Then visit:
    http://127.0.0.1:5000/

You should see "Hello, World!" in your browser. Stop the server with Ctrl-C.

What to notice
--------------
* `Flask(__name__)` creates the application object. The `__name__` argument
  tells Flask where to find templates and static files (relative to this
  module).
* `@app.route("/")` registers the function below it as the handler for the
  URL path `/`.
* The function's return value becomes the response body. A bare string is
  served as `text/html` with status `200 OK`.
* `app.run(debug=True)` starts Flask's built-in development server with
  hot-reload and the in-browser interactive debugger. NEVER use
  `debug=True` in production.

Stretch
-------
* Change the message and watch the server auto-reload.
* Add a second route at `/health` that returns the dict {"status": "ok"} —
  Flask will automatically serialize it as JSON.
* Print `app.url_map` at the bottom of the file (after `app.run(...)` is
  unreachable, so put it before) to see every route Flask knows about.

References
----------
* Flask quickstart: https://flask.palletsprojects.com/en/stable/quickstart/
"""
from flask import Flask

app: Flask = Flask(__name__)


@app.route("/")
def hello() -> str:
    """Return a friendly greeting at the root URL."""
    return "Hello, World!"


if __name__ == "__main__":
    # Debug mode reloads on file changes and shows tracebacks in the browser.
    app.run(debug=True)
