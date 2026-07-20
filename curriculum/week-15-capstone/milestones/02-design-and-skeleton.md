# Milestone 02 — Design & Skeleton (Day 2)

## Goal

By end of Day 2, you have a **public GitHub repository** with the
project's folder structure scaffolded, a working CI pipeline that is
**green on a placeholder test**, a license, a starter README, and one
**GitHub issue per user story** open and labelled.

There is still no feature code. The day's product is a skeleton you can
build on tomorrow.

## Tasks

1. **Create the GitHub repository.** On <https://github.com/new>,
   create a repo named with hyphens (e.g. `habit-tracker`), tick
   *Add a README*, *Add .gitignore (Python)*, and *Choose a license
   (MIT)*. Make it **Public**.

2. **Clone and link your Day 1 work.** Clone the new repo and copy
   `docs/PROPOSAL.md` over from yesterday's local repo. Commit and
   push.

3. **Scaffold the folder structure.** Pick a layout from Lecture 2
   (the `src/` layout is recommended). Create the directories and
   empty placeholder files:

   ```text
   src/<your_package>/
       __init__.py
       core.py          # or similar — a placeholder for real code
   tests/
       __init__.py
       test_smoke.py
   docs/
       PROPOSAL.md      # already there
   .github/
       workflows/
           ci.yml
   ```

4. **Write a placeholder test.** The CI must have something to run.
   In `tests/test_smoke.py`:

   ```python
   """A smoke test that proves the package imports."""

   from your_package import core


   def test_package_imports() -> None:
       """Importing the package should not raise."""
       assert core is not None
   ```

   And in `src/your_package/core.py`:

   ```python
   """Core module — placeholder for Milestone 03."""

   __all__: list[str] = []
   ```

5. **Write `pyproject.toml`.** Use the template from Lecture 2. Replace
   `habit-tracker` with your project name and `habit_tracker` with your
   package name. Add only the runtime deps you actually know you'll
   need; you can add more in Milestone 03.

6. **Install your package locally.** `pip install -e ".[dev]"` should
   succeed. Run `pytest`. It should pass (one test). If either step
   fails, fix before moving on — CI will trip on the same problems.

7. **Add the CI workflow.** Drop the `.github/workflows/ci.yml` from
   Lecture 2 into your repo. Commit. Push. Open the **Actions** tab on
   GitHub. Watch the workflow run. When it goes green, take a screenshot
   for joy.

8. **Add the CI badge to the top of your README.** The URL pattern is:

   ```markdown
   ![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)
   ```

9. **Write a *starter* README.** It doesn't need to be perfect today —
   you will polish it in Milestone 04 — but it must contain:

   - Title and one-sentence pitch.
   - CI badge.
   - "Status" line: *Work in progress — capstone project for Code Crunch
     Convos Week 15.*
   - Install instructions (which must actually work).
   - A "Planned features" bullet list (copy your user stories).
   - A link to `docs/PROPOSAL.md`.
   - A License section pointing to `LICENSE`.

10. **Open one GitHub issue per user story.** Title each like
    *"Story 1: As a new user I can sign up"*. Label them `enhancement`
    and `mvp`. Drop them into a project board if you like, but a flat
    list of issues is enough.

11. **Create a `dev` or feature branch.** From now on, you do not push
    feature code straight to `main`. Branch with a name like
    `feature/01-signup` and open a draft pull request tomorrow.

12. **Make the repo show well.** Add a one-line description and a few
    topics on the GitHub repo settings page (e.g. `flask`, `python`,
    `capstone`, `bootcamp`). Topics make the repo discoverable.

## Outputs

By end of Day 2 your repo on GitHub has:

- [ ] Public visibility.
- [ ] `LICENSE`, `.gitignore`, `README.md`, `pyproject.toml`,
      `docs/PROPOSAL.md`.
- [ ] `src/<package>/` with at least one module.
- [ ] `tests/` with at least one passing test.
- [ ] `.github/workflows/ci.yml` and a **green** Actions run on `main`.
- [ ] Green CI badge in the README.
- [ ] One open issue per user story.
- [ ] A topic/description on the repo settings.

## Sample first commit graph

If everything went well, your commit history on `main` looks something
like:

```text
*  e7c2a1b   docs: link PROPOSAL.md from README
*  9b3f0d2   ci: add GitHub Actions workflow
*  4f81a6e   chore: scaffold src layout and smoke test
*  c1d28a0   docs: add PROPOSAL.md
*  a0b9e3f   Initial commit
```

If your tree is one giant commit titled "scaffold", split it next time —
small commits read well in interviews ("this is the kind of git hygiene
I bring to a team").

## Pitfalls

- **CI failing on day 2 and ignored.** Fix it now while there is only
  one test. Debugging CI on Day 5 with a real test suite is much harder.
- **Skipping the license.** Without a license, your repo is technically
  not open-source. Add MIT today.
- **Pushing to `main` for everything.** Branch + PR is part of the
  rubric (git hygiene). Start the habit now.
- **Forgetting `__init__.py`.** Pytest discovery breaks in confusing
  ways without it. Add empty ones in `src/<package>/` and `tests/`.
- **Adding twelve dependencies "just in case".** Add only what you'll
  use this week.

## Done check

- [ ] Repo is public and findable.
- [ ] CI is green on `main`.
- [ ] README has install steps that work.
- [ ] One issue per user story is open.
- [ ] Feature branch for tomorrow's work is created.

Tomorrow: write code. See
[03-build-core.md](03-build-core.md).
