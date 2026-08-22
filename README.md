# Start here — Course Overview

> A fifteen-week, open-source Python bootcamp — designed for the absolute beginner, sharpened to the standards of professional engineering. Five hundred and forty hours of lectures, labs, projects, and a capstone. Free, forever.

| | |
| --- | --- |
| **15 weeks** | Program length |
| **540 hrs** | Total workload |
| **14 +1** | Projects + capstone |
| **$0** | Tuition · always |

## An open course, in the open

Code Crunch Convos began in August 2024 as a small interview-prep workshop run by Code Crunch Worldwide — a global, learner-led community. It ran quietly through its first year and a half while we built out the branding, website, assessments, and event programming behind the scenes. In 2026 we rebuilt it as a complete fifteen-week Python bootcamp — a public curriculum that any learner, anywhere, can use without permission or payment.

The course is structured like a real-world bootcamp: lectures, hands-on labs, weekly projects, quizzes, homework, and a portfolio capstone. It is engineered to be taken on its own, or taught from by instructors and university clubs. Everything is GPL-3.0 licensed and lives on GitHub.

> “The best way to predict the future is to teach it.” — Code Crunch Worldwide

## Who it is for

*Built for four kinds of learner.*

No prerequisites beyond a willingness to read documentation and roughly thirty-six hours a week. There is room for everyone.

- **The Absolute Beginner** — Has never written code. Week 1 begins with installing Python and ends with their first commit on GitHub.
- **The Self-Taught Coder** — Has dabbled in tutorials. Wants structure, accountability, and a portfolio of finished, polished work.
- **The Career-Switcher** — Needs hire-ready Python skills, version control habits, and projects to show — all without paying for a paid bootcamp.
- **The Instructor** — Teaches a club or class. Wants a ready-to-deliver, modifiable curriculum that they can fork and adapt.

## The stack

*Free, open, and cross-platform.*

No paid platforms. No proprietary dependencies. No required SaaS. Every tool below works on macOS, Windows, and Linux.

- **Python 3.11+** — Language. python.org
- **VS Code** — Editor. free · cross-platform
- **Git + GitHub** — Version Control. free for public repos
- **venv · uv** — Environments. isolated installs
- **ruff · black** — Format / Lint. opinionated, fast
- **pytest** — Testing. w/ coverage
- **Flask · Jinja2** — Web. minimal framework
- **SQLite · SQLAlchemy** — Database. no server required
- **requests · httpx** — HTTP. de facto clients
- **NumPy · pandas** — Data. the analytics stack
- **matplotlib** — Plotting. via pandas .plot
- **scikit-learn** — Machine Learning. classical ML

## What you walk away with

By the end of Week 15, you are able to do each of the following — credibly, on a real codebase, in front of real reviewers.

- Write clean, idiomatic Python that passes PEP 8 and type-checking.
- Use Git and GitHub fluently — branches, PRs, code review.
- Design data structures and pick the right one for the job.
- Build object-oriented systems with clear, testable interfaces.
- Read and write files, handle exceptions, and parse structured data.
- Consume third-party REST APIs and produce well-formed JSON.
- Build a small web application from scratch with Flask.
- Query relational databases with SQL and SQLAlchemy.
- Write unit and integration tests with pytest and target coverage.
- Automate repetitive tasks with command-line scripts.
- Analyze real datasets with pandas, NumPy, and matplotlib.
- Train, evaluate, and reason about a basic machine-learning model.
- Wire up GitHub Actions CI on every project you ship.
- Read the documentation as a first move, not a last resort.
- Write a README that lets a stranger run your code in five minutes.
- Ship a polished, portfolio-grade project — end to end.

## The capstone

*One project. Five tracks. Your choice.*

Week 15 is reserved for a substantial, public project of your choosing. Pick the track that excites you most. Each track has a worked example in the repository.

- **Web App** (Track i) — A Flask application with database, multiple routes, and one significant interactive feature.
- **Data** (Track ii) — A real public dataset analyzed end-to-end, with cleaning, EDA, and a written summary of findings.
- **Machine Learning** (Track iii) — Train a scikit-learn model, evaluate it honestly, and ship a CLI or web endpoint for inference.
- **Automation** (Track iv) — A working tool that solves a real problem — in your school, your club, your daily life.
- **API** (Track v) — A small REST API with documentation, tests, authentication, and a deployed demo.

## Getting started

*Four commands. Then begin.*

The setup is intentionally lightweight. If you can run a terminal command, you can begin the bootcamp today.

```sh
# 1. Clone the curriculum repository
git clone https://github.com/CODECRUNCHWORLDWIDE/C1-Code-Crunch-Convos.git
cd C1-Code-Crunch-Convos

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate       # Windows

# 3. Open the Week 1 README and begin reading
code curriculum/week-01-python-foundations/00-overview.md

# 4. Push your first mini-project to your own GitHub by Sunday
git push origin main
```

## Education without paywalls

Code Crunch Convos is released under the **GNU General Public License v3**. Anyone may use, copy, modify, and redistribute it — including for commercial teaching — provided derivative works remain under the same license and credit the original.
We made this choice deliberately. A curriculum that only opens up after payment is, in our view, no curriculum at all. Improvements come from the learners who pass through and give back: a fixed typo, a sharper explanation, a translation, a new exercise. That cycle of public improvement is what makes a course durable across years.
The tools we teach are open source. The platform we publish on is open source. The contributing guide invites you in. Read it, fork it, send a pull request.
[Read the contributing guide](https://github.com/CODECRUNCHWORLDWIDE/C1-Code-Crunch-Convos/blob/main/CONTRIBUTING.md)

## Questions, anticipated

---

## The curriculum

The week-by-week programme, the phase breakdown and the time budget live in one place: **[C1 · Code Crunch Convos — Syllabus](SYLLABUS.md)**.
