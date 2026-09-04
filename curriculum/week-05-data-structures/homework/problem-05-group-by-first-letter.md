# Homework Problem 5 — Group by first letter

> **Topic:** `setdefault`, a dict whose values are lists, and using aliasing on purpose
> **Lecture:** [02 — Sets and Dictionaries](../lecture-notes/02-sets-and-dicts.md)
> **Difficulty:** Medium
> **Target time:** 35 minutes
> **Why this one:** grouping is the single most common shape in data work — every "by category", "by day", "by customer" report in the world is this function with a different key — and it is the first time you use aliasing deliberately instead of tripping over it. One line does three jobs here, and being able to say which three is the point.

## The Brief

You have a pile of words. You want them sorted into buckets, one bucket per
starting letter.

```python
group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])
# {"a": ["apple", "ant"], "b": ["bee", "banana"], "c": ["cherry"]}
```

A dict whose values are lists. The key is the letter; the value is every word
that started with it, **in the order they arrived**. `"apple"` came before
`"ant"` in the input, so it comes before it in the bucket.

Write one function.

```python
def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    ...
```

The awkward part is not the loop. It is the first word of each letter. When
`"apple"` arrives there is no `"a"` bucket yet, so you cannot append to it; you
have to make it first. When `"ant"` arrives the bucket exists and you must
*not* make a new one, because that would throw `"apple"` away.

You could write that as an `if`. Python gives you something better:
**`dict.setdefault`**, which means "give me the value under this key, and if
there isn't one, put this there first and give me that". One call, both cases,
no branch. `collections.defaultdict(list)` does the same job differently and the
brief allows either.

One more instruction, and it is a real one: the words arrive already in lower
case. **Do not lower them again.** If a capital letter ever shows up, that is
somebody upstream's problem and not yours to paper over.

## Starter

Save this in your `homework/` folder as part of `week-05-solutions.py` and fill
in the `TODO`. It runs as pasted — it just gives back an empty dict:

```python
"""Week 5 homework, problem 5: sort words into buckets by their first letter."""


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    """Map each starting letter to the words that begin with it, in order.

    Args:
        words: Already-lowercased words. None of them may be empty.

    Returns:
        A new dict of letter to list of words.

    Example:
        >>> group_by_first_letter(["apple", "ant", "bee"])
        {'a': ['apple', 'ant'], 'b': ['bee']}
    """
    groups: dict[str, list[str]] = {}
    # TODO: one loop over words. For each word, get the list stored under its
    #       first letter -- creating an empty one if there isn't one yet --
    #       and append the word to it. `groups.setdefault(key, [])` does the
    #       first half and hands you the list.
    return groups


def _demo() -> None:
    """Print the brief's example and the empty case."""
    print(group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"]))
    print(group_by_first_letter([]))


if __name__ == "__main__":
    _demo()
```

Try `setdefault` on its own first, twice on the same key, and watch what comes
back:

```python
d = {}
print(d.setdefault("a", []))
d["a"].append("apple")
print(d.setdefault("a", []))
```

```text
[]
['apple']
```

The second call did **not** replace the list. It found one and handed it over.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/homework/problem-05-group-by-first-letter.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `group_by_first_letter(words)` returns a dict mapping each first letter to
   the list of words that begin with it.
2. Each list holds its words in the order they appeared in the input.
3. `group_by_first_letter([])` returns `{}`.
4. The input list is not changed.
5. The words are used exactly as given — no lowercasing, no stripping, no
   sorting.
6. The body uses `dict.setdefault` or `collections.defaultdict(list)`.
7. Type hints on the signature and a docstring on the function.
8. These three asserts pass:

   ```python
   result = group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])
   assert result == {"a": ["apple", "ant"], "b": ["bee", "banana"], "c": ["cherry"]}
   assert group_by_first_letter([]) == {}
   assert group_by_first_letter(["zebra"]) == {"z": ["zebra"]}
   ```

## Constraints

- **Append to the list; do not rebuild it.** `groups[k] = groups.get(k, []) + [w]`
  gives the right answer and makes a whole new list every single word. See
  *Common bugs to catch* for what that costs.
