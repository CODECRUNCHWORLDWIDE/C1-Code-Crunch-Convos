# Exercise 3 — Word Frequency

> **Topic:** counting things into a dictionary, then ranking the tally into a top-three list
> **Lecture:** [02 — Sets and Dicts](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Easy
> **Target time:** 60 minutes
> **Why this one:** counting things into a dict is the single most reused pattern in all of data work — reading logs, tallying votes, building a histogram, breaking text into words. It is also where beginners meet `KeyError` and finally understand why `.get(key, 0)` exists. The ranking half teaches the other lesson: "sort by count" is almost never the whole rule, because ties have to break *somewhere*, and if you do not say where, the data decides for you.

## The Brief

At the end of each study session the community collects one-line notes from
whoever turns up. You have a short block of that feedback, and the organisers
want to know which words keep coming up, so they know what to run more of.

Build the pipeline in three pieces:

1. **Clean.** Turn raw text into a tidy list of words. Lowercase everything so
   `Loops` and `loops` count as the same word, and knock the full stops and
   commas off the ends.
2. **Count.** Walk that list and build a dictionary: each word to how many
   times it turned up.
3. **Rank.** Turn the dictionary into a top-three list.

Three small functions, each testable on its own. That is how you should break
up every text-processing job you meet — when the answer is wrong you want to
know *which* of the three is lying.

The counting is easy. The ranking bites. Three different words appear exactly
three times each, and the obvious sort puts them in the wrong order.

One thing about the notes is deliberate and you should know about it now: they
contain a **double space**, because whoever typed them hit the space bar
twice. It is invisible on the page. It is not invisible to Python, and one of
the two obvious ways to split text into words falls straight into it.

## Starter

Create `exercise-03-word-frequency.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""exercise-03-word-frequency.py — which words keep coming up.

Tokenise text, count the words into a dict, and return the top N by
frequency with a tie-break that does not depend on the data.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
NOTES: str = (
    "Loops are fun. Loops are hard. "
    "Dicts are fast, and dicts are everywhere. "
    " Practice loops, practice dicts, practice sets!"
)

PUNCTUATION: str = ".,!?;:"


# ---- Your task ----
def normalize(text: str) -> list[str]:
    """Split text into lowercase words with edge punctuation removed.

    Empty tokens are dropped.

    Args:
        text: The raw notes.

    Returns:
        The words, lowercased, in the order they appeared.
    """
    # TODO: split on whitespace, strip PUNCTUATION from each end, lowercase
    # TODO: drop anything that is left empty
    ...


def count_words(words: list[str]) -> dict[str, int]:
    """Return a dict mapping each word to how many times it appears.

    Args:
        words: The cleaned words, in any order.

    Returns:
        A dict whose values add back up to len(words).
    """
    # TODO: build the dict with .get(word, 0) + 1
    ...


def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Return the n most frequent (word, count) pairs.

    Highest count first. Ties are broken by the word, A to Z.

    Args:
        counts: The tally to rank.
        n: How many pairs to return.

    Returns:
        Up to n (word, count) pairs, best first.
    """
    # TODO: sort .items() with a two-part key, then slice
    ...


# ---- Self-check ----
if __name__ == "__main__":
    words = normalize(NOTES)
    counts = count_words(words)

    print(f"{len(words)} words, {len(counts)} unique")
    for word, count in top_n(counts, 3):
        print(f"{word:<12}{count}")

    assert len(words) == 19
    assert len(counts) == 10
    assert sum(counts.values()) == 19
    assert counts["are"] == 4
    assert counts["practice"] == 3
    assert counts.get("missing", 0) == 0
    assert top_n(counts, 3) == [("are", 4), ("dicts", 3), ("loops", 3)]
    print("All checks passed.")
```

Five words you need before you start.

**Dict.** A dict is a set of labelled boxes. The label is the **key**, what is
in the box is the **value**. `counts["are"]` means "open the box labelled
`are`". Looking a box up does not involve reading the other boxes — a dict is
the same machine as the set from Exercise 2, with a value stored beside each
key.

**`KeyError`.** Asking for a box that does not exist. `counts["loops"]` on an
empty dict raises `KeyError: 'loops'`, because there is nothing to open.

**`.get`.** `counts.get("loops", 0)` means "open the box labelled `loops`, and
if there is no such box, hand me `0`". It never raises and it never creates
anything.

**`.items()`.** Looping over a dict gives you its **keys** and nothing else.
`counts.items()` gives you `(key, value)` pairs. Which one you ask for decides
what shape comes out, and picking the wrong one is on the bug list below.

**Tokenise.** To tokenise text is to chop it into the pieces you care about —
here, words. A **token** is one of those pieces, before you have tidied it up.
`"sets!"` is a token; `"sets"` is the word you want.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/exercises/exercise-03-word-frequency.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `normalize` lowercases every word and strips the characters in
   `PUNCTUATION` from **both ends** of each token, leaving punctuation *inside*
   a word alone. It returns exactly 19 words and no empty strings.
2. `count_words` returns a plain `dict[str, int]` with 10 keys whose values
   add back up to 19. A tally that does not add up to the word count has lost
   data.
3. `top_n` sorts by count downwards, then by word A to Z, and slices
   afterwards. It returns `(word, count)` tuples — not a dict, not a list of
   words.
4. `top_n(counts, 3)` is exactly `[("are", 4), ("dicts", 3), ("loops", 3)]`.
5. Each ranked line prints as `f"{word:<12}{count}"` — the word left-aligned
   in a twelve-character column, the count straight after.
6. Every function keeps its type hints and its docstring,
   `list[tuple[str, int]]` included.

## Constraints

- **Split with `text.split()`, not `text.split(" ")`.** Bare `.split()` splits
  on *runs* of whitespace — any mix of spaces, tabs and newlines, however
  many in a row — and throws them away. `.split(" ")` splits on each single
  space, so where two spaces meet it hands you an empty string as if it were a
  word. The notes contain exactly one double space, put there on purpose, and
  it is enough to make your word count 20 instead of 19.

- **Count with a dict, never with `words.count(w)` in a loop.** `list.count`
  reads through the whole word list every time you call it, and you would be
  calling it once per unique word. Reading and writing a dict key does not
  depend on how big the dict is. On 50,000 words the dict version measured
  0.0024 seconds and the `list.count` version 1.25 seconds — five hundred
  times slower for the same answer, from ten words of prose. The numbers are
  in *Under the hood*.

- **Use `counts.get(word, 0) + 1`, not `counts[word] += 1`.** The bare
  subscript raises `KeyError` the first time it meets any word, because `+=`
  has to *read* the box before it can add to it, and there is no box yet.
  `.get` with a default handles the first sighting and the four hundredth with
  the same line.

- **Break ties on purpose, with `key=lambda kv: (-kv[1], kv[0])`.** Python's
  sort is stable, which means tied items keep the order they arrived in. Sort
  on count alone and you still get *an* answer — just not the one asked for,
  and it changes the moment somebody edits a sentence. Determinism is what
  makes the assert mean anything.

- **Sort `counts.items()`, not `counts`.** Looping over a dict yields keys, so
  `sorted(counts, ...)` hands you back plain strings. The self-check then
  tries to unpack a five-letter word into two names and the run dies before it
  even reaches an assert.

- **No `collections.Counter` in the main solution.** `Counter(words)` plus
  `.most_common(3)` does most of this exercise in two lines. Build the tally
  by hand once, so that when you use `Counter` forever after you know exactly
  what it is doing — and you will also know the one thing it does *not* do,
  which the first stretch item shows you.

- **Do not delete keys while looping over the dict.** Python raises
  `RuntimeError: dictionary changed size during iteration`. Take a snapshot
  with `list(counts)` first, or filter the word list *before* counting, which
  is nearly always the better move.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-word-frequency.py
19 words, 10 unique
are         4
dicts       3
loops       3
All checks passed.
```

Rows two and three are the trap. `dicts`, `loops` and `practice` all appear
three times. Insertion order puts `loops` first, because it opens the text.
The rule says alphabetical, so `dicts` wins. If your output reads `loops` then
`dicts`, your sort key has one part and needs two.

## Steps

1. Create `exercise-03-word-frequency.py` and paste the starter in.
2. Write `normalize` first, and print its output before you count anything.
   Look at the list with your own eyes: nineteen items, all lowercase, no
   stray full stops, no empty strings.
3. Count the tokens by hand. `NOTES` is four sentences; count each and add
   them up. If your function says 20, you have an empty string in there and
   the constraints tell you why.
4. Write `count_words`, then print `counts` directly — ten entries is small
   enough to read. Check one by hand: `are` appears once in each of the first
   two sentences and twice in the third.
5. Write `top_n`. Try the naive one-part key first, on purpose, and see which
   order the three threes come out in. Then fix it and watch them move.
6. When `All checks passed.` prints, paste a paragraph of your own over
   `NOTES`, update the numbers in the asserts, and check the whole thing still
   holds together.

## The Solution

```python
"""exercise-03-word-frequency-solution.py — which words keep coming up.

Three functions, one job each: clean the text into words, count the words
into a dict, rank the dict into a top-N list.

The counting is `counts.get(word, 0) + 1` and nothing else. The ranking is a
two-part sort key, so words that tie on count come out in a fixed order.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
NOTES: str = (
    "Loops are fun. Loops are hard. "
    "Dicts are fast, and dicts are everywhere. "
    " Practice loops, practice dicts, practice sets!"
)

PUNCTUATION: str = ".,!?;:"


# ---- Your task ----
def normalize(text: str) -> list[str]:
    """Split text into lowercase words with edge punctuation removed.

    Empty tokens are dropped.

    Args:
        text: The raw notes.

    Returns:
        The words, lowercased, in the order they appeared.
    """
    words: list[str] = []
    for token in text.split():
        word = token.strip(PUNCTUATION).lower()
        if word:
            words.append(word)
    return words


def count_words(words: list[str]) -> dict[str, int]:
    """Return a dict mapping each word to how many times it appears.

    Args:
        words: The cleaned words, in any order.

    Returns:
        A dict whose values add back up to len(words).
    """
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Return the n most frequent (word, count) pairs.

    Highest count first. Ties are broken by the word, A to Z.

    Args:
        counts: The tally to rank.
        n: How many pairs to return.

    Returns:
        Up to n (word, count) pairs, best first.
    """
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]


