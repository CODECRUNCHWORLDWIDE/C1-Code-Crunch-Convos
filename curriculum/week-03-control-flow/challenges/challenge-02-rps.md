# Challenge 2 — Rock, Paper, Scissors

> **Topic:** a `while True` game loop, three counters that have to stay honest, and putting the rules of a game in a data structure instead of in `if` statements
> **Lecture:** [02 — Loops](../lecture-notes/02-loops.md)
> **Difficulty:** the game is easy; making a bad answer cost the player nothing is the real work
> **Target time:** 60–90 minutes
> **Why this one:** it is the first program that keeps a running total across rounds. Deciding *where* a counter is allowed to change is a skill you will use in every program that has a score, a total, a cart, or a balance.

## The Brief

Write a rock-paper-scissors game you play against the computer at the
command line. It keeps score across the whole session and keeps going
until you type `quit`.

The rules, in case you need them:

- Rock crushes scissors.
- Scissors cuts paper.
- Paper covers rock.
- The same choice on both sides is a tie.

Each round the program asks what you want to play, picks its own move at
random, says who won, and prints the running score. When you quit, it
prints a final scoreboard.

The interesting requirement is the last one. If you type `banana`, the
program has to say so politely and then ask again — and that round must
not count. Not as a win, not as a loss, not as a tie, and not as a round
number. Getting that right is not about being careful. It is about
putting the counters somewhere a bad answer physically cannot reach.

> *As a* learner who has just met `while True`, `break` and `continue`,
> *I want* a loop that keeps a score and refuses to be confused by
> nonsense,
> *so that* I learn where state is allowed to change.

## Starter

Save this as `challenge-02-rps.py` and run it before you change anything.
It runs exactly as pasted: it plays a round, prints a score of all
zeroes, and quits. The four `TODO`s are the game.

```python
"""TODO: one line saying what this file does."""

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

DEMO_ANSWERS: list[str] = ["rock", "quit"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        print(f"{prompt}{answer}")
        return answer


random.seed(5)  # delete this line to play a real game

wins = 0
losses = 0
ties = 0
round_number = 1

while True:
    print(f"Round {round_number}")
    raw = ask("Choose rock/paper/scissors (or quit): ", "quit").strip().lower()
    choice = raw
    # TODO 1: expand a short form (r/p/s/q) into the full word.

    if choice == "quit":
        break

    # TODO 2: if choice is not in CHOICES, print the complaint, print a
    #         blank line, and `continue` so the bad round costs nothing.

    computer = random.choice(CHOICES)
    print(f"You chose {choice}. Computer chose {computer}.")

    # TODO 3: tie, win or loss - print the result and add one to the
    #         matching counter.

    print(f"Score - You: {wins}  Computer: {losses}  Ties: {ties}")
    print()
    round_number += 1

# TODO 4: print the final scoreboard, above the goodbye.
print("Thanks for playing!")
```

Run it and you get a game that plays but does not know who won:

```text
$ python challenge-02-rps.py
Round 1
Choose rock/paper/scissors (or quit): rock
You chose rock. Computer chose scissors.
Score - You: 0  Computer: 0  Ties: 0

Round 2
Choose rock/paper/scissors (or quit): quit
Thanks for playing!
```

**About the two lines you did not expect.**

`ask()` is given to you and you never have to write one. It asks a
question and reads a line, and if there is nobody there to answer — a
checker is running the file, or you piped input in and it ran out — it
uses the next of the `DEMO_ANSWERS` instead and prints it, so the file
always produces a whole session. It reaches ahead of Week 3 on purpose:
`def` is Week 4 and `try` / `except` is Week 6. That is fine, because it
is scaffolding rather than the answer. Everything below it stays inside
this week's toolbox.

`random.seed(5)` makes the computer's moves come out the same every run,
which is what lets this page promise you an exact session. It also makes
the game unplayable in the long run, because the computer's moves become
memorisable. Delete that one line when you want a real game. The
*Under the hood* block explains what a seed actually is, and there is an
unseeded version under *Stretch*.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/challenges/challenge-02-rps.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Each round, ask `Choose rock/paper/scissors (or quit): `. Accept any
   capitalisation and stray spaces, so `Rock`, ` ROCK ` and `rock` all
   work, and accept the short forms `r`, `p`, `s` and `q`.
