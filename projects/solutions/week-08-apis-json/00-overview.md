# Week 8 Mini-Project — Reference Implementation

This folder is the worked answer to [Week 8's weather dashboard CLI](../../../curriculum/week-08-apis-json/mini-project/README.md). It is a real, runnable program, not a sketch: every transcript below was produced by running these exact files on CPython 3.13.2 on Windows 11.

This file doubles as the README the rubric asks for ("README in the project folder explaining how to run it", 5 points).

Read the walkthrough — architecture, the decisions that were genuinely open, where people get stuck — in [`../../../curriculum/week-08-apis-json/mini-project/README.md`](../../../curriculum/week-08-apis-json/mini-project/README.md). This file is just "what it is and how to run it".

---

## What it is

A command-line weather dashboard on top of [Open-Meteo](https://open-meteo.com/), which is free, needs no API key, and needs no signup. Two endpoints:

| Call | Purpose |
|---|---|
| `GET https://geocoding-api.open-meteo.com/v1/search?name=Paris&count=1` | city name → latitude/longitude/elevation |
| `GET https://api.open-meteo.com/v1/forecast?latitude=…&longitude=…&current_weather=true&daily=…` | coordinates → current conditions + daily rows |

## Files

| File | What it is |
|---|---|
| `weather.py` | The whole CLI: HTTP plumbing, parsing, formatting, history, cache. ~700 lines including comments and the WMO table. |
| `test_weather.py` | 23 `pytest` cases over the network-free half (stretch goal 5). |
| `requirements.txt` | `requests` + `python-dotenv`, plus optional `rich` and `pytest`. |
| `.env.example` | The committed template. There is no `.env` here because Open-Meteo's free tier needs no key. |
| `.gitignore` | Ignores `.env`, plus the `history.json` / `cache.json` / `*.csv` the tool writes at runtime. |

## How to run it

```bash
python -m pip install -r requirements.txt
python weather.py "Paris"
```

Real output, 2026-08-21:

```text
$ python weather.py "Paris"
Paris, France  (48.85°N, 2.35°E, 42 m)
──────────────────────────────────────
Now:        Partly cloudy, 21.9°C, wind 16 km/h (as of 2026-08-21 17:45)
3-day forecast:
  2026-08-22  ☁️  Overcast               lo 14.4°C  hi 23.7°C
  2026-08-23  ☁️  Overcast               lo 14.1°C  hi 23.8°C
  2026-08-24  🌦️  Slight rain showers    lo 14.0°C  hi 25.9°C

Saved this lookup to history.json.
```

Your numbers will differ — it is a live forecast. The *shape* is what you are comparing against.

```text
$ python weather.py "NotARealPlace"
Error: could not find a city called 'NotARealPlace'.

$ echo $?     # PowerShell: $LASTEXITCODE
1
```

## Every flag

| Flag | Effect |
|---|---|
| *(positional)* | One or more city names: `python weather.py Paris Tokyo Lima` (stretch 2) |
| `--history` | Print recent lookups, newest first, and exit |
| `--limit N` | How many history rows `--history` prints (default 10) |
| `--no-save` | Do not append this lookup to `history.json` |
| `--hours N` | Also print the next N hourly rows (stretch 1) |
| `--no-cache` | Bypass `cache.json` entirely (stretch 3) |
| `--rich` | Render with the `rich` library if it is installed (stretch 4) |
| `--ascii` | Force plain-ASCII glyphs for terminals that cannot print emoji |
| `--export-csv FILE` | Write the four daily rows to a CSV (stretch 6) |
| `--history-file FILE` | Use a different history file |

## Running the tests

```bash
$ python -m pytest test_weather.py -q
.......................                                                  [100%]
23 passed in 0.89s
```

The tests never touch the network. `parse_forecast` takes a dict, so a captured response literal is a complete test fixture, and the two `geocode` tests pass a stub session object with a four-line `get()`.

## How it maps to the spec

| Spec requirement | Where |
|---|---|
| 1. `argparse` CLI, city may contain spaces | `build_parser()`, `city` is `nargs="*"` |
| 2. Geocode the city, friendly error when missing | `geocode()` |
| 3. Forecast call with the six required query params | `fetch_forecast()` |
| 4. Decode `weather_code` | `WEATHER_CODES` + `decode_weather_code()` |
| 5. Print the dashboard | `format_dashboard()` (pure — returns a string) |
| 6. Save to history | `save_history()`, on by default, `--no-save` opts out |
| 7. `--history` prints the last N, newest first | `format_history()` |
| 8. Timeout on every call, no tracebacks | `get_json()` is the single network chokepoint |
| `make_session()` with a `Retry` policy | `make_session()` |
| Type hints, small functions, `main()` only | throughout; `__main__` is one line |
| No hard-coded keys | there are none to hard-code; see `.env.example` |
