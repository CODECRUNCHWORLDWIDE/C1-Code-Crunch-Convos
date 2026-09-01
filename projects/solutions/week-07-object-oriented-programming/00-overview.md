# Reference implementation — Week 7 mini-project (library management system)

This folder is the working answer to [Week 7's mini-project](../../../curriculum/week-07-object-oriented-programming/mini-project/README.md). It is a real, runnable program: every transcript in the [mini-project walkthrough](../../../curriculum/week-07-object-oriented-programming/mini-project/README.md) was produced by running exactly these files.

Read the walkthrough for the *why* — architecture, the decisions that were genuinely open, and where people get stuck. This file tells you what is here and how to run it.

---

## What is in the folder

| File | What it is |
|---|---|
| `book.py` | `Book` — a catalogue entry, its copy counts, and its JSON round trip. |
| `member.py` | `Loan` (frozen dataclass) and `Member` — who is holding what, until when. |
| `library.py` | `Library` — owns the two dictionaries, enforces the rules, saves and loads. |
| `librarian.py` | Stretch goal: `Librarian(Member)`, the one honest subclass in the project. |
| `main.py` | The menu REPL, plus `--demo` — a non-interactive run that exercises everything. |
| `test_library.py` | Stretch goal: 13 pytest tests over borrowing, overdue detection and save/load. |

Standard library only. No `pip install` step, no `requirements.txt`, nothing to configure.

---

## How to run it

Python 3.10 or newer — the code uses `X | None` unions and `list[Book]` builtin generics. It was developed and verified on **CPython 3.13.2, Windows 11**.

```bash
cd projects/solutions/week-07-object-oriented-programming
python main.py --demo
```

`--demo` runs a scripted walkthrough with a pinned clock (`date(2026, 3, 1)`), so its output is identical on every machine and every day of the year:

```text
Library(name='Crunch Community Library', books=3, members=0)
members: ['M-001', 'M-002', 'M-003', 'S-100']
loan: 978-1492056355 due 2026-03-15
after two loans: 'Fluent Python' by Luciano Ramalho (0/2 available)
ValueError: no copies of 'Fluent Python' available
ValueError: unknown member id 'M-999'
ValueError: 'Ada Lovelace' already has 978-1491939369 on loan
after rollback: 'Think Python' by Allen B. Downey (2/3 available)
overdue: Alan Turing -> 978-1718502703 due 2026-02-06 (24 days late)
fines: {'M-003': 6.0}
reloaded: Library(name='Crunch Community Library', books=3, members=4)
round-trip identical: True
loan survived reload: [Loan(isbn='978-1492056355', due_date=datetime.date(2026, 3, 15)), Loan(isbn='978-1491939369', due_date=datetime.date(2026, 3, 15))]
counts survived reload: 'Fluent Python' by Luciano Ramalho (0/2 available)
after return: 'Fluent Python' by Luciano Ramalho (1/2 available)
ValueError: 'Ada Lovelace' has no loan for isbn '978-1492056355'
search 'python': ['Fluent Python', 'Python Crash Course', 'Think Python']
search 'downey': ['Think Python']
demo complete
```

For the menu the spec actually asks for:

```bash
python main.py
```

Option `6` writes `library.json` next to the script; option `7` reads it back.

### Run the tests

```bash
python -m pytest -q
```

```text
.............                                                            [100%]
13 passed in 0.04s
```

---

## How it maps to the spec

| Spec requirement | Where it lives |
|---|---|
| `Book` fields + internal loaned count | `book.py` — `title`, `author`, `isbn`, `copies_total`, `_copies_loaned` |
| `@property copies_available` | `Book.copies_available` (derived, never stored) |
| `loan_one()` / `return_one()` raising `ValueError` | `Book.loan_one`, `Book.return_one` |
| `__str__` friendly, `__repr__` for debugging | `Book.__str__`; the `@dataclass` repr is left as-is |
| `Book.to_dict()` / `@classmethod from_dict` | bottom of `book.py` |
| `Loan` as a small frozen dataclass | `member.py` — `Loan(isbn, due_date)` |
| `Member` with add/remove loan | `Member.add_loan`, `Member.remove_loan` |
| `Member.to_dict()` / `from_dict()` | bottom of the `Member` class |
| `Library.books` / `Library.members` dicts | `Library.__init__` |
| `add_book`, `register_member` | `library.py` |
| `borrow(member_id, isbn, days=14)` | `Library.borrow` — with rollback if the member half fails |
| unknown member/book and no-copies errors | `get_member`, `get_book`, and `Book.loan_one` |
| `return_book(member_id, isbn)` | `Library.return_book` |
| `overdue_loans(today=None)` | `Library.overdue_loans` |
| `save(path)` / `@classmethod load(path)` | `Library.save`, `Library.load`, via `to_dict` / `from_dict` |
| `main.py` menu covering every feature | `main.py` — options 1–9 plus `--demo` |
| `pathlib` for paths | every path is a `Path`; `save` creates parent folders |
| dates as ISO strings in JSON | `Loan.to_dict` / `Loan.from_dict` |

---

## The stretch goals

All five of the mini-project's stretch goals are implemented.

| Stretch goal | Where |
|---|---|
| `Librarian(Member)` that can register members | `librarian.py`; `Library.from_dict` rebuilds the right class from the stored `role` |
| `search(query)` by partial title or author | `Library.search` |
| Fines at $0.25 per overdue day | `Library.fines`, backed by `Loan.days_overdue` |
| A pytest suite | `test_library.py` — 13 tests |
| `for book in library:` | `Library.__iter__`, plus `__len__` and `__contains__` |

The `argparse` CLI stretch goal is deliberately *not* implemented — `main.py --demo` covers the "run it without typing" need, and an `argparse` front end would double the file for no new OOP content. If you want it, `parse_args` returning the same handler functions `repl` already dispatches to is a 30-line addition.

---

## Reading order

If you are studying the code rather than running it, read it in dependency order — that is also the order the data is built:

1. `book.py` — the smallest complete idea: state, a derived property, two guarded transitions, a JSON round trip.
2. `member.py` — `Loan` first (a frozen value object), then `Member`, which owns a list of them.
3. `library.py` — the orchestrator. `borrow` is the most interesting method in the project; read it twice, especially the `try`/`except` rollback.
4. `librarian.py` — 25 lines showing what an honest subclass looks like next to all that composition.
5. `test_library.py` — the executable version of the spec.
6. `main.py` — read last. It is glue, and glue only makes sense once you know what it is gluing.
