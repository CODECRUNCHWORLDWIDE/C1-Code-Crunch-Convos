# Homework Problem 2 — Count Vowels in a String

> **Topic:** the counting pattern, iterating over a string, `in` as a membership test, and normalising case with `.lower()`
> **Lecture:** [03 — Loop Patterns You Will Use Forever](../lecture-notes/03-loop-patterns.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** it is the smallest possible version of a loop that produces an *answer* rather than a side effect. Nine lines, one counter, no cleverness — and the two ways it goes wrong (a counter reset inside the loop, and forgetting about capital letters) are the two ways every counting loop you ever write will go wrong.

## The Brief

Ask someone for a sentence, then tell them how many vowels it has.

Vowels are `a`, `e`, `i`, `o` and `u`. Capitals count too — `A` is the
same vowel as `a` — so `Extra` has two vowels and `AEIOU` has five.

```text
Enter a sentence: Hello, World!
That sentence has 3 vowel(s).
```

Count the vowels in `Hello, World!` by hand before you write anything.
`e`, `o`, `o` — three. Do that once, on paper, because a counting loop
that returns a plausible-but-wrong number looks exactly like a counting
loop that works. The only defence is knowing the right answer in advance
for at least one input.

The `(s)` in `vowel(s)` is not a typo and it is not yours to improve. The
brief specifies that output, so that is the output. Matching a given
format character for character is the skill this problem quietly tests
alongside the counting.

## Starter

Save this as `homework-02-count-vowels.py` and fill in the `TODO`. It
runs as pasted and reports zero vowels every time:

```python
"""Homework 2 - Count the vowels in a sentence.

Case-insensitive: a, e, i, o and u in either case all count.
"""

VOWELS = "aeiou"

text = input("Enter a sentence: ")

count = 0
for ch in text.lower():
    pass  # TODO: if this character is a vowel, add one to count

print(f"That sentence has {count} vowel(s).")
```

Three lines of that starter are already the answer and you should be able
to say why each one is there. `count = 0` sits **outside** the loop.
`text.lower()` is in the `for` header, not in the body. `VOWELS` is a
named constant at the top rather than five letters buried in an `if`.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/homework/problem-02-count-vowels-in-a-string.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks for a sentence with the prompt `Enter a sentence: `.
2. It prints exactly `That sentence has <n> vowel(s).` — one line,
   including the literal `(s)`.
3. `Hello, World!` reports 3.
4. `AEIOU rhythm Extra` reports 7. Capital vowels count.
5. `rhythm` reports 0, without any special case for the empty answer.
6. The counting is a loop, not a library call.

## Constraints

- **No functions.** `def` is Week 4.
- **No `try` / `except`.** Nothing here can raise anyway — `input()`
  returns a string and you are treating it as a string.
- **Normalise the case exactly once.** Either lower the whole sentence
  in the `for` header and keep `VOWELS = "aeiou"`, or leave the sentence
  alone and widen the constant to `"aeiouAEIOU"`. One of those two,
  never both, and never neither.
- **Use `in` for the membership test.** `if ch in VOWELS:` — not a chain
  of five `==` comparisons joined by `or`. Common bugs to catch shows
  what that chain actually does, and it is worse than wrong.
- **`count = 0` goes above the loop.** Put it inside and it resets on
  every character.

## Expected output

The downloadable file below types `Hello, World!` on your behalf when
nobody is at the keyboard, so the run is the same every time:

```text
$ python problem-02-count-vowels-in-a-string.py
Enter a sentence: Hello, World!
That sentence has 3 vowel(s).
```

Run it in your own terminal and it asks you instead. Fed a shoutier
sentence from Git Bash:

```bash
printf 'AEIOU rhythm Extra\n' | python -u problem-02-count-vowels-in-a-string.py 2>&1
```

```text
Enter a sentence: That sentence has 7 vowel(s).
```

The prompt and the answer share a line because piped input is never
echoed back. Five capitals in `AEIOU`, none in `rhythm`, `E` and `a` in
`Extra` — seven.

## Steps

1. Activate your Week 3 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `homework-02-count-vowels.py`. Run it. It says
   zero, which is honest — it has not counted anything yet.
3. Replace the `pass` with the two lines that test the character and
   bump the counter.
4. Run it on `Hello, World!` and check against the 3 you worked out by
   hand.
5. Run it on `AEIOU rhythm Extra`. If you get 1, you lost the case
   handling somewhere. If you get 18, read the third bug below.
6. Run it on `rhythm`. Zero, no crash, no special case needed.
7. Cross-check yourself against the one-liner in **Stretch**. Two
   implementations that agree are much better evidence than one that
   looks right.
8. Commit: `git add homework/homework-02-count-vowels.py` then
   `git commit -m "Week 3 homework: count vowels"`.

## The Solution

```python
"""Count the vowels in a sentence.

Week 3 homework, problem 2, Code Crunch Convos.

Vowels are a, e, i, o and u, and the count is case-insensitive, so A and
a are the same letter.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-02-count-vowels.py``, write ``input("Enter a sentence: ")``
instead.

Questions go to the error stream and the count goes to the normal output
stream, so ``python homework-02-count-vowels.py > count.txt`` saves the
answer and not the question.
"""

import sys

VOWELS: str = "aeiou"
DEMO_SENTENCE: str = "Hello, World!"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


text = ask("Enter a sentence: ", DEMO_SENTENCE)

# The counting pattern: start at zero outside the loop, add one inside.
count = 0
for ch in text.lower():
    if ch in VOWELS:
        count += 1

print(f"That sentence has {count} vowel(s).")
```

**Why it works.**

**This is the counting pattern from
[Lecture 3 §1](../lecture-notes/03-loop-patterns.md) with nothing added.**
Start the counter at zero *outside* the loop, walk the thing you are
counting, add one *inside* when the test passes. Three moves. Every
"how many X are in Y" program you will ever write is this shape, and the
only part that changes is the test.

**`for ch in text.lower()` walks the sentence one character at a time.**
A Python string is iterable, so a `for` loop over it hands you each
character in turn as a one-character string. `text.lower()` builds a
lowercase copy first, and the loop walks that copy, so by the time `ch`
reaches the `if` it is already lowercase and `VOWELS` only needs the five
lowercase letters.

**Lowering in the header, not in the body, is a real choice.**
`for ch in text.lower():` builds one lowercase string, once, for the
whole sentence. `if ch.lower() in VOWELS:` calls a method once *per
character*. Both are correct and on a sentence you can type the
difference is invisible, but the first version says what it means: "from
here down, everything is lowercase."

**`ch in VOWELS` asks "does this appear inside that string".** For a
one-character `ch` that is exactly a membership test, and on a
five-character constant it is as close to free as an operation gets. In
Week 5 you will meet sets and write `ch in {"a", "e", "i", "o", "u"}`,
which is the right tool once the collection is large. For five letters,
the string is clearer.

**`rhythm` needs no special case.** The loop runs six times, the `if` is
false six times, `count` is still `0`, and the f-string prints
`That sentence has 0 vowel(s).` A counter that starts at the right answer
for the empty case is a counter you never have to guard.

**`ask()` is the one piece the brief did not ask for**, and the one `def`
in the file. It exists so this download runs to completion with nobody at
the keyboard: `input()` with nothing to read raises `EOFError`, and
`ask()` catches that and supplies the example sentence. Your own
`homework-02-count-vowels.py` calls `input("Enter a sentence: ")`
directly. It also sends the prompt to the **error** stream rather than
the output stream, so `python homework-02-count-vowels.py > count.txt`
saves the one sentence you wanted and not the question you were asked.

## Download and run

Download [problem-02-count-vowels-in-a-string-solution.py](./problem-02-count-vowels-in-a-string-solution.py)
and run it:

```bash
python problem-02-count-vowels-in-a-string-solution.py
```

Run from a terminal, it asks for a sentence. Run by a script, or with its
input redirected, it uses `Hello, World!` instead of hanging. Save your
own copy as `homework-02-count-vowels.py` in your homework folder, and
commit that one.

## Common bugs to catch

- **The case handling is missing on both sides.** `for ch in text:` with
  `VOWELS = "aeiou"` silently ignores every capital vowel. On
  `AEIOU rhythm Extra` the right answer is 7 and you get:

  ```text
  1
  ```

  No error, no warning, just a number that is wrong in a way you will
  only notice by checking it against a count you did yourself.
  Case-insensitivity fails quietly, so test it with a deliberately
  shouty sentence every time.
- **`count = 0` is inside the loop.** It resets on every character, so
  the answer is always `1` or `0` depending on whether the last
  character happened to be a vowel.
  [Lecture 3 §1](../lecture-notes/03-loop-patterns.md) names this the
  most common bug in beginner loop code. **Initialize outside, update
  inside.**
- **`if ch == "a" or "e" or "i" or "o" or "u":`** — the boolean trap, and
  the reason the constraints say to use `in`. `or` does not compare, it
  *chooses*: it returns the first operand that is truthy. The string
  `"e"` is not empty, so it is truthy, so the whole condition is truthy
  for **every** character and the program reports the length of the
  sentence. `Hello, World!` gives 13. It never raises anything.
- **`count += ch`.** A `TypeError` the moment the first vowel arrives —
  `unsupported operand type(s) for +=: 'int' and 'str'`. You want to add
  one, not add the letter.
- **`print(count)` on its own line inside the loop.** You get a running
  tally printed once per vowel instead of one final answer. The `print`
  belongs after the loop, at the same indent as `count = 0`.

## Under the hood

<details>
<summary>Under the hood — str.count, five passes, and why the loop is the honest version</summary>

Python already has a counting method, and it does not solve this problem
by itself:

```bash
python -c "print('Hello, World!'.lower().count('o'))"
```

```text
2
```

`str.count(sub)` counts non-overlapping occurrences of one substring. One
call, one letter. To count all five vowels you have to call it five
times:

```bash
python -c "text = 'Hello, World!'.lower(); print(sum(text.count(v) for v in 'aeiou'))"
```

```text
3
```

That is correct, and it is worth knowing, but look at what it does:
**five separate passes over the whole sentence**, one per vowel. The
`for` loop makes exactly one pass and asks each character five questions
while it is already there. For a sentence, the difference is nothing. For
a ten-megabyte file it is five reads of ten megabytes against one.

The reason `str.count` still tends to win in practice is that its single
pass runs in C, inside CPython, with no Python-level bytecode per
character — so five fast passes can beat one slow one. That is a real and
slightly annoying fact about Python: the built-in doing more work is
often quicker than your loop doing less. The way out, when it matters, is
not to write cleverer loops but to hand the whole job to something that
loops in C for you.

None of that is why the brief asks for the loop. It asks for the loop
because you are learning what a loop *is*, and because the loop
generalises: change `if ch in VOWELS` to any test at all and it still
works, while `str.count` can only ever count a literal substring.

One more thing `str.count` does that surprises people — it does not count
overlaps:

```bash
python -c "print('aaaa'.count('aa'))"
```

```text
2
```

There are three places where `aa` appears in `aaaa`, but after matching
at position 0 the search resumes at position 2, so the middle one is
never seen. Non-overlapping is the documented behaviour and it is almost
always what you want; it is only surprising the first time.

</details>

<details>
<summary>Under the hood — why "is this a vowel" costs the same no matter how long the sentence is</summary>

There are two different sizes in this program and it is worth keeping
them apart.

The **sentence** can be any length. Call it `n` characters. The loop runs
`n` times, so the program's total work grows in step with the sentence —
double the sentence, double the work. That is what "linear time", or
`O(n)`, means.

The **vowel list** is five characters and always will be. `ch in VOWELS`
scans at most five characters, whatever `n` is. Five is a constant, so
the cost of one membership test does not grow at all as the sentence gets
longer. That is what "constant time", or `O(1)`, means — not "instant",
but "does not depend on the size of the input".

Multiply them and the whole program is `n` iterations at constant cost
each: linear. Which is the best you can do, because you have to look at
every character at least once to know whether it is a vowel.

Now change one thing and watch it break. Suppose the collection were not
five vowels but every word in a dictionary, and you kept it in a list:

```python
if word in every_english_word:   # a list of ~170,000 strings
```

`in` on a list checks the elements one at a time until it finds a match,
so that test is `O(m)` where `m` is 170,000 — and the whole loop becomes
`n * m`. This is the single most common accidental slowness in beginner
Python: a membership test against a big list, inside a loop.

The fix is Week 5's, and it is one character of syntax:

```python
if word in every_english_word_set:   # a set, built with {...} or set(...)
```

A set stores its members by **hash**. It computes a number from the
string and jumps straight to the one place that string could be, instead
of walking the collection. That makes the test `O(1)` — constant, the
same for five members or five million — and turns `n * m` back into `n`.

So `ch in VOWELS` is fine here for a specific, checkable reason: the
right-hand side is tiny and fixed. When the right-hand side is large,
reach for a set. That single habit will save you more time than any other
optimisation you learn this year.

</details>

## Acceptance checklist

- [ ] Running the file asks `Enter a sentence: ` and waits.
- [ ] `Hello, World!` prints `That sentence has 3 vowel(s).`
- [ ] `AEIOU rhythm Extra` prints `That sentence has 7 vowel(s).`
- [ ] `rhythm` prints `That sentence has 0 vowel(s).`
- [ ] The output line matches the brief exactly, `(s)` included.
- [ ] `count = 0` is above the loop, not inside it.
- [ ] The case is normalised in exactly one place.
- [ ] The membership test is `in`, not a chain of `or`.
- [ ] There is no `def` and no `try` in your own file.
- [ ] Committed with a message like `Week 3 homework: count vowels`.

## Stretch

- **Cross-check with the one-liner.** It is a genuinely different
  implementation of the same idea, so if the two disagree, one of them is
  wrong:

  ```bash
  python -c "text = 'Hello, World!'; print(sum(c in 'aeiou' for c in text.lower()))"
  ```

  ```text
  3
  ```

  `sum` over booleans works because `True` is `1` and `False` is `0` in
  Python — the same fact Week 2's grade-letter problem was built on. The
  `c in 'aeiou' for c in ...` part is a generator expression, which is
  Week 5. Write the loop first, then check yourself against the
  one-liner; never the other way round.
- **Report which vowel appeared most often.** Keep five counters in a
  list, `counts = [0, 0, 0, 0, 0]`, so that `counts[i]` is the tally for
  `VOWELS[i]`. Use `enumerate(VOWELS)` to get the index and the letter
  together, and `break` as soon as a character matches, because a
  character cannot be two vowels. Then `zip(VOWELS, counts)` walks the
  labels and the tallies side by side
  ([Lecture 2 §5](../lecture-notes/02-loops.md)) so the max scan from
  [Lecture 3 §3](../lecture-notes/03-loop-patterns.md) can carry the
  winning *letter* along with the winning *number*.

  ```python
  counts = [0, 0, 0, 0, 0]
  total = 0
  for ch in text.lower():
      for index, vowel in enumerate(VOWELS):
          if ch == vowel:
              counts[index] += 1
              total += 1
              break

  print(f"That sentence has {total} vowel(s).")

  if total == 0:
      print("No vowels at all, so there is no most common one.")
  else:
      best_vowel = ""
      best_count = 0
      for vowel, count in zip(VOWELS, counts):
          if count > best_count:
              best_vowel = vowel
              best_count = count
      print(f"Most common vowel: {best_vowel!r} ({best_count} time(s)).")
  ```

  Two decisions in there are worth arguing about. Ties go to the earliest
  vowel alphabetically, because the test is `count > best_count` and not
  `>=`; flip it and ties go to the last one instead. Neither is more
  correct — pick one deliberately and say which. And the `total == 0`
  guard is not decoration: without it, a vowel-free sentence reports that
  the most common vowel is the empty string. In Week 5 this whole thing
  becomes a dictionary and about four lines, which is exactly why writing
  the parallel-lists version once makes dictionaries feel like a relief
  rather than magic.
- **Count consonants too**, and check that vowels plus consonants plus
  everything else adds up to `len(text)`. Sums that have to balance are
  free tests.
- **Count the vowels in a file** instead of a typed sentence. You have
  not met file reading yet, so for now paste a long paragraph at the
  prompt and watch the same nine lines handle it without changing.

Next: [Homework Problem 3 — Reverse a Number](./problem-03-reverse-a-number.md).
