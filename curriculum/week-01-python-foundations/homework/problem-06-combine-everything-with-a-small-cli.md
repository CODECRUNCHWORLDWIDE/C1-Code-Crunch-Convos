# Homework Problem 6 — Combine Everything with a Small CLI

> **Topic:** `input()`, `.strip()`, a `for` loop with `enumerate`, small single-purpose functions, and committing the result
> **Lecture:** [Lecture 1 — Installing Python and Running Your First Program](../lecture-notes/01-installing-python-and-running-your-first-program.md)
> **Difficulty:** Beginner
> **Target time:** 1 hour 45 minutes
> **Why this one:** it is the first program in this course that has a conversation. It asks, it listens, it answers. Everything from the previous five problems shows up here at once, and the result is the last commit of your Week 1 repository.

## The Brief

In the same repository, write `day_planner.py`. It should:

1. Ask the user for their name.
2. Ask for three things they want to do today.
3. Print a numbered list of those three things, under a heading that says
   `Today, <Name>:`.

Two details carry all the weight.

**Clean the input at the door.** When somebody types ` Ada ` with stray
spaces, you want `Ada`. Python's `.strip()` removes whitespace from both
ends of a string. Call it the instant the value arrives — in the function
that reads it — and then nothing further down the program ever has to
wonder whether it was done.

**Number the list with `enumerate`.** Python counts from zero, and a
to-do list that starts at zero looks broken. `enumerate(tasks, start=1)`
hands you the item and its number together, counting from one, so you
never write `+ 1` anywhere.

A note on the format. The brief says "prefixed by `Today, <Name>:`" but
does not say exactly where that goes. The answer below reads it as a
heading on its own line with the tasks indented under it. Putting it
inline instead also satisfies a literal reading and is not wrong. Pick a
reading and make your code match it consistently — that is the part
anybody can actually assess.

## Starter

Save this as `day_planner.py` and fill in the `TODO`s. It runs as pasted
and will ask you one question:

```python
"""TODO: one line saying what this file does."""

import sys

TASK_COUNT: int = 3


def ask(prompt: str) -> str:
    """Show ``prompt``, then return the typed answer without padding."""
    print(prompt, end="", file=sys.stderr, flush=True)
    return input()  # TODO: strip it


def prompt_name() -> str:
    """Return the typed name with surrounding whitespace removed."""
    return ask("What is your name? ")


def prompt_tasks(count: int = TASK_COUNT) -> list[str]:
    """Return ``count`` stripped task strings, asking once per task."""
    tasks: list[str] = []
    # TODO: ask `count` times, appending each answer to `tasks`
    return tasks


def print_plan(name: str, tasks: list[str]) -> None:
    """Print the header line, then one numbered line per task."""
    print(f"Today, {name}:")
    # TODO: one numbered line per task, using enumerate(..., start=1)


def main() -> None:
    """Collect a name and three tasks, then print the numbered plan."""
    print_plan(prompt_name(), prompt_tasks())


if __name__ == "__main__":
    main()
```

`ask()` prints the question to `sys.stderr` — the stream a program uses
for everything that is not its answer — and then reads a line. Why that
is better than passing the question to `input()` is explained under The
Solution.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-01-python-foundations/homework/problem-06-combine-everything-with-a-small-cli.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Running `python day_planner.py` asks for a name, then asks for three
   tasks, then prints the plan.
2. The output is a heading line `Today, <Name>:` followed by three
   numbered lines.
3. `main()` is annotated `-> None`, and every other function has type
   hints too.
4. Every value the user types has `.strip()` applied to it before it is
   used or stored.
5. The finished file is committed with a message like
   `Add day_planner CLI`, and pushed to the GitHub repository from
   Problem 5.

## Constraints

- **Strip on the way in, not on the way out.** Clean each value inside the
  function that reads it. If you strip only where you print, the printed
  line looks right while the stored value is still dirty, and the bug
  stays invisible until something compares it to something else.
- **Use `enumerate(tasks, start=1)`.** Not `range(len(tasks))`, and not
  `index + 1` in the f-string. See The Solution for why.
- **Ask in a loop, not three times by hand.** "Three" should appear once
  in your program, as `TASK_COUNT`. Three copied-and-pasted `input()`
  calls stop working the moment you want four tasks.
- **Do not name a variable `input`.** You would replace the built-in
  function with a string, and the next call to it fails with a message
  that points at the wrong line. It is in Common bugs to catch, with the
  real traceback.

