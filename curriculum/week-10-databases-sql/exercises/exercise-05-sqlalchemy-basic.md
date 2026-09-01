# Exercise 5 — The Same Table with SQLAlchemy

> **Topic:** Rebuild Exercise 1 with the SQLAlchemy ORM — a mapped class, a `Session`, and a `select()` with no SQL string in sight
> **Lecture:** [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md), sections 8–10
> **Difficulty:** Medium
> **Target time:** 35 minutes
> **Why this one:** almost every Python job that touches a database touches SQLAlchemy, and the fastest way to understand an ORM is to point it at a problem you have already solved by hand. You know exactly what SQL the roaster catalogue needs, so when the ORM produces something different you will notice. Doing this last, rather than first, is what keeps the ORM a convenience instead of a mystery.

## The Brief

Same coffee roaster, same four roasts, same question: what is in stock,
most expensive first. Byte for byte the same output as Exercise 1.

Everything underneath changes. Instead of a `CREATE TABLE` string you write
a Python class and let SQLAlchemy derive the schema from it. Instead of a
cursor and tuples you get a `Session` and objects with attributes. Instead
of `"SELECT ... WHERE in_stock > ?"` you write
`select(Roast).where(Roast.in_stock > 0)`, and what you build is a query
object rather than text.

The payoff to watch for: `Roast.in_stock > 0` is not a Python comparison
and does not evaluate to `True` or `False`. It builds a SQL expression that
renders to `roasts.in_stock > ?` with the zero bound as a parameter —
SQLAlchemy parameterizes everything, always, without being asked. Exercise
2's lesson is built into the tool. This is also the only exercise this week
with an install.

## Starter

Install SQLAlchemy first, then create `exercise-05-sqlalchemy-basic.py`.

```bash
pip install sqlalchemy
```

```python
"""exercise-05-sqlalchemy-basic.py — Exercise 1 again, through the ORM.

Same four roasts, same listing, no SQL strings. Uses SQLAlchemy 2.0 style:
DeclarativeBase, Mapped, mapped_column, Session, select.
"""

from typing import Final

from sqlalchemy import Float, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DB_URL: Final[str] = "sqlite:///roastery_orm.db"

SEED_ROWS: Final[list[tuple[str, str, float, int]]] = [
    ("Sunrise Blend",     "Colombia", 14.50, 12),
    ("Night Shift",       "Ethiopia", 17.25, 5),
    ("Cold Brew Base",    "Brazil",   12.00, 30),
    ("Decaf Quiet Hours", "Peru",     15.75, 0),
]


class Base(DeclarativeBase):
    """Common declarative base for every model in this script."""


class Roast(Base):
    """One coffee in the roaster's catalogue."""

    __tablename__ = "roasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    # TODO: origin        -> Mapped[str],   String(40), not nullable
    # TODO: price_per_bag -> Mapped[float], Float,      not nullable
    # TODO: in_stock      -> Mapped[int],   Integer,    not nullable, default 0

    def __repr__(self) -> str:
        return f"<Roast {self.id} {self.name!r} ${self.price_per_bag:.2f}>"


def seed(session: Session) -> int:
    """Add the seed roasts if the table is empty. Return how many were added."""
    # TODO: if total_count(session) > 0, return 0 — the table is already seeded
    # TODO: build a Roast(...) for each tuple in SEED_ROWS
    # TODO: session.add_all(...), then session.commit()
    return 0


def in_stock(session: Session) -> list[Roast]:
    """Return in-stock roasts, most expensive first."""
    # TODO: stmt = select(Roast).where(Roast.in_stock > 0)
    #                           .order_by(Roast.price_per_bag.desc())
    # TODO: return list(session.scalars(stmt))
    return []


def total_count(session: Session) -> int:
    """Return the number of rows in the roasts table."""
    # TODO: session.scalar(select(func.count()).select_from(Roast))
    return 0


def main() -> None:
    """Create the schema, seed it, and print the in-stock listing."""
    engine = create_engine(DB_URL, echo=False)
    print(f"Engine: {DB_URL}")

    Base.metadata.create_all(engine)
    print("Created table: roasts")

    with Session(engine) as session:
        print(f"Added {seed(session)} roasts.")

        rows = in_stock(session)
        print("\nIn stock, most expensive first:")
        for roast in rows:
            print(
                f"{roast.id:>2}  {roast.name:<18} "
                f"{roast.origin:<10} ${roast.price_per_bag:.2f}"
            )
        print(f"\n{len(rows)} of {total_count(session)} roasts are in stock.")

    print("Session closed.")


if __name__ == "__main__":
    main()
```

