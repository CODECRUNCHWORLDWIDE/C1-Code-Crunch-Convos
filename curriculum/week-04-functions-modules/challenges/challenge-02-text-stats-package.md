# Challenge 2 — Text Stats Package

> **Topic:** one public function with a tidy private inside, `collections.Counter`, and sorting by two things at once
> **Lecture:** [04 — Modules and Imports](../lecture-notes/04-modules-and-imports.md)
> **Difficulty:** harder than Challenge 1, and the hard part is a tie nobody notices
> **Why this one:** it is the first time you design a module's *front door* — deciding what other files may call and what stays behind the curtain. That decision, made once, is what lets you rewrite the inside later without breaking anybody.

## The Brief

Hand your program a paragraph. It hands you back four facts about it:
how many words, how many characters, how long the average word is, and
which three words came up most.

Like Challenge 1, this is a two-file project:

- **`text_stats.py`** — the module. It exposes exactly **one** public
  function, `analyze(text)`, which returns a dictionary of the four
  facts. Everything else in the file is private plumbing.
- **`main.py`** — a demo. It holds a paragraph, calls `analyze`, and
  prints the results neatly.

The dictionary `analyze` returns has exactly four keys:

| Key | Type | What it is |
|-----|------|------------|
| `word_count` | `int` | how many words |
| `char_count` | `int` | how many characters in the original text, spaces included |
| `avg_word_length` | `float` | mean word length, rounded to 2 decimals, `0.0` when there are no words |
| `top_3_words` | `list[tuple[str, int]]` | the three commonest words, each with its count |

**What counts as a word.** Split the text on whitespace, then clean each
piece: lowercase it, and shave punctuation off the front and the back.
`Fox,` and `fox.` and `Fox` all become `fox`. Punctuation *inside* a
word stays, so `don't` stays `don't`. A piece that is nothing but
punctuation cleans down to an empty string and is thrown away.

**And now the part that is actually hard.** The top three are ordered by
count, biggest first. But two different words can have the same count,
and then you have to decide which goes first. The rule is alphabetical:

```text
[('the', 7), ('fox', 5), ('dog', 2)]
```

`dog`, `is` and `was` all appear twice in the demo paragraph. `dog`
wins third place because `d` comes before `i` and `w`. That single rule
is where most submissions quietly go wrong, because the obvious tool —
`Counter.most_common(3)` — breaks ties a different way and *sometimes
gives the right answer anyway*. More on that below, because it is the
most instructive trap in the week.

> *As a* learner who has just met `def`, `return` and `import`,
> *I want* to build a module whose insides I could throw away and
> rewrite without breaking the file that uses it,
> *so that* I find out what a public interface is.

## Starter

Two files, in a new folder called `challenge-02-text-stats/` inside
`challenges/`. Save both and run them before you change anything.

`text_stats.py`:

```python
"""TODO: one line saying what this file does."""

import string
from collections import Counter

_PUNCT = string.punctuation


def _normalize(word: str) -> str:
    """Lowercase and strip leading/trailing punctuation."""
    return word.strip(_PUNCT).lower()


def _tokenize(text: str) -> list[str]:
    """Split `text` into normalized words, dropping empties."""
    # TODO 1: normalize every whitespace-separated piece, then drop the empties.
    return text.split()


def analyze(text: str) -> dict[str, object]:
    """Return a stats dict for `text`."""
    words = _tokenize(text)
    # TODO 2: count the words with Counter.
    # TODO 3: rank them: count descending, then word ascending.
    # TODO 4: average word length, rounded to 2, and 0.0 when there are no words.
    return {
        "word_count": len(words),
        "char_count": len(text),
        "avg_word_length": 0.0,
        "top_3_words": [],
    }


def _self_test() -> None:
    """Run a small self-test over the documented edge cases."""
    # TODO 5: one case per bullet in Requirements 7.
    print("OK")


if __name__ == "__main__":
    _self_test()
```

`main.py`:

```python
"""TODO: one line saying what this file does."""

from text_stats import analyze

PARAGRAPH = """The quick brown fox jumps over the lazy dog. The dog was not amused.
The fox, however, was delighted. The fox is the fox is the fox."""


def main() -> None:
    """Analyze the demo paragraph and print each statistic."""
    stats = analyze(PARAGRAPH)
    avg = stats["avg_word_length"]
    print(f"Words: {stats['word_count']}")
    print(f"Characters: {stats['char_count']}")
    print(f"Average word length: {avg:.2f}")
    print("Top 3 words:")
    for word, count in stats["top_3_words"]:
        print(f"  {word}: {count}")


if __name__ == "__main__":
    main()
```

