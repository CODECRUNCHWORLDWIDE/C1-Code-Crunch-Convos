"""
Self-check for the Week 5 mini-project reference implementation.

Run it from this folder:

    python selfcheck.py

It does three jobs:

1. Replays the exact sample session printed in the mini-project spec and
   compares the transcript character for character.
2. Exercises every rubric line -- load, menu, add, list, search, update,
   delete, save, and the "never crash on weird input" row.
3. Exercises all eight stretch goals from `stretch.py`.

The replay works by swapping `builtins.input` for a function that pops the
next scripted answer and writes `prompt + answer` into the same buffer stdout
is redirected to. That reconstructs what a terminal would show, because a
terminal's transcript is exactly the program's output interleaved with the
echo of what you typed.
"""

import builtins
import contextlib
import io
import tempfile
from pathlib import Path

import contact_book
from contact_book import find_matches, format_row, load_contacts, plural, save_contacts
from stretch import (
    Contact,
    History,
    export_csv,
    find_matches_any_field,
    import_csv,
    looks_like_email,
    looks_like_phone,
    pages,
    render_page,
    sorted_contacts,
    to_dict,
    to_record,
    validate,
)

SAMPLE_SESSION = """\
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
"""


def replay(script: list[str], path: Path) -> str:
    """Run a whole session against a scripted stdin; return the transcript."""
    answers = iter(script)
    buffer = io.StringIO()

    def fake_input(prompt: str = "") -> str:
        try:
            answer = next(answers)
        except StopIteration:
            raise EOFError from None  # script exhausted == user pressed Ctrl-D
        buffer.write(f"{prompt}{answer}\n")
        return answer

    real_input = builtins.input
    builtins.input = fake_input
    try:
        with contextlib.redirect_stdout(buffer):
            contact_book.main(path)
    finally:
        builtins.input = real_input
    return buffer.getvalue()


# ---------------------------------------------------------------------------


def check_sample_session(tmp: Path) -> None:
    transcript = replay(
        ["1", "Ada Lovelace", "ada@example.com", "555-0100", "2", "3", "ada", "6"],
        tmp / "contacts.json",
    )
    if transcript != SAMPLE_SESSION:
        print("--- produced ---")
        print(transcript)
        print("--- expected ---")
        print(SAMPLE_SESSION)
        raise AssertionError("transcript does not match the spec's sample session")
    print("Transcript matches the spec's sample session exactly.")


def check_persistence(tmp: Path) -> None:
    path = tmp / "book.json"

    # A missing file is an empty book, not an error.
    assert load_contacts(path) == []

    people = [
        {"name": "Ada Lovelace", "email": "ada@example.com", "phone": "555-0100"},
        {"name": "Grace Hopper", "email": "grace@example.com", "phone": "555-0200"},
    ]
    save_contacts(people, path)
    assert load_contacts(path) == people          # round trip
    assert not path.with_suffix(".json.tmp").exists()  # the temp file is gone

    # Garbage in the file must not crash the program. load_contacts explains
    # itself on stdout; swallow that here so the check output stays clean.
    noise = io.StringIO()
    with contextlib.redirect_stdout(noise):
        path.write_text("{not json at all", encoding="utf-8")
        assert load_contacts(path) == []

        path.write_text('{"name": "Ada"}', encoding="utf-8")  # object, not array
        assert load_contacts(path) == []
    assert "is not valid JSON" in noise.getvalue()
    assert "does not contain a JSON array" in noise.getvalue()

    # Missing keys are filled in; nameless records are dropped; a stray
    # non-dict element is skipped rather than exploding.
    path.write_text('[{"name": "Ada"}, {"email": "x@y.z"}, "nope"]', encoding="utf-8")
    assert load_contacts(path) == [{"name": "Ada", "email": "", "phone": ""}]

    # Non-ASCII survives the round trip.
    save_contacts([{"name": "Ada Lovelace", "email": "ada@exämple.com", "phone": ""}], path)
    assert load_contacts(path)[0]["email"] == "ada@exämple.com"


