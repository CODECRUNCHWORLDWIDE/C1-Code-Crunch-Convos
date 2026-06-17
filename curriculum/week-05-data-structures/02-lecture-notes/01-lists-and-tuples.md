# 01 — Lists and Tuples

> "If your data is a sequence of related things, reach for a list. If it's a fixed record with a known shape, reach for a tuple." — A useful first heuristic.

Reading time: **~25 minutes**. Type along in a Python REPL as you go.

---

## 1. Why we need containers

Up to now, your variables have held *one* value at a time: `age = 30`, `name = "Ada"`. Real programs need to hold **collections** — a list of contacts, the lines of a file, the scores of a class. Python ships with four primary built-in containers:

| Type | Ordered? | Mutable? | Allows duplicates? | Typical use |
|---|---|---|---|---|
| `list` | yes | yes | yes | a growing sequence of items |
| `tuple` | yes | **no** | yes | a fixed record (e.g. `(x, y)` coordinates) |
| `set` | no | yes | **no** | uniqueness, membership tests |
| `dict` | yes (insertion order, since 3.7) | yes | keys unique | key → value lookup |

This lecture covers **lists** and **tuples**. The next lecture covers sets and dicts.

---

## 2. Creating lists

A list is a comma-separated sequence inside square brackets.

```python
empty: list = []
primes: list[int] = [2, 3, 5, 7, 11]
mixed: list = [1, "two", 3.0, True, None]   # legal but usually a code smell
```

Lists can hold *anything*, including other lists:

```python
matrix: list[list[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
```

You can also build a list from any iterable using `list()`:

```python
chars = list("hello")          # ['h', 'e', 'l', 'l', 'o']
numbers = list(range(5))       # [0, 1, 2, 3, 4]
```

---

## 3. Indexing and slicing

Lists are **zero-indexed**. Negative indices count from the end (`-1` is the last item).

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

fruits[0]    # 'apple'
fruits[1]    # 'banana'
fruits[-1]   # 'elderberry'
fruits[-2]   # 'date'
```

A **slice** `[start:stop:step]` returns a new list. `start` is inclusive, `stop` is exclusive. Any part can be omitted.

```python
fruits[1:3]    # ['banana', 'cherry']
fruits[:2]     # ['apple', 'banana']
fruits[2:]     # ['cherry', 'date', 'elderberry']
fruits[::2]    # ['apple', 'cherry', 'elderberry']   (every 2nd)
fruits[::-1]   # full reverse
```

Out-of-range *indexing* raises `IndexError`. Out-of-range *slicing* silently clamps:

```python
fruits[100]      # IndexError: list index out of range
fruits[100:200]  # [] -- no error
```

You can **assign through a slice**, which replaces a range:

```python
nums = [1, 2, 3, 4, 5]
nums[1:4] = [20, 30]   # replace 3 elements with 2
# nums == [1, 20, 30, 5]
```

---

## 4. The list methods you must know

Lists are mutable — methods modify them **in place** and return `None`. This trips up beginners constantly:

```python
sorted_list = [3, 1, 2].sort()   # WRONG: sorted_list is None
```

| Method | What it does | Returns |
|---|---|---|
| `lst.append(x)` | add `x` to the end | `None` |
| `lst.extend(it)` | append all items of iterable `it` | `None` |
| `lst.insert(i, x)` | insert `x` at index `i` | `None` |
| `lst.pop()` / `lst.pop(i)` | remove and return last (or i-th) item | the item |
| `lst.remove(x)` | remove the first occurrence of `x` | `None` (raises `ValueError` if absent) |
| `lst.clear()` | empty the list | `None` |
| `lst.sort(key=..., reverse=...)` | sort **in place** | `None` |
| `lst.reverse()` | reverse **in place** | `None` |
| `lst.index(x)` | first index of `x` | `int` (raises `ValueError`) |
| `lst.count(x)` | how many times `x` appears | `int` |
| `lst.copy()` | shallow copy | new list |

If you want a *new* sorted list without modifying the original, use the **built-in** `sorted()`:

```python
original = [3, 1, 2]
new_sorted = sorted(original)   # [1, 2, 3]; original unchanged
```

### Examples

```python
queue: list[str] = []
queue.append("Ada")
queue.append("Linus")
queue.append("Grace")
print(queue)            # ['Ada', 'Linus', 'Grace']