# ---- Self-check ----
if __name__ == "__main__":
    words = normalize(NOTES)
    counts = count_words(words)

    print(f"{len(words)} words, {len(counts)} unique")
    for word, count in top_n(counts, 3):
        print(f"{word:<12}{count}")

    assert len(words) == 19
    assert len(counts) == 10
    assert sum(counts.values()) == 19
    assert counts["are"] == 4
    assert counts["practice"] == 3
    assert counts.get("missing", 0) == 0
    assert top_n(counts, 3) == [("are", 4), ("dicts", 3), ("loops", 3)]
    print("All checks passed.")
```

**`normalize` does three things, in a fixed order.**

`text.split()` with no argument splits on runs of whitespace and discards
them, so it can never hand you an empty token no matter how the text is
spaced. `token.strip(PUNCTUATION)` then removes characters from both ends —
and the argument is a *set of characters*, not a piece of text to look for.
`".,!?;:"` means "any of these, over and over, from each end", which is why
`"sets!"` becomes `"sets"` and why `"hard.,"` would too. Punctuation in the
middle of a word survives, which is what you want for `"don't"` and
`"e-mail"`. Then `.lower()`, so `"Loops"` and `"loops"` tally together.

The `if word:` guard drops anything that reduced to nothing — someone typing
`"..."` on its own line. With `.split()` doing the splitting, nothing in this
text reduces to nothing, so the guard never fires. Keep it anyway. The
docstring promises it, and text you have not seen yet will need it.

**`count_words` is `.get(word, 0) + 1` and nothing else.**

```python
counts[word] = counts.get(word, 0) + 1
```

Read it right to left. `.get(word, 0)` asks the dict for the current tally and
supplies `0` when the word is new; it never raises and it never writes. Add
one. Then the assignment on the left creates the box if it was missing and
overwrites it if it was not. One line handles the first sighting and the four
hundredth identically, which is why there is no `if word in counts` above it.

`counts[word] += 1` cannot work on a fresh dict, and the reason is mechanical
rather than arbitrary. `+=` on a box expands to *read it, add one, write it
back*, and the read happens first. There is nothing to read.

**`top_n` sorts the items, not the dict.** Looping over a dict yields its
**keys**, so `sorted(counts, ...)` hands you strings. You want pairs, and
`counts.items()` is what gives them to you. Then the same tuple key as
Exercise 1:

```python
key=lambda kv: (-kv[1], kv[0])
```

`kv` is a `(word, count)` pair, so `kv[1]` is the count and `kv[0]` is the
word: count downwards, word upwards. `dicts`, `loops` and `practice` all
appear three times, and without the second part of the key they come out in
insertion order — `loops` first, because it opens the text. That is *an*
answer, and it changes the moment somebody edits a sentence. The tie-break is
what makes the assert mean something.

**Ranking everything to take three is slightly wasteful, and worth it.** In
theory you could find the top three without ordering the other seven. In
practice `sorted` is one fast call inside Python itself, and the code that
picks three without sorting is longer than the saving is worth at any size you
will meet this year. Reach for the clever version when you have measured, not
before.

## Run it

Copy the worked answer on this page into `exercise-03-word-frequency.py` and run it:

```bash
python exercise-03-word-frequency.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-03-word-frequency.py`.

## Common bugs to catch

- **`KeyError: 'loops'`.** You wrote `counts[word] += 1` on a fresh dict:

  ```text
  Traceback (most recent call last):
      counts[word] += 1
      ~~~~~~^^^^^^
  KeyError: 'loops'
  ```

  The squiggle sits under `counts[word]`, which is Python showing you the
  *read* that failed rather than the addition. `'loops'` is simply the first
  word in the text — the error would name whatever came first.
  `counts.get(word, 0) + 1` fixes it in one edit.

- **`20 words, 11 unique`, and an empty string among your keys.** You used
  `text.split(" ")` **and** dropped the `if word:` guard:

  ```text
  20 words, 11 unique
  are         4
  dicts       3
  loops       3
  Traceback (most recent call last):
      assert len(words) == 19
             ^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Splitting on a literal space yields an empty token wherever two spaces meet,
  and the notes contain one double space on purpose. Notice the top three are
  still right — the phantom word only appeared once, so it never reached the
  podium. This is what a data bug usually looks like: the headline is fine and
  the totals are not. Use bare `.split()`. Keep the guard as well; belt and
  braces cost you one line.

