# Exercise 1 — Greet CLI

> **Topic:** `argparse` basics — positionals, flags, choices, custom types, exit codes
> **Lecture:** [01 — CLI Scripts with `argparse`](../lecture-notes/01-cli-scripts-with-argparse.md)
> **Difficulty:** Beginner
> **Target time:** 20 min
> **Why this one:** every other script this week starts with a parser. If you are still hand-slicing `sys.argv` in Exercise 3, the subprocess material will be buried under argument plumbing. Twenty minutes here buys you a shape you will reuse for the rest of the course: `build_parser()`, `main(argv)`, `raise SystemExit(main())`.

## The Brief

Code Crunch runs a community coding night. There is a laptop at the door, and
whoever is on check-in duty types a name and gets a badge line to read out.
You are writing that tool.

The greeting is trivial. The interface around it is not: a required name, an
optional repeat count that must be positive, a greeting word from a fixed set,
a shout mode, and a `--version`. Every one of those is something `argparse`
does for you, and something people get wrong parsing `sys.argv` by hand. Watch
`--times 0` in particular — a hand-rolled parser accepts it, prints nothing,
exits 0, and the volunteer at the door assumes the laptop is broken. Yours
should reject it before `main()` ever runs.

## Starter

Create `exercise-01-greet-cli.py` in your practice repo and paste this in:

```python
"""exercise-01-greet-cli.py — a check-in desk greeter built with argparse.

Prints one badge line per --times, using the greeting word chosen by
--greeting, optionally shouted.
"""

from __future__ import annotations

import argparse

GREETINGS: tuple[str, ...] = ("hello", "welcome", "howdy")


def positive_int(value: str) -> int:
    """Parse a command-line string as a whole number greater than zero.

    Raises:
        argparse.ArgumentTypeError: if the value is zero or negative.
    """
    # TODO: convert with int(), then reject anything <= 0 with
    # argparse.ArgumentTypeError(f"must be a positive whole number, got {n}")
    raise NotImplementedError


def build_parser() -> argparse.ArgumentParser:
    """Return the fully configured parser for the greet CLI."""
    parser = argparse.ArgumentParser(
        prog="greet",
        description="Greet a volunteer at the Code Crunch check-in desk.",
    )
    parser.add_argument("name", help="Name to print on the badge line")
    # TODO: -n / --times, type=positive_int, default=1, help mentions %(default)s
    # TODO: --greeting, choices=GREETINGS, default="hello"
    # TODO: --shout, action="store_true"
    # TODO: --version, action="version", version="%(prog)s 1.0.0"
    return parser


def badge_line(name: str, greeting: str, index: int, total: int) -> str:
    """Build a single badge line, e.g. 'Hello, Ada. (1 of 3)'."""
    # TODO: capitalize the greeting word only; leave the name's casing alone
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Parse argv, print the badge lines, and return an exit code."""
    args = build_parser().parse_args(argv)
    # TODO: for i in 1..args.times, build the line and print it,
    # upper-casing the whole line when args.shout is set
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. One line prints per repetition, in the exact form
   `Hello, Ada. (1 of 3)` — greeting word capitalized, comma, space, name as
   typed, period, space, then the counter in parentheses.
2. The counter is one-based and always shows the total, even when the total is
   one: `Hello, Ada. (1 of 1)`.
3. `--greeting` accepts only `hello`, `welcome`, or `howdy`. Anything else is
   an argparse error, not an `if` statement you wrote.
4. `--shout` upper-cases the **entire** line, counter included:
   `HELLO, ADA. (1 OF 1)`. Not just the name.
5. `--times 0`, `--times -4`, and `--times two` all fail at parse time with a
   message naming the flag, and the process exits 2.
6. `main()` returns `0` and the module ends with
   `if __name__ == "__main__": raise SystemExit(main())`.

## Constraints

- **`main()` must accept `argv: list[str] | None = None` and pass it to
  `parse_args()`.** With that one parameter you can call
  `main(["Ada", "-n", "3"])` from a test. Without it, the only way to exercise
  your CLI is to shell out to a new process, which is slow and awkward to
  assert on.
- **Validate `--times` with a `type=` callable, not an `if` inside `main()`.**
  A `type=` callable fails before any work starts and names the offending flag
  for you. An `if` fails after your program has already begun, and you have to
  write the error text and the exit code yourself.
- **Use `choices=` for the greeting instead of checking the string.**
  `argparse` then lists the valid options in `--help` and in the error
  message for free. A hand-written check gives you neither.
- **`%(default)s` in the help string, not a hard-coded "(default: 1)".** When
  you change the default, a hard-coded string quietly starts lying.

## Expected output

The shipped answer, [`exercise-01-greet-cli-solution.py`](./exercise-01-greet-cli-solution.py),
cannot sit waiting for command-line arguments, so it proves the parser by
driving `main()` with the same argv lists you would type — the good runs, and
the ones `argparse` rejects — and printing each one's output and exit code.
Yours reads its arguments from the shell instead; the parser being exercised is
the same. Real captured output, with the usage width pinned to 80 columns:

```text
$ python exercise-01-greet-cli-solution.py
Greet CLI — driving the parser headless with fixed argv lists.

