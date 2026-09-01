# Mini-Project — Weather Dashboard CLI

> **Topic:** gluing every Week 8 habit — URLs, query parameters, JSON parsing, error handling — into one end-to-end tool
> **Lecture:** [01 — HTTP and REST](../lecture-notes/01-http-and-rest.md) · [02 — Using `requests`](../lecture-notes/02-using-requests.md) · [03 — Authentication and Secrets](../lecture-notes/03-authentication-and-secrets.md)
> **Difficulty:** Advanced
> **Target time:** 5–7 hours
> **Why this one:** it is the week's capstone, and it is the first program you write that talks to *two* services in a row — one call's answer becomes the next call's question. Along the way it uses every habit the week installed: a Session with a timeout and a retry, `raise_for_status()`, JSON navigation, a friendly error instead of a traceback, and a little local file to remember what it did.

<!-- no-runnable-file: this page is the project brief, and the project's deliverable is a folder in your own repository holding a script, a history file it produced, and a commit history. The runnable answer is weather_dashboard.py, which ships beside this page and is linked from Download and run. It is named after the project rather than the page because a file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

A weather app is really two questions asked in a row. First, *where is this
place?* — you have a city name, but a weather service speaks in latitude and
longitude, not "Paris". Second, *what is the weather at those coordinates?* The
answer to the first question is the input to the second. That hand-off is the
whole shape of the project.

