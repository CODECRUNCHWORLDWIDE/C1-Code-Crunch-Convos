# Hello, You

A very small command-line program that asks for your name and your
favorite programming language, then greets you by both.

Built as the Week 1 mini-project for **Code Crunch Convos**, an
open-source Python bootcamp.

```text
$ python hello_you.py
Your name: Ada
Favorite programming language [Python]:
Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
```

Press Enter at the language prompt and it defaults to `Python`.

## Requirements

- Python 3.11 or newer (`python --version` to check).
- Nothing else. `hello_you.py` imports no third-party packages.

## Setup

```bash
git clone https://github.com/your-username/hello-you.git
cd hello-you
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\Activate.ps1      # Windows PowerShell
```

Your prompt should now start with `(.venv)`. To leave the environment
later, run `deactivate`.

## Run it

```bash
python hello_you.py
```

## The fancy version

`hello_you_plus.py` is the same program with the stretch goals turned on:
it loops until you type `quit`, prints an ASCII banner around your name,
varies the closing line per language, writes every greeting to
`guests.txt` with a timestamp, and colorizes the output when the `rich`
package is installed.

```bash
python -m pip install -r requirements.txt
python hello_you_plus.py
```

`rich` is optional. Without it the script prints exactly the same text,
just without color.

## Files

| File | What it is |
|------|------------|
| `hello_you.py` | The program. Two functions plus a `main()`. |
| `hello_you_plus.py` | The stretch version described above. |
| `banner.py` | The ASCII banner generator, reused from Week 1 Challenge 1. |
| `requirements.txt` | Pinned dependencies for the stretch version only. |
| `.gitignore` | Keeps `.venv/`, caches, and OS clutter out of the repo. |