## Expected output

The downloadable file below prints its built-in example when nobody is at
the keyboard, so the run is the same every time:

```text
$ python problem-06-combine-everything-with-a-small-cli.py
Today, Ada:
  1. ship the mini-project
  2. read PEP 8
  3. walk the dog
```

Run the same program in your own terminal and it has the conversation
instead. Here is a real session, typed sloppily on purpose to exercise the
stripping:

```text
What is your name? Ada
Task 1: ship the mini-project
Task 2: read PEP 8
Task 3: walk the dog
Today, Ada:
  1. ship the mini-project
  2. read PEP 8
  3. walk the dog
```

## Steps

1. Activate your environment and `cd` into `week-01-homework`.
2. Save the Starter as `day_planner.py`.
3. Fill in `prompt_name` first. Run it. It should ask one question and
   print an empty plan.
4. Fill in `prompt_tasks`. Run it again. Three questions, still an empty
   plan.
5. Fill in `print_plan` with the `enumerate` loop. Run it. Now the plan
   appears.
6. Run it once more and type deliberately messy answers, with spaces
   before and after. The output should look identical to the tidy run.
7. Check the formatting without typing anything by calling the printing
   function on its own:

   ```bash
   python -c "from day_planner import print_plan; print_plan('Ada', ['ship the mini-project', 'read PEP 8', 'walk the dog'])"
   ```

8. Commit and push:

   ```bash
   git add day_planner.py
   git commit -m "Add day_planner CLI"
   git push
   ```

   A bare `git push` works here because Problem 5's `-u` already recorded
   where this branch goes.

## The Solution

```python
"""Ask for a name and three tasks, then print a numbered plan.

Week 1 homework, problem 6, Code Crunch Convos. Everything typed is
stripped of surrounding whitespace before it is used or printed. Save
your own copy as ``day_planner.py`` in your homework repository.

Prompts go to the error stream and the plan goes to the normal output
stream, so ``python day_planner.py > plan.txt`` saves the plan and
nothing else. When nobody is at the keyboard, the script prints a
built-in example rather than waiting for typing that is never coming.
"""

import sys

TASK_COUNT: int = 3
SAMPLE_NAME: str = "  Ada  "
SAMPLE_TASKS: list[str] = [
    "  ship the mini-project ",
    "read PEP 8",
    "walk the dog  ",
]


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str) -> str:
    """Show ``prompt``, then return the typed answer without padding."""
    print(prompt, end="", file=sys.stderr, flush=True)
    return input().strip()


def prompt_name() -> str:
    """Return the typed name with surrounding whitespace removed."""
    return ask("What is your name? ")


def prompt_tasks(count: int = TASK_COUNT) -> list[str]:
    """Return ``count`` stripped task strings, asking once per task."""
    tasks: list[str] = []
    for number in range(1, count + 1):
        tasks.append(ask(f"Task {number}: "))
    return tasks


def print_plan(name: str, tasks: list[str]) -> None:
    """Print the header line, then one numbered line per task."""
    print(f"Today, {name}:")
    for index, task in enumerate(tasks, start=1):
        print(f"  {index}. {task}")


def main() -> None:
    """Collect a name and three tasks, then print the numbered plan."""
    name: str = SAMPLE_NAME.strip()
    tasks: list[str] = [task.strip() for task in SAMPLE_TASKS]
    if someone_is_typing():
        try:
            name = prompt_name()
            tasks = prompt_tasks()
        except EOFError:
            print("\nNo input; showing the example plan.", file=sys.stderr)
    print_plan(name, tasks)


if __name__ == "__main__":
    main()
```

**Why it works.**

**`enumerate(tasks, start=1)` is worth understanding, not copying.**
`enumerate` wraps any sequence and hands back pairs: the position and the
item. Without `start=1` it counts from zero and you would have to write
`index + 1` inside the f-string. That works, and it is the single most
popular place in programming to be off by one. `start=1` puts the
correction in one place, where it is stated once and cannot drift.

The version most people write first is:

```python
for i in range(len(tasks)):
    print(f"  {i + 1}. {tasks[i]}")
```

It is correct. It is also three separate chances to be wrong — the
`len`, the `+ 1`, and the subscript — and it only works on things you can
index. `enumerate` is the idiom for a reason.

