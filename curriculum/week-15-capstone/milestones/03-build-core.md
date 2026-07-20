# Milestone 03 — Build Core (Days 3–4)

## Goal

By end of Day 4 your MVP sentence is **true**, demonstrated end-to-end,
running locally on a feature branch with an open **draft pull request**.
The code is not polished, the tests are minimal, but the user story
spine works.

This is the only milestone where you really write features. Two days,
four half-day chunks, four GitHub issues closed.

## Tasks

This milestone is structured as four half-day chunks. Aim for one
"chunk" each morning and afternoon. If you finish early, do *not* start
the next chunk early — use the spare time on tests for what you just
built.

### Day 3 — AM: data layer

1. **Define your data model(s).** SQLAlchemy `Model` classes for a web
   app, `@dataclass` for an in-memory tool, a `pydantic` model for an
   API. Keep them in their own module (`models.py`).

2. **Write a connection / persistence helper.** For SQLite: a function
   that opens a session, a context manager that closes it, a function
   that creates tables on first run.

3. **Write one test per model** that proves you can create and round-trip
   the object. These tests are also documentation — a future reader
   learns the model by reading its test.

4. **Commit.** Message like `feat(models): add User and Habit models`.

### Day 3 — PM: the first user story

1. **Implement Story 1.** For a web app, this is typically signup or
   login. For a CLI, it is the first command. For an API, it is one
   endpoint. For data, it is the first cleaning step.

2. **Wire it end-to-end.** A request hits the route, the route saves a
   row, the response renders. No skipping the middle.

3. **Write one happy-path test and one failure test.** "User can sign
   up" and "duplicate email is rejected". Tests run against an
   *in-memory* SQLite or a temporary file under `tmp_path` — never
   your real DB file.

4. **Commit.** Push the feature branch. Open a **draft pull request**
   from the feature branch to `main`. Title it `Build core (WIP)`.
   Reference the story issues in the PR description with
   `Refs #1, #2, ...`.

### Day 4 — AM: the next stories

1. **Pick the next 1–2 user stories** and implement them. Use the same
   pattern: code, end-to-end wire, two tests, commit, push.

2. **Resist new ideas.** Anything that appears in your head and is *not*
   on the proposal goes into a new GitHub issue with the label
   `nice-to-have`. Future-you will love present-you for this.

3. **If a story is bigger than you thought** — that's normal — cut it.
   Reduce its acceptance criteria so the *spirit* of the story still
   ships. A working signup with email-only and no password reset is a
   real signup; a never-shipping signup with OAuth and 2FA is not.

### Day 4 — PM: the last story + glue

1. **Implement the final story** that completes the MVP sentence.

2. **Walk through your own app.** Open it like a brand-new user. Sign
   up, create a habit, check in, see the streak. Fix the one or two
   embarrassing things you find.

3. **Update the draft PR description** with screenshots and a "what's
   in this PR" bullet list. The draft PR is the historical record of
   how the MVP came together — make it readable.

## Habits to develop this week

These are not optional. They are the spine of the *Git Hygiene* and
*Architecture* rubric scores.

- **Commit often.** Aim for 4–8 commits per day. Many small commits beat
  one giant "added everything" commit.
- **Message your commits.** Use the [Conventional Commits](https://www.conventionalcommits.org/)
  shape if you can: `feat(routes): add /signup`. Even without the prefix,
  one clear imperative sentence is fine.
- **Push every commit.** No work lives only on your laptop. Your laptop
  could die.
- **Keep tests passing.** If a commit makes a test fail, the next commit
  fixes it. Do not pile broken commits.
- **One PR, many commits.** All your work this milestone lives on one
  feature branch with one PR. Multiple PRs for a 2-day push is overkill;
  zero PRs is wrong.

## Sample feature branch flow

```bash
git checkout -b feature/03-core-mvp
# ... write code ...
git add -p                    # stage hunks, not whole files
git commit -m "feat(models): add User and Habit models"
git push -u origin feature/03-core-mvp
# open draft PR on GitHub

# ... more code ...
git commit -m "feat(routes): signup and login"
git commit -m "test(auth): cover happy path and duplicate email"
git push
# the draft PR updates automatically
```

## Type hints, today

Add them as you write. The rubric expects type hints on *public*
functions; you do not need them on every single internal helper.

A typed function looks like:

```python
from datetime import date


def streak_length(check_in_dates: list[date], today: date) -> int:
    """Return the current consecutive-day streak ending today.

    A streak counts only check-ins on consecutive days up to and
    including ``today``. Returns ``0`` if there is no check-in today.
    """
    if today not in check_in_dates:
        return 0
    sorted_dates = sorted(set(check_in_dates), reverse=True)
    streak = 0
    expected = today
    for d in sorted_dates:
        if d != expected:
            break
        streak += 1
        expected = expected.replace(day=expected.day) - _one_day(expected)
    return streak
```

Even if the body is rough, the *signature* tells a reviewer what the
function is for. That alone earns rubric points.

## Outputs

By end of Day 4 your repo has:

- [ ] At least three Python modules under `src/<package>/`.
- [ ] At least one test file per module (six-ish tests total).
- [ ] The MVP sentence demonstrably true when you run the app locally.
- [ ] A draft pull request on GitHub, titled `Build core (WIP)`,
      containing all of Day 3–4's commits.
- [ ] All issues for the implemented user stories closed (use
      `Closes #1` in commit messages to auto-close).
- [ ] Type hints on every public function and class.
- [ ] CI still green.

## Pitfalls

- **"I'll add tests at the end."** You won't, and they will be worse if
  you do. Write one test as you build each feature.
- **The dreaded refactor.** If you find a deep refactor you want to do
  on Day 4, write it down in an issue and *do it next week*. Refactors
  mid-build kill momentum.
- **Skipping the draft PR.** Reviewers (and future-you) love to see the
  shape of the work. A draft PR is free; not having one is a missed
  opportunity.
- **Working without coffee or sleep.** Sounds glib; it isn't. Tired
  capstone code is the kind that fails CI on Day 5.

## Done check

- [ ] The MVP sentence is true on `localhost`.
- [ ] Every story issue from Milestone 02 is closed *or* explicitly
      moved to a `nice-to-have` issue.
- [ ] The draft PR exists and is up to date.
- [ ] You can demo the project to yourself in under 60 seconds.

Tomorrow: tests, lint, and polish. See
[04-test-and-polish.md](04-test-and-polish.md).
