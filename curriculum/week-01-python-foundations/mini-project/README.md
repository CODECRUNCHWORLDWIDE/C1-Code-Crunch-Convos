# Mini-Project — "Hello, You"

> **Topic:** the whole of Week 1 in one small project — a script, an environment, a repository
> **Lecture:** [03 — Git and GitHub Basics](../lecture-notes/03-git-and-github-basics.md)
> **Difficulty:** the code is easy; the workflow around it is the work
> **Target time:** 2–3 hours, spread over more than one sitting
> **Why this one:** it is the first thing you will have that somebody else can find, clone, and run. Everything after this week assumes you can do these steps without looking them up.

<!-- no-runnable-file: this page is the project brief, and the project's deliverable is a repository rather than a single script. The runnable answer is hello_you.py, which ships beside this page and is linked from Download and run. -->

## The Brief

This is the capstone of Week 1. Everything the week taught — installing
Python, writing a script, making a virtual environment, using pip, and
version control — comes together in one small project called **Hello, You**.

The program itself is tiny. It asks your name, asks your favourite
programming language, and prints one friendly line back:

```text
Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
```

That is the easy half. The other half is everything around the program: it
lives in its own folder, with its own virtual environment, tracked by Git from
the very first commit, and pushed to a public repository on GitHub under your
own account.

Think of it as the difference between cooking a meal and running a kitchen.
The recipe is three lines. Knowing where the knives go, and being able to hand
the kitchen to somebody else without a tour, is the skill.

> *As a* curious learner just starting Python,
> *I want* a script that greets me by name,
> *so that* I prove to myself I can collect input, transform it, and publish
> working code where anyone can run it.

## Starter

The scaffold, with four `TODO`s to fill in, is on its own page:
**[starter.md](./starter.md)**. Copy the code block from there into a file
called `hello_you.py` inside your new `hello-you/` folder. It runs before you
touch it, so you always have a working program to grow rather than a broken
one to repair.

The shape it gives you:

```python
"""hello_you.py -- greet one person, by name, from the terminal."""

DEFAULT_NAME: str = "friend"
DEFAULT_LANGUAGE: str = "Python"


def prompt_user() -> tuple[str, str]:
    """Ask for a name and a favorite language and return both, cleaned."""
    # TODO 1: read the name, strip it, fall back to DEFAULT_NAME.
    # TODO 2: read the language the same way.
    # TODO 3: return the two cleaned strings as one tuple, name first.
    return DEFAULT_NAME, DEFAULT_LANGUAGE


def build_greeting(name: str, language: str) -> str:
    """Return the greeting line for name and language."""
    # TODO 4: build the sentence with an f-string and return it.
    return f"Hello, {name}."


def main() -> None:
    """Collect the two answers, build the greeting, and print it."""
    name, language = prompt_user()
    print(build_greeting(name, language))


if __name__ == "__main__":
    main()
```

