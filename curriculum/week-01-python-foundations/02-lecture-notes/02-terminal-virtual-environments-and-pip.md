# Lecture 2 — Terminal, Virtual Environments, and pip

You wrote your first script in Lecture 1, but you didn't really *control*
the environment around it. This lecture fixes that. By the end you'll be
fluent in the four most-used terminal commands, you'll understand why
serious Python projects always live inside a **virtual environment**, and
you'll know how to install and freeze third-party packages with `pip`.

## Why the Terminal?

A **terminal** (also called a *shell* or *command line*) is a text-based
interface to your operating system. Every productive Python developer lives
in one. Why? Because the terminal lets you:

- Run scripts with arguments and see their output.
- Switch between projects in one keystroke.
- Activate the right virtual environment for the project you're working on.
- Use Git and dozens of other developer tools that don't have a graphical
  equivalent.

If terminals feel intimidating, don't worry — you only need a handful of
commands to get started.

## The Four Core Commands

The big four work on macOS, Linux, and (with slight tweaks) Windows
PowerShell. We'll use the macOS/Linux names first, then the Windows
equivalents.

### `pwd` — print working directory

`pwd` tells you where you currently are in the filesystem. The "working
directory" is the folder your terminal session is sitting in.

```bash
pwd
```

```text
/Users/you/projects
```

On Windows PowerShell, the equivalent is `Get-Location` or just `pwd` (it's
aliased).

### `ls` — list files

`ls` shows the contents of the current directory.

```bash
ls
```

```text
greet.py    hello.py    notes.txt
```

Add `-la` for a long-format listing including hidden files (files whose
name starts with `.`):

```bash
ls -la
```

On Windows PowerShell, use `Get-ChildItem` or its alias `ls`.

### `cd` — change directory

`cd` moves you into a different directory. Pass the path as an argument.

```bash
cd projects
cd /Users/you/projects/code-crunch
cd ..             # one level up
cd ~              # back to your home directory
```

PowerShell uses the same `cd` command.

### `mkdir` — make directory

`mkdir` creates a new folder.

```bash
mkdir my-first-project
cd my-first-project
```

Add `-p` to create any missing parent directories along the way:

```bash
mkdir -p week-01/exercises
```

PowerShell: `mkdir` works, or use `New-Item -ItemType Directory`.

### A quick session

Putting it all together, here's what a typical first-project session looks
like:

```bash
cd ~
mkdir code-crunch-week-01
cd code-crunch-week-01
pwd
ls
```

That sequence: goes home, creates a project folder, enters it, prints where
you are, and lists the contents (currently empty).

## Windows PowerShell Cheat Sheet

If you're on Windows, the table below maps the macOS/Linux commands you'll
see throughout this course to their PowerShell equivalents. The good news:
in modern PowerShell, the short Unix-style names are aliased, so most
commands "just work."

| What you want      | macOS / Linux          | Windows PowerShell           |
|--------------------|------------------------|------------------------------|
| Where am I?        | `pwd`                  | `pwd` or `Get-Location`      |
| List files         | `ls -la`               | `ls -Force` or `Get-ChildItem -Force` |
| Move directories   | `cd path`              | `cd path`                    |
| Make a directory   | `mkdir name`           | `mkdir name`                 |
| Delete a file      | `rm file`              | `rm file` or `Remove-Item file` |
| Show a file        | `cat file`             | `cat file` or `Get-Content file` |

## Why Virtual Environments?

Imagine you're working on two projects:

- **Project A** needs version 1.0 of a library called `awesome`.
- **Project B** needs version 2.0 of `awesome` because it uses a feature
  that didn't exist in 1.0.

If you install `awesome` globally on your machine, you can only have one
version at a time. Project A and Project B fight each other forever. This
is the **dependency-conflict problem**, and every working programmer has
been bitten by it.

A **virtual environment** (or *venv*) solves this by giving each project
its own isolated Python installation living in a folder inside the
project. Anything you `pip install` while the venv is active lives only
inside that folder. Other projects — and the rest of your system — are
unaffected. Conceptually:

```text
your machine
├── system Python (don't touch)
├── Project A/
│   └── .venv/        <- awesome==1.0 lives here
└── Project B/
    └── .venv/        <- awesome==2.0 lives here
```