## Requirements

1. All four columns are declared with `Mapped[...]` annotations and
   `mapped_column(...)`. The annotation is not decoration — SQLAlchemy 2.0
   reads it to infer nullability and the Python type.
2. `Base.metadata.create_all(engine)` builds the table. You never write
   `CREATE TABLE`.
3. `seed` is idempotent: it returns `4` on a fresh database and `0` on every
   run after that, because `name` is unique and re-adding would raise.
4. `in_stock` returns `Roast` objects — not tuples, not rows — filtered to
   `in_stock > 0` and ordered by `price_per_bag` descending.
5. `session.commit()` is called inside `seed` after `add_all`.
6. The printed output is identical to Exercise 1's, apart from the first and
   last lines. Compare them side by side; that identity is the deliverable.

## Constraints

- **Use the 2.0 declarative style shown here.** Older tutorials use
  `declarative_base()`, `Column(...)`, and `session.query(Roast)`. Those
  still run and are on their way out. `DeclarativeBase`, `mapped_column`,
  and `select()` are the current API, and they are the ones your type
  checker understands.
- **Call `session.commit()`, and let the `with` block close the session.**
  A `Session` holds your new objects in memory until you commit. Leave the
  `with` block without committing and SQLAlchemy rolls the transaction back
  and closes — four objects that were "added", no exception, and an empty
  table on the next run. It is the same silent loss as a missing
  `conn.commit()` in Exercises 1 to 4, wearing different clothes.
- **Do not build a SQL string anywhere.** If you find yourself reaching for
  `session.execute(text("SELECT ..."))` you have opted out of the thing you
  are here to learn. `select(Roast).where(...)` is the exercise.
- **Let the ORM parameterize.** `Roast.in_stock > 0` renders to
  `roasts.in_stock > ?`. You could not inject through it if you tried,
  because there is no string for the value to escape out of. Turn on
  `echo=True` once and read the `?` in the log to prove it to yourself.
- **Count with `func.count()`, not `len(session.scalars(...).all())`.**
  Loading four objects to find out there are four is harmless. Loading four
  million is not, and the shape of the mistake is identical at both sizes.
- **Use a different file from Exercise 1 (`roastery_orm.db`), and keep
  `*.db` in `.gitignore`.** Keeping the two databases apart means you can
  delete either without losing the other, and it proves the ORM built its
  own schema rather than reusing yours.

## Expected output

First run, with no `roastery_orm.db` present:

```text
$ pip install sqlalchemy
$ python exercise-05-sqlalchemy-basic.py
Engine: sqlite:///roastery_orm.db
Created table: roasts
Added 4 roasts.

In stock, most expensive first:
 2  Night Shift        Ethiopia   $17.25
 1  Sunrise Blend      Colombia   $14.50
 3  Cold Brew Base     Brazil     $12.00

3 of 4 roasts are in stock.
Session closed.
```

Second run, same file:

```text
Added 0 roasts.
```

Put this listing next to Exercise 1's. Three lines, same order, same ids,
same prices. Two completely different pieces of code produced the same
three rows, because both of them ended up asking SQLite the same question.

## Steps

1. `pip install sqlalchemy` inside your virtual environment. Confirm it
   landed: `python -c "import sqlalchemy; print(sqlalchemy.__version__)"`
   should print a 2.x version.