- **`len(counts)` is 13, `counts["Loops"]` is 2 and `counts["loops"]` is 1.**
  You forgot to lowercase, so `"Loops"` and `"loops"` are two separate boxes:

  ```text
  19 words, 13 unique
  are         4
  Loops       2
  dicts       2
  Traceback (most recent call last):
      assert len(counts) == 10
             ^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Thirteen keys instead of ten: `Loops`/`loops`, `Dicts`/`dicts` and
  `Practice`/`practice` each split in two. The word count is still 19, because
  nothing was lost — it was scattered. Watch what that does to the ranking. A
  word that genuinely appears three times now shows up twice under one
  spelling and once under another, and ranks *below* a word that appears
  twice. A tally that splits its keys does not fail loudly; it quietly lies.

- **`counts["fun."]` exists.** You lowercased but did not strip punctuation.
  `"fun."`, `"hard."`, `"fast,"`, `"dicts,"` and `"sets!"` all become their own
  keys and `len(counts)` is 12. Print the dict when this happens — ten entries
  is small enough to read, and `'fun.'` sitting there with its full stop tells
  you more than the `AssertionError` does. The habit generalises: when an
  assert about a *size* fails, print the thing whose size is wrong.

- **The counts are right and the order is wrong.** You used a one-part key:

  ```text
  19 words, 10 unique
  are         4
  loops       3
  dicts       3
  Traceback (most recent call last):
      assert top_n(counts, 3) == [("are", 4), ("dicts", 3), ("loops", 3)]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  `key=lambda kv: kv[1], reverse=True` sorts by count and leaves the three-way
  tie in insertion order, so `loops` — the first word of the text — wins a tie
  it should lose. `reverse=True` cannot be rescued by adding `kv[0]` to the
  key, either: it would reverse the alphabetical part too. Negate the count
  and sort upwards on the word.

