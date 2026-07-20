# Challenge 02 — Rock, Paper, Scissors

Build a command-line rock-paper-scissors game where the user plays
against the computer. The game keeps a running score and continues until
the user types `quit`.

## Requirements

Save your solution as `challenge-02-rps.py` in this folder.

1. On each round, the program asks the user to choose `rock`, `paper`,
   `scissors`, or `quit`. Accept any reasonable casing (`Rock`, `ROCK`,
   `rock` all work) and accept the short forms `r`, `p`, `s`, `q`.
2. The computer's choice is **random** each round. Import the `random`
   module and call `random.choice([...])`.
3. The program prints both choices and the round result (`You win!`,
   `Computer wins.`, or `Tie.`).
4. The program tracks **wins**, **losses**, and **ties** for the current
   session and prints the running score after every round.
5. Typing `quit` exits the loop and prints a final scoreboard:

   ```text
   Final score:
     You:      4
     Computer: 3
     Ties:     2
   Thanks for playing!
   ```

6. Invalid input (`"banana"`, an empty string, etc.) prints a polite
   error and **does not** consume a round — the score stays the same
   and the program asks again.

## The rules (in case you need a refresher)

- Rock crushes scissors.
- Scissors cuts paper.
- Paper covers rock.
- Same choice = tie.

## Sample session

```text
Round 1
Choose rock/paper/scissors (or quit): rock
You chose rock. Computer chose scissors.
You win!
Score - You: 1  Computer: 0  Ties: 0

Round 2
Choose rock/paper/scissors (or quit): r
You chose rock. Computer chose paper.
Computer wins.
Score - You: 1  Computer: 1  Ties: 0

Round 3
Choose rock/paper/scissors (or quit): banana
'banana' is not a valid choice. Try rock, paper, scissors, or quit.

Round 3
Choose rock/paper/scissors (or quit): quit
Final score:
  You:      1
  Computer: 1
  Ties:     0
Thanks for playing!
```

## Hints

- The main loop is a `while True:` that `break`s on `quit`.
- Normalize input with `.strip().lower()` and a small lookup dict to
  expand short forms:

  ```python
  short_forms = {"r": "rock", "p": "paper", "s": "scissors", "q": "quit"}
  ```

- The "who wins" logic is a 3x3 table. One clean way is to enumerate the
  three losing-pairings:

  ```python
  user_wins = {
      ("rock", "scissors"),
      ("scissors", "paper"),
      ("paper", "rock"),
  }
  ```

  Then `if (user, computer) in user_wins:` settles it in one line.

- Use the accumulator pattern (Lecture 3) for the three counters.

## Acceptance criteria

- The game runs at least one round without crashing.
- Random output: two consecutive runs do not always pick the same
  computer move.
- Invalid input does not change any counter.
- `quit` (and `q`) exits cleanly and prints the final scoreboard.
- Scoreboard totals always equal the number of valid rounds played.

## Stretch goals

- Add a "best of N" mode: play until either side wins `N` rounds.
- Add `lizard` and `spock` for the
  [Sheldon Cooper variant](https://en.wikipedia.org/wiki/Rock_paper_scissors#Additional_weapons).
- Save the scoreboard to a JSON file at the end of each session (file
  I/O is Week 6 — this is a preview challenge if you finish early).
