# C1 · Code Crunch Convos — Syllabus

**Format:** 15 weeks · ~36 hrs/week intensive (or 30 weeks at ~18 hrs/week part-time) · absolute beginner → portfolio-ready Python engineer

The flagship Python bootcamp of the Code Crunch Club, and the on-ramp to C2, C13, and C14.

**Prerequisites.** None beyond a computer, a willingness to read documentation, and the weekly hours. No prior programming experience is assumed — Week 1 starts at "I've never written code."

**Assessment is honor-based.** There are no proctors and no grades. Every quiz, homework set, and mini-project is self-checked against the rubric in its week folder; the credential is the public work in your GitHub repo, not a certificate. You advance when your own work convinces you — and anyone who reads your repo — that you have it.

---

## Mission & Goals

**Mission.** Make a high-quality, project-based Python education freely available to any learner, anywhere — built and improved in the open.

**Goals.**

1. Teach Python the way it's used in industry: with version control, testing, code review, and real tooling.
2. Build a portfolio of 15 mini-projects and one capstone — every artifact public on GitHub.
3. Reinforce **how to learn** (reading docs, writing tests, asking good questions) as much as **what to learn**.
4. Stay free, open, and remixable forever.

---

## Program at a glance

| Phase                         | Weeks    | Outcome                                                |
| ----------------------------- | -------- | ------------------------------------------------------ |
| **Phase 1 — Foundations**     | 01 – 04  | Write programs with variables, control flow, functions |
| **Phase 2 — Core programming**| 05 – 07  | Data structures, files, OOP                            |
| **Phase 3 — Real-world Python**| 08 – 11 | APIs, web, databases, testing                          |
| **Phase 4 — Applied Python**  | 12 – 14  | Automation, data analysis, intro ML                    |
| **Phase 5 — Capstone**        | 15       | Ship a portfolio project                               |

---

## Weekly load

| Component | hrs/wk |
|-----------|------:|
| Lectures / study material | 6 |
| Hands-on exercises | 8 |
| Coding challenges | 4 |
| Quizzes & readings | 3 |
| Homework problems | 6 |
| Mini-project | 7 |
| Self-study / review | 2 |
| **Total** | **36** |

Part-time learners stretch the same content to 30 weeks at ~18 hrs/week.

---

**Outcome:** a portfolio-ready engineer who has shipped 15 mini-projects and one capstone — written clean idiomatic Python, used Git and GitHub, built OOP systems, consumed REST APIs, deployed a Flask web app, queried databases with SQL and SQLAlchemy, written `pytest` suites, analyzed data with pandas, and trained a basic scikit-learn model, every artifact public on GitHub with a README, tests, and CI.

---

## Weekly modules

| #   | Week                                                                  | Mini-project                  |
| --- | --------------------------------------------------------------------- | ----------------------------- |
| 01  | [Python Foundations](curriculum/week-01-python-foundations/)                     | "Hello, You" CLI greeter      |
| 02  | [Variables, Data Types & Operators](curriculum/week-02-data-types-operators/)    | Unit converter                |
| 03  | [Control Flow](curriculum/week-03-control-flow/)                                 | Number-guessing game          |
| 04  | [Functions, Modules & Scope](curriculum/week-04-functions-modules/)              | Personal finance calculator   |
| 05  | [Data Structures & Comprehensions](curriculum/week-05-data-structures/)          | Contact book                  |
| 06  | [File I/O & Exception Handling](curriculum/week-06-file-io-exceptions/)          | Log file analyzer             |
| 07  | [Object-Oriented Programming](curriculum/week-07-object-oriented-programming/)   | Library management system     |
| 08  | [APIs, JSON & HTTP](curriculum/week-08-apis-json/)                               | Weather dashboard             |
| 09  | [Web Development with Flask](curriculum/week-09-web-development-flask/)          | Personal blog                 |
| 10  | [Databases & SQL](curriculum/week-10-databases-sql/)                             | Task tracker                  |
| 11  | [Testing, Debugging & Quality](curriculum/week-11-testing-debugging/)            | Tested utility library + CI   |
| 12  | [Automation & Scripting](curriculum/week-12-automation-scripting/)               | File organizer bot            |
| 13  | [Data Analysis with pandas](curriculum/week-13-data-analysis/)                   | Dataset analysis              |
| 14  | [Intro to AI/ML](curriculum/week-14-intro-ai-ml/)                                | Spam classifier               |
| 15  | [Capstone](curriculum/week-15-capstone/)                                         | Portfolio centerpiece         |

