"""
Exercise 04 — Form echo with flash messages
===========================================

Goal
----
Build a single page with one text field. When the user submits the form,
flash their name back to them on the same page.

Layout
------
    exercise-04-form-echo/
    ├── app.py                  <- this file
    └── templates/
        └── form.html

Run it
------
    cd exercise-04-form-echo
    python app.py

Then visit:
    http://127.0.0.1:5000/

Type a name, submit, and see it flashed back. Submit an empty field and
see the validation error.

What to notice
--------------
* The same route handles GET (showing the form) and POST (handling the
  submission), branching on `request.method`.
* `request.form.get("name", "").strip()` reads the field value safely and
  trims whitespace.
* We use the Post / Redirect / Get (PRG) pattern: after a successful POST
  we `redirect(...)` rather than returning a page. Refreshing then is a
  harmless GET, not a re-submit.
* `flash(msg, category=...)` queues a message for the next page. The
  template reads it with `get_flashed_messages(with_categories=true)`.
* `app.secret_key` is required because `flash` (and `session`) use a
  signed cookie. In production, load this from an environment variable.

Stretch
-------
* Add a second field for "age" that must parse as a positive integer.
  Flash an error if it does not.
* Replace the redirect with a render_template that re-displays the form
  pre-filled with what the user typed (helpful when validation fails).
* Read about Flask-WTF and rewrite the form using a `FlaskForm` class.

References
----------
* `request.form`: https://flask.palletsprojects.com/en/stable/api/#flask.Request.form
* Flashing messages: https://flask.palletsprojects.com/en/stable/patterns/flashing/
"""
from flask import (
    Flask, flash, get_flashed_messages, redirect, render_template, request,
    url_for,
)

app: Flask = Flask(__name__)
# Required for flash() and session — in a real app, load from an env var.
app.secret_key = "dev-only-secret-do-not-use-in-production"


@app.route("/", methods=["GET", "POST"])
def form():
    """Show the form on GET; handle submission on POST."""
    if request.method == "POST":
        name: str = request.form.get("name", "").strip()

        if not name:
            flash("Name is required.", category="error")
        elif len(name) > 50:
            flash("Name must be 50 characters or fewer.", category="error")
        else:
            flash(f"Hello, {name}!", category="success")

        # Post / Redirect / Get — refresh-safe.
        return redirect(url_for("form"))

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
