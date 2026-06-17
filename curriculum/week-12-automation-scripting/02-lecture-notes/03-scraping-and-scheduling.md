# Lecture 3 — Scraping and Scheduling

This lecture is about pulling information *out* of the web and getting your scripts to run *without you*. Both topics are huge — entire books exist for each — so we'll focus on the 80% that gives you the most leverage.

We'll cover **ethics first**, then mechanics. That order is deliberate.

---

## 1. Scraping ethics (read this section twice)

Web scraping is the act of programmatically downloading and parsing web pages that were designed for humans. It's *technically* doing the same thing your browser does. **But** the way you do it matters.

### 1.1 Check `robots.txt`

`robots.txt` is a plain-text file at the root of every well-behaved domain (e.g. `https://example.com/robots.txt`). It tells crawlers which paths they're allowed to fetch.

```
User-agent: *
Disallow: /private/
Crawl-delay: 5
```

Python ships with a parser:

```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://example.com/robots.txt")
rp.read()

if rp.can_fetch("MyBot/1.0", "https://example.com/private/list"):
    print("allowed")
else:
    print("disallowed by robots.txt")
```

`robots.txt` is **not** legally binding in most jurisdictions, but ignoring it is the fastest way to get your IP banned and (worse) to make life harder for the next person who tries to scrape that site.

### 1.2 Read the Terms of Service

If the site's ToS explicitly forbids scraping, treat that as a strong signal. For *commercial* projects, talk to a lawyer. For *personal learning* it usually doesn't matter — but be honest with yourself about what you're doing with the data.

### 1.3 Rate-limit yourself

A real human clicks once every few seconds. A naive script can fire 100 requests per second. That's a denial-of-service attack from the server's point of view.

Polite defaults:

- 1 request every 1–2 seconds for small sites.
- Honor `Crawl-delay` in `robots.txt`.
- Use exponential backoff on `429 Too Many Requests` or `503 Service Unavailable`.

```python
import time, random
time.sleep(1.0 + random.random())   # jittered delay
```

### 1.4 Identify yourself

Default `requests` user-agent is `python-requests/X.Y`. Replace it with something that says who you are:

```python
import requests

headers = {
    "User-Agent": "CodeCrunchBot/0.1 (+https://your-site.example; you@example.com)",
}
r = requests.get("https://example.com/", headers=headers, timeout=10)
```

If the site owner notices a problem, they can contact you instead of just blocking you. That's good citizenship.

### 1.5 Cache aggressively

Don't re-fetch the same page on every run. Save responses locally (`Path.write_bytes(r.content)`) and only refresh when you have to. Your scripts run faster *and* you put less load on the server.

### 1.6 When *not* to scrape

If an official **API** exists, use it. APIs are stable, documented, and intended for programmatic use. Scraping HTML is fragile — a CSS class change breaks your script overnight.

---

## 2. The mechanics: `requests` + `BeautifulSoup4`

Install the libraries (in a venv, please):

```bash
pip install requests beautifulsoup4
```

### 2.1 Fetching a page

```python
import requests

resp = requests.get(
    "http://quotes.toscrape.com/",
    headers={"User-Agent": "CodeCrunchBot/0.1"},
    timeout=10,
)
resp.raise_for_status()      # raise on 4xx/5xx
html = resp.text
```

`raise_for_status()` is the single most underused line in `requests` tutorials. **Use it.** Otherwise a 500 error silently becomes an empty page and you'll wonder why your scraper found nothing.

### 2.2 Parsing with BeautifulSoup

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
# 'html.parser' is built-in. For larger docs: pip install lxml; use "lxml".

title = soup.title.string
print(title)
```

### 2.3 CSS selectors (the part you'll actually use)

CSS selectors are the same syntax you'd use in JavaScript's `document.querySelectorAll`. Open the page in your browser, hit "Inspect", and copy the selector that wraps the data.

```python
quotes = soup.select("div.quote")           # all <div class="quote">
for q in quotes:
    text = q.select_one("span.text").get_text(strip=True)
    author = q.select_one("small.author").get_text(strip=True)
    tags = [t.get_text(strip=True) for t in q.select("a.tag")]
    print(f"{author}: {text}")
    print("  tags:", tags)
```

Common selectors:

| Selector            | Matches                                       |
|---------------------|-----------------------------------------------|
| `div.quote`         | Every `<div class="quote">`                   |
| `a[href^='/page/']` | Anchors whose `href` starts with `/page/`     |
| `ul > li`           | Direct `<li>` children of `<ul>`              |
| `#main`             | The element with `id="main"`                  |
| `[data-x]`          | Any element with attribute `data-x`           |

