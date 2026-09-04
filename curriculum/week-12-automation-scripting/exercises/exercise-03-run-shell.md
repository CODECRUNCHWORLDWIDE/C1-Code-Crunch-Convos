# Exercise 3 — Run Shell

> **Topic:** `subprocess.run` with an argument list, capturing and parsing output
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Medium
> **Target time:** 25 min
> **Why this one:** the moment you can call other programs from Python, every CLI on your machine becomes a library. That is a large amount of power to hand a script, and the way you hand it over decides whether the script is a tool or a hole in your system. This exercise teaches the safe call shape and shows you the attack that motivates it, on a command you run yourself.

## The Brief

You are writing a **toolbox doctor**: a script that reports which command-line
tools are installed on this machine and at what version. Onboarding a new
member to the org, you run it once and know whether their laptop is ready.

For each tool the script runs that tool's own version command, captures the
output, digs the version number out of it, and prints a row. Tools that are
not installed get a row too — a missing tool is information, not a crash.

Three things make this harder than it looks. Some tools print their version to
stderr instead of stdout. Some exit non-zero even when they answer. And the
list of tools comes partly from the user, which means user input is about to
become a program name.

### Why you pass a list and never `shell=True`

Suppose you built the command as a string and let the shell run it:

```python
# Never do this.
subprocess.run(f"{name} --version", shell=True)
```

Now someone runs your doctor with `--tool "git; rm -rf ~"`. The shell sees a
semicolon, splits the line into two commands, checks git's version, and then
deletes the caller's home directory. Nothing in your Python is wrong. The
shell simply did what a shell does.

With a list, `subprocess.run(["git; rm -rf ~", "--version"])` asks the
operating system to execute a program whose **name** is the string
`git; rm -rf ~`. No such program exists, you get `FileNotFoundError`, and your
script prints `not installed`. The semicolon never means anything, because no
shell was ever involved.

That is the whole rule: **a list of arguments, and `shell=False`, which is the
default.** The shipped answer runs the attack against itself so you can see it
do nothing.

## Starter

```python
"""exercise-03-run-shell.py — report which CLI tools are installed.

Runs each tool's version command, parses the version number out of the
output, and prints one row per tool.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

VERSION_RE = re.compile(r"\d+(?:\.\d+)+")
ROW = "{name:<12}  {version:<8}  {status}"


def default_tools() -> list[tuple[str, list[str]]]:
    """Return (label, argv) pairs for the tools checked by default."""
    return [
        ("python", [sys.executable, "-V"]),
        ("pip", [sys.executable, "-m", "pip", "--version"]),
        ("git", ["git", "--version"]),
    ]


def probe(argv: list[str], timeout: float) -> str | None:
    """Run argv and return the first version number in its output.

    Returns None if the program is missing, times out, or prints nothing
    that looks like a version.
    """
    # TODO: subprocess.run(argv, capture_output=True, text=True,
    #                      timeout=timeout, check=False)
    # TODO: search VERSION_RE in result.stdout + result.stderr
    # TODO: catch FileNotFoundError and subprocess.TimeoutExpired, return None
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Probe every tool, print the table, return an exit code."""
    parser = argparse.ArgumentParser(
        prog="toolbox-doctor",
        description="Report installed command-line tools and their versions.",
    )
    parser.add_argument("--tool", action="append", default=[], metavar="NAME",
                        help="Extra tool to check, run as `NAME --version`. Repeatable.")
    parser.add_argument("--timeout", type=float, default=10.0,
                        help="Seconds to wait for each tool (default: %(default)s)")
    args = parser.parse_args(argv)

    tools = default_tools()
    # TODO: extend tools with (name, [name, "--version"]) for each args.tool

    print(ROW.format(name="TOOL", version="VERSION", status="STATUS"))
    found = 0
    # TODO: for each tool, call probe(), print a row, count the hits

    print()
    print(f"{found} of {len(tools)} tools available")
    return 0 if found == len(tools) else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. One header row, then one row per tool, in the order the tools were listed —
   defaults first, then `--tool` entries in the order given.
2. A tool that answers shows its version and the status `ok`. A tool that
   cannot be found, times out, or prints nothing version-shaped shows `-` and
   the status `not installed`.
3. Search **both** streams for the version. Combine `result.stdout` and
   `result.stderr` before running the pattern.
4. A blank line, then `N of M tools available`.
5. Exit 0 when every tool was found, 1 when any was missing.
6. Never construct a shell command string. Every call is a list.

## Constraints

- **Pass `check=False` here, deliberately.** Lecture 2 §3.1 recommends
  `check=True` and it is the right default in general — but this script's job
  is to *report* failure, not abort on it. A tool that exits 3 while printing
  a perfectly good version is still installed. `check=True` would raise
  `CalledProcessError` and throw that information away.
- **Always pass `timeout=`.** A tool waiting on a network mount or a stuck
  credential prompt hangs forever, and your doctor hangs with it. Ten seconds
  is generous for a version flag.
- **Use `sys.executable`, not the literal string `"python"`.** Inside a
  virtual environment `python` may resolve to a different interpreter than the
  one running your script. `sys.executable` is the absolute path to *this*
  Python, so the row you print describes the environment you are in.
- **Catch `FileNotFoundError` around the `run` call, not the whole loop.**
  Wrap the loop and one missing tool ends the report; wrap the call and a
  missing tool is one row.
- **`text=True` with `capture_output=True`.** Without it you get `bytes`, and
  a `str` pattern against `bytes` raises `TypeError: cannot use a string
  pattern on a bytes-like object`.
- **Do not trim or sanitize the user's `--tool` value.** Scrubbing punctuation
  is the fragile way to be safe. Not invoking a shell is the reliable way.

## Expected output

The shipped answer, [`exercise-03-run-shell-solution.py`](./exercise-03-run-shell-solution.py),
drives `main()` with the three default tools, one that is not installed, and the
injection string from the brief, then confirms the file contains no `shell=True`
anywhere. Your version numbers will differ; the shape is what matters. Real
captured output on this machine:

```text
$ python exercise-03-run-shell.py
Run Shell — the toolbox doctor, driven headless.
Your version numbers will differ; the shape is what matters.

