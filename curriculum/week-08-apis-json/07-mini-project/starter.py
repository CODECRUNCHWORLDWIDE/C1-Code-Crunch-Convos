"""Weather dashboard CLI — starter file.

A skeleton you complete to satisfy the spec in README.md. Search for
`TODO` markers and replace each one with real code. The function
signatures and the main() flow are correct as given — do not change them
unless you have a reason.

USAGE
-----
    python starter.py "Paris"
    python starter.py "New York"
    python starter.py --history

APIS (no key required)
----------------------
    Geocoding: https://geocoding-api.open-meteo.com/v1/search
    Forecast:  https://api.open-meteo.com/v1/forecast
    Docs:      https://open-meteo.com/en/docs
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ─────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
HISTORY_FILE = Path(__file__).parent / "history.json"
DEFAULT_TIMEOUT = 5.0  # seconds


# A subset of the WMO weather codes used by Open-Meteo.
# Full table: https://open-meteo.com/en/docs (search "WMO Weather interpretation codes")
WEATHER_CODE_DESCRIPTIONS: dict[int, str] = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with light hail",
    99: "Thunderstorm with heavy hail",
}


# ─────────────────────────────────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────────────────────────────────


@dataclass
class Location:
    name: str
    country: str
    latitude: float
    longitude: float
    elevation_m: float


@dataclass
class CurrentWeather:
    temperature_c: float
    wind_kmh: float
    weather_code: int
    observed_at: str   # ISO timestamp as returned by the API


@dataclass
class DailyForecast:
    date: str          # "YYYY-MM-DD"
    weather_code: int
    temp_min_c: float
    temp_max_c: float


# ─────────────────────────────────────────────────────────────────────────
# HTTP session
# ─────────────────────────────────────────────────────────────────────────


def make_session() -> requests.Session:
    """Return a requests.Session configured with sensible defaults.

    - User-Agent identifies our app (Open-Meteo likes to know who's calling).
    - Automatic retries for transient 429/5xx responses on idempotent GETs.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "code-crunch-bootcamp/weather-dashboard (educational)",
        "Accept": "application/json",
    })
    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
        respect_retry_after_header=True,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


# ─────────────────────────────────────────────────────────────────────────
# API calls
# ─────────────────────────────────────────────────────────────────────────


def geocode(city: str, session: requests.Session, *, timeout: float = DEFAULT_TIMEOUT) -> Location | None:
    """Resolve a city name to a Location, or return None if not found."""
    # TODO:
    # 1. Call GET GEOCODING_URL with params={"name": city, "count": 1}.
    # 2. raise_for_status().
    # 3. Parse the JSON; the array of results is under the "results" key,
    #    but the key may be MISSING entirely if the city is unknown.
    #    Use data.get("results") or [] to handle both cases.
    # 4. If empty, return None.
    # 5. Otherwise return a Location built from the first result.
    raise NotImplementedError("Implement geocode()")


def fetch_forecast(
    location: Location,
    session: requests.Session,
    *,
    days: int = 4,
    timeout: float = DEFAULT_TIMEOUT,
) -> tuple[CurrentWeather, list[DailyForecast]]:
    """Fetch the current weather and a daily forecast for `location`.

    Returns:
        (current_weather, [today, day+1, day+2, day+3])

    Hint about the response shape:
        {
          "current_weather": {
              "temperature": 14.2,
              "windspeed": 18.0,
              "weathercode": 61,
              "time": "2026-05-13T16:00"
          },
          "daily": {
              "time":               ["2026-05-13", "2026-05-14", ...],
              "weather_code":       [61, 80, 2, 1],
              "temperature_2m_max": [14.8, 14.8, 17.0, 19.3],
              "temperature_2m_min": [ 9.2,  9.2, 10.1, 11.5]
          }
        }
    """
    # TODO:
    # 1. Build params with latitude, longitude, current_weather=true,
    #    daily="weather_code,temperature_2m_max,temperature_2m_min",
    #    forecast_days=days, timezone="auto".
    # 2. GET FORECAST_URL with those params.
    # 3. raise_for_status().
    # 4. Parse "current_weather" into a CurrentWeather instance.
    # 5. Parse "daily" — note that "daily" is a dict of parallel arrays;
    #    iterate by index to build a list[DailyForecast].
    # 6. Return (current, daily_list).
    raise NotImplementedError("Implement fetch_forecast()")


