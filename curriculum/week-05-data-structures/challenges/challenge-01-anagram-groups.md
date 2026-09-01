# Challenge 1 — Anagram Groups

> **Topic:** giving each group a name you can compute, so the dict can find it for you
> **Lecture:** [02 — Sets and Dicts](../lecture-notes/02-sets-and-dicts.md) and [03 — Comprehensions and Big-O](../lecture-notes/03-comprehensions-and-big-o.md)
> **Difficulty:** the code is seven lines; seeing *which* seven is the work
> **Target time:** 60–90 minutes
> **Why this one:** this is the challenge where "use a dict" stops being advice and becomes a technique. There is an obvious solution that compares everything against everything, and it passes every test on this page. There is a better one that never compares anything at all — it works out where each word belongs and puts it there. Learning to spot when a search can be turned into a lookup is the single most valuable habit this week teaches.

## The Brief

Two words are **anagrams** of each other when they are made of exactly the
same letters, the same number of times, in a different order.

- `"listen"` and `"silent"` are anagrams.
- `"evil"`, `"vile"`, `"live"` and `"veil"` are all anagrams of each other.
- `"hello"` and `"world"` are not.

Given a list of lowercase words, **put the anagrams into groups**. A word with
no anagram partner still gets a group — a group of one. The order of the
groups does not matter, and neither does the order of words inside a group.

Here is the obvious way to do it, and it is the way you are being asked not
to:

> Take a word. Walk through every group you have made so far. For each one,
> check whether this word is an anagram of the group's first word. If it is,
> add it there. If you get to the end without a match, start a new group.

That is a **search**. For every word, you look through everything you have
built. Fourteen words is nothing. Two hundred thousand words — the size of a
system dictionary — would be roughly twenty-seven billion comparisons, which
is most of an hour of a modern computer's time.

The move you want is to turn that search into a **lookup**. Instead of
*hunting* for the group a word belongs to, work out the group's **name**
directly from the word, and ask the dict for it. A dict finds a key without
reading through its other keys — that is the whole point of the machine, and
Exercise 2 explains how it manages it.

So the real question is: **what is the name of an anagram group?**

It has to be something you can compute from any member, and it has to come out
identical for every member and different for every non-member. Sit with that
for a minute before you read on. The answer is one short line of Python, and
finding it yourself is worth more than being told.

### Example input

```python
words = [
    "eat", "tea", "tan", "ate", "nat", "bat",
    "listen", "silent", "enlist",
    "evil", "vile", "live", "veil",
    "hello",
]
```

### Example output, one valid arrangement

```python
[
    ["eat", "tea", "ate"],
    ["tan", "nat"],
    ["bat"],
    ["listen", "silent", "enlist"],
    ["evil", "vile", "live", "veil"],
    ["hello"],
]
```

## Starter

Create `challenge-01-anagram-groups.py` in your `challenges/` folder and paste
this in. The checks are given; the two functions are yours.

```python
"""challenge-01-anagram-groups.py — group the anagrams together.

TODO: replace this docstring with a short paragraph saying which data
structure you chose and why. That reflection is part of the grade.
"""


def signature(word: str) -> str:
    """Return a canonical name for a word's letter multiset.

    Args:
        word: The word to name.

    Returns:
        A value that is identical for every anagram of `word` and different
        for every word that is not one.
    """
    # TODO: compute the group's name from the word itself.
    # It must be hashable -- a dict key cannot be a list.
    ...


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group the words that are anagrams of one another.

    Args:
        words: The words to group. Order is preserved within each group.

    Returns:
        One list per signature. A word with no anagram partner comes back as
        a group of one.
    """
    # TODO: one dict, one pass, no loop inside the loop.
    # groups.setdefault(key, []) hands you the list for `key`, making an
    # empty one first if that key is new.
    ...


if __name__ == "__main__":
    words = [
        "eat", "tea", "tan", "ate", "nat", "bat",
        "listen", "silent", "enlist",
        "evil", "vile", "live", "veil",
        "hello",
    ]

    groups = group_anagrams(words)

    # total word count is preserved
    assert sum(len(g) for g in groups) == len(words)

    # every group is internally consistent (sorted chars match)
    for g in groups:
        sig = sorted(g[0])
        for w in g:
            assert sorted(w) == sig

    # group sizes (sorted) should be [1, 1, 2, 3, 3, 4]
    sizes = sorted(len(g) for g in groups)
    assert sizes == [1, 1, 2, 3, 3, 4]

    # the four cases the brief calls out by name
    assert group_anagrams([]) == []                           # empty input
    assert group_anagrams(["ab", "abc"]) == [["ab"], ["abc"]]  # lengths never merge
    assert group_anagrams(["a", "a"]) == [["a", "a"]]          # exact repeats, one group
    assert group_anagrams(["bat"]) == [["bat"]]                # singletons are groups

    print("All checks passed.")

    for g in groups:
        print(g)
```