You will use **[Open-Meteo](https://open-meteo.com/)**, which is free, needs
**no key and no signup**, and answers both questions on two endpoints:

```text
geocoding:  GET https://geocoding-api.open-meteo.com/v1/search?name=Paris&count=1
forecast:   GET https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true&daily=...
```

The geocoder hands back a `results` list; the first entry has `latitude`,
`longitude`, `country` and `elevation`. Feed those coordinates to the forecast
endpoint and it returns the current weather plus a day-by-day forecast, where
each day's sky is a **WMO weather code** — a small integer like `61` that you
translate into "Light rain".

The finished tool takes a city name and prints a clean dashboard:

```text
$ python weather.py "Paris"
Paris, France  (48.85°N, 2.35°E, 42 m)
──────────────────────────────────────
Now:  Light rain, 14.2°C, wind 18 km/h  (as of 2026-05-13 16:00)

3-day forecast:
  2026-05-14   Rain showers     lo   9.2°C   hi  14.8°C
  2026-05-15   Partly cloudy    lo  10.1°C   hi  17.0°C
  2026-05-16   Mainly clear     lo  11.5°C   hi  19.3°C
```

A city it cannot find gets a friendly line, not a stack trace:

```text
$ python weather.py "NotARealPlace"
Error: could not find a city called 'NotARealPlace'.
```

And every successful lookup is written to a little `history.json`, which a
`--history` flag reads back:

```text
$ python weather.py --history
Recent lookups:
  2026-05-13 16:02  Paris, France
```

The exact spacing and any emoji are up to you — the rubric grades behaviour, not
decoration.

**Why the shipped answer runs offline.** The real weather changes every hour, so
a live tool can never have a fixed "expected output". The reference answer
therefore hides the network behind a *seam* — the `fetch` argument — and by
default feeds it **recorded** Open-Meteo replies, so it prints the same
dashboard on every machine. Pass `--live` and the identical code calls the real
API. This is the same move Homework 3 and 6 make: put the thing you cannot
control behind a door you can open from the inside.

## Starter

There is no separate starter file — the stubs below are the whole of the
scaffolding, and they are the shape the finished tool takes. Save this as
`weather.py` in your project folder and fill in the `TODO`s. It runs as
pasted; it just reports that the dashboard is not built yet:

```python
"""Weather dashboard CLI — geocode a city, fetch its forecast, print it."""

from __future__ import annotations

import sys
from typing import Any, Callable, NamedTuple

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "code-crunch-bootcamp/1.0"

#: Anything that turns (url, params) into a decoded JSON document.
Fetch = Callable[[str, dict[str, Any]], dict[str, Any]]

#: One real Open-Meteo geocoder reply, so you can build this offline.
RECORDED: dict[str, dict[str, Any]] = {
    "https://geocoding-api.open-meteo.com/v1/search?count=1&name=Paris": {
        "results": [
            {"name": "Paris", "country": "France",
             "latitude": 48.85341, "longitude": 2.3488, "elevation": 42.0}
        ]
    },
}


class WeatherError(Exception):
    """Raised when a dashboard cannot be produced."""


class Place(NamedTuple):
    """One geocoded location."""
    name: str
    country: str
    latitude: float
    longitude: float
    elevation: float


def fetch_recorded(url: str, params: dict[str, Any]) -> dict[str, Any]:
    """Answer one request from RECORDED, touching no network."""
    query = "&".join(f"{k}={params[k]}" for k in sorted(params))
    key = f"{url}?{query}" if params else url
    recorded = RECORDED.get(key)
    if recorded is None:
        raise RuntimeError(f"no recorded reply for {key}; re-run with --live")
    return recorded


def geocode(city: str, *, fetch: Fetch) -> Place:
    """Turn a city name into a Place with coordinates."""
    payload = fetch(GEOCODE_URL, {"name": city, "count": 1})
    # TODO: read results[0]; raise WeatherError if the list is empty.
    return Place(city, "?", 0.0, 0.0, 0.0)


def fetch_forecast(place: Place, *, fetch: Fetch) -> dict[str, Any]:
    """Fetch the current weather and daily forecast for a Place."""
    # TODO: build the params (current_weather, daily, forecast_days, timezone)
    #       and call fetch(FORECAST_URL, params).
    return {"current_weather": {}, "daily": {}}


def decode_weather_code(code: int) -> str:
    """Turn a WMO weather code into a description."""
    # TODO: look code up in a small table; fall back to "Unknown (code N)".
    return "TODO"


def format_dashboard(place: Place, forecast: dict[str, Any]) -> str:
    """Build the dashboard text."""
    # TODO: header line, "Now" line, then the next three forecast days.
    return f"{place.name}: dashboard not built yet"


def main(argv: list[str] | None = None) -> int:
    """Geocode the city named in argv and print its dashboard."""
    args = sys.argv[1:] if argv is None else argv
    city = " ".join(args) or "Paris"
    place = geocode(city, fetch=fetch_recorded)
    forecast = fetch_forecast(place, fetch=fetch_recorded)
    print(format_dashboard(place, forecast))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**No setup needed — you can build this one in the browser.** The default path uses recorded replies, so it never touches the network. Open the starter in the [online code editor](../../../README.md) and run it there.

## Requirements

1. **CLI parsing with `argparse`.** A positional city name (which may contain
   spaces), a `--history` flag, and a `--live` flag that switches from the
   recording to the real API.
2. **Geocode the city.** Call the search endpoint with `name=<city>&count=1`.
   If the `results` list is empty or missing, raise `WeatherError` and exit
   non-zero with a friendly message.
3. **Fetch the weather.** Call the forecast endpoint with the geocoder's
   latitude and longitude, `current_weather=true`,
   `daily=weather_code,temperature_2m_max,temperature_2m_min`,
   `forecast_days=4` and `timezone=auto`.
4. **Decode `weather_code`** into a human-readable description with a small
   table, falling back gracefully on a code the table does not list.
5. **Print the dashboard** — a location header, a "Now" line, and the next
   three days.
6. **Save to history.** Append a JSON object (timestamp, city, country,
   temperature) to `history.json` on each successful lookup.
7. **`--history`** prints the most recent lookups, newest first.
8. **Robust error handling.** Every HTTP call has a `timeout=`. Network failures
   and 4xx/5xx responses print a short message and exit non-zero — no
   tracebacks for the user.

## Constraints

- **The network lives behind a seam, and the endpoints are keyless.** The
  `fetch` argument threaded through `geocode` and `fetch_forecast` is the seam:
  the default is a recording, so the tool prints the same dashboard every run
  and needs no connection; `--live` swaps in the real Open-Meteo. Weather that
  changes every hour is impossible to write an expected output for, which is the
  whole reason to record. Open-Meteo needs no key, so nothing secret is in play.

- **`timeout=` on every live request, always.** `requests` waits forever by
  default. A weather tool that hangs because a server accepted the connection
  and went quiet is worse than one that fails — a failure you can see, a hang
  you cannot.

- **`raise_for_status()` before `.json()` on the live path.** A `404` or `500`
  arrives as an HTML error page; without the check you get a confusing
  `JSONDecodeError` far from the real problem.

- **Two calls, one Session with a retry policy.** Build one `requests.Session`
  (Exercise 5's `make_session`) and send both calls through it. A transient
  `503` should be retried a few times with a growing pause; a `404` for a
  missing city should not — it will be missing on the retry too.

- **A friendly error is a caught error.** An unknown city, a dropped connection,
  a refused request — each becomes a `WeatherError` the `main` layer prints as
  one line before exiting non-zero. No bare `except Exception`, no `eval`, and
  no weather data hard-coded into the logic.

## Expected output

The shipped answer runs a demo when you give it no arguments: it geocodes Paris
from the recording, prints the dashboard, saves the lookup into a scratch
`history.json`, reads it back with `--history`, and shows the unknown-city path
— all offline, so the transcript is the same on every machine.

```text
$ python weather_dashboard.py
--- replaying Open-Meteo replies recorded on 2026-05-13; pass --live for real ---

Paris, France  (48.85°N, 2.35°E, 42 m)
──────────────────────────────────────
Now:  Light rain, 14.2°C, wind 18 km/h  (as of 2026-05-13 16:00)

3-day forecast:
  2026-05-14   Rain showers     lo   9.2°C   hi  14.8°C
  2026-05-15   Partly cloudy    lo  10.1°C   hi  17.0°C
  2026-05-16   Mainly clear     lo  11.5°C   hi  19.3°C

Saved this lookup to history.json.

Recent lookups:
  2026-05-13 16:02  Paris, France

unknown city -> WeatherError: could not find a city called 'NotARealPlace'.
```

Given a real city and `--live`, it does the real job:

```bash
python weather_dashboard.py "Tokyo" --live
```

## Steps

Build it in the order the data flows — that is also the order each stage is
easiest to test on its own.

1. **Geocode first, and print the raw `Place`.** Get `geocode` returning real
   coordinates for Paris from the recording before anything else exists. Handle
   the empty-`results` case now, while it is the only thing on screen.
2. **Then `fetch_forecast`.** Feed it the `Place` and print the raw dict. Check
   that `current_weather` and `daily` are both there.
3. **Then `decode_weather_code`.** A pure function — a dict lookup with a
   fallback. Test it on `0`, `61`, `95`, and a code you left out.
4. **Then `format_dashboard`.** Pure string work on data you already have.
   Compare it line by line against the brief's example.
5. **Then history.** `save_history` and `load_history` are independent of the
   API, so build them last and test them with a hand-written entry.
6. **Then `main`.** It is only glue: parse the args, call the four functions in
   order, catch `WeatherError`. Read it last.
7. **Now break it on purpose.** Point it at `"NotARealPlace"`. You want one
   friendly line and a non-zero exit, not a traceback.
8. **Only now try `--live`.** The offline path proved your logic; the live path
   proves your wiring.

## The Solution

The reference answer is one file. It keeps the function names the brief
suggests, adds a couple more, and threads the `fetch` seam and a `now` clock
seam through so the whole thing runs offline and deterministically.

```python
"""weather_dashboard.py — the finished answer to Week 8's mini-project.

A small command-line tool that turns a city name into a weather dashboard. It
wraps two free, keyless Open-Meteo endpoints:

    geocoding  city name  -> latitude / longitude / country / elevation
    forecast   lat, lon   -> current weather + a daily forecast

Base usage (matches the mini-project spec):

    python weather_dashboard.py "Paris"
    python weather_dashboard.py --history
    python weather_dashboard.py "Paris" --live

This shipped answer replays **recorded** replies by default -- real Open-Meteo
bodies captured on 2026-05-13 -- so the download prints the same dashboard every
time and needs no network. The weather changes every hour, which makes a live
run impossible to write an expected output for. The seam is the ``fetch``
argument threaded through ``geocode`` and ``fetch_forecast``: pass
``fetch_recorded`` and the identical code runs offline; pass ``--live`` and it
calls the real API with a ``timeout=``, a retry policy and ``raise_for_status()``.

Run it with no arguments and it walks through a worked example in a scratch
folder it cleans up on the way out.

Only "Paris" is in the recording. Offline lookups of any other city print a
"re-run with --live" note; live lookups work for any city on Earth.

Standard library plus ``requests``. Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, NamedTuple

import requests

# Box-drawing lines and the degree sign have to reach the terminal, and a
# legacy Windows console defaults to a code page that cannot encode them —
# printing one there raises UnicodeEncodeError before the first line lands.
# Switching this stream to UTF-8 makes the dashboard print on any terminal.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0

#: A slice of the WMO weather-code table Open-Meteo uses. Any code not listed
#: falls back to "Unknown (code N)" rather than crashing -- a forecast is still
#: useful when one day's icon is a guess.
WEATHER_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}

#: Anything that turns (url, params) into a decoded JSON document.
Fetch = Callable[[str, dict[str, Any]], dict[str, Any]]

#: Real Open-Meteo replies captured on 2026-05-13, keyed by the request that
#: produced them (see recorded_key). "NotARealPlace" is a real empty geocoder
#: answer, kept so the offline demo can show the unknown-city path.
RECORDED: dict[str, dict[str, Any]] = {
    "https://geocoding-api.open-meteo.com/v1/search?count=1&name=Paris": {
        "results": [
            {
                "name": "Paris",
                "country": "France",
                "latitude": 48.85341,
                "longitude": 2.3488,
                "elevation": 42.0,
            }
        ]
    },
    "https://geocoding-api.open-meteo.com/v1/search?count=1&name=NotARealPlace": {
        "generationtime_ms": 0.7,
    },
    "https://api.open-meteo.com/v1/forecast?current_weather=true"
    "&daily=weather_code,temperature_2m_max,temperature_2m_min"
    "&forecast_days=4&latitude=48.85341&longitude=2.3488&timezone=auto": {
        "latitude": 48.86,
        "longitude": 2.34,
        "timezone": "Europe/Paris",
        "current_weather": {
            "temperature": 14.2,
            "windspeed": 18.0,
            "weathercode": 61,
            "time": "2026-05-13T16:00",
        },
        "daily": {
            "time": ["2026-05-13", "2026-05-14", "2026-05-15", "2026-05-16"],
            "weather_code": [61, 80, 2, 1],
            "temperature_2m_max": [15.0, 14.8, 17.0, 19.3],
            "temperature_2m_min": [11.0, 9.2, 10.1, 11.5],
        },
    },
}


class WeatherError(Exception):
    """Raised when a dashboard cannot be produced, for any reason.

    Everything the user needs to read is in ``str(exc)``. Where the failure was
    a network error, the original cause stays reachable as ``__cause__``.
    """


class Place(NamedTuple):
    """One geocoded location, with everything the forecast call needs."""

    name: str
    country: str
    latitude: float
    longitude: float
    elevation: float


def recorded_key(url: str, params: dict[str, Any]) -> str:
    """Build the RECORDED key for one request.

    Args:
        url: The full endpoint URL.
        params: Query parameters, or an empty dict.

    Returns:
        The URL with its parameters appended in sorted order, so the key does
        not depend on the order a dict happened to be built in.
    """
    if not params:
        return url
    query = "&".join(f"{key}={params[key]}" for key in sorted(params))
    return f"{url}?{query}"


def make_session() -> requests.Session:
    """Build a Session with a User-Agent and a retry policy.

    The retry policy re-sends a GET a few times, with a growing pause between
    tries, when the server answers with a "try again" status or the connection
    drops. It never retries a 404 -- a missing city will still be missing.

    Returns:
        A configured Session.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_live(
    url: str, params: dict[str, Any], *, session: requests.Session, timeout: float
) -> dict[str, Any]:
    """GET one URL for real and return the decoded body.

    Args:
        url: The endpoint URL.
        params: Query parameters, sent through params= so they are encoded.
        session: The Session to send through.
        timeout: Seconds to wait before giving up.

    Returns:
        The decoded JSON document.

    Raises:
        WeatherError: the request failed or the server refused it.
    """
    try:
        response = session.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        raise WeatherError(f"could not reach {url}: {exc}") from exc


def fetch_recorded(url: str, params: dict[str, Any]) -> dict[str, Any]:
    """Answer one request from RECORDED, touching no network.

    Args:
        url: The endpoint URL.
        params: Query parameters.

    Returns:
        The decoded JSON document.

    Raises:
        RuntimeError: nothing was recorded for this request. Nothing is wrong
            with your code; only Paris is recorded. Re-run with --live.
    """
    key = recorded_key(url, params)
    recorded = RECORDED.get(key)
    if recorded is None:
        raise RuntimeError(f"no recorded reply for {key}; re-run with --live")
    return recorded


def geocode(city: str, *, fetch: Fetch) -> Place:
    """Turn a city name into a Place with coordinates.

    Args:
        city: The city name to look up.
        fetch: How to reach the geocoder.

    Returns:
        The first matching Place.

    Raises:
        WeatherError: no city of that name was found.
    """
    payload = fetch(GEOCODE_URL, {"name": city, "count": 1})
    results = payload.get("results") or []
    if not results:
        raise WeatherError(f"could not find a city called {city!r}.")
    top = results[0]
    return Place(
        name=top["name"],
        country=top.get("country", "?"),
        latitude=top["latitude"],
        longitude=top["longitude"],
        elevation=top.get("elevation", 0.0),
    )


def fetch_forecast(place: Place, *, fetch: Fetch) -> dict[str, Any]:
    """Fetch the current weather and daily forecast for a Place.

    Args:
        place: The location to fetch for.
        fetch: How to reach the forecast endpoint.

    Returns:
        The decoded forecast document.
    """
    params = {
        "latitude": place.latitude,
        "longitude": place.longitude,
        "current_weather": "true",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "forecast_days": 4,
        "timezone": "auto",
    }
    return fetch(FORECAST_URL, params)


def decode_weather_code(code: int) -> str:
    """Turn a WMO weather code into a short human-readable description.

    Args:
        code: The numeric weather code.

    Returns:
        A description, or "Unknown (code N)" for a code not in the table.
    """
    return WEATHER_CODES.get(code, f"Unknown (code {code})")


def format_coord(value: float, positive: str, negative: str) -> str:
    """Format one coordinate with a hemisphere letter.

    Args:
        value: The signed latitude or longitude.
        positive: Letter for a non-negative value ("N" or "E").
        negative: Letter for a negative value ("S" or "W").

    Returns:
        A string like "48.85 deg N", using a real degree sign.
    """
    letter = positive if value >= 0 else negative
    return f"{abs(value):.2f}°{letter}"


def format_dashboard(place: Place, forecast: dict[str, Any]) -> str:
    """Build the dashboard text for one place and its forecast.

    Args:
        place: The geocoded location.
        forecast: The forecast document from fetch_forecast.

    Returns:
        The full dashboard as one multi-line string.
    """
    current = forecast["current_weather"]
    daily = forecast["daily"]

    lat = format_coord(place.latitude, "N", "S")
    lon = format_coord(place.longitude, "E", "W")
    header = f"{place.name}, {place.country}  ({lat}, {lon}, {place.elevation:.0f} m)"

    lines = [header, "─" * len(header)]
    when = current["time"].replace("T", " ")
    lines.append(
        f"Now:  {decode_weather_code(current['weathercode'])}, "
        f"{current['temperature']:.1f}°C, "
        f"wind {current['windspeed']:.0f} km/h  (as of {when})"
    )
    lines.append("")
    lines.append("3-day forecast:")

    times = daily["time"]
    codes = daily["weather_code"]
    highs = daily["temperature_2m_max"]
    lows = daily["temperature_2m_min"]
    # Index 0 is today, already shown on the "Now" line; show the next three.
    for day in range(1, len(times)):
        desc = decode_weather_code(codes[day])
        lines.append(
            f"  {times[day]}   {desc:<16} "
            f"lo {lows[day]:>5.1f}°C   hi {highs[day]:>5.1f}°C"
        )
    return "\n".join(lines)


def make_entry(place: Place, forecast: dict[str, Any], *, now: Callable[[], datetime]) -> dict[str, Any]:
    """Build one history entry for a completed lookup.

    The clock is a seam (the ``now`` argument) for the same reason the network
    is: a wall-clock timestamp is impossible to write an expected output for, so
    the demo passes a fixed clock and real runs pass ``datetime.now``.

    Args:
        place: The geocoded location.
        forecast: The forecast document.
        now: A callable returning the current time.

    Returns:
        A JSON-serialisable dict for the history file.
    """
    return {
        "looked_up_at": now().strftime("%Y-%m-%d %H:%M"),
        "city": place.name,
        "country": place.country,
        "temperature_c": forecast["current_weather"]["temperature"],
    }


def load_history(path: Path) -> list[dict[str, Any]]:
    """Read the history file, returning an empty list if it does not exist.

    Args:
        path: The history file.

    Returns:
        The list of recorded lookups, oldest first.
    """
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_history(path: Path, entry: dict[str, Any]) -> None:
    """Append one entry to the history file.

    Args:
        path: The history file.
        entry: The lookup to record.
    """
    history = load_history(path)
    history.append(entry)
    with path.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
        f.write("\n")


def format_history(history: list[dict[str, Any]], limit: int = 10) -> str:
    """Format the most recent lookups, newest first.

    Args:
        history: The full history, oldest first.
        limit: How many recent entries to show.

    Returns:
        The listing as one multi-line string.
    """
    lines = ["Recent lookups:"]
    for entry in list(reversed(history))[:limit]:
        lines.append(f"  {entry['looked_up_at']}  {entry['city']}, {entry['country']}")
    return "\n".join(lines)


def run(
    argv: list[str],
    *,
    fetch: Fetch | None = None,
    now: Callable[[], datetime] = datetime.now,
) -> int:
    """Parse arguments, build the dashboard, print it.

    Args:
        argv: Command-line arguments, without the program name.
        fetch: How to reach the API. None means "decide from --live".
        now: The clock used for history timestamps.

    Returns:
        The process exit code. 0 on success, 1 on a handled failure.
    """
    parser = argparse.ArgumentParser(
        prog="weather_dashboard.py",
        description="Print a weather dashboard for a city.",
    )
    parser.add_argument("city", nargs="*", help="city name (may contain spaces)")
    parser.add_argument(
        "--history", action="store_true", help="show recent lookups and exit"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="do not record this lookup"
    )
    parser.add_argument(
        "--history-file", type=Path, default=Path("history.json"), metavar="PATH"
    )
    parser.add_argument("--live", action="store_true", help="call the real API")
    args = parser.parse_args(argv)

    if fetch is not None:
        get: Fetch = fetch
    elif args.live:
        session = make_session()
        get = lambda url, params: fetch_live(
            url, params, session=session, timeout=TIMEOUT_SECONDS
        )
    else:
        get = fetch_recorded

    if args.history:
        history = load_history(args.history_file)
        print(format_history(history) if history else "No lookups yet.")
        return 0

    if not args.city:
        parser.error("give a city name, or --history")
    city = " ".join(args.city)

    try:
        place = geocode(city, fetch=get)
        forecast = fetch_forecast(place, fetch=get)
    except WeatherError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    print(format_dashboard(place, forecast))

    if not args.no_save:
        save_history(args.history_file, make_entry(place, forecast, now=now))
        print()
        print(f"Saved this lookup to {args.history_file.as_posix()}.")
    return 0


def _demo() -> int:
    """Walk through a worked example in a scratch folder, then clean it up.

    Everything is offline: the recording answers the API calls and a fixed clock
    stamps the history entry, so the transcript is the same on every machine.

    Returns:
        The exit code of the successful lookup.
    """
    print("--- replaying Open-Meteo replies recorded on 2026-05-13; pass --live for real ---")
    print()
    fixed_now: Callable[[], datetime] = lambda: datetime(2026, 5, 13, 16, 2)

    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="weather_dashboard_") as scratch:
        try:
            os.chdir(scratch)
            code = run(["Paris"], fetch=fetch_recorded, now=fixed_now)
            print()
            run(["--history"], fetch=fetch_recorded, now=fixed_now)
            print()
            # An unknown city: geocode raises, and run() sends the message to
            # stderr the way a CLI should. The demo shows it on stdout so the
            # transcript is complete.
            try:
                geocode("NotARealPlace", fetch=fetch_recorded)
            except WeatherError as err:
                print(f"unknown city -> WeatherError: {err}")
        finally:
            os.chdir(home)
    return code


