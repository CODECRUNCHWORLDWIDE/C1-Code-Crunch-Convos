# Week 5 — Quiz

Ten multiple-choice questions. Pick the **single best** answer. Aim for at least **8/10**. Each answer and its explanation are folded under the question — commit to yours first.

---

### Q1. Which of these creates an **empty set**?

A. `s = {}`
B. `s = set()`
C. `s = []`
D. `s = ()`

<details>
<summary>Answer</summary>

**B.** `{}` is an empty **dict**, not a set. The only way to make an empty set is `set()`.

</details>

---

### Q2. What is the value of `a` after this code runs?

```python
a = [1, 2, 3]
b = a
b.append(4)
```

A. `[1, 2, 3]`
B. `[1, 2, 3, 4]`
C. `None`
D. A `NameError`

<details>
<summary>Answer</summary>

**B.** `b = a` aliases the same list. Appending through `b` mutates the object `a` also points to. This is the aliasing gotcha from lecture 01. To avoid it, use `b = a.copy()`.

</details>

---

### Q3. Which method returns `None` rather than the modified list?

A. `sorted(my_list)`
B. `my_list.copy()`
C. `my_list.sort()`
D. `list(my_list)`

<details>
<summary>Answer</summary>

**C.** `list.sort()` sorts in place and returns `None`. Use `sorted(my_list)` if you want a new list.

</details>

---

### Q4. What does the expression `{x for x in "banana"}` evaluate to?

A. `{'b', 'a', 'n'}`
B. `{'b', 'a', 'n', 'a', 'n', 'a'}`
C. `"banana"`
D. A syntax error

<details>
<summary>Answer</summary>

**A.** Set comprehensions deduplicate automatically. The duplicates `'a'` and `'n'` collapse to one each.

</details>

---

### Q5. Given `d = {"a": 1, "b": 2}`, which expression returns `0` when the key is missing instead of raising `KeyError`?

A. `d["z"]`
B. `d.get("z", 0)`
C. `d["z"] or 0`
D. `d.fetch("z", 0)`

<details>
<summary>Answer</summary>

**B.** `d.get(key, default)` returns `default` instead of raising when the key is missing. `d["z"]` raises `KeyError`. There is no `.fetch()` method on dict.

</details>

---

### Q6. Which of the following is **NOT** a valid dict key?

A. `(1, 2)`
B. `"hello"`
C. `frozenset({1, 2})`
D. `[1, 2]`

<details>
<summary>Answer</summary>

**D.** Lists are mutable and therefore unhashable; they cannot be dict keys. Tuples (of hashables), strings, and frozensets are all hashable.

</details>

---

### Q7. What is the average-case Big-O of `x in some_set`?

A. O(1)
B. O(log n)
C. O(n)
D. O(n²)

<details>
<summary>Answer</summary>

**A.** Hash-based lookup is average-case constant time. (Worst case with bad hash collisions is O(n), but for normal data you can assume O(1).)

</details>

---

### Q8. Which expression produces `[1, 4, 9, 16]`?

A. `[x**2 for x in range(1, 5)]`
B. `[x*2 for x in range(1, 5)]`
C. `[x**2 for x in range(0, 4)]`
D. `(x**2 for x in range(1, 5))`

<details>
<summary>Answer</summary>

**A.** `range(1, 5)` is `[1, 2, 3, 4]`; squaring gives `[1, 4, 9, 16]`. Option D uses **parentheses**, which makes it a generator expression, not a list.

</details>

---

### Q9. What's the result of `{1, 2, 3} & {2, 3, 4}`?

A. `{1, 2, 3, 4}`
B. `{2, 3}`
C. `{1, 4}`
D. `{1, 2, 3, 2, 3, 4}`

<details>
<summary>Answer</summary>

**B.** `&` is set intersection: items present in both sets.

</details>

---

### Q10. After this code runs, what is `outer`?

```python
inner = [1, 2]
outer = [inner, inner]
outer[0].append(99)
```

A. `[[1, 2], [1, 2]]`
B. `[[1, 2, 99], [1, 2]]`
C. `[[1, 2, 99], [1, 2, 99]]`
D. A `RuntimeError`

<details>
<summary>Answer</summary>

**C.** `outer` contains the **same** inner list twice — both indices reference the one `inner` object. Appending through `outer[0]` mutates that single object, and both views show the change. This is why `copy.deepcopy()` exists.

---

### Scoring

- **9–10/10** — solid. Move on to the homework with confidence.
- **7–8/10** — re-skim the lecture sections matching your misses, then continue.
- **6 or fewer** — re-read lectures 01 and 02 carefully, type the examples in the REPL, and retake.

</details>

---

---
