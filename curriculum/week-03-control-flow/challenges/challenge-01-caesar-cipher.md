# Challenge 1 — Caesar Cipher

> **Topic:** looping over the characters of a string, turning letters into numbers and back, and the one operator that makes the alphabet wrap around
> **Lecture:** [03 — Loop Patterns](../lecture-notes/03-loop-patterns.md)
> **Difficulty:** the arithmetic is four lines; getting `z` to wrap round to `a` is the whole challenge
> **Target time:** 60–90 minutes
> **Why this one:** it is the first program where a letter and a number are the same thing wearing different hats. Once you can move between them, sorting, hashing, and every text-processing task later in the course stops looking like magic.

## The Brief

A **Caesar cipher** slides every letter of a message a fixed number of
places along the alphabet. It is named after Julius Caesar, who used it
to write to his generals. It is not real security — you will break it by
hand at the bottom of this page — but it is a perfect shape for what
Week 3 teaches.

With a shift of 3:

- `A` becomes `D`
- `B` becomes `E`
- `Z` becomes `C`, because after `Z` you start again at `A`
- a space, a comma or a digit is copied straight through, untouched

So `Hello, World!` with a shift of 3 comes out as `Khoor, Zruog!`. The
comma, the space and the exclamation mark did not move.

Decoding is the same trick backwards. Shift by `-3` and `Khoor, Zruog!`
turns back into `Hello, World!`.

Write a small command-line tool that does both. It asks which way you
want to go, how far to shift, and what the message is. Then it prints
the answer and offers to do another one.

Three things make this harder than it looks, and each one is a Week 3
idea:

1. **The wrap.** `z` shifted by 3 has to become `c`, not the punctuation
   three places past `z`. That is the `%` operator, and it is the point
   of the challenge.
2. **Two alphabets.** `A` and `a` are different characters to a
   computer, so uppercase and lowercase need separate handling if
   `Hello` is going to stay capitalised.
3. **The shift is typed by a human.** Somebody will type `three`. Your
   program has to say something polite rather than fall over — and this
   week you have to do that *without* `try` / `except`, which is Week 6.

> *As a* learner who has just met `while`, `for` and `%`,
> *I want* to turn a line of text into a different line of text, one
> character at a time,
> *so that* I find out what a string is actually made of.

## Starter

Save this as `challenge-01-caesar-cipher.py` and run it before you change
anything. It runs exactly as pasted: it asks the three questions and
prints the message back **unshifted**, because the shifting is the part
you write.

```python
"""TODO: one line saying what this file does."""

import sys

LOWER_A: int = ord("a")  # 97
UPPER_A: int = ord("A")  # 65
DIGITS: str = "0123456789"

DEMO_ANSWERS: list[str] = ["encode", "3", "Hello, World!", "n"]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        print(f"{prompt}{answer}")
        return answer


mode = ask("Mode (encode/decode): ", "encode").strip().lower()
# TODO 1: keep asking until mode is "encode" or "decode".

raw_shift = ask("Shift: ", "0").strip()
# TODO 2: keep asking until raw_shift is a whole number, then convert it.
shift = 0

# TODO 3: if the mode is decode, flip the sign of the shift.
# TODO 4: wrap the shift into 0-25 with % 26.

message = ask("Message: ", "")
pieces = []
for ch in message:
    # TODO 5: shift a-z, shift A-Z, copy anything else through unchanged.
    pieces.append(ch)

print(f"Result:  {''.join(pieces)}")

# TODO 6: wrap all of the above in a `while True:` loop, and ask
#         "Encode another? (y/n) " at the bottom of it.
```

Run it and you get this, which is a working program that has not learned
the cipher yet:

```text
$ python challenge-01-caesar-cipher.py
Mode (encode/decode): encode
Shift: 3
Message: Hello, World!
Result:  Hello, World!
```

**About `ask()`.** It is given to you, and you never have to write one.
It asks a question and reads a line, and if there is nobody there to
answer — because a checker is running the file, or because you piped
input into it and the input ran out — it uses one of the `DEMO_ANSWERS`
instead and prints it, so the file always produces a whole session.

