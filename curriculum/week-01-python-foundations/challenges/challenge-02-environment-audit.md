# Challenge 2 — Environment Audit

> **Topic:** virtual environments, `sys`, `platform`, and installed packages
> **Lecture:** [02 — Terminal, Virtual Environments and pip](../lecture-notes/02-terminal-virtual-environments-and-pip.md)
> **Difficulty:** starter to work, and the answer teaches you something about your own machine
> **Target time:** 30–60 minutes
> **Why this one:** almost every confusing Python problem in your first year is really "which Python am I running", and this script answers that question out loud.

<!-- no-runnable-file: the audit reports on the machine and environment it runs in, so its output differs on every machine and cannot be pinned to one fixed block. challenge-02-environment-audit.py ships beside this page and runs as downloaded; only the automatic output comparison is skipped. -->

## The Brief

Imagine handing someone a recipe. They cook it and it comes out wrong. Was it
the recipe, or was it their oven?

Software has the same problem. Your code works on your laptop, then it fails
on a classmate's, and the first honest question is: *are we even running the
same Python?* Most of the time the answer is no. There is one Python that
came with the operating system, another you installed yourself, and a third
sitting inside a project's `.venv` folder. They have different versions and
different packages, and the one you *think* you are running is often not the
one you are running.

You are going to write `audit.py`, a small script that prints a plain report
about the Python running it: which version, which interpreter file, where it
was launched from, whether it is inside a virtual environment, and every
package installed in it.

When your code misbehaves next month, this is the first thing you run.

## Starter

Save this as `audit.py`. It runs as pasted and prints the first four lines of
the report. The rest is yours.

```python
"""audit.py -- print a summary of the current Python environment."""

import platform
import sys

RULE_WIDTH: int = 58


def is_in_virtualenv() -> bool:
    """Return True when running inside a venv."""
    # TODO 1: compare sys.prefix with sys.base_prefix.
    return False


def installed_packages() -> list[tuple[str, str]]:
    """Return (name, version) pairs for every installed distribution."""
    # TODO 2: walk importlib.metadata.distributions() and collect the
    #         name and version of each one, sorted, with no duplicates.
    return []


def main() -> None:
    """Print the whole audit to standard output."""
    print("=" * RULE_WIDTH)
    print(" Python Environment Audit")
    print("=" * RULE_WIDTH)
    print(f"Python version : {platform.python_version()}")
    print(f"Implementation : {platform.python_implementation()}")
    print(f"Platform       : {platform.platform()}")
    print(f"Executable     : {sys.executable}")
    # TODO 3: print the working directory and the venv flag.
    # TODO 4: print the package list, name column padded so versions line up.
    print("=" * RULE_WIDTH)


if __name__ == "__main__":
    main()
```

## Requirements

The report must contain, in this order:

1. The Python version, as three numbers — `3.13.2`, not the long banner
   string.
2. The implementation name. Almost always `CPython`.
3. A platform string: operating system and architecture.
4. The full path of the interpreter that is running the script.
5. The directory the script was launched from.
6. `Inside venv : yes` or `Inside venv : no`.
7. A count of installed packages, then one line per package with its version.

And in the code:

8. A module-level docstring, and a docstring on every function.
9. Type hints on every parameter and every return.
10. `sys` and `platform` from the standard library. Nothing installed.
11. The package list comes from `importlib.metadata.distributions()`.
12. An `if __name__ == "__main__":` guard around `main()`.

## Constraints

- **Detect the venv by comparing `sys.prefix` with `sys.base_prefix`, not by
  reading the `VIRTUAL_ENV` environment variable.** `VIRTUAL_ENV` is set by
  the *activation* script. Run `.venv/bin/python audit.py` without activating
  and the variable is missing, even though you are unmistakably running the
  environment's Python. The prefixes come from the interpreter itself, so they
  are always right.
- **`importlib.metadata`, not a `pip` subprocess.** It reads the same records
  pip wrote, in the interpreter that is running right now. No second process
  to start, no risk of asking a different Python, and it works even where pip
  is not installed. The `pip` version is shown under *Under the hood* so you
  can see the trade.
- **The rule width lives in one constant.** `print("=" * 58)` typed three
  times is how you end up widening the top rule and forgetting the bottom.
- **Standard library only.** A tool for diagnosing a broken environment must
  not need anything installed into that environment.
