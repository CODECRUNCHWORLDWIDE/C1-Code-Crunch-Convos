"""Application factory for the Week 9 blog, made testable.

The Week 9 app created its ``Flask`` object at import time::

    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

That single line is what makes the app hard to test. There is exactly one app,
it is built the moment anything imports the module, and its configuration comes
from the environment rather than from the caller. A test cannot ask for a
*different* app with a throwaway database, because there is no seam to ask
through.

:func:`create_app` is that seam. It takes a config mapping, applies it over the
defaults, wires up storage and blueprints, and hands back a fresh app. Every
test gets its own app object and its own in-memory SQLite database, so no test
can leak state into the next one.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from flask import Flask

from blog import auth, db, views

__all__ = ["create_app"]

DEFAULT_CONFIG: dict[str, Any] = {
    # ":memory:" is also the production-unfriendly default on purpose: an
    # unconfigured app is obviously a scratch app, not a silently broken one.
    "DATABASE": ":memory:",
    "SECRET_KEY": "dev-only-change-me",
    "ADMIN_PASSWORD": "letmein",
}


def create_app(config: Mapping[str, Any] | None = None) -> Flask:
    """Build and return a configured :class:`~flask.Flask` application.

    Args:
        config: Overrides applied on top of :data:`DEFAULT_CONFIG`. Tests pass
            ``{"TESTING": True, "DATABASE": ":memory:", "SECRET_KEY": ...}``.
    """
    app = Flask(__name__)
    app.config.from_mapping(DEFAULT_CONFIG)
    if config is not None:
        app.config.from_mapping(config)

    db.init_app(app)

    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)
    app.register_error_handler(404, views.page_not_found)

    return app
