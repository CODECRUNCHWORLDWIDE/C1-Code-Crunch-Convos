"""exercise-03-template-loop-solution.py — the workshop board, proven headless.

The exercise part is the one-line TODO filled in: `index()` hands the
`WORKSHOPS` list to `render_template`. The template is the exact
`templates/list.html` the exercise page gives you.

Two things make this download different from the folder you build yourself,
and both exist so one file runs anywhere:

1. **The template travels inside the file.** Your build keeps `list.html` in
   a `templates/` folder on disk. Here the same text sits in the
   ``LIST_HTML`` constant and is handed to Jinja through a ``DictLoader`` —
   a loader that reads templates out of a dict instead of a folder. Jinja
   neither knows nor cares; the name is still `list.html`, so autoescaping
   stays on exactly as it would from disk.
2. **No server starts.** Your build ends in ``app.run(debug=True)`` and you
   look at the page in a browser. This file drives the app with
   ``app.test_client()``, Flask's in-process fake browser, prints the lines
   the exercise's checklist cares about, and exits.

Run it with::

    python exercise-03-template-loop-solution.py
"""

from dataclasses import dataclass

from flask import Flask, render_template
from jinja2 import DictLoader

#: templates/list.html, byte for byte as the exercise page gives it.
LIST_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Workshops — Code Crunch</title>
  </head>
  <body>
    <h1>Upcoming workshops</h1>
    <p>{{ workshops|length }} workshop(s) on the board.</p>

    <ul>
      {% for workshop in workshops %}
        <li>
          {{ loop.index }}. <strong>{{ workshop.title }}</strong>
          hosted by {{ workshop.host }} &mdash;
          {% if workshop.seats_left > 0 %}
            {{ workshop.seats_left }} seat(s) left
          {% else %}
            <em>full</em>
          {% endif %}
          <p>{{ workshop.notes|truncate(60) }}</p>
        </li>
      {% else %}
        <li><em>Nothing on the board yet.</em></li>
      {% endfor %}
    </ul>
  </body>
</html>
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader({"list.html": LIST_HTML})


@dataclass
class Workshop:
    """One workshop on the study-hall board."""

    id: int
    title: str
    host: str
    seats_left: int
    notes: str


WORKSHOPS: list[Workshop] = [
    Workshop(
        1,
        "Loops and Lists",
        "ada",
        4,
        "Bring a laptop. We rewrite three loops as comprehensions and time them.",
    ),
    Workshop(2, "Sorting, Big-O & <you>", "grace", 0, "Short one."),
    Workshop(
        3,
        "Reading Tracebacks",
        "ada",
        2,
        "Wi-fi is flaky in room B; download the slides first.",
    ),
]


@app.route("/")
def index() -> str:
    """Render the workshop board."""
    return render_template("list.html", workshops=WORKSHOPS)


def line_with(page: str, needle: str) -> str:
    """Return the first line of *page* containing *needle*, stripped."""
    for line in page.splitlines():
        if needle in line:
            return line.strip()
    return f"(no line contains {needle!r})"


def main() -> None:
    """Render the board twice — full and empty — and print the proof lines."""
    client = app.test_client()

    response = client.get("/")
    body = response.get_data(as_text=True)
    print(f"GET / -> {response.status_code}")
    print(f"count line  : {line_with(body, 'workshop(s) on the board')}")
    print(f"escaped     : {line_with(body, 'Big-O')}")
    print(f"raw <you> reached the page: {'<you>' in body}")
    print(f"full branch : {line_with(body, '<em>full</em>')}")
    print(f"truncated   : {line_with(body, 'Bring a laptop')}")
    print(f"left alone  : {line_with(body, 'Short one.')}")

    print()
    print("Empty the board and ask again:")
    WORKSHOPS.clear()
    response = client.get("/")
    body = response.get_data(as_text=True)
    print(f"GET / -> {response.status_code}")
    print(f"count line  : {line_with(body, 'workshop(s) on the board')}")
    print(f"else branch : {line_with(body, 'Nothing on the board yet.')}")


if __name__ == "__main__":
    main()