2. Create the file and finish the three `TODO` columns on the model. Run it.
   The table is created, nothing is seeded yet, and the listing is empty.
3. Check what SQLAlchemy built for you: `python -m sqlite3 roastery_orm.db`,
   then `.schema roasts`. Compare it to the `SCHEMA` string you wrote by
   hand in Exercise 1 and note every difference.
4. Fill in `total_count`, then `seed`. Run it twice and confirm 4 then 0.
5. Fill in `in_stock`. Compare the three lines to Exercise 1 character for
   character.
6. Set `echo=True` in `create_engine` and run once more. Read the SQL
   SQLAlchemy emitted — the `CREATE TABLE`, the `INSERT`, and the
   `SELECT ... WHERE roasts.in_stock > ?` you would have written yourself.
   Set it back to `False`, delete `roastery_orm.db`, and run clean.

## The Solution

```python
"""exercise-05-sqlalchemy-basic-solution.py — Exercise 1 again, through the ORM.

Same four roasts, same listing, no SQL strings. Uses SQLAlchemy 2.0 style:
DeclarativeBase, Mapped, mapped_column, Session, select.

Your own exercise-05-sqlalchemy-basic.py keeps roastery_orm.db in the folder
you run it from, so you can inspect the schema the ORM built. This shipped
answer runs the same code inside a throwaway temporary folder instead, so
the download never collides with a database of yours and never leaves a file
behind. Every run is therefore a first run: fresh file, four adds. The model
and the three query functions are the whole exercise and know nothing about
the harness.

Run it with::

    pip install sqlalchemy
    python exercise-05-sqlalchemy-basic-solution.py
"""

import os
import tempfile
from pathlib import Path
from typing import Final

from sqlalchemy import Float, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DB_URL: Final[str] = "sqlite:///roastery_orm.db"

SEED_ROWS: Final[list[tuple[str, str, float, int]]] = [
    ("Sunrise Blend",     "Colombia", 14.50, 12),
    ("Night Shift",       "Ethiopia", 17.25, 5),
    ("Cold Brew Base",    "Brazil",   12.00, 30),
    ("Decaf Quiet Hours", "Peru",     15.75, 0),
]


class Base(DeclarativeBase):
    """Common declarative base for every model in this script."""


class Roast(Base):
    """One coffee in the roaster's catalogue."""

    __tablename__ = "roasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    origin: Mapped[str] = mapped_column(String(40), nullable=False)
    price_per_bag: Mapped[float] = mapped_column(Float, nullable=False)
    in_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"<Roast {self.id} {self.name!r} ${self.price_per_bag:.2f}>"


def seed(session: Session) -> int:
    """Add the seed roasts if the table is empty. Return how many were added."""
    if total_count(session) > 0:
        return 0
    roasts = [
        Roast(name=name, origin=origin, price_per_bag=price, in_stock=bags)
        for name, origin, price, bags in SEED_ROWS
    ]
    session.add_all(roasts)
    session.commit()
    return len(roasts)


def in_stock(session: Session) -> list[Roast]:
    """Return in-stock roasts, most expensive first."""
    stmt = (
        select(Roast)
        .where(Roast.in_stock > 0)
        .order_by(Roast.price_per_bag.desc())
    )
    return list(session.scalars(stmt))


def total_count(session: Session) -> int:
    """Return the number of rows in the roasts table."""
    return session.scalar(select(func.count()).select_from(Roast)) or 0


def main() -> None:
    """Create the schema, seed it, and print the in-stock listing."""
    engine = create_engine(DB_URL, echo=False)
    print(f"Engine: {DB_URL}")

    Base.metadata.create_all(engine)
    print("Created table: roasts")

    with Session(engine) as session:
        print(f"Added {seed(session)} roasts.")

        rows = in_stock(session)
        print("\nIn stock, most expensive first:")
        for roast in rows:
            print(
                f"{roast.id:>2}  {roast.name:<18} "
                f"{roast.origin:<10} ${roast.price_per_bag:.2f}"
            )
        print(f"\n{len(rows)} of {total_count(session)} roasts are in stock.")

    print("Session closed.")
    engine.dispose()


def run_in_throwaway_folder() -> None:
    """Run main() inside a temporary folder that is deleted afterwards.

    DB_URL is a relative sqlite:/// URL, so the database lands in the current
    folder. Moving into a temporary folder first means this download builds
    its catalogue and leaves your disk exactly as it found it.
    """
    keep = Path.cwd()
    with tempfile.TemporaryDirectory() as workspace:
        os.chdir(workspace)
        try:
            main()
        finally:
            os.chdir(keep)


if __name__ == "__main__":
    run_in_throwaway_folder()
```

