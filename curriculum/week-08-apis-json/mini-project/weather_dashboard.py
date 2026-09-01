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