2. The computer's move is chosen at random from the three options, once
   per round.
3. Print both moves as `You chose X. Computer chose Y.` and then the
   result on its own line: `You win!`, `Computer wins.`, or `Tie.`.
4. Keep a running count of wins, losses and ties for the session, and
   print `Score - You: W  Computer: L  Ties: T` after every valid round.
   That is two spaces before `Computer:` and before `Ties:`.
5. `quit` — or `q` — ends the loop and prints the final scoreboard:

   ```text
   Final score:
     You:      4
     Computer: 3
     Ties:     2
   Thanks for playing!
   ```

6. Anything else — `banana`, an empty line — prints
   `'banana' is not a valid choice. Try rock, paper, scissors, or quit.`
   with the answer quoted, and **does not consume a round**. No counter
   changes and the round number does not go up.

## Constraints

- **No `def`.** Functions are Week 4. The whole game is one `while True`
  loop at the top level of the file. The only exception is the supplied
  `ask()`.
- **No `try` / `except`.** Exceptions are Week 6. Nothing here needs
  them: every answer is checked with `in` against a list or a dictionary.
- **Call `random.choice` exactly once per round, and store the result.**
  Call it twice and the computer plays one move in the message and a
  different one in the comparison. *Common bugs to catch* has the
  symptom.
- **Put the win table in a data structure, not in nine branches.** There
  are nine possible pairs of moves. Three of them are ties and one
  comparison catches all three. Three of them are wins, and those three
  go in `USER_WINS`. The other three need no code at all — they are
  whatever is left.
- **The counters live below the guard.** The `continue` for an invalid
  answer has to happen *before* anything that changes a counter. That is
  what makes requirement 6 true by construction rather than by
  remembering to be careful.
- **Standard library only.** `random` and `sys`, both of which come with
  Python.

## Expected output

Run the file with nothing attached to its input and it answers its own
questions from the demo script. Because the seed is fixed, this is the
same session every time. Real stdout on CPython 3.13.2:

```text
$ python challenge-02-rps.py
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

Look at what `banana` did, because it is the whole point of requirement
6. It printed the complaint. It did not print a `You chose` line, so the
computer never even moved. The score line did not appear. And
`Round 3` is printed **twice** — once for the round that was thrown away
and once for the round that replaced it. Nothing about the game state
moved forward.

Also worth noticing: round 2 was typed as `r` and the program played
`rock`. That is requirement 1.

Run it in your own terminal and it asks you instead. Feeding the answers
in from the shell shows the same thing with the questions stripped out,
because they go to the error stream — see *The Solution*:

```text
$ printf 'ROCK \np\nq\n' | python challenge-02-rps.py
Round 1
You chose rock. Computer chose scissors.
You win!
Score - You: 1  Computer: 0  Ties: 0

Round 2
You chose paper. Computer chose paper.
Tie.
Score - You: 1  Computer: 0  Ties: 1

Round 3
Final score:
  You:      1
  Computer: 0
  Ties:     1
