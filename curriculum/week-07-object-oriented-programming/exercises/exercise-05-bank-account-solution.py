"""exercise-05-bank-account-solution.py — money in integer cents, errors that say why.

A single-account ledger for a credit union teller screen. The `-solution` in
the name keeps this file from colliding with the `exercise-05-bank-account.py`
you write yourself. Run it with::

    python exercise-05-bank-account-solution.py
"""

CENTS_PER_DOLLAR = 100


class InsufficientFunds(ValueError):
    """Raised when a withdrawal would push the balance below zero."""


def format_usd(cents: int) -> str:
    """Render a non-negative whole number of cents as `$1,234.56`.

    format_usd(0)       -> "$0.00"
    format_usd(12550)   -> "$125.50"
    format_usd(1234567) -> "$12,345.67"
    """
    dollars = cents // CENTS_PER_DOLLAR
    remainder = cents % CENTS_PER_DOLLAR
    return f"${dollars:,}.{remainder:02d}"


class BankAccount:
    """One account. The balance is an integer number of cents, always."""

    def __init__(self, holder: str) -> None:
        """Open an empty account for `holder`."""
        self.holder = holder
        self._balance_cents = 0
        self._history: list[tuple[str, int]] = []

    @staticmethod
    def _check_amount(cents: int) -> None:
        """Raise if `cents` is not a positive whole number of cents."""
        if not isinstance(cents, int):
            raise TypeError(
                f"amount must be a whole number of cents, got {cents!r}"
            )
        if cents <= 0:
            raise ValueError(f"amount must be positive, got {cents}")

    @property
    def balance_cents(self) -> int:
        """The balance, in cents. Read-only from outside the class."""
        return self._balance_cents

    @property
    def balance_display(self) -> str:
        """The balance as `$125.50`."""
        return format_usd(self._balance_cents)

    @property
    def history(self) -> list[tuple[str, int]]:
        """A copy of the ledger: ("deposit" | "withdraw", cents) pairs."""
        return list(self._history)

    def deposit(self, cents: int) -> None:
        """Add `cents` to the balance and record it."""
        self._check_amount(cents)
        self._balance_cents += cents
        self._history.append(("deposit", cents))

    def withdraw(self, cents: int) -> None:
        """Remove `cents` from the balance and record it.

        Raises InsufficientFunds if the balance would go negative.
        """
        self._check_amount(cents)
        if cents > self._balance_cents:
            raise InsufficientFunds(
                f"withdrawal of {format_usd(cents)} exceeds balance of "
                f"{format_usd(self._balance_cents)}"
            )
        self._balance_cents -= cents
        self._history.append(("withdraw", cents))

    def __repr__(self) -> str:
        """Developer form: BankAccount(holder='Ravi Menon', balance_cents=12550)."""
        return (
            f"BankAccount(holder={self.holder!r}, "
            f"balance_cents={self._balance_cents!r})"
        )

    def __str__(self) -> str:
        """Teller-screen form: Ravi Menon: $125.50."""
        return f"{self.holder}: {self.balance_display}"


def main() -> None:
    """Run one account through a good day and four bad requests."""
    account = BankAccount("Ravi Menon")
    print(account)

    account.deposit(12_550)
    print(account)
    print(repr(account))

    try:
        account.withdraw(20_000)
    except InsufficientFunds as exc:
        print(f"Declined: {exc}")

    account.withdraw(10_000)
    print(account)

    try:
        account.deposit(5.5)
    except TypeError as exc:
        print(f"Declined: {exc}")

    try:
        account.deposit(-100)
    except ValueError as exc:
        print(f"Declined: {exc}")

    print(f"history: {account.history}")
    print(f"0.1 + 0.2 == 0.3 -> {0.1 + 0.2 == 0.3}")
    print(f"10 + 20 == 30 -> {10 + 20 == 30}")


if __name__ == "__main__":
    main()
