# Homework Problem 3 — Word and Character Counter

> **Topic:** `len()`, `.replace()`, `.split()`, `.upper()`, and why string methods hand back new strings
> **Lecture:** [02 — Operators and Strings](../lecture-notes/02-operators-and-strings.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** four statistics, four single method calls, no loops allowed. The ban on loops is the lesson. Somebody has already written the code that walks a string character by character, and it is faster and shorter and correct. Learning to look for that first is most of what separates fluent Python from translated Java.

## The Brief

Read one line of text from the person at the keyboard, then print four
things about it:

- **Characters** — how long the line is, spaces and punctuation included.
- **Non-space chars** — how long it is once the spaces are taken out.
- **Words** — how many words there are.
- **Uppercase** — the same line, shouted.

```text
Characters       : 18
Non-space chars  : 16
Words            : 3
Uppercase        : HELLO THERE FRIEND
```

Each of the four is one call:

- `len(text)` counts the characters.
- `text.replace(" ", "")` builds a copy with every space swapped for
  nothing, and `len()` of that counts what is left.
- `text.split()` chops the line into a list of words, and `len()` of that
  counts them.
- `text.upper()` builds an upper-case copy.

**No loops.** You do not have `for` yet anyway, and that is deliberate. The
standard library has already counted for you.

Two of those calls need a second look before you write them.

**`len()` is a function; the other three are methods.** You can see it in
the shape: `len(text)` puts the text inside the brackets, while
`text.upper()` hangs off the end of the text with a dot. A method belongs to
the value it is attached to. A function is free-standing and takes the value
as an argument.

**None of the three methods changes `text`.** They each build a *new*
string and hand it back. `text` itself is untouched from the first line to
the last, which is exactly why the four statistics can be computed in any
order and never interfere.

## Starter

Save this as `homework-03-word-counter.py` and fill in the `TODO`s. It runs
as pasted and prints the first statistic:

```python
"""TODO: one line saying what this file does."""

LABEL_WIDTH: int = 17


def main() -> None:
    """Read one line and print four statistics about it."""
    text: str = input("Enter a line: ")

    print(f"{'Characters':<{LABEL_WIDTH}}: {len(text)}")
    # TODO: Non-space chars, using text.replace(' ', '')
    # TODO: Words, using text.split()
    # TODO: Uppercase, using text.upper()


if __name__ == "__main__":
    main()
```

`LABEL_WIDTH` is 17 because the longest label, `Non-space chars`, is fifteen
characters and needs a gap before the colon. Padding all four to the same
number is what puts the colons in a column.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/homework/problem-03-word-and-character-counter.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program reads exactly one line, using a single `input()` call.
2. It prints four lines, in the order shown in The Brief.
3. `Characters` counts everything, spaces and punctuation included.
4. `Non-space chars` counts the line with the spaces removed.
5. `Words` is correct even when there are several spaces between two words.
6. `Uppercase` prints the whole line in capitals.
7. There is no `for` and no `while` anywhere in the file.
8. `main()` is annotated `-> None`, and every variable carries a type hint.

## Constraints

- **One method call per statistic.** If a line of your code is doing two
  jobs, split it.
- **Call `split()` with no argument.** `split(" ")` looks like it does the
  same thing and does not. The difference is in Common bugs to catch, and it
  is the single most likely way to get this problem wrong while still
  passing the sample.
- **Do not strip the input.** `Characters` is defined as the length of the
  line *including* spaces, so `input().strip()` changes the answer for
  anybody who types a leading space. Read the line as it came.
- **Nested quotes have to differ.** Inside a double-quoted f-string, the
  string you pass to `.replace()` has to be single-quoted:
  `f"...{text.replace(' ', '')}..."`. Same-style quotes inside the braces
  are an error before Python 3.12, and using the opposite style is the habit
  that works everywhere.
- **No loops.** Not for counting characters, not for counting words.

## Expected output

The downloadable file below uses its built-in example line when nobody is at
the keyboard, so the run is the same every time:

```text
$ python problem-03-word-and-character-counter.py
Characters       : 18
Non-space chars  : 16
Words            : 3
Uppercase        : HELLO THERE FRIEND
```

Run the same program in your own terminal and it has the conversation
instead:

```text
Enter a line: hello there friend
Characters       : 18
Non-space chars  : 16
Words            : 3
Uppercase        : HELLO THERE FRIEND
```

Now the run that separates a correct answer from a lucky one — extra spaces
between the words:

```text
Enter a line: hello   there  friend
Characters       : 21
Non-space chars  : 16
Words            : 3
Uppercase        : HELLO   THERE  FRIEND
```

Still three words. `split(" ")` would have said seven.

## Steps

1. Activate your Week 2 environment and `cd` into your `homework/` folder.
2. Save the Starter as `homework-03-word-counter.py`.
3. Run it as pasted and type `hello there friend`. One line comes back and
   it says `18`.
4. Before you add the rest, look at what `split()` actually returns:

   ```bash
   python -c "print('hello there friend'.split())"
   ```

   ```text
   ['hello', 'there', 'friend']
   ```

   A list of three strings. `len()` of a list counts its items, which is why
   `len(text.split())` is a word count.
5. Add the three remaining lines. Each is the same shape as the first, with
   a different label and a different expression after the colon.
6. Run it with the tidy sample and compare against the block above.
7. Run it again with several spaces between the words. `Characters` and
   `Uppercase` should change; `Non-space chars` and `Words` should not.
8. Prove no method changed the original:

   ```bash
   python -c "t = 'a b'; t.upper(); print(repr(t))"
   ```

   ```text
   'a b'
   ```

9. Commit: `git add homework-03-word-counter.py` then
   `git commit -m "Add word and character counter"`.

## The Solution

```python
"""Word and character counter.

Week 2 homework, problem 3, Code Crunch Convos. One method call per
statistic, no loops.

The question goes to the error stream and the four statistics go to the
normal output stream. When nobody is at the keyboard the script uses the
example line. Save your own copy as ``homework-03-word-counter.py``.
"""

import sys

LABEL_WIDTH: int = 17

SAMPLE_TEXT: str = "hello there friend"


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str, fallback: str) -> str:
    """Return the typed line, or ``fallback`` when nobody is at the keyboard."""
    if not someone_is_typing():
        return fallback
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        return fallback


def print_report(text: str) -> None:
    """Print four statistics about ``text``, one per line."""
    print(f"{'Characters':<{LABEL_WIDTH}}: {len(text)}")
    print(f"{'Non-space chars':<{LABEL_WIDTH}}: {len(text.replace(' ', ''))}")
    print(f"{'Words':<{LABEL_WIDTH}}: {len(text.split())}")
    print(f"{'Uppercase':<{LABEL_WIDTH}}: {text.upper()}")


def main() -> None:
    """Read one line and print four statistics about it."""
    text: str = ask("Enter a line: ", SAMPLE_TEXT)
    print_report(text)


if __name__ == "__main__":
    main()
```

**Why it works.**

**`text.split()` with no argument is not the same as `text.split(" ")`.**
This is the heart of the problem. With no separator, `split()` treats *any
run of whitespace* as a single divider, and throws away whitespace at the
start and end. With a separator, it splits on every single occurrence and
keeps the empties:

```bash
python -c "print('  a   b  '.split()); print('  a   b  '.split(' '))"
```

```text
['a', 'b']
['', '', 'a', '', '', 'b', '', '']
```

Two words versus eight pieces, six of them empty. The no-argument form is
the one that answers "how many words", and it is the reason this problem
does not need a loop.

**`text.replace(" ", "")` removes spaces and only spaces.** Not tabs, not
newlines. That is exactly what the brief asked for. `input()` cannot return
a newline anyway — it stops at Enter — and a literal tab is unlikely, so for
this problem the two readings agree. If you wanted "all whitespace of any
kind" you would want `"".join(text.split())` instead, which reuses the
splitting rule above.

**Every method returns a new string, and `text` never moves.** That is why
the four lines are independent — delete one, reorder them, and the other
three still give the same answers. It is also the reason `text.upper()` on a
line by itself does nothing at all: the new string is built, handed back,
and immediately thrown away.

**`len()` counts items, whatever the items are.** For a string it counts
characters; for the list that `split()` produced it counts words. One
function, two jobs, because both types know how long they are.

**The nested quotes are legal because they differ.**
`f"...{text.replace(' ', '')}..."` puts single-quoted strings inside a
double-quoted f-string. Python 3.12 relaxed this and allows matching quotes,
but code that has to run anywhere still uses the opposite style, and it
costs nothing to keep the habit.

**One label width for four labels.** `Non-space chars` is fifteen
characters, so seventeen is the smallest width that still leaves a gap
before the colon. Padding all four to the same number is what puts the
colons in a column — the same `<` alignment Problem 1 used.

**`ask()` is the one piece the brief did not ask for.** It lets the
downloadable file run with nobody present. `sys.stdin.isatty()` asks whether
there is a real terminal with a person at it. When there is, the program
asks its question; when there is not, `ask()` hands back the example line
instead of hanging on an `input()` that will never be answered. Note that it
returns the line *raw*, with no `.strip()` — stripping would change the
`Characters` count, which is the one statistic that has to see the line
exactly as it arrived.

## Download and run

Download [problem-03-word-and-character-counter-solution.py](./problem-03-word-and-character-counter-solution.py)
and run it:

```bash
python problem-03-word-and-character-counter-solution.py
```

Run from a terminal, it asks you for a line. Run by a script or with its
input redirected, it uses the example line instead of hanging. Save your own
copy as `homework-03-word-counter.py` in your homework folder, and commit
that.

## Common bugs to catch

- **You counted words with `len(text.split(" "))`.** For the sample line it
  gives `3`, which is precisely why it survives testing. Type two spaces
  between two words and it reports `3` for a two-word line. Use the
  argument-free `split()`.
- **You called `.strip()` before counting characters.** `Characters` is
  defined as the length of the line including spaces. Stripping changes the
  answer for anybody who types a leading space, and the tidy sample will
  never catch it.
- **You expected `.upper()` to change `text`.**

  ```python
  text.upper()
  print(text)     # unchanged
  ```

  Nothing was assigned, so nothing was kept. Every "modifying" string method
  returns a new string; the returned value is the whole point.
- **You wrote a loop.** `for ch in text: ...` is banned here, and the ban is
  the lesson. Reaching for a loop when a method already exists is the most
  common way beginner Python gets long and slow.
- **`SyntaxError: f-string: unmatched '('`** on Python 3.11 or older,
  because you used double quotes inside a double-quoted f-string. Switch the
  inner pair to single quotes.
- **`AttributeError: 'str' object has no attribute 'lenght'`.** A typo in a
  method name is not caught until the line runs, because Python looks the
  name up at the last moment. Read the attribute name in the message; it is
  usually your typo spelled back at you.
- **The colons do not line up.** One of your four labels was padded to a
  different width, or you left a space before the `:` in one f-string and
  not another.

## Under the hood

<details>
<summary>Under the hood — what split really does, and the family it belongs to</summary>

`str.split()` has two quite different behaviours depending on whether you
give it a separator, and the documentation calls this out explicitly.

**With no separator** (or `None`), consecutive whitespace is treated as one
separator and leading and trailing whitespace is discarded. Whitespace means
space, tab, newline, carriage return, form feed and vertical tab.

**With a separator**, every single occurrence splits, so `n` separators give
`n + 1` pieces, empties included. That is the behaviour you want for parsing
data — `"a,,b".split(",")` giving `['a', '', 'b']` is correct, because the
middle field really is empty.

The family:

- `rsplit()` splits from the right. With `maxsplit` it is how you take the
  last piece off a path.
- `splitlines()` splits on line boundaries and understands every kind of
  line ending, which is what you want for file text and what `split("\n")`
  gets wrong on Windows files.
- `partition(sep)` splits once and always returns three pieces — before,
  separator, after — so there is no "what if it was not found" branch.
- `"".join(parts)` is the inverse. Note it is a method on the *glue*, not on
  the list, which surprises everybody once.

Word counting is genuinely harder than this problem lets on.
`"it's".split()` is one word, and so is `"state-of-the-art"`. Splitting on
whitespace is a decision, not a truth. Real text processing reaches for
`re.findall(r"\w+", text)` or a proper tokenizer, and both make different
decisions.

</details>

<details>
<summary>Under the hood — len is instant, and why an emoji can count as two</summary>

`len()` does not walk the string. A Python string knows its own length,
stored alongside the characters, so `len()` reads one number and returns.
That is true for lists, tuples, dictionaries and sets too — under the hood
`len(x)` calls `x.__len__()`, and every built-in container keeps a running
count.

```bash
python -c "print(len.__doc__.splitlines()[0])"
```

```text
Return the number of items in a container.
```

What `len()` counts for a string is **code points**, not letters as a human
would count them. Usually those are the same thing. Sometimes they are not:

```bash
python -c "print(len('cafe\u0301'), len('caf\u00e9'))"
```

```text
5 4
```

Both display as `café`. `́` is a combining acute accent that
attaches itself to the letter before it, so the first string is a plain `e`
with an accent stuck on; the second is a single pre-composed character. `unicodedata.normalize`
exists to make the two agree.

Emoji push it further. Many are built from several code points joined by an
invisible zero-width joiner, so a single picture on screen can be four or
more to `len()`.

`.upper()` has its own surprises for the same reason. German `ß`
upper-cases to `SS`, so the string gets *longer*; the Turkish dotless `ı`
needs to know the language to convert correctly. For case-insensitive
comparison, `.casefold()` is the method that handles those properly —
`.upper()` and `.lower()` are for display.

None of this affects `hello there friend`. All of it affects the moment your
program meets real text from real people, which is sooner than you think.

</details>

## Acceptance checklist

- [ ] The program reads exactly one line with one `input()` call.
- [ ] Four lines print, in the order given, with the colons in a column.
- [ ] `Characters` includes spaces and punctuation.
- [ ] `Non-space chars` matches `Characters` minus the number of spaces.
- [ ] Typing several spaces between two words still reports two words.
- [ ] `Uppercase` shows the whole line in capitals.
- [ ] There is no `for` and no `while` in the file.
- [ ] `main()` is annotated `-> None` and every variable carries a type
      hint.
- [ ] Committed with a message like `Add word and character counter`.

## Stretch

- Add a fifth statistic: how many vowels the line contains, still without a
  loop. `sum(text.lower().count(v) for v in "aeiou")` does it, and taking
  that expression apart is worth ten minutes.
- Add the average word length, to one decimal place. Watch what happens on
  an empty line, and think about what your program should do rather than
  what it does.
- Print the line reversed with `text[::-1]`, then work out what the three
  numbers in those brackets mean.
- Compare `text.replace(" ", "")` with `"".join(text.split())` on a line
  containing a tab. Type the tab with `python -c "print('a\tb')"` if your
  terminal will not let you paste one. The two answers differ, and the
  difference is the whole point of the previous Under the hood block.
- Read the string methods page at
  <https://docs.python.org/3/library/stdtypes.html#string-methods> and count
  how many of them you could have used instead of a loop.

Next: [Homework Problem 4 — Grade Letter Assigner (No `if`)](./problem-04-grade-letter-assigner-no-if.md).
