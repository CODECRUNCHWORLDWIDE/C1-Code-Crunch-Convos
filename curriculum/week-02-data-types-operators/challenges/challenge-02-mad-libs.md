# Challenge 2 — Mad Libs Generator

> **Topic:** reading seven strings, cleaning each one at the door, and dropping them into a multi-line template
> **Lecture:** [02 — Operators and Strings](../lecture-notes/02-operators-and-strings.md)
> **Difficulty:** starter
> **Target time:** 30–60 minutes
> **Why this one:** a multi-line string is *one value*, not a stack of `print` calls, and this is the challenge that makes you feel the difference. Once the story is a single string you can save it, measure it, or hand it to something else — which is exactly what the stretch goals do.

## The Brief

Mad Libs is an old paper word game. One person holds a story with holes
in it and asks the other for words — a noun, a verb, a place — without
showing them the sentences those words are about to land in. Then they
read the finished story out loud, and it is nonsense.

Your program plays the person holding the paper. It asks for seven
words, one at a time, and then prints the story with the words dropped
into their slots:

```text
=== Your Mad Libs Story ===

One sunny morning, a very spectacular group of ferrets decided
to visit Brooklyn. They spent the day juggling and pretending to be
Grace Hopper. After about 7 hours, everyone was hungry, so
they shared a giant plate of tacos and went home with a great story
to tell.

=== The End ===
```

Two rules make this more than seven `print` calls.

**The whole story is one string.** Not five lines printed one after the
other — one value, with newline characters inside it, printed once. You
type the line breaks in your source and they become part of the string.

**Every answer is cleaned the moment it arrives.** Somebody types
`  spectacular  ` with stray spaces and you want `spectacular`.
`.strip()` removes whitespace from both ends of a string. Call it in the
same breath as the question, and nothing further down the program ever
has to wonder whether it was done.

To prove the cleaning happened, the program echoes each word back before
it tells the story, in quotes:

```text
Got 'spectacular'
```

Quotes around a value are how you make invisible spaces visible.

## Starter

Save this as `madlibs.py` and run it before you change anything. It runs
as pasted — it asks all seven questions and then prints the heading with
no story under it.

```python
"""TODO: one line saying what this file does."""

import sys

DEMO_ADJECTIVE: str = "  spectacular"
DEMO_PLURAL_NOUN: str = "ferrets"
DEMO_PLACE: str = "Brooklyn"
DEMO_VERB_ING: str = "juggling"
DEMO_FAMOUS_PERSON: str = "Grace Hopper"
DEMO_NUMBER: str = "7"
DEMO_FOOD: str = "tacos"


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or ``demo`` when nobody answers."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


def main() -> None:
    """Collect the seven words and print the story."""
    adjective = ask("Give me an adjective: ", DEMO_ADJECTIVE).strip()
    plural_noun = ask("Give me a plural noun: ", DEMO_PLURAL_NOUN).strip()
    place = ask("Name a place: ", DEMO_PLACE).strip()
    verb_ing = ask("A verb ending in -ing: ", DEMO_VERB_ING).strip()
    famous_person = ask(
        "A famous person's name: ", DEMO_FAMOUS_PERSON
    ).strip()
    number = ask("A number: ", DEMO_NUMBER).strip()
    food = ask("A type of food: ", DEMO_FOOD).strip()

    # TODO 1: echo each cleaned word back, one per line, as
    #         Got 'spectacular'

    # TODO 2: build the whole story as ONE triple-quoted f-string, with
    #         the seven names in their slots. Watch where the quotes go.
    story = "=== Your Mad Libs Story ==="

    print(story)


if __name__ == "__main__":
    main()
```

`ask()` is given to you, and it is the same helper as in
[Challenge 1](./challenge-01-tip-calculator.md). It writes the question
to the *error stream* — the second way out of a program, used for
everything that is not the answer — then reads a line. If there is
nothing to read, it uses the demo word instead and prints it, so the file
always produces a whole session. *Constraints* says why that matters.

The first demo word has two leading spaces on purpose. That way the
automatic run proves your `.strip()` works without anybody typing
anything.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/challenges/challenge-02-mad-libs.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Ask for seven words, in this order: an adjective, a plural noun, a
   place, a verb ending in `-ing`, a famous person's name, a number, and
   a type of food. The wording is yours, as long as it says what kind of
   word you want.
