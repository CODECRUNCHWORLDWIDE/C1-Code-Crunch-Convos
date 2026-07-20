# Python Syntax Cheatsheet

One-page reference. For depth, see the [official docs](https://docs.python.org/3/).

## Variables & literals

```python
name = "Ada"            # str
age = 36                # int
pi = 3.14159            # float
is_active = True        # bool
nothing = None          # NoneType
```

## Strings

```python
s = "hello"
len(s)                  # 5
s.upper()               # "HELLO"
s.replace("l", "L")     # "heLLo"
s.split("l")            # ['he', '', 'o']
",".join(["a", "b"])    # "a,b"

# f-strings
f"My name is {name}, age {age}."
f"{pi:.2f}"             # "3.14"
```

## Numbers

```python
a + b   a - b   a * b   a / b      # true division → float
a // b                              # floor division
a % b                               # remainder
a ** b                              # exponent
abs(-5)   round(2.7)   min(1, 2)    # built-ins
```

## Booleans & comparison

```python
==  !=  <  >  <=  >=
and  or  not
x is None              # identity, use for None
x in [1, 2, 3]         # membership
```

## Conditionals

```python
if x > 0:
    ...
elif x == 0:
    ...
else:
    ...

# Ternary
status = "adult" if age >= 18 else "minor"
```

## Loops

```python
for item in [1, 2, 3]:
    print(item)

for i in range(5):           # 0..4
    print(i)

for i, v in enumerate(seq):
    print(i, v)

while condition:
    ...

# break and continue
for x in data:
    if x is None:
        continue
    if x == "stop":
        break
```

## Lists

```python
nums = [1, 2, 3]
nums.append(4)        # [1, 2, 3, 4]
nums.pop()            # returns 4
nums[0]               # 1 — first
nums[-1]              # last
nums[1:3]             # slice
nums.sort()           # in-place
sorted(nums)          # returns a new list
len(nums)
3 in nums             # True

# Comprehension
squares = [x*x for x in range(10)]
evens = [x for x in nums if x % 2 == 0]
```

## Tuples

```python
point = (3, 4)
x, y = point          # unpack
```

## Dicts

```python
user = {"name": "Ada", "age": 36}
user["name"]          # "Ada"
user.get("email")     # None (safer than user["email"])
user["email"] = "ada@example.com"
del user["age"]
"name" in user        # True
for key, value in user.items(): ...

# Dict comprehension
inverted = {v: k for k, v in user.items()}
```

## Sets

```python
s = {1, 2, 3}
s.add(4)
s.discard(2)          # no error if missing
{1, 2} | {2, 3}       # union
{1, 2} & {2, 3}       # intersection
{1, 2} - {2}          # difference
```

## Functions

```python
def greet(name: str, times: int = 1) -> str:
    """Return a greeting repeated `times` times."""
    return f"Hello, {name}!\n" * times

# Positional, keyword, default, *args, **kwargs
def f(a, b, c=10, *args, **kwargs): ...

# Lambdas (anonymous)
double = lambda x: x * 2
```

## Files

```python
# Read
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
    # or .readlines(), or iterate: for line in f:

# Write
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
```

## Errors

```python
try:
    risky()
except ValueError as e:
    print(f"bad value: {e}")
except (TypeError, KeyError):
    print("type or key error")
else:
    print("no error")
finally:
    print("always runs")

# Raise
raise ValueError("explanation")
```

## Classes

```python
class Dog:
    species = "Canis familiaris"   # class attribute

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def bark(self) -> str:
        return f"{self.name} says woof!"

    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, age={self.age})"

d = Dog("Rex", 4)
d.bark()
```

## Inheritance

```python
class Puppy(Dog):
    def bark(self) -> str:
        return super().bark().lower()
```

## Modules & imports

```python
import math
from pathlib import Path
from collections import defaultdict, Counter
import json
import csv
```

## Useful built-ins

```python
type(x)   isinstance(x, int)
list(...)   tuple(...)   set(...)   dict(...)
sorted(seq, key=lambda x: x.age, reverse=True)
zip([1,2], ["a","b"])     # → [(1,"a"), (2,"b")]
map(fn, seq)              # apply fn to each
filter(pred, seq)
sum(seq)   max(seq)   min(seq)
any([T, F, F])   all([T, T])
```

## Standard library highlights

| Module          | What it's for                                  |
| --------------- | ---------------------------------------------- |
| `os` / `pathlib`| File paths, env vars                           |
| `sys`           | argv, exit, stdout                             |
| `json`          | Parse / serialize JSON                         |
| `csv`           | CSV files                                      |
| `datetime`      | Dates and times                                |
| `re`            | Regular expressions                            |
| `collections`   | `Counter`, `defaultdict`, `deque`, `namedtuple`|
| `itertools`     | `chain`, `groupby`, `combinations`, ...        |
| `functools`     | `lru_cache`, `partial`, `reduce`               |
| `subprocess`    | Run shell commands                             |
| `argparse`      | Command-line argument parsing                  |
| `logging`       | Structured logs                                |
| `unittest`      | Built-in testing (we'll use pytest instead)    |

Full standard library: <https://docs.python.org/3/library/>
