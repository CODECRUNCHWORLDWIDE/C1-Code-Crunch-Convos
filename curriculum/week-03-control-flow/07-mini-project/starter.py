"""
Week 3 Mini-Project — Number Guessing Game (Starter)
====================================================

Goal
----
The computer picks a random integer from 1 to 100 (inclusive). You
guess. After each guess, the program tells you "too low", "too high",
or "correct!". When you guess correctly, it congratulates you with the
number of attempts you used. Then it asks if you want to play again.

You will combine almost every Week 3 idea:

- `while True:` with `break` for both the guessing loop and the replay
  loop.
- `if / elif / else` to decide too-low / too-high / correct.
- Guard clauses + `continue` to reject invalid input without counting it
  as an attempt.
- The accumulator pattern: `attempts += 1` on each valid guess.
- `random.randint(low, high)` from the standard library.

How to use this file
--------------------
1. Read the docstring (you are here).
2. Skim the function `play_round` and the `TODO` comments inside it.
3. Run the file once to make sure Python finds it:

       python starter.py

   (It will print a welcome message and exit; that is expected for the
   un-finished skeleton.)
4. Fill in the TODOs one by one. Run the script after each step to
   confirm it still works.
5. When everything works, save your version as `guessing_game.py` so
   `starter.py` stays clean for the next learner.

Task list (do these in order)
-----------------------------
[ ] 1. In `play_round`, generate the secret number with
       `random.randint(1, 100)`.
[ ] 2. Inside the inner `while True` loop, read a line of input with
       `input("Your guess: ")` and strip whitespace.
[ ] 3. Validate that the input is an integer. Hint:
       `raw.lstrip("-").isdigit()` returns True for things that look
       like integers (allow optional leading "-").
[ ] 4. Convert to int and check it is between 1 and 100. If not, print
       a polite message and `continue` (do NOT increment the counter).
[ ] 5. Increment `attempts` only AFTER you have a valid in-range
       number.
[ ] 6. Compare the guess to the secret. Print "Too low.", "Too high.",
       or the success message and `break` on a match.
[ ] 7. In the outer "play again?" loop, accept y / yes / n / no in any
       case. Anything else should be treated as "no" (or you can
       re-prompt; designer's choice — document whichever you pick).
[ ] 8. (Stretch) Pick one item from the README's stretch goals list and
       implement it.

Style reminders
---------------
- Indent with four spaces. No tabs.
- One blank line between logical chunks helps readability.
- Top-of-file docstring (the thing you are reading) is a good habit;
  keep it accurate as you change the code.
"""

import random

LOW = 1
HIGH = 100


def play_round() -> int:
    """Play one round of the game. Return the number of attempts used."""
    # TODO 1: Pick the secret number.
    # secret = random.randint(LOW, HIGH)
    secret = 0  # placeholder so the file still runs

    attempts = 0

    while True:
        raw = input("Your guess: ").strip()

        # TODO 2 & 3: Validate that `raw` looks like an integer.
        # If not, print a polite message and `continue`.

        # TODO 4: Convert and range-check (LOW <= guess <= HIGH).
        # If out of range, print a message and `continue`.

        # TODO 5: It is a valid guess — count it.
        # attempts += 1

        # TODO 6: Compare the guess to the secret. Print one of:
        #   "Too low."
        #   "Too high."
        #   f"Correct! You got it in {attempts} attempts."
        # Break out of the loop only when the guess is correct.

        # The next line keeps the skeleton from looping forever while
        # you build it. DELETE this line once your real logic is in
        # place.
        break

    return attempts


def main() -> None:
    print("Welcome to Guess The Number!")
    print(f"I am thinking of an integer between {LOW} and {HIGH}.")
    print()

    while True:
        attempts = play_round()
        # `attempts` is currently always 0 in the skeleton — that is
        # expected until you finish the TODOs.

        again = input("\nPlay again? (y/n): ").strip().lower()

        # TODO 7: Accept y / yes (case-insensitive) to replay.
        # Anything else exits.
        if again not in ("y", "yes"):
            print("Thanks for playing!")
            break

        print()
        print(f"I am thinking of an integer between {LOW} and {HIGH}.")


if __name__ == "__main__":
    main()
