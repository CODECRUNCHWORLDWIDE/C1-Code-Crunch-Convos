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