Run both:

```text
$ python text_stats.py
OK
```

```text
$ python main.py
Words: 27
Characters: 132
Average word length: 0.00
Top 3 words:
```

The word and character counts are already right, because `text.split()`
happens to get the count right on this paragraph even without cleaning.
The average is `0.00` and the top-three list is empty, because those are
the TODOs. `main.py` is finished — you do not need to touch it.

**`_normalize` is given to you** because the one call it makes,
`word.strip(_PUNCT).lower()`, hides a detail worth knowing rather than
guessing at. `str.strip` with a string argument does **not** remove that
substring. It removes any leading or trailing character that appears
anywhere in it, one after another, until it hits a character that does
not. That is why `hello!!!` loses all three exclamation marks in one
call, and why `don't` comes through untouched — the apostrophe is in the
middle, and `strip` only eats from the ends.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/challenges/challenge-02-text-stats-package.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Two files, `text_stats.py` and `main.py`, in one folder.
2. `text_stats.py` exposes exactly one public function:
   `analyze(text: str) -> dict[str, object]`.
3. The returned dict has exactly the four keys in the table above, with
   those types.
4. Two private helpers do the work: `_normalize(word: str) -> str`
   lowercases one word and shaves punctuation off both ends, and
   `_tokenize(text: str) -> list[str]` returns the cleaned word list
   with empties dropped.
5. Counting uses `collections.Counter`. Sorting is yours to do — see
   requirement 6.
6. `top_3_words` is ordered by count descending, and words with the same
   count are ordered alphabetically ascending. Fewer than three distinct
   words means a shorter list; never pad it.
7. `_self_test()` covers, at least: the empty string, a whitespace-only
   string, a word with trailing punctuation, a word with an apostrophe
   in the middle, and a tie that needs the alphabetical rule. It prints
   `OK` or names the first case that failed, and runs under
   `if __name__ == "__main__":`.
8. `main.py` defines `PARAGRAPH` as a triple-quoted string, imports
   `analyze`, prints each stat on its own line, and has a `main()`
   under the `__main__` guard.
9. Every function — public and private — has type hints and a one-line
   docstring. Both files have a module docstring.

## Constraints

- **One public name.** `analyze` is the module's entire contract.
  Anything else in the file starts with an underscore, which is Python's
  way of saying "this is my business, not yours". Nothing in `main.py`
  may call `_normalize` or `_tokenize`.
- **Do not use `Counter.most_common(3)` for the final list.** Use
  `Counter` to count — that is requirement 5 — then sort the counts
  yourself. `most_common` breaks ties by the order it first saw each
  word, which is not the rule requirement 6 asks for. *Common bugs to
  catch* shows exactly how this bites.
- **Sort with one `sorted` call and a tuple key**, not two passes.
  `key=lambda pair: (-pair[1], pair[0])` does descending-by-count and
  ascending-by-word at the same time. *The Solution* takes it apart.
- **`char_count` is `len(text)`** — the raw input, before any cleaning.
  Spaces and newlines are characters.
- **An empty text must not crash.** `sum(...) / len(words)` with no
  words is a division by zero. Guard it and return `0.0`.
- **Standard library only.** `string` and `collections`, both of which
  ship with Python.
- **Runs on Python 3.10 or newer**, from inside its own folder.

## Expected output

The downloadable answer is the two files folded into one, so that it
runs the moment you have it — *Download and run* says why, and *The
Solution* shows where the seam is. Real stdout on CPython 3.13.2:

```text
$ python challenge-02-text-stats-package.py
OK

Words: 27
Characters: 132
Average word length: 3.70
Top 3 words:
  the: 7
  fox: 5
  dog: 2
```

The `OK` is what `python text_stats.py` prints on its own in the
two-file version. Everything below the blank line is what
`python main.py` prints.

**Check the numbers by hand, because the point of this challenge is
that plausible numbers can be wrong.** The paragraph is two lines:

```text
The quick brown fox jumps over the lazy dog. The dog was not amused.
The fox, however, was delighted. The fox is the fox is the fox.
```

- **27 words.** Line one splits into 14 pieces, line two into 13.
- **132 characters.** Every letter, every space, the punctuation, and
  the one newline between the two lines. This is the stat that moves if
  you write the triple-quoted string differently — start the text on the
  line *after* the opening `"""` and you gain two newlines and get 134.
  Write it exactly as the starter does and you get 132.
- **`the` appears 7 times.** Two on line one (`The`, `the`), five on
  line two.
