"""exercise-04-scrape-quotes-solution.py — the quotes scraper, proven offline.

The exercise part is the starter with its TODOs filled in: fetch
https://quotes.toscrape.com page by page, pull the text, author, and tags out
of each quote, stop on the first empty page, and write JSON.

Your own exercise-04-scrape-quotes.py ends in ``raise SystemExit(main())`` and
hits the live practice site. A published answer must not depend on somebody
else's uptime or spend their bandwidth every time a test runs, so this file
ships a recorded copy of page 1 (RECORDED_PAGES, real quotes captured from the
site) behind a one-line fetch seam. With USE_LIVE = False it parses the
recording, never touching the network, and prints the same thing every run. The
parser being tested is identical either way; set USE_LIVE = True to fetch for
real.

When you do go live, do it the way Lecture 3 §1 lays out: read the site's
robots.txt and its Terms of Service first, send the real User-Agent below so an
operator can find you, and keep the delay.

Run it with::

    python exercise-04-scrape-quotes-solution.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
USER_AGENT = "CodeCrunchBot/0.1 (Week 12 exercise; you@example.com)"
CURLY_QUOTES = "“”"
MIN_DELAY = 0.5
TIMEOUT = 10

# Flip to True to fetch the real site instead of the recording below.
USE_LIVE = False

# A recorded copy of page 1: the ten real quotes from quotes.toscrape.com, with
# only the elements parse_quotes reads. Page 2 is deliberately absent, so the
# scraper meets an empty page and stops — the same signal the live site gives
# past its last page.
RECORDED_PAGES: dict[int, str] = {
    1: """\
