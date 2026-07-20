# Git & GitHub Workflow

A practical guide to the Git habits you'll build over the bootcamp. By Week 15 these should be muscle memory.

> 📚 **Official references**
>
> - [Git documentation](https://git-scm.com/doc)
> - [GitHub Docs](https://docs.github.com/)
> - [Pro Git book](https://git-scm.com/book/en/v2) — free, comprehensive

---

## The mental model

Git tracks **snapshots** of your project. Every commit is a snapshot. You move between snapshots, compare them, and combine them.

```text
working dir  ──add──►  staging area  ──commit──►  local repo  ──push──►  GitHub
     ▲                                                  │
     └─────────────────────────────────────checkout─────┘
```

- **Working directory** — the files you see and edit.
- **Staging area** — files you've marked to include in the next commit.
- **Local repo** — your history of commits, stored in `.git/`.
- **Remote (GitHub)** — a copy of your repo hosted online.

---

## Daily workflow

Use this loop every coding session.

```bash
# 1. Start: pull the latest from GitHub
git pull

# 2. Edit your files.

# 3. See what changed
git status            # which files are modified?
git diff              # what specifically changed?

# 4. Stage and commit
git add path/to/file.py
git commit -m "Add greeting function"

# 5. Push to GitHub
git push
```

That's 80% of what you'll do. The rest is variations.

---

## One-time setup (per machine)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false        # use merge on pull
```

## Starting a new project

```bash
mkdir my-project && cd my-project
git init
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"
# create the repo on GitHub, then:
git remote add origin git@github.com:you/my-project.git
git push -u origin main
```

## Cloning an existing project

```bash
git clone https://github.com/owner/repo.git
cd repo
```

## Branching

Always work on a branch, never directly on `main`.

```bash
git checkout -b feature/add-greeting
# ... make changes ...
git add . && git commit -m "Add greeting function"
git push -u origin feature/add-greeting
```

Then open a Pull Request on GitHub. After it's merged:

```bash
git checkout main
git pull
git branch -d feature/add-greeting
```

## Writing good commit messages

A commit message answers: **what changed, and why?**

```text
Add greeting function for new users

The signup flow currently redirects to a blank dashboard. This adds
a `greet_user()` helper that returns a personalized welcome string,
which the dashboard template will use next.
```

Rules of thumb:

- **Subject line** ≤ 50 characters, imperative mood ("Add", "Fix", not "Added", "Fixes").
- **Blank line** between subject and body.
- **Body** explains the why if it's not obvious from the diff.

## Common situations

### Oops, I committed to the wrong branch

```bash
git log --oneline -5            # find the commit hash
git checkout correct-branch
git cherry-pick <hash>
git checkout wrong-branch
git reset --hard HEAD~1         # CAREFUL: removes the commit
```

### I want to undo my last commit but keep the changes

```bash
git reset --soft HEAD~1
```

### I want to throw away local changes to a file

```bash
git checkout -- path/to/file
```

### I want to see who wrote which line

```bash
git blame path/to/file.py
```

### Merge conflict during pull/merge

When Git can't auto-merge, it marks conflicts in the file:

```text
<<<<<<< HEAD
your version
=======
their version
>>>>>>> branch-name
```

Open the file, pick what you want, remove the markers, then:

```bash
git add path/to/conflicted-file
git commit
```

---

## Pull request etiquette

For every PR you open in this bootcamp (or in industry):

- **One logical change per PR.** Easier to review.
- **Self-review before requesting review.** Read your own diff.
- **Title** says what the PR does. **Description** explains why.
- **Link the issue** if there is one ("Closes #42").
- **Respond to feedback** promptly — don't take it personally.

---

## SSH vs HTTPS

You'll be asked to authenticate when pushing.

- **HTTPS** — easier to set up; uses a [Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) as a password.
- **SSH** — more convenient long-term. [Set up SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

Pick one, set it up once, forget about it.

---

## Cheatsheet

See [cheatsheets/git-commands.md](cheatsheets/git-commands.md) for a one-page reference.