2. Apply `.strip()` to every answer.
3. Echo each cleaned answer back, one per line, in the form
   `Got 'spectacular'` — the value in quotes.
4. Print the story shown in *The Brief*, with the seven words in their
   slots, using **exactly one** `print()` call and **one** triple-quoted
   f-string.
5. The story block starts with `=== Your Mad Libs Story ===`, then a
   blank line, then five lines of story, then a blank line, then
   `=== The End ===`.
6. An empty answer is allowed. The story just has a gap in it, and the
   program does not crash.
7. Every function has type hints on its parameters and its return, and a
   docstring.
8. The file ends with an `if __name__ == "__main__":` guard.

## Constraints

- **One `print()` for the story, and one f-string.** Seven prints would
  produce identical output on the screen, and that is the point of the
  rule: identical on screen, completely different in what you have. A
  single string can be put in a variable, measured with `len()`, saved to
  a file, or handed to another function. Seven prints have already
  committed to the terminal and cannot be taken back. The "save the
  story to a file" stretch goal is one line because of this constraint,
  and impossible without it.
- **Inside a triple-quoted string, indentation is content.** The opening
  `"""` sits immediately before `=== Your Mad Libs Story ===`, with no
  Enter after the quotes, and the closing `"""` immediately after
  `=== The End ===`. Push the text right to line up with the rest of the
  function and every line of your story gains those leading spaces.
- **`.strip()` on the way in, not on the way out.** Clean each value in
  the same expression that reads it. Strip only where you print and the
  printed line looks right while the stored value is still dirty — a bug
  that stays invisible until something compares the value to something
  else.
- **Echo with `!r`, not with hand-typed quotes.** `f"Got {word!r}"` asks
  Python for the value's *representation*, which for a string includes
  the quotes. It is the tool built for this job, and it never lies about
  what is in the string.
- **The questions answer themselves when nobody is typing.** `input()`
  with nothing attached to it raises `EOFError`, or sits there waiting
  for typing that is never coming, and a file that hangs cannot be run by
  anybody but you. `ask()` catches that and falls back to the demo words,
  so the downloadable file prints a full session every time. Run it in
  your own terminal and it has the real conversation. The plain-`input()`
  version, with no `ask()` at all, is under *Stretch* with its own real
  session.
- **Standard library only.** The file imports `sys` and nothing else.

## Expected output

Run with nothing attached to its input, the file answers its own
questions from the demo words. This is the real stdout on CPython
3.13.2:

```text
$ python challenge-02-mad-libs.py
Give me an adjective:   spectacular
Give me a plural noun: ferrets
Name a place: Brooklyn
A verb ending in -ing: juggling
A famous person's name: Grace Hopper
A number: 7
A type of food: tacos
Got 'spectacular'
Got 'ferrets'
Got 'Brooklyn'
Got 'juggling'
Got 'Grace Hopper'
Got '7'
Got 'tacos'
=== Your Mad Libs Story ===

One sunny morning, a very spectacular group of ferrets decided
to visit Brooklyn. They spent the day juggling and pretending to be
Grace Hopper. After about 7 hours, everyone was hungry, so
they shared a giant plate of tacos and went home with a great story
to tell.

=== The End ===
```

Look at the first question and the first echo. The question line shows
two spaces before `spectacular`, because that is what the demo word
contains. The echo shows `Got 'spectacular'` with the quotes tight
against the word. That gap between the two lines *is* the `.strip()`
working, and it is the only way to see it happen.

Run it in your own terminal and it asks you instead:

```text
$ python challenge-02-mad-libs.py
Give me an adjective: enormous
Give me a plural noun: raccoons
Name a place: the library
A verb ending in -ing: arguing
A famous person's name: Ada Lovelace
A number: 3
A type of food: dumplings
Got 'enormous'
Got 'raccoons'
Got 'the library'
Got 'arguing'
Got 'Ada Lovelace'
Got '3'
Got 'dumplings'
=== Your Mad Libs Story ===

One sunny morning, a very enormous group of raccoons decided
to visit the library. They spent the day arguing and pretending to be
Ada Lovelace. After about 3 hours, everyone was hungry, so
they shared a giant plate of dumplings and went home with a great story
to tell.

=== The End ===
```

## Steps

1. Save the Starter as `madlibs.py` and run `python madlibs.py`. Seven
   questions, then a heading with nothing after it. That is correct so
   far.
