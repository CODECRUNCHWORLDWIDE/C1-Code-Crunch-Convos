# Lecture 01 — Variables and Built-in Types

Every program manipulates values: numbers, text, true/false flags, missing
information. Before you can manipulate a value, you need a way to refer to
it. That's what variables are for. In this lecture you'll learn how Python
stores values, the five core types you'll use every day, what *dynamic
typing* actually means, and how to convert safely between types.

## 1. What is a Variable?

A variable is a **name** that refers to a **value** stored in memory. In
Python you create one with a single `=` sign:

```python
age = 30
name = "Ada"
pi = 3.14159
is_active = True
```

After those four lines run, Python has four names in its current namespace,
each pointing at a value. You can use a variable anywhere you'd otherwise
use the value:

```python
print(age)          # 30
print(name + "!")   # Ada!
print(pi * 2)       # 6.28318
```

The `=` sign in Python is **not** the equals sign from math. It's the
**assignment operator**. It says "make this name refer to that value."
Reading `age = 30` aloud as "age gets thirty" or "age is assigned thirty"
will save you a lot of confusion later.

## 2. Dynamic Typing

In some languages (Java, C, Rust) you must declare a variable's type up
front and you can never change it. Python is different: the **type belongs
to the value, not the name**. You can reassign a variable to a value of a
completely different type and Python will not complain:

```python
x = 10          # x refers to an int
x = "ten"       # now x refers to a str
x = [1, 2, 3]   # now x refers to a list
```

This is called **dynamic typing**. It makes Python fast to write but means
you have to keep types straight in your head — or, as you'll see in
Lecture 3, use *type hints* to document your intent.

A subtle point: when you do `x = "ten"`, Python doesn't erase the integer
`10` from memory. It just stops `x` from pointing at it. Garbage collection
cleans up unused values eventually.

## 3. Naming Conventions (PEP 8)