**Why it works.**

**The class *is* the `CREATE TABLE`.** Think of `class Roast(Base)` as a
form you design once. Each `mapped_column` is a box on that form: a name, a
type, and the rules about what may go in it. `Base.metadata.create_all` walks
every form it knows about and builds the matching table in the database. You
never wrote `CREATE TABLE roasts (...)`, and yet the table has exactly the
four columns, the primary key, and the `UNIQUE` on `name` that you asked for
— because you asked for them in Python.

**`Mapped[...]` is the label on the box, and SQLAlchemy reads it.** In most
Python code a type annotation is a note for humans and for your editor.
Here it is load-bearing. `Mapped[str]` tells SQLAlchemy the attribute holds
text; `Mapped[int]` says a whole number. That is why the annotation and the
`mapped_column(...)` have to agree — they are two halves of one sentence,
and the library reads both.

**`Roast.in_stock > 0` does not compare anything.** This is the strangest
and best part. In ordinary Python, `5 > 0` is `True` straight away. But
`Roast.in_stock` is a *class* attribute, and SQLAlchemy has taught it to
answer `>` by building a little description instead of an answer. The
description says "the `in_stock` column, greater than a value I am holding
for you". When `session.scalars` runs it, that description becomes
`roasts.in_stock > ?` with the zero handed over separately. There is no
string for a value to escape out of, so Exercise 2's injection lesson is
simply built into the tool. Turn on `echo=True` once and you will see the
`?` in the log.

**`select` builds the question; `scalars` hands back objects.**
`session.scalars(stmt)` returns `Roast` objects, not tuples — so the print
loop says `roast.name` and `roast.price_per_bag` instead of `row[1]` and
`row[3]`. Same three rows as Exercise 1, but you stopped counting columns.
That is the whole trade an ORM offers: a little machinery underneath, a lot
less finger-counting on top.

**`seed` looks before it writes.** `name` is `unique=True`, so adding the
same four roasts twice would raise an `IntegrityError`. The early return —
"if the table already has rows, add nothing and report `0`" — is what makes
the script safe to run over and over. Idempotent is the word for it: doing
it twice leaves the world exactly as doing it once did.

**The count is done by the database.** `select(func.count()).select_from(Roast)`
asks SQLite for one number and gets one number back. The tempting
alternative — load every roast into a list and call `len` on it — gives the
right answer for four rows and drags four million across the wire when the
catalogue grows. Same mistake at both sizes; only one of them hurts.

**The trailing `or 0` is a promise to the type checker.**
`session.scalar(...)` is allowed to hand back `None`, because in general a
query might match nothing. A `COUNT` never does — it answers `0` — but the
library cannot know that, so `or 0` turns the "maybe a number" into a
number and `total_count` can honestly say it returns an `int`.

**The shipped answer runs in a throwaway folder.** `DB_URL` is
`"sqlite:///roastery_orm.db"` with no folder in front of the filename, so the
database lands wherever you are standing when you run it.
`run_in_throwaway_folder` steps into a temporary directory, calls `main`, and
steps back out so the directory can be deleted. Your own
`exercise-05-sqlalchemy-basic.py` should *not* do this — you want
`roastery_orm.db` left behind so you can open it and read the schema the ORM
built for you.

## Download and run

Download [exercise-05-sqlalchemy-basic-solution.py](./exercise-05-sqlalchemy-basic-solution.py),
install SQLAlchemy, and run it:

