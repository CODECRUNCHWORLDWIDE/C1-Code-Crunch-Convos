# Git Commands Cheatsheet

## Setup (once per machine)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## Daily loop

```bash
git pull                           # get latest from remote
git status                         # what changed?
git diff                           # show unstaged changes
git diff --staged                  # show staged changes
git add <file>                     # stage a file
git add .                          # stage everything
git commit -m "Message"            # commit
git push                           # send to remote
```

## Branches

```bash
git branch                         # list local branches
git branch -a                      # list all (incl. remote)
git checkout -b feature/foo        # create + switch to branch
git checkout main                  # switch to existing branch
git switch main                    # newer alternative to checkout
git merge feature/foo              # merge a branch into current
git branch -d feature/foo          # delete merged branch
git branch -D feature/foo          # force-delete (careful)
```

## History

```bash
git log                            # full history
git log --oneline -10              # last 10 as one-liners
git log --graph --oneline --all    # tree view
git show <hash>                    # detail of one commit
git blame <file>                   # who wrote each line
```

## Undo

```bash
git restore <file>                 # discard unstaged changes
git restore --staged <file>        # unstage (keep changes)
git reset --soft HEAD~1            # undo last commit, keep changes staged
git reset --mixed HEAD~1           # undo last commit, keep changes unstaged
git reset --hard HEAD~1            # ⚠️ DESTROY last commit
git revert <hash>                  # safe undo via a new commit
```

## Stash (temporarily set aside changes)

```bash
git stash                          # save current uncommitted changes
git stash pop                      # reapply most recent stash
git stash list                     # see stashes
```

## Remotes

```bash
git remote -v                      # list remotes
git remote add origin <url>        # add a remote
git push -u origin <branch>        # push and set upstream
git fetch                          # download remote refs without merging
git pull                           # = fetch + merge
```

## Inspect

```bash
git diff <branch1> <branch2>       # compare branches
git log --author="Name"            # commits by an author
git log -p <file>                  # history of a specific file
git log --since="2 weeks ago"
```

## Tags (release markers)

```bash
git tag v1.0.0
git tag -a v1.0.0 -m "Release 1.0" # annotated
git push origin v1.0.0             # push a tag
```

## .gitignore essentials for Python

```text
__pycache__/
*.pyc
.venv/
.env
.pytest_cache/
.coverage
*.sqlite3
.DS_Store
```

## Help

```bash
git help <command>                 # full docs
git <command> --help               # same
git <command> -h                   # short summary
```

## Official docs

- <https://git-scm.com/doc>
- <https://docs.github.com/>
