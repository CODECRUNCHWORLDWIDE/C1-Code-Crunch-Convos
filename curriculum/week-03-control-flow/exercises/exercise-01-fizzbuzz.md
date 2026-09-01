# Exercise 1 — FizzBuzz

> **Topic:** `for`, `range`, `if`/`elif`/`else`, and the remainder operator `%`
> **Lecture:** [01 — Conditionals: Deciding What Runs](../lecture-notes/01-conditionals.md)
> **Difficulty:** Beginner
> **Target time:** 15 minutes
> **Why this one:** the answer depends on the *order* you write your branches in, and nothing else. Get the order wrong and the program still runs, still prints a hundred tidy lines, and is still wrong. That is the kind of bug that survives into real software. Meet it here, where you can see it at a glance, and you will recognise it later when the branches are shipping prices instead of multiples of three.

## The Brief

A room full of people is counting out loud, one to a hundred. There is a
rule. Every third count, you say `Fizz` instead of the number. Every fifth
count, you say `Buzz`. And when a count is both — every fifteenth — you say
`FizzBuzz`. Any count the rules do not touch, you just say the number.

You are printing the call sheet for that drill: one line per count, a
hundred lines.

Here is the trap, and it is the whole exercise. Fifteen belongs to three
rules at once. It is a multiple of three, a multiple of five, and a
multiple of fifteen. If you ask "is it a multiple of three?" first, fifteen
says yes, and the program prints `Fizz` and moves on. It never gets around
to asking the question you cared about. Nothing crashes. You just quietly
lose every `FizzBuzz` in the run.

So you ask the narrowest question first.

You will write it as two pieces: one small function that takes a single
count and hands back the word for it, and a `main()` that calls that
function a hundred times and prints what comes back. Splitting it that way
means you can check one awkward number without reading a hundred lines of
output.

## Starter

Create `exercise-01-fizzbuzz.py` in your practice repo, paste this in, then
fill in the two `TODO`s:

```python
"""exercise-01-fizzbuzz.py — branch ordering with an if/elif/else chain.

Prints the counts 1 through 100, replacing multiples of 3 with "Fizz",
multiples of 5 with "Buzz", and multiples of both with "FizzBuzz".
"""

FIRST_COUNT = 1
LAST_COUNT = 100


def fizzbuzz_word(count: int) -> str:
    """Return the word that should be called out for `count`.

    Returns "FizzBuzz" for multiples of 15, "Fizz" for other multiples of
    3, "Buzz" for other multiples of 5, and the count itself as a string
    otherwise.
    """
    # TODO: add the branches above this line — the both-case first, then
    # the multiple-of-3 case, then the multiple-of-5 case. The line below
    # is the fall-through "it is just a number" case.
    return str(count)


def main() -> None:
    """Print one line per count from FIRST_COUNT to LAST_COUNT."""
    for count in range(FIRST_COUNT, LAST_COUNT + 1):
        # TODO: print the word for this count, not the count itself.
        print(count)


if __name__ == "__main__":
    main()
```

Two words you need before you start.

**Remainder.** `%` is the leftover after a division. `17 % 5` is `2`,
because five goes into seventeen three times with two left over. When there
is nothing left over, the leftover is zero — so `count % 3 == 0` is the
sentence "count divides evenly by three".

**Chain.** `if` … `elif` … `elif` … `else` is one decision with several
possible answers, not several separate decisions. Python walks down it,
stops at the first branch that is true, and never looks at the rest.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/exercises/exercise-01-fizzbuzz.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `fizzbuzz_word()` hands back a `str` in every case — including the plain
   numbers, which come back as `"7"`, not `7`. One kind of thing coming out
   of a function means nobody has to check what they got.
2. The three words are exactly `Fizz`, `Buzz`, and `FizzBuzz`. Capital F,
   capital B, no spaces, no punctuation.
3. `main()` prints exactly 100 lines: the counts 1 through 100 inclusive.
   Line one is `1` and line one hundred is `Buzz`.
4. Divisibility is tested with `%`. `count % 3 == 0` means "count divides
   evenly by 3".
5. The two bounds live in the constants at the top of the file. Changing
   `LAST_COUNT` to `20` must change the run without touching any other
   line.

## Constraints

