"""
Contact Book Manager — Week 5 mini-project starter.

What's already done for you:
  * JSON load/save (you'll learn this properly in Week 6).
  * The main menu loop dispatches to operation functions.
  * Stubs for each operation with `# TODO` markers.

What YOU need to do:
  * Fill in the bodies of add_contact, list_contacts, search_contacts,
    update_contact, and delete_contact.
  * Make sure invalid input never crashes the program.

Run:
    python starter.py
"""

from __future__ import annotations

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CONTACTS_PATH: Path = Path(__file__).parent / "contacts.json"


# ---------------------------------------------------------------------------
# Persistence (already implemented -- preview of Week 6)
# ---------------------------------------------------------------------------

def load_contacts() -> list[dict[str, str]]:
    """Load contacts from CONTACTS_PATH. Return [] if the file is missing."""
    if not CONTACTS_PATH.exists():
        return []
    try:
        with CONTACTS_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        # Defensive: only accept lists of dicts.
        if isinstance(data, list):
            return [c for c in data if isinstance(c, dict)]
        return []
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Warning: could not load {CONTACTS_PATH}: {exc}")
        return []


def save_contacts(contacts: list[dict[str, str]]) -> None:
    """Write the contact list to CONTACTS_PATH as pretty-printed JSON."""
    with CONTACTS_PATH.open("w", encoding="utf-8") as fh:
        json.dump(contacts, fh, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def prompt(label: str, *, allow_empty: bool = False) -> str:
    """Repeatedly ask for input until a non-empty string is given (unless allow_empty=True)."""
    while True:
        value = input(f"{label}: ").strip()
        if value or allow_empty:
            return value
        print("  (cannot be empty)")


def render(contact: dict[str, str]) -> str:
    """Format a single contact as a one-line string."""
    return (
        f"{contact.get('name', '?'):<25} | "
        f"{contact.get('email', ''):<25} | "
        f"{contact.get('phone', '')}"
    )


def find_matches(
    contacts: list[dict[str, str]], query: str
) -> list[tuple[int, dict[str, str]]]:
    """Return a list of (index, contact) tuples whose name contains query (case-insensitive)."""
    q = query.lower().strip()
    return [(i, c) for i, c in enumerate(contacts) if q in c.get("name", "").lower()]


# ---------------------------------------------------------------------------
# Operations -- YOU IMPLEMENT THESE
# ---------------------------------------------------------------------------

def add_contact(contacts: list[dict[str, str]]) -> None:
    """Prompt for name/email/phone, append a new dict to `contacts`."""
    # TODO:
    # 1. name = prompt("Name")                # required
    # 2. email = prompt("Email", allow_empty=True)
    # 3. phone = prompt("Phone", allow_empty=True)
    # 4. contacts.append({"name": name, "email": email, "phone": phone})
    # 5. print(f"Added {name}.")
    raise NotImplementedError("add_contact")


def list_contacts(contacts: list[dict[str, str]]) -> None:
    """Print every contact in the list, numbered from 1."""
    # TODO:
    # if not contacts:  print "No contacts yet." and return.
    # else: for i, c in enumerate(contacts, 1): print(f"{i}. {render(c)}")
    raise NotImplementedError("list_contacts")


def search_contacts(contacts: list[dict[str, str]]) -> None:
    """Ask for a substring, print every matching contact."""
    # TODO:
    # 1. query = prompt("Search for")
    # 2. matches = find_matches(contacts, query)
    # 3. if not matches: print "No matches." and return
    # 4. else: print count and each match (use render()).
    raise NotImplementedError("search_contacts")


def update_contact(contacts: list[dict[str, str]]) -> None:
    """Find a contact by name search, then edit its fields."""
    # TODO:
    # 1. query = prompt("Update which contact (search by name)")
    # 2. matches = find_matches(contacts, query)
    # 3. if not matches: print "No matches." and return
    # 4. if more than one match, print them numbered and ask which to update.
    #    Validate the choice is an int in range; reprompt on failure.
    # 5. For the chosen contact, for each field (name/email/phone) ask for a new value;
    #    if the user just presses Enter (empty string), keep the old value.
    # 6. Update the dict in place.
    # 7. Print "Updated."
    raise NotImplementedError("update_contact")


def delete_contact(contacts: list[dict[str, str]]) -> None:
    """Find a contact by name search, then delete it (with a yes/no confirm)."""
    # TODO:
    # 1. query = prompt("Delete which contact (search by name)")
    # 2. matches = find_matches(contacts, query)
    # 3. if not matches: print and return
    # 4. If more than one match, list them and ask which number to delete.
    # 5. Confirm with input("Are you sure? [y/N] ").lower() == "y".
    # 6. del contacts[index].
    # 7. Print confirmation.
    raise NotImplementedError("delete_contact")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

MENU = """
=== Code Crunch Contact Book ===

1) Add contact
2) List all
3) Search
4) Update
5) Delete
6) Save & quit
"""

ACTIONS = {
    "1": add_contact,
    "2": list_contacts,
    "3": search_contacts,
    "4": update_contact,
    "5": delete_contact,
}


def main() -> None:
    contacts: list[dict[str, str]] = load_contacts()
    print(f"Loaded {len(contacts)} contact(s) from {CONTACTS_PATH.name}.")

    while True:
        print(MENU)
        choice = input("> ").strip()

        if choice == "6":
            save_contacts(contacts)
            print(f"Saved {len(contacts)} contact(s) to {CONTACTS_PATH.name}. Bye!")
            return

        action = ACTIONS.get(choice)
        if action is None:
            print(f"  Unknown option: {choice!r}. Try 1-6.")
            continue

        try:
            action(contacts)
        except NotImplementedError as exc:
            print(f"  (Not implemented yet: {exc}.)")
        except KeyboardInterrupt:
            print("\n(cancelled)")
        except Exception as exc:  # broad on purpose for a beginner CLI
            print(f"  Error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