Three words you need before you start.

**Multiset.** A set holds each thing once. A **multiset** holds each thing as
many times as it turned up. `"letter"` as a set is `{l, e, t, r}`; as a
multiset it is one `l`, two `e`, two `t`, one `r`. Anagrams are words with the
same multiset of letters — which is why counts matter and `"lettr"` is not an
anagram of `"letter"`.

**Canonical form.** A canonical form is one agreed spelling for a thing that
can be written many ways. Every member of the group produces the same
canonical form; nothing outside the group does. That is precisely what a
group's name has to be.

**`setdefault`.** `groups.setdefault(key, [])` means "give me the list stored
under `key`, and if there is nothing there, put an empty list there first and
give me *that*". Either way you get back **the list that lives inside the
dict**, so appending to it appends into the dict.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/challenges/challenge-01-anagram-groups.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `signature(word)` returns a value that is identical for anagrams and
   different for non-anagrams, and it must be usable as a dict key.
2. `group_anagrams(words)` returns a list of groups, using a **dict** for the
   grouping. No `for` inside a `for` over `words`.
3. `group_anagrams([])` returns `[]`, with no special case written for it.
4. Words of different lengths never end up in the same group.
5. A word with no partner comes back as a list of one.
6. Type hints on both signatures, a docstring on each, and the module
   docstring replaced with your one-paragraph reflection on why you picked the
   structure you picked.
7. The file runs and prints `All checks passed.` followed by the groups.

## Constraints

- **Use a dict for the grouping. No scan.** This is the difference between the
  challenge and a warm-up. Walking your existing groups to find the right one
  means that as the groups pile up, every new word costs more than the last —
  and on top of that the naive version re-sorts the group's first word on
  every single comparison. The dict version computes one name per word and
  hands it to the dict. One pass, and the cost per word does not depend on how
  many words came before it.

- **The signature must be hashable.** `sorted(word)` gives you a **list**, and
  a list cannot be a dict key, because a dict key has to promise not to change
  after it is filed. `"".join(sorted(word))` gives you a string, which can.
  `tuple(sorted(word))` works too, and *Under the hood* measures which of the
  two you want.

- **Do not sort the list of words.** Sorting `words` puts `"ate"`, `"eat"` and
  `"tea"` in three different places, because alphabetical order has nothing to
  do with being an anagram. Sorting the **letters inside each word** is the
  operation you want; sorting the **list of words** is not. The two are one
  character apart to type and completely different ideas.

- **Do not delete keys while looping over the dict.** If you decide to prune
  the singleton groups, `for sig in groups: ... del groups[sig]` raises
  `RuntimeError: dictionary changed size during iteration`. Take a snapshot
  with `for sig in list(groups):` first.

- **Do not write special cases for the empty list, for singletons, or for
  words of different lengths.** All three fall out of the right structure for
  free. If you find yourself adding an `if` for any of them, that is a signal
  that the structure is wrong, not that the input is awkward.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-anagram-groups.py
