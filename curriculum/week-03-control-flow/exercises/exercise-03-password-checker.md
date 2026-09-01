# Exercise 3 — Password Checker

> **Topic:** `while True`, `break`, `continue`, `any()`, and guard clauses
> **Lecture:** [02 — Loops: Doing Things Repeatedly](../lecture-notes/02-loops.md)
> **Difficulty:** Easy
> **Target time:** 25 minutes
> **Why this one:** `while True` with a `break` is the shape of every interactive program you will ever write — menus, prompts, retry loops, the guessing game at the end of this week. It is also the fastest way to write a program that never stops, so learning exactly where the `break` goes is not optional. On top of that it makes you collect *every* reason something failed instead of bailing at the first one, which is the difference between a form that helps a person and one that fights them.

## The Brief

You are writing the sign-up prompt for the Code Crunch practice server.
Somebody types a password. If it breaks any of the rules, you tell them
**every** rule it broke — not just the first one — and ask again. When they
finally type something acceptable, you say so and stop asking.

The "every rule" part matters more than it looks. Picture a checker that
stops at the first problem. Someone fixes the length, sends it again,
learns they also need a digit, fixes that, sends it again, and learns it
was on the banned list all along. Three round trips for one decision, and
they are annoyed by the second one. Gather the problems into a list and
print them together.

Two of the four rules are cleanest with `any()`. `any(...)` looks at a
row of true-or-false answers and says `True` if at least one of them is
true. Pair it with a small loop expression and it reads almost like
English: `any(ch.isdigit() for ch in candidate)` is "is there any character
in this candidate that is a digit". You met `any` in the preview list at
the end of Lecture 3. This is where you use it.

One more thing this program teaches, quietly. A password should never end
up in a file, a screenshot or a terminal history. So the prompt and the
typing go to one place, and the checker's verdict goes to another. That is
what the two output streams are for, and this page explains them where they
come up.

## Starter

Create `exercise-03-password-checker.py` in your practice repo, paste this
in, then fill in the four `TODO`s:

```python
"""exercise-03-password-checker.py — retry loop with a full problem report.

Prompts until the typed password satisfies every rule, listing all the
rules it breaks on each attempt.

Two ways to run it:

    python exercise-03-password-checker.py         walks the sample session
    python exercise-03-password-checker.py --ask   asks you to type

The sample session is the default so that a run with nobody at the
keyboard prints the same six lines every time instead of waiting for
typing that is never coming.

The prompt and the password go to stderr; only the verdict goes to
stdout. That is why `python … > report.txt` saves the verdict and never
saves a password.
"""

import sys

MIN_LENGTH = 12
BLOCKLIST = ("password1234", "qwertyuiop12", "letmein12345")

ASK_FLAG = "--ask"
PROMPT = "> "
DEMO_ATTEMPTS = ("crunch", "123456789012", "letmein12345", "crunchtime12")
DEMO_NOTE = f"Walking the sample session. Pass {ASK_FLAG} to type your own."
DEMO_EXHAUSTED = "Sample session ran out with nothing acceptable in it."


def find_problems(candidate: str) -> list[str]:
    """Return a list of human-readable reasons `candidate` is unacceptable.

    An empty list means the candidate passed every rule.
    """
    problems: list[str] = []
    if len(candidate) < MIN_LENGTH:
        problems.append(
            f"Too short: {len(candidate)} characters, minimum is {MIN_LENGTH}."
        )
    # TODO: append a problem if the candidate contains no digit.
    # TODO: append a problem if the candidate contains no letter.
    # TODO: append a problem if the candidate is on the blocklist,
    #       compared without caring about capitals.
    return problems


def read_candidate(attempt: int, interactive: bool) -> str:
    """Return the password for this attempt, typed or scripted.

    `attempt` is 1 on the first pass, 2 on the second, and so on. The
    prompt and the scripted answer both go to stderr, so no password
    ever reaches stdout.
    """
    print(PROMPT, end="", file=sys.stderr, flush=True)
    if interactive:
        return input()
    scripted = DEMO_ATTEMPTS[attempt - 1]
    print(scripted, file=sys.stderr)
    return scripted


def main() -> None:
    """Prompt until the password is acceptable, then report the attempt count."""
    interactive = ASK_FLAG in sys.argv[1:]
    if not interactive:
        print(DEMO_NOTE, file=sys.stderr)

    print("Choose a password. It is never printed back to you.")
    attempts = 0

    while True:
        if not interactive and attempts == len(DEMO_ATTEMPTS):
            print(DEMO_EXHAUSTED)
            break

        attempts += 1
        candidate = read_candidate(attempts, interactive)
        problems = find_problems(candidate)

        # TODO: if there are problems, print each one indented with "  - "
        #       and continue to the next attempt.

        print(f"Password accepted after {attempts} attempts.")
        break


if __name__ == "__main__":
    main()
```

