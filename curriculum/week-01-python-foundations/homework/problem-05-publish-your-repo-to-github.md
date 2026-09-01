# Homework Problem 5 — Publish Your Repo to GitHub

> **Topic:** remotes, `git push -u`, personal access tokens, and the rejected-push error everybody meets once
> **Lecture:** [Lecture 3 — Git and GitHub Basics](../lecture-notes/03-git-and-github-basics.md)
> **Difficulty:** Beginner
> **Target time:** 1 hour
> **Why this one:** up to now your work exists in one place, on one machine, and a spilled drink ends it. This is the step that turns it into something that exists somewhere else and that other people can read.

<!-- no-runnable-file: publishing needs a GitHub account, a credential only you hold, and a network connection. A script cannot create your repository, cannot hold your token, and must not push on your behalf. -->

## The Brief

Take the local repository you built in Problems 2, 3 and 4 and put a copy
on GitHub, at a public address anybody can read.

Two halves, and it matters that they stay separate in your head:

**A repository on GitHub** is just another copy of your project. GitHub
does not run anything, does not check anything, and has no special powers.
It is a copy that lives on a computer that is always switched on.

**A remote** is a nickname your local repository keeps for the address of
that copy. Adding one contacts nobody. It writes four lines into a config
file. The first time anything actually travels is when you push.

Then you push, and you meet the credential question. GitHub stopped
accepting account passwords over HTTPS on 13 August 2021. You will use a
**personal access token** instead: a long random string you generate,
scoped to just what it needs to do, that you can throw away without
touching your account.

## Starter

Create the repository on GitHub first, in a browser:

1. Click **+** in the top right, choose **New repository**.
2. Name it `week-01-homework`. Visibility: **Public**.
3. Description: `Code Crunch Convos — Week 1 homework`.
4. Leave *Add a README file*, *Add .gitignore* and *Choose a license* all
   **unchecked**.
5. Click **Create repository**.

Step 4 is not a style preference. Your local repository already has
commits in it. If GitHub also makes a commit, the two histories have
nothing in common and your first push is rejected. The exact error, and
the fix, are in Common bugs to catch.

Then, in your project folder:

```bash
git remote add origin https://github.com/your-username/week-01-homework.git
git push -u origin main
```

## Requirements

1. A public repository named `week-01-homework` exists on GitHub under
   your account.
2. Its front page shows `about_me.py`, `.gitignore` and
   `requirements.txt`, and does **not** show `.venv/`.
3. Its history contains at least two commits.
4. The first line of the repository's README, or its description, names
   this course: `Code Crunch Convos — Week 1 homework`.
5. You authenticated with a personal access token, not an account
   password.

## Constraints

- **Do not tick any of GitHub's "initialize this repository with" boxes.**
  See the Starter. This is the single most common Week 1 failure.
- **Use a token, never your password.** Password authentication over
  HTTPS was switched off in 2021. A token is a separate credential with
  its own permissions and its own expiry date, and revoking it costs you
  nothing.
- **Scope the token as narrowly as it will go.** A fine-grained token,
  limited to this one repository, with *Contents: Read and write*, is the
  least privilege that can do the job. Anything wider is a bigger
  accident waiting to happen.
- **Never put a token in a file.** Paste it at the terminal prompt, and
  nowhere else. A token committed to a public repository is a token that
  is already being used by somebody else.
- **Do not reach for `git push --force`.** It works, and it silently
  destroys whatever was on the other end. Today that would be a
  throwaway README, which is exactly what makes this a dangerous place to
  learn the habit.

## Expected output

Real output. Adding the remote says nothing at all, which is itself worth
seeing:

```text
$ git remote add origin https://github.com/your-username/week-01-homework.git
$ git remote -v
origin  https://github.com/your-username/week-01-homework.git (fetch)
origin  https://github.com/your-username/week-01-homework.git (push)
$ git log --oneline
87df03f Add about_me.py and day_planner CLI
8595108 Initial commit: project skeleton with venv and gitignore
$ git push -u origin main
branch 'main' set up to track 'origin/main'.
To https://github.com/your-username/week-01-homework.git
 * [new branch]      main -> main
```

