"""Exercise 05 — Same idea as Exercise 1, but with the SQLAlchemy ORM.

Goal
----
Reimplement Exercise 1 (create a `books` table, insert three rows, then
read and print them) using the SQLAlchemy ORM. Compare the two scripts
side by side; notice that you write *no* raw SQL.

Setup
-----
    pip install sqlalchemy

Run it
------
    python exercise-05-sqlalchemy-basic.py

Docs
----
SQLAlchemy ORM Quick Start: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
"""

from __future__ import annotations

from typing import Final

from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DB_URL: Final[str] = "sqlite:///exercise-05.db"


class Base(DeclarativeBase):
    """Shared base class for all ORM models in this script."""


class Book(Base):
    """One row in the `books` table = one `Book` Python object."""

    __tablename__ = "books"

    id:     Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title:  Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year:   Mapped[int | None] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r} author={self.author!r} year={self.year}>"


def reset_schema(engine) -> None:  # type: ignore[no-untyped-def]
    """Drop and recreate every table the Base knows about.

    Doing this each run keeps the exercise idempotent — no duplicate rows
    pile up if you run the script multiple times.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_books(session: Session) -> None:
    session.add_all([
        Book(title="The Pragmatic Programmer", author="Hunt & Thomas", year=1999),
        Book(title="Code Complete",            author="Steve McConnell", year=2004),
        Book(title="Clean Code",               author="Robert Martin",  year=2008),
    ])
    session.commit()


def list_books(session: Session) -> list[Book]:
    """Query every book, ordered by id, using the ORM's `select`."""
    stmt = select(Book).order_by(Book.id)
    return list(session.scalars(stmt))


def main() -> None:
    # `echo=True` would log the generated SQL — turn it on if you're curious.
    engine = create_engine(DB_URL, echo=False)
    reset_schema(engine)

    with Session(engine) as session:
        insert_books(session)

    with Session(engine) as session:
        books = list_books(session)
        print(f"Found {len(books)} books via the SQLAlchemy ORM:")
        for book in books:
            print(f"  [{book.id:>3}] {book.title!r} by {book.author} ({book.year})")


if __name__ == "__main__":
    main()
