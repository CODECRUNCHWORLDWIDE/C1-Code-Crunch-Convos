# Lecture 1 — CLI Scripts with `argparse`

> *"If you do it more than twice, automate it."* — every senior developer, eventually.

This lecture is in two halves. First we explore the **automation mindset** — what to automate, what *not* to automate, and how to think about the problem. Then we get our hands dirty with Python's built-in command-line argument parser, `argparse`, the foundation under almost every script you'll write this week.

---

## 1. The automation mindset

### Why automate?

Automation does three things humans don't:

1. **It doesn't get bored.** A bored human makes mistakes. A `for` loop does not.
2. **It's exactly reproducible.** Run it today, run it in six months — same result.
3. **It scales.** You can rename three files by hand. You can't rename thirty thousand.

It also has a fourth, sneakier benefit: **it documents the process**. The script *is* the runbook. Two months later when you've forgotten *how* you did something, the code remembers.

### What is worth automating?

A rough back-of-the-envelope formula:

```
worth_it = (frequency × time_saved_per_run) - cost_to_build - cost_to_maintain
```

If a task takes 30 minutes, you do it once a year, and the script would take a day to build, **don't automate it**. Write a checklist instead.

If a task takes 30 seconds, you do it 50 times a day, and the script takes 2 hours to build — automate the heck out of it.

Good candidates for automation:

- Renaming, sorting, or backing up files.
- Generating reports from CSVs or databases.
- Polling APIs at intervals.
- Triggering email or chat notifications when something changes.
- Resizing, watermarking, or converting media.
- Bootstrapping new projects (scaffolding folders, configs, git hooks).

Bad candidates:

- One-off tasks.
- Tasks that change every time (each one is a snowflake).
- Tasks where the cost of *getting it wrong* (silently!) is enormous and you don't have great testing yet — e.g. an automatic "delete old emails" script.

### Three rules for safe automation

1. **Make it idempotent if you can.** Running the script twice should be safe. If it isn't, document why.
2. **Default to dry-run.** Show what would happen before it actually does it. Add a `--apply` or `--execute` flag for the real thing.
3. **Log everything.** Use the `logging` module (Week 6 covered the basics). Future-you will thank present-you when something goes wrong at 3 a.m.

OK — mindset established. Let's make some CLIs.

---

## 2. Why `argparse`?

When you run `python myscript.py foo --bar 3`, the strings `["foo", "--bar", "3"]` are sitting in `sys.argv` waiting for you. You *could* parse them by hand:

```python
import sys

name = sys.argv[1]
shout = "--shout" in sys.argv
```

…and that quickly turns into a mess. What about `--shout=true`? What about `-s`? What about `--help`? What if someone passes an integer where a string is expected?

`argparse` (in the standard library since Python 3.2) handles **all** of that for you:

- Parses positional and optional arguments.
- Validates types (`int`, `float`, custom callables).
- Generates `--help` text automatically.
- Exits with a useful error message on bad input.
- Supports subcommands like `git commit` / `git push`.

Other options exist — `click`, `typer`, `fire` — but `argparse` is built in and is what most production scripts still use. Master it first, reach for the others when you outgrow it.

---

## 3. Your first parser

```python
# greet.py
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="greet",
        description="Say hello to someone.",
    )
    parser.add_argument("name", help="Who to greet")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
```

Try it:

```bash
$ python greet.py Alice
Hello, Alice!

$ python greet.py
usage: greet [-h] name
greet: error: the following arguments are required: name

$ python greet.py --help
usage: greet [-h] name

Say hello to someone.

positional arguments:
  name        Who to greet

options:
  -h, --help  show this help message and exit
```

Notice three things you got for free:

- A `usage:` line.
- A friendly error on missing input.
- A `--help` flag.

This is the baseline. Always start a script with `argparse`, even if it only takes one argument — you'll thank yourself when you add a second.

---

## 4. Positional vs. optional arguments

The rule of thumb:

- **Positional**: required, has a meaning by position. Example: `cp source dest`.
- **Optional** (flag-style): tweaks behavior, has a default. Example: `cp --recursive source dest`.

```python
parser.add_argument("source", help="File to copy")
parser.add_argument("dest", help="Destination path")
parser.add_argument("-r", "--recursive", action="store_true",
                    help="Copy directories recursively")
```

`store_true` means: if the flag is present, set the attribute to `True`; otherwise `False`. Its cousin `store_false` does the opposite. Both flags take **no value**.

If you *do* want a value:

```python
parser.add_argument("--threads", type=int, default=4,
                    help="Number of worker threads (default: 4)")
```

Now `--threads 8` sets `args.threads = 8`.

---

## 5. Types and validation

`type=` accepts **any callable** that takes a string and returns the parsed value. That means built-ins (`int`, `float`, `Path`) work — and so do your own functions.

```python
from pathlib import Path
import argparse


def positive_int(value: str) -> int:
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError(f"must be > 0, got {n}")
    return n


parser = argparse.ArgumentParser()
parser.add_argument("--count", type=positive_int, default=1)
parser.add_argument("--config", type=Path, default=Path("config.json"))
```

When the user passes `--count 0`, `argparse` catches the `ArgumentTypeError` and prints a clean error.

---

## 6. Choices, defaults, and "store_const"

```python
parser.add_argument(
    "--loglevel",
    choices=["debug", "info", "warning", "error"],
    default="info",
    help="Verbosity (default: %(default)s)",
)
```

The `%(default)s` token is interpolated into the help text. Tiny trick, huge readability win.

To track verbosity with `-v`, `-vv`, `-vvv` use `action="count"`:

```python
parser.add_argument("-v", "--verbose", action="count", default=0,
                    help="Increase verbosity (-v, -vv, -vvv)")
```

`args.verbose` will be 0, 1, 2, or 3. Map it to a `logging` level later.

---

## 7. Subcommands (`git`-style)

Big tools have subcommands: `git commit`, `git push`, `pip install`. `argparse` supports this via `add_subparsers`.

```python
import argparse


def cmd_add(args: argparse.Namespace) -> int:
    print(f"adding {args.item}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    print("listing items...")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add an item")
    p_add.add_argument("item")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List items")
    p_list.set_defaults(func=cmd_list)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

Run:

```bash
$ python todo.py add buy-milk
adding buy-milk

$ python todo.py list
listing items...
```

The `set_defaults(func=...)` trick attaches a handler to each subparser. `main()` just calls `args.func(args)`. Clean, scalable, and the pattern used by tools like `aws` and `gh`.

---

## 8. Exit codes and `sys.exit`

CLI scripts communicate success or failure to their **caller** (shell, cron, CI) by way of an integer **exit code**:

| Code | Meaning                                    |
|------|--------------------------------------------|
| 0    | Success                                    |
| 1    | Generic failure                            |
| 2    | Misuse / bad CLI args (argparse uses this) |
| 64–78| Various BSD-defined errors                 |
| 130  | Killed by Ctrl-C (SIGINT)                  |

In Python you set exit codes via `sys.exit(n)` (or `raise SystemExit(n)`, identical effect):

```python
import sys

if not config.exists():
    print(f"ERROR: missing config {config}", file=sys.stderr)
    sys.exit(1)
```

Two practical tips:

1. **Print errors to `stderr`.** `print(..., file=sys.stderr)` keeps `stdout` clean so it can be piped.
2. **Return ints from `main()`, hand them to `SystemExit`.** It makes `main()` testable from inside another Python process.

```python
def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

---

## 9. CLI conventions worth following

Borrowed mostly from the [GNU coding standards](https://www.gnu.org/prep/standards/) and the [Command Line Interface Guidelines](https://clig.dev/) — both worth a skim.

- **Short flag + long flag** for common options: `-v`, `--verbose`.
- **Lowercase, kebab-case long flags**: `--dry-run`, not `--DryRun`.
- **Boolean flags default off**: presence means "yes".
- **`--help` and `-h`** print help. (`argparse` gives this free.)
- **`--version`** prints version and exits. Wire it up:

  ```python
  parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
  ```

- **Quiet mode and verbose mode** are different things — support both (`-q`, `-v`).
- **Read config from a file first, override with env vars, override with flags.** That's the [twelve-factor](https://12factor.net/) order. Flags always win.
- **Be polite when things go wrong.** "Error: file `foo.txt` not found. Did you mean `foo.txt.bak`?" is gold-standard. "Traceback (most recent call last):" is not.

---

## 10. Putting it together: a real-ish script

```python
# rename_bulk.py
"""Bulk-rename files in a directory by replacing one substring with another."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rename_bulk",
        description="Replace `old` with `new` in filenames inside DIR.",
    )
    p.add_argument("directory", type=Path, help="Folder to operate on")
    p.add_argument("old", help="Substring to look for")
    p.add_argument("new", help="Replacement")
    p.add_argument("--pattern", default="*", help="Glob pattern (default: *)")
    p.add_argument("--apply", action="store_true",
                   help="Actually rename. Without it, just preview.")
    p.add_argument("-v", "--verbose", action="count", default=0)
    p.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    return p


def configure_logging(verbosity: int) -> None:
    level = logging.WARNING - (verbosity * 10)  # -v=INFO, -vv=DEBUG
    logging.basicConfig(level=max(level, logging.DEBUG), format="%(message)s")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.verbose)

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    renamed = 0
    for path in args.directory.glob(args.pattern):
        if not path.is_file() or args.old not in path.name:
            continue
        target = path.with_name(path.name.replace(args.old, args.new))
        logging.info("%s -> %s", path.name, target.name)
        if args.apply:
            path.rename(target)
        renamed += 1

    verb = "renamed" if args.apply else "would rename"
    print(f"{verb} {renamed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

This script is **small, complete, and friendly**:

- It defaults to dry-run.
- It logs at the verbosity you ask for.
- It has a `--version`.
- It exits with the right code on bad input.
- The `main(argv=None)` signature makes it trivially testable.

---

## 11. Quick checklist for any new CLI

Before you call a CLI "done", run through:

- [ ] `--help` reads like documentation.
- [ ] All required inputs are *positional*, optional knobs are *flags*.
- [ ] Has a `--dry-run` (or defaults to dry-run) when it modifies state.
- [ ] Uses `logging`, not `print`, for diagnostic output.
- [ ] Exits 0 on success, non-zero on failure.
- [ ] Error messages go to stderr, results go to stdout.
- [ ] Has a `--version`.
- [ ] Has at least one test that calls `main(["arg1", "arg2"])`.

---

## Where next?

In the next lecture we'll connect Python to the rest of your operating system: copying and archiving files with `shutil`, walking directory trees with `pathlib`, and running shell commands safely with `subprocess`.

**Further reading**

- [`argparse` reference](https://docs.python.org/3/library/argparse.html)
- [`argparse` tutorial](https://docs.python.org/3/howto/argparse.html)
- [Command Line Interface Guidelines (clig.dev)](https://clig.dev/)
- Real Python: ["Build Command-Line Interfaces With Python's argparse"](https://realpython.com/command-line-interfaces-python-argparse/)
