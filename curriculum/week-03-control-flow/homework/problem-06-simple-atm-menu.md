# Homework Problem 6 — Simple ATM Menu

> **Topic:** `while True` with `break` and `continue`, guard clauses instead of nested `if`s, and refusing an operation before it can corrupt anything
> **Lecture:** [01 — Conditionals: Deciding What Runs](../lecture-notes/01-conditionals.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour 30 minutes
> **Why this one:** it is the first program you write that keeps something valuable — a balance — alive across many turns of a loop, where a wrong branch does not print a wrong number, it *breaks the money*. The habit this problem is really teaching is refusing an operation **before** you touch the thing it would damage, and that habit is the difference between software that fails safely and software that fails expensively.

## The Brief

Build a tiny cash machine. It starts with a balance of `100.00` and it
shows the same menu every time round:

```text
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4:
```

What each option does:

- **Deposit** — ask for an amount and add it to the balance. Refuse zero
  and refuse negative amounts.
- **Withdraw** — ask for an amount and subtract it, but **refuse if that
  would push the balance below zero.**
- **Show balance** — print the balance with two decimal places.
- **Quit** — leave the loop and print `Goodbye.`.

Anything else at the menu prints `Please choose 1, 2, 3, or 4.` and shows
the menu again. It does not quit. It does not crash. A cash machine that
hangs up on you because you leaned on the keyboard is not a cash machine.

The requirement that carries the most weight is the one about the
withdrawal, and it has a subtle shape. "Refuse if the result would go
below zero" is a statement about a balance that does not exist yet. You
can answer it without ever computing that balance: if the amount is
bigger than the balance, refuse. Doing it that way means there is never a
moment where the balance is wrong, not even briefly.

## Starter

Save this as `homework-06-atm.py` and fill in the `TODO`s. It runs as
pasted: the menu appears, `4` quits, and every other key gets the
complaint:

```python
"""Homework 6 - A very small ATM simulator.

Starts with a balance of 100.00. Deposits must be positive; withdrawals
may not push the balance below zero; invalid menu choices reshow the
menu.
"""

DIGITS = "0123456789"

balance = 100.00

while True:
    print("1) Deposit")
    print("2) Withdraw")
    print("3) Show balance")
    print("4) Quit")
    choice = input("Choose 1-4: ").strip()

    if choice == "4":
        print("Goodbye.")
        break

    # TODO: option 3 - print the balance, then continue

    if choice not in ("1", "2"):
        print("Please choose 1, 2, 3, or 4.")
        continue

    # Both remaining options need an amount, so read and validate it once.
    action = "deposit" if choice == "1" else "withdraw"
    raw = input(f"Amount to {action}: ").strip()

    # TODO: reject anything float() cannot read, with
    #       "Please type an amount like 25 or 25.50."
    # TODO: reject amounts that are zero or negative, with
    #       "The amount must be greater than zero."

    amount = float(raw)

    if choice == "1":
        pass  # TODO: add to the balance and report it
    else:
        pass  # TODO: refuse if amount > balance, otherwise subtract and report
```

Read the shape of that loop before you fill anything in. It is a
**ladder**, not a nest. Each rung deals with one case and then leaves —
`break` for quit, `continue` for everything that has been handled or
refused. By the time control reaches the bottom of the ladder, `choice`
can only be `"1"` or `"2"`, and nothing down there has to check again.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/homework/problem-06-simple-atm-menu.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The balance starts at `100.00`.
2. The four menu lines print before every choice, exactly as shown.
3. The prompt is `Choose 1-4: `.
4. `3` prints `Balance: 100.00` — two decimals, and a thousands separator
   once the number gets big enough to need one.
5. `1` then `50` prints `Deposited 50.00. Balance: 150.00`.
6. `2` for more than the balance prints
   `Insufficient funds. Balance: <unchanged balance>` and leaves the
   balance alone.
7. `2` for an affordable amount prints
   `Withdrew <amount>. Balance: <new balance>`.
8. A menu choice that is not 1–4 prints `Please choose 1, 2, 3, or 4.`
   and shows the menu again.
9. An amount of zero or less prints
   `The amount must be greater than zero.` and returns to the menu.
10. An amount that is not a number prints
    `Please type an amount like 25 or 25.50.` and returns to the menu.
11. `4` prints `Goodbye.` and ends the program.

## Constraints

- **No functions.** `def` is Week 4. This is the problem where that
  starts to hurt, and it is supposed to.
- **No `try` / `except`.** Exceptions are Week 6, so
  `float("fifty")` has to be prevented rather than caught. Inspect the
  characters first.
- **Exactly one `break`.** The one under option 4. Every other bail-out
  is a `continue`. If you have two `break`s, one of them is a bug — see
  Common bugs to catch.
- **`choice` stays a string.** `input()` returns `str`, so compare
  against `"1"`, not `1`. No conversion means nothing to validate and
  nothing to crash.
- **Refuse the withdrawal before you subtract.** Not "subtract, check,
  put it back".
- **Format money with `f"{balance:,.2f}"`.** The `,` adds thousands
  separators and the `.2f` fixes two decimal places, so `2500.0` prints
  as `2,500.00`.
- **`.strip()` every line you read from a human.** A trailing space from
  a paste is otherwise enough to make `"1 "` fail to equal `"1"`.

## Expected output

The downloadable file below carries a scripted demonstration session —
`3 1 50 2 2000 2 125.50 9 1 -5 4` — that it types on your behalf when
nobody is at the keyboard. That walks every branch in the program: show
balance, a deposit, a refused withdrawal, an accepted withdrawal, an
invalid menu choice, a rejected negative amount, then quit.

```text
$ python problem-06-simple-atm-menu.py
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4: 3
Balance: 100.00
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4: 1
Amount to deposit: 50
Deposited 50.00. Balance: 150.00
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4: 2
Amount to withdraw: 2000
Insufficient funds. Balance: 150.00
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4: 2
Amount to withdraw: 125.50
Withdrew 125.50. Balance: 24.50
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4: 9
Please choose 1, 2, 3, or 4.
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4: 1
Amount to deposit: -5
The amount must be greater than zero.
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4: 4
Goodbye.
```

Read that as a checklist rather than as a transcript. The balance starts
at `100.00`. The deposit takes it to `150.00`. Withdrawing `2000` is
refused and the balance is **unchanged** — that is the line that matters
most. `125.50` goes through. `9` reshows the menu instead of quitting.
`-5` is rejected on its *value*, not on its form, which is why the
message is about being greater than zero and not about typing a number.
`4` prints `Goodbye.` and stops.

Run it in your own terminal and it asks you the questions instead, and
your session goes wherever you take it. **Stretch** has a real
interactive run to compare against.

## Steps

1. Activate your Week 3 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `homework-06-atm.py`. Run it, press `4`, and
   confirm it says `Goodbye.` and stops. Then press `9` and confirm it
   complains and comes back. You now have a working loop with nothing in
   it.
3. Add option 3. Two lines: print the balance, `continue`. Run it and
   press `3` a few times.
4. Add the deposit branch and nothing else. Deposit `50`, then press `3`
   and check the balance moved.
5. Add the withdrawal branch, refusal first. Try to withdraw `2000`
   before you try to withdraw anything sensible, because the refusal is
   the part that can be wrong in a way you would not notice.
6. Add the zero-or-negative check. Deposit `-5` and `0`.
7. Add the character validation for the amount, last. Type `fifty` and
   confirm you get a message rather than a traceback.
8. Walk the whole demonstration session by hand and compare your output
   against **Expected output** line by line.
9. Commit: `git add homework/homework-06-atm.py` then
   `git commit -m "Week 3 homework: simple ATM menu"`.

## The Solution

```python
"""A very small ATM simulator.

Week 3 homework, problem 6, Code Crunch Convos.

Starts with a balance of 100.00. Deposits must be positive, withdrawals
may not push the balance below zero, and an invalid menu choice reshows
the menu instead of ending the session.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. ``DEMO_SESSION`` is the list of
answers it types on your behalf when the keyboard is missing. In your own
copy, saved as ``homework-06-atm.py``, write ``input("Choose 1-4: ")``
instead and delete both.

Questions go to the error stream and the receipt goes to the normal
output stream, so ``python homework-06-atm.py > receipt.txt`` saves the
transactions and not the questions.
"""

import sys

DIGITS: str = "0123456789"
DEMO_SESSION: str = "3 1 50 2 2000 2 125.50 9 1 -5 4"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


demo_answers = DEMO_SESSION.split()
balance = 100.00

while True:
    print("1) Deposit")
    print("2) Withdraw")
    print("3) Show balance")
    print("4) Quit")
    choice = ask("Choose 1-4: ", demo_answers.pop(0) if demo_answers else "4").strip()

    if choice == "4":
        print("Goodbye.")
        break

    if choice == "3":
        print(f"Balance: {balance:,.2f}")
        continue

    if choice not in ("1", "2"):
        print("Please choose 1, 2, 3, or 4.")
        continue

    # Both remaining options need an amount, so read and validate it once.
    action = "deposit" if choice == "1" else "withdraw"
    raw = ask(f"Amount to {action}: ", demo_answers.pop(0) if demo_answers else "0").strip()

    # A valid amount: an optional sign, at least one digit, at most one dot.
    body = raw[1:] if raw[:1] in ("-", "+") else raw
    digit_count = 0
    dot_count = 0
    is_amount = True
    for ch in body:
        if ch in DIGITS:
            digit_count += 1
        elif ch == ".":
            dot_count += 1
        else:
            is_amount = False
    if digit_count == 0 or dot_count > 1:
        is_amount = False

    if not is_amount:
        print("Please type an amount like 25 or 25.50.")
        continue

    amount = float(raw)

    if amount <= 0:
        print("The amount must be greater than zero.")
        continue

    if choice == "1":
        balance += amount
        print(f"Deposited {amount:,.2f}. Balance: {balance:,.2f}")
    else:
        if amount > balance:
            print(f"Insufficient funds. Balance: {balance:,.2f}")
            continue
        balance -= amount
        print(f"Withdrew {amount:,.2f}. Balance: {balance:,.2f}")
```

**Why it works.**

**The loop body is a ladder of guard clauses, not a nest of `if`s.** Read
the top of the loop in order. Quit leaves. Show-balance handles itself
and `continue`s. Anything that is not `"1"` or `"2"` complains and
`continue`s. By the time control reaches the middle of the body,
`choice` is provably `"1"` or `"2"` and nothing below it has to re-check
that. This is [Lecture 1 §9](../lecture-notes/01-conditionals.md)'s
guard-clause pattern with `continue` playing the part the lecture gives
to `return`. The naive version wraps everything in
`if choice == "1": ... elif choice == "2": ... else: ...` and ends up
with the amount-reading code duplicated inside two branches.

**Reading the amount once, above the branch, is the design decision worth
arguing about.** Deposit and withdraw differ only in their last three
lines. Everything before that — the prompt, the character check, the
rejection of non-positive amounts — is identical. Hoisting the shared
part above the split means the validation exists in exactly one place, so
it cannot drift out of step between the two options. The cost is one
line, the `action` conditional expression that gets the prompt wording
right. If you wrote it the other way, with the validation duplicated,
your program is still correct — but count the lines you would have to
change to add a "5) Transfer" option and you will see the argument.

**`choice` stays a string, deliberately.** `input()` always returns
`str`. Comparing against `"1"` rather than `1` means there is no
conversion, so there is nothing to validate and nothing to crash.
`choice == 1` is `False` forever, and Python will not warn you.

**Validating a decimal without `try` / `except`.** `float("fifty")`
raises `ValueError`, so the characters get inspected before `float()` is
allowed to see them. Strip one optional leading `-` or `+` using
`raw[:1]`, not `raw[0]` — **slicing an empty string gives `''` while
indexing it raises `IndexError`**, and that is the difference between
pressing Enter at the prompt getting a polite message and pressing Enter
at the prompt getting a traceback. Then walk the rest: digits are
counted, dots are counted, anything else fails on the spot. Require at
least one digit, so `"."` and `"-"` are rejected. Require at most one
dot, so `"1.2.3"` is rejected. Everything that survives is something
`float()` can read.

**The sign is *accepted* by the validator and *rejected* by the value
check, and that split is not an accident.** If `-` failed the character
scan, typing `-5` would produce "Please type an amount like 25 or 25.50",
which is unhelpful and also untrue — `-5` is perfectly well-formed, it is
just not allowed. Letting it through to `if amount <= 0` produces "The
amount must be greater than zero", which tells the person what they
actually did wrong. **Validate for form, then check for meaning, and give
a different message for each.**

**`if amount > balance: continue` comes before `balance` is touched.**
The brief says refuse if the result would go below zero. Testing
`amount > balance` answers that question without computing a balance you
are about to throw away, and the `continue` means the refusal path cannot
possibly fall through into the subtraction. Compare with the version that
subtracts first and adds it back on failure: that one has a window where
the balance is wrong, and windows like that are where real financial bugs
live.

**`ask()` is the one piece the brief did not ask for**, and the one `def`
in the file. `input()` with nothing to read raises `EOFError`, and
`ask()` catches that and types the next answer from `DEMO_SESSION`, which
is what lets this download be run automatically and still reach
`Goodbye.`. It also sends the prompts to the **error** stream rather than
the output stream, so `python homework-06-atm.py > receipt.txt` gives you
a file of transactions with no questions in it. Your own
`homework-06-atm.py` deletes both and calls `input("Choose 1-4: ")`
directly.

## Download and run

Download [problem-06-simple-atm-menu-solution.py](./problem-06-simple-atm-menu-solution.py)
and run it:

```bash
python problem-06-simple-atm-menu-solution.py
```

Run from a terminal, it hands you the menu and waits. Run by a script, or
with its input redirected, it plays the scripted session in
`DEMO_SESSION` instead of hanging. Save your own copy as
`homework-06-atm.py` in your homework folder, and commit that one.

## Common bugs to catch

- **`if choice == 1:` — comparing a string to an integer.** `input()`
  returns `str`, so this is never true, and Python does not warn you,
  because comparing values of different types with `==` is perfectly
  legal:

  ```bash
  python -c "print('1' == 1)"
  ```

  ```text
  False
  ```

  The symptom is a menu where *every* option, including a correctly typed
  `1`, falls through to "Please choose 1, 2, 3, or 4." Either quote the
  literals or convert the input — but converting means validating, so
  quoting is less work and cannot fail.
- **`float(input(...))` with no validation.** Type a word at the amount
  prompt and the program dies mid-transaction:

  ```text
  ValueError: could not convert string to float: 'fifty'
  ```

  An ATM that crashes and forgets your balance because you fat-fingered a
  key is not an ATM.
- **`raw[0]` instead of `raw[:1]` when looking for the sign.** Press
  Enter with nothing typed and indexing an empty string raises:

  ```text
  IndexError: string index out of range
  ```

  Slicing is the forgiving operation — `''[:1]` is just `''` — which is
  why the answer slices.
- **Checking the withdrawal *after* subtracting.**

  ```python
  balance -= amount
  if balance < 0:
      print("Insufficient funds.")
      balance += amount     # undo it
  ```

  It works, right up until somebody adds a `break`, a `continue` or a
  second `if` between those two lines and the undo stops running.
  Refusing before you mutate has no such window. This is the ATM's
  version of the mini-project's "do not count the attempt until the guess
  is valid".
- **`break` where `continue` belongs.** Using `break` for an invalid menu
  choice quits the whole ATM instead of reshowing the menu. `continue`
  starts the next turn of the loop; `break` leaves it altogether
  ([Lecture 2 §6 and §7](../lecture-notes/02-loops.md)). Exactly one
  `break` in this program is correct — the one under option 4.
- **Forgetting `.strip()`.** A trailing space from a paste makes `"1 "`
  not equal to `"1"`, and the person sees "Please choose 1, 2, 3, or 4."
  after typing something that looks exactly like `1`. Strip every line
  you read from a human.
- **The `Show balance` branch with no `continue`.** It falls through into
  the "not 1 or 2" test, so pressing `3` prints the balance *and then*
  complains about the choice. Every rung of a ladder has to end in a
  `continue` or the ladder is a nest again.

## Under the hood

<details>
<summary>Under the hood — why a bank would never store this balance in a float</summary>

This program keeps the balance in a `float`, because that is what the
brief asks for and what you know in Week 3. It is also the wrong type for
money, and it is worth seeing exactly why.

A `float` is a **binary** fraction. Binary can write one half, one
quarter and one eighth exactly. It cannot write one tenth exactly, for
the same reason base ten cannot write one third exactly. So `0.1` is
stored as the nearest available binary value, which is slightly off, and
the error compounds:

```bash
python -c "print(0.1 + 0.2)"
```

```text
0.30000000000000004
```

Now do it with a balance. Take `33.33` out of `100.00` three times:

```bash
python -c "
b = 100.00
for _ in range(3):
    b -= 33.33
print(repr(b))
print(f'{b:,.2f}')
"
```

```text
0.010000000000005116
0.01
```

The true answer is `0.01`. The stored value is not `0.01`. The `:,.2f`
formatting **hides** the tail, which is the dangerous part — the display
is right while the value is wrong, so nothing looks broken until the day
you compare two balances with `==` and they differ in the last bit, or
you sum a million rows and the rounding error becomes visible in a real
column of a real ledger.

Two real fixes, and you will meet both:

**Store whole cents as an `int`.** `10000` instead of `100.00`. Integers
in Python are exact and unbounded, so nothing drifts, and you divide by
100 only at the moment you print. Most payment systems do this.

**Use `decimal.Decimal`.** It does arithmetic in base ten, the way a
ledger does, with a precision and a rounding mode you choose explicitly:

```bash
python -c "
from decimal import Decimal
d = Decimal('100.00')
for _ in range(3):
    d -= Decimal('33.33')
print(d)
"
```

```text
0.01
```

Exactly `0.01`, with the two decimal places preserved rather than
reconstructed by a format spec. Note the quotes: `Decimal('33.33')` is
exact, while `Decimal(33.33)` takes the float's error along with it.

None of this is this week's work. But
[Lecture 1 §10](../lecture-notes/01-conditionals.md)'s warning about
comparing floats with `==` and this drifting balance are the same warning
in different clothes, and it is better to know now that the shortcut is a
shortcut.

</details>

<details>
<summary>Under the hood — the ladder, the nest, and the state machine underneath both</summary>

Compare the two ways to write this loop body.

**The nest**, which is what most people write first:

```python
if choice == "1":
    raw = input("Amount to deposit: ")
    if is_valid(raw):
        amount = float(raw)
        if amount > 0:
            balance += amount
            print(...)
        else:
            print(...)
    else:
        print(...)
elif choice == "2":
    raw = input("Amount to withdraw: ")
    if is_valid(raw):
        ...
```

**The ladder**, which is the answer above: handle a case, then leave.

They compute the same thing. What differs is how much you have to hold in
your head at any line. In the nest, the deposit body sits four levels
deep, and to know whether a line runs you have to carry three conditions
in your head at once. In the ladder every line is at one level, and the
conditions above it are *facts*, not conditions — `choice` is `"1"` or
`"2"`, the amount is well-formed, the amount is positive. Each guard
turns a question into a settled fact and then gets out of the way.

There is a name for the count of paths through a piece of code:
**cyclomatic complexity**, roughly one plus the number of branches. It
does not fall when you flatten a nest — the same decisions are still
being made. What falls is the *nesting depth*, and depth is what human
readers actually pay for. That is why every style guide you will ever
read says the same thing about early returns, and why the pattern is
worth adopting before anyone makes you.

Underneath both versions there is a **state machine**, and naming it
makes the program easier to think about. The whole state is one number,
`balance`. The events are the menu choices. Each event is a transition
that either changes the state or refuses to:

| State | Event | Guard | New state |
|---|---|---|---|
| `balance` | deposit `a` | `a > 0` | `balance + a` |
| `balance` | deposit `a` | `a <= 0` | `balance` (refused) |
| `balance` | withdraw `a` | `0 < a <= balance` | `balance - a` |
| `balance` | withdraw `a` | `a > balance` | `balance` (refused) |
| `balance` | show | — | `balance` |
| `balance` | quit | — | (ended) |

Read the guard column. Every row either has a guard or does not need one,
and every refused row leaves the state exactly where it was. That is the
property the whole problem is built around, and it has a name too:
**atomicity**. A transaction either happens completely or does not happen
at all, and never leaves the balance in a half-changed condition. Writing
`if amount > balance: continue` above the subtraction rather than
`balance -= amount` followed by an undo is the smallest possible version
of the idea that databases build entire engines around.

</details>

## Acceptance checklist

- [ ] The balance starts at `100.00`.
- [ ] The four menu lines print before every choice.
- [ ] `3` prints the balance with two decimals.
- [ ] Depositing `50` reports `Deposited 50.00. Balance: 150.00`.
- [ ] Withdrawing more than the balance is refused and the balance is
      **unchanged**.
- [ ] An affordable withdrawal reports the amount and the new balance.
- [ ] `9` reshows the menu instead of quitting.
- [ ] `-5` and `0` are refused with the greater-than-zero message.
- [ ] `fifty` is refused with the amount-format message, not a
      traceback.
- [ ] Pressing Enter with nothing typed does not raise `IndexError`.
- [ ] `4` prints `Goodbye.` and ends.
- [ ] There is exactly one `break` in your loop.
- [ ] There is no `def` and no `try` in your own file.
- [ ] Committed with a message like `Week 3 homework: simple ATM menu`.

## Stretch

- **Run it for real and compare.** The Expected output block is the
  scripted run. Sit down at the terminal, type the same eleven answers,
  and you get the same transactions with your typing echoed between the
  prompts and the results:

  ```text
  1) Deposit
  2) Withdraw
  3) Show balance
  4) Quit
  Choose 1-4: 3
  Balance: 100.00
  1) Deposit
  2) Withdraw
  3) Show balance
  4) Quit
  Choose 1-4: 1
  Amount to deposit: 50
  Deposited 50.00. Balance: 150.00
  ```

  Then keep going off-script. Deposit `2500` and check the thousands
  separator appears: `Balance: 2,650.00`. Type `1.2.3` at an amount
  prompt. Press Enter with nothing typed. Type a single `-`. Every one of
  those should get a message and the menu back.
- **Add a transaction history.** A list before the loop, one `append` on
  each *successful* transaction, and a fifth menu option that walks it:

  ```python
  history = []
  ```

  ```python
      if choice == "5":
          if not history:
              print("No transactions yet.")
              continue
          for number, entry in enumerate(history, start=1):
              kind, amount = entry
              sign = "+" if kind == "deposit" else "-"
              print(f"{number:>3}. {kind:<10} {sign}{amount:>10,.2f}")
          continue
  ```

  ```python
          history.append(("deposit", amount))       # after balance += amount
  ```

  ```python
          history.append(("withdrawal", amount))    # after balance -= amount
  ```

  The menu block gains `print("5) Print history")`, the prompt becomes
  `Choose 1-5: `, the error message becomes
  `Please choose 1, 2, 3, 4, or 5.`, and the `if choice not in ("1", "2")`
  test does not change at all — options 3, 4 and 5 are all handled above
  it.

  Four things in that block are worth more than the feature. **Append
  *after* the balance changes**, so a refused withdrawal `continue`s out
  before it can be recorded; the history then contains exactly the
  transactions that happened, which is the only property a ledger really
  has to have. **`if not history:`** reads as "if there is no history",
  because an empty list is falsy
  ([Lecture 1 §4](../lecture-notes/01-conditionals.md)) — `len(history) == 0`
  is identical and wordier. **The format spec is doing real work**:
  `{number:>3}` right-aligns the row number in three columns,
  `{kind:<10}` left-aligns the word in ten so the amounts all start at
  the same place, and `{amount:>10,.2f}` right-aligns the money in ten
  columns with separators and two decimals. Right-align numbers,
  left-align words, and the digits line up by place value. And
  **`enumerate(history, start=1)`** numbers from 1 rather than 0, because
  this is a receipt, not an index
  ([Lecture 2 §4](../lecture-notes/02-loops.md)). Deposit `2500`,
  withdraw `99.99`, then print the history and you get:

  ```text
    1. deposit    +  2,500.00
    2. withdrawal -     99.99
  ```

  `("deposit", 2500.0)` is a tuple pairing a kind with an amount, and
  `kind, amount = entry` unpacks it — the same unpacking as
  `a, b = 0, 1` in problem 5. In Week 5 you will reach for a dictionary
  here, and much later a dataclass. The tuple is the honest Week 3
  answer.
- **Store cents as integers instead.** Change `balance = 100.00` to
  `balance_cents = 10000`, read amounts as whole cents, and divide by 100
  only when you print. The first **Under the hood** block explains why a
  real system does it this way, and doing the conversion yourself is the
  fastest way to understand what a `float` was costing you.
- **Add a daily withdrawal limit.** Keep a running total of what has been
  taken out and refuse once it passes, say, `500.00`. Notice that this is
  a *second* guard on the same operation, and that it slots in beside
  `if amount > balance:` without disturbing anything — which is the
  ladder paying for itself.
- **Count the copies of the amount-validation block** across your six
  homework answers this week. That count is the argument for functions,
  and it is the argument Week 4 opens with.

Next: back to [the Week 3 homework index](./README.md), then
[the mini-project](../mini-project/README.md) and
[the quiz](../quiz.md).
