# Mini-Project — Number Guessing Game

This week's mini-project ties together every idea from the lectures:
`while` and `for` loops, conditionals, the accumulator pattern, guard
clauses, and a tiny dash of randomness with the standard library's
`random` module. It is the kind of game that fits on one screen but
gives you a satisfying back-and-forth in the terminal.

## What you are building

A command-line program that:

1. Picks a random integer between **1 and 100** (inclusive).
2. Repeatedly asks the user to **guess** the number.
3. After each guess, replies with `"too low"`, `"too high"`, or
   `"correct!"`.
4. Counts the number of attempts.
5. When the user guesses correctly, prints a congratulatory message
   that includes the attempt count.
6. Asks if they want to **play again**. If yes, picks a new number and
   starts over. If no, exits with a friendly goodbye.

A starter file with a skeleton and a docstring is provided at
[starter.py](./starter.py). Copy or rename it to `guessing_game.py`
before you start working — leave `starter.py` clean so others can
revisit it.

## Sample session

```text
Welcome to Guess The Number!
I am thinking of an integer between 1 and 100.

Your guess: 50
Too high.
Your guess: 25
Too low.
Your guess: 37
Too high.
Your guess: 30
Too low.
Your guess: 33
Correct! You got it in 5 attempts.

Play again? (y/n): y

I am thinking of an integer between 1 and 100.
Your guess: 42
...

Play again? (y/n): n
Thanks for playing!
```

## Requirements

You must handle all of the following:

- The secret number is generated with `random.randint(1, 100)`
  (inclusive on both ends).
- The guessing loop keeps going until the guess matches the secret.
- Each guess is converted to `int(...)`. If the user types something
  that is not a valid integer (`"abc"`, `""`), print a polite error and
  ask again **without** consuming an attempt.
- If the guess is outside the 1–100 range, print a polite reminder and
  ask again **without** consuming an attempt.
- Attempts are counted only on valid in-range numeric guesses.
- The replay prompt accepts `y`, `yes`, `n`, `no` in any case.

## Suggested structure

You will not yet have learned about functions formally (that is Week
4), but you can still organize your script with named blocks of
comments to keep it tidy:

```python
# === setup ===
import random

# === outer "play again" loop ===
while True:
    secret = random.randint(1, 100)
    attempts = 0

    # === guessing loop ===
    while True:
        raw = input("Your guess: ")
        # validate raw -> int between 1 and 100
        # if invalid, print error and `continue` (don't count it)
        # compare guess to secret, print too low / high / correct
        # if correct: break

    # === replay prompt ===
    again = input("Play again? (y/n): ").strip().lower()
    if again not in ("y", "yes"):
        print("Thanks for playing!")
        break
```

That outline maps almost line-for-line onto the spec above. Fill in the
TODOs in [starter.py](./starter.py) and you will have a clean,
beginner-readable solution.

## Rubric

When you grade yourself (or when a peer reviews your code), use this
table. Aim for "Complete" on at least the first four rows before
calling it done.

| Criterion | Incomplete | Partial | Complete |
|-----------|------------|---------|----------|
| Secret number is random in `[1, 100]` | Hard-coded value | Random but wrong range | `random.randint(1, 100)` |
| Loops until correct | Single guess only | Loops but no end condition | Clean loop with `break` on correct |
| Invalid input does not crash | Crashes on letters | Crashes on some inputs | Polite re-prompt every time |
| Attempt counter is accurate | Not tracked | Counts invalid guesses too | Counts valid in-range guesses only |
| Replay loop works | No replay | Replay loops but does not reset secret | Fresh random number every replay |
| Code style | Mixed tabs/spaces, no docstring | Some inconsistency | PEP 8 indentation, top-of-file docstring |
| Stretch features | None | One stretch goal | Two or more stretch goals |

## Stretch goals

If you want to push the mini-project further:

1. **Difficulty levels**: ask the player to choose easy (1–10), medium
   (1–100), or hard (1–1000) at the start of each round.
2. **Best score**: track the lowest attempt count across rounds in a
   single session and announce when the player beats their record.
3. **Hint system**: after every guess, print "warmer" or "colder"
   compared to the previous guess (in addition to "too high/low").
4. **Cap the attempts**: give the player a limited number of guesses
   (say, 10). If they run out, print the secret number and end the
   round.
5. **Reverse mode**: let the *computer* guess a number the *player* is
   thinking of, with the player giving "higher / lower / correct"
   feedback. A binary search makes this surprisingly snappy.

## How to submit

Push your finished game to your GitHub repository under the path
`curriculum/week-03-control-flow/mini-project/guessing_game.py` (or
the equivalent location in your own learner repo). Commit message
suggestion:

```bash
git add curriculum/week-03-control-flow/mini-project/guessing_game.py
git commit -m "Week 3 mini-project: number guessing game"
git push
```

## Why this project matters

Every concept this week shows up in this single script: a `while True`
loop with `break`, conditional branches, input validation with
`continue`, the accumulator pattern (`attempts += 1`), and a
guard-clause style for invalid input. When you can write this game
without copy-pasting the starter, you have internalized Week 3.
