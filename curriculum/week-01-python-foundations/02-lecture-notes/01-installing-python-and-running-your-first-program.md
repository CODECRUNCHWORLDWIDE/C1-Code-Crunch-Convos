# Lecture 1 — Installing Python and Running Your First Program

Welcome to your first Code Crunch Convos lecture. By the end of this session
you will have Python installed on your machine, verified that it works, run
code two different ways, written your first real script, and understood the
basic vocabulary every Python programmer uses. We'll move slowly and define
every new word. If something doesn't click, re-read the section and try the
example yourself — typing the code is what makes it stick.

## What Is Python?

**Python** is a high-level, general-purpose programming language. "High-level"
means it abstracts away the gritty details of the hardware so you can focus
on the problem you're solving. "General-purpose" means people use it for
nearly everything: web sites, data analysis, machine learning, scientific
computing, automating boring tasks, game prototypes, robotics, financial
modeling, and more.

Python was created by **Guido van Rossum** in the late 1980s and first
released in 1991. The name has nothing to do with snakes — Guido was a fan
of the British comedy troupe *Monty Python's Flying Circus*. Today Python is
maintained by the Python Software Foundation and a global community of
volunteers, with a new feature release every October. We're targeting
**Python 3.11 or newer** in this course because every version from 3.11
onward includes substantial speed improvements and better error messages,
both of which make your life easier as a beginner.