---

## Weekly breakdown

### Phase 1 — Foundations

#### [Week 1 — Python Foundations & Dev Environment](curriculum/week-01-python-foundations/)

Install Python, write your first program, learn the REPL, get comfortable with the terminal and Git. Hello world done properly: with version control, virtual environments, and `pip`.

- **Mini-project:** "Hello, You" — a personal CLI greeter committed to your own GitHub.

#### [Week 2 — Variables, Data Types & Operators](curriculum/week-02-data-types-operators/)

Numbers, strings, booleans, type coercion, f-strings, arithmetic, comparison, logical operators. Reading user input. Type hints.

- **Mini-project:** Unit converter (temperature, currency, distance).

#### [Week 3 — Control Flow](curriculum/week-03-control-flow/)

`if/elif/else`, `while` loops, `for` loops, `range`, `break`, `continue`. Logical decomposition.

- **Mini-project:** Number-guessing game with replay loop.

#### [Week 4 — Functions, Modules & Scope](curriculum/week-04-functions-modules/)

Defining functions, parameters, return values, default & keyword args, `*args`/`**kwargs`, scope rules, importing modules, organizing code into multiple files.

- **Mini-project:** Personal finance calculator (income, expenses, savings).

---

### Phase 2 — Core Programming

#### [Week 5 — Data Structures & Comprehensions](curriculum/week-05-data-structures/)

Lists, tuples, sets, dicts. When to use each. List, dict, and set comprehensions. Big-O intuition.

- **Mini-project:** Contact book manager.

#### [Week 6 — File I/O & Exception Handling](curriculum/week-06-file-io-exceptions/)

Reading and writing files, `pathlib`, CSV, JSON, structured logging, the exception model, custom exceptions.

- **Mini-project:** Log file analyzer.

#### [Week 7 — Object-Oriented Programming](curriculum/week-07-object-oriented-programming/)

Classes, instances, attributes, methods, inheritance, composition, `__init__`, `__repr__`, dunder methods, `dataclasses`, design tradeoffs (OOP vs. procedural).

- **Mini-project:** Library management system.

---

### Phase 3 — Real-World Python

#### [Week 8 — APIs, JSON & HTTP](curriculum/week-08-apis-json/)

HTTP basics, JSON, the `requests` library, pagination, authentication, rate limiting, error handling. Reading and producing JSON.

- **Mini-project:** Weather dashboard CLI.

#### [Week 9 — Web Development with Flask](curriculum/week-09-web-development-flask/)

Routes, request/response, templates with Jinja2, forms, sessions, deploying for free.

- **Mini-project:** Personal blog web app.

#### [Week 10 — Databases & SQL with Python](curriculum/week-10-databases-sql/)

Relational data, SQL fundamentals (SELECT/JOIN/GROUP BY), SQLite, the `sqlite3` module, an intro to SQLAlchemy.

- **Mini-project:** Task tracker with SQLite-backed storage.

#### [Week 11 — Testing, Debugging & Code Quality](curriculum/week-11-testing-debugging/)

`pytest`, fixtures, parametrize, the debugger (`pdb`/VS Code), `ruff` & `black`, type checking with `mypy`, GitHub Actions CI.

- **Mini-project:** Tested utility library with CI pipeline.

---

### Phase 4 — Applied Python

#### [Week 12 — Automation & Scripting](curriculum/week-12-automation-scripting/)