- **`ValueError: too many values to unpack (expected 2)`.** You sorted
  `counts` instead of `counts.items()`:

  ```text
  19 words, 10 unique
  Traceback (most recent call last):
      for word, count in top_n(counts, 3):
          ^^^^^^^^^^^
  ValueError: too many values to unpack (expected 2)
  ```

  This one dies in the **print loop**, before any assert runs. `top_n` handed
  back `['are', 'dicts', 'loops']` — bare strings — and `for word, count in
  ...` tried to split the three-letter string `'are'` into two names. The
  order was actually correct; the *shape* was not. Looping a dict gives keys;
  `.items()` gives pairs.

- **`TypeError: bad operand type for unary -: 'str'`.** Your key negates the
  wrong half of the pair:

  ```text
  Traceback (most recent call last):
      sorted(counts.items(), key=lambda kv: (-kv[0], kv[1]))
                                             ^^^^^^
  TypeError: bad operand type for unary -: 'str'
  ```

  `kv[0]` is the word and `kv[1]` is the count. The minus goes on the count.

- **`RuntimeError: dictionary changed size during iteration`.** You filtered
  stop words by deleting keys inside `for word in counts:`:

  ```text
  Traceback (most recent call last):
      for word in c:
                  ^
  RuntimeError: dictionary changed size during iteration
  ```

  Take a snapshot of the keys first with `list(counts)`, or — better — filter
  the word list before you count it, which never creates the problem at all.