2. Fill in **TODO 1**: seven lines, each `print(f"Got {name!r}")`. Run
   it. Compare your echo lines to *Expected output*.
3. Fill in **TODO 2**, and build the story in stages. Start with just
   the first sentence:

   ```python
   story = f"""=== Your Mad Libs Story ===

   One sunny morning, a very {adjective} group of {plural_noun} decided
   """
   ```

   Run it, and look carefully at the left edge of the output. Every line
   has picked up the three spaces you indented it by. Now pull the story
   lines flush against the left margin of the file and run it again. The
   spaces are gone. That is the lesson of this challenge in fifteen
   seconds.
4. Type the rest of the story, one line at a time, running after each
   one.
5. Get the ends right. No Enter after the opening `"""`, or your output
   starts with a blank line. No Enter before the closing `"""`, or it
   ends with two blank lines — one from your string, one from `print`.
6. Run it once more and type deliberately messy answers, with spaces
   before and after. The echo lines should show the words with no spaces
   inside the quotes.
7. Commit it:

   ```bash
   git add madlibs.py
   git commit -m "Add Challenge 2: mad libs generator"
   ```

## The Solution

```python
"""Mad Libs generator using input() and f-strings.

Challenge 2, Week 2, Code Crunch Convos. Prompts for seven words,
strips the whitespace off each one, echoes them back, and prints the
finished story as a single multi-line f-string.

The questions go to the error stream and the story goes to the normal
output stream, so ``python madlibs.py > story.txt`` saves the story and
nothing else. When the input stream is already finished -- which is what
happens when a checker runs the file -- each question answers itself
from the demo words below instead of waiting for typing that is never
coming. The first demo word carries two leading spaces on purpose, so
the automatic run proves the stripping works with nobody typing.

Run it with::

    python madlibs.py
"""

import sys

DEMO_ADJECTIVE: str = "  spectacular"
DEMO_PLURAL_NOUN: str = "ferrets"
DEMO_PLACE: str = "Brooklyn"
DEMO_VERB_ING: str = "juggling"
DEMO_FAMOUS_PERSON: str = "Grace Hopper"
DEMO_NUMBER: str = "7"
DEMO_FOOD: str = "tacos"


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or ``demo`` when nobody answers.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on when the input stream has
            already ended.

    Returns:
        The line that was typed, or ``demo``. A demo answer is echoed
        after the prompt on the normal output stream, so the printed
        session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


def main() -> None:
    """Collect the seven words and print the story."""
    adjective = ask("Give me an adjective: ", DEMO_ADJECTIVE).strip()
    plural_noun = ask("Give me a plural noun: ", DEMO_PLURAL_NOUN).strip()
    place = ask("Name a place: ", DEMO_PLACE).strip()
    verb_ing = ask("A verb ending in -ing: ", DEMO_VERB_ING).strip()
    famous_person = ask(
        "A famous person's name: ", DEMO_FAMOUS_PERSON
    ).strip()
    number = ask("A number: ", DEMO_NUMBER).strip()
    food = ask("A type of food: ", DEMO_FOOD).strip()

    print(f"Got {adjective!r}")
    print(f"Got {plural_noun!r}")
    print(f"Got {place!r}")
    print(f"Got {verb_ing!r}")
    print(f"Got {famous_person!r}")
    print(f"Got {number!r}")
    print(f"Got {food!r}")

    story = f"""=== Your Mad Libs Story ===

One sunny morning, a very {adjective} group of {plural_noun} decided
to visit {place}. They spent the day {verb_ing} and pretending to be
{famous_person}. After about {number} hours, everyone was hungry, so
they shared a giant plate of {food} and went home with a great story
to tell.

=== The End ==="""

    print(story)


if __name__ == "__main__":
    main()
```

**One `print()`, one string, seven line breaks.** The triple-quoted
f-string is a single value that happens to contain newline characters.
The line breaks you typed in the source *are* those newlines. That is why
`story` can be assigned to a name at all — and why the "save it to a
file" stretch goal is one extra line rather than a rewrite.

**Where the quotes sit is the whole formatting.** The opening `"""` is
immediately followed by `=== Your Mad Libs Story ===`, on the same line.
The closing `"""` immediately follows `=== The End ===`. Press Enter
after the opening quotes and the string begins with a newline, so your
output gains a blank first line. Press Enter before the closing quotes
and it ends with one, and `print()` adds its own on top, so you get two.
This is also why the story sits jammed against the left margin while
everything around it is indented: inside a triple-quoted string,
whitespace is content, not layout.

