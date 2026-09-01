"""weather.py -- Week 8 mini-project reference implementation.

A command-line weather dashboard built on Open-Meteo (free, no key, no signup).

    python weather.py "Paris"
    python weather.py Paris Tokyo Lima
    python weather.py "Paris" --hours 6
    python weather.py --history
    python weather.py "Paris" --export-csv paris.csv

Two endpoints do all the work:

    GET https://geocoding-api.open-meteo.com/v1/search   city name -> lat/lon
    GET https://api.open-meteo.com/v1/forecast           lat/lon   -> weather

Everything else in this file is the discipline the mini-project is actually
grading: one `timeout=` on every call, a `Session` with a retry policy, narrow
`except` clauses, small typed functions, and a `main()` that returns an exit
code instead of raising a traceback at the user.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Every outbound call gets this. Never call an API without a timeout: the
# default in `requests` is "wait forever", and a hung CLI looks like a bug in
# your code long before it looks like a bug in theirs.
TIMEOUT_SECONDS = 8.0

USER_AGENT = "code-crunch-bootcamp/1.0 (week-08 weather CLI)"

# Files live next to the script so a run from any directory finds them.
DEFAULT_HISTORY = Path(__file__).with_name("history.json")
DEFAULT_CACHE = Path(__file__).with_name("cache.json")

# Geocoding answers never change (Paris does not move), so cache them forever.
# Weather does change, so cache it for ten minutes.
GEOCODE_TTL_SECONDS = float("inf")
FORECAST_TTL_SECONDS = 600.0

# WMO weather interpretation codes, from the "Weather variable documentation"
# table at https://open-meteo.com/en/docs. Both `current_weather.weathercode`
# and `daily.weather_code` use this scale.
WEATHER_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# One emoji per code band. Ranges, not 27 entries, because the WMO scale is
# already grouped: 5x drizzle, 6x rain, 7x snow, 8x showers, 9x thunder.
_EMOJI_BANDS: tuple[tuple[range, str], ...] = (
    (range(0, 1), "☀️"),   # sun
    (range(1, 3), "⛅"),         # sun behind cloud
    (range(3, 4), "☁️"),   # cloud
    (range(45, 49), "\U0001f32b️"),  # fog
    (range(51, 58), "\U0001f327️"),  # drizzle
    (range(61, 68), "☔"),       # rain
    (range(71, 78), "❄️"),  # snow
    (range(80, 83), "\U0001f326️"),  # showers
    (range(85, 87), "\U0001f328️"),  # snow showers
    (range(95, 100), "⛈️"),  # thunder
)

_ASCII_BANDS: tuple[tuple[range, str], ...] = (
    (range(0, 1), "(o)"),
    (range(1, 3), "(-)"),
    (range(3, 4), "(=)"),
    (range(45, 49), "(~)"),
    (range(51, 58), "(')"),
    (range(61, 68), "(,)"),
    (range(71, 78), "(*)"),
    (range(80, 83), "(,)"),
    (range(85, 87), "(*)"),
    (range(95, 100), "(!)"),
)


class WeatherError(Exception):
    """Anything the user should see as one line of English, not a traceback."""


# --------------------------------------------------------------------------
# Data shapes
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Place:
    """One geocoding hit, trimmed to the five fields the dashboard prints."""

    name: str
    country: str
    latitude: float
    longitude: float
    elevation: float


@dataclass(frozen=True)
class Current:
    """The `current_weather` block."""

    time: str
    temperature: float
    windspeed: float
    code: int


@dataclass(frozen=True)
class Day:
    """One row of the `daily` block."""

    date: str
    code: int
    low: float
    high: float


@dataclass(frozen=True)
class Hour:
    """One row of the `hourly` block (used only by --hours)."""

    time: str
    temperature: float
    code: int


@dataclass(frozen=True)
class Forecast:
    """Everything one forecast call returned, already unpacked."""

    current: Current
    days: list[Day]
    temp_unit: str
    wind_unit: str
    hours: list[Hour] = field(default_factory=list)


# --------------------------------------------------------------------------
# HTTP plumbing
# --------------------------------------------------------------------------


def make_session() -> requests.Session:
    """Build a Session with a descriptive User-Agent and a retry policy.

    `Retry` only fires for the statuses in `status_forcelist` and only for the
    methods in `allowed_methods`. A 404 is *not* retried -- the city will still
    be missing on the fourth attempt, and burning three extra requests on a
    permanent failure is rude.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    retry = Retry(
        total=3,
        backoff_factor=1.0,                          # sleeps 0s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_json(
    session: requests.Session,
    url: str,
    params: dict[str, Any],
    *,
    timeout: float = TIMEOUT_SECONDS,
) -> Any:
    """GET `url` and return the parsed JSON body, or raise `WeatherError`.

    This is the only place in the file that touches the network, so it is the
    only place that has to know about `requests` exception types. Every caller
    above it deals in `WeatherError` and plain Python objects.
    """
    try:
        response = session.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as exc:
        raise WeatherError(f"{url} did not answer within {timeout:.0f}s.") from exc
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "?"
        raise WeatherError(f"{url} returned HTTP {status}.") from exc
    except requests.RequestException as exc:
        raise WeatherError(f"could not reach {url} ({exc.__class__.__name__}).") from exc
    except ValueError as exc:
        # requests.exceptions.JSONDecodeError subclasses ValueError.
        raise WeatherError(f"{url} did not return JSON.") from exc