def main(argv: list[str] | None = None) -> int:
    """Run the tool, or the built-in demo when no arguments are given.

    Args:
        argv: Command-line arguments, without the program name. None means read
            them from sys.argv.

    Returns:
        The process exit code.
    """
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return _demo()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

**Why it works.**

**The whole program is two calls chained through a seam.** `geocode` turns a
name into a `Place`; `fetch_forecast` turns that `Place` into weather. Neither
one says `requests.get` in its own body — both say `fetch`, the argument. Build
the tool normally and `fetch` is the real network (through one Session with a
timeout and a retry). Build it in the demo and `fetch` is `fetch_recorded`, so
the identical two-call chain runs with no network at all. That single argument
is what makes the whole thing testable and what lets this page have a fixed
expected output for a tool whose real answer changes every hour.

**The boundary is crossed exactly once, and everything after it is yours.** The
API speaks in `results` lists, decimetres of elevation, `weathercode` integers
and a `weathercode`/`weather_code` spelling that is genuinely inconsistent
between the two halves of the forecast response. `geocode` converts all of the
first call's foreignness into a tidy `Place`, and `format_dashboard` never has
to know the geocoder existed. That is this week's one idea — *treat the boundary
as the boundary* — applied to a two-hop program.

**`decode_weather_code` guesses rather than crashes.** A weather code the table
does not list returns `"Unknown (code 96)"`, not a `KeyError`. A forecast with
one unfamiliar icon is still a useful forecast; a forecast that crashes on day
four helps nobody. `dict.get(code, default)` is the whole technique.