- **No fixed expected output, and that is the point.** Every line the script
  prints is a fact about the machine it ran on. Two people running the same
  file correctly will see different reports. See *Expected output*.

## Expected output

This script has no single correct output, because its whole job is to
describe the computer it is running on. Your version numbers, your paths and
your package list will not match anyone else's — and if they did, the script
would be lying.

So read the block below as a **shape**, not as a target. Only the words on the
left of each colon are fixed. Everything on the right is that machine's own
answer.

This is a real run, captured on CPython 3.13.2 on Windows 11, inside a fresh
virtual environment with `requests` installed into it. The long temporary
folder path is shortened to `C:\...\audittest` for readability; nothing else
is edited.

```text
$ python audit.py
==========================================================
 Python Environment Audit
==========================================================
Python version : 3.13.2
Implementation : CPython
Platform       : Windows-11-10.0.26200-SP0
Executable     : C:\...\audittest\.venv\Scripts\python.exe
Working dir    : C:\...\audittest
Inside venv    : yes

Installed packages (6):
  - certifi             2026.7.22
  - charset-normalizer  3.5.1
  - idna                3.19
  - pip                 26.2.1
  - requests            2.34.2
  - urllib3             2.7.0
==========================================================
```

What is fixed, line by line:

| Line | Fixed on every machine | Varies on every machine |
|---|---|---|
| The two `=` rules | 58 characters wide | nothing |
| The title | `Python Environment Audit` | nothing |
| The six labels | the wording and the column of colons | nothing |
| `Python version` | — | `3.13.2` here, whatever you installed for you |
| `Implementation` | `CPython` for nearly everyone | `PyPy`, `GraalPy` on other runtimes |
| `Platform` | — | your operating system and chip |
| `Executable` | — | where your interpreter file lives |
| `Working dir` | — | where you were standing when you ran it |
| `Inside venv` | `yes` or `no`, nothing else | which of the two |
| `Installed packages (N)` | the wording and the count in brackets | `N`, and every line under it |

That last row is the one worth staring at. This run asked for exactly one
package, `requests`, and got six. Five of them are `requests` and its
dependencies, plus `pip` itself. Ask for one thing, receive six — and that is
in a *clean* environment. Run the same script against a system Python that has
been collecting packages for two years and the list runs to hundreds. Seeing
both numbers is the entire argument for virtual environments, delivered in one
screen.

## Steps

1. Save the starter as `audit.py`. Run `python audit.py`. Four lines of report
   between two rules.
2. Fill in **TODO 1**. One line: `return sys.prefix != sys.base_prefix`.
3. Fill in **TODO 3**. `os.getcwd()` gives the working directory, so add
   `import os` at the top with the others. For the flag, a conditional
   expression reads well inside the f-string:
   `{'yes' if is_in_virtualenv() else 'no'}`.
4. Run it from a plain terminal. `Inside venv` should say `no`.
5. Make an environment and run it again. This is the test that matters:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install requests
   python audit.py
   ```

   On Windows PowerShell the activate line is `.venv\Scripts\Activate.ps1`.
   Now `Inside venv` should say `yes`, and `Executable` should point inside
   `.venv`. If both runs say the same thing, your check is broken — that is
   why you run it twice.
6. Fill in **TODO 2**. Add `from importlib.metadata import distributions`.
   Loop over `distributions()`, read `dist.metadata["Name"]` and
   `dist.version`, keep them in a dictionary so a package reachable from two
   places is not listed twice, and return the pairs sorted.
7. Fill in **TODO 4**. Find the longest name with
   `max(len(name) for name, _ in packages)`, then `name.ljust(width)` so the
   version column lines up. Handle the empty list, or `max()` raises
   `ValueError: max() iterable argument is empty`.
8. Commit it:

   ```bash
   git add audit.py
   git commit -m "Add Challenge 2: environment audit script"
   ```

## The Solution

```python
"""audit.py -- print a summary of the current Python environment.

Challenge 2, Week 1, Code Crunch Convos. Reports the interpreter version,
implementation, platform, executable path, working directory, whether we
are inside a virtual environment, and every installed distribution.

Every line this prints describes the machine and the environment it ran
in, so two people never see the same report.

Run it with::

    python audit.py
"""

import os
import platform
import sys
from importlib.metadata import distributions

RULE_WIDTH: int = 58