# --------------------------------------------------------------------------
# Cache (stretch goal 3)
# --------------------------------------------------------------------------


def _load_cache(path: Path) -> dict[str, Any]:
    """Read the on-disk cache. A corrupt or missing cache is simply empty."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def cache_get(path: Path, key: str, ttl: float) -> Any | None:
    """Return the cached value for `key` if it is younger than `ttl` seconds."""
    entry = _load_cache(path).get(key)
    if not isinstance(entry, dict) or "stored_at" not in entry:
        return None
    if time.time() - float(entry["stored_at"]) > ttl:
        return None
    return entry.get("value")


def cache_put(path: Path, key: str, value: Any) -> None:
    """Store `value` under `key`. Cache failures must never break a lookup."""
    cache = _load_cache(path)
    cache[key] = {"stored_at": time.time(), "value": value}
    try:
        path.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    except OSError:
        pass


# --------------------------------------------------------------------------
# API calls
# --------------------------------------------------------------------------


def geocode(
    session: requests.Session,
    city: str,
    *,
    cache_path: Path | None = DEFAULT_CACHE,
) -> Place:
    """Resolve a city name to coordinates using Open-Meteo's geocoder."""
    key = f"geocode:{city.strip().lower()}"
    if cache_path is not None:
        cached = cache_get(cache_path, key, GEOCODE_TTL_SECONDS)
        if isinstance(cached, dict):
            return Place(**cached)

    payload = get_json(session, GEOCODE_URL, {"name": city, "count": 1})

    # The geocoder answers 200 with NO "results" key at all when nothing
    # matches -- it does not 404 and it does not send an empty list. `or []`
    # collapses both "missing" and "null" into the same empty case.
    results = payload.get("results") or []
    if not results:
        raise WeatherError(f"could not find a city called {city!r}.")

    hit = results[0]
    place = Place(
        name=str(hit.get("name", city)),
        country=str(hit.get("country", "")),
        latitude=float(hit["latitude"]),
        longitude=float(hit["longitude"]),
        elevation=float(hit.get("elevation", 0.0)),
    )
    if cache_path is not None:
        cache_put(cache_path, key, place.__dict__)
    return place


def fetch_forecast(
    session: requests.Session,
    place: Place,
    *,
    hours: int = 0,
    cache_path: Path | None = DEFAULT_CACHE,
) -> Forecast:
    """Fetch current conditions plus today + the next three days."""
    params: dict[str, Any] = {
        "latitude": place.latitude,
        "longitude": place.longitude,
        "current_weather": "true",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "forecast_days": 4,
        "timezone": "auto",
    }
    if hours > 0:
        params["hourly"] = "temperature_2m,weather_code"

    key = f"forecast:{place.latitude},{place.longitude},hours={hours > 0}"
    payload: Any = None
    if cache_path is not None:
        payload = cache_get(cache_path, key, FORECAST_TTL_SECONDS)
    if payload is None:
        payload = get_json(session, FORECAST_URL, params)
        if cache_path is not None:
            cache_put(cache_path, key, payload)

    return parse_forecast(payload, hours=hours)