TOOL          VERSION   STATUS
python        3.13.2    ok
pip           26.0.1    ok
git           2.49.0    ok
nosuchtool    -         not installed
echo hi & echo pwned  -         not installed

3 of 5 tools available
[exit 1]

Every call passed a list of arguments, so no shell was ever spawned.
The injection string became one program name, which does not exist, so
neither 'hi' nor 'pwned' ran. The safe path is also the default path.
searching this file for shell=True finds: 0
```

Neither `hi` nor `pwned` appears anywhere in that table. The whole injection
string was treated as one program name, and there is no program by that name.

## Steps

1. Paste the starter and implement `probe`. Start with the happy path only.
2. Fill in the loop in `main()` and run it with no arguments. You should get
   three rows.
3. Break one on purpose: `--tool nosuchtool`. If you get a traceback instead of
   a row, your `except FileNotFoundError` is in the wrong place.
4. Check `--timeout 0.001`. Every tool should come back `not installed`,
   because `TimeoutExpired` and "missing" are the same outcome from the
   caller's point of view. If that distinction matters to you, add a third
   status.
5. Run the injection attempt exactly as written above:
   `python exercise-03-run-shell.py --tool "echo hi; echo pwned"`. Confirm no
   echo output appears. If you want to see the contrast, put
   `subprocess.run("echo hi; echo pwned --version", shell=True)` in a scratch
   file — never in this script — watch what happens, then delete it. Read the
   Under the hood note first: on Windows that particular string does *not*
   demonstrate the attack, and knowing why is half the lesson.

## The Solution

The shipped file is your answer — `default_tools`, `probe`, `main` — with a
`demo()` that runs the table and the injection string. Your own file stops at
`raise SystemExit(main())` and reads `--tool` from the shell.

```python
"""exercise-03-run-shell-solution.py — the toolbox doctor, proven headless.

The exercise part is the starter with its TODOs filled in: run each tool's
version command with a *list* of arguments, dig the version number out of
either output stream, and print one row per tool — a missing tool is a row, not
a crash.

Your own exercise-03-run-shell.py ends in ``raise SystemExit(main())`` and is
run from the shell: ``python exercise-03-run-shell.py --tool ...``. This file
drives ``main()`` with a fixed argv list — the three default tools, one that is
not installed, and the injection string from the exercise page — so it prints a
table you can check without typing anything. The probe being tested is
identical either way.

Run it with::

    python exercise-03-run-shell-solution.py
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

VERSION_RE = re.compile(r"\d+(?:\.\d+)+")
ROW = "{name:<12}  {version:<8}  {status}"


def default_tools() -> list[tuple[str, list[str]]]:
    """Return (label, argv) pairs for the tools checked by default."""
    return [
        ("python", [sys.executable, "-V"]),
        ("pip", [sys.executable, "-m", "pip", "--version"]),
        ("git", ["git", "--version"]),
    ]


def probe(argv: list[str], timeout: float) -> str | None:
    """Run argv and return the first version number in its output.

    Returns None if the program is missing, times out, or prints nothing
    that looks like a version.
    """
    try:
        result = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, PermissionError, subprocess.TimeoutExpired):
        return None

    match = VERSION_RE.search(result.stdout + result.stderr)
    return match.group(0) if match else None


def main(argv: list[str] | None = None) -> int:
    """Probe every tool, print the table, return an exit code."""
    parser = argparse.ArgumentParser(
        prog="toolbox-doctor",
        description="Report installed command-line tools and their versions.",
    )
    parser.add_argument("--tool", action="append", default=[], metavar="NAME",
                        help="Extra tool to check, run as `NAME --version`. Repeatable.")
    parser.add_argument("--timeout", type=float, default=10.0,
                        help="Seconds to wait for each tool (default: %(default)s)")
    args = parser.parse_args(argv)

    tools = default_tools()
    tools.extend((name, [name, "--version"]) for name in args.tool)

    print(ROW.format(name="TOOL", version="VERSION", status="STATUS"))
    found = 0
    for label, command in tools:
        version = probe(command, args.timeout)
        if version is None:
            print(ROW.format(name=label, version="-", status="not installed"))
        else:
            found += 1
            print(ROW.format(name=label, version=version, status="ok"))

    print()
    print(f"{found} of {len(tools)} tools available")
    return 0 if found == len(tools) else 1


# --------------------------------------------------------------------------- #
# The headless demo — the default tools, a missing one, and the injection
# string from the exercise page. Your own file has no demo; it reads --tool
# from the shell.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Drive the doctor and show the injection string is inert."""
    print("Run Shell — the toolbox doctor, driven headless.")
    print("Your version numbers will differ; the shape is what matters.")
    print()
    code = main(["--tool", "nosuchtool", "--tool", "echo hi & echo pwned"])
    print(f"[exit {code}]")
    print()
    print("Every call passed a list of arguments, so no shell was ever spawned.")
    print("The injection string became one program name, which does not exist, so")
    print("neither 'hi' nor 'pwned' ran. The safe path is also the default path.")
    needle = "shell=" + "True"
    count = Path(__file__).read_text(encoding="utf-8").count(needle)
    print(f"searching this file for {needle} finds: {count}")


