# Mini-project — Personal Blog Web App

Build a small personal blog in Flask. By the end you will have a homepage
listing all posts, a single-post page for each one, a "create post" form,
and a small CSS file. Posts live in an in-memory list — restarts wipe them.
That is fine; Week 10 swaps it for a SQLite database with one-line changes
to the views.

If you finish early, deploy it. Send the URL to a friend. Your code on the
internet is the whole point.

---

## Specification

### Routes

| Method | URL                  | Behaviour                                              |
|--------|----------------------|--------------------------------------------------------|
| GET    | `/`                  | List all posts (newest first), with title + excerpt.   |
| GET    | `/post/<int:post_id>`| Show one post in full.                                 |
| GET    | `/new`               | Show the "create post" form.                           |
| POST   | `/new`               | Validate, store, flash, then redirect to `/`.          |
| GET    | `/static/style.css`  | Your stylesheet (Flask serves this automatically).     |

A 404 on `/post/9999` is required (use `abort(404)` for unknown ids).

### Data model

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Post:
    id: int
    title: str
    body: str
    created_at: datetime = field(default_factory=datetime.now)
```

Store posts in a module-level list:

```python
POSTS: list[Post] = []
```

Use `itertools.count(1)` for an id sequence.

### Templates

You must have:

- `templates/base.html` — the layout (head, header, nav, flash widget,
  footer, content block).
- `templates/index.html` — extends base; loops over `POSTS`.
- `templates/post.html` — extends base; shows one post.
- `templates/new.html` — extends base; the create-post form.

Every page must use `url_for` for every link. No hard-coded URLs.

### Form validation

In the `POST /new` view, reject:

- Empty `title` or `body`.
- `title` longer than 120 characters.
- `body` longer than 10,000 characters.

On any error, **re-render `new.html`** with the values the user typed (so
they do not lose their draft) and `flash(...)` an error message.

On success, append the post, flash "Post published.", and **redirect** to
`/`.

### Styling

A single `static/style.css` file. You can start from the one in the starter
folder and tweak. Required minimums:

- Body uses a readable font (system font stack is fine).
- Width is capped to ~40rem so prose is comfortable to read.
- Posts on the index are visually separated (border, card, or spacing).
- Form fields are full-width with visible labels and a working submit
  button.

### Optional extras (any of these earn rubric points)

- Tag pills under each post title (homework problem 4).
- A search box (homework problem 5).
- A 404 page that extends `base.html` (homework problem 1).
- Deployed to Fly.io / Render / Railway. Submit the URL.

---

## Starter

The `starter/` folder gives you a runnable skeleton with one hard-coded
post, `base.html`, `index.html`, and `style.css`. You add the rest.

```text
mini-project/
├── README.md
└── starter/
    ├── app.py
    ├── templates/
    │   ├── base.html
    │   └── index.html
    └── static/
        └── style.css
```

Run it:

```bash
cd starter
pip install flask
python app.py
```

Then open <http://127.0.0.1:5000>.

---

## Rubric (100 pts)

| Criterion                                                  | Pts |
|------------------------------------------------------------|----:|
| `GET /` lists posts; each title links to its detail page   |  10 |
| `GET /post/<id>` shows the full post; unknown id 404s      |  10 |
| `GET /new` renders the create-post form                    |   5 |
| `POST /new` validates, stores, flashes, redirects (PRG)    |  20 |
| Form re-renders typed values when validation fails         |   5 |
| All templates extend `base.html` (no duplicated layout)    |  10 |
| All inter-app links use `url_for`                          |   5 |
| Flash messages are rendered and styled                     |   5 |
| CSS file is linked via `url_for("static", ...)`            |   5 |
| Code is readable: type hints on view fns, docstrings, no   |     |
| commented-out junk                                         |  10 |
| Has at least one extra (tags, search, custom 404, deploy)  |  15 |
| **Total**                                                  | **100** |

---

## Tips

- Build it route-by-route, not file-by-file. Get `GET /` working with one
  hard-coded post; *then* add `/post/<id>`; *then* the form.
- When something looks broken, **read the terminal**. Flask prints every
  request, every traceback, and every template-render error.
- Resist the urge to add CSS frameworks. A 40-line `style.css` looks
  great and teaches you more.
- **Do not** commit a `.env` file with a real secret. `.gitignore` it.

---

## Up next

Week 10 swaps `POSTS: list[Post] = []` for a SQLite database. The route
code stays almost identical — that is the point of writing well-organised
views this week.