## Creating a Virtual Environment with `venv`

Python ships with a `venv` module that creates virtual environments. To
create one in the current directory, run:

```bash
python -m venv .venv
```

This produces a `.venv/` folder with its own copy of the Python interpreter
and its own `pip`. The leading dot is a convention so the folder is
"hidden" from default `ls` output.

Read the official `venv` docs at <https://docs.python.org/3/library/venv.html>.

## Activating and Deactivating

Creating a venv is not enough — you must **activate** it so your shell uses
its Python and `pip` instead of the system ones.

### macOS / Linux

```bash
source .venv/bin/activate
```

After activation, your prompt usually changes to show the venv name:

```text
(.venv) you@machine code-crunch-week-01 %
```

### Windows PowerShell

```text
.venv\Scripts\Activate.ps1
```

If PowerShell refuses with an *execution policy* error, you may need to run
the following once per machine (it allows local scripts to run):

```text
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Verifying activation

After activation, ask Python where it lives:

```bash
python -c "import sys; print(sys.executable)"
```

The path should point inside your project's `.venv/` folder. If it points
to a system-wide location, activation didn't take effect.

### Deactivating

When you're done, simply run:

```bash
deactivate
```

Your prompt returns to normal and the system Python is back in charge.

## Installing Packages with `pip`

`pip` is Python's package installer. The safest way to invoke it is via the
Python module flag we learned in Lecture 1:

```bash
python -m pip install requests
```

The `python -m pip` form guarantees you're using the `pip` belonging to
the currently active Python (which, when a venv is activated, is the venv's
pip). Once installed, you can use the package in code:

```python
"""show_status.py — fetch a URL and print the HTTP status."""

import requests


def main() -> None:
    response = requests.get("https://www.python.org")
    print(response.status_code)


if __name__ == "__main__":
    main()
```

Run it:

```bash
python show_status.py
```

You should see `200` printed if Python's home page is reachable.

## Listing What's Installed

To see every package currently installed in your active environment:

```bash
python -m pip list
```

You'll get a two-column table of package names and versions. Right after
creating a fresh venv it shows just `pip` and a couple of dependencies — a
nice, clean starting point.

## Freezing Your Dependencies

When you share your project, other people need to know which packages —
and which **versions** — to install. The conventional answer is a file
called `requirements.txt` that you produce with `pip freeze`:

```bash
python -m pip freeze > requirements.txt
```

`requirements.txt` is a plain-text list of one package per line:

```text
requests==2.31.0
certifi==2024.7.4
charset-normalizer==3.3.2
idna==3.7
urllib3==2.2.2
```

To recreate the same environment elsewhere (or in CI), the recipient runs:

```bash
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\Activate.ps1 on Windows
python -m pip install -r requirements.txt
```

This is the bedrock of reproducible Python projects.

## Putting It All Together

A typical first-day-of-a-new-project ritual:

```bash
cd ~/projects
mkdir tiny-app
cd tiny-app
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests
python -m pip freeze > requirements.txt
```

You now have a brand-new project folder with an isolated environment and a
recorded list of dependencies. Future you (and future collaborators) will
thank present you.

## Common Pitfalls

- **"It worked yesterday."** Almost always means you forgot to activate the
  venv today. Check your prompt for the `(.venv)` prefix.
- **`pip` is installing to the wrong place.** Always use `python -m pip`
  inside an active venv. Bare `pip` can shadow to a different Python.
- **You added `.venv/` to Git.** Don't. Add `.venv/` to your `.gitignore`
  (we'll cover that in Lecture 3). Virtual envs are recreated on each
  machine from `requirements.txt`.
- **PowerShell won't let you activate the venv.** The execution-policy fix
  shown above is a one-time per-user setting and is safe for normal use.

## Recap

You now know how to:

- Move around the filesystem with `pwd`, `ls`, `cd`, and `mkdir`.
- Translate those commands to Windows PowerShell.
- Create an isolated virtual environment with `python -m venv .venv`.
- Activate and deactivate that environment.
- Install, list, and freeze packages with `python -m pip`.
- Reproduce an environment from a `requirements.txt` file.

Next up: Lecture 3, where we'll bring everything you've built so far under
**version control** with Git and publish it to GitHub.