Thanks for playing!
```

`ROCK ` with a capital and a trailing space became `rock`, `p` became
`paper`, and `q` quit. Three different spellings of requirement 1 in one
run.

## Steps

1. Save the Starter as `challenge-02-rps.py` and run it. You should see
   the two-round session above. Nothing is broken; the scoring is
   missing on purpose.

2. Do **TODO 3** first, because it is the game. Three branches:

   ```python
   if choice == computer:
       ties += 1
       print("Tie.")
   elif (choice, computer) in USER_WINS:
       wins += 1
       print("You win!")
   else:
       losses += 1
       print("Computer wins.")
   ```

   Run it a few times with the seed deleted and check that the results
   match the rules. Rock against scissors should be a win.

3. Do **TODO 4**. Four `print` lines above the goodbye, copied from
   requirement 5. Mind the padding: `You:` gets six spaces after it,
   `Computer:` gets one, `Ties:` gets five, so the three numbers line up.

4. Do **TODO 1**. One `if` / `else`:

   ```python
   if raw in SHORT_FORMS:
       choice = SHORT_FORMS[raw]
   else:
       choice = raw
   ```

   `raw in SHORT_FORMS` asks whether `raw` is one of the dictionary's
   *keys*. Test with `r`, then with `q` — `q` should quit.

5. Do **TODO 2** last:

   ```python
   if choice not in CHOICES:
       print(f"{raw!r} is not a valid choice. Try rock, paper, scissors, or quit.")
       print()
       continue
   ```

   Now type `banana` and watch `Round 3` appear twice. If it appears once
   and then `Round 4`, your `continue` is in the wrong place or
   `round_number += 1` is above it.

6. Play a full session by hand: a win, a loss, a tie, a `banana`, and a
   `quit`. Check that the three final numbers add up to the number of
   real rounds you played.

7. Commit it:

   ```bash
   git add challenge-02-rps.py
   git commit -m "Add Challenge 2: rock, paper, scissors"
   ```

## The Solution

```python
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
```

**Tidy the answer up once, then never think about spelling again.**
`.strip().lower()` deals with `Rock`, ` ROCK ` and `rock` in one
expression. The `SHORT_FORMS` lookup then turns `r`, `p`, `s` and `q`
into whole words. After those two steps, `choice` is either one of four
known words or it is nonsense, and the rest of the loop only has to tell
those two cases apart. Requirement 1 asks for casing tolerance *and*
short forms; doing both up front is why the game logic underneath stays
short enough to read in one go.

**The order of the three checks is the design.** Quit is tested first,
because `q` has just become `quit` and quitting must not be mistaken for
a bad answer. Validity is tested second, and its `continue` fires
*before* `random.choice` is ever called. So there is no path from an
invalid answer to a counter, or even to the computer making a move. You
can see that by looking at the shape of the code, which is a much
stronger guarantee than testing it a few times and hoping.

That is a **guard clause**: deal with the bad case and leave immediately,
so the good case below it needs no extra indentation. Inside a loop,
`continue` is what does the leaving.

**`round_number += 1` sits at the bottom, next to the score.** That
placement is why `Round 3` prints twice after `banana`. The round number
counts rounds that were actually played, so it only moves where a played
round finishes. You get the last acceptance criterion for free from the
same placement: `wins + losses + ties` always equals `round_number - 1`,
because both sides are incremented in the same block.

**The win table is three pairs, not nine branches.** There are nine ways
the two moves can pair up. Here is the whole table, generated from
`USER_WINS`, from your side:

```text
rock     tie   lose  win
paper    win   tie   lose
scissors lose  win   tie
```

The columns are the computer's rock, paper and scissors. The diagonal is
the three ties, and `choice == computer` catches all three in one
comparison. The three `win` cells are the three pairs in `USER_WINS`. And
the three `lose` cells need no code whatsoever — they are the `else`.
Nine cases, three lines.

`in` on a set is a hash lookup, so adding more moves does not slow it
down. The *Stretch* section adds lizard and spock, which takes the table
from three pairs to ten, and the game loop does not change by one
character.

**`{raw!r}` prints the answer with quotes round it.** `!r` asks for the
`repr()` of the value, so `banana` prints as `'banana'`. The quotes earn
their place on the empty answer: `'' is not a valid choice.` tells you
what happened, where `is not a valid choice.` just looks like a bug in
the program.

**`ask()` puts the questions on the other stream.** A program has two
ways to send text out: the normal output stream, `stdout`, for its
answers, and the error stream, `stderr`, for everything else. `ask()`
prints the question to `stderr` with `end=""` so the cursor stays put,
and `flush=True` so the question appears before the program starts
waiting. Then it calls `input()` with **no argument**, because
`input("prompt")` would print that prompt to stdout and mix the questions
in with the game. That separation is why the piped session in *Expected
output* is nothing but the game.

## Download and run

Download [challenge-02-rps-solution.py](./challenge-02-rps-solution.py)
and run it:

```bash
python challenge-02-rps-solution.py
```

In your own terminal it asks you what to play. Run by a script, or with
its input closed, it plays the demo session above.

You can also feed it moves from the shell, one per line:

```bash
printf 'ROCK \np\nq\n' | python challenge-02-rps-solution.py
```

Because the questions go to the error stream, `>` captures the game on
its own:

```bash
python challenge-02-rps-solution.py > game.txt
```

**Delete the `random.seed(SEED)` line before you actually play.** With it
in place the computer opens with scissors, then paper, then the same
sequence every single time you start the program. That is what makes the
printed session above reproducible, and it is also completely beatable.

In your own project, save the same code as `challenge-02-rps.py`.

## Common bugs to catch

**`if choice == "quit" or "q":`** — the most common logic bug in Python,
and nothing raises. `or` hands back the first operand that counts as
true, and a non-empty string always counts as true:

```text
>>> raw = "rock"
>>> bool(raw == "q" or "quit")
True
```

So the condition is true no matter what was typed, and the game quits on
round one with a scoreboard of zeroes. Write `if choice in ("quit", "q"):`
— one membership test, no trap. (In the answer above, `q` has already
been expanded to `quit`, so a plain `==` is enough.)

**You called `random.choice(CHOICES)` twice in one round.** Once in the
message and once in the comparison. The player is told the computer chose
`rock` and then scored against `scissors`. The scoreboard is genuinely
wrong and it looks like the *rules* are broken rather than the code. Call
it once, store it in `computer`, and use that name everywhere.

**`random.choice("rock")`.** A string is a sequence of characters, so
this picks a letter:

```text
>>> import random
>>> random.seed(0)
>>> random.choice("rock")
'k'
```

No error, just a computer playing `k` and losing to everything.
`random.choice` needs a sequence of the things you want to choose
between, so pass the list.

**You counted the round before checking the answer.** Move
`round_number += 1` to the top of the loop, or add a counter inside the
invalid branch, and requirement 6 and the last acceptance criterion both
break at once. The symptom is a final scoreboard whose three numbers do
not add up to the rounds you played.

**The computer plays the same three moves every run.** You left
`random.seed(SEED)` in. That is deliberate in the downloadable file and
wrong in a game you want to play. Delete the line.

**The score columns do not line up.** Requirement 4 wants two spaces
before `Computer:` and before `Ties:`, and the final scoreboard pads the
three labels to the same width. Copy those `print` lines exactly from
requirement 5.

## Under the hood

<details>
<summary>Under the hood — a nine-cell table, and why it is not nine ifs</summary>

Two players, three moves each, so there are `3 * 3` — nine — ways a round
can come out. The obvious first program writes one branch per cell:

```python
if choice == "rock" and computer == "rock":
    ...