**Small single-purpose functions instead of one big one.** Each does
exactly one thing, and only `print_plan` writes the plan. That is what
makes step 7 of Steps possible: you can check the formatting without
typing at a prompt, because `print_plan` does not care where its
arguments came from. It also means `prompt_tasks(5)` already works if you
ever want five tasks.

**`ask()` puts the prompt on the error stream, not the output stream.**
Every program has two ways out: standard output, for the answer, and
standard error, for everything else. `input("prompt")` puts the prompt on
standard output, which mixes the question in with the answer. Writing it
to `sys.stderr` instead keeps them apart, and the payoff is immediate:
`python day_planner.py > plan.txt` saves a file containing the plan and
nothing else, while the questions still appear on your screen. The
`flush=True` matters because the error stream is line-buffered: text with
no newline on the end waits in a buffer until something pushes it out. A
prompt that appears after you have already answered it is useless, so you
push it out yourself.

**`.strip()` is called at the boundary, immediately.** Every value is
cleaned the moment it enters the program. That principle — *normalise at
the edge* — is why the rest of the program can be simple. Stripping later
means the raw value floats around in between, and some future line
forgets.

`str.strip()` with no argument removes spaces, tabs, newlines, and
carriage returns from both ends. That last one quietly fixes a whole
category of cross-platform bug, because a Windows line ending carries a
`\r`. And like every string method it returns a *new* string — strings
cannot be changed in place — so `raw.strip()` on a line by itself does
nothing at all, a mistake that produces no error and no effect.

**`input()` always returns a string,** minus the trailing newline. It
never converts anything. In Week 2, when you start asking for numbers,
`int(input(...))` is the conversion and it can fail; here there is nothing
to convert, so there is nothing to fail.

**`someone_is_typing()` is the one piece the brief did not ask for.** It
exists so the downloadable file can be run automatically and still
finish. `sys.stdin.isatty()` answers "is standard input a real terminal
with a person attached to it". When it is, the program has its
conversation. When it is not, calling `input()` would either raise
`EOFError` or wait forever for typing that is never coming, so the
program prints the example plan instead. The `except EOFError` is a
second belt for the same trousers: some terminals claim somebody is there
and then close the input immediately.

Notice the sample values are deliberately padded with spaces. That means
the automatic run proves the stripping works, on its own, with nobody
typing anything.

**`list[str]` needs Python 3.9 or newer.** On older versions you would
import `List` from `typing` and write `List[str]`. This course targets
3.11 and up, so the built-in spelling is the right one and the import is
dead weight.

## Run it

Copy the worked answer on this page into `problem-06-combine-everything-with-a-small-cli.py` and run it:
and run it:

```bash
python problem-06-combine-everything-with-a-small-cli.py
```

Run from a terminal, it asks you the four questions. Run by a script or
with its input redirected, it prints the built-in example instead of
hanging. Save your own copy as `day_planner.py` in your homework
repository, and commit that.

## Common bugs to catch

- **The list starts at zero.**

  ```text
  Today, Ada:
    0. ship the mini-project
    1. read PEP 8
    2. walk the dog
  ```

  You forgot `start=1`. No error, no traceback, just a list that is wrong.
  This is why "it ran" is not the same as "it is right".
- **You stripped the display, not the value.**

  ```python
  print(f"  {index}. {task.strip()}")
  ```

  The printed line looks correct, so the bug hides until something else
  uses the unstripped value — a comparison, a lookup, a line written to a
  file. `"walk the dog" == "walk the dog  "` is `False`, and you will
  spend an hour on that one day.
- **You used `input` as a variable name.**

  ```python
  input = input("What is your name? ")   # don't
  ```

  The first call works. The name `input` now refers to a string, and the
  *second* prompt raises:

  ```text
  Traceback (most recent call last):
    File "day_planner.py", line 12, in <module>
      task = input(f"Task {number}: ")
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: 'str' object is not callable
  ```

  Python let you replace a built-in without a word of warning, and the
  error surfaces one step away from its cause. Note the `^^^^` markers
  under the exact call — that is the Python 3.11 feature Problem 1 said
  was worth the upgrade.
- **`EOFError: EOF when reading a line`.** Something called `input()` when
  there was no input left. It happens when you pipe a file into a script
  that asks more questions than the file has lines, or when a checker runs
  your script with nothing attached to its input.
- **The prompts all run together on one line.** Pipe input into a version
  that prompts through `input("...")` and you get:

  ```text
  What is your name? Task 1: Task 2: Task 3: Today, Ada:
  ```

  Nothing is broken. In a real terminal your *typing* is echoed after each
  prompt and breaks the line; through a pipe there is no typing to echo,
  so the prompts land side by side. Worth knowing before you go hunting
  for a formatting bug that is not there.
