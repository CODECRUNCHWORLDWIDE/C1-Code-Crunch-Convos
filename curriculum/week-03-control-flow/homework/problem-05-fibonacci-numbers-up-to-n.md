# Homework Problem 5 — Fibonacci Numbers up to N

> **Topic:** a `while` loop whose length you cannot know in advance, tuple assignment as a simultaneous update, and getting the boundary right
> **Lecture:** [02 — Loops: Doing Things Repeatedly](../lecture-notes/02-loops.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** the algorithm is four lines and one of them, `a, b = b, a + b`, is not a shortcut — it is a correctness requirement. Split it into two ordinary assignments and the program still runs, still prints a plausible-looking sequence, and is completely wrong. That is the most valuable kind of bug to meet early.

## The Brief

The **Fibonacci sequence** starts with `0` and `1`, and every term after
that is the sum of the two before it:

```text
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
```

`0 + 1` is `1`. `1 + 1` is `2`. `1 + 2` is `3`. `2 + 3` is `5`. Keep
going and it never stops.

Ask for a positive whole number `N`, then print every Fibonacci number
that is **less than or equal to** `N`, one per line.

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

Ten lines. The next term is `55`, which is bigger than `50`, so it does
not appear.

Two details in that output are easy to get wrong and both are in the
sample. The `1` appears **twice**, because the sequence genuinely has two
of them — a version printing only one has started in the wrong place.
And "less than or equal" means `34` would still print if you asked for
`N = 34`, so the comparison is `<=` and not `<`.

You do not know in advance how many numbers you are going to print. That
is what makes this a `while` and not a `for`: a `for` loop is for "do
this once per item in a collection I already have", and a `while` loop is
for "keep going until a condition stops being true".

## Starter

Save this as `homework-05-fibonacci.py` and fill in the `TODO`s. It runs
as pasted and prints nothing after the prompt:

```python
"""Homework 5 - Print every Fibonacci number less than or equal to N."""

DIGITS = "0123456789"

while True:
    raw = input("Enter N: ").strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number and int(raw) >= 1:
        n = int(raw)
        break
    print("Please type a positive whole number, like 50.")

a, b = 0, 1
while False:                 # TODO: keep going while a is still small enough
    # TODO: print a
    # TODO: move both variables one step along the sequence
    pass
```

Notice the validator has grown one clause since problem 4:
`and int(raw) >= 1`. The brief asked for a *positive* integer, and `0` is
a perfectly good whole number that is not positive, so the check has to
say both things.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/homework/problem-05-fibonacci-numbers-up-to-n.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks with the prompt `Enter N: `.
2. It prints every Fibonacci number `<= N`, one per line, in order, with
   nothing else on those lines.
3. `50` prints ten lines, `0` through `34`.
4. `1` prints three lines: `0`, `1`, `1`.
5. `34` prints `34` as its last line.
6. `0` is rejected — the brief says positive — and so is any input that
   is not a run of digits.

## Constraints

- **No functions.** `def` is Week 4, and the recursive definition of
  Fibonacci that every textbook opens with needs one. The first
  **Under the hood** block below shows what that version costs when you
  get there.
- **No `try` / `except`.** Exceptions are Week 6.
- **Use `while`, not `for`.** There is no `range` to write, because you
  do not know how many terms fit under `N` until you have generated
  them.
- **Move both variables in one statement.** `a, b = b, a + b`. Two
  separate assignments do not work, and Common bugs to catch shows the
  convincing-looking sequence you get instead.
- **`<=`, not `<`.** Check `N = 34` specifically. Every other input
  looks fine either way.

## Expected output

The downloadable file below types `50` on your behalf when nobody is at
the keyboard, so the run is the same every time and matches the brief's
sample exactly:

```text
$ python problem-05-fibonacci-numbers-up-to-n.py
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

Run it in your own terminal and it asks you instead. Fed the boundary
case `34` from Git Bash:

```bash
printf '34\n' | python -u problem-05-fibonacci-numbers-up-to-n.py 2>&1
```

```text
Enter N: 0
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

The `0` on the prompt line is the first Fibonacci number, printed
immediately after an input that was never echoed — not part of the
prompt. The last line is `34`, which is the whole reason to run this
input.

## Steps

1. Activate your Week 3 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `homework-05-fibonacci.py`.
3. Before you write the loop, do four steps on paper. Start with `a = 0`
   and `b = 1`. Write down what `a` and `b` are after each move. If your
   fourth row is not `a = 2, b = 3`, do it again — the table under
   **The Solution** is the answer, so cover it up.
4. Replace `while False:` with the real condition and write the two
   lines inside. Delete the `pass`.
5. Run `50`. Count the lines. You want ten.
6. Run `34`. If your last line is `21`, you wrote `<` instead of `<=`.
7. Run `1`. You want `0`, `1`, `1` and nothing more.
8. Run `0` and then a word, and check both are refused politely.
9. Commit: `git add homework/homework-05-fibonacci.py` then
   `git commit -m "Week 3 homework: fibonacci up to N"`.

## The Solution

```python
"""Print every Fibonacci number less than or equal to N.

Week 3 homework, problem 5, Code Crunch Convos.

The sequence starts 0, 1, 1, 2, 3, 5, 8, 13 and each term is the sum of
the two before it. Two variables hold the whole state, and one tuple
assignment moves both forward at once.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-05-fibonacci.py``, write ``input("Enter N: ")`` instead.

Questions go to the error stream and the numbers go to the normal output
stream, so ``python homework-05-fibonacci.py > fib.txt`` saves the
sequence and not the question.
"""

import sys

DIGITS: str = "0123456789"
DEMO_N: str = "50"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


# Read N, refusing anything that is not a positive whole number.
while True:
    raw = ask("Enter N: ", DEMO_N).strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number and int(raw) >= 1:
        n = int(raw)
        break
    print("Please type a positive whole number, like 50.")

a, b = 0, 1
while a <= n:
    print(a)
    a, b = b, a + b
```

**Why it works.**

**The whole state of the sequence is two numbers.** At any moment you
only need to know the term you are on and the term after it. `a` is the
current one, `b` is the next one, and `a, b = b, a + b` moves both
along in a single step. Four lines of algorithm, no list, no index, no
memory of anything you already printed.

**The tuple assignment is not a shortcut, it is a correctness
requirement.** Python evaluates the entire right-hand side **first**,
builds a tuple out of it, and only then unpacks that tuple into the names
on the left. So `a, b = b, a + b` computes `(b, a + b)` using the *old*
`a` and the *old* `b`, and rebinds both afterwards. Write it as two
statements and you destroy `a` before you need it:

```python
a = b          # a is now the old b
b = a + b      # BUG: this is old_b + old_b, not old_a + old_b
```

The three-line correct version needs a temporary variable:
`temp = a; a = b; b = temp + b`. The tuple form is that, with Python
holding the temporary for you.

**Trace it against the brief's sample, `N = 50`:**

| Step | `a` | `b` | `a <= 50`? | prints |
|---|---|---|---|---|
| 0 | 0 | 1 | yes | `0` |
| 1 | 1 | 1 | yes | `1` |
| 2 | 1 | 2 | yes | `1` |
| 3 | 2 | 3 | yes | `2` |
| 4 | 3 | 5 | yes | `3` |
| 5 | 5 | 8 | yes | `5` |
| 6 | 8 | 13 | yes | `8` |
| 7 | 13 | 21 | yes | `13` |
| 8 | 21 | 34 | yes | `21` |
| 9 | 34 | 55 | yes | `34` |
| 10 | 55 | 89 | **no** | — |

Ten lines, `0` through `34`. The `1` at steps 1 and 2 is printed twice
because `a` really is `1` on both, and that is the sequence, not a bug.

**`<=` and not `<`.** The brief says "less than **or equal to** N". With
`<`, running `N = 34` prints only as far as `21`, the boundary case
disappears, and every other input still looks right. Whenever a spec says
"up to and including", find the comparison operator that says it too, and
then test the boundary input on purpose.

**Why `while` and not `for`.** You cannot know how many Fibonacci
numbers fit under `N` without generating them, so there is no `range` to
write. `for` is for a known collection; `while` is for "until this stops
being true" ([Lecture 2 §1 and §2](../lecture-notes/02-loops.md)).
Recognising which of the two a problem wants is most of what this week
teaches.

**`ask()` is the one piece the brief did not ask for**, and the one `def`
in the file. `input()` with nothing to read raises `EOFError`, and
`ask()` catches that and supplies `50` so the download can be run
automatically. It also sends the prompt to the **error** stream rather
than the output stream, so `python homework-05-fibonacci.py > fib.txt`
gives you a file of ten clean numbers and not a question. Your own file
calls `input("Enter N: ")` directly.

## Download and run

Download [problem-05-fibonacci-numbers-up-to-n-solution.py](./problem-05-fibonacci-numbers-up-to-n-solution.py)
and run it:

```bash
python problem-05-fibonacci-numbers-up-to-n-solution.py
```

Run from a terminal, it asks for `N`. Run by a script, or with its input
redirected, it uses `50` instead of hanging. Save your own copy as
`homework-05-fibonacci.py` in your homework folder, and commit that one.

## Common bugs to catch

- **Two separate assignments instead of the tuple swap.** This is the
  defining mistake of this problem. `a = b` then `b = a + b` gives you
  `old_b + old_b`, so every step doubles, and starting from `0, 1` you
  get powers of two:

  ```text
  [0, 1, 2, 4, 8, 16, 32]
  ```

  It looks like a sequence. It grows. It stops at the right sort of
  place. It is not Fibonacci. Check your output against the brief's
  sample line by line, because "looks like a sequence" is not a test.
- **`while a < n`.** Off by one at the boundary. `N = 34` should end on
  `34` and instead ends on `21`:

  ```text
  [0, 1, 1, 2, 3, 5, 8, 13, 21]
  ```
- **Starting at `a, b = 1, 1`.** Drops the leading `0`. Both conventions
  exist in the wild, which is exactly why you read the spec rather than
  your memory. This brief states the sequence explicitly and it starts
  `0, 1, 1, 2`, so `0` belongs.
- **Printing `b` instead of `a`.** You get the sequence shifted one place
  along — `1, 1, 2, 3, 5, ...` — and the last line overshoots `N`,
  because `b` is the term you have not checked yet.
- **Forgetting the `>= 1` clause in the validator.** `0` passes the digit
  check, and `while a <= 0` then prints a single `0` and stops. The brief
  asked for a positive integer; a validator that only checks the
  characters is checking the form and not the meaning.

## Under the hood

<details>
<summary>Under the hood — the recursive version you will meet in Week 4, and what it costs</summary>

Every textbook defines Fibonacci like this:

```text
fib(0) = 0
fib(1) = 1
fib(n) = fib(n - 1) + fib(n - 2)
```

That is a definition in terms of itself, and in Week 4 you will be able
to write it in Python almost word for word:

```python
def fib(n: int) -> int:
    """The nth Fibonacci number, defined the way the textbook does."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

It is beautiful and it is correct and it is disastrously slow, for a
reason worth understanding before you meet it.

Ask for `fib(5)`. It asks for `fib(4)` and `fib(3)`. `fib(4)` asks for
`fib(3)` and `fib(2)`. **`fib(3)` is now being computed twice**, from
scratch, with no memory that it was ever computed before. One level down,
`fib(2)` is computed three times. The duplication doubles at every level,
so the number of calls grows roughly like `1.6 ** n`:

| `n` | calls to compute `fib(n)` |
|---:|---:|
| 10 | 177 |
| 20 | 21,891 |
| 30 | 2,692,537 |

Two and a half million function calls to produce a number the loop in
your homework reaches in thirty steps. Timed on the machine this course
was written on, CPython 3.13.2:

```text
0.102s vs 0.5 microseconds  ratio 188,170x
```

The loop wins by a factor of about 190,000 at `n = 30`, and the gap
widens every time you add one to `n`. At `n = 50` the recursive version
would take days.

The loop is fast for a simple reason: **it never computes anything
twice.** Each term is produced once, used to make the next one, and
forgotten. That is `n` additions, full stop.

Recursion is not the villain here — the duplicated work is. There are two
standard cures, and you will meet both:

- **Remember the answers.** Keep a cache of `n -> fib(n)` and check it
  before recursing. In Python that is one line,
  `@functools.cache` above the function, and it turns the same recursive
  code from exponential to linear. Week 4 introduces decorators far
  enough for that to make sense.
- **Turn the recursion inside out.** Build the answers from the bottom
  up instead of the top down, which is precisely what `a, b = b, a + b`
  is doing. You have already written the fast version.

There is a hard limit as well as a slow one. Python refuses to nest
function calls more than about a thousand deep by default:

```bash
python -c "import sys; print(sys.getrecursionlimit())"
```

```text
1000
```

Go past it and you get `RecursionError: maximum recursion depth exceeded`
instead of an answer. The loop has no such ceiling — and Python's
integers have no size limit either, so the loop will happily print the
thousandth Fibonacci number, all 209 digits of it, on a machine where the
recursive version cannot even reach it.

</details>

<details>
<summary>Under the hood — why the ratio settles down, and the closed form that is not quite exact</summary>

Divide each Fibonacci number by the one before it and watch what happens:

```bash
python -c "
a, b = 1, 1
for _ in range(10):
    print(f'{b / a:.10f}')
    a, b = b, a + b
"
```

```text
1.0000000000
2.0000000000
1.5000000000
1.6666666667
1.6000000000
1.6250000000
1.6153846154
1.6190476190
1.6176470588
1.6181818182
```

The ratio bounces above and below a value and closes in on it. That value
is `(1 + 5 ** 0.5) / 2`, about `1.6180339887`, and it is called the
**golden ratio**. It is not a coincidence: if the ratio settles at some
number `r`, then `r` must satisfy `r = 1 + 1 / r`, and the positive
solution to that is the golden ratio.

Which means Fibonacci numbers grow **exponentially** — roughly `r ** n` —
and that is the real reason the sequence runs out of small values so
fast. Only ten of them are `<= 50`. Only thirty-one are below a
million.

There is even a closed form, called Binet's formula, that computes the
nth term with no loop at all:

```bash
python -c "
r = (1 + 5 ** 0.5) / 2
for n in (10, 30, 70, 71):
    print(n, round((r ** n - (-r) ** -n) / 5 ** 0.5))
"
```

```text
10 55
30 832040
70 190392490709135
71 308061521170130
```

The first three are right. The fourth is wrong. The true 71st term is
`308061521170129` and the formula says `...130` — out by one. `5 ** 0.5`
is a float, floats carry about sixteen significant digits, and the 71st
Fibonacci number has fifteen; by the 80th the formula is out by 59.

So the closed form is exact in mathematics and approximate in floating
point, while the four-line loop is exact for ever, because Python's
integers never run out of room. That is a fair summary of the difference
between a formula and a program: the formula tells you what the answer
is, and the program has to actually produce it.

</details>

## Acceptance checklist

- [ ] Running the file asks `Enter N: ` and waits.
- [ ] `50` prints exactly ten lines, `0` through `34`.
- [ ] `1` prints `0`, `1`, `1` and stops.
- [ ] `34` prints `34` as its final line.
- [ ] `0` is refused with the retry message.
- [ ] A typed word is refused with the retry message.
- [ ] The update is one statement, `a, b = b, a + b`.
- [ ] The loop condition uses `<=`.
- [ ] There is no `def` and no `try` in your own file.
- [ ] Committed with a message like
      `Week 3 homework: fibonacci up to N`.

## Stretch

- **Count them instead of printing them.** Replace `print(a)` with
  `count += 1` and report the total. Nothing else moves:

  ```python
  a, b = 0, 1
  count = 0
  while a <= n:
      count += 1
      a, b = b, a + b

  print(f"{count} Fibonacci number(s) are <= {n}.")
  ```

  Fed `50` it prints `10 Fibonacci number(s) are <= 50.` — count the
  lines in the Expected output block and they agree. That
  substitutability is the payoff of thinking in patterns: the traversal
  and the thing you do per item are separate concerns, and swapping one
  never disturbs the other. It is the same observation problems 3 and 4
  are built on.
- **Print them on one line.** `print(a, end=" ")` inside the loop and a
  bare `print()` after it. Compare the two shapes and decide which you
  would rather read for `N = 1000000`.
- **Sum the even ones.** Add `if a % 2 == 0: total += a` inside the loop.
  For `N = 4000000` the answer is `4613732`, which is Project Euler
  problem 2 — your homework is now competition practice.
- **Watch the ratio converge.** Print `b / a` each turn, from the second
  turn onwards, and see it close in on `1.618...`. The first
  **Under the hood** block explains what that number is.
- **Ask for the first N terms instead of terms up to N.** That version
  *does* know its own length, so it is a `for` loop over
  `range(n)` — the same algorithm with the other kind of loop around it.
  Writing both is the fastest way to feel the difference between them.

Next: [Homework Problem 6 — Simple ATM Menu](./problem-06-simple-atm-menu.md).
