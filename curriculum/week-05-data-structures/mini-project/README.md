# Mini-Project — Contact Book Manager

> **Topic:** a list of dicts, a menu loop, and a file that has to still be there tomorrow
> **Lecture:** [02 — Sets and Dictionaries](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** no single function here is hard; keeping the program from losing your data is the whole project
> **Target time:** 5–7 hours, spread over more than one sitting
> **Why this one:** it is the first program you have written that a real person could use twice. That changes everything — it has to survive being closed, survive being reopened, survive somebody typing nonsense at it, and survive a half-finished save. Every one of those is a decision, and none of them showed up in a program that printed once and stopped.

<!-- no-runnable-file: this page is the project brief, and what you hand in is a program in your own repository together with the contacts.json it wrote and a session you can show somebody. The runnable answer is contact_book.py, which ships beside this page and is linked from Download and run. It is named after the project rather than the page because a file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

This is the capstone of Week 5. You are building a small **contact book** that
runs at the terminal: a menu, six options, and a file on disk so that the
contacts are still there next time.

The book itself is a plain list, and each contact in it is a plain dict:

```python
[
    {"name": "Ada Lovelace", "email": "ada@example.com", "phone": "555-0100"},
    {"name": "Grace Hopper", "email": "grace@example.com", "phone": "555-0200"},
]
```

That is the whole data model. Three string fields, and the name is the only one
that has to be filled in.

**Wait — a list?** Week 5 has spent three lectures telling you that dicts and
sets turn searching into looking up, and now the capstone asks for a list.
Noticing why is most of the learning in this project.

The headline operation is *find every name that contains this bit of text*.
Type `ada` and you should find `Ada Lovelace`. A dict can find an exact key
instantly because it computes an address from the whole key — but `"ada"` and
`"Ada Lovelace"` compute completely unrelated addresses, and there is no
relationship between the two. So that search has to look at every contact
whatever container you choose. Once the cost is settled, you pick on other
grounds, and a list is ordered, allows two people to share a name, and is
exactly what a JSON array becomes when you read it back.

Keying the book by name would also smuggle in a rule nobody asked for:

```text
contacts stored: 1
{'Ada Lovelace': {'name': 'Ada Lovelace', 'email': 'ada@home.com'}}
```

Two people can share a name. One person can have a work entry and a home entry.
A dict makes both impossible, and makes the second one **silently overwrite** the
first. Uniqueness is a rule about your data; do not sneak it in through a
container choice.

So the question to carry out of this week is not "can I use a dict here?" It is:
**what am I scanning for, and could that scan be a key?** Here the honest answer
is no.

Here is the session the finished program should produce:

```text
$ python contact_book.py
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

> *As a* learner who can use lists, dicts and comprehensions,
> *I want* to build something that remembers what I typed after I close it,
> *so that* I find out which decisions only appear once a program has to run
> twice.

The JSON parts are a **preview of Week 6**. If `json.load` feels a bit magical
right now, that is fine and expected — next week takes it apart.

## Starter

There is no starter file for this project, and that is deliberate. You have
written five weeks of Python; starting from an empty file is the point.

What follows is the scaffolding, so you know the shape you are aiming at. Save
it as `contact_book.py` in a folder of your own — `week-05-contacts/` beside
your other Week 5 work is fine. It runs as pasted; every option just says it is
not written yet.

```python
"""Contact Book Manager. Week 5 mini-project, Code Crunch Convos."""

import json
from pathlib import Path

CONTACTS_PATH = Path(__file__).parent / "contacts.json"

FIELDS = ("name", "email", "phone")

MENU = (
    "1) Add contact\n"
    "2) List all\n"
    "3) Search\n"
    "4) Update\n"
    "5) Delete\n"
    "6) Save & quit"
)


def load_contacts(path: Path = CONTACTS_PATH) -> list[dict[str, str]]:
    """Read the book from `path`, or return [] when there is nothing to read."""
    if not path.exists():
        return []
    # TODO 1: read the text, parse the JSON, and hand back the list. Then come
    #         back and make this survive a file that is not valid JSON.
    return []


def save_contacts(contacts: list[dict[str, str]], path: Path = CONTACTS_PATH) -> None:
    """Write the whole book back to `path` as JSON."""
    path.write_text(json.dumps(contacts, indent=2) + "\n", encoding="utf-8")


def find_matches(
    contacts: list[dict[str, str]], query: str
) -> list[tuple[int, dict[str, str]]]:
    """Return the (index, contact) pairs whose name contains `query`."""
    # TODO 2: lowercase both sides. Return pairs, not contacts -- the index is
    #         what update and delete need. A blank query matches nothing.
    return []


def add_contact(contacts: list[dict[str, str]]) -> None:
    """Ask for the three fields and append the new contact."""
    # TODO 3: refuse a blank name.
    print("(not written yet)")


def list_contacts(contacts: list[dict[str, str]]) -> None:
    """Print the whole book, numbered from 1."""
    # TODO 4
    print("(not written yet)")


def search_contacts(contacts: list[dict[str, str]]) -> None:
    """Ask for a piece of a name and print every contact that contains it."""
    # TODO 5
    print("(not written yet)")


def update_contact(contacts: list[dict[str, str]]) -> None:
    """Find one contact and edit its fields."""
    # TODO 6
    print("(not written yet)")


def delete_contact(contacts: list[dict[str, str]]) -> None:
    """Find one contact, confirm, and remove it."""
    # TODO 7
    print("(not written yet)")


def main(path: Path = CONTACTS_PATH) -> None:
    """Load the book, run the menu until the user quits, and save on the way out."""
    contacts = load_contacts(path)
    print("=== Code Crunch Contact Book ===")
    print()
    print(MENU)
    while True:
        choice = input("> ").strip()
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            list_contacts(contacts)
        elif choice == "3":
            search_contacts(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            save_contacts(contacts, path)
            print(f"Saved {len(contacts)} contacts to {path.name}. Bye!")
            return
        else:
            print(f"{choice!r} is not one of 1-6.")
        print()


if __name__ == "__main__":
    main()
```

Two notes before you start filling it in.

**`find_matches` returns pairs, not contacts.** That is the single most
important line in the scaffold and *Common bugs to catch* explains what happens
without it.

**The `input("> ")` in `main` is the version you write first.** It is fine while
you are typing at it by hand. The downloadable answer uses a different shape,
and *The Solution* explains why — but get the program working before you worry
about that.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](../../../README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. **Load** the contacts from `contacts.json` at startup. If the file is not
   there, start with an empty list and do not complain.
2. **A menu loop** offering six options:
   1. Add contact
   2. List all contacts
   3. Search by name, matching any part of it, ignoring case
   4. Update an existing contact
   5. Delete a contact
   6. Save and quit
3. **Save** the list back to `contacts.json` on quit. Saving after every change
   as well is better, and is stretch goal 1.
4. **Add** appends a contact with all three fields. A blank name is refused.
5. **List** prints every contact, numbered from 1.
6. **Search** matches any part of the name, in any case: `ADA`, `ada` and `dA`
   all find `Ada Lovelace`.
7. **Update** finds a contact, edits its fields, and the change is still there
   after a restart.
8. **Delete** finds a contact, confirms, and removes that one and only that one.
9. **Never crash.** An invalid menu choice re-prompts. A letter where a number
   was wanted is refused politely. A corrupted `contacts.json` starts an empty
   book rather than a traceback.
10. Type hints on every signature and a docstring on every function.

## Constraints

- **The book is a `list` of `dict`s**, exactly as the data model says. Not a
  dict of dicts, not a set, not a class — you meet those in Week 7.
- **`find_matches` returns `(index, contact)` pairs.** The number the user picks
  and the position in the book are different numbers, and they only agree when
  the search matched everything, which is exactly the case you will test by
  accident.
- **Delete by position, with `contacts.pop(index)`.** `contacts.remove(contact)`
  finds the first item *equal to* the one you passed, which is the wrong one as
  soon as the book holds two identical entries.
- **Update the dict in place.** `contact[field] = answer` edits the book.
  `contact = {...}` and `contact = contacts[i].copy()` both edit something
  nobody else can see, and your change vanishes on save.
- **Validate with `raw.isdecimal()`, not `raw.isdigit()`.** `try` / `except` is
  the better tool and it is next week's lecture; this project has to survive bad
  input with Week 5 material only. *The Solution* shows why the two string
  methods are not interchangeable.
- **A blank search query matches nothing.** `"" in anything` is `True`, so
  without a guard, pressing Enter at `Delete which name?` offers to delete your
  whole book.
- **Standard library only** — `json` and `pathlib`, both previews of Week 6, and
  `sys` if you follow the answer's prompt handling.
- **Runs on Python 3.10 or newer.**

## Expected output

The downloadable answer runs the session from *The Brief*. Point it at nothing
— no keyboard, no piped input — and it interviews itself so you can see the
whole thing at once. Real stdout on CPython 3.13.2:

```text
$ python contact_book.py
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

That is the brief's sample session, line for line.

**Now the part the happy session does not cover.** Feed it answers from the
shell, one line per question, and watch it refuse four bad ones in a row:

```bash
printf '\n7\nbanana\n1\n\n4\nzzz\n6\n' | python contact_book.py
```

```text
=== Code Crunch Contact Book ===

1) Add contact
2) List all
3) Search
4) Update
5) Delete
6) Save & quit
'' is not one of 1-6. Type ? for the menu.

'7' is not one of 1-6. Type ? for the menu.

'banana' is not one of 1-6. Type ? for the menu.


A contact needs a name. Nothing added.

No match for 'zzz'. Nothing to update.

Saved 0 contacts to contacts.json. Bye!
```

The prompts are missing from that block because they go to the error stream,
which is why the complaints stand out so clearly. Read it against the
requirements:

| Input | What should happen | The line it produced |
|---|---|---|
| *(blank)* | not a menu choice, ask again | `'' is not one of 1-6. Type ? for the menu.` |
| `7` | out of range, ask again | `'7' is not one of 1-6. Type ? for the menu.` |
| `banana` | not a number at all, ask again | `'banana' is not one of 1-6. Type ? for the menu.` |
| `1` then blank name | a contact needs a name | `A contact needs a name. Nothing added.` |
| `4` then `zzz` | nothing matches, so do nothing | `No match for 'zzz'. Nothing to update.` |
| `6` | save an empty book without complaint | `Saved 0 contacts to contacts.json. Bye!` |

Six pieces of nonsense, six sentences, no traceback. That is requirement 9.

## Steps

Build it in the order that lets you run something after every step. Do not write
all seven functions and then start testing.

1. Save the scaffold and run it. You should get the banner, the menu, and
   `(not written yet)` for options 1 to 5.
2. Do **TODO 4**, `list_contacts`. It is the shortest one and it gives you a way
   to see everything else working:

   ```python
   for number, contact in enumerate(contacts, start=1):
       print(f"{number}. {contact['name']}  | {contact['email']}  | {contact['phone']}")
   ```

   Handle the empty book separately — `(no contacts yet)` beats a blank screen.
3. Do **TODO 3**, `add_contact`. Ask, strip, refuse a blank name, append. Now
   run the program and use options 1 and 2 together. You have a working program
   that forgets everything when it closes.
4. Do **TODO 1**, `load_contacts`, and check `save_contacts` works. Add a
   contact, quit, look at `contacts.json` in an editor, run again, press `2`.
   Your contact is there. **This is the moment the project becomes real** — stop
   and enjoy it.
5. Do **TODO 2**, `find_matches`. Lowercase both sides, guard the blank query,
   and return pairs:

   ```python
   needle = query.strip().lower()
   if not needle:
       return []
   return [(i, c) for i, c in enumerate(contacts) if needle in c["name"].lower()]
   ```

6. Do **TODO 5**, `search_contacts`, on top of it. Print the matches numbered
   from 1. Test `ADA`, `ada`, `dA` and `zzz`.
7. Write `choose_match` before you write update or delete. Both need "find one
   specific contact, or give up politely", and writing it twice guarantees the
   two copies drift apart.
8. Do **TODO 6** and **TODO 7** on top of `choose_match`. Test delete by
   deleting the **third** contact in a book of three, using a search that
   matches only it. Deleting the first one passes even when the code is wrong.
9. Make it survive nonsense. A letter at the picker, a number out of range, a
   blank query, a hand-broken `contacts.json`. Run the `printf` session from
   *Expected output*.
10. Read *The Solution*, then go back and look at your `save_contacts` again.
    There is one line in there that decides whether a crash mid-save costs you
    one contact or all of them.
11. Commit and push:

    ```bash
    git add week-05-contacts/
    git commit -m "Week 5 mini-project: contact book manager"
    git push
    ```

## The Solution

```python
"""Contact Book Manager: a small address book that survives being closed.

Mini-project, Week 5, Code Crunch Convos.

The book is a ``list`` of ``dict``s, exactly as the brief's data model says::

    [{"name": str, "email": str, "phone": str}, ...]

A list is the right container even though the rest of Week 5 pushes you towards
dicts and sets. The headline operation is "find every name that contains this
piece of text", and a piece of text does not hash to the same place as the whole
name, so that search has to look at every contact whichever container you pick.
Once the cost is settled you choose on other grounds, and a list is ordered,
allows two people to share a name, and is what JSON hands back for an array.

Questions go to the error stream and results go to the normal output stream, so
``python contact_book.py > session.txt`` saves the book and not the interview.
With nothing attached to its input the file interviews itself from
``DEMO_ANSWERS`` and keeps its ``contacts.json`` in a throwaway folder, so
running the download can never touch a book of your own.

Run it::

    python contact_book.py
"""

import json
import sys
import tempfile
from pathlib import Path

CONTACTS_PATH = Path(__file__).parent / "contacts.json"

# Where an unattended demo run writes instead. Same file name, different folder.
DEMO_PATH = Path(tempfile.gettempdir()) / "contact-book-demo" / "contacts.json"

# The three keys of a contact, in display order. Keeping them in one tuple lets
# `update_contact` loop over the fields instead of repeating itself three times,
# and lets `load_contacts` reshape a record in one comprehension.
FIELDS = ("name", "email", "phone")

MENU = (
    "1) Add contact\n"
    "2) List all\n"
    "3) Search\n"
    "4) Update\n"
    "5) Delete\n"
    "6) Save & quit"
)

# The session this file gives itself when nobody is typing.
DEMO_ANSWERS: list[str] = [
    "1",
    "Ada Lovelace",
    "ada@example.com",
    "555-0100",
    "2",
    "3",
    "ada",
    "6",
]

# One entry per answer this file had to make up. Empty means a person answered.
UNATTENDED: list[str] = []


def ask(prompt: str, demo: str) -> str:
    """Return the answer to `prompt`, or a demo answer when nobody is typing.

    Args:
        prompt: The question, including its trailing space.
        demo: What to answer once the scripted session above has run out. Every
            call site passes something that ends its loop, so the file can never
            run forever unattended.

    Returns:
        The line that was typed, or the next demo answer. A demo answer is
        echoed after its prompt on the normal output stream, so the saved
        transcript reads like a real terminal session.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        UNATTENDED.append(answer)
        print(f"{prompt}{answer}".rstrip())
        return answer


def store_for(path: Path) -> Path:
    """Return the file to write to: `path`, or the throwaway demo copy."""
    return DEMO_PATH if UNATTENDED else path


def load_contacts(path: Path = CONTACTS_PATH) -> list[dict[str, str]]:
    """Read the book from `path`, returning an empty list rather than raising.

    Args:
        path: The JSON file to read. It is allowed not to exist.

    Returns:
        Every usable record, reshaped to exactly the three keys in FIELDS with
        string values, so nothing further along has to defend itself against a
        half-built dict. A missing file, damaged JSON, or JSON that is not an
        array all give back an empty list.
    """
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"! {path.name} is not valid JSON ({exc.msg}); starting empty.")
        return []
    except OSError as exc:
        print(f"! could not read {path.name} ({exc.strerror}); starting empty.")
        return []
    if not isinstance(raw, list):
        print(f"! {path.name} does not contain a JSON array; starting empty.")
        return []
    contacts: list[dict[str, str]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        if not str(entry.get("name", "")).strip():
            continue  # a nameless contact is not a contact
        contacts.append({field: str(entry.get(field, "")) for field in FIELDS})
    return contacts


def save_contacts(contacts: list[dict[str, str]], path: Path) -> None:
    """Write the whole book back as JSON, without a window to lose it in.

    Args:
        contacts: The book to write.
        path: Where to write it. Its folder is created if it is missing.

    Returns:
        None. The new text lands in a temporary file first and is then renamed
        over the old one, so the old book stays whole until the new one is
        complete.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(contacts, indent=2, ensure_ascii=False) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def format_row(number: int, contact: dict[str, str]) -> str:
    """Return one display line, in the layout the brief's session shows."""
    return f"{number}. {contact['name']}  | {contact['email']}  | {contact['phone']}"


def plural(count: int, singular: str, suffix: str = "s") -> str:
    """Return '1 contact' or '2 contacts'; the brief's quit line is singular."""
    return f"{count} {singular}" if count == 1 else f"{count} {singular}{suffix}"


def find_matches(
    contacts: list[dict[str, str]], query: str
) -> list[tuple[int, dict[str, str]]]:
    """Return the (index, contact) pairs whose name contains `query`.

    Args:
        contacts: The book to search.
        query: The text to look for. Case does not matter, and a blank query
            matches nothing rather than everything.

    Returns:
        Pairs of the contact's real position in the book and the contact
        itself. Carrying the real position is the trick behind update and
        delete: the user picks the Nth match, but what you change is the Nth
        contact, and those two numbers differ the moment a search filters
        anything out.
    """
    needle = query.strip().lower()
    if not needle:
        return []
    return [(i, c) for i, c in enumerate(contacts) if needle in c["name"].lower()]


def print_matches(matches: list[tuple[int, dict[str, str]]]) -> None:
    """Print matches numbered from 1, indented two spaces."""
    for number, (_, contact) in enumerate(matches, start=1):
        print("  " + format_row(number, contact))


def add_contact(contacts: list[dict[str, str]]) -> None:
    """Ask for a name, an email and a phone, and append the new contact."""
    print()
    name = ask("Name : ", "").strip()
    if not name:
        print("A contact needs a name. Nothing added.")
        return
    email = ask("Email: ", "").strip()
    phone = ask("Phone: ", "").strip()
    contacts.append({"name": name, "email": email, "phone": phone})
    print(f"Added {name}.")


def list_contacts(contacts: list[dict[str, str]]) -> None:
    """Print the whole book, numbered from 1."""
    print()
    if not contacts:
        print("(no contacts yet)")
        return
    for number, contact in enumerate(contacts, start=1):
        print(format_row(number, contact))


def search_contacts(contacts: list[dict[str, str]]) -> None:
    """Ask for a piece of a name and print every contact that contains it."""
    matches = find_matches(contacts, ask("Search for: ", ""))
    if not matches:
        print("Found 0 matches.")
        return
    print(f"Found {plural(len(matches), 'match', 'es')}:")
    print_matches(matches)


def choose_match(
    contacts: list[dict[str, str]], verb: str
) -> tuple[int, dict[str, str]] | None:
    """Search, show the hits, and ask which one the user means.

    Args:
        contacts: The book to search.
        verb: The word for what is about to happen, such as "Update".

    Returns:
        The (index, contact) pair the user picked, or None for every way of
        declining: no query, no hits, an answer that is not a number, a number
        outside the list. Each one says why first.
    """
    query = ask(f"{verb} which name? ", "").strip()
    matches = find_matches(contacts, query)
    if not matches:
        print(f"No match for {query!r}. Nothing to {verb.lower()}.")
        return None
    print_matches(matches)
    # isdecimal, not isdigit: the superscript two passes isdigit and then int()
    # refuses it, which is a crash hiding inside a check that looks careful.
    raw = ask(f"Which one? (1-{len(matches)}) ", "0").strip()
    if not raw.isdecimal():
        print(f"{raw!r} is not a number. Cancelled.")
        return None
    pick = int(raw)
    if not 1 <= pick <= len(matches):
        print(f"There is no #{pick}. Cancelled.")
        return None
    return matches[pick - 1]


def update_contact(contacts: list[dict[str, str]]) -> None:
    """Find one contact and edit its fields in place."""
    picked = choose_match(contacts, "Update")
    if picked is None:
        return
    _, contact = picked
    print("Enter a new value, blank to keep, '-' to clear.")
    for field in FIELDS:
        answer = ask(f"{field.capitalize():<5} [{contact[field]}]: ", "").strip()
        if answer == "":
            continue
        if answer == "-":
            if field == "name":
                print("A contact needs a name; keeping it.")
                continue
            contact[field] = ""
            continue
        contact[field] = answer
    print(f"Updated {contact['name']}.")


def delete_contact(contacts: list[dict[str, str]]) -> None:
    """Find one contact, confirm, and remove it by its real position."""
    picked = choose_match(contacts, "Delete")
    if picked is None:
        return
    index, contact = picked
    answer = ask(f"Really delete {contact['name']}? (y/n) ", "n").strip().lower()
    if answer not in {"y", "yes"}:
        print("Cancelled.")
        return
    removed = contacts.pop(index)  # the real position, not the match number
    print(f"Deleted {removed['name']}.")


def main(path: Path = CONTACTS_PATH) -> None:
    """Load the book, run the menu until the user quits, and save on the way out."""
    contacts = load_contacts(path)
    print("=== Code Crunch Contact Book ===")
    print()
    print(MENU)
    while True:
        choice = ask("> ", "6").strip()
        if choice == "1":
            add_contact(contacts)
            save_contacts(contacts, store_for(path))
        elif choice == "2":
            list_contacts(contacts)
        elif choice == "3":
            search_contacts(contacts)
        elif choice == "4":
            update_contact(contacts)
            save_contacts(contacts, store_for(path))
        elif choice == "5":
            delete_contact(contacts)
            save_contacts(contacts, store_for(path))
        elif choice == "6":
            store = store_for(path)
            save_contacts(contacts, store)
            print(f"Saved {plural(len(contacts), 'contact')} to {store.name}. Bye!")
            return
        elif choice in {"?", "m", "menu"}:
            print()
            print(MENU)
        else:
            print(f"{choice!r} is not one of 1-6. Type ? for the menu.")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Interrupted.")
```

**Why it works.**

**`find_matches` is the function everything else is built on**, and three things
in it are load bearing.

*`.lower()` on both sides.* Ignoring case means normalising the thing you are
looking for **and** the thing you are looking in. Lower only the query and
`"ada"` finds `"ada@example.com"` but not `"Ada Lovelace"` — which is the exact
bug the brief's own hint is written to prevent.

*It returns `(index, contact)` pairs.* The user picks "match number 2". The
thing you must change is "contact number 7". Those two numbers are equal only
when the search matched everything, which is exactly the case you will test by
accident.

*A blank query matches nothing, not everything.*

```python
>>> "" in "Ada Lovelace"
True
```

Without the guard, pressing Enter at `Search for:` matches every contact — and
then Enter at `Delete which name?` offers you your whole book. Guarding the
empty string is a safety property, not a nicety.

**`update` and `delete` share `choose_match` because they share a problem.**
Both are "find the one contact the user means, or give up politely", and that
interaction has four separate ways to end in doing nothing:

| The user does this | `choose_match` gives back | What is printed |
|---|---|---|
| Types a name that matches nothing | `None` | `No match for 'zzz'. Nothing to update.` |
| Types a non-number at the picker | `None` | `'x' is not a number. Cancelled.` |
| Types a number out of range | `None` | `There is no #99. Cancelled.` |
| Types a blank query | `None` | `No match for ''. Nothing to delete.` |

Write that twice and the two copies drift. Write it once and both callers open
the same way — `picked = choose_match(...)`, `if picked is None: return` — and
the rest of each function is only the part that genuinely differs. Returning
`None` for "nothing to do" and a value for "here it is" is the same shape as
`dict.get`, and readers already know how to hold it.

**`isdecimal()` and not `isdigit()`.** If you wrote `isdigit()` there — most
people do — you wrote a crash:

```python
>>> "²".isdigit(), "²".isdecimal()
(True, False)
>>> int("²")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: '²'
```

`isdigit()` is true for superscripts and other digit-ish characters that `int()`
refuses. `isdecimal()` is true for exactly the characters `int()` accepts. The
two disagree on maybe a hundred code points out of a million, and one of them is
on a keyboard people actually use.

**`delete` uses `contacts.pop(index)`, not `contacts.remove(contact)`.**
`list.remove(x)` scans for the first item **equal to** `x` and deletes that.
Contacts are dicts, and dicts compare by value, so if the same person is in the
book twice with identical fields, `remove` deletes the first copy regardless of
which one the user picked. `pop(index)` deletes the one at that position, full
stop.

**`update` edits the dict in place and never rebinds it.**

```python
_, contact = picked
contact[field] = answer
```

`contact` is a **second name for the dict inside the list** — the aliasing rule
from [lecture 01](../lecture-notes/01-lists-and-tuples.md#aliasing--the-gotcha),
used on purpose. Changing it through that name changes the book. What you must
not write is `contact = {...}`, which only moves the local label, or
`contact = contacts[i].copy()`, which edits an object nobody else can see:

```text
edited copy : ada@newdomain.org
in the book : ada@example.com
```

No exception, no warning, and the edit simply evaporates on save. This is the
most common silent bug in this project.

**`load_contacts` is where "never crash" is won.** It is the only function
reading data it did not write, so it is the only one that has to be paranoid. It
has four guards and each matches a real way `contacts.json` goes bad:

| Guard | Real cause |
|---|---|
| `if not path.exists()` | First run — requirement 1 asks for exactly this |
| `except json.JSONDecodeError` | The program was killed mid-write, or somebody hand-edited the file |
| `if not isinstance(raw, list)` | Somebody saved one contact instead of a list of them |
| Skip non-dicts, skip nameless records, `str(...)` every value | Hand-edited entries, a field left as `null`, a phone number written as a JSON number |

The last one matters more than it looks. `{"phone": 5550100}` is legal JSON, and
without the `str(...)` a later `c["phone"].lower()` raises
`AttributeError: 'int' object has no attribute 'lower'` — a crash two hundred
lines away from the file that caused it. **Normalise at the boundary and the
inside can stop defending itself.** That principle is worth more than this
project.

**`save_contacts` writes to a temporary file and renames it.**

```python
tmp = path.with_suffix(path.suffix + ".tmp")
tmp.write_text(text, encoding="utf-8")
tmp.replace(path)
```

`write_text` on the real file empties it *before* writing the new content. Kill
the program in that window — a crash, a Ctrl-C, a laptop lid — and
`contacts.json` is empty or half an array, which the next run cannot parse.
Writing somewhere else and renaming makes the swap atomic: the old file stays
whole until the instant the new one is complete. Saving after every change makes
a torn write **more** likely, not less, which is why frequency without atomicity
is not crash safety.

**`ask()` puts the questions on the other stream.** A program has two ways to
send text out: the normal output stream for its results, and the error stream
for everything else. `ask` prints the question to the error stream with `end=""`
so the cursor stays put, and `flush=True` so it appears before the program starts
waiting. Then it calls `input()` with **no argument at all**.

That last detail is the one people get wrong. `input("Name : ")` prints its
prompt to the *normal* output stream, mixed into your results. Keeping them apart
is what makes this work:

```bash
python contact_book.py > session.txt
```

That is not a trick to make a checker happy. It is how every well-behaved
command-line tool on your machine already works, which is why you can pipe one
into another.

**And `ask` never blocks when nobody is typing.** `input()` with no keyboard and
no piped input raises `EOFError`. The `except` catches it, takes the next line
out of `DEMO_ANSWERS` instead, and echoes it — so the file always produces a
whole session instead of hanging or crashing. `store_for` then points the save
at a throwaway folder, so running the download can never overwrite a book of
your own.

## Download and run

Download [contact_book.py](./contact_book.py) and run it:

```bash
python contact_book.py
```

In your own terminal it talks to you and keeps `contacts.json` beside itself.
Run by a script, or with its input closed, it interviews itself from
`DEMO_ANSWERS`, prints the session in *Expected output*, and keeps its
`contacts.json` in a throwaway folder so your own book is never touched.

You can also feed it answers from the shell, one line per question:

```bash
printf '1\nGrace Hopper\ngrace@example.com\n555-0200\n2\n6\n' | python contact_book.py
```

Because the questions go to the error stream, `>` captures the session on its
own:

```bash
python contact_book.py > session.txt
```

**It is named after the project, not after this page.** A file called
`README.py` would be a strange thing to ask anybody to download.

**What you hand in is your own program**, in a folder in your own repository,
with the `contacts.json` it wrote, the commit history that built it, and a
session you can show somebody. This file is here so you can run a finished
answer in ten seconds and compare.

## Common bugs to catch

**Using the match number as the position in the book.** The big one.

```python
matches = [c for c in contacts if q in c["name"].lower()]   # no indexes kept
...
contacts.pop(pick - 1)                                      # the WRONG list
```

```text
user asked to delete: Linus Torvalds
actually deleted    : Ada Lovelace
book now            : ['Grace Hopper', 'Linus Torvalds']
```

No traceback. The program cheerfully prints `Deleted Linus Torvalds.`, deletes
Ada, and you find out weeks later. Keep the index with the match —
`[(i, c) for i, c in enumerate(contacts) if ...]`, which is what the brief's own
hint hands you — and this entire family of bugs becomes unwritable.

**`json.load` on a file that is not there.**

```python
with open("contacts.json") as fh:
    contacts = json.load(fh)
```

```text
Traceback (most recent call last):
  File "contact_book.py", line 30, in <module>
    with open("no-such-file.json") as fh:
         ~~~~^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'no-such-file.json'
```

The very first run of a brand-new contact book crashes before it prints the
banner. That is requirement 1. `if not path.exists(): return []` is the Week 5
fix; `try` / `except FileNotFoundError` is the Week 6 fix and is better, because
between the check and the open the file can still disappear.

**Removing from a list while looping over it.**

```python
for c in contacts:
    if "ada" in c["name"].lower():
        contacts.remove(c)
```

```text
survivors: ['Ada B', 'Zoe']
```

No error — and `Ada B` is still there. The loop walks by position: it hands you
index 0 (`Ada A`), you delete it, everything shifts left, and the next turn
hands you index 1, which is now `Ada C`. Every second match is skipped. Unlike a
dict, a list does **not** raise `RuntimeError: dictionary changed size during
iteration`; it just quietly gives you the wrong answer. Build the survivors
instead (`contacts[:] = [c for c in contacts if ...]`) or delete one at a time by
position, which is what the answer does.

**Not handling the end of input.**

```text
Traceback (most recent call last):
  File "contact_book.py", line 49, in <module>
    input("> ")
    ~~~~~^^^^^^
EOFError: EOF when reading a line
```

You meet this the first time you pipe a script into your program
(`printf '2\n6\n' | python contact_book.py`) and the first time you press
Ctrl-D. Requirement 9 covers it. One `except EOFError` turns a traceback into a
graceful exit — and the answer's `ask()` turns it into a demo session instead.

**Editing a copy of the contact.** Covered in *The Solution*.
`contacts[i].copy()` in `update_contact` produces an update that looks like it
worked and changed nothing. If your update prints `Updated Grace Hopper.` and
option 2 still shows the old email, this is why.

**Trying to make contacts hashable so you can use a set.**

```text
TypeError: unhashable type: 'dict'
```

and its cousin, when you try to sort the book without saying what to sort on:

```text
TypeError: '<' not supported between instances of 'dict' and 'dict'
```

Dicts are mutable, so they are unhashable, so they cannot go in a set or be used
as dict keys; and they have no natural order, so `sorted(contacts)` cannot work.
Both messages are telling you the same thing: **a dict is a record, not a
value.** Sort with `key=lambda c: c["name"].lower()`, and deduplicate on a field
you choose rather than on the whole record.

**Printing the menu every time round the loop.** Not a bug, but a decision you
should make on purpose. The brief's sample session shows the menu once at the
top and a bare `> ` for every later prompt, so the answer prints it once and adds
`?` to summon it again. Reprinting every time is friendlier for a beginner and
does **not** match the given transcript. If your grader diffs against the sample
session, print once. Either way, say which you did and why.

## Under the hood

<details>
<summary>Under the hood — what json.dumps and json.loads actually do to your data</summary>

JSON is a text format, and Python objects are not text, so both directions
involve a translation — and the translation is not perfectly reversible. Knowing
where it loses information saves you a bad afternoon.

`json.dumps` turns an object into a string:

```python
>>> import json
>>> json.dumps({"name": "Ada", "age": 36})
'{"name": "Ada", "age": 36}'
```

Note the quotes on the outside. That is one Python `str`, and every key inside
it is double-quoted, because JSON has no single-quoted strings and no trailing
commas. `json.loads` reverses it.

**The type mapping is small, and things fall off the edges.**

| Python | JSON | Coming back |
|---|---|---|
| `dict` | object | `dict` |
| `list`, `tuple` | array | **`list`** — a tuple comes back a list |
| `str` | string | `str` |
| `int`, `float` | number | `int` or `float` |
| `True` / `False` | `true` / `false` | `True` / `False` |
| `None` | `null` | `None` |
| `set`, dates, objects | *nothing* | `TypeError` |

Two of those rows bite in this project.

**Tuples become lists.** If you take the `namedtuple` stretch goal, remember
that a namedtuple **is** a tuple, so it serialises as an array and the field
names simply vanish:

```text
dumps: [["Ada Lovelace", "ada@example.com", "555-0100"]]
loads: [['Ada Lovelace', 'ada@example.com', '555-0100']]
```

Round-trip it and you have plain lists, not `Contact`s. Convert at the file
boundary — `_asdict()` on the way out, the constructor on the way in — which is
the same normalise-at-the-boundary move `load_contacts` already makes.

**Sets are not JSON at all.**

```python
>>> json.dumps({"tags": {"friend", "work"}})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Object of type set is not JSON serializable
```

A JSON array is ordered and allows duplicates; a set is neither. `sorted(...)`
on the way out and `set(...)` on the way in is the usual fix, and sorting also
makes your file's contents stable between runs, which makes it diff cleanly in
git.

**Dict keys are always strings in JSON.** This one is genuinely sneaky:

```python
>>> json.loads(json.dumps({1: "a"}))
{'1': 'a'}
```

The key went in as an integer and came out as a string, with no error anywhere.
If you ever key data by number and persist it as JSON, that conversion is
waiting for you.

Two arguments in the answer's `dumps` call are worth naming. `indent=2` makes
the file readable and diffable instead of one enormous line — worth it for a
config or a small database, not worth it for a million rows. And
`ensure_ascii=False` keeps `José` as `José` rather than escaping it to
`José`; both are valid JSON and both read back identically, but only one is
readable when you open the file.

Finally, `encoding="utf-8"` on every read and write. Without it Python picks a
default that differs between Windows and Linux, so a file with an accent in a
name works on your machine and breaks on somebody else's. Always say it.

</details>

<details>
<summary>Under the hood — why the same string search is fast enough here and hopeless at a million rows</summary>

The brief argues that a substring search has to look at every contact, so a list
is fine. That is true, and it is worth knowing exactly where it stops being
true, because "just scan it" is the right answer far more often than beginners
expect and then abruptly is not.

**What the scan costs.** For each contact, `needle in c["name"].lower()` does
two things: it builds a lowercased copy of the name, and it looks for the needle
inside it. The search itself is clever — CPython uses a mix of algorithms that
skips ahead rather than comparing character by character — but both steps are
proportional to the length of the name. So the whole search costs roughly "the
total number of characters in all your names".

Put numbers on it. A thousand contacts averaging fifteen characters is fifteen
thousand characters — microseconds. A million contacts is fifteen million
characters per keystroke, which is the difference between an instant answer and
a visible pause.

**Why a hash table cannot help.** A dict finds `"Ada Lovelace"` instantly
because it computes an address from the *whole* key. There is no relationship
between that address and the address of `"ada"`, `"da L"` or any other piece of
it — a good hash function is *designed* so that similar inputs land far apart.
You cannot ask a hash table for "keys containing this" any more than you can ask
a phone book for "everyone whose name has a Q in the middle" without reading it.

**What does help, when you get there.** Three ideas, in increasing order of
effort:

*Normalise once instead of per search.* The scan lowercases every name on every
keystroke. Store a `name_lower` field when the contact is saved and the search
stops rebuilding the same strings over and over. Same shape of algorithm, a
constant factor faster, and about four lines.

*Prefix search with a sorted list.* If you only need names that **start with**
the query, sort the book and use `bisect` to jump straight to the block that
matches. That turns the scan into a couple of dozen comparisons. It answers a
narrower question — `bisect` cannot find `"Love"` inside `"Ada Lovelace"` — and
narrowing the question is very often the real fix.

*An index of pieces.* Build a dict from every three-character run of every name
to the set of contacts containing it. Now `"ada"` is one lookup, and a longer
query is the intersection of a few lookups. This is roughly what a search engine
does, and the cost is that every add, update and delete must maintain the index
— which is the trade behind every database index you have ever created.

**The order to try things in.** Scan first. Measure. Only then index. A scan of
a thousand records is invisible, correct, and four lines long, and an index that
is out of step with the data is worse than no index at all. The judgement being
taught here is not "dicts are fast", it is: **know what your container can and
cannot answer, and pick the simplest one that can answer your actual question.**

</details>

<details>
<summary>Under the hood — the decisions in this project that were genuinely open</summary>

A grader should accept any of the following, argued. What they should not accept
is not having noticed there was a choice.

**1. Print the menu once, or every time round the loop?** The brief's sample
session shows it once, with a bare `> ` afterwards, so the answer prints nothing
extra and adds `?` to summon it again. Reprinting is friendlier and does not
match the transcript. Pick one and say why.

**2. Auto-save, or save only on quit?** The brief calls auto-save a stretch and
marks either acceptable. The answer auto-saves because the cost is one function
call per change and the alternative loses an hour of typing to one Ctrl-C. The
argument the other way is real: saving on every action writes a bug in
`add_contact` to disk before you have noticed it. That objection is live at
scale and irrelevant at two hundred contacts.

**3. What does a blank answer mean at an update prompt?** The answer chose:
blank Enter **keeps** the current value, a single `-` **clears** it, and `-` on
the name is refused. The alternative — retype every field every time — is
simpler code and much worse to use. Whichever you pick, say it on screen
(`Enter a new value, blank to keep, '-' to clear.`), because an invisible
convention is a bug.

**4. `""` or `None` for a missing email?** The data model says `str` and "may be
empty string", so `""`. That also means every `c["email"].lower()` is safe with
no `None` check, and JSON round-trips it unchanged. `None` would be more honest
about "unknown" versus "deliberately blank" and would cost you a guard at every
use site. The brief decided; follow the brief.

**5. Number the search results, or number by position in the book?** The answer
numbers matches from 1 and keeps the real position privately. Showing the true
position (`7. Grace Hopper`) is defensible — it is stable across searches — but
then "which one?" wants a number the user cannot guess for a hit they can see.
Show 1 to n, act on the hidden position.

**6. One file or several?** One. The graded program is about 250 lines and has
exactly one job; splitting it into `storage.py`, `ui.py` and `models.py` at this
size adds imports and indirection without removing any complexity. Week 4's
mini-project split into four files because the *dependencies* wanted separating,
not because the line count did. Knowing the difference is the point.

**7. Confirm before deleting, or just do it?** The brief says "find by match,
confirm, remove", so confirm. Worth noticing what the confirmation is actually
buying: not protection from a mis-typed name — the match list already shows you
that — but a second look at *which* of several similar hits you picked. A
confirmation that shows you nothing new is a keystroke tax, and there are a lot
of those in the world.

</details>

## Acceptance checklist

- [ ] A fresh run with no `contacts.json` starts an empty book and does not
      crash.
- [ ] Adding a contact, quitting, and running again shows it still there.
- [ ] `2` on an empty book prints something, not a blank screen.
- [ ] Numbering in the listing starts at 1 and has no gaps.
- [ ] `ADA`, `ada` and `dA` all find `Ada Lovelace`; `zzz` finds nothing.
- [ ] A blank search query matches **nothing**.
- [ ] Updating an email, quitting, restarting, and listing shows the new value.
- [ ] Deleting the **third** contact of three, via a search that matches only
      it, leaves the other two.
- [ ] A letter at the "which one?" prompt is refused politely.
- [ ] A number out of range at the "which one?" prompt is refused politely.
- [ ] `7`, `banana` and an empty line at the menu all re-prompt.
- [ ] A hand-corrupted `contacts.json` starts an empty book with a message, not
      a traceback.
- [ ] Ctrl-D at the `> ` prompt does not print a traceback.
- [ ] `contacts.json` after a save holds the current book, and is valid JSON.
- [ ] Every function has type hints and a docstring.
- [ ] No function body is longer than 25 lines.
- [ ] No `TODO` comments left.
- [ ] Committed with a message such as
      `Week 5 mini-project: contact book manager`.

**Grade your own.** The rubric is 100 points across nine rows. Run these nine
checks against *your* program:

| Rubric row | Points | The check that proves it |
|---|---|---|
| Load existing JSON at startup, handles missing file | 10 | Delete `contacts.json`, run, no traceback, `2` prints an empty book |
| Menu loop with 6 working options | 15 | Every digit 1–6 does its job; `7`, `""` and `banana` re-prompt |
| Add — appends a validated contact | 10 | Add one, then `2` shows it; a blank name is refused |
| List — prints all contacts, numbered | 10 | Numbering starts at 1 and is contiguous |
| Search — case-insensitive substring | 15 | `ADA`, `ada` and `dA` all find `Ada Lovelace`; `zzz` finds nothing |
| Update — find, edit, changes stick | 15 | Update an email, quit, restart, `2` shows the new value |
| Delete — find, confirm, remove | 10 | Delete the **third** contact via a search that matches only it |
| Save to JSON on quit | 10 | Open `contacts.json` after `6`; it holds the current book |
| No unhandled crashes on weird input | 5 | Ctrl-D at `> `; a letter at "which one?"; a broken JSON file |

The delete row is where most self-assessments are too generous. Deleting the
*first* contact passes even with the match-number bug. Delete the third.

## Stretch

**1. Auto-save after every change.** Call `save_contacts` immediately after add,
update and delete rather than only on quit. The part people miss is that saving
*more often* makes a torn write *more likely*, which is why `save_contacts`
writes a `.tmp` file and renames it. Frequency without atomicity is not crash
safety.

**2. Sort alphabetically by name.**

```python
def sorted_contacts(contacts: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return a new list, sorted by name then email, without touching the book."""
    return sorted(contacts, key=lambda c: (c["name"].lower(), c["email"].lower()))
```

Lower the **key**, never the stored value — `"ada lovelace"` must not end up in
the file. The tuple key breaks ties on email so two people with the same name
keep a stable order between runs. And it returns a *new* list rather than calling
`contacts.sort()`, so you can print sorted output without renumbering the
positions that update and delete depend on. If you do sort the real list, sort it
before every listing *and* every search, or the numbers on screen and the
positions in memory will disagree.

**3. Validate the email and the phone.**

```python
def looks_like_email(value: str) -> bool:
    """Return True when `value` is shaped enough like an address to be worth trying."""
    if value.count("@") != 1:
        return False
    local, _, domain = value.partition("@")
    return bool(local) and "." in domain and not domain.startswith(".")
```

Note the name — `looks_like_email`, not `is_valid_email`. The real grammar
permits quoted local parts, comments and bracketed IP addresses; every "email
regex" you find online is wrong in both directions, and the only complete
validation is sending mail to the address. A loose check that catches
`ada.example.com` and `@example.com` is genuinely useful; a strict one rejects
real addresses and makes people hate your program.

Have your validator return a **list of complaints** rather than a bool. That
lets the caller decide the policy — the menu can print them and store the
contact anyway, a bulk importer can reject the row — and it reports *all* the
problems at once, so the user fixes them in one pass instead of playing
whack-a-mole.

**4. Search every field at once.**

```python
return [
    (i, c) for i, c in enumerate(contacts)
    if any(needle in c[field].lower() for field in FIELDS)
]
```

`any` over a generator stops at the first hit, so a name match costs one
comparison rather than three. This is also the feature that makes the `str(...)`
in `load_contacts` load bearing: a phone number that came back from JSON as an
integer blows up on `.lower()` here and nowhere else.

**5. Export to CSV** with `csv.DictWriter`. `newline=""` on the `open` call is
not optional — the csv module writes its own line ending, and without it Python
translates the newline as well, you get a doubled one, and every other row in a
spreadsheet is blank. It is the single most reported "the csv module is broken"
bug and it is in the first paragraph of the module's documentation.

**6. Use a `namedtuple` for contacts.** You gain `record.name` alongside
`record[0]`, and immutability — which means `update_contact` can no longer edit
in place and has to build a replacement with `record._replace(email=...)`. That
is a real trade, not a free upgrade, and the JSON trap is in the first *Under the
hood* block.

**7. Paginate.**

```python
def pages(contacts: list[dict[str, str]], size: int = 20) -> list[list[dict[str, str]]]:
    """Split the book into chunks of `size`, the last one possibly short."""
    return [contacts[start : start + size] for start in range(0, len(contacts), size)]
```

Slicing past the end clamps rather than raising, so the last page is simply
short. 45 contacts at 20 a page gives lengths `[20, 20, 5]`; an empty book gives
`[]`, not `[[]]`. The detail that matters for usability is numbering rows by
their position in the **whole book**, so page 3 starts at `41.` — restarting the
numbers on each page is how you get somebody deleting the wrong contact.

**8. Undo.** Keep a small stack of previous states.

```python
states.append([dict(c) for c in contacts])     # snapshot
contacts[:] = states.pop()                     # undo
```

Two lines carry the whole idea. `[dict(c) for c in contacts]` copies one level
deeper than `contacts.copy()` — a plain copy gives you a new outer list holding
*the very dicts `update_contact` edits in place*, which is a snapshot that
changes along with the thing it is snapshotting. And `contacts[:] = ...` is slice
assignment: it replaces the contents of the existing list rather than rebinding a
name, so the caller's book really does change. Take the snapshot **before** the
change, not after; a stack of after-states can only undo you to where you already
are.

Next: **Week 6 — File I/O & Exceptions**, where the JSON parts of this project
stop being magic.