> That push transcript is real output from a push to a local bare
> repository standing in for GitHub, so the wording is exactly what Git
> prints. The one thing no transcript can show you is the credential
> prompt, because what appears there depends on which credential helper
> your machine has installed.

## Steps

1. Create the empty public repository on GitHub, following the Starter.
2. Generate a token at <https://github.com/settings/tokens>. Fine-grained,
   this repository only, *Contents: Read and write*. Copy it once — GitHub
   will not show it to you again.
3. In `week-01-homework`, add the remote and check it with
   `git remote -v`.
4. Make sure you have at least two commits and a README whose first line
   names the course. If your work so far is one commit, this is the moment
   to commit `about_me.py` and `requirements.txt`.
5. `git push -u origin main`.
6. At the prompt, your username is your GitHub username and your password
   is the token.
7. Reload the repository page in your browser. Check the file list, check
   the commit count, check that it does not say `Private` next to the
   name.

## The Solution

**On GitHub**, in a browser: create a new **public** repository called
`week-01-homework`, description `Code Crunch Convos — Week 1 homework`,
with *Add a README file*, *Add .gitignore* and *Choose a license* all left
unchecked.

**On your machine**, in `week-01-homework/`:

```bash
git remote add origin https://github.com/your-username/week-01-homework.git
git remote -v
```

```text
origin  https://github.com/your-username/week-01-homework.git (fetch)
origin  https://github.com/your-username/week-01-homework.git (push)
```

Make sure you have at least two commits and a README whose first line
names the course:

```bash
printf 'Code Crunch Convos - Week 1 homework\n' > README.md
git add README.md about_me.py requirements.txt
git commit -m "Add about_me.py and day_planner CLI"
git log --oneline
```

```text
87df03f Add about_me.py and day_planner CLI
8595108 Initial commit: project skeleton with venv and gitignore
```

Push:

```bash
git push -u origin main
```

```text
branch 'main' set up to track 'origin/main'.
To https://github.com/your-username/week-01-homework.git
 * [new branch]      main -> main
```

When prompted, the **username** is your GitHub username and the
**password** is a **personal access token** from
<https://github.com/settings/tokens>. Generate a fine-grained token scoped
to this one repository with *Contents: Read and write*. Treat it like a
password: it goes into the terminal prompt and nowhere else.

**Why it works.**

**A remote is a name for an address, and nothing more.**
`git remote add origin <url>` writes four lines into `.git/config`. It
contacts nothing and checks nothing. You can point a remote at an address
that does not exist and Git will not complain until you try to use it.
`origin` is only a convention — the customary name for "where this came
from" — and a repository can have as many remotes as you like.

**`-u` is why every later push is one word.** It records that your local
`main` follows `origin/main`. After that, a bare `git push` and a bare
`git pull` know what you meant, and `git status` starts telling you useful
things like `Your branch is ahead of 'origin/main' by 1 commit`. Read the
first line of the push output again — that is `-u` reporting what it did.

**`* [new branch] main -> main` is the success message.** Git is terse
when things work. The `*` marks a branch that did not exist on the other
end before. A later push of more commits prints a range instead, like
`c5ab292..2364db9  main -> main`, telling you exactly which commits moved.

**Nothing you push can contain `.venv/`,** because a push sends commits,
and `.venv/` was never committed. The requirement about `.venv/` not
appearing on GitHub is already satisfied by Problem 2's `.gitignore`.
Getting the ignore rules right early means the later steps have nothing
left to get wrong.

## Download and run

There is no file to download. Publishing needs an account only you have, a
credential only you hold, and a network connection — a script cannot do
any of it on your behalf, and should not try.

The check that matters does not use your machine at all. Clone your own
repository into a temporary folder, the way a stranger would:

```bash
cd /tmp
git clone https://github.com/your-username/week-01-homework.git check
ls -a check
```

You should see `.gitignore`, `README.md`, `about_me.py` and
`requirements.txt` — and no `.venv`. If the clone asks you for
credentials, the repository is not public. Delete `/tmp/check` when you
are done.

## Common bugs to catch