`read_candidate()` and the `--ask` handling are written for you. You are
filling in the three missing rules and the guard in `main()`.

Four words you need before you start.

**`while True`.** A loop with a condition that is always true, so the only
way out is a `break` inside it. That sounds reckless and it is the standard
shape for "keep asking until something happens", because the reason you
stop is usually something you learn *inside* the loop, not before it.

**`break` and `continue`.** `break` leaves the loop for good. `continue`
abandons the rest of *this* pass and goes straight back to the top for the
next one.

**stdout and stderr.** Every program has two output pipes. `print()` uses
the first one, stdout, which is what `>` captures into a file. The second
one, stderr, is where prompts and warnings go, and it goes to the screen
even when stdout has been redirected. Keeping them separate is why this
program can be run with `> report.txt` and save a report with no passwords
in it.

**Blocklist.** A short list of passwords nobody is allowed to use, because
they are the first things anyone guesses.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/exercises/exercise-03-password-checker.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Four rules, checked on every attempt, all reported together:
   - at least `MIN_LENGTH` characters,
   - at least one digit,
   - at least one letter,
   - not on `BLOCKLIST`, compared without caring about capitals.
2. `find_problems()` returns a list of strings. An empty list means "this
   one is fine". It never prints anything and never reads anything.
3. The digit and letter rules use `any()` with `str.isdigit()` and
   `str.isalpha()` applied to single characters.
4. Each problem prints on its own line, indented, in the form
   `  - Too short: 6 characters, minimum is 12.`
5. The success exit is the empty-problems path, and the final line is
   `Password accepted after N attempts.` with the real count, the
   successful attempt included.
6. The program never prints the candidate password to stdout — not on
   success, not in a problem message, not anywhere.

## Constraints

- **Use `while True` with a `break`, not a flag variable.** A
  `done = False` flag takes three lines to do what `break` does in one, and
  every one of those three lines is somewhere to forget an update and loop
  forever. This is the idiom from
  [Lecture 2 §1](../lecture-notes/02-loops.md), and it is the backbone of
  this week's mini-project.
- **Use `continue` as your guard clause.** When there are problems, print
  them and jump to the next attempt. The alternative — wrapping the success
  path in an `else` — pushes the important lines one indent deeper for
  nothing. Lecture 1 calls this the early return. Inside a loop, `continue`
  is its twin.
- **Do not call `.strip()` on the input.** For a name or a menu choice,
  trimming stray spaces is a kindness. For a password it is a bug: a space
  is a perfectly legal password character, and silently deleting one means
  the password you stored is not the password they typed. `input()` has
  already removed the newline. Leave the rest of the line alone.
- **Lowercase only for the blocklist comparison.** Write
  `candidate.lower() in BLOCKLIST` and do not reassign `candidate` itself.
  The check should ignore capitals; the password must not.
- **Keep the blocklist to three entries in a tuple.** A real blocklist has
  millions of entries and lives in a file, which needs file reading
  (Week 6) and a set for fast lookup (Week 5). Three is enough to exercise
  the branch, and a tuple says out loud that it never changes while the
  program runs.
- **Report every problem, never just the first.** This is the one place
  this week where bailing out early is the *wrong* tool, which is why
  `find_problems()` builds a list instead of returning at the first
  failure.
- **No `try` / `except` anywhere.** Exceptions are Week 6. Everything here
  is checked with what Week 3 gives you: `len()`, `in`, comparisons, string
  methods and guard clauses.
- **`def` is Week 4, and these five exercises are the deliberate exception:
  the starter hands you the function headers already written, so you are
  filling in a body someone else declared rather than deciding what a
  function should be.**

## Expected output

