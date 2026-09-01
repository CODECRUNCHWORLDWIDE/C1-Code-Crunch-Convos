"""problem-05-orm-relationships-solution.py — authors and posts, one-to-many.

The models and the demo the problem asks for, in one runnable file. An
Author has many Posts; a Post belongs to exactly one Author; the two sides
are wired together with ``relationship`` and ``back_populates``, in modern
``Mapped`` / ``mapped_column`` style.

The demo opens an in-memory SQLite database, inserts two authors and five
posts, and answers both questions through ORM queries — each author with a
post count, then every title by the most prolific author. No SQL string
appears anywhere, nothing touches disk.

Run it with::

    pip install sqlalchemy
    python problem-05-orm-relationships-solution.py
"""

from typing import Final

from sqlalchemy import ForeignKey, Integer, String, create_engine, func, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

DB_URL: Final[str] = "sqlite://"   # in-memory


class Base(DeclarativeBase):
    """Common declarative base for both models."""


class Author(Base):
    """One writer, owning any number of posts."""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Author {self.id} {self.name!r}>"


class Post(Base):
    """One article, belonging to exactly one author."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(120), nullable=False)

    author: Mapped[Author] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.id} {self.title!r}>"


def seed(session: Session) -> None:
    """Two authors, five posts — attached through the relationship,
    so no author_id is ever assigned by hand."""
    ada = Author(name="Ada Lovelace")
    alan = Author(name="Alan Turing")
    ada.posts = [
        Post(title="Notes on the Analytical Engine"),
        Post(title="On Bernoulli numbers"),
        Post(title="Reflections on the difference engine"),
    ]
    alan.posts = [
        Post(title="On computable numbers"),
        Post(title="Computing machinery and intelligence"),
    ]
    session.add_all([ada, alan])
    session.commit()


def authors_with_counts(session: Session) -> list[tuple[str, int]]:
    """(name, post count) per author, most posts first — one grouped query."""
    stmt = (
        select(Author.name, func.count(Post.id))
        .join(Post, Post.author_id == Author.id)
        .group_by(Author.id)
        .order_by(func.count(Post.id).desc(), Author.name)
    )
    return [(name, count) for name, count in session.execute(stmt)]


def most_prolific(session: Session) -> Author:
    """The author with the most posts, as a real Author object."""
    stmt = (
        select(Author)
        .join(Post, Post.author_id == Author.id)
        .group_by(Author.id)
        .order_by(func.count(Post.id).desc(), Author.name)
        .limit(1)
    )
    author = session.scalars(stmt).first()
    assert author is not None, "seed() ran, so there is always an author"
    return author


def main() -> None:
    """Create the schema in memory, seed it, and answer the two questions."""
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        seed(session)

        counts = authors_with_counts(session)
        width = max(len(name) for name, _ in counts)
        print("Authors:")
        for name, count in counts:
            noun = "post" if count == 1 else "posts"
            print(f"  {name:<{width}} ({count} {noun})")

        star = most_prolific(session)
        print(f"\nMost prolific: {star.name}")
        for post in sorted(star.posts, key=lambda p: p.title):
            print(f"  - {post.title}")

    engine.dispose()


if __name__ == "__main__":
    main()