- **Do not use `dict.fromkeys` to pre-make the buckets.** It gives every key
  the *same* list object, and then all your letters share one bucket.
- **Do not normalise the words.** The brief says the input is already lower
  case. Lowercasing again is an invisible change to the contract you were given.
- **Return a plain `dict`.** If you use `defaultdict`, wrap the result in
  `dict(...)` before returning it, for the reason in *Why it works*.
- **`_demo` prints; `group_by_first_letter` does not.**

## Expected output

```text
$ python problem-05-group-by-first-letter.py
{'a': ['apple', 'ant'], 'b': ['bee', 'banana'], 'c': ['cherry']}
{}
{'z': ['zebra']}
['a', 'b', 'c']
All 4 asserts passed.
```

The first three lines are the brief's example and the required asserts.

The fourth line is `list(result)`, which is the dict's **keys**. They come out
`a, b, c` — and that is first-seen order, not alphabetical order. It looks the
same here only because the brief's example happens to arrive in alphabetical
order. Feed it `["zebra", "apple"]` and you get `['z', 'a']`:

```bash
python -c "from week_05_solutions import group_by_first_letter as g; print(list(g(['zebra','apple'])))"
```

```text
['z', 'a']
```

Worth knowing before you assume a printed dict is sorted.

## Steps

1. Save the Starter into `week-05-solutions.py` and run it. An empty dict twice.
2. Play with `setdefault` at the REPL until you can predict it, using the
   snippet in *Starter*. The question to be able to answer: what does it return
   when the key is already there?
3. Write the loop. It is two lines, or one if you like:

   ```python
   for word in words:
       groups.setdefault(word[0], []).append(word)
   ```

4. Run it. The first line should be
   `{'a': ['apple', 'ant'], 'b': ['bee', 'banana'], 'c': ['cherry']}`.
5. Split that one line into two and print the middle, so you can see what
   `setdefault` handed back:

   ```python
   bucket = groups.setdefault(word[0], [])
   print(word, "->", bucket)
   bucket.append(word)
   ```

   Watch `['apple']` come back when `"ant"` arrives. That returned list is not a
   copy — it is the one living inside `groups`.
6. Put the line back together. Add the three required asserts, plus
   `assert list(result) == ["a", "b", "c"]`.
7. Try `group_by_first_letter(["apple", ""])` and read the traceback. Decide
   whether to guard it, and say what you decided in a comment.
8. Compare with **The Solution**, tick the acceptance checklist, and commit:
   `git commit -m "Week 5 homework: group by first letter"`.

## The Solution

```python
"""Sort words into one bucket per starting letter, keeping their order.

Week 5 homework, problem 5, Code Crunch Convos.

Add ``group_by_first_letter`` to your own ``week-05-solutions.py``. This file is
the published answer, and the longer name keeps it from landing on top of your
work.

``setdefault`` is the whole trick. It hands back the list already stored under a
letter, or puts a fresh empty one there first and hands back that. Either way
what comes back is the list living inside the dict, so appending to it changes
the dict.
"""


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    """Map each starting letter to the words that begin with it, in order.

    Args:
        words: Already-lowercased words. None of them may be empty.

    Returns:
        A new dict. Each list holds its words in the order they arrived, and the
        letters themselves come out in first-seen order.

    Example:
        >>> group_by_first_letter(["apple", "ant", "bee"])
        {'a': ['apple', 'ant'], 'b': ['bee']}
    """
    groups: dict[str, list[str]] = {}
    for word in words:
        groups.setdefault(word[0], []).append(word)
    return groups


def _check() -> None:
    """Run the three asserts the brief requires, plus one it implies."""
    result = group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])
    assert result == {"a": ["apple", "ant"], "b": ["bee", "banana"], "c": ["cherry"]}
    assert group_by_first_letter([]) == {}
    assert group_by_first_letter(["zebra"]) == {"z": ["zebra"]}
    assert list(result) == ["a", "b", "c"]


def _demo() -> None:
    """Print the brief's example, the two small cases, and the key order."""
    print(group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"]))
    print(group_by_first_letter([]))
    print(group_by_first_letter(["zebra"]))
    print(list(group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])))
    print("All 4 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
```

