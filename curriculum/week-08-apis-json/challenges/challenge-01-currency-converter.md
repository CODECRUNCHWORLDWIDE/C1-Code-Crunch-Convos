# Challenge 01 — Currency Converter CLI

> ~2 hours. Uses the [Frankfurter](https://www.frankfurter.app/) API. Free, no key, no signup.

## Story

You are travelling and need a quick command-line tool to convert money between currencies using up-to-date exchange rates from the European Central Bank.

## Goal

Build a script `challenge-01-currency-converter.py` that runs like this:

```bash
$ python challenge-01-currency-converter.py 100 USD EUR
100.00 USD = 92.50 EUR  (rate 0.925, ECB 2026-05-13)

$ python challenge-01-currency-converter.py 50 GBP JPY
50.00 GBP = 9842.50 JPY  (rate 196.85, ECB 2026-05-13)

$ python challenge-01-currency-converter.py 10 XYZ EUR
Error: 'XYZ' is not a supported currency code.
Run with --list to see supported codes.
```

## API

Base URL: `https://api.frankfurter.app`

Endpoints you will need:

| Endpoint | Purpose |
|---|---|
| `GET /latest?amount=100&from=USD&to=EUR` | Latest rate, one or many target currencies |
| `GET /currencies` | The full list of supported codes |

Sample response from `/latest`:

```json
{
  "amount": 100.0,
  "base": "USD",
  "date": "2026-05-13",
  "rates": { "EUR": 92.50 }
}
```

You can verify with `curl`:

```bash
curl "https://api.frankfurter.app/latest?amount=100&from=USD&to=EUR"
```

## Requirements

The script must:

1. Accept three positional arguments: `amount`, `from_currency`, `to_currency`.
2. Validate that `amount` is a positive number and the currency codes are three letters.
3. Call `/latest` with `amount`, `from`, and `to` query parameters.
4. Print the converted amount, the rate, and the date returned by Frankfurter.
5. Handle errors gracefully:
   - Invalid currency code → print a helpful message and exit non-zero.
   - Network failure → catch, print a message, exit non-zero.
6. Set a `timeout=` on every HTTP call.
7. Support a `--list` flag that prints all supported currency codes and exits.

The script must **not**:

- Hard-code any exchange rate (always call the live API).
- Use `eval` on user input.
- Build the URL by string concatenation. Use `params=`.

## Grading rubric

| Criterion | Points |
|---|---|
| Runs without errors on valid inputs | 25 |
| Handles invalid currency codes with a useful message | 15 |
| Handles network failure (timeout, connection error) without traceback | 15 |
| Uses `params=` correctly (no manual URL string building) | 10 |
| Uses type hints on every function | 10 |
| `--list` flag works | 10 |
| Code is readable: small functions, clear names, docstrings | 10 |
| Write-up answers all three questions | 5 |
| **Total** | **100** |

## Hints

- `argparse` from Week 4 is the right tool for argument parsing. `argparse.ArgumentTypeError` can validate the currency-code format up front.
- A regex like `^[A-Z]{3}$` validates currency codes cheaply (after `.upper()`).
- Use one small helper for `_get_json(url, params)` so you don't repeat the timeout/error code twice.
- The Frankfurter response keys you need are `rates[to_currency]` and `date`.

## Stretch (optional)

- Support a `--date YYYY-MM-DD` flag that fetches a historical rate via `/{date}` instead of `/latest`.
- Support converting to multiple targets at once: `python ... 100 USD EUR GBP JPY`.
- Cache the `/currencies` list to a local JSON file so `--list` is offline-safe after the first run (use what you learned in Week 6).