`ask()` reaches ahead of Week 3 on purpose. `def` is Week 4 and
`try` / `except` is Week 6. That is fine, because it is scaffolding
rather than the answer: everything below it — the loops, the validation,
the cipher — stays inside the tools this week gave you. *Constraints*
says exactly what those are, and if you would rather see the version with
no `ask()` in it at all, it is the first thing under *Stretch*.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/challenges/challenge-01-caesar-cipher.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Ask for three things, in this order, with these exact prompts:
   `Mode (encode/decode): `, `Shift: `, and `Message: `.
2. The mode is `encode` or `decode`. Accept any capitalisation and stray
   spaces around it. Anything else gets a polite message and the question
   again.
3. The shift is a whole number, and it may be negative or zero. Anything
   else — `three`, `3.5`, an empty line — gets a polite message and the
   question again. Do **not** use `try` / `except` to find out.
4. Print the transformed message as `Result:  ` followed by the text.
   That is **two** spaces after the colon, so `Result` lines up under
   `Message` in the session.
5. Uppercase stays uppercase, lowercase stays lowercase, and every
   character that is not an English letter is copied through unchanged.
6. The shift wraps modulo 26: a shift of `3` and a shift of `29` produce
   the same output, and a shift of `26` changes nothing.
7. `decode` with shift `n` undoes `encode` with shift `n`.
8. After each result, ask `Encode another? (y/n) `. On `y` or `yes`, go
   round again. On anything else, print `Bye!` and stop.

## Constraints

- **No `def`.** Functions are Week 4. Every loop, every branch and every
  bit of arithmetic in this program is written straight out at the top
  level of the file. You will notice some duplication near the end.
  That is deliberate, and *The Solution* says what Week 4 does about it.
  The one exception is the `ask()` helper, which is handed to you.
- **No `try` / `except`.** Exceptions are Week 6. `int("three")` raises,
  so you never call `int()` until you already know the text is a number.
  Ask questions about the string first — `in`, slicing, a `for` over its
  characters — and convert only once the answer is yes. This is not a
  workaround for missing a feature. Checking before you convert is a good
  habit that outlives Week 6.
- **Build the result in a list, then join it.** `pieces.append(ch)`
  inside the loop and `"".join(pieces)` after it. Lecture 3 §6 has the
  reason: strings cannot be changed once made, so `result += ch` quietly
  builds a brand-new string on every single character.
- **Test which letter it is with a comparison, not a method.**
  `if "a" <= ch <= "z":` asks the question your arithmetic actually
  depends on. `ch.isalpha()` asks a different question that only looks
  the same, and *Common bugs to catch* shows a real message it mangles.
- **Two spaces after `Result:`.** Requirement 4. It is there so the
  result lines up under the message in the terminal, and it is the kind
  of thing a grader compares character by character.
- **Standard library only.** The file imports `sys` and nothing else, so
  it runs on a fresh Python the moment somebody downloads it.

## Expected output

Run the file with nothing attached to its input and it answers its own
questions from the demo script and prints a whole two-round session. This
is the real stdout on CPython 3.13.2:

```text
$ python challenge-01-caesar-cipher.py
Mode (encode/decode): encode
Shift: 3
Message: Hello, World!
Result:  Khoor, Zruog!
Encode another? (y/n) y

Mode (encode/decode): decode
Shift: 3
Message: Khoor, Zruog!
Result:  Hello, World!
Encode another? (y/n) n
Bye!
```

Round one encodes, round two decodes what round one produced, and gets
the original back. That is requirement 7, proved in one run.

Run it in your own terminal and it asks *you* the questions instead. Here
is a session that walks every acceptance criterion, produced by feeding
the answers in from the shell. The questions are not shown, because they
go to the error stream — that is explained in *The Solution*, and it is
why the results come out this clean:

```text
$ printf 'encode\n1\nabc\ny\nencode\n3\nxyz\ny\nencode\n29\nabc\ny\nencode\n0\nHello, World!\ny\nencode\n-3\nKhoor, Zruog!\ny\nencode\n13\nHello, World!\ny\ndecode\n13\nUryyb, Jbeyq!\nn\n' | python challenge-01-caesar-cipher.py
Result:  bcd

Result:  abc

Result:  def

Result:  Hello, World!

Result:  Hello, World!

Result:  Uryyb, Jbeyq!

Result:  Hello, World!
Bye!
```