- **`fox` appears 5 times.** One on line one; four on line two, counting
  `fox,` and `fox.` once punctuation is shaved off.
- **Average 3.70.** The 27 cleaned words have 100 letters between them,
  and `100 / 27` is `3.7037…`, which rounds to `3.70`.
- **Third place is `dog`.** Three words tie on 2 — `dog`, `is` and
  `was` — and `dog` is first alphabetically.

Ask for more than three and the tie is right there:

```text
$ python -c "from main import PARAGRAPH; from text_stats import _tokenize; from collections import Counter; print(Counter(_tokenize(PARAGRAPH)).most_common(8))"
[('the', 7), ('fox', 5), ('dog', 2), ('was', 2), ('is', 2), ('quick', 1), ('brown', 1), ('jumps', 1)]
```

Three twos in a row. Your sort decides which of them is third, and
requirement 6 says it must be `dog`.

## Steps

1. Save both starter files into the folder and run them. You should see
   the two sessions above.

2. Do **TODO 1**. `_tokenize` is one line once you see it: clean every
   piece from `text.split()`, then keep the ones that are not empty.

   ```python
   return [w for w in (_normalize(raw) for raw in text.split()) if w]
   ```

   Check it at the REPL — `python -i text_stats.py`, then
   `_tokenize("Hello, world! ---")`. You want
   `['hello', 'world']`, with the `---` gone.

3. Do **TODO 4**, the average, next, because it is short and it makes
   the demo output move:

   ```python
   total_letters = sum(len(w) for w in words)
   avg = round(total_letters / len(words), 2) if words else 0.0
   ```

   Run `main.py` and you should see `3.70`.

4. Do **TODO 2** and **TODO 3** together. `counts = Counter(words)`
   gives you a dict-like thing from word to count. Then:

   ```python
   ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
   ```

   Return `ranked[:3]`. Run `main.py` and check you get `the`, `fox`,
   `dog` — in that order, with `dog` third and not `is` or `was`.

5. Prove the tiebreak actually works, because on this paragraph it
   happens to look right either way. At the REPL:

   ```text
   >>> analyze("b b a a c")["top_3_words"]
   [('a', 2), ('b', 2), ('c', 1)]
   ```

   If you get `[('b', 2), ('a', 2), ('c', 1)]`, your sort is not doing
   the alphabetical half. This is the single most useful check on the
   page.

6. Do **TODO 5**, the self-test. Five cases, one per bullet in
   requirement 7. Compare the whole dict, not one key — that way a
   change to any of the four is caught.

7. Run `python text_stats.py` and `python main.py` and compare both
   against *Expected output*.

8. Commit:

   ```bash
   git add challenges/challenge-02-text-stats/
   git commit -m "Add Challenge 2: text stats module"
   ```

## The Solution

```python
"""Text statistics: count the words in a paragraph and rank them.

Challenge 2, Week 4, Code Crunch Convos.

The project this answers is two files. ``text_stats.py`` holds ``analyze`` and
its two private helpers; ``main.py`` imports ``analyze`` and prints the demo.
This download folds both halves into one file so that it runs the moment you
save it: everything above the ``main.py half`` banner is what ``text_stats.py``
contains, and everything below it is what ``main.py`` contains. The page beside
this file shows the two-file split, and the package version -- a folder with an
``__init__.py`` in it -- that the challenge's title promises.

Nothing here asks a question, so there is no input handling to arrange. The
whole file is pure computation plus one printing function.

Run it with::

    python challenge-02-text-stats-package-solution.py
"""

import string
from collections import Counter

# --- the text_stats.py half: computation, and nothing else -----------------

_PUNCT = string.punctuation


def _normalize(word: str) -> str:
    """Lowercase and strip leading/trailing punctuation."""
    return word.strip(_PUNCT).lower()


def _tokenize(text: str) -> list[str]:
    """Split `text` into normalized words, dropping empties."""
    return [w for w in (_normalize(raw) for raw in text.split()) if w]


def analyze(text: str) -> dict[str, object]:
    """Return a stats dict for `text`."""
    words = _tokenize(text)
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    total_letters = sum(len(w) for w in words)
    avg = round(total_letters / len(words), 2) if words else 0.0
    return {
        "word_count": len(words),
        "char_count": len(text),
        "avg_word_length": avg,
        "top_3_words": ranked[:3],
    }


def _self_test() -> None:
    """Run a small self-test over the documented edge cases."""
    cases: list[tuple[str, dict[str, object]]] = [
        ("", {"word_count": 0, "char_count": 0, "avg_word_length": 0.0, "top_3_words": []}),
        ("   ", {"word_count": 0, "char_count": 3, "avg_word_length": 0.0, "top_3_words": []}),
        ("hello!!!", {"word_count": 1, "char_count": 8, "avg_word_length": 5.0,
                      "top_3_words": [("hello", 1)]}),
        ("don't", {"word_count": 1, "char_count": 5, "avg_word_length": 5.0,
                   "top_3_words": [("don't", 1)]}),
        ("b b a a c", {"word_count": 5, "char_count": 9, "avg_word_length": 1.0,
                       "top_3_words": [("a", 2), ("b", 2), ("c", 1)]}),
    ]
    for text, expected in cases:
        got = analyze(text)
        if got != expected:
            print(f"FAIL: analyze({text!r})\n  got      {got}\n  expected {expected}")
            return
    print("OK")


# --- the main.py half: printing the demo -----------------------------------

# Import choice. In the two-file version this line reads
# ``from text_stats import analyze``, because the module's whole public surface
# is that one name and repeating ``text_stats.`` in front of it says nothing.

PARAGRAPH = """The quick brown fox jumps over the lazy dog. The dog was not amused.
The fox, however, was delighted. The fox is the fox is the fox."""


def main() -> None:
    """Analyze the demo paragraph and print each statistic."""
    stats = analyze(PARAGRAPH)
    avg = stats["avg_word_length"]
    print(f"Words: {stats['word_count']}")
    print(f"Characters: {stats['char_count']}")
    print(f"Average word length: {avg:.2f}")
    print("Top 3 words:")
    for word, count in stats["top_3_words"]:
        print(f"  {word}: {count}")


if __name__ == "__main__":
    _self_test()
    print()
    main()
```