**`!r` is a conversion flag, and it does the quoting for you.**
`f"Got {adjective!r}"` runs `repr()` on the value before formatting it,
and `repr()` of a string includes the quotes. So `Got 'spectacular'`
comes out with no quote characters typed anywhere in your source. The
same trick is what lecture 3 section 3 recommends for error messages, for
the same reason: it makes stray whitespace visible. If your `.strip()`
were missing, the echo would read `Got '  spectacular'` and the bug
would announce itself.

One honest caveat. `repr()` switches to double quotes when the string
itself contains a single quote, so a person named `Grace O'Malley` echoes
as `Got "Grace O'Malley"`. If you want single quotes in every case, write
`f"Got '{famous_person}'"` and accept `Got 'Grace O'Malley'`. Both are
defensible. `!r` is the one that never lies about the contents.

**`.strip()` gives you a new string.** Strings in Python cannot be
changed once they exist — lecture 2 section 5.4 — so `raw.strip()` does
not clean `raw`, it hands you a cleaned copy. That is why the call is
chained straight onto `ask()`: there is no reason to keep the dirty
version around. A bare `raw.strip()` on a line of its own does nothing at
all, and gives you no error to warn you.

**Empty answers are fine, on purpose.** `"".strip()` is `""`, and
dropping an empty string into the template just leaves a gap.
Requirement 6 allows it, so there is no guard. Do not add a loop that
nags the user; that is not what was asked for, and looping is Week 3.

**`ask()` reads a line and has an answer ready if there is none.** It
prints the question to `sys.stderr` with `end=""` so the cursor stays put,
and `flush=True` so the text appears before the program starts waiting —
the error stream holds unfinished lines in a buffer otherwise, and a
question that arrives after you have answered it is no use. Then
`input()` reads one line. When the stream has already ended, `input()`
raises `EOFError`, and the `except` prints the question and the demo word
together on the normal output stream and hands the word back.

## Download and run

Download [challenge-02-mad-libs-solution.py](./challenge-02-mad-libs-solution.py) and run
it:

```bash
python challenge-02-mad-libs-solution.py
```

In your own terminal it asks you the seven questions. Run by a script, or
with its input closed, it answers itself from the demo words.

You can also feed it seven answers from the shell:

```bash
printf 'tiny\ncats\nMiami\nsinging\nAda Lovelace\n4\npizza\n' | python challenge-02-mad-libs-solution.py
```

Because the questions go to the error stream, `>` saves the story and the
echo lines on their own:

```bash
python challenge-02-mad-libs-solution.py > story.txt
```

In your own project, save the same code as `madlibs.py`.

## Common bugs to catch

**The story is indented.** You lined the text up with the rest of the
function:

```python
    story = f"""
        === Your Mad Libs Story ===

        One sunny morning, a very {adjective} group of {plural_noun} decided
    """
```

Every line comes out with eight leading spaces, and there is a blank line
at the top from the Enter after the opening quotes. Nothing is broken;
everything between the quotes is literal text and you literally typed
those spaces. Keep the content flush left, or look up
`textwrap.dedent()`, which is in the standard library and exists for
exactly this.

**A `<built-in method ...>` appears in your story.**

```bash
python -c "raw='  hi  '; print(f'Got {raw.strip!r}')"
```

```text
Got <built-in method strip of str object at 0x00000262DD5EB150>
```

You wrote `.strip` without the parentheses, so you referred to the method
instead of calling it. No exception, no traceback, just nonsense in the
output. Whenever a value renders as `<built-in method …>`, you forgot a
pair of `()`.

**The words land in the wrong holes.** You switched to `%` or to
`"...".format(a, b, c)` with positional slots, and slot four got the
value meant for slot five. Nothing raises, because every value is a
string and every slot accepts a string, so you get a trip to tacos and a
plate of Brooklyn. Named slots that read like the sentence are the whole
argument for f-strings.

**`SyntaxError: unterminated triple-quoted string literal`.** You have an
odd number of `"""`, usually because the closing one is missing. The
error points at the *end* of the file, not at the mistake, because Python
read all the way there still waiting for the partner quotes.

**A stray blank line at the top or the bottom.** Count your Enters
against *The Solution*. Enter after the opening `"""` puts one at the
top. Enter before the closing `"""` puts one at the bottom, and `print`
adds another.

