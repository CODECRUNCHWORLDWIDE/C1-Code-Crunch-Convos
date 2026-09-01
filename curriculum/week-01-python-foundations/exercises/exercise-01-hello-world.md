# Exercise 1 — Hello, World

> **Topic:** Writing a `.py` file, running it, reading the output
> **Lecture:** [01 — Installing Python and Running Your First Program](../lecture-notes/01-installing-python-and-running-your-first-program.md)
> **Difficulty:** Beginner
> **Target time:** 5 minutes, plus 10 minutes of poking at it
> **Why this one:** every other exercise in this course assumes you can make a file, save it, run it from a terminal, and read what came back. That loop — edit, run, read — is the whole job. Do it once on purpose here and you stop thinking about it.

## The Brief

Make a file called `exercise-01-hello-world.py`. Run it from a terminal. It
prints three lines: a greeting, your name, and the version of Python that
ran it.

The first two lines are warm-up. Line three is the exercise.

Here is why. Lots of computers have two or three Pythons installed at
once, and the `python` command picks one of them without telling you.
Guessing which one is like guessing which key opens a door — you can
guess, or you can try the key and watch. Printing the version from
*inside* the running program is trying the key. The program tells you
which interpreter is holding it, and now you know instead of hoping.

## Starter

Make the file with exactly this content, then fill in the two spots marked
`TODO`.

```python
"""exercise-01-hello-world.py — first program, first run.

Prints a greeting, the author's name, and the running Python version.
"""

import sys


def main() -> None:
    """Print the three lines described in the module docstring."""
    print("Hello, Code Crunch.")
    print("My name is ...")  # TODO: put your name here
    # TODO: print the Python version. sys.version_info has .major and .minor


if __name__ == "__main__":
    main()
```

Two things in that starter are not taught until later, and you are not
expected to design them today. `def main() -> None:` makes a function, and
you meet functions properly in Week 4. The `f"..."` string you are about
to write is an f-string, and it arrives in Week 2. This week they are
handed to you finished. You are filling in bodies, not inventing shapes.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-01-python-foundations/exercises/exercise-01-hello-world.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The file starts with a module docstring — a triple-quoted string on the
   first line, not a `#` comment.
2. The greeting is exactly `Hello, Code Crunch.` Capital H, capital C,
   period at the end. Later work compares output character by character,
   so the habit of matching a spec exactly starts now.
3. Line two says `My name is <your name>` with your real name in it.
4. Line three says `Running Python <major>.<minor>` — for example
   `Running Python 3.12`. Read those two numbers from `sys.version_info`.
   Do not type them yourself. A version you typed by hand is a sentence
   that turns into a lie the day you upgrade.
5. The `if __name__ == "__main__":` guard stays exactly as given.

## Constraints

- **Use `sys.version_info`, not `sys.version`.** Both know the version.
  `sys.version` hands it to you as one long messy sentence with the
  compiler build wedged in the middle, and digging `3.13` out of that
  means slicing up a string. `sys.version_info` hands you the pieces
  already separated, as numbers. When a tool offers you the neat version
  and the pretty version, take the neat one.
- **No third-party packages.** `sys` comes with Python. If this exercise
  needed a `pip install`, it would be testing your internet connection
  instead of your setup.
- **Run it from a terminal, not from your editor's green run button.** The
  button quietly picks an interpreter and does not show you which. The
  terminal shows you, and the terminal is where you live for the next
  fifteen weeks.

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2:

```text
$ python exercise-01-hello-world.py
Hello, Code Crunch.
My name is Ada Lovelace.
Running Python 3.13
```

Your run will differ in two places, and both are correct. Line two carries
your name, not mine. Line three carries *your* interpreter's version, so
if you installed 3.12 you will see `Running Python 3.12`. That is the
whole point of reading the number instead of typing it — the line changes
when the truth changes.

## Steps

1. Turn on your Week 1 virtual environment (Lecture 2). Your prompt should
   show `(.venv)` or something like it.
2. Make the file inside your `exercises/` folder.
3. Paste the starter in, fill the two `TODO`s, save.
4. Run it: `python exercise-01-hello-world.py`.
5. Read all three lines out loud. Is the version the one you expected when
   you installed Python?
6. Now run `python -V` on its own and compare. The two have to agree on
   the first two numbers. If they do not, your terminal and your script
   are using different Pythons, and that is worth fixing before Week 2.

## The Solution

