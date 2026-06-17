# 02 — Sets and Dictionaries

Reading time: **~25 minutes**.

In lecture 01 you met **ordered** containers (lists and tuples). This lecture covers the two **hash-based** containers: `set` and `dict`. They unlock a different kind of thinking — instead of "the item at position 3", you ask "is this item present?" or "what value goes with this key?"

---

## 1. Sets — a bag of unique things

A set is an **unordered** collection of **unique**, **hashable** items.

```python
empty: set = set()             # NOT {} -- that's an empty dict!
primes: set[int] = {2, 3, 5, 7, 11}
fruits = {"apple", "banana", "cherry"}

# duplicates are silently dropped
unique = {1, 1, 2, 2, 3}       # {1, 2, 3}
```

Two key properties:

1. **Uniqueness** — adding a duplicate is a no-op.
2. **O(1) membership** — `x in s` is on average constant time, regardless of set size.

### Building sets from iterables

```python
words = ["the", "quick", "brown", "fox", "the", "lazy", "dog"]
unique_words: set[str] = set(words)   # {'the', 'quick', 'brown', 'fox', 'lazy', 'dog'}
```

This is the canonical way to **deduplicate** a list (though you lose order; see Exercise 02 for an order-preserving variant).

### Mutating sets

```python
s = {1, 2, 3}
s.add(4)            # {1, 2, 3, 4}
s.add(4)            # no change
s.discard(2)        # remove 2 if present; no error if absent
s.remove(2)         # KeyError if absent
s.pop()             # remove and return an arbitrary element
s.clear()           # empty the set
```

### What can go in a set?

Only **hashable** items. In practice: ints, floats, strings, tuples of hashables, and `frozenset`s. You **cannot** put lists or dicts in a set:

```python
{[1, 2]}    # TypeError: unhashable type: 'list'
{(1, 2)}    # fine
```

### Set operations

This is where sets shine. Given two sets `A` and `B`:

```
   A         A & B         B
 ┌──────┐     ┌──┐     ┌──────┐
 │      │.....│..│.....│      │
 │  A-B │  intersect    │ B-A │
 │      │.....│..│.....│      │
 └──────┘     └──┘     └──────┘
        A | B  (union, everything in either)
        A ^ B  (symmetric difference, in exactly one)
```

| Operator | Method | Meaning |
|---|---|---|
| `A \| B` | `A.union(B)` | all items in either set |
| `A & B` | `A.intersection(B)` | items in both |
| `A - B` | `A.difference(B)` | items in A but not B |
| `A ^ B` | `A.symmetric_difference(B)` | items in exactly one |
| `A <= B` | `A.issubset(B)` | every A in B? |
| `A >= B` | `A.issuperset(B)` | every B in A? |

```python
mon_attendees = {"Ada", "Grace", "Linus", "Guido"}
tue_attendees = {"Linus", "Guido", "Donald", "Margaret"}

mon_attendees | tue_attendees   # everyone who attended either day
mon_attendees & tue_attendees   # attended both days -> {'Linus', 'Guido'}
mon_attendees - tue_attendees   # only Monday        -> {'Ada', 'Grace'}
mon_attendees ^ tue_attendees   # exactly one day    -> {'Ada', 'Grace', 'Donald', 'Margaret'}
```

In-place versions: `|=`, `&=`, `-=`, `^=`.

### `frozenset` — the immutable cousin

`frozenset` is to `set` what `tuple` is to `list`: same API, no mutation. Hashable, so it can live inside another set or be a dict key.

```python
read_only: frozenset[int] = frozenset({1, 2, 3})
read_only.add(4)             # AttributeError
```

Useful for cached results, dict keys, and explicit "do not modify" intent.

### When to use a set

- You need to test "is X in the collection?" frequently — `O(1)` beats `list`'s `O(n)`.
- You need to deduplicate.
- You're doing set math (overlap, exclusivity).
- You don't care about order.

See [Built-in Set Types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset).

---

## 2. Dictionaries — key → value lookup

A dictionary maps **hashable keys** to **arbitrary values**. Since Python 3.7, dicts maintain **insertion order**.

```python
empty: dict = {}
ages: dict[str, int] = {"Ada": 37, "Grace": 85, "Guido": 67}

# alternative constructors
d1 = dict(name="Ada", age=37)                  # from kwargs
d2 = dict([("a", 1), ("b", 2)])                # from list of pairs
d3 = dict(zip(["x", "y"], [10, 20]))           # from two iterables
```

### Access and assignment

```python
ages["Ada"]              # 37
ages["Linus"] = 54       # insert (or overwrite if key exists)
del ages["Grace"]        # remove a key

len(ages)                # number of keys
"Ada" in ages            # True  -- checks KEYS, not values
```

Accessing a missing key with `[]` raises `KeyError`:

```python
ages["Missing"]          # KeyError: 'Missing'
```

### `.get()` — the safer access

```python
ages.get("Ada")          # 37
ages.get("Missing")      # None
ages.get("Missing", 0)   # 0   (default if absent)
```

Use `.get()` whenever the absence of a key is a valid situation rather than a bug. Use `d[key]` when the key *must* exist.

### `.setdefault()` — get-or-insert

`setdefault(key, default)` returns the value for `key`; if `key` is missing, it inserts `key=default` first and returns `default`.

```python
groups: dict[str, list[str]] = {}
for word in ["ant", "bee", "ape", "bat", "antelope"]:
    groups.setdefault(word[0], []).append(word)

# groups == {'a': ['ant', 'ape', 'antelope'], 'b': ['bee', 'bat']}
```

For this pattern, `collections.defaultdict(list)` is even cleaner — see the stretch goals.

### `.update()` — merge another mapping

