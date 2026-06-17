# Lecture 3 — Presentation and Portfolio

A finished capstone is half the value. The other half is whether anyone
who matters — a future employer, a graduate-school admissions reader, a
client, a collaborator — ever sees it and understands what it shows about
you. This lecture is about closing that gap. It covers pinning your repo,
writing a project bullet for your resume, talking about the project in an
interview, open-sourcing it so others can contribute, and getting useful
feedback after the bootcamp ends.

## Pinning your repo

GitHub lets each user pin up to **six** repositories to the top of their
profile. These are the first thing a recruiter or admissions reader sees
after your avatar and bio. Pin your capstone *immediately* on the day you
ship.

To pin a repo:

1. Visit your profile, `https://github.com/<your-username>`.
2. Click **Customize your pins** on the right.
3. Tick your capstone repo. Untick anything embarrassing — yes, that
   includes the half-finished tutorial fork from Week 2.
4. Drag the capstone to the first position.
5. Save.

A good pinned set for a bootcamp graduate looks like:

1. **Capstone** — the headline project.
2. **Mini-project from a strong earlier week** — Week 9 (Flask),
   Week 10 (SQL), or Week 13 (data analysis).
3. **A library or utility** — even a tiny `pip`-installable package
   demonstrates that you have published code.
4. **A "playground" repo** — solved exercises from the bootcamp, if they
   are tidy.

Three pinned repos is plenty if the rest are not capstone-grade. Quality
over quantity.

### Your profile README

Beyond pinning, GitHub lets you create a special repo whose name matches
your username (`yourname/yourname`) — its README appears on your profile.
A short profile README that links to your capstone, names your stack, and
points to your email or LinkedIn is a five-minute upgrade with outsized
returns. Keep it under a screen of text. Do not list every emoji.

## Writing a project summary for resumes

You have one to three lines on a resume to describe the capstone. Almost
every student writes "Built a Flask app with a database" and stops.
Better summaries do three things:

1. **State what the project does** (the problem, plainly).
2. **State a measurable outcome** (a number, a feature count, a coverage
   percent).
3. **Name the tools** (a short list, no more than five).

A weak version:

> *Habit Tracker — A Flask web app for tracking habits.*

A strong version:

> *Habit Tracker — A Flask + SQLite web app for daily habit logging,
> serving 80% test-covered endpoints with GitHub Actions CI and deployed
> on Fly.io. Three real users (myself plus two friends) have logged 600+
> check-ins.* Python 3.12, Flask, SQLAlchemy, pytest, GitHub Actions.

Even if you have only one real user (yourself), that is fine — say so.
Pretending you have ten users when a recruiter clicks the link and sees an
empty dashboard is worse than admitting you have one.

Two specific anti-patterns to avoid:

- **Vague verbs.** "Worked on", "helped with", "was involved in" — drop
  them. You built it.
- **Adjective inflation.** Avoid "innovative", "robust", "seamless".
  Recruiters skim past adjectives; numbers stop their eye.

## Talking about the project in interviews

The most reliable way to talk about a project in a behavioural or
technical interview is the **STAR method**: Situation, Task, Action,
Result. It is overused in career-coaching content because it works. Most
candidates ramble; STAR keeps you honest.

Pick one challenging moment from the capstone — a bug, a refactor, a
design decision, a deployment failure — and prepare a STAR story about
it. Keep each section to two or three sentences. The whole thing should
take under two minutes spoken.

### A worked STAR example

**Situation** — "On Day 4 of my capstone I discovered that my login
flow was issuing the session cookie before the password hash was
verified — meaning the redirect happened on success and failure alike.
The bug only showed up because I wrote a test that asserted the redirect
target."

**Task** — "I needed to fix the auth flow before I could ship, and I
needed to prove the fix actually held."

**Action** — "I rewrote the login handler so that the cookie was only
issued inside the branch that verified the password using bcrypt's
constant-time compare. I added two pytest cases — one for a correct
password, one for a wrong one — that asserted on both the redirect
target and the presence/absence of the session cookie. I then audited
the rest of the routes for the same pattern."

**Result** — "Both tests passed, the bug is gone, and my coverage went
up by 6%. More importantly, I learned to write the test first when the
code being tested is security-adjacent — I'm now in the habit of doing
that on all auth code."

Notice the *Result* is not just "I fixed it". It is what you *learned*.
Interviewers like the learning answer because it tells them you will
keep getting better, not just that you solved one specific bug.