**The download is one file, and the project is two. Here is why.** Every
page in this course ships one file you can download and run. A two-file
project cannot be one download without a zip, and a zip is a thing you
have to unpack before you can read it. So the answer above is both files
stacked, with a comment banner at the seam — everything above
`--- the main.py half` is `text_stats.py`, everything below it is
`main.py`. Split it there, put `from text_stats import analyze` at the
top of the lower half, and you have the project the brief asked for.

**`sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))` is the
whole tiebreak, and it is worth reading slowly.**

`counts.items()` gives you pairs like `("fox", 5)`. `sorted` walks the
pairs and, for each one, calls your `key` function to get the thing it
should actually sort on. Here that thing is another tuple:
`(-5, "fox")`.

Python compares tuples the way you compare words: first item first, and
only look at the second if the firsts are equal. So:

- `-pair[1]` is the count with a minus sign. A bigger count becomes a
  *smaller* negative number, so sorting ascending puts the biggest count
  first. That is "descending by count", done with an ordinary ascending
  sort.
- `pair[0]` is the word, and it is only ever reached when two counts
  were equal. Then plain alphabetical order settles it.

Take `("a", 2)` and `("b", 2)`. Both keys start `-2`, so the comparison
moves to the second item, and `"a" < "b"` puts `a` first. One sort call,
two directions, no second pass. You will reach for this tuple-key trick
constantly.

Why negate instead of `reverse=True`? Because `reverse=True` reverses
*everything*, including the alphabet, and you would get `was` before
`is` before `dog`. You need one direction for the number and the other
for the word, and negating the number is how you mix them in one key.
You cannot negate a string, which is exactly why the count is the one
that gets the minus sign.

**`Counter` still does the real work; you are only replacing its sort.**
`Counter(words)` walks the list once and builds the word-to-count
mapping, which is requirement 5. What you do not use is
`most_common(3)`, because it breaks ties by whichever word it saw first.
On this particular paragraph that happens to give the right answer — see
*Common bugs to catch*, where it is the most dangerous item on the list
precisely because it looks fine.

**`_tokenize` is a list comprehension wrapped around a generator.**

```python
return [w for w in (_normalize(raw) for raw in text.split()) if w]
```

Read it inside out. `text.split()` gives raw pieces. The round brackets
make a **generator**: it produces cleaned words one at a time, on
demand, without building a list of its own. The square brackets around
the outside collect the ones that survive `if w`. Two ideas, one pass
over the text, no throwaway list in the middle.

That `if w` is doing real work. An empty string is falsy in Python, so
`if w` means "if this is not empty". A piece that was pure punctuation —
`---` — cleans down to `""` and disappears here, instead of being
counted as a word of length zero and dragging the average down.

**`avg` guards the empty case with a conditional expression.**

```python
avg = round(total_letters / len(words), 2) if words else 0.0
```