def parse_forecast(payload: dict[str, Any], *, hours: int = 0) -> Forecast:
    """Turn one raw forecast document into a `Forecast`. No I/O -- testable."""
    current_raw = payload.get("current_weather")
    if not isinstance(current_raw, dict):
        raise WeatherError("the forecast response had no current_weather block.")

    current = Current(
        time=str(current_raw["time"]),
        temperature=float(current_raw["temperature"]),
        windspeed=float(current_raw["windspeed"]),
        # NOTE the spelling. current_weather uses "weathercode" (one word);
        # the daily block uses "weather_code" (underscore). This is the single
        # most common KeyError in this mini-project.
        code=int(current_raw["weathercode"]),
    )

    daily = payload.get("daily") or {}
    days = [
        Day(date=str(d), code=int(c), low=float(lo), high=float(hi))
        for d, c, lo, hi in zip(
            daily.get("time", []),
            daily.get("weather_code", []),
            daily.get("temperature_2m_min", []),
            daily.get("temperature_2m_max", []),
        )
    ]
    if not days:
        raise WeatherError("the forecast response had no daily block.")

    hourly = payload.get("hourly") or {}
    hour_rows = [
        Hour(time=str(t), temperature=float(temp), code=int(code))
        for t, temp, code in zip(
            hourly.get("time", []),
            hourly.get("temperature_2m", []),
            hourly.get("weather_code", []),
        )
    ]
    hour_rows = _hours_from_now(hour_rows, current.time, hours) if hours > 0 else []

    units = payload.get("current_weather_units") or {}
    return Forecast(
        current=current,
        days=days,
        temp_unit=str(units.get("temperature", "°C")),
        wind_unit=str(units.get("windspeed", "km/h")),
        hours=hour_rows,
    )


def _hours_from_now(rows: list[Hour], now: str, count: int) -> list[Hour]:
    """Return the next `count` hourly rows at or after the current-weather time.

    The hourly block always starts at 00:00 local time today, so slicing from
    the front would show you this morning, not the next few hours.
    """
    start = 0
    for index, row in enumerate(rows):
        if row.time >= now:  # ISO-8601 strings sort chronologically
            start = index
            break
    return rows[start : start + count]


# --------------------------------------------------------------------------
# Formatting
# --------------------------------------------------------------------------


def decode_weather_code(code: int) -> str:
    """Translate a WMO code into English. Unknown codes degrade, not crash."""
    return WEATHER_CODES.get(code, f"Unknown (code {code})")


def emoji_for_code(code: int, *, unicode_ok: bool = True) -> str:
    """One glyph summarising a WMO code, with an ASCII fallback."""
    bands = _EMOJI_BANDS if unicode_ok else _ASCII_BANDS
    for span, glyph in bands:
        if code in span:
            return glyph
    return "?" if not unicode_ok else "❓"


def format_coords(place: Place) -> str:
    """`48.85` -> `48.85°N`, `-58.38` -> `58.38°W`."""
    ns = "N" if place.latitude >= 0 else "S"
    ew = "E" if place.longitude >= 0 else "W"
    return (
        f"{abs(place.latitude):.2f}°{ns}, "
        f"{abs(place.longitude):.2f}°{ew}, "
        f"{place.elevation:.0f} m"
    )


