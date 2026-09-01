"""
Week 5 mini-project — the eight stretch goals, as importable pieces.

They live here rather than inside `contact_book.py` on purpose: the base
program has to reproduce the spec's sample session byte for byte, and half of
these goals change what it prints. Keeping them separate means you can read
each one on its own, test it on its own, and bolt the ones you want onto the
menu loop without breaking the graded behaviour.

Every function here is pure with respect to module state -- the contact list
arrives as an argument. `python selfcheck.py` exercises all of them.
"""

import csv
from collections import namedtuple
from pathlib import Path

from contact_book import FIELDS, format_row

# ---------------------------------------------------------------------------
# Stretch 1 -- auto-save
# ---------------------------------------------------------------------------
# Already implemented in contact_book.main(): every mutating branch (1, 4, 5)
# calls save_contacts() immediately, and the EOFError/KeyboardInterrupt handler
# saves on the way out. save_contacts() itself writes to `contacts.json.tmp`
# and then calls Path.replace(), so a kill in the middle of the write leaves
# the old file intact instead of a half-written one. There is nothing to add
# here; selfcheck.py proves it by killing a session mid-loop.


# ---------------------------------------------------------------------------
# Stretch 2 -- sort alphabetically by name
# ---------------------------------------------------------------------------


def sorted_contacts(contacts: list[dict[str, str]]) -> list[dict[str, str]]:
    """A new list, ordered by name, case-insensitively, ties broken by email.

    `sorted` is stable and `key=` never mutates the strings it inspects, so
    the stored names keep their original casing -- you lower the KEY, not the
    payload. Returning a new list (rather than calling contacts.sort()) means
    a caller can print sorted output while the on-disk order stays as-is.
    """
    return sorted(contacts, key=lambda c: (c["name"].lower(), c["email"].lower()))


# ---------------------------------------------------------------------------
# Stretch 3 -- validation
# ---------------------------------------------------------------------------


def looks_like_email(value: str) -> bool:
    """A deliberately loose check: one '@', something either side, a dot after.

    Do not try to validate email properly with string methods -- the real
    grammar (RFC 5322) allows quoted local parts, comments and bracketed IP
    domains. The only complete validation is sending mail to the address.
    """
    if value.count("@") != 1:
        return False
    local, _, domain = value.partition("@")
    return bool(local) and "." in domain and not domain.startswith(".") and not domain.endswith(".")


def looks_like_phone(value: str) -> bool:
    """At least three digits, and nothing but digits and the usual furniture."""
    allowed = set("0123456789 -()+.")
    digits = [ch for ch in value if ch.isdigit()]
    return len(digits) >= 3 and all(ch in allowed for ch in value)


def validate(contact: dict[str, str]) -> list[str]:
    """Return a list of complaints. Empty list means the contact is fine.

    Returning complaints instead of raising lets the caller decide the policy:
    the CLI prints them as warnings and stores the contact anyway, a bulk
    importer might reject the row. Empty email and phone are allowed, because
    the spec's data model says so.
    """
    problems: list[str] = []
    if not contact.get("name", "").strip():
        problems.append("name is empty")
    email = contact.get("email", "")
    if email and not looks_like_email(email):
        problems.append(f"{email!r} does not look like an email address")
    phone = contact.get("phone", "")
    if phone and not looks_like_phone(phone):
        problems.append(f"{phone!r} does not look like a phone number")
    return problems


# ---------------------------------------------------------------------------
# Stretch 4 -- search every field at once
# ---------------------------------------------------------------------------


def find_matches_any_field(
    contacts: list[dict[str, str]], query: str
) -> list[tuple[int, dict[str, str]]]:
    """Substring match across name, email and phone, case-insensitively.

    `any(...)` over a generator short-circuits on the first field that hits,
    so a name match costs one comparison, not three.
    """
    needle = query.strip().lower()
    if not needle:
        return []
    return [
        (i, c)
        for i, c in enumerate(contacts)
        if any(needle in c[field].lower() for field in FIELDS)
    ]


# ---------------------------------------------------------------------------
# Stretch 5 -- CSV export
# ---------------------------------------------------------------------------


def export_csv(contacts: list[dict[str, str]], path: Path) -> int:
    """Write the book as CSV with a header row. Returns the rows written.

    `newline=""` is not optional on Windows: the csv module writes its own
    "\\r\\n" line terminator, and without it Python's text layer translates the
    "\\n" as well and you get blank lines between every row.
    """
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(FIELDS))
        writer.writeheader()
        writer.writerows(contacts)
    return len(contacts)


def import_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV written by export_csv back into the list-of-dicts shape."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [
            {field: row.get(field, "") or "" for field in FIELDS}
            for row in csv.DictReader(handle)
        ]


# ---------------------------------------------------------------------------
# Stretch 6 -- namedtuple records
# ---------------------------------------------------------------------------

Contact = namedtuple("Contact", FIELDS)


def to_record(contact: dict[str, str]) -> Contact:
    """dict -> Contact. `**` unpacking works because the keys ARE the fields."""
    return Contact(**{field: contact.get(field, "") for field in FIELDS})


def to_dict(record: Contact) -> dict[str, str]:
    """Contact -> dict, for json.dump. `_asdict` returns a real dict."""
    return dict(record._asdict())


# ---------------------------------------------------------------------------
# Stretch 7 -- pagination
# ---------------------------------------------------------------------------


def pages(contacts: list[dict[str, str]], size: int = 20) -> list[list[dict[str, str]]]:
    """Split into chunks of `size`. The last page may be short; never empty."""
    if size <= 0:
        raise ValueError(f"page size must be positive, got {size}")
    return [contacts[start : start + size] for start in range(0, len(contacts), size)]


def render_page(
    page: list[dict[str, str]], page_index: int, page_count: int, size: int = 20
) -> str:
    """Render one page, numbering rows by their position in the WHOLE book."""
    first = page_index * size
    lines = [format_row(first + offset + 1, c) for offset, c in enumerate(page)]
    lines.append(f"-- page {page_index + 1} of {page_count} --")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Stretch 8 -- undo
# ---------------------------------------------------------------------------


class History:
    """A bounded stack of past states of the contact list.

    Each snapshot is `[dict(c) for c in contacts]`: a new outer list holding
    new inner dicts. That is one level deeper than `contacts.copy()`, which
    would share the very dicts that `update_contact` mutates in place -- and a
    snapshot that mutates with the thing it is snapshotting is not a snapshot.
    `copy.deepcopy` would also work and is slower for no gain, because the
    values are strings and strings are immutable.
    """

    def __init__(self, limit: int = 10) -> None:
        self.limit = limit
        self.states: list[list[dict[str, str]]] = []

    def snapshot(self, contacts: list[dict[str, str]]) -> None:
        """Call this BEFORE a mutation, not after."""
        self.states.append([dict(c) for c in contacts])
        if len(self.states) > self.limit:
            self.states.pop(0)  # drop the oldest

    def undo(self, contacts: list[dict[str, str]]) -> bool:
        """Restore the last snapshot in place. False when there is nothing left."""
        if not self.states:
            return False
        contacts[:] = self.states.pop()  # slice assignment: same list object
        return True

    def __len__(self) -> int:
        return len(self.states)