`sum(...) / 0` raises, and requirement 7 says an empty text must give
`0.0`. `if words else 0.0` reads left to right — "this, unless there are
no words, in which case zero" — and is one line where an `if` statement
would be four.

**`char_count` is `len(text)`, not the length of the cleaned words.**
The requirement says characters in the original text, spaces included,
so it is the raw input before anything happens to it. Easy marks, easy
to overthink.

**`avg = stats["avg_word_length"]` on its own line in `main.py` is not
decoration.** `analyze` is annotated `-> dict[str, object]`, so as far
as a type checker is concerned every value coming out is just some
`object`, and `f"{stats['avg_word_length']:.2f}"` gets flagged even
though it runs fine. Binding it to a local first is the cheap dodge. The
real fix is a more precise return type — a `TypedDict`, or a small
class — and that is Week 7. Notice now that a loose return type is a
cost you pay at every call site, not once.

**The underscores are the whole design.** `_normalize` and `_tokenize`
are implementation. `analyze` is the contract. If you later replace
`str.split()` with something cleverer, no caller has to change, because
no caller was ever allowed to reach in. The leading underscore is not
enforced by Python — you *can* call `text_stats._tokenize` — but it is
a universally understood sign saying "this may change without warning".
That is what a clean public surface means.

## Download and run

Download [challenge-02-text-stats-package-solution.py](./challenge-02-text-stats-package-solution.py)
and run it:

```bash
python challenge-02-text-stats-package-solution.py
```

It takes no input, so it prints the same thing every time.

**This one file is the two-file project stacked up.** It is written that
way so the download runs immediately. In your own repository, build the
real thing: a folder `challenges/challenge-02-text-stats/` holding
`text_stats.py` and `main.py`, split at the `--- the main.py half`
banner, with `from text_stats import analyze` at the top of `main.py`.
That is what the brief asks for and what gets graded.

If you want to see the internals from outside the file:

```bash
python -c "from text_stats import analyze; print(analyze('b b a a c'))"
```

```text
{'word_count': 5, 'char_count': 9, 'avg_word_length': 1.0, 'top_3_words': [('a', 2), ('b', 2), ('c', 1)]}
```

That is the tiebreak, proved in one line, on a text small enough to
check in your head.

## Common bugs to catch

**You trusted `most_common(3)` — and it looked like it worked.** This is
the most instructive bug in Week 4, so read it even if you think you
avoided it.

```python
return {"top_3_words": counts.most_common(3)}   # WRONG on ties
```

Run it on the demo paragraph and you get:

```text
[('the', 7), ('fox', 5), ('dog', 2)]
```

Which is **correct**. Not because `most_common` follows the rule, but
because `dog` happens to appear earlier in the paragraph than `is` or
`was`, and `most_common` breaks ties by first-seen order. It agreed with
the alphabet by luck.

Now run the same code on five words where luck runs out:

```text
>>> from collections import Counter
>>> c = Counter("b b a a c".split())
>>> c.most_common(3)
[('b', 2), ('a', 2), ('c', 1)]
>>> sorted(c.items(), key=lambda p: (-p[1], p[0]))[:3]
[('a', 2), ('b', 2), ('c', 1)]
```

`b` before `a`. No error, no warning, and if you only ever tested on the
demo paragraph you would never have seen it. This is why requirement 7
asks for a tie in your self-test, and why step 5 tells you to check
`"b b a a c"` specifically. A test that only passes on the happy example
is not a test.

(Why first-seen order? Because a `Counter` is a dictionary, and since
Python 3.7 a dictionary remembers the order its keys were added.
`most_common` is honest about what it does — the rule it follows is just
not the rule you were given.)

**You divided by zero on an empty text.**

```python
avg = round(sum(len(w) for w in words) / len(words), 2)   # WRONG on ""
```

```text
Traceback (most recent call last):
  File "text_stats.py", line 6, in <module>
    analyze('')
    ~~~~~~~^^^^
  File "text_stats.py", line 4, in analyze
    avg = round(sum(len(w) for w in words) / len(words), 2)
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~
ZeroDivisionError: division by zero
```

`""` and `"   "` are in requirement 7 precisely because this is where
beginners crash. Somebody will paste an empty box into your program on
day one.

**You stripped punctuation from the whole string instead of each word.**

```python
words = text.strip(_PUNCT).lower().split()   # WRONG
```

`text.strip(...)` only touches the two ends of the **entire paragraph**.
Interior `fox,` and `dog.` keep their punctuation, so `fox`, `fox,` and
`fox.` are counted as three different words and every number comes out
wrong. That `_normalize` takes one word and not a paragraph is the file
quietly stopping you from doing this.

