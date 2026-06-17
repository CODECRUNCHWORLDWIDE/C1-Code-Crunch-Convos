# Mini-Project — Weather Dashboard CLI

> Estimated time: 5–7 hours. Uses **[Open-Meteo](https://open-meteo.com/)**, a free, no-key, no-signup weather API.

This week's capstone. You will write a small command-line tool that takes a city name, looks up its coordinates, fetches the current weather and a 3-day forecast, and prints a clean dashboard. Optionally, it logs each lookup to a local JSON history file.

The goal is not "build a weather app" — it is to glue together every habit from Week 8 (URLs, query params, error handling, JSON parsing) into one end-to-end program.

---

## Why Open-Meteo?

- **Free.** No credit card.
- **No API key.** No signup. You can run the script right after `pip install`.
- **Two endpoints we need**, both documented at <https://open-meteo.com/en/docs>:
  - Geocoding (city name → lat/lon): `https://geocoding-api.open-meteo.com/v1/search?name=Paris&count=1`
  - Forecast (lat/lon → weather): `https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true&daily=...`

---

## What the finished tool looks like

```
$ python weather.py "Paris"
Paris, France  (48.85°N, 2.35°E, 35 m)
─────────────────────────────────────
Now:        Light rain, 14.2°C, wind 18 km/h (as of 2026-05-13 16:00)
3-day forecast:
  2026-05-14  ☔  Rain showers       lo  9.2°C  hi 14.8°C
  2026-05-15  ⛅  Partly cloudy      lo 10.1°C  hi 17.0°C
  2026-05-16  ☀️  Mainly clear       lo 11.5°C  hi 19.3°C

Saved this lookup to history.json.
```

The exact emoji or alignment is up to you — the rubric grades behavior, not aesthetics.

```
$ python weather.py "NotARealPlace"
Error: could not find a city called 'NotARealPlace'.
```

```
$ python weather.py --history
Recent lookups:
  2026-05-13 16:02  Paris, France
  2026-05-12 09:14  Tokyo, Japan
  2026-05-11 18:30  Buenos Aires, Argentina
```

---

## Specification

### Required behavior

1. **CLI argument parsing** — use `argparse`. Positional argument is the city name (may contain spaces; let argparse handle that with `nargs="+"` or take the whole string with quotes).
2. **Geocode the city.** Call:
   `GET https://geocoding-api.open-meteo.com/v1/search?name=<city>&count=1`
   The response includes `latitude`, `longitude`, `name`, `country`, `elevation`. If the `results` array is empty or missing, print a friendly error and exit non-zero.
3. **Fetch the weather.** Call:
   `GET https://api.open-meteo.com/v1/forecast`
   with query parameters:
   - `latitude`, `longitude` — from the geocoder
   - `current_weather=true`
   - `daily=weather_code,temperature_2m_max,temperature_2m_min`
   - `forecast_days=4` (today + next 3)
   - `timezone=auto`
4. **Decode `weather_code`** into a human-readable description. Use the table in the Open-Meteo docs (a small dict in your code is fine — see the starter file for a stub).
5. **Print the dashboard** as shown in the example: location header, "Now" line, 3-day forecast.
6. **Save to history.** If `--save` (or by default — your choice, document it), append a JSON object to `history.json` recording the timestamp, the city, the country, and the current temperature.
7. **`--history` flag** prints the last N (default 10) entries from `history.json`, most recent first.
8. **Robust error handling.** Every HTTP call has a `timeout=`. Network failures and 4xx/5xx responses print a short message and exit non-zero (no tracebacks for the user).

### Code-quality requirements

- Type hints on every function.
- Small functions: at least one of `geocode`, `fetch_forecast`, `format_dashboard`, `save_history`, `load_history`.
- A `make_session()` helper that builds a `requests.Session` with a sane User-Agent and a `Retry` policy (Exercise 05 pattern).
- A `main()` function that drives everything; the `if __name__ == "__main__":` block does nothing but call it.
- No hard-coded API keys (Open-Meteo's free tier needs none). If you implement the commercial-tier stretch goal, read the key from `os.environ` via `python-dotenv`.

### Not allowed

- Hard-coding any weather data.
- Calling `eval()` on anything.
- Catching `Exception:` bare — be specific.
- `requests.get(...)` without a `timeout=`.

---

## Rubric (100 points)

| Section | Criterion | Pts |
|---|---|---|
| **Function** | Geocodes a real city to the correct coordinates | 10 |
| | Fetches and parses the current weather correctly | 10 |
| | Fetches and parses the 3-day daily forecast correctly | 10 |
| | Translates `weather_code` to a human-readable description | 5 |
| | Saves a history entry per successful lookup | 10 |
| | `--history` flag prints recent lookups in reverse-chronological order | 5 |
| **Robustness** | Unknown city handled with a clean error (no traceback) | 5 |
| | Network failure handled with a clean error (no traceback) | 5 |
| | All HTTP calls have `timeout=` | 5 |
| | `make_session()` with retry policy is present and used | 5 |
| **Code quality** | Type hints throughout | 5 |
| | Functions are small and named clearly | 5 |
| | No bare `except Exception:` | 5 |
| | README in the project folder explaining how to run it | 5 |
| | Output is readable and well-formatted | 5 |
| | `.env` (if any) is in `.gitignore` | 5 |
| **Total** | | **100** |

---

## Stretch goals (optional)

1. **Hourly forecast.** Add a `--hours N` flag that prints the next N hours of temperature and weather code, using `hourly=temperature_2m,weather_code`.
2. **Multiple cities.** Pass several cities at once: `python weather.py Paris Tokyo Lima`. Print each dashboard, separated by a horizontal rule.
3. **Cache results.** Cache the geocoder response for each city forever (city → lat/lon doesn't change) and the forecast for 10 minutes. Use a JSON file or `requests-cache`.
4. **Color output.** Use [`rich`](https://rich.readthedocs.io/) for tables and color. Install with `pip install rich`; replace `print` with `rich.print` selectively.
5. **Unit test the decoders.** Extract `decode_weather_code(code: int) -> str` into a pure function with no I/O and write `pytest` cases for it (preview of Week 11).
6. **CSV export.** `--export-csv FILE` writes the daily forecast to a CSV (Week 6 patterns).

---

## How to start

1. Read the [Open-Meteo API docs](https://open-meteo.com/en/docs) end to end — it is short.
2. Test the two endpoints with `curl` first:
   ```bash
   curl "https://geocoding-api.open-meteo.com/v1/search?name=Paris&count=1"
   curl "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
   ```
3. Open `starter.py`. It has imports, the function stubs you need to fill in, and a working `main()` skeleton.
4. Fill in stubs one at a time. Test each by running the script after each function works.
5. Write the history-saving logic last (it is independent of the API logic).
6. Polish the output formatting.

Good luck. When you finish, push your code to your fork, link it in your write-up, and start Week 9.
