# Week 3 — Homework

Six practice problems. Solve each one in its own `.py` file inside a
`homework/` folder of your own repository. Naming suggestion:
`homework-01-leap-year.py`, `homework-02-count-vowels.py`, and so on.

Each problem includes a short spec, a few sample inputs and outputs,
and an "extension" idea if you finish quickly.

You can assume input is keyboard input via `input(...)` unless the
problem says otherwise.

---

## 1. Leap year checker

Write a program that asks for a year and prints `"<year> is a leap
year."` or `"<year> is not a leap year."`.

The Gregorian rule: a year is a leap year if it is divisible by 4,
**except** centuries (years divisible by 100) which are **only** leap
years if also divisible by 400.

| Year | Leap? |
|------|-------|
| 2024 | yes (divisible by 4, not 100) |
| 2023 | no  |
| 1900 | no (divisible by 100 but not 400) |
| 2000 | yes (divisible by 400) |

**Hints**

- Combine `and` / `or` carefully — parentheses help readability.
- Or, write three guard clauses in order: divisible by 400 → leap;
  divisible by 100 → not leap; divisible by 4 → leap; else not leap.

**Extension**: ask for a range of years and print only the leap years
in that range.

---

## 2. Count vowels in a string

Ask the user for a sentence and print how many vowels it contains.
Vowels are `a, e, i, o, u`, case-insensitive.

```text
Enter a sentence: Hello, World!
That sentence has 3 vowel(s).
```

**Hints**

- `text.lower()` makes case handling trivial.
- The counting pattern from Lecture 3.
- For a one-liner once you have it working: `sum(c in 'aeiou' for c in
  text.lower())`.

**Extension**: also report which vowel appeared most often.

---

## 3. Reverse a number

Ask the user for a non-negative integer and print the integer formed by
reversing its digits. **Do not** convert the input to a string — use
the math approach with `// 10` and `% 10` to build it digit by digit.

```text
Enter a non-negative integer: 12345
Reversed: 54321

Enter a non-negative integer: 1200
Reversed: 21
```

**Hints**

- `digit = n % 10` peels off the last digit.
- `n = n // 10` removes that digit.
- Use a `while n > 0:` loop and an accumulator: `result = result * 10
  + digit`.

**Extension**: after you have the math version working, write a
one-line string version (`int(str(n)[::-1])`) and confirm they agree.

---

## 4. Sum of digits

Ask the user for a non-negative integer and print the sum of its
digits.

```text
Enter a non-negative integer: 12345
Sum of digits: 15

Enter a non-negative integer: 0
Sum of digits: 0
```

**Hints**

- Same `% 10` / `// 10` shape as the previous problem, but accumulate
  the sum instead of building a new number.

**Extension**: keep summing the digits of the result until you get a
single-digit number (the "digital root"). For example, `12345` → `15`
→ `6`.

---

## 5. Fibonacci numbers up to N

Ask the user for a positive integer `N`. Print every Fibonacci number
that is less than or equal to `N`, one per line.

Recall: the sequence starts `0, 1, 1, 2, 3, 5, 8, 13, ...` where each
term is the sum of the previous two.

```text
Enter N: 50
0
1
1
2
3
5
8
13
21
34
```

**Hints**

- Maintain two variables `a, b = 0, 1`. While `a <= N`, print `a` then
  update with `a, b = b, a + b`. Tuple assignment lets you swap in one
  step.

**Extension**: print only the *count* of Fibonacci numbers `<= N`
instead of the numbers themselves.

---

## 6. Simple ATM menu

Build a very small ATM simulator. Start with a balance of `100.00`. In
a loop, show the menu:

```text
1) Deposit
2) Withdraw
3) Show balance
4) Quit
Choose 1-4:
```

- **Deposit**: ask for an amount, add it to the balance. Reject
  negative or zero amounts.
- **Withdraw**: ask for an amount, subtract it from the balance, but
  refuse if the result would go below zero.
- **Show balance**: print the current balance with two decimal places.
- **Quit**: leave the loop and print "Goodbye.".

Invalid menu choices print "Please choose 1, 2, 3, or 4." and reshow
the menu.

**Hints**

- `while True:` + `break` on quit.
- Use `float()` for amounts and check the value with guard clauses.
- Format with `f"{balance:,.2f}"` for nice thousand-separated output.

**Extension**: add a transaction history list and a "5) Print history"
option that prints every deposit and withdrawal in order. (List of
tuples will do for now; we will see dataclasses much later.)

---

## Submitting your work

If you are using Git (see Week 1), commit each problem as you finish:

```bash
git add homework/homework-01-leap-year.py
git commit -m "Week 3 homework: leap year checker"
```

Each homework file should start with a short docstring describing what
it does, just like the exercise skeletons. Good docstrings now become
muscle memory for Week 4.
