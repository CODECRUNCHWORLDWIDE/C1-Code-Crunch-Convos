# Challenge 01 — Anagram Groups

**Estimated time:** 60–90 minutes.
**Concepts used:** strings, lists, tuples, dicts, sorted, comprehensions.

---

## The problem

Two words are **anagrams** of each other if they contain exactly the same letters with the same counts. For example:

- `"listen"` and `"silent"` are anagrams.
- `"evil"`, `"vile"`, `"live"`, and `"veil"` are all anagrams of each other.
- `"hello"` and `"world"` are not.

Given a list of lowercase strings, **group the anagrams together**. The order of groups, and the order of words within a group, do not matter.

### Example input

```python
words = [
    "eat", "tea", "tan", "ate", "nat", "bat",
    "listen", "silent", "enlist",
    "evil", "vile", "live", "veil",
    "hello",
]
```

### Example output (one valid arrangement)

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

---

## Your task

Implement a function:

```python
def group_anagrams(words: list[str]) -> list[list[str]]:
    ...
```

It should return a list of groups, where each group is a list of words that are anagrams of one another. Words that have no anagram partner should appear as a singleton group of size 1.

---

## The key insight

Two strings are anagrams **iff** their sorted character sequences are identical. So `sorted("listen")` and `sorted("silent")` both return `['e', 'i', 'l', 'n', 's', 't']`. That sequence — converted to a tuple or back to a string — makes a great **dictionary key**.

The algorithm is:

1. Initialize `groups: dict[str, list[str]] = {}`.
2. For each word, compute its signature, e.g. `"".join(sorted(word))`.
3. `groups.setdefault(signature, []).append(word)`.
4. Return `list(groups.values())`.

That's it. Big-O is **O(n × k log k)** where `n` is the number of words and `k` is the average word length (the `k log k` is the per-word sort).

---

## Requirements

Your `solution.py` must:

- Define `group_anagrams(words)` with the signature above.
- Use a **dictionary** to do the grouping (not nested loops over `words`).
- Handle the empty input (`group_anagrams([])` returns `[]`).
- Handle words of different lengths correctly — they can never be in the same group.
- Run on the sample input below and pass the asserts.

### Sample test scaffolding

```python
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

print("All checks passed.")
```

---

## Rubric

| Criterion | Points |
|---|---|
| Function runs on the sample input | 30 |
| Uses a dict for grouping (no O(n²) scan) | 25 |
| Type hints present and correct | 15 |
| Handles empty input | 10 |
| Asserts pass | 15 |
| Reflection paragraph in docstring | 5 |
| **Total** | **100** |

---

## Stretch

1. Add a `case_sensitive: bool = True` flag. When `False`, `"Tea"` and `"ate"` should land in the same group.
2. Sort the groups so that the largest group comes first, and within each group sort words alphabetically. Make this deterministic.
3. Compare two signatures: `"".join(sorted(word))` vs `tuple(Counter(word).items())`. Which is faster? Which is more memory-efficient? Use `timeit` to find out.
4. Read words from a file (`/usr/share/dict/words` on macOS/Linux) and find the **longest** anagram group in English. (Spoiler: it's big.)
