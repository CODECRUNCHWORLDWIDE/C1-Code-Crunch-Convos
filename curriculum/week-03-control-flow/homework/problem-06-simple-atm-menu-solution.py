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