All checks passed.
['eat', 'tea', 'ate']
['tan', 'nat']
['bat']
['listen', 'silent', 'enlist']
['evil', 'vile', 'live', 'veil']
['hello']
```

The group order comes from dict insertion order, which Python has guaranteed
since 3.7, so it is the same on every run: groups appear in the order their
first member appeared in `words`. The brief says group order does not matter,
so a different arrangement is still correct — but if yours changes
*between runs of the same file*, something is wrong, and it is almost
certainly a set where a dict belongs.

## Steps

1. Before you write anything, answer the question in the brief on paper: what
   is the name of an anagram group? Write down your candidate and test it by
   hand on `listen`, `silent` and `hello`.
2. Try it in the REPL:

   ```text
   >>> sorted("listen")
   ['e', 'i', 'l', 'n', 's', 't']
   >>> sorted("silent")
   ['e', 'i', 'l', 'n', 's', 't']
   ```

   Same list. Now try using that list as a dict key and read the error you
   get. That error is the reason for the `"".join(...)`.
3. Write `signature`. It is one line.
4. Write `group_anagrams` with a dict and `setdefault`. It is three lines.
5. Run the file. If the sizes assert fails, print `groups` — six groups is
   small enough to read, and the wrong shape is usually obvious on sight.
6. Check the three "free" requirements deliberately: run it on `[]`, on
   `["bat"]`, and on `["ab", "abc"]`. Confirm you did not write a single line
   for any of them.
7. Write your reflection paragraph at the top. Say what you chose, what you
   rejected, and what the rejected version would have cost. That paragraph is
   the part of this challenge that is actually about you.

## The Solution

```python
"""challenge-01-anagram-groups-solution.py — group the anagrams together.

Reflection on the structure I picked, as the rubric asks for.

I chose a dict keyed by each word's sorted-letter signature because the
anagram relation is exactly "same multiset of letters", and a sorted letter
string is a canonical, hashable name for that multiset. That turns an
O(n^2) all-pairs comparison into n independent O(k log k) key computations
plus n O(1) dict insertions. A list of lists would have forced a linear
scan per word to find the right group; the dict does that lookup by hash.
"""