**`EOFError: EOF when reading a line`** in a version you wrote with plain
`input()`, run by something that is not a keyboard:

```text
Traceback (most recent call last):
  File "madlibs.py", line 8, in <module>
    main()
    ~~~~^^
  File "madlibs.py", line 4, in main
    adjective = input("Give me an adjective: ").strip()
                ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
```

`input()` raises this when there is nothing left to read, which is also
what Ctrl+D — Ctrl+Z on Windows — does. It is not a bug in your program.
It is the reason the downloadable file uses `ask()`.

## Under the hood

<details>
<summary>Under the hood — what an f-string really is, and what a template is not</summary>

An f-string is not a string with magic in it. It is a **syntax**, and
Python turns it into instructions while it is reading your file, long
before the program runs. Ask Python to show you:

```bash
python -c "import dis
def f(a, b): return f'{a} and {b}'
dis.dis(f)"
```

```text
  3           RESUME                   0
              LOAD_FAST                0 (a)
              FORMAT_SIMPLE
              LOAD_CONST               1 (' and ')
              LOAD_FAST                1 (b)
              FORMAT_SIMPLE
              BUILD_STRING             3
              RETURN_VALUE
```

Read it as a recipe. Load `a`, format it. Load the literal text
`' and '`. Load `b`, format it. Build one string out of those three
pieces. There is no `{` anywhere in the finished program — the braces
were instructions to the compiler, and they are gone by the time
anything runs. That is why an f-string is fast, and why the names inside
the braces are ordinary variable lookups that fail with `NameError` like
any other.

Three consequences follow, and all three surprise people.

**An f-string cannot be stored and used later.** This does nothing
useful:

```bash
python -c "adjective = 'tiny'
template = f'a very {adjective} cat'
adjective = 'enormous'
print(template)"
```

```text
a very tiny cat
```

The substitution happened on the line where the f-string was written.
Changing `adjective` afterwards changes nothing, because there is no
longer a slot to fill.

**A string that arrives from somewhere else is never an f-string.** A
line read from a file, typed by the user, or stored in a variable is just
characters. The `f` has to be in your source code. That is why you cannot
put your Mad Libs story in `story.txt` and expect `{adjective}` to fill
itself in.

**So how do you fill in a template you did not write?** With
`str.format_map`, which takes a dictionary of names and fills the slots
at run time:

```bash
python -c "
words = {'adjective': 'tiny', 'plural_noun': 'cats'}
template = 'a very {adjective} group of {plural_noun}'
print(template.format_map(words))"
```

```text
a very tiny group of cats
```

Here the braces survive into the running program as ordinary characters,
and `format_map` scans the string looking for them, pulls each name out,
looks it up in the dictionary, applies any format spec after a colon, and
glues the pieces together. All of that work happens every single time you
call it — which is the trade. An f-string does its work once, at compile
time, and cannot be changed. A template does its work on every call, and
can come from anywhere.

**What `format_map` does with a missing name.** It raises, and the
message names the slot:

```bash
python -c "print('{a} and {b}'.format_map({'a': 1}))" 2>&1 | tail -1
```

```text
KeyError: 'b'
```

The interesting part is *how* it looks the name up: `format_map` uses the
mapping directly, exactly as given, instead of copying it into keyword
arguments the way `format(**words)` does. That means you can hand it a
dictionary that knows how to answer for keys it does not have:

```bash
python -c "
class Blanks(dict):
    def __missing__(self, key):
        return '____'

print('{a} and {b}'.format_map(Blanks(a='ferrets')))"
```

```text
ferrets and ____
```

`__missing__` is the method Python calls on a `dict` subclass when a key
is absent. Forty seconds of work turns a strict template into a forgiving
one, and it is impossible with `format(**words)`, because `**` copies the
keys into a plain argument list before the template ever sees them.

**Which should you use?** In this challenge, the f-string, every time:
you wrote the story, you know the names, and the compiler doing the work
once is free. Reach for `format_map` the moment the template stops being
yours — read from a file, chosen from a menu, translated, edited by
somebody who does not write Python. The "two stories" stretch goal below
is the first step down that road, and a fifth or sixth story is the point
where a dictionary of templates beats another branch.

</details>

<details>
<summary>Under the hood — what strip really removes, and the one that surprises everyone</summary>