if __name__ == "__main__":
    demo()
```

**A list of arguments means no shell exists to be injected into.**
`subprocess.run(["git; rm -rf ~", "--version"])` asks the operating system to
start a program whose *filename* is the eleven-character string
`git; rm -rf ~`. There is no such file, so the call raises `FileNotFoundError`
and your handler prints `not installed`. The semicolon never means anything
because nothing that understands semicolons was ever invited. `shell=False` is
`subprocess.run`'s default, so the safe path is also the path you get by not
thinking about it.

**The shell metacharacters are not a fixed list you can filter for.** This is
the deeper reason the list beats scrubbing. On Windows, `shell=True` runs your
string through `cmd.exe`, and `cmd.exe` does not treat `;` as a command
separator — it uses `&`. So the classic `echo hi; echo pwned` string prints
one line on Windows and two on a POSIX shell, and you would have to know which
shell was going to see your string to know which characters were dangerous.
`bash`, `zsh`, `sh`, PowerShell and `cmd.exe` all differ, and they differ
between versions. Passing a list needs none of that knowledge, because there is
no shell at the other end.

**`check=False` is a deliberate reversal of the usual advice.** Lecture 2 §3.1
tells you to use `check=True`, and for a script that depends on a command
succeeding, that is right. This script's whole job is to *report* on commands
that fail. A tool that exits 3 while printing a readable version banner is
installed, and `check=True` would raise `CalledProcessError` and throw the
banner away with it.

**Both streams are searched, concatenated.** On this machine `git --version`
writes to stdout; on another machine, or with another tool, it is the other way
round. `result.stdout + result.stderr` means you never have to know which. It
costs one `+` and removes an entire class of "it works on my machine".

**`\d+(?:\.\d+)+` requires at least one dot, and `search` takes the first
match.** `\d+` alone matches the `3` in `3.13.2` and stops. And the first match
is the right one because tools put their own version first and context
afterwards — `pip 24.3.1 from ...\pip (python 3.13)` gives `24.3.1` with
`search`, and the Python version if you take the last match instead.

**`sys.executable`, not `"python"`.** Inside a virtual environment the bare
name `python` may resolve through the `PATH` to a different interpreter than the
one running your script — and on a fresh Windows install there may be no
`python` on the `PATH` at all. `sys.executable` is the absolute path to *this*
Python, and `[sys.executable, "-m", "pip", ...]` is *this* environment's pip.

## Run it

Copy the worked answer on this page into `exercise-03-run-shell.py` and run it:

```bash
python exercise-03-run-shell.py
```

It needs nothing but the standard library and the tools it probes. Because it
is pure stdlib, you can also
[run it in the online editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-12-automation-scripting/exercises/exercise-03-run-shell.md).
The `-solution` in the name keeps it from colliding with your own
`exercise-03-run-shell.py`.

## Common bugs to catch

- **`FileNotFoundError: [Errno 2] No such file or directory: 'nosuchtool'`**
  (or `[WinError 2] The system cannot find the file specified` on Windows).
  You did not wrap the `run` call. This exception is the *only* thing that
  tells you a program is missing, so catching it is the feature, not the
  workaround.
- **`TypeError: cannot use a string pattern on a bytes-like object`.** You
  forgot `text=True`, so `result.stdout` is `b"git version 2.49.0\n"`.
- **`git` reports `-` even though it is installed.** You only searched
  `result.stdout`. Several tools, and older Pythons in particular, write the
  version banner to stderr. Concatenate both streams.
- **`AttributeError: 'NoneType' object has no attribute 'group'`.**
  `re.search` returns `None` when nothing matches. Check the match object
  before calling `.group()` — `match.group(0) if match else None` does it on
  one line.
- **The version comes out as `3` instead of `3.13.2`.** Your pattern was
  `\d+` and it stopped at the first digit run. `\d+(?:\.\d+)+` requires at
  least one dot-separated part.
- **`subprocess.CalledProcessError: Command '[...]' returned non-zero exit
  status 1`.** You left `check=True` in. See the constraint above.
- **The script hangs and never prints the summary.** A tool is waiting for
  input on stdin. You forgot `timeout=`, and `capture_output=True` means you
  cannot even see the prompt it is waiting on.
- **`pip` shows the Python version instead of pip's.** Your pattern found the
  wrong number in `pip 24.3.1 from /path/... (python 3.13)`. Take the **first**
  match, not the last.

## Under the hood

<details>
<summary>Under the hood — what `shell=True` actually does, and why it is a different program</summary>

`subprocess.run(["git", "--version"])` and
`subprocess.run("git --version", shell=True)` look like two spellings of the
same thing. They are not. The first calls the operating system's "run this
program with these exact arguments" primitive directly — on POSIX that is
`execvp`, on Windows `CreateProcess` — handing over an argument *vector* the
kernel never re-parses. The second starts a *shell* (`/bin/sh -c "git
--version"` on POSIX, `cmd.exe /c "git --version"` on Windows) and hands it your
whole string to interpret, and interpreting strings is a shell's entire job:
splitting on whitespace, expanding `$VAR` and `~`, globbing `*.txt`, and running
whatever `;`, `&&`, `|` or backticks it finds.