**Why it works.**

**One line does three jobs.** Pull them apart and they are obvious:

```python
bucket = groups.setdefault(word[0], [])   # 1. make sure the key exists
                                          # 2. hand me the list under it
bucket.append(word)                       # 3. push into the list that lives
                                          #    inside groups
```

`setdefault` **writes if it must, then returns**. New letter: it inserts
`letter -> []` and returns that fresh list. Letter already there: it returns the
existing list and touches nothing. Either way, what you get back is *the list
object stored inside `groups`* — not a copy. So `.append` changes the dict's own
data.

That is aliasing, used on purpose. Two names for one list, and a change through
either name is visible through both. It is the rule from
[lecture 01](../lecture-notes/01-lists-and-tuples.md#aliasing--the-gotcha) that
bites people in Problem 1, working *for* you here. The same idiom is in
[lecture 02's grouping example](../lecture-notes/02-sets-and-dicts.md#grouping)
and in Challenge 01's anagram grouper.

**Order comes free, twice over.** The brief requires the word lists to keep
their input order, and they do, because you append in input order and never
sort. As a bonus the **keys** come out in first-seen order, since dicts have
preserved insertion order since Python 3.7 — that is what
`list(result) == ["a", "b", "c"]` checks. Nothing in the required asserts
depends on key order, because `==` on dicts ignores it. Your printed output does
depend on it, and so does anybody who reads that output and assumes it is
alphabetical.

**`word[0]`, not `word[0].lower()`.** The brief says: *"Treat input as
already-lowercased; do not normalize."* Resist being helpful. Lowercase anyway
and `["Apple", "ant"]` silently collapses into one group, which means you have
changed the contract you were handed without telling anyone. When a spec is
explicit about not normalising, it is usually because somebody upstream already
did — and doing it twice hides where that responsibility lives.

**`setdefault` against `defaultdict`.** Both are allowed and both are correct.

```python
from collections import defaultdict


def group_by_first_letter_dd(words: list[str]) -> dict[str, list[str]]:
    """Same thing with collections.defaultdict, returned as a plain dict."""
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)
    return dict(groups)
```

- `setdefault` keeps the container an ordinary `dict`. Its cost is that the `[]`
  argument is built on **every** call, even when the key already exists, and
  then thrown away. That is a small waste, not a bug.
- `defaultdict(list)` shortens the body and only builds a list when one is
  really needed. Its cost is that **any read of a missing key creates it**.
  `groups["q"]` returns `[]` *and inserts* `"q" -> []`, so merely looking at your
  data grows it. That is why the version above returns `dict(groups)`: callers
  get something that cannot sprout keys behind their backs.

The rule of thumb: `defaultdict` where insertion dominates and the dict never
leaves the function; plain `dict` at the boundaries.

## Run it

Copy the worked answer on this page into `problem-05-group-by-first-letter.py` and run it:
and run it:

```bash
python problem-05-group-by-first-letter.py
```

Your own copy of `group_by_first_letter` belongs in `week-05-solutions.py`, and
that is the file you commit. The longer download name keeps the published answer
from landing on top of your work.

## Common bugs to catch

- **Rebuilding the list instead of appending to it.**

  ```python
  groups[word[0]] = groups.get(word[0], []) + [word]
  ```

  Every assert passes. It is still the wrong answer to the problem, because `+`
  on lists means "make a new one": grouping `n` words into a single bucket
  copies 1, then 2, then 3, ... elements, which adds up to a multiple of `n × n`.
  `.append` changes the list where it sits and costs the same however long the
  list already is. The difference between `+` and `.append` is the difference
  between "make a new one" and "extend this one", and at scale that is the
  difference between a program that finishes and one that does not.
- **`dict.fromkeys` for the buckets.**

  ```python
  groups = dict.fromkeys({w[0] for w in words}, [])
  for word in words:
      groups[word[0]].append(word)
  ```

  ```text
  {'a': ['apple', 'ant', 'bee', 'banana', 'cherry'], 'b': [...same list...], 'c': [...same list...]}
  ```

  `fromkeys` uses **one** default object for every key, so all three letters
  share a single list and each shows every word. Exactly the same trap as
  `[[0] * n] * m` in Problem 1. `dict.fromkeys` is only safe with immutable
  defaults.
- **An empty string in the input.**

  ```python
  group_by_first_letter(["apple", ""])
  ```

  ```text
  Traceback (most recent call last):
    File "week-05-solutions.py", line 6, in <module>
      print(group_by_first_letter(["apple", ""]))
            ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
    File "week-05-solutions.py", line 4, in group_by_first_letter
      groups.setdefault(w[0], []).append(w)
                        ~^^^
  IndexError: string index out of range
  ```

  `""[0]` has no character to hand back. The brief never mentions empty strings
  so this is out of scope — but `if not word: continue` is one line and costs
  nothing. Decide it deliberately rather than discovering it later.
- **Sorting the words to group them.** `sorted(words)` does put same-letter
  words next to each other, and you can then walk the sorted list and cut at
  every letter change. It works. It is slower than a single pass, it destroys
  the input order the brief tells you to preserve, and it is four times the
  code. Sorting is what you reach for when you have not got a dict.
- **Returning the `defaultdict`.** If you used `defaultdict` and forgot
  `dict(groups)`, then a caller writing `if result["q"]:` to check for an empty
  bucket silently adds a `"q"` key. The equality asserts still pass, so the only
  thing that catches it is
  `assert type(group_by_first_letter([])) is dict`.

## Under the hood

<details>
<summary>Under the hood — why a dict of lists beats a list of pairs for grouping</summary>

There is another way to hold grouped data, and it is the one people reach for
before they have met dicts: a list of pairs.

```python
groups = [("a", ["apple", "ant"]), ("b", ["bee", "banana"])]
```

It holds the same information. It is even ordered, which the dict is too. So why
is the dict not merely nicer to type but genuinely the right structure?

**Adding one word is the whole argument.** With a dict:

```python
groups.setdefault(letter, []).append(word)
```

One hash, one slot, done. The cost does not change as the data grows — twenty
groups or twenty thousand, it is the same work.

With a list of pairs you have to find the pair first:

```python
for pair in groups:                      # walk until you find the letter
    if pair[0] == letter:
        pair[1].append(word)
        break
else:
    groups.append((letter, [word]))
```

That walk looks at every group you have made so far, and it happens **once per
word**. Group `n` words into `g` groups and the dict does about `n` units of
work while the list of pairs does about `n × g`. With 26 letters and a thousand
words that is 1,000 against 26,000 — survivable. Group a million log lines by
customer id and `g` is in the thousands, and the list version stops being a
program you can run.

The shape is the same one from Problem 4's wrong turns: **a search inside a loop
over the same data.** You are scanning to find where something belongs, and
"where does this belong" is precisely the question a hash table answers without
looking.

Three more things the dict gives you that are easy to miss:

**Keys cannot accidentally repeat.** A list of pairs will happily hold `("a",
[...])` twice if one code path forgets to search first, and then half your
`"a"` words are in a group nobody ever reads. The dict makes that state
impossible to represent.

**Reading one group back is direct.** `groups["b"]` against another walk. Every
consumer of your grouped data pays the list version's cost again.

**It says what it means.** `dict[str, list[str]]` reads as "each letter has a
list of words". `list[tuple[str, list[str]]]` reads as "a list of things, and
you will have to go and look at what is in them".

When is the list of pairs right? When the keys are **not hashable** — you cannot
key a dict by a list, per Problem 2's *Under the hood* — or when you genuinely
want duplicate keys, or when you have finished grouping and now want the result
in a particular order. That last one is common, and it is why
`sorted(groups.items(), key=...)` exists: build with the dict, and turn it into
a list of pairs at the end, once, when the shape you need is "in this order"
rather than "look this up".

</details>

<details>
<summary>Under the hood — setdefault, defaultdict, and the argument that is always built</summary>

`setdefault` has one wart, and it is worth understanding rather than
memorising.

**The default is evaluated every time, even when it is not needed.**

```python
def make_bucket() -> list:
    """Return a new empty bucket, noisily."""
    print("built a bucket")
    return []


groups = {"a": ["apple"]}
groups.setdefault("a", make_bucket()).append("ant")
```

```text
built a bucket
```

The `"a"` key already existed and the fresh bucket was thrown away unused — but
it was still built, because Python works out every argument *before* calling the
method. `setdefault` cannot skip work it was handed as a finished value.

With `[]` that waste is a few nanoseconds and nobody cares. With something
expensive — a database connection, a parsed file, a network call — it is a real
bug, and the symptom is "why is this slow" rather than a traceback.

`defaultdict` does not have the problem, because you give it the **function**
rather than the result:

```python
from collections import defaultdict

groups = defaultdict(make_bucket)
groups["a"].append("apple")     # prints once: the key was missing
groups["a"].append("ant")       # prints nothing: the key was there
```

`defaultdict(list)` passes `list` itself — no brackets — and the dict calls it
only when a key is genuinely absent. That is the same "pass the function, not
the answer" idea as `sorted(key=...)`.

What `defaultdict` costs you in exchange is that **reading creates**:

```python
>>> from collections import defaultdict
>>> d = defaultdict(list)
>>> "q" in d
False
>>> d["q"]
[]
>>> "q" in d
True
```

Merely looking at `d["q"]` put it there. Now `len(d)` is wrong, iterating gives
a group nobody added, and saving it writes a key that never had data. This is
the classic `defaultdict` surprise, and it is why the `dict(groups)` conversion
on the way out of a function is such a common habit — a plain dict cannot do it,
so callers cannot trip over it.

Note that `.get()` never creates, on either kind of dict, which makes
`d.get("q")` the safe way to look without touching:

```python
>>> d.get("nope")
>>> "nope" in d
False
```

Three tools, three jobs: `.get` to look, `setdefault` to look-or-make when the
default is cheap, `defaultdict` to look-or-make when the default is not — or
when you would otherwise write `setdefault` on every single line.

</details>

## Acceptance checklist

- [ ] `group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])` gives
      `{'a': ['apple', 'ant'], 'b': ['bee', 'banana'], 'c': ['cherry']}`.
- [ ] `group_by_first_letter([])` gives `{}`.
- [ ] `group_by_first_letter(["zebra"])` gives `{'z': ['zebra']}`.
- [ ] Each list is in input order — nothing is sorted.
- [ ] The body uses `setdefault` or `defaultdict`, and appends rather than
      rebuilding with `+`.
- [ ] The words are stored exactly as given, with no lowercasing.
- [ ] The returned object is a plain `dict`.
- [ ] The input list is unchanged.
- [ ] The signature has type hints and the function has a docstring.
- [ ] Committed with a message like `Week 5 homework: group by first letter`.

## Stretch

- **Group by anything.** Write
  `group_by(items: list, key: Callable) -> dict` that takes the grouping rule as
  an argument, so `group_by(words, lambda w: w[0])` is this problem and
  `group_by(words, len)` groups by length instead. One function, every "by
  something" report you will ever need. Then look at
  `itertools.groupby` and find the trap: it only groups **runs** of adjacent
  equal keys, so it needs a sorted input and is not the same thing at all.
- **Write the `defaultdict` version too.** It is in *Why it works*. Assert that
  both versions produce equal answers on the same input, and add
  `assert type(group_by_first_letter_dd([])) is dict` so the plain-dict
  conversion cannot quietly disappear.
- **Count instead of collecting.** Change the value from a list of words to the
  number of them. Notice that the whole `setdefault` dance collapses into
  Problem 4's `counts.get(letter, 0) + 1`, because an integer is immutable so
  there is nothing to append to. Grouping and counting are the same shape with
  different value types, and only one of them needs aliasing.
- **Group into sets rather than lists.** `setdefault(letter, set()).add(word)`
  deduplicates within each bucket. Then work out what you lost: sets have no
  order, so the brief's "preserve the original order" requirement is gone. Every
  container choice trades something.
- **Sort the output without breaking the input order.**
  `dict(sorted(groups.items()))` gives alphabetical keys while leaving each
  bucket's word order alone. Convince yourself of why that is safe, and why
  `sorted(words)` before grouping is not.

Next: [Homework Problem 6 — Intersect dictionaries](./problem-06-intersect-dictionaries.md).
