"""
Week 5 mini-project — Contact Book Manager (reference implementation).

The database is a `list` of `dict`s, exactly as the spec's data model says:

    [{"name": str, "email": str, "phone": str}, ...]

A list is the right structure here even though the rest of Week 5 pushes you
towards dicts and sets. The book's headline operation is "case-insensitive
substring match on the name", and a substring match cannot be a hash lookup --
"ada" does not hash to the same bucket as "Ada Lovelace". That scan is O(n) no
matter what container you pick, so you take the container that is simplest to
read, order-preserving, and JSON-native. A dict keyed by name would also make
two people called "Ada Lovelace" impossible, which is a policy the spec never
asked for.

Everything below is Week 1-5 material plus `json` and `pathlib`, which the
mini-project explicitly previews from Week 6.

Run it:      python contact_book.py
Check it:    python selfcheck.py
"""

import json
from pathlib import Path

CONTACTS_PATH = Path(__file__).parent / "contacts.json"

# The three keys of a contact record, in display order. Having them in one
# tuple means `update_contact` can loop over the fields instead of repeating
# itself three times, and `load_contacts` can normalise a record in one
# comprehension.
FIELDS = ("name", "email", "phone")

MENU = (
    "1) Add contact\n"
    "2) List all\n"
    "3) Search\n"
    "4) Update\n"
    "5) Delete\n"
    "6) Save & quit"
)


# --------------------------------------------------------------------------
# Persistence
# --------------------------------------------------------------------------


def load_contacts(path: Path = CONTACTS_PATH) -> list[dict[str, str]]:
    """Read the contact list from `path`.

    Returns an empty list -- never raises -- when the file is missing, is not
    valid JSON, or does not hold a JSON array. Every surviving record is
    normalised to exactly the three keys in FIELDS, with string values, so no
    later function has to defend against a half-shaped dict.
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


def save_contacts(contacts: list[dict[str, str]], path: Path = CONTACTS_PATH) -> None:
    """Write the whole list back as pretty-printed JSON, atomically-ish."""
    text = json.dumps(contacts, indent=2, ensure_ascii=False) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)  # os.replace is atomic on POSIX and on NTFS


# --------------------------------------------------------------------------
# Display helpers
# --------------------------------------------------------------------------


def format_row(number: int, contact: dict[str, str]) -> str:
    """One display line, in the exact layout the spec's sample session shows."""
    return f"{number}. {contact['name']}  | {contact['email']}  | {contact['phone']}"


def plural(count: int, singular: str, suffix: str = "s") -> str:
    """'1 contact' / '2 contacts' -- the spec's quit line is singular."""
    return f"{count} {singular}" if count == 1 else f"{count} {singular}{suffix}"


def find_matches(
    contacts: list[dict[str, str]], query: str
) -> list[tuple[int, dict[str, str]]]:
    """Case-insensitive substring match on `name`.

    Returns `(index, contact)` pairs, where `index` is the position in the
    REAL list. Carrying the true index is the whole trick behind update and
    delete: what the user picks is the Nth *match*, but what you mutate is
    the Nth *contact*, and those two numbers are different as soon as a
    search filters anything out.
    """
    needle = query.strip().lower()
    if not needle:
        return []
    return [(i, c) for i, c in enumerate(contacts) if needle in c["name"].lower()]


def print_matches(matches: list[tuple[int, dict[str, str]]]) -> None:
    """Print matches numbered from 1, indented two spaces."""
    for number, (_, contact) in enumerate(matches, start=1):
        print("  " + format_row(number, contact))


# --------------------------------------------------------------------------
# The five operations
# --------------------------------------------------------------------------


def add_contact(contacts: list[dict[str, str]]) -> None:
    print()
    name = input("Name : ").strip()
    if not name:
        print("A contact needs a name. Nothing added.")
        return
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    contacts.append({"name": name, "email": email, "phone": phone})
    print(f"Added {name}.")