- **You ticked "Add a README file", and the push was rejected.**

  ```text
  To https://github.com/your-username/week-01-homework.git
   ! [rejected]        main -> main (fetch first)
  error: failed to push some refs to 'https://github.com/your-username/week-01-homework.git'
  hint: Updates were rejected because the remote contains work that you do not
  hint: have locally. This is usually caused by another repository pushing to
  hint: the same ref. If you want to integrate the remote changes, use
  hint: 'git pull' before pushing again.
  hint: See the 'Note about fast-forwards' in 'git push --help' for details.
  ```

  Nobody else pushed. GitHub made a commit on your behalf when it created
  that README, and your history does not contain it. The fix, exactly:

  ```bash
  git pull --rebase origin main
  git push -u origin main
  ```

  ```text
  From https://github.com/your-username/week-01-homework
   * branch            main       -> FETCH_HEAD
   * [new branch]      main       -> origin/main
  Successfully rebased and updated refs/heads/main.
  branch 'main' set up to track 'origin/main'.
  To https://github.com/your-username/week-01-homework.git
     c5ab292..2364db9  main -> main
  ```

  `--rebase` replays your commits on top of GitHub's rather than tying the
  two together with a merge commit, so a brand-new repository does not
  begin its life with a merge in it. Notice the push output is now a
  range, not `[new branch]` — the branch already existed on the far end.
- **You pasted your account password.**

  ```text
  remote: Support for password authentication was removed on August 13, 2021.
  fatal: Authentication failed for 'https://github.com/your-username/week-01-homework.git/'
  ```

  Generate a token. If your machine cached a wrong credential, clear it —
  `git credential-manager erase` on Windows, or delete the `github.com`
  entry from Keychain Access on macOS.
- **`error: remote origin already exists.`** You ran `git remote add`
  twice. You wanted `git remote set-url origin <url>`. `add` creates;
  `set-url` changes. This bites when you are fixing a typo in the address.
- **The repository is private and you did not notice.** GitHub's create
  form remembers your last choice, so a private repository you made months
  ago quietly makes this one private too. Look for the `Private` badge
  next to the name, or check *Settings → General → Danger Zone → Change
  repository visibility*.
- **`error: src refspec main does not match any`.** Your branch is called
  something else, almost certainly `master`, or you have no commits yet.
  `git branch -M main` renames it; `git log --oneline` tells you whether
  there is anything to push.
- **You committed a token or an API key.** Treat it as compromised the
  second it lands and revoke it at <https://github.com/settings/tokens>.
  Deleting the file in a later commit does not help: the old commit is
  still in the history and still readable. Rewriting history is a much
  later topic; revoking the credential takes ten seconds and actually
  solves the problem.

## Under the hood

<details>
<summary>Under the hood — what git push actually sends, and what a branch really is</summary>

Problem 2's Under the hood explained what a commit is: an object named by
the hash of its own contents, pointing at a tree and at its parent. A push
is the natural consequence of that design.

**A branch is a file containing one hash.** Look:

```bash
cat .git/refs/heads/main
```

```text
87df03f4a1c9e5b2d8f0a3c6e9b1d4f7a2c5e8b0
```

That is the entire implementation of `main`. Not a copy of your project,
not a folder — forty characters naming the newest commit. Committing means
writing a new object and then rewriting that one line. This is why
creating and deleting branches in Git is instant, and why other version
control systems that copy whole trees feel so different.

**A push is a negotiation, then a transfer.** Your Git and the far end
compare which commit hashes each already has, and only the missing objects
travel, packed together. Then the far end updates its own
`refs/heads/main` to point at your newest commit.

**"Fast-forward" is the rule that protects you.** A push is allowed when
the far end's current commit is an ancestor of the one you are sending —
that is, when your history already contains everything theirs does, and
just goes further. Then updating the pointer loses nothing.

The rejection in Common bugs to catch happens when that is not true.
GitHub's auto-created README commit is not an ancestor of anything you
have, so accepting your pointer would make that commit unreachable, and
Git refuses. `--force` means "do it anyway", which is exactly the
unreachable-commit outcome the rule exists to prevent.