Read it as a checklist. `abc` shifted by 1 is `bcd`. `xyz` shifted by 3
is `abc`, so the wrap works. `abc` shifted by **29** is `def`, the same
as a shift of 3, so requirement 6 holds. A shift of 0 changes nothing. A
shift of `-3` recovers `Hello, World!` from `Khoor, Zruog!`. And the last
pair is ROT13 out and back.

And the two ways of typing something the program cannot use:

```text
$ printf 'sideways\nencode\nthree\n\n3\nHello\nn\n' | python challenge-01-caesar-cipher.py
Please type 'encode' or 'decode'.
The shift must be a whole number, like 3, 0 or -3.
The shift must be a whole number, like 3, 0 or -3.
Result:  Khoor
Bye!
```

`sideways` is not a mode. `three` is not a number. The empty line — the
second complaint — is somebody pressing Enter with nothing typed. All
three get a sentence and another go, and none of them produces a
traceback.

## Steps

1. Save the Starter as `challenge-01-caesar-cipher.py` and run
   `python challenge-01-caesar-cipher.py`. You should see the session
   above, with the message unchanged. Nothing is broken; the cipher is
   missing on purpose.

2. Do **TODO 5** first, because it is the interesting one, and do only
   lowercase to begin with. Replace the body of the `for` loop with:

   ```python
   if "a" <= ch <= "z":
       position = ord(ch) - LOWER_A
       pieces.append(chr((position + shift) % 26 + LOWER_A))
   else:
       pieces.append(ch)
   ```

   `shift` is still `0`, so the output should still be unchanged. Now
   edit the line `shift = 0` to say `shift = 3` and run it again. The
   lowercase letters should move and `H` should not. Put `shift = 0`
   back afterwards.

3. Add the uppercase branch as an `elif`, with `UPPER_A` instead of
   `LOWER_A`. Test it with `shift = 3` hard-coded again: you want
   `Khoor, Zruog!`.

4. Do **TODO 2**. You need to know whether `raw_shift` is a whole number
   before you call `int()` on it. Three lines:

   ```python
   body = raw_shift[1:] if raw_shift[:1] in ("-", "+") else raw_shift
   is_whole_number = body != ""
   for ch in body:
       if ch not in DIGITS:
           is_whole_number = False
           break
   ```

   Then wrap it in `while True:` — if `is_whole_number`, do
   `shift = int(raw_shift)` and `break`; otherwise print the complaint
   and let the loop ask again. Test it with `three`, with an empty line,
   and with `-3`.

5. Do **TODO 3** and **TODO 4**. Two lines: `if mode == "decode":
   shift = -shift`, then `shift %= 26`. Check that `encode` 3 and then
   `decode` 3 gives you your message back.

6. Do **TODO 1** — the same `while True:` shape as step 4, with
   `if mode in ("encode", "decode"): break`.

7. Do **TODO 6** last. Indent everything you have written by four
   spaces, put `while True:` above it, and add the `Encode another?`
   question at the bottom. Watch your indentation; this is the step that
   most often breaks a working program.

8. Run the whole session from *Expected output* and compare it character
   by character, including the two spaces after `Result:`.

9. Commit it:

   ```bash
   git add challenge-01-caesar-cipher.py
   git commit -m "Add Challenge 1: Caesar cipher"
   ```

## The Solution

