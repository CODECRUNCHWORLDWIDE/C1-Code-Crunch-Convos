# Exercise 4 — Scrape Quotes

> **Topic:** `requests` + `BeautifulSoup` — fetching, selecting, paginating, and doing it politely
> **Lecture:** [03 — Scraping and Scheduling](../lecture-notes/03-scraping-and-scheduling.md)
> **Difficulty:** Medium
> **Target time:** 35 min
> **Why this one:** the mechanics of scraping take about ten minutes to learn. The manners take longer, and they are what keeps you out of trouble. Challenge 1 asks you to poll a live URL on a schedule; if the polite-client habits are not automatic by then, you will write something that hammers a stranger's server every sixty seconds. Build them here, on a site that was made for it.

## The Brief

Collect quotes from a practice site into a JSON file you can use later —
Week 13 will hand it to pandas. Each record holds the quote text, the author,
and the list of tags.

Everything here targets **`https://quotes.toscrape.com`**, published by the
maintainers of Scrapy for exactly one purpose: giving people somewhere safe to
practice. Its content is fake and nobody's business depends on its uptime. The
site paginates at `/page/1/`, `/page/2/`, and so on, ten quotes per page. Past
the last page it serves a page with no quotes rather than a 404, which gives
you a clean stopping condition: fetch until a page comes back empty.

Your script has **no `--url` flag**. The base URL is a constant in the source.
That is a design choice, not laziness: a practice scraper with a `--url` flag
is a general-purpose scraper, and the first time someone points it at a live
site with `--delay 0`, the manners you learned here stop mattering. Before you
point any scraper at any other domain, do the four things Lecture 3 §1 lists:
read `robots.txt` at the root and honour it; read the Terms of Service and treat
a ban on automated access as your answer; check whether an official API exists,
because if it does it is stable, documented, and intended for you; and ask
whether the data is yours to take at all.

## Starter

Install the two libraries in your virtual environment first:

```bash
pip install requests beautifulsoup4
```

```python
"""exercise-04-scrape-quotes.py — collect quotes from the Scrapy practice site.

Fetches https://quotes.toscrape.com page by page, extracts text, author, and
tags for each quote, and writes the result to JSON.

This script targets one practice site on purpose. Do not repoint it.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
USER_AGENT = "CodeCrunchBot/0.1 (Week 12 exercise; you@example.com)"
CURLY_QUOTES = "“”"


def polite_delay(value: str) -> float:
    """Parse a delay in seconds, refusing anything under half a second.

    Raises:
        argparse.ArgumentTypeError: if the delay is below 0.5.
    """
    # TODO: float(value), reject < 0.5 with argparse.ArgumentTypeError
    raise NotImplementedError


def parse_quotes(html: str) -> list[dict[str, object]]:
    """Extract every quote on one page of HTML.

    Returns a list of dicts with keys "text", "author", and "tags".
    An empty list means the page held no quotes.
    """
    soup = BeautifulSoup(html, "html.parser")
    # TODO: soup.select("div.quote"), then per block:
    #   span.text  -> strip the curly quotation marks with .strip(CURLY_QUOTES)
    #   small.author
    #   a.tag      -> a list of strings
    raise NotImplementedError


def scrape(session: requests.Session, pages: int, delay: float) -> list[dict[str, object]]:
    """Fetch up to `pages` pages, sleeping `delay` seconds between requests."""
    collected: list[dict[str, object]] = []
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/page/{page}/"
        print(f"fetching {url}")
        # TODO: session.get(url, timeout=10), then raise_for_status()
        # TODO: parse, print f"  {len(found)} quotes", break when empty
        # TODO: sleep `delay` between requests, but not after the last one
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
    # TODO: scrape, then write JSON with indent=2 and ensure_ascii=False
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. Every request carries the `USER_AGENT` header and a `timeout=10`.
2. Every response goes through `raise_for_status()` before you parse it.
3. Sleep at least `--delay` seconds between requests. Do not sleep after the
   final request — that is dead time that helps nobody.
4. Stop early when a page yields zero quotes, even if `--pages` allows more.
5. Quote text is stored without the surrounding curly quotation marks the site
   wraps it in.
6. The JSON file is written with `indent=2` and `ensure_ascii=False`, so the
   apostrophes and accents stay readable instead of turning into `\uXXXX`.
7. Exit 0 on success; exit 1 with a message on stderr if the site cannot be
   reached.

## Constraints

- **Use one `requests.Session` for the whole run.** It reuses the TCP
  connection and sends your headers every time without you remembering. Ten
  separate `requests.get` calls open ten connections to do the work of one.
- **Set the delay with a `type=` callable that enforces a floor of 0.5s.** A
  plain `type=float` lets `--delay 0` through, and a scraper with no delay is
  a load test somebody else is paying for. Putting the floor in the parser
  means nobody can turn the manners off from the command line.
- **`raise_for_status()` before parsing, always.** Without it a 503 page
  parses fine, yields zero quotes, trips your empty-page stop condition, and
  the script reports success with no data. A silent wrong answer is worse than
  a crash.
- **Select with CSS selectors (`div.quote`, `span.text`), not by walking
  `.children` or slicing raw HTML with `re`.** Selectors survive the
  whitespace and attribute-order changes that break both alternatives.
- **Keep `BASE_URL` a module constant with no CLI override.** See the top of
  this page.
- **Do not add threads or `asyncio`.** Concurrency here would only make you
  faster at being impolite, and there are ten pages.

## Expected output

The shipped answer, [`exercise-04-scrape-quotes-solution.py`](./exercise-04-scrape-quotes-solution.py),
ships a recorded copy of page 1 — the ten real quotes — behind a one-line
`fetch_page` seam, so it runs with no network and prints the same thing every
time. Page 2 is deliberately absent, so the scraper meets an empty page and
stops, exactly as it would past the live site's last page. Real captured output:

```text
$ python exercise-04-scrape-quotes-solution.py
Scrape Quotes — proven offline against a recorded copy of page 1.

