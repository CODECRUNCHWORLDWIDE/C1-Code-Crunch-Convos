"""Tests for the app factory itself.

The factory is the change that made this project testable, so it gets its own
tests rather than being covered only as a side effect of the route tests.
"""

from __future__ import annotations

from blog import create_app


def test_factory_works_with_no_config() -> None:
    """``create_app()`` with no arguments must still produce a usable app."""
    app = create_app()
    try:
        assert app.config["DATABASE"] == ":memory:"
        assert app.config["TESTING"] is False
        assert app.test_client().get("/").status_code == 200
    finally:
        app.extensions["blog_db"].close()


def test_config_overrides_the_defaults() -> None:
    app = create_app({"TESTING": True, "SECRET_KEY": "override-me"})
    try:
        assert app.config["TESTING"] is True
        assert app.config["SECRET_KEY"] == "override-me"
        assert app.config["ADMIN_PASSWORD"] == "letmein", "untouched keys keep their default"
    finally:
        app.extensions["blog_db"].close()


def test_two_apps_do_not_share_a_database() -> None:
    """The whole point of the factory, in one assertion."""
    first = create_app({"TESTING": True})
    second = create_app({"TESTING": True})
    try:
        first.test_client().post("/posts", data={"title": "Only in first", "body": "b"})

        assert b"Only in first" in first.test_client().get("/").data
        assert b"Only in first" not in second.test_client().get("/").data
    finally:
        first.extensions["blog_db"].close()
        second.extensions["blog_db"].close()
