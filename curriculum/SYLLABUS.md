# Code Crunch Convos — Full Program Syllabus

15 weeks · ~540 hours · ~36 hours/week · Beginner → Industry-ready

This page is the **table of contents** for the entire program. Each week links to its own README with detailed objectives, materials, exercises, and a mini-project.

---

## Program at a glance

| Phase                         | Weeks    | Outcome                                                |
| ----------------------------- | -------- | ------------------------------------------------------ |
| **Phase 1 — Foundations**     | 01 – 04  | Write programs with variables, control flow, functions |
| **Phase 2 — Core programming**| 05 – 07  | Data structures, files, OOP                            |
| **Phase 3 — Real-world Python**| 08 – 11 | APIs, web, databases, testing                          |
| **Phase 4 — Applied Python**  | 12 – 14  | Automation, data analysis, intro ML                    |
| **Phase 5 — Capstone**        | 15       | Ship a portfolio project                               |

## How the weekly load adds up

| Component                 | hrs/wk |
| ------------------------- | ------ |
| Lectures / readings       | 6      |
| Hands-on exercises        | 8      |
| Coding challenges         | 4      |
| Quiz + readings           | 3      |
| Homework problems         | 6      |
| Mini-project              | 7      |
| Self-study & review       | 2      |
| **Total**                 | **36** |

Each week is **modular** — instructors can adjust pacing without breaking later weeks.

---

## Weekly breakdown

### Phase 1 — Foundations

#### [Week 1 — Python Foundations & Dev Environment](week-01-python-foundations/)

Install Python, write your first program, learn the REPL, get comfortable with the terminal and Git. Hello world done properly: with version control, virtual environments, and `pip`.

- **Mini-project:** "Hello, You" — a personal CLI greeter committed to your own GitHub.

#### [Week 2 — Variables, Data Types & Operators](week-02-data-types-operators/)

Numbers, strings, booleans, type coercion, f-strings, arithmetic, comparison, logical operators. Reading user input. Type hints.

- **Mini-project:** Unit converter (temperature, currency, distance).

#### [Week 3 — Control Flow](week-03-control-flow/)

`if/elif/else`, `while` loops, `for` loops, `range`, `break`, `continue`. Logical decomposition.

- **Mini-project:** Number-guessing game with replay loop.

#### [Week 4 — Functions, Modules & Scope](week-04-functions-modules/)

Defining functions, parameters, return values, default & keyword args, `*args`/`**kwargs`, scope rules, importing modules, organizing code into multiple files.

- **Mini-project:** Personal finance calculator (income, expenses, savings).

---

### Phase 2 — Core Programming

#### [Week 5 — Data Structures & Comprehensions](week-05-data-structures/)

Lists, tuples, sets, dicts. When to use each. List, dict, and set comprehensions. Big-O intuition.

- **Mini-project:** Contact book manager.

#### [Week 6 — File I/O & Exception Handling](week-06-file-io-exceptions/)

Reading and writing files, `pathlib`, CSV, JSON, structured logging, the exception model, custom exceptions.

- **Mini-project:** Log file analyzer.

#### [Week 7 — Object-Oriented Programming](week-07-object-oriented-programming/)

Classes, instances, attributes, methods, inheritance, composition, `__init__`, `__repr__`, dunder methods, `dataclasses`, design tradeoffs (OOP vs. procedural).

- **Mini-project:** Library management system.

---

### Phase 3 — Real-World Python

#### [Week 8 — APIs, JSON & HTTP](week-08-apis-json/)

HTTP basics, JSON, the `requests` library, pagination, authentication, rate limiting, error handling. Reading and producing JSON.

- **Mini-project:** Weather dashboard CLI.

#### [Week 9 — Web Development with Flask](week-09-web-development-flask/)

Routes, request/response, templates with Jinja2, forms, sessions, deploying for free.

- **Mini-project:** Personal blog web app.

#### [Week 10 — Databases & SQL with Python](week-10-databases-sql/)

Relational data, SQL fundamentals (SELECT/JOIN/GROUP BY), SQLite, the `sqlite3` module, an intro to SQLAlchemy.

- **Mini-project:** Task tracker with SQLite-backed storage.

#### [Week 11 — Testing, Debugging & Code Quality](week-11-testing-debugging/)

`pytest`, fixtures, parametrize, the debugger (`pdb`/VS Code), `ruff` & `black`, type checking with `mypy`, GitHub Actions CI.

- **Mini-project:** Tested utility library with CI pipeline.

---

### Phase 4 — Applied Python

#### [Week 12 — Automation & Scripting](week-12-automation-scripting/)

`argparse`, `subprocess`, `pathlib`, `shutil`, scheduling with `cron`, web scraping basics with `BeautifulSoup`, `Selenium`/`Playwright` overview.

- **Mini-project:** File organizer bot.

#### [Week 13 — Data Analysis with pandas](week-13-data-analysis/)

`NumPy` basics, `pandas` DataFrames, loading CSV/JSON/Excel, cleaning, aggregating, plotting with `matplotlib`/`seaborn`, Jupyter notebooks.

- **Mini-project:** Real-world dataset analysis (you pick the dataset).

#### [Week 14 — Intro to AI/ML with scikit-learn](week-14-intro-ai-ml/)

Supervised vs. unsupervised, train/test split, linear & logistic regression, decision trees, `scikit-learn` pipeline, model evaluation, where ML can and can't help.

- **Mini-project:** Spam classifier.

---

### Phase 5 — Capstone

#### [Week 15 — Capstone Project](week-15-capstone/)

You design and build a substantial project of your choice that exercises the skills from Weeks 1–14. Ships with README, tests, CI, deployable demo, and a 5-minute video walkthrough.

- **Deliverable:** A public GitHub repo you'd be proud to show in a job interview.

---

## Skills progression chart

```text
W1  ─ environment, REPL, first script
W2  │ variables, types
W3  │ control flow
W4  │ functions, modules
W5  │ data structures
W6  │ files, exceptions
W7  ─ OOP
W8  ─ HTTP, JSON, APIs
W9  │ web with Flask
W10 │ SQL, databases
W11 ─ testing, CI
W12 ─ automation, scripting
W13 │ data analysis (pandas)
W14 ─ intro ML (scikit-learn)
W15 ─ CAPSTONE
```

## What you won't learn (but should later)

To keep this curriculum focused, we don't cover:

- Concurrency / async (`asyncio`, threads) — touched in stretch goals only
- C extensions, performance tuning
- Type theory (advanced `typing`)
- Production-scale deployment (K8s, IaC) — Week 9 covers free hosting
- Distributed systems
- Deep learning (PyTorch / TensorFlow) — Week 14 stays with classical ML

We list resources for each of these as **stretch reading** in the relevant weeks.

---

## Adapting the syllabus

- **Part-time (18 hrs/wk):** Each "week" becomes 2 weeks. Total = 30 weeks.
- **University semester (15 weeks × 9 hrs/wk):** Drop homework and one challenge per week. Keep all lectures, exercises, and mini-projects.
- **High-school club (15 weeks × ~3 hrs/wk):** Skip Weeks 11, 13, 14 — extend the capstone instead. Or treat it as a two-year program.

Instructors: feel free to fork and adjust. If you do something that works well, [send us a PR](../CONTRIBUTING.md) so others can benefit.
