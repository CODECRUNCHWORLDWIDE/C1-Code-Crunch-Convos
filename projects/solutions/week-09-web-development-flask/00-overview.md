# Crunch Blog — Week 9 reference implementation

This is the finished answer to the Week 9 mini-project, [Personal Blog Web
App](../../../curriculum/week-09-web-development-flask/mini-project/README.md).
It also implements all six [homework](../../../curriculum/week-09-web-development-flask/homework/README.md)
problems and three of the week's stretch goals, because those problems were
written to fold into this app rather than to stand beside it.

Each homework problem is worked through on its own page, beside the runnable
answer for that problem. This file is the operating manual for the app the six
of them add up to: what the files are, how to run them, and how each line of
the rubric is satisfied.

---

## Run it

```bash
cd projects/solutions/week-09-web-development-flask
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open <http://127.0.0.1:5000>. Seven posts are seeded so that pagination and
search have something to chew on.

To create a post you must log in first: **Log in** in the nav, password
`letmein` (or whatever `ADMIN_PASSWORD` is set to). That gate is homework
problem 6 and it is a **demo of sessions, not real authentication** — see
[Security: what is deliberately wrong here](#security-what-is-deliberately-wrong-here).

`/weather` calls the live [Open-Meteo](https://open-meteo.com/) API, the same
one your Week 8 CLI used. It needs no key and no signup. With no network, the
route flashes `Could not reach the weather service.` and re-renders the form —
which is exactly the behaviour homework problem 3 asks for.

## Check it

```bash
python smoke_test.py
```

The last line should read:

```text
ALL 46 CHECKS PASSED
```

`smoke_test.py` drives the app through Flask's built-in test client, in
process — nothing binds a port, no browser is involved, and the weather calls
are stubbed so the suite passes offline. Deliberately no `pytest`: you do not
meet it until Week 11, and plain `assert` plus a counter is enough here.

---

## The files, in the order worth reading them

| File | What it holds |
|---|---|
| [`app.py`](./app.py) | Every route. Read `index` → `show_post` → `new_post` first; everything else is a variation. |
| [`templates/base.html`](./templates/base.html) | The layout. Head, header, nav, flash include, content block, footer. |
| [`templates/_flashes.html`](./templates/_flashes.html) | The flash widget, included by `base.html`. Leading underscore = partial, not a page. |
| [`templates/index.html`](./templates/index.html) | Search form, post cards, tag pills, pager. |
| [`templates/post.html`](./templates/post.html) | One post in full. |
| [`templates/new.html`](./templates/new.html) | The create-post form, re-populated from whatever the user typed. |
| [`templates/tag.html`](./templates/tag.html) | Posts carrying one tag. |
| [`templates/login.html`](./templates/login.html) | The demo login, with its warning banner. |
| [`templates/weather.html`](./templates/weather.html) | The Week 8 lookup, wearing this site's layout. |
| [`templates/404.html`](./templates/404.html) | Homework problem 1. |
| [`static/style.css`](./static/style.css) | About 150 lines, all of it readable in a minute. |
| [`weather.py`](./weather.py) | The Week 8 networking logic with the printing removed. |
| [`smoke_test.py`](./smoke_test.py) | The 46 checks. |
| [`requirements.txt`](./requirements.txt), [`Procfile`](./Procfile), [`.env.example`](./.env.example), [`.gitignore`](./.gitignore) | Deployment. |

The route table, straight from the CLI:

```text
$ flask routes
Endpoint   Methods    Rule
---------  ---------  -----------------------
api_posts  GET        /api/posts
healthz    GET        /healthz
index      GET        /
login      GET, POST  /login
logout     POST       /logout
new_post   GET, POST  /new
show_post  GET        /post/<int:post_id>
show_tag   GET        /tag/<tag>
static     GET        /static/<path:filename>
weather    GET        /weather
```

---

## How it maps to the mini-project spec

Every required route, present and behaving:

| Method | URL | Where |
|---|---|---|
| GET | `/` | `index` — newest first, `?q=` filtered, 5 per page |
| GET | `/post/<int:post_id>` | `show_post` — unknown ids 404 through `find_post` |
| GET | `/new` | `new_post`, `request.method == "GET"` branch |
| POST | `/new` | `new_post`, validate → flash → redirect |
| GET | `/static/style.css` | Flask's built-in static handler |

And the rubric, line by line:

| Criterion | Pts | Where it is satisfied |
|---|---:|---|
| `GET /` lists posts; each title links to its detail page | 10 | `index.html`, `url_for('show_post', post_id=post.id)` |
| `GET /post/<id>` shows the full post; unknown id 404s | 10 | `show_post` + `find_post`'s `abort(404)` |
| `GET /new` renders the create-post form | 5 | `new_post` GET branch → `new.html` |
| `POST /new` validates, stores, flashes, redirects (PRG) | 20 | `new_post` POST branch |
| Form re-renders typed values when validation fails | 5 | `render_template("new.html", title=title, body=body, tags=raw_tags)` |
| All templates extend `base.html` | 10 | every file in `templates/` except `_flashes.html`, which is included |
| All inter-app links use `url_for` | 5 | no `href="/..."` literal anywhere in `templates/` |
| Flash messages are rendered and styled | 5 | `_flashes.html` + `.flash-success` / `.flash-error` |
| CSS linked via `url_for("static", ...)` | 5 | `base.html`, line 7 |
| Readable code: type hints, docstrings, no junk | 10 | every view is annotated and documented |
| At least one extra | 15 | four of them: tags, search, custom 404, deploy config |

## How it maps to the homework

| Problem | Where |
|---|---|
| 1 — Custom 404 page | `@app.errorhandler(404) page_not_found` + `templates/404.html` |
| 2 — Base template | `templates/base.html`; every page is `{% extends %}` plus two blocks |
| 3 — Week 8 weather CLI on a `/weather` route | `weather.py` + the `weather` view; caching is the stretch goal, `CACHE_TTL_SECONDS = 300` |
| 4 — Post tags | `Post.tags`, `parse_tags`, the pills in `index.html`/`post.html`, `show_tag` |
| 5 — Search filter | `index`'s `raw_q` / `needle` pair and the `<form class="search">` |
| 6 — Session-based auth (demo only) | `login`, `logout`, the guard at the top of `new_post`, the nav branch in `base.html` |

## Stretch goals that made it in

- **Pagination** — `paginate()` and the pager in `index.html`. `PAGE_SIZE = 5`.
- **`/api/posts`** — returns a JSON array. Flask 2.2+ jsonifies a returned
  `list` for you, so the view is one comprehension.
- **`/healthz`** — returns `"OK", 200` for a load balancer.
- **Weather cache** — `weather.py` keeps a 5-minute per-city cache keyed on the
  lowercased city name, timed with `time.monotonic()` so a clock change cannot
  make an entry immortal.

Not done here, on purpose, because Week 10 does it properly: persistence.
`POSTS` is a module-level list and a restart wipes it.

---

## Security: what is deliberately wrong here

The login is homework problem 6, and that problem is explicit that it is a
demonstration of how a Flask session works — not a way to protect anything.
Named plainly, so nobody copies it into something real:

1. **The password is a constant**, compared with `==`. No hashing (so anyone
   who reads the source or the environment has it) and no constant-time
   comparison (so the check leaks a little timing information).
2. **There is no CSRF token.** Any page on the internet can make your logged-in
   browser POST to `/new`. `Flask-WTF` is the standard fix.
3. **There is no rate limiting.** Guessing is free and unlimited.
4. **There is one shared account and no user model**, so nothing can be
   audited, revoked, or scoped.
5. **The session cookie is signed, not encrypted.** Anyone holding it can read
   it. That is fine for `is_admin`, and fatal for anything you would not print
   on a postcard.

Watch that last one directly — this is a real `Set-Cookie` header from this app
after a flash:

```text
Set-Cookie: session=eyJfZmxhc2hlcyI6W3siIHQiOlsic3VjY2VzcyIsIkFkZGVkLiJdfV19.aohYsQ.1w24BFMvp5cJAsX1aTRrLYLAaas; HttpOnly; Path=/
```

Base64-decode the first dot-separated segment and you get the payload in the
clear:

```json
{"_flashes":[{" t":["success","Added."]}]}
```

The two segments after it are a timestamp and the HMAC signature. The signature
is what your `SECRET_KEY` protects: a visitor can *read* that JSON, and cannot
*change* it without the key. Hence rule one of secret keys — long, random, and
never committed.

The [OWASP Session Management Cheat
Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
is the reading that turns those five bullets into instincts.

---

## Deploying

`requirements.txt` and `Procfile` are ready for Render or Railway; Fly.io wants
the same start command in `fly.toml`.

```text
web: gunicorn "app:app" --bind 0.0.0.0:$PORT --workers 2
```

Then, in the host's environment-variable UI, set:

```text
SECRET_KEY=<output of: python -c "import secrets; print(secrets.token_hex(32))">
ADMIN_PASSWORD=<something that is not "letmein">
```

`.env` is gitignored; `.env.example` is the committed template that documents
which variables exist without leaking their values. Never run `app.run(debug=True)`
on a public host — the interactive debugger is a remote code execution vector,
not a nice-to-have.

## What Week 10 changes

`POSTS: list[Post] = []` becomes a SQLite table. `find_post` becomes a
`SELECT ... WHERE id = ?`. `POSTS.append(...)` becomes an `INSERT`. The views,
the templates, the CSS, the validation and the PRG flow do not move. That is
the payoff for keeping storage decisions inside three small helpers instead of
smeared across every view.
