# Week 1 — Python Foundations & Dev Environment

Welcome to **Code Crunch Convos**, an open-source Python bootcamp built in the
open for learners everywhere. Week 1 lays the foundation you'll stand on for
the rest of the program: you'll install Python, get comfortable in a terminal,
write your first scripts, learn how to isolate project dependencies with
virtual environments, and publish your very first commit to GitHub. By the
end of the week you will have a working Python development environment on
your machine and a small command-line program — "Hello, You" — pushed to a
public repository you own. No prior programming experience is required; we
will move slowly, define jargon, and build muscle memory through hands-on
exercises.

## Learning Objectives

By the end of this week, you will be able to:

- **Install** Python 3.11 or later on macOS, Linux, or Windows and verify the
  installation from a terminal.
- **Navigate** the filesystem from the command line using `cd`, `ls`,
  `mkdir`, and `pwd` (or PowerShell equivalents).
- **Execute** Python code in two distinct ways: interactively in the REPL and
  by running a `.py` script file.
- **Create** and **activate** an isolated virtual environment with `venv` and
  install packages into it with `pip`.
- **Author** clean, readable Python source files with comments, docstrings,
  and type hints.
- **Initialize** a Git repository, stage and commit changes, and push the
  repository to GitHub.
- **Configure** Visual Studio Code to run and debug Python files using its
  built-in Python extension.
- **Ship** a small interactive CLI program called "Hello, You" to your own
  GitHub account.

## Prerequisites

None. Week 1 assumes zero programming experience. You only need a computer
running macOS, Linux, or Windows 10/11, an internet connection, and a free
GitHub account (you'll create one this week if you don't already have one).

## Topics Covered

- What Python is and why it dominates so many industries
- Installing and verifying Python 3.11+
- The Python REPL vs running scripts (`python file.py`)
- Terminal and shell basics (`cd`, `ls`, `mkdir`, `pwd`)
- Virtual environments with `venv` — why and how
- Package management basics with `pip install`
- Writing your first program: `print("Hello, world!")`
- Single-line (`#`) and triple-quoted comments / docstrings
- Useful invocations: `python -m`, `python -c`
- Git basics: `init`, `add`, `commit`, `push`, `clone`
- GitHub: creating a repository and pushing your first commit
- VS Code essentials for Python: running and debugging

## Weekly Schedule

The schedule below adds up to approximately **36 hours**. Treat it as a
target, not a contract — some sections will click faster, others slower.

| Day       | Focus                                    | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----------|------------------------------------------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday    | Install Python; first program            |    2h    |    1h     |     0h     |    0.5h   |   1h     |     0h       |    0.5h    |     5h      |
| Tuesday   | Terminal, REPL, scripts                  |    2h    |    2h     |     0h     |    0.5h   |   1h     |     0h       |    0.5h    |     6h      |
| Wednesday | Virtual environments & pip               |    2h    |    2h     |     1h     |    0.5h   |   1h     |     0h       |    0h      |     6.5h    |
| Thursday  | Git basics & first commit                |    0h    |    1h     |     1h     |    0.5h   |   1h     |     2h       |    0.5h    |     6h      |
| Friday    | GitHub, VS Code, push your project       |    0h    |    1h     |     1h     |    0.5h   |   1h     |     2h       |    0.5h    |     6h      |
| Saturday  | Mini-project deep work                   |    0h    |    1h     |     1h     |    0h     |   1h     |     3h       |    0h      |     6h      |
| Sunday    | Quiz, review, polish                     |    0h    |    0h     |     0h     |    0.5h   |   0h     |     0h       |    0h      |     0.5h    |
| **Total** |                                          | **6h**   | **8h**    | **4h**     | **3h**    | **6h**   |   **7h**     |   **2h**   |  **36h**    |

## How to Navigate This Week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview (you are here) |
| [resources.md](./resources.md) | Curated readings, free books, and Python docs links |
| [lecture-notes/01-installing-python-and-running-your-first-program.md](./lecture-notes/01-installing-python-and-running-your-first-program.md) | Install Python, use the REPL, run your first script |
| [lecture-notes/02-terminal-virtual-environments-and-pip.md](./lecture-notes/02-terminal-virtual-environments-and-pip.md) | Terminal commands, `venv`, and `pip` |
| [lecture-notes/03-git-and-github-basics.md](./lecture-notes/03-git-and-github-basics.md) | Version control, your first repository, pushing to GitHub |
| [exercises/README.md](./exercises/README.md) | Index of short coding exercises |
| [exercises/exercise-01-hello-world.py](./exercises/exercise-01-hello-world.py) | Print your first message |
| [exercises/exercise-02-repl-explorer.py](./exercises/exercise-02-repl-explorer.py) | Drive the REPL like a calculator |
| [exercises/exercise-03-script-vs-repl.py](./exercises/exercise-03-script-vs-repl.py) | Compare running modes |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-personalized-banner.md](./challenges/challenge-01-personalized-banner.md) | Build a centered ASCII banner |
| [challenges/challenge-02-environment-audit.md](./challenges/challenge-02-environment-audit.md) | Print details about your Python install |
| [quiz.md](./quiz.md) | 10 multiple-choice questions |
| [homework.md](./homework.md) | Six practice problems for the week |
| [mini-project/README.md](./mini-project/README.md) | Full spec for the "Hello, You" CLI |
| [mini-project/starter.py](./mini-project/starter.py) | Starter file for the mini-project |

## Stretch Goals

If you finish early and want to push further, try any of the following:

- Configure a global `~/.gitignore_global` and learn what belongs in it.
- Set up SSH authentication with GitHub instead of HTTPS + token.
- Install and try a second Python version with `pyenv` (macOS/Linux) or
  `pyenv-win` (Windows) and switch between them per project.
- Read PEP 8 cover to cover at <https://peps.python.org/pep-0008/> and skim
  PEP 20 (`import this`) for Python's design philosophy.
- Add a `Makefile` or `justfile` to the mini-project that wraps `python -m
  venv`, install, and run commands behind one-word recipes.

## Up Next

Continue to [Week 2 — Variables, Data Types & Operators](../week-02-data-types-operators/README.md)
once you've pushed your mini-project to GitHub.
