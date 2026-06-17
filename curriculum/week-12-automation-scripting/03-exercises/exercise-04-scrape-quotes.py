"""Exercise 04 — Scrape quotes.

Fetch http://quotes.toscrape.com/ (a site explicitly built for practice
scraping) and print the first 10 quotes as "AUTHOR: TEXT".

Run:
    pip install requests beautifulsoup4
    python exercise-04-scrape-quotes.py

Stretch:
  1. Add a --pages N flag to scrape the first N pages.
  2. Save results to quotes.json instead of printing.
  3. Add a 1-second sleep between page requests (we are not in a hurry).
  4. Use urllib.robotparser to confirm we are allowed to scrape this URL.
"""
from __future__ import annotations

import argparse
import sys
import time
from typing import Iterable

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com/page/{page}/"
USER_AGENT = "CodeCrunchBot/0.1 (Week 12 exercise)"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Scrape quotes.toscrape.com")
    p.add_argument("--limit", type=int, default=10, help="Max quotes to print")
    p.add_argument("--pages", type=int, default=1, help="Pages to fetch (default: 1)")
    return p


def fetch_page(session: requests.Session, page: int) -> str:
    url = BASE_URL.format(page=page)
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_quotes(html: str) -> list[dict[str, str | list[str]]]:
    soup = BeautifulSoup(html, "html.parser")
    results: list[dict[str, str | list[str]]] = []
    for quote in soup.select("div.quote"):
        text_el = quote.select_one("span.text")
        author_el = quote.select_one("small.author")
        if text_el is None or author_el is None:
            continue
        results.append({
            "text": text_el.get_text(strip=True),
            "author": author_el.get_text(strip=True),
            "tags": [t.get_text(strip=True) for t in quote.select("a.tag")],
        })
    return results


def iter_quotes(pages: int) -> Iterable[dict[str, str | list[str]]]:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    for page in range(1, pages + 1):
        html = fetch_page(session, page)
        page_quotes = parse_quotes(html)
        if not page_quotes:
            return
        yield from page_quotes
        time.sleep(1.0)        # polite delay


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    printed = 0
    for q in iter_quotes(args.pages):
        if printed >= args.limit:
            break
        print(f"{q['author']}: {q['text']}")
        printed += 1
    if printed == 0:
        print("no quotes found", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