`argparse`, `subprocess`, `pathlib`, `shutil`, scheduling with `cron`, web scraping basics with `BeautifulSoup`, `Selenium`/`Playwright` overview.

- **Mini-project:** File organizer bot.

#### [Week 13 — Data Analysis with pandas](curriculum/week-13-data-analysis/)

`NumPy` basics, `pandas` DataFrames, loading CSV/JSON/Excel, cleaning, aggregating, plotting with `matplotlib`/`seaborn`, Jupyter notebooks.

- **Mini-project:** Real-world dataset analysis (you pick the dataset).

#### [Week 14 — Intro to AI/ML with scikit-learn](curriculum/week-14-intro-ai-ml/)

Supervised vs. unsupervised, train/test split, linear & logistic regression, decision trees, `scikit-learn` pipeline, model evaluation, where ML can and can't help.

- **Mini-project:** Spam classifier.

---

### Phase 5 — Capstone

#### [Week 15 — Capstone Project](curriculum/week-15-capstone/)

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

---

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

Instructors: feel free to fork and adjust. If you do something that works well, [send us a PR](curriculum/../CONTRIBUTING.md) so others can benefit.

---

## How to Navigate This Repository

```text
C1-Code-Crunch-Convos/
├── README.md                  ← you are here
├── CONTRIBUTING.md            ← how to contribute
├── CODE_OF_CONDUCT.md         ← community rules
├── LICENSE                    ← GPL-3.0
├── curriculum/                ← the 15-week course
│   ├── SYLLABUS.md            ← full program overview
│   ├── week-01-python-foundations/
│   ├── week-02-data-types-operators/
│   ├── ...
│   └── week-15-capstone/
├── projects/
│   ├── mini-projects/         ← cross-week project specs
│   └── capstone/              ← capstone guide & rubric
├── resources/
│   ├── setup-guides/          ← install Python, Git, VS Code
│   ├── cheatsheets/           ← quick reference sheets
│   ├── git-github-workflow.md
│   └── coding-standards.md
├── community/
│   ├── support.md             ← where to ask for help
│   └── faqs.md
├── past-sessions/
│   └── SPRING-2025/           ← archived cohort materials
└── assets/                    ← shared images / diagrams
```

### Inside each `curriculum/week-XX-*/` you will find

```text
week-XX-topic/
├── README.md               ← objectives, schedule, navigation
├── lecture-notes/          ← written material to study
├── resources.md            ← curated readings + docs links
├── exercises/              ← guided, small practice problems
├── challenges/             ← harder, open-ended problems
├── quiz.md                 ← knowledge check
├── homework.md             ← graded practice
└── mini-project/           ← week-capping deliverable
```

```text
week-XX-topic/
├── README.md          ← objectives, schedule, navigation
├── resources.md       ← curated readings + docs links
├── lecture-notes/     ← written material
├── exercises/         ← guided practice (5–30 min each)
├── challenges/        ← harder, open-ended problems
├── quiz.md            ← knowledge check
├── homework.md        ← graded problems
└── mini-project/      ← week-capping deliverable
```

Start each week by reading the week's **README.md**, then follow the day-by-day schedule. Don't skip the homework — it's where most learning happens.

---

## Where things live

-  [Capstone guide](projects/capstone/) — Week 15 deliverable
-  [Setup guides](resources/setup-guides/) — install Python before Week 1
-  [Contributing](CONTRIBUTING.md) — fix typos, add exercises

---

## Past Sessions

Previous cohorts and their materials are preserved under [past-sessions/](past-sessions/) for historical reference:

- [SPRING 2025](past-sessions/SPRING-2025/) — original interview-prep focused 5-unit series

---

## Outcome

**Outcome:** a portfolio-ready engineer who has shipped 15 mini-projects and one capstone — written clean idiomatic Python, used Git and GitHub, built OOP systems, consumed REST APIs, deployed a Flask web app, queried databases with SQL and SQLAlchemy, written `pytest` suites, analyzed data with pandas, and trained a basic scikit-learn model, every artifact public on GitHub with a README, tests, and CI.
