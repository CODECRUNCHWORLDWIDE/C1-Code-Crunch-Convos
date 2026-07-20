# Capstone Project Master Guide

> The capstone is your portfolio centerpiece — a substantial, public, polished project that demonstrates everything you've learned in Weeks 1–14.

This document is the **single source of truth** for capstone requirements, milestones, rubric, and submission. The Week 15 curriculum folder ([curriculum/week-15-capstone/](../../curriculum/week-15-capstone/)) breaks the same content into a day-by-day plan; consult this file when you need the whole picture in one place.

---

## At a glance

| Aspect              | Detail                                                          |
| ------------------- | --------------------------------------------------------------- |
| Duration            | 1 week (~36 hours) following the 14-week curriculum             |
| Deliverable         | A public GitHub repository                                      |
| Format              | Web app · CLI · Notebook · API · Data analysis · Automation tool |
| Required submission | Repo URL + 3–5 minute walkthrough video                         |
| Audience            | Yourself, future employers, the open-source community            |

---

## Why a capstone?

Three reasons:

1. **You retain what you build.** Most of what you learned will fade unless you apply it. A capstone forces synthesis.
2. **You leave with a portfolio.** A polished GitHub repo is the most credible artifact you can hand a recruiter — far more than certificates.
3. **You learn to ship.** Real software is "done enough to release." Most beginners can write code; few can polish it to shipping quality. The capstone teaches the difference.

---

## Tracks (pick one)

Pick the track that excites you. You don't need permission — the tracks are guidance, not gates.

### 🌐 Web App track
Build a Flask web application with multiple routes, templates, persistence, and at least one external API integration or significant interactive feature.

Examples: habit tracker, recipe sharer, study-group scheduler, expense splitter, book club platform.

### 📊 Data track
Analyze a real, public dataset. Deliver a Jupyter notebook with cleaning, EDA, visualizations, and a written summary of insights. Optionally turn the notebook into a dashboard.

Examples: NYC taxi efficiency, transit reliability, global climate data, music streaming patterns, athlete performance trends.

### 🤖 ML track
Train, evaluate, and deploy a scikit-learn model. Build a tiny inference CLI or web endpoint.

Examples: movie recommender, news topic classifier, sentiment analyzer, fraud detector, image-class style classifier (tabular).

### ⚙️ Automation track
Build a working automation tool that solves a real problem in your life, school, or club.

Examples: GitHub repo triage bot, file backup with cloud sync, content scheduler, exam-question generator, link-rot detector.

### 🔌 API track
Build and deploy a small REST API with documentation, tests, and authentication.

Examples: book catalog, URL shortener, simple analytics ingest, public dataset wrapper, paste/snippet store.

See [curriculum/week-15-capstone/examples/](../../curriculum/week-15-capstone/examples/) for a worked example of each track with full scope, day-by-day plan, and folder layout.

---

## What "done" looks like — required for all tracks

Your capstone repo MUST include:

- **A working program.** It actually runs end-to-end on a fresh clone.
- **A great README** with: what it does, screenshots/screen-cap, how to install, how to use, dependencies, license. Link to your walkthrough video.
- **Modular code.** Multiple files organized into logical modules; no 500-line `main.py`.
- **Type hints** on all functions you author.
- **Tests** with `pytest`. Aim for ≥70% coverage on your own code (you don't need to test third-party libraries).
- **CI** via GitHub Actions running `ruff`, `black --check`, `pytest` on push.
- **Clean git history.** Multiple meaningful commits; no "asdf" or "fix" with no context.
- **Dependencies pinned** via `requirements.txt` or `pyproject.toml`.
- **A `LICENSE` file** (MIT, Apache-2.0, or GPL-3.0 — pick one).
- **A `.gitignore`** that excludes `__pycache__/`, `.venv/`, `.env`, etc.
- **A walkthrough video.** 3–5 minutes. Free tools: [Loom free tier](https://www.loom.com/), [OBS](https://obsproject.com/), [Kap (macOS)](https://getkap.co/). Show the working program, the repo structure, and one technical choice you're proud of.

At least ONE of:

- Persists state (SQLite or JSON storage)
- Calls an external API
- Performs a meaningful data analysis (notebook or script with multi-step transformations)
- Trains and uses an ML model

---

## The 7-day plan

| Day | Milestone                                                          | Output                              |
| --- | ------------------------------------------------------------------ | ----------------------------------- |
| 1   | [Idea & scope](../../curriculum/week-15-capstone/milestones/01-idea-and-scope.md) | 1-page proposal in your repo |
| 2   | [Design & skeleton](../../curriculum/week-15-capstone/milestones/02-design-and-skeleton.md) | Repo scaffold pushed to GitHub |
| 3–4 | [Build core](../../curriculum/week-15-capstone/milestones/03-build-core.md) | Draft PR with MVP feature complete |
| 5   | [Test & polish](../../curriculum/week-15-capstone/milestones/04-test-and-polish.md) | Tests + lint + README + screenshots |
| 6–7 | [Ship & present](../../curriculum/week-15-capstone/milestones/05-ship-and-present.md) | Deployed (if applicable) + video    |

Push commits every day. Visible progress beats invisible perfection.

---

## Rubric (100 points)

| Category                 | Points | What we look for                                                                    |
| ------------------------ | ------ | ----------------------------------------------------------------------------------- |
| **Code Quality**         | 20     | PEP 8, ruff clean, black formatted, type hints, no dead code                        |
| **Architecture**         | 15     | Logical module structure, separation of concerns, no god-objects                    |
| **Testing & CI**         | 15     | ≥70% coverage on learner code, CI passes, tests cover happy + edge cases            |
| **Documentation**        | 15     | README is excellent, docstrings on public funcs, decisions documented                |
| **Functionality**        | 15     | MVP scope delivered, polished UX (terminal/UI/notebook), no obvious bugs            |
| **Git Hygiene**          | 10     | Meaningful commits, branches for features, descriptive PRs, no committed secrets    |
| **Presentation**         | 10     | Walkthrough video is clear and 3–5 min, repo is pinned, talks about *why* not just *what* |
| **Total**                | **100**|                                                                                     |

A passing capstone is **70+**. An excellent capstone is **90+** and could be shown verbatim to a recruiter.

Detailed score bands per dimension: [curriculum/week-15-capstone/rubric.md](../../curriculum/week-15-capstone/rubric.md).

---

## Submission

When you're done:

1. **Repo must be public** on GitHub.
2. **Pin it** to your GitHub profile (Profile → Customize your pins).
3. **Upload your video** somewhere streamable (unlisted YouTube, Loom, Vimeo).
4. **Link the video** at the top of the repo README.
5. **Open a Discussion** on this curriculum repo's [Discussions](https://github.com/CODE-CRUNCH-CLUB/C1-Code-Crunch-Convos/discussions) with: capstone repo URL, video URL, 2-sentence pitch, what you'd improve with another week.

The Code Crunch Club community celebrates capstones in a monthly showcase — sharing is encouraged.

---

## After the capstone

You're done with the bootcamp. Now keep building.

- **Specialize.** Pick a deeper track: web (Django/FastAPI), data (more SQL + visualization), ML (full Andrew Ng course), DevOps (Docker, CI/CD), or systems (Rust).
- **Contribute to open source.** Find an issue labelled "good first issue" on any Python project you use.
- **Build 3–5 more portfolio projects.** Variety beats depth at this stage. Show range.
- **Interview prep.** [NeetCode](https://neetcode.io), [LeetCode](https://leetcode.com), system-design fundamentals.
- **Mentor someone going through this curriculum.** Teaching is the strongest test of mastery.

---

## Questions?

- **"My idea is too ambitious / too small."** → If you can describe it in one sentence, it's the right size. If it takes a paragraph to even explain the goal, it's too big.
- **"I can't pick a track."** → Default to the **Web app** track — it exercises the most breadth.
- **"I'm stuck on day 4."** → Reduce scope. Drop a feature. Ship the smaller thing.
- **"Can I use AI to help?"** → Yes, for explanations and review. No, for writing your code wholesale — see [community/support.md](../../community/support.md#6-using-ai-assistants-responsibly).

Good luck. Build something you'd be proud to show.