Run with no arguments, the program walks a scripted sample session so it
behaves the same way every time. This is its real stdout, captured on
CPython 3.13.2:

```text
$ python exercise-03-password-checker.py
Choose a password. It is never printed back to you.
  - Too short: 6 characters, minimum is 12.
  - No digits: add at least one 0-9.
  - No letters: add at least one A-Z or a-z.
  - That password is on the community blocklist. Pick something else.
Password accepted after 4 attempts.
```

No password appears in there, which is requirement 6 holding. That is not
an accident of the sample data — the prompt and the password are printed to
stderr, and stdout gets only the verdict.

On your screen both streams land in the same window, so what you actually
*see* is this:

```text
$ python exercise-03-password-checker.py
Walking the sample session. Pass --ask to type your own.
Choose a password. It is never printed back to you.
> crunch
  - Too short: 6 characters, minimum is 12.
  - No digits: add at least one 0-9.
> 123456789012
  - No letters: add at least one A-Z or a-z.
> letmein12345
  - That password is on the community blocklist. Pick something else.
> crunchtime12
Password accepted after 4 attempts.
```

Send stdout to a file and the difference becomes obvious:

```bash
python exercise-03-password-checker.py > report.txt
```

The prompts and the passwords still appear on screen. `report.txt` holds
only the six verdict lines.

Look closely at the last two attempts. `letmein12345` is exactly twelve
characters, has digits, and has letters — it passes three rules out of four
and must still be rejected. `crunchtime12` is also exactly twelve
characters, which is the *minimum*, so it must be **accepted**. If you
wrote the length test as `len(candidate) <= MIN_LENGTH`, that is the input
that catches you.

## Steps

1. Create `exercise-03-password-checker.py` and paste the starter in. The
   length rule is already written as a worked example of the shape the
   other three take.
2. Fill in the three remaining rules in `find_problems()`. Run nothing yet.
3. Test the function on its own before you test the loop. Run
   `python -i exercise-03-password-checker.py`, let the sample session
   finish, and then at the `>>>` prompt:

   ```text
   >>> find_problems("crunchtime12")
   []
   >>> len(find_problems(""))
   3
   ```

   Three problems for the empty string: too short, no digits, no letters.
   It is not on the blocklist, so the fourth rule correctly stays quiet.
4. Fill in the `if problems:` guard in `main()`: loop over the problems,
   print each with the `  - ` prefix, then `continue`.
5. Run it plain: `python exercise-03-password-checker.py`. Compare against
   the screen version above, line for line.
6. Now run it for real: `python exercise-03-password-checker.py --ask`, and
   type the same four passwords by hand. You should get the same verdicts.
7. Try to break it. Type twelve spaces, then `PASSWORD1234` in capitals.
   Twelve spaces are long enough and should fail on digits and letters; the
   capitalised blocklist entry should still be blocked. The verdict lines,
   with the prompts and your typing left out, are:

   ```text
   Choose a password. It is never printed back to you.
     - No digits: add at least one 0-9.
     - No letters: add at least one A-Z or a-z.
     - That password is on the community blocklist. Pick something else.
   Password accepted after 3 attempts.
   ```

## The Solution