def format_dashboard(place: Place, forecast: Forecast, *, unicode_ok: bool = True) -> str:
    """Render the whole dashboard as one string. Pure -- no printing, no I/O."""
    header = f"{place.name}, {place.country}  ({format_coords(place)})"
    rule = ("─" if unicode_ok else "-") * max(len(header), 37)

    now = forecast.current
    lines = [
        header,
        rule,
        f"Now:        {decode_weather_code(now.code)}, "
        f"{now.temperature:.1f}{forecast.temp_unit}, "
        f"wind {now.windspeed:.0f} {forecast.wind_unit} "
        f"(as of {now.time.replace('T', ' ')})",
        "3-day forecast:",
    ]
    # days[0] is today, which the "Now" line already covered.
    for day in forecast.days[1:4]:
        glyph = emoji_for_code(day.code, unicode_ok=unicode_ok)
        # `:<22` pads the description; the literal space after it guarantees a
        # gap even for "Thunderstorm with slight hail", which overflows 22.
        lines.append(
            f"  {day.date}  {glyph}  {decode_weather_code(day.code):<22} "
            f"lo {day.low:4.1f}{forecast.temp_unit}  "
            f"hi {day.high:4.1f}{forecast.temp_unit}"
        )

    if forecast.hours:
        lines.append(f"Next {len(forecast.hours)} hours:")
        for hour in forecast.hours:
            glyph = emoji_for_code(hour.code, unicode_ok=unicode_ok)
            clock = hour.time.replace("T", " ")
            lines.append(
                f"  {clock}  {glyph}  {hour.temperature:5.1f}{forecast.temp_unit}"
                f"  {decode_weather_code(hour.code)}"
            )

    return "\n".join(lines)


def print_rich_dashboard(place: Place, forecast: Forecast) -> None:
    """Stretch goal 4 -- the same dashboard as a coloured `rich` table."""
    try:
        from rich.console import Console
        from rich.table import Table
    except ImportError:
        print("rich is not installed. Run: python -m pip install rich")
        print(format_dashboard(place, forecast))
        return

    console = Console()
    now = forecast.current
    console.print(
        f"[bold cyan]{place.name}, {place.country}[/]  "
        f"[dim]({format_coords(place)})[/]"
    )
    console.print(
        f"[bold]Now:[/] {decode_weather_code(now.code)}, "
        f"[yellow]{now.temperature:.1f}{forecast.temp_unit}[/], "
        f"wind {now.windspeed:.0f} {forecast.wind_unit} [dim](as of "
        f"{now.time.replace('T', ' ')})[/]"
    )
    table = Table(title="3-day forecast")
    table.add_column("Date")
    table.add_column("Conditions")
    table.add_column("Low", justify="right")
    table.add_column("High", justify="right")
    for day in forecast.days[1:4]:
        table.add_row(
            day.date,
            f"{emoji_for_code(day.code)}  {decode_weather_code(day.code)}",
            f"[blue]{day.low:.1f}{forecast.temp_unit}[/]",
            f"[red]{day.high:.1f}{forecast.temp_unit}[/]",
        )
    console.print(table)


# --------------------------------------------------------------------------
# History
# --------------------------------------------------------------------------


def load_history(path: Path) -> list[dict[str, Any]]:
    """Read history.json. A missing or corrupt file reads as an empty list."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    except OSError as exc:
        raise WeatherError(f"could not read {path}: {exc.strerror or exc}") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise WeatherError(f"{path} is not valid JSON (line {exc.lineno}).") from exc
    return data if isinstance(data, list) else []


def save_history(path: Path, place: Place, current: Current, unit: str) -> None:
    """Append one lookup to history.json (read, append, rewrite)."""
    entries = load_history(path)
    entries.append(
        {
            "timestamp": datetime.now().replace(microsecond=0).isoformat(sep=" "),
            "city": place.name,
            "country": place.country,
            "temperature": current.temperature,
            "unit": unit,
        }
    )
    try:
        path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as exc:
        raise WeatherError(f"could not write {path}: {exc.strerror or exc}") from exc


def format_history(entries: list[dict[str, Any]], limit: int) -> str:
    """Render the last `limit` lookups, most recent first."""
    if not entries:
        return "No lookups recorded yet."
    lines = ["Recent lookups:"]
    for entry in reversed(entries[-limit:]):
        stamp = str(entry.get("timestamp", "?"))[:16]
        city = entry.get("city", "?")
        country = entry.get("country", "")
        where = f"{city}, {country}" if country else str(city)
        lines.append(f"  {stamp}  {where}")
    return "\n".join(lines)


def export_csv(path: Path, place: Place, forecast: Forecast) -> None:
    """Stretch goal 6 -- write the daily rows to a CSV file."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["city", "country", "date", "code", "conditions", "low", "high"])
            for day in forecast.days:
                writer.writerow(
                    [
                        place.name,
                        place.country,
                        day.date,
                        day.code,
                        decode_weather_code(day.code),
                        day.low,
                        day.high,
                    ]
                )
    except OSError as exc:
        raise WeatherError(f"could not write {path}: {exc.strerror or exc}") from exc


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def enable_unicode_output() -> bool:
    """Switch stdout to UTF-8 if we can; report whether glyphs are safe.

    The legacy Windows console runs cp1252, which cannot encode a box-drawing
    character or an emoji -- printing one raises UnicodeEncodeError. Rather
    than pretend that is not a problem, ask for UTF-8 and fall back to ASCII
    glyphs when the terminal refuses.
    """
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        try:
            reconfigure(encoding="utf-8")
            return True
        except (OSError, ValueError):
            pass
    return (getattr(sys.stdout, "encoding", "") or "").lower().replace("-", "").startswith("utf")


