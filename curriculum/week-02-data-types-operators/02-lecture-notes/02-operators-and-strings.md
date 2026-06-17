# Lecture 02 — Operators and Strings

In Lecture 1 you learned about values and the types they belong to. This
lecture teaches you what to *do* with those values: arithmetic, comparison,
logic, and the most important type of all — strings. By the end, you'll
read and write expressions confidently and format output that looks
professional.

## 1. Arithmetic Operators

Python supports the seven arithmetic operators you'd expect from a
calculator, plus one (`//`) you might not have seen before.

| Operator | Name              | Example   | Result |
|----------|-------------------|-----------|-------:|
| `+`      | Addition          | `7 + 3`   |   `10` |
| `-`      | Subtraction       | `7 - 3`   |    `4` |
| `*`      | Multiplication    | `7 * 3`   |   `21` |
| `/`      | True division     | `7 / 3`   | `2.333...` |
| `//`     | Floor division    | `7 // 3`  |    `2` |
| `%`      | Modulo (remainder)| `7 % 3`   |    `1` |
| `**`     | Exponent          | `2 ** 10` | `1024` |

Three of these deserve special attention.

### 1.1 True division `/` always returns a float

```python
print(10 / 2)   # 5.0 — not 5!
print(10 / 3)   # 3.3333333333333335
```

If you want an integer result and you know the division is exact, cast it:
`int(10 / 2)`. If you want floor division, use `//`.

### 1.2 Floor division `//` rounds **down**, not toward zero

```python
print(7 // 3)    # 2
print(-7 // 3)   # -3  (not -2 — it rounds toward negative infinity)
```

### 1.3 Modulo `%` and a classic trick

The remainder operator is how you check divisibility:

```python
def is_even(n):
    return n % 2 == 0

print(is_even(4))   # True
print(is_even(7))   # False
```

Modulo also handles "wrap around" — useful for cyclic things like days of
the week.

### 1.4 Exponent `**`

```python
print(2 ** 10)     # 1024
print(2 ** 0.5)    # 1.4142135623730951 — square root
print(10 ** -2)    # 0.01
```

### 1.5 Augmented assignment

These shortcuts let you update a variable in place:

```python
count = 0
count += 1   # same as: count = count + 1
count -= 1
count *= 2
count //= 3
count %= 5
count **= 2
```

All seven arithmetic operators have an augmented form.

## 2. Operator Precedence

