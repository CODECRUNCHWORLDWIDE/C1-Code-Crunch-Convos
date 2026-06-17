# Week 12 — Resources

Curated references to read alongside the lectures. Anything marked **(read)** is strongly recommended for the week; the rest are bookmark-worthy.

---

## Official Python documentation

- **`argparse`** — Parser for command-line options, arguments and sub-commands.
  https://docs.python.org/3/library/argparse.html **(read)**
- **`argparse` tutorial** — Friendlier introduction with worked examples.
  https://docs.python.org/3/howto/argparse.html
- **`subprocess`** — Spawn new processes, connect to their input/output/error pipes, and obtain return codes.
  https://docs.python.org/3/library/subprocess.html **(read)**
- **`shutil`** — High-level file operations: copy, move, archive, disk usage.
  https://docs.python.org/3/library/shutil.html **(read)**
- **`pathlib`** — Object-oriented filesystem paths.
  https://docs.python.org/3/library/pathlib.html
- **`os` and `os.path`** — Lower-level OS interfaces.
  https://docs.python.org/3/library/os.html
- **`sys`** — System-specific parameters and functions (incl. `sys.exit`, `sys.argv`).
  https://docs.python.org/3/library/sys.html
- **`logging`** — Reliable logging — way better than `print` for automation scripts.
  https://docs.python.org/3/library/logging.html
- **`smtplib`** — SMTP protocol client for sending email.
  https://docs.python.org/3/library/smtplib.html
- **`email`** — Building and parsing MIME messages (used with `smtplib`).
  https://docs.python.org/3/library/email.html
- **`urllib.robotparser`** — Parse `robots.txt` files.
  https://docs.python.org/3/library/urllib.robotparser.html

---

## Third-party libraries

- **`requests`** — HTTP for humans.
  https://requests.readthedocs.io/
- **`BeautifulSoup4`** — HTML/XML parsing.
  https://www.crummy.com/software/BeautifulSoup/bs4/doc/ **(read the "Quick Start" section)**
- **`schedule`** — Friendly in-process job scheduling.
  https://schedule.readthedocs.io/
- **`APScheduler`** — Heavier-duty scheduler with persistence and cron-like syntax.
  https://apscheduler.readthedocs.io/
- **`watchdog`** — OS-level file system event monitoring.
  https://python-watchdog.readthedocs.io/
- **`python-dotenv`** — Load environment variables from `.env`.
  https://pypi.org/project/python-dotenv/
- **`Playwright (Python)`** — Reliable browser automation.
  https://playwright.dev/python/docs/intro **(read the "Getting started" page)**
- **`Pillow`** — Image processing (used in homework).
  https://pillow.readthedocs.io/
- **`pypdf`** — Pure-Python PDF library (successor to `PyPDF2`).
  https://pypdf.readthedocs.io/

---

## Books

- **Al Sweigart — *Automate the Boring Stuff with Python* (2nd ed., No Starch Press, 2019)**. Full free read at https://automatetheboringstuff.com/ . Chapters 9, 10, 12, 15, 17, and 18 directly support this week. **(read at least one chapter)**
- **Mark Pilgrim — *Dive Into Python 3*** (free online): https://diveintopython3.net/ — handy for `subprocess` background.
- **Doug Hellmann — *The Python 3 Standard Library by Example***. The `argparse`, `subprocess`, `shutil`, and `pathlib` chapters are gold.

---

## Articles (Real Python)

- "Build Command-Line Interfaces With Python's argparse" — https://realpython.com/command-line-interfaces-python-argparse/
- "An Introduction to subprocess in Python With Examples" — https://realpython.com/python-subprocess/
- "Beautiful Soup: Build a Web Scraper With Python" — https://realpython.com/beautiful-soup-web-scraper-python/
- "Run Python Versions in Docker: How to Try the Latest Python Release" — useful for scheduled scripts in containers. https://realpython.com/python-versions-docker/
- "Working With Files in Python" — https://realpython.com/working-with-files-in-python/
- "Sending Emails With Python" — https://realpython.com/python-send-email/
- "Modern Web Automation With Python and Selenium" — context for why we prefer Playwright today.
  https://realpython.com/modern-web-automation-with-python-and-selenium/

---

## Ethics & legal background for scraping

- **`robots.txt` specification (RFC 9309)** — https://www.rfc-editor.org/rfc/rfc9309.html
- **EFF on scraping & the CFAA (US legal context)** — https://www.eff.org/issues/cfaa
- **hiQ Labs vs. LinkedIn (US 9th Circuit, 2022)** — public data scraping landmark. Background reading: https://www.eff.org/deeplinks/2022/04/scraping-public-websites-still-isnt-crime-court-appeals-confirms

---

## Tooling cheat-sheets

- **cron** — https://crontab.guru/ (interactive cron expression builder)
- **Windows Task Scheduler** — https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page
- **GitHub Actions `schedule` trigger** — https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule

---

## Practice playgrounds

- **Quotes to Scrape** — http://quotes.toscrape.com/ (used in exercise 04)
- **Books to Scrape** — http://books.toscrape.com/
- **HTTPBin** — https://httpbin.org/ (great for testing `requests`)
- **httpstat.us** — https://httpstat.us/ (return arbitrary HTTP status codes)

Use these instead of hammering real production sites while you learn.