**The retry policy is on the transport, and it knows what not to retry.**
`make_session` retries a `503` or a dropped connection a few times with a
growing pause, because those are usually temporary. It does **not** retry a
`404`, because a city that is missing now will be missing on the retry — retrying
it just makes the user wait longer for the same "not found". Choosing *which*
failures are worth retrying is the actual skill; the `Retry` object is just where
you write the choice down.

**The clock is a seam too.** History entries carry a timestamp, and a wall-clock
timestamp would make the demo print something different every run. So the time
comes from a `now` argument, defaulting to `datetime.now` for real use and set
to a fixed instant in the demo. It is the exact same move as the `fetch` seam,
applied to time instead of the network — the lesson Homework 3 drills.

**Diagnostics and results go to different places.** The dashboard and the
history listing are results, and they go to stdout. The unknown-city message
goes to stderr, so `python weather.py Paris > today.txt` saves the forecast and
leaves the errors on screen. That split is why the two are separated.

## Download and run

The answer to this project is a **folder in your own repository** — your
`weather.py`, the `history.json` it produced, and a commit history showing how
you got there. That is why this page carries no `README.py`.

The runnable answer ships beside it, named after the project:

Download [weather_dashboard.py](./weather_dashboard.py) and run it:

```bash
python weather_dashboard.py
```

