"""The application factory.

    flask --app app init-db      # drop + recreate the schema
    flask --app app seed         # drop + recreate + sample data
    flask --app app run --debug  # serve it

A factory rather than a module-level `app = Flask(__name__)` because the smoke
test needs a *second* application pointed at a throwaway database. With a
factory that is one extra call; with a module-level app it is monkeypatching.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask

import blog
import db as database
from auth import bp as auth_bp

BASE_DIR = Path(__file__).resolve().parent


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        # In production this comes from the environment and is never in git.
        # A blank default would make session cookies forgeable.
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret"),
        DATABASE=os.environ.get("BLOG_DB", str(BASE_DIR / "blog.db")),
    )
    if test_config is not None:
        app.config.update(test_config)

    database.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog.bp)
    # blog.index is registered at "/", so give it the short endpoint name
    # `index` too -- that is what url_for("index") in the templates uses.
    app.add_url_rule("/", endpoint="index")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