```python
"""exercise-03-password-checker-solution.py — retry loop with a full problem report.

Prompts until the typed password satisfies every rule, listing all the
rules it breaks on each attempt.

Two ways to run it:

    python exercise-03-password-checker-solution.py         walks the sample session
    python exercise-03-password-checker-solution.py --ask   asks you to type

The sample session is the default so that a run with nobody at the
keyboard prints the same six lines every time instead of waiting for
typing that is never coming.

The prompt and the password go to stderr; only the verdict goes to
stdout. That is why `python … > report.txt` saves the verdict and never
saves a password.
"""

import sys

MIN_LENGTH = 12
BLOCKLIST = ("password1234", "qwertyuiop12", "letmein12345")

ASK_FLAG = "--ask"
PROMPT = "> "
DEMO_ATTEMPTS = ("crunch", "123456789012", "letmein12345", "crunchtime12")
DEMO_NOTE = f"Walking the sample session. Pass {ASK_FLAG} to type your own."
DEMO_EXHAUSTED = "Sample session ran out with nothing acceptable in it."


def find_problems(candidate: str) -> list[str]:
    """Return a list of human-readable reasons `candidate` is unacceptable.

    An empty list means the candidate passed every rule.
    """
    problems: list[str] = []
    if len(candidate) < MIN_LENGTH:
        problems.append(
            f"Too short: {len(candidate)} characters, minimum is {MIN_LENGTH}."
        )
    if not any(ch.isdigit() for ch in candidate):
        problems.append("No digits: add at least one 0-9.")
    if not any(ch.isalpha() for ch in candidate):
        problems.append("No letters: add at least one A-Z or a-z.")
    if candidate.lower() in BLOCKLIST:
        problems.append(
            "That password is on the community blocklist. Pick something else."
        )
    return problems


def read_candidate(attempt: int, interactive: bool) -> str:
    """Return the password for this attempt, typed or scripted.

    `attempt` is 1 on the first pass, 2 on the second, and so on. The
    prompt and the scripted answer both go to stderr, so no password
    ever reaches stdout.
    """
    print(PROMPT, end="", file=sys.stderr, flush=True)
    if interactive:
        return input()
    scripted = DEMO_ATTEMPTS[attempt - 1]
    print(scripted, file=sys.stderr)
    return scripted


def main() -> None:
    """Prompt until the password is acceptable, then report the attempt count."""
    interactive = ASK_FLAG in sys.argv[1:]
    if not interactive:
        print(DEMO_NOTE, file=sys.stderr)

    print("Choose a password. It is never printed back to you.")
    attempts = 0

    while True:
        if not interactive and attempts == len(DEMO_ATTEMPTS):
            print(DEMO_EXHAUSTED)
            break

        attempts += 1
        candidate = read_candidate(attempts, interactive)
        problems = find_problems(candidate)

        if problems:
            for problem in problems:
                print(f"  - {problem}")
            continue

        print(f"Password accepted after {attempts} attempts.")
        break


if __name__ == "__main__":
    main()
```

**Four plain `if`s, deliberately not a chain.** Everywhere else this week,
two branches that could both be true is a bug. Here it is the requirement.
A candidate can be too short *and* have no digits, and the person typing
deserves to hear both at once. So the four checks are independent
statements, each adding to the same list, and not one of them is an `elif`.
Knowing *why* the usual rule is suspended here is worth more than the rule
itself.

**An empty list is the "everything passed" signal, and an empty list counts
as false.** `find_problems` never returns `None` and never returns a status
code. It returns a list that happens to be empty when there is nothing to
say. That is what lets `main()` write `if problems:` and have it read as
English ([Lecture 1 §4](../lecture-notes/01-conditionals.md)):

```text
>>> bool([])
False
>>> bool(['Too short: 6 characters, minimum is 12.'])
True
```

You never need `if len(problems) > 0:`. The container's own truth value
already means "has anything in it".

**`any(ch.isdigit() for ch in candidate)` asks about characters;
`candidate.isdigit()` asks about the whole string.** Two different
questions, and the second one is not yours:

```text
>>> "crunchtime12".isdigit()
False
>>> any(ch.isdigit() for ch in "crunchtime12")
True
```

`str.isdigit()` on a whole string means "is *every* character a digit",
which is only true of something like `"12345"`. The `any(...)` form walks
the characters one at a time and stops at the first digit it finds, which
is "at least one". `not any(...)` is then "none at all", and that is when a
problem gets added.

**Guard clause, then `continue`.** Inside a loop, `continue` is what
`return` is inside a function: a way to say "this pass is over, do not read
further" ([Lecture 2 §7](../lecture-notes/02-loops.md)). The success path —
the accepted message and the `break` — sits at the loop's own level rather
than inside an `else`, so the two lines that matter are not indented one
step deeper for nothing. If you ever find yourself writing `else:` after a
block that already ends in `continue`, delete the `else` and pull the body
back out.

**`attempts += 1` at the top, `break` on the success path.** The counter
goes up before the password is read, so the attempt being made right now is
already counted. That is what makes the last line say 4 and not 3 for a
session with three rejections, which is what requirement 5 asks for.
Increment before, report after.

**`<` and not `<=`, and only one input in the sample session reveals it.**
`crunchtime12` is exactly twelve characters, the stated minimum, and must
be accepted. `len(candidate) < MIN_LENGTH` is the rule "shorter than the
minimum is a problem". `<=` would make the minimum itself a problem. When
you write a bound, test the bound.