With no arguments it geocodes Paris from the recording, prints the dashboard,
saves and reads back a history entry in a temporary folder, and deletes the
folder on the way out — so it works from a clean checkout with nothing set up.
Point it at any city and add `--live` to hit the real Open-Meteo:

```bash
python weather_dashboard.py "Tokyo" --live
```

Save your own copy as `weather.py` in your project folder, and commit that one.
The longer download name is there so it cannot overwrite your work.

## Common bugs to catch

- **Feeding the city name straight to the forecast endpoint.** The forecast API
  has no idea what "Paris" is — it only speaks coordinates. Skipping the
  geocoding step gives you an empty or error response. The two calls are in that
  order for a reason: the first answers "where", the second answers "what".

- **Assuming `results` is always there.** A misspelled city returns a body with
  **no** `results` key at all, not an empty list. `payload["results"][0]` then
  raises `KeyError`, and `payload.get("results")[0]` raises `TypeError` on the
  `None`. `payload.get("results") or []` handles both — missing key and empty
  list — in one line.

- **`weathercode` vs `weather_code`.** The current-weather block spells it
  `weathercode` (no underscore); the daily block you asked for with
  `daily=weather_code` spells it `weather_code`. Read one with the other's
  spelling and you get a `KeyError`. This is a real inconsistency in the API, not
  a typo in the brief — copy the spellings exactly.