Prepare two or three of these stories about your capstone before you
hit the job market. They become the spine of every technical
conversation.

### Technical deep-dive questions

Expect questions like:

- "Walk me through the architecture."
- "Why did you pick SQLite over Postgres?"
- "How do you handle X failure case?"
- "What would you change if you started over?"
- "Where is your code the weakest?"

The last two are the ones candidates fumble most. The honest answer to
"where is your code weakest?" is *much more impressive* than the
defensive answer. Pick something real — "the auth code is hand-rolled and
in a production setting I'd reach for Flask-Login" — and the interviewer
mentally upgrades your score for self-awareness.

## Open-sourcing it well

Your capstone is on a public GitHub repo. That makes it technically
open-source. To make it *welcomingly* open-source — meaning a stranger
could plausibly contribute — add three small files.

### LICENSE

Pick MIT unless you have a reason not to. Add the standard text from
<https://choosealicense.com/licenses/mit/>. The file itself goes at the
top of the repo as `LICENSE`. Reference it in your README under a
**License** heading.

### CONTRIBUTING.md

A short file in the repo root that says:

- How to set up a dev environment.
- How to run the tests and linters.
- How issues are labelled.
- What you expect in a pull request (passing CI, one feature per PR,
  brief description).
- Whether you accept feature requests.

Two paragraphs is fine. Here is a template:

```markdown
# Contributing

Thanks for considering a contribution! This is a small project, so
contributions are appreciated.

## Setup

1. Fork the repo and clone your fork.
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -e ".[dev]"`
4. `pytest` — make sure tests pass before changing anything.

## Pull requests

- Open an issue first if you are proposing a feature; bug fixes can go
  straight to a PR.
- Keep PRs focused — one feature or fix per PR.
- Make sure `ruff check .`, `black --check .`, and `pytest` all pass.
- Add tests for any new behaviour.

## Code of conduct

Be kind. We follow the
[Contributor Covenant](https://www.contributor-covenant.org/).
```

### Issue templates

Inside `.github/ISSUE_TEMPLATE/` you can drop two files: `bug.md` and
`feature.md`. GitHub then shows a chooser when a stranger clicks "New
issue". A minimal `bug.md`:

```markdown
---
name: Bug report
about: Something is not working
labels: bug
---

## What happened?

<replace with description>

## What did you expect to happen?

## Steps to reproduce

1. ...
2. ...

## Environment

- OS:
- Python version:
- Project version / commit:
```

These are optional. If you add them, even one contribution-friendly
issue label (`good first issue`) increases the chance someone actually
opens one.

## Getting feedback

The hardest thing to get after the bootcamp ends is honest, useful
feedback on your code. There are four sources, in increasing order of
quality.

### 1. Self-review with a checklist

Open your own PR a week after merging it. Read it like a stranger. The
discomfort is the point. You will spot half the issues a reviewer would.

### 2. Peer review with a classmate

Trade reviews with someone else from this cohort. Set a 30-minute timer
each. Use this checklist:

- Does the README make sense to me?
- Could I install and run it?
- Is there one file or function I do not understand the purpose of?
- Is there one thing I would refactor?
- Is anything *missing* that I expected?

Write the answers in a GitHub issue on each other's repos.

### 3. Public posting

Post the repo and the video on a relevant subreddit (e.g.
r/Python, r/learnpython, r/flask), Hacker News (the "Show HN" tag), or
Mastodon/Bluesky. Use a humble title: "I built X for my bootcamp
capstone — feedback welcome". You will get a mix of useful feedback and
internet noise; learn to filter. Specific code suggestions with line
numbers are signal; generic advice is usually not.

### 4. Mentor or recruiter review

If you can get a working engineer to read the code for ten minutes,
that beats all of the above. Ask specifically for "the one thing you
would change about this code, and why" — open-ended "what do you think?"
gets you "nice work" and nothing else. Specificity gets specificity.

## After the bootcamp

The capstone is not a tombstone for your learning. It is a *starting
point*. Two habits, formed in the months after the bootcamp, will keep
your work compounding:

- **Ship one small thing per month.** Even a hundred-line script with
  tests and a README counts. Volume builds judgement.
- **Read code you did not write.** Pick a small open-source project per
  month and read its source. The first time is slow; the tenth time is
  fast and unreasonably educational.

You are now someone who builds things in Python. Keep building.