**You returned the `Counter` instead of a list of tuples.** A `Counter`
is a `dict` subclass, so
`analyze(...)["top_3_words"] == [("the", 7), ...]` is `False` and your
own self-test fails with a message that makes no sense. Requirement 3
says `list[tuple[str, int]]`. `sorted(...)` already returns a list of
tuples — just slice it.

**You used `.isalpha()` or `.isalnum()` to decide what to strip.** Both
ask a Unicode question, not the question you need. `don't` is not
alphanumeric, so a filter built on it drops a perfectly good word.
`str.strip(_PUNCT)` asks the narrow question — "is this character one of
these specific marks, and is it at an end" — which is the one the rules
in the brief actually describe.

**You worried about whether to lowercase before or after stripping.**
Do not. `word.strip(_PUNCT).lower()` and `word.lower().strip(_PUNCT)`
give the same answer, because lowercasing never turns a letter into
punctuation. Spend the time on the tiebreak instead.

**`main.py` prints `3.7` instead of `3.70`.** `round(3.7037, 2)` gives
the float `3.7`, and printing a float shows the shortest form. The
formatting is the printer's job: `f"{avg:.2f}"`. Keep `round` in
`analyze` anyway — requirement 3 says the value in the dict is rounded,
and a caller who does arithmetic with it should get the rounded number.

## Under the hood

<details>
<summary>Under the hood — what __init__.py is for, and what a package really is</summary>

This challenge is called a *package* and asks you to build two flat
modules. That is not a mistake in the title so much as a promise about
where you are heading, so here is what the package version looks like.

A **module** is one `.py` file. A **package** is a folder of them with a
file called `__init__.py` inside:

```text
text_stats/
    __init__.py     the front door
    tokens.py       normalize + tokenize
    analysis.py     analyze
main.py
```

`__init__.py` is the file Python runs when somebody says
`import text_stats`. Its job is to decide what the package looks like
from outside:

```python
"""Text statistics: the package's front door."""

from .analysis import analyze

__all__ = ["analyze"]
```

The leading dot in `from .analysis import` means "the `analysis` module
next to me, inside this package" rather than some `analysis` module
elsewhere on the system. It is called a **relative import**, and inside
a package it is what you want.

Now `main.py` is unchanged from the two-file version:

```python
"""Demo for the text_stats package."""

from text_stats import analyze

print(analyze("the fox the fox the dog"))
```

```text
$ python main.py
{'word_count': 6, 'char_count': 23, 'avg_word_length': 3.0, 'top_3_words': [('the', 3), ('fox', 2), ('dog', 1)]}
```

That is the payoff. The caller says `from text_stats import analyze`
whether `text_stats` is one file or a folder of six. `__init__.py` is
what makes those two look identical from outside, which means you can
grow a module into a package later without touching anybody's import
line.

**A package is a module too.** Look at what you actually got:

```text
>>> import text_stats, sys
>>> text_stats
<module 'text_stats' from '.../ts/text_stats/__init__.py'>
>>> text_stats.__path__
['.../ts/text_stats']
>>> [n for n in sys.modules if n.startswith('text_stats')]
['text_stats.tokens', 'text_stats.analysis', 'text_stats']
```

The package *is* its `__init__.py`, wearing the folder's name. The one
thing it has that a plain module does not is `__path__`, the list of
places to look for things inside it. And `sys.modules` has three
entries, not one: the package and each submodule that got loaded, each
under its full dotted name.

**`__all__` is a list of names, and it does one specific thing.** It
says which names `from text_stats import *` would bring in. It does not
make anything private and it does not stop anyone reaching
`text_stats.tokens.normalize`. Think of it as a label on the front of
the box, not a lock.

**Since Python 3.3 you can leave `__init__.py` out — and mostly should
not.** A folder without one still imports, as an *implicit namespace
package*:

```text
>>> import pkg
>>> pkg
<module 'pkg' (namespace) from ['.../ns/pkg']>
>>> pkg.tools
AttributeError: module 'pkg' has no attribute 'tools'
>>> from pkg.tools import hi
>>> hi()
'hi'
```

Notice the word `namespace` in there, and notice that `pkg.tools` failed
until something imported it explicitly. Namespace packages exist so one
logical package can be spread across several folders on disk — a real
need, and not yours. Write the `__init__.py`. It makes the package a
deliberate thing with a front door, instead of a folder that happens to
have `.py` files in it.