`select` returns a list, `select_one` returns the first match (or `None`).

### 2.4 Pagination

Quotes-to-Scrape paginates with `?page=N`. Loop until you stop seeing data:

```python
import requests, time
from bs4 import BeautifulSoup

session = requests.Session()
session.headers["User-Agent"] = "CodeCrunchBot/0.1"

page = 1
all_quotes: list[dict] = []
while True:
    url = f"http://quotes.toscrape.com/page/{page}/"
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    page_quotes = soup.select("div.quote")
    if not page_quotes:
        break
    for q in page_quotes:
        all_quotes.append({
            "text": q.select_one("span.text").get_text(strip=True),
            "author": q.select_one("small.author").get_text(strip=True),
        })
    page += 1
    time.sleep(1.0)         # be polite

print(f"got {len(all_quotes)} quotes")
```

Two patterns to notice:

1. **`requests.Session()`** reuses the TCP connection — faster, lower load on the server.
2. **The break condition is "empty result"** — robust to changes in pagination styles.

### 2.5 Forms and logged-in scraping

For form-based logins:

```python
session = requests.Session()
session.post("https://example.com/login",
             data={"username": "u", "password": "p"},
             timeout=10)
# subsequent session.get calls are authenticated
```

For sites that need CSRF tokens, fetch the login page first, parse the token from the form, then post it back. (This is where things stop being trivial.)

---

## 3. Headless browsers and Playwright

`requests` + `BeautifulSoup` only see the HTML the server sent. Modern sites build their UI with JavaScript *after* the page loads — and you'll see an empty `<div id="app"></div>` shell.

For those sites you need a real browser, headless (no GUI). **Playwright** is the modern choice. Selenium has been around longer but Playwright has a cleaner API, ships with the browsers it needs, and handles auto-waiting for elements.

Quick taste (overview only — install in your venv if you want to try):

```bash
pip install playwright
python -m playwright install chromium
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com/")
    print(page.title())
    browser.close()
```

When to reach for Playwright:

- The page renders content with JavaScript.
- You need to interact (click, type, scroll).
- You need to screenshot or generate a PDF.
- You need to test a real web app.

When to stick with `requests`:

- The HTML you need is in the initial response.
- You're scraping at high volume (Playwright is *much* slower).
- You're running in a tightly resourced environment (Playwright bundles a full browser).

We won't go deeper here, but a stretch goal of this week is to convert one of your scrapers to Playwright and feel the difference.

---

## 4. Scheduling: making things run without you

Three options, in order of complexity:

| Option              | When to use                                                       |
|---------------------|-------------------------------------------------------------------|
| `time.sleep` loop   | Quick scripts you start by hand and let run in a terminal.        |
| `schedule` package  | One-off Python process that runs jobs at intervals.               |
| `APScheduler`       | Long-running app, persistent job stores, cron-style triggers.     |
| cron (Unix)         | "Run this command at this time" — independent of your script.    |
| Task Scheduler (Win)| Cron's Windows cousin.                                            |

For most personal automation, **cron** is the answer. Run the Python script *as a regular script* and let the OS schedule it. That way the script doesn't have to know how to schedule itself.

### 4.1 The `schedule` package

```bash
pip install schedule
```

```python
import schedule, time

def job() -> None:
    print("backup running")

schedule.every().day.at("02:00").do(job)
schedule.every(15).minutes.do(job)
schedule.every().monday.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
```

Trade-offs:

- **Pros**: pure Python, no system config, easy to test.
- **Cons**: your script has to be running. If it crashes or the machine reboots, jobs stop. No persistence.

### 4.2 `APScheduler`

A more serious alternative for long-running apps. Highlights:

- Job stores (in-memory, SQLite, Redis).
- Cron-style triggers and interval triggers.
- Async support.

```python
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job("cron", hour=2, minute=0)
def nightly() -> None:
    print("nightly backup")

sched.start()
```

If you're building a service (Flask app, Discord bot, scraper that runs 24/7), `APScheduler` is a better fit than `schedule`.

### 4.3 cron (macOS / Linux)

A crontab entry has five time fields and a command:

```
# m   h   dom mon dow  command
  0   2   *   *   *    /usr/bin/python3 /home/jane/scripts/backup.py
```

| Field          | Meaning             | Range          |
|----------------|---------------------|----------------|
| Minute         | minute of hour      | 0–59           |
| Hour           | hour of day (24h)   | 0–23           |
| Day-of-month   | day                 | 1–31           |
| Month          | month               | 1–12 (or names)|
| Day-of-week    | weekday             | 0–6 (Sun=0)    |

