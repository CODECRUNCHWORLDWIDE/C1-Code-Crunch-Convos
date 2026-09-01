"""Tests for the pure, no-I/O half of weather.py (mini-project stretch goal 5).

Every function tested here is deliberately network-free: decoding a WMO code,
unpacking a forecast document, formatting a dashboard. That split is the point
of the stretch goal -- if parsing lives inside the function that also does the
HTTP call, you cannot test it without either a live network or a mocking
library. Here `parse_forecast` takes a dict, so a literal is a complete test.

    python -m pytest test_weather.py -q
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from weather import (
    Current,
    Day,
    Hour,
    Place,
    WeatherError,
    _hours_from_now,
    decode_weather_code,
    emoji_for_code,
    format_coords,
    format_dashboard,
    format_history,
    geocode,
    get_json,
    parse_forecast,
    save_history,
)

# A trimmed copy of a real Open-Meteo response, captured on 2026-08-21.
SAMPLE: dict = {
    "current_weather_units": {"temperature": "°C", "windspeed": "km/h"},
    "current_weather": {
        "time": "2026-08-21T17:45",
        "temperature": 21.9,
        "windspeed": 16.4,
        "winddirection": 322,
        "is_day": 1,
        "weathercode": 2,
    },
    "daily": {
        "time": ["2026-08-21", "2026-08-22", "2026-08-23", "2026-08-24"],
        "weather_code": [3, 3, 3, 80],
        "temperature_2m_max": [23.1, 23.7, 23.8, 25.9],
        "temperature_2m_min": [16.8, 14.4, 14.1, 14.0],
    },
}


# --------------------------------------------------------------------------
# decode_weather_code
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        (0, "Clear sky"),
        (2, "Partly cloudy"),
        (45, "Fog"),
        (61, "Slight rain"),
        (80, "Slight rain showers"),
        (95, "Thunderstorm"),
        (99, "Thunderstorm with heavy hail"),
    ],
)
def test_decode_known_codes(code: int, expected: str) -> None:
    assert decode_weather_code(code) == expected


def test_decode_unknown_code_degrades_instead_of_raising() -> None:
    # 4 is not in the WMO table. A weather CLI must not die over one number.
    assert decode_weather_code(4) == "Unknown (code 4)"


def test_emoji_has_an_ascii_fallback() -> None:
    assert emoji_for_code(0, unicode_ok=False) == "(o)"
    assert emoji_for_code(4, unicode_ok=False) == "?"


# --------------------------------------------------------------------------
# parse_forecast
# --------------------------------------------------------------------------


def test_parse_forecast_reads_current_block() -> None:
    forecast = parse_forecast(SAMPLE)
    assert forecast.current == Current(
        time="2026-08-21T17:45", temperature=21.9, windspeed=16.4, code=2
    )
    assert forecast.temp_unit == "°C"


def test_parse_forecast_zips_four_days_in_order() -> None:
    forecast = parse_forecast(SAMPLE)
    assert len(forecast.days) == 4
    assert forecast.days[0] == Day(date="2026-08-21", code=3, low=16.8, high=23.1)
    assert forecast.days[-1] == Day(date="2026-08-24", code=80, low=14.0, high=25.9)


def test_parse_forecast_does_not_swap_low_and_high() -> None:
    # temperature_2m_min and _max arrive as separate arrays and it is very easy
    # to zip them the wrong way round. This assertion is the guard.
    assert all(day.low <= day.high for day in parse_forecast(SAMPLE).days)


def test_parse_forecast_rejects_a_response_with_no_current_block() -> None:
    with pytest.raises(WeatherError, match="no current_weather block"):
        parse_forecast({"daily": SAMPLE["daily"]})


def test_parse_forecast_rejects_a_response_with_no_daily_block() -> None:
    with pytest.raises(WeatherError, match="no daily block"):
        parse_forecast({"current_weather": SAMPLE["current_weather"]})


# --------------------------------------------------------------------------
# Formatting
# --------------------------------------------------------------------------


def test_format_coords_uses_hemispheres_not_minus_signs() -> None:
    lima = Place("Lima", "Peru", -12.04318, -77.02824, 152.0)
    assert format_coords(lima) == "12.04°S, 77.03°W, 152 m"


def test_dashboard_skips_today_in_the_three_day_list() -> None:
    paris = Place("Paris", "France", 48.85341, 2.3488, 42.0)
    text = format_dashboard(paris, parse_forecast(SAMPLE), unicode_ok=False)
    lines = text.splitlines()
    assert lines[0] == "Paris, France  (48.85°N, 2.35°E, 42 m)"
    assert "Partly cloudy, 21.9°C, wind 16 km/h" in lines[2]
    forecast_rows = [line for line in lines if line.startswith("  2026-")]
    assert len(forecast_rows) == 3
    assert forecast_rows[0].startswith("  2026-08-22")  # today is not repeated


def test_history_is_rendered_newest_first_and_capped() -> None:
    entries = [
        {"timestamp": "2026-05-11 18:30:00", "city": "Buenos Aires", "country": "Argentina"},
        {"timestamp": "2026-05-12 09:14:00", "city": "Tokyo", "country": "Japan"},
        {"timestamp": "2026-05-13 16:02:00", "city": "Paris", "country": "France"},
    ]
    assert format_history(entries, limit=2).splitlines() == [
        "Recent lookups:",
        "  2026-05-13 16:02  Paris, France",
        "  2026-05-12 09:14  Tokyo, Japan",
    ]


def test_history_of_an_empty_file_is_a_sentence_not_a_crash() -> None:
    assert format_history([], limit=10) == "No lookups recorded yet."


def test_hours_slice_starts_at_now_not_at_midnight() -> None:
    rows = [
        Hour(time=f"2026-08-21T{h:02d}:00", temperature=float(h), code=0)
        for h in range(24)
    ]
    picked = _hours_from_now(rows, "2026-08-21T17:45", 3)
    assert [row.time for row in picked] == [
        "2026-08-21T18:00",
        "2026-08-21T19:00",
        "2026-08-21T20:00",
    ]


# --------------------------------------------------------------------------
# Error paths, tested with a stub session (still no network)
# --------------------------------------------------------------------------


class _StubResponse:
    def __init__(self, payload: object) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return self._payload


class _StubSession:
    """Enough of requests.Session for get_json to run offline."""

    def __init__(self, payload: object) -> None:
        self._payload = payload
        self.calls: list[tuple[str, dict]] = []

    def get(self, url: str, params: dict, timeout: float) -> _StubResponse:
        self.calls.append((url, params))
        return _StubResponse(self._payload)


def test_geocode_raises_when_the_geocoder_omits_results() -> None:
    # Open-Meteo answers 200 with NO "results" key when nothing matched.
    session = _StubSession({"generationtime_ms": 0.54})
    with pytest.raises(WeatherError, match="could not find a city"):
        geocode(session, "NotARealPlace", cache_path=None)  # type: ignore[arg-type]


def test_geocode_sends_the_city_as_a_query_parameter() -> None:
    session = _StubSession(
        {"results": [{"name": "Paris", "country": "France", "latitude": 48.85,
                      "longitude": 2.35, "elevation": 42.0}]}
    )
    place = geocode(session, "Paris", cache_path=None)  # type: ignore[arg-type]
    assert place.country == "France"
    assert session.calls[0][1] == {"name": "Paris", "count": 1}


def test_get_json_turns_a_non_json_body_into_a_weather_error() -> None:
    class _BadJSON(_StubResponse):
        def json(self) -> object:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")

    class _BadSession(_StubSession):
        def get(self, url: str, params: dict, timeout: float) -> _StubResponse:
            return _BadJSON(None)

    with pytest.raises(WeatherError, match="did not return JSON"):
        get_json(_BadSession(None), "https://example.test/x", {})  # type: ignore[arg-type]


def test_save_history_appends_rather_than_overwrites(tmp_path: Path) -> None:
    path = tmp_path / "history.json"
    place = Place("Paris", "France", 48.85, 2.35, 42.0)
    current = Current(time="2026-08-21T17:45", temperature=21.9, windspeed=16.4, code=2)
    save_history(path, place, current, "°C")
    save_history(path, place, current, "°C")
    assert len(json.loads(path.read_text(encoding="utf-8"))) == 2