greet Ada
Hello, Ada. (1 of 1)
[exit 0]

greet Ada --times 3 --greeting welcome
Welcome, Ada. (1 of 3)
Welcome, Ada. (2 of 3)
Welcome, Ada. (3 of 3)
[exit 0]

greet Grace H --shout
HELLO, GRACE H. (1 OF 1)
[exit 0]

greet --version
greet 1.0.0
[exit 0]

greet Ada --times 0
usage: greet [-h] [-n TIMES] [--greeting {hello,welcome,howdy}] [--shout]
             [--version]
             name
greet: error: argument -n/--times: must be a positive whole number, got 0
[exit 2]

greet Ada --times two
usage: greet [-h] [-n TIMES] [--greeting {hello,welcome,howdy}] [--shout]
             [--version]
             name
greet: error: argument -n/--times: invalid positive_int value: 'two'
[exit 2]

greet Ada --greeting hi
usage: greet [-h] [-n TIMES] [--greeting {hello,welcome,howdy}] [--shout]
             [--version]
             name
greet: error: argument --greeting: invalid choice: 'hi' (choose from hello, welcome, howdy)
[exit 2]
```

The usage block wraps at the terminal width. This run pins it to 80 columns so
it is stable; on your own machine it may break in different places. The `error:`
line will not.

## Steps

1. Activate your virtual environment. Nothing here needs `pip install`.
2. Create the file, paste the starter, and fill in `positive_int`.
3. Add the four remaining `add_argument` calls, then run
   `python exercise-01-greet-cli.py --help` and read it top to bottom. If a
   line of that help text would not make sense to the volunteer at the door,
   rewrite the `help=` string.
4. Fill in `badge_line`, then the loop in `main()`.
5. Work through every command the demo runs and compare character for
   character: `Ada`, `Ada --times 3 --greeting welcome`, `"Grace H" --shout`,
   `--version`, and the three that must fail.
6. Check the exit codes: `echo $?` on macOS or Linux, `echo $LASTEXITCODE` in
   PowerShell. A good run is 0, a bad flag is 2.

## The Solution

The shipped file is your own answer — `positive_int`, `build_parser`,
`badge_line`, `main` — with a `demo()` driver bolted on the end so it can prove
itself with no arguments. Your own `exercise-01-greet-cli.py` stops at
`raise SystemExit(main())`; the `show()`/`demo()` helpers below exist only so a
downloadable answer can run and print the session above.

```python
"""exercise-01-greet-cli-solution.py — the greet CLI, proven headless.

The exercise part is the starter with its TODOs filled in: a check-in desk
greeter built with argparse — a required name, a positive --times, a --greeting
from a fixed set, --shout, and --version.

Your own exercise-01-greet-cli.py ends in ``raise SystemExit(main())`` and is
run from the shell: ``python exercise-01-greet-cli.py Ada --times 3``. A
published answer cannot sit waiting for command-line arguments, so this file
proves the parser by calling ``main()`` with fixed argv lists itself and
printing what each one does — the good runs and the ones argparse rejects. The
parser being tested is identical either way.

Run it with::

    python exercise-01-greet-cli-solution.py
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys

GREETINGS: tuple[str, ...] = ("hello", "welcome", "howdy")


def positive_int(value: str) -> int:
    """Parse a command-line string as a whole number greater than zero.

    Raises:
        argparse.ArgumentTypeError: if the value is zero or negative.
    """
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"must be a positive whole number, got {number}"
        )
    return number


def build_parser() -> argparse.ArgumentParser:
    """Return the fully configured parser for the greet CLI."""
    parser = argparse.ArgumentParser(
        prog="greet",
        description="Greet a volunteer at the Code Crunch check-in desk.",
    )
    parser.add_argument("name", help="Name to print on the badge line")
    parser.add_argument(
        "-n", "--times",
        type=positive_int,
        default=1,
        help="How many badge lines to print (default: %(default)s)",
    )
    parser.add_argument(
        "--greeting",
        choices=GREETINGS,
        default="hello",
        help="Which word to open with (default: %(default)s)",
    )
    parser.add_argument(
        "--shout",
        action="store_true",
        help="Print the whole line in capitals, counter included",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    return parser


def badge_line(name: str, greeting: str, index: int, total: int) -> str:
    """Build a single badge line, e.g. 'Hello, Ada. (1 of 3)'."""
    return f"{greeting.capitalize()}, {name}. ({index} of {total})"


def main(argv: list[str] | None = None) -> int:
    """Parse argv, print the badge lines, and return an exit code."""
    args = build_parser().parse_args(argv)
    for index in range(1, args.times + 1):
        line = badge_line(args.name, args.greeting, index, args.times)
        print(line.upper() if args.shout else line)
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — the same argv lists the exercise page walks through.
# Your own file has no demo; it ends in ``raise SystemExit(main())`` and reads
# its arguments from the shell.
# --------------------------------------------------------------------------- #


def show(argv: list[str]) -> None:
    """Run the CLI once with *argv*, echoing the command, its output, exit code.

    argparse writes to stdout for --version and to stderr for a bad flag, and
    exits the process itself; capturing both streams and catching SystemExit is
    what lets one file demonstrate the success and the failure paths together.
    """
    print(f"greet {' '.join(argv)}")
    captured = io.StringIO()
    try:
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            code = main(argv)
    except SystemExit as exc:
        code = exc.code
    text = captured.getvalue()
    if text and not text.endswith("\n"):
        text += "\n"
    sys.stdout.write(text)
    print(f"[exit {code}]")
    print()


def demo() -> None:
    """Drive the parser with fixed argv lists and print the whole session."""
    os.environ["COLUMNS"] = "80"  # fixed width, so the usage block wraps the same everywhere
    print("Greet CLI — driving the parser headless with fixed argv lists.")
    print()
    show(["Ada"])
    show(["Ada", "--times", "3", "--greeting", "welcome"])
    show(["Grace H", "--shout"])
    show(["--version"])
    show(["Ada", "--times", "0"])
    show(["Ada", "--times", "two"])
    show(["Ada", "--greeting", "hi"])


if __name__ == "__main__":
    demo()
```

**A `type=` callable is a validator that runs before your program starts.**
`argparse` calls `positive_int("0")` while it is still building the namespace.
Anything that callable raises — `ValueError`, `TypeError`, or
`argparse.ArgumentTypeError` — is turned into a usage message on stderr and
`SystemExit(2)`. You never wrote the exit code, never wrote the `usage:` block,
and never wrote the `argument -n/--times:` prefix that tells the user *which*
flag they got wrong. That prefix is the whole reason to prefer this over an
`if` in `main()`: an `if` knows the value is bad but has forgotten which flag
it came from.

The two failure modes produce different messages, and both are correct. The
`invalid positive_int value: 'two'` line is `argparse`'s own wording, generated
when your callable raises something it did not expect — here `int("two")`
raising `ValueError`. The `must be a positive whole number, got 0` line is your
`ArgumentTypeError`, passed through verbatim. So you only write the message for
the case Python cannot describe on its own. `int()` already handles "that is
not a number"; you handle "that is a number and it is still wrong".

**`badge_line` returns a string instead of printing one.** That is what makes
`--shout` a single `.upper()` on the finished line rather than three separate
upper-cases that drift apart. It is also the only function in the file you can
test without capturing stdout: `badge_line("Ada", "hello", 1, 3)` either equals
`"Hello, Ada. (1 of 3)"` or it does not.

**`.capitalize()` is applied to the greeting only.** It upper-cases the first
character and lower-cases everything after it, which is exactly right for a
one-word greeting from a closed set and exactly wrong for a person's name —
`"Grace H".capitalize()` gives `"Grace h"`. The name goes through untouched,
because the person at the door typed it and they know how it is spelled.

**The counter is `range(1, args.times + 1)`.** Humans count from one, Python
counts from zero, and doing the adjustment in the `range` rather than at the
print site means there is exactly one place the off-by-one can live.

**`main(argv=None)` and `raise SystemExit(main())`.** Nothing below `main`
calls `sys.exit`, so every function is importable. `main(["Ada", "-n", "3"])`
runs the entire program in-process — which is exactly how the demo drives it,
and how you would write a test for a CLI without paying for a subprocess.

## Download and run

Download
[exercise-01-greet-cli-solution.py](./exercise-01-greet-cli-solution.py)
and run it:

```bash
python exercise-01-greet-cli-solution.py
```

It needs nothing but the standard library and prints the session shown above.
Because the answer is pure stdlib, you can also
[run it in the online editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-12-automation-scripting/exercises/exercise-01-greet-cli.md).
The `-solution` in the filename keeps it from colliding with your own
`exercise-01-greet-cli.py`.

## Common bugs to catch

- **`greet: error: argument -n/--times: invalid positive_int value: 'two'`.**
  That is the correct behavior, not a bug. `int("two")` raises `ValueError`,
  `argparse` catches it, and it names your callable in the message. Only the
  `<= 0` case needs your own `ArgumentTypeError`.
- **`AttributeError: 'Namespace' object has no attribute 'times'`.** You wrote
  `parser.add_argument("-n", "--times")` but read `args.n`. `argparse` names
  the attribute after the **long** flag, with dashes turned into underscores.
  `--dry-run` becomes `args.dry_run`.
- **`HELLO, ADA. (1 of 1)`.** You upper-cased the greeting and the name
  separately and forgot the counter. Build the whole line first, then call
  `.upper()` on the finished string once.
- **`hello, Ada. (1 of 1)` with a lowercase h.** You passed the raw choice
  through. `"hello".capitalize()` gives `Hello` — and also lower-cases the
  rest, which is fine for a one-word greeting and would be wrong for the name.
  That is why only the greeting gets it.
- **`(0 of 3)` on the first line.** `range(args.times)` starts at zero. Use
  `range(1, args.times + 1)`, or add one when you print.
- **`TypeError: 'str' object cannot be interpreted as an integer`.** You
  forgot `type=positive_int`, so `args.times` is the string `"3"` and
  `range("3")` blows up. Which exact message you get depends on how you wrote
  the loop — `range(args.times)` gives this one, `range(1, args.times + 1)`
  gives `can only concatenate str (not "int") to str` — but both mean the same
  thing: everything from the command line arrives as a string until a `type=`
  says otherwise. Note too that `--times 0` is *accepted* in this state, so the
  program prints nothing and exits 0, which is the failure the brief warned of.

## Under the hood

<details>
<summary>Under the hood — why the attribute is named after the long flag</summary>

When you write `add_argument("-n", "--times")`, `argparse` has to pick one name
for the attribute it hangs on the `Namespace`. It uses the first `--long`
option string it sees, strips the leading dashes, and replaces the inner ones
with underscores — so `--times` becomes `times` and `--dry-run` becomes
`dry_run`. If you give only short flags, it falls back to the short one
(`-n` alone would give you `args.n`), which is one reason every real flag has a
long form. The short flag is a typing shortcut for the person at the keyboard;
the long flag is the name your code reads.

You can override the choice with `dest=`: `add_argument("-n", "--times",
dest="count")` makes it `args.count`. Useful when the natural long name
collides with a Python keyword, or when you are keeping a flag's user-facing
name and its internal name deliberately different.

</details>

## Acceptance checklist

- [ ] `--help` lists every flag with a sentence a non-programmer could follow.
- [ ] `--version` prints `greet 1.0.0` and exits 0.
- [ ] All four success commands match the demo exactly.
- [ ] `--times 0` exits 2 with a message that names `-n/--times`.
- [ ] `main()` is called in exactly one place, inside the `__main__` guard.
- [ ] The file is committed to Git with a message like
      `Add Week 12 exercise 1: greet CLI`.

## Stretch

- Add `-q/--quiet` that drops the counter and prints only `Hello, Ada.`
  Decide what `--quiet --shout` together should mean, and put that decision in
  the help text.
- Add `--out FILE` with `type=Path` that appends the badge lines to a file
  instead of stdout.
- Turn the greeting into a subcommand set — `greet one Ada`, `greet all
  names.txt` — with `add_subparsers` and the `set_defaults(func=...)` trick
  from Lecture 1 §7.

When your four commands match, move on to
[Exercise 2 — Bulk Rename](./exercise-02-bulk-rename.md).