def is_in_virtualenv() -> bool:
    """Return True when running inside a venv.

    Returns:
        True when ``sys.prefix`` and ``sys.base_prefix`` differ, which is
        the interpreter's own record of being inside an environment.
    """
    return sys.prefix != sys.base_prefix


def installed_packages() -> list[tuple[str, str]]:
    """Return ``(name, version)`` pairs for every installed distribution.

    Returns:
        One pair per distribution, sorted by name, case-insensitively.
        Duplicates reachable from two places on ``sys.path`` appear once.
    """
    found: dict[str, str] = {}
    for dist in distributions():
        name: str = dist.metadata["Name"] or ""
        if name and name not in found:
            found[name] = dist.version
    return sorted(found.items(), key=lambda pair: pair[0].lower())


def main() -> None:
    """Print the whole audit to standard output."""
    print("=" * RULE_WIDTH)
    print(" Python Environment Audit")
    print("=" * RULE_WIDTH)
    print(f"Python version : {platform.python_version()}")
    print(f"Implementation : {platform.python_implementation()}")
    print(f"Platform       : {platform.platform()}")
    print(f"Executable     : {sys.executable}")
    print(f"Working dir    : {os.getcwd()}")
    print(f"Inside venv    : {'yes' if is_in_virtualenv() else 'no'}")

    packages: list[tuple[str, str]] = installed_packages()
    print()
    print(f"Installed packages ({len(packages)}):")
    if not packages:
        print("  (none)")
    else:
        width: int = max(len(name) for name, _ in packages)
        for name, version in packages:
            print(f"  - {name.ljust(width)}  {version}")
    print("=" * RULE_WIDTH)


if __name__ == "__main__":
    main()
```

**`sys.prefix != sys.base_prefix` is the whole venv check.** Think of two
addresses. `sys.base_prefix` is the address of the Python you *installed* —
the one from python.org, or Homebrew, or your package manager.
`sys.prefix` is the address of the environment you are *standing in* right
now. Outside a virtual environment those two addresses are the same folder.
Inside one, `sys.prefix` points at your `.venv` and `base_prefix` still points
at the installation. Different addresses, so you are in an environment. On the
machine that produced the transcript above:

```text
C:\...\audittest\.venv
C:\Users\Telsa\AppData\Local\Programs\Python\Python313
```

**`platform.python_version()` gives you the three numbers and nothing else.**
The other obvious candidate, `sys.version`, is a chatty string built for a
startup banner: `'3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, ...) [MSC ...]'`.
Requirement 1 asks for `3.13.2`. If you want the parts as numbers for a
comparison, `sys.version_info` is a tuple you can compare directly:
`sys.version_info >= (3, 11)` is the normal way to write a version gate.

**`distributions()` reads what pip left behind.** Every time pip installs
something it drops a small folder next to the package called
`something.dist-info`, and inside it a `METADATA` file with the name and
version. `distributions()` walks the folders Python searches for imports and
hands you one object per record. So it is reporting on the interpreter running
right now, with nothing else to go wrong.

**The dictionary is there to remove duplicates.** If the same package is
reachable from two of the folders Python searches, you would otherwise print
it twice. `if name and name not in found` keeps the first one seen and skips
the rest.

**`dist.metadata["Name"] or ""` guards a real edge case.** A half-deleted
`dist-info` folder produces a record whose `Name` is `None`. Without the
guard, `sorted()` later raises
`TypeError: '<' not supported between instances of 'NoneType' and 'str'`.
Turning it into an empty string and then skipping empty names sidesteps it.

**`key=lambda pair: pair[0].lower()` sorts the way a human reads.** Plain
`sorted()` compares strings by character code, and every capital letter comes
before every lowercase one, so `Pygments` would land before `certifi`.
Lowercasing inside the sort key fixes the order. Note that it lowercases only
for the *comparison* — the printed name keeps its real capitals.

**`ljust(width)` where `width` is the longest name.** That is why the version
column lines up. Hard-code `ljust(15)` and it works until somebody installs
`charset-normalizer`, which is eighteen characters, and the column breaks.
Measure the data, then format to the measurement.

## Download and run

Download [challenge-02-environment-audit-solution.py](./challenge-02-environment-audit-solution.py) and run it:

```bash
python challenge-02-environment-audit-solution.py
```

Run it twice, and compare. Once from a plain terminal, and once from inside an
activated virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python challenge-02-environment-audit-solution.py
```

The `Executable`, `Inside venv` and package lines should all change. If they
do not, you did not activate.