- **No `timeout=`.** The one run where a server is slow, your tool hangs with no
  output and no error, and nothing in the code looks wrong.

- **Letting a bad city reach the user as a traceback.** It does exit non-zero —
  eventually, after a wall of `KeyError`. The brief asks for one friendly line
  and a clean exit, which is what catching `WeatherError` in `main` gives you.

- **Building the forecast URL with an f-string.** The `daily` parameter has
  commas in it and the coordinates are floats; hand-built URLs get the encoding
  wrong. `params=` lets `requests` do it correctly.

- **Hard-coding the dashboard.** Tempting when you are matching an example
  output, and it passes exactly one test — the one you looked at. The rubric
  runs a city you did not.

## Under the hood

<details>
<summary>Under the hood — why ISO dates let the history sort itself</summary>

The history entries store their date as a string like `"2026-05-13 16:02"`, and
`--history` shows them newest first. It would be natural to reach for
`datetime.strptime` to parse each one before sorting — but you never need to.

Open-Meteo, like most of the modern web, uses **ISO 8601** dates:
`YYYY-MM-DD HH:MM`, biggest unit first. That ordering is not a cosmetic choice.
It means the **text** order of two ISO timestamps is the same as their **time**
order — `"2026-05-12"` sorts before `"2026-05-13"` as plain strings, with no
parsing at all, because the characters that differ are the ones that matter and
they are in the right place.

