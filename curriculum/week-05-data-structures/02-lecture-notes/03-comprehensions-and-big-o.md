# 03 — Comprehensions and Big-O

Reading time: **~22 minutes**.

Once you have the four containers (list, tuple, set, dict), the next leap in Python fluency is **comprehensions**: compact, expressive syntax for building new collections. We close the week by zooming out — what does each operation actually *cost*? — so you can pick the right structure deliberately.

---

## 1. Why comprehensions exist

Suppose you want the squares of the numbers 0–9. With a plain loop:

```python
squares: list[int] = []
for n in range(10):
    squares.append(n * n)
```

Four lines, three concepts (declare, loop, mutate). Now the comprehension version:

```python
squares = [n * n for n in range(10)]
```

One line, one concept (a transformation of an iterable). Comprehensions are:

- **Shorter** — the intent stands out.
- **Faster** — the interpreter can optimize them slightly compared to a manual `append` loop.
- **More expression-like** — they can sit inside function calls (`sum([n*n for n in range(10)])`).

But they are not always better. If logic gets complex, a regular `for` loop wins on readability. **A comprehension that needs a comment is a comprehension that should be a loop.**

See [PEP 202](https://peps.python.org/pep-0202/) for the original motivation.

---

## 2. List comprehension syntax

The general shape is:

```
[expression for item in iterable if condition]
```

Read it as: *"the `expression`, for each `item` in `iterable`, but only when `condition` is true."*

### Plain transformation

```python
names = ["ada", "grace", "linus"]
upper = [name.upper() for name in names]
# ['ADA', 'GRACE', 'LINUS']

word_lengths = [len(name) for name in names]
# [3, 5, 5]
```

### With a filter (`if`)

```python
nums = range(20)
evens = [n for n in nums if n % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

passing = [grade for grade in [55, 72, 88, 41, 95] if grade >= 60]
# [72, 88, 95]
```

The `if` is a filter — it decides which items survive.

### With `if`/`else` inside the expression

If you want to *transform* the item differently depending on a condition, the conditional goes **before** the `for`:

```python
nums = range(6)
labels = ["even" if n % 2 == 0 else "odd" for n in nums]
# ['even', 'odd', 'even', 'odd', 'even', 'odd']
```

Read this as: *"`('even' if … else 'odd')` for each `n`."* It's a ternary expression inside the comprehension.

You can combine both forms:

```python
nums = range(10)
# Square evens, halve odds — only keep results <= 25
result = [
    (n * n if n % 2 == 0 else n // 2)
    for n in nums
    if (n * n if n % 2 == 0 else n // 2) <= 25
]
```

If that hurts to read, that's the lesson: **complex comprehensions should be loops**.

### Nested comprehensions

You can have multiple `for` clauses. They read left-to-right, like nested loops:

```python
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
# [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
```

Equivalent loop:

```python
pairs = []
for x in range(3):
    for y in range(3):
        if x != y:
            pairs.append((x, y))
```

A common nested case is **flattening** a matrix:

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [n for row in matrix for n in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

And **transposing** a matrix:

```python
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

**Warning**: anything with three or more `for` clauses, or two `for` clauses plus an `if`, is usually clearer as nested `for` loops. Don't sacrifice readability for one-liner pride.

---

## 3. Dict and set comprehensions

Same idea, different brackets.

### Dict comprehension

```python
{ key_expr: value_expr for item in iterable if condition }
```

```python
nums = range(6)
squares_map = {n: n * n for n in nums}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# invert a dict
codes = {"red": 1, "green": 2, "blue": 3}
inverted = {v: k for k, v in codes.items()}
# {1: 'red', 2: 'green', 3: 'blue'}

# filter a dict
ages = {"Ada": 37, "Grace": 85, "Linus": 54, "Kid": 12}
adults = {name: age for name, age in ages.items() if age >= 18}
```

### Set comprehension

```python
{ expression for item in iterable if condition }
```

(Note: same braces as a dict, but no `key: value` — Python tells them apart.)

```python
text = "the quick brown fox the lazy dog"
unique_words = {w for w in text.split()}
# {'the', 'quick', 'brown', 'fox', 'lazy', 'dog'}

first_letters = {w[0].upper() for w in text.split()}
# {'T', 'Q', 'B', 'F', 'L', 'D'}
```

---

## 4. Generator expressions (a preview)

Replace the brackets with parentheses and you get a **generator expression** — a lazy iterator that produces values one at a time:

```python
squares_gen = (n * n for n in range(10))
print(squares_gen)            # <generator object ...>
print(next(squares_gen))      # 0
print(next(squares_gen))      # 1
for s in squares_gen:
    print(s)
```

Why bother? Because generators **don't build the whole list in memory**. Two scenarios where this matters:

1. **Huge iterables** — `sum(n*n for n in range(10_000_000))` works fine with a generator and would waste memory as a list.
2. **Pipelines** — chain transformations without intermediate lists.

When a generator is the *only* argument to a function, you can omit the extra parens:

```python
total = sum(n * n for n in range(100))     # clean
any_negatives = any(x < 0 for x in nums)
all_positive  = all(x > 0 for x in nums)
```

You will study generators properly later in the bootcamp. For now: know they exist and that **`(...)` makes a generator, `[...]` makes a list, `{...}` makes a set or dict**.

---

## 5. Big-O — what each operation costs

You can write code that *works* without knowing Big-O, but you can't write code that *scales* without it. Here is the practical cheat sheet for CPython.

### Notation reminder

- **O(1)** — constant time, doesn't grow with input size.
- **O(log n)** — slow growth (binary search).
- **O(n)** — linear, grows proportionally.
- **O(n log n)** — sort-like.
- **O(n²)** — quadratic, nested-loop territory.

`n` below is the size of the container.

### List operations

| Operation | Cost | Notes |
|---|---|---|
| `lst[i]` | O(1) | Index lookup |
| `lst[i] = x` | O(1) | Index assignment |
| `lst.append(x)` | O(1) amortized | Occasionally O(n) when the underlying array resizes |
| `lst.pop()` | O(1) | Remove from end |
| `lst.pop(0)` or `lst.insert(0, x)` | **O(n)** | Everything shifts |
| `x in lst` | **O(n)** | Linear scan |
| `lst.remove(x)` | **O(n)** | Scan + shift |
| `lst.sort()` / `sorted(lst)` | O(n log n) | Timsort |
| `len(lst)` | O(1) | Tracked internally |

### Set operations (average case)

| Operation | Cost |
|---|---|
| `x in s` | **O(1)** |
| `s.add(x)` | O(1) |
| `s.discard(x)` / `s.remove(x)` | O(1) |
| `A \| B`, `A & B`, `A - B` | O(len(A) + len(B)) |

Worst case for hash collisions can degrade to O(n), but for normal data this is rare.

### Dict operations (average case)

| Operation | Cost |
|---|---|
| `d[k]` | **O(1)** |
| `d[k] = v` | O(1) |
| `k in d` | **O(1)** |
| `del d[k]` | O(1) |
| `len(d)` | O(1) |
| Iteration | O(n) |

### The headline fact

> `x in list` is **O(n)**.
> `x in set` and `x in dict` are **O(1)** on average.

Translation: if you find yourself testing membership in a loop (`for x in some_list: if x in another_list: ...`), convert `another_list` to a `set` first. A short benchmark:

```python
import timeit

big_list = list(range(100_000))
big_set  = set(big_list)

# look for the last item (worst case for list)
print(timeit.timeit("99_999 in big_list", globals=globals(), number=1000))
print(timeit.timeit("99_999 in big_set",  globals=globals(), number=1000))
```

You'll see the list version take roughly **1000x** longer.

See [TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity) for the full table.

---

## 6. Picking the right structure — a recipe

For each use case, ask three questions:

1. **What kind of access do I need?** Position (`[i]`), key (`d[k]`), or "is X present?"
2. **Do duplicates matter?**
3. **Will order matter when I iterate?**

| Use case | Structure | Why |
|---|---|---|
| Sequence of items, may grow | `list` | Indexed, ordered, mutable |
| Fixed record / coordinates | `tuple` / `namedtuple` | Immutable, hashable |
| Test membership / deduplicate | `set` | O(1) `in`, automatic uniqueness |
| Lookup value by key | `dict` | O(1) by key |
| Count occurrences | `dict` or `collections.Counter` | Map item → count |
| Group items by category | `dict[str, list]` or `defaultdict(list)` | Category → items |
| Nested record (e.g. "products by category") | `dict[str, dict[str, T]]` | Two-level key access |
| Cache, hashable read-only set | `frozenset` | Hashable, immutable |

---

## 7. Putting it together

Here's a realistic snippet that uses every concept from the week:

```python
from collections import Counter

logs: list[dict] = [
    {"user": "ada",   "action": "login",  "country": "UK"},
    {"user": "ada",   "action": "logout", "country": "UK"},
    {"user": "grace", "action": "login",  "country": "US"},
    {"user": "linus", "action": "login",  "country": "FI"},
    {"user": "ada",   "action": "login",  "country": "UK"},
]

# Unique users (set comprehension)
users: set[str] = {log["user"] for log in logs}

# Count logins per country (Counter from a generator expression)
logins_by_country = Counter(
    log["country"] for log in logs if log["action"] == "login"
)

# Logs grouped by user (dict comprehension over a set, then list comp)
by_user: dict[str, list[dict]] = {
    u: [log for log in logs if log["user"] == u] for u in users
}

print(users)              # {'ada', 'grace', 'linus'}
print(logins_by_country)  # Counter({'UK': 2, 'US': 1, 'FI': 1})
print(by_user["ada"])     # 3 records
```

Eight lines of real work. That's the payoff for this week.

---

## 8. What to do next

1. Complete **Exercise 05** (convert loops to comprehensions).
2. Tackle the **challenges** (`challenges/`).
3. Build the **mini-project** (contact book).
4. Take the **quiz**.

---

**Sources**
- [Python tutorial — List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [PEP 202 — List Comprehensions](https://peps.python.org/pep-0202/)
- [PEP 274 — Dict Comprehensions](https://peps.python.org/pep-0274/)
- [TimeComplexity (Python wiki)](https://wiki.python.org/moin/TimeComplexity)
- [Real Python — List Comprehensions in Python](https://realpython.com/list-comprehension-python/)
