"""Per-request database connections, plus the init-db and seed CLI commands.

The pattern here is the one from the official Flask tutorial, and it is worth
understanding rather than copying: **one connection per request, stored on
`g`, closed when the request ends.**

`g` is Flask's per-request scratch space. It is not a global in the Python
sense -- it is bound to the current application context, which Flask pushes at
the start of a request and pops at the end. Two simultaneous requests get two
different `g` objects and therefore two different connections, which is what
makes this safe. A single module-level connection shared by every request
would not be: `sqlite3` connections are not designed to be used from several
threads at once, and Flask's development server is threaded by default.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import click
from flask import Flask, current_app, g


def get_db() -> sqlite3.Connection:
    """Return this request's connection, opening one on first use.

    Called many times per request (a route, then a template filter, then a
    context processor) and opens exactly one connection, because the second
    call finds it already on `g`.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            # Let sqlite3 parse DECLTYPES/COLNAMES? No -- we store ISO-8601
            # text and read it back as text. Fewer moving parts, and the
            # template formats it.
            detect_types=0,
        )
        g.db.row_factory = sqlite3.Row
        # Without this, ON DELETE CASCADE on comments.post_id does nothing and
        # deleting a post silently orphans its comments.
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(exception: BaseException | None = None) -> None:
    """Close this request's connection, if it opened one."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Drop and recreate every table from schema.sql."""
    db = get_db()
    schema = (Path(current_app.root_path) / "schema.sql").read_text(encoding="utf-8")
    db.executescript(schema)
    db.commit()


def seed_db() -> dict[str, Any]:
    """Load sample data. Returns the demo credentials so the CLI can print them.

    Imported here rather than at module scope to keep the import graph acyclic:
    seed imports db, db only needs seed when the command actually runs.
    """
    from seed import load_sample_data

    return load_sample_data(get_db())


@click.command("init-db")
def init_db_command() -> None:
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("seed")
def seed_command() -> None:
    """Drop, recreate and populate the database with sample data."""
    init_db()
    info = seed_db()
    click.echo("Seeded the database.")
    click.echo(f"  users:    {info['users']}")
    click.echo(f"  posts:    {info['posts']}")
    click.echo(f"  comments: {info['comments']}")
    click.echo("Log in with any of:")
    for username, password in info["credentials"]:
        click.echo(f"  {username} / {password}")


def init_app(app: Flask) -> None:
    """Wire the teardown hook and the CLI commands into an application."""
    # teardown_appcontext runs after every request, whether it succeeded or
    # raised. That is what guarantees the connection is closed even when a
    # view blows up with a 500.
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_command)