# ─────────────────────────────────────────────────────────────────────────
# Output
# ─────────────────────────────────────────────────────────────────────────


def describe_code(code: int) -> str:
    """Return a human-readable description for a WMO weather code."""
    return WEATHER_CODE_DESCRIPTIONS.get(code, f"Unknown code {code}")


def format_dashboard(
    location: Location,
    current: CurrentWeather,
    forecast: list[DailyForecast],
) -> str:
    """Build the multi-line dashboard string. No I/O — pure function."""
    # TODO: assemble a string roughly like the example in README.md.
    #   Header:       "Paris, France  (48.85°N, 2.35°E, 35 m)"
    #   Now line:     "Now: <description>, <temp>°C, wind <wind> km/h (as of <time>)"
    #   Forecast:     one indented line per DailyForecast, skipping index 0 (today)
    raise NotImplementedError("Implement format_dashboard()")


# ─────────────────────────────────────────────────────────────────────────
# History persistence
# ─────────────────────────────────────────────────────────────────────────


def save_history(location: Location, current: CurrentWeather, *, path: Path = HISTORY_FILE) -> None:
    """Append a record of this lookup to the history JSON file.

    The file is a JSON array of records. We load (or start with []),
    append, and re-write atomically-enough (rewrite the whole file).
    """
    # TODO:
    # 1. Build a record dict with at least: timestamp (UTC ISO), city,
    #    country, temperature_c.
    # 2. If path.exists(), load JSON; otherwise start with [].
    # 3. Append, then write back with indent=2 and ensure_ascii=False.
    raise NotImplementedError("Implement save_history()")


def load_history(*, path: Path = HISTORY_FILE) -> list[dict[str, Any]]:
    """Return the full history list (empty if the file is missing)."""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def print_history(*, limit: int = 10) -> None:
    """Print the last `limit` history entries, most recent first."""
    entries = load_history()
    if not entries:
        print("(no history yet)")
        return
    print("Recent lookups:")
    for entry in reversed(entries[-limit:]):
        ts = entry.get("timestamp", "?")
        city = entry.get("city", "?")
        country = entry.get("country", "?")
        print(f"  {ts}  {city}, {country}")


# ─────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Weather dashboard CLI using Open-Meteo.")
    parser.add_argument("city", nargs="*", help="City name (use quotes if it has spaces).")
    parser.add_argument("--history", action="store_true", help="Show recent lookups and exit.")
    parser.add_argument("--no-save", action="store_true", help="Don't append to history.json.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.history:
        print_history()
        return 0

    if not args.city:
        print("Error: please provide a city name (or --history).", file=sys.stderr)
        return 2

    city = " ".join(args.city).strip()

    with make_session() as session:
        try:
            location = geocode(city, session)
            if location is None:
                print(f"Error: could not find a city called {city!r}.", file=sys.stderr)
                return 1

            current, forecast = fetch_forecast(location, session)
        except requests.exceptions.RequestException as exc:
            print(f"Error: network/HTTP failure: {exc}", file=sys.stderr)
            return 1

    print(format_dashboard(location, current, forecast))

    if not args.no_save:
        save_history(location, current)
        print("\nSaved this lookup to history.json.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ─────────────────────────────────────────────────────────────────────────
# Implementation tips
# ─────────────────────────────────────────────────────────────────────────
# - `datetime.now(timezone.utc).isoformat(timespec="seconds")` produces
#   ISO-8601 timestamps you can sort lexically.
# - Open-Meteo's daily.time is a list of "YYYY-MM-DD" strings — they
#   already sort correctly in lexical order.
# - format_dashboard is the easiest function to test by eye. Get it
#   working with hard-coded dummy data first, then plug in the real
#   API calls.
# - If you implement the --hours stretch goal, the relevant params are
#   hourly=temperature_2m,weather_code and forecast_hours=N.