In your own project, save the same code as `audit.py`.

## Common bugs to catch

**`NameError: name 'os' is not defined`.** You added the working-directory
line and forgot the import. On CPython 3.13.2:

```text
Traceback (most recent call last):
  File "audit.py", line 15, in <module>
    main()
    ~~~~^^
  File "audit.py", line 11, in main
    print(f"Working dir    : {os.getcwd()}")
                              ^^
NameError: name 'os' is not defined. Did you forget to import 'os'?
```

Python 3.13 even guesses the fix for you. Add `import os` at the top, in
alphabetical order with the other imports. Notice the `~~~~^^` markers under
the call: those are fine-grained error locations, added in 3.11, pointing at
the exact piece of the line that failed.

**`ValueError: max() iterable argument is empty`.** Your package list came
back empty and `max(len(name) for name, _ in packages)` had nothing to
measure. It happens in a `--without-pip` environment. The `if not packages:`
branch is not decoration.

**The report says `no` while you are clearly inside the environment.** You
used `os.environ.get("VIRTUAL_ENV")` instead of comparing the prefixes. That
variable is set by the activation script, so running `.venv/bin/python
audit.py` directly leaves it unset. Some shells also leave it behind, stale,
after `deactivate`, which gives you the opposite lie.

**The package list belongs to a different Python.** You shelled out with
`subprocess.run(["pip", "list"], ...)` — bare `pip`, no `-m`. That runs
whichever `pip` your `PATH` finds first, which on a machine with several
Pythons is regularly not the one executing your script. You get a confident,
neatly formatted, wrong answer. Use `sys.executable`, which is by definition
the interpreter running right now.

**Reporting `sys.path[0]` as the working directory.** It is not the same
thing. `sys.path[0]` is the folder the script lives in. `os.getcwd()` is the
folder your terminal was in when you pressed Enter. Run
`python subdir/audit.py` from a project root and the two differ.

**The bottom rule is a different length from the top.** You typed `58` in
three places and changed two of them. That is what `RULE_WIDTH` prevents.

## Under the hood

<details>
<summary>Under the hood — what a virtual environment actually is, and how it redirects your imports</summary>

A virtual environment sounds like a sandbox or a container. It is neither. It
is a folder with a copy of the `python` launcher in it and a two-line
configuration file, and the entire trick is that the interpreter reads that
file at startup and changes where it looks for packages.

**The file that does it.** `python -m venv .venv` writes `.venv/pyvenv.cfg`.
Here is a real one:

```text
home = C:\Users\Telsa\AppData\Local\Programs\Python\Python313
include-system-site-packages = false
version = 3.13.2
executable = C:\Users\Telsa\AppData\Local\Programs\Python\Python313\python.exe
command = C:\...\Python313\python.exe -m venv C:\...\audittest\.venv
```

When you launch `.venv/Scripts/python.exe`, the interpreter looks beside
itself, finds `pyvenv.cfg`, and reads it. `home` tells it where the real
installation is, so it can find the standard library. Then it sets
`sys.prefix` to the environment folder and `sys.base_prefix` to `home`. That
is where the check in `is_in_virtualenv` gets its two values. They are not
guesses — they are written down at startup by the interpreter itself.

**What `sys.executable` really tells you.** It is the path of the running
interpreter file, as the operating system resolved it. It is the answer to
"which Python is this, actually" — not "which Python did I type", and not
"which Python does `PATH` prefer". Those three can all be different, and when
they are, `sys.executable` is the one telling the truth. This is why
`[sys.executable, "-m", "pip", "list"]` is strictly better than
`["pip", "list"]`: it asks the interpreter you are inside, not the one the
shell happens to find.

**How imports get redirected.** Python searches a list of folders, in order,
held in `sys.path`. Compare the two lists on the same machine.

Outside the environment:

```text
C:\...\Python313\python313.zip
C:\...\Python313\DLLs
C:\...\Python313\Lib
C:\...\Python313
C:\...\Python313\Lib\site-packages
```

Inside it:

```text
C:\...\Python313\python313.zip
C:\...\Python313\DLLs
C:\...\Python313\Lib
C:\...\Python313
C:\...\audittest\.venv\Lib\site-packages
```

The first four entries are identical: that is the standard library, shared,
not copied. Only the last entry changed. `site-packages` is the folder that
installed packages land in, and the environment simply substitutes its own.
That single swap is the whole isolation mechanism. Nothing is sandboxed,
nothing is virtualised — Python is just looking somewhere else.

