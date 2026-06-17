# Week 1 Homework

Six practice problems that revisit the week's topics. The full set should
take about **6 hours** in total. Work in your Week 1 Git repository so
each problem produces at least one commit you can point to later.

Each problem includes:

- A short **problem statement**.
- **Acceptance criteria** so you know when you're done.
- A **hint** if you get stuck.
- An **estimated time**.

---

## Problem 1 — Verify your install

**Problem statement.** Open a fresh terminal and confirm you can run
Python 3.11+ end-to-end. Capture proof.

**Acceptance criteria.**

- Run `python --version` (or `python3 --version`) and the printed version
  is 3.11 or higher.
- Start the REPL, type `print("Week 1!")`, and see `Week 1!` echoed back.
- Save a screenshot or copy/paste of the REPL session into a file called
  `notes/install-check.txt` in your repo.

**Hint.** If `python` isn't found, try `python3`. If neither works, re-run
the installer and ensure "Add Python to PATH" is selected (Windows) or
that `/usr/local/bin` (macOS) is on your PATH.

**Estimated time.** 30 minutes.

---

## Problem 2 — Build a project skeleton with a venv

**Problem statement.** Create a brand-new folder called `week-01-homework`,
initialize a Git repository inside it, and add a virtual environment plus
a `.gitignore`.

**Acceptance criteria.**

- `git status` shows a clean working tree after your initial commit.
- `.venv/` exists on disk but is **not** tracked by Git.
- `.gitignore` includes at least `.venv/`, `__pycache__/`, and
  `.DS_Store`.
- `git log --oneline` shows a single initial commit with a meaningful
  message.

**Hint.** Build the project up step-by-step with the commands at the end
of Lecture 3, but stop before adding any GitHub remote.

**Estimated time.** 45 minutes.

---

## Problem 3 — A tiny script with comments and a docstring

**Problem statement.** Inside the project from problem 2, create a script
called `about_me.py` that prints three facts about you (name, favorite
food, one programming goal for this course). The file must include a
module-level docstring and at least two inline `#` comments.

**Acceptance criteria.**

- `python about_me.py` prints exactly three lines, one per fact.
- The file's first non-blank line is a triple-quoted docstring.
- At least two `#` comments live somewhere in the file.
- The script uses one function with type hints (even if it's just `def
  main() -> None:`).

**Hint.** Re-read the "Comments and Docstrings" section of Lecture 1.

**Estimated time.** 45 minutes.

---

## Problem 4 — Install and freeze a package

**Problem statement.** With your venv activated, install the `requests`
package and freeze your dependencies. Then deactivate, reactivate, and
verify the package is still available.

**Acceptance criteria.**

- `python -m pip install requests` completes without error.
- A `requirements.txt` file exists in the project root, contains at least
  one line, and is committed to Git.
- After `deactivate` followed by re-activation, `python -c "import
  requests; print(requests.__version__)"` prints a version number.

**Hint.** Use `python -m pip freeze > requirements.txt`. Do **not**
hand-edit the file.

**Estimated time.** 45 minutes.

---

## Problem 5 — Publish your repo to GitHub

**Problem statement.** Take the local repository from problems 2–4 and
push it to GitHub as a new public repository called `week-01-homework`.

**Acceptance criteria.**

- The repository exists on GitHub under your account.
- The repository's homepage shows your `about_me.py`, `.gitignore`, and
  `requirements.txt` (but **not** `.venv/`).
- At least two commits are visible in the repository's history.
- The first line of the GitHub README (or repo description) names this
  course: "Code Crunch Convos — Week 1 homework".

**Hint.** Follow Lecture 3's "Creating a GitHub Repository" section.
Authenticate with a personal access token, not your password.

**Estimated time.** 1 hour.

---

## Problem 6 — Combine everything with a small CLI

**Problem statement.** Inside the same repo, create a script
`day_planner.py` that:

1. Prompts the user for their name.
2. Prompts the user for three tasks to do today.
3. Prints a numbered list of those tasks, prefixed by `Today, <Name>:`.

**Acceptance criteria.**

- Running `python day_planner.py` reproduces the prompts and prints a
  three-item numbered list.
- The script uses a `main()` function with a `-> None` return type hint.
- All user input is stripped of surrounding whitespace before being used.
- The final solution is committed to Git with a message like
  `Add day_planner CLI`, and the commit is pushed to GitHub.

**Hint.** A `for i, task in enumerate(tasks, start=1):` loop is a clean
way to print the numbered list.

**Estimated time.** 1 hour 45 minutes.

---

## Time budget recap

| Problem | Estimated time |
|--------:|--------------:|
| 1 | 30 min |
| 2 | 45 min |
| 3 | 45 min |
| 4 | 45 min |
| 5 | 1 h 0 min |
| 6 | 1 h 45 min |
| **Total** | **~6 hours** |