`str.strip()` with no argument removes every character Python considers
whitespace from both ends: space, tab, newline, carriage return, form
feed, vertical tab, and a handful of Unicode spaces. That newline and
carriage return matter more than they look. `input()` has already removed
the newline that ended the line, but text pasted from a Windows file
carries a `\r` too, and stripping quietly fixes a whole category of
cross-platform bug.

With an argument, it does something people routinely get wrong. The
argument is a **set of characters to remove**, not a prefix:

```bash
python -c "print(repr('banana'.strip('ban')))"
```

```text
''
```

Every character in `banana` is one of `b`, `a`, `n`, so the whole string
is eaten from both ends. If you want to remove an exact prefix or suffix,
Python 3.9 added `removeprefix()` and `removesuffix()`, which are the
tools that actually do what people assume `strip()` does.

And because strings never change in place, the result has to be used:

```bash
python -c "s = '  Ada  '; s.strip(); print(repr(s))"
```

```text
'  Ada  '
```

Nothing happened, because the cleaned copy was thrown away. `s =
s.strip()` is the version that does something. This is the most common
silent no-op a beginner writes, and Python will never warn you about it.

</details>

## Acceptance checklist

- [ ] `python madlibs.py` asks for all seven words, each prompt saying
      what kind of word it wants.
- [ ] `.strip()` is applied in the same expression that reads each
      answer, not later.
- [ ] Seven echo lines appear, in the form `Got 'spectacular'`.
- [ ] Typing `  spectacular  ` produces `Got 'spectacular'` with no
      spaces inside the quotes.
- [ ] The story is built by exactly one triple-quoted f-string and
      printed by exactly one `print()`.
- [ ] The story block starts with `=== Your Mad Libs Story ===` and ends
      with `=== The End ===`, with no extra blank line at either end.
- [ ] No line of the story is indented.
- [ ] All seven words land in the right slots — read the story out loud
      and check.
- [ ] Pressing Enter without typing anything at a prompt leaves a gap in
      the story and does not crash the program.
- [ ] Every function has type hints and a docstring, and no `TODO`
      comments remain.
- [ ] The file ends with the `if __name__ == "__main__":` guard.
- [ ] Committed with a message such as
      `Add Challenge 2: mad libs generator`.

## Stretch

**The plain `input()` version.** The graded file uses `ask()` so it can
run with nobody at the keyboard. Take that out and the program is shorter
and can only ever be run by hand. Keep it as a second file,
`madlibs_ask.py`:

```python
"""Mad Libs generator using input() and f-strings."""


def main() -> None:
    """Collect the seven words and print the story."""
    adjective = input("Give me an adjective: ").strip()
    plural_noun = input("Give me a plural noun: ").strip()
    place = input("Name a place: ").strip()
    verb_ing = input("A verb ending in -ing: ").strip()
    famous_person = input("A famous person's name: ").strip()
    number = input("A number: ").strip()
    food = input("A type of food: ").strip()

    print(f"Got {adjective!r}")
    print(f"Got {plural_noun!r}")
    print(f"Got {place!r}")
    print(f"Got {verb_ing!r}")
    print(f"Got {famous_person!r}")
    print(f"Got {number!r}")
    print(f"Got {food!r}")

    story = f"""=== Your Mad Libs Story ===

One sunny morning, a very {adjective} group of {plural_noun} decided
to visit {place}. They spent the day {verb_ing} and pretending to be
{famous_person}. After about {number} hours, everyone was hungry, so
they shared a giant plate of {food} and went home with a great story
to tell.

=== The End ==="""

    print(story)


if __name__ == "__main__":
    main()
```

A real session, typed at a terminal, answering the first question with
`  spectacular  ` and the deliberate spaces:

```text
$ python madlibs_ask.py
Give me an adjective:   spectacular
Give me a plural noun: ferrets
Name a place: Brooklyn
A verb ending in -ing: juggling
A famous person's name: Grace Hopper
A number: 7
A type of food: tacos
Got 'spectacular'
Got 'ferrets'
Got 'Brooklyn'
Got 'juggling'
Got 'Grace Hopper'
Got '7'
Got 'tacos'
=== Your Mad Libs Story ===

One sunny morning, a very spectacular group of ferrets decided
to visit Brooklyn. They spent the day juggling and pretending to be
Grace Hopper. After about 7 hours, everyone was hungry, so
they shared a giant plate of tacos and went home with a great story
to tell.

=== The End ===
```