- **Ask the multiple-of-15 question first.** A chain stops at the first
  branch that is true ([Lecture 1 §3](../lecture-notes/01-conditionals.md)).
  Put `count % 3 == 0` at the top and fifteen matches it, so the
  `FizzBuzz` branch is code that can never run. You may write the first
  test as `count % 15 == 0` or as `count % 3 == 0 and count % 5 == 0` —
  they agree on every number — but it goes first either way.
- **One chain, not four separate `if` statements.** Four independent `if`s
  let more than one of them fire for the same count, which is the exact bug
  the ordering rule exists to prevent. The chain makes "only one of these
  can win" part of the shape of the code instead of something you have to
  remember.
- **Return the word. Do not print it inside `fizzbuzz_word()`.** A function
  that prints can only be checked by squinting at a terminal. A function
  that returns can be checked with one line —
  `fizzbuzz_word(15) == "FizzBuzz"` — and in Week 11 that line becomes a
  test.
- **Stop at 100, and know why before you type it.** A hundred lines is
  short enough to scroll through in one go, and it holds six multiples of
  fifteen (15, 30, 45, 60, 75, 90). Six is enough repetitions of the tricky
  case that a wrong branch order is impossible to miss.
- **No lists.** Do not collect the hundred words into a list and print the
  list at the end. `range` hands you one number at a time and never holds
  more than one ([Lecture 2 §3](../lecture-notes/02-loops.md)); a list would
  hold all hundred for no reason at all.
- **`def` is Week 4, and these five exercises are the deliberate exception:
  the starter hands you the function headers already written, so you are
  filling in a body someone else declared rather than deciding what a
  function should be.**

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2.
One hundred lines:

```text
$ python exercise-01-fizzbuzz.py
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
Fizz
22
23
Fizz
Buzz
26
Fizz
28
29
FizzBuzz
31
32
Fizz
34
Buzz
Fizz
37
38
Fizz
Buzz
41
Fizz
43
44
FizzBuzz
46
47
Fizz
49
Buzz
Fizz
52
53
Fizz
Buzz
56
Fizz
58
59
FizzBuzz
61
62
Fizz
64
Buzz
Fizz
67
68
Fizz
Buzz
71
Fizz
73
74
FizzBuzz
76
77
Fizz
79
Buzz
Fizz
82
83
Fizz
Buzz
86
Fizz
88
89
FizzBuzz
91
92
Fizz
94
Buzz
Fizz
97
98
Fizz
Buzz
```

Line 15 is the one that matters. If it says `Fizz`, your branches are in
the wrong order. Nothing else on the page will tell you.

## Steps

1. Turn on your Week 3 virtual environment. Your prompt should show
   `(.venv)` or something like it.
2. Create `exercise-01-fizzbuzz.py` and paste the starter in.
3. Fill in `fizzbuzz_word()` first. Leave `main()` alone for the moment.
4. Check the function before you touch the loop. Run
   `python -i exercise-01-fizzbuzz.py` — the `-i` runs the file and then
   leaves you at a `>>>` prompt with everything in it loaded:

   ```text
   >>> fizzbuzz_word(15), fizzbuzz_word(9), fizzbuzz_word(10), fizzbuzz_word(7)
   ('FizzBuzz', 'Fizz', 'Buzz', '7')
   ```

   Note the quotes around `'7'`. That is requirement 1 holding. Leave with
   `Ctrl+Z` then Enter on Windows, or `Ctrl+D` elsewhere.
5. Now fix `main()`: print `fizzbuzz_word(count)` instead of `count`. The
   `+ 1` in the range is already there, and it is load-bearing — `range`
   stops *before* its stop value, so without it the run would end at 99.
6. Run it: `python exercise-01-fizzbuzz.py`.
7. Count the lines instead of trusting your eyes. In Git Bash, macOS or
   Linux:

   ```bash
   python exercise-01-fizzbuzz.py | wc -l
   python exercise-01-fizzbuzz.py | sort | uniq -c | sort -rn | head -3
   ```

   ```text
   100
        27 Fizz
        14 Buzz
         6 FizzBuzz
   ```

   27 + 14 + 6 is 47 words, which leaves 53 plain numbers. On Windows
   PowerShell, `python exercise-01-fizzbuzz.py | Measure-Object -Line`
   gives you the 100.
8. Set `LAST_COUNT = 20`, run again, and confirm you get exactly the first
   twenty lines of the full run and nothing else. Then set it back.