```python
"""Caesar cipher: shift every letter, leave everything else alone.

Challenge 1, Week 3, Code Crunch Convos. Encodes or decodes one line of
text with a Caesar shift. Uppercase stays uppercase, lowercase stays
lowercase, and digits, spaces and punctuation pass straight through.

Week 3 rules: the cipher itself uses no functions -- ``def`` is Week 4 --
and no ``try`` / ``except``, which is Week 6. The one helper below,
``ask()``, is scaffolding rather than part of the answer. It is what lets
this file run and print a whole session when nobody is at the keyboard.

The questions go to the error stream and the results go to the normal
output stream, so ``python caesar.py > out.txt`` saves the results and
none of the questions.

Run it with::

    python caesar.py
"""

import sys

LOWER_A: int = ord("a")  # 97
UPPER_A: int = ord("A")  # 65
DIGITS: str = "0123456789"

# The session this file plays when its input stream is already finished.
DEMO_ANSWERS: list[str] = [
    "encode",
    "3",
    "Hello, World!",
    "y",
    "decode",
    "3",
    "Khoor, Zruog!",
    "n",
]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on once the demo script above has
            run out. Every call site passes something that ends the
            program, so the file can never loop forever unattended.

    Returns:
        The line that was typed, or the next demo answer. A demo answer
        is echoed after the prompt on the normal output stream, so the
        printed session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        print(f"{prompt}{answer}")
        return answer


while True:
    # --- mode ---
    while True:
        mode = ask("Mode (encode/decode): ", "encode").strip().lower()
        if mode in ("encode", "decode"):
            break
        print("Please type 'encode' or 'decode'.")

    # --- shift (a whole number, possibly negative) ---
    while True:
        raw_shift = ask("Shift: ", "0").strip()
        body = raw_shift[1:] if raw_shift[:1] in ("-", "+") else raw_shift
        is_whole_number = body != ""
        for ch in body:
            if ch not in DIGITS:
                is_whole_number = False
                break
        if is_whole_number:
            shift = int(raw_shift)
            break
        print("The shift must be a whole number, like 3, 0 or -3.")

    # Decoding is just encoding by the opposite shift.
    if mode == "decode":
        shift = -shift
    shift %= 26  # 3 and 29 now agree; -3 becomes 23

    # --- transform ---
    message = ask("Message: ", "")
    pieces = []
    for ch in message:
        if "a" <= ch <= "z":
            position = ord(ch) - LOWER_A
            pieces.append(chr((position + shift) % 26 + LOWER_A))
        elif "A" <= ch <= "Z":
            position = ord(ch) - UPPER_A
            pieces.append(chr((position + shift) % 26 + UPPER_A))
        else:
            pieces.append(ch)

    result = "".join(pieces)
    print(f"Result:  {result}")

    again = ask("Encode another? (y/n) ", "n").strip().lower()
    if again not in ("y", "yes"):
        print("Bye!")
        break
    print()
```

**Decoding is encoding, backwards.** Requirement 2 asks for two modes,
but there is only one transformation in this file. The line
`if mode == "decode": shift = -shift` folds the second mode into the
first *before a single character is touched*. Everything after that point
does not know or care which mode you picked. That is why the decoder can
never drift out of step with the encoder — there is only one of them.

**`shift %= 26` does three jobs in one line.** `%` gives you the
remainder after division. `29 % 26` is `3`, so a shift of 29 and a shift
of 3 become the same thing, which is requirement 6. `-3 % 26` is `23`,
and stepping forward 23 places lands you exactly where stepping back 3
places would, so the decode negation is tidied up too. And afterwards
`shift` is always somewhere in `0` to `25`, so the `% 26` inside the loop
never has to deal with a huge or negative number.

**`ord` and `chr` are a letter's two faces.** `ord("a")` is `97` and
`chr(97)` is `"a"`. Every character has a number, and the 26 lowercase
letters have 26 numbers in a row. So `ord(ch) - LOWER_A` turns a letter
into its *position* in the alphabet — `a` is 0, `z` is 25 — and adding
`LOWER_A` back turns a position into a letter. All the shifting happens
in between, on plain small numbers, where `% 26` makes obvious sense.

**Why `"a" <= ch <= "z"` and not `ch.islower()`.** Both look like "is
this a lowercase letter". Only one of them asks the question the
arithmetic depends on, which is "is this one of the 26 characters I am
about to do `% 26` on". `é` is a lowercase letter and it is not one of
those 26. *Common bugs to catch* shows what it does to a message.

**Validation happens before conversion.** `int("three")` raises, and
`try` / `except` is Week 6, so the shift loop checks the characters
itself: peel off a leading `-` or `+` if there is one, then confirm what
is left is not empty and contains only `0`–`9`. Note `raw_shift[:1]`
rather than `raw_shift[0]`. Slicing an empty string gives you `""`;
*indexing* an empty string raises. That one character is the difference
between a polite message and a crash when somebody presses Enter.