def build_parser() -> argparse.ArgumentParser:
    """Every flag the tool accepts, in one place."""
    parser = argparse.ArgumentParser(
        prog="weather.py",
        description="Print current conditions and a 3-day forecast for a city.",
    )
    parser.add_argument("city", nargs="*", help='city name, e.g. "Buenos Aires" (repeatable)')
    parser.add_argument("--history", action="store_true", help="print recent lookups and exit")
    parser.add_argument("--limit", type=int, default=10, help="how many history rows (default 10)")
    parser.add_argument("--no-save", action="store_true", help="do not append to history.json")
    parser.add_argument("--hours", type=int, default=0, metavar="N", help="also print the next N hours")
    parser.add_argument("--no-cache", action="store_true", help="ignore and bypass cache.json")
    parser.add_argument("--rich", action="store_true", help="render with the rich library")
    parser.add_argument("--ascii", action="store_true", help="force plain-ASCII glyphs")
    parser.add_argument("--export-csv", metavar="FILE", help="write the daily forecast to FILE")
    parser.add_argument(
        "--history-file",
        default=str(DEFAULT_HISTORY),
        metavar="FILE",
        help="where lookups are recorded (default: history.json beside this script)",
    )
    return parser


def report_city(
    session: requests.Session,
    city: str,
    args: argparse.Namespace,
    *,
    unicode_ok: bool,
) -> None:
    """Do one city end to end: geocode, fetch, print, save, optionally export."""
    cache_path = None if args.no_cache else DEFAULT_CACHE
    place = geocode(session, city, cache_path=cache_path)
    forecast = fetch_forecast(session, place, hours=args.hours, cache_path=cache_path)

    if args.rich:
        print_rich_dashboard(place, forecast)
    else:
        print(format_dashboard(place, forecast, unicode_ok=unicode_ok))

    if args.export_csv:
        export_csv(Path(args.export_csv), place, forecast)
        print(f"Wrote the daily forecast to {args.export_csv}.")

    if not args.no_save:
        history_path = Path(args.history_file)
        save_history(history_path, place, forecast.current, forecast.temp_unit)
        print(f"\nSaved this lookup to {history_path.name}.")


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments, run the requested job, return a process exit code."""
    args = build_parser().parse_args(argv)
    unicode_ok = enable_unicode_output() and not args.ascii

    if args.history:
        try:
            print(format_history(load_history(Path(args.history_file)), args.limit))
        except WeatherError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0

    if not args.city:
        print("Error: give a city name, or use --history.", file=sys.stderr)
        return 2

    exit_code = 0
    with make_session() as session:
        for index, city in enumerate(args.city):
            if index:
                print("\n" + ("─" if unicode_ok else "-") * 45 + "\n")
            try:
                report_city(session, city, args, unicode_ok=unicode_ok)
            except WeatherError as exc:
                print(f"Error: {exc}", file=sys.stderr)
                exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
