# Homework Problem 3 — Reverse a Number

> **Topic:** a `while` loop with an accumulator, `% 10` and `// 10` as a way to take a number apart, and a loop condition that handles zero for free
> **Lecture:** [02 — Loops: Doing Things Repeatedly](../lecture-notes/02-loops.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** `% 10` peels off a digit and `// 10` throws it away. That pair is how you take any number apart, in any base, and it turns up in hashing, in checksums, in base conversion and in about a third of all interview warm-up questions. Doing it with `str()` teaches you nothing. Doing it with arithmetic teaches you the pair.

## The Brief

Ask for a whole number that is zero or bigger, then print the number you
get by writing its digits backwards.

```text
Enter a non-negative integer: 12345
Reversed: 54321

Enter a non-negative integer: 1200
Reversed: 21
```

**Do not turn the number into a string.** No `str()`, no slicing, no
`[::-1]`. Take it apart with arithmetic.

Two operators do all the work:

- `n % 10` gives you the **last digit**. `12345 % 10` is `5`.
- `n // 10` gives you the number **without** its last digit.
  `12345 // 10` is `1234`.

Together they are a conveyor belt. Every turn of the loop hands you one
more digit, right to left, until there is nothing left to hand you.

Then you have to put the digits back together in the new order, and that
is the part worth thinking about. If you have `543` so far and the next
digit is `2`, you want `5432`. You get there by pushing the digits you
already have one place to the left — multiplying by ten — and dropping
the new digit into the empty units column:

```text
543 * 10 + 2 = 5432
```

Notice what happens to `1200`. The first two digits off the belt are `0`
and `0`, and `0 * 10 + 0` is still `0`. Leading zeros cannot survive
inside an integer, because an integer stores a *value*, not a spelling.
`21` is the right answer, and the brief says so.

## Starter

Save this as `homework-03-reverse-number.py` and fill in the `TODO`s. It
runs as pasted and always prints `Reversed: 0`:

```python
"""Homework 3 - Reverse the digits of a non-negative integer.

Arithmetic only: the digits are peeled off with % 10 and // 10 and
rebuilt with an accumulator. No str() anywhere.
"""

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
reversed_number = 0

while remaining > 0:
    digit = remaining % 10           # last digit
    # TODO: shift reversed_number left by one place and add digit
    # TODO: drop the last digit from remaining
    break                            # DELETE this line once the TODOs are done

print(f"Reversed: {reversed_number}")
```

That `break` on the last line of the loop is there so the starter does
not hang while the two updates are missing. Delete it when you write
them. If you forget to delete it, you get the last digit and nothing
else, which is at least a loud failure.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/homework/problem-03-reverse-a-number.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks with the prompt `Enter a non-negative integer: `.
2. It prints `Reversed: <n>` on one line.
3. `12345` gives `54321`.
4. `1200` gives `21`.
5. `0` gives `0`.
6. `7` gives `7`.
7. Anything that is not a run of digits produces a message and another
   question, never a crash.

## Constraints

- **No `str()`, no `[::-1]`, no `reversed()`.** Arithmetic only. The
  string version exists and it is under **Stretch**, where it belongs —
  as a second opinion you check yourself against, not as the answer.
- **No functions.** `def` is Week 4.
- **No `try` / `except`.** Exceptions are Week 6. Check the characters
  before you hand the string to `int()`.
- **`//`, never `/`.** `//` is floor division and it stays in whole
  numbers. `/` gives you a float and quietly destroys the program. This
  is the single most common typo in this problem and Common bugs to
  catch shows exactly what it does.
- **Every `while` loop needs a line that moves it towards the exit.** In
  this loop that line is `remaining = remaining // 10`. If you cannot
  point at it, you have written an infinite loop.

## Expected output

The downloadable file below types `1200` on your behalf when nobody is
at the keyboard — the trickiest of the brief's two samples — so the run
is the same every time:

```text
$ python problem-03-reverse-a-number.py
Enter a non-negative integer: 1200
Reversed: 21
```

Run it in your own terminal and it asks you instead. Fed the other four
interesting inputs from Git Bash, one run each:

```bash
for n in 12345 1200 0 7; do printf "$n\n" | python -u problem-03-reverse-a-number.py 2>&1; done
```

```text
Enter a non-negative integer: Reversed: 54321
Enter a non-negative integer: Reversed: 21
Enter a non-negative integer: Reversed: 0
Enter a non-negative integer: Reversed: 7
```

The prompt and the answer share a line because piped input is never
echoed back.

## Steps

1. Activate your Week 3 environment and `cd` into your `homework/`
   folder.
2. Before you type anything, trace `12345` on paper. Five rows: what
   `digit` is, what `reversed_number` becomes, what `remaining` becomes.
   The table under **The Solution** is the answer, so cover it up first.
3. Save the Starter as `homework-03-reverse-number.py`.
4. Write the accumulator line. Run it — still `Reversed: 5`, because the
   `break` is still there.
5. Write the `remaining = remaining // 10` line, then delete the
   `break`. Now run `12345` and you should see `54321`.
6. Run `1200`. If you get `0021` you have not written this in Python; if
   you get `21` you have.
7. Run `0` and `7`. Neither should need a special case. If you added
   one, your loop condition is wrong.
8. Commit: `git add homework/homework-03-reverse-number.py` then
   `git commit -m "Week 3 homework: reverse a number"`.

## The Solution

```python
"""Reverse the digits of a non-negative integer.

Week 3 homework, problem 3, Code Crunch Convos.

Arithmetic only: the digits are peeled off with ``% 10`` and ``// 10``
and rebuilt with an accumulator. There is no ``str()`` anywhere in the
answer, which is the whole point of the exercise.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-03-reverse-number.py``, write
``input("Enter a non-negative integer: ")`` instead.

Questions go to the error stream and the result goes to the normal output
stream, so ``python homework-03-reverse-number.py > result.txt`` saves the
answer and not the question.
"""

import sys

DIGITS: str = "0123456789"
DEMO_NUMBER: str = "1200"


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
reversed_number = 0

while remaining > 0:
    digit = remaining % 10           # last digit
    reversed_number = reversed_number * 10 + digit
    remaining = remaining // 10      # drop that digit

print(f"Reversed: {reversed_number}")
```

**Why it works.**

**Trace it once and the pattern is yours forever.** Here is `12345`, one
row per turn of the loop:

| Turn | `remaining` at the top | `digit` | `reversed_number` after | `remaining` after |
|---|---|---|---|---|
| 1 | 12345 | 5 | `0 * 10 + 5` = 5 | 1234 |
| 2 | 1234 | 4 | `5 * 10 + 4` = 54 | 123 |
| 3 | 123 | 3 | `54 * 10 + 3` = 543 | 12 |
| 4 | 12 | 2 | `543 * 10 + 2` = 5432 | 1 |
| 5 | 1 | 1 | `5432 * 10 + 1` = 54321 | 0 |
| — | 0 | — | the condition is false, the loop ends | — |

**The `* 10` is the whole trick.** An accumulator usually looks like
`total += n` — see problem 4, which is this program with the `* 10`
removed. Here the update has to *shift the digits you already have one
place to the left* before it can put the new one in the units column, and
multiplying by ten is what shifting left means in base 10. Take the
`* 10` out and you have accidentally written the sum-of-digits problem
instead, which is exactly why these two problems are neighbours.

**`remaining = number` instead of counting `number` itself down.** The
loop destroys whatever it walks, so keeping the original in `number`
means you can still print it, reuse it, or check your work afterwards.
It costs one line and saves the "wait, where did my input go" moment.

**Zero is handled by doing nothing at all.** `while remaining > 0` is
false the very first time it is asked, the loop body never runs,
`reversed_number` is still the `0` it was initialised to, and the program
prints `Reversed: 0`. Getting the empty case right for free is the mark
of a well-chosen loop condition. Write it as `while True:` with a `break`
at the bottom instead and zero needs a special case of its own.

**`1200` and the missing leading zeros.** Turns 1 and 2 pull off `0` and
`0`, and `0 * 10 + 0` is `0` both times, so the accumulator is still
sitting at zero when the `2` arrives. There is nothing to preserve: an
`int` has no idea what a leading zero is. The brief's own sample expects
`21`, so this is correct behaviour, not a bug looking for a fix.

**`ask()` is the one piece the brief did not ask for**, and the one `def`
in the file. `input()` with nothing to read raises `EOFError`, so `ask()`
catches that and supplies the example number, which is what lets this
download be run automatically. It also puts the prompt on the **error**
stream instead of the output stream, so
`python homework-03-reverse-number.py > result.txt` saves the one line
you wanted. Your own file calls
`input("Enter a non-negative integer: ")` directly — no `def`, no
`except`.

## Download and run

Download [problem-03-reverse-a-number-solution.py](./problem-03-reverse-a-number-solution.py)
and run it:

```bash
python problem-03-reverse-a-number-solution.py
```

Run from a terminal, it asks for a number. Run by a script, or with its
input redirected, it uses `1200` instead of hanging. Save your own copy
as `homework-03-reverse-number.py` in your homework folder, and commit
that one.

## Common bugs to catch

- **`remaining = remaining // 10` is missing.** The condition never
  changes, so the loop never ends — the accidental infinite loop from
  [Lecture 2 §1](../lecture-notes/02-loops.md). There is no error and no
  output. The program simply sits there while `reversed_number` grows
  without bound, and Python's integers do not overflow, so it will
  happily eat memory until you stop it. Press `Ctrl+C`; Python prints a
  `KeyboardInterrupt` traceback pointing at whichever line it happened to
  be on. Then go and find the line that was supposed to move `remaining`
  towards zero.
- **`/` instead of `//`.** This one is spectacular. `12345 / 10` is
  `1234.5`, a float, and from there everything is floats. `%` on a float
  gives a fractional digit, the accumulator multiplies fractions by ten
  over and over, and `remaining` creeps towards zero by tenths without
  ever reaching it, so the loop runs until the float underflows. The real
  output:

  ```text
  Reversed: inf
  ```

  after 328 turns of a loop that should have run five times. `inf` is
  Python's floating-point infinity — the accumulator got bigger than the
  largest number a float can hold. `//` is floor division and it keeps
  you in whole numbers.
- **`reversed_number += digit`** — the `* 10` is missing, so you have
  solved problem 4 by mistake and `12345` gives `15`. There is no error.
  Check `12345 → 54321` before you check anything else, because it is the
  one input that catches this immediately.
- **`while remaining >= 0`.** Once `remaining` is `0`, `0 // 10` is still
  `0`, so the condition stays true forever and the loop spins with
  nothing changing. The answer is already correct; the program just never
  says so. Use `> 0`.
- **Reaching for `str()` after being told not to.** `int(str(n)[::-1])`
  is a perfectly good one-liner and it is under **Stretch**. It is out of
  bounds for the main answer because the point of the arithmetic version
  is the `% 10` / `// 10` pair, and you will use that pair for years.

## Under the hood

<details>
<summary>Under the hood — the arithmetic reverse and the string reverse are not the same operation</summary>

Both routes give `54321` for `12345`, so it is tempting to file them as
two spellings of one idea. They are not. They operate on different things
and they disagree at the edges.

`int(str(n)[::-1])` reverses **the way the number is written down**.
`str(n)` produces a spelling in base 10, `[::-1]` walks that spelling
backwards, and `int(...)` reads the result back as a value.

The arithmetic version never produces a spelling at all. It reverses **a
sequence of remainders modulo 10**, which happens to coincide with the
base-10 spelling because that is what base 10 *is*.

Three places where the difference shows.

**1. The base is a parameter, and only one version has it.** Change the
`10`s to `2`s and the arithmetic version reverses the number's binary
digits instead. The string version cannot follow — `str(n)` only ever
gives you base 10, and you would have to go and find `bin()`, strip its
`0b` prefix, and convert back with `int(s, 2)`.

```bash
python -c "
n = 12345
r = 0
while n > 0:
    r = r * 2 + n % 2
    n = n // 2
print(r)
"
```

```text
9987
```

**2. Leading zeros vanish in both, but for different reasons.** In the
arithmetic version they never exist: `0 * 10 + 0` is `0`, and the
accumulator has nowhere to put a zero that means nothing. In the string
version `str(1200)[::-1]` genuinely is the four-character string
`'0021'`, and it is `int()` that throws the zeros away when it reads that
spelling back. Two different mechanisms reaching the same answer by
accident is exactly the kind of coincidence that stops being one when
you change something.

**3. The string version accepts things the arithmetic one does not.**
`str()` on a negative number includes the `-`, and reversing that puts
the minus sign at the end:

```bash
python -c "print(str(-12)[::-1])"
```

```text
21-
```

`int('21-')` then raises `ValueError: invalid literal for int() with
base 10: '21-'`. The arithmetic version has no such trap, because a sign
is not a digit and never enters the loop.

On cost: the arithmetic version does about one division and one
multiplication per digit and allocates nothing. The string version
allocates a string, allocates a reversed copy, then parses it. For a
number you can type, both are instant. For an integer with a million
digits — which Python will happily give you — the string version's
allocations start to matter, and its base-10 conversion is itself the
expensive part.

Use the string version when you want to talk about how a number is
*written*, such as testing for a palindrome. Use the arithmetic version
when you want to talk about the number's *value*, which is nearly every
other time.

</details>

<details>
<summary>Under the hood — why // and % are one machine instruction, and what Python does with huge integers</summary>

`remaining % 10` and `remaining // 10` look like two divisions. On the
processor they are usually one: a single integer-division instruction
produces the quotient and the remainder together, in two registers, and
compilers routinely spot the pair and emit it once.

Python does not quite get that for free, because a Python `int` is not a
machine word. CPython stores integers as an array of 30-bit digits with a
sign, which is why `2 ** 1000` just works instead of overflowing the way
it would in C or Java. Small integers still take one pass through the
division routine; a thousand-digit integer takes proportionally longer.
If you want both results explicitly, `divmod` gives you them in one call:

```bash
python -c "print(divmod(12345, 10))"
```

```text
(1234, 5)
```

That is the same pair the loop computes, and on large integers it is
genuinely cheaper than doing `%` and `//` separately, because the
division only happens once.

The other thing worth knowing is how many turns the loop takes. It is
**one per digit**, not one per unit. `999999999` takes nine turns, not a
billion — each turn divides the number by ten, so the count is
`log10(n)` rounded up. That is why this technique stays fast on numbers
far too large to loop over directly, and it is the same reason binary
search is fast: repeatedly dividing the problem by a constant factor gets
you to the bottom in a number of steps proportional to the *number of
digits*, not to the number itself.

Since Python 3.11 there is a guard rail on the other side of this.
Converting a truly enormous integer to or from a string raises by
default:

```text
ValueError: Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
```

That limit exists because base-10 conversion of a huge integer is
quadratic and was being used to hang servers. It is a limit on `str()`
and `int()`, not on arithmetic — one more reason the `% 10` / `// 10`
version is the sturdier of the two.

</details>

## Acceptance checklist

- [ ] Running the file asks `Enter a non-negative integer: ` and waits.
- [ ] `12345` prints `Reversed: 54321`.
- [ ] `1200` prints `Reversed: 21`.
- [ ] `0` prints `Reversed: 0`, with no special case in your code.
- [ ] `7` prints `Reversed: 7`.
- [ ] Typing a word prints the retry message and asks again.
- [ ] There is no `str()`, no `[::-1]` and no `reversed()` anywhere.
- [ ] The loop uses `//`, not `/`.
- [ ] You can point at the line that moves `remaining` towards zero.
- [ ] There is no `def` and no `try` in your own file.
- [ ] Committed with a message like
      `Week 3 homework: reverse a number`.

## Stretch

- **Write the string version and confirm the two agree.** This is the
  cheapest real test there is: two independent implementations, the same
  inputs, and any disagreement means one of them is wrong.

  ```bash
  python -c "
  for n in (12345, 1200, 0, 7, 100000):
      print(n, '->', int(str(n)[::-1]))
  "
  ```

  ```text
  12345 -> 54321
  1200 -> 21
  0 -> 0
  7 -> 7
  100000 -> 1
  ```

  `str(n)` spells the number, `[::-1]` is a slice with step `-1` that
  walks the spelling backwards, and `int(...)` reads it back as a value.
  Checking two implementations against each other over a range of inputs
  is the whole idea behind property-based testing, which you meet
  properly in Week 11.
- **Test for a palindrome.** A number reads the same forwards and
  backwards when `reversed_number == number`. Try `12321`, `1221`, `7`
  and `1200`. This is the one job where the *string* version is the more
  honest tool, because a palindrome is a fact about the spelling.
- **Reverse in another base.** Change both `10`s to `2` and print the
  result. Then check it with
  `python -c "print(bin(12345), bin(9987))"` and read the two binary
  strings side by side.
- **Add the digits up while you are already peeling them off.** One extra
  accumulator in the same loop and you have solved problem 4 at the same
  time. Notice that the traversal and the thing you do per digit are
  separate concerns — that is the idea problem 4 is built on.

Next: [Homework Problem 4 — Sum of Digits](./problem-04-sum-of-digits.md).