**`pieces` and `"".join(...)`.** A Python string cannot be changed after
it is made. `result += ch` therefore does not add a character to a
string — it builds a whole new string with one more character in it, and
throws the old one away, once per letter. Appending to a list and joining
at the end walks the message once. On a one-line message you would never
feel the difference; the habit is what matters.

**Two spaces after `Result:`.** Look at the session: `Result:  Khoor,
Zruog!` sits directly under `Message: Hello, World!`. `Message:` is eight
characters and `Result:` is seven, so `Result:` needs one extra space to
catch up. That is the entire reason.

**`ask()` puts the questions on the other stream.** A program has two
ways to send text out: the normal output stream, `stdout`, for its
answers, and the error stream, `stderr`, for everything else. `ask()`
prints the question to `stderr` with `end=""` so the cursor stays on the
same line, and `flush=True` so the question appears *before* the program
starts waiting rather than being held in a buffer. Then it calls `input()`
with no argument at all.

That last detail is the one people get wrong. `input("Shift: ")` prints
its prompt to **stdout**, mixed in with your results. Keeping them apart
means `python caesar.py > out.txt` saves the results and none of the
questions, which is what you saw in the second *Expected output* block.

**What Week 4 will change.** The two branches of the letter test are the
same three lines twice, once with `LOWER_A` and once with `UPPER_A`. You
cannot remove that duplication cleanly without a function. In Week 4 you
will write one `def shift_char(ch: str, amount: int) -> str:` and call it
from a single loop, and this file gets about a third shorter. Notice the
duplication now, while it is still mildly annoying — that annoyance is
what makes `def` feel like a relief rather than more syntax to learn.

## Download and run

Download [challenge-01-caesar-cipher-solution.py](./challenge-01-caesar-cipher-solution.py)
and run it:

```bash
python challenge-01-caesar-cipher-solution.py
```

In your own terminal it asks you the questions. Run by a script, or with
its input closed, it answers itself from the demo script and prints the
same session every time.

You can also feed it answers from the shell, one line per question:

```bash
printf 'encode\n13\nHello, World!\nn\n' | python challenge-01-caesar-cipher-solution.py
```

Because the questions go to the error stream, `>` captures the results on
their own:

```bash
python challenge-01-caesar-cipher-solution.py > out.txt
```

In your own project, save the same code as
`challenge-01-caesar-cipher.py`.

## Common bugs to catch

**You called `int()` before checking.** The direct translation of the
brief is `shift = int(input("Shift: "))`. Type `three`:

```text
Mode (encode/decode): Shift: Traceback (most recent call last):
  File "challenge-01-caesar-cipher.py", line 2, in <module>
    shift = int(input("Shift: "))
ValueError: invalid literal for int() with base 10: 'three'
```

`try` / `except` would catch that, and it is Week 6. This week, ask about
the characters first.

**You used `raw_shift[0]` instead of `raw_shift[:1]`.** Press Enter with
nothing typed:

```text
Shift: Traceback (most recent call last):
  File "challenge-01-caesar-cipher.py", line 2, in <module>
    first = raw_shift[0]
            ~~~~~~~~~^^^
IndexError: string index out of range
```

There is no character at position 0 of an empty string. A *slice* of an
empty string is just an empty string, and comparing `""` to `"-"` is
perfectly fine.

**You validated with `.isdigit()`.** It is the obvious method and it is
wrong twice over:

```text
>>> "-3".isdigit()
False
>>> "³".isdigit()
True
```

The first line rejects the negative shifts requirement 3 asks for. The
second accepts a superscript three, and then:

```text
  File "challenge-01-caesar-cipher.py", line 1, in <module>
    print(int("³"))
          ~~~^^^^^^
ValueError: invalid literal for int() with base 10: '³'
```

Checking each character against the literal `"0123456789"` has neither
problem.

**You used `isalpha()` and it quietly ruined a word.** There is no error
message here, which is what makes it the dangerous one. `café` at shift
3, with `isalpha()` as the test:

```text
fdij
```