## The Solution

```python
"""exercise-01-fizzbuzz-solution.py — branch ordering with an if/elif/else chain.

Prints the counts 1 through 100, replacing multiples of 3 with "Fizz",
multiples of 5 with "Buzz", and multiples of both with "FizzBuzz".
"""

FIRST_COUNT = 1
LAST_COUNT = 100


def fizzbuzz_word(count: int) -> str:
    """Return the word that should be called out for `count`.

    Returns "FizzBuzz" for multiples of 15, "Fizz" for other multiples of
    3, "Buzz" for other multiples of 5, and the count itself as a string
    otherwise.
    """
    if count % 15 == 0:
        return "FizzBuzz"
    elif count % 3 == 0:
        return "Fizz"
    elif count % 5 == 0:
        return "Buzz"
    else:
        return str(count)


def main() -> None:
    """Print one line per count from FIRST_COUNT to LAST_COUNT."""
    for count in range(FIRST_COUNT, LAST_COUNT + 1):
        print(fizzbuzz_word(count))


if __name__ == "__main__":
    main()
```

**Narrow question first, wide question last.** That is the entire rule, and
it is worth saying in a way that outlives FizzBuzz. `count % 15 == 0` is
true of six numbers under a hundred. `count % 3 == 0` is true of
thirty-three of them. The small set has to be asked about first, because
the chain gives the number to the first branch that says yes and never
offers it to anyone else. When you meet price tiers, grade boundaries or
shipping bands later, "narrow to wide" is this same instruction wearing
different clothes.

**`% 15` and "divisible by 3 and by 5" agree here, and you should know
why.** Three and five share no factors, so anything divisible by both is
divisible by their product. That reasoning is worth carrying explicitly,
because it stops being true the moment the two divisors overlap: a number
divisible by 3 and by 6 is divisible by 6, not by 18. "Divisible by both"
is the form that is always safe. `% 15` is a shortcut you have earned by
checking.

**One chain, even though four `if`s would work here.** Every branch ends in
`return`, and a `return` leaves the function immediately, so four separate
`if` statements would in fact behave identically today. Write the chain
anyway. Delete one `return` from the four-`if` version and it silently
starts falling through into the next test; delete one from the chain and
Python still only ever reaches one branch. Write the shape that survives
the edit you have not made yet.

**Every branch returns a string, including the boring one.** `str(count)`
is what makes `fizzbuzz_word(7)` come back as `'7'` and not `7`. It looks
like a fussy detail. It is the difference between a function whose result
you can print, join, or compare without thinking, and one where you have to
ask what type you got before you can use it.

**`LAST_COUNT + 1`, and why `range(LAST_COUNT)` is worse than off by one.**
`range` stops before its stop value, so the `+ 1` is what makes 100 print.
Reaching for `range(LAST_COUNT)` instead does not only lose the last line —
it *gains* a wrong first one. Zero divides evenly by everything, so
`0 % 15 == 0` is true, and the run opens with `FizzBuzz` before it has
counted anything at all.

No list appears anywhere in this program. `range` produces one count,
`print` consumes it, and the next one arrives. The program holds exactly
one number in its hand no matter how large `LAST_COUNT` gets.

## Download and run

Download
[exercise-01-fizzbuzz-solution.py](./exercise-01-fizzbuzz-solution.py) and
run it:

```bash
python exercise-01-fizzbuzz-solution.py
```

It is the same program as the one you are writing, under a name that will
not collide with your own `exercise-01-fizzbuzz.py`.

## Common bugs to catch

- **Line 15 says `Fizz` instead of `FizzBuzz`, and `FizzBuzz` never appears
  at all.** The most common version of this program, and it raises nothing:

  ```python
  if count % 3 == 0:
      return "Fizz"
  elif count % 5 == 0:
      return "Buzz"
  elif count % 15 == 0:
      return "FizzBuzz"
  ```

  Lines 13 to 16 of the run come out as `13`, `14`, `Fizz`, `16`. The third
  branch is unreachable: anything that would satisfy it satisfied the first
  branch already and left. Move the both-case to the top.

- **15 prints on three separate lines.** You used three independent `if`
  statements with three `print()` calls instead of one chain returning one
  value.