<html><body>
<div class="quote"><span class="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span><small class="author">Albert Einstein</small><div class="tags"><a class="tag">change</a><a class="tag">deep-thoughts</a><a class="tag">thinking</a><a class="tag">world</a></div></div>
<div class="quote"><span class="text">“It is our choices, Harry, that show what we truly are, far more than our abilities.”</span><small class="author">J.K. Rowling</small><div class="tags"><a class="tag">abilities</a><a class="tag">choices</a></div></div>
<div class="quote"><span class="text">“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”</span><small class="author">Albert Einstein</small><div class="tags"><a class="tag">inspirational</a><a class="tag">life</a><a class="tag">live</a><a class="tag">miracle</a><a class="tag">miracles</a></div></div>
<div class="quote"><span class="text">“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”</span><small class="author">Jane Austen</small><div class="tags"><a class="tag">aliteracy</a><a class="tag">books</a><a class="tag">classic</a><a class="tag">humor</a></div></div>
<div class="quote"><span class="text">“Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.”</span><small class="author">Marilyn Monroe</small><div class="tags"><a class="tag">be-yourself</a><a class="tag">inspirational</a></div></div>
<div class="quote"><span class="text">“Try not to become a man of success. Rather become a man of value.”</span><small class="author">Albert Einstein</small><div class="tags"><a class="tag">adulthood</a><a class="tag">success</a><a class="tag">value</a></div></div>
<div class="quote"><span class="text">“It is better to be hated for what you are than to be loved for what you are not.”</span><small class="author">André Gide</small><div class="tags"><a class="tag">life</a><a class="tag">love</a></div></div>
<div class="quote"><span class="text">“I have not failed. I've just found 10,000 ways that won't work.”</span><small class="author">Thomas A. Edison</small><div class="tags"><a class="tag">edison</a><a class="tag">failure</a><a class="tag">inspirational</a><a class="tag">paraphrased</a></div></div>
<div class="quote"><span class="text">“A woman is like a tea bag; you never know how strong it is until it's in hot water.”</span><small class="author">Eleanor Roosevelt</small><div class="tags"><a class="tag">misattributed-eleanor-roosevelt</a></div></div>
<div class="quote"><span class="text">“A day without sunshine is like, you know, night.”</span><small class="author">Steve Martin</small><div class="tags"><a class="tag">humor</a><a class="tag">obvious</a><a class="tag">simile</a></div></div>
</body></html>
""",
}


def polite_delay(value: str) -> float:
    """Parse a delay in seconds, refusing anything under half a second.

    Raises:
        argparse.ArgumentTypeError: if the delay is below 0.5.
    """
    seconds = float(value)
    if seconds < MIN_DELAY:
        raise argparse.ArgumentTypeError(
            f"delay must be at least {MIN_DELAY} seconds, got {seconds}"
        )
    return seconds


def fetch_page(session: requests.Session, page: int) -> str:
    """Return the HTML of one page — from the recording, or live if USE_LIVE.

    This is the seam. Everything else in the file is the same whether the bytes
    came off the network or out of RECORDED_PAGES, which is exactly why a
    recording can stand in for the site.
    """
    if USE_LIVE:
        response = session.get(f"{BASE_URL}/page/{page}/", timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    return RECORDED_PAGES.get(page, "")


def parse_quotes(html: str) -> list[dict[str, object]]:
    """Extract every quote on one page of HTML.

    Returns a list of dicts with keys "text", "author", and "tags".
    An empty list means the page held no quotes.
    """
    soup = BeautifulSoup(html, "html.parser")
    quotes: list[dict[str, object]] = []
    for block in soup.select("div.quote"):
        text_node = block.select_one("span.text")
        author_node = block.select_one("small.author")
        if text_node is None or author_node is None:
            continue
        quotes.append({
            "text": text_node.get_text(strip=True).strip(CURLY_QUOTES),
            "author": author_node.get_text(strip=True),
            "tags": [tag.get_text(strip=True) for tag in block.select("a.tag")],
        })
    return quotes


def scrape(session: requests.Session, pages: int, delay: float) -> list[dict[str, object]]:
    """Fetch up to `pages` pages, sleeping `delay` seconds between requests."""
    collected: list[dict[str, object]] = []
    for page in range(1, pages + 1):
        print(f"fetching {BASE_URL}/page/{page}/")
        found = parse_quotes(fetch_page(session, page))
        print(f"  {len(found)} quotes")
        if not found:
            break
        collected.extend(found)

        if page < pages:
            time.sleep(delay)
    return collected


def main(argv: list[str] | None = None) -> int:
    """Scrape, write the JSON file, return an exit code."""
    parser = argparse.ArgumentParser(
        prog="scrape-quotes",
        description="Collect quotes from the Scrapy practice site into JSON.",
    )
    parser.add_argument("--pages", type=int, default=2,
                        help="Maximum pages to fetch (default: %(default)s)")
    parser.add_argument("--delay", type=polite_delay, default=1.0,
                        help="Seconds between requests, minimum 0.5 (default: %(default)s)")
    parser.add_argument("--out", type=Path, default=Path("quotes.json"),
                        help="Where to write the JSON (default: %(default)s)")
    args = parser.parse_args(argv)

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    try:
        quotes = scrape(session, args.pages, args.delay)
    except requests.RequestException as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    args.out.write_text(
        json.dumps(quotes, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(quotes)} quotes to {args.out}")
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — scrape the recording into a temp file, then show the
# first record. Your own file has no demo; it hits the live site from the shell.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Scrape the recorded page and print the first record it wrote."""
    print("Scrape Quotes — proven offline against a recorded copy of page 1.")
    print()
    original = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            code = main(["--pages", "2", "--delay", "0.5"])
            data = json.loads(Path("quotes.json").read_text(encoding="utf-8"))
        finally:
            os.chdir(original)
    print(f"[exit {code}]")
    print()

    first = data[0]
    print("first record written to quotes.json:")
    print(f"  text  : {first['text']}")
    print(f"  author: {first['author']}")
    print(f"  tags  : {', '.join(first['tags'])}")
    print()
    print(f"quotes collected: {len(data)} (the recording is page 1; page 2 is empty, so it stops)")


if __name__ == "__main__":
    demo()