The prompt wording is yours to pick. `starter.md` suggests
`Favorite language (Enter for Python): `; the answer below uses
`Favorite programming language [Python]: `. Either is fine, as long as the
prompt tells the user what pressing Enter will do.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](../../../README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

The program:

1. Asks for a **name**, with a clear prompt.
2. Asks for a **favourite programming language**, and accepts an empty answer,
   which becomes `Python`.
3. Strips the whitespace from around every answer.
4. Prints one greeting containing both values, worded exactly like this for
   `Ada` and `Python`:

   ```text
   Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
   ```

5. Exits on its own. No traceback, no prompt left hanging.

The project:

6. Lives in its own folder named `hello-you`.
7. Has a virtual environment named `.venv` inside that folder, which is
   **not** committed.
8. Is tracked by Git from the first commit, with at least three commits whose
   messages say what changed.
9. Is pushed to a **public** GitHub repository under your own account, named
   `hello-you`.
10. Contains a `.gitignore` listing at least `.venv/`, `__pycache__/`, and
    `.DS_Store`.
11. Contains a `README.md` written for somebody who found your repository —
    what it does, how to set it up, how to run it. That is a different
    document from this brief.

The code:

12. Type hints on every parameter and every return.
13. A module docstring, and a docstring on every function.
14. `main()` behind an `if __name__ == "__main__":` guard.

The finished folder:

```text
hello-you/
├── .gitignore
├── .venv/                  (on disk, never committed)
├── README.md
├── hello_you.py
└── requirements.txt        (only if you do the dependency stretch goal)
```

## Constraints

- **`build_greeting` returns a string; only `main` prints.** A function that
  returns can be tested, joined into a longer message, written to a file, or
  coloured by its caller. A function that prints can only ever print. This is
  the one design decision to take away from the project, and *Steps* below
  checks your greeting without you typing anything, which is only possible
  because of it.
- **`.strip()` before `or`, always in that order.** An empty string is falsy,
  so `or` reaches for the default. A string of three spaces is *truthy*, so it
  does not. Strip first and the spaces become empty, and the default fires.
- **The `.gitignore` is written before the first `git add`.** Ignore rules only
  apply to files Git is not already tracking. They do not retroactively
  untrack anything. Write it first and the problem never happens.
- **The repository is public.** The point of this project is that a stranger
  can clone it and run it. *Steps* ends with you doing exactly that.
- **Standard library only for `hello_you.py`.** It imports nothing at all, so
  it runs on any Python 3.11 or newer with no install step. An empty
  dependency list here is a feature, not an omission.
- **Underscores in the module name, hyphens in the folder name.** The folder is
  `hello-you`; the file is `hello_you.py`. A hyphen in Python means
  subtraction, so `import hello-you` is a syntax error, and you will not find
  out until the first time you try to import it.

## Expected output

A real session on CPython 3.13.2. Type `Ada`, then press Enter at the second
prompt to take the default:

```text
$ python hello_you.py
Your name: Ada
Favorite programming language [Python]:
Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
```

That last line is character for character the string requirement 4 specifies.

Feed it deliberately sloppy input and the defaults and the stripping both do
their jobs:

```bash
printf '   Grace Hopper  \n\n' | python hello_you.py
```

```text
Your name: Favorite programming language [Python]: Hello, Grace Hopper! Welcome to Code Crunch Convos. May your Python be readable.
```

```bash
printf '  \n  rust  \n' | python hello_you.py
```

```text
Your name: Favorite programming language [Python]: Hello, friend! Welcome to Code Crunch Convos. May your rust be readable.
```

The two prompts run together on one line because nothing echoes back through
a pipe — in a real terminal your typing separates them. Nothing is wrong. What
matters is the last line: no stray spaces around `Grace Hopper`, the empty
language answer defaulted to `Python`, and the whitespace-only name defaulted
to `friend`.

And the repository, at the end:

```bash
git log --oneline
```

```text
706a5ec Add stretch version: banner, guest book, rich color
c78fec5 Add README with setup and run instructions
76656f7 Add hello_you.py: prompt for name and language
22d90fe Initial commit: add .gitignore for a Python project
```

Your hashes will be different from these and from everybody else's. A commit
hash is computed from the content, the author, *and* the timestamp, so no two
people ever get the same one.

## Steps

**1. Make the folder and start the repository.**

```bash
mkdir hello-you
cd hello-you
git init
```

```text
Initialized empty Git repository in /path/to/hello-you/.git/
```

**2. Make the environment and activate it.**

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell the second line is `.venv\Scripts\Activate.ps1`. Your
prompt should now start with `(.venv)`.

**3. Write `.gitignore` before anything else gets staged.** The full file is
in *The Solution*. Then check what Git can see:

```bash
git status
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore

nothing added to commit but untracked files present (use "git add" to track)
```

`.venv/` is not in that list. It is sitting right there on disk and Git is
already refusing to look at it. Ask Git which rule made that decision:

```bash
git check-ignore -v .venv/pyvenv.cfg
```

```text
.gitignore:2:.venv/	.venv/pyvenv.cfg
```

The format is `file:line:pattern`, then a tab, then the path. Line 2 of your
`.gitignore` is the `.venv/` line.

**4. Copy the scaffold from [starter.md](./starter.md) into `hello_you.py`**
and run it once before editing anything. You should see one line:
`Hello, friend.` Seeing it proves your file, your interpreter and your
terminal all agree with each other.

**5. Work the four `TODO`s top to bottom**, running the script after each one.
Four short runs beat one long guess. Delete each `# TODO:` comment as you
satisfy it.

**6. Check the exact wording without typing at a prompt.** This is what
returning instead of printing bought you:

```bash
python -c "from hello_you import build_greeting; print(build_greeting('Ada', 'Python'))"
```

```text
Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
```

Compare it against requirement 4, character by character. The import is silent
only because of the `__main__` guard.

**7. Write your user-facing `README.md`.** Not this brief — a page for
somebody who found your repository. What it is, one sample of the output, how
to set up an environment, how to run it, what each file is for.

**8. Commit in pieces, so the history tells a story.**

```bash
git add .gitignore
git commit -m "Initial commit: add .gitignore for a Python project"
git add hello_you.py
git commit -m "Add hello_you.py: prompt for name and language"
git add README.md
git commit -m "Add README with setup and run instructions"
```

**9. Create the repository on GitHub.** Public, named `hello-you`, with *Add a
README file* left **unchecked**. Then:

```bash
git remote add origin https://github.com/your-username/hello-you.git
git push -u origin main
```

```text
branch 'main' set up to track 'origin/main'.
To https://github.com/your-username/hello-you.git
 * [new branch]      main -> main
```

When it asks for credentials, the **username** is your GitHub username and the
**password** is a personal access token from
<https://github.com/settings/tokens>, never your account password.

**10. Prove it works for a stranger.** Clone your own repository into a
throwaway folder, as somebody else would:

```bash
cd /tmp
git clone https://github.com/your-username/hello-you.git check
cd check
ls -a
python hello_you.py
```

```text
.
..
.git
.gitignore
README.md
hello_you.py
```

No `.venv` in the clone, and the program runs with no setup at all. If the
clone asks you for credentials, your repository is private and requirement 9
asks for public. Delete `/tmp/check` when you are done.

**11. Paste the repository URL into your Week 1 notes.** This is the step
people skip, and it is the one Week 2 needs.

## The Solution

`hello_you.py` is the graded artifact. Forty-two lines, importing nothing:

```python
"""hello_you.py -- greet the user by name.

Week 1 mini-project, Code Crunch Convos. Asks for a name and, optionally,
a favorite programming language, then prints one personalized greeting.

Run it with::

    python hello_you.py
"""

DEFAULT_LANGUAGE: str = "Python"
DEFAULT_NAME: str = "friend"


def prompt_user() -> tuple[str, str]:
    """Return ``(name, language)``, both stripped of outer whitespace.

    An empty name becomes ``DEFAULT_NAME`` and an empty language becomes
    ``DEFAULT_LANGUAGE``, so neither answer can be blank downstream.
    """
    name: str = input("Your name: ").strip() or DEFAULT_NAME
    prompt: str = f"Favorite programming language [{DEFAULT_LANGUAGE}]: "
    language: str = input(prompt).strip() or DEFAULT_LANGUAGE
    return name, language


def build_greeting(name: str, language: str) -> str:
    """Return the one-line greeting for ``name`` and ``language``."""
    return (
        f"Hello, {name}! Welcome to Code Crunch Convos. "
        f"May your {language} be readable."
    )


def main() -> None:
    """Prompt once, greet once."""
    name, language = prompt_user()
    print(build_greeting(name, language))


if __name__ == "__main__":
    main()
```

`.gitignore`, committed before the first `git add`:

```text
# Virtual environments
.venv/
venv/

# Byte-compiled / cache
__pycache__/
*.pyc

# IDE / editor
.vscode/
.idea/

# OS metadata
.DS_Store
Thumbs.db

# Secrets
.env

# Generated by the stretch script, not source
guests.txt
```

The requirements ask for three lines. This has those three plus six more.
`guests.txt` is the interesting addition: the stretch script writes it while
it runs, so it is *output*, not source, and output does not belong in version
control. Committing it would mean every clone of your repository carries a log
of everyone you happened to greet on your laptop.

**Why it works, piece by piece.**

**The empty-name decision.** The requirements say an empty *language* becomes
`Python`. They do not say what an empty *name* should do. This answer defaults
it to `friend`, because it reuses the exact idiom already given for the
language, and because it never produces the sad line
`Hello, ! Welcome to...`. Re-prompting in a loop would also be correct, and it
is more work than was asked for; say so in your README and a reader will
agree with you.

**`prompt_user` returns a tuple, and `main` takes it apart.**
`return name, language` builds a two-item tuple — the *comma* makes the tuple,
not the parentheses, which are absent here. Then
`name, language = prompt_user()` is *unpacking*: Python opens the tuple and
binds each item to a name, left to right. If the counts do not match you get
`ValueError`. Returning two related values as one tuple is ordinary Python,
and it is why the annotation reads `tuple[str, str]`.

**`.strip()` before `or`, and why the order is load-bearing.** These two lines
look like they do the same thing:

```python
language = input(prompt).strip() or DEFAULT_LANGUAGE   # correct
language = input(prompt) or DEFAULT_LANGUAGE           # subtly broken
```

An empty string is falsy, so `or` reaches past it to the default. But a string
of spaces is truthy:

```bash
python -c "print(bool(''), bool('   '))"
```

```text
False True
```

The second line therefore accepts three spaces as a language name. Strip
first, the spaces become `""`, and the default fires. The general habit is
**normalise at the edge**: clean each value in the same expression that reads
it, and nothing further down ever has to wonder whether it was cleaned.

`str.strip()` with no argument removes every kind of surrounding whitespace —
spaces, tabs, newlines, carriage returns. That last one quietly fixes a whole
category of cross-platform bug. And like every string method it returns a
*new* string, because strings never change in place. A bare `raw.strip()` on a
line of its own does nothing at all, and gives you no error to warn you.

**The prompt advertises its own default.**
`Favorite programming language [Python]: ` tells the user, in the prompt
itself, what pressing Enter will do. Square brackets are the near-universal
convention for that in command-line tools. It costs one f-string and turns
requirement 2's "optionally" from a secret into an instruction. `prompt` is
pulled into its own variable only to keep the line under 79 characters, which
is the limit PEP 8 sets.

**Two constants instead of two string literals.** `DEFAULT_LANGUAGE` appears
twice — once in the prompt text, once in the fallback — and they have to agree
or the prompt is lying. Naming it once makes that impossible to get wrong.
`SCREAMING_SNAKE_CASE` is the convention for module-level constants. Python
has no `const` keyword and will happily let you reassign them, so the capitals
are a message to humans.

**`if __name__ == "__main__":` makes the file both a program and a library.**
Running a file directly sets its `__name__` to `"__main__"`. Importing the
same file sets `__name__` to the module name, `"hello_you"`. So the guard
means: only prompt when I am the program. Without it, step 6's one-line check
would stop and demand your name before printing anything.

## Download and run

Download [hello_you.py](./hello_you.py) and run it:

```bash
python hello_you.py
```

Type a name, then press Enter at the second prompt to take the default.

This page has no `.py` of its own on purpose. The deliverable of a
mini-project is the whole repository — the environment, the ignore file, the
history, the push — and no single script can stand in for that. `hello_you.py`
is the part of it that runs, and it is the file above.

The scaffold you build it from is on [starter.md](./starter.md).

## Common bugs to catch

**A stray `None` after the greeting.**

```text
Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.
None
```

You put a `print()` inside `build_greeting` instead of a `return`. A function
with no `return` gives back `None`, so `print(build_greeting(...))` prints the
greeting from inside the function, then prints `None`. Whenever a stray `None`
appears in your output, look for a function you are printing that has already
printed.

**`TypeError: cannot unpack non-iterable NoneType object`.** `prompt_user()`
has no `return` — you deleted the placeholder while filling in TODO 3 and
never replaced it. `None` cannot be spread across `name, language`.

**Extra spaces inside the greeting.** No error, just an ugly line. Typing
`  Ada  ` and `  Python ` without stripping:

```text
Hello,   Ada  ! Welcome to Code Crunch Convos. May your   Python  be readable.
```

This is invisible unless you deliberately type padded input when you test.

**The language vanishes.** Typing three spaces at the language prompt, with
`input(prompt) or DEFAULT_LANGUAGE`:

```text
Hello, Ada! Welcome to Code Crunch Convos. May your     be readable.
```

The default never fired, because `"   "` is truthy. Strip first.

**You forgot to unpack.**

```python
name = prompt_user()                      # no comma on the left
print(f"Hello, {name}!")
```

```text
Your name: Favorite programming language [Python]: Hello, ('Ada', 'Python')!
```

No error, because a tuple has a perfectly good text form. Python did exactly
what you asked. The fix is `name, language = prompt_user()`.

**`SyntaxError: invalid syntax` on `import hello-you`.** You named the file
`hello-you.py` to match the folder.

```text
  File "<string>", line 1
    import hello-you
                ^
SyntaxError: invalid syntax
```

The script still *runs* — `python hello-you.py` is a filename, not an
identifier — so the mistake hides until the first time you import it, which
for most people is a stretch goal. Folders get hyphens; modules get
underscores.

**`EOFError: EOF when reading a line`.** You piped input in and it ran out
before the second prompt:

```text
Your name: Traceback (most recent call last):
  File "hello_you.py", line 42, in <module>
    main()
    ~~~~^^
  File "hello_you.py", line 37, in main
    name, language = prompt_user()
                     ~~~~~~~~~~~^^
  File "hello_you.py", line 21, in prompt_user
    name: str = input("Your name: ").strip() or DEFAULT_NAME
                ~~~~~^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
```

`input()` raises `EOFError` when there is nothing left to read, which is also
what Ctrl+D (Ctrl+Z on Windows) does. This is not a bug in the answer, and
requirement 5's "exit cleanly" is about a normal run, not about a user who
hangs up mid-prompt. Catching it needs `try` / `except`, which arrives in
Week 6.

**The push is rejected.**

```text
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/your-username/hello-you.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

The most common Week 1 failure, and the message reads like an accusation about
somebody else. Nobody else pushed. GitHub made a commit on your behalf when
you created the repository with *Add a README file* checked. Fix it with
`git pull --rebase origin main`, then push again. Do not reach for
`git push --force`; it works, and it silently deletes GitHub's commit, and
this is a bad day to learn that habit.

**You committed `.venv/` because you ran `git add .` first.** Fix it with
`git rm -r --cached .venv` — note `--cached`, or you delete the folder from
disk too — then commit the `.gitignore`.

## Under the hood

<details>
<summary>Under the hood — why Git will not track your environment even when you forget</summary>

Since Python 3.11, `python -m venv` writes a `.gitignore` file *inside* the
environment containing a single `*`. So the environment ignores itself, and
Git will not offer to track it even if your own `.gitignore` forgets the
`.venv/` line. Belt and braces, for free.

You should still write the line. Not everyone is on 3.11 or newer, not every
environment is created by `venv`, and somebody naming their folder `venv`
instead of `.venv` on an older Python will commit the whole thing. Relying on
a default that you did not set and cannot see is how surprises happen.

`git check-ignore -v` is the tool for settling any argument about this. It
tells you which file, which line, and which pattern made the decision — and if
it prints nothing at all, the path is not ignored, whatever you believed.

Why the environment must never be committed, beyond size: it records absolute
paths pointing at your own machine. Move the folder, rename your user account,
or hand it to somebody on another operating system, and it stops working. A
`requirements.txt` is portable; a `.venv` is not. Delete and recreate is the
normal fix, and it takes seconds.

</details>

<details>
<summary>Under the hood — what a commit really is, and why hashes never repeat</summary>

A commit is not a diff. It is a full snapshot of every tracked file, plus a
pointer to the commit that came before it, plus who made it and when. Git
stores the snapshot efficiently — files that did not change are not stored
again — but the model in your head should be "photograph", not "list of
changes". That is why checking out an old commit gives you the whole project
as it was, instantly, with no replaying of history.

The short string at the front of each `git log --oneline` row is the first
seven characters of a hash computed from all of that: the file contents, the
parent commit, the author name and email, and the timestamp to the second.
Change any one of those and you get a completely different hash. This is why
your hashes will never match the ones printed on this page, why amending a
commit gives it a new identity, and why rewriting history that other people
have already pulled is rude — every commit after the rewritten one gets a new
hash too, and their copy and yours no longer agree on what happened.

Committing in pieces, as step 8 does, is not ceremony. Each commit should be
one decision you could describe in a sentence and undo on its own. Four
commits that each do one thing are worth far more later than one commit called
"done", because six months from now `git log` is the only surviving record of
why the code looks the way it does.

</details>

<details>
<summary>Under the hood — the credential prompt, and why your password does not work</summary>

Pushing over HTTPS asks for a username and a password. Your GitHub account
password will be rejected. GitHub stopped accepting it for Git operations in
2021.

What it wants instead is a **personal access token** — a long generated string
from <https://github.com/settings/tokens> that you paste into the password
field. A token is better than a password in three ways: you can give it a
narrow scope, so a leaked token cannot change your account settings; you can
give it an expiry date; and you can revoke one without changing anything else.

Your operating system's credential helper will normally remember it after the
first successful push, so you type it once. If you are ever asked repeatedly,
the helper is not configured, and `git config --global credential.helper` will
tell you what, if anything, is set.

The alternative is SSH keys, where the remote URL looks like
`git@github.com:you/hello-you.git` instead of `https://...`. It is a better
long-term setup and one more thing to configure on day one, so it is not
required here.

</details>

## Acceptance checklist

- [ ] `python hello_you.py` runs with no traceback and exits on its own.
- [ ] It prompts for a name and for an optional language.
- [ ] The greeting contains both values, worded exactly as requirement 4
      shows.
- [ ] Whitespace-only input for either question falls back to the default.
- [ ] Both functions carry type hints and a docstring, and no `TODO` comments
      are left in the file.
- [ ] `main()` sits behind `if __name__ == "__main__":`.
- [ ] The project is in its own `hello-you/` folder with a `.venv/` that Git
      is not tracking — proved with `git check-ignore -v .venv/pyvenv.cfg`.
- [ ] `.gitignore` lists at least `.venv/`, `__pycache__/`, and `.DS_Store`.
- [ ] `git status --short` prints nothing at all.
- [ ] `git ls-files` shows no `.venv` anywhere.
- [ ] At least three commits, each message saying what changed.
- [ ] A user-facing `README.md` explains what the program does, how to set it
      up, and how to run it.
- [ ] The repository is on GitHub, public, and a fresh clone runs without
      asking for credentials.
- [ ] The repository URL is in your Week 1 notes.

## Stretch

Pick any of these that appeal. Keep them in a second file,
`hello_you_plus.py`, so that `hello_you.py` stays the small clean thing the
checklist grades.

**Loop until "quit".** Keep asking for names until the user types `quit`, in
any capitalisation, then say goodbye. Have the loop body return a `bool` —
`False` means "the user is done" — and the whole loop becomes
`while greet_once(): pass`, with no `break` anywhere. Case-insensitive means
normalise, then compare: `raw_name.lower() in QUIT_WORDS`.

**Save names to a guest book.** Append every greeted name to `guests.txt`,
one per line, with a timestamp. Open it with `"a"` for append, not `"w"` —
`"w"` silently empties the file on every run, which is the classic way to lose
data with no error message. Pass `encoding="utf-8"` so a name like `José`
writes the same on every operating system. Use
`datetime.now().isoformat(timespec="seconds")` for a timestamp that sorts and
parses cleanly. File writing is Week 6 material, borrowed early.

**A line per language.** Keep a dictionary from language name to a punchy
closing sentence, and look it up with `.get(key, default)` so an unknown
language falls back instead of raising `KeyError`. Lower-case the key so
`RUST`, `Rust` and `rust` all match, but echo the user's own spelling back in
the fallback. Adding a language then costs one line and no code change.

**Print the greeting inside a banner.** Reuse
[Challenge 1](../challenges/challenge-01-personalized-banner.md): copy
`banner.py` next to `hello_you_plus.py` and write
`from banner import build_banner`. A real import, not a copy-paste. This only
works because the challenge's `build_banner` returns its banner instead of
printing it, and keeps its command-line reading behind a `__main__` guard.

**Add a dependency, and see what you actually got.** Install `rich`, then
freeze it:

```bash
python -m pip install rich
python -m pip freeze > requirements.txt
cat requirements.txt
```

```text
markdown-it-py==4.2.0
mdurl==0.1.2
Pygments==2.21.0
rich==15.0.0
```

You asked for one package and received four. `rich` pulls in `markdown-it-py`,
which pulls in `mdurl`, plus `Pygments` for syntax highlighting. That is the
argument for virtual environments, delivered as a receipt. Note that the file
was *frozen*, not hand-written: `pip freeze` reports what is actually
installed, and the moment you type a version by hand the file becomes a claim
rather than an observation.

Two details when you use `rich`: wrap the import in `try` / `except
ImportError` so the file still runs for somebody who does not have it, and
pass `markup=False` when printing, or a user who types `[bold]` as their name
will vanish from the output.
