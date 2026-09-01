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