**When to bother.** Not yet. Two files that fit on one screen do not
need a folder around them. Reach for a package when the module has grown
past a few hundred lines, or when a natural seam appears — "these four
functions are about tokenizing, those three are about ranking". The
mistake is building the folder first and finding out later that the
seams were somewhere else.

</details>

<details>
<summary>Under the hood — why sorting by a tuple works at all</summary>

`key=lambda pair: (-pair[1], pair[0])` leans on one rule: Python knows
how to compare two tuples, and it does it the way a dictionary orders
words.

```text
>>> (-2, "a") < (-2, "b")
True
>>> (-7, "zebra") < (-2, "aardvark")
True
```

The second one is the interesting one. `-7 < -2`, so the comparison
stops there and never looks at the words. `zebra` sorts before
`aardvark` because its count was higher. That is the descending-by-count
rule, and it is happening entirely inside the number.

The rule Python follows: compare the first items. If one is smaller,
that tuple is smaller, and stop. If they are equal, move to the second
item and repeat. If you run out of items, the shorter tuple is smaller.
It is exactly how you would alphabetise `car`, `card` and `cart`.

**`sorted` calls your key once per item, not once per comparison.** It
builds the list of keys first, then sorts. So an expensive key function
costs you `n` calls, not `n log n` — which is why
`key=lambda w: expensive(w)` is fine and
`sorted(words, key=lambda w: words.count(w))` is not, since `count`
walks the whole list every time it is called.

**`sorted` is stable**, meaning two items whose keys compare equal come
out in the order they went in. That is a real guarantee you can lean on:
sort by one thing, then sort the result by another, and the first sort
survives inside groups of the second. It is also why sorting by a tuple
and sorting twice give the same answer — the tuple version is just one
pass instead of two, and says what it means in one line.

**What `Counter` is doing while you are not looking.** It is a `dict`
subclass with a counting constructor. `Counter(words)` walks the list
once and adds one to a dictionary entry per word, so counting 27 words
takes 27 steps, not 27 × 12. Compare the version people write first:

```python
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
```

That is what `Counter` does, in the same number of steps. `Counter` is
not faster magic — it is that loop, written once, by somebody else,
with a name that says what it is for. It also gives you `most_common`,
arithmetic between counters, and a sensible `0` for a word it has never
seen instead of a `KeyError`.

</details>

## Acceptance checklist

- [ ] Two files, `text_stats.py` and `main.py`, in a folder of their own
      under `challenges/`.
- [ ] `python text_stats.py` prints `OK` and nothing else.
- [ ] `python main.py` prints `Words: 27`, `Characters: 132`,
      `Average word length: 3.70`, then `the: 7`, `fox: 5`, `dog: 2`.
- [ ] `analyze("")` returns
      `{"word_count": 0, "char_count": 0, "avg_word_length": 0.0, "top_3_words": []}`
      and does not raise.
- [ ] `analyze("   ")` gives the same, except `char_count` is `3`.
- [ ] `analyze("hello!!!")` counts one word, `hello`.
- [ ] `analyze("don't")` counts one word, `don't`, with the apostrophe
      still in it.
- [ ] `analyze("b b a a c")["top_3_words"]` is
      `[("a", 2), ("b", 2), ("c", 1)]` — `a` before `b`.
- [ ] `top_3_words` is a list of tuples, not a `Counter` and not a dict.
- [ ] A text with two distinct words returns a list of two, not a
      padded list of three.
- [ ] `text_stats.py` exposes exactly one name without a leading
      underscore: `analyze`.
- [ ] `main.py` never calls `_normalize` or `_tokenize`.
- [ ] Every function has type hints and a one-line docstring, and both
      files have a module docstring.
- [ ] Both files end with `if __name__ == "__main__":`.
- [ ] No `TODO` comments left.
- [ ] Committed with a message such as
      `Add Challenge 2: text stats module`.

## Stretch

**A `top_n` count, a stop-words filter, and the longest word.** All
three fit in one signature. Note that the extras come after a bare `*`,
which makes them **keyword-only** — callers must write
`analyze(text, top_n=5)` and cannot write `analyze(text, 5, True,
False)`, which nobody could read.

