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