elif choice == "rock" and computer == "paper":
    ...
```

Nine branches, eighteen comparisons, and every one of them is a chance to
type the wrong word. It works. It is also unmaintainable: adding lizard
and spock takes it from nine branches to twenty-five.

Lay the nine cells out as a grid instead, with your move down the side
and the computer's along the top:

```text
         rock  paper scissors
rock     tie   lose  win
paper    win   tie   lose
scissors lose  win   tie
```

Now the structure is visible. There are three regions, not nine cases:

- **The diagonal** is every tie, and the thing every cell on it has in
  common is `choice == computer`. One comparison.
- **Three cells** are wins. They are the three pairs in `USER_WINS`.
- **Everything left over** is a loss. It needs no test at all.

That is the reduction from nine to three, and it came from drawing the
table rather than from being clever with `if`.

**Why a set of tuples.** A tuple `("rock", "scissors")` is one pair, kept
in order — your move first, the computer's second — and order is exactly
what decides the round. `in` on a `set` is a hash lookup, so it takes the
same time whether the set holds three pairs or ten thousand, unlike
scanning a list.

**The counting check.** With five moves, each one beats exactly two
others, so a correct table has `5 * 2` — ten — pairs, and no pair may
appear in both directions. With three moves it is `3 * 1`, which is the
three pairs above. That arithmetic is how you sanity-check a table you
typed by hand, and it is much faster than playing until something looks
wrong.

**The general shape.** This is a *lookup table*: the rules of the game
live in data, and the code that reads the data does not change when the
rules do. You will meet the idea again as a dictionary in Week 5, as a
configuration file in Week 8, and as a database row later still. Every
time, the payoff is the same one you can see in *Stretch*: adding five
moves to this game changes two lines and touches no logic at all.

</details>

<details>
<summary>Under the hood — where random numbers come from, and what a seed does</summary>

`random.choice` does not consult anything genuinely unpredictable. It
uses a **pseudo-random number generator**: a piece of arithmetic that
starts from one number and grinds out a long stream of numbers that
*look* patternless. The starting number is the **seed**.

Same seed, same stream, every time, on every machine:

```text
>>> import random
>>> random.seed(5)
>>> [random.choice(["rock", "paper", "scissors"]) for _ in range(5)]
['scissors', 'paper', 'scissors', 'paper', 'scissors']
>>> random.seed(5)
>>> [random.choice(["rock", "paper", "scissors"]) for _ in range(5)]
['scissors', 'paper', 'scissors', 'paper', 'scissors']
>>> random.seed(6)
>>> [random.choice(["rock", "paper", "scissors"]) for _ in range(5)]
['scissors', 'rock', 'paper', 'paper', 'rock']
```

Nothing was remembered between those calls. The second run produced the
same five moves because the arithmetic is the same arithmetic and it
started from the same place. Change the seed by one and the stream is
completely different.

**What happens when you do not seed it.** Python seeds the generator for
you the first time you use it, from the operating system's pool of real
unpredictability — timings of hardware events, mostly. That is why an
unseeded program behaves differently on every run. The same three moves
played twice, against the answer with its `random.seed` line deleted:

```text
$ printf 'rock\nrock\nrock\nquit\n' | python rps.py | grep 'Computer chose'
You chose rock. Computer chose paper.
You chose rock. Computer chose scissors.
You chose rock. Computer chose rock.

