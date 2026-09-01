"""Week 8 weather logic, lifted so a Flask view can call it.

Homework problem 3 asks you to reuse the Week 8 weather CLI from inside a
route. This module is that CLI's networking half with the printing removed:
pure functions in, dataclass out, no `print`, no `sys.exit`. A web view cannot
call `sys.exit`, so the CLI's "print an error and exit non-zero" behaviour is
replaced by raising `WeatherError`, which the view turns into a flash message.

Open-Meteo's free tier needs no API key. The commercial tier does, and that key
is read from `os.environ` -- never hard-coded, never committed. That satisfies
the homework's "API key (if any) is loaded from os.environ" criterion whether
or not you ever set one.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Every outbound call gets a timeout. A hung upstream must never hang your
# web server -- with the dev server being single-threaded, one stuck request
# freezes the whole site.
TIMEOUT_SECONDS = 5.0

# Cache entries live this long (homework problem 3 stretch goal).
CACHE_TTL_SECONDS = 300

# WMO weather interpretation codes, as documented by Open-Meteo.
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


class WeatherError(RuntimeError):
    """Anything that should become a flash message rather than a traceback."""


@dataclass
class CurrentWeather:
    """One city's current conditions, ready to hand to a template."""

    city: str
    country: str
    temp: float
    unit: str
    description: str


# city (lowercased) -> (monotonic timestamp, CurrentWeather)
_CACHE: dict[str, tuple[float, CurrentWeather]] = {}


def decode_weather_code(code: int) -> str:
    """Turn a WMO code into English. Unknown codes degrade, they do not crash."""
    return WEATHER_CODES.get(code, f"Unknown conditions (code {code})")


def _commercial_params() -> dict[str, str]:
    """Add the paid-tier key only if the environment supplies one."""
    key = os.environ.get("OPEN_METEO_API_KEY", "").strip()
    return {"apikey": key} if key else {}


def geocode(city: str) -> dict[str, object]:
    """Resolve a city name to the first matching Open-Meteo geocoding result."""
    params: dict[str, object] = {"name": city, "count": 1}
    params.update(_commercial_params())
    try:
        response = requests.get(GEOCODE_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except requests.Timeout as exc:
        raise WeatherError("The weather service timed out. Try again.") from exc
    except requests.RequestException as exc:
        raise WeatherError("Could not reach the weather service.") from exc
    except ValueError as exc:  # .json() on a non-JSON body
        raise WeatherError("The weather service sent a malformed reply.") from exc

    results = payload.get("results") or []
    if not results:
        raise WeatherError(f"No city called {city!r} was found.")
    return results[0]


def fetch_current(latitude: float, longitude: float) -> dict[str, object]:
    """Fetch the `current_weather` block for one coordinate pair."""
    params: dict[str, object] = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": "auto",
    }
    params.update(_commercial_params())
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except requests.Timeout as exc:
        raise WeatherError("The weather service timed out. Try again.") from exc
    except requests.RequestException as exc:
        raise WeatherError("Could not reach the weather service.") from exc
    except ValueError as exc:
        raise WeatherError("The weather service sent a malformed reply.") from exc

    current = payload.get("current_weather")
    if not isinstance(current, dict):
        raise WeatherError("The weather service did not return current conditions.")
    return current


def get_current_weather(city: str, *, use_cache: bool = True) -> CurrentWeather:
    """Geocode `city`, fetch its current weather, and cache the result.

    Raises `WeatherError` for every failure a user can cause or a network can
    inflict. The caller flashes the message; nothing here ever prints.
    """
    key = city.strip().lower()
    if not key:
        raise WeatherError("Please enter a city name.")

    if use_cache:
        cached = _CACHE.get(key)
        if cached is not None:
            cached_at, value = cached
            if time.monotonic() - cached_at < CACHE_TTL_SECONDS:
                return value

    place = geocode(city)
    current = fetch_current(
        float(place["latitude"]),  # type: ignore[arg-type]
        float(place["longitude"]),  # type: ignore[arg-type]
    )

    result = CurrentWeather(
        city=str(place.get("name", city)),
        country=str(place.get("country", "")),
        temp=float(current.get("temperature", 0.0)),  # type: ignore[arg-type]
        unit="°C",
        description=decode_weather_code(int(current.get("weathercode", -1))),  # type: ignore[arg-type]
    )
    _CACHE[key] = (time.monotonic(), result)
    return result


def clear_cache() -> None:
    """Drop every cached city. Used by the smoke tests."""
    _CACHE.clear()
