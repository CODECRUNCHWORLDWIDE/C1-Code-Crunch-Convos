# Week 5 — Homework

Six problems to consolidate everything you learned this week. For each, write a Python function that meets the spec, include type hints, and verify with at least three `assert` statements.

Submit a single file `homework/week-05-solutions.py` in your fork, with each problem implemented and tested.

---

## Problem 1 — Matrix transpose (with a comprehension)

Given a matrix represented as a list of rows of equal length, return its transpose.

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    ...
```

Constraint: implement it with a **list comprehension** (nested is fine).

### Example

```python
transpose([[1, 2, 3], [4, 5, 6]])
# [[1, 4], [2, 5], [3, 6]]

transpose([[1]])
# [[1]]
```

Required asserts:

```python
assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert transpose([[1]]) == [[1]]
assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
```

Hint: `[[row[i] for row in matrix] for i in range(len(matrix[0]))]`.

---

## Problem 2 — Invert a dictionary

Given a dict whose values are all unique and hashable, return a new dict that swaps keys and values.

```python
def invert(d: dict) -> dict:
    ...
```

### Example

```python
invert({"red": 1, "green": 2, "blue": 3})
# {1: "red", 2: "green", 3: "blue"}
```

Constraint: use a dict comprehension.

Required asserts:

```python
assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}
assert invert({}) == {}
assert invert({"x": "X", "y": "Y"}) == {"X": "x", "Y": "y"}
```

Stretch: what if the values are **not** unique? Adapt `invert` to return `dict[value, list[key]]` instead.

---

## Problem 3 — Two-Sum (classic)

Given a list of integers and a target `t`, return a tuple of the two **indices** `(i, j)` with `i < j` such that `nums[i] + nums[j] == t`. If no such pair exists, return `None`. Assume at most one solution exists.

```python
def two_sum(nums: list[int], t: int) -> tuple[int, int] | None:
    ...
```

### Example

```python
two_sum([2, 7, 11, 15], 9)    # (0, 1)
two_sum([3, 2, 4], 6)         # (1, 2)
two_sum([1, 2, 3], 100)       # None
```

**Naive solution** is O(n²) with nested loops. **Required**: write an **O(n)** solution using a dictionary `seen: dict[int, int]` that maps each number to the index where you saw it. As you iterate, ask: "have I previously seen `t - nums[i]`?"

Required asserts:

```python
assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([3, 2, 4], 6) == (1, 2)
assert two_sum([1, 2, 3], 100) is None
assert two_sum([], 5) is None
```

---

## Problem 4 — Find duplicates

Return a sorted list of items that appear more than once in the input list.

```python
def find_duplicates(items: list) -> list:
    ...
```

### Example

```python
find_duplicates([1, 2, 3, 2, 4, 5, 1, 1])    # [1, 2]
find_duplicates(["a", "b", "c"])             # []
```

Constraint: solution should be **O(n)**. Use a dict (or `Counter`) for counts, then filter and sort.

Required asserts:

```python
assert find_duplicates([1, 2, 3, 2, 4, 5, 1, 1]) == [1, 2]
assert find_duplicates(["a", "b", "c"]) == []
assert find_duplicates(["x", "x", "y", "y", "z"]) == ["x", "y"]
```

---

## Problem 5 — Group by first letter

Given a list of strings, return a dict mapping each starting letter to the list of words that begin with it. The lists should preserve the original order.

```python
def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    ...
```

### Example

```python
group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])
# {"a": ["apple", "ant"], "b": ["bee", "banana"], "c": ["cherry"]}
```

Constraint: use `dict.setdefault` or `collections.defaultdict(list)`. Treat input as already-lowercased; do not normalize.

Required asserts:

```python
result = group_by_first_letter(["apple", "ant", "bee", "banana", "cherry"])
assert result == {"a": ["apple", "ant"], "b": ["bee", "banana"], "c": ["cherry"]}
assert group_by_first_letter([]) == {}
assert group_by_first_letter(["zebra"]) == {"z": ["zebra"]}
```

---

## Problem 6 — Intersect dictionaries

Given two dicts, return a new dict containing only the keys that appear in **both**, with values taken from the **first** dict.

```python
def intersect_dicts(d1: dict, d2: dict) -> dict:
    ...
```

### Example

```python
intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4})
# {"b": 2, "c": 3}
```

Constraint: use either a dict comprehension or the **dict view set operation** `d1.keys() & d2.keys()`.

Required asserts:

```python
assert intersect_dicts({"a": 1, "b": 2, "c": 3}, {"b": 99, "c": 100, "d": 4}) == {"b": 2, "c": 3}
assert intersect_dicts({}, {"a": 1}) == {}
assert intersect_dicts({"x": 1}, {"x": 1}) == {"x": 1}
```

---

## Submission checklist

- [ ] All six functions implemented and runnable.
- [ ] All required asserts pass.
- [ ] Type hints on every function signature.
- [ ] No bare `except:` blocks.
- [ ] No global state — pure functions only.
- [ ] File runs without errors: `python homework/week-05-solutions.py`.

When all checks pass, you're ready for **Week 6 — File I/O & Exceptions**.
