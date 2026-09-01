"""Rock, paper, scissors against the computer, with a running score.

Challenge 2, Week 3, Code Crunch Convos. Plays rounds until the player
types ``quit``, tracks wins, losses and ties, and prints a final
scoreboard. Invalid input never costs a round.

Week 3 rules: the game itself uses no functions -- ``def`` is Week 4 --
and no ``try`` / ``except``, which is Week 6. The one helper below,
``ask()``, is scaffolding rather than part of the answer. It is what lets
this file run and print a whole session when nobody is at the keyboard.

``random.seed(SEED)`` is here for the same reason: it pins the computer's
moves so the printed session is the same every run. Delete that line to
play a real game.

Run it with::

    python rps.py
"""

import random
import sys

CHOICES: list[str] = ["rock", "paper", "scissors"]
SHORT_FORMS: dict[str, str] = {
    "r": "rock",
    "p": "paper",
    "s": "scissors",
    "q": "quit",
}
USER_WINS: set[tuple[str, str]] = {
    ("rock", "scissors"),
    ("scissors", "paper"),
    ("paper", "rock"),
}

SEED: int = 5  # delete the random.seed call below to play a real game

# The session this file plays when its input stream is already finished.
DEMO_ANSWERS: list[str] = ["rock", "r", "banana", "quit"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on once the demo script above has
            run out. The call site passes ``"quit"``, so the file can
            never loop forever unattended.

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

wins = 0
losses = 0
ties = 0
round_number = 1

while True:
    print(f"Round {round_number}")
    raw = ask("Choose rock/paper/scissors (or quit): ", "quit").strip().lower()

    if raw in SHORT_FORMS:
        choice = SHORT_FORMS[raw]
    else:
        choice = raw

    if choice == "quit":
        break

    if choice not in CHOICES:
        print(f"{raw!r} is not a valid choice. Try rock, paper, scissors, or quit.")
        print()
        continue

    computer = random.choice(CHOICES)
    print(f"You chose {choice}. Computer chose {computer}.")

    if choice == computer:
        ties += 1
        print("Tie.")
    elif (choice, computer) in USER_WINS:
        wins += 1
        print("You win!")
    else:
        losses += 1
        print("Computer wins.")

    print(f"Score - You: {wins}  Computer: {losses}  Ties: {ties}")
    print()
    round_number += 1

print("Final score:")
print(f"  You:      {wins}")
print(f"  Computer: {losses}")
print(f"  Ties:     {ties}")
print("Thanks for playing!")