Python is permissive about variable names, but the community follows
[PEP 8](https://peps.python.org/pep-0008/) closely. Follow these rules and
your code will look professional from day one:

- **Variables and functions** use `snake_case`: `total_price`,
  `user_name`, `is_valid`.
- **Constants** (values you don't intend to change) use
  `UPPER_SNAKE_CASE`: `MAX_RETRIES`, `PI`, `API_BASE_URL`.
- **Classes** (Week 7) use `CapWords`: `OrderItem`, `HttpClient`.
- Names start with a letter or underscore, never a digit.
- Names are case-sensitive: `name` and `Name` are different variables.
- Don't shadow built-ins: avoid `list`, `dict`, `str`, `type`, `sum`,
  `input` as variable names.
- Use descriptive names. `customer_count` beats `cc` every time.

Reserved words like `if`, `for`, `class`, `True`, `None`, `def`, `return`,
and a few dozen others cannot be used as names at all. Your editor will
highlight them.

## 4. The Five Core Built-in Types

For the first half of this bootcamp you'll use just five types constantly.
Let's meet each one.

### 4.1 `int` — integers

Whole numbers, positive or negative, with no fractional part. Python
integers have arbitrary precision — they can be as large as your memory
allows.

```python
year = 2026
score = -7
big = 10 ** 100  # a googol, no overflow
print(type(year))  # <class 'int'>
```

Underscores can be used as visual separators in large numbers:

```python
distance_to_sun_km = 149_600_000
```

### 4.2 `float` — floating-point numbers

Numbers with a decimal point. Python uses 64-bit IEEE 754 doubles, which
means `0.1 + 0.2` is famously `0.30000000000000004`, not `0.3`. This is
not a Python bug; it's how binary floating point works. For money, use the
`decimal` module (covered later). For everything else, format your output
to a sensible number of decimal places.

```python
pi = 3.14159
temperature = -2.5
print(type(pi))  # <class 'float'>
print(0.1 + 0.2)  # 0.30000000000000004
```

You can also write floats in scientific notation:

```python
plancks_constant = 6.626e-34  # 6.626 * 10^-34
```

### 4.3 `str` — strings

Text. Strings are sequences of Unicode characters wrapped in single quotes,
double quotes, or triple quotes for multi-line content. Choose whichever
quote style avoids needing to escape characters inside the string.

```python
greeting = "Hello, world!"
name = 'Ada'
multiline = """This string
spans multiple
lines."""
print(type(greeting))  # <class 'str'>
print(len(multiline))  # 32
```

Strings are **immutable**: you cannot change a character in place. You can
only build a new string. We'll cover string operations in detail in
Lecture 2.

### 4.4 `bool` — booleans

Truth values. Exactly two of them, with capital first letters: `True` and
`False`. They're the result of every comparison and the input to every
logical operation.

```python
is_logged_in = True
is_admin = False
print(type(is_logged_in))  # <class 'bool'>
print(5 > 3)               # True
```

A curious detail: `bool` is a subclass of `int`. `True` equals `1` and
`False` equals `0`. You'll occasionally see code that exploits this (e.g.
`sum([True, False, True])` gives `2`). It's clever; don't write it
yourself.

### 4.5 `None` — the absence of a value

`None` is Python's single "nothing" value. Use it to signal "no result
yet," "not applicable," or "default." It is its own type, `NoneType`, with
exactly one instance.

```python
result = None
print(type(result))  # <class 'NoneType'>
print(result is None)  # True
```

The idiomatic way to check for `None` is `is None`, not `== None`. We'll
explain why in Week 5 when we cover identity vs equality.

## 5. Mutable vs Immutable (A Preview)

Two things can be true of a value: you can rebind a *name* to a different
value (always allowed), or you can change the value *itself* in place
(only allowed if the value is mutable). The five types you've met today
are all **immutable**:

- `int`, `float`, `bool`, `str`, and `None` cannot be changed in place.

Lists, dictionaries, and sets (Week 5) are **mutable**. This distinction
matters a lot once you start passing values around between functions, but
for now just file it away.

## 6. Inspecting Types: `type()` and `isinstance()`

Python ships two built-ins for asking "what type is this?":

```python
x = 42
print(type(x))             # <class 'int'>
print(type(x) is int)      # True
print(isinstance(x, int))  # True
```

`type()` returns the exact class. `isinstance()` also returns `True` for
subclasses, which is what you almost always want. Use `isinstance()`.

You can check against multiple types at once:

```python
def describe(value):
    if isinstance(value, (int, float)):
        print("a number")
    elif isinstance(value, str):
        print("text")
    else:
        print("something else")
```

(We haven't covered `if` formally yet — Week 3 — but the syntax should be
guessable.)

## 7. Type Casting

Casting means **converting** a value from one type to another. Python's
constructor functions do double duty as cast functions:

### 7.1 To `int`

```python
int("42")        # 42
int(3.9)         # 3 (truncates toward zero, doesn't round)
int(-3.9)        # -3
int(True)        # 1
int(False)       # 0
int("3.14")      # ValueError! int() can't parse a float string
int("3.14"[0])   # 3 (you'd have to chop it first, or go through float())
```

A common pattern: convert a float-shaped string in two steps:

```python
int(float("3.14"))  # 3
```

### 7.2 To `float`

```python
float("3.14")    # 3.14
float(7)         # 7.0
float("inf")     # inf — Python supports infinity
float("nan")     # nan — and not-a-number
float("seven")   # ValueError
```

### 7.3 To `str`

`str()` works on virtually anything and is what `print()` calls internally:

```python
str(42)          # '42'
str(3.14)        # '3.14'
str(True)        # 'True'
str(None)        # 'None'
str([1, 2, 3])   # '[1, 2, 3]'
```

### 7.4 To `bool` — Truthiness

This is the most interesting cast. `bool()` returns `False` for a fixed
set of *falsy* values and `True` for everything else. The official falsy
values are:

- `False`
- `None`
- Any zero of a numeric type: `0`, `0.0`, `0j`
- Any empty sequence or collection: `""`, `[]`, `()`, `{}`, `set()`,
  `range(0)`

Everything else is truthy. Examples:

```python
bool(0)        # False
bool(1)        # True
bool(-1)       # True (any non-zero number is truthy)
bool("")       # False
bool(" ")      # True (a space is a non-empty string)
bool("False")  # True (a non-empty string!)
bool(None)     # False
bool([])       # False
bool([0])      # True (the list has one element)
```

That last one trips people up: the string `"False"` is truthy because it
isn't empty. Truthiness operates on the *container*, not the content.

This is why you'll see Pythonic checks like `if name:` instead of `if name
!= "":` — it works for both empty strings and `None`, which is usually
what you want.

## 8. Putting It Together — Worked Examples

### Example 1: Inspecting a value

```python
value = "42"
print(value, type(value))   # 42 <class 'str'>
value = int(value)
print(value, type(value))   # 42 <class 'int'>
print(value + 1)            # 43
```

### Example 2: A truthiness gotcha

```python
user_input = input("Are you sure? ")
if bool(user_input):
    print("you typed something")
# The user could type "no" and this would still print —
# truthiness only checks if the string is non-empty!
```

### Example 3: Working with `None`

```python
last_login = None
if last_login is None:
    print("first time visitor")
```

### Example 4: A subtle int/float interaction

```python
print(10 / 3)    # 3.3333333333333335 — always returns a float
print(10 // 3)   # 3 — floor division, returns int when both args are int
print(10.0 // 3) # 3.0 — floor division of a float returns a float
```

### Example 5: Concatenation needs same types

```python
age = 30
# print("I am " + age)  # TypeError: can only concatenate str to str
print("I am " + str(age))  # I am 30
print(f"I am {age}")        # I am 30 (preferred — see Lecture 2)
```

### Example 6: `bool` as `int`

```python
flags = [True, True, False, True]
# True is 1, False is 0
print(sum(flags))  # 3
```

### Example 7: Reassigning across types

```python
result = 42         # int
result = 42.0       # float
result = "42"       # str
result = None       # NoneType
print(type(result)) # <class 'NoneType'>
```

### Example 8: Constants by convention

```python
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY
print(SECONDS_PER_DAY)  # 86400
```

Python has no real way to enforce that a constant doesn't change. The
`UPPER_SNAKE_CASE` name is a promise to other readers (and your future
self) that you won't reassign it.

### Example 9: Defensive casting

```python
raw = input("Enter your age: ")    # always returns a str
try:
    age = int(raw)
    print(f"Next year you'll be {age + 1}")
except ValueError:
    print(f"{raw!r} doesn't look like a whole number.")
```

We'll dig into `try`/`except` properly in Week 6, but you can already use
the pattern above.

### Example 10: `isinstance()` with a tuple

```python
def kind(x):
    if isinstance(x, bool):
        return "bool"   # check before int! bool is a subclass of int
    if isinstance(x, (int, float)):
        return "number"
    if isinstance(x, str):
        return "text"
    return "other"

print(kind(True))   # bool
print(kind(3.14))   # number
print(kind("hi"))   # text
print(kind(None))   # other
```

## 9. Wrap-up

You now know:

- How to create and reassign variables.
- That Python is dynamically typed and types belong to values.
- The five primitive types: `int`, `float`, `str`, `bool`, `None`.
- How to inspect a type with `type()` and `isinstance()`.
- How to cast between types and what truthiness means.

Lecture 2 covers what to **do** with these values: arithmetic, comparison,
and logical operators, plus a deeper dive on strings and f-strings.

## Further Reading

- [docs.python.org — Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [docs.python.org — Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
- [PEP 8 — Naming Conventions](https://peps.python.org/pep-0008/#naming-conventions)
