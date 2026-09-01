"""problem-01-bankaccount-with-interest-solution.py — a savings account that pays interest.

The `-solution` in the name keeps this file from colliding with the
`savings_account.py` you write yourself. Run it with::

    python problem-01-bankaccount-with-interest-solution.py

The balance is a whole number of cents and `deposit` refuses anything that is
not an `int`. The interest rate is a float, so the product is a float, so the
one place the two meet — `round(self._balance * self.interest_rate)` — turns it
straight back into a whole cent before it goes anywhere near `deposit`.
"""

CENTS_PER_DOLLAR = 100


def format_usd(cents: int) -> str:
    """Render a non-negative whole number of cents as `$1,234.56`."""
    dollars, remainder = divmod(cents, CENTS_PER_DOLLAR)
    return f"${dollars:,}.{remainder:02d}"


class InsufficientFunds(ValueError):
    """Raised when a withdrawal would take the balance below zero."""


class BankAccount:
    """A balance in whole cents that only moves through deposit and withdraw."""

    def __init__(self, owner: str, balance: int = 0) -> None:
        """Open an account for `owner`, optionally with an opening balance."""
        self._check_amount(balance, allow_zero=True)
        self.owner = owner
        self._balance = balance
        self._history: list[tuple[str, int]] = []

    @staticmethod
    def _check_amount(amount: int, *, allow_zero: bool = False) -> None:
        """Raise unless `amount` is a whole number of cents of the right sign."""
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise TypeError(f"amount must be whole cents as an int, got {amount!r}")
        if amount < 0 or (amount == 0 and not allow_zero):
            raise ValueError(f"amount must be positive cents, got {amount!r}")

    @property
    def balance(self) -> int:
        """The balance, in whole cents. Read-only from outside."""
        return self._balance

    @property
    def history(self) -> list[tuple[str, int]]:
        """A copy of the ledger: ("deposit" | "withdraw", cents) pairs."""
        return list(self._history)

    def deposit(self, cents: int) -> None:
        """Add `cents` to the balance and record it."""
        self._check_amount(cents)
        self._balance += cents
        self._history.append(("deposit", cents))

    def withdraw(self, cents: int) -> None:
        """Take `cents` off the balance, or refuse if there is not enough."""
        self._check_amount(cents)
        if cents > self._balance:
            raise InsufficientFunds(
                f"cannot withdraw {format_usd(cents)} from {format_usd(self._balance)}"
            )
        self._balance -= cents
        self._history.append(("withdraw", cents))

    def __repr__(self) -> str:
        """Developer form, naming the actual subclass."""
        return f"{type(self).__name__}(owner={self.owner!r}, balance={self._balance})"

    def __str__(self) -> str:
        """Teller-screen form, e.g. `Ada: $123.45`."""
        return f"{self.owner}: {format_usd(self._balance)}"


class SavingsAccount(BankAccount):
    """A BankAccount that pays interest on its own balance."""

    def __init__(
        self, owner: str, balance: int = 0, interest_rate: float = 0.02
    ) -> None:
        """Let BankAccount set up the money, then check the rate."""
        super().__init__(owner, balance)
        if interest_rate < 0:
            raise ValueError(
                f"interest_rate must be non-negative, got {interest_rate!r}"
            )
        self.interest_rate = interest_rate

    def apply_interest(self) -> None:
        """Credit one period of interest, rounded to the nearest whole cent.

        The balance is an integer number of cents and the rate is a float, so
        the product is a float and `deposit` will not take it. `round()` picks
        the nearest cent, and on an exact half it picks the even one, so a long
        run of halves does not drift towards the bank or the customer. Interest
        that rounds to nothing is not deposited at all — `deposit(0)` is
        refused, and a period that earns nothing is not an error.
        """
        earned = round(self._balance * self.interest_rate)
        if earned == 0:
            return
        self.deposit(earned)

    def __repr__(self) -> str:
        """Developer form, including the rate."""
        return (
            f"SavingsAccount(owner={self.owner!r}, balance={self._balance}, "
            f"interest_rate={self.interest_rate!r})"
        )


def main() -> None:
    """Run one savings account through a month, then two edge cases."""
    account = SavingsAccount("Ada", 12_345, interest_rate=0.02)
    print(account)

    account.deposit(5_000)
    print(f"after depositing {format_usd(5_000)}: {account}")

    account.withdraw(2_500)
    print(f"after withdrawing {format_usd(2_500)}: {account}")

    account.apply_interest()
    print(f"after one period of interest:  {account}")

    try:
        account.withdraw(1_000_000)
    except InsufficientFunds as exc:
        print(f"refused: {exc}")

    tiny = SavingsAccount("Grace", 10, interest_rate=0.001)
    tiny.apply_interest()
    print(f"a penny at 0.1% earns nothing: {tiny}")

    print(f"history: {account.history}")
    print(f"repr: {account!r}")


if __name__ == "__main__":
    main()