`include-system-site-packages = false` in the config is what keeps the
installation's `site-packages` off the list. Create the environment with
`--system-site-packages` and it says `true`, both folders are searched, and
your isolation is partial by design.

**Why the environment is disposable, and why you never commit it.** Everything
in `.venv` is either a copy of something you already have or something pip can
fetch again. It also records absolute paths, so moving or renaming the folder
breaks it. Delete it, recreate it, reinstall from `requirements.txt`. That
takes seconds and is the normal fix for a confusing environment. Since Python
3.11 the environment even ignores itself: `python -m venv` writes a
`.gitignore` containing `*` inside `.venv`, so Git will not offer to track it
even if your own `.gitignore` forgets to.

</details>

<details>
<summary>Under the hood — asking pip instead, and why this answer does not</summary>

The other reasonable way to list packages is to run pip and read what it
prints:

```python
"""subproc_variant.py -- listing packages by asking pip."""

import subprocess
import sys


def pip_list() -> str:
    """Return the output of ``pip list`` for the *running* interpreter."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.rstrip()


if __name__ == "__main__":
    print(pip_list())
```

In the same environment that produced the transcript above:

```text
Package            Version
------------------ ---------
certifi            2026.7.22
charset-normalizer 3.5.1
idna               3.19
pip                26.2.1
requests           2.34.2
urllib3            2.7.0
```

Three arguments to `subprocess.run` are doing real work.
`capture_output=True` collects the child's output instead of letting it spill
into your terminal. `text=True` decodes the raw bytes into a `str` so you do
not have to. `check=True` raises `subprocess.CalledProcessError` when the
child exits with a failure code, instead of quietly handing you an empty
string — a silent failure is the worst kind.

And `sys.executable` rather than the literal `"python"`, for the reason in the
other block: `"python"` is resolved through `PATH`, and auditing the wrong
interpreter is precisely the failure this script exists to catch.

`importlib.metadata` is still the better default here. It starts no second
process, so it is roughly a hundred times faster; it does not require pip to
exist; and it gives you structured data instead of a table you would have to
take apart again. Reach for the subprocess when what you actually want is
pip's own formatting, verbatim.

</details>

## Acceptance checklist

- [ ] The script runs and prints all seven required facts.
- [ ] Run from a plain terminal, `Inside venv` says `no`.
- [ ] Run from inside an activated environment, `Inside venv` says `yes` and
      `Executable` points inside `.venv`.
- [ ] The two `=` rules are the same length as each other.
- [ ] The version column lines up even when one package name is much longer
      than the rest.
- [ ] The package count in brackets matches the number of lines below it.
- [ ] Type hints on every parameter and every return.
- [ ] A module docstring and a docstring on every function.
- [ ] No third-party import anywhere in the file.
- [ ] Committed with a clear message such as
      `Add Challenge 2: environment audit script`.

## Stretch

**Print the report as JSON.** Accept `--json` on the command line and print
machine-readable output instead. The move that makes this easy is splitting
*collecting* the facts from *rendering* them: a `collect()` function that
returns a plain dictionary, then either `json.dumps(data, indent=2)` or a
`render_text(data)`. Add a third format later and you write one more renderer,
not one more copy of the gathering code.

Store the truth and format at the edge: keep `inside_venv` as a real `True` or
`False` in the dictionary, and let only the text renderer turn it into `yes`
or `no`. JSON consumers want the boolean; humans want the word. And use
`json.dumps`, not `print(data)` — printing a dictionary gives you Python's own
notation, with single quotes and a bare `True`, which no JSON parser will
accept.

**Colour the venv flag.** Green for `yes`, red for `no`, via `colorama`. Put
the import in a `try` / `except ImportError` so the file still runs without
it.

**Write the report to a file.** Accept `--output report.txt`. Suppress the
colour when the destination is a file — escape codes are invisible in a
terminal and ugly in an editor, where they show up as `←[32myes←[0m`.

**Compare two environments.** Run the audit in your system Python and again
inside a fresh `.venv`, save both with `--output`, and `diff` them. The
difference is exactly what the environment is buying you.

**Explain a surprise.** Pick any package in your list that you never asked
for, and find out who pulled it in:

```bash
python -m pip show requests
```

The `Requires` line names its dependencies. Follow the chain until every
package in your report has a reason to be there.
