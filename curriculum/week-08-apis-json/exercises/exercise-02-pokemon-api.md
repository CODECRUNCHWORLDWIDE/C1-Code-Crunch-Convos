# Exercise 2 — PokeAPI and Nested JSON

> **Topic:** walking a deeply nested JSON response and reducing it to one small typed record
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md)
> **Difficulty:** Easy
> **Target time:** 50 minutes
> **Why this one:** real API answers are enormous. One PokeAPI payload is about 290,000 characters and you need six things out of it. The skill is not "call the API" — it is walking a nested structure without guessing, and turning somebody else's sprawl into a small object your own code can lean on. Both challenges and the mini-project do exactly this.

## The Brief

[PokeAPI](https://pokeapi.co/) is a free, keyless, read-only API over the
Pokémon game data. `GET https://pokeapi.co/api/v2/pokemon/{name}` returns one
creature.

**Nested** means boxes inside boxes. A JSON document is made of two container
shapes: an **object**, which is a box with named compartments and becomes a
Python `dict`, and an **array**, which is a numbered row and becomes a Python
`list`. Either one can hold more of either one, as deep as the people who
designed it felt like going. PokeAPI felt like going quite deep: the types
arrive as a list of little boxes that each wrap *another* box, and the name you
want is inside that inner box.

You are building a card printer. Give it names on the command line and it
prints a compact summary of each. Everything else in the payload gets thrown
away, and that is the point — your program should depend on six fields, not on
three hundred.

Two traps are built into the data on purpose. Pikachu has one type, so code
that reads only the first entry looks correct and passes every test you would
have written; Bulbasaur has two, and the same code silently drops one. And
`height` is measured in decimetres while `weight` is in hectograms, which is to
say tenths of a metre and tenths of a kilogram, and neither field name mentions
it.

## Starter

Save this as `exercise-02-pokemon-api.py` and fill in every `TODO`.

```python
"""exercise-02-pokemon-api.py — reduce a large nested payload to a small record."""

import sys
from typing import Any, TypedDict

import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"
TIMEOUT_SECONDS = 5.0


class PokemonCard(TypedDict):
    """The six fields we display, lifted out of a much larger payload."""

    name: str
    number: int
    types: list[str]
    height_m: float
    weight_kg: float
    abilities: list[str]
    stat_total: int


def fetch_pokemon(name: str) -> dict[str, Any]:
    """Fetch the raw JSON payload for one Pokemon.

    Raises:
        requests.HTTPError: the name is unknown; the API answers 404.
    """
    # TODO: GET f"{BASE_URL}/{name.lower()}" with timeout=TIMEOUT_SECONDS
    # TODO: raise_for_status(), then return .json()
    raise NotImplementedError


def to_card(payload: dict[str, Any]) -> PokemonCard:
    """Reduce a raw payload to a PokemonCard (height dm, weight hg)."""
    # TODO: types      -> sort payload["types"] by "slot", read ["type"]["name"]
    # TODO: abilities  -> sort payload["abilities"] by "slot", read
    #                     ["ability"]["name"], append " (hidden)" when is_hidden
    # TODO: stat_total -> sum of s["base_stat"] for s in payload["stats"]
    raise NotImplementedError


def render(card: PokemonCard) -> str:
    """Format one card as the five aligned lines in Expected output."""
    raise NotImplementedError  # TODO


def main(argv: list[str]) -> int:
    """Print one card per name given on the command line."""
    names = argv[1:] or ["pikachu"]
    for name in names:
        print(render(to_card(fetch_pokemon(name))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

Here is the shape you are walking into, with everything you do not need cut
out. One `types` entry:

```json
{ "slot": 1, "type": { "name": "grass", "url": "https://pokeapi.co/api/v2/type/12/" } }
```

Read that from the outside in. `payload["types"]` is a list. Each element of
the list is an object with two compartments, `slot` and `type`. The `type`
compartment holds *another* object, and the name is in there. So the full path
to the word `grass` is `payload["types"][0]["type"]["name"]` — four steps, and
you should never write four steps you have not walked one at a time.

**`TypedDict`.** A `PokemonCard` is an ordinary dictionary at runtime. Nothing
is checked and nothing is enforced. What the `TypedDict` declaration buys you
is a written-down promise about which keys exist and what type each one holds,
so your editor can underline `card["numbr"]` before you ever run the program.

## Requirements

1. `fetch_pokemon()` lowercases the name before building the path, sets
   `timeout=`, and calls `raise_for_status()` before `.json()`.
2. `to_card()` returns every type, in slot order, joined with `", "`.
3. `height_m` is `payload["height"] / 10` and `weight_kg` is
   `payload["weight"] / 10`. Decimetres to metres, hectograms to kilograms.
4. `stat_total` sums `base_stat` across all entries of `payload["stats"]`. Do
   not hard-code six; sum whatever the list contains.
5. Abilities appear in slot order, and hidden ones are marked `(hidden)`.
6. Running with no arguments prints the Pikachu card. Running with
   `pikachu bulbasaur` prints both, in that order.

## Constraints

- **Sort `types` and `abilities` by `slot`; do not trust list order.** A JSON
  array *is* ordered, and today the entries happen to arrive in slot order. But
  `slot` is the field the data model uses to say "this one is the primary one";
  the position in the list is just how it got written down. Read the field that
  carries the meaning, not the accident, and your code survives a change on
  their side.

- **Use the `TypedDict`, not a bare `dict[str, Any]`.** The whole exercise is
  narrowing something loose into something known. If the return type stays
  `Any`, your editor cannot tell you that `card["numbr"]` is a typo, and you
  have done the work of narrowing without collecting the payoff.

- **Divide by 10 in `to_card()`, not in `render()`.** Convert foreign units at
  the boundary where the foreign data enters your program. Leave it to the
  formatter and the unit quirk has escaped: every future caller — a sort, a
  filter, a CSV export — has to remember it.

- **Set `timeout=` on the request.** Without one `requests` waits forever;
  there is no default. Ten names on the command line is ten chances to hang
  with nothing on screen.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3:

```text
$ python exercise-02-pokemon-api.py
--- replaying recorded payloads; pass fetch=fetch_live to go online ---
pikachu (#25)
  types      electric
  size       0.4 m, 6.0 kg
  abilities  static, lightning-rod (hidden)
  stat total 320

bulbasaur (#1)
  types      grass, poison
  size       0.7 m, 6.9 kg
  abilities  overgrow, chlorophyll (hidden)
  stat total 318

snorlax (#143)
  types      normal
  size       2.1 m, 460.0 kg
  abilities  immunity, thick-fat, gluttony (hidden)
  stat total 540
```

Your own program takes the three names on the command line —
`python exercise-02-pokemon-api.py pikachu bulbasaur snorlax` — because
requirement 6 asks you to default to Pikachu alone. The shipped file defaults
to all three instead, since Bulbasaur is the row that catches the bug and a
download nobody types arguments into should still show it.

Game data does not change, so these numbers are the numbers. If Bulbasaur
prints `grass` and stops, you read the first entry instead of the whole list.

## Steps

1. Open `https://pokeapi.co/api/v2/pokemon/bulbasaur` in a browser and find
   `types`, `abilities`, `stats`, `height`, `weight`. Your browser will show
   the JSON folded into a tree you can click open, which is the easiest way to
   see nesting there is.
2. Write `fetch_pokemon()`, then print `sorted(payload.keys())`. Seeing the
   full list of top-level keys once beats reading the documentation twice.
3. In the REPL, unpack one level at a time. Print `payload["types"]`. Then
   `payload["types"][0]`. Then `payload["types"][0]["type"]`. Then add
   `["name"]`. Never write a four-link chain you have not walked.
4. Write `to_card()`. Test it on Pikachu, then on Bulbasaur. The second one is
   the test that means something.
5. Write `render()`, run all three names, and compare with the block above.
6. Run a name that does not exist, such as `pikchu`, and read the traceback.
   Exercise 5 is where you turn that traceback into a message.

## The Solution

```python
"""exercise-02-pokemon-api-solution.py — reduce a large nested payload to a small record.

The exercise reads https://pokeapi.co/api/v2/pokemon/{name} and squeezes a
payload of several hundred keys down to the six a card needs.

This shipped answer does not call PokeAPI. It replays **recorded** payloads --
real bodies captured from that endpoint, trimmed to the keys this program
reads, and pasted in below -- so the download prints the same three cards with
no network at all.

The switch is one argument. ``main()`` passes ``fetch=fetch_recorded``; pass
``fetch=fetch_live``, or leave the argument off entirely, and the very same
``fetch_pokemon``, ``to_card`` and ``render`` call the real server.

Run it with::

    python exercise-02-pokemon-api-solution.py
    python exercise-02-pokemon-api-solution.py pikachu bulbasaur
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, TypedDict

import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"
TIMEOUT_SECONDS = 5.0

#: The names the download prints when you give it none. Your own version of
#: this exercise defaults to ["pikachu"] (requirement 6); the shipped answer
#: shows all three because Bulbasaur is the one that catches the bug.
DEMO_NAMES = ["pikachu", "bulbasaur", "snorlax"]

#: Real payloads captured from pokeapi.co, keyed by the name in the path.
#: Trimmed to the seven keys this program reads: the live documents also carry
#: sprites, moves, game appearances and cross-reference URLs, and run to about
#: 290,000 characters each. Nothing here was invented or edited -- only dropped.
RECORDED_POKEMON: dict[str, str] = {
    "pikachu": (
        '{"name": "pikachu", "id": 25, "types": [{"slot": 1, "type": '
        '{"name": "electric"}}], "abilities": [{"ability": {"name": '
        '"static"}, "is_hidden": false, "slot": 1}, {"ability": {"name": '
        '"lightning-rod"}, "is_hidden": true, "slot": 3}], "stats": '
        '[{"base_stat": 35, "stat": {"name": "hp"}}, {"base_stat": 55, '
        '"stat": {"name": "attack"}}, {"base_stat": 40, "stat": {"name": '
        '"defense"}}, {"base_stat": 50, "stat": {"name": '
        '"special-attack"}}, {"base_stat": 50, "stat": {"name": '
        '"special-defense"}}, {"base_stat": 90, "stat": {"name": '
        '"speed"}}], "height": 4, "weight": 60}'
    ),
    "bulbasaur": (
        '{"name": "bulbasaur", "id": 1, "types": [{"slot": 1, "type": '
        '{"name": "grass"}}, {"slot": 2, "type": {"name": "poison"}}], '
        '"abilities": [{"ability": {"name": "overgrow"}, "is_hidden": '
        'false, "slot": 1}, {"ability": {"name": "chlorophyll"}, '
        '"is_hidden": true, "slot": 3}], "stats": [{"base_stat": 45, '
        '"stat": {"name": "hp"}}, {"base_stat": 49, "stat": {"name": '
        '"attack"}}, {"base_stat": 49, "stat": {"name": "defense"}}, '
        '{"base_stat": 65, "stat": {"name": "special-attack"}}, '
        '{"base_stat": 65, "stat": {"name": "special-defense"}}, '
        '{"base_stat": 45, "stat": {"name": "speed"}}], "height": 7, '
        '"weight": 69}'
    ),
    "snorlax": (
        '{"name": "snorlax", "id": 143, "types": [{"slot": 1, "type": '
        '{"name": "normal"}}], "abilities": [{"ability": {"name": '
        '"immunity"}, "is_hidden": false, "slot": 1}, {"ability": '
        '{"name": "thick-fat"}, "is_hidden": false, "slot": 2}, '
        '{"ability": {"name": "gluttony"}, "is_hidden": true, "slot": '
        '3}], "stats": [{"base_stat": 160, "stat": {"name": "hp"}}, '
        '{"base_stat": 110, "stat": {"name": "attack"}}, {"base_stat": '
        '65, "stat": {"name": "defense"}}, {"base_stat": 65, "stat": '
        '{"name": "special-attack"}}, {"base_stat": 110, "stat": {"name":'
        ' "special-defense"}}, {"base_stat": 30, "stat": {"name": '
        '"speed"}}], "height": 21, "weight": 4600}'
    ),
}

#: Anything that turns a URL into a decoded JSON document. There are two in
#: this file: one that uses the network and one that does not.
Fetch = Callable[[str], dict[str, Any]]


class PokemonCard(TypedDict):
    """The six fields we display, lifted out of a much larger payload."""

    name: str
    number: int
    types: list[str]
    height_m: float
    weight_kg: float
    abilities: list[str]
    stat_total: int


def fetch_live(url: str) -> dict[str, Any]:
    """GET *url* for real and return the decoded JSON body.

    Args:
        url: Absolute https URL to call.

    Returns:
        The decoded payload, exactly as the API sent it.

    Raises:
        requests.HTTPError: the API answered 4xx or 5xx.
    """
    response = requests.get(url, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def fetch_recorded(url: str) -> dict[str, Any]:
    """Answer *url* from RECORDED_POKEMON, touching no network.

    Args:
        url: A URL ending in a name RECORDED_POKEMON knows.

    Returns:
        The decoded payload, parsed from the recorded text by the same
        json module the live path uses.

    Raises:
        requests.HTTPError: nothing was recorded for that name, which is
            what the live API does for a name it does not know.
    """
    name = url.rsplit("/", 1)[-1]
    if name not in RECORDED_POKEMON:
        raise requests.HTTPError(f"404 Client Error: Not Found for url: {url}")
    return json.loads(RECORDED_POKEMON[name])


def fetch_pokemon(name: str, *, fetch: Fetch = fetch_live) -> dict[str, Any]:
    """Fetch the raw JSON payload for one Pokemon.

    Args:
        name: Species name in any case; the path is lowercased for you.
        fetch: How to get the document. Defaults to the real network.

    Returns:
        The decoded payload, exactly as the API sent it.

    Raises:
        requests.HTTPError: the name is unknown; the API answers 404.
    """
    return fetch(f"{BASE_URL}/{name.lower()}")


def to_card(payload: dict[str, Any]) -> PokemonCard:
    """Reduce a raw payload to a PokemonCard (height dm, weight hg).

    Args:
        payload: One decoded /pokemon/{name} document.

    Returns:
        The six fields we display, with units converted to metres and kilograms.
    """
    types = [
        entry["type"]["name"]
        for entry in sorted(payload["types"], key=lambda entry: entry["slot"])
    ]
    abilities = [
        entry["ability"]["name"] + (" (hidden)" if entry["is_hidden"] else "")
        for entry in sorted(payload["abilities"], key=lambda entry: entry["slot"])
    ]
    return PokemonCard(
        name=payload["name"],
        number=payload["id"],
        types=types,
        height_m=payload["height"] / 10,
        weight_kg=payload["weight"] / 10,
        abilities=abilities,
        stat_total=sum(stat["base_stat"] for stat in payload["stats"]),
    )


def render(card: PokemonCard) -> str:
    """Format one card as the five aligned lines in Expected output.

    Args:
        card: A narrowed record from to_card().

    Returns:
        Five lines plus a trailing newline, so consecutive cards are separated
        by a blank line when printed.
    """
    rows = [
        ("types", ", ".join(card["types"])),
        ("size", f"{card['height_m']:.1f} m, {card['weight_kg']:.1f} kg"),
        ("abilities", ", ".join(card["abilities"])),
        ("stat total", str(card["stat_total"])),
    ]
    lines = [f"{card['name']} (#{card['number']})"]
    lines += [f"  {label:<11}{value}" for label, value in rows]
    return "\n".join(lines) + "\n"


def main(argv: list[str], *, fetch: Fetch = fetch_live) -> int:
    """Print one card per name given on the command line.

    Args:
        argv: The full argument vector, sys.argv style.
        fetch: How to get each document. Defaults to the real network.

    Returns:
        The process exit code.
    """
    names = argv[1:] or DEMO_NAMES
    for name in names:
        print(render(to_card(fetch_pokemon(name, fetch=fetch))))
    return 0


if __name__ == "__main__":
    print("--- replaying recorded payloads; pass fetch=fetch_live to go online ---")
    raise SystemExit(main(sys.argv, fetch=fetch_recorded))
```

**Three functions, three jobs, one direction of travel.** `fetch_pokemon` deals
with getting the document and knows nothing about cards. `to_card` deals with
the shape of the data and knows nothing about where it came from. `render`
deals with text and knows nothing about either. That separation is why the
shipped answer can run with no network: only the first function ever touches
one, so only the first function needs replacing.

**`fetch` is the seam.** `fetch_pokemon` does not call `requests.get`. It calls
whatever function it was handed, and the default is the real one. Hand it
`fetch_recorded` and it reads from a constant in the file instead. That is
**dependency injection**: the thing a function depends on is passed *in* rather
than reached for. `to_card` and `render` never learn that anything changed,
which is the proof that the boundary is in the right place.

**`fetch_recorded` raises the same exception the network would.** For a name it
does not know it raises `requests.HTTPError` with the message the real 404
produces, rather than a `KeyError`. A stand-in whose failures look different
from the real thing teaches you the stand-in, and the first time you meet a
real 404 you will not recognise it.

**`sorted(..., key=lambda entry: entry["slot"])` reads the intent.** One line,
and it means "primary first" instead of "whatever order they wrote it in".

**The conversion lives in `to_card`, and that is the load-bearing decision.**
Divide in `render` and the unit quirk is loose in your program. Divide once,
where the foreign data crosses into your code, and `height_m` means exactly
what it says everywhere after that. Naming a variable after a unit is a promise
you have to keep at the boundary or not at all.

**`stat_total` sums whatever is there.** A generator expression over
`payload["stats"]` is shorter than hard-coding six and immune to the day the
game adds a seventh stat.

**`render` returns a trailing newline on purpose.** `main` calls
`print(render(...))`. `print` adds one newline; the one inside `render` adds
the blank line that separates one card from the next. Remove it and the cards
run together.

**About `.lower()`.** Keep it — requirement 1 asks for it and it is right. But
keep it for the right reason. Lowercasing at the boundary means `Pikachu`,
`PIKACHU` and `pikachu` all become one path, one cache key, one log line, which
is worth having. It is **not** because the API rejects capitals. It does not,
and you can check in ten seconds:

```text
>>> for name in ("pikachu", "Pikachu", "PIKACHU"):
...     r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}", timeout=5)
...     print(name, r.status_code, len(r.content))
...
pikachu 200 290335
Pikachu 200 290335
PIKACHU 200 290335
```

Three identical bodies. An API that tolerates something today has not promised
to tolerate it tomorrow, and the documentation says lowercase — so normalise at
the boundary and stop thinking about it. That is a better reason than a
mistaken one.

## Run it

Copy the worked answer on this page into `exercise-02-pokemon-api.py` and run it:

```bash
python exercise-02-pokemon-api.py
```

It needs `requests` installed and **no internet**. The three payloads it prints
were captured from `pokeapi.co` and pasted into the file as
`RECORDED_POKEMON`, so the download works on a plane and on a network that
blocks unknown hosts.

They are trimmed. A live payload is about 290,000 characters — sprites, moves,
every game the creature has appeared in, and a cross-reference URL beside
almost every name. The recordings keep the seven keys this program reads and
drop the rest. Nothing was invented and nothing was edited; entire keys were
removed, and the file says so where they are defined.

To point the same code at the real API, change one argument at the bottom of
the file:

```python
raise SystemExit(main(sys.argv, fetch=fetch_live))
```

`fetch_live` is already in the file and is the default value of the parameter,
so deleting `fetch=fetch_recorded` also works. It takes names the recording
does not have, which is the point of going live.

The `-solution` in the filename keeps this file from colliding with your own
`exercise-02-pokemon-api.py`.

## Common bugs to catch

- **`TypeError: list indices must be integers or slices, not str`.**

  ```text
  Traceback (most recent call last):
    File "exercise-02-pokemon-api.py", line 21, in to_card
      types = payload["types"]["name"]
              ~~~~~~~~~~~~~~~~^^^^^^^^
  TypeError: list indices must be integers or slices, not str
  ```

  You wrote `payload["types"]["name"]`. `types` is a JSON array, so it is a
  Python list, and lists are indexed by number. You have to loop over it.

- **`KeyError: 'name'` inside the types loop.** You stopped one level early.
  Each entry is `{"slot": 1, "type": {"name": "grass", "url": "..."}}`, so the
  name lives at `entry["type"]["name"]`, not `entry["name"]`.

- **Only one type prints for Bulbasaur.**

  ```text
  bulbasaur (#1)
    types      grass
  ```

  You indexed the first element instead of iterating. This is the bug the
  exercise exists to catch, and it passes every test written against Pikachu.
  A one-element case cannot tell "first" apart from "all".

- **`size 4.0 m, 60.0 kg` for Pikachu.** You skipped the unit conversion.
  Nothing raised, because decimetres and metres are both just numbers. A
  four-metre, sixty-kilogram Pikachu is what a missing conversion looks like
  when the program is otherwise perfect.

- **`stat total 6`.** You counted the entries instead of adding their
  `base_stat` values. If every creature's total is a small single-digit number,
  this is why.

- **`requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://pokeapi.co/api/v2/pokemon/pikchu`.**
  The name is misspelled. This is correct behaviour — `raise_for_status()`
  stopped you before `.json()` could turn an error page into a confusing parse
  failure. Exercise 5 turns this traceback into a one-line message.

- **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.**
  You called `.json()` before `raise_for_status()`, and the body you tried to
  parse was an HTML error page. Status first, parse second, every time.

## Under the hood

<details>
<summary>Under the hood — what JSON has, and the four things it does not</summary>

JSON has exactly six types, and that is the whole list:

| JSON | Python |
|---|---|
| object | `dict` |
| array | `list` |
| string | `str` |
| number | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Everything you will ever receive from an API is built out of those six. Which
makes the absences worth knowing by heart, because each one is a bug waiting
for somebody.

**There is no date.** Not one. Every timestamp you have ever seen in an API
response was a string that you and the server agreed to read as a date —
usually `"2026-08-24T06:15"`, which is the ISO 8601 format, and which sorts
correctly as plain text precisely because it is written biggest-unit-first. If
you send a `datetime` object, Python will not even get as far as the network:

```text
TypeError: Object of type datetime is not JSON serializable
```

**There are no comments.** A `//` or a `#` in a JSON file is a parse error, not
a note. This is deliberate — the format's designer removed them after watching
people use comments to smuggle in parsing directives. If you want to explain a
field, add a field.

**Object keys are always strings.** Always, with no exception. So a Python dict
keyed by numbers does not survive the round trip:

```text
>>> import json
>>> json.loads(json.dumps({1: "a", 2: "b"}))
{'1': 'a', '2': 'b'}
```

Nothing raised. Your integer keys came back as text, and the next `data[1]`
raises `KeyError: 1` somewhere else entirely.

**There is no tuple and no set.** Both become arrays on the way out and lists
on the way back. Exercise 3 makes you watch that happen.

There is one more sharp edge, in numbers. JSON does not distinguish an integer
from a float — it has one number type — and it has no way to write `NaN` or
`Infinity` at all. Python's `json` module writes them anyway, as bare
`NaN`/`Infinity` tokens, which is convenient right up until a parser in another
language rejects the document. `json.dumps(value, allow_nan=False)` makes that
a loud local `ValueError` instead, and it is what `requests` does for you when
you use `json=`.

</details>

<details>
<summary>Under the hood — why narrowing at the boundary is worth the extra function</summary>

`to_card` exists to shrink a 290,000-character document into seven fields. It
would be less code to pass the payload around and read `payload["height"] / 10`
wherever you needed a height. Here is what that costs.

**Every reader becomes a dependency on their schema.** With the payload loose
in your program, a function three modules away is coupled to PokeAPI's exact
key names. Rename one key on their side and you are hunting for the breakage
across your whole codebase rather than fixing one function.

**Failures move away from their cause.** A missing key inside `to_card` fails
on the line that reads it, while the payload is still in front of you. The same
missing key read lazily, deep in a report generator, fails an hour into a batch
job with no clue about where the data came from.

**Units stop being invisible.** `payload["height"]` is a number with a unit
that lives only in the documentation. `card["height_m"]` carries its unit in
its name. That rename is the entire difference between the correct answer and
the four-metre Pikachu, and it is only possible because there is a boundary to
do the renaming at.

**Tests stop needing a network.** `to_card` and `render` take plain Python
values and return plain Python values. You can test both of them completely
with a saved payload and no internet — which is exactly what the shipped answer
on this page does, and exactly what Week 11 will formalise.

The pattern has a name outside this course: an **anti-corruption layer**. One
place where somebody else's model is translated into yours, so that their
choices stop at the border. It is worth the extra function every time the data
crosses a boundary you do not control.

</details>

## Acceptance checklist

- [ ] Bulbasaur prints both of its types, in slot order.
- [ ] Pikachu reads `0.4 m, 6.0 kg`, not `4.0 m, 60.0 kg`.
- [ ] `stat total` is `320` for Pikachu and `318` for Bulbasaur.
- [ ] Hidden abilities are marked and normal ones are not.
- [ ] `to_card()` is annotated `-> PokemonCard` and the request has `timeout=`.
- [ ] A misspelled name produces the API's 404 and no silent wrong answer.
- [ ] You can name the six JSON types without looking.
- [ ] Committed to Git with a message like `Add Week 8 exercise 2: PokeAPI card printer`.

## Stretch

- Add the sprite URL from `payload["sprites"]["front_default"]` to the card.
  The field is nullable in the API's schema, so treat `None` as a real
  possibility — `payload["sprites"]["front_default"] or "(no sprite)"` is
  enough. You will need `fetch_live` for this one; the recordings dropped
  `sprites`.

- Print the stats individually, sorted highest first, using
  `stat["stat"]["name"]` for the labels. For Snorlax that gives:

  ```text
  hp              160
  attack          110
  special-defense 110
  defense         65
  special-attack  65
  speed           30
  ```

- Reuse one `requests.Session` across every name on the command line and
  compare the runtime for ten names against ten separate `requests.get` calls.
  The session keeps the connection open instead of building a new one each
  time.

- Write your own `fetch_recorded` for a different API. Capture one real body,
  paste it in, and run your program against it. That is a **test fixture**, and
  you now know how to make one for anything.

When both types print for Bulbasaur, move on to
[Exercise 3 — Sending Data with POST](./exercise-03-post-data.md).
