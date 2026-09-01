# Exercise 3 — Template Loop

> **Topic:** `render_template`, passing a list into Jinja2, and looping over it with `{% for %}`
> **Lecture:** [02 — Templates and Static Files](../lecture-notes/02-templates-and-static.md)
> **Difficulty:** Easy
> **Target time:** 1 hour
> **Why this one:** Exercise 2 ended with you gluing HTML together out of f-strings. That approach does not merely get ugly — it is the standard way beginners ship a cross-site-scripting hole, because an f-string will happily paste a visitor's `<script>` tag straight into your page. Templates fix the readability problem and the security problem in the same move. Every page in the mini-project goes through `render_template`.

## The Brief

The study hall now publishes a board of upcoming workshops: a title, who is
hosting, how many seats are left, and a note. You are going to render that
board as a real HTML page, from a real template file, with a real loop.

Three details in the data are there to bite you, and you should let them.
One workshop is full, so your template needs a conditional. One note is long
enough to need truncating. And one title contains an ampersand and a pair of
angle brackets — `Sorting, Big-O & <you>` — which is exactly the kind of
string that would have broken your Exercise 2 index, or worse, executed.

This is the first exercise with a folder instead of a single file, because
Flask looks for templates in a directory named `templates/` sitting next to
your app.

## Directory layout

Create this tree in your practice repo. The folder name `templates` is not
optional — it is where Flask's default template loader looks, and getting it
wrong is the single most common error in this exercise.

```text
exercise-03-template-loop/
├── app.py
└── templates/
    └── list.html
```

## Starter

### `app.py`

```python
"""app.py — render a list of study-hall workshops through a Jinja2 template.

Run from inside exercise-03-template-loop/:
    python app.py
"""

from dataclasses import dataclass

from flask import Flask, render_template

app: Flask = Flask(__name__)


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
    # TODO: return render_template(...) and pass WORKSHOPS in as `workshops`.
    ...


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

### `templates/list.html`

This one is complete. Read every line before you run it; you are being given
the answer to the template so that you can spend the hour understanding it
rather than typing angle brackets.

```jinja
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
```

## Requirements

1. `GET /` renders `list.html` and returns status `200`.
2. The count line reads `3 workshop(s) on the board.` and comes from
   `{{ workshops|length }}`, not from a number you typed.
3. All three workshops appear, numbered `1.`, `2.`, `3.` by `loop.index`.
4. Workshop 2 shows `full`; workshops 1 and 3 show their seat counts.
5. Workshop 1's note is truncated to `Bring a laptop. We rewrite three loops
   as comprehensions...` — that is `truncate(60)` doing the work, not a
   slice you wrote in Python.
6. Workshop 2's title appears in the page source as
   `Sorting, Big-O &amp; &lt;you&gt;` and in the browser as
   `Sorting, Big-O & <you>`. If you see a raw `<you>` in the source,
   autoescaping is off and you have a bug.
7. Setting `WORKSHOPS = []` and refreshing shows `Nothing on the board yet.`
   from the `{% else %}` branch of the loop — you do not wrap the whole list
   in an extra `{% if %}`.

## Constraints

- **Pass the whole list into the template; do not pre-format anything in
  Python.** No building `<li>` strings in the view. The split is: Python
  decides *what* the data is, the template decides *how it looks*. Blur that
  line and every visual change starts requiring a Python change.
- **Leave autoescaping alone.** Flask turns Jinja2 autoescaping **on by
  default**, which is why requirement 6 passes without you doing anything.
  Four things turn it off, and you should be able to name them: the `|safe`
  filter, an `{% autoescape false %}` block, wrapping the value in
  `markupsafe.Markup(...)` in Python, and — the one that surprises people —
  giving the template a non-HTML extension. Flask only autoescapes files
  ending in `.html`, `.htm`, `.xml`, `.xhtml`, and `.svg`. Rename
  `list.html` to `list.txt` and your escaping silently disappears.
- **Do not name the loop variable `session`.** Flask injects its own
  `session` object into every template context. Shadowing it works right up
  until the day you reference `session` outside the loop and silently read
  Flask's cookie object instead of your data. Reserved-ish names in every
  Flask template: `session`, `request`, `g`, `config`, `url_for`.
- **Use `{% else %}` inside the `{% for %}` for the empty case, not a
  separate `{% if workshops %}`.** Jinja gives you the empty branch for free,
  and the two-construct version drifts out of sync the moment someone edits
  one and not the other.
- **Use the `truncate` filter, not `notes[:60]`.** A raw slice cuts words in
  half and produces `comprehensi`. `truncate` backs up to a word boundary and
  appends an ellipsis. It also leaves short strings alone — it only trims
  when the string is longer than the limit plus a small leeway, which is why
  `Short one.` comes through whole.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0 and Jinja2 3.1.5:

```text
$ python exercise-03-template-loop-solution.py
GET / -> 200
count line  : <p>3 workshop(s) on the board.</p>
escaped     : 2. <strong>Sorting, Big-O &amp; &lt;you&gt;</strong>
raw <you> reached the page: False
full branch : <em>full</em>
truncated   : <p>Bring a laptop. We rewrite three loops as comprehensions...</p>
left alone  : <p>Short one.</p>

