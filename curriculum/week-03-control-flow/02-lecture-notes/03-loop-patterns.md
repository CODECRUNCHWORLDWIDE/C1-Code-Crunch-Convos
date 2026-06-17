# Lecture 3 — Loop Patterns You Will Use Forever

The first two lectures gave you the syntax. This lecture is about
**recognizing patterns**: a handful of recipes that come up so often that
once you can spot them, half the loops you write afterwards will be
small variations of one of them. Mastering these five — counting,
accumulating, max/min, filtering, and searching — also gives you a
vocabulary to talk about your code in reviews and interviews.

## 1. Counting

Use a counter when you want to know "how many" of something there are.

```python
text = "Code Crunch Convos"
vowels = "aeiouAEIOU"
count = 0

for char in text:
    if char in vowels:
        count += 1

print(count)  # 6
```

The recipe:

1. Initialize a counter to `0` *before* the loop.
2. Walk the iterable.
3. When the condition matches, do `count += 1`.

A counter started at zero is the most common bug in beginner code: people
forget to initialize it, get a `NameError`, then declare it inside the
loop and reset it every iteration. **Initialize outside, update inside.**

## 2. Accumulating (sum, product, concat)

Same shape as counting, but instead of `+= 1` you accumulate values from
the iterable.

```python
numbers = [3, 7, 2, 8, 5]
total = 0

for n in numbers:
    total += n

print(total)  # 25
```

Product (use `1` as the starting value, since `x * 1 == x`):

```python
numbers = [3, 7, 2]
product = 1

for n in numbers:
    product *= n

print(product)  # 42
```

For sums and products of numeric iterables Python has built-ins:
`sum(numbers)` and `math.prod(numbers)`. Use them in real code; the
hand-rolled loop above is for teaching.

## 3. Max / min finding

To find the largest item, start by assuming the first item is the winner,
then update as you scan:

```python
numbers = [4, 9, 1, 7, 9, 3]
largest = numbers[0]

for n in numbers[1:]:
    if n > largest:
        largest = n

print(largest)  # 9
```

For `min`, flip the comparison to `<`. Notes:

- `numbers[1:]` skips the first item, since we already used it as the
  starting "best so far". Slicing is fine for short lists; for big lists
  it copies, which costs memory.
- If the iterable might be empty, decide up front what you want to do —
  either check `if not numbers: ...` first, or use a sentinel like
  `float("-inf")` for max.
- Python's built-in `max(numbers)` and `min(numbers)` exist; again, the
  hand-roll is for learning.

## 4. Filtering

Keep only the items that match a condition. The straightforward loop
version is:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = []

for n in numbers:
    if n % 2 == 0:
        evens.append(n)

print(evens)  # [2, 4, 6, 8, 10]
```

The recipe: empty list before the loop, `.append(...)` the items you want
to keep. In Week 5 we will rewrite this as a list comprehension:
`evens = [n for n in numbers if n % 2 == 0]`. For now, the explicit loop
is fine and very readable.

## 5. Searching with `break` (and the `else` clause)

Searching answers "is this item in there, and if so, where?".

```python
words = ["alpha", "beta", "gamma", "delta"]
target = "gamma"
found_at = -1

for index, word in enumerate(words):
    if word == target:
        found_at = index
        break

if found_at == -1:
    print(f"{target} not found.")
else:
    print(f"{target} found at index {found_at}.")
```

The cleaner way uses the `else` clause on the `for` loop you met in the
previous lecture:

```python
for index, word in enumerate(words):
    if word == target:
        print(f"{target} found at index {index}.")
        break
else:
    print(f"{target} not found.")
```

When you only care about presence, Python has the `in` operator:
`if target in words:`. Use it for simple membership checks. Use the loop
when you also need the index, or when the "check" is more complicated
than equality.

## 6. Building strings vs building lists (a performance hint)

Suppose you want to repeat the letter `"a"` `n` times. The obvious thing
is to glue characters onto a string in a loop:

```python
n = 10_000
result = ""

for _ in range(n):
    result += "a"   # slow!
```

This works, but it is **O(n²)** — Python strings are immutable, so each
`+=` allocates a brand-new string and copies all the previous characters
into it. Doing that 10,000 times is millions of character copies.

The Pythonic fix is to collect the pieces in a list and join them once at
the end:

```python
parts = []

for _ in range(n):
    parts.append("a")

result = "".join(parts)  # O(n)
```

`str.join(...)` walks the list once and produces the final string in a
single pass. This is the single most common surprise for people coming
from languages where strings are mutable. For tiny strings (a handful of
characters), `+=` is fine and readable. For big loops, reach for the
list-and-join pattern.

## 7. Putting two patterns together

Patterns combine. Here we count the long words and also collect them:

```python
sentence = "Control flow turns scripts into programs"
words = sentence.split()

long_words = []
long_count = 0

for word in words:
    if len(word) >= 7:
        long_words.append(word)
        long_count += 1

print(long_count, long_words)
```

You will write hundreds of loops shaped exactly like this — a counter, an
accumulator list, a guard, an `append`. Once you can see it, you will
also see how to *not* repeat yourself: helper functions (Week 4), list
comprehensions (Week 5), and built-ins like `sum`, `max`, `min`,
`filter`.

## 8. The underscore `_` as a "don't care" variable

In `for _ in range(n):` the underscore is a conventional Python name
that means "I am not going to use this value". It is just a regular
variable name — Python does not enforce anything special — but humans
reading the code immediately know "the loop index is irrelevant here, it
is just used for repetition". Use it whenever the loop variable is
unused.

## 9. A taste of Pythonic alternatives

You will see these in later weeks; we are previewing only.

- **List comprehension** (Week 5): `[n * 2 for n in numbers if n > 0]`
  builds a new list in one expression.
- **Generator expression**: `sum(n * n for n in numbers)` does the
  squaring and summing without ever building the list.
- **Built-ins**: `sum`, `min`, `max`, `any`, `all`, `len`, `sorted`,
  `reversed`, and `filter` cover the common loop patterns at C speed.

These do not replace the loop in your head — they replace the *typing*
once you can see the pattern.

## 10. A common-bug checklist

Run through these whenever your loop misbehaves:

- Did you **initialize** the counter / accumulator / "best so far"
  variable *before* the loop?
- Are you **updating** the loop variable (for `while`)?
- Is the condition correct? Off-by-one is the bug of all bugs — remember
  that `range(stop)` excludes `stop`.
- Did you `break` when you should have used `continue`, or vice versa?
- Are you modifying the list you are iterating over? Don't.
- For floats, are you comparing with `==`? Don't — use `math.isclose`.

## 11. Recap

- **Counting**: zero-initialized counter, `+= 1` on match.
- **Accumulating**: zero (sum) or one (product) initial, `+=` or `*=`
  inside the loop.
- **Max/min**: start with the first item, compare and replace.
- **Filtering**: empty list, `.append(...)` what you want to keep.
- **Searching**: walk with `enumerate`, `break` when found, use the loop
  `else` to print a "not found" message.
- **Strings**: build with a list and `"".join(...)` for big loops; raw
  `+=` is O(n²).
- Underscore `_` means "I do not care about this value".
- Built-ins and comprehensions will replace many of these by-hand loops
  in later weeks — but learning the loop first means the built-ins make
  sense rather than feel like magic.

With patterns in hand, head to the exercises and try to spot which
pattern each one is asking for *before* you start typing.