Common shorthand: `@daily`, `@hourly`, `@reboot`, `@weekly`.

Install / edit your crontab:

```bash
crontab -e            # opens your editor
crontab -l            # list current jobs
```

Tips:

- Use **absolute paths**: cron's `PATH` is minimal.
- Activate your venv inside the command: `/path/to/venv/bin/python script.py`.
- Redirect logs: `>> /tmp/backup.log 2>&1`.
- Test the expression at [crontab.guru](https://crontab.guru/).

Example you might actually use:

```
0 9 * * 1   /home/jane/scripts/venv/bin/python /home/jane/scripts/weekly_report.py >> /home/jane/scripts/cron.log 2>&1
```

Every Monday at 9 a.m.

### 4.4 Windows Task Scheduler

GUI-based, but you can also use the `schtasks` command line.

```cmd
schtasks /Create /SC DAILY /TN "Backup" /TR "C:\Python\python.exe C:\scripts\backup.py" /ST 02:00
```

Or via the Task Scheduler UI: **Create Basic Task → Daily → Start a Program**.

Like cron, give absolute paths and a `Start in` directory.

### 4.5 GitHub Actions as a scheduler

If your script only needs the internet (and not your local files), GitHub Actions can run it on a schedule for free:

```yaml
# .github/workflows/scrape.yml
on:
  schedule:
    - cron: "0 6 * * *"
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python scrape.py
```

Great for daily scrapers, RSS-feed builders, and "send me an email if X" scripts.

---

## 5. Sending email with `smtplib`

The standard library can send mail through any SMTP server (Gmail, your ISP, an outbound relay like SendGrid, etc.).

```python
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Nightly report"
msg["From"] = "bot@example.com"
msg["To"] = "you@example.com"
msg.set_content("Backup finished successfully.")

with smtplib.SMTP_SSL("smtp.example.com", 465) as smtp:
    smtp.login("bot@example.com", "APP_PASSWORD")
    smtp.send_message(msg)
```

A few practicalities:

- **Never** hard-code passwords. Load them from environment variables (next section).
- For Gmail, you must create an **app password** in your Google account — your normal password won't work.
- For production use, use a transactional email service (Postmark, SES, SendGrid, Mailgun) — they handle deliverability for you.

---

## 6. Scripting with environment variables and `.env`

Twelve-factor rule of thumb: **config goes in the environment, not in code**.

```python
import os

api_key = os.environ["WEATHER_API_KEY"]   # raises KeyError if missing
smtp_pw = os.environ.get("SMTP_PASSWORD", "")  # default if missing
```

For local development, a `.env` file is the convention:

```
# .env
WEATHER_API_KEY=abcd1234
SMTP_PASSWORD=hunter2
```

Load it with [`python-dotenv`](https://pypi.org/project/python-dotenv/):

```python
from dotenv import load_dotenv
load_dotenv()      # reads .env into os.environ
```

**Critically**, add `.env` to your `.gitignore`. Otherwise you'll publish your secrets to GitHub — and bots will find them in minutes. Pair it with a checked-in `.env.example`:

```
# .env.example (commit this)
WEATHER_API_KEY=
SMTP_PASSWORD=
```

That way teammates know which variables to set without seeing your values.

---

## 7. Recap

- Scrape ethically: read `robots.txt`, rate-limit, identify yourself, prefer the API.
- `requests` + `BeautifulSoup4` cover static HTML. Playwright covers JavaScript-rendered pages.
- For scheduling: cron on Unix, Task Scheduler on Windows, `schedule` for in-process jobs, GitHub Actions for cloud cron.
- `smtplib` + `email.message.EmailMessage` send mail. Move credentials out of code.
- `.env` + `python-dotenv` + `.gitignore` is the standard pattern.

---

## Further reading

- BeautifulSoup4: [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- `requests` quickstart: [https://requests.readthedocs.io/en/latest/user/quickstart/](https://requests.readthedocs.io/en/latest/user/quickstart/)
- `urllib.robotparser`: [https://docs.python.org/3/library/urllib.robotparser.html](https://docs.python.org/3/library/urllib.robotparser.html)
- `schedule` docs: [https://schedule.readthedocs.io/](https://schedule.readthedocs.io/)
- crontab.guru: [https://crontab.guru/](https://crontab.guru/)
- Playwright Python: [https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)
- *Automate the Boring Stuff*, Chapters 12 ("Web Scraping") and 17 ("Scheduling Tasks and Launching Programs").
