# Challenge 2 — Flask blog integration tests (reference solution)

![CI](https://github.com/YOUR-USERNAME/week-11-flask-tests/actions/workflows/ci.yml/badge.svg)

The Week 9 blog, refactored until it could be tested, then tested: 39 tests,
100 % branch coverage on `blog/`, `ruff`/`black`/`mypy --strict` clean, and a
GitHub Actions workflow that runs all four on every push.

## How to run the tests

```bash
cd challenge-02-flask-blog-tests
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt

pytest                                                        # fast loop
pytest -vv                                                    # per-test listing
pytest --cov=blog --cov-report=term-missing --cov-fail-under=80
```

`pyproject.toml` sets `addopts = "-ra -q"`, so plain `pytest -v` cancels back
to normal verbosity. Use `-vv` for the listing below.

## `pytest -vv` output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.1.1, pluggy-1.6.0
rootdir: .../challenge-02-flask-blog-tests
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0, mock-3.15.1
collected 39 items

tests/test_app_factory.py::test_factory_works_with_no_config PASSED      [  2%]
tests/test_app_factory.py::test_config_overrides_the_defaults PASSED     [  5%]
tests/test_app_factory.py::test_two_apps_do_not_share_a_database PASSED  [  7%]
tests/test_auth.py::test_delete_redirects_anonymous_callers_to_login PASSED [ 10%]
tests/test_auth.py::test_anonymous_delete_does_not_delete PASSED         [ 12%]
tests/test_auth.py::test_login_redirect_remembers_where_you_were_going PASSED [ 15%]
tests/test_auth.py::test_login_page_renders PASSED                       [ 17%]
tests/test_auth.py::test_correct_password_logs_you_in PASSED             [ 20%]
tests/test_auth.py::test_wrong_password_returns_401 PASSED               [ 23%]
tests/test_auth.py::test_missing_password_returns_401 PASSED             [ 25%]
tests/test_auth.py::test_logout_clears_the_session PASSED                [ 28%]
tests/test_auth.py::test_logout_is_idempotent PASSED                     [ 30%]
tests/test_blog.py::test_index_returns_200 PASSED                        [ 33%]
tests/test_blog.py::test_index_lists_seeded_posts PASSED                 [ 35%]
tests/test_blog.py::test_index_says_so_when_empty PASSED                 [ 38%]
tests/test_blog.py::test_show_post_returns_200_for_existing_post PASSED  [ 41%]
tests/test_blog.py::test_show_missing_post_returns_404 PASSED            [ 43%]
tests/test_blog.py::test_unknown_url_returns_404 PASSED                  [ 46%]
tests/test_blog.py::test_create_post_redirects_and_shows_up_on_the_index PASSED [ 48%]
tests/test_blog.py::test_create_post_follow_redirects_lands_on_the_post PASSED [ 51%]
tests/test_blog.py::test_create_post_strips_surrounding_whitespace PASSED [ 53%]
tests/test_blog.py::test_create_post_rejects_incomplete_forms[empty-form] PASSED [ 56%]
tests/test_blog.py::test_create_post_rejects_incomplete_forms[no-body] PASSED [ 58%]
tests/test_blog.py::test_create_post_rejects_incomplete_forms[no-title] PASSED [ 61%]
tests/test_blog.py::test_create_post_rejects_incomplete_forms[whitespace-only] PASSED [ 64%]
tests/test_blog.py::test_rejected_post_is_not_stored PASSED              [ 66%]
tests/test_blog.py::test_create_post_rejects_an_over_long_title PASSED   [ 69%]
tests/test_blog.py::test_create_post_rejects_an_over_long_body PASSED    [ 71%]
tests/test_blog.py::test_rejected_form_keeps_what_you_typed PASSED       [ 74%]
tests/test_blog.py::test_new_post_form_renders PASSED                    [ 76%]
tests/test_blog.py::test_new_is_not_parsed_as_a_post_id PASSED           [ 79%]
tests/test_blog.py::test_delete_via_form_route_removes_the_post PASSED   [ 82%]
tests/test_blog.py::test_delete_via_http_delete_removes_the_post PASSED  [ 84%]
tests/test_blog.py::test_delete_missing_post_returns_404 PASSED          [ 87%]
tests/test_blog.py::test_404_logs_a_warning PASSED                       [ 89%]
tests/test_blog.py::test_public_pages_return_200[/] PASSED               [ 92%]
tests/test_blog.py::test_public_pages_return_200[/about] PASSED          [ 94%]
tests/test_blog.py::test_public_pages_return_200[/posts/1] PASSED        [ 97%]
tests/test_blog.py::test_seeded_app_fixture_pre_populates_three_posts PASSED [100%]

============================= 39 passed in 0.40s ==============================
```

## Coverage

```text
Name               Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------
blog\__init__.py      17      0      2      0   100%
blog\auth.py          32      0      4      0   100%
blog\db.py            29      0      0      0   100%
blog\views.py         54      0     12      0   100%
--------------------------------------------------------------
TOTAL                132      0     18      0   100%
Required test coverage of 80% reached. Total coverage: 100.00%
```

The rubric asks for 80 % on the routes module. 100 % on all four modules is
what falls out once you write the seven required tests plus the three stretch
tests — the app is small enough that there is nowhere for an untested line to
hide, which is itself the argument for keeping views thin.

## What changed in the Week 9 code to make it testable

Three changes, in the order they mattered.

**An app factory replaced the module-level `app`.** Week 9 opened with
`app = Flask(__name__)` at import time, configured from environment variables.
That gives the whole process exactly one app, built before any test can say
what it wants. `create_app(config)` takes a mapping, layers it over the
defaults, and returns a fresh app — so `tests/conftest.py` can ask for
`{"TESTING": True, "DATABASE": ":memory:"}` and every test gets its own
universe. `test_two_apps_do_not_share_a_database` is that change expressed as
an assertion.

**Storage moved out of the views and behind `blog/db.py`.** Week 9 kept posts
in a module-level `POSTS: list[Post]`, which survives between tests and makes
test order matter. Now the views call `db.list_posts()`, `db.get_post()`,
`db.create_post()`, `db.delete_post()`, and the database is a `:memory:` SQLite
file that dies with its app. Note the deliberate oddity documented at the top
of `db.py`: one connection per *application*, not per request. An in-memory
SQLite database lives inside its connection, so a per-request connection would
hand every request an empty database and the tests would pass while proving
nothing.

**Routes moved onto blueprints, and an auth gate was added.** `blog.views`
holds the public routes; `blog.auth` holds the login gate that required test 7
needs — one password in config, one `session["is_admin"]` flag, one
`login_required` decorator on the delete route. Week 9 had no auth at all, so
this is genuinely new code rather than a refactor, and only the delete route is
protected so the other five routes keep their Week 9 behaviour.

## Quality gates

```bash
ruff check .        # All checks passed!
black --check .     # 8 files would be left unchanged.
mypy blog tests     # Success: no issues found in 8 source files
```

Two of those took a fix worth naming:

- **`ruff` `target-version = "py311"`, not `"py312"`.** CI runs a 3.11 + 3.12
  matrix, and `target-version` must name the *oldest* interpreter you support.
  At `py312`, rule `UP047` tells you to rewrite `login_required`'s `TypeVar` as
  a PEP 695 generic (`def login_required[ViewT: ...]`), which is a syntax error
  on 3.11 and would turn half the matrix red.
- **`redirect()` returns a `werkzeug` response, not a `flask` one.** Annotate a
  view `-> flask.Response` and `mypy --strict` says
  `Incompatible return value type (got "werkzeug.wrappers.response.Response", expected "flask.wrappers.Response")`.
  Import `Response` from `werkzeug.wrappers` in any module that returns a
  redirect.

## Where to read

1. `blog/__init__.py` — the factory. The whole challenge is downstream of it.
2. `blog/db.py` — storage, and the one-connection-per-app note.
3. `blog/views.py` — six routes, each one thin.
4. `blog/auth.py` — the login gate and `login_required`.
5. `tests/conftest.py` — the fixture graph. Read this before the tests.
6. `tests/test_blog.py` — required tests 1–6 plus the three stretch tests.
7. `tests/test_auth.py` — required test 7 and the gate's own behaviour.
8. `tests/test_app_factory.py` — the factory tested directly.
