# C1 · Code Crunch Convos — Course Syllabus

![C1 · Code Crunch Convos — Python Bootcamp](assets/brand/c1-social-16x9.png)

> A fully open-source, 15-week Python bootcamp designed for absolute beginners progressing toward industry-ready engineering skills.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://img.shields.io/badge/open%20source-%E2%9C%94-green.svg)](#open-source-philosophy)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Overview

**Code Crunch Convos (C1)** is the flagship Python program of the [Code Crunch Worldwide](https://github.com/CODECRUNCHWORLDWIDE) — a global, learner-led learning community. This curriculum reorganizes C1 into a complete **15-week Python Bootcamp** that takes a learner from "I've never written code" to a portfolio-ready engineer who has shipped real projects, written tests, queried databases, consumed APIs, deployed a web app, and trained a basic ML model.

The program is delivered as a public, version-controlled repository — designed equally well for:

- **Self-study learners** working through the curriculum at their own pace.
- **Instructors and clubs** running it as a synchronous cohort.
- **Contributors** improving exercises, fixing bugs, or adding new modules.

---

## Standards & equivalency

> C1 stands in for a university's first programming course.

**University equivalent.** Introduction to Programming — `COP 2210`, `CS 101`, `CS 106A`, `CSE 8A`, `6.100A`. Coverage: full.

C1 carries no credit, no transcript entry, no accreditation and no proctored exam. The equivalence is one of **content and skill**: everything an accredited section of that course teaches, taught here at the same depth or deeper, and assessed. What a registrar records is not something an open repository can give you.

| University outcome | Where this course teaches it | Depth |
| --- | --- | --- |
| Write, run and debug a program in a high-level language, and use the tooling that surrounds it | [Week 01](curriculum/week-01-python-foundations/) | deeper |
| Use primitive types, variables, expressions and operators, and reason about conversion between them | [Week 02](curriculum/week-02-data-types-operators/) | same |
| Direct a program with conditionals, loops and iteration, including early exit | [Week 03](curriculum/week-03-control-flow/) | same |
| Decompose a problem into functions with parameters, return values and scope, and write a recursive one | [Week 04](curriculum/week-04-functions-modules/) | deeper |
| Choose among the built-in collections — lists, tuples, dictionaries, sets — and reason about what each one costs | [Week 05](curriculum/week-05-data-structures/) | deeper |
| Read and write files, and raise and handle exceptions instead of letting a program crash | [Week 06](curriculum/week-06-file-io-exceptions/) | deeper |
| Define classes and objects, with encapsulation and inheritance | [Week 07](curriculum/week-07-object-oriented-programming/) | same |
| Use libraries the course did not write, by reading their documentation | [Week 08](curriculum/week-08-apis-json/) | deeper |
| Test and debug a program systematically rather than by guessing | [Week 11](curriculum/week-11-testing-debugging/) | deeper |
| Complete a substantial program of the learner's own design, and defend it | [Week 15](curriculum/week-15-capstone/) | deeper |

Every row above points at a week that **assigns work** on that outcome — an exercise, a challenge, homework, a quiz item or a project — not merely a week that mentions it.

**The industry bar.** What an employer expects of somebody paid to write Python, and where this course makes the learner do it.

| What the job expects | Where this course does it |
| --- | --- |
| Work lands as a commit in a repository you own, not a file on your desktop | [`resources/git-github-workflow.md`](resources/git-github-workflow.md), from Week 01's first push onward |
| You read code you did not write and form a judgement on it | [`curriculum/week-11-testing-debugging/challenges/challenge-03-review-the-parser.md`](curriculum/week-11-testing-debugging/challenges/challenge-03-review-the-parser.md) |
| Tests exist, and the command to run them is written down | [`curriculum/week-11-testing-debugging/lecture-notes/01-intro-to-pytest.md`](curriculum/week-11-testing-debugging/lecture-notes/01-intro-to-pytest.md), with worked test suites under [`projects/solutions/`](projects/solutions/) |
| You read a real traceback instead of guessing | the `Common bugs to catch` section on every problem page, quoting output captured from a real run |
| Dependencies are isolated per project | [`curriculum/week-01-python-foundations/lecture-notes/02-terminal-virtual-environments-and-pip.md`](curriculum/week-01-python-foundations/lecture-notes/02-terminal-virtual-environments-and-pip.md) |
| A formatter, a linter and a pipeline that runs on every push | [`curriculum/week-11-testing-debugging/lecture-notes/03-quality-tools-and-ci.md`](curriculum/week-11-testing-debugging/lecture-notes/03-quality-tools-and-ci.md) |
| Code that reads the way the rest of the codebase reads | [`resources/coding-standards.md`](resources/coding-standards.md) |
| It runs from a clean clone by following the README | [`curriculum/week-15-capstone/submission-checklist.md`](curriculum/week-15-capstone/submission-checklist.md) |

**Beyond both bars.** Clearing the two floors is entry, not success. Open any of these and check in under a minute.

| What we add | Which bar it beats | Where it lives |
| --- | --- | --- |
| Every assigned problem publishes its worked answer on its own page, visible, with a runnable file beside it — no answer key, nothing withheld until a deadline | both | [`curriculum/week-05-data-structures/exercises/`](curriculum/week-05-data-structures/exercises/) |
| `Under the hood` blocks carry the internals a first-course syllabus stops short of, folded so a learner may skip every one and still finish | university | [`curriculum/week-11-testing-debugging/challenges/challenge-01-tdd-fizzbuzz.md`](curriculum/week-11-testing-debugging/challenges/challenge-01-tdd-fizzbuzz.md) |
| The learner finishes holding a public repository somebody can clone, not a grade only a registrar can see | both | [`projects/capstone/`](projects/capstone/) |
| Five weeks sit entirely past the first-course outcome set — a served web application, a queried database, unattended automation, tabular analysis, and a trained model | university | [`curriculum/week-09-web-development-flask/`](curriculum/week-09-web-development-flask/) |
| A written code review of somebody else's working-but-wrong module: findings ranked by severity, a failing test for each, then the repair | industry | [`curriculum/week-11-testing-debugging/challenges/challenge-03-review-the-parser.md`](curriculum/week-11-testing-debugging/challenges/challenge-03-review-the-parser.md) |
| A quiz every week whose answers are published with it, folded under the question they answer | both | [`curriculum/week-03-control-flow/quiz.md`](curriculum/week-03-control-flow/quiz.md) |

**Gaps we declare.** None against the first-course outcome set. C1 does not teach a second language, formal algorithm analysis beyond informal cost, or data structures implemented from scratch — those belong to a second course and to [C2 · CrunchTime](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code), and C1 does not claim them.

---

## Mission & Goals

**Mission.** Make a high-quality, project-based Python education freely available to any learner, anywhere — built and improved in the open.

**Goals.**

1. Teach Python the way it's used in industry: with version control, testing, code review, and real tooling.
2. Build a portfolio of 15 mini-projects and one capstone — every artifact public on GitHub.
3. Reinforce **how to learn** (reading docs, writing tests, asking good questions) as much as **what to learn**.
4. Stay free, open, and remixable forever.

---

## Target Audience

- **Absolute beginners** with no prior programming experience.
- **Self-taught coders** wanting a structured path with accountability.
- **CS learners** seeking practical, project-driven reinforcement of coursework.
- **Career-switchers** building a portfolio for technical interviews.
- **Educators and clubs** looking for ready-to-teach open curriculum.

No prerequisites beyond: a computer, a willingness to read documentation, and ~36 hours per week.

---

## Estimated Workload

Total program: **~540 hours over 15 weeks (≈36 hrs/week).**

Each week typically breaks down as:

| Component                 | Hours/week |
| ------------------------- | ---------- |
| Lectures / study material | 6          |
| Hands-on exercises        | 8          |
| Coding challenges         | 4          |
| Quizzes & readings        | 3          |
| Homework problems         | 6          |
| Mini-project              | 7          |
| Self-study / review       | 2          |
| **Total**                 | **~36**    |

Part-time learners can stretch the program to **30 weeks at ~18 hrs/week** without changing the content.

---

## Skills You'll Gain

By the end of Week 15, learners will be able to:

- Write clean, idiomatic Python (PEP 8 / PEP 257).
- Use Git and GitHub for collaborative version control.
- Design data structures and pick the right one for the job.
- Build object-oriented systems with clear interfaces.
- Read and write files, handle exceptions, and parse structured data.
- Consume REST APIs and produce JSON.
- Build a small web application with Flask.
- Query relational databases with SQL and SQLAlchemy.
- Write unit and integration tests with `pytest`.
- Automate repetitive tasks with scripts.
- Analyze data with `pandas`, `NumPy`, and `matplotlib`.
- Train and evaluate a basic ML model with `scikit-learn`.
- Ship a full capstone project on GitHub with README, tests, and CI.

---

## Technologies & Tools

All free, open-source, and cross-platform.

| Category        | Tool                                                                                                        |
| --------------- | ----------------------------------------------------------------------------------------------------------- |
| Language        | [Python 3.11+](https://www.python.org/)                                                                     |
| Editor          | [VS Code](https://code.visualstudio.com/) (recommended) or any editor                                       |
| Notebooks       | [Jupyter](https://jupyter.org/)                                                                             |
| Version control | [Git](https://git-scm.com/) + [GitHub](https://github.com/)                                                 |
| Env management  | [venv](https://docs.python.org/3/library/venv.html) / [uv](https://github.com/astral-sh/uv)                 |
| Linting / format| [ruff](https://github.com/astral-sh/ruff), [black](https://black.readthedocs.io/)                           |
| Testing         | [pytest](https://docs.pytest.org/)                                                                          |
| Web             | [Flask](https://flask.palletsprojects.com/)                                                                 |
| Databases       | [SQLite](https://www.sqlite.org/), [SQLAlchemy](https://www.sqlalchemy.org/)                                |
| HTTP            | [requests](https://requests.readthedocs.io/), [httpx](https://www.python-httpx.org/)                        |
| Data            | [NumPy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/)    |
| ML              | [scikit-learn](https://scikit-learn.org/)                                                                   |
| CI              | [GitHub Actions](https://docs.github.com/en/actions)                                                        |

See [resources/setup-guides/](resources/setup-guides/) for installation instructions on macOS, Windows, and Linux.

---

## How This Course Reads

Every page here is written to be understood the first time you read it. Short
sentences, plain words, and a picture in your head before any jargon. When a new
term shows up, it gets explained in the same breath. That is on purpose, and it
is the same for the hardest week as for the first one.

Four things are true of every problem in the course:

- **The main text is the whole lesson.** You do not need anything outside a page
  to do its work.
- **The answer is right there on the page**, under a heading called *The
  Solution*. Read it after you have tried, not before — the learning happens in
  the gap between the two. It is not hidden behind a click; it is just further
  down, after the part where you do the work.
- **Every problem ships a file you can download and run.** The page links it
  under *Download and run*, and it is the exact code shown on the page, so what
  you read is what runs.
- **Anything deeper than you need lives in a box marked *Under the hood*.** Those
  boxes are folded shut. Open them if you are curious about why something works
  the way it does — the memory, the internals, the history. Skip every single
  one and you can still finish the course. Nothing important hides in there.

Where a problem needs only plain Python, the page also offers to open it in the
**browser code editor** — no install, nothing to set up, and your work stays on
your own machine. Problems that need a real computer (installing things, a
virtual environment, Git, a web server) say so and skip that offer.

## How to Navigate This Repository

```text
C1-Code-Crunch-Convos/
├── README.md                  ← you are here; the whole course, in one document
├── CONTRIBUTING.md            ← how to contribute
├── CODE_OF_CONDUCT.md         ← community rules
├── CONTENT-POLICY.md          ← what every problem page must contain
├── LICENSE.md                 ← GPL-3.0
├── curriculum/                ← the 15-week course, one folder per week
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
├── homework/               ← graded practice, one page per problem
└── mini-project/           ← week-capping deliverable
```

Every problem — exercise, challenge, homework problem, mini-project — is one
page, and its answer is on that page: complete, visible, never hidden behind a
toggle, with a runnable file beside it whose code is byte-identical to the block
you can read. There is no separate answers folder anywhere in this course. The
answer and the question are edited together or not at all.

---

## Getting Started

1. **Install prerequisites** — Python 3.11+, Git, and VS Code. Follow the [setup guide for your OS](resources/setup-guides/).
2. **Fork & clone this repo.**

   ```bash
   git clone https://github.com/<your-username>/C1-Code-Crunch-Convos.git
   cd C1-Code-Crunch-Convos
   ```

3. **Create a virtual environment.**

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # macOS/Linux
   .venv\Scripts\activate             # Windows
   ```

4. **Start with [Week 1](curriculum/week-01-python-foundations/).**
5. Submit your work via pull request to your personal fork, or share publicly on your GitHub profile.

---

## Contribution Guidelines

We welcome contributions from learners, instructors, and the wider community. See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full guide.

Quick links:
- 🐛 [Report a bug or typo](https://github.com/CODECRUNCHWORLDWIDE/C1-Code-Crunch-Convos/issues/new)
- 💡 [Suggest an improvement](https://github.com/CODECRUNCHWORLDWIDE/C1-Code-Crunch-Convos/issues/new)
- 🧑‍🏫 [Add or improve a lecture / exercise](CONTRIBUTING.md#contributing-curriculum)
- 🌐 [Translate a week into another language](CONTRIBUTING.md#translations)

All contributors agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Open Source Philosophy

This curriculum is licensed under **[GPL-3.0](LICENSE.md)**. That means:

- Anyone may use, copy, modify, and redistribute this material — including for commercial teaching.
- Derivative works (forks, translations, modified curricula) must remain under GPL-3.0 and credit the original.
- We rely **only** on free and open-source tools. No paid platforms, no proprietary dependencies, no required SaaS.

We believe education should be unbounded by paywalls. Improvements come from learners who pass through it and give back — that's the loop we want to encourage.

---

## Community & Support

- 💬 **Discussions** — [GitHub Discussions](https://github.com/CODECRUNCHWORLDWIDE/C1-Code-Crunch-Convos/discussions)
- 🐦 **Updates** — follow [@CODECRUNCHWORLDWIDE](https://github.com/CODECRUNCHWORLDWIDE) on GitHub
- 🆘 **Stuck on an exercise?** — see [community/support.md](community/support.md)
- ❓ **Frequently asked questions** — see [community/faqs.md](community/faqs.md)

---

## Past Sessions

Material from earlier cohorts has been moved out of this course into the
2025 archive, so that a learner reading the curriculum only ever sees the
current one. Nothing was deleted.

---

## Program at a glance

**Format:** 15 weeks · ~36 hrs/week intensive (or 30 weeks at ~18 hrs/week part-time) · absolute beginner → portfolio-ready Python engineer

The flagship Python bootcamp of Code Crunch Worldwide, and the on-ramp to C2, C13, and C14.

**Prerequisites.** None beyond a computer, a willingness to read documentation, and the weekly hours. No prior programming experience is assumed — Week 1 starts at "I've never written code."

**Assessment is honor-based.** There are no proctors and no grades. Every quiz, homework set, and mini-project is self-checked against the rubric in its week folder; the credential is the public work in your GitHub repo, not a certificate. You advance when your own work convinces you — and anyone who reads your repo — that you have it.

---

### Weekly load

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

## Week by week

15 weeks · ~540 hours · ~36 hours/week · Beginner → Industry-ready

This page is the **table of contents** for the entire program. Each week links to its own README with detailed objectives, materials, exercises, and a mini-project.

---

### Program at a glance

| Phase                         | Weeks    | Outcome                                                |
| ----------------------------- | -------- | ------------------------------------------------------ |
| **Phase 1 — Foundations**     | 01 – 04  | Write programs with variables, control flow, functions |
| **Phase 2 — Core programming**| 05 – 07  | Data structures, files, OOP                            |
| **Phase 3 — Real-world Python**| 08 – 11 | APIs, web, databases, testing                          |
| **Phase 4 — Applied Python**  | 12 – 14  | Automation, data analysis, intro ML                    |
| **Phase 5 — Capstone**        | 15       | Ship a portfolio project                               |

### Weekly breakdown

#### Phase 1 — Foundations

##### [Week 1 — Python Foundations & Dev Environment](curriculum/week-01-python-foundations/)

Install Python, write your first program, learn the REPL, get comfortable with the terminal and Git. Hello world done properly: with version control, virtual environments, and `pip`.

- **Mini-project:** "Hello, You" — a personal CLI greeter committed to your own GitHub.

##### [Week 2 — Variables, Data Types & Operators](curriculum/week-02-data-types-operators/)

Numbers, strings, booleans, type coercion, f-strings, arithmetic, comparison, logical operators. Reading user input. Type hints.

- **Mini-project:** Unit converter (temperature, currency, distance).

##### [Week 3 — Control Flow](curriculum/week-03-control-flow/)

`if/elif/else`, `while` loops, `for` loops, `range`, `break`, `continue`. Logical decomposition.

- **Mini-project:** Number-guessing game with replay loop.

##### [Week 4 — Functions, Modules & Scope](curriculum/week-04-functions-modules/)

Defining functions, parameters, return values, default & keyword args, `*args`/`**kwargs`, scope rules, importing modules, organizing code into multiple files.

- **Mini-project:** Personal finance calculator (income, expenses, savings).

---

#### Phase 2 — Core Programming

##### [Week 5 — Data Structures & Comprehensions](curriculum/week-05-data-structures/)

Lists, tuples, sets, dicts. When to use each. List, dict, and set comprehensions. Big-O intuition.

- **Mini-project:** Contact book manager.

##### [Week 6 — File I/O & Exception Handling](curriculum/week-06-file-io-exceptions/)

Reading and writing files, `pathlib`, CSV, JSON, structured logging, the exception model, custom exceptions.

- **Mini-project:** Log file analyzer.

##### [Week 7 — Object-Oriented Programming](curriculum/week-07-object-oriented-programming/)

Classes, instances, attributes, methods, inheritance, composition, `__init__`, `__repr__`, dunder methods, `dataclasses`, design tradeoffs (OOP vs. procedural).

- **Mini-project:** Library management system.

---

#### Phase 3 — Real-World Python

##### [Week 8 — APIs, JSON & HTTP](curriculum/week-08-apis-json/)

HTTP basics, JSON, the `requests` library, pagination, authentication, rate limiting, error handling. Reading and producing JSON.

- **Mini-project:** Weather dashboard CLI.

##### [Week 9 — Web Development with Flask](curriculum/week-09-web-development-flask/)

Routes, request/response, templates with Jinja2, forms, sessions, deploying for free.

- **Mini-project:** Personal blog web app.

##### [Week 10 — Databases & SQL with Python](curriculum/week-10-databases-sql/)

Relational data, SQL fundamentals (SELECT/JOIN/GROUP BY), SQLite, the `sqlite3` module, an intro to SQLAlchemy.

- **Mini-project:** Task tracker with SQLite-backed storage.

##### [Week 11 — Testing, Debugging & Code Quality](curriculum/week-11-testing-debugging/)

`pytest`, fixtures, parametrize, the debugger (`pdb`/VS Code), `ruff` & `black`, type checking with `mypy`, GitHub Actions CI.

- **Mini-project:** Tested utility library with CI pipeline.

---

#### Phase 4 — Applied Python

##### [Week 12 — Automation & Scripting](curriculum/week-12-automation-scripting/)

`argparse`, `subprocess`, `pathlib`, `shutil`, scheduling with `cron`, web scraping basics with `BeautifulSoup`, `Selenium`/`Playwright` overview.

- **Mini-project:** File organizer bot.

##### [Week 13 — Data Analysis with pandas](curriculum/week-13-data-analysis/)

`NumPy` basics, `pandas` DataFrames, loading CSV/JSON/Excel, cleaning, aggregating, plotting with `matplotlib`/`seaborn`, Jupyter notebooks.

- **Mini-project:** Real-world dataset analysis (you pick the dataset).

##### [Week 14 — Intro to AI/ML with scikit-learn](curriculum/week-14-intro-ai-ml/)

Supervised vs. unsupervised, train/test split, linear & logistic regression, decision trees, `scikit-learn` pipeline, model evaluation, where ML can and can't help.

- **Mini-project:** Spam classifier.

---

#### Phase 5 — Capstone

##### [Week 15 — Capstone Project](curriculum/week-15-capstone/)

You design and build a substantial project of your choice that exercises the skills from Weeks 1–14. Ships with README, tests, CI, deployable demo, and a 5-minute video walkthrough.

- **Deliverable:** A public GitHub repo you'd be proud to show in a job interview.

---

### Skills progression chart

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

### What you won't learn (but should later)

To keep this curriculum focused, we don't cover:

- Concurrency / async (`asyncio`, threads) — touched in stretch goals only
- C extensions, performance tuning
- Type theory (advanced `typing`)
- Production-scale deployment (K8s, IaC) — Week 9 covers free hosting
- Distributed systems
- Deep learning (PyTorch / TensorFlow) — Week 14 stays with classical ML

We list resources for each of these as **stretch reading** in the relevant weeks.

---

### Adapting the syllabus

- **Part-time (18 hrs/wk):** Each "week" becomes 2 weeks. Total = 30 weeks.
- **University semester (15 weeks × 9 hrs/wk):** Drop homework and one challenge per week. Keep all lectures, exercises, and mini-projects.
- **High-school club (15 weeks × ~3 hrs/wk):** Skip Weeks 11, 13, 14 — extend the capstone instead. Or treat it as a two-year program.

Instructors: feel free to fork and adjust. If you do something that works well, [send us a PR](curriculum/../CONTRIBUTING.md) so others can benefit.

---

## Curriculum map

The 15-week Python bootcamp lives here. Start with the [full syllabus](README.md), then dive into [Week 1](curriculum/week-01-python-foundations/).

### Quick links

- 📋 [Full syllabus](README.md) — phase breakdown, time budget, prerequisites
- 🎯 [Capstone guide](curriculum/../projects/capstone/) — Week 15 deliverable
- 🛠️ [Setup guides](curriculum/../resources/setup-guides/) — install Python before Week 1
- 🤝 [Contributing](curriculum/../CONTRIBUTING.md) — fix typos, add exercises

### Weekly modules

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

### How each week is organized

```text
week-XX-topic/
├── README.md          ← objectives, schedule, navigation
├── resources.md       ← curated readings + docs links
├── lecture-notes/     ← written material
├── exercises/         ← guided practice (5–30 min each)
├── challenges/        ← harder, open-ended problems
├── quiz.md            ← knowledge check
├── homework/          ← graded problems, one page each
└── mini-project/      ← week-capping deliverable
```

Every problem is one page and carries its own answer, visible on the page, with
a runnable `-solution.py` beside it. There is no separate answers folder — the
answer lives under the question that asked it.

Start each week by reading the week's **README.md**, then follow the day-by-day schedule. Don't skip the homework — it's where most learning happens.
