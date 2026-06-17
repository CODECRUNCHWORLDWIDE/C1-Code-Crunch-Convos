# Week 2 — Homework

Six problems to work through this week. The early ones reinforce the
lectures; the later ones stretch a little. Save each solution as a
runnable ``.py`` file inside a ``homework/`` directory in your Week 2
repository.

Naming convention: ``homework-01-simple-interest.py``,
``homework-02-bmi.py``, and so on.

Each problem includes inputs, the formula or rule, and example
output. Match the output format exactly when one is shown — output
formatting is a real skill.

---

## Problem 1 — Simple Interest Calculator

The formula for simple interest is:

```text
interest = principal * (rate / 100) * years
```

Prompt the user for:

- ``Principal in dollars`` (float)
- ``Annual interest rate in percent`` (float, e.g. ``5`` for 5%)
- ``Number of years`` (int)

Print:

```text
Principal : $    1,000.00
Rate      :        5.00%
Years     :            3
Interest  : $      150.00
Total     : $    1,150.00
```

Hints:

- Right-align numeric fields to width 11.
- Use ``,.2f`` for the dollar amounts, ``.2f`` (with ``%``) for the
  rate, and a plain integer for the years.

---

## Problem 2 — BMI Calculator

Body Mass Index is computed as:

```text
BMI = weight_kg / (height_m ** 2)
```

Prompt for weight in kilograms (float) and height in meters (float).
Print the BMI rounded to **one** decimal place, followed by a category
on a separate line:

- ``Underweight`` if BMI is less than 18.5.
- ``Normal``      if BMI is at least 18.5 and less than 25.
- ``Overweight``  if BMI is at least 25 and less than 30.
- ``Obese``       if BMI is 30 or above.

Important constraint: solve this **without** an ``if`` statement. (You
haven't learned `if` yet.) Use the next problem's trick: build a
string with the comparisons that evaluate to ``True``/``False``, and
join them. Or, simpler, just print all four category labels next to
their boolean and let the user read it:

```text
BMI: 23.1
Underweight : False
Normal      : True
Overweight  : False
Obese       : False
```

The boolean-listing approach is what we expect for Week 2. After
Week 3 you can revisit this and clean it up with ``if/elif``.

---

## Problem 3 — Word and Character Counter

Read a single line of text from the user. Print:

- The total number of characters in the line (including spaces and
  punctuation) — use ``len(text)``.
- The number of characters with whitespace removed — use
  ``text.replace(" ", "")`` and then ``len()``.
- The number of words — use ``text.split()`` and ``len()``.
- The line with all words uppercased — use ``.upper()``.

Example session:

```text
Enter a line: hello there friend
Characters       : 18
Non-space chars  : 16
Words            : 3
Uppercase        : HELLO THERE FRIEND
```

**No loops allowed.** Everything here should be one method call per
statistic.

---

## Problem 4 — Grade Letter Assigner (No `if`)

You are given a percentage score from 0 to 100 (a float, read from
input). Print the corresponding letter grade based on this table:

| Score range | Letter |
|-------------|--------|
| 90–100      | A      |
| 80–89.99    | B      |
| 70–79.99    | C      |
| 60–69.99    | D      |
| Below 60    | F      |

You **may not** use `if`/`elif` (you haven't learned them yet). Solve
it using comparison operators, booleans, and arithmetic only.

Hints:

- A boolean is also an integer: `True == 1`, `False == 0`.
- ``score >= 90`` is `True` or `False`. Multiply by 1.
- One workable approach:

  ```python
  index = (score >= 60) + (score >= 70) + (score >= 80) + (score >= 90)
  letter = "FDCBA"[index]
  ```

  Walk through this on paper for `score = 75`. Convince yourself it
  prints ``C``.

Example sessions:

```text
Enter your score: 92
Grade: A

Enter your score: 73
Grade: C

Enter your score: 41
Grade: F
```

---

## Problem 5 — Compound Interest

Same shape as Problem 1, but using **compound** interest, which grows
faster because it earns interest on previous interest:

```text
final_amount = principal * (1 + rate / 100) ** years
```

Prompt for principal (float), annual rate (float, in percent), and
years (int). Print:

```text
Principal     : $   1,000.00
Rate          :        5.00%
Years         :            3
Final amount  : $   1,157.63
Total interest: $     157.63
```

Compare your result with Problem 1's simple-interest figure. The
difference is small over short horizons, dramatic over long ones.

---

## Problem 6 — Distance & Speed Report

Prompt the user for:

- ``Distance in kilometers`` (float).
- ``Time in hours`` (float).

Compute and print a small report:

```text
--- Trip Report ---
Distance : 250.0 km
Time     :   3.5 hours
Speed    :  71.43 km/h
In miles : 155.34 mi
At MPH   :  44.38 mph
```

Conversion factors (hardcode them as named constants):

```python
KM_PER_MILE: float = 1.609344
```

Therefore ``miles = kilometers / KM_PER_MILE``. Validate that ``time``
is greater than zero; if not, print ``Error: time must be positive.``
and stop.

This problem is also a warm-up for the mini-project, so put real
effort into the output formatting.

---

## How to Submit

When you've done all six, commit them to the Week 2 directory of your
repository:

```text
week-02/
  homework/
    homework-01-simple-interest.py
    homework-02-bmi.py
    homework-03-word-counter.py
    homework-04-grade-letter.py
    homework-05-compound-interest.py
    homework-06-distance-speed.py
```

A clean commit message like ``"week 2 homework"`` is fine.
