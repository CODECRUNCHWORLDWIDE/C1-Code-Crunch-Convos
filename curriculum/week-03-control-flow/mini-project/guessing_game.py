"""Guess The Number: the computer picks 1-100, you close in on it.

Mini-project, Week 3, Code Crunch Convos. Counts only the guesses that
were whole numbers inside the range, so typos and out-of-range numbers
are free, then offers a rematch with a fresh secret.

Week 3 rules: the game itself uses no functions -- ``def`` is Week 4 --
and no ``try`` / ``except``, which is Week 6, so every guess is checked
character by character before ``int()`` ever sees it. The one helper
below, ``ask()``, is scaffolding rather than part of the answer. It is
what lets this file run and print a whole session when nobody is at the
keyboard.

``random.seed(SEED)`` is here for the same reason: it pins the secret
numbers so the printed session is the same every run. Delete that line
to play a real game.

Run it with::

    python guessing_game.py
"""

# === setup ===
import random
import sys

DIGITS: str = "0123456789"
LOW: int = 1
HIGH: int = 100

SEED: int = 77  # delete the random.seed call below to play a real game

# The session this file plays when its input stream is already finished.
DEMO_ANSWERS: list[str] = ["50", "25", "37", "30", "33", "y", "42", "n"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on once the demo script above has
            run out. Every call site passes something that ends what it
            is asking about, so the file can never loop forever
            unattended.

    Returns:
        The line that was typed, or the next demo answer. A demo answer
        is echoed after the prompt on the normal output stream, so the
        printed session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        print(f"{prompt}{answer}")
        return answer


random.seed(SEED)

print("Welcome to Guess The Number!")

# === outer "play again" loop ===
while True:
    secret = random.randint(LOW, HIGH)
    attempts = 0

    print(f"I am thinking of an integer between {LOW} and {HIGH}.")
    print()

    # === guessing loop ===
    while True:
        raw = ask("Your guess: ", str(secret)).strip()

        # Guard 1: it has to be a whole number.
        body = raw[1:] if raw[:1] in ("-", "+") else raw
        is_whole_number = body != ""
        for ch in body:
            if ch not in DIGITS:
                is_whole_number = False
                break
        if not is_whole_number:
            print("That is not a whole number. Try again.")
            continue

        guess = int(raw)

        # Guard 2: it has to be in range.
        if not LOW <= guess <= HIGH:
            print(f"Please guess a number between {LOW} and {HIGH}.")
            continue

        # Past both guards, so this one counts.
        attempts += 1

        if guess < secret:
            print("Too low.")
        elif guess > secret:
            print("Too high.")
        else:
            word = "attempt" if attempts == 1 else "attempts"
            print(f"Correct! You got it in {attempts} {word}.")
            break

    print()

    # === replay prompt ===
    while True:
        again = ask("Play again? (y/n): ", "n").strip().lower()
        if again in ("y", "yes", "n", "no"):
            break
        print("Please answer y or n.")

    if again in ("n", "no"):
        print("Thanks for playing!")
        break

    print()
