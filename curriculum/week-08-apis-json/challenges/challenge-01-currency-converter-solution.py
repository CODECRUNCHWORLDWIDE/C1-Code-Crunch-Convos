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