$ printf 'rock\nrock\nrock\nquit\n' | python rps.py | grep 'Computer chose'
You chose rock. Computer chose scissors.
You chose rock. Computer chose paper.
You chose rock. Computer chose rock.
```

Two runs can still match by chance — three rolls of a three-sided die
land the same way about eleven times in a hundred — so if your own two
runs agree, run it again before you suspect the code.

**Why seed it on purpose.** Because "it worked when I ran it" is not a
test. Pinning the seed turns a random program into a repeatable one, so a
page can promise you an exact session and a checker can compare against
it. Every serious test suite that touches randomness does this.

**The rule to remember.** Pseudo-random is fine for a game, a shuffle,
a sample, or a simulation. It is **not** fine for anything that has to
stay secret. If you can guess the seed you can reproduce the entire
stream, and Python's default generator was designed for speed and
statistical quality, not secrecy. When you need randomness nobody can
predict — passwords, tokens, keys — the standard library has a separate
module, `secrets`, that draws straight from the operating system. Use
that one, and never `random`, for anything with a lock on it.

</details>

## Acceptance checklist

- [ ] The game plays at least one round without crashing.
- [ ] `Rock`, ` ROCK `, `rock` and `r` all play rock.
- [ ] `q` and `quit` both end the game.
- [ ] The computer's move is picked once per round and the message and
      the result agree about what it was.
- [ ] With `random.seed(SEED)` deleted, two runs do not always produce
      the same computer moves.
- [ ] `banana` prints `'banana' is not a valid choice. Try rock, paper,
      scissors, or quit.` with the quotes.
- [ ] After `banana`, no counter changed and the round number did not go
      up — the same `Round N` line prints twice.
- [ ] Pressing Enter with nothing typed is treated the same way as
      `banana`.
- [ ] The running score line appears after every valid round, with two
      spaces before `Computer:` and before `Ties:`.
- [ ] Quitting prints the four-line final scoreboard with the numbers
      lined up, then `Thanks for playing!`.
- [ ] `wins + losses + ties` equals the number of rounds actually played.
- [ ] No `def` and no `try` / `except` outside the supplied `ask()`.
- [ ] Four-space indentation, `snake_case` names, a docstring at the top,
      no `TODO` comments left.
- [ ] Committed with a message such as
      `Add Challenge 2: rock, paper, scissors`.

## Stretch

**The plain `input()` version.** The downloadable answer uses `ask()` so
it runs with nobody at the keyboard, and a seed so its session is
reproducible. Strip both out and the program is shorter, stays entirely
inside Week 3 — no `def`, no `try` — and is a real game again. Keep it as
a second file, `rps_ask.py`:

```python
"""Challenge 02 — Rock, paper, scissors against the computer.

Tracks wins, losses and ties for the session and prints a final
scoreboard when the player quits. Invalid input never costs a round.
"""