Empty the board and ask again:
GET / -> 200
count line  : <p>0 workshop(s) on the board.</p>
else branch : <li><em>Nothing on the board yet.</em></li>
```

Those are the lines the acceptance checklist cares about, pulled out of the
rendered page. In a browser your own build reads as:

```console
Upcoming workshops

3 workshop(s) on the board.

  1. Loops and Lists hosted by ada — 4 seat(s) left
     Bring a laptop. We rewrite three loops as comprehensions...
  2. Sorting, Big-O & <you> hosted by grace — full
     Short one.
  3. Reading Tracebacks hosted by ada — 2 seat(s) left
     Wi-fi is flaky in room B; download the slides first.
```

and the proof that escaping happened is in the raw source (the leading
whitespace comes from your template's indentation and will vary):

```console
$ curl -s http://127.0.0.1:5000/ | grep "Big-O"
<strong>Sorting, Big-O &amp; &lt;you&gt;</strong>
```

## Steps

1. Make the folder and the `templates/` subfolder. Create both files.
2. Fill in the one `TODO` in `app.py`. The keyword name you pass
   (`workshops=WORKSHOPS`) is the name the template uses — they must match.
3. Run `python app.py` from inside `exercise-03-template-loop/` and load
   <http://127.0.0.1:5000>.
4. View the page source in the browser (Ctrl-U, or Cmd-Opt-U on macOS) and
   find the `Big-O` line. Confirm you see `&amp;` and `&lt;`, not `&` and `<`.
5. Now break it on purpose: change the template to
   `{{ workshop.title|safe }}`, refresh, and view the source again. The angle
   brackets are raw and the browser is trying to parse `<you>` as a tag.
   That is a cross-site-scripting hole in miniature. Undo it.
6. Set `WORKSHOPS = []`, refresh, and confirm the `{% else %}` branch
   renders. Put the data back.
7. Change a workshop's `seats_left` to `0` and confirm the `{% if %}` branch
   flips. Templates are re-read on the next request in debug mode, so a
   template edit needs only a browser refresh, not a restart.

## The Solution

```python
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
```

**The keyword name is the template variable name.** `workshops=WORKSHOPS`
means the template sees `workshops`. Not `WORKSHOPS`, not the name of the
Python variable — the keyword. That is the entire contract between the two
files, and getting it wrong does not raise; see the bug list below for what
it does instead, which is worse.

**`Flask(__name__)` is how `templates/` gets found.** The `__name__` you pass
in lets Flask locate the module on disk and set its `root_path`; the default
template loader then looks in `root_path/templates`. That is why the folder
name is not a suggestion and why the app has to be started from inside the
exercise folder. The shipped file swaps that loader for a `DictLoader` so the
template can travel inside the file — same names, same autoescaping, no
folder.

**`WORKSHOPS` is looked up per request, so the empty case is testable.**
`index()` reads the module global when it runs, which is why `main()` can call
`WORKSHOPS.clear()` between two requests and watch the page change. Had the
view closed over a value captured at import time, requirement 7 would need a
restart to test.

**`{% else %}` on a `{% for %}` means "the iterable was empty".** Python has
`for`/`else` too and it means something entirely different there — it runs
unless you `break`. Jinja's version is the branch a template actually wants,
and using it instead of wrapping the whole block in `{% if workshops %}` means
there is one place that decides what "empty" looks like.

**`loop.index` is the position in the loop, not the record's id.** It starts
at 1, and `loop.index0` starts at 0. Here they agree with `workshop.id`
because the list happens to be in id order; sort the board differently, as the
stretch asks, and they immediately disagree. If you want the id, say
`workshop.id`.

**`truncate(60)` cuts at a word boundary, and leaves short strings alone.**
The filter takes a `leeway` of 5 by default, so anything up to 65 characters
comes through untouched; past that it cuts at 57 characters — the limit minus
the three-character ellipsis — backs up to the last whole word, and appends
`...`. The three notes are 71, 10 and 52 characters long, so exactly one of
them is trimmed. The slice you were tempted to write, `notes[:60]`, produces
`...three loops as comprehensions and` — no ellipsis, a dangling "and", and
on a different note it would cut a word in half.

**Autoescaping is on because the template is named `list.html`.** That is why
requirement 6 passes without you doing anything: `{{ workshop.title }}`
renders `Sorting, Big-O &amp; &lt;you&gt;` in the source and
`Sorting, Big-O & <you>` on screen. The Under the hood block below lists the
four things that turn it off — including the file-extension one that nobody
sees coming.

## Download and run

Download
[exercise-03-template-loop-solution.py](./exercise-03-template-loop-solution.py)
and run it:

```bash
python exercise-03-template-loop-solution.py
```

It needs Flask installed and nothing else, and it exits on its own — the
template travels inside the file, so no `templates/` folder is required. Your
own build keeps the two-file layout this page teaches, because that layout is
the thing Flask expects from every real project.

The `-solution` in the filename keeps this file from colliding with your own
exercise folder.

## Common bugs to catch

- **`jinja2.exceptions.TemplateNotFound: list.html`.** Your template is not
  at `templates/list.html`. Check for `template/` singular, a nested
  `templates/templates/`, or a file saved as `list.html.txt` by an editor
  that hid the extension.
- **The board renders perfectly and is empty — `0 workshop(s)` and the
  `{% else %}` message, status `200`, no error anywhere.** You passed
  `WORKSHOPS=WORKSHOPS` or `workshop=WORKSHOPS` to `render_template`. This
  does *not* raise: Jinja's default `Undefined` prints as an empty string,
  reports a `length` of 0, and iterates as empty, so `{{ workshops|length }}`
  prints `0` and the loop takes its empty branch. The keyword name *is* the
  template variable name, and the tell for getting it wrong is a page that
  looks finished and shows nothing. (Attribute access is the loud version:
  `{{ workshops.title }}` on an undefined name does raise
  `jinja2.exceptions.UndefinedError: 'workshops' is undefined`.)
- **The page shows a literal `{{ workshops|length }}`.** You are not
  rendering the template — you returned the file's text, or you opened the
  `.html` file directly from disk. Check that the address bar says
  `127.0.0.1:5000` and not `file:///`.