```python
ages.update({"Linus": 54, "Donald": 86})        # add/overwrite many keys at once
ages.update(name="Ada Lovelace", role="math")   # also accepts kwargs
```

In Python 3.9+, you can also use the `|` and `|=` operators on dicts:

```python
combined = ages | {"Ada": 38}        # new dict; right-hand side wins on conflicts
ages |= {"Ada": 38}                  # in-place update
```

### Iterating dicts

By default, iterating a dict yields **keys**:

```python
for name in ages:
    print(name, ages[name])
```

But the explicit forms are nicer:

```python
for name in ages.keys():
    ...

for age in ages.values():
    ...

for name, age in ages.items():     # the one you'll use most
    print(f"{name} is {age}")
```

**Important**: do not add or remove keys while iterating a dict — Python raises `RuntimeError: dictionary changed size during iteration`. If you need to modify, iterate over a *copy* of the keys:

```python
for name in list(ages.keys()):     # snapshot
    if ages[name] < 18:
        del ages[name]
```

### Dict views

`.keys()`, `.values()`, `.items()` return **views**, not lists. They are live: if the dict changes, the view reflects it. Views support `in`, `len`, and iteration; key/item views also support set operations.

```python
common_keys = d1.keys() & d2.keys()   # keys present in both dicts
```

---

## 3. Common dict patterns

### Counting

```python
text = "the quick brown fox jumps over the lazy dog the the"
counts: dict[str, int] = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1

# counts == {'the': 4, 'quick': 1, 'brown': 1, ...}
```

The idiomatic alternative is `collections.Counter`:

```python
from collections import Counter
counts = Counter(text.split())
counts.most_common(3)    # top 3 by frequency
```

### Grouping

```python
people = [
    {"name": "Ada", "team": "math"},
    {"name": "Grace", "team": "compilers"},
    {"name": "Guido", "team": "language"},
    {"name": "Barbara", "team": "math"},
]

by_team: dict[str, list[str]] = {}
for p in people:
    by_team.setdefault(p["team"], []).append(p["name"])

# by_team == {'math': ['Ada', 'Barbara'], 'compilers': ['Grace'], 'language': ['Guido']}
```

### Inverting (swap keys and values)

```python
codes = {"red": 1, "green": 2, "blue": 3}
inverted = {v: k for k, v in codes.items()}
# {1: 'red', 2: 'green', 3: 'blue'}
```

(That's a dict comprehension — you'll meet them formally in lecture 03.)

### Translating with `.get()`

```python
symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
def render(code: str, amount: float) -> str:
    return f"{symbols.get(code, code)} {amount:.2f}"

render("USD", 9.99)      # '$ 9.99'
render("JPY", 1500)      # 'JPY 1500.00'
```

---

## 4. Nested data structures

Real data is rarely flat. You will routinely build lists of dicts, dicts of lists, and dicts of dicts.

### List of dicts (the "table" pattern)

This is how JSON arrays of objects show up in Python:

```python
contacts: list[dict[str, str]] = [
    {"name": "Ada", "email": "ada@example.com",  "phone": "555-0100"},
    {"name": "Grace", "email": "grace@example.com","phone": "555-0200"},
]

# find a contact by name
def find_by_name(name: str) -> dict | None:
    for c in contacts:
        if c["name"] == name:
            return c
    return None
```

This is the structure we use in this week's mini-project.

### Dict of lists (the "grouping" pattern)

```python
roster: dict[str, list[str]] = {
    "engineering": ["Ada", "Grace"],
    "design":      ["Linus", "Guido"],
    "ops":         [],
}
roster["engineering"].append("Barbara")
```

### Dict of dicts (the "nested record" pattern)

```python
inventory: dict[str, dict[str, int]] = {
    "fruit": {"apple": 5, "banana": 3},
    "tools": {"hammer": 1, "saw": 2},
}
inventory["fruit"]["apple"]            # 5
inventory["fruit"]["apple"] += 2       # 7
```

Beware: deep mutation reaches into shared inner dicts. If you copy the outer dict shallowly and mutate an inner one, both copies see the change — same aliasing rule as for lists.

### Reading nested data safely

When you don't know whether a path exists, chain `.get()` carefully:

```python
inventory.get("fruit", {}).get("kiwi", 0)   # 0, no KeyError
```

---

## 5. Choosing the right structure

A starter decision tree:

1. **Do I need key → value lookup?** → `dict`.
2. **Do I need uniqueness or fast `in` tests, and I don't care about order?** → `set`.
3. **Do I have a fixed-size record (e.g. coordinates)?** → `tuple` (or `namedtuple`).
4. **Do I have an ordered, growing sequence?** → `list`.

If unsure, start with the simplest structure that works (often a list) and refactor only if performance or readability demands it.

---

## 6. Quick reference

```python
# Sets
s = {1, 2, 3}
s.add(4); s.discard(2)
A | B; A & B; A - B; A ^ B
fs = frozenset({1, 2})        # hashable, immutable

# Dicts
d = {"a": 1, "b": 2}
d["c"] = 3
d.get("z", 0)
d.setdefault("k", []).append("x")
d.update({"a": 10})
for k, v in d.items(): ...
```

---

## 7. What to do next

1. Type out every example in a REPL.
2. Complete **Exercise 03** (word frequency) and **Exercise 04** (set operations).
3. Move on to lecture **03 — Comprehensions and Big-O**.

---

**Sources**
- [Python tutorial — Data Structures, sections on sets and dictionaries](https://docs.python.org/3/tutorial/datastructures.html#sets)
- [Built-in Types — set/frozenset](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Built-in Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [`collections.Counter`, `defaultdict`](https://docs.python.org/3/library/collections.html)