Python's design philosophy is captured in a tongue-in-cheek poem called the
*Zen of Python* (PEP 20, <https://peps.python.org/pep-0020/>). Two lines you
should internalize today:

- *Beautiful is better than ugly.*
- *Readability counts.*

Python code is meant to read like pseudocode. If your code is hard to read,
something has gone wrong.

## Installing Python 3.11+

Pick the section that matches your operating system. After installing, jump
to the "Verifying Your Install" section below.

### macOS

The Python that ships with macOS is often outdated. Install a fresh copy
using one of the following:

1. **Official installer:** download from <https://www.python.org/downloads/>
   and run the `.pkg` file.
2. **Homebrew (recommended if you already use it):**

   ```bash
   brew install python@3.12
   ```

### Linux

Most modern distributions include a recent Python. On Ubuntu/Debian, install
or upgrade with:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

On Fedora:

```bash
sudo dnf install python3 python3-pip
```

### Windows

1. Go to <https://www.python.org/downloads/windows/> and download the latest
   Python 3.11+ installer.
2. **Important:** check the box that says *"Add python.exe to PATH"* before
   clicking *Install Now*. This makes `python` work from any terminal.

## Verifying Your Install

Open a terminal (Terminal on macOS, your favorite terminal emulator on
Linux, or PowerShell/Windows Terminal on Windows) and type:

```bash
python --version
```

You should see something like:

```text
Python 3.12.3
```

On some systems Python 3 is named `python3` instead of `python`:

```bash
python3 --version
```

If neither works, the installer probably didn't add Python to your `PATH`.
Re-run the installer and double-check the option, or follow the official
guide at <https://docs.python.org/3/using/index.html>.

## The Python REPL

A **REPL** stands for *Read–Eval–Print Loop*. It reads what you type,
evaluates it, prints the result, and loops back to read again. Start the
REPL by typing `python` (or `python3`) with no filename:

```bash
python
```

You'll see something like this:

```text
Python 3.12.3 (main, Apr  9 2024, 18:00:00) [Clang 14.0.0] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

The `>>>` is the **prompt** — Python is waiting for you to type. Try it:

```python
>>> 1 + 1
2
>>> print("Hello from the REPL")
Hello from the REPL
>>> name = "Ada"
>>> name
'Ada'
```

The REPL is your laboratory. Use it any time you want to check what a piece
of code does without committing it to a file. To exit, type `exit()` or
press **Ctrl+D** (macOS/Linux) or **Ctrl+Z** then Enter (Windows).

## Running a Python Script

Once your snippets get longer than a few lines, you'll want to save them in
a file and run them as a **script**. By convention, Python files end in
`.py`. Create a file called `hello.py` containing:

```python
# hello.py — our first Python script
print("Hello, world!")
```

Run it from the terminal:

```bash
python hello.py
```

You should see:

```text
Hello, world!
```

That's it. You have written and executed your first Python program.

## Interactive Mode vs Script Mode

The two modes you've now seen — REPL (also called *interactive mode*) and
script mode — differ in three important ways:

1. **Where the code lives.** REPL code lives only in memory. Script code
   lives in a file you can re-run or share.
2. **How output works.** In the REPL, typing an expression like `1 + 1`
   automatically prints `2`. In a script, *you must call* `print()` to see
   anything.
3. **What's left over.** When the REPL exits, all your variables are gone.
   When a script ends, the variables are gone too — but the file is still
   there for next time.

You can blend the two with `python -i hello.py`, which runs the script then
drops you into a REPL with the script's variables already defined. We'll
practice this in exercise 3.

## Comments and Docstrings

A **comment** is a note for humans that Python ignores. Single-line comments
start with `#`:

```python
# This is a comment. Python will not execute this line.
print("This line runs.")  # Comments can also follow code.
```

A **docstring** is a triple-quoted string that documents what a file,
function, or class does. It looks like a comment but is actually a string
that lives inside your program. Place a *module-level docstring* at the very
top of every `.py` file you write this week:

```python
"""hello.py — print a friendly greeting.

This script demonstrates the simplest possible Python program.
"""

print("Hello, world!")
```

Triple-quoted strings can span multiple lines, which makes them perfect for
multi-paragraph documentation. Read the official guidance on docstrings in
PEP 257 (<https://peps.python.org/pep-0257/>).

## The `print()` Function

`print()` is a **builtin function** — it's available everywhere without
needing to be imported. Its basic job is to send a string to standard
output. A few useful tricks:

```python
# Multiple arguments are joined by spaces.
print("Hello,", "world!")        # -> Hello, world!

# Change the separator with sep=.
print("a", "b", "c", sep="-")    # -> a-b-c

# Change the line ending with end=.
print("no newline here", end="")
print(" and continued on same line")  # -> no newline here and continued on same line
```

The full documentation lives at
<https://docs.python.org/3/library/functions.html#print>.

## Useful Invocations: `python -c` and `python -m`

Two flags will make your life easier:

- **`python -c "..."`** runs a tiny one-line program directly from the
  terminal, no file required. Great for quick checks:

  ```bash
  python -c "print(2 ** 10)"
  ```

- **`python -m module_name`** runs a module as a script. You'll use this all
  the time. For example, `python -m venv .venv` runs the `venv` module to
  create a virtual environment, and `python -m pip install requests` is the
  safest way to invoke pip.

## A Slightly Larger First Program

Let's combine everything. Save the following as `greet.py`:

```python
"""greet.py — greet the user by name."""


def greet(name: str) -> str:
    """Return a friendly greeting for ``name``."""
    return f"Hello, {name}! Welcome to Code Crunch Convos."


if __name__ == "__main__":
    user_name: str = input("What is your name? ")
    print(greet(user_name))
```

Run it:

```bash
python greet.py
```

You'll be prompted for your name, then Python will print a personalized
greeting. Don't worry about the `def`, `f"..."`, or `if __name__ ==
"__main__":` syntax yet — we'll cover them in detail in weeks 2 and 4. The
important takeaway is that this is a complete, runnable program, and you
just wrote it.

## Common First-Day Errors

A few errors trip up nearly everyone on day one. None of them are bugs in
Python — they're all easy fixes.

- **`SyntaxError: invalid syntax`** usually means a typo: a missing
  parenthesis, a stray comma, or `Print` (with a capital P — Python is
  case-sensitive; use lowercase `print`).
- **`NameError: name 'foo' is not defined`** means you tried to use a
  variable that hasn't been created yet. Check your spelling.
- **`IndentationError`** means your whitespace is inconsistent. Python uses
  indentation to group code. Pick four spaces and stick with it.
- **`python: command not found`** means Python isn't on your `PATH`. Try
  `python3` instead, or re-install with the *Add to PATH* option checked.

## Recap

You now know:

- What Python is and where it came from.
- How to install Python 3.11+ on macOS, Linux, and Windows.
- The difference between the REPL (interactive) and running a `.py` script.
- How to write single-line comments and module docstrings.
- How `print()` works and a couple of its handy keyword arguments.
- Two power-flags: `python -c` and `python -m`.

Head to exercises 1–3 to put it all into practice, then come back for
Lecture 2, where we'll explore the terminal and virtual environments.