- **`jinja2.exceptions.TemplateSyntaxError: Unexpected end of template.
  Jinja was looking for the following tags: 'endfor' or 'else'.`** A
  `{% for %}` with no `{% endfor %}`. Every Jinja block tag needs its
  partner; unlike Python, indentation means nothing here.
- **`jinja2.exceptions.UndefinedError: 'list object' has no attribute
  'title'`.** You wrote `{{ workshops.title }}` instead of
  `{{ workshop.title }}` — the loop variable is the singular one.
- **`jinja2.exceptions.UndefinedError: 'len' is undefined`.** Jinja has no
  Python builtins. Use the `length` filter: `{{ workshops|length }}`.
- **The full workshop prints `0 seat(s) left` instead of `full`.** Your
  condition is inverted, or you wrote `{% if workshop.seats_left = 0 %}`.
  Jinja uses Python's comparison operators, so a single `=` is a syntax
  error and `>` / `==` behave exactly as you expect.
- **Nothing renders at all and the log shows a `500`.** You left the `...`
  in `index()`, so the view returned `None`:
  `TypeError: The view function for 'index' did not return a valid
  response.`

## Under the hood

<details>
<summary>Under the hood — the four ways autoescaping turns off, and the file-extension trap</summary>

Flask switches Jinja2's autoescaping on for you, per template, by name. All
four of the off-switches below were checked against Flask 3.1.0 and Jinja2
3.1.5 before being written down here:

| What you write | What `Sorting, Big-O & <you>` renders as |
|---|---|
| `{{ title }}` | `Sorting, Big-O &amp; &lt;you&gt;` |
| `{{ title\|safe }}` | `Sorting, Big-O & <you>` |
| `{% autoescape false %}{{ title }}{% endautoescape %}` | `Sorting, Big-O & <you>` |
| `{{ title }}`, with `markupsafe.Markup(title)` passed in from Python | `Sorting, Big-O & <you>` |

The fourth way is the file extension, and it is the one nobody sees coming.
Flask decides per template with a plain suffix check: autoescaping is on for
`.html`, `.htm`, `.xml`, `.xhtml` and `.svg`, and off for everything else.
Copy `list.html` to `list.txt`, render that instead, and nothing warns you:

```text
list.html -> 2. <strong>Sorting, Big-O &amp; &lt;you&gt;</strong>
list.txt  -> 2. <strong>Sorting, Big-O & <you></strong>
```

Same template text, same data, and the second one is a cross-site-scripting
hole.

Now the part that bites people who read style guides: **`.html.jinja` and
`.j2` are not on the list either.** Both are popular naming conventions —
Ansible ships `.j2` files, and several linters suggest `.html.jinja` so
editors pick the right syntax highlighting. Flask's suffix check does not
strip the extra extension first; `list.html.jinja` simply does not end in
`.html`, so escaping is off. Verified on this exact stack:

```text
>>> app.select_jinja_autoescape("list.html")        # True
>>> app.select_jinja_autoescape("list.html.jinja")  # False
>>> app.select_jinja_autoescape("list.j2")          # False
```

Adopt one of those conventions from a blog post and you turn escaping off
across your whole project in one rename commit, with no error, no warning,
and every page still rendering. If you want the suffix, override the check —
`app.select_jinja_autoescape` is a method you can replace — or, simpler,
keep templates named `.html`.

Why is the default not "always on"? Because Jinja is not only an HTML
engine — people render emails, config files and SQL from it, where `&amp;`
would be corruption, not safety. The extension is the signal Flask uses to
guess what you are rendering. It is a good guess, and it is only a guess.

</details>

## Acceptance checklist

- [ ] `python app.py` serves a rendered page at `/` with status `200`.
- [ ] The count line comes from the `length` filter, and all three workshops render.
- [ ] The full workshop shows `full`; the others show seat counts.
- [ ] Workshop 1's note is truncated at a word boundary with an ellipsis.
- [ ] Page source shows `&amp;` and `&lt;` for workshop 2's title.
- [ ] An empty `WORKSHOPS` list renders the `{% else %}` message.
- [ ] You can name at least three ways autoescaping gets turned off.
- [ ] The folder is committed to Git with a message like `Add Week 9 exercise 3: template loop`.

## Stretch

- Split `list.html` into `base.html` plus a child that uses `{% extends %}`
  and `{% block content %}`. It is more files for the same page today, and it
  is the only sane structure by the third page.
- Add `static/style.css` next to `app.py` and link it with
  `{{ url_for('static', filename='style.css') }}`. Give full workshops a grey
  background.
- Sort the board by seats remaining before rendering. Do the sorting in
  Python (`sorted(WORKSHOPS, key=...)`), not in the template — ordering is a
  decision about the data, and the template's job is presentation.
- Add a `/workshop/<int:workshop_id>` route with its own template and link
  each title to it with `url_for`. That is Exercise 2's converter plus this
  exercise's template, which is most of a real app.

When your board renders and escapes correctly, move on to
[Exercise 4 — Form Echo](./exercise-04-form-echo.md).
