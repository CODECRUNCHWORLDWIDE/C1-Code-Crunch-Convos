# Week 9 Homework — Six Problems

Six problems that fold into your blog (the mini-project). Work them in
order; problems 2, 4, 5, and 6 build directly on top of each other. Each
problem lists *acceptance criteria* — that is what to aim for.

Estimated total time: **5–7 hours**.

---

## Problem 1 — Custom 404 page

Right now, visiting `/post/9999` shows Flask's default "Not Found" page.
Replace it with a friendly one that extends `base.html`.

### What to do

1. Register an error handler:
   ```python
   @app.errorhandler(404)
   def page_not_found(e):
       return render_template("404.html"), 404
   ```
2. Create `templates/404.html` that extends `base.html` and shows a
   message and a link back to `/`.

### Acceptance criteria

- [ ] `/post/9999` returns status **404** AND renders your custom page.
- [ ] The page uses the same header/footer as the rest of the site
  (i.e., extends `base.html`).
- [ ] Refreshing any *existing* page still works (you did not break
  the happy path).

---

## Problem 2 — Base template

If you have not already done this in the mini-project, extract a
`base.html` and refactor `index.html` and `post.html` to extend it. Move
the `<header>`, `<nav>`, flash-messages widget, and `<footer>` into the
base template.

### Acceptance criteria

- [ ] `base.html` contains the `<!doctype html>`, `<head>`, header, nav,
  flash widget, footer.
- [ ] `index.html` and `post.html` each contain only `{% extends "base.html" %}`
  and the `{% block content %}` (and `{% block title %}`).
- [ ] Adding a new page is one new file plus two block overrides.

---

## Problem 3 — Plug the Week 8 weather CLI into a `/weather` route

In Week 8 you wrote a small CLI that fetched weather data from a public
API and printed it. Lift that logic out (or import it) and put a thin
Flask wrapper around it.

### What to do

1. Add a route `GET /weather` that:
   - Reads `?city=...` from the query string.
   - Calls your Week 8 function (or a freshly-written `requests.get(...)`)
     to fetch the current weather.
   - Renders `weather.html` with `city`, `temp`, and `description`.
2. Show a small form on `/weather` (no `?city=` yet) where the user can
   type a city and submit (`GET` form — search-style).
3. If the API call fails (timeout, 404, no API key), flash an error and
   re-render the form.

### Acceptance criteria

- [ ] `/weather` (no params) shows the search form.
- [ ] `/weather?city=London` shows the current weather for London.
- [ ] A bad city flashes a clean error message — no traceback in the
  browser when debug is off.
- [ ] Your API key (if any) is loaded from `os.environ`, NOT hard-coded.

### Stretch

- Cache results for 5 minutes per city in a module-level dict so repeated
  refreshes do not hammer the API.

---

## Problem 4 — Post tags

Add a `tags: list[str]` field to your `Post` dataclass. Let the user enter
tags as a comma-separated string in the create-post form; split them on
the server.

### What to do

1. Update `Post`:
   ```python
   @dataclass
   class Post:
       id: int
       title: str
       body: str
       tags: list[str] = field(default_factory=list)
   ```
2. Add a `<input name="tags">` to the create-post form.
3. Server-side, split on `,`, strip whitespace, lowercase, drop empties.
4. Show tags as small pills next to each post title.
5. Add a route `GET /tag/<tag>` that lists posts with that tag (or 404 if
   nothing matches).

### Acceptance criteria

- [ ] Creating a post with `python, flask, web` saves three tags.
- [ ] The blog index shows tag pills under each title.
- [ ] Clicking a tag goes to `/tag/python` and lists only matching posts.
- [ ] An unknown tag (`/tag/zzz`) returns 404.

---

## Problem 5 — Search filter

Add a search box to your blog index. Submitting it filters posts whose
title OR body contains the query (case-insensitive).

### What to do

1. Put a `<form method="get" action="/">` at the top of `index.html` with
   one text field named `q`.
2. In the index view: read `q = request.args.get("q", "").strip().lower()`
   and filter your posts before passing them to the template.
3. If `q` is empty, show all posts (default behaviour).
4. Show the query in the page title so it round-trips back to the user:
   "Search results for 'flask' (3 found)".

### Acceptance criteria

- [ ] `/?q=flask` shows only matching posts.
- [ ] `/?q=` (empty) shows all posts.
- [ ] The form's text input keeps the typed value on reload
  (`value="{{ request.args.get('q', '') }}"`).
- [ ] No traceback for any input, including unicode and HTML-looking
  strings.

---

## Problem 6 — Simple session-based auth (DEMO ONLY)

> **Security warning.** This problem demonstrates **how Flask sessions
> work**, NOT how to build real authentication. The password is hardcoded
> in source. Real apps store hashed passwords in a database and protect
> against timing attacks, brute force, and CSRF. **Do not deploy this
> auth pattern anywhere real.**

Gate the `/new` (create-post) route behind a hardcoded password.

### What to do

1. Add a config value:
   ```python
   app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD", "letmein")
   ```
2. Add a `GET/POST /login` route:
   - GET shows a form with a single `password` field.
   - POST compares `request.form["password"]` to
     `app.config["ADMIN_PASSWORD"]`. On success, set
     `session["is_admin"] = True` and redirect to `/`. On failure, flash
     an error.
3. Add a `POST /logout` route that pops `is_admin` from the session.
4. Protect `/new`: at the top of the view function,
   ```python
   if not session.get("is_admin"):
       flash("Please log in to create posts.", "error")
       return redirect(url_for("login"))
   ```
5. Show a "Log in" / "Log out" link in the nav depending on
   `session.get("is_admin")`.

### Acceptance criteria

- [ ] Unauthenticated `/new` redirects to `/login` with a flash.
- [ ] Correct password sets `session["is_admin"] = True`.
- [ ] Logout clears it.
- [ ] The "Log in" link in the nav flips to "Log out" after logging in.

### Stretch (and a security exercise)

Read the OWASP cheat sheet on session management:
<https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
and write 3 bullet points describing what is wrong with the auth in this
homework. (You will not turn it in; the point is to think about it.)

---

## References

- Flask error handlers — <https://flask.palletsprojects.com/en/stable/errorhandling/>
- Flask template inheritance — <https://flask.palletsprojects.com/en/stable/patterns/templateinheritance/>
- Flask sessions — <https://flask.palletsprojects.com/en/stable/quickstart/#sessions>
- Flask config handling — <https://flask.palletsprojects.com/en/stable/config/>
- OWASP — Session Management Cheat Sheet — <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