def check_search_indexes() -> None:
    people = [
        {"name": "Ada Lovelace", "email": "", "phone": ""},
        {"name": "Grace Hopper", "email": "", "phone": ""},
        {"name": "Linus Torvalds", "email": "", "phone": ""},
    ]
    # Case-insensitive substring, in both directions.
    assert [i for i, _ in find_matches(people, "ADA")] == [0]
    assert [i for i, _ in find_matches(people, "ac")] == [0, 1]  # lovelACe, grACe
    assert find_matches(people, "zzz") == []
    assert find_matches(people, "   ") == []                     # blank query
    # Match #1 of this search is contact #2 -- the distinction delete depends on.
    assert find_matches(people, "linus")[0][0] == 2


def check_add_list_update_delete(tmp: Path) -> None:
    path = tmp / "crud.json"

    # Add two, refuse a nameless third, list them.
    transcript = replay(
        [
            "1", "Ada Lovelace", "ada@example.com", "555-0100",
            "1", "Grace Hopper", "grace@example.com", "555-0200",
            "1", "   ",                       # whitespace-only name -> rejected
            "2",
            "6",
        ],
        path,
    )
    assert "A contact needs a name. Nothing added." in transcript
    assert "1. Ada Lovelace  | ada@example.com  | 555-0100" in transcript
    assert "2. Grace Hopper  | grace@example.com  | 555-0200" in transcript
    assert "Saved 2 contacts to crud.json. Bye!" in transcript
    assert len(load_contacts(path)) == 2

    # Update: keep the name, change the email, clear the phone.
    transcript = replay(
        ["4", "grace", "1", "", "grace@navy.mil", "-", "6"],
        path,
    )
    assert "Updated Grace Hopper." in transcript
    assert load_contacts(path)[1] == {
        "name": "Grace Hopper",
        "email": "grace@navy.mil",
        "phone": "",
    }

    # '-' clears an optional field but is refused for the name.
    transcript = replay(["4", "grace", "1", "-", "", "", "6"], path)
    assert "A contact needs a name; keeping it." in transcript
    assert load_contacts(path)[1]["name"] == "Grace Hopper"

    # Delete match #1 of a search that skipped contact #1: Grace must go, not Ada.
    transcript = replay(["5", "grace", "1", "y", "6"], path)
    assert "Deleted Grace Hopper." in transcript
    assert [c["name"] for c in load_contacts(path)] == ["Ada Lovelace"]

    # Declining the confirmation keeps the contact.
    transcript = replay(["5", "ada", "1", "n", "6"], path)
    assert "Cancelled." in transcript
    assert [c["name"] for c in load_contacts(path)] == ["Ada Lovelace"]


def check_bad_input(tmp: Path) -> None:
    path = tmp / "bad.json"
    save_contacts([{"name": "Ada Lovelace", "email": "", "phone": ""}], path)

    transcript = replay(
        [
            "7",            # out of range
            "",             # empty line
            "banana",       # nonsense
            "3", "",        # empty search query
            "3", "zzz",     # no hits
            "4", "zzz",     # update: nothing matches
            "5", "ada", "x",   # delete: pick is not a number
            "5", "ada", "\N{SUPERSCRIPT TWO}",  # isdigit() says yes, int() says no
            "5", "ada", "99",  # delete: pick out of range
            "?",            # reprint the menu
            "6",
        ],
        path,
    )
    for expected in [
        "'7' is not one of 1-6. Type ? for the menu.",
        "'' is not one of 1-6. Type ? for the menu.",
        "'banana' is not one of 1-6. Type ? for the menu.",
        "Found 0 matches.",
        "No match for 'zzz'. Nothing to update.",
        "'x' is not a number. Cancelled.",
        "'\N{SUPERSCRIPT TWO}' is not a number. Cancelled.",
        "There is no #99. Cancelled.",
        "1) Add contact",
    ]:
        assert expected in transcript, expected
    assert [c["name"] for c in load_contacts(path)] == ["Ada Lovelace"]