fetching https://quotes.toscrape.com/page/1/
  10 quotes
fetching https://quotes.toscrape.com/page/2/
  0 quotes
wrote 10 quotes to quotes.json
[exit 0]

first record written to quotes.json:
  text  : The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.
  author: Albert Einstein
  tags  : change, deep-thoughts, thinking, world

quotes collected: 10 (the recording is page 1; page 2 is empty, so it stops)
```

Set `USE_LIVE = True` and the same code fetches the real site instead; the
`fetching`/`N quotes` lines and the JSON are identical, only the bytes now come
off the network.

## Steps

1. Open `https://quotes.toscrape.com/robots.txt` in a browser and read
   whatever comes back. If it is a 404, note that "no rules published" is not
   the same as "permission granted" — the site has simply not written any down.
2. Open `https://quotes.toscrape.com/page/1/`, right-click a quote, and choose
   Inspect. Your selectors should come from what you see there, not from this
   page.
3. Implement `polite_delay` and `parse_quotes`. Test `parse_quotes` against a
   page you already saved to disk — no network, and no traffic spent on a
   parser bug.
4. Implement `scrape` and debug it with `--pages 1`. One page, one request.
5. Run `--pages 2`, then read `quotes.json` in your editor. Are the tags a
   real list, or one string with commas in it?
6. Run `--pages 20` and watch it stop on its own at the first empty page. Then
   try `--delay 0` and confirm the parser refuses before any request is sent.

## The Solution

The shipped file is your answer — `polite_delay`, `parse_quotes`, `scrape`,
`main` — plus a `fetch_page` seam and a recorded page so it proves itself
offline. Your own file has no recording and no `USE_LIVE`; it always hits the
live site. Everything else is the same.

```python
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
```

**The fetch seam is the whole trick.** `parse_quotes`, the pagination, the stop
condition, and the JSON writing do not care whether the HTML came off a socket
or out of a module constant, so the recording stands in for the site with no
change to any of it. That is also the shape of a good test: the part that talks
to the world is one small function you can swap, and everything worth testing
sits above it.

**The delay floor lives in the parser, so it is enforced before a single packet
moves.** `--delay 0` never reaches `main()`; `argparse` rejects it with exit 2
while the `Session` does not yet exist. Compare that with an `if delay < 0.5`
inside `scrape()`, which runs after the first request has already gone out.
Politeness that a flag can switch off is not politeness, it is a default.

**`str.strip` takes a set of characters, not a substring.** `CURLY_QUOTES` is
the two-character string `"“”"`, and `.strip(CURLY_QUOTES)` removes any of those
characters from either end. This trips people up in both directions: it is
*not* looking for the sequence `“”`, and `.strip('"')` does nothing here because
the straight double quote on your keyboard is a different character from the
curly ones the site uses.

**Tags are built by iterating `a.tag`, not by reading their container.**
`block.select("a.tag")` gives a list of anchor elements, one per tag, and the
comprehension turns each into its own string. Ask the container for its text
instead and you get `Tags:changedeep-thoughtsthinkingworld` — one string, the
word `Tags:` glued to the front, and no separator anywhere to split on
afterwards. Structure you have thrown away is expensive to get back.

**`ensure_ascii=False` with `encoding="utf-8"` is what makes the file
readable.** By default `json.dump` escapes every non-ASCII character to a
`\uXXXX` sequence — valid JSON, no data lost, and unreadable. `André Gide`
becomes `André Gide`. Week 13 opens this file in an editor, so it is
written as real UTF-8, and the two settings are a pair: emit raw non-ASCII and
then let Windows pick the encoding, and you get a code-page-1252 file that
anything else misreads.