```python
"""exercise-01-hello-world-solution.py — first program, first run.

Prints a greeting, the author's name, and the running Python version.
"""

import sys


def main() -> None:
    """Print the three lines described in the module docstring."""
    print("Hello, Code Crunch.")
    print("My name is Ada Lovelace.")
    print(f"Running Python {sys.version_info.major}.{sys.version_info.minor}")


if __name__ == "__main__":
    main()
```

Put your own name on line two. Line one is fixed by requirement 2 and has
to match exactly.

**`sys.version_info` is a labelled box, not a paragraph.** Ask
`sys.version` and you get this back:

```text
3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)]
```

Everything you want is in there, buried in things you do not. Ask
`sys.version_info` instead and the pieces come pre-separated and already
labelled: `.major` is the number `3`, `.minor` is the number `13`. No
cutting up a sentence, so nothing to cut wrong.

**The f-string looks the numbers up while the program runs, and that is
the point.** An f-string is a string with `f` in front of it, and anything
you put inside `{}` gets worked out on the spot and dropped in. So
`f"Running Python {sys.version_info.major}.{sys.version_info.minor}"` asks
the interpreter for its own version every single time that line runs. Type
`"Running Python 3.13"` as plain text instead and the line is right today
and quietly wrong the morning you upgrade — wrong in the most expensive
way, by agreeing with what you already believed.

**The dot between the two `{}` blocks is just a dot.** Only what is inside
the braces gets worked out. The `.` in the middle is an ordinary character
sitting in the string.

**`.major` and `.minor`, but not `.micro`.** `3.13` is the feature
version, which is what people mean when they ask what Python you are on.
The third number — the `2` in `3.13.2` — changes for bug fixes that do not
change anything you can see.

**The guard does nothing today, and that is fine.** `if __name__ ==
"__main__":` is a rule about *who started this file*. When you run the
file yourself, the rule is true and `main()` runs. When some other file
borrows yours, the rule is false and nothing runs, so the borrower gets
your functions without your program firing off. You have nothing to borrow
from yet. Requirement 5 makes you type it anyway, because it costs nothing
on day one and costs a whole afternoon the first time you forget it in
Week 4.

## Download and run

Download [exercise-01-hello-world-solution.py](./exercise-01-hello-world-solution.py) and run it:

```bash
python exercise-01-hello-world-solution.py
```

## Common bugs to catch

- **`NameError: name 'sys' is not defined. Did you forget to import
  'sys'?`** You used `sys.version_info` without the `import sys` line, or
  you put the import inside `main()` and then used it outside. The real
  run looks like this:

  ```text
  Hello, Code Crunch.
  My name is Ada Lovelace.
  Traceback (most recent call last):
    File "exercise-01-hello-world.py", line 16, in <module>
      main()
      ~~~~^^
    File "exercise-01-hello-world.py", line 12, in main
      print(f"Running Python {sys.version_info.major}.{sys.version_info.minor}")
                              ^^^
  NameError: name 'sys' is not defined. Did you forget to import 'sys'?
  ```

  Read the first two lines of that. They printed. Python works down the
  file and stops where it breaks, so getting *some* output before a crash
  is normal and does not mean the earlier lines are guilty.

- **`SyntaxError: unterminated triple-quoted string literal`.** You opened
  the docstring with `"""` and closed it with `'''`, or the other way
  round. They have to match:

  ```text
    File "exercise-01-hello-world.py", line 10
      """Print the three lines described in the module docstring."""
                                                                 ^
  SyntaxError: unterminated triple-quoted string literal (detected at line 17)
  ```

  Line 10 is not where you made the mistake. When a `SyntaxError` points
  at a line that looks fine, the real mistake is above it, at the last
  quote or bracket you left open. Scroll up.

- **Nothing prints at all, and there is no error.** You mistyped the
  guard. `_main_` and `__main__` are different strings, so the comparison
  is simply false and Python has nothing to complain about:

  ```text
  $ python exercise-01-hello-world.py
  $
  ```

  Count the underscores: two before, two after, four in total. This one is
  nastier than a traceback, because silence looks like nothing happened
  rather than like something broke.

- **A whole tuple prints instead of a version.**
  `print("Running Python", sys.version_info)` runs fine and says
  `Running Python sys.version_info(major=3, minor=13, micro=2,
  releaselevel='final', serial=0)`. Useful for reading, useless for a spec
  that asked for `Running Python 3.13`. Pull out the two fields you want.

- **`python: command not found`.** On macOS and many Linux systems the
  command is `python3`. On Windows, try `py`. Lecture 1 covers this.

