# Reference implementation — Week 1 mini-project ("Hello, You")

This folder is the working answer to [Week 1's mini-project](../../../curriculum/week-01-python-foundations/mini-project/README.md). It is a real, runnable project, not an excerpt: `hello-you/` is exactly the tree that produced every transcript in the [mini-project walkthrough](../../../curriculum/week-01-python-foundations/mini-project/README.md).

Read the walkthrough for the *why*. This file tells you what is here and how to run it.

The mini-project's real deliverable is **a repository on GitHub**, not a folder on a course website. So treat `hello-you/` as a copy of what your own `hello-you` repository should look like the moment before you push it — same files, same `.gitignore`, same shape. What it cannot show you is your commit history, and that is half the assignment. The walkthrough covers that part.

---

## What is in the folder

```text
week-01-python-foundations/
├── 00-overview.md          (this file)
└── hello-you/
    ├── .gitignore
    ├── README.md           the user-facing README the spec asks for
    ├── banner.py           Challenge 1's build_banner, reused by the stretch script
    ├── hello_you.py        the mini-project proper — 42 lines
    ├── hello_you_plus.py   all five stretch goals
    └── requirements.txt    pinned rich, for the stretch script only
```

Two files are not committed here because they are not source:

- **`.venv/`** — you create it yourself with `python -m venv .venv`. The whole point of the assignment's `.gitignore` is that this folder never enters a repository.
- **`guests.txt`** — written by `hello_you_plus.py` at runtime. It is generated output, so it is ignored too.

---

## How to run it

Python 3.11 or newer. `hello_you.py` imports nothing outside the standard library, so there is no install step for the core answer.

```bash
cd projects/solutions/week-01-python-foundations/hello-you
python hello_you.py
```

```text
Your name: Ada
Favorite programming language [Python]:
Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
```

That greeting line is the exact string the spec's requirement 4 asks for.

### The stretch version

```bash
python -m venv .venv
source .venv/bin/activate          # or .venv\Scripts\Activate.ps1 on Windows
python -m pip install -r requirements.txt
python hello_you_plus.py
```

`rich` is optional. Without it, `hello_you_plus.py` prints character-for-character the same text with no color — the `try` / `except ImportError` at the top of the file is what makes that true, and it is why a grader without `rich` installed still sees a working program.

---

## How it maps to the spec

| Spec requirement | Where it lives |
|---|---|
| 1 — prompt for a name | `prompt_user`, first `input()` |
| 2 — optional language, empty defaults to `Python` | `prompt_user`, `... .strip() or DEFAULT_LANGUAGE` |
| 3 — strip whitespace from every answer | `.strip()` on both `input()` calls, at the moment the value enters |
| 4 — greeting includes name and language, exact wording | `build_greeting` |
| 5 — exit cleanly, no tracebacks | `main()` ends after one `print`; no exception can escape a run that answers both prompts |
| own folder named `hello-you` | this folder |
| `.venv` not committed | `.gitignore` line 2, plus venv's own self-ignore |
| user-facing `README.md` | `hello-you/README.md` |
| `.gitignore` with `.venv/`, `__pycache__/`, `.DS_Store` | `hello-you/.gitignore` — all three, plus five more |
| type hints on every function | every `def` in all three `.py` files |
| `if __name__ == "__main__":` guard | bottom of `hello_you.py`, `hello_you_plus.py`, `banner.py` |

| Stretch goal | Where it lives |
|---|---|
| Loop until `quit` | `main` / `greet_once` in `hello_you_plus.py`, and `QUIT_WORDS` |
| Save names to a file with a timestamp | `record_guest` → `guests.txt` |
| Vary the greeting per language | `LANGUAGE_LINES` and `closing_line` |
| Pretty banner | `from banner import build_banner`, called in `greet_once` |
| Add a dependency | `rich` in `requirements.txt`, used by `show` |

---

## Reading order

If you are studying the code rather than running it:

1. `hello_you.py` top to bottom. It is short enough to read in one sitting, and it is the thing being graded.
2. `banner.py` — one function, already familiar from Challenge 1.
3. `hello_you_plus.py` in this order: `closing_line` and `build_greeting` (pure functions, no I/O), then `record_guest` and `show` (each owns one side effect), then `greet_once`, then `main`.

That is also a reasonable order to *write* them in. Every function that computes a string returns it instead of printing it, and only `show` and `record_guest` touch the outside world. Keeping those two jobs apart is what lets you verify the whole program without typing at a prompt.
