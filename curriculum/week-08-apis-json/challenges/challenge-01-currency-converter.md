# Challenge 01 — Currency Converter CLI

> **Topic:** a real command-line tool over a real API, with argument validation and errors that never show a traceback
> **Lecture:** [01 — HTTP and REST](../lecture-notes/01-http-and-rest.md) for status codes, and [02 — Using `requests`](../lecture-notes/02-using-requests.md) for `params=`
> **Difficulty:** Intermediate
> **Target time:** 2 hours
> **Why this one:** every exercise so far printed something for you to look at. This is the first thing on the week that another person could actually use, and being usable is a different bar — it has to reject nonsense before it sends it, explain a failure in one line, and exit with a code a script can test.

## The Brief

You are travelling and you want a quick command-line tool that converts money
between currencies at up-to-date rates.

The rates come from [Frankfurter](https://frankfurter.dev), a free, keyless API
over the European Central Bank's daily reference rates. Two endpoints do
everything you need:

| Endpoint | What it gives you |
|---|---|
| `GET /latest?amount=100&from=USD&to=EUR` | the converted amount and the date it was fixed |
| `GET /currencies` | every code the service publishes, with its full name |

A reply from `/latest` looks like this:

```json
{
  "amount": 100.0,
  "base": "USD",
  "date": "2026-08-21",
  "rates": { "EUR": 85.48 }
}
```

Notice the `date`. The ECB fixes its rates once a working day, around
16:00 Central European Time, and Frankfurter serves that fix until the next
one. So the number you get on a Sunday is Friday's number, and a tool that
prints the rate without the date is telling you half of the truth.

Your finished tool runs like this:

```bash
$ python currency.py 100 USD EUR
100.00 USD = 85.48 EUR  (rate 0.8548, ECB 2026-08-21)

$ python currency.py 10 XYZ EUR
Error: 'XYZ' is not a supported currency code.
Run with --list to see supported codes.

$ python currency.py --list
30 supported codes:
  AUD  Australian Dollar
  ...
```

Three positional arguments, one flag, and — this is the part that makes it a
tool rather than a script — no traceback ever reaches the person using it.

## Starter

Save this as `currency.py` and fill in every `TODO`. It runs as pasted; it just
refuses to do anything yet.

```python
"""currency.py — convert money between currencies at ECB reference rates."""

from __future__ import annotations

import argparse
import re
import sys
from typing import Any, NamedTuple

import requests

BASE_URL = "https://api.frankfurter.app"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0

CODE_PATTERN = re.compile(r"^[A-Z]{3}$")


class ConversionError(Exception):
    """Raised when a conversion cannot be completed, for any reason."""


class Quote(NamedTuple):
    """One completed conversion, with everything needed to print it."""

    amount: float
    source: str
    target: str
    converted: float
    rate: float
    date: str


def get_json(path: str, params: dict[str, Any]) -> dict[str, Any]:
    """GET one Frankfurter path and return the decoded body."""
    # TODO: requests.get(f"{BASE_URL}{path}", params=params, timeout=...)
    # TODO: raise_for_status(), then return .json()
    # TODO: turn HTTPError into ConversionError, and RequestException too
    raise NotImplementedError


def currency_code(text: str) -> str:
    """Normalise and validate one currency code."""
    # TODO: upper-case it, check CODE_PATTERN, raise
    #       argparse.ArgumentTypeError if it does not match
    raise NotImplementedError


def convert(amount: float, source: str, target: str) -> Quote:
    """Convert amount from source to target at the latest rate."""
    # TODO: call /latest with amount, from and to in params=
    # TODO: read payload["rates"][target] and payload["date"]
    # TODO: the unit rate is converted / amount
    raise NotImplementedError


def format_quote(quote: Quote) -> str:
    """Format one Quote as the single line the tool prints."""
    raise NotImplementedError  # TODO


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, do the conversion, print the result."""
    parser = argparse.ArgumentParser(description="Convert money at ECB rates.")
    parser.add_argument("amount", nargs="?", type=float)
    parser.add_argument("source", nargs="?", type=currency_code)
    parser.add_argument("target", nargs="?", type=currency_code)
    parser.add_argument("--list", action="store_true", help="list supported codes")
    args = parser.parse_args(argv)

    # TODO: handle --list first and return 0
    # TODO: convert and print, catching ConversionError, printing
    #       f"Error: {err}" to sys.stderr and returning 2
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
```

**`type=` in argparse.** You can hand `add_argument` any function that takes a
string and returns the value you want. If it raises
`argparse.ArgumentTypeError`, argparse prints a usage message and exits — no
traceback, no work on your side. That is where validation belongs: at the edge,
before anything is sent.

**Exit codes.** A program hands the shell a number when it finishes. `0` means
it worked. Anything else means it did not, and shell scripts test that number.
Printing an error and returning `0` is a lie that other programs believe.

## Requirements

1. Accept three positional arguments: `amount`, `source`, `target`.
2. Validate that `amount` is a positive number and that both codes are three
   letters, **before** any request goes out.
3. Call `/latest` with `amount`, `from` and `to` as query parameters.
4. Print the converted amount, the unit rate, and the date Frankfurter
   returned.
5. Handle failure without a traceback: an unsupported code gets a helpful
   message and a non-zero exit; a network failure gets a short message and a
   non-zero exit.
6. Every HTTP call passes `timeout=`.
7. A `--list` flag prints every supported code with its name, then exits `0`.

## Constraints

- **Do not hard-code an exchange rate anywhere in your own tool.** Rates move
  daily; a number in your source is wrong by tomorrow and wrong silently.
  (The shipped answer on this page *does* carry recorded rates, for a reason
  spelled out under **Download and run** — and it labels them with the date
  they were captured, which is the whole difference.)

- **Build the query with `params=`, never by concatenating strings.** Exercise
  1's Under the hood block shows what a value containing an `&` does to a
  hand-built URL.

- **Never call `eval()` on user input.** Not on the amount, not on anything.
  `float()` parses a number; `eval()` runs whatever was typed.

- **Errors go to `stderr`; results go to `stdout`.** So that
  `python currency.py 100 USD EUR > rate.txt` saves the rate and not the
  complaint. There is more on why in Under the hood.

- **Validate before you send.** A three-letter check costs nothing and stops a
  request that was never going to work. It also means the API's `404` is
  reserved for the case that actually needs it — a well-formed code the service
  does not publish.

- **Catch narrow exceptions, never bare `except Exception:`.** A typo in your
  own code should crash loudly, not be reported to the user as a network
  problem.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with requests
2.32.3:

```text
$ python challenge-01-currency-converter.py
--- replaying rates recorded on 2026-08-21; pass --live for today's ---
100.00 USD = 85.48 EUR  (rate 0.8548, ECB 2026-08-21)
50.00 GBP = 10836.00 JPY  (rate 216.72, ECB 2026-08-21)
caught ConversionError: 'XYZ' is not a supported currency code.
Run with --list to see supported codes.
30 supported codes, first five: AUD, BRL, CAD, CHF, CNY
```

Run with no arguments, the shipped file walks through three worked examples and
then reads the currency list. Run with arguments it is the tool:

```bash
$ python challenge-01-currency-converter.py 100 USD EUR --live
100.00 USD = 85.48 EUR  (rate 0.8548, ECB 2026-08-21)

$ python challenge-01-currency-converter.py 10 XYZ EUR --live
Error: 'XYZ' is not a supported currency code.
Run with --list to see supported codes.
```

Those two were captured live on the same day, which is why the first matches
the recording exactly. Run them tomorrow and the number moves. **The rate is
not the thing to check. The shape of the line is.**

Notice that the third example in the demo says `caught ConversionError:` rather
than `Error:`. That is not a different message — it is the same one, reached a
different way. `main()` sends errors to `stderr`, and `stderr` is not part of
the output this page can promise, so the demo calls `convert()` directly and
catches the exception the tool would have turned into that `stderr` line.

## Steps

1. Create `currency.py` and paste the starter in.
2. Write `currency_code()` first and test it alone:
   `python -c "import currency; print(currency.currency_code('usd'))"`. Then
   try `'us'` and read what argparse does with the error.
3. Write `get_json()` and call `/currencies` by hand. Print
   `len(payload)` — you should get 30 or so.
4. Write `convert()` and get one conversion printing. Do not format it nicely
   yet; print the whole `Quote` and check the fields.
5. Write `format_quote()` and match the line in the brief.
6. Now break it on purpose, four ways: an unknown code, a negative amount, a
   non-numeric amount, and no network at all (turn off your Wi-Fi). Each one
   should print one line and exit non-zero.
7. Check the exit codes: `echo $?` on macOS or Linux, `$LASTEXITCODE` in
   PowerShell.
8. Add `--list`.

## The Solution

```python
"""challenge-01-currency-converter-solution.py — convert money at ECB rates.

Wraps the Frankfurter API (https://frankfurter.dev), which publishes the
European Central Bank's daily reference rates. Free, keyless, no signup.

    python challenge-01-currency-converter-solution.py 100 USD EUR
    python challenge-01-currency-converter-solution.py --list
    python challenge-01-currency-converter-solution.py 100 USD EUR --live

This shipped answer replays **recorded** replies by default -- real bodies
captured from that API on 2026-08-21 -- so the download prints the same numbers
every time and works with no network. Exchange rates move every weekday, which
makes a live run impossible to write an expected output for. Pass ``--live``
and the identical code calls the real API for today's rates.

Run with no arguments at all and it walks through three worked examples.
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import Any, Callable, NamedTuple

import requests

BASE_URL = "https://api.frankfurter.app"
USER_AGENT = "code-crunch-bootcamp/1.0"
TIMEOUT_SECONDS = 5.0

#: A currency code is three capital letters. Nothing else gets sent.
CODE_PATTERN = re.compile(r"^[A-Z]{3}$")

#: Real replies captured from api.frankfurter.app on 2026-08-21, keyed by the
#: request that produced them. An int value means the API answered with that
#: status code instead of a document: Frankfurter returns 404 for a currency it
#: does not publish.
RECORDED: dict[str, dict[str, Any] | int] = {
    "/latest?amount=100.0&from=USD&to=EUR": {
        "amount": 100.0,
        "base": "USD",
        "date": "2026-08-21",
        "rates": {"EUR": 85.48},
    },
    "/latest?amount=50.0&from=GBP&to=JPY": {
        "amount": 50.0,
        "base": "GBP",
        "date": "2026-08-21",
        "rates": {"JPY": 10836},
    },
    "/latest?amount=10.0&from=XYZ&to=EUR": 404,
    "/currencies": {
        "AUD": "Australian Dollar",
        "BRL": "Brazilian Real",
        "CAD": "Canadian Dollar",
        "CHF": "Swiss Franc",
        "CNY": "Chinese Renminbi Yuan",
        "CZK": "Czech Koruna",
        "DKK": "Danish Krone",
        "EUR": "Euro",
        "GBP": "British Pound",
        "HKD": "Hong Kong Dollar",
        "HUF": "Hungarian Forint",
        "IDR": "Indonesian Rupiah",
        "ILS": "Israeli New Shekel",
        "INR": "Indian Rupee",
        "ISK": "Icelandic Krona",
        "JPY": "Japanese Yen",
        "KRW": "South Korean Won",
        "MXN": "Mexican Peso",
        "MYR": "Malaysian Ringgit",
        "NOK": "Norwegian Krone",
        "NZD": "New Zealand Dollar",
        "PHP": "Philippine Peso",
        "PLN": "Polish Zloty",
        "RON": "Romanian Leu",
        "SEK": "Swedish Krona",
        "SGD": "Singapore Dollar",
        "THB": "Thai Baht",
        "TRY": "Turkish Lira",
        "USD": "United States Dollar",
        "ZAR": "South African Rand",
    },
}

#: Anything that turns (path, query parameters) into a decoded JSON document.
Fetch = Callable[[str, dict[str, Any]], dict[str, Any]]


class ConversionError(Exception):
    """Raised when a conversion cannot be completed, for any reason.

    Everything the user needs to read is in str(exc). The original cause,
    where there was one, stays reachable as __cause__.
    """


class Quote(NamedTuple):
    """One completed conversion, with everything needed to print it."""

    amount: float
    source: str
    target: str
    converted: float
    rate: float
    date: str


def recorded_key(path: str, params: dict[str, Any]) -> str:
    """Build the RECORDED key for one request.

    Args:
        path: The API path, starting with a slash.
        params: Query parameters, or an empty dict.

    Returns:
        The path with its parameters appended in sorted order.
    """
    if not params:
        return path
    query = "&".join(f"{key}={params[key]}" for key in sorted(params))
    return f"{path}?{query}"


def fetch_live(path: str, params: dict[str, Any]) -> dict[str, Any]:
    """GET one Frankfurter path for real and return the decoded body.

    Args:
        path: The API path, starting with a slash.
        params: Query parameters, sent through params= so they are encoded.

    Returns:
        The decoded JSON document.

    Raises:
        ConversionError: the request failed, or the API refused it.
    """
    try:
        response = requests.get(
            f"{BASE_URL}{path}",
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as exc:
        raise ConversionError(describe_status(exc.response.status_code, params)) from exc
    except requests.exceptions.RequestException as exc:
        raise ConversionError(f"could not reach the rates service: {exc}") from exc


def fetch_recorded(path: str, params: dict[str, Any]) -> dict[str, Any]:
    """Answer one request from RECORDED, touching no network.

    Args:
        path: The API path, starting with a slash.
        params: Query parameters.

    Returns:
        The decoded JSON document.

    Raises:
        ConversionError: the recording holds a status code for this request.
        RuntimeError: nothing at all was recorded for this request. Nothing is
            wrong with your code; the recording is small. Use --live.
    """
    key = recorded_key(path, params)
    recorded = RECORDED.get(key)
    if recorded is None:
        raise RuntimeError(f"no recorded reply for {key}; re-run with --live")
    if isinstance(recorded, int):
        raise ConversionError(describe_status(recorded, params))
    return recorded


def describe_status(status_code: int, params: dict[str, Any]) -> str:
    """Turn a failing status code into a sentence a person can act on.

    Args:
        status_code: The status the API answered with.
        params: The parameters that produced it, used to name the code.

    Returns:
        One line of plain English.
    """
    if status_code == 404:
        unknown = params.get("from") or params.get("to") or "that code"
        return (
            f"'{unknown}' is not a supported currency code.\n"
            f"Run with --list to see supported codes."
        )
    return f"the rates service answered {status_code}."


def positive_amount(text: str) -> float:
    """Parse an amount, rejecting anything that is not a positive number.

    Args:
        text: The raw command-line argument.

    Returns:
        The amount as a float.

    Raises:
        argparse.ArgumentTypeError: not a number, or not above zero.
    """
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not a number") from None
    if value <= 0:
        raise argparse.ArgumentTypeError("amount must be greater than zero")
    return value


def currency_code(text: str) -> str:
    """Normalise and validate one currency code.

    Args:
        text: The raw command-line argument, in any case.

    Returns:
        The code in capitals.

    Raises:
        argparse.ArgumentTypeError: it is not three letters.
    """
    code = text.upper()
    if not CODE_PATTERN.match(code):
        raise argparse.ArgumentTypeError(
            f"{text!r} is not a three-letter currency code"
        )
    return code


def convert(
    amount: float, source: str, target: str, *, fetch: Fetch = fetch_live
) -> Quote:
    """Convert *amount* from *source* to *target* at the latest ECB rate.

    Args:
        amount: How much to convert. Must be positive.
        source: Three-letter code to convert from.
        target: Three-letter code to convert to.
        fetch: How to reach the API. Defaults to the real network.

    Returns:
        A Quote holding the converted amount, the unit rate, and the date.

    Raises:
        ConversionError: the API refused the request or could not be reached.
    """
    amount = float(amount)
    if source == target:
        return Quote(amount, source, target, amount, 1.0, "no conversion needed")
    params = {"amount": amount, "from": source, "to": target}
    payload = fetch("/latest", params)
    try:
        converted = float(payload["rates"][target])
    except (KeyError, TypeError) as exc:
        raise ConversionError(
            f"the rates service returned no rate for {target}."
        ) from exc
    return Quote(
        amount=amount,
        source=source,
        target=target,
        converted=converted,
        rate=converted / amount,
        date=payload["date"],
    )


def supported_codes(*, fetch: Fetch = fetch_live) -> dict[str, str]:
    """Return every currency code the service publishes, with its name.

    Args:
        fetch: How to reach the API. Defaults to the real network.

    Returns:
        A mapping of code to full name.

    Raises:
        ConversionError: the API could not be reached.
    """
    return fetch("/currencies", {})


def format_quote(quote: Quote) -> str:
    """Format one Quote as the single line the tool prints.

    Args:
        quote: A completed conversion.

    Returns:
        One line, with both amounts to two decimal places.
    """
    return (
        f"{quote.amount:.2f} {quote.source} = {quote.converted:.2f} {quote.target}"
        f"  (rate {quote.rate:.6g}, ECB {quote.date})"
    )


def main(argv: list[str] | None = None, *, fetch: Fetch | None = None) -> int:
    """Parse arguments, do the conversion, print the result.

    Args:
        argv: Arguments after the program name. None means sys.argv[1:].
        fetch: How to reach the API. None means "decide from --live".

    Returns:
        The process exit code. 0 on success, 2 on a handled failure.
    """
    parser = argparse.ArgumentParser(description="Convert money at ECB rates.")
    parser.add_argument("amount", nargs="?", type=positive_amount)
    parser.add_argument("source", nargs="?", type=currency_code)
    parser.add_argument("target", nargs="?", type=currency_code)
    parser.add_argument("--list", action="store_true", help="list supported codes")
    parser.add_argument("--live", action="store_true", help="call the real API")
    args = parser.parse_args(argv)

    get = fetch or (fetch_live if args.live else fetch_recorded)

    try:
        if args.list:
            codes = supported_codes(fetch=get)
            print(f"{len(codes)} supported codes:")
            for code in sorted(codes):
                print(f"  {code}  {codes[code]}")
            return 0
        if args.amount is None or args.source is None or args.target is None:
            parser.error("give an amount and two currency codes, or --list")
        print(format_quote(convert(args.amount, args.source, args.target, fetch=get)))
    except ConversionError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    return 0


def demo() -> int:
    """Walk through three worked examples against the recording.

    Returns:
        The process exit code.
    """
    print("--- replaying rates recorded on 2026-08-21; pass --live for today's ---")
    main(["100", "USD", "EUR"], fetch=fetch_recorded)
    main(["50", "GBP", "JPY"], fetch=fetch_recorded)

    # The third example fails on purpose. main() sends the message to stderr,
    # the way a command-line tool should, so the demo calls convert() directly
    # to show you the exception the tool turns into that stderr line.
    try:
        convert(10, "XYZ", "EUR", fetch=fetch_recorded)
    except ConversionError as err:
        print(f"caught ConversionError: {err}")

    codes = supported_codes(fetch=fetch_recorded)
    print(f"{len(codes)} supported codes, first five: {', '.join(sorted(codes)[:5])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(demo() if len(sys.argv) == 1 else main())
```

**Validation happens twice, at two different distances, and both are needed.**
`currency_code` rejects `"us"` and `"12"` before a single byte leaves your
machine, because those are not currency codes in any universe. But `"XYZ"` *is*
a well-formed code — it is just not one the ECB publishes — and no local check
can know that without the list. So the second layer is the API's `404`, turned
into the same sentence a person can act on. Cheap check first, authoritative
check second.

**`ConversionError` is the boundary, exactly like Exercise 5's `ApiError`.**
`main()` catches one exception type and prints one line. It does not know that
`requests` has five failure classes, and it does not know whether the failure
was a bad code or a dead network. That is why `main()` is nine lines and
readable.

**`fetch` is the seam.** `convert` and `supported_codes` take a `fetch`
argument and never mention `requests`. `fetch_live` calls the API;
`fetch_recorded` reads a constant. Both raise `ConversionError` for a failure,
so the error handling above them is tested by the recording too — including the
404 path, which is the one you would otherwise have to break the network to
reach.

**`describe_status` exists so the two fetchers cannot drift.** Both call it, so
the recorded 404 produces character-for-character the message the live 404
produces. When you build a stand-in, share the code that formats the answer;
fake only the part that goes over the wire.

**`fetch_recorded` distinguishes "recorded as a failure" from "not recorded".**
A `404` in the recording raises `ConversionError`, because that is a real
outcome. A request nobody recorded raises `RuntimeError` naming the key and
telling you to use `--live`, because that is not an outcome at all — it is a
gap in the fixture. Collapsing those two would teach you that any unrecorded
currency is an invalid currency, which is false.

**`Quote` is a `NamedTuple`, and the rate is computed once.** Frankfurter gives
you the converted total, not the unit rate; `converted / amount` is the rate,
and it belongs in the record rather than in the formatter. Same rule as
Exercise 2's decimetres: derive at the boundary, so nothing downstream has to
remember.

**`amount = float(amount)` at the top of `convert`.** An `int` and a `float`
are the same number to Python and two different strings in a URL —
`amount=10` against `amount=10.0`. Normalising at the top means the request is
the same whichever the caller passed, which matters for caching, for logs, and
here for finding the recording.

**`source == target` never asks the API.** Converting dollars to dollars has
one right answer and the network cannot improve on it. Every request you can
answer without sending is a request that cannot fail.

**Errors go to `stderr` and results to `stdout`.** So a pipe or a redirect
captures the number and not the complaint.

**Exit `2`, not `1` and not `0`.** Nonzero because it failed, and `2` by
convention for "you asked for something impossible" — which is also what
argparse itself exits with. A script wrapping your tool can test the number
instead of parsing your prose.

## Run it

Copy the worked answer on this page into `challenge-01-currency-converter.py` and run it:

```bash
python challenge-01-currency-converter.py
```

It needs `requests` installed and **no internet**. The four replies it uses
were captured from `api.frankfurter.app` on 2026-08-21 and pasted into the file
as `RECORDED`.

Recording this one is not laziness, it is the only honest option. Exchange
rates change every working day, so a page that promised you a live number would
be wrong within hours — and there is no way to write an expected output for a
value that moves. What *can* be promised is the shape of the line, the
behaviour of the error path, and the exit codes. Those are what the recording
pins down.

To call the real API, pass a flag:

```bash
python challenge-01-currency-converter.py 100 USD EUR --live
```

`--live` swaps `fetch_recorded` for `fetch_live` and changes nothing else. The
recording is small — four requests — so an unrecorded pair raises a
`RuntimeError` that tells you to use `--live` rather than pretending the
currency does not exist.

Two edits were made to the recorded currency list and both are cosmetic:
`Icelandic Króna` and `Polish Złoty` are stored without their accents, so that
the file is pure ASCII and cannot be mangled by an editor with the wrong
encoding. The live list has the accents, and Exercise 1 of Week 6 is where you
learned why they sometimes do not survive.

The `-solution` in the filename keeps this file from colliding with your own
`currency.py`.

## Common bugs to catch

- **`KeyError: 'EUR'` from `payload["rates"][target]`.**

  ```text
  Traceback (most recent call last):
    File "currency.py", line 61, in convert
      converted = payload["rates"][target]
                  ~~~~~~~~~~~~~~~~^^^^^^^^
  KeyError: 'EUR'
  ```

  You sent the target code in the wrong case, or you did not send `to` at all —
  in which case Frankfurter returns every currency it has and `EUR` really is
  in there, so this is more likely a case problem. Print `payload` and look.

- **`TypeError: '<=' not supported between instances of 'str' and 'int'`.** You
  wrote `type=positive_amount` but forgot the `float()` inside it, so you are
  comparing the raw string. argparse hands your `type=` function a `str`, every
  time.

- **The rate is 100 times too big.** You printed `payload["rates"][target]` as
  the rate. That field is the converted *total*, because you sent
  `amount=100`. The unit rate is `converted / amount`.

- **`Error: the rates service answered 404.` for a code you know is real.** You
  hit `/latest` with a lowercase code. Frankfurter's codes are uppercase;
  `currency_code` should have normalised it, so check that `type=` is actually
  wired to the argument.

- **A traceback instead of a message when the network is off.**

  ```text
  requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.frankfurter.app', port=443): Max retries exceeded with url: /latest?amount=100.0&from=USD&to=EUR (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x0000021B4C119160>: Failed to resolve 'api.frankfurter.app' ([Errno 11001] getaddrinfo failed)"))
  ```

  You caught `HTTPError` but not `RequestException`. A name-resolution failure
  never produces a status code, so `raise_for_status()` is never reached.

- **The tool prints an error and exits `0`.** You returned `0` from the
  `except` block, or you forgot `raise SystemExit(main())` and the return value
  went nowhere. Check with `echo $?`.

- **`argparse.ArgumentTypeError` escaping as a traceback.** You raised it from
  inside `convert()` instead of from a `type=` function. argparse only
  translates it for arguments it is parsing.

- **Today's rate does not match this page.** That is not a bug. Read the date
  in your own output.

## Under the hood

<details>
<summary>Under the hood — why errors belong on stderr</summary>

Every program starts with three channels open. `stdin` is where input arrives,
`stdout` is where results go, and `stderr` is where diagnostics go. The split
between the last two is the whole point, and it only becomes visible when
somebody redirects one of them.

```bash
$ python currency.py 100 USD EUR > rate.txt
$ cat rate.txt
100.00 USD = 85.48 EUR  (rate 0.8548, ECB 2026-08-21)
```

Now the failing case:

```bash
$ python currency.py 10 XYZ EUR > rate.txt
Error: 'XYZ' is not a supported currency code.
Run with --list to see supported codes.
$ cat rate.txt
$
```

The error appeared on screen even though stdout was redirected, and `rate.txt`
is empty rather than containing a sentence that is not a rate. That is the
behaviour you want in a pipeline: the next program in the chain gets data or
gets nothing, never prose.

Python's `print` writes to stdout unless told otherwise, so the whole
implementation is `file=sys.stderr`. The same idea, in the other direction, is
why §4c of the course framework insists that a program which asks the user
questions sends the *prompts* to stderr — so that
`python report.py > out.txt` saves the report and not the questions.

Two related habits fall out of it.

**stderr is unbuffered, or nearly so.** If your program dies halfway, the
diagnostics have usually already been written while buffered stdout may be
lost. That is another reason not to put them in the same stream.

**Redirect them separately when you need to.** `2> errors.log` sends only
stderr to a file; `2>&1` merges stderr into stdout; `2>/dev/null` throws
diagnostics away. In PowerShell the syntax differs but the streams are the
same.

</details>

<details>
<summary>Under the hood — never do money in floats, and what this tool gets away with</summary>

This tool prints `85.48` and it is fine, and both halves of that sentence are
worth understanding, because financial code that uses `float` is a genuine
professional hazard.

A `float` is a binary fraction. Some decimal numbers have no exact binary form,
in the same way that one third has no exact decimal form:

```text
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

Now scale that up. Add a hundred thousand small amounts and the tiny errors
accumulate into a real one — and financial systems are built out of exactly
that kind of loop. It is why banks do not use floats, why databases have a
`DECIMAL` type, and why Python ships `decimal.Decimal`:

```text
>>> from decimal import Decimal
>>> Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
True
```

`Decimal` stores digits in base ten, so a decimal fraction you can write down
is a decimal fraction it holds exactly. Note the strings in that example:
`Decimal(0.1)` from a float inherits the float's error, which defeats the
purpose entirely.

So why is this tool acceptable? Because of what it does and does not do.

**It converts once and prints once.** There is no accumulation, so there is
nothing for an error to accumulate into.

**It is informational.** Nobody is being charged this number. The ECB reference
rate is not a price you can trade at anyway — a real transaction has a spread
and fees on top of it.

**It rounds for display, at the end, once.** `f"{value:.2f}"` is the last thing
that happens to the number.

The line to draw: floats are fine for *estimating* money and unacceptable for
*holding* it. The moment a value is a balance, a ledger entry, or something
somebody is charged, it belongs in `Decimal` — or, better still, in an integer
count of the smallest unit, which is how a great deal of real financial code
stores money and why so many APIs quote amounts in cents.

There is a hint of it in the recording, by the way. `"JPY": 10836` came back as
an integer with no decimal point, because the yen has no subunit and JSON does
not distinguish integers from floats. A tool that assumed two decimal places
everywhere would already be slightly wrong about Japan.

</details>

## Acceptance checklist

- [ ] `python currency.py 100 USD EUR` prints one line with amount, rate and
      date.
- [ ] Lowercase codes work: `100 usd eur` gives the same answer.
- [ ] `10 XYZ EUR` prints a helpful message on stderr and exits non-zero.
- [ ] `-5 USD EUR` and `abc USD EUR` are rejected before any request goes out.
- [ ] `--list` prints every supported code and exits `0`.
- [ ] Every request passes `timeout=` and the query is built with `params=`.
- [ ] With the network off, the tool prints one line and exits non-zero.
- [ ] No bare `except Exception:` anywhere in the file.
- [ ] Committed to Git with a message like `Add Week 8 challenge 1: currency converter`.

## Stretch

- Add `--date YYYY-MM-DD`, which fetches a historical rate from `/{date}`
  instead of `/latest`. Then try a Sunday and read the `date` field in the
  reply carefully — you will not get back the date you asked for, and the
  reason is in the brief.

- Convert to several targets at once: `100 USD EUR GBP JPY`. Frankfurter takes
  a comma-separated `to`, so this is one parameter change and a loop over
  `payload["rates"]`.

- Cache the `/currencies` list to a local JSON file so `--list` works offline
  after the first run. Week 6's file patterns are what you need. Then decide
  how long the cache should live, and write the reason down.

- Redo the arithmetic with `decimal.Decimal` and compare the output on a
  hundred conversions. Where it differs, work out which one is right.

- Add a recorded reply of your own for a pair you care about, captured with
  `curl`, and prove your tool prints it correctly without going online.

When your tool handles all four failures cleanly, move on to
[Challenge 02 — GitHub User Stats](./challenge-02-github-user-stats.md).