import random

CHOICES = ["rock", "paper", "scissors"]
SHORT_FORMS = {"r": "rock", "p": "paper", "s": "scissors", "q": "quit"}
USER_WINS = {
    ("rock", "scissors"),
    ("scissors", "paper"),
    ("paper", "rock"),
}

wins = 0
losses = 0
ties = 0
round_number = 1

while True:
    print(f"Round {round_number}")
    raw = input("Choose rock/paper/scissors (or quit): ").strip().lower()

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
```

One real session, typed at a terminal, playing rock three times:

```text
$ python rps_ask.py
Round 1
Choose rock/paper/scissors (or quit): rock
You chose rock. Computer chose scissors.
You win!
Score - You: 1  Computer: 0  Ties: 0

Round 2
Choose rock/paper/scissors (or quit): rock
You chose rock. Computer chose rock.
Tie.
Score - You: 1  Computer: 0  Ties: 1

Round 3
Choose rock/paper/scissors (or quit): rock
You chose rock. Computer chose paper.
Computer wins.
Score - You: 1  Computer: 1  Ties: 1

Round 4
Choose rock/paper/scissors (or quit): quit
Final score:
  You:      1
  Computer: 1
  Ties:     1
Thanks for playing!
```

Your session will not match, and that is the point — this is the version
where the acceptance criterion about randomness can actually be checked.
It also stops dead the moment nothing is typing at it, which is the whole
reason the downloadable file is written the other way.

**Best of N.** Play until one side reaches a target. The neat move is to
put the target in the loop header rather than adding another `break` in
the middle:

```python
target = 3
while wins < target and losses < target:
    ...
if wins > losses:
    print(f"You take the match {wins}-{losses}.")
else:
    print(f"The computer takes the match {losses}-{wins}.")
```

Ties not counting towards the match falls out for free: neither counter
moved, so the condition is still true and the loop goes round again. Keep
the `quit` `break` inside for a player who wants out early. That
combination — a natural finish *and* an escape hatch — is exactly when
`while True` with a `break` is still the right shape.

**Lizard and spock.** Two lines change, and the game loop does not change
at all:

```python
CHOICES = ["rock", "paper", "scissors", "lizard", "spock"]
SHORT_FORMS = {"r": "rock", "p": "paper", "s": "scissors",
               "l": "lizard", "k": "spock", "q": "quit"}
USER_WINS = {
    ("rock", "scissors"), ("rock", "lizard"),
    ("paper", "rock"), ("paper", "spock"),
    ("scissors", "paper"), ("scissors", "lizard"),
    ("lizard", "paper"), ("lizard", "spock"),
    ("spock", "rock"), ("spock", "scissors"),
}
```

Note `k` for spock, because `s` is already scissors — a real design
decision that the five-move version forces on you. Check your table
before you trust it: each move beats exactly two others, so there must be
exactly ten pairs, and no pair may appear in both directions.

That the loop needs no edit at all is the payoff for having put the rules
in a data structure. It is the same payoff the mini-project's difficulty
levels get from a dictionary.

**Saving the scoreboard to a JSON file** needs `open()` and the `json`
module, which are Week 6 and Week 8. Leave it until then.