queue.extend(["Guido", "Donald"])
print(queue)            # ['Ada', 'Linus', 'Grace', 'Guido', 'Donald']

queue.insert(0, "Alan")  # insert at the front
print(queue)            # ['Alan', 'Ada', 'Linus', 'Grace', 'Guido', 'Donald']

first = queue.pop(0)     # 'Alan'
last = queue.pop()       # 'Donald'

queue.remove("Linus")    # removes first occurrence
print(queue)            # ['Ada', 'Grace', 'Guido']

queue.sort()             # alphabetical
queue.sort(key=len)      # by string length
queue.sort(reverse=True) # descending
```

A common pitfall: `lst.insert(0, x)` is **O(n)** because every other item must shift right. If you need a queue, use `collections.deque` (you will meet it later).

---

## 5. Mutation vs reassignment

This is the single most important concept in this lecture. Watch carefully:

```python
a = [1, 2, 3]
a.append(4)        # mutation: a is still the same object
print(a)           # [1, 2, 3, 4]

a = [99, 100]      # reassignment: a now points to a NEW list
```

To Python, a variable name is a **label** stuck onto an object. Mutation changes the object; reassignment moves the label.

### Aliasing — the gotcha

When you write `b = a`, you do **not** copy the list. You give the same list a second name.

```python
a = [1, 2, 3]
b = a              # b and a refer to the SAME list
b.append(4)
print(a)           # [1, 2, 3, 4]   <-- surprise!
```

Use `id()` to confirm:

```python
print(id(a), id(b))   # same number
print(a is b)         # True
```

This is *not* a Python bug — it's how object references work. But it bites every beginner. The fix is to make a copy explicitly.

### Shallow copy

`list.copy()` (or the slice `a[:]`, or `list(a)`) creates a **new** list containing the **same** items.

```python
import copy

a = [1, 2, 3]
b = a.copy()       # or a[:], or list(a), or copy.copy(a)
b.append(4)
print(a)           # [1, 2, 3]      <-- unaffected
print(b)           # [1, 2, 3, 4]
```

Shallow copy is enough for lists of immutable items (ints, strings, tuples of primitives).

### Deep copy

If your list contains *other* mutable objects (like nested lists or dicts), a shallow copy only copies the outer list; the inner objects are still shared.

```python
import copy

grid = [[1, 2], [3, 4]]
shallow = grid.copy()
shallow[0].append(999)
print(grid)        # [[1, 2, 999], [3, 4]]   <-- inner list is shared!
```

Use `copy.deepcopy()` for a fully independent copy:

```python
deep = copy.deepcopy(grid)
deep[0].append(7)
print(grid)        # unchanged
print(deep)        # [[1, 2, 999, 7], [3, 4]]
```

Rule of thumb: if you have nested mutable structures, use `deepcopy`. Otherwise, shallow is faster and sufficient.

See the [`copy` module docs](https://docs.python.org/3/library/copy.html) for the full story.

---

## 6. Iterating lists

The Pythonic way is the `for` loop:

```python
for fruit in fruits:
    print(fruit.upper())
```

If you need both the index and the value, use `enumerate`:

```python
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

If you need to iterate two lists in parallel, use `zip`:

