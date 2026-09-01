"""A library management system whose persistence layer is SQLite.

The Week 7 version kept `Book`, `Member` and `Loan` objects in dictionaries and
saved them to JSON. Here the same three concepts are rows in three tables, and
the objects in `models.py` are plain dataclasses that carry a row's data around
after it has been read.

Module map, in the order worth reading them:

- `db.py`         -- connections, PRAGMAs, the transaction context manager.
- `models.py`     -- the dataclasses. No SQL, no behaviour, no surprises.
- `repository.py` -- every SQL statement in the project, in one file.
- `cli.py`        -- argument parsing and printing. No SQL.
"""

from __future__ import annotations

__all__ = ["db", "models", "repository"]