**Case-insensitive check, case-sensitive password.**
`candidate.lower() in BLOCKLIST` lowercases a *copy* for the comparison and
leaves `candidate` untouched. Writing `candidate = candidate.lower()`
instead would work for the blocklist and quietly ruin everything after it —
the password you accepted would not be the password that was typed. Every
entry in `BLOCKLIST` is already lowercase, which is what makes lowering
just the one side enough.

**No `.strip()`, and it is not an oversight.** A space is a legal password
character. Trimming one means storing something the person did not type.

**The password never reaches stdout.** Not on success, not in a problem
message — the "too short" message reports the *length*, a number, rather
than the text. The prompt and the typing go to stderr, which your terminal
shows you and a redirect does not capture. Anything a program prints to
stdout can end up in a log file, a pasted transcript or a screenshot.

**Two ways out of the loop, on purpose.** The success `break` is the one
you designed. The `DEMO_EXHAUSTED` guard at the top is the one that stops
the scripted session from spinning forever if a rule is wrong. Without it,
a broken rule that rejects the last sample password means the program asks
for a fifth attempt that does not exist and never stops. A loop with only
one exit is a loop that can hang, and hanging is a much worse way to fail
than printing a sentence and stopping.

**What Week 4 will change here: almost nothing.** `find_problems` is
already a *pure* function — same input, same output, no printing, no
reading. That is exactly the property that will make it testable in Week 11
and reusable in the Week 9 web form. The function you were handed is shaped
better than the one you would have written inline, and it is worth noticing
why.

## Download and run

Download
[exercise-03-password-checker-solution.py](./exercise-03-password-checker-solution.py)
and run it:

```bash
python exercise-03-password-checker-solution.py
```

Add `--ask` to type your own passwords instead of watching the sample
session:

```bash
python exercise-03-password-checker-solution.py --ask
```

It is the same program as the one you are writing, under a name that will
not collide with your own `exercise-03-password-checker.py`.

## Common bugs to catch

- **Every password is accepted, even a six-character one.**
  `find_problems()` is missing its `return problems` on some path, so it
  hands back `None`:

  ```text
  Walking the sample session. Pass --ask to type your own.
  Choose a password. It is never printed back to you.
  > crunch
  Password accepted after 1 attempts.
  ```

  `if None:` is false, so `main()` sails straight past the guard. A
  function that runs out of body hands back `None`. Always return the list.

- **The digit rule never fires.** You wrote
  `any(ch.isdigit for ch in candidate)` without the call brackets:

  ```text
  Walking the sample session. Pass --ask to type your own.
  Choose a password. It is never printed back to you.
  > crunch
    - Too short: 6 characters, minimum is 12.
  > 123456789012
    - No letters: add at least one A-Z or a-z.
  > letmein12345
    - That password is on the community blocklist. Pick something else.
  > crunchtime12
  Password accepted after 4 attempts.
  ```

  Look at the first attempt: `crunch` has no digit at all and nobody
  mentioned it. Without the `()` you are not calling the method, you are
  collecting the method itself — a real object, and every real object
  counts as true. `any()` then says `True` for any non-empty string, so
  `not any(...)` is never true and the rule never fires. **When a check
  silently never fires, look for a missing `()`.**

- **`crunchtime12` is reported as having no digits, and the sample session
  runs out.** The mirror image: you wrote `not candidate.isdigit()`
  instead of the `any` form, so the rule fires when it should not:

  ```text
  > letmein12345
    - No digits: add at least one 0-9.
    - That password is on the community blocklist. Pick something else.
  > crunchtime12
    - No digits: add at least one 0-9.
  Sample session ran out with nothing acceptable in it.
  ```

  Perfectly good passwords are rejected for a fault they do not have,
  because you asked whether the whole string was digits. That last line is
  the second loop exit earning its keep: with only the success `break`,
  this run would never have stopped.

- **It prints the problems and then accepts the password anyway.** The
  `continue` is missing:

  ```text
  Choose a password. It is never printed back to you.
    - Too short: 6 characters, minimum is 12.
    - No digits: add at least one 0-9.
  Password accepted after 1 attempts.
  ```

  Printing is not deciding. Without `continue`, execution walks straight
  out of the `if` block and into the success path on the same pass.