That looks plausible. Now decode it with shift `-3`:

```text
cafg
```

The `é` did not come back. Its code point is `233`, nowhere near the 26
letters starting at `97`, so `(233 - 97 + 3) % 26 + 97` lands on `j` and
the original is gone for good. With `"a" <= ch <= "z"` the accented
letter is copied through untouched, `café` encodes to `fdié`, and
decoding gives you `café` back.

**You handled decode with `26 - shift`.** It looks the same as `-shift`,
and for a shift of 3 it is (`23` either way). It stops being the same
when the shift is 0 or bigger than 26, unless you remember to add another
`% 26` — and the version people actually write does not. Negate first,
then take `% 26` once. One rule, every input.

**The result does not line up under the message.** One space after
`Result:` instead of two. The program is still correct; the session no
longer matches. Requirement 4.

**Everything works, and then the second round is wrong.** You wrote
`shift %= 26` but left the decode negation *after* it. Order matters:
flip the sign first, then wrap, because it is the flipped value that
needs wrapping.

**The `y` at the end restarts, but `Y` does not.** You compared before
normalising. The order is read, `.strip()`, `.lower()`, then test.

## Under the hood

<details>
<summary>Under the hood — modular arithmetic, and why the alphabet is a circle</summary>

`%` is the remainder operator. `17 % 5` is `2`, because 5 goes into 17
three times with 2 left over. That much is division you already know.

The useful part is what it does to a *sequence* of numbers. Take the
positions 0 to 25 and add 3 to each, then take `% 26`:

```text
x 23 0 a
y 24 1 b
z 25 2 c
a 0 3 d
b 1 4 e
```

The first column is the letter, then its position, then the shifted
position, then the shifted letter. Look at `z`: position 25, plus 3 is
28, and `28 % 26` is `2`, which is `c`. The line that would have run off
the end of the alphabet comes back round to the beginning. `%` has turned
a straight line of 26 letters into a circle.

That is the whole cipher. Everything else in the file is bookkeeping.

**Why a shift of 26 does nothing.** Twenty-six steps round a circle of
twenty-six positions is one complete lap:

```text
>>> [(s, (0 + s) % 26) for s in (0, 26, 52, -26)]
[(0, 0), (26, 0), (52, 0), (-26, 0)]
```

Every one of those shifts leaves the message exactly as it was. So there
are not infinitely many Caesar ciphers — there are 26, and one of them is
"do nothing". That is also why the brute-force attack under *Stretch*
only needs 26 lines.

**Python's `%` always agrees with its divisor's sign.** This is the part
that surprises people who have written C or Java:

```text
>>> -3 % 26
23
>>> -3 % -26
-3
>>> 3 % -26
-23
```

The result takes the sign of the number on the right. With a positive
divisor — which is all this program ever uses — you can never get a
negative answer out of `%`. That is exactly the guarantee the cipher
needs, and it is why the same code in C or Java needs an extra `+ 26`
that Python does not.

**Reading the two `%`s in the answer.** There are two, and they are doing
different jobs. `shift %= 26` normalises the shift *once*, before the
loop, so it is a plain number between 0 and 25. The `% 26` inside the
loop wraps each *position*. You could delete the first one and the
program would still be correct, because the second one would clean up
after it. Doing it once up front is cheaper and, more importantly, means
that by the time you read the loop, `shift` is already a small friendly
number.

</details>

<details>
<summary>Under the hood — what a code point is, and why ord and chr exist</summary>

A computer stores numbers. It does not store letters. So every character
you can type has been assigned a number, and `ord()` tells you which:

```text
>>> for ch in "Az 0!":
...     print(repr(ch), ord(ch))
'A' 65
'z' 122
' ' 32
'0' 48
'!' 33
```

That number is called the character's **code point**. `chr()` goes the
other way: `chr(65)` is `"A"`.

The numbers are not random. Whoever laid them out put `A` through `Z` in
26 consecutive slots starting at 65, and `a` through `z` in 26
consecutive slots starting at 97. Everything this challenge does depends
on that decision. `ord(ch) - 97` only means "position in the alphabet"
because the alphabet is stored in order.

