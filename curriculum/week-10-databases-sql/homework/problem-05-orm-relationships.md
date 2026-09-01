# Homework Problem 5 — ORM Relationships (One-to-Many)

> **Topic:** modelling "one author has many posts" as Python objects, and letting SQLAlchemy write the SQL
> **Lecture:** [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md) (the ORM sections)
> **Difficulty:** Intermediate
> **Target time:** 45 minutes
> **Why this one:** so far you have written SQL by hand. An ORM — Object-Relational Mapper — lets you describe your tables as Python classes and get objects back instead of tuples, so `author.posts` is just a list. This problem is where a foreign key stops being a column you remember to fill in and becomes a relationship the library manages for you. That shift is how most professional Python talks to a database.

## The Brief

You are modelling a blog with two kinds of thing: **authors** and
**posts**. An author writes many posts; each post has exactly one author.
That is a **one-to-many relationship**, the most common shape in all of
data modelling, and this problem is about expressing it cleanly.

In raw SQL you would make a `posts.author_id` foreign key and write a
`JOIN` every time you wanted an author with their posts. An **ORM** lets
you say it once, in the class definitions, and then just write
`author.posts` to get a list of `Post` objects, or `post.author` to get
the `Author` object back. SQLAlchemy — the standard Python ORM — turns
those attribute accesses into the joins for you.

You will write two things:

- **The models.** A `Base`, an `Author`, and a `Post` class, using
  SQLAlchemy's modern `Mapped` / `mapped_column` typed style. The `Post`
  has a `ForeignKey` to the author, and both sides declare a
  `relationship` so the link works in both directions.
- **The demo.** Open an in-memory database, create the tables, insert two
  authors and five posts spread across them, and answer two questions
  *through the ORM* — no raw SQL strings: each author with their post
  count, and every title by the most prolific author.

## Starter

Save this as `models.py` and fill in the `TODO`s. It needs SQLAlchemy —
`pip install sqlalchemy` — and runs as pasted once you fill the classes
in, printing nothing until the demo is written.

```python
"""A blog modelled with the SQLAlchemy ORM: authors have many posts."""

from sqlalchemy import ForeignKey, Integer, String, create_engine, func, select
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, Session, mapped_column, relationship,
)


class Base(DeclarativeBase):
    """Common declarative base for both models."""


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    # TODO: posts: Mapped[list["Post"]] = relationship(back_populates="author", ...)


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # TODO: author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), ...)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    # TODO: author: Mapped[Author] = relationship(back_populates="posts")


def main() -> None:
    engine = create_engine("sqlite://", echo=False)   # in-memory
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        # TODO: create two authors and five posts, attach posts through
        #       author.posts, add_all, commit
        # TODO: query each author with a post count (select + func.count + group_by)
        # TODO: find the most prolific author and print their post titles
        pass
    engine.dispose()


if __name__ == "__main__":
    main()
```

## Requirements

1. `Author` and `Post` use `Mapped` / `mapped_column` typing, not the old
   `Column(...)` style.
2. `Post` has an `author_id` column that is a `ForeignKey("authors.id")`
   and is `NOT NULL`.
3. Both classes declare a `relationship` with `back_populates`, so
   `author.posts` and `post.author` both work and stay in sync.
4. The demo opens an in-memory database (`sqlite://`), creates the tables,
   and inserts at least two authors and at least five posts across them —
   attaching posts through the relationship, never setting `author_id` by
   hand.
5. It prints each author with their post count, and the titles of every
   post by the most prolific author.
6. Every query is an ORM query (`select(...)`) — no raw SQL strings.

## Constraints

- **Attach posts through the relationship, not by setting `author_id`.**
  Writing `ada.posts = [Post(title=...), ...]` lets SQLAlchemy fill in the
  foreign key when it flushes. Setting `author_id = 1` by hand means
  guessing the id before the author has one, and it bypasses the
  relationship that keeps both sides consistent.
- **Count in the database with `func.count`, not in Python.** The "posts
  per author" answer is a `GROUP BY` with `COUNT(*)`, expressed as
  `select(Author.name, func.count(Post.id)).join(...).group_by(...)`.
  Pulling every post into Python and counting in a loop gives the right
  answer for five posts and falls over at five million — the same lesson
  as every other problem this week, now through the ORM.
- **No raw SQL strings.** The whole point of the exercise is to express
  the joins and the grouping as ORM constructs. If you find yourself
  writing `session.execute("SELECT ...")` with a string, you have dropped
  out of the ORM and lost the thing being practised.