- **The version printed does not match `python -V`.** Your virtual
  environment is not switched on, or your editor is launching a different
  interpreter than your terminal is. Fix it now.

## Under the hood

<details>
<summary>Under the hood — what sys.version_info really is, and the other three fields</summary>

`sys.version_info` is a **named tuple**. A tuple is a fixed row of values;
a named tuple is the same row with a label on each slot, so you can say
`.major` instead of counting to position zero. It has five slots, not two:

```text
sys.version_info(major=3, minor=13, micro=2, releaselevel='final', serial=0)
```

`.micro` is the patch number. `.releaselevel` is one of `'alpha'`,
`'beta'`, `'candidate'` or `'final'`, and `.serial` numbers the pre-release
builds. On any Python you actually installed to work in, `releaselevel` is
`'final'` and `serial` is `0`.

Because it is a tuple underneath, it compares the way you would hope:
`sys.version_info >= (3, 11)` is a real, correct version check, and it is
the right way to write "this code needs 3.11 or newer". Compare the
*strings* instead and you get `"3.9" > "3.11"` being `True`, because
string comparison goes character by character and `9` sorts after `1`.
That bug is real and it bites people every October.

`sys.version` is the same information formatted for a human to read, and
it is built by CPython at compile time out of the tag, the commit hash,
the build date and the compiler. There is no promise anywhere that its
shape will stay the same, which is exactly why parsing it is a trap.

</details>

<details>
<summary>Under the hood — why the __main__ guard exists at all</summary>

Every Python file that gets loaded is a **module**, and every module has a
variable called `__name__` that Python fills in for you. The value depends
entirely on how the file was started.

- Run it directly — `python exercise-01-hello-world.py` — and Python sets
  `__name__` to the string `"__main__"`.
- Load it from another file — `import exercise_01` — and Python sets
  `__name__` to `"exercise_01"`, the module's own name.

So `if __name__ == "__main__":` is not magic. It is an ordinary string
comparison against an ordinary variable, and it means "only do this if I
am the file that was started, not if somebody borrowed me".

Why that matters: importing a module *runs every line in it*. That is how
the definitions get made. If your printing were sitting at the top level
with nothing guarding it, then the moment another file imported yours it
would print, in the middle of somebody else's program, for no reason. The
guard is the line between "here is what I can do" and "here is what I do
when I am in charge".

You will feel this properly in Week 11, when a test file imports your
module to check your functions. Unguarded top-level work turns a test run
into a mess of stray output.

</details>

<details>
<summary>Under the hood — the little arrows under the traceback</summary>

In the `NameError` above, look at these two lines:

```text
    main()
    ~~~~^^
```

The squiggles and carets are **fine-grained error locations**, added in
Python 3.11. Older Pythons could only tell you which *line* failed. From
3.11 on, the interpreter stores a column range for every instruction, so
it can underline the exact piece of the line that broke — the `^^^` under
`sys`, not under the whole `print(...)` call.

On a line with one operation this is barely worth it. On
`a["x"]["y"]["z"]` it turns "one of these three lookups failed" into
"*this* one failed", which is the difference between a minute and twenty.
It is one of the reasons this course asks for 3.11 or newer.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] Three lines print, in the order the brief gives.
- [ ] The greeting matches the spec exactly.
- [ ] The version line comes from `sys.version_info`, not from text you typed.
- [ ] `python -V` and the script's third line agree on the first two numbers.
- [ ] The file is committed to Git with a message like `Add Week 1 exercise 1: hello world`.

## Stretch

- Print the full path of the interpreter running you, with
  `sys.executable`, and compare it to your virtual environment's folder.
  If the path has no `.venv` in it, your environment is not switched on.
  This is the same fact Challenge 2 checks from a different angle.
- Print `sys.platform` and note the exact word it gives you. On 64-bit
  Windows it says `win32`, which is a leftover name from the 1990s and has
  nothing to do with your machine being 32-bit. On macOS it says `darwin`,
  not `macos`. Both surprise people, and both are the strings your code
  will one day have to match against.
- Move the three lines into a function that *returns* a list of strings,
  and have `main()` print them in a loop. Same output. It is the shape a
  test needs in Week 11, because
  `assert report_lines("Ada")[0] == "Hello, Code Crunch."` is one short
  line and there is no equally short way to check that something got
  printed.

When your three lines look right, move on to
[Exercise 2 — REPL Explorer](./exercise-02-repl-explorer.md).