So appending to the list keeps it in time order for free (each new entry is
later than the last), and `reversed(history)` gives newest-first without a
`key=` function or a single `datetime` object. The moment your timestamps mix
time zones this breaks and you must parse — but for a single-machine history
file it is the format where the lazy thing is also the correct thing.

This is the same property the Week 6 log analyzer leaned on to find the earliest
and latest entry by sorting strings. It is worth internalising: **choose ISO
8601 for any date you store, and half your date handling disappears.**

</details>

<details>
<summary>Under the hood — one Session, two hosts, and why the retry lives there</summary>

The geocoder and the forecast live on two different hostnames —
`geocoding-api.open-meteo.com` and `api.open-meteo.com` — yet the tool sends both
through **one** `Session`. That is fine, and it is worth understanding why.

A `Session` is not tied to a host. It is a bundle of shared state — default
headers (the `User-Agent`), a connection pool, and the mounted adapters — that
rides along with every request you send through it. When it meets a new host it
opens a fresh connection for that host and keeps it in the pool alongside the
others. So the single `User-Agent` and the single `Retry` policy apply to both
calls, and each host still gets its own reused connection.

The retry lives on the adapter, mounted onto the Session, rather than being
written by hand around each call, because retrying correctly is more subtle than
a `for` loop with a `sleep`:

