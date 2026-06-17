# Mini-Project — Unit Converter CLI

Your Week 2 mini-project is a menu-driven unit converter that runs in a
terminal. It will convert between three pairs of units:

1. **Celsius ↔ Fahrenheit** (temperature)
2. **Kilometers ↔ Miles** (distance)
3. **USD ↔ EUR** (currency, with a hardcoded exchange rate)

You'll exercise everything you've learned this week: variables, types,
casting, arithmetic, comparisons, `input()`, error handling, f-strings
with format specs, and type hints. You'll *not* yet use loops or `if`
chains in a sophisticated way — those come next week. That's fine; this
project is genuinely small and the constraint keeps the code simple.

## Final User Experience

When the user runs ``python unit_converter.py``, this is the kind of
session they should see:

```text
================================
   Code Crunch Unit Converter
================================

Categories:
  1) Temperature (C / F)
  2) Distance    (km / mi)
  3) Currency    (USD / EUR)

Pick a category (1-3): 1

Direction:
  a) Celsius     -> Fahrenheit
  b) Fahrenheit  -> Celsius

Choose direction (a/b): a

Value in Celsius: 100

Result: 100.00 C = 212.00 F

Thanks for using the converter!
```

A second session, for currency:

```text
================================
   Code Crunch Unit Converter
================================

Categories:
  1) Temperature (C / F)
  2) Distance    (km / mi)
  3) Currency    (USD / EUR)

Pick a category (1-3): 3

Direction:
  a) USD -> EUR
  b) EUR -> USD

Choose direction (a/b): a

Value in USD: 250

Result: $250.00 USD = €228.50 EUR  (rate: 1 USD = 0.9140 EUR)

Thanks for using the converter!
```

## Requirements

### Functional

- The program must run once and exit cleanly. (Repeating in a loop is a
  stretch goal.)
- It must support all three categories listed above and both
  directions for each.
- It must accept the category as ``1``, ``2``, or ``3`` and the
  direction as ``a`` or ``b`` (case-insensitive — accept ``A`` too).
- It must validate the numeric value, printing a clear error message
  and exiting if the user types something that isn't a number.
- It must format the result with **two decimal places** for
  temperature and currency. Distance should also use two decimals.
- It must include the unit symbols/labels in the output as shown
  above.

### Technical

- Define the constants at the top of the file:

  ```python
  USD_TO_EUR: float = 0.9140  # hardcoded; see note in stretch goals
  KM_PER_MILE: float = 1.609344
  ```

- Write a function for each conversion:

  ```python
  def c_to_f(c: float) -> float: ...
  def f_to_c(f: float) -> float: ...
  def km_to_mi(km: float) -> float: ...
  def mi_to_km(mi: float) -> float: ...
  def usd_to_eur(usd: float) -> float: ...
  def eur_to_usd(eur: float) -> float: ...
  ```

- Use type hints on every function.
- Use f-strings with ``:.2f`` (or ``:,.2f`` for currency) for output.
- Put the program flow inside a ``main()`` function and guard the
  entry with the ``if __name__ == "__main__":`` idiom.
- Provide a module docstring and a docstring on every function.

### Constraints

- **No imports** from third-party packages. (Standard library is fine
  if you really want it; the spec only needs builtins.)
- **No loops** beyond an outermost ``while True:`` if you choose to add
  the "convert again?" stretch goal.
- **No** ``if/elif`` ladders of more than ~3 branches — Week 3 covers
  cleaner control flow.

## Suggested Build Order

1. Open ``mini-project/starter.py``. Read the docstring and stubs.
2. Implement the six conversion functions. Test each in the REPL by
   importing the file. Spend ten minutes here; don't move on with
   wrong math.
3. Implement ``main()`` step by step:
   - Print the banner.
   - Print the category menu and read the choice.
   - Print the direction menu (the specific labels depend on the
     category) and read the choice.
   - Prompt for the numeric value, cast it with ``float()`` inside
     ``try/except``.
   - Call the right conversion function.
   - Print the formatted result.
4. Test all six paths by hand.
5. Commit and push.

## Rubric (40 Points Total)

| Criterion | Points |
|-----------|-------:|
| Six conversion functions implemented correctly | 12 |
| Each function has a docstring and type hints | 4 |
| Banner and menus match the specified layout closely | 4 |
| Reads category, direction, and value from `input()` | 4 |
| Validates non-numeric input gracefully | 4 |
| Output is formatted with two decimals and correct unit labels | 6 |
| Constants used for exchange rate and km-per-mile | 2 |
| Code organised into `main()` with `if __name__ == "__main__":` | 2 |
| Clean, readable code; PEP 8 names | 2 |
| **Total** | **40** |

## Stretch Goals

In rough order of difficulty:

- **Loop until quit**: wrap the main flow in ``while True:`` and add a
  fourth menu option ``q) Quit``. Keep handling one conversion at a
  time.
- **Live exchange rate**: read the rate from an environment variable
  ``USD_TO_EUR`` if it's set, falling back to the constant. (Week 12
  covers fetching it from an API; for now an env var is plenty.)
- **More categories**: add kilograms ↔ pounds and 24h ↔ 12h time.
- **Pretty banner**: paint the banner with ANSI escape codes (e.g.
  ``"\033[1;36m"`` and ``"\033[0m"``).
- **Type-checked**: install ``mypy`` and make the file pass with
  ``--strict``.
- **Unit tested**: write a few ``assert`` statements at the bottom of
  the file that exercise each conversion against known values
  (``assert c_to_f(0) == 32``, ``assert round(km_to_mi(1.609344), 4)
  == 1.0``). Pytest comes in Week 11 — for now, assertions are great.

## How to Submit

Save your finished program as ``mini-project/unit_converter.py`` in
your Week 2 repository. Commit, push, and link it from your repo
README. A short demo recording (even a couple of screenshots) is
worth more than your code on its own — get used to showing what you
built.
