# Homework Problem 2 — Project Skeleton with a venv

> **Topic:** a new folder, a Git repository, a virtual environment, and a `.gitignore` that keeps the environment out of the history
> **Lecture:** [Lecture 3 — Git and GitHub Basics](../lecture-notes/03-git-and-github-basics.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** this is the folder that Problems 3, 4, 5 and 6 all live in. Build it once, correctly, in the right order, and the rest of the week has nothing left to go wrong.

<!-- no-runnable-file: the answer to this problem is a folder on your disk with a Git history inside it. A script that built it would be doing the exercise instead of you, and running it here would create a repository inside the course repository. -->

## The Brief

Make a new project the way a professional makes one, on the first day,
before there is any code to protect.

Four things go in, in this order:

1. **A folder** — `week-01-homework`.
2. **A Git repository** inside it. Git is a machine that remembers every
   version of every file you tell it about, forever.
3. **A virtual environment** — a private box of Python packages that
   belongs to this project alone, so installing something here can never
   break another project.
4. **A `.gitignore`** — a list of things Git should pretend not to see.

The last one is the one people skip, and it is the one this problem is
really about. Your virtual environment is tens of megabytes of files that
were built for *your* computer. Nobody else can use them. If it gets into
the history, it is in the history forever, because Git's whole promise is
that it never forgets.

So the order matters. Write the "pretend not to see" list *before* you
tell Git to look at anything.

## Starter

The exact contents of the `.gitignore` you are aiming for. Type this into
your editor and save it in the project root:

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
```

Lines starting with `#` are comments — notes for humans, ignored by Git.
A trailing `/` says "this is a folder".

## Requirements

1. A folder called `week-01-homework` exists, with a Git repository
   initialized inside it.
2. A virtual environment lives at `.venv/` inside that folder, and is
   **not** tracked by Git.
3. `.gitignore` sits in the project root and lists at least `.venv/`,
   `__pycache__/`, and `.DS_Store`.
4. `git log --oneline` shows exactly one commit, with a message that says
   what it did.
5. `git status` reports a clean working tree after that commit.

## Constraints

- **Write `.gitignore` before the first `git add`.** Ignore rules only
  apply to files Git is not already tracking. Once a file is tracked,
  adding it to `.gitignore` changes nothing at all — you have to untrack
  it by hand, and the old copies stay in the history regardless.
- **Do not add a GitHub remote yet.** That is Problem 5, and doing it out
  of order is how people end up with two unrelated histories and a
  rejected push.
- **Name the environment `.venv`, with the dot.** The dot makes it a
  hidden folder on macOS and Linux, and `.venv` is what nearly every
  editor and tool looks for first. `venv` also works and is in the
  ignore list above so that a collaborator using the other name is
  covered too.
- **One commit, not five.** The point is a single clean starting state
  that you can describe in one sentence.

## Expected output

Real output, in order. Straight after `git init` and before the commit:

```text
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	README.md

nothing added to commit but untracked files present (use "git add" to track)
```

Notice what is **not** in that list: `.venv/`. That is the whole problem,
and it is already working.

After the commit:

```text
$ git status
On branch main
nothing to commit, working tree clean
$ git log --oneline
8595108 Initial commit: project skeleton with venv and gitignore
```

Your hash will be different. A commit hash is computed from the content,
the author, *and* the timestamp, so no two people ever get the same one.

## Steps

1. `mkdir week-01-homework` and `cd` into it.
2. `git init`.
3. `python -m venv .venv`.
4. Activate the environment. Your prompt should gain a `(.venv)` prefix.
5. Create `.gitignore` with the Starter contents.
6. Create `README.md` with one line: `Code Crunch Convos - Week 1 homework`.
7. `git status`, and read it. `.venv` should not be listed.
8. `git add .` then `git commit -m "..."`.
9. `git status` and `git log --oneline` to confirm.

## The Solution

Six commands. The order is the answer.

```bash
mkdir week-01-homework
cd week-01-homework
git init
python -m venv .venv
```

macOS and Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```text
.venv\Scripts\Activate.ps1
```

Then write the `.gitignore` *before* the first `git add`, and commit:

```bash
printf '# Virtual environments\n.venv/\nvenv/\n\n# Byte-compiled / cache\n__pycache__/\n*.pyc\n\n# IDE / editor\n.vscode/\n.idea/\n\n# OS metadata\n.DS_Store\nThumbs.db\n\n# Secrets\n.env\n' > .gitignore
printf 'Code Crunch Convos - Week 1 homework\n' > README.md
git add .
git commit -m "Initial commit: project skeleton with venv and gitignore"
```

On Windows PowerShell, `printf` does not exist. Create the two files in
your editor with the same contents, or use `Set-Content -Encoding utf8`
with a here-string.

Confirm the environment is actually active:

```bash
python -c "import sys; print(sys.prefix != sys.base_prefix)"
```

```text
True
```

**Why it works.**

`git init` before `python -m venv` is deliberate. Either order technically
works, but running `git init` first means the very first `git status` you
ever type in this project already shows the environment being correctly
left alone. You get the reassurance for free, at the moment it helps most.

Since Python 3.11, a virtual environment ignores *itself*. That is why
`.venv/` was missing from that first `git status` even though you had not
written any ignore rules yet. `python -m venv` quietly drops a
`.gitignore` inside the environment:

```bash
cat .venv/.gitignore
```

```text
# Created by venv; see https://docs.python.org/3/library/venv.html
*
```

A `.gitignore` applies to its own folder and everything below it, and `*`
matches everything, so the environment excludes itself.

So why write the root `.gitignore` at all? Three reasons, and the
requirements are quietly testing all three. It also covers `venv/`, for
the day you or a teammate uses the other name. It covers `__pycache__/`
and `.DS_Store`, which nothing creates for you. And it is *committed*, so
the rules travel with the project instead of living in a folder that gets
deleted and rebuilt. A rule that only exists on your disk is not a rule.

`git add .` is not "add everything". It is "add everything Git is willing
to look at" — it walks the folder and obeys the ignore rules as it goes.
That distinction is exactly why the command is safe here and dangerous in
a project with no `.gitignore`.

And "clean working tree" means all three of Lecture 3's places agree: the
files on your disk match the staging area, and the staging area matches
the last commit. It says nothing about ignored files. `.venv/` is sitting
right there taking up space, and the tree is still clean.

## Download and run

There is no file to download. The deliverable is a folder on your disk
with a history inside it, and a script that built it for you would be
doing the problem instead of you.

To check your own work, run these four in the project root:

```bash
git status --short
git check-ignore -v .venv/
git log --oneline
python -c "import sys; print(sys.prefix != sys.base_prefix)"
```

`git status --short` printing **nothing at all** is the clean-tree check.

## Common bugs to catch

- **You committed the environment, and deleting the folder did not fix
  it.** Deleting it just records a deletion; the old copies stay in the
  history. The fix is to stop tracking it while leaving it on disk:
  `git rm -r --cached venv`, then commit. That `--cached` is the entire
  difference between "stop tracking this" and "delete this". Without it,
  `git rm -r venv` removes the folder from your disk as well, and you get
  to rebuild your environment.
- **You wrote `.gitignore` after the first commit.** Ignore rules never
  reach backwards. That is precisely why the fix above needs
  `git rm --cached` at all. Write the file first, every time.
- **`Author identity unknown`.**

  ```text
  Author identity unknown

  *** Please tell me who you are.

  Run

    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"

  to set your account's default identity.
  ```

  That is Lecture 3's one-time setup step showing up as an error because
  it was skipped. Run the two commands, run the commit again, lose
  nothing.
- **Your branch is called `master`.** Git versions before 2.28 have no
  default-branch setting, and some installations still start on `master`.
  Fix this repository with `git branch -M main`, and fix it permanently
  with `git config --global init.defaultBranch main`. It matters because
  GitHub's default is `main`, and a mismatch is a confusing way to fail
  your first push in Problem 5.
- **`.venv` with no trailing slash.** `.venv/` matches only a folder;
  `.venv` matches a file or a folder with that name. Either works here,
  but the slash says what you meant.
- **Activation seems to do nothing.** In PowerShell you may get an
  execution-policy error. Lecture 2's one-time
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
  is the documented fix.

## Under the hood

<details>
<summary>Under the hood — what a virtual environment actually does to PATH and sys.prefix</summary>

A virtual environment is far less magical than it looks. It is a folder
with three things in it: a copy of (or a link to) the Python program, an
empty `site-packages` folder where installed packages will land, and a
small text file called `pyvenv.cfg` that points back at the Python it was
made from.

```bash
cat .venv/pyvenv.cfg
```

```text
home = C:\Users\you\AppData\Local\Programs\Python\Python313
include-system-site-packages = false
version = 3.13.2
```

**Activation does one thing: it edits `PATH`.** The activate script puts
`.venv/bin` (or `.venv\Scripts` on Windows) at the very front of the list
of folders your shell searches, sets a `VIRTUAL_ENV` variable, and changes
your prompt so you can see it happened. It copies nothing, installs
nothing, and starts no background process. `deactivate` puts the old
`PATH` back. That is the entire mechanism.

Because the search stops at the first match — see Problem 1's Under the
hood — putting one folder at the front is enough to change which `python`
answers.

**Then the interpreter does the other half.** When Python starts, it looks
at its own location, walks up looking for `pyvenv.cfg`, and if it finds
one it sets:

- `sys.prefix` — the root of the environment currently in charge.
- `sys.base_prefix` — the root of the Python that the environment was
  built from.

Outside an environment those two are the same string. Inside one they
differ, and that is the only honest test for "am I in a virtual
environment":

```bash
python -c "import sys; print(sys.prefix); print(sys.base_prefix)"
```

```text
C:\Users\you\week-01-homework\.venv
C:\Users\you\AppData\Local\Programs\Python\Python313
```

`sys.prefix` is what decides where `import` searches and where `pip`
installs. This is why the whole folder can be deleted and rebuilt without
consequence, and why you never commit it: it is a derived thing, fully
described by `requirements.txt` in Problem 4.

A useful consequence: you do not actually have to activate anything.
Running `.venv/bin/python script.py` by full path gives you the same
environment, because the interpreter works out `sys.prefix` from where it
lives, not from `PATH`. Activation is a convenience for your fingers.

</details>

<details>
<summary>Under the hood — what Git actually stores when you commit</summary>

Git does not store changes. It stores whole snapshots, deduplicated, and
then works out the differences when you ask to see them.

Three kinds of object go into `.git/objects`:

- A **blob** is the contents of one file. No name, no path, no
  permissions — just bytes.
- A **tree** is a folder listing: names, modes, and the hash of the blob
  or tree each name points to.
- A **commit** points at one top-level tree, plus the hash of its parent
  commit, the author, the committer, the timestamps, and your message.

Every object is named by the SHA-1 hash of its own contents. That single
design choice gives you most of Git's behaviour for free. Two files with
identical contents are stored once, whatever they are called. Changing one
byte changes the hash, so nothing can be quietly altered. And because the
commit's hash covers its parent's hash, which covers *its* parent's, the
whole history is sealed: you cannot rewrite an old commit without every
commit after it getting a new hash too.

You can look at all of it. In your project:

```bash
git cat-file -p HEAD
```

```text
tree 2a1f0b8c...
author Your Name <you@example.com> 1755900000 -0400
committer Your Name <you@example.com> 1755900000 -0400

Initial commit: project skeleton with venv and gitignore
```

Then walk one level down with `git cat-file -p 2a1f0b8c` to see the tree
that lists `.gitignore` and `README.md`, and once more to see a blob's
raw contents.

Two things fall out of this that explain earlier rules:

- **A commit hash depends on the timestamp and the author**, so two people
  committing identical files get different hashes. Yours will never match
  the transcript above.
- **Git has no concept of an empty folder.** Trees list files. A folder
  with nothing in it produces no entries, so it cannot be committed. That
  is why Problem 1 asked for `notes/install-check.txt` rather than
  `notes/`.

</details>

## Acceptance checklist

- [ ] `week-01-homework/` exists with a Git repository inside it.
- [ ] `.venv/` exists on disk.
- [ ] `git status` does not mention `.venv`.
- [ ] `.gitignore` is committed and lists `.venv/`, `__pycache__/`, and
      `.DS_Store` at minimum.
- [ ] `git log --oneline` shows one commit with a meaningful message.
- [ ] `git status` says `nothing to commit, working tree clean`.
- [ ] `python -c "import sys; print(sys.prefix != sys.base_prefix)"`
      prints `True` while the environment is active.

## Stretch

- Ask Git to explain itself. `git check-ignore -v .venv/pyvenv.cfg` names
  the file and the line number of the rule that made the decision. Run it
  before you add your own `.gitignore` and after, and watch the answer
  change from `.venv/.gitignore:2:*` to `.gitignore:2:.venv/`. This is the
  tool to reach for any time you are arguing with Git about whether
  something is ignored.
- Set up a **global** ignore file. A project's `.gitignore` should
  describe the *project* — `__pycache__/`, `.venv/`. Things that are about
  *your machine* — `.DS_Store`, `Thumbs.db`, your editor's folder —
  arguably belong somewhere personal, so you are not asking teammates to
  carry your operating system's litter:

  ```bash
  git config --global core.excludesfile ~/.gitignore_global
  printf '.DS_Store\nThumbs.db\n.idea/\n*.swp\n' > ~/.gitignore_global
  ```

  Keep them in the project file as well. Two lines of overlap covers the
  teammate who never did this.
- Delete `.venv/` entirely and rebuild it with `python -m venv .venv`.
  Confirm that `git status` is still clean afterwards. Feeling how
  disposable the folder is makes the "never commit it" rule stop being a
  rule you memorised.

Next: [Homework Problem 3 — A Tiny Script with Comments and a Docstring](./problem-03-a-tiny-script-with-comments-and-a-docstring.md).