```python
"""Stretch demo: top_n, stop-words filter, longest word."""

import string
from collections import Counter

_PUNCT = string.punctuation
_STOPWORDS = frozenset({"a", "an", "and", "is", "of", "or", "the", "to", "was"})


def _normalize(word: str) -> str:
    """Lowercase and strip leading/trailing punctuation."""
    return word.strip(_PUNCT).lower()


def _tokenize(text: str, remove_stopwords: bool = False) -> list[str]:
    """Split `text` into normalized words, optionally dropping stop-words."""
    words = [w for w in (_normalize(raw) for raw in text.split()) if w]
    if remove_stopwords:
        words = [w for w in words if w not in _STOPWORDS]
    return words


def analyze(
    text: str,
    *,
    top_n: int = 3,
    remove_stopwords: bool = False,
    include_longest: bool = False,
) -> dict[str, object]:
    """Return a stats dict for `text`, with optional extras."""
    words = _tokenize(text, remove_stopwords)
    ranked = sorted(Counter(words).items(), key=lambda pair: (-pair[1], pair[0]))
    avg = round(sum(len(w) for w in words) / len(words), 2) if words else 0.0
    stats: dict[str, object] = {
        "word_count": len(words),
        "char_count": len(text),
        "avg_word_length": avg,
        f"top_{top_n}_words": ranked[:top_n],
    }
    if include_longest:
        stats["longest_word"] = max(words, key=len) if words else ""
    return stats
```

Verified output on the demo paragraph:

```text
{'word_count': 27, 'char_count': 132, 'avg_word_length': 3.7, 'top_5_words': [('the', 7), ('fox', 5), ('dog', 2), ('is', 2), ('was', 2)]}
{'word_count': 16, 'char_count': 132, 'avg_word_length': 4.31, 'top_3_words': [('fox', 5), ('dog', 2), ('amused', 1)], 'longest_word': 'delighted'}
```

Two design decisions in there worth arguing about with somebody.

The key is `f"top_{top_n}_words"`, so `top_n=5` produces a `top_5_words`
key. That keeps the key honest about what is in it, but it means a
caller cannot look up a fixed name — they have to build the string too.
The alternative is to call it `top_words` whatever `n` is, which is
kinder to callers and less faithful to the original spec. Either is
defensible. Pick one and say why in the docstring.

And `char_count` stays `132` even with stop-words removed, because it
measures the input, not the tokens. If you think it should change, that
is a question about the spec, not a bug — and the answer is to write
your reading down where the next person will see it.

`_STOPWORDS` is a `frozenset` for two reasons: checking membership in a
set is fast no matter how long the set gets, and `frozenset` cannot be
modified, which is what you want from a constant sitting at module
level where anything could reach it.

**Read the text from a file with `argparse`.**

```python
"""Demo for the text_stats module, with an optional --file flag."""

import argparse
from pathlib import Path

from text_stats import analyze

PARAGRAPH = """The quick brown fox jumps over the lazy dog. The dog was not amused.
The fox, however, was delighted. The fox is the fox is the fox."""


def load_text(path: str | None) -> str:
    """Return the file's text, or the built-in demo paragraph when path is None."""
    if path is None:
        return PARAGRAPH
    return Path(path).read_text(encoding="utf-8")


def main() -> None:
    """Parse flags, analyze the chosen text, and print each statistic."""
    parser = argparse.ArgumentParser(description="Print text statistics.")
    parser.add_argument("--file", help="path to a UTF-8 text file to analyze")
    args = parser.parse_args()
    stats = analyze(load_text(args.file))
    avg = stats["avg_word_length"]
    print(f"Words: {stats['word_count']}")
    print(f"Characters: {stats['char_count']}")
    print(f"Average word length: {avg:.2f}")
    print("Top 3 words:")
    for word, count in stats["top_3_words"]:
        print(f"  {word}: {count}")


if __name__ == "__main__":
    main()
```

`load_text` exists so that the flag handling stays one line. Passing
`None` for "no file given" and branching inside a small named function
is far easier to check than an `if args.file:` buried in the middle of
`main`. Always pass `encoding="utf-8"` when you read a file — the
default differs between Windows and Linux and will bite you on somebody
else's machine. (Reading files properly is Week 6; take this as a
preview.)

```bash
printf 'to be or not to be\n' > sample.txt
python main.py --file sample.txt
```

```text
Words: 6
Characters: 19
Average word length: 2.17
Top 3 words:
  be: 2
  to: 2
  not: 1
```

And the help text `argparse` writes for you, for free:

```bash
python main.py --help
```

```text
usage: main.py [-h] [--file FILE]

Print text statistics.

options:
  -h, --help   show this help message and exit
  --file FILE  path to a UTF-8 text file to analyze
```

**Turn it into the package** from the *Under the hood* block above:
`text_stats/__init__.py`, `text_stats/tokens.py`,
`text_stats/analysis.py`. The test to pass is that `main.py` does not
change by a single character. If it does, your `__init__.py` is not
doing its job.

When you finish, commit and move on to the
[mini-project](../mini-project/README.md).