def check_autosave_survives_a_kill(tmp: Path) -> None:
    """Stretch 1: a session that never reaches option 6 still persists."""
    path = tmp / "kill.json"
    transcript = replay(["1", "Ada Lovelace", "ada@example.com", "555-0100"], path)
    assert "Interrupted. Saved 1 contact to kill.json." in transcript
    assert load_contacts(path)[0]["name"] == "Ada Lovelace"


def check_stretch(tmp: Path) -> None:
    people = [
        {"name": "linus torvalds", "email": "linus@kernel.org", "phone": "555-0300"},
        {"name": "Ada Lovelace", "email": "ada@example.com", "phone": "555-0100"},
        {"name": "Grace Hopper", "email": "grace@example.com", "phone": "555-0200"},
    ]

    # 2 -- sorting is case-insensitive and does not touch the stored names.
    assert [c["name"] for c in sorted_contacts(people)] == [
        "Ada Lovelace",
        "Grace Hopper",
        "linus torvalds",
    ]
    assert people[0]["name"] == "linus torvalds"  # original list untouched

    # 3 -- validation
    assert looks_like_email("ada@example.com")
    assert not looks_like_email("ada.example.com")
    assert not looks_like_email("ada@@example.com")
    assert not looks_like_email("@example.com")
    assert not looks_like_email("ada@example")
    assert looks_like_phone("555-0100")
    assert looks_like_phone("+44 (0)20 7946 0958")
    assert not looks_like_phone("call me")
    assert not looks_like_phone("12")
    assert validate(people[1]) == []
    assert validate({"name": "", "email": "", "phone": ""}) == ["name is empty"]
    assert validate({"name": "Ada", "email": "nope", "phone": "x"}) == [
        "'nope' does not look like an email address",
        "'x' does not look like a phone number",
    ]

    # 4 -- multi-field search finds people by email and phone too.
    assert [i for i, _ in find_matches_any_field(people, "kernel")] == [0]
    assert [i for i, _ in find_matches_any_field(people, "555-02")] == [2]
    assert [i for i, _ in find_matches_any_field(people, "example.com")] == [1, 2]
    assert find_matches(people, "kernel") == []  # name-only search does not

    # 5 -- CSV round trip
    csv_path = tmp / "contacts.csv"
    assert export_csv(people, csv_path) == 3
    assert csv_path.read_text(encoding="utf-8").splitlines()[0] == "name,email,phone"
    assert import_csv(csv_path) == people

    # 6 -- namedtuple records
    record = to_record(people[1])
    assert record == Contact("Ada Lovelace", "ada@example.com", "555-0100")
    assert record.name == record[0] == "Ada Lovelace"
    assert to_dict(record) == people[1]

    # 7 -- pagination
    many = [{"name": f"Person {n:02d}", "email": "", "phone": ""} for n in range(45)]
    chunks = pages(many, 20)
    assert [len(chunk) for chunk in chunks] == [20, 20, 5]
    assert pages([], 20) == []
    last = render_page(chunks[2], 2, len(chunks), 20).splitlines()
    assert last[0] == format_row(41, many[40])   # numbered across pages, not per page
    assert last[-1] == "-- page 3 of 3 --"

    # 8 -- undo restores in place, and snapshots are independent
    book = [dict(c) for c in people]
    history = History(limit=2)
    history.snapshot(book)
    book.pop()
    book[0]["name"] = "MUTATED"
    assert history.undo(book) is True
    assert [c["name"] for c in book] == [c["name"] for c in people]
    assert history.undo(book) is False   # nothing left to undo
    for _ in range(5):
        history.snapshot(book)
    assert len(history) == 2             # the limit is honoured

    # plural() -- the singular/plural rule the quit line depends on
    assert plural(1, "contact") == "1 contact"
    assert plural(0, "contact") == "0 contacts"
    assert plural(1, "match", "es") == "1 match"
    assert plural(3, "match", "es") == "3 matches"


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        check_sample_session(tmp)
        check_persistence(tmp)
        check_search_indexes()
        check_add_list_update_delete(tmp)
        check_bad_input(tmp)
        check_autosave_survives_a_kill(tmp)
        check_stretch(tmp)
    print("All checks passed.")


if __name__ == "__main__":
    main()