**Why 65 and 97, of all numbers.** They come from ASCII, a table agreed
in 1963 for teleprinters. It has 128 entries: control codes first, then
punctuation and digits, then the uppercase letters, then more
punctuation, then the lowercase letters. The gap of exactly 32 between
`A` and `a` was chosen so that changing letter case is a single bit flip
— which is why `ord("a") - ord("A")` is `32`, and why an old machine
could uppercase text almost for free.

**Beyond 127 is where it gets interesting.** ASCII has no `é`, no `ñ`,
no `字`, no emoji. Modern Python strings use Unicode, which has room for
over a million code points and currently defines about 150,000 of them.
`ord("é")` is `233`. `ord("字")` is `23383`.

This is the whole reason `"a" <= ch <= "z"` is the right test and
`ch.isalpha()` is not. `isalpha()` is asking Unicode "is this a letter in
any language", and the honest answer for `é` is yes. But the arithmetic
underneath this cipher only works on 26 specific code points, and `233`
is not one of them. The comparison asks the narrower question, which
happens to be the true one.

Comparing characters with `<` and `<=` is comparing their code points,
which is also why `"apple" < "banana"` is `True` — Python walks the two
strings together and compares code points at the first place they differ.
Sorting a list of words is that same comparison, over and over.

</details>

## Acceptance checklist

- [ ] `python challenge-01-caesar-cipher.py` asks the three questions in
      order, with the exact wording in requirement 1.
- [ ] Encoding `abc` with shift `1` gives `bcd`.
- [ ] Encoding `xyz` with shift `3` gives `abc`.
- [ ] Encoding `abc` with shift `29` gives `def` — the same as shift 3.
- [ ] A shift of `0` returns the message unchanged.
- [ ] Encoding `Hello, World!` with shift `13` and decoding the result
      with shift `13` gives `Hello, World!` back.
- [ ] Decoding `Khoor, Zruog!` with shift `3` gives `Hello, World!`, and
      so does *encoding* it with shift `-3`.
- [ ] `Hello, World!` keeps its capital H, its comma, its space and its
      exclamation mark in the right places.
- [ ] Typing `three`, or pressing Enter with nothing typed, at the
      `Shift: ` prompt prints a message and asks again.
- [ ] Typing `sideways` at the `Mode` prompt prints a message and asks
      again.
- [ ] No traceback appears for any of those.
- [ ] `Result:` has two spaces after the colon.
- [ ] `y` and `Y` and `yes` all start another round; anything else
      prints `Bye!`.
- [ ] No `def` and no `try` / `except` outside the supplied `ask()`.
- [ ] Four-space indentation, `snake_case` names, a docstring at the top,
      and no `TODO` comments left.
- [ ] Committed with a message such as `Add Challenge 1: Caesar cipher`.

## Stretch

**The plain `input()` version.** The downloadable answer uses `ask()` so
that it runs with nobody at the keyboard. Strip that out and the program
is shorter, stays entirely inside Week 3 — no `def`, no `try` — and can
only ever be run by hand. Keep it as a second file, `caesar_ask.py`:

```python
"""Challenge 01 — Caesar cipher.

Encodes or decodes a single line of text with a Caesar shift.
Letters keep their case, everything else passes through untouched.
Week 3: no functions yet (that is Week 4) and no try/except (Week 6).
"""

LOWER_A = ord("a")  # 97
UPPER_A = ord("A")  # 65
DIGITS = "0123456789"

while True:
    # --- mode ---
    while True:
        mode = input("Mode (encode/decode): ").strip().lower()
        if mode in ("encode", "decode"):
            break
        print("Please type 'encode' or 'decode'.")

    # --- shift (a whole number, possibly negative) ---
    while True:
        raw_shift = input("Shift: ").strip()
        body = raw_shift[1:] if raw_shift[:1] in ("-", "+") else raw_shift
        is_whole_number = body != ""
        for ch in body:
            if ch not in DIGITS:
                is_whole_number = False
                break
        if is_whole_number:
            shift = int(raw_shift)
            break
        print("The shift must be a whole number, like 3, 0 or -3.")

    # Decoding is just encoding by the opposite shift.
    if mode == "decode":
        shift = -shift
    shift %= 26  # 3 and 29 now agree; -3 becomes 23

    # --- transform ---
    message = input("Message: ")
    pieces = []
    for ch in message:
        if "a" <= ch <= "z":
            position = ord(ch) - LOWER_A
            pieces.append(chr((position + shift) % 26 + LOWER_A))
        elif "A" <= ch <= "Z":
            position = ord(ch) - UPPER_A
            pieces.append(chr((position + shift) % 26 + UPPER_A))
        else:
            pieces.append(ch)

    result = "".join(pieces)
    print(f"Result:  {result}")

    again = input("Encode another? (y/n) ").strip().lower()
    if again not in ("y", "yes"):
        print("Bye!")
        break
    print()
```

