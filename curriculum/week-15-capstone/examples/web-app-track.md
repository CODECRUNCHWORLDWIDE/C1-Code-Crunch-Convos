# Web App Track Example — Habit Tracker

A small Flask + SQLite app where a logged-in user creates habits, marks
them done each day, and sees their current streak. Deployed to a free
host. Designed to be finishable in seven days while still demonstrating
auth, persistence, templates, testing, and CI.

## MVP sentence

> *A logged-in user can record a daily check-in for one habit and see
> their current streak.*

If that sentence is true on the deployed app, the MVP is done.

## User stories

1. **Sign up.** As a new user, I can create an account with email and
   password, and be logged in afterwards.
2. **Log in / log out.** As a returning user, I can log in and log out.
3. **Add a habit.** As a logged-in user, I can add a named habit.
4. **Check in.** As a logged-in user, I can mark today's habit as done.
5. **See streaks.** As a logged-in user, I can see my current streak for
   each habit.

## Anti-goals (NOT building this week)

- Social / friends / sharing.
- Mobile-only features (PWA, push notifications).
- Habit categories, tags, or color themes.
- Charts beyond a current-streak integer.
- Email reminders.
- OAuth or "Sign in with Google" — local password is enough.

## Suggested tech stack

- Python 3.11+
- Flask 3
- Flask-Login (or a hand-rolled session, your choice — but Flask-Login
  is short, well-known, and rubric-friendly)
- SQLAlchemy 2 + SQLite
- bcrypt or werkzeug.security for password hashing
- Jinja2 templates (built into Flask)
- Pico.css or Tailwind via CDN for tolerable styling without
  build-tools
- pytest + pytest-cov for tests
- ruff + black for lint and format
- GitHub Actions for CI
- Fly.io or Render for deploy

## Folder layout

```text
habit-tracker/
├── src/habit_tracker/
│   ├── __init__.py
│   ├── app.py           # create_app(), routes, blueprint registration
│   ├── auth.py          # signup, login, logout routes
│   ├── habits.py        # habit + check-in routes
│   ├── models.py        # User, Habit, CheckIn
│   ├── database.py      # init_db, session_scope
│   ├── streaks.py       # pure functions: streak_length(...)
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       └── today.html
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_streaks.py
│   ├── test_auth.py
│   └── test_habits.py
├── docs/
│   ├── PROPOSAL.md
│   ├── RETRO.md
│   └── screenshots/
├── scripts/
│   └── seed.py
├── .github/workflows/ci.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

## Suggested data model

```python
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from your_package.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    habits: Mapped[list["Habit"]] = relationship(back_populates="user")


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(index=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="habits")
    check_ins: Mapped[list["CheckIn"]] = relationship(back_populates="habit")


class CheckIn(Base):
    __tablename__ = "check_ins"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(index=True)
    on_date: Mapped[date]

    habit: Mapped[Habit] = relationship(back_populates="check_ins")
```

Note the *streak* logic does not live in the database. It lives in a
pure function in `streaks.py` — that makes it trivially unit-testable.

## Day-by-day plan

**Day 1 — Idea & Scope.** Write the proposal. (You're doing it now.)

**Day 2 — Skeleton.** Repo, CI, layout, smoke test, issues for
each story.

**Day 3 AM — Models + DB.** Define `User`, `Habit`, `CheckIn`. Write
`init_db()`. Three tests, one per model.

**Day 3 PM — Auth.** Signup, login, logout routes. `current_user`
helper. Two tests: happy path + duplicate email.

**Day 4 AM — Habits.** "Add a habit" route + form + template. "Check
in for today" POST handler. Two tests covering both.

**Day 4 PM — Today view.** A page listing the user's habits with their
current streak. Pull from `streaks.streak_length(...)`. One integration
test that signs up, adds a habit, checks in, and asserts the streak.

**Day 5 — Test & polish.** Push coverage past 70%. Add error pages.
Style with Pico.css. Screenshots. Rewrite README.

**Day 6 AM — Deploy.** Fly.io. Mount a volume for the SQLite file.

**Day 6 PM — Video.** Record 4 minutes. Upload as Unlisted.

**Day 7 — Retro, pin, submit.**

## What "done" looks like

A reviewer can:

1. Open the deployed URL.
2. Sign up with any email and password.
3. Add a habit ("drink water").
4. Click "I did it today".
5. See the streak go to 1.
6. Log out and log back in; data is still there.

And, in the repo:

- CI is green.
- `pytest --cov` shows ≥ 70%.
- README has a screenshot, install steps, demo link, video link.
- The walkthrough video is 3–5 minutes.

## Where this project demonstrates each week

- **Week 1–7** — package layout, modules, classes, exceptions.
- **Week 8** — JSON handling in your future API endpoint, if you add one.
- **Week 9** — Flask, blueprints, Jinja2 templates.
- **Week 10** — SQLAlchemy + SQLite.
- **Week 11** — pytest, fixtures, integration tests, CI.
- **Week 12** — `scripts/seed.py` as a small automation script.

That is the bootcamp's whole spine, demonstrated in one repo.

## Stretch goals (only if Day 5 is finished by lunchtime)

- A `nice-to-have` GitHub label and one stretch issue: weekly chart of
  check-ins (matplotlib server-side rendering, embed as PNG).
- A `flask --app habit_tracker.app shell` recipe in the README.
- A pre-commit hook config.

Resist any stretch goal that touches the data model — schema migrations
are out of scope.