- **In-memory database, so it leaves nothing behind.** `sqlite://` with
  no path is a database that lives entirely in RAM and vanishes when the
  engine is disposed. Perfect for a demo — no file to clean up, no state
  to carry between runs.

## Expected output

```text
Authors:
  Ada Lovelace (3 posts)
  Alan Turing  (2 posts)

Most prolific: Ada Lovelace
  - Notes on the Analytical Engine
  - On Bernoulli numbers
  - Reflections on the difference engine
```

## Steps

1. `pip install sqlalchemy`, then fill in the two `relationship` lines and
   the `ForeignKey`. Run the file; with an empty demo it prints nothing,
   but any typo in the models raises immediately at `create_all`.
2. Write the seed: two `Author`s, and assign each a list of `Post`s
   through `author.posts`. `add_all([ada, alan])`, then `commit()`.
3. Write the counts query with `select`, `func.count`, `join`, and
   `group_by`. Print each author and count.
4. Write the "most prolific" query — the same shape with
   `order_by(...desc()).limit(1)` — and print that author's post titles.
5. Compare with the Expected output, character for character.

## The Solution

```python
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
```

<!--@@INSERT:problem-05-orm-relationships-solution.py@@-->

**Why it works.**

**The relationship is the foreign key, seen from Python.** In the
database there is one link: `posts.author_id` points at `authors.id`. In
the models that single link shows up as two attributes —
`Author.posts` and `Post.author` — tied together by `back_populates`.
When you do `ada.posts = [Post(...), Post(...)]`, SQLAlchemy knows those
posts belong to Ada, and when it writes them to the database it fills in
each `author_id` for you. You never typed a foreign key value; you
expressed a relationship and let the library do the bookkeeping.

**`Mapped` / `mapped_column` is the modern, typed way to declare a
column.** `id: Mapped[int] = mapped_column(Integer, primary_key=True)`
tells both SQLAlchemy *and* your type checker that `author.id` is an
`int`. The older `id = Column(Integer, ...)` style still works, but the
typed form means your editor autocompletes `author.name` and catches
`author.nme` before you run anything.

**The counts come from one grouped query, run in the database.**
`select(Author.name, func.count(Post.id)).join(Post, ...).group_by(
Author.id)` is a `GROUP BY` written in Python objects. SQLAlchemy
compiles it to real SQL and SQLite does the counting. The result is a
list of `(name, count)` tuples — the totals arrive already computed, not
as a pile of rows for Python to tally.

**"Most prolific" is the same query with `limit(1)`.** Order the grouped
result by count descending, take one, and you have the top author as a
real `Author` object — which means `star.posts` is right there, a list of
`Post` objects, no second query to write. That is the ORM paying off: the
relationship you declared once turns a "now go fetch their posts" into an
attribute access.

**The tie-break keeps the output stable.** Both `order_by` clauses end
with `Author.name` after the count, so when two authors have the same
number of posts the result is still deterministic instead of depending on
insertion order. Small detail, but it is why the Expected output is a
fact and not a coin flip.

## Download and run

Download [problem-05-orm-relationships-solution.py](./problem-05-orm-relationships-solution.py),
install SQLAlchemy, and run it:

```bash
pip install sqlalchemy
python problem-05-orm-relationships-solution.py
```

It builds the schema in an in-memory database, seeds two authors and five
posts, and answers both questions through ORM queries. The database lives
in RAM and vanishes when the engine is disposed, so nothing is written to
disk.

(This is the one homework problem that needs a third-party package, so it
is also the one you cannot run in the browser sandbox — it wants a real
`pip install`.)

## Common bugs to catch

- **`sqlalchemy.exc.ArgumentError: Mapper ... could not assemble any
  primary key columns`.** You forgot `primary_key=True` on `id`. Every
  mapped class needs a primary key.
- **`sqlalchemy.exc.NoForeignKeysError` / relationship cannot determine
  join.** The `relationship` has no `ForeignKey` to follow. `Post` needs
  `author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))` —
  the relationship rides on top of that column, it does not replace it.
- **`back_populates` names mismatched.** `Author.posts` says
  `back_populates="author"` and `Post.author` says
  `back_populates="posts"` — each names the attribute *on the other
  class*. Swap them and SQLAlchemy raises a mapping error at import.
