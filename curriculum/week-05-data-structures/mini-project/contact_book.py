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
