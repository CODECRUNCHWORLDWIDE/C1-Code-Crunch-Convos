# Mini-Project — Contact Book Manager

The capstone for Week 5. You'll build a small **command-line contact book** that stores contacts as a **list of dicts** and persists them to a JSON file between runs. It exercises every data structure concept from the week:

- A `list` of contacts.
- Each contact is a `dict` (`name`, `email`, `phone`).
- Searches use `in` and string methods.
- Persistence uses `json.dump` / `json.load`.
- A menu loop drives the user interaction.

This is a **preview of next week's file I/O lecture**: don't worry if the JSON parts feel a bit magical — we'll demystify them in Week 6.

---

## Functional requirements (the spec)

Your program must:

1. **Load** existing contacts from `contacts.json` at startup. If the file doesn't exist, start with an empty list.
2. Present a **menu loop** offering these options:
   1. Add contact
   2. List all contacts
   3. Search contact by name (case-insensitive substring match)
   4. Update an existing contact
   5. Delete a contact
   6. Save & quit
3. **Save** the current list back to `contacts.json` on quit (and ideally after each modification, so a crash doesn't lose data — a "stretch" requirement).
4. **Validate input** gracefully: empty names should be rejected; invalid menu choices should re-prompt.
5. **Never crash** on user input.

---

## Data model

A contact is exactly this dict:

```python
{
    "name":  str,    # required, non-empty
    "email": str,    # may be empty string
    "phone": str,    # may be empty string
}
```

The full database is `list[dict[str, str]]`. The JSON file looks like:

```json
[
  {"name": "Ada Lovelace",   "email": "ada@example.com",   "phone": "555-0100"},
  {"name": "Grace Hopper",   "email": "grace@example.com", "phone": "555-0200"}
]
```

---

## Provided starter code

See `starter.py`. It already includes:

- The `json` import and `CONTACTS_PATH = Path(__file__).parent / "contacts.json"` setup.
- `load_contacts()` and `save_contacts()` stubs (with working JSON code).
- A `main()` function with the menu loop scaffolded.
- Stubs for each operation function: `add_contact`, `list_contacts`, `search_contacts`, `update_contact`, `delete_contact`.

Your job is to **fill in the bodies** of the operation functions and any helper you need.

---

## Suggested function signatures

```python
def add_contact(contacts: list[dict]) -> None: ...
def list_contacts(contacts: list[dict]) -> None: ...
def search_contacts(contacts: list[dict]) -> None: ...
def update_contact(contacts: list[dict]) -> None: ...
def delete_contact(contacts: list[dict]) -> None: ...
```

All five take the contacts list (which they may mutate) and return `None` — they print directly to stdout and use `input()` for prompts.

---

## Sample session

```
=== Code Crunch Contact Book ===

1) Add contact
2) List all
3) Search
4) Update
5) Delete
6) Save & quit
> 1

Name : Ada Lovelace
Email: ada@example.com
Phone: 555-0100
Added Ada Lovelace.

> 2

1. Ada Lovelace  | ada@example.com  | 555-0100

> 3
Search for: ada
Found 1 match:
  1. Ada Lovelace  | ada@example.com  | 555-0100

> 6
Saved 1 contact to contacts.json. Bye!
```

---

## Implementation hints

1. **Search by name (substring, case-insensitive)** — use `query.lower() in c["name"].lower()` inside a list comprehension.
2. **Find a contact for update/delete** — first list the matches with numbers, then ask the user which number to act on. Validate the number is in range.
3. **Don't trust user input** — always strip whitespace and check for empty strings before adding.
4. **List comprehension to pick matches**:
   ```python
   matches = [(i, c) for i, c in enumerate(contacts) if q in c["name"].lower()]
   ```
5. **Save after every change** if you want crash safety; otherwise only on quit. Either is acceptable.

---

## Rubric (100 points)

| Criterion | Points |
|---|---|
| Load existing JSON file at startup (handles missing file) | 10 |
| Menu loop with 6 working options | 15 |
| Add — appends a validated contact to the list | 10 |
| List — prints all contacts, numbered | 10 |
| Search — case-insensitive substring match | 15 |
| Update — find by match, edit fields, save changes | 15 |
| Delete — find by match, confirm, remove | 10 |
| Save to JSON on quit | 10 |
| No unhandled crashes on weird input (empty, wrong type, missing key) | 5 |
| **Total** | **100** |

---

## Stretch goals

1. **Auto-save** after each modification — survive a hard kill.
2. **Sort contacts** alphabetically by name on every list/save.
3. **Validation** — require an `@` in email; require digits in phone.
4. **Multi-field search** — search across name, email, and phone simultaneously.
5. **Export to CSV** — using the `csv` module (`csv.DictWriter`). Preview of next week.
6. **Use `namedtuple`** for contacts, then convert to/from dict when saving JSON.
7. **Pagination** — if there are more than 20 contacts, list them 20 at a time.
8. **Undo** — keep a small stack of the last N states and offer an "undo" command.

---

## What you'll have learned

When this works end-to-end you will have built a real, persistent, interactive Python program using **only** Week 5 concepts plus a tiny bit of file I/O. That's a remarkable distance from `print("Hello, World!")` in Week 1.

Up next: **Week 6 — File I/O & Exceptions**. The JSON parts of this project will feel obvious.
