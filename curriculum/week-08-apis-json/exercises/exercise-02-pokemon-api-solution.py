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
