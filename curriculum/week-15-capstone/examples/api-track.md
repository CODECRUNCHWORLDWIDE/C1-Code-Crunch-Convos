# API Track Example — Currency Conversion API

A small but real REST API that converts between currencies, caches
exchange-rate lookups, exposes auto-generated OpenAPI documentation,
and deploys to **Fly.io**. The headline endpoint:

```text
GET /convert?from=USD&to=EUR&amount=100
→ { "from": "USD", "to": "EUR", "amount": 100, "converted": 92.13, "rate": 0.9213, "as_of": "2026-05-13T08:00:00Z" }
```

## MVP sentence

> *A user can call `GET /convert?from=USD&to=EUR&amount=100` on the
> deployed API and receive a JSON response with the converted amount,
> served from a 60-second cache.*

If that endpoint returns correctly on the deployed URL, the MVP is
done.

## User stories

1. **Convert.** As a developer, I can `GET /convert` with `from`, `to`,
   and `amount` query parameters and receive the converted amount as
   JSON.
2. **List currencies.** As a developer, I can `GET /currencies` and
   receive the list of supported currency codes.
3. **Discover.** As a developer, I can visit `/docs` and read the
   auto-generated OpenAPI / Swagger UI.
4. **Health.** As an operator, I can `GET /health` and receive a 200
   with a build version and uptime.
5. **Cache.** As an operator, repeated calls for the same pair within
   60 seconds do not call the upstream rate provider.

## Anti-goals

- User accounts, billing, rate-limiting per key.
- A web UI for end-users — the API *is* the product.
- Historical rates beyond "today".
- More than one upstream provider.
- More than ~30 currencies — pick the ECB / European Central Bank set
  or the top-30 G20 currencies.

## Suggested tech stack

- Python 3.11+
- **Flask** + `flask-smorest` *or* **FastAPI** — both auto-generate
  OpenAPI docs. Pick whichever you used in Week 9 (Flask) or are
  curious about (FastAPI). The rest of this doc uses Flask for
  consistency with the rest of the bootcamp.
- `flask-smorest` for OpenAPI docs and request/response schemas
- `marshmallow` (bundled with flask-smorest) for validation
- `requests` to call the upstream rate provider
- `cachetools` for the in-process TTL cache
- `gunicorn` for production
- `pytest`, `pytest-cov`, `requests-mock`
- `ruff`, `black`
- GitHub Actions
- Fly.io for deployment

## Upstream rate provider

Use one of:

- **exchangerate.host** — free, no key required, generous limits.
  <https://exchangerate.host/>
- **ECB Reference Rates** — XML feed, refreshed daily.
  <https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html>
- **Frankfurter** — free wrapper on ECB rates, JSON.
  <https://www.frankfurter.app/>

`exchangerate.host` is the easiest for a week-long project.

## Folder layout

```text
currency-api/
├── src/currency_api/
│   ├── __init__.py
│   ├── app.py            # create_app(), register blueprints
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── convert.py    # GET /convert
│   │   ├── currencies.py # GET /currencies
│   │   └── health.py     # GET /health
│   ├── schemas.py        # marshmallow schemas
│   ├── rates.py          # upstream client + cache
│   └── config.py         # env-driven settings
├── tests/
│   ├── conftest.py
│   ├── test_convert.py
│   ├── test_currencies.py
│   ├── test_rates.py
│   └── test_health.py
├── docs/
│   ├── PROPOSAL.md
│   └── RETRO.md
├── fly.toml
├── Dockerfile
├── pyproject.toml
├── .github/workflows/ci.yml
├── README.md
└── LICENSE
```

## A representative `rates.py`

