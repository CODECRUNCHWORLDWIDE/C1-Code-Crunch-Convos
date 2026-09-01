# Reference implementation — Week 5 mini-project (contact book manager)

This folder is the working answer to [Week 5's mini-project](../../../curriculum/week-05-data-structures/mini-project/README.md). It is a real, runnable program, not an excerpt: the transcripts quoted in the [mini-project walkthrough](../../../curriculum/week-05-data-structures/mini-project/README.md) were produced by running exactly these files.

Read the walkthrough for the *why*. This file tells you what is here and how to run it.

---

## What is in the folder

| File | What it is |
|---|---|
| `contact_book.py` | The whole program. One file, standard library only, ~250 lines including docstrings. This is the graded answer. |
| `stretch.py` | All eight stretch goals as separate, importable functions, so the graded program keeps its exact specified output. |
| `selfcheck.py` | The test harness. Replays the spec's sample session and compares it character for character, then walks every rubric line and every stretch goal. |
| `contacts.sample.json` | Five contacts to play with. Copy it to `contacts.json` to start with data instead of an empty book. |

`contacts.json` is deliberately **not** in the folder. The program creates it on first save, and the spec requires that a missing file means "start with an empty list" — so the missing file is part of what you are testing.

---

## How to run it

Python 3.10 or newer (the `list[dict[str, str]]` and `X | None` annotations need 3.10). Everything it imports — `json`, `pathlib`, `csv`, `collections` — ships with CPython, so there is no `pip install` step.

```bash
cd projects/solutions/week-05-data-structures
python contact_book.py
```

To start with the sample data instead of an empty book:

```bash
cp contacts.sample.json contacts.json
python contact_book.py
```

A short scripted run against that data (piping stdin means your typed answers are not echoed, so the prompts look bare):

```bash
printf '2\n3\nhop\n6\n' | python contact_book.py
```

```text
=== Code Crunch Contact Book ===

1) Add contact
2) List all
3) Search
4) Update
5) Delete
6) Save & quit
>
1. Ada Lovelace  | ada@example.com  | 555-0100
2. Grace Hopper  | grace@example.com  | 555-0200
3. Linus Torvalds  | linus@example.com  | 555-0300
4. Margaret Hamilton  | margaret@example.com  |
5. Katherine Johnson  |   | 555-0500

> Search for: Found 1 match:
  1. Grace Hopper  | grace@example.com  | 555-0200

> Saved 5 contacts to contacts.json. Bye!
```

(Trailing spaces have been stripped from that block — a contact with no phone really does print a trailing `| ` with nothing after it, because `format_row` uses no column padding. `selfcheck.py` compares the *unstripped* text.)

---

## How to check it

```bash
cd projects/solutions/week-05-data-structures
python selfcheck.py
```

```text
Transcript matches the spec's sample session exactly.
All checks passed.
```

The first line is the important one. `selfcheck.py` swaps `builtins.input` for a function that pops a scripted answer and writes `prompt + answer` into the same buffer stdout is redirected to — which reconstructs precisely what a terminal shows, because a terminal transcript *is* the program's output interleaved with the echo of your typing. The result is compared against the sample session copied verbatim out of the mini-project spec. If a single space moves, the check fails and prints both versions.

---

## How it maps to the spec

| Spec requirement | Where it lives | Rubric points |
|---|---|---|
| Load `contacts.json` at startup, empty list if missing | `load_contacts` | 10 |
| Menu loop with six working options | `main` | 15 |
| Add — append a validated contact | `add_contact` | 10 |
| List — print all contacts, numbered | `list_contacts` + `format_row` | 10 |
| Search — case-insensitive substring on name | `find_matches`, printed by `search_contacts` | 15 |
| Update — find by match, edit fields, keep the change | `choose_match` + `update_contact` | 15 |
| Delete — find by match, confirm, remove | `choose_match` + `delete_contact` | 10 |
| Save to JSON on quit | `save_contacts`, called from the `"6"` branch | 10 |
| No unhandled crashes on weird input | `load_contacts`'s three guards, `choose_match`'s four refusals, `main`'s `except (EOFError, KeyboardInterrupt)` | 5 |
| Suggested signatures `(contacts: list[dict]) -> None` | all five operations match | — |
| Stretch: save after every modification | the `save_contacts` call in branches 1, 4 and 5 | — |

---

## The stretch goals

All eight are implemented. Stretch 1 (auto-save) is in `contact_book.py` because the spec itself blesses it; the other seven live in `stretch.py` so the graded program's output stays exactly as specified.

| Stretch goal | Where |
|---|---|
| 1 — auto-save after each modification | `contact_book.main` + the atomic write in `save_contacts` |
| 2 — sort alphabetically by name | `stretch.sorted_contacts` |
| 3 — validate email and phone | `stretch.looks_like_email`, `looks_like_phone`, `validate` |
| 4 — search across all fields | `stretch.find_matches_any_field` |
| 5 — export to CSV | `stretch.export_csv` (plus `import_csv`, for the round-trip test) |
| 6 — `namedtuple` contacts | `stretch.Contact`, `to_record`, `to_dict` |
| 7 — pagination at 20 rows | `stretch.pages`, `render_page` |
| 8 — undo | `stretch.History` |

---

## Reading order

If you are studying the code rather than running it, read it in the order the data flows:

1. `FIELDS` and `format_row` — the shape of one record and how it prints.
2. `load_contacts` / `save_contacts` — the file becomes a list, and back again.
3. `find_matches` — the one function every other feature is built on. Note that it returns `(index, contact)` pairs, not bare contacts.
4. `add_contact`, `list_contacts`, `search_contacts` — the three easy operations.
5. `choose_match`, then `update_contact` and `delete_contact` — the two hard ones, and the helper that makes them nearly identical.
6. `main` — the glue. Read it last, because it only makes sense once you know what it is gluing.

That is also a good order to *write* it in, and it is why the file is laid out that way.
