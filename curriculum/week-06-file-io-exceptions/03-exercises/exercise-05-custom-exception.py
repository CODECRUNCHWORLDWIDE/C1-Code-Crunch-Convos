"""Exercise 05 — Custom exception class.

Topic: defining custom exceptions, raise / try / except.
Reference: lecture-notes/03-exceptions-and-logging.md sections 6 and 7.

Task
----
Define `InsufficientFundsError`, a custom exception that:

  * Inherits from Exception.
  * Carries the current balance and the attempted withdrawal amount.
  * Has a useful default __str__ (so a plain `print(err)` is readable).

Then implement `withdraw(balance, amount)`:

  * If `amount` is negative, raise ValueError.
  * If `amount` exceeds `balance`, raise InsufficientFundsError.
  * Otherwise, return the new balance.

The __main__ block exercises both the happy path and the failure path
so you can see your exception in action.

Expected output:

    Withdrew $40. New balance: $60
    Insufficient funds: tried to withdraw $200, but balance is only $60.
       (short by $140)
    Caught ValueError: amount must be non-negative
"""

from __future__ import annotations


class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the current balance."""

    def __init__(self, balance: float, amount: float) -> None:
        self.balance = balance
        self.amount = amount
        message = (
            f"tried to withdraw ${amount:g}, "
            f"but balance is only ${balance:g}"
        )
        super().__init__(message)

    @property
    def shortfall(self) -> float:
        """How much more money would be needed for the withdrawal to succeed."""
        return self.amount - self.balance


def withdraw(balance: float, amount: float) -> float:
    """Return the new balance after withdrawing `amount` from `balance`."""
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if amount > balance:
        raise InsufficientFundsError(balance=balance, amount=amount)
    return balance - amount


if __name__ == "__main__":
    balance = 100.0

    # Happy path
    balance = withdraw(balance, 40)
    print(f"Withdrew $40. New balance: ${balance:g}")

    # Insufficient funds
    try:
        withdraw(balance, 200)
    except InsufficientFundsError as e:
        print(f"Insufficient funds: {e}.")
        print(f"   (short by ${e.shortfall:g})")

    # Bad input
    try:
        withdraw(balance, -10)
    except ValueError as e:
        print(f"Caught ValueError: {e}")