```python
"""Upstream rate fetching with a tiny TTL cache."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

import requests
from cachetools import TTLCache

_logger = logging.getLogger(__name__)
_cache: TTLCache[tuple[str, str], "Rate"] = TTLCache(maxsize=1024, ttl=60)


@dataclass(frozen=True)
class Rate:
    """A single currency-pair exchange rate."""

    base: str
    quote: str
    value: float
    as_of: datetime


def get_rate(base: str, quote: str) -> Rate:
    """Return the exchange rate from ``base`` to ``quote``.

    Cached for 60 seconds per pair. Raises ``ValueError`` for unknown
    or malformed currency codes; raises ``requests.HTTPError`` if the
    upstream call fails.
    """
    key = (base.upper(), quote.upper())
    if key in _cache:
        _logger.debug("rate cache hit %s", key)
        return _cache[key]

    response = requests.get(
        "https://api.exchangerate.host/latest",
        params={"base": key[0], "symbols": key[1]},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()

    try:
        value = float(payload["rates"][key[1]])
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Unknown currency pair {key}") from exc

    rate = Rate(
        base=key[0],
        quote=key[1],
        value=value,
        as_of=datetime.now(tz=timezone.utc),
    )
    _cache[key] = rate
    return rate
```

That function is short, typed, has a docstring on each public piece,
caches sensibly, and is easy to test with `requests-mock`.

## A representative test

```python
"""Tests for the /convert endpoint."""

from __future__ import annotations

import responses


@responses.activate
def test_convert_usd_to_eur(client) -> None:
    """A USD->EUR conversion returns a sensible JSON payload."""
    responses.get(
        "https://api.exchangerate.host/latest",
        json={"rates": {"EUR": 0.9213}},
    )

    response = client.get("/convert?from=USD&to=EUR&amount=100")

    assert response.status_code == 200
    body = response.get_json()
    assert body["from"] == "USD"
    assert body["to"] == "EUR"
    assert body["amount"] == 100
    assert body["converted"] == 92.13
    assert "as_of" in body
```

`client` comes from a fixture in `tests/conftest.py` that builds the
Flask app with `create_app(testing=True)`.

## Day-by-day plan

**Day 1.** Proposal. Pick an upstream provider.

**Day 2.** Skeleton, CI, smoke test, hello-world `/health` endpoint.

**Day 3 AM.** `rates.py` — upstream client with cache. Tests with
`responses`.

**Day 3 PM.** `routes/convert.py` — `GET /convert` with input
validation via marshmallow schemas. Integration tests.

**Day 4 AM.** `routes/currencies.py` — `GET /currencies` returning the
list of supported codes (hard-code 30 or fetch and cache once).

**Day 4 PM.** Wire `flask-smorest` so that `/docs` serves Swagger UI
with descriptions, examples, and error responses.

**Day 5.** Coverage past 70%. Error handling: return 400 for invalid
codes, 502 if the upstream fails. Logging. README with full curl
examples.

**Day 6 AM.** Deploy to Fly.io. Dockerfile that runs `gunicorn
"currency_api.app:create_app()" -b 0.0.0.0:$PORT`. `fly launch`.

**Day 6 PM.** Record walkthrough: live curl against the deployed API,
then `/docs`, then a code tour.

**Day 7.** Retro, pin, submit.

## Where this project demonstrates each week

- **Week 8** — calling and handling JSON APIs.
- **Week 9** — Flask, blueprints, request validation.
- **Week 11** — pytest, HTTP mocks, CI.
- **Week 12** — Docker as automation.

## "Done" check

- [ ] `GET /convert?from=USD&to=EUR&amount=100` returns valid JSON on
      the deployed URL.
- [ ] `GET /currencies` returns a non-empty list.
- [ ] `GET /docs` shows Swagger UI with all endpoints documented.
- [ ] Repeated calls within 60s show cache behaviour (you can prove
      this with a test or with logs).
- [ ] CI green, coverage ≥ 70%, lint clean.
- [ ] README has copy-pasteable `curl` examples.

## Stretch goals

- A `GET /history?from=USD&to=EUR&days=30` endpoint that returns a
  small time series for charting. Start *only* if Day 5 ends early.
- A `Last-Modified` header and `If-Modified-Since` support.
- Prometheus `/metrics` endpoint.

## A note on free-tier limits

`exchangerate.host` is free but not unlimited. Your 60-second cache
keeps you well inside any reasonable hobby quota. If the upstream rate
provider rate-limits you in development, switch to Frankfurter for the
demo — both expose the same shape of response.