- **`ModuleNotFoundError: No module named 'day_planner'`** from the step 7
  check. You are not in the folder that holds the file. `cd` there first.

## Under the hood

<details>
<summary>Under the hood — what enumerate actually hands you, and why it costs nothing</summary>

`enumerate` does not build a list of pairs. It returns an **iterator**: an
object that produces one pair at a time, when asked, and remembers nothing
else. Look at it without a loop:

```bash
python -c "e = enumerate(['a', 'b'], start=1); print(e); print(next(e)); print(next(e))"
```

```text
<enumerate object at 0x000001C4...>
(1, 'a')
(2, 'b')
```

Ask once more and it raises `StopIteration`, which is precisely the signal
a `for` loop catches to know it has finished. That is the whole protocol
behind every `for` loop you will ever write.

Because it produces pairs on demand, memory use does not grow with the
length of the sequence — enumerating a million-line file costs the same as
enumerating three tasks. `range` behaves the same way, which is why
`range(len(tasks))` is not *wasteful* so much as it is *indirect*: it
gives you numbers and then makes you go and fetch the items yourself.

`for index, task in ...` is doing a second thing quietly: **unpacking**.
Each pair is a tuple, and Python takes it apart into two names in one
step. You can unpack anywhere:

```python
first, second = ("a", "b")
```

That is the same mechanism, and it is why swapping two variables in Python
is `a, b = b, a`.

</details>

<details>
<summary>Under the hood — strings never change, and what strip really removes</summary>

Python strings are **immutable**: once a string object exists, its
characters cannot be altered. Every method that looks like it edits a
string actually builds a new one and hands it back.

```bash
python -c "s = '  Ada  '; s.strip(); print(repr(s))"
```

```text
'  Ada  '
```

Nothing changed, because the result was thrown away. This is the most
common silent no-op a beginner writes. `s = s.strip()` is the version that
does something.

`strip()` with no argument removes any character that Python considers
whitespace: space, tab, newline, carriage return, form feed, vertical tab,
and a handful of Unicode spaces. With an argument it does something people
often get wrong — the argument is a *set of characters*, not a prefix:

```bash
python -c "print('banana'.strip('ban'))"
```

```text
''
```

Every character in `banana` is one of `b`, `a`, `n`, so the whole string
is eaten from both ends. If you want to remove a prefix or a suffix
exactly, Python 3.9 added `removeprefix()` and `removesuffix()`, which are
the tools that actually mean what people assume `strip()` means.

Immutability is why `.strip()` at the boundary is safe: nothing anywhere
else in the program can be holding a reference that suddenly changes under
it. It is also why building a long string by repeated `+=` in a loop is
slow — each `+=` builds a whole new string — and why `"".join(parts)` is
the idiom for that job.

</details>

## Acceptance checklist

- [ ] `python day_planner.py` asks for a name, then three tasks.
- [ ] The output is a `Today, <Name>:` heading followed by three numbered
      lines, starting at 1.
- [ ] Messy input with spaces around it produces output identical to tidy
      input.
- [ ] `main()` is annotated `-> None`, and every function has type hints.
- [ ] `.strip()` is applied in the function that reads each value, not at
      the point of printing.
- [ ] "Three" appears once in the file, as `TASK_COUNT`.
- [ ] Committed with a message like `Add day_planner CLI` and pushed to
      GitHub.

## Stretch

- Let the user choose how many tasks. Ask for a number first, and pass it
  to `prompt_tasks(count)`. Then find out what happens when they type
  `three` instead of `3`, and read the `ValueError` carefully — Week 2
  turns that into a proper conversation.
- Write the plan to a file as well as the screen, named after today's
  date. `from datetime import date` and `date.today().isoformat()` gives
  you `2026-08-23`.
- Refuse empty tasks. If somebody presses Enter without typing anything,
  ask again for that same task. Careful: this is a loop inside a loop, and
  it is easy to write one that never ends.
- Reject a task that is only whitespace *after* stripping, and notice that
  the check is now trivial because you stripped at the boundary. That is
  the payoff for the constraint at the top of this page.

That is the last of the Week 1 homework. When it is pushed, go back to
[the Week 1 mini-project](../mini-project/README.md) and finish "Hello,
You", then take [the quiz](../quiz.md).
