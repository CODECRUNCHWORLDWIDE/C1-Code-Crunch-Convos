# Homework Problem 4 — Sum of Digits

> **Topic:** the accumulator pattern, and noticing that two loops with the same traversal can differ only in what they do per item
> **Lecture:** [03 — Loop Patterns You Will Use Forever](../lecture-notes/03-loop-patterns.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** it is problem 3 with one operator removed, and that is the lesson. The conveyor belt that hands you digits is a separate idea from what you do with each digit as it arrives. Once you can see those two parts as separate, you can swap either one without disturbing the other — which is what makes a pattern a pattern instead of a program you memorised.

## The Brief

Ask for a whole number that is zero or bigger, then print the total you
get by adding its digits together.

```text
Enter a non-negative integer: 12345
Sum of digits: 15

Enter a non-negative integer: 0
Sum of digits: 0
```

`1 + 2 + 3 + 4 + 5` is `15`. That is the whole specification.

You already know how to get at the digits, because you did it in problem
3: `% 10` hands you the last one, `// 10` throws it away, and a `while`
loop keeps going until there is nothing left. The only thing that changes
is what you do with each digit when it arrives.

In problem 3 you had to be careful about *when* each digit turned up,
because a reversed number depends entirely on the order. Here you do not.
Addition does not care what order you add things in, so a right-to-left
walk gives the same total as a left-to-right one, and the accumulator
collapses from `acc = acc * 10 + digit` to a plain `acc += digit`.

That simplification is worth pausing on. Whenever an update looks
complicated, ask whether the operation you are doing actually cares about
order. Very often it does not, and the complexity was imaginary.

## Starter

Save this as `homework-04-sum-digits.py` and fill in the `TODO`s. It runs
as pasted and always reports zero:

```python
"""Homework 4 - Sum the digits of a non-negative integer."""

DIGITS = "0123456789"

while True:
    raw = input("Enter a non-negative integer: ").strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number:
        number = int(raw)
        break
    print("Please type a non-negative whole number, like 12345.")

remaining = number
digit_sum = 0

while remaining > 0:
    # TODO: add the last digit of remaining to digit_sum
    # TODO: drop the last digit from remaining
    break                            # DELETE this line once the TODOs are done

print(f"Sum of digits: {digit_sum}")
```

You have now typed that six-line reading loop three times. It is the same
six lines every time, and by now it should be annoying you. Hold on to
that annoyance — it is precisely the feeling Week 4 exists to fix, and a
function is the fix.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/homework/problem-04-sum-of-digits.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks with the prompt `Enter a non-negative integer: `.
2. It prints `Sum of digits: <n>` on one line.
3. `12345` gives `15`.
4. `0` gives `0`, with no special case.
5. `999` gives `27`.
6. Anything that is not a run of digits produces a message and another
   question, never a crash.

## Constraints

- **Arithmetic, not `str()`.** Same rule as problem 3, and for the same
  reason: `% 10` and `// 10` are the tools being taught. The one-line
  `sum(int(c) for c in str(n))` is a good cross-check and it is under
  **Stretch**.
- **No functions.** `def` is Week 4.
- **No `try` / `except`.** Exceptions are Week 6.
- **`while remaining > 0`, not `>= 0`.** The `>=` version is an infinite
  loop with a correct answer already in hand, which is a strange and
  memorable way to fail. Common bugs to catch explains it.
- **Add the digit, not the number.** `digit_sum += remaining % 10`, not
  `digit_sum += remaining`.

## Expected output

The downloadable file below types `12345` on your behalf when nobody is
at the keyboard, so the run is the same every time:

```text
$ python problem-04-sum-of-digits.py
Enter a non-negative integer: 12345
Sum of digits: 15
```

Run it in your own terminal and it asks you instead. Fed the brief's
other sample and a third case from Git Bash, one run each:

```bash
for n in 12345 0 999; do printf "$n\n" | python -u problem-04-sum-of-digits.py 2>&1; done
```

```text
Enter a non-negative integer: Sum of digits: 15
Enter a non-negative integer: Sum of digits: 0
Enter a non-negative integer: Sum of digits: 27
```

The prompt and the answer share a line because piped input is never
echoed back.

## Steps

1. Activate your Week 3 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `homework-04-sum-digits.py`.
3. Open your problem 3 answer beside it. Copy the loop across, then
   delete the `* 10`. That is the entire change, and doing it as a
   deletion rather than a rewrite is what makes the point stick.
4. Delete the `break`. Run `12345`. You want `15`.
5. Run `0`. You want `0`, and you should not have written anything
   special to get it.
6. Run `999`. You want `27`. If you get something in the thousands, read
   the first bug below.
7. Cross-check against the one-liner under **Stretch** on all three
   inputs.
8. Commit: `git add homework/homework-04-sum-digits.py` then
   `git commit -m "Week 3 homework: sum of digits"`.

## The Solution

```python
"""Sum the digits of a non-negative integer.

Week 3 homework, problem 4, Code Crunch Convos.

The same conveyor belt as problem 3 - ``% 10`` to read the last digit,
``// 10`` to drop it - with a plainer accumulator: add the digit instead
of shifting the total left first.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-04-sum-digits.py``, write
``input("Enter a non-negative integer: ")`` instead.

Questions go to the error stream and the total goes to the normal output
stream, so ``python homework-04-sum-digits.py > total.txt`` saves the
answer and not the question.
"""

import sys

DIGITS: str = "0123456789"
DEMO_NUMBER: str = "12345"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


# Read a number, refusing anything that is not a whole number.
while True:
    raw = ask("Enter a non-negative integer: ", DEMO_NUMBER).strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number:
        number = int(raw)
        break
    print("Please type a non-negative whole number, like 12345.")

remaining = number
digit_sum = 0

while remaining > 0:
    digit_sum += remaining % 10
    remaining = remaining // 10

print(f"Sum of digits: {digit_sum}")
```

**Why it works.**

**Same belt, different accumulator.** Put the two loops side by side and
the whole lesson is in one row of the table:

| | Reverse (problem 3) | Sum of digits (this one) |
|---|---|---|
| Start the accumulator at | `0` | `0` |
| Per digit | `acc = acc * 10 + digit` | `acc = acc + digit` |
| Why | shift left, then place the digit in the units column | order is irrelevant, so just add |
| Get `remaining` closer to done | `remaining = remaining // 10` | `remaining = remaining // 10` |

The traversal is identical. The thing you do per item is not. Every loop
pattern in [Lecture 3](../lecture-notes/03-loop-patterns.md) — counting,
accumulating, max and min, filtering, searching — is a different "thing
you do per item" bolted onto the same handful of traversals.

**`digit_sum += remaining % 10` fuses two lines into one.** Problem 3
needed `digit` as a named variable because it appeared twice in the same
expression. Here it appears once, so naming it is optional. Name it
anyway if that reads better to you — clarity beats brevity at this stage,
and the digital-root version under **Stretch** keeps the two-line form
for exactly that reason.

**Zero falls out for free again.** `while remaining > 0` is false
immediately, the body never runs, `digit_sum` is still `0`, and the
program prints the brief's second sample without a line of special-case
code. That is the second time this week a condition-first `while` has
handled the empty case by itself, and it is not a coincidence: choosing
the condition so that "nothing to do" means "the loop does not run" is
one of the reliable ways to avoid special cases.

**This loop runs once per digit, not once per unit.** `999999999` takes
nine turns, not a billion, because each turn divides the number by ten.
The number of turns is the number of digits — roughly `log10(n)` — which
is why the technique stays fast on numbers far too large to count up to.
Python's integers have no fixed size, so it keeps working past the point
where the same code in C or Java would overflow and start producing
nonsense.

**`ask()` is the one piece the brief did not ask for**, and the one `def`
in the file. `input()` with nothing to read raises `EOFError`, and
`ask()` catches that and supplies the example number so the download can
be run automatically. It also puts the prompt on the **error** stream
rather than the output stream, so
`python homework-04-sum-digits.py > total.txt` saves the answer and not
the question. Your own file calls
`input("Enter a non-negative integer: ")` directly.

## Download and run

Download [problem-04-sum-of-digits-solution.py](./problem-04-sum-of-digits-solution.py)
and run it:

```bash
python problem-04-sum-of-digits-solution.py
```

Run from a terminal, it asks for a number. Run by a script, or with its
input redirected, it uses `12345` instead of hanging. Save your own copy
as `homework-04-sum-digits.py` in your homework folder, and commit that
one.

## Common bugs to catch

- **`digit_sum += remaining` instead of `remaining % 10`.** You add the
  whole remaining number every turn, so `12345` gives
  `12345 + 1234 + 123 + 12 + 1`:

  ```text
  Sum of digits: 13715
  ```

  No error. The sanity check that catches it instantly: a digit sum can
  never be bigger than `9 × (number of digits)`, so five digits can never
  total more than 45. If your answer is suspiciously large, this is why.
- **`while remaining >= 0`.** An off-by-one that turns into an infinite
  loop. Once `remaining` reaches `0`, `0 % 10` is `0` and `0 // 10` is
  `0`, so nothing changes and the condition stays true forever. The
  strange part is that `digit_sum` is already correct — the program has
  finished the work and simply never stops to say so. Use `> 0`.
- **`remaining = remaining % 10` instead of `// 10`.** Now `remaining`
  becomes the last digit rather than losing it. `12345` becomes `5`, then
  `5` again, then `5` forever, and `digit_sum` climbs by five every turn.
  Another infinite loop, and one where the answer is also wrong.
- **`digit_sum = remaining % 10`** with `=` instead of `+=`. Each turn
  overwrites the total, so you end up with the *first* digit of the
  number and nothing else. `12345` gives `1`.
- **Reaching for `str()` and `int()` per character.**
  `sum(int(c) for c in str(n))` is a fine one-liner and it agrees with
  this answer on every input. It is out of bounds here for the same
  reason as in problem 3: learn the arithmetic first, then use the
  one-liner as a second opinion.

## Under the hood

<details>
<summary>Under the hood — why a digit sum tells you the remainder after dividing by 9</summary>

Add the digits of `12345` and you get `15`. Add the digits of `15` and
you get `6`. Now divide `12345` by `9`:

```bash
python -c "print(12345 % 9, 15 % 9, 6 % 9)"
```

```text
6 6 6
```

All three agree, and that is not luck. **A number and the sum of its
digits always leave the same remainder when divided by 9.**

Here is why, and it takes one line. In base 10, a number is
`d0 + d1*10 + d2*100 + ...`. Every power of ten is one more than a
multiple of nine: `10 = 9 + 1`, `100 = 99 + 1`, `1000 = 999 + 1`. So each
`dk * 10^k` is `dk * (a multiple of 9) + dk`. Throw away all the multiples
of nine — which is exactly what taking the remainder does — and what is
left is `d0 + d1 + d2 + ...`, the digit sum.

That gives you the closed form for the **digital root**, the single digit
you reach by summing repeatedly. For any positive `n`:

```text
digital_root(n) == 1 + (n - 1) % 9
```

```bash
python -c "print(1 + (12345 - 1) % 9, 1 + (999999999 - 1) % 9)"
```

```text
6 9
```

The `- 1` and `+ 1` shift the answer from the range 0–8 into 1–9, because
a digital root of 9 shows up as a remainder of 0.

Accountants used this for centuries under the name **casting out
nines**. Add a long column of figures, take the digital root of your
answer, take the digital root of the digital roots of the inputs, and
compare. If they disagree, you made an arithmetic mistake. If they agree,
you probably did not — it catches eight errors in nine, and it is free.
The same trick is a checksum digit on an ISBN, on a credit card (that one
uses a weighted variant called the Luhn algorithm), and on a VIN.

What it cannot catch: any mistake that changes your answer by a multiple
of nine, which includes the very common one of swapping two digits.
`54` and `45` have the same digital root. That is the one-in-nine it
misses, and it is why modern checksums use larger moduli.

</details>

<details>
<summary>Under the hood — the same problem four ways, and which one to reach for</summary>

Four correct answers to "sum the digits of `n`", in the order you will
meet them across this course:

```bash
python -c "
n = 12345

total = 0
remaining = n
while remaining > 0:
    total += remaining % 10
    remaining //= 10
print('arithmetic       ', total)

print('per-character int', sum(int(c) for c in str(n)))
print('map              ', sum(map(int, str(n))))
print('closed form (root)', 1 + (n - 1) % 9)
"
```

```text
arithmetic        15
per-character int 15
map               15
closed form (root) 6
```

Three of those are the digit sum. The fourth is the *digital root*, which
is a different question — printed here so you can see that they are not
interchangeable, however often people muddle them.

**The arithmetic version** allocates nothing and works in any base. It is
the one to reach for when the number is huge, when you are on a
microcontroller, or when the base is not ten.

**`sum(int(c) for c in str(n))`** is the one you will write in real
Python most of the time, because it reads like its own description. It
does allocate: one string for the number, one small `int` per character.
It is also the only one of the three that stops working on a truly
gigantic integer, because Python 3.11 and later refuse to render integers
beyond 4300 digits as strings by default.

**`sum(map(int, str(n)))`** is the same idea with the loop pushed into C.
`map` applies `int` to each character without running Python bytecode per
item, so on long strings it is measurably quicker. `map` is Week 5
material; it is here so that when you meet it you recognise it as the
same program.

**The closed form** answers a different question in constant time — no
loop at all, whatever the size of `n`. When a problem has a closed form,
finding it beats optimising the loop, every time. The catch is that
closed forms are rare, and reaching for one when it does not exist is how
people talk themselves into wrong answers.

Ranking by speed is not the point here. The point is that "sum the
digits" is one specification with four implementations that differ in
what they allocate, what they assume about the base, and what they do
when the input gets extreme. Choosing between them is engineering.
Knowing only one of them is not.

</details>

## Acceptance checklist

- [ ] Running the file asks `Enter a non-negative integer: ` and waits.
- [ ] `12345` prints `Sum of digits: 15`.
- [ ] `0` prints `Sum of digits: 0`, with no special case in your code.
- [ ] `999` prints `Sum of digits: 27`.
- [ ] Typing a word prints the retry message and asks again.
- [ ] The loop condition is `> 0`.
- [ ] The accumulator adds `remaining % 10`, not `remaining`.
- [ ] There is no `str()` in your answer.
- [ ] There is no `def` and no `try` in your own file.
- [ ] Committed with a message like `Week 3 homework: sum of digits`.

## Stretch

- **Cross-check against the string version.** It must agree on every
  input:

  ```bash
  python -c "
  for n in (12345, 0, 999, 100000):
      print(n, '->', sum(int(c) for c in str(n)))
  "
  ```

  ```text
  12345 -> 15
  0 -> 0
  999 -> 27
  100000 -> 1
  ```
- **The digital root.** Keep summing the digits of the result until only
  one digit is left: `12345` → `15` → `6`. The honest way to build this
  is to wrap the loop you already have in a second loop, so the inner
  `while` is problem 4 word for word and the outer one re-runs it.
  `while current >= 10` is the exact test for "more than one digit",
  which reads better than `> 9` even though the two are identical.

  ```python
  current = number
  print(current, end="")

  while current >= 10:
      remaining = current
      digit_sum = 0
      while remaining > 0:
          digit_sum += remaining % 10
          remaining = remaining // 10
      current = digit_sum
      print(f" -> {current}", end="")

  print()
  print(f"Digital root: {current}")
  ```

  `end=""` replaces the newline `print` normally adds, so the arrows
  build up on one line; the bare `print()` afterwards supplies the
  newline the chain has been missing. That is the same trick
  [Lecture 2 §11](../lecture-notes/02-loops.md) uses to print a grid row.

  Fed `12345`, `0` and `999999999` it prints:

  ```text
  Enter a non-negative integer: 12345 -> 15 -> 6
  Digital root: 6
  Enter a non-negative integer: 0
  Digital root: 0
  Enter a non-negative integer: 999999999 -> 81 -> 9
  Digital root: 9
  ```

  Note that `0` produces no arrows at all — it is already a single digit,
  so the outer loop never runs. Check the two-arrow case against the
  closed form in the first **Under the hood** block: `1 + (12345 - 1) % 9`
  is `6`, and the loop agrees.
- **Prove the outer loop terminates.** It is not obvious that summing
  digits always shrinks a number. Write `n` as `10 * q + r`, where `r` is
  the last digit and `q >= 1` is everything above it. The digit sum of
  `n` is `digit_sum(q) + r`, and `digit_sum(q) <= q`, so the whole thing
  is at most `q + r` — which for `q >= 1` is at least nine less than
  `10 * q + r`. Every pass drops the number by at least nine, and a
  strictly decreasing sequence of non-negative integers has to stop. That
  is why nine digits of `9` reach a single digit in two passes.
- **Count the digits instead of summing them.** Same loop, replace the
  accumulator with `count += 1`, and you have written `len(str(n))`
  without the string. Watch out for `0`, which has one digit and a loop
  that never runs — the first time this week that the free empty case
  gives you the wrong answer.

Next: [Homework Problem 5 — Fibonacci Numbers up to N](./problem-05-fibonacci-numbers-up-to-n.md).