A real session, typed at a terminal:

```text
$ python caesar_ask.py
Mode (encode/decode): encode
Shift: 3
Message: Hello, World!
Result:  Khoor, Zruog!
Encode another? (y/n) y

Mode (encode/decode): decode
Shift: 3
Message: Khoor, Zruog!
Result:  Hello, World!
Encode another? (y/n) n
Bye!
```

Identical output, and it stops dead the moment nothing is typing at it.
That trade is the whole reason the downloadable file is written the other
way.

**Brute force: break a message you do not have the key for.** There are
only 26 shifts, so print all of them and read the answer off the list.
Save as `caesar_brute.py`:

```python
"""Challenge 01 stretch — brute-force every possible Caesar shift."""

LOWER_A = ord("a")
UPPER_A = ord("A")

message = input("Message: ")

for shift in range(26):
    pieces = []
    for ch in message:
        if "a" <= ch <= "z":
            pieces.append(chr((ord(ch) - LOWER_A + shift) % 26 + LOWER_A))
        elif "A" <= ch <= "Z":
            pieces.append(chr((ord(ch) - UPPER_A + shift) % 26 + UPPER_A))
        else:
            pieces.append(ch)
    candidate = "".join(pieces)
    print(f"shift {shift:2d}: {candidate}")
```

This is the nested loop from
[Lecture 2 §11](../lecture-notes/02-loops.md): the outer loop runs 26
times and the inner loop runs once per character, so the body runs
`26 * len(message)` times. `{shift:2d}` pads the number to two columns so
the candidate plaintexts line up in a readable block.

```bash
printf 'Khoor, Zruog!\n' | python caesar_brute.py
```

```text
Message: shift  0: Khoor, Zruog!
shift  1: Lipps, Asvph!
shift  2: Mjqqt, Btwqi!
shift  3: Nkrru, Cuxrj!
shift  4: Olssv, Dvysk!
shift  5: Pmttw, Ewztl!
shift  6: Qnuux, Fxaum!
shift  7: Rovvy, Gybvn!
shift  8: Spwwz, Hzcwo!
shift  9: Tqxxa, Iadxp!
shift 10: Uryyb, Jbeyq!
shift 11: Vszzc, Kcfzr!
shift 12: Wtaad, Ldgas!
shift 13: Xubbe, Mehbt!
shift 14: Yvccf, Nficu!
shift 15: Zwddg, Ogjdv!
shift 16: Axeeh, Phkew!
shift 17: Byffi, Qilfx!
shift 18: Czggj, Rjmgy!
shift 19: Dahhk, Sknhz!
shift 20: Ebiil, Tloia!
shift 21: Fcjjm, Umpjb!
shift 22: Gdkkn, Vnqkc!
shift 23: Hello, World!
shift 24: Ifmmp, Xpsme!
shift 25: Jgnnq, Yqtnf!
```

Exactly one line is English, and it is `shift 23`. Note that the message
was *encoded* with shift 3 and reads correctly on the shift **23** line,
because `-3 % 26` is `23` — the same identity as the main program, seen
from the other end.

Twenty-six lines is why nobody uses this cipher for anything that
matters. A real key space has to be far too large to print.

**The other two stretch goals in the original brief** — reading the
message from a file, and replacing the prompts with `argparse` — need
`open()` and `def`, which are Week 6 and Week 4. Leave them until you
have those. Doing them now means copying code you cannot yet read, and
copying code you cannot read is the one habit this course is built to
prevent.
