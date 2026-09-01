# Homework Problem 4 — Install and Freeze a Package

> **Topic:** `pip install`, `pip freeze`, `requirements.txt`, and proving an environment can be rebuilt from a file
> **Lecture:** [Lecture 2 — Terminal, Virtual Environments, and pip](../lecture-notes/02-terminal-virtual-environments-and-pip.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** an environment nobody can rebuild is a machine you are not allowed to lose. This problem turns tens of megabytes of installed packages into one small committed file that anybody, anywhere, can turn back into the same environment.

<!-- no-runnable-file: this problem installs packages from the internet into your virtual environment and then deletes and rebuilds that environment. A script doing it would need a network connection and would change the machine that ran it, which is not something a page should do to a reader. -->

## The Brief

With the environment from Problem 2 switched on, install a package called
`requests`, then write down exactly what you ended up with.

`requests` is the library almost everybody uses to fetch things over the
web. You will use it properly in Week 8. Today it is a stand-in for "a
thing that is not built into Python", because installing it teaches three
separate lessons at once.

**Lesson one: you never install just one thing.** `requests` needs four
other packages to do its job. pip works that out for you and installs
them too.

**Lesson two: a list of what you installed is not the same as a list of
what you have.** `pip freeze` writes down the *exact* version of
*everything* in the environment. That file is a recipe. Hand somebody the
recipe and they can bake the same cake.

**Lesson three: the packages live in a folder, not in your shell.** You
will switch the environment off, switch it back on, and prove the package
survived. It never went anywhere. All that changed was which Python your
terminal reaches for.

## Starter

Nothing to paste into a file. Four commands, run in `week-01-homework`
with your environment active — your prompt should show `(.venv)`:

```bash
python -m pip install requests
python -m pip freeze > requirements.txt
deactivate
```

Then activate again and check:

```bash
python -c "import requests; print(requests.__version__)"
```

## Requirements

1. `python -m pip install requests` finishes without an error.
2. A file `requirements.txt` exists in the project root and has at least
   one line in it.
3. `requirements.txt` was produced by `pip freeze`, not typed by hand.
4. `requirements.txt` is committed to Git.
5. After `deactivate` and re-activating,
   `python -c "import requests; print(requests.__version__)"` prints a
   version number.

## Constraints

- **Activate the environment first, every time.** Installing without
  activating still succeeds — that is exactly what makes the mistake so
  easy to miss — but the package lands in your system-wide Python, and
  then `requirements.txt` becomes a snapshot of your whole computer. The
  tell is a `requirements.txt` with thirty lines in it when you installed
  one package.
- **Write `python -m pip`, not bare `pip`.** They are usually the same
  program and occasionally are not. `pip` is found through your `PATH`;
  `python -m pip` is found through the interpreter you are already
  running. On a machine with several Pythons they can disagree, and the
  failure is the nasty kind: pip says it succeeded, and `import requests`
  then says the module does not exist.
- **Do not hand-edit `requirements.txt`.** The value of `freeze` is that
  it reports what is *actually installed*. The moment you type a version
  in by hand, the file stops being an observation and becomes a claim.
- **Commit `requirements.txt`, never `.venv/`.** They are alternatives,
  not companions. One is about 120 bytes and describes the environment;
  the other is tens of megabytes of files compiled for your processor and
  your operating system, useless to anybody else.

## Expected output

Real output. Versions move on; the shape does not.

```text
$ python -m pip install requests
Installing collected packages: urllib3, idna, charset_normalizer, certifi, requests
Successfully installed certifi-2026.7.22 charset_normalizer-3.5.1 idna-3.19 requests-2.34.2 urllib3-2.7.0
$ python -m pip freeze > requirements.txt
$ cat requirements.txt
certifi==2026.7.22
charset-normalizer==3.5.1
idna==3.19
requests==2.34.2
urllib3==2.7.0
$ deactivate
$ source .venv/bin/activate
$ python -c "import requests; print(requests.__version__)"
2.34.2
```

Read the install line once more. You asked for one package and five
arrived, with `requests` last, because pip installs what a package needs
before it installs the package.

## Steps

1. `cd week-01-homework` and activate the environment. Confirm with
   `python -c "import sys; print(sys.prefix != sys.base_prefix)"` — it
   must print `True` before you install anything.
2. `python -m pip install requests`. Read the last two lines of output.
3. `python -m pip freeze > requirements.txt`, then open the file and look
   at it.
4. Commit it.
5. `deactivate`. Your prompt loses the `(.venv)` marker.
6. Activate again.
7. `python -c "import requests; print(requests.__version__)"` and check
   the number matches the one in `requirements.txt`.

## The Solution

With the environment from Problem 2 **activated**:

```bash
python -m pip install requests
```

The last lines of real output:

```text
Installing collected packages: urllib3, idna, charset_normalizer, certifi, requests
Successfully installed certifi-2026.7.22 charset_normalizer-3.5.1 idna-3.19 requests-2.34.2 urllib3-2.7.0
```

Freeze it. Do not write it:

```bash
python -m pip freeze > requirements.txt
cat requirements.txt
```

```text
certifi==2026.7.22
charset-normalizer==3.5.1
idna==3.19
requests==2.34.2
urllib3==2.7.0
```

Commit it:

```bash
git add requirements.txt
git commit -m "Add requirements.txt with requests"
```

Now the round trip the problem actually cares about — switch the
environment off, switch it back on, and prove the package survived:

```bash
deactivate
source .venv/bin/activate      # or .venv\Scripts\Activate.ps1 on Windows
python -c "import requests; print(requests.__version__)"
```

```text
2.34.2
```

**Why it works.**

**One request, five packages.** `requests` leans on `urllib3` to hold
network connections open, `idna` to handle domain names written in
alphabets other than the Latin one, `charset-normalizer` to guess what
character encoding a web page came back in, and `certifi` for the list of
authorities whose security certificates are trusted. pip works out that
whole chain and installs the deepest parts first. Five packages from one
command, into a folder you can delete without consequence, is the
argument for virtual environments delivered as a receipt.

**`pip freeze` and `pip list` are not the same command wearing different
clothes.** `pip list` shows `pip` itself; `pip freeze` does not. That is
deliberate. `freeze` produces a file meant to be fed back into
`pip install -r`, and pinning pip's own version inside pip's own input
file starts an argument about which comes first. `list` is for a human
looking at an environment; `freeze` is for a machine rebuilding one.

**The `==` is the whole point.** `requests==2.34.2` means *this exact
version*, which is what turns the file into a reproduction recipe instead
of a wish list. Under the hood goes into what the alternatives cost you.

**`>` is your shell, not pip.** `pip freeze` prints to the screen like any
other program; the shell catches that output and puts it in a file. `>>`
would add to the end instead of replacing, which is how people end up with
a `requirements.txt` containing the same five lines four times.

**Deactivating proves the packages are in the folder, not in the shell.**
Activation only reorders your `PATH`. The packages sat in
`.venv/lib/python3.13/site-packages/` the entire time and never moved.
That is why the round trip works, and equally why the whole folder can be
thrown away and rebuilt from the committed file with no ceremony.

**`requests.__version__` rather than `pip show requests`.** The first is
read from the package that the *running interpreter* actually imported;
the second reads installation paperwork. If they ever disagree you have
found a genuinely interesting problem, and the import is the one telling
you the truth about what your code will use.

## Download and run

There is no file to download. Running one would mean downloading packages
from the internet onto your machine and rewriting your environment, which
is a decision that belongs to you and your terminal, not to a page.

The check that proves your work is a rebuild from nothing but the
committed file. Do it in a throwaway environment so a mistake costs you
nothing:

```bash
python -m venv /tmp/rebuild
/tmp/rebuild/bin/python -m pip install -q -r requirements.txt
/tmp/rebuild/bin/python -c "import requests; print(requests.__version__)"
```

```text
2.34.2
```

Same version, a different environment, built from a file. That is what
"reproducible" means. Delete `/tmp/rebuild` afterwards. On Windows, use
`$env:TEMP\rebuild` and `\Scripts\python.exe`.

## Common bugs to catch

- **`error: externally-managed-environment`.**

  ```text
  error: externally-managed-environment

  × This environment is externally managed
  ╰─> To install Python packages system-wide, try apt install
      python3-xyz, where xyz is the package you are trying to
      install.
  ```

  You are installing into the system Python on macOS or Linux, and the
  operating system is protecting its own Python from you. The answer is
  never `--break-system-packages`. The answer is to activate your virtual
  environment.
- **`ModuleNotFoundError: No module named 'requests'` right after a
  successful install.** Bare `pip` installed into a different interpreter
  than the one running your code. Use `python -m pip` and try again.
- **`bash: .venv/bin/activate: No such file or directory` on Windows.**
  The layout differs by platform: `.venv/bin/` on macOS and Linux,
  `.venv\Scripts\` on Windows. In PowerShell the command is
  `.venv\Scripts\Activate.ps1`.
- **PowerShell refuses to run the activate script.** That is the execution
  policy. Lecture 2's one-time
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
  is the documented fix.
- **`requirements.txt` has thirty lines in it.** You froze your system
  Python. Delete the file, activate the environment, freeze again.
- **`requirements.txt` shows the same lines several times.** You used `>>`
  where you meant `>`.

## Under the hood

<details>
<summary>Under the hood — why requirements.txt pins versions, and what == versus >= costs you</summary>

A dependency line is a promise about which versions are acceptable. There
are three common spellings and they buy very different things.

**`requests` — no version at all.** "Whatever is current when you install
this." Cheap to write, and it means two people installing on two different
days get two different programs. Every "works on my machine" story starts
here.

**`requests>=2.34` — a floor.** "This version or anything newer." It says
something true and useful: your code needs a feature that arrived in
2.34. What it cannot say is which future version will break you.
Maintainers do not know in advance which change will be the one that
matters to your code, so a floor is an open-ended bet that nothing ahead
of you will ever be wrong. Sooner or later that bet loses, and it loses on
a day you were not touching that code, which makes it maximally
confusing.

**`requests==2.34.2` — a pin.** "Exactly this." A rebuild in six months
produces the same bytes as a rebuild today. The cost is real: nothing
updates until you deliberately update it, so security fixes do not arrive
on their own and the pins go stale. You have swapped surprise for
maintenance, which is the correct trade for anything you have to be able
to reproduce.

The two-file convention most projects settle on splits the difference:

- Loose ranges in `pyproject.toml` describe what your code *needs*, for
  people who install it as a library.
- Exact pins in `requirements.txt` describe what you *tested*, for
  rebuilding a working environment.

`pip freeze` writes the second kind, always, because it is not guessing —
it is reporting what is on disk right now.

There is a limit worth knowing about. A pin fixes the version number, not
the file. Version numbers can, in unusual circumstances, be reused or
replaced upstream. Tools that need certainty go further and record a hash
of each downloaded file, so a changed file is refused outright:

```text
requests==2.34.2 \
    --hash=sha256:...
```

That is what `pip-tools`, Poetry's lock file, and `uv` are for. You do not
need them this week. You need to know that "pinned" and "verified" are two
different levels of certainty, and `requirements.txt` gives you the first.

One more thing the file cannot capture: it lists packages, not the Python
version, not your operating system, and not compiled extensions built for
a particular processor. A `requirements.txt` from a Windows machine can
fail on Linux for reasons that have nothing to do with the file. That is
where containers come in, much later.

</details>

<details>
<summary>Under the hood — where pip actually puts things, and how import finds them</summary>

`pip install` downloads an archive — usually a `.whl` file, a "wheel",
which is a zip file with a strict naming convention — and unpacks it into
one folder:

```bash
python -c "import site; print(site.getsitepackages())"
```

Inside an active environment that path is under `.venv/`. Alongside the
package it writes a `.dist-info` folder holding the metadata `pip list`
and `pip show` read: name, version, the list of files installed, and the
dependencies.

When you write `import requests`, Python walks `sys.path` in order and
takes the first match:

```bash
python -c "import sys; print(sys.path)"
```

`sys.path` is built from `sys.prefix` — the value Problem 2 explained —
which is why activating an environment changes what `import` can find
without changing a single file.

Two consequences that explain the failures in Common bugs to catch:

- **A file in your current folder shadows an installed package.** Name a
  file `requests.py` and `import requests` finds yours, because the
  current directory is at the front of `sys.path`. The error that follows
  is `AttributeError` on something you never wrote, and it is baffling
  until you know this rule.
- **`pip install` and `import` can consult different environments.** pip
  installs relative to whichever interpreter *it* belongs to. `python -m
  pip` removes the ambiguity by definition: the pip that runs is the one
  belonging to the `python` you just typed.

</details>

## Acceptance checklist

- [ ] The environment was active before the install
      (`sys.prefix != sys.base_prefix` printed `True`).
- [ ] `python -m pip install requests` finished with
      `Successfully installed ...`.
- [ ] `requirements.txt` exists, was produced by `pip freeze`, and pins
      versions with `==`.
- [ ] `requirements.txt` is committed; `.venv/` is not.
- [ ] After `deactivate` and re-activating,
      `python -c "import requests; print(requests.__version__)"` prints a
      version.
- [ ] A rebuild from `requirements.txt` in a throwaway environment prints
      the same version.

## Stretch

- Compare `python -m pip list` and `python -m pip freeze` side by side in
  the same environment, and find the one package that appears in one and
  not the other. Then work out why that is the sensible choice.
- Draw the dependency chain: `python -m pip show requests` lists what it
  requires and what requires it. Follow one of those packages and do it
  again. Three levels down is usually the bottom.
- Wrap the whole setup in one-word commands with a `Makefile` or a
  `justfile` — a `setup` recipe that creates the environment and installs
  from `requirements.txt`, and a `run` recipe that runs your script. You
  will type those two words for the rest of the course.
- Delete `.venv/` completely, rebuild it, install from `requirements.txt`,
  and confirm `about_me.py` from Problem 3 still runs. Doing that once
  removes the fear of deleting an environment, which is a fear that costs
  people hours.

Next: [Homework Problem 5 — Publish Your Repo to GitHub](./problem-05-publish-your-repo-to-github.md).
