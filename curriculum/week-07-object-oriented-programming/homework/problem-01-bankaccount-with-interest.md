# Problem 1 — `BankAccount` with interest

> **Topic:** subclassing a class that guards its own state, and turning a fraction into a whole cent on purpose
> **Lecture:** [02 — Inheritance and Composition](../lecture-notes/02-inheritance-and-composition.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** it is the smallest problem where inheritance and a real-world rule collide. The parent refuses anything that is not a whole number of cents. Interest is a fraction. Something has to give, and *you* have to decide what — and be able to say why out loud.

## The Brief

Take the `BankAccount` from
[Exercise 5](../exercises/exercise-05-bank-account.md) and add a subclass,
`SavingsAccount`, that pays interest.

A savings account is an account that also has an interest rate. It **is a**
`BankAccount` in the honest sense: nothing is taken away, one thing is added.
So it subclasses, calls `super().__init__(...)` for the shared setup, and adds
one field and one method:

- `interest_rate: float` — `0.02` means 2% per period.
- `apply_interest(self) -> None` — works out one period of interest and
  credits it by calling `deposit`.

That last word is the design. `apply_interest` must call `deposit`, not reach
into `_balance` and add. Interest is a credit like any other credit: it goes
through the same check, it lands in the same history, and if the bank later
adds a deposit fee or an audit hook, interest gets it for free. Reaching past
the method works today and silently skips every one of those.

**Now the part that makes this a real problem. The balance is in whole cents,
and interest is not.**

`BankAccount` stores money as an integer number of cents and refuses anything
that is not an `int` — that refusal is the whole point of Exercise 5. But
`balance * interest_rate` multiplies an `int` by a decimal, and a decimal is
exactly what `deposit` will not take. Handing it straight to `deposit` cannot
work, and it should not: 2% of 12,345 cents is 246.9 cents, and there is no
such thing as nine tenths of a cent in an account.

So you have to decide what happens to the fraction, and say so:

1. Work out the interest as a decimal.
2. Turn it into a whole number of cents with a rule you can state out loud.
3. Deposit that integer.

Use `round()`, and be ready to explain why in your docstring. Rounding down
every period quietly shorts the customer; rounding up quietly shorts the
bank. `round()` goes to the nearest cent, and on an exact half it goes to the
**even** one — so a long run of halves cancels out instead of drifting
towards one side. Real banks write this rule down and so should you.

One more edge case. If the interest rounds to `0` — a tiny balance, a tiny
rate — deposit nothing at all rather than calling `deposit(0)`, which
Exercise 5 rejects for good reason. A period that earns nothing is not an
error.

## Starter

Save this as `savings_account.py` and fill in the `TODO` markers. The
`BankAccount` half is given complete, so the file runs standalone. **If your
own Exercise 5 differs, keep yours** — only `SavingsAccount` is the homework.

```python
"""savings_account.py — a savings account that pays interest.

    python savings_account.py
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
        # TODO: super().__init__(...) FIRST, then refuse a negative rate,
        # then store self.interest_rate

    def apply_interest(self) -> None:
        """Credit one period of interest, rounded to the nearest whole cent."""
        # TODO: work out self._balance * self.interest_rate,
        # round it to a whole number of cents,
        # return early if that is 0,
        # otherwise call self.deposit(...) with the integer.
        # Say which rounding rule you chose, and why, in this docstring.

    def __repr__(self) -> str:
        """Developer form, including the rate."""
        # TODO


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
```

Two details in the given half that are worth a second look, because your
`SavingsAccount` depends on both.

**`_check_amount` refuses `bool` as well as non-integers.** `isinstance(True, int)`
is `True` in Python — `bool` really is a subclass of `int` — so without that
extra clause `deposit(True)` would add one cent. That is the stretch goal
from Exercise 5, already applied.

**`__repr__` uses `type(self).__name__`.** That is why a `SavingsAccount`
would already print `SavingsAccount(...)` even if you wrote no repr at all.
You override it anyway, because there is now a field worth showing — but the
base class was written so that a *future* subclass with no extra fields needs
nothing.

## Requirements

1. `SavingsAccount` subclasses `BankAccount`.
2. `__init__` calls `super().__init__(owner, balance)` as its first
   statement, then validates and stores `interest_rate`.
3. A negative `interest_rate` raises `ValueError` naming the value.
4. `apply_interest()` returns `None`. It works out
   `balance * interest_rate`, rounds it to a whole number of cents with
   `round()`, and passes that integer to `self.deposit(...)`.
5. Interest that rounds to `0` deposits nothing and raises nothing.
6. `apply_interest` never touches `self._balance` directly.
7. `__repr__` shows the owner, the balance in cents, and the rate.
8. Do not edit `main()`.

## Constraints

- **Credit through `deposit`, never through `_balance`.** Interest that goes
  round the side of the method is interest with no history entry, no
  validation, and no future deposit rule applied to it. It would work today
  and be wrong forever.
- **Round to a whole cent before `deposit` sees the number.** `deposit`
  refuses decimals on purpose. `round()` returns an `int` when you give it
  one argument, which is precisely what you need. `round(246.9, 2)` returns a
  *decimal* — the two-argument form keeps the type — so do not use it here.
- **State your rounding rule in the docstring.** `round()` goes to the
  nearest cent and, on an exact half, to the even cent. Half-up hands the
  customer a fraction every period; half-down keeps it. Half-to-even means
  the halves cancel instead of piling up on one side. Over a few million
  interest runs that is a real number on somebody's books.
- **Zero interest is not an error.** Return early. `deposit(0)` raises
  `ValueError: amount must be positive cents, got 0`, and "you earned nothing
  this month" is not a failure.
- **`super().__init__(...)` comes first, before your own checks.** Validate
  the parent's state first, so a bad owner name fails before an interest rate
  is stored.
- **The rate is the only decimal in the class, and it meets the integers in
  exactly one line.** `round(self._balance * self.interest_rate)`. That is
  the money decision, and it is the line a reviewer will read first.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-bankaccount-with-interest.py
Ada: $123.45
after depositing $50.00: Ada: $173.45
after withdrawing $25.00: Ada: $148.45
after one period of interest:  Ada: $151.42
refused: cannot withdraw $10,000.00 from $151.42
a penny at 0.1% earns nothing: Grace: $0.10
history: [('deposit', 5000), ('withdraw', 2500), ('deposit', 297)]
repr: SavingsAccount(owner='Ada', balance=15142, interest_rate=0.02)
```

Check the arithmetic by hand, in cents. Ada opens with 12,345. Plus 5,000 is
17,345. Minus 2,500 is 14,845. Two per cent of 14,845 is 296.9, which rounds
to **297**, giving 15,142 — `$151.42`.

Grace has 10 cents at 0.1%, which is 0.01 cents. `round(0.01)` is `0`, so
nothing was deposited and nothing raised. Her balance is still `$0.10`.

The `history` line is the proof that interest went through `deposit`. There
are three entries and you only wrote two of them by hand — `('deposit', 297)`
is the interest, recorded automatically, as an integer.

## Steps

1. Save the starter and run it. It fails in `SavingsAccount.__init__`,
   because a method whose body is only a comment returns `None` and never
   sets `interest_rate`.
2. Write `__init__`. Run — the first three lines should be right, because
   they only use inherited behaviour.
3. Before you write `apply_interest`, do the arithmetic in a REPL so you know
   what you are aiming at:

   ```bash
   python -c "print(14845 * 0.02, round(14845 * 0.02))"
   ```

   ```text
   296.90000000000003 297
   ```

   Note what came back. Not `296.9` — the product carries a little binary
   noise, which is exactly why it must not be allowed anywhere near the
   balance. `round()` throws the noise away and hands you a clean `297`.

4. Write `apply_interest`. Get the fourth line to say `$151.42`.
5. Now break it on purpose. Delete the `round()` and pass the raw product to
   `deposit`. Read the `TypeError` in full — it is the parent class refusing
   to let a fraction into the ledger, which is exactly what you wanted it to
   do. Put the `round()` back.
6. Add the early return for zero interest and confirm Grace's line prints
   rather than raising.
7. Write `__repr__` and check the last two lines.
8. Prove the credit really went through `deposit`: `account.history` must
   hold three entries, the last of which is `('deposit', 297)`.

## The Solution

```python
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
```

**`apply_interest` calls `deposit` instead of touching `_balance`.** This is
the single decision that makes the problem interesting. The payoff is that
interest is a credit like any other: it is checked by the same rule, it
appears in `history` as `('deposit', 297)`, and if the bank later adds a
deposit fee or an audit hook, interest gets it automatically. Reaching
straight into `self._balance += earned` would work today and silently bypass
every one of those.

**The whole money question lives in one line, and it is defensible.**
`round(self._balance * self.interest_rate)` is where a decimal turns back
into a whole cent, and it does it before `deposit` is ever called. `round()`
with one argument returns an `int`, which is exactly the type `deposit`
wants:

```text
>>> round(296.9)
297
>>> type(round(296.9))
<class 'int'>
>>> round(296.9, 2)
296.9
>>> type(round(296.9, 2))
<class 'float'>
```

Note the second pair. The two-argument form keeps the type, so it would hand
`deposit` the very thing `deposit` exists to refuse.

**Why to the even cent on an exact half.** Watch it:

```text
>>> [round(x) for x in (0.5, 1.5, 2.5, 3.5, 4.5)]
[0, 2, 2, 4, 4]
```

Half of those went down and half went up. That is the point. Always rounding
a half up hands the customer a fraction of a cent every period; always
rounding down keeps it. Over a few million interest runs either choice is a
real number on somebody's books, and going to the even one means the halves
cancel out instead of piling up on one side. Banks call this rule
**banker's rounding**, and Python's `round()` and `decimal`'s
`ROUND_HALF_EVEN` both implement it.

**The `if earned == 0: return` guard exists because `deposit` rejects
non-positive amounts.** A tiny balance at a tiny rate computes less than half
a cent, which rounds to zero, and depositing zero raises. There is no
sensible reading in which "you earned nothing this month" is an error, so the
method returns early. This is the kind of interaction that only shows up when
you actually run the demo with an edge case in it — which is why the demo has
one.

**`balance` is a read-only `@property` over `_balance`.** The underscore says
"internal"; the property gives callers a supported way to read the number
without a supported way to write it. `account.balance = 1_000_000` raises
`AttributeError: property 'balance' of 'SavingsAccount' object has no setter`
instead of quietly minting money.

**`super().__init__(owner, balance)` before anything else.** The parent sets
`owner`, `_balance` and `_history` and runs their checks. The subclass then
adds only what is new. Note the order: validate the parent's state first, so
a bad opening balance fails before an interest rate is stored.

**`InsufficientFunds(ValueError)`, not a bare `ValueError`.** Callers who do
not know the type still catch it with `except ValueError`; callers who care
can tell "you asked for a nonsense amount" from "you do not have that much".
Same design as `EmptyDeckError(IndexError)` in Challenge 01.

## Run it

Copy the worked answer on this page into `problem-01-bankaccount-with-interest.py` and run it:

```bash
python problem-01-bankaccount-with-interest.py
```

It imports nothing and needs no setup. Save your own version as
`savings_account.py`; the longer download name is there so it cannot
overwrite your work.

## Common bugs to catch

- **`TypeError: amount must be whole cents as an int, got 296.9`.** You passed
  the raw product to `deposit`:

  ```python
      def apply_interest(self) -> None:
          self.deposit(self._balance * self.interest_rate)
  ```

  This is the parent class doing its job. `int` times `float` is `float`, and
  `deposit` refuses floats on purpose. Round first.

- **`ValueError: amount must be positive cents, got 0`.** You forgot the
  early return, and a balance small enough to earn less than half a cent
  reached `deposit(0)`. Grace's line in the demo is there specifically to
  catch this.

- **`TypeError: amount must be whole cents as an int, got 296.9` — even
  though you called `round`.** You wrote `round(x, 2)`. The two-argument form
  returns a float. Drop the second argument.

- **`AttributeError: 'SavingsAccount' object has no attribute '_balance'`.**
  You forgot `super().__init__(...)`:

  ```python
  class SavingsAccount(BankAccount):
      def __init__(self, owner, balance=0, interest_rate=0.02):
          self.interest_rate = interest_rate   # and nothing else
  ```

  The traceback points at `deposit` or `__str__`, several calls away from the
  actual mistake, because nothing reads `_balance` until then.

- **`AttributeError: 'SavingsAccount' object has no attribute 'interest_rate'`.**
  Your `__init__` body is only comments, so it returns `None` and sets
  nothing. The starter is written that way on purpose so the first run tells
  you where to begin.

- **The history has two entries instead of three.** You mutated `_balance`
  directly in `apply_interest`. The balance is right, the ledger is wrong,
  and nothing raised — which is what makes this one worth naming.

- **`AttributeError: property 'balance' of 'BankAccount' object has no setter`.**
  You wrote `self.balance = balance` somewhere. Assign the *underlying*
  attribute, `self._balance`, which is what the property is a view of.

- **Twelve calls give twelve identical credits.** They should not.
  `for _ in range(12): account.apply_interest()` is *compound* interest —
  each call earns interest on the previous interest. That may well be what
  you want; just know it is what you wrote. Two calls on Ada's balance give
  297 then 303, not 297 twice.

## Under the hood

<details>
<summary>Under the hood — round(), banker's rounding, and the two ways a half can go</summary>

`round()` surprises almost everybody the first time:

```text
>>> round(2.5)
2
>>> round(3.5)
4
>>> round(0.5)
0
```

That is not a bug and it is not an approximation error. It is a deliberate
rule called **round-half-to-even**, and Python chose it because the
alternative has a bias.

Think about rounding a long column of numbers that all end in exactly half.
Round every one up and the total is systematically too high; round every one
down and it is systematically too low. Neither error cancels — it accumulates
in one direction, forever. Send half of them up and half down, chosen by
whether the neighbour is even, and the errors cancel over any reasonable
sample.

For interest that means the difference between "the bank quietly gains a
fraction of a cent per account per period" and "nobody does". At one account
it is invisible. At ten million accounts, twelve times a year, it is a line
item.

There is a second surprise underneath, and it is not `round()`'s fault:

```text
>>> round(2.675, 2)
2.67
```

That looks like half-to-even going the wrong way — 7 is odd, so surely it
should go up to 2.68? It is not doing half-to-even at all. `2.675` is not
exactly 2.675 in binary:

```text
>>> from decimal import Decimal
>>> Decimal(2.675)
Decimal('2.67499999999999982236431605997495353221893310546875')
```

The stored number is a hair *below* the halfway point, so `round` correctly
rounds it down. There was never a tie to break. This is the same family of
problem as `int(4.35 * 100)` giving `434` in Exercise 5, and it is why
"decimals plus rounding" is not a fix for money — the rounding is honest
about a number that was already wrong.

`decimal.Decimal` gives you the tie back, and lets you name the rule:

```text
>>> from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
>>> Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
Decimal('2.68')
>>> Decimal("2.665").quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
Decimal('2.66')
>>> Decimal("2.665").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
Decimal('2.67')
```

`Decimal("2.675")` really is two point six seven five, so the tie is real and
half-to-even breaks it upward to the even 8. The next pair shows the same tie
breaking downward, and the last shows a different rule giving a different —
and equally defensible, if you have written it down — answer.

`decimal` has eight rounding modes for exactly this reason: which one you owe
your customer is a business decision and sometimes a legal one, not a
programming detail. `ROUND_HALF_EVEN` is the default because it is the least
biased, but tax authorities in several countries mandate `ROUND_HALF_UP`, and
a system that silently used the wrong one would be wrong in a way no test
would catch.

So the full picture for this problem:

- The **balance** is integer cents, so it never drifts.
- The **rate** is the only decimal, and it touches the integers in exactly
  one line.
- That line **names its rounding rule in a docstring**, so the next person to
  read it knows the decision was made rather than defaulted into.

If this were a real bank, the rate would be a `Decimal` too, built from a
string, and the line would end in an explicit `.quantize(...)`. Reach for
that the moment somebody hands you a rounding rule in writing.

</details>

## Acceptance checklist

- [ ] `python savings_account.py` runs with no traceback.
- [ ] All eight output lines match exactly.
- [ ] `SavingsAccount.__init__` calls `super().__init__(...)` first.
- [ ] `apply_interest` calls `deposit` and never touches `_balance`.
- [ ] The interest reaching `deposit` is an `int`.
- [ ] Interest that rounds to `0` deposits nothing and raises nothing.
- [ ] The docstring says which rounding rule you chose and why.
- [ ] `account.history` ends with `('deposit', 297)`.
- [ ] Every signature is type-hinted.
- [ ] Committed to Git with a message like
      `Add Week 7 homework 1: savings account`.

## Stretch

- Add `apply_interest(periods: int = 1)` that compounds. Then print the
  balance after twelve monthly periods at 2% and compare it against
  `balance * 1.02 ** 12` rounded once at the end. They will differ, because
  rounding at every step is not the same as rounding once. Write one sentence
  saying which one a bank should use and why.
- Rebuild `SavingsAccount` with `decimal.Decimal` for the rate, built from a
  string, and an explicit `quantize(..., rounding=ROUND_HALF_EVEN)`. Keep the
  balance in integer cents. Note what changed and what did not.
- Add a `statement()` method that returns a multi-line string from `history`,
  using `format_usd` on each amount and marking the interest credits
  differently from the customer's own deposits. You will need a third value
  in each history entry — decide whether that is a tuple, a small
  `@dataclass`, or a subclass, and say why.
- Add a minimum-balance rule: below `$5.00`, no interest is paid at all. Where
  does that check belong — in `apply_interest`, or in a new
  `_eligible_for_interest` property? Write one sentence defending your choice.

Next: [Problem 2 — Polygon hierarchy](./problem-02-polygon-hierarchy.md).
