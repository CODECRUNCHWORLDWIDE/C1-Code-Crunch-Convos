# Mini-Project — Library Management System

> **Estimated time:** 6–8 hours. **Difficulty:** medium.
> Combines OOP (Week 7) with file I/O and JSON (Week 6).

You will build a small **library management system** that tracks books,
members, and loans. The system can save and load its entire state to a JSON
file, so members and their borrowed books survive a program restart.

This is the kind of project that, done well, looks great in a beginner
portfolio. It exercises every concept from this week.

---

## What you are building

A command-line library application with three core classes:

- `Book` — title, author, ISBN, total copies, and how many are currently
  loaned out.
- `Member` — name, member id, and a list of currently borrowed books with
  due dates.
- `Library` — top-level container. Holds books and members; offers methods
  to register members, add books, borrow, return, look up overdue items,
  and save/load to a JSON file.

A user-facing `main.py` drives a tiny menu loop so you can manually test it.

---

## Functional requirements

### `Book`

- Fields: `title: str`, `author: str`, `isbn: str`, `copies_total: int`.
- Internal field for the count currently loaned out.
- A `@property` `copies_available` derived from the two.
- Methods `loan_one()` and `return_one()` that mutate the loaned count and
  raise `ValueError` on under/overflow.
- `__str__` for friendly display; `__repr__` for debugging.
- A `@classmethod` `from_dict(data)` and an instance method `to_dict()` for
  JSON round-tripping.

### `Member`

- Fields: `name: str`, `member_id: str`.
- A list of currently loaned items. Suggested shape: `list[Loan]`, where
  `Loan` is a small `@dataclass` holding `isbn: str` and
  `due_date: date`. Alternatively use a list of dicts — your call.
- Methods to add and remove a `Loan`.
- `to_dict()` / `from_dict()` like `Book`.

### `Library`

- Fields: `books: dict[str, Book]` keyed by ISBN, and
  `members: dict[str, Member]` keyed by `member_id`.
- Methods:
  - `add_book(book: Book) -> None`
  - `register_member(member: Member) -> None`
  - `borrow(member_id: str, isbn: str, days: int = 14) -> Loan`
    - Raises `ValueError` if the member or book is unknown.
    - Raises `ValueError` if no copies are available.
    - Decrements `Book.copies_available` and appends a `Loan` to the
      member.
  - `return_book(member_id: str, isbn: str) -> None`
  - `overdue_loans(today: date | None = None) -> list[tuple[Member, Loan]]`
    — returns every (member, loan) pair whose `due_date` is before `today`
    (default: `date.today()`).
  - `save(path: str | Path) -> None` — write the library to JSON.
  - `@classmethod load(path: str | Path) -> Library` — read it back.

### `main.py`

A simple REPL that lets a tester:

1. Add a book.
2. Register a member.
3. Borrow / return a book.
4. List overdue loans.
5. Save / load.
6. Quit.

The menu is not graded for style — only that it exercises the library.

---

## Class design hints

- Use `@dataclass` wherever you can. `Book`, `Member`, and `Loan` are
  excellent candidates. `Library` is the only one where you might prefer
  a hand-written class because it owns the dictionaries.
- **Composition** is the right relationship throughout: `Library` has
  books and members; `Member` has loans. **No inheritance is needed** —
  resist the temptation.
- Validate on the boundary (`__post_init__`, or at the top of methods)
  so internal code can assume valid data.
- Keep JSON serialization in `to_dict` / `from_dict` methods, *not*
  scattered across the rest of the code.
- `date` values can be stored as ISO strings (`d.isoformat()`) in JSON
  and parsed back with `date.fromisoformat(s)`.
- Use `pathlib.Path` for file paths.

A reasonable rough sketch:

```
Library
├── books: dict[str, Book]       # composition
├── members: dict[str, Member]   # composition
└── methods that orchestrate the two

Member
├── name, member_id
└── loans: list[Loan]            # composition

Loan (frozen dataclass)
├── isbn, due_date

Book
├── title, author, isbn, copies_total
├── _copies_loaned (encapsulated)
└── @property copies_available
```

---

## Starter files

A skeleton is provided in `starter/`. You may copy it into a new folder
(e.g. `solution/`) and fill it in there. The skeleton is **runnable** —
it prints help text and a TODO list. Each `TODO` is intentionally small.

```
starter/
├── book.py         # Book class skeleton
├── member.py       # Member and Loan skeletons
├── library.py      # Library class skeleton + save/load
└── main.py         # tiny REPL
```

---

## Grading rubric (out of 100)

| Area                                | Points |
|-------------------------------------|-------:|
| `Book` class correct                |   15   |
| `Member` + `Loan` correct           |   15   |
| `Library` core operations correct   |   20   |
| Overdue detection works             |   10   |
| JSON save/load round-trips cleanly  |   15   |
| Type hints everywhere               |    5   |
| Validation errors are clear         |    5   |
| `main.py` exercises every feature   |    5   |
| Code style (PEP 8, naming, docs)    |   10   |

A 70 is "passing"; a 90+ is portfolio-worthy.

---

## Stretch goals

- Add a `Librarian(Member)` subclass that has the extra method
  `register_member(other_member)` (delegates to the Library).
- Add a `search(query: str) -> list[Book]` method that finds books by
  partial title or author match.
- Add fines: a fine of $0.25 per overdue day, computed in
  `overdue_loans`.
- Add a tiny `pytest` suite that exercises borrowing, overdue detection,
  and save/load.
- Replace the REPL with a CLI using `argparse`.

---

## Submitting

Place your finished project under
`week-07-mini-project/` in your fork of the bootcamp. Include a short
`README.md` that lists any design choices you made (especially anything
that differs from the rubric) and how to run it.

Good luck.