- **The run starts with `FizzBuzz` and ends at 99.** You wrote
  `range(LAST_COUNT)`, which counts 0 through 99. Zero is divisible by
  everything. Use `range(FIRST_COUNT, LAST_COUNT + 1)`.

- **Every line prints `None`.** A branch has no `return` — usually the
  final `else` went missing, so the function runs out of body. A Python
  function that falls off the end hands back `None`, and `print(None)` is
  perfectly happy to print it. Counts 1 to 7 look like this:

  ```text
  None
  None
  Fizz
  None
  Buzz
  Fizz
  None
  ```

  If you see `None` in output, the question is always "which path through
  this function forgot to return".

- **`Buzz` never appears, and 5, 10 and 20 come out as `FizzBuzz`.** You
  wrote `if count % 3 and count % 5 == 0:` and the `== 0` on the first half
  went missing:

  ```text
  1 2 Fizz 4 FizzBuzz Fizz 7 8 Fizz FizzBuzz 11 Fizz 13 14 Fizz 16 17 Fizz 19 FizzBuzz
  ```

  `count % 3` is a *number*, not a yes-or-no, and Python treats any non-zero
  number as true ([Lecture 1 §4](../lecture-notes/01-conditionals.md)):

  ```text
  >>> 15 % 3, bool(15 % 3)
  (0, False)
  >>> 10 % 3, bool(10 % 3)
  (1, True)
  ```

  So your first branch reads "*not* a multiple of 3, and a multiple of 5",
  which is exactly backwards. Every comparison in an `and` needs its own
  `== 0`.

- **`TypeError: not all arguments converted during string formatting`.**
  You handed `fizzbuzz_word()` a string — usually whatever `input()` gave
  you, unconverted:

  ```text
  Count: Traceback (most recent call last):
    File "exercise-01-fizzbuzz.py", line 35, in <module>
      main()
      ~~~~^^
    File "exercise-01-fizzbuzz.py", line 31, in main
      print(fizzbuzz_word(count))
            ~~~~~~~~~~~~~^^^^^^^
    File "exercise-01-fizzbuzz.py", line 18, in fizzbuzz_word
      if count % 15 == 0:
         ~~~~~~^~~~
  TypeError: not all arguments converted during string formatting
  ```

  That message looks like it belongs to a different program, and there is a
  reason. `%` between a string and something else is not remainder at all —
  it is Python's old string-formatting operator, the one behind
  `"%s items" % 3`. `"15" % 15` asks Python to slot 15 into a template with
  no slots in it, and it complains that you gave it something it had
  nowhere to put. Wrap the value in `int()` before you do arithmetic on it.

- **`SyntaxError: invalid syntax` pointing at an `elif` line.** Either the
  colon at the end of the previous branch went missing, or you wrote
  `else if`. Python has no `else if`; the word is `elif`.

- **`IndentationError: expected an indented block after 'for' statement`.**
  The `print()` under your `for` sits at the same indentation as the `for`
  itself. The loop body needs four more spaces.

## Under the hood

<details>
<summary>Under the hood — why remainder beats counting, and what % does with negative numbers</summary>

**The version without `%`.** You do not strictly need remainder for
FizzBuzz. You could keep two little counters, add one to each on every
pass, and reset a counter to zero when it reaches its limit:

```python
since_fizz = 0
since_buzz = 0
for count in range(1, 101):
    since_fizz += 1
    since_buzz += 1
    is_fizz = since_fizz == 3
    is_buzz = since_buzz == 5
    if is_fizz:
        since_fizz = 0
    if is_buzz:
        since_buzz = 0
    ...
```

That works. Notice what it cost. Two counters, and then two more names to
remember what the counters said, because resetting a counter destroys the
very fact you needed. Four pieces of state, all of which have to stay in
step with each other and with `count`, and every one of them is a place to
forget an update.

`count % 3 == 0` asks the question fresh every time and remembers nothing
at all. Anything a program does not have to remember is something it cannot
get wrong.

The counting version has one genuine advantage worth knowing about: it
never divides. On hardware where division is expensive and addition is
cheap — a small microcontroller, or a tight inner loop in a graphics engine
— that trade is sometimes made deliberately. On CPython the difference is
nowhere near the cost of the `print`, so it buys you nothing here.

**What `%` does with negatives.** You will not hit this in FizzBuzz, where
every count is positive, but it catches people later and the rule is short.
In Python the result of `%` takes the **sign of the divisor**, not the sign
of the thing being divided:

