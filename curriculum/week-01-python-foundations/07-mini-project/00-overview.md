# Mini-Project — "Hello, You"

This is the capstone of Week 1. You'll combine **every** topic from the
week — installing Python, writing a script, using a virtual environment,
managing dependencies, and version control — into a single small project
called **Hello, You**. When you're done, your project will live on
GitHub under your own account, ready to share with friends, family, and
future employers.

## Goal

Build a tiny command-line program that asks the user for their name (and,
optionally, their favorite programming language), then prints a friendly
personalized greeting.

## User Story

> *As a* curious learner just starting Python,
> *I want* a script that greets me by name,
> *so that* I prove to myself I can collect input, transform it, and
> publish working code to GitHub.

## Functional Requirements

The program must:

1. Prompt the user for their **name** with a clear message.
2. Optionally prompt the user for their **favorite programming language**
   (an empty answer is allowed and should default to "Python").
3. Strip leading/trailing whitespace from every answer.
4. Print a greeting that includes both the name and the language. For
   example, given `Ada` and `Python`:

   ```text
   Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
   ```

5. Exit cleanly. No tracebacks, no leftover prompts.

## Technical Requirements

You must:

- Develop the project inside its **own folder** named `hello-you`.
- Use a **virtual environment** named `.venv` inside that folder. Do
  **not** commit the `.venv/` directory.
- Track the project with **Git** from the very first commit, and push it
  to a **new public GitHub repository** under your own account named
  `hello-you`.
- Include a project-level `README.md` (different from this spec — yours
  is for the end user) that explains what the project does and how to
  run it.
- Include a `.gitignore` containing at least `.venv/`, `__pycache__/`,
  and `.DS_Store`.
- Use **type hints** on every function you define.
- Place the entry point inside an `if __name__ == "__main__":` guard.

## Suggested File Structure

```text
hello-you/
├── .gitignore
├── .venv/                  (not committed)
├── README.md
├── hello_you.py            (your real script — rename starter.py)
└── requirements.txt        (optional, see stretch goals)
```

## How to Get Started

1. Pick a parent folder on your machine (for example, `~/projects`).
2. Copy `starter.py` from this folder into a new `hello-you/` directory
   and rename it to `hello_you.py`.
3. Open a terminal in that directory and run:

   ```bash
   python -m venv .venv
   source .venv/bin/activate     # or .venv\Scripts\Activate.ps1 on Windows
   ```

4. Initialize Git and make your first commit:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: starter for Hello, You"
   ```

5. Implement `prompt_user()` and `build_greeting()` in `hello_you.py`.
6. Run the script and refine until the output matches the example above.
7. Create a `hello-you` repository on GitHub, add it as `origin`, and
   push.

## Hints

- `input("Your name: ")` returns whatever the user types, as a string.
- `str.strip()` removes leading/trailing whitespace.
- A short conditional like `language = raw_language.strip() or "Python"`
  uses the fact that empty strings are *falsy* in Python — it defaults
  to `"Python"` when the user just presses Enter.
- F-strings make string assembly easy: `f"Hello, {name}!"`.

## Stretch Goals (Pick Any That Excite You)

- **Loop until "quit".** Keep asking for names until the user types
  `quit` (case-insensitive). Print a friendly farewell on exit.
- **Save names to a file.** Append every greeted name to a file called
  `guests.txt`, one per line, with a timestamp.
- **Multiple languages.** If the user enters something other than
  Python, vary the greeting line per language (a small dictionary
  mapping language names to a punchy line works well).
- **Pretty banner.** Reuse the banner generator from Challenge 1 to
  print the name in a fancy box.
- **Add a dependency.** Install `rich` (`python -m pip install rich`),
  freeze it into `requirements.txt`, and use it to colorize the
  greeting.

## Rubric / Self-Check Checklist

Tick each box before declaring the mini-project done.

- [ ] `python hello_you.py` runs without errors.
- [ ] The script prompts for a name and an optional language.
- [ ] The greeting line correctly includes the name and the language.
- [ ] Empty whitespace input is handled gracefully.
- [ ] The project lives in its own folder with a `.venv/` that is **not**
      tracked.
- [ ] A `.gitignore` exists and excludes `.venv/`, `__pycache__/`, and
      OS junk.
- [ ] At least three commits are in the Git history with clear messages.
- [ ] Type hints are present on every function signature.
- [ ] A user-facing `README.md` explains how to clone, set up a venv,
      and run the project.
- [ ] The repository has been pushed to GitHub and is publicly visible.
- [ ] You've added the GitHub URL to your Week 1 notes so the next
      instructor (or future you) can find it.

## What to Submit

Self-submission only for Week 1. Paste the URL of your GitHub repository
into your personal notes (or, if you're learning with a cohort, into the
agreed shared channel) so you can refer back to it during Week 2.

Good luck — and welcome to Code Crunch Convos!
