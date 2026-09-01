# Mini-Project Starter — Number Guessing Game

> **Project:** [Mini-Project — Number Guessing Game](./README.md)
> **Week:** 3
> **What this is:** the scaffold for the Week 3 mini-project. Copy the block
> below into a file called `guessing_game.py` in your Week 3 folder, then fill
> in the five `TODO`s. It runs the moment you paste it, so you are always
> editing a program that works rather than one that does not.

One note before you start. The project README sketches the game as a flat
script with comment banners, because it was written assuming you had not met
`def` yet. Every exercise this week uses small named functions instead, and so
does this starter — it is the same logic, cut into three pieces that each fit
on one screen. Week 4 formalizes what a function is; using them a week early
costs you nothing and makes the guessing loop far easier to read.

## How to use this page

1. Open a terminal in your Week 3 folder and activate the virtual
   environment. Your prompt should show `(.venv)`.

2. Create the file:

   ```bash
   touch guessing_game.py
   ```

   On Windows PowerShell, `New-Item guessing_game.py` does the same job.

3. Paste in the whole code block from the section below, unchanged.

4. Run it before you edit anything:

   ```bash
   python guessing_game.py
   ```

   It prints the welcome lines, admits it is not built yet, tells you what the
   secret number would have been, and exits. Nothing hangs and nothing
   crashes. That is your baseline.

5. Work the `TODO`s in order: TODO 1 and 2 build the input reader, TODO 3 and
   4 build the guessing loop, TODO 5 builds the rematch prompt. Run the
   program after each one.

6. Delete the placeholder `print` in `play_round()` once TODO 4 works, and
   delete each `# TODO:` comment as you satisfy it. Leaving the secret on
   screen makes for a short game.

## The starter

```python
"""guessing_game.py — guess the secret number between 1 and 100.

Week 3 mini-project for Code Crunch Convos. Picks a random integer,
takes guesses until one is right, counts only the valid guesses, and
offers a rematch. Run it with: python guessing_game.py
"""

import random

LOWEST: int = 1
HIGHEST: int = 100
YES_ANSWERS: tuple[str, ...] = ("y", "yes")


def read_guess() -> int:
    """Prompt until the user types a whole number in range, then return it.

    Returns:
        A guess between LOWEST and HIGHEST inclusive. Invalid answers are
        reported and re-asked here, so the caller only ever sees a good
        number and never has to count a bad one.
    """
    while True:
        raw: str = input("Your guess: ")
        # TODO 1: try int(raw). On ValueError, print
        #         f"{raw!r} is not a whole number. Try again."
        #         and `continue` so the loop asks again.
        # TODO 2: if the number is outside LOWEST..HIGHEST, print
        #         f"Stay between {LOWEST} and {HIGHEST}. Try again."
        #         and `continue`. Otherwise return it.
        return LOWEST


def play_round(secret: int) -> int:
    """Take guesses until secret is found and return the attempt count.

    Args:
        secret: the number the player is trying to find.

    Returns:
        How many valid, in-range guesses it took.
    """
    attempts: int = 0
    # TODO 3: loop forever. Each pass, call read_guess() and add one to
    #         attempts. Only valid guesses reach here, so every pass counts.
    # TODO 4: compare the guess to secret. Print "Too low." or "Too high."
    #         and keep looping; on a match print
    #         f"Correct! You got it in {attempts} attempts."
    #         and return attempts.
    print(f"(not built yet - the secret was {secret})")
    return attempts


def wants_rematch() -> bool:
    """Ask whether to play another round and return True for yes."""
    print()
    # TODO 5: read the answer with input("Play again? (y/n): "), strip it,
    #         lower it, and return whether it is in YES_ANSWERS.
    return False


def main() -> None:
    """Play rounds until the user declines a rematch."""
    print("Welcome to Guess The Number!")
    while True:
        print(f"I am thinking of an integer between {LOWEST} and {HIGHEST}.")
        print()
        play_round(random.randint(LOWEST, HIGHEST))
        if not wants_rematch():
            print("Thanks for playing!")
            return
        print()


if __name__ == "__main__":
    main()
```

## What each TODO is asking for

- **TODO 1 — survive a non-number.** Wrap `int(raw)` in a `try`, and catch
  `ValueError` specifically rather than writing a bare `except`. A bare
  `except` also swallows Ctrl+C, which would leave a player with no way out of
  the loop except closing the terminal. In the handler, print the complaint
  and `continue`. `continue` jumps straight back to the top of the `while`,
  which is exactly "ask again" — and crucially it skips the `return`, so
  nothing invalid ever leaves this function.
- **TODO 2 — reject out-of-range numbers.** `150` is a perfectly good integer
  and a useless guess. Test it with a chained comparison —
  `if not LOWEST <= guess <= HIGHEST:` reads the way you would say it out
  loud, and Python evaluates it as the two comparisons joined by `and`. Print
  the reminder, `continue`, and let the loop ask again. This is a guard
  clause: handle the bad case and leave, so the good case below it needs no
  indentation.