## Under the hood

<details>
<summary>Under the hood — why a dict remembers the order you put things in</summary>

Try this and notice what does **not** happen:

```text
>>> counts
{'loops': 3, 'are': 4, 'fun': 1, 'hard': 1, 'dicts': 3, 'fast': 1, 'and': 1, 'everywhere': 1, 'practice': 3, 'sets': 1}
>>> list(counts)
['loops', 'are', 'fun', 'hard', 'dicts', 'fast', 'and', 'everywhere', 'practice', 'sets']
```

The keys came back in the order the words first appeared in the text. Every
time. On every machine. That is a promise the language makes, and it is
younger than most of the code you will read.

**The history in three lines.** Before Python 3.6, dict order was undefined
and genuinely jumbled — if you needed order you imported
`collections.OrderedDict`. Python 3.6 got a new dict layout, and keeping
insertion order fell out of it as a side effect. Python 3.7 promised it in the
language specification, which is what turned an accident into something you
are allowed to rely on.

**Why the new layout gives it to you for free.** The old dict was one big
sparse array of slots. Two-thirds of that array was empty space, on purpose —
a hash table needs room, or collisions pile up (Exercise 2's *Under the hood*
explains why). Each slot held a hash, a key and a value, so all that empty
space was three pointers wide.

The new dict splits that in two:

```text
indices:  [ -, 1, -, -, 0, -, -, 2 ]        one small number per slot
entries:  [ (hash, 'loops', 3),
            (hash, 'are',   4),
            (hash, 'fun',   1) ]            packed, in insertion order
```

The sparse part is now just a row of small integers — positions into the
second array. The actual keys and values live packed together, appended in the
order you added them, with no gaps.

Two things follow. The dict got **smaller**, by roughly a third, because the
wasteful sparse part now holds one number per slot instead of three pointers.
And looping over it walks the packed array from the start, which *is*
insertion order. Nobody had to add bookkeeping to make ordering work; it is
what walking the compact array does.

The design came from a 2012 proposal by Raymond Hettinger, and PyPy shipped it
before CPython did.

**What you may and may not rely on.**

You may rely on: a plain `dict` iterates in insertion order; `dict.fromkeys`
preserves first-seen order, which is what makes Exercise 2's one-liner work;
`**kwargs` arrives in the order it was written.

You must not rely on: `set` iteration order. Sets did **not** get this change.
A set has no values to pack, so it kept the sparse layout, and its order still
depends on hash values and is deliberately randomised for strings. That is why
Exercise 4 sorts everything before it prints.

**Deleting is where the packed array shows through.** A deleted entry leaves a
hole, marked as dead, and the array is only rebuilt when the dict next grows.
So a dict that has had keys removed and added back can look slightly odd
inside — but the order you *observe* is still the insertion order of the keys
that are actually there. If you want an ordering that survives being reordered
on purpose, `collections.OrderedDict` still exists and has a `move_to_end`
that plain dicts do not.