```bash
pip install sqlalchemy
python exercise-05-sqlalchemy-basic-solution.py
```

This is the one exercise this week that needs an install. `sqlite3` comes
with Python; SQLAlchemy does not. If the run stops at
`ModuleNotFoundError: No module named 'sqlalchemy'`, the install went to a
different Python than the one running the script — activate your virtual
environment, then run both commands again from inside it.

It creates the table, seeds the four roasts, prints the listing, and takes
its database with it on the way out, so your folder is left exactly as it was
found. Because the temporary folder is new every time, every run is a first
run — which is why the shipped answer always reports `Added 4 roasts.` and
never `Added 0`. Your own file keeps its `roastery_orm.db`, so yours will
report `0` on the second run.

Your own file is `exercise-05-sqlalchemy-basic.py`. The `-solution` suffix is
what keeps the shipped answer from landing on top of it.

## Common bugs to catch

- **`ModuleNotFoundError: No module named 'sqlalchemy'`.** The install went
  to a different interpreter than the one running the script. Activate the
  virtual environment first, then `pip install sqlalchemy`, then run.
- **`sqlalchemy.exc.ArgumentError: Mapper ... could not assemble any primary
  key columns`.** No column is marked `primary_key=True`. Every mapped class
  needs one; the ORM has no way to identify an object without it.
- **`AttributeError: type object 'Roast' has no attribute 'origin'`.** A
  `TODO` column is still a comment, so the class has no such attribute and
  neither does the table.
- **The listing is empty but `Added 4 roasts.` printed.** `seed` never
  called `session.commit()`, or it committed after the `with` block had
  already exited. Nothing raises; the rows simply never left memory.
- **`sqlalchemy.exc.IntegrityError: UNIQUE constraint failed:
  roasts.name`.** `seed` is not idempotent — it added the four roasts again
  on a second run. The early return when `total_count` is non-zero is what
  stops it.
- **`Decaf Quiet Hours` appears in the listing.** Your filter is
  `Roast.in_stock >= 0`, which is true for every row. It is the same
  off-by-one as Exercise 1 and it looks even more innocent in Python syntax.
- **`TypeError: '>' not supported between instances of ...`.** You compared
  an instance attribute (`some_roast.in_stock`) instead of the class
  attribute (`Roast.in_stock`). Only the class attribute builds a SQL
  expression; the instance one is a plain integer.
- **Adding a column to the class changes nothing in the database.**
  `create_all` creates missing tables; it does not alter existing ones.
  Delete the `.db` file, or reach for a migration tool — this is the exact
  gap Alembic exists to fill, from Lecture 3 section 11.

## Acceptance checklist

- [ ] `pip install sqlalchemy` succeeded and the script imports cleanly.
- [ ] All four columns use `Mapped[...]` with `mapped_column(...)`.
- [ ] The listing matches Exercise 1's three lines exactly.
- [ ] Running the script twice reports `Added 0 roasts.` the second time and does not raise.
- [ ] `session.commit()` is called inside `seed`, inside the `with` block.
- [ ] No SQL string appears anywhere in your file.
- [ ] The file is committed to Git with a message like `Add Week 10 exercise 5: SQLAlchemy ORM basics`.

## Stretch

- Add a `roasted_on: Mapped[str]` column, delete the `.db`, rerun, and note
  how little work that was compared to what it would cost with live data in
  the table.
- Reproduce Exercise 4's `GROUP BY` in the ORM:
  `select(Roast.origin, func.sum(Roast.in_stock)).group_by(Roast.origin)`.
  Compare the generated SQL with the query you wrote by hand.
- Write the same catalogue a third time with SQLAlchemy Core (Lecture 3
  section 9) — `Table`, `Column`, `insert`, `select`, no classes — and
  decide for yourself which of the three you would reach for on a
  hundred-line script.

That is the week's drills done. Now build something with them:
[Week 10 Challenges](../challenges/README.md).
