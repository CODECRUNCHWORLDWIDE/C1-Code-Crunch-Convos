# Week 1 Homework

Six problems that walk you from "I think Python is installed" to "here is
a public repository with my first program in it". The whole set takes
about **6 hours**. Unlike the exercises, these are not independent — each
one builds on the folder the one before it created, so work them in
order.

## How to Work a Problem

Each problem below is a page, not a program. The page gives you the brief,
a starter to copy, the exact output to expect, the full worked answer, and
the mistakes to watch for. You do the typing.

1. Open a terminal.
2. Activate your Week 1 virtual environment — Problem 2 is where you
   create it.
3. Read the whole page before you type anything. The Constraints section
   is short and it is where the traps are named.
4. Do the work, then compare against **The Solution**.
5. Tick every box in the page's acceptance checklist honestly.
6. Commit. Every problem should leave at least one commit behind in your
   `week-01-homework` repository that you can point at later.

Problems 3 and 6 end in a real script, and each ships the finished `.py`
beside its page under **Download and run**. The other four are terminal
and Git work — verifying an install, building an environment, freezing
dependencies, publishing to GitHub — so there is no file to download.
Those pages say so, and give you the commands that check your work
instead.

## Index

| # | Problem | What you'll practice | Difficulty | Est. time |
|---|---------|----------------------|-----------:|----------:|
| 1 | [problem-01-verify-your-install.md](./problem-01-verify-your-install.md) | Proving `python` reaches a real 3.11+, and saving the proof | Beginner | 30 min |
| 2 | [problem-02-project-skeleton-with-a-venv.md](./problem-02-project-skeleton-with-a-venv.md) | `git init`, `python -m venv`, and a `.gitignore` written in the right order | Beginner | 45 min |
| 3 | [problem-03-a-tiny-script-with-comments-and-a-docstring.md](./problem-03-a-tiny-script-with-comments-and-a-docstring.md) | Docstrings, comments, constants, type hints, the `__main__` guard | Beginner | 45 min |
| 4 | [problem-04-install-and-freeze-a-package.md](./problem-04-install-and-freeze-a-package.md) | `pip install`, `pip freeze`, and rebuilding an environment from a file | Beginner | 45 min |
| 5 | [problem-05-publish-your-repo-to-github.md](./problem-05-publish-your-repo-to-github.md) | Remotes, `git push -u`, tokens, and the rejected-push error | Beginner | 1 h |
| 6 | [problem-06-combine-everything-with-a-small-cli.md](./problem-06-combine-everything-with-a-small-cli.md) | `input()`, `.strip()`, `enumerate`, and shipping the result | Beginner | 1 h 45 min |

**Total: about 6 hours.**

## Checking Your Work

There is no automated grader for Week 1. For each problem, satisfy
yourself that:

- The commands ran without an error you had to ignore.
- The output matches the page's **Expected output** section.
- Every box in the page's acceptance checklist is honestly ticked.
- The work is committed, and — from Problem 5 onwards — pushed.

When all six are done, finish
[the Week 1 mini-project](../mini-project/README.md) and take
[the quiz](../quiz.md).