Identical output, and it stops with an `EOFError` the moment nothing is
typing at it. That trade is why the downloadable file is written the
other way.

**All four of the original stretch goals at once:** a title-cased name, a
second story to choose between, a one-word guard on the adjective, and
the finished story saved to a file.

```python
"""Mad Libs, stretch edition: two templates, title-case, guard, save to file."""

OUTPUT_FILE: str = "my_madlib.txt"


def ask_single_word(prompt: str) -> str:
    """Ask for one word; if the answer has spaces, ask exactly once more."""
    answer = input(prompt).strip()
    if " " in answer:
        print("  One word please - I'll ask once more.")
        answer = input(prompt).strip()
    return answer


def main() -> None:
    """Play the chosen template and save the result."""
    pick = input("Story: 1) classic  2) sci-fi  > ").strip()

    adjective = ask_single_word("Give me an adjective: ")
    plural_noun = input("Give me a plural noun: ").strip()
    place = input("Name a place: ").strip()
    verb_ing = input("A verb ending in -ing: ").strip()
    famous_person = input("A famous person's name: ").strip().title()
    number = input("A number: ").strip()
    food = input("A type of food: ").strip()

    if pick == "2":
        story = f"""=== Your Mad Libs Story ===

The cargo hauler dropped out of warp above {place}, its hold full of
{plural_noun}. The {adjective} crew spent the next {number} cycles
{verb_ing} while the navigator, a clone of {famous_person}, argued
with the galley printer about whether {food} counts as a vegetable.

=== The End ==="""
    else:
        story = f"""=== Your Mad Libs Story ===

One sunny morning, a very {adjective} group of {plural_noun} decided
to visit {place}. They spent the day {verb_ing} and pretending to be
{famous_person}. After about {number} hours, everyone was hungry, so
they shared a giant plate of {food} and went home with a great story
to tell.

=== The End ==="""

    print(story)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:
        handle.write(story + "\n")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
```

A real session:

```text
Story: 1) classic  2) sci-fi  > 2
Give me an adjective: very shiny
  One word please - I'll ask once more.
Give me an adjective: chrome
Give me a plural noun: service drones
Name a place: Titan Station
A verb ending in -ing: sulking
A famous person's name: grace hopper
A number: 12
A type of food: pierogi
=== Your Mad Libs Story ===

The cargo hauler dropped out of warp above Titan Station, its hold full of
service drones. The chrome crew spent the next 12 cycles
sulking while the navigator, a clone of Grace Hopper, argued
with the galley printer about whether pierogi counts as a vegetable.

=== The End ===
Saved to my_madlib.txt
```

And the file it left behind:

```bash
$ cat my_madlib.txt
=== Your Mad Libs Story ===

The cargo hauler dropped out of warp above Titan Station, its hold full of
service drones. The chrome crew spent the next 12 cycles
sulking while the navigator, a clone of Grace Hopper, argued
with the galley printer about whether pierogi counts as a vegetable.

=== The End ===
```

**Title-case, and its limits.** `.strip().title()` reads left to right:
strip first, so the capitalisation is applied to the trimmed text, then
title-case it. `grace hopper` becomes `Grace Hopper`. Be aware that
`.title()` is naive about apostrophes — `o'malley` becomes `O'Malley`,
which is right, but `it's` becomes `It'S`, which is not. It is a display
nicety, not a name-formatting engine.

**The one-word guard.** `" " in answer` asks whether that string contains
a space, and hands back `True` or `False`. Asking exactly once more is
what was specified: one reprompt, then take whatever you get. A `while`
loop would nag forever, and loops are Week 3 anyway.

**Saving to a file.**
`with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:` opens the
file, gives you a handle, and closes it when the block ends — even if
something raises inside. Always pass `encoding="utf-8"` on purpose: on
Windows the default is still a legacy code page, which is exactly how "it
worked on my machine" begins. `story + "\n"` adds the trailing newline
that `print()` would have added, so the file ends the way a text file
should. Week 6 covers all of this properly; this is a legal peek ahead.

**Then try it with a template instead.** Once you have two stories, write
a third — and notice that the `if` / `elif` is growing a branch per
story. Put the templates in a dictionary keyed by the menu answer, put
the seven words in a second dictionary, and print
`stories[pick].format_map(words)`. Adding a fourth story is then one
line of data and no code at all. The *Under the hood* block above is the
background you need for it.