- **Setting `author_id` by hand and getting `None`.** You wrote
  `Post(title=..., author_id=ada.id)` before committing Ada, so her `id`
  was still `None`. Attach through `ada.posts` and the id is filled in at
  flush time, after Ada exists.
- **Counting in Python.** `len(author.posts)` in a loop works for five
  posts but issues a query per author and moves the work out of the
  database. `func.count` in one grouped query is the shape that scales.

## Under the hood

<details>
<summary>Under the hood — what the ORM is really doing when you touch author.posts</summary>

`author.posts` looks like a plain attribute, but the first time you read
it SQLAlchemy may quietly run a `SELECT * FROM posts WHERE author_id = ?`
to fill it in. This is **lazy loading**, and it is the ORM's greatest
convenience and its most famous performance trap.

The trap has a name: the **N+1 query problem**. Loop over ten authors and
read `author.posts` inside the loop, and you have run one query for the
authors plus one query for *each* author's posts — eleven queries where
one join would have done. It gives the right answer, so it passes every
test, and then it makes the page slow in production when there are ten
thousand authors.

The reference solution sidesteps it by asking the database the aggregate
question directly — `func.count` in a grouped query — instead of loading
every post into Python and counting. When it *does* touch `star.posts`,
it is for a single author, so it is one extra query, not N.

SQLAlchemy gives you tools to control this: `selectinload` and
`joinedload` fetch the related rows up front in one go, turning N+1 back
into 2 (or 1). The lesson for now is just to know the machinery is there.
`author.posts` is not free — it is a query wearing an attribute's
clothes, and knowing that is the difference between an ORM helping you and
an ORM surprising you.

</details>

<details>
<summary>Under the hood — Core vs ORM, and when you would drop down to raw SQL</summary>

SQLAlchemy is really two libraries stacked. **Core** is a Python way to
build SQL — `select(...)`, `join(...)`, `where(...)` — that returns rows.
The **ORM** sits on top and maps those rows onto your `Author` and `Post`
objects, tracking which ones changed so it can write them back. This
problem uses the ORM, but the `select(...)` statements are Core
constructs the ORM understands.

Why have both? Because they are good at different jobs. The ORM shines
when you are working with *objects* — load an author, change a field,
commit, and it writes the update for you. Core (or raw SQL) shines when
you are working with *sets* — a bulk update of a million rows, a
reporting query with three levels of subquery, a database-specific
feature the ORM does not model. Reaching for raw SQL is not a failure;
it is picking the right altitude.

The rule of thumb professionals use: **ORM by default, drop to Core or
SQL for the queries that are about data rather than objects.** A blog's
"show me this author and their posts" is an object job — ORM. A
dashboard's "revenue by region by month, year over year" is a set job —
Core or a hand-written query. Knowing that both exist, and that you can
mix them in one program, is what keeps you from forcing every problem
through the one tool you happen to know.

</details>

## Acceptance checklist

- [ ] `Author` and `Post` use `Mapped` / `mapped_column`.
- [ ] `Post.author_id` is a `NOT NULL` `ForeignKey("authors.id")`.
- [ ] Both sides declare a `relationship` with matching `back_populates`.
- [ ] The demo uses an in-memory database and disposes the engine.
- [ ] Posts are attached through `author.posts`, not by setting `author_id`.
- [ ] Counts come from a `func.count` grouped query, not a Python loop.
- [ ] The output matches the Expected output exactly.

## Stretch

- **Make it many-to-many.** Add a `Tag` model and an association table so
  a post can have many tags and a tag many posts. This is the ORM version
  of Problem 1's `product_categories` junction — notice SQLAlchemy manages
  the join table for you.
- **Add `cascade="all, delete-orphan"`** (the reference already has it)
  and prove it: delete an author, then query posts and confirm theirs are
  gone. Then remove the cascade and watch the delete fail with a foreign-
  key violation instead. That contrast is what the cascade *is*.
- **Fix an N+1 by hand.** Load all authors, loop, and read `.posts` inside
  the loop with SQL echo on (`echo=True`) — count the queries. Then add
  `selectinload(Author.posts)` and count again.
- **Add a `published` boolean and a query** for "authors with at least one
  published post", using `.where(...)` and `.having(...)`. Feel where the
  ORM makes it pleasant and where it makes you look up syntax.

Next: [Problem 6 — Backup and Restore Script](./problem-06-backup-restore.md),
the safe way to snapshot a database that might be in use.