def signature(word: str) -> str:
    """Return a canonical name for a word's letter multiset.

    Args:
        word: The word to name.

    Returns:
        The word's letters, sorted and joined back into a string. Two words
        are anagrams exactly when their signatures are equal.
    """
    return "".join(sorted(word))


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group the words that are anagrams of one another.

    Args:
        words: The words to group. Order is preserved within each group.

    Returns:
        One list per signature, in the order each signature was first seen.
        A word with no anagram partner comes back as a group of one.
    """
    groups: dict[str, list[str]] = {}
    for word in words:
        groups.setdefault(signature(word), []).append(word)
    return list(groups.values())


if __name__ == "__main__":
    words = [
        "eat", "tea", "tan", "ate", "nat", "bat",
        "listen", "silent", "enlist",
        "evil", "vile", "live", "veil",
        "hello",
    ]

    groups = group_anagrams(words)

    # total word count is preserved
    assert sum(len(g) for g in groups) == len(words)

    # every group is internally consistent (sorted chars match)
    for g in groups:
        sig = sorted(g[0])
        for w in g:
            assert sorted(w) == sig

    # group sizes (sorted) should be [1, 1, 2, 3, 3, 4]
    sizes = sorted(len(g) for g in groups)
    assert sizes == [1, 1, 2, 3, 3, 4]

    # the four cases the brief calls out by name
    assert group_anagrams([]) == []                           # empty input
    assert group_anagrams(["ab", "abc"]) == [["ab"], ["abc"]]  # lengths never merge
    assert group_anagrams(["a", "a"]) == [["a", "a"]]          # exact repeats, one group
    assert group_anagrams(["bat"]) == [["bat"]]                # singletons are groups

    print("All checks passed.")

    for g in groups:
        print(g)
```

**The whole challenge collapses into one question, and `sorted` answers it.**

`"listen"` and `"silent"` are different strings but the same bag of letters.
You cannot use the word itself as the group's name, because two anagrams are
different strings and would land in different places. You need a **normal
form** — one value that every member produces and no outsider does.

Sorting the letters gives you exactly that, and the reason is worth saying out
loud: **sorting throws away the ordering, and the ordering is the only thing
anagrams disagree about.** What is left is the multiset, which is what the
anagram relation is defined on.

```text
>>> sorted("listen")
['e', 'i', 'l', 'n', 's', 't']
>>> sorted("silent")
['e', 'i', 'l', 'n', 's', 't']
```

**`"".join(...)` is not cosmetic.** It is the step that makes the dict
possible at all. `sorted` hands back a list, a list can be changed, so Python
refuses to let one be a dict key. A string cannot be changed, so it can.

**`setdefault` does two jobs in one line.**

```python
groups.setdefault(signature(word), []).append(word)
```

If the signature is new, it stores `signature -> []` and hands you that fresh
empty list. If the signature already exists, it hands you the existing list
and leaves it alone. Either way, what you get back is **the list object that
is sitting inside the dict**, so `.append` on it appends into the dict. That
is aliasing — two names for one object — working *for* you instead of against
you.

**`list(groups.values())` throws the names away.** The brief asks for groups,
not for a mapping. The keys were scaffolding, and scaffolding comes down.

**Three of the requirements are met by not writing code.** `"hello"` gets the
signature `"ehllo"`, nothing else shares it, so its list has one element —
singletons need no special case. Empty input never enters the loop, `groups`
stays `{}`, and `list({}.values())` is `[]`. And `"ab"` and `"abc"` have
signatures of different lengths, so they can never collide. When the right
structure makes three requirements disappear, that is the structure telling
you it fits.

**Cost.** Per word: one sort of its letters, and one dict operation whose cost
does not depend on how many words came before. The forbidden version compares
every word against every group and re-sorts on each comparison. At fourteen
words nobody can tell. At two hundred thousand it is the difference between
about a second and most of an hour — the arithmetic is in *Under the hood*.

## Download and run

Download
[challenge-01-anagram-groups-solution.py](./challenge-01-anagram-groups-solution.py)
and run it:

```bash
python challenge-01-anagram-groups-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-01-anagram-groups.py`.

## Common bugs to catch

- **`TypeError: unhashable type: 'list'`.** You used the sorted list itself as
  the key:

  ```text
  Traceback (most recent call last):
      groups.setdefault(sorted(w), []).append(w)
      ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  `sorted()` returns a list, and a list can be changed after you make it, so
  Python will not let it be a dict key — an item that could change would end
  up filed in the wrong place and never be findable again. Wrap it:
  `"".join(sorted(word))` or `tuple(sorted(word))`.

- **Every assert passes and the solution is still wrong.** This is the
  dangerous one, and it has no traceback at all:

  ```python
  groups = []
  for word in words:
      for group in groups:
          if sorted(group[0]) == sorted(word):
              group.append(word)
              break
      else:
          groups.append([word])
  ```

  That is a scan, and it passes **every check on this page**. The tests cannot
  tell you it is wrong, because it is not wrong — it is slow, in a way that
  only shows up on data larger than any test here. If your solution has a
  `for` inside a `for` over the same list, you have written a search where the
  brief asked for a lookup.

- **The groups are alphabetical rather than grouped.** You sorted `words`
  instead of sorting the letters inside each word. `sorted(words)` gives you
  `ate`, `bat`, `eat`, … — the anagrams are now further apart than they
  started.

- **`RuntimeError: dictionary changed size during iteration`.** You tried to
  prune the singletons in place:

  ```text
  Traceback (most recent call last):
      for sig in groups:
                 ^^^^^^
  RuntimeError: dictionary changed size during iteration
  ```

  A dict will not let you remove keys from underneath a loop that is walking
  it. `for sig in list(groups):` takes a snapshot of the keys first, and then
  the loop is walking a list you are not touching.

- **Counts are ignored, so `"letter"` and `"retell"` land in the same group.**
  You used `set(word)` instead of `sorted(word)` for the signature:

  ```text
  >>> set("letter") == set("retell")
  True
  >>> sorted("letter") == sorted("retell")
  False
  ```

  A set throws away *how many* of each letter there were, and anagrams care
  about that: `letter` has two `t`s and one `l`, `retell` has one `t` and two
  `l`s. `sorted` keeps the counts, because a sorted list has one entry per
  letter rather than one entry per distinct letter.

## Under the hood

<details>
<summary>Under the hood — the arithmetic behind "a second versus an hour"</summary>

Two numbers describe this problem: **n**, how many words there are, and **k**,
how long a word is. Both versions do work proportional to some combination of
them, and writing the combination down is what makes the choice obvious.

**The scan version.** For each word you walk the groups built so far. By the
time you are halfway through, that is about n/2 groups, and each comparison
sorts a k-letter word. Total work grows with **n² · k log k**.

**The dict version.** For each word you sort its k letters once, and do one
dict operation whose cost does not depend on n. Total work grows with
**n · k log k**.

The `k log k` appears in both, so it cancels out of the comparison. What
separates them is n against n². Put real numbers in:

| n | n (dict) | n² (scan) |
|---|---|---|
| 14 | 14 | 196 |
| 1,000 | 1,000 | 1,000,000 |
| 235,000 | 235,000 | 55,000,000,000 |

The last row is the macOS system word list. The dict version finishes in about
a second. The scan version is doing tens of billions of comparisons, each one
sorting a word — which is why the estimate is "most of an hour" rather than "a
bit slower".

Note what this does **not** depend on: how clever the comparison is, or how
fast your machine is. Buying a computer twice as fast moves the scan version
from an hour to half an hour. Changing the structure moves it to a second.
That is why the shape of the algorithm is the thing worth arguing about.

**Why the two group counts are the same.** Both versions produce identical
groups. The scan version is not wrong; it is *the same answer, found the
expensive way*. That is exactly why a passing test suite cannot protect you
here, and why the rubric awards points for the structure rather than the
output.

**Choosing between `"".join(sorted(word))` and `tuple(sorted(word))`.** Both
are hashable and both are canonical, so both work. Timed on the 12-letter word
`"encyclopedia"`, 200,000 repetitions, CPython 3.13.2:

```text
python      : 3.13.2
n           : 200000
sig_sorted  : 0.107 s
sig_counter : 0.499 s
ratio       : 4.7x
sizeof str signature   : 53 bytes  'accdeeilnopy'
sizeof tuple signature : 120 bytes (shallow, excludes the 10 inner tuples)
deep-ish tuple total   : 1380 bytes
```

(`sig_counter` there is the `Counter`-based signature from the stretch below,
which is the slower alternative people most often reach for.) The string wins
on both speed and size: one string is one object with a compact buffer of
characters, while a tuple of pairs is an outer tuple plus an inner tuple per
letter plus the numbers inside them.

**A signature that does not need sorting at all.** For lowercase English you
could count the 26 letters into a fixed-size tuple:

```python
def signature_counts(word: str) -> tuple[int, ...]:
    """Canonical name as 26 letter counts."""
    counts = [0] * 26
    for ch in word:
        counts[ord(ch) - ord("a")] += 1
    return tuple(counts)
```

That is proportional to **k**, with no `log k`, so on paper it beats sorting.
In practice `sorted` on a short string is one tight loop inside Python itself
while this is a Python-level loop, so for ordinary words the "worse" algorithm
wins comfortably. It only pays off for very long strings, and it stops working
entirely the moment a word has an accent, an apostrophe or a capital letter.
This is the standard shape of these arguments: the better big-O is a promise
about how things scale, not a promise that this input is big enough for the
promise to matter.

</details>

## Acceptance checklist

- [ ] `python challenge-01-anagram-groups.py` prints `All checks passed.` then six groups.
- [ ] The grouping uses a dict. The file contains no `for` inside a `for` over `words`.
- [ ] `signature` returns something hashable, and it is one line.
- [ ] No special case anywhere for empty input, singletons, or differing lengths.
- [ ] Type hints on both signatures and a docstring on each.
- [ ] The module docstring holds your own reflection paragraph, naming the
      structure you chose and what you rejected.
- [ ] Committed to Git with a message like `Add Week 5 challenge 1: anagram groups`.

## Stretch

- **A `case_sensitive` flag.**

  ```python
  def group_anagrams_ci(words: list[str], case_sensitive: bool = True) -> list[list[str]]:
      """Group anagrams, optionally ignoring case."""
      groups: dict[str, list[str]] = {}
      for word in words:
          key = word if case_sensitive else word.lower()
          groups.setdefault(signature(key), []).append(word)
      return list(groups.values())
  ```

  ```text
  case sensitive  : [['Tea'], ['ate', 'eat']]
  case insensitive: [['Tea', 'ate', 'eat']]
  ```

  Notice carefully what gets lowercased and what does not: the **key** is
  normalised, the **stored word** keeps its original spelling. People want
  `"Tea"` back as `"Tea"`. If that sounds familiar it is because Exercise 2
  made the same point with sign-up sheets — normalise for comparison, store
  what arrived. It is the shape of every case-insensitive lookup you will ever
  write.

- **Deterministic ordering — largest group first, words alphabetical inside.**

  ```python
  def group_anagrams_deterministic(words: list[str]) -> list[list[str]]:
      """Return the groups largest first, words alphabetical within each."""
      groups = group_anagrams(words)
      for group in groups:
          group.sort()
      groups.sort(key=lambda g: (-len(g), g[0]))
      return groups
  ```

  ```text
  ['evil', 'live', 'veil', 'vile']
  ['ate', 'eat', 'tea']
  ['enlist', 'listen', 'silent']
  ['nat', 'tan']
  ['bat']
  ['hello']
  ```

  Two details make this genuinely deterministic rather than merely sorted.
  Sort the words *inside* each group **before** sorting the groups, so that
  `g[0]` is a stable, meaningful tie-breaker. And use the tuple key
  `(-len(g), g[0])`, so size goes downwards and ties break alphabetically —
  the same trick as Exercise 1. Without the second element, two groups of
  equal size keep whatever order they happened to be in.

  Note that `.sort()` is fine here, unlike in Exercise 1, because these lists
  are yours: `group_anagrams` built them a moment ago and nobody else is
  holding them. The rule was never "never sort in place"; it was "never
  rearrange something you were handed".

- **Compare the sorted-string signature with a `Counter` one.**

  Before you benchmark anything: **the obvious `Counter` signature is wrong.**
  `Counter` remembers insertion order, so two anagrams produce different
  tuples:

  ```text
    tuple(Counter('eat').items()) = (('e', 1), ('a', 1), ('t', 1))
    tuple(Counter('tea').items()) = (('t', 1), ('e', 1), ('a', 1))
    equal? False
  ```

  You have to sort it to get a canonical form:
  `tuple(sorted(Counter(word).items()))`. This is an excellent bug to meet
  once, because "it's a Counter, so order doesn't matter" is a
  reasonable-sounding sentence that is simply false about `.items()`.

  With that fixed, the string signature is still about five times faster and
  much smaller — the measurements are in *Under the hood*. `Counter` earns its
  keep when you want the counts afterwards. As a pure name for a group, it is
  strictly worse.

  Reproduce it yourself:

  ```python
  import timeit

  SETUP = """
  from collections import Counter
  word = "encyclopedia"
  def sig_sorted(w):
      return "".join(sorted(w))
  def sig_counter(w):
      return tuple(sorted(Counter(w).items()))
  """

  print(timeit.timeit("sig_sorted(word)",  setup=SETUP, number=200_000))
  print(timeit.timeit("sig_counter(word)", setup=SETUP, number=200_000))
  ```

- **Find the longest anagram group in English.**

  ```python
  from pathlib import Path


  def longest_anagram_group(path: str = "/usr/share/dict/words") -> list[str]:
      """Return the largest anagram group in a newline-delimited word list."""
      words_file = Path(path)
      if not words_file.exists():
          raise FileNotFoundError(
              f"{path} not found. On Debian or Ubuntu install `wamerican`; "
              "on Windows point this at any newline-delimited word list."
          )
      words = [
          line.strip().lower()
          for line in words_file.read_text(encoding="utf-8", errors="ignore").splitlines()
          if line.strip().isalpha()
      ]
      groups = group_anagrams(sorted(set(words)))
      return max(groups, key=len)
  ```

  **Stated honestly:** this reference was written on Windows, where
  `/usr/share/dict/words` does not exist, so the answer it prints is **not**
  verified here. Do not quote a number from this page — run it and find out.

  What you can predict without running it is the *shape* of the winner: a
  short signature made of common letters, because the number of English words
  sharing a letter multiset falls away fast as words get longer.

  The `set(words)` is load-bearing. Many word lists contain both `Aaron` and
  `aaron`, which become the same word after `.lower()`, and without the
  deduplication your groups are inflated by pairs that are really one word
  twice. The `sorted(...)` only makes the output stable; it does not make it
  correct.

  And note that this runs at all *because* you used a dict. Two hundred
  thousand words is fine for one pass and hopeless for a scan.

When your groups are right, move on to
[Challenge 2 — Inventory Tracker](./challenge-02-inventory-tracker.md).
