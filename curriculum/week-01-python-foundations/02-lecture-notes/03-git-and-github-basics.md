# Lecture 3 — Git and GitHub Basics

You've written Python code and isolated its dependencies with a virtual
environment. Now it's time to do what every working developer does on day
one of every project: put your code under **version control**. By the end
of this lecture you'll be able to track changes locally with Git and
publish your work to a public repository on GitHub.

## What Is Version Control?

**Version control** is software that records every change you make to a set
of files, when you made it, why you made it, and lets you go back to any
previous state at any time. Imagine an "undo" button for your entire
project that survives across days, computers, and collaborators — that's
version control.

The version-control system we'll use is **Git**, created by Linus Torvalds
in 2005 (the same Linus who created Linux). Git is *distributed*, which
means every clone of the project contains the entire history. There's no
single "server" your work depends on, which is what makes Git fast and
resilient.

The canonical reference is the free Pro Git book at
<https://git-scm.com/doc>. Bookmark it now.

## Installing Git

- **macOS:** `git` ships with the Command Line Tools. Run `git --version`
  in a terminal. If you're prompted to install the tools, accept.
- **Linux (Debian/Ubuntu):** `sudo apt install git`
- **Linux (Fedora):** `sudo dnf install git`
- **Windows:** download "Git for Windows" from <https://git-scm.com/download/win>.

Verify the install:

```bash
git --version
```

You should see a line like `git version 2.44.0`.

## One-Time Configuration

Tell Git who you are. These two values get embedded into every commit you
ever make, so use the same email you'll use for GitHub.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Set your default branch name to `main` (this matches GitHub's default and
avoids confusion):

```bash
git config --global init.defaultBranch main
```

## Initializing a Repository

A **repository** (or *repo*) is just a folder Git is watching. Inside any
project folder, run:

```bash
git init
```

You'll see a message like *"Initialized empty Git repository in
/path/to/your/project/.git/"*. Git stores all its bookkeeping inside a
hidden `.git/` directory — don't delete or edit it manually.

Run `git status` to see Git's current view of your project:

```bash
git status
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        hello.py

nothing added to commit yet (use "git add" to track)
```

Git is showing you that it has noticed `hello.py` but isn't yet tracking
it.

## The Three States: Working, Staging, Committed

Every file in a Git project lives in one of three places:

```text
working directory  ->  staging area  ->  committed history
   (you edit)         (git add)         (git commit)
```

- **Working directory:** the actual files on disk that you edit.
- **Staging area** (also called the *index*): a snapshot of changes
  you're about to commit. You build this snapshot one file at a time with
  `git add`.
- **Committed history:** the permanent record. Each commit is a snapshot
  with an author, date, message, and a unique ID called a *hash*.

Understanding these three states is the most important Git concept of the
week. Most beginner confusion is "I edited the file but the commit didn't
include my changes" — that means the edit was in the working directory but
never made it to the staging area.

## Staging Files with `git add`

To stage a specific file:

```bash
git add hello.py
```

To stage every change in the current directory and below:

```bash
git add .
```

Run `git status` again and you'll see the file is now listed under
*"Changes to be committed."*

## Committing with `git commit`

A **commit** is a permanent snapshot of whatever is currently staged.

```bash
git commit -m "Add hello.py with first print statement"
```

The `-m` flag provides the *commit message* inline. If you omit `-m`, Git
opens your editor and asks for one.

Verify the commit landed:

```bash
git log --oneline
```

```text
a1b2c3d Add hello.py with first print statement
```

The seven characters at the start are the short form of the commit's hash.

## Writing Good Commit Messages

A good commit message tells the next reader (often: future-you) **what**
changed and **why**. Some practical rules:

1. Write the **subject line** in the imperative mood: "Add greeting
   feature", not "Added" or "Adds".
2. Keep the subject under **50 characters**.
3. Capitalize the subject line; do not end with a period.
4. If you need more detail, add a blank line and a body paragraph that
   explains *why* the change was needed.

A solid commit message looks like:

```text
Add personalized greeting to hello.py

Replace the static "Hello, world!" with a prompt that asks the user
for their name and prints a greeting. This is the foundation for the
Week 1 mini-project.
```

## The `.gitignore` File

Some files should never be committed: virtual environments, OS junk,
secrets. List them in a file called `.gitignore` at the root of your repo.
A solid starter `.gitignore` for Python:

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

Commit the `.gitignore` itself — that way every collaborator inherits the
same exclusions.

## Creating a GitHub Repository

**GitHub** is a hosting service for Git repositories. It is *not* Git
itself — Git is the underlying tool; GitHub is a place to put copies of
your repos so others (or future-you on another machine) can access them.

To publish your local repo:

1. Sign up at <https://github.com/> if you don't have an account.
2. Click the **+** icon in the top-right and choose **New repository**.
3. Name it (for example, `code-crunch-week-01`), leave it **public**, and
   **do not** check "Initialize this repository with a README" — your
   local repo already has files in it.
4. Click **Create repository**. GitHub will show you a page with the
   instructions you need next.

## Connecting Local to GitHub

In your local project, tell Git where the remote copy lives. GitHub calls
this URL the *origin*.

```bash
git remote add origin https://github.com/your-username/code-crunch-week-01.git
```

Verify:

```bash
git remote -v
```

```text
origin  https://github.com/your-username/code-crunch-week-01.git (fetch)
origin  https://github.com/your-username/code-crunch-week-01.git (push)
```

## Pushing Your First Commit

A **push** uploads your local commits to the remote. The first time, use
the `-u` flag to set up tracking so future pushes can be just `git push`:

```bash
git push -u origin main
```

GitHub will ask for your username and a **personal access token** (not
your password — GitHub disabled password authentication in 2021). Create
one at
<https://github.com/settings/tokens> and copy it into the prompt. You'll
only need to do this once per machine; the token is cached.

Refresh your repository page on GitHub. Your `hello.py` is now live and
shareable.

## Cloning an Existing Repository

When you want a local copy of someone else's repository — or your own from
another machine — use `git clone`:

```bash
git clone https://github.com/your-username/code-crunch-week-01.git
cd code-crunch-week-01
```

`git clone` creates a new folder, downloads the full history, and sets
`origin` for you automatically.

## A Complete Day-One Workflow

Putting all of Week 1 together, here's the canonical workflow for a brand-
new project:

```bash
mkdir hello-you
cd hello-you
git init
python -m venv .venv
source .venv/bin/activate
printf '.venv/\n__pycache__/\n.DS_Store\n' > .gitignore
printf 'print("Hello, world!")\n' > hello.py
git add .gitignore hello.py
git commit -m "Initial commit: project skeleton"
git remote add origin https://github.com/your-username/hello-you.git
git push -u origin main
```

That's the loop you'll repeat for every new project from now until you
retire.

## Common Pitfalls

- **Committed `.venv/` by accident.** Add it to `.gitignore`, then run
  `git rm -r --cached .venv` to untrack it, and commit again.
- **Pushed a secret (API key, password).** Treat it as compromised the
  moment it hits GitHub. Rotate the secret immediately; rewriting Git
  history is a topic for a later week.
- **`git push` says "rejected".** Someone (or another machine) pushed
  changes you don't have. Run `git pull --rebase` first, resolve any
  conflicts, then push again.
- **You forgot to set your remote.** `git remote add origin <url>` is a
  per-repository step. If you skipped it, `git push` has nowhere to go.

## Recap

You can now:

- Explain what version control is and why every project should use it.
- Configure Git globally with your name and email.
- Initialize a repository, stage changes, and commit them with `git add`
  and `git commit`.
- Write a clear, conventional commit message.
- Use `.gitignore` to keep junk out of your repo.
- Create a GitHub repository, connect it as `origin`, and push your first
  commit.
- Clone an existing repository onto a new machine.

That's everything you need to share the Week 1 mini-project — "Hello, You"
— with the world.
