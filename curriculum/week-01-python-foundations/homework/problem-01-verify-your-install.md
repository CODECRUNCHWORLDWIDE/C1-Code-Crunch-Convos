# Homework Problem 1 — Verify Your Install

> **Topic:** proving that the word `python` in a terminal reaches a real Python 3.11 or newer
> **Lecture:** [Lecture 1 — Installing Python and Running Your First Program](../lecture-notes/01-installing-python-and-running-your-first-program.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** every other page this week starts with "open a terminal and run `python`". If that one word does not reach the Python you think it reaches, everything after it is confusing for the wrong reason. Prove it once, keep the proof, and never wonder again.

<!-- no-runnable-file: the thing being tested is whether your terminal can find Python at all. A script cannot prove that, because running the script already requires having found it. The evidence is a terminal session and a saved file. -->

## The Brief

You installed Python. Now prove it, the way a scientist proves something:
with evidence you could show to somebody else.

Think of your terminal as a receptionist. You say a name — `python` — and
the receptionist goes and fetches whoever is registered under that name. A
computer can easily have three different Pythons registered, in three
different folders, installed at three different times. The receptionist
only ever fetches one of them, and it is not always the one you meant.

So you are going to ask two questions in a freshly opened terminal:

1. Does anybody answer to the name `python`?
2. If so, which one is it, and is it new enough for this course?

Then you save the answer into a file called `notes/install-check.txt`, so
the proof survives after the terminal window closes.

**Fresh terminal matters.** An installer changes the list of folders your
terminal searches. A window you opened *before* you installed Python is
still holding the old list, and it will tell you Python does not exist
when it does. Close it. Open a new one.

## Starter

Nothing to copy into a file this time. Type these into a brand-new
terminal window, one at a time, and read what comes back:

```bash
python --version
python
```

The second command starts the **REPL** — the interactive Python prompt,
where you type one line and Python answers immediately. Its prompt is
three greater-than signs, `>>>`. You leave it by typing `exit()`.

On macOS and most Linux systems the command is `python3`, not `python`.
Both are covered under Common bugs to catch.

## Requirements

1. `python --version` (or `python3 --version`) prints a version of **3.11
   or higher**.
2. You start the REPL, type `print("Week 1!")`, and see `Week 1!` printed
   straight back at you.
3. A file `notes/install-check.txt` exists in your Week 1 repository and
   contains the proof — either your pasted REPL session, or the two lines
   the redirect recipe below produces.
4. That file is committed to Git.

## Constraints

- **Open a new terminal window first.** An installer edits the list of
  folders your terminal searches for programs. A window that was already
  open kept the old list, so it will answer the question wrongly and you
  will spend an hour fixing something that is not broken.
- **3.11 is a floor, not a suggestion.** Python 3.11 is the version that
  started printing `~~~~^^` markers underneath the exact piece of a line
  that failed. When you are new, an error message that points at the
  right character is worth more than every other feature in the release.
- **The proof is a file, not a memory.** Git tracks files. It cannot track
  an empty folder, and it certainly cannot track "I saw it work". Write
  the file.
- **No packages, no downloads.** Everything here ships with Python. If
  this problem needed an install, it would be testing your network rather
  than your setup.

## Expected output

A real session. Your version and your build details will differ; the
shape will not.

```text
$ python --version
Python 3.13.2
$ python
Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Week 1!")
Week 1!
>>> exit()
$ cat notes/install-check.txt
Python 3.13.2
Week 1!
```

## Steps

1. Close every terminal window you already had open. Open one new one.
2. Run `python --version`. If nothing answers to `python`, try `python3`,
   then read Common bugs to catch before touching the installer.
3. Read the number. It must start `3.11`, `3.12`, `3.13` or higher.
4. Run `python` on its own to start the REPL. Read the banner it prints.
5. At the `>>>` prompt, type `print("Week 1!")` and press Enter.
6. Leave the REPL with `exit()`.
7. Save the proof into `notes/install-check.txt` — copy and paste the
   session, or use the two-line redirect recipe in The Solution.
8. Commit the file.

## The Solution

Three commands, in a freshly opened terminal.

```bash
python --version
```

```text
Python 3.13.2
```

Then start the REPL with no filename and type the one line the problem
asks for:

```bash
python
```

```text
Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Week 1!")
Week 1!
>>> exit()
```

Now capture the proof. Select the whole transcript in your terminal, copy
it, and paste it into `notes/install-check.txt`. If you would rather have
the machine do it, this produces an equivalent file with no copy and
paste at all:

```bash
mkdir -p notes
python --version > notes/install-check.txt
python -c "print('Week 1!')" >> notes/install-check.txt
```

```text
Python 3.13.2
Week 1!
```

Then commit it, because a file nobody committed is a file you will lose:

```bash
git add notes/install-check.txt
git commit -m "Add install verification notes"
```

**Why it works.**

`python --version` answers two questions in one breath. It proves that
*something* named `python` can be found, and it tells you *which*
something. Those are separate facts, and the second one is the one that
bites people later.

The banner the REPL prints is the more useful of the two answers. Look at
what is packed into it: the exact version, a build tag, the date it was
built, the compiler that built it, and the platform name. When you later
ask for help somewhere, pasting that one line answers half the questions
a helper would otherwise have to ask you.

`python -c "..."` is the REPL's quiet twin. It runs one line of Python
and exits. That is what lets the second recipe write to a file — you can
point a program's output into a file, but you cannot point an
interactive conversation into one.

The `>` and `>>` are not Python. They are your terminal. `>` creates the
file or wipes it and starts over; `>>` adds to the end of it. Getting
those two the wrong way round is how you end up with a one-line file and
no idea why.

## Download and run

There is no file to download for this problem, and that is the point: the
thing being checked is whether your terminal can find Python without any
help from a script. Running a script would already assume the answer.

The commands to run are the ones in The Solution. If you want a single
line that answers the whole question, this is it:

```bash
python -c "import sys; print(sys.version_info >= (3, 11))"
```

```text
True
```

## Common bugs to catch

- **`bash: python: command not found`.** On macOS and most Linux systems
  the program is deliberately named `python3`, and there is no plain
  `python` at all. That is on purpose: for years `python` meant Python 2,
  and the confusion did real damage. Try `python3 --version` before you
  re-run any installer.
- **On Windows, `python` opens the Microsoft Store instead.** That is a
  placeholder Windows ships called an App Execution Alias, and seeing it
  means the real Python is not on your search path. Turn the alias off in
  *Settings → Apps → Advanced app settings → App execution aliases*, or
  re-run the python.org installer with *Add python.exe to PATH* ticked.
- **You get 3.9 or 3.10 and decide it is close enough.** It is not, for
  this course. See Constraints — the error messages are genuinely worse,
  and you will feel it every day.
- **You checked in the terminal you already had open.** The installer
  changed where your terminal looks; a window that was already running
  kept the old settings. Close it, open a new one, check again.
- **You made a `notes/` folder and Git ignores it.** Git tracks files, not
  folders. An empty folder simply never appears in `git status`. It shows
  up the moment `install-check.txt` is inside it, which is exactly why
  this problem asks for a file and not a folder.
- **`notes/install-check.txt` has one line in it.** You used `>` twice
  instead of `>` then `>>`, so the second command wiped the first one's
  work.

## Under the hood

<details>
<summary>Under the hood — how your terminal decides which Python "python" means</summary>

`PATH` is an ordered list of folders, kept in an environment variable. When
you type a bare command name, your shell walks that list from left to
right and runs the **first** match it finds. Not the newest, not the best
— the first. That is the entire algorithm, and it explains almost every
"but I installed it" story you will ever hear.

You can look at the list:

```bash
python -c "import os; print(os.environ['PATH'].split(os.pathsep)[:3])"
```

And you can ask which file actually won: `which python` on macOS and
Linux, `where python` on Windows, `Get-Command python` in PowerShell.

Two consequences worth carrying with you:

- An installer that edits `PATH` cannot reach into a shell that is already
  running. Environment variables are copied into a process when it starts
  and never updated from outside. That is why "close the window and open a
  new one" is real advice and not folklore.
- Because the search stops at the first hit, *order* is the whole game.
  Activating a virtual environment in Problem 2 works by putting one
  folder at the very front of this list. Nothing is installed, nothing is
  copied — one list is reordered.

</details>

<details>
<summary>Under the hood — every field in the REPL banner, and why win32 is a lie</summary>

Take the banner apart:

```text
Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
```

- `3.13.2` — major, minor, patch.
- `tags/v3.13.2:4f8bb39` — the tag and the short commit hash in CPython's
  own source repository. This build was made from exactly that commit.
- `Feb  4 2025, 15:23:48` — when the binary was compiled.
- `MSC v.1942` — the C compiler used. Microsoft's on Windows; you will see
  `Clang` on macOS and `GCC` on Linux. Python itself is written in C, and
  this is the compiler that turned that C into the program you are
  running.
- `64 bit (AMD64)` — the real word size and processor family.
- `on win32` — a legacy label every Windows build reports, 64-bit ones
  included. It does **not** mean 32-bit. Notice it contradicts the field
  right before it. This confuses somebody every single year.

The same values are available to your code as `sys.version` (one long
string) and `sys.version_info` (a named tuple of integers). Prefer the
tuple. Comparing versions as strings is a trap, because `"3.9"` sorts
*after* `"3.11"` — the comparison goes character by character, and `9` is
bigger than `1`. As numbers, `(3, 9) < (3, 11)`, which is what you meant:

```bash
python -c "import sys; print(sys.version_info >= (3, 11))"
```

```text
True
```

</details>

## Acceptance checklist

- [ ] The terminal window was opened *after* Python was installed.
- [ ] `python --version` (or `python3 --version`) prints 3.11 or higher.
- [ ] The REPL started, `print("Week 1!")` echoed `Week 1!`, and `exit()`
      returned you to the shell.
- [ ] `notes/install-check.txt` exists and contains the proof.
- [ ] `python -c "import sys; print(sys.version_info >= (3, 11))"` prints
      `True`.
- [ ] The file is committed with a message like
      `Add install verification notes`.

## Stretch

- Find out *which* file answered to the name. Run `which python` (macOS,
  Linux) or `where python` (Windows) and compare it to
  `python -c "import sys; print(sys.executable)"`. They should agree. When
  they do not, you have found a real problem early and cheaply.
- Install a second Python version side by side with `pyenv` (macOS,
  Linux) or `pyenv-win` (Windows), and switch between them per project.
  It is the cleanest way to see that "the Python" is not a thing — there
  are only Pythons, and one of them is currently first on your `PATH`.
- Add the platform to your notes file:
  `python -c "import sys; print(sys.platform)"`. Write down the exact
  string you get — `win32`, `darwin`, or `linux`. Two of those three
  surprise people.

Next: [Homework Problem 2 — Project Skeleton with a venv](./problem-02-project-skeleton-with-a-venv.md).
