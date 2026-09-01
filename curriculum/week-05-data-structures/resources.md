# Week 5 — Resources

A curated set of references for **lists, tuples, sets, dicts, and comprehensions**. Skim everything once; bookmark the items you reach for most often.

---

## Official Python documentation

These are the canonical sources. When in doubt, check the official docs first.

- **[Data Structures tutorial](https://docs.python.org/3/tutorial/datastructures.html)** — the single best read for this week. Covers lists as stacks/queues, list comprehensions, the `del` statement, tuples, sets, and dictionaries in one tightly-written page.
- **[`collections` module](https://docs.python.org/3/library/collections.html)** — `namedtuple`, `Counter`, `defaultdict`, `deque`, `OrderedDict`, `ChainMap`. We use `namedtuple` and `Counter` this week; the rest you will revisit later.
- **[Built-in Types — Sequence Types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)** — every list and tuple method, with semantics.
- **[Built-in Types — Set Types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)** — full reference for `set` and `frozenset`, including operator vs method equivalences.
- **[Built-in Types — Mapping Types](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)** — full `dict` reference, including dict views (`.keys()`, `.values()`, `.items()`).
- **[`copy` module](https://docs.python.org/3/library/copy.html)** — `copy.copy()` vs `copy.deepcopy()`. Required reading before the mutability section.
- **[`json` module](https://docs.python.org/3/library/json.html)** — used in the mini-project. Read `json.load`, `json.dump`, `json.loads`, `json.dumps`.

---

## Performance references

- **[TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity)** — the official-ish Big-O table for CPython's list, set, dict, deque. Memorize the highlights:
  - `list.append` is amortized **O(1)**, `list.insert(0, x)` is **O(n)**.
  - `x in list` is **O(n)**, `x in set` and `x in dict` are average **O(1)**.
  - `dict[key]` get/set is average **O(1)**.
- **[Python Performance Tips (PythonSpeed wiki)](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)** — older but still relevant; section on string concatenation and list building is gold.

---

## Tutorials and deeper reads

- **[Real Python — List Comprehensions in Python](https://realpython.com/list-comprehension-python/)** — clearest write-up of comprehension syntax, conditional forms, and when *not* to use them.
- **[Real Python — Dictionaries in Python](https://realpython.com/python-dicts/)** — comprehensive tour, including dict views and dict comprehensions.
- **[Real Python — Sets in Python](https://realpython.com/python-sets/)** — uniqueness, set operations, frozensets.
- **[Real Python — Tuples vs Lists vs Sets vs Dicts](https://realpython.com/python-data-structures/)** — decision matrix for picking a structure.
- **[Trey Hunner — Comprehensions in Python](https://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/)** — colour-coded breakdown that finally makes nested comprehensions click.

---

## PEPs (Python Enhancement Proposals)

You don't need to read these cover-to-cover, but skimming the motivation section of each is useful.

- **[PEP 202 — List Comprehensions](https://peps.python.org/pep-0202/)** — why they exist.
- **[PEP 274 — Dict Comprehensions](https://peps.python.org/pep-0274/)** — added in Python 2.7 / 3.0.
- **[PEP 218 — Adding a Built-In Set Object Type](https://peps.python.org/pep-0218/)** — historical context for `set`.

---

## Videos (optional)

- **[Raymond Hettinger — "Beyond PEP 8"](https://www.youtube.com/watch?v=wf-BqAjZb8M)** — section on dict idioms is gold.
- **[Ned Batchelder — "Loop Like a Native"](https://www.youtube.com/watch?v=EnSu9hHGq5o)** — how to iterate Pythonically; sets up the mindset for comprehensions.

---

## Cheat sheets

- **[Python Cheatsheet — Data Structures](https://www.pythoncheatsheet.org/cheatsheet/lists-and-tuples)** — one-page quick reference.
- **[Big-O Cheat Sheet](https://www.bigocheatsheet.com/)** — generic, but good for cross-language intuition.

---

## How to use these resources

1. **First pass** — read the [Data Structures tutorial](https://docs.python.org/3/tutorial/datastructures.html) end to end.
2. **As you study lecture notes** — keep the [Built-in Types reference](https://docs.python.org/3/library/stdtypes.html) open in a tab; jump to it whenever a method name surprises you.
3. **Before the mini-project** — read the [`json` module](https://docs.python.org/3/library/json.html) intro section.
4. **After exercises** — skim Real Python's comprehensions article to consolidate.
5. **Stretch** — explore the `collections` module.

If something is unclear, your first question should always be: *"What does the official doc say?"* That habit alone makes you a better Python developer.