- **Backoff.** `backoff_factor=0.5` waits longer after each failure —
  roughly 0.5s, then 1s, then 2s — so a server that is briefly overloaded gets
  breathing room instead of a tighter hammering.
- **Only some statuses.** `status_forcelist` retries `429` (rate limited) and
  the `5xx` family (server errors), which are usually transient. A `404` is not
  in the list, so a missing city fails immediately.
- **Only idempotent methods.** `allowed_methods=("GET",)` means only reads are
  retried. Retrying a `POST` could submit a form twice — the exact hazard
  Homework 1's idempotency table is about.

Writing all three of those correctly by hand, for two calls, is how a five-line
retry loop becomes a source of bugs. The adapter is where the library already
solved it.

</details>

## Acceptance checklist

- [ ] `python weather.py "Paris"` prints a header, a "Now" line and three
      forecast days.
- [ ] An unknown city prints one friendly line and exits non-zero — no
      traceback.
- [ ] Every HTTP call passes `timeout=` and goes through one Session.
- [ ] `raise_for_status()` is called before `.json()` on the live path.
- [ ] `weather_code` is decoded through a table with a graceful fallback.
- [ ] Each successful lookup appends to `history.json`, and `--history` reads it
      back newest-first.
- [ ] `results` missing *and* `results` empty are both handled without a
      `KeyError` or `TypeError`.
- [ ] No bare `except Exception`, no `eval`, no hard-coded weather data.
- [ ] Every function has type hints and a docstring.
- [ ] Committed in stages, not one lump, and pushed to your fork.

## Stretch

1. **Hourly forecast.** A `--hours N` flag that prints the next N hours, using
   `hourly=temperature_2m,weather_code`.
2. **Several cities at once.** `python weather.py Paris Tokyo Lima` prints each
   dashboard, separated by a rule.
3. **Cache the geocoder.** A city's coordinates never change, so remember them
   in a small JSON file and skip the first call on a repeat lookup.
4. **A real weather symbol.** Map each `weather_code` to an emoji as well as a
   description, and print it in the forecast rows.
5. **Unit-test the decoder.** `decode_weather_code` is a pure function with no
   I/O — write a handful of `assert`s for it now, as a preview of Week 11.
6. **CSV export.** `--export-csv FILE` writes the daily forecast as CSV, reusing
   Week 6's `csv.writer` patterns.

## Up next

You have spent Week 8 *calling* other people's HTTP APIs. Next is
[Week 9 — Web Development with Flask](../../week-09-web-development-flask/), where
you cross to the other side and *build* one — the server that answers requests
exactly like the ones this dashboard sent. Every status code, JSON body and
query parameter you learned to read, you will now learn to write.