def list_contacts(contacts: list[dict[str, str]]) -> None:
    print()
    if not contacts:
        print("(no contacts yet)")
        return
    for number, contact in enumerate(contacts, start=1):
        print(format_row(number, contact))


def search_contacts(contacts: list[dict[str, str]]) -> None:
    query = input("Search for: ").strip()
    matches = find_matches(contacts, query)
    if not matches:
        print("Found 0 matches.")
        return
    print(f"Found {plural(len(matches), 'match', 'es')}:")
    print_matches(matches)


def choose_match(
    contacts: list[dict[str, str]], verb: str
) -> tuple[int, dict[str, str]] | None:
    """Search, show the hits, ask which one. Returns `(index, contact)`.

    Returns None -- meaning "the caller should do nothing" -- for every way
    the user can decline: no query, no hits, a non-number, a number out of
    range. Every one of those prints a reason first.
    """
    query = input(f"{verb} which name? ").strip()
    matches = find_matches(contacts, query)
    if not matches:
        print(f"No match for {query!r}. Nothing to {verb.lower()}.")
        return None

    print_matches(matches)
    raw = input(f"Which one? (1-{len(matches)}) ").strip()
    # isdecimal(), not isdigit(): "2".isdigit() is True for the superscript
    # two as well, and int("\N{SUPERSCRIPT TWO}") raises ValueError.
    if not raw.isdecimal():
        print(f"{raw!r} is not a number. Cancelled.")
        return None

    pick = int(raw)
    if not 1 <= pick <= len(matches):
        print(f"There is no #{pick}. Cancelled.")
        return None

    return matches[pick - 1]


def update_contact(contacts: list[dict[str, str]]) -> None:
    picked = choose_match(contacts, "Update")
    if picked is None:
        return
    _, contact = picked

    print("Enter a new value, blank to keep, '-' to clear.")
    for field in FIELDS:
        current = contact[field]
        answer = input(f"{field.capitalize():<5} [{current}]: ").strip()
        if answer == "":
            continue  # keep
        if answer == "-":
            if field == "name":
                print("A contact needs a name; keeping it.")
                continue
            contact[field] = ""
            continue
        contact[field] = answer

    print(f"Updated {contact['name']}.")


def delete_contact(contacts: list[dict[str, str]]) -> None:
    picked = choose_match(contacts, "Delete")
    if picked is None:
        return
    index, contact = picked

    answer = input(f"Really delete {contact['name']}? (y/n) ").strip().lower()
    if answer not in {"y", "yes"}:
        print("Cancelled.")
        return

    removed = contacts.pop(index)  # the TRUE index, not the match number
    print(f"Deleted {removed['name']}.")


# --------------------------------------------------------------------------
# The menu loop
# --------------------------------------------------------------------------


def main(path: Path = CONTACTS_PATH) -> None:
    contacts = load_contacts(path)

    print("=== Code Crunch Contact Book ===")
    print()
    print(MENU)

    while True:
        try:
            choice = input("> ").strip()

            if choice == "1":
                add_contact(contacts)
                save_contacts(contacts, path)
            elif choice == "2":
                list_contacts(contacts)
            elif choice == "3":
                search_contacts(contacts)
            elif choice == "4":
                update_contact(contacts)
                save_contacts(contacts, path)
            elif choice == "5":
                delete_contact(contacts)
                save_contacts(contacts, path)
            elif choice == "6":
                save_contacts(contacts, path)
                print(f"Saved {plural(len(contacts), 'contact')} to {path.name}. Bye!")
                return
            elif choice in {"?", "m", "menu"}:
                print()
                print(MENU)
            else:
                print(f"{choice!r} is not one of 1-6. Type ? for the menu.")

        except (EOFError, KeyboardInterrupt):
            # Ctrl-C, Ctrl-D, or a closed pipe: save rather than lose data.
            print()
            save_contacts(contacts, path)
            print(f"Interrupted. Saved {plural(len(contacts), 'contact')} to {path.name}.")
            return

        print()


if __name__ == "__main__":
    main()
