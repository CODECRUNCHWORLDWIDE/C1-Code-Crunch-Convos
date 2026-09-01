"""A thin command-line front end. Argument parsing and printing only.

There is not one `execute` in this file. Every command translates arguments
into a repository call and formats what comes back. If you ever need to put
this behind a web app instead, this is the only file you throw away.

    python -m library.cli --help
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import date

from . import repository as repo
from .db import init_db
from .models import LibraryError


def iso_date(raw: str) -> str:
    try:
        date.fromisoformat(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected ISO-8601 YYYY-MM-DD, got {raw!r}")
    return raw


def positive_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a whole number, got {raw!r}")
    if value < 0:
        raise argparse.ArgumentTypeError("must be zero or more")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="library",
        description="A library management system backed by SQLite.",
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    p = sub.add_parser("add-book", help="add a catalogue entry")
    p.add_argument("title")
    p.add_argument("author")
    p.add_argument("--isbn", default=None)
    p.add_argument("--copies", type=positive_int, default=1)

    p = sub.add_parser("add-member", help="register a member")
    p.add_argument("name")
    p.add_argument("email")

    p = sub.add_parser("borrow", help="borrow a copy of a book")
    p.add_argument("book_id", type=int)
    p.add_argument("member_id", type=int)
    p.add_argument("--due", type=iso_date, default=None, metavar="YYYY-MM-DD")

    p = sub.add_parser("return", help="return a loan (and fulfil the next reservation)")
    p.add_argument("loan_id", type=int)
    p.add_argument("--on", type=iso_date, default=None, metavar="YYYY-MM-DD")

    sub.add_parser("members", help="every member and what they have out")

    p = sub.add_parser("popular", help="most-borrowed books for one month")
    p.add_argument("--month", default=None, metavar="YYYY-MM")
    p.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("reserve", help="join the queue for a book")
    p.add_argument("book_id", type=int)
    p.add_argument("member_id", type=int)

    p = sub.add_parser("overdue", help="active loans past their due date, with fees")
    p.add_argument("--as-of", type=iso_date, default=None, metavar="YYYY-MM-DD")
    p.add_argument("--fee", type=float, default=repo.DEFAULT_FEE_PER_DAY)

    p = sub.add_parser("available", help="how many copies of a book are on the shelf")
    p.add_argument("book_id", type=int)

    p = sub.add_parser("explain", help="show the query plan for the availability query")
    p.add_argument("book_id", type=int)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    init_db()

    try:
        return _dispatch(args)
    except LibraryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def _dispatch(args: argparse.Namespace) -> int:
    if args.command == "add-book":
        book_id = repo.add_book(args.title, args.author, args.isbn, args.copies)
        plural = "copy" if args.copies == 1 else "copies"
        print(f"Added book {book_id}: {args.title} ({args.copies} {plural})")
        return 0

    if args.command == "add-member":
        member_id = repo.register_member(args.name, args.email)
        print(f"Registered member {member_id}: {args.name}")
        return 0

    if args.command == "borrow":
        loan_id = repo.borrow_book(args.book_id, args.member_id, args.due)
        book = repo.get_book(args.book_id)
        member = repo.get_member(args.member_id)
        print(f"Loan {loan_id}: {member.name} borrowed {book.title!r}")
        return 0

    if args.command == "return":
        loan, new_loan_id = repo.return_book_and_fulfil(args.loan_id, args.on)
        book = repo.get_book(loan.book_id)
        print(f"Loan {loan.id}: {book.title!r} returned on {loan.returned_on}")
        if new_loan_id is not None:
            new_loan = repo.get_loan(new_loan_id)
            new_member = repo.get_member(new_loan.member_id)
            print(f"  Reservation fulfilled -> loan {new_loan_id} for {new_member.name}")
        return 0

    if args.command == "members":
        for entry in repo.members_with_loans():
            titles = ", ".join(entry.titles) if entry.titles else "(nothing out)"
            print(f"{entry.member_id:>3}  {entry.name:<20}  {titles}")
        return 0

    if args.command == "popular":
        rows = repo.most_popular_this_month(args.month, args.limit)
        if not rows:
            print("No loans in that month.")
            return 0
        print(f"{'Borrows':>7}  Title")
        for row in rows:
            print(f"{row.times_borrowed:>7}  {row.title} - {row.author}")
        return 0

    if args.command == "reserve":
        reservation_id = repo.place_reservation(args.book_id, args.member_id)
        print(f"Reservation {reservation_id} placed.")
        return 0

    if args.command == "overdue":
        rows = repo.overdue_loans(args.as_of, args.fee)
        if not rows:
            print("Nothing overdue. Remarkable.")
            return 0
        print(f"{'Loan':>4}  {'Days':>4}  {'Fee':>6}  Member / Title")
        for row in rows:
            print(f"{row.loan_id:>4}  {row.days_overdue:>4}  {row.fee:>6.2f}  "
                  f"{row.member_name} / {row.title}")
        return 0

    if args.command == "available":
        print(repo.available_copies(args.book_id))
        return 0

    if args.command == "explain":
        for line in repo.explain_availability(args.book_id):
            print(line)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