```python
names = ["Ada", "Grace", "Guido"]
ages  = [37, 85, 67]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

Avoid `for i in range(len(lst))` unless you genuinely need the index.

---

## 7. Tuples — immutable sequences

A tuple looks like a list but uses parentheses (or no brackets at all) and **cannot be modified after creation**.

```python
point: tuple[int, int] = (3, 4)
rgb = (255, 128, 0)
single = (42,)       # NOTE the trailing comma -- (42) is just an int in parens
empty = ()
implicit = 1, 2, 3   # also a tuple
```

Tuples support the same indexing, slicing, `len()`, `in`, iteration, and `+`/`*` operators as lists. They just lack methods that would mutate them:

```python
point[0]            # 3
len(point)          # 2
3 in point          # True
point + (5,)        # (3, 4, 5)   -- new tuple
point * 2           # (3, 4, 3, 4)
```

### Why use a tuple instead of a list?

1. **Intent** — a tuple signals "this is a fixed record". A list signals "this might grow or change". Reading `(latitude, longitude)` vs `[latitude, longitude]` tells the reader something.
2. **Safety** — you can't accidentally append to it.
3. **Hashability** — tuples of hashable items are hashable, which means you can use them as **dict keys or set members**. Lists cannot.
4. **Slight performance edge** — tuples are marginally faster to construct and iterate.

```python
coords_seen: set[tuple[int, int]] = set()
coords_seen.add((3, 4))
coords_seen.add((3, 4))    # no effect; set is still {(3, 4)}
```

### Packing and unpacking

This is one of Python's most beloved features.

```python
# packing
person = "Ada", 37, "Engineer"     # tuple of 3

# unpacking
name, age, role = person
print(name, age, role)             # Ada 37 Engineer

# swap variables
a, b = 1, 2
a, b = b, a                        # no temp variable needed
```

Use `*` to grab "the rest":

```python
first, *middle, last = [1, 2, 3, 4, 5]
print(first)    # 1
print(middle)   # [2, 3, 4]   (middle is a list!)
print(last)     # 5
```

This pattern works for function return values too:

```python
def min_max(nums: list[int]) -> tuple[int, int]:
    return min(nums), max(nums)

lo, hi = min_max([3, 1, 4, 1, 5, 9, 2, 6])
```

### `namedtuple` — tuples with field names

When a tuple has more than 2 or 3 fields, accessing them by index (`person[0]`, `person[1]`) gets hard to read. `collections.namedtuple` builds a tuple subclass with named fields:

```python
from collections import namedtuple

Contact = namedtuple("Contact", ["name", "email", "phone"])
ada = Contact("Ada Lovelace", "ada@example.com", "555-0100")

print(ada.name)        # 'Ada Lovelace'
print(ada.email)       # 'ada@example.com'
print(ada[0])          # still works -- it IS a tuple

# still immutable
ada.email = "new@x"    # AttributeError
```

You get readability *and* immutability. For mutable records, you'll later prefer `@dataclass` (Week 7), but `namedtuple` is perfect for lightweight read-only records and serialization.

See [`collections.namedtuple` docs](https://docs.python.org/3/library/collections.html#collections.namedtuple).

---

## 8. Quick reference

```python
# Lists
nums = [1, 2, 3]
nums.append(4); nums.extend([5, 6]); nums.insert(0, 0)
nums.pop(); nums.remove(2); nums.sort(); nums.reverse()
copy_of = nums.copy()

# Tuples
point = (3, 4)
x, y = point
seen = {(1, 2), (3, 4)}   # tuples can live in sets

# Named tuples
from collections import namedtuple
Point = namedtuple("Point", "x y")
p = Point(3, 4); p.x; p.y
```

---

## 9. What to do next

1. Open a REPL and type every example above by hand. Don't copy-paste.
2. Do **Exercise 01** (`exercises/exercise-01-list-operations.py`).
3. Do **Exercise 02** (`exercises/exercise-02-deduplicate.py`).
4. Continue to lecture **02 — Sets and Dicts**.

---

**Sources**
- [Python tutorial — Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Built-in Types — Sequence Types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
- [`copy` module](https://docs.python.org/3/library/copy.html)
- [`collections.namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple)