**In the live version, `raise_for_status()` runs before parsing, every time.**
Skip it and a 404 or 503 parses to zero quotes, trips the empty-page stop
condition on page one, and the script writes an empty file and reports success.
A crash you can see beats a success you cannot check.

## Download and run

Download
[exercise-04-scrape-quotes-solution.py](./exercise-04-scrape-quotes-solution.py)
and run it:

```bash
pip install requests beautifulsoup4
python exercise-04-scrape-quotes-solution.py
```

It runs against the recorded page with no network at all, so you can also
[run it in the online editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-12-automation-scripting/exercises/exercise-04-scrape-quotes.md).
The `-solution` in the name keeps it from colliding with your own
`exercise-04-scrape-quotes.py`.

## Common bugs to catch

- **`AttributeError: 'NoneType' object has no attribute 'get_text'`.**
  `select_one` returns `None` when nothing matches, and you called `.get_text()`
  on it. Either your selector is wrong, or you are on a page with no quotes.
  Check the block for `None` before reaching into it.
- **Quote text arrives as `"“The world as we have created it ...”"`.**
  The site wraps the text in curly quotation marks, which are not the plain
  `"` on your keyboard. `.strip('"')` will not remove them. Strip the actual
  characters, `“` and `”`.
- **`requests.exceptions.MissingSchema: Invalid URL '/page/2/'`.** You built
  the URL from the `href` you found in the HTML, which is a relative path.
  This answer sidesteps it by building `f"{BASE_URL}/page/{page}/"` from a
  counter; if you follow links instead, join them with `urllib.parse.urljoin`.
- **`json.decoder.JSONDecodeError`** when you read the file back. You called
  `json.dump` once per page, so the file holds several JSON documents glued
  together. Collect everything in one list and dump once.
- **Every quote is identical, a hundred times over.** Your loop calls
  `session.get` with `page` fixed at 1, or you appended the same dict object
  each pass instead of building a new one.
- **The script finishes instantly and writes an empty list.** Something
  returned a non-200 and you skipped `raise_for_status()`, so an error page
  parsed to zero quotes and tripped the stop condition on page one.
- **`ModuleNotFoundError: No module named 'bs4'`.** The package on PyPI is
  `beautifulsoup4`; the module you import is `bs4`. Also check your virtual
  environment is active — installing into one Python and running another is
  the classic version of this.
- **The JSON has `"tags": "changedeep-thoughtsthinkingworld"`.** You called
  `get_text()` on the container instead of iterating `a.tag` into a list.

## Under the hood

<details>
<summary>Under the hood — why a recorded response is the honest way to test a scraper</summary>

A scraper has two jobs tangled together: fetching bytes over the network, and
turning those bytes into structured data. The network half is slow, flaky, and
someone else's server; the parsing half is where all your bugs actually live.
Testing them together means every run of your parser test spends a real HTTP
request on a real site, fails randomly when the site is slow, and changes its
answer the day the site's content changes. None of that is testing your code.

Pulling the fetch into its own one-line function — the seam — lets you feed the
parser bytes you captured once and control completely. Now the parser test is
instant, deterministic, offline, and pinned to a known page, and it fails only
when *your* parsing changes. The shipped answer does exactly this with a module
constant, and flipping `USE_LIVE` swaps the recording for the live call without
touching a line of the parsing logic. The same shape scales up: a bigger project
records fixtures to files, or uses a library like `responses` or `vcrpy` to tape
real HTTP traffic and replay it, but the idea is the one you just used — isolate
the part that talks to the world so the rest can be tested without it.

</details>

## Acceptance checklist

- [ ] `--pages 2` against the live site writes exactly 20 records.
- [ ] `--pages 20` stops on its own at the first empty page and writes 100.
- [ ] Quote text has no leading or trailing curly quotation marks.
- [ ] `tags` is a JSON array of strings.
- [ ] `--delay 0` is rejected by the parser, before any network call.
- [ ] The `User-Agent` header names the bot and gives a way to contact you.
- [ ] `BASE_URL` appears once and no flag can change it.
- [ ] The file is committed to Git with a message like
      `Add Week 12 exercise 4: quotes scraper`.

## Stretch

- Cache each page to `cache/page-N.html` and read from the cache when the file
  exists. Add `--refresh` to bypass it. Lecture 3 §1.5 explains why this is
  the most polite thing a scraper can do.
- Check `robots.txt` from inside the script with `urllib.robotparser` and
  refuse any path it disallows. Lecture 3 §1.1 has the six lines you need.
- Write a `pytest` test for `parse_quotes` using a small HTML string defined
  in the test file. No network, no flakiness, instant feedback — the same idea
  the shipped answer's recording is built on.

When your scraper stops on its own and sleeps between pages, move on to
[Exercise 5 — Schedule](./exercise-05-schedule.md).
