# Challenge 2 — Integration tests for the Week 9 Flask blog

**Goal:** retrofit a real test suite onto the Flask blog you built in Week 9. By the end of this challenge you can refactor that app with confidence — because the tests scream the moment you break something.

**Approx. time:** 3 hours.

---

## Background

In Week 9 you built a small Flask app — at minimum, a few routes for listing, reading, and creating posts. You probably tested it by clicking around in the browser. That works for one developer on one feature. It does not scale.

Flask ships with a `test_client`, a fake browser that lets you fire requests at your views without starting a server, and assert on the response. Combined with pytest fixtures, you can spin up a fresh app + database per test, exercise every route, and tear it down — all in under a second.

---

## Setup

Copy your Week 9 project into a new folder for this challenge so you don't break the original:

```bash
cp -r ../../week-09-web-development-flask/mini-project ./week-11-flask-tests
cd week-11-flask-tests
python -m venv .venv && source .venv/bin/activate
pip install flask pytest pytest-cov
```

Add a `tests/` directory next to your app code. Create `tests/conftest.py`:

```python
"""Shared pytest fixtures for the Flask blog tests."""
from __future__ import annotations

import pytest
from flask import Flask

# Adjust the import below to match where your `create_app` lives.
# If your Week 9 project does not yet have an app factory, refactor it
# so it does — this is a common Flask pattern and the first
# "make it testable" change you will make this week.
from blog import create_app


@pytest.fixture
def app() -> Flask:
    """A Flask app configured for tests (in-memory DB, TESTING=True)."""
    flask_app = create_app(
        {
            "TESTING": True,
            "DATABASE": ":memory:",
            "SECRET_KEY": "test-secret",
        }
    )
    return flask_app


@pytest.fixture
def client(app: Flask):
    """A Flask test client bound to the test app."""
    return app.test_client()
```

If your Week 9 project does not have a `create_app` factory yet, **introduce one**. Move global `app = Flask(__name__)` initialisation into a function that takes a config dict and returns the configured app. This is the single biggest improvement you can make for testability.

---

## What to write

### Required tests

1. **`GET /` returns 200 and the page title appears.**

   ```python
   def test_index_returns_200(client) -> None:
       response = client.get("/")
       assert response.status_code == 200
       assert b"My Blog" in response.data
   ```

2. **`GET /posts/<id>` returns 200 for an existing post.**

3. **`GET /posts/9999` returns 404 for a non-existent post.**

4. **`POST /posts` creates a post.** Assert that:
   - The response is a redirect (`302`) **or** `201`, depending on your design.
   - A `GET /` after the create shows the new title.

5. **`POST /posts` with missing fields returns 400.**

6. **`DELETE /posts/<id>` (or the `POST /posts/<id>/delete` form route) removes the post.**

7. **Authentication, if your app has it.** A protected route returns 401 or redirects to the login page when not logged in.

### Stretch tests

- Use the `caplog` fixture to assert that a warning is logged when a 404 happens.
- Parametrize one test across multiple paths (`/`, `/about`, `/posts/1`) — all should return 200.
- Add a fixture `seeded_app` that pre-populates 3 posts before each test.

---

## Deliverables

1. The full `tests/` directory with at least the 6 required tests.
2. A `conftest.py` with the `app` and `client` fixtures.
3. A `pyproject.toml` (or `pytest.ini`) that points `testpaths` at `tests`.
4. A `README.md` with:
   - How to run the tests.
   - One paragraph on what you changed in the Week 9 code to make it testable.
   - A screenshot or paste of the `pytest -v` output.
5. `pytest --cov=blog --cov-report=term-missing` shows ≥ 80 % coverage on your routes module.
6. A GitHub Actions workflow at `.github/workflows/ci.yml` that runs the tests on push.

---

## Rubric

| Criterion                                  | Points |
|--------------------------------------------|--------|
| App factory + test fixtures in `conftest`  | 3      |
| All 6 required tests pass                  | 4      |
| ≥ 80 % coverage on the routes module       | 1      |
| GitHub Actions workflow green              | 2      |
| **Total**                                  | **10** |

---

## Hints

- `client.get`, `client.post`, `client.delete` all return a `Response` you can inspect with `.status_code`, `.data`, `.headers`, `.json`.
- `follow_redirects=True` lets you chase a redirect in one call: `client.post("/posts", data={...}, follow_redirects=True)`.
- For SQLite in tests, use `":memory:"` so each test gets a fresh database.
- If a test mysteriously hangs, your view is probably waiting for input — check for `input()` or unclosed file handles.

Cite:

- Flask testing docs — <https://flask.palletsprojects.com/en/latest/testing/>
- Flask `test_client` — <https://flask.palletsprojects.com/en/latest/api/#flask.Flask.test_client>
