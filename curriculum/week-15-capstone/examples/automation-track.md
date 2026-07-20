# Automation Track Example — GitHub Repo Triage Bot

A bot that watches a GitHub repository for new issues and **labels**
them automatically based on rules (keyword matches) and a small
**classifier** (a logistic-regression model trained on the project's
historical labelled issues). The bot can run as a scheduled cron-style
job or as a webhook. Designed to solve a real workflow pain — open-source
maintainers triage the same issue types every day — and to be usable on
the maintainer's own repo by Day 7.

## MVP sentence

> *A maintainer can run `repo-triage scan <owner>/<repo>` and the bot
> will fetch open unlabelled issues, predict labels with the trained
> classifier, and apply them via the GitHub API.*

If that command works against a real repo (with the maintainer's PAT),
the MVP is done.

## User stories

1. **Train.** As a maintainer, I can run
   `repo-triage train <owner>/<repo>` to fetch the repo's *closed*
   issues and train a classifier on their titles/bodies and labels.
2. **Scan.** As a maintainer, I can run `repo-triage scan <owner>/<repo>`
   to label every open unlabelled issue with the predicted label(s).
3. **Dry-run.** As a maintainer, I can pass `--dry-run` to see what the
   bot *would* do without it actually calling the API.
4. **Schedule.** As a maintainer, I can put the scan command in a cron
   job (or a GitHub Action) and have the repo triage itself daily.

## Anti-goals

- A general-purpose hosted service. This bot runs against one repo at a
  time, locally or in CI.
- Real-time webhooks. Scheduled runs are enough.
- A web UI.
- Multi-label classification with thresholding gymnastics. One label
  per issue is fine.
- Anything that requires a paid GitHub plan.

## Suggested tech stack

- Python 3.11+
- `PyGithub` or `httpx` directly against the GitHub REST API
- `click` for the CLI
- `scikit-learn` for the classifier (TF-IDF + logistic regression is
  perfect — boring and effective)
- `joblib` for saving the model
- `python-dotenv` for managing the PAT secret in dev
- `pytest`, `pytest-cov`, with `responses` or `respx` to mock HTTP
- GitHub Actions for both CI and (stretch) running the bot itself

## Folder layout

```text
repo-triage/
├── src/repo_triage/
│   ├── __init__.py
│   ├── cli.py             # click entry point
│   ├── github_client.py   # thin wrapper around the GitHub API
│   ├── rules.py           # hand-written keyword rules
│   ├── classifier.py      # TF-IDF + LR pipeline
│   ├── triage.py          # the "scan" orchestrator
│   └── persistence.py     # save_model / load_model
├── tests/
│   ├── fixtures/
│   │   └── sample_issues.json
│   ├── test_rules.py
│   ├── test_classifier.py
│   ├── test_triage.py
│   └── test_cli.py
├── models/
│   └── triage.pkl
├── docs/
│   ├── PROPOSAL.md
│   └── RETRO.md
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── triage.yml      # stretch — the bot triaging this repo
│   └── ISSUE_TEMPLATE/
│       ├── bug.md
│       └── feature.md
├── .env.example
├── pyproject.toml
├── README.md
└── LICENSE
```

## Architecture: rules then model

The cleanest design is a *two-stage* labeller:

1. **Rules first.** If the issue title or body matches one of a small
   list of obvious keyword rules — e.g. "stack trace" → `bug`,
   "documentation" → `docs` — apply that label and stop.
2. **Model second.** Otherwise, ask the classifier for its top
   prediction. If the classifier's confidence is above a threshold
   (say 0.6), apply it.
3. **Otherwise.** Apply the label `triage` so a human can decide. This
   is your honest "I don't know" output.

This split is satisfying because the rules side is unit-testable as
pure functions, and the model side is unit-testable as a small fitted
estimator on a tiny fixture dataset.

## A representative `rules.py`

```python
"""Hand-written triage rules.

Each rule is a ``(label, predicate)`` pair. ``predicate(issue)`` returns
True if the rule fires for the issue. The first matching rule wins.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Iterable

import re


@dataclass(frozen=True)
class Issue:
    """A minimal GitHub issue as seen by the triage logic."""

    number: int
    title: str
    body: str


Predicate = Callable[[Issue], bool]
Rule = tuple[str, Predicate]


def _has(pattern: str) -> Predicate:
    """Return a predicate that matches a regex (case-insensitive)."""
    regex = re.compile(pattern, re.IGNORECASE)

    def matcher(issue: Issue) -> bool:
        return bool(regex.search(issue.title) or regex.search(issue.body))

    return matcher


DEFAULT_RULES: tuple[Rule, ...] = (
    ("bug", _has(r"traceback|stack trace|exception|error")),
    ("docs", _has(r"\bdoc(s|umentation)?\b|typo|readme")),
    ("question", _has(r"\?$|how do i|how to|^how\b")),
    ("performance", _has(r"slow|memory|leak|profil(e|ing)")),
)


def apply_rules(issue: Issue, rules: Iterable[Rule] = DEFAULT_RULES) -> str | None:
    """Return the first matching label, or ``None`` if no rule fires."""
    for label, matches in rules:
        if matches(issue):
            return label
    return None
```

Notice: pure logic, deterministic, no I/O. The test file for this
module is essentially a list of `(input, expected_label)` cases.

## Day-by-day plan

**Day 1.** Proposal. Pick a *target repo* — your own, or a small
open-source project. Create a GitHub PAT with `public_repo` scope and
store it in `.env`.

**Day 2.** Skeleton, CI, click CLI with stub commands. Mock HTTP set up
with `responses` or `respx`.

**Day 3 AM.** `github_client.py` — a thin wrapper with three methods:
`list_closed_issues_with_labels`, `list_open_unlabelled_issues`,
`add_labels`. Test it with HTTP mocks.

**Day 3 PM.** `rules.py` — the keyword rules and `apply_rules`. Tests
covering each rule.

**Day 4 AM.** `classifier.py` — fit a `Pipeline(TfidfVectorizer,
LogisticRegression)` on the labelled training set. Save with joblib.

**Day 4 PM.** `triage.py` — orchestrate scan: fetch open issues, run
rules, fall back to classifier, apply labels (or just print under
`--dry-run`). Integration test using HTTP mocks end-to-end.

**Day 5.** Coverage past 70%. README explains rules vs model, shows
the CLI in action against a public repo, includes a screenshot of the
labels being applied. Document the PAT scope you need.

**Day 6.** Record the video. Demo: train, dry-run scan, real scan.

**Day 7.** (Stretch) Wire `.github/workflows/triage.yml` to run the
bot daily against this repo itself. Retro. Pin. Submit.

## Where this project demonstrates each week

- **Week 6** — file I/O, `.env`, persistence.
- **Week 7** — classes (`Issue`, the client wrapper).
- **Week 8** — REST APIs, JSON, authentication headers.
- **Week 11** — pytest with mocked HTTP, CI.
- **Week 12** — automation, cron-style scheduling.
- **Week 14** — the scikit-learn classifier.

## "Done" check

- [ ] `repo-triage train <owner>/<repo>` produces `models/triage.pkl`.
- [ ] `repo-triage scan <owner>/<repo> --dry-run` prints predicted
      labels without modifying the repo.
- [ ] `repo-triage scan <owner>/<repo>` (with a real PAT) labels real
      issues.
- [ ] Tests cover ≥ 70%, CI green, no PAT committed to the repo.
- [ ] The README explains the rule + model split.
- [ ] Walkthrough video shows a real labelled issue at the end.

## Security note

Your bot needs a GitHub Personal Access Token to call the API. Two
rules, no exceptions:

- Use a **fine-grained** PAT, scoped to *only* the target repo.
- Never commit the PAT. Use a `.env` file (already in `.gitignore`) for
  local dev; use GitHub Actions secrets for the scheduled run.

`git secrets` or `pre-commit` with `detect-secrets` is worth installing
the first time you write a project like this.