- **TODO 3 — the attempt counter.** `while True:` with `read_guess()` at the
  top. `attempts += 1` is the accumulator pattern from Lecture 3 section 1,
  and the reason it belongs *here* rather than inside `read_guess()` is the
  spec: only valid, in-range guesses count. Because `read_guess()` returns
  nothing else, putting the increment in this loop makes that rule true by
  construction rather than by remembering to check.
- **TODO 4 — the three-way comparison.** An `if`/`elif`/`else` chain: less
  than, greater than, otherwise equal. The `else` is the win, and it is the
  only branch that returns. Do not write a separate `if guess == secret:`
  after the chain — the `else` already means exactly that, and a fourth test
  is a fourth chance to get it wrong.
- **TODO 5 — the rematch answer.** Chain three things onto `input()`:
  `.strip()` to drop stray spaces, `.lower()` so `Y` and `YES` work, then test
  membership with `in YES_ANSWERS`. Return that comparison directly rather
  than writing `if ...: return True else: return False` — the comparison is
  already a `bool`. Anything that is not a yes is a no, which is the safe
  default for a question about continuing.

## Expected output when you are done

One session with two rounds. The second round deliberately types nonsense and
then an out-of-range number, so you can see that neither one costs an
attempt — seven prompts, five counted guesses.

```text
$ python guessing_game.py
Welcome to Guess The Number!
I am thinking of an integer between 1 and 100.

Your guess: 50
Too low.
Your guess: 75
Too high.
Your guess: 62
Too high.
Your guess: 58
Correct! You got it in 4 attempts.

Play again? (y/n): y

I am thinking of an integer between 1 and 100.

Your guess: seventy
'seventy' is not a whole number. Try again.
Your guess: 150
Stay between 1 and 100. Try again.
Your guess: 50
Too low.
Your guess: 80
Too high.
Your guess: 70
Too low.
Your guess: 75
Too high.
Your guess: 72
Correct! You got it in 5 attempts.

Play again? (y/n): n
Thanks for playing!
```

Your secret numbers will differ, so the guesses will too. What must match is
the shape: the two error messages, the blank line before each
`Play again?`, and an attempt count that ignores the two rejected inputs.

## Common bugs to catch

- **`ValueError: invalid literal for int() with base 10: 'seventy'`.** The
  `int()` call is outside the `try` block, or TODO 1 is still a placeholder.
  Check the indentation — the `int(raw)` line has to sit under `try:`, not
  beside it.
- **The program hangs and never asks anything.** You wrote `while True:` in
  `play_round()` but the body has no `read_guess()` call in it, so the loop
  spins on nothing. Press Ctrl+C to escape and put the call back.
- **The game never ends even when you guess right.** Your winning branch
  prints the congratulations but does not `return`. `break` would work too,
  but then `play_round()` falls off the end and gives back `None` instead of
  the count. Return the number.
- **It says `You got it in 1 attempts.` after seven guesses.** The
  `attempts += 1` line is inside the `else` branch instead of at the top of
  the loop, so it only runs on the winning guess. Increment once per pass,
  before you compare. While you are there: `1 attempts` reads badly. Fixing
  the singular is a two-line change and a good first stretch goal.
- **Invalid guesses still cost an attempt.** You moved the counter into
  `read_guess()`. Move it back — `read_guess()` cannot know how many attempts
  a round has had, and it should not have to.
- **`UnboundLocalError: cannot access local variable 'guess'`.** Your `return`
  in `read_guess()` is inside the `except` block, or the range check is
  reading `guess` on a pass where the `int()` cast failed. After a `continue`
  in the handler, nothing below it runs on that pass — which is the point.
- **`Play again? (y/n): Y` starts a new round but `YES` does not.** You called
  `.lower()` on the wrong side, or compared before lowering. The order is
  read, strip, lower, then test.
- **Every round uses the same secret.** `random.randint()` is called once,
  above the outer loop. It has to be called inside it, once per round, which
  is why `main()` passes a fresh value into `play_round()` each time.

## When you are done

Check yourself against the rubric in the project README. Aim for "Complete" on
at least the first four rows.

- [ ] The secret comes from `random.randint(LOWEST, HIGHEST)` and both ends
      are reachable.
- [ ] The guessing loop runs until the guess matches, then stops.
- [ ] Letters, empty input, and out-of-range numbers all get a polite message
      and a fresh prompt, with no traceback.
- [ ] The attempt count includes only valid in-range guesses.
- [ ] Answering `y` starts a new round with a new secret; `n` prints
      `Thanks for playing!` and exits.
- [ ] The file has a module docstring, every function has a docstring and type
      hints, and the indentation is four spaces throughout.
- [ ] No `TODO` comments and no placeholder `print` are left in the file.
- [ ] At least one stretch goal from the project README is in place, and you
      can say in one sentence what it changed.
- [ ] Committed and pushed:

      ```bash
      git add curriculum/week-03-control-flow/mini-project/guessing_game.py
      git commit -m "Week 3 mini-project: number guessing game"
      git push
      ```

Then delete the file and write it again from a blank page. It takes about ten
minutes the second time, and the second time is the one that proves you have
Week 3.
