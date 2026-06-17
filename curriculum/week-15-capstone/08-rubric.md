# Capstone Rubric (100 points)

Your capstone is graded out of **100 points** across seven dimensions.
This page is the source of truth — read it on Day 1, refer back on Day
5, and self-grade with it on Day 7 before submitting.

| Dimension                  | Points |
|----------------------------|-------:|
| Code Quality               |     20 |
| Architecture & Modularity  |     15 |
| Testing & CI               |     15 |
| Documentation              |     15 |
| Functionality & Polish     |     15 |
| Git Hygiene                |     10 |
| Presentation               |     10 |
| **Total**                  | **100**|

A passing capstone scores **≥ 70**. A distinction-grade capstone scores
**≥ 85**. The breakdown below gives you the criteria each rubric uses.

---

## Code Quality — 20 points

What we check:

- PEP 8 compliance (verified by `ruff`).
- Consistent formatting (`black --check .` exits clean).
- Type hints on public functions and classes.
- No dead code, no commented-out blocks left from debugging.
- Sensible variable and function names.
- No "magic numbers" — constants are named.
- Errors are raised meaningfully, not swallowed.

| Score   | What that looks like                                                      |
|--------:|---------------------------------------------------------------------------|
| 20      | Lint- and format-clean. Type hints everywhere public. Code reads cleanly. |
| 16–19   | One or two lint warnings. Type hints mostly present.                      |
| 12–15   | Several lint issues. Type hints inconsistent. Some unused imports.        |
|  8–11   | Linter not run. Long lines, mixed quotes, inconsistent style.             |
|  0–7    | Code visibly unrefined; no formatter run; hard to read.                   |

---

## Architecture & Modularity — 15 points

What we check:

- More than one module — clear separation of concerns.
- Models / routes / services / utilities live in distinct files.
- No circular imports.
- Functions do one thing; modules do one thing.
- A reasonable folder layout (the `src/` layout earns full marks).
- Dependencies flow in one direction (e.g. routes import services;
  services do not import routes).

| Score   | What that looks like                                                      |
|--------:|---------------------------------------------------------------------------|
| 15      | Multi-module, clear concerns, `src/` layout, no circular imports.         |
| 12–14   | Multi-module, mostly clear concerns, one or two long files.               |
|  9–11   | Two or three modules; some mixing of concerns.                            |
|  5–8    | Mostly one file with some helpers.                                        |
|  0–4    | A single `main.py`.                                                       |

---

## Testing & CI — 15 points

What we check:

- `pytest` runs and all tests pass.
- Coverage is **≥ 70%** measured by `coverage.py`.
- At least one *integration* test exists.
- Tests have descriptive names and assert meaningful behaviour.
- Tests do not depend on each other's order.
- GitHub Actions workflow runs lints + tests on every push and PR.
- CI is **green on `main`** at submission time.

| Score   | What that looks like                                                      |
|--------:|---------------------------------------------------------------------------|
| 15      | ≥ 70% coverage, real integration tests, CI green, badge on README.        |
| 12–14   | ≥ 60% coverage, CI green, some integration testing.                       |
|  9–11   | < 60% coverage, CI green, mostly unit tests.                              |
|  5–8    | A handful of tests, CI exists but is sometimes red.                       |
|  0–4    | No tests, no CI, or CI not connected to the repo.                         |

---

## Documentation — 15 points

What we check:

- README contains: title, pitch, badges, screenshot, install, usage,
  demo link, video link, structure, dev setup, contributing, license.
- Install instructions actually work on a clean clone.
- A `docs/PROPOSAL.md` exists.
- A `docs/RETRO.md` exists by submission.
- Public functions, classes, and modules have docstrings.
- The README has at least one *screenshot* of the working project.

| Score   | What that looks like                                                      |
|--------:|---------------------------------------------------------------------------|
| 15      | All sections present, install works first try, docstrings everywhere.     |
| 12–14   | One section missing or thin. Install works after one tweak.               |
|  9–11   | Several README sections missing. Some docstrings absent.                  |
|  5–8    | README is a stub. Install instructions do not work.                       |
|  0–4    | Default GitHub README only.                                               |

---

## Functionality & Polish — 15 points

What we check:

- The MVP sentence from your proposal is **demonstrably true**.
- The demo runs end-to-end without crashes.
- Edge cases (empty state, missing data, invalid input) are handled
  gracefully — no stack traces in the user's face.
- For web apps: a sensible empty state on the home page when no data
  exists.
- For data/ML: outputs reproduce when the notebook is re-run from a
  fresh kernel.
- At least one of: persists state, calls an external API, performs
  data analysis, trains an ML model.

| Score   | What that looks like                                                      |
|--------:|---------------------------------------------------------------------------|
| 15      | Whole MVP works. Edges handled. Empty state is friendly.                  |
| 12–14   | MVP works. One small rough edge.                                          |
|  9–11   | Most of MVP works. Crashes in one or two corners.                         |
|  5–8    | Half the MVP works. Visible bugs on the main path.                        |
|  0–4    | Demo does not run.                                                        |

---

## Git Hygiene — 10 points

What we check:

- More than one commit, distributed across at least three days.
- Commit messages describe *what* in imperative voice.
- A feature branch and a pull request were used (not just direct
  pushes to `main`).
- The PR has a useful description.
- Issues were opened for user stories and closed as they shipped.
- No commits to `main` that broke CI and were left broken overnight.

| Score   | What that looks like                                                      |
|--------:|---------------------------------------------------------------------------|
| 10      | Many small commits, clean messages, feature branch + PR, closed issues.   |
|  8–9    | Mostly clean, one or two giant commits.                                   |
|  6–7    | A handful of commits, some "wip" messages.                                |
|  3–5    | Two or three commits total.                                               |
|  0–2    | One "initial commit" with everything in it.                               |

---

## Presentation — 10 points

What we check:

- A 3–5 minute walkthrough video, unlisted, linked from the README.
- The video covers the demo, the code tour, and one design decision.
- The repo is pinned in position 1 on the student's GitHub profile.
- The repo has a description and 3+ topic tags.
- The README's "live demo" link works (where applicable).

| Score   | What that looks like                                                      |
|--------:|---------------------------------------------------------------------------|
| 10      | Video clear and audible. Repo pinned. Demo lives at a public URL.         |
|  8–9    | Video present but rambling, or one of the polish items missing.           |
|  6–7    | Video present but short, no decision-tour. Repo not pinned.               |
|  3–5    | No video, but repo is otherwise complete.                                 |
|  0–2    | No video, no pinned repo, no live demo.                                   |

---

## How to self-grade

On Day 7, before you submit, go through this rubric and assign yourself
a number in each row. Be honest. If you score yourself **below 70**, use
the remaining time to lift the weakest rows — usually testing or
documentation. Above 70, ship it.