When an expression mixes operators, Python evaluates them in a fixed
order. The full table is in the
[official docs](https://docs.python.org/3/reference/expressions.html#operator-precedence).
You only need to remember a handful for arithmetic:

1. Parentheses `()` — always evaluated first.
2. Exponent `**` — right-associative.
3. Unary `-` (negation) and `+`.
4. `*`, `/`, `//`, `%` — left-to-right.
5. `+`, `-` — left-to-right.

Examples:

```python
print(2 + 3 * 4)        # 14, not 20
print((2 + 3) * 4)      # 20
print(2 ** 3 ** 2)      # 512, because ** is right-associative: 2**(3**2) = 2**9
print(-2 ** 2)          # -4! Unary minus is *lower* precedence than **
print((-2) ** 2)        # 4
```

When in doubt, use parentheses. Clarity beats cleverness.

## 3. Comparison Operators

Comparison operators always return a `bool`.

| Operator | Meaning              | Example  | Result |
|----------|----------------------|----------|--------|
| `==`     | Equal to             | `5 == 5` | `True` |
| `!=`     | Not equal to         | `5 != 4` | `True` |
| `<`      | Less than            | `5 < 9`  | `True` |
| `>`      | Greater than         | `9 > 5`  | `True` |
| `<=`     | Less than or equal   | `5 <= 5` | `True` |
| `>=`     | Greater than or equal| `5 >= 6` | `False`|

Pitfalls:

- `=` is assignment; `==` is comparison. Mixing them up is the single
  most common beginner bug.
- Comparing different types: most cross-type comparisons (e.g. `1 < "a"`)
  raise `TypeError`. Numeric types interoperate (`1 == 1.0` is `True`).
- Floating-point equality is unreliable. `0.1 + 0.2 == 0.3` is `False`.
  For floats, compare with a tolerance: `abs(a - b) < 1e-9`.

Python also supports **chained comparisons**, which read like math:

```python
age = 25
print(18 <= age < 65)   # True
# equivalent to:
print(18 <= age and age < 65)
```

## 4. Logical Operators

Three of them: `and`, `or`, `not`. Use lowercase English words, not `&&`
or `||` from other languages.

```python
is_admin = True
is_active = False

print(is_admin and is_active)  # False — both must be True
print(is_admin or is_active)   # True  — at least one is True
print(not is_admin)            # False
```

### 4.1 Short-circuit evaluation

`and` and `or` don't always evaluate both sides:

- `False and X` returns `False` without looking at `X`.
- `True or X` returns `True` without looking at `X`.

This is called *short-circuiting* and is useful for guarding against
errors:

```python
name = ""
# This would crash if name were None or empty without the guard:
if name and name[0].isupper():
    print("starts uppercase")
```

### 4.2 `and`/`or` return values, not just booleans

Subtle but powerful:

```python
print(0 or "default")    # "default"
print(5 or "default")    # 5
print(0 and "anything")  # 0
print(5 and "yes")       # "yes"
```

`or` returns the first truthy operand (or the last operand if all are
falsy). `and` returns the first falsy operand (or the last operand if all
are truthy). The Pythonic `value = user_input or "anonymous"` pattern
exploits this.

## 5. Strings — A Closer Look

You met `str` in Lecture 1. Now you'll learn to operate on them.

### 5.1 Creating strings

```python
single = 'hello'
double = "hello"
triple = """multi
line"""
```

All three produce the same type. Triple-quoted strings preserve newlines
and are commonly used for docstrings.

### 5.2 Indexing

Strings are sequences. You can grab a character by position with square
brackets. Indexing starts at **zero**, and negative indices count from
the end.

```python
word = "Python"
print(word[0])     # 'P'
print(word[1])     # 'y'
print(word[-1])    # 'n' — last character
print(word[-2])    # 'o' — second to last
print(len(word))   # 6
# print(word[6])   # IndexError: string index out of range
```

Indexing always returns a string of length 1 — Python has no separate
"char" type.

### 5.3 Slicing

Slicing extracts a *substring* using `[start:stop:step]`. The `start` is
included; the `stop` is excluded.

```python
word = "Python"
print(word[0:3])    # 'Pyt'
print(word[:3])     # 'Pyt' — start defaults to 0
print(word[3:])     # 'hon' — stop defaults to len(word)
print(word[:])      # 'Python' — full copy
print(word[::2])    # 'Pto' — every other character
print(word[::-1])   # 'nohtyP' — reversed (a classic idiom)
print(word[1:-1])   # 'ytho' — strip first and last character
```

Slicing never raises `IndexError`. If the slice is out of range, you get
an empty string:

```python
print("hi"[5:10])   # '' — no error
```

### 5.4 Common string methods

There are about 40 methods on `str`. The ones you'll use weekly:

| Method            | What it does                                              |
|-------------------|-----------------------------------------------------------|
| `s.upper()`       | Returns an uppercase copy                                 |
| `s.lower()`       | Returns a lowercase copy                                  |
| `s.title()`       | Capitalizes each word: `"my name"` → `"My Name"`          |
| `s.strip()`       | Removes leading/trailing whitespace                       |
| `s.lstrip()` / `rstrip()` | Removes only left or right whitespace            |
| `s.split(sep)`    | Splits into a list; `sep` defaults to any whitespace      |
| `s.replace(old, new)` | Returns a copy with all occurrences replaced          |
| `s.find(sub)`     | Returns index of first match, or `-1` if not found        |
| `s.index(sub)`    | Like `find()`, but raises `ValueError` if not found       |
| `s.startswith(prefix)` | `True` if the string starts with `prefix`            |
| `s.endswith(suffix)`   | `True` if the string ends with `suffix`              |
| `s.count(sub)`    | Number of non-overlapping occurrences                     |
| `s.isdigit()`     | `True` if all characters are digits and the string isn't empty |
| `s.isalpha()`     | `True` if all characters are letters                      |
| `s.join(iterable)`| Concatenates an iterable with `s` between each element    |

Crucially, **strings are immutable** — every method that "modifies" a
string actually returns a new one. The original is untouched:

```python
greeting = "  hello  "
trimmed = greeting.strip()
print(repr(greeting))  # '  hello  ' — unchanged
print(repr(trimmed))   # 'hello'
```

Worked examples:

```python
email = "  Ada.Lovelace@EXAMPLE.com  "
clean = email.strip().lower()
print(clean)                       # 'ada.lovelace@example.com'
print(clean.endswith("@example.com"))  # True

name = "Alan Turing"
parts = name.split()               # ['Alan', 'Turing']
first, last = parts[0], parts[1]
print(last)                        # 'Turing'

joined = "-".join(["2026", "05", "13"])
print(joined)                      # '2026-05-13'

sentence = "I love coffee. coffee is great."
print(sentence.replace("coffee", "tea"))
# 'I love tea. tea is great.'

print(sentence.count("coffee"))    # 2
print(sentence.find("tea"))        # -1 (not found)
```

### 5.5 Escape sequences

Some characters need an escape inside a string literal because they would
otherwise confuse Python's parser or be invisible. The escape character is
the backslash `\`.

| Escape | Meaning                  |
|--------|--------------------------|
| `\n`   | Newline                  |
| `\t`   | Tab                      |
| `\\`   | Literal backslash        |
| `\'`   | Literal single quote     |
| `\"`   | Literal double quote     |
| `\r`   | Carriage return          |
| `\0`   | Null character           |
| `\uXXXX` | Unicode code point     |

```python
print("Line 1\nLine 2")
# Line 1
# Line 2

print("Name:\tAda")
# Name:   Ada

print("Path: C:\\Users\\ada")
# Path: C:\Users\ada

print("She said \"hi\"")
# She said "hi"

print("✨ sparkle")  # ✨ sparkle (if your terminal supports it)
```

### 5.6 Raw strings

If a string contains many backslashes — common with Windows paths or
regular expressions — prefix it with `r` to disable escape interpretation:

```python
path = r"C:\Users\ada\Documents"
print(path)   # C:\Users\ada\Documents

pattern = r"\d{3}-\d{4}"  # a regex pattern; you'll meet regex later
```

A raw string still cannot end with a single backslash, but `r"\\"` (two
backslashes) works fine.

### 5.7 String concatenation and repetition

```python
print("foo" + "bar")    # 'foobar'
print("ha" * 3)         # 'hahaha'
print("-" * 40)         # a 40-character separator line
```

The `+` operator only works between two strings. To embed a non-string
value, cast it with `str()` or — better — use an f-string.

## 6. f-strings — Formatted String Literals

[PEP 498](https://peps.python.org/pep-0498/) introduced f-strings in
Python 3.6, and they're the right tool for almost every string-building
job today.

### 6.1 Basics

Prefix a string with `f` (or `F`) and put expressions in `{}`:

```python
name = "Ada"
age = 30
print(f"Hi, {name}. You are {age}.")
# Hi, Ada. You are 30.
```

The expression inside the braces is real Python — you can do math, call
methods, anything:

```python
price = 9.99
quantity = 3
print(f"Total: ${price * quantity}")          # Total: $29.97
print(f"Yelling: {name.upper()}!")            # Yelling: ADA!
print(f"Tomorrow you'll be {age + 1}")        # Tomorrow you'll be 31
```

### 6.2 Self-documenting expressions: `=`

A handy debugging shortcut: end the placeholder with `=` and Python prints
the source plus the value.

```python
x = 5
print(f"{x=}")          # x=5
print(f"{x * 2 + 1=}")  # x * 2 + 1=11
```

### 6.3 Format specs

After a colon inside the braces, you can give a *format spec* that
controls how the value is rendered. The full grammar lives in the
[Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language).
The essentials:

#### Numeric precision

```python
pi = 3.14159265
print(f"{pi:.2f}")    # '3.14' — fixed-point, 2 decimals
print(f"{pi:.4f}")    # '3.1416'
print(f"{pi:.0f}")    # '3'    — rounded to integer-like string
print(f"{pi:.3e}")    # '3.142e+00' — scientific notation
```

`.2f` means "fixed-point notation, two digits after the decimal." Use it
constantly when printing money or measurements.

#### Width and alignment

```python
name = "Ada"
print(f"|{name:>10}|")    # |       Ada| — right-aligned in width 10
print(f"|{name:<10}|")    # |Ada       | — left-aligned
print(f"|{name:^10}|")    # |   Ada    | — centered
print(f"|{name:*^10}|")   # |***Ada****| — centered, padded with *
```

#### Thousands separators

```python
big = 1_234_567
print(f"{big:,}")     # '1,234,567'
print(f"{big:_}")     # '1_234_567'
```

#### Percentages

```python
ratio = 0.875
print(f"{ratio:.1%}")  # '87.5%'
```

#### Combining specs

The full mini-language is `[[fill]align][sign][#][0][width][,][.precision][type]`.
You don't need to memorize that; remember the common ones and look the
rest up.

```python
amount = 12345.6789
print(f"{amount:>15,.2f}")   # '      12,345.68' — width 15, comma, 2 decimals
```

### 6.4 Multi-line f-strings

For receipts, banners, and reports:

```python
name = "Ada"
score = 92
print(f"""
+----------------------+
| Name : {name:<12} |
| Score: {score:>12} |
+----------------------+
""")
```

### 6.5 What f-strings cannot do

- They can't contain a backslash inside the braces. Compute the value
  outside, then reference it: `f"{'\\n'.join(parts)}"` is illegal; do
  `sep = "\n"; f"{sep.join(parts)}"` instead. (In Python 3.12+ this
  restriction was relaxed, but writing portable code today still respects
  it.)
- The same quote style as the surrounding string isn't allowed inside the
  braces in older Pythons. Use the opposite quote, or `'''`.

## 7. Putting It Together

```python
PRICE = 19.99
TAX_RATE = 0.07
QUANTITY = 3

subtotal = PRICE * QUANTITY
tax = subtotal * TAX_RATE
total = subtotal + tax

print(f"""
Item price : ${PRICE:>10,.2f}
Quantity   : {QUANTITY:>11}
Subtotal   : ${subtotal:>10,.2f}
Tax (7%)   : ${tax:>10,.2f}
{'-' * 28}
Total      : ${total:>10,.2f}
""")
```

Output:

```text
Item price : $     19.99
Quantity   :           3
Subtotal   : $     59.97
Tax (7%)   : $      4.20
----------------------------
Total      : $     64.17
```

That's a complete receipt printer in twelve lines, using nothing but the
material from this lecture.

## 8. Wrap-up

You can now:

- Compute with `+ - * / // % **` and understand precedence.
- Compare values and combine results with `and`, `or`, `not`.
- Index, slice, and call methods on strings.
- Write multi-line, aligned, padded, comma-formatted output with
  f-strings.

Lecture 3 closes the loop: you'll learn to *read* input from the user and
write your first type-annotated functions.

## Further Reading

- [docs.python.org — Operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)
- [docs.python.org — String methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [docs.python.org — Format spec mini-language](https://docs.python.org/3/library/string.html#format-specification-mini-language)
- [PEP 498 — Literal String Interpolation](https://peps.python.org/pep-0498/)
