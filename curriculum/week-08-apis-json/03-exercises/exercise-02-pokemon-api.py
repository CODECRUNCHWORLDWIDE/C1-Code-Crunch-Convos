"""Exercise 02 — Fetch a Pokémon from PokeAPI.

GOAL
----
Given a Pokémon name (default: "pikachu"), call PokeAPI and print:
  - name
  - height (in decimetres — that is what the API returns)
  - types (the list of type names, e.g. ['electric'])

PokeAPI is free, public, and needs no key. Docs: https://pokeapi.co/

EXPECTED OUTPUT for "pikachu":

    name:   pikachu
    height: 4 dm
    types:  electric

EXPECTED OUTPUT for "charizard":

    name:   charizard
    height: 17 dm
    types:  fire, flying

KEY CONCEPTS
------------
- Using f-strings to build a URL safely (PokeAPI takes the name in the
  path; for query params you would still use `params=`).
- Navigating nested JSON: a list of dicts where each dict has a nested
  dict — exactly what you will do constantly in the real world.
- Type hints on a function return value.

Reference:
  https://pokeapi.co/docs/v2#pokemon
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import requests


BASE_URL = "https://pokeapi.co/api/v2/pokemon"


@dataclass
class Pokemon:
    """A tiny, typed view of one Pokémon."""

    name: str
    height_dm: int  # decimetres
    types: list[str]


def fetch_pokemon(name: str, *, timeout: float = 5.0) -> Pokemon:
    """Fetch one Pokémon by name.

    Raises:
        requests.HTTPError: if PokeAPI returns 4xx/5xx (e.g. unknown name).
    """
    url = f"{BASE_URL}/{name.lower()}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data: dict = response.json()

    # `data["types"]` looks like:
    #   [{"slot": 1, "type": {"name": "electric", "url": "..."}}, ...]
    # We just want the inner names.
    type_names: list[str] = [entry["type"]["name"] for entry in data["types"]]

    return Pokemon(
        name=data["name"],
        height_dm=data["height"],
        types=type_names,
    )


def main() -> None:
    # Read the Pokémon name from the command line, default to "pikachu".
    requested = sys.argv[1] if len(sys.argv) > 1 else "pikachu"

    pokemon = fetch_pokemon(requested)

    print(f"name:   {pokemon.name}")
    print(f"height: {pokemon.height_dm} dm")
    print(f"types:  {', '.join(pokemon.types)}")


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────────────────────────────────
# Hints
# ─────────────────────────────────────────────────────────────────────────
# 1. PokeAPI is case-sensitive on the path. "Pikachu" returns 404 but
#    "pikachu" works — that is why we call `.lower()`.
# 2. Try `python exercise-02-pokemon-api.py charizard` to see types
#    with multiple entries.
# 3. To explore the full response, add `print(json.dumps(data, indent=2))`
#    inside `fetch_pokemon` temporarily. The response is huge — that is
#    why we filter it to just what we care about.
