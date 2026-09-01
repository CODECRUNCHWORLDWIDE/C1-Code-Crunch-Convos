"""Shared pytest fixtures for the Flask blog tests.

Four fixtures, each one layer on top of the last:

    app  ->  client
     |
     +----->  seeded_app  ->  seeded_client
     |
     +----->  admin_client

``seeded_app`` returns *the same object* as ``app``, so a test may depend on
both ``client`` and ``seeded_app`` and still be talking to one application with
one database. That is deliberate: two apps in one test is the single most
confusing bug in a Flask suite, and the fixture graph should make it impossible
rather than merely unlikely.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from blog import create_app, db

ADMIN_PASSWORD = "test-password"


@pytest.fixture
def admin_password() -> str:
    """The password the test app accepts.

    Exposed as a fixture rather than imported from this file, because
    ``from tests.conftest import ADMIN_PASSWORD`` only works if ``tests/`` is
    an importable package — and whether it is depends on ``pythonpath`` and on
    whether an ``__init__.py`` exists. A fixture always works.
    """
    return ADMIN_PASSWORD


@pytest.fixture
def app() -> Iterator[Flask]:
    """A Flask app configured for tests (in-memory DB, TESTING=True)."""
    flask_app = create_app(
        {
            "TESTING": True,
            "DATABASE": ":memory:",
            "SECRET_KEY": "test-secret",
            "ADMIN_PASSWORD": ADMIN_PASSWORD,
        }
    )
    yield flask_app
    # The app owns exactly one SQLite connection (see blog/db.py). Closing it
    # here is what actually destroys the in-memory database; without this the
    # connection object survives until garbage collection and the suite slowly
    # accumulates open handles.
    flask_app.extensions["blog_db"].close()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """A Flask test client bound to the test app."""
    return app.test_client()


@pytest.fixture
def seeded_app(app: Flask) -> Flask:
    """The same app, with three posts already in the database.

    Ids are 1, 2, 3 because every test gets a brand-new ``:memory:`` database
    and ``AUTOINCREMENT`` starts over. Tests may rely on that.
    """
    with app.app_context():
        for n in (1, 2, 3):
            db.create_post(f"Seed post {n}", f"Body of seed post {n}.")
    return app


@pytest.fixture
def seeded_client(seeded_app: Flask) -> FlaskClient:
    """A test client for an app that already has three posts."""
    return seeded_app.test_client()


@pytest.fixture
def admin_client(seeded_app: Flask) -> FlaskClient:
    """A logged-in test client for the seeded app.

    The client keeps a cookie jar between calls, so logging in once here is
    enough for every later request the test makes.
    """
    logged_in = seeded_app.test_client()
    response = logged_in.post("/login", data={"password": ADMIN_PASSWORD})
    assert response.status_code == 302, "fixture failed to log in"
    return logged_in
