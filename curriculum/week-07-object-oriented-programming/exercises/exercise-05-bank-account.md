# Exercise 5 — Bank Account

> **Topic:** state a class guards rather than merely stores, custom exceptions, and `__repr__` vs `__str__`
> **Lecture:** [03 — Dataclasses, Dunder Methods, and Friends](../lecture-notes/03-dataclasses-and-magic-methods.md)
> **Also read:** [01 — Classes and Instances](../lecture-notes/01-classes-and-instances.md), section 8, for the `__repr__` and `__str__` contract
> **Difficulty:** Medium
> **Target time:** 90 minutes
> **Why this one:** this is where a class stops being a container and starts being a *guard*. A balance is not just a number you store. It is a number that must never go negative, must never change except through two recorded operations, and must never be a decimal. Every one of those rules is enforced by the class or by nobody. The mini-project at the end of this week is the same shape with more nouns.

## The Brief

You are writing the account object behind a credit union's teller screen. It
holds one balance, it accepts deposits and withdrawals, and it keeps a
history of what actually happened.

The requirement that trips people up is the money itself. **The balance is a
whole number of cents.** Not dollars, not a decimal. A balance of `$125.50`
is stored as the integer `12550`. Every amount that crosses the class
boundary is in cents too. Turning cents into dollars for a human happens at
the very edge, in one function, and nowhere else.

Here is why, and it is worth ten seconds in a REPL before you read on.
Computers store decimals in binary, and most ordinary decimals have no exact
binary form — the same way one third has no exact decimal form. So:

```text
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

That is not a display glitch. That number *is* what the machine holds. Add
seventy cents to a running total ten times and you get `7.000000000000001`,
and it will never be `7.0` again. Whole numbers have no such problem: `10 + 20`
is exactly `30`, and Python integers never run out of room. So you count
cents.

This is the single most common serious bug in beginner financial code, and it
is why every payment system you will ever plug into — Stripe, PayPal, your
bank's API — quotes amounts in the smallest currency unit.

The other new idea here is a **custom exception**. You will write
`class InsufficientFunds(ValueError)` — a brand-new error type that *is a*
`ValueError`, using the inheritance you learned in Exercise 3. Callers who
only know about `ValueError` still catch it. Callers who care can catch just
this one.

## Starter

Create `exercise-05-bank-account.py` and fill in the `TODO` markers:

```python
"""exercise-05-bank-account.py — money in integer cents, errors that say why.

A single-account ledger for a credit union teller screen. Run it with:

    python exercise-05-bank-account.py
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
    # TODO: integer-divide for the dollars, modulo for the cents.
    # Use :, on the dollars and :02d on the cents.
    raise NotImplementedError


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
        # TODO: TypeError(f"amount must be a whole number of cents, got {cents!r}")
        #       when cents is not an int
        # TODO: ValueError(f"amount must be positive, got {cents}")
        #       when cents is zero or negative

    @property
    def balance_cents(self) -> int:
        """The balance, in cents. Read-only from outside the class."""
        # TODO
        raise NotImplementedError

    @property
    def balance_display(self) -> str:
        """The balance as `$125.50`."""
        # TODO: reuse format_usd
        raise NotImplementedError

    @property
    def history(self) -> list[tuple[str, int]]:
        """A copy of the ledger: ("deposit" | "withdraw", cents) pairs."""
        # TODO: return a new list, not self._history itself
        raise NotImplementedError

    def deposit(self, cents: int) -> None:
        """Add `cents` to the balance and record it."""
        # TODO: validate, then update, then record

    def withdraw(self, cents: int) -> None:
        """Remove `cents` from the balance and record it.

        Raises InsufficientFunds if the balance would go negative.
        """
        # TODO: validate the amount, then check funds, then update, then record

    def __repr__(self) -> str:
        """Developer form: BankAccount(holder='Ravi Menon', balance_cents=12550)."""
        # TODO
        raise NotImplementedError

    def __str__(self) -> str:
        """Teller-screen form: Ravi Menon: $125.50."""
        # TODO
        raise NotImplementedError


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
```

Three things in that starter you have not met.

**`@staticmethod`** marks a method that does not take `self`. `_check_amount`
validates an amount, and an amount is an amount whether or not anybody owns
it. Keeping it on the class groups it with the code that uses it; marking it
static says plainly that it reads no state, so nobody has to check.

**`isinstance(x, int)`** asks whether a value really is a whole number. This
is the check you need, and a type hint is not a substitute. `cents: int` is
documentation — Python never looks at it and never stops anything. `isinstance`
is a real question with a real answer.

**`12_550`** is `12550`. Underscores in numbers are ignored by Python and
exist purely so you can see the groups. `1_000_000` is a great deal easier to
read than `1000000`.

## Requirements

1. `format_usd` is the only place in the file that turns cents into a dollar
   string. `format_usd(12550)` is `"$125.50"`; `format_usd(1234567)` is
   `"$12,345.67"`.
2. `_check_amount` raises `TypeError` for a non-integer amount and
   `ValueError` for zero or a negative one, with the exact messages in the
   starter docstrings. Two different mistakes deserve two different exception
   types.
3. `balance_cents`, `balance_display`, and `history` are read-only
   properties. There is no setter for any of them.
4. `history` returns a **copy**. A caller who changes the returned list must
   not change the account's ledger.
5. `deposit` and `withdraw` each validate first, change the balance second,
   record third. A failed operation leaves the balance and the history
   exactly as they were.
6. `withdraw` raises `InsufficientFunds` with the message
   `withdrawal of $200.00 exceeds balance of $125.50`, built with
   `format_usd` on both numbers.
7. `InsufficientFunds` subclasses `ValueError`, so existing code that catches
   `ValueError` around a withdrawal keeps working.
8. `__repr__` shows the raw integer; `__str__` shows the formatted dollars.
   They are for different readers and they should not match.
9. Do not edit `main()`.

## Constraints

- **The balance is an `int` of cents. Never a decimal.** Store dollars as
  decimals and every operation adds a tiny error. After a few thousand
  transactions the ledger no longer sums to the statement, and you cannot
  tell a rounding artifact from a real discrepancy. Integers are exact,
  Python integers never overflow, and `12550` means one thing only.
- **Converting a decimal price to cents loses money.** The obvious bridge
  from a decimal world into this one is `int(price * 100)`, and it is wrong:

  ```text
  >>> 4.35 * 100
  434.99999999999994
  >>> int(4.35 * 100)
  434
  ```

  A `$4.35` item became 434 cents. `int()` chops rather than rounds, and
  `4.35 * 100` lands a hair *below* 435, so the cent is gone, silently, on a
  price that looks completely ordinary. If you must accept a decimal price,
  parse the text or go through `decimal.Decimal`, and never let a plain float
  sit in the middle.
- **`round()` is not a fix for decimal money.** It corrects what you print
  and leaves the stored value wrong, which is worse than leaving the error
  visible: the bug survives and the evidence does not.
- **Validate before you change anything.** If `withdraw` subtracts first and
  checks the balance afterwards, a declined withdrawal has already moved
  money. The order in requirement 5 is the whole safety property of the
  class.
- **`_balance_cents` gets one leading underscore, and no code outside the
  class touches it.** The underscore is a convention, not a lock — Python
  will happily let a caller write `account._balance_cents = 999999`. What the
  convention buys you is that every legitimate change goes through `deposit`
  or `withdraw`, so the history is complete, and any line that reaches past
  the underscore is visibly suspicious in review.
- **`history` returns a copy for the same reason.** Handing out the real list
  means any caller can rewrite the audit trail, by accident or otherwise.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-bank-account.py
Ravi Menon: $0.00
Ravi Menon: $125.50
BankAccount(holder='Ravi Menon', balance_cents=12550)
Declined: withdrawal of $200.00 exceeds balance of $125.50
Ravi Menon: $25.50
Declined: amount must be a whole number of cents, got 5.5
Declined: amount must be positive, got -100
history: [('deposit', 12550), ('withdraw', 10000)]
0.1 + 0.2 == 0.3 -> False
10 + 20 == 30 -> True
```

Read the `history` line carefully. After the opening deposit there were four
more requests — one withdrawal that succeeded and three that were refused —
so the ledger holds exactly two entries. If yours holds three or five, you
are recording attempts instead of transactions.

Lines two and three are the same object printed for two audiences: dollars
for the teller, raw cents for whoever is reading a log.

The last two lines are the money argument in one line each.

## Steps

1. Create the file and implement `format_usd` first. Test it in the REPL
   against all three examples in its docstring before you go further — every
   other piece of output depends on it.
2. Implement `_check_amount`, then check both failure modes directly:
   `BankAccount._check_amount(5.5)` and `BankAccount._check_amount(0)`.
3. Implement the three properties, then `deposit`. Run the script; the first
   three lines should be right.
4. Implement `withdraw`, including the funds check and the
   `InsufficientFunds` message.
5. Implement `__repr__` and `__str__`. Confirm lines two and three of the
   output differ — same object, two audiences.
6. Verify the failure path leaves no trace. In the REPL: open an account,
   deposit `500`, attempt `withdraw(9_999)` inside a `try`, then check that
   `balance_cents` is still `500` and `history` has one entry.
7. Verify the copy: `h = account.history; h.append(("fake", 1))`, then print
   `account.history` and confirm the fake entry is not there.
8. Run the money experiment for yourself. Add `0.7` to a running total ten
   times and print the result: you get `7.000000000000001`, not `7.0`. Add
   `70` cents ten times and you get exactly `700`. Then try
   `int(4.35 * 100)`. That is the constraint, in three lines, with your own
   eyes.

## The Solution

```python
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
```

**Validate, then change, then record — in that order, in both methods.** This
is the safety property of the whole class, and the order is not cosmetic. If
`withdraw` subtracts before it checks, a declined withdrawal has already
moved money. If either method records before it changes anything, the ledger
contains transactions that never happened. Because every guard raises before
touching a single field, a failed operation leaves the account exactly as it
was — which is why the demo's three rejections leave a two-entry history.

**Two mistakes get two exception types.** A decimal amount is a caller who
does not understand the units. A negative amount is a caller who understands
them and got the sign wrong. `TypeError` and `ValueError` let a caller handle
those differently.

The order of the two checks is worth being precise about, because it is easy
to mis-remember. Checking the type first is not what stops `5.5`. What stops
`5.5` is the type check *existing at all* — `5.5` is a perfectly positive
number, so it walks straight past `cents <= 0` untouched no matter which
check runs first. Take the `isinstance` line out and the deposit is simply
accepted, and the last bug in the list below shows where it eventually
surfaces.

Where the order *does* matter is a negative decimal. With the type check
first, `-5.5` is reported as `TypeError: amount must be a whole number of
cents, got -5.5`, which names the real problem: wrong units. With the value
check first, it is reported as `ValueError: amount must be positive, got
-5.5`, which sends the caller off to fix a sign that was never the issue.
Both refuse the amount; only one of them tells the truth about why.

`InsufficientFunds` subclasses `ValueError` for the opposite reason: it is a
special case, not a new category, so existing code with a broad
`except ValueError` around a withdrawal keeps working, while careful code can
catch just this one. The cost is that you must order your own handlers
specific-first — `except InsufficientFunds` above `except ValueError`, or the
broad one swallows it.

**`_check_amount` is a `@staticmethod` because it never looks at an account.**
It validates an amount, and an amount is an amount whether or not anyone owns
it.

**`history` returns `list(self._history)`, and that one call is the difference
between a ledger and a suggestion.** Returning `self._history` hands every
caller a live handle on the audit trail, and any one of them can append,
delete or reorder it — by accident, which is the common case, or otherwise.
The copy is shallow, which is enough here because the entries are tuples and
tuples cannot be changed in place.

**`format_usd` is the only place cents become dollars.** One function, called
by `balance_display` and by the `InsufficientFunds` message, so the comma
separator and the two-digit cents cannot drift apart between the teller
screen and the decline notice. `//` takes the dollars and `%` takes the
remainder, both on integers, so no decimal is created anywhere on the path
from stored value to printed string.

## Run it

Copy the worked answer on this page into `exercise-05-bank-account.py` and run it:

```bash
python exercise-05-bank-account.py
```

It imports nothing and needs no setup. The `-solution` in the name keeps it
from colliding with your own `exercise-05-bank-account.py`. Homework
problem 1 extends this exact class with a `SavingsAccount` that pays
interest, so keep it.

## Common bugs to catch

- **`$125.5` instead of `$125.50`.** The cents half is missing `:02d`:

  ```text
  $125.50
  $4.5
  ```

  The first line is right by luck — fifty cents happens to be two digits.
  `format_usd(405)` is the one that shows the bug: five cents printed as a
  single `5`, so `$4.05` reads as forty-five cents. A missing `:,` on the
  dollars half has the same flavour, and only shows up above a thousand
  dollars.

- **`$125.5.50`.**

  ```text
  $125.5.50
  ```

  You used `/` where you needed `//`. True division returns a decimal, so
  `12550 / 100` is `125.5`, and the formatted cents get glued onto the end of
  it.

- **The balance goes negative.** The funds check happens after the
  subtraction, or it compares `cents < self._balance_cents` when the
  rejection rule is `cents > self._balance_cents`.

- **`history` shows three entries.**

  ```text
  history: [('deposit', 12550), ('withdraw', 20000), ('withdraw', 10000)]
  ```

  Three entries where the correct answer is two. You appended to `_history`
  before the guards, so the declined `$200.00` withdrawal is in the ledger as
  though it happened, and the history no longer explains the balance. You are
  recording attempts; the ledger records transactions.

- **`AttributeError: property 'balance_cents' of 'BankAccount' object has no setter`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 12, in <module>
      BankAccount("Ravi Menon").deposit(12_550)
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
    File "<string>", line 10, in deposit
      self.balance_cents += cents
      ^^^^^^^^^^^^^^^^^^
  AttributeError: property 'balance_cents' of 'BankAccount' object has no setter
  ```

  Inside `deposit` you wrote `self.balance_cents += cents`. The property is
  the public read-only view; the writable field is `self._balance_cents`. The
  fact that this error exists at all is the read-only design doing its job —
  even against you.

- **Skipping the `isinstance` check entirely.** This is the one to read
  slowly, because there is no error where the mistake is:

  ```python
      @staticmethod
      def _check_amount(cents: int) -> None:
          if cents <= 0:
              raise ValueError(f"amount must be positive, got {cents}")
  ```

  `account.deposit(5.5)` now **succeeds**. `5.5` is positive, so the only
  guard lets it through, and the balance quietly becomes `12555.5` — a
  decimal, in an account that promised never to hold one. The program carries
  on. The failure arrives later, somewhere else entirely:

  ```text
  Traceback (most recent call last):
    File "wrong.py", line 29, in <module>
      print(a)
      ~~~~~^^
    File "wrong.py", line 23, in __str__
      return f"{self.holder}: {format_usd(self._balance_cents)}"
                               ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
    File "wrong.py", line 6, in format_usd
      return f"${dollars:,}.{remainder:02d}"
                            ^^^^^^^^^^^^^^^
  ValueError: Unknown format code 'd' for object of type 'float'
  ```

  Look at the distance. The mistake was in `deposit`. The traceback names
  `__str__` and a formatting code, neither of which has anything to do with
  deposits, and it may not arrive until the next time somebody prints the
  account — which could be a completely different run. That distance is what
  an unenforced rule costs you. `cents: int` is documentation; it does not
  stop anything. `isinstance` does.

- **`Declined: amount must be positive, got -100` appears where the
  insufficient-funds message should be.** `InsufficientFunds` subclasses
  `ValueError`, so a broad `except ValueError` catches it too. When you write
  your own handlers, order them specific-first: `except InsufficientFunds`
  above `except ValueError`.

## Under the hood

<details>
<summary>Under the hood — why __repr__ is for you and __str__ is for the reader</summary>

Both are dunder methods that return a string, and beginners reasonably ask
why Python needs two. The answer is that they answer different questions, and
the standard library documents the difference in one word each:
`__repr__` should be **unambiguous**, `__str__` should be **readable**.

Who calls which:

| you write | Python calls |
|---|---|
| `print(account)` | `__str__` |
| `str(account)` | `__str__` |
| `f"{account}"` | `__str__` |
| `repr(account)` | `__repr__` |
| `f"{account!r}"` | `__repr__` |
| `account` at the REPL | `__repr__` |
| `print([account])` | `__repr__` on each item |

That last row surprises people, and it is the practical reason `__repr__`
matters most. A container's `__str__` calls `repr` on its contents, not
`str`. So a class with a beautiful `__str__` and no `__repr__` prints
perfectly on its own and turns into gibberish the moment you put it in a
list:

```text
>>> print(account)
Ravi Menon: $25.50
>>> print([account, account])
[BankAccount(holder='Ravi Menon', balance_cents=2550), BankAccount(...)]
```

Why does the container do that? Because a list is a developer-facing thing.
Joining the `str` of every element would produce a display where you could
not tell `["1", 2]` from `[1, "2"]`. `repr` keeps the quotes, so the display
stays honest.

The fallback rules are asymmetric, and asymmetric in a useful direction:

- Define **neither** and you inherit `object.__repr__`, which gives
  `<__main__.BankAccount object at 0x000001DC80211440>`. Both spellings show
  that.
- Define **only `__repr__`** and `str()` falls back to it. You get a good
  answer everywhere.
- Define **only `__str__`** and `repr()` does *not* fall back to it. You get
  the memory address in every list, every dict, every debugger.

So the rule of thumb is: **if you write only one, write `__repr__`.** Add
`__str__` when there is a genuinely different thing a non-developer should
see — which there is here, because a teller does not want to read `12550`.

The best `__repr__` looks like the code that would rebuild the object:

```text
>>> repr(account)
"BankAccount(holder='Ravi Menon', balance_cents=2550)"
```

That is not always achievable — this one is not literally constructible, since
the balance arrives through `deposit` — but it is the target, and `!r` is what
gets you there. `!r` inside an f-string asks a value for *its* repr, which is
why the holder's name comes back with quotes on it. Without them, a name with
a trailing space, or a name that is secretly the number `12550`, looks exactly
like a name that is not.

One more asymmetry worth knowing: `__format__`. `f"{account}"` calls
`__str__` only because the default `__format__` inherited from `object`
delegates to it. Define `__format__` yourself and you can support
`f"{account:cents}"` or `f"{account:usd}"` — which is how `datetime` supports
`f"{when:%Y-%m-%d}"`. You will not need it this week, but that is where the
format spec after the colon actually goes.

</details>

<details>
<summary>Under the hood — decimal.Decimal, the other correct answer to money</summary>

Integer cents is not the only right answer. `decimal.Decimal` is the other
one, and it is correct **only if you build every value from a string**.

```text
>>> from decimal import Decimal
>>> Decimal("0.10")
Decimal('0.10')
>>> Decimal(0.10)
Decimal('0.1000000000000000055511151231257827021181583404541015625')
```

`Decimal("0.10")` is exactly one tenth. `Decimal(0.10)` takes the binary
decimal's error and carries it out to fifty-five places. The type did not fix
the number; it faithfully recorded a number that was already wrong. Feed it
strings and it behaves:

```text
>>> total = Decimal("0")
>>> for _ in range(10):
...     total += Decimal("0.70")
...
>>> total
Decimal('7.00')
>>> Decimal("4.35") * 100
Decimal('435.00')
```

Both of the failures from the Constraints section, gone.

`Decimal` also refuses to mix with plain decimals, which is the whole point
of the type:

```text
>>> Decimal("1.10") * 1.05
TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'
```

That refusal is `decimal` declining to let binary error back in through the
side door. It is the same instinct as `deposit` refusing a float: make the
wrong thing impossible rather than asking everyone to remember.

When you do need to land on a whole cent, say the rule out loud rather than
letting the default decide:

```text
>>> from decimal import Decimal, ROUND_HALF_EVEN
>>> Decimal("2.465").quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
Decimal('2.46')
>>> Decimal("2.475").quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
Decimal('2.48')
```

Read those two together. On an exact half, `ROUND_HALF_EVEN` goes to the even
cent — down to `2.46` in the first, up to `2.48` in the second. Always
rounding a half up hands the customer a fraction of a cent every time; always
rounding down keeps it. Going to the even one means the halves cancel instead
of piling up on one side. Over a few million interest runs that is a real
number on somebody's books, which is why real banks write the rule down.
Python's built-in `round()` uses the same rule, and homework problem 1 leans
on exactly that.

So: which do you reach for?

- **Integer cents** when every amount is a whole cent — a plain ledger, a
  cart total, a payment API. Simpler, exactly as correct, and impossible to
  get subtly wrong.
- **`Decimal`** when you need fractions of a cent along the way, or a
  mandated rounding rule — interest, tax, currency conversion, anything with
  a percentage in it.

What you never do is store money in a plain float.

</details>

## Acceptance checklist

- [ ] `python exercise-05-bank-account.py` runs with no traceback.
- [ ] All ten output lines match exactly.
- [ ] No decimal appears anywhere in the balance, the amounts, or the
      history.
- [ ] A declined withdrawal changes neither `balance_cents` nor `history`.
- [ ] `history` returns a copy that cannot corrupt the ledger.
- [ ] `repr(account)` and `str(account)` produce different strings, and the
      repr shows the integer cents.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 5: bank account`.

## Stretch

- `account.deposit(True)` currently adds one cent, because `bool` is a
  subclass of `int` and `isinstance(True, int)` is `True`. Reject it with
  `if isinstance(cents, bool) or not isinstance(cents, int)`, then write one
  comment explaining why the `bool` test has to come first.
- Add `transfer_to(self, other: "BankAccount", cents: int) -> None` that
  withdraws from `self` and deposits into `other`. Make sure a failed
  withdrawal moves nothing — the withdraw must complete before the deposit
  starts.
- Add a `statement()` method returning a multi-line string: one line per
  history entry using `format_usd`, then a total. Return the string rather
  than printing it, so you can assert on it later.
- Rebuild the class with `decimal.Decimal` instead of cents, following the
  rules in the second Under the hood block, and write a short note comparing
  the two. Then add interest at 1.5% a year and decide — and document —
  whether a fractional cent rounds up, down, or to even, and who benefits
  from your choice. Homework problem 1 is that question with the answer
  already picked.

That is Week 7's exercises. Next come the two longer problems in
[Week 7 Challenges](../challenges/README.md), where you build a full deck of
cards and an employee hierarchy from scratch.