- **The program congratulates you and then asks again.** The `break` is
  inside the `if problems:` block, or it is missing entirely. It belongs on
  the success path, after the accepted message, at the same indentation as
  that `print`.

- **Nothing is ever accepted and the prompt never stops.** Press `Ctrl+C`.
  Then check whether one of your rules is inverted — an `if any(...)` where
  you meant `if not any(...)`. The "no digits" problem should be added when
  there is **no** digit.

- **`PASSWORD1234` in capitals gets through.** Your blocklist comparison is
  case-sensitive. `candidate.lower() in BLOCKLIST` fixes it, and every
  entry in `BLOCKLIST` has to be lowercase already for that to work.

- **`EOFError: EOF when reading a line`.** You ran it with `--ask` and
  piped input in, and the pipe ran dry while the loop was still asking:

  ```text
  Choose a password. It is never printed back to you.
  >   - Too short: 6 characters, minimum is 12.
    - No digits: add at least one 0-9.
  > Traceback (most recent call last):
    File "exercise-03-password-checker.py", line 96, in <module>
      main()
      ~~~~^^
    File "exercise-03-password-checker.py", line 83, in main
      candidate = read_candidate(attempts, interactive)
    File "exercise-03-password-checker.py", line 62, in read_candidate
      return input()
  EOFError: EOF when reading a line
  ```

  That is the input running out, not a bug in your rules. Feed it more
  lines, or drop the `--ask` and let the sample session drive. Week 6 shows
  you how to catch that one and turn it into a polite goodbye.

## Under the hood

<details>
<summary>Under the hood — how any() and a generator expression stop early</summary>

`any(ch.isdigit() for ch in candidate)` does not test every character. It
tests characters until one of them says yes, and then it stops.

The part in the brackets is a **generator expression**. It is not a list
and it does not build one. It is a set of instructions for producing values
one at a time, and it produces the next one only when something asks. You
can watch it happen by writing a version that narrates:

```python
def looked(text):
    for ch in text:
        print("looking at", repr(ch))
        yield ch.isdigit()
```

```text
>>> any(looked("ab1cdefgh"))
looking at 'a'
looking at 'b'
looking at '1'
True
```

Three characters looked at out of nine. `any()` asked for a value, got
`False`, asked again, got `False`, asked again, got `True`, and returned
immediately. Nobody ever looked at `'c'`.

This matters twice over.

**It is fast on the cases you care about.** A password with a digit near
the front costs three character tests, not the length of the password. On a
twelve-character password nobody notices. On a scan through a million-line
file, "stop at the first hit" is the entire performance story.

**It is what lets `any()` be safe.** Because the generator has not produced
the later values yet, nothing later has been evaluated. That is the same
guarantee `and` gives you, and you rely on it whenever a later test would
only make sense if an earlier one passed.

The mirror image is `all()`, which stops at the first `False`. Both of them
also have a defined answer for nothing at all, and the answers surprise
people:

```text
>>> any([])
False
>>> all([])
True
```

`any([])` is false because there is nothing in there that is true.
`all([])` is true because there is nothing in there that is false. `all()`
on an empty sequence being `True` catches people out constantly — a rule
like "every character must be allowed" quietly passes an empty password.
This program dodges it by testing the length separately, which is one more
reason the four rules are four separate `if`s.

**Why not a plain loop?** You could write:

```python
has_digit = False
for ch in candidate:
    if ch.isdigit():
        has_digit = True
        break
```

Six lines, one flag variable, one `break`, and one chance to forget the
`break` and turn it into a full scan. `any()` is that loop with a name.
When you meet `any()` in someone else's code, read it as exactly this loop
and you will never be surprised by it.

</details>

<details>
<summary>Under the hood — why prompts go to stderr, and what a redirect really does</summary>

When your program starts, the operating system hands it three open
channels: **stdin** (number 0) to read from, **stdout** (1) to write
results to, and **stderr** (2) to write everything else to. They are not a
Python invention. Every program on your machine gets the same three.

`print()` writes to stdout. `print(..., file=sys.stderr)` writes to stderr.
On a terminal both arrive in the same window, in order, which is why the
screen version of this program looks like an ordinary conversation.

The moment you redirect, they come apart:

```bash
python exercise-03-password-checker.py > report.txt   # stdout to the file
python exercise-03-password-checker.py 2> log.txt     # stderr to the file
python exercise-03-password-checker.py > out.txt 2>&1 # both to one file
```

`2>` means "channel 2", stderr. `2>&1` means "send channel 2 wherever
channel 1 is already going".

So the split is a design decision with a consequence you can see. Results
on stdout means the program can be a piece of a pipeline — something else
can read what it produced. Prompts and status on stderr means those never
contaminate the result. It is why `python thing.py > out.txt` saves the
answer and not the questions, and here it is why a saved report contains no
passwords.

**The trap this program avoids.** `input("> ")` looks like the obvious way
to prompt, and it writes that `> ` to **stdout**, which puts it in the
saved file. That is why `read_candidate()` prints the prompt to stderr
first and then calls `input()` with no argument at all.

**Why the `flush=True`.** Output to a terminal is usually sent a line at a
time, but a prompt has no newline on the end — that is the point of
`end=""`. Without a nudge it could sit in a buffer while the program waits
for typing, so you would be staring at a blank line wondering what it
wanted. `flush=True` pushes it out immediately. stderr is unbuffered by
default in Python, so this particular `flush` is belt and braces, and it is
the habit that saves you when the same line is on stdout.

**One ordering wrinkle worth knowing.** When stdout goes to a terminal
Python sends it a line at a time, so stdout and stderr interleave the way
you would expect. When stdout goes to a *pipe or a file*, Python buffers it
in larger chunks for speed, and the two streams can come out grouped rather
than interleaved. That is not a bug and it does not affect either stream's
own contents. If you ever need strict interleaving while piping, run
`python -u`, which turns the buffering off.

</details>

## Acceptance checklist

- [ ] `python exercise-03-password-checker.py` runs and stops on its own.
- [ ] A single bad attempt can print more than one problem line.
- [ ] `crunchtime12` is accepted; `letmein12345` and `PASSWORD1234` are not.
- [ ] An empty password reports exactly three problems.
- [ ] `find_problems()` contains no `print()` and reads no input.
- [ ] No password appears in `report.txt` after
      `python exercise-03-password-checker.py > report.txt`.
- [ ] `python exercise-03-password-checker.py --ask` lets you type, and
      gives the same verdicts for the same four passwords.
- [ ] Committed to Git with a message like `Add Week 3 exercise 3: password checker`.

## Stretch

- Cap the attempts at five. When the cap is hit, print a refusal and
  `break` out from the failure path too. Your loop now has three exits and
  you have to decide what the last line should say for each one.
- Strip the file back to the plain interactive version. Delete the flag,
  the sample session and the exhausted guard; delete `read_candidate()` and
  put `candidate = input("> ")` in its place. It is a good deal shorter,
  and it is what most people write first. Type the four passwords and the
  screen looks exactly like the sample session above with the first line
  gone.

  Then run it two ways it was never going to survive. First, with nobody
  typing — pipe an empty file into it:

  ```text
  Choose a password. It is never printed back to you.
  > Traceback (most recent call last):
    File "exercise-03-password-checker.py", line 45, in <module>
      main()
      ~~~~^^
    File "exercise-03-password-checker.py", line 32, in main
      candidate = input("> ")
  EOFError: EOF when reading a line
  ```

  Second, with stdout redirected. Type one good password and then look at
  the file:

  ```text
  Choose a password. It is never printed back to you.
  > Password accepted after 1 attempts.
  ```

  The `> ` prompt is in the saved file, because `input("> ")` writes its
  prompt to **stdout**. Those two runs are the whole argument for the
  shipped shape: a sample session so it can run unattended, and prompts on
  stderr so a redirect saves a report and not a conversation.
- Replace `input()` with `getpass.getpass("")` from the standard library so
  the characters do not appear on screen at all. Run it and notice that
  your typing has vanished from the transcript, which is the whole purpose
  of that function.
- Add a fifth rule that rejects a candidate made of one repeated character,
  such as `aaaaaaaaaaaa`. It is one line if you remember that
  `set(candidate)` collapses duplicates, and a small loop if you do not.

When the loop stops exactly when it should, move on to
[Exercise 4 — Multiplication Table](./exercise-04-multiplication-table.md).
