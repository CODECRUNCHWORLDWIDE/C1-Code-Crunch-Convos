"""Exercise 05 — A BankAccount with deposit, withdraw, and dual reprs.

Goal
----
Build a `BankAccount` class with:

* ``__init__(self, holder: str, balance: float = 0.0)`` — store both.
* ``deposit(amount: float) -> None`` — increase the balance. Raise
  ``ValueError`` for non-positive amounts.
* ``withdraw(amount: float) -> None`` — decrease the balance. Raise
  ``ValueError`` for non-positive amounts and for overdraw attempts.
* ``__repr__`` — developer form, e.g.
  ``BankAccount(holder='Ada', balance=120.0)``.
* ``__str__`` — user form, e.g. ``"Ada's account: $120.00"``.

In `main()`, exercise the happy path then deliberately trigger the overdraw
error and print the message.

Expected output
---------------
    BankAccount(holder='Ada', balance=0.0)
    BankAccount(holder='Ada', balance=120.0)
    Ada's account: $120.00
    caught: insufficient funds (tried to withdraw 500 from 120.0)

Run with:

    python exercise-05-bank-account.py
"""

from __future__ import annotations


class BankAccount:
    """A minimal checking account."""

    def __init__(self, holder: str, balance: float = 0.0) -> None:
        self.holder = holder
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("withdraw amount must be positive")
        if amount > self.balance:
            raise ValueError(
                f"insufficient funds (tried to withdraw {amount} from {self.balance})"
            )
        self.balance -= amount

    def __repr__(self) -> str:
        return f"BankAccount(holder={self.holder!r}, balance={self.balance!r})"

    def __str__(self) -> str:
        return f"{self.holder}'s account: ${self.balance:,.2f}"


def main() -> None:
    account = BankAccount("Ada")
    print(repr(account))           # developer form

    account.deposit(120)
    print(repr(account))
    print(str(account))            # user form

    try:
        account.withdraw(500)
    except ValueError as exc:
        print(f"caught: {exc}")


if __name__ == "__main__":
    main()