So the danger of `shell=True` is not a bug you can patch — it is the feature you
asked for. The moment any part of that string came from outside your program, a
user, a filename, a web response, you have handed a stranger the shell's full
grammar. The fix is not to sanitize the string; it is to not create a shell.
The list form has no string for a shell to parse and no shell to parse it. Keep
`shell=True` for the rare case where you genuinely want shell features on a
string you wrote yourself in full, and even then prefer building the pieces
explicitly.

</details>

## Acceptance checklist

- [ ] Three rows with no arguments, all `ok` on a normal dev machine.
- [ ] `--tool nosuchtool` adds a `not installed` row and does not crash.
- [ ] The injection string prints no echo output and no traceback.
- [ ] `--timeout 0.001` degrades to `not installed` rows instead of hanging.
- [ ] Searching the finished file for `shell=True` finds nothing.
- [ ] Exit code is 0 when all tools are present, 1 otherwise.
- [ ] The file is committed to Git with a message like
      `Add Week 12 exercise 3: toolbox doctor with subprocess`.

## Stretch

- Add `--json` that prints the same data as a JSON array, so another script
  can consume it. Lecture 2 §3.2 shows the pattern in reverse.
- Add a `--min` map like `--min git=2.30` and flag rows that are installed but
  older than the floor. Comparing versions correctly is harder than it looks —
  `"2.9" < "2.30"` is `False` as strings and `True` as versions.
- Let each tool carry its own version flag, since not every tool uses
  `--version` (`java -version`, `go version`).

When nothing you type can make the script run a shell, move on to
[Exercise 4 — Scrape Quotes](./exercise-04-scrape-quotes.md).