```text
>>> -7 % 3
2
>>> 7 % -3
-2
>>> -7 % -3
-1
```

That surprises anyone arriving from C or Java, where `-7 % 3` is `-1`. The
reason is that Python defines `%` to agree with `//`, and `//` rounds
*down* — toward negative infinity — rather than toward zero:

```text
>>> -7 // 3
-3
>>> -7 - (-3 * 3)
2
```

`a % b` is always exactly `a - (a // b) * b`. Once `//` rounds down, the
remainder has to come out with the divisor's sign for that identity to
hold.

The practical upshot is a good one. With a positive divisor, Python's `%`
always gives you "how far past the last multiple you are", and that answer
is never negative. `n % 2 == 0` is a correct evenness test for negative
numbers, `n % 3` is always 0, 1 or 2, and a value you use as an index never
comes back negative and blows up. In C or Java you have to write the extra
correction yourself. This is one of the places where Python's choice is
simply the more useful one.

**Everything divides zero.** `0 % 15 == 0` is `True`, and so is `0 % n` for
any `n` that is not itself zero. Nothing is going wrong — zero really is a
multiple of every number — but it is why a run that starts at zero opens
with `FizzBuzz`. Any time a divisibility test fires unexpectedly on the
very first item, check whether you started counting at zero.

</details>

<details>
<summary>Under the hood — what "the chain stops at the first match" costs and saves</summary>

An `if`/`elif` chain is not four tests. It is one test, then possibly a
second, then possibly a third. On a multiple of fifteen Python evaluates
`count % 15 == 0`, gets `True`, and jumps straight past the rest of the
chain to the end. On a plain number like 7 it evaluates all three
conditions and falls into the `else`.

So the chain does *less* work than four independent `if`s, and it does the
least work on the cases you put first. That gives you a second, weaker
reason for ordering — put the common case early and you do fewer
comparisons — which occasionally pulls against the first reason. When the
two disagree, correctness wins: order by how narrow the case is, not by how
often it happens. Here they happen to agree, because the narrowest case is
also the rarest.

The same short-circuiting is what makes `and` safe to lean on.
`count % 3 == 0 and count % 5 == 0` never evaluates the right half when the
left half is false. That is not an optimisation Python is allowed to skip;
it is part of what `and` means. You will use it later to write things like
`if items and items[0] == "x"`, where evaluating the right half on an empty
list would raise.

</details>

## Acceptance checklist

- [ ] `python exercise-01-fizzbuzz.py` runs with no traceback.
- [ ] Exactly 100 lines print, starting at `1` and ending at `Buzz`.
- [ ] Line 15 reads `FizzBuzz`, and so do lines 30, 45, 60, 75, and 90.
- [ ] `fizzbuzz_word()` returns strings and never calls `print()`.
- [ ] `fizzbuzz_word(7)` comes back as `'7'`, with the quotes, not as `7`.
- [ ] Changing `LAST_COUNT` to `20` produces a 20-line run with no other edit.
- [ ] The tallies come out to 6 `FizzBuzz`, 27 `Fizz`, 14 `Buzz`, 53 numbers.
- [ ] Committed to Git with a message like `Add Week 3 exercise 1: fizzbuzz`.

## Stretch

- Add a third rule: multiples of 7 become `Bang`, and combinations join up
  in order, so 21 is `FizzBang` and 105 is `FizzBuzzBang`. Count how many
  branches three rules need if you keep the chain. Then throw the chain
  away and build the word up from pieces instead — start with an empty
  string, add `"Fizz"` if it divides by 3, add `"Buzz"` if it divides by 5,
  and fall back to `str(count)` if the string is still empty. Notice which
  version you would rather add a fourth rule to.
- Move the rules into a list of `(divisor, word)` pairs at the top of the
  file and loop over them inside `fizzbuzz_word()`. A fourth rule then
  costs one line. This is the shape the problem takes once Week 5 gives you
  data structures, and it is worth seeing the destination now.
- Add three `assert` lines at the bottom of `main()` covering 15, 9 and 7.
  They cost nothing while the code is right and shout the moment a later
  edit breaks it.

When your hundred lines look right, move on to
[Exercise 2 — Sum of Evens](./exercise-02-sum-evens.md).
