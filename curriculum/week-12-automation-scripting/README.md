# Week 12 — Automation & Scripting

Welcome to Week 12 of **Code Crunch Convos**! This week we turn Python into a tireless personal assistant. You will write small programs that replace the boring, repetitive parts of your day: organizing files, scraping websites, scheduling jobs, sending emails, and running shell commands — all from Python.

By the end of the week you will have a complete CLI tool, a **File Organizer Bot**, plus a toolbox of patterns you can reuse forever.

---

## Learning Objectives

By the end of Week 12, you will be able to:

1. Adopt an **automation mindset** — spot tasks worth automating and estimate the payoff.
2. Build polished command-line scripts with `argparse` (positional/optional args, subcommands, help text, exit codes).
3. Run shell commands safely from Python with `subprocess.run` and capture their output.
4. Use `pathlib` and `shutil` to copy, move, archive, and rename files at scale.
5. Detect file changes by polling a directory (no extra dependencies).
6. Schedule scripts using **cron** (macOS/Linux), **Task Scheduler** (Windows), or the `schedule` Python package.
7. Scrape static web pages with `requests` + `BeautifulSoup4` — and do it ethically (`robots.txt`, rate limits, identification).
8. Know when a headless browser like **Playwright** is the right tool.
9. Send notification emails with `smtplib`.
10. Load secrets from a `.env` file using environment variables.

---

## Prerequisites

You should be comfortable with everything covered in **Weeks 1–11**, especially:

- Functions, modules, and packages (Week 4).
- Lists, dicts, comprehensions (Week 5).
- File I/O and exception handling (Week 6).
- Classes and dataclasses (Week 7).
- Working with HTTP APIs and JSON (Week 8).
- Virtual environments and `pip install` (recap as needed).
- Writing unit tests (Week 11).

If any of those feels rusty, revisit the relevant week before diving in.

---

## Topics Covered

| # | Topic                                                            | Where to find it                                    |
|---|------------------------------------------------------------------|-----------------------------------------------------|
| 1 | The automation mindset                                           | `lecture-notes/01-cli-scripts-with-argparse.md`     |
| 2 | `argparse` for CLI scripts                                       | `lecture-notes/01-cli-scripts-with-argparse.md`     |
| 3 | `subprocess` — running shell commands from Python                | `lecture-notes/02-file-system-and-subprocess.md`    |
| 4 | `pathlib` recap + `shutil` for copy/move/archive                 | `lecture-notes/02-file-system-and-subprocess.md`    |
| 5 | Watching for file changes (poll-based)                           | `lecture-notes/02-file-system-and-subprocess.md`    |
| 6 | Web scraping with `requests` + `BeautifulSoup4`                  | `lecture-notes/03-scraping-and-scheduling.md`       |
| 7 | Respecting `robots.txt`, ToS, rate limits                        | `lecture-notes/03-scraping-and-scheduling.md`       |
| 8 | Headless browsers (Playwright overview)                          | `lecture-notes/03-scraping-and-scheduling.md`       |
| 9 | Scheduling: `schedule`, `apscheduler`, cron, Task Scheduler      | `lecture-notes/03-scraping-and-scheduling.md`       |
| 10| Sending emails (`smtplib`) and `.env` configuration              | `lecture-notes/03-scraping-and-scheduling.md`       |

---

## Schedule (~36 hours total)

| Day      | Focus                                              | Hours |
|----------|----------------------------------------------------|-------|
| Mon      | Read lecture 1; complete exercises 01 and 02       |   5   |
| Tue      | Read lecture 2; complete exercise 03               |   5   |
| Wed      | Read lecture 3; complete exercises 04 and 05       |   6   |
| Thu      | Quiz + start challenges 01 and 02                  |   5   |
| Fri      | Mini-project: file organizer bot (build)           |   6   |
| Sat      | Mini-project: polish, tests, README                |   5   |
| Sun      | Homework set + review                              |   4   |

Spend more time on the mini-project if scraping is new — it pays off in Week 13.

---

## Navigation

- **Lecture notes**: [`lecture-notes/`](./lecture-notes/)
- **Exercises** (guided, ~30 min each): [`exercises/`](./exercises/)
- **Challenges** (longer, integration-style): [`challenges/`](./challenges/)
- **Quiz**: [`quiz.md`](./quiz.md)
- **Homework** (6 problems): [`homework.md`](./homework.md)
- **Mini-project**: [`mini-project/`](./mini-project/)
- **External resources**: [`resources.md`](./resources.md)

---

## Stretch Goals

If you finish early, try one of these:

1. **Watchdog upgrade** — replace the polling loop in your file organizer with the [`watchdog`](https://pypi.org/project/watchdog/) library for true OS-level events.
2. **Slack / Discord notifications** — add a webhook so your script DMs you when it does something interesting.
3. **Packaging** — wrap your mini-project as an installable CLI with `pyproject.toml` and `entry_points`, so you can run `organize` from anywhere.
4. **Dry-run mode** — every file-modifying script you write this week should support `--dry-run`. Audit your code.
5. **Playwright deep-dive** — pick a JavaScript-heavy site and scrape it with Playwright instead of `requests`.
6. **GitHub Action** — schedule one of your scripts to run daily in a GitHub Action.

---

## Up Next

Next week we leave automation behind (sort of — we'll still schedule things) and dive into **data**: pandas, NumPy, and turning raw CSVs into insight.

Continue to: **[Week 13 — Data Analysis](../week-13-data-analysis/)**

---

*Code Crunch Convos — building Pythonistas one week at a time.*