**And the cost table for this exercise.** Reading, writing or testing a dict
key is O(1) on average — one hash, one look — for the same reason set
membership is. `list.count(w)` is O(n): it reads the whole list. Counting with
`list.count` runs one full scan per unique word, and the vocabulary grows with
the text, so it gets quadratically worse. On 50,000 words with a 2,000-word
vocabulary, CPython 3.13.2:

```text
python      : 3.13.2
n           : 50000 words, 2000 unique
dict .get   : 0.0024 s
list.count  : 1.2504 s
ratio       : 510x
```

Ten words of prose separate the two versions and a factor of five hundred
separates their running times. This is the move the whole week is about:
`list.count` **searches**, `counts.get` **looks up**.

</details>

## Acceptance checklist

- [ ] `python exercise-03-word-frequency.py` prints the summary line, three ranked rows, then `All checks passed.`
- [ ] `sum(counts.values())` equals `len(words)`.
- [ ] `normalize` uses bare `.split()` and keeps the `if word:` guard.
- [ ] `top_n` sorts `.items()` with a two-part key and slices afterwards.
- [ ] `collections` is not imported in the main solution.
- [ ] All three functions do one job each and are callable on their own.
- [ ] Type hints on all three signatures, `list[tuple[str, int]]` included.
- [ ] Committed to Git with a message like `Add Week 5 exercise 3: word frequency`.

## Stretch

- **`collections.Counter` — and the assert that fails.**

  ```python
  from collections import Counter

  counts = Counter(normalize(NOTES))
  ```

  ```text
  Counter == hand-built dict: True
  most_common(3)            : [('are', 4), ('loops', 3), ('dicts', 3)]
  assert on most_common(3)  : FAILED
  Counter + our top_n       : [('are', 4), ('dicts', 3), ('loops', 3)]
  ```

  `Counter` is a kind of `dict`, so it compares equal to the dict you built by
  hand and every other function in the file keeps working. For counting it is
  strictly better than your `count_words`: one call, and the loop runs inside
  Python itself.

  The failure is in the **ranking**. `most_common` sorts by count and leaves
  ties in the order the keys were inserted — which is exactly the one-part-key
  bug from the list above, shipped in the standard library. It is not a
  defect; `Counter` simply never promised a tie-break, so code that needs one
  has to supply it. The honest answer to this stretch item: use `Counter` for
  the counting, keep your own `top_n` for the ranking.

- **Stop words.**

  ```python
  STOP_WORDS: set[str] = {"are", "and", "the"}


  def normalize_without_stop_words(text: str) -> list[str]:
      """Tokenise, then drop the words in STOP_WORDS."""
      return [word for word in normalize(text) if word not in STOP_WORDS]
  ```

  ```text
  with stop words removed   : 14 words, 8 unique
  top 3                     : [('dicts', 3), ('loops', 3), ('practice', 3)]
  ```

  `STOP_WORDS` is a **set**, not a list, and that is the whole point of it
  being here. `word not in STOP_WORDS` runs once per word: instant against a
  set, a read-through against a list. With three stop words the difference is
  nothing; with a realistic list of two hundred it is a two-hundred-fold
  difference on the busiest line in the function, for the cost of typing `{`
  instead of `[`.

  Filter *before* counting rather than deleting keys afterwards. Notice what
  removing `are` did to the ranking: the top three are now a clean three-way
  tie broken alphabetically, which shows the tie-break off better than the
  original data does.

- **`bottom_n` — the words nobody repeats.**

  ```python
  def bottom_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
      """Return the n least frequent (word, count) pairs, ties A to Z."""
      ranked = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]))
      return ranked[:n]
  ```

  ```text
  bottom 3                  : [('and', 1), ('everywhere', 1), ('fast', 1)]
  words appearing once      : 6
  ```

  One character changes: the minus goes away, so count sorts upwards. The word
  part stays as it was, because "A to Z" did not become "Z to A" just because
  the counts flipped — and that is exactly the mistake `reverse=True` would
  have made for you. Six of the ten words appear once, which is what
  word-frequency data always looks like: a short head of common words and a
  long tail of things said once.

When your top three are right, move on to
[Exercise 4 — Set Operations](./exercise-04-set-operations.md).