`git pull --rebase` fixes it properly: it takes your commits off, moves
your branch to theirs, and replays yours on top. Your commits get new
hashes — a rebased commit has a different parent, and the parent's hash is
part of what the child's hash is computed from — and now their commit
really is an ancestor of yours, so the push is a fast-forward and is
allowed.

**Tracking is two more lines of config.** `-u` writes them:

```bash
git config --get branch.main.remote
git config --get branch.main.merge
```

```text
origin
refs/heads/main
```

That is all "upstream" means. `git status` reads those two values to work
out what "ahead by 1 commit" is measured against.

</details>

<details>
<summary>Under the hood — why tokens replaced passwords, and what a credential helper does with them</summary>

A password is one secret that opens everything you own, forever, and you
cannot tell where it has been used. A token is a different shape of thing:

- **Scoped.** A fine-grained token can be limited to one repository and to
  reading and writing file contents, and nothing else. It cannot delete
  the repository or change your account.
- **Expiring.** You choose a lifetime. A leaked token stops working on its
  own.
- **Revocable in isolation.** Deleting one token breaks nothing else you
  own. Changing a password logs out everything.
- **Auditable.** GitHub records when each token was last used, so you can
  see one being used from somewhere you have never been.

That is why the change happened in 2021, and it is the same reasoning
behind API keys everywhere else you will meet them.

**Where does the token go after you type it?** Not into the repository —
`.git/config` stores the address, never the credential. Git hands the
question to a **credential helper**, an external program:

```bash
git config --get credential.helper
```

On Windows that is usually `manager`, which stores the token in Windows
Credential Manager. On macOS it is `osxkeychain`, which uses the system
Keychain. On Linux it varies, and `store` — which writes the token in
plain text to `~/.git-credentials` — is common and is worth knowing about
precisely so you can avoid choosing it by accident.

When a helper caches the wrong credential, no amount of retyping helps,
because Git stops asking. That is why the fix in Common bugs to catch is
to erase the cached entry rather than to try again.

**SSH keys are the other road.** Instead of a secret you type, you have a
key pair: a private half that never leaves your machine and a public half
you paste into GitHub. There is no prompt at all, ever. It is in Stretch,
and once you have set it up once you will not go back.

</details>

## Acceptance checklist

- [ ] A **public** repository named `week-01-homework` exists on GitHub
      under your account.
- [ ] `git remote -v` shows `origin` pointing at it, for both fetch and
      push.
- [ ] `git log --oneline` shows at least two commits, and the same
      commits appear on GitHub.
- [ ] The repository page lists `about_me.py`, `.gitignore` and
      `requirements.txt`, and no `.venv`.
- [ ] The README's first line, or the repository description, reads
      `Code Crunch Convos — Week 1 homework`.
- [ ] You authenticated with a token, and the token is not in any file in
      the repository.
- [ ] Cloning the repository into a temporary folder works without a
      credential prompt.

## Stretch

- Switch from HTTPS and a token to SSH keys:

  ```bash
  ssh-keygen -t ed25519 -C "you@example.com"
  cat ~/.ssh/id_ed25519.pub          # paste into github.com/settings/keys
  ssh -T git@github.com
  git remote set-url origin git@github.com:your-username/week-01-homework.git
  git push
  ```

  `ssh -T git@github.com` should answer:

  ```text
  Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
  ```

  That message *is* the success case, despite reading like a refusal.
  Choose `ed25519` over RSA because the keys are shorter and faster and
  GitHub has recommended it for years. The private half —
  `~/.ssh/id_ed25519`, the one with no `.pub` — never leaves your machine
  and never gets pasted anywhere.
- Add a real README. Say what the repository is, how to create the
  environment, and how to run `about_me.py`. Write it for somebody who
  has never met you, because on a public repository that is who is
  reading.
- Look at your own repository through the API instead of the web page:
  `curl https://api.github.com/repos/your-username/week-01-homework` and
  find the `private` field. That is the same fact the badge on the page
  shows, from the machine's side.

Next: [Homework Problem 6 — Combine Everything with a Small CLI](./problem-06-combine-everything-with-a-small-cli.md).
