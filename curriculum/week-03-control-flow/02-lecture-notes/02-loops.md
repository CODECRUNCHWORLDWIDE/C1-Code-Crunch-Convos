# Lecture 2 — Loops: Doing Things Repeatedly

Programs become powerful the moment you stop typing the same logic over
and over and let the computer repeat it for you. **Loops** are how Python
expresses repetition. There are two flavours: `while`, which loops as
long as a condition is true, and `for`, which loops through the items of
an *iterable* such as a string, list, or `range`. This lecture covers
both, plus the helpers `range()`, `enumerate()`, and `zip()`, the loop
control keywords `break` and `continue`, the surprisingly useful `else`
clause on loops, and nested loops. We will also look at infinite loops —
both how to write them on purpose and how to avoid them by accident.

## 1. The `while` loop

A `while` loop runs its body **as long as** a condition is true:

```python
count = 1

while count <= 5:
    print(f"count is {count}")
    count += 1

print("done")
```

Output:

```text
count is 1
count is 2
count is 3
count is 4
count is 5
done
```

The pattern is always:

1. Initialize a variable before the loop.
2. Check the condition at the top of the loop.
3. Update the variable inside the loop so that the condition eventually
   becomes false.

Skip step 3 and you have an **infinite loop** — Python will happily run
forever (or until you press `Ctrl+C`). For example, this is a bug:

```python
count = 1

# BUG: count is never incremented, so the condition stays True forever.
while count <= 5:
    print(count)
```

If you ever start an infinite loop in your terminal, press `Ctrl+C` to
interrupt it. Most editors also let you stop a running program with a
"stop" button.

### Intentional infinite loops

Sometimes you *want* a loop that runs until something explicit stops it,
such as a menu that runs until the user picks "quit". The idiomatic
pattern is `while True:` paired with `break`:

```python
while True:
    choice = input("> ").strip().lower()
    if choice == "quit":
        break
    print(f"You typed: {choice}")
```

This is clearer than trying to invent a flag variable, and it is the
backbone of the mini-project for this week.

## 2. The `for` loop

`for` loops iterate over the items of an **iterable**. An iterable is
anything you can step through one item at a time — strings, lists,
tuples, dictionaries, sets, files, and the special `range` object are all
iterables.

```python
for letter in "Python":
    print(letter)
```

```text
P
y
t
h
o
n
```

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")
```

The loop variable (`letter`, `fruit`) is created automatically and takes
on each item in turn. You can name it anything you like; pick a name that
describes one item from the collection.

## 3. `range()` — the bread-and-butter iterable for counting

`range(stop)` generates the integers `0, 1, 2, ..., stop - 1`. Crucially,
the `stop` value is **excluded**:

```python
for i in range(5):
    print(i)
# prints 0, 1, 2, 3, 4
```

`range(start, stop)` starts at `start` (inclusive) and stops at `stop`
(exclusive):

```python
for i in range(1, 6):
    print(i)
# prints 1, 2, 3, 4, 5
```

`range(start, stop, step)` adds a step size, which can be negative for
counting down:

```python
for i in range(0, 11, 2):
    print(i)
# prints 0, 2, 4, 6, 8, 10

for i in range(10, 0, -1):
    print(i)
# prints 10, 9, 8, ..., 1
```

A few useful facts:

- `range` returns a lightweight `range` object, *not* a list. It
  generates values on demand, so `range(10**9)` uses constant memory.
- To turn it into a list (for debugging, mostly): `list(range(5))`
  → `[0, 1, 2, 3, 4]`.
- The official reference is at
  <https://docs.python.org/3/library/stdtypes.html#range>.

## 4. `enumerate()` — index *and* value

When you need both the index and the value while iterating, do **not**
write `range(len(items))`. Use `enumerate()`:

```python
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

```text
0: apple
1: banana
2: cherry
```

`enumerate()` takes an optional `start` argument if you prefer 1-based
numbering:

```python
for n, fruit in enumerate(fruits, start=1):
    print(f"#{n} {fruit}")
```

Reference: <https://docs.python.org/3/library/functions.html#enumerate>.

## 5. `zip()` — iterate two (or more) iterables in parallel

To walk through two lists side-by-side, use `zip()`:

```python
names = ["Aisha", "Bayo", "Chen"]
scores = [88, 91, 79]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

```text
Aisha: 88
Bayo: 91
Chen: 79
```

`zip()` stops as soon as the *shortest* iterable runs out. If you want it
to raise an error when lengths differ, pass `strict=True` (Python 3.10+).
Reference: <https://docs.python.org/3/library/functions.html#zip>.

We will go deeper on `enumerate` and `zip` in Week 5 — this lecture is a
preview so you can use them in this week's exercises and homework.

## 6. `break` — leave the loop now

`break` exits the *innermost* loop immediately:

```python
for n in range(1, 11):
    if n == 5:
        break
    print(n)
# prints 1, 2, 3, 4 then stops
```

Use `break` for searches: as soon as you have found what you wanted,
there is no reason to keep iterating.

## 7. `continue` — skip to the next iteration

`continue` jumps straight to the next iteration without running the rest
of the loop body:

```python
for n in range(1, 11):
    if n % 2 == 0:
        continue
    print(n)
# prints 1, 3, 5, 7, 9
```

`continue` is the loop equivalent of a guard clause: bail out of this
iteration early, instead of wrapping the rest of the body in a big `if`.

## 8. The often-missed `else` on loops

Both `for` and `while` accept an `else` clause that runs **only if the
loop completed normally** (i.e. without hitting `break`):

```python
target = 7
numbers = [1, 3, 5, 9, 11]

for n in numbers:
    if n == target:
        print(f"Found {target}.")
        break
else:
    print(f"{target} not in list.")
```

If the `break` fires, the `else` is skipped. If the loop finishes
naturally — runs out of items, or the `while` condition becomes false —
the `else` runs. This is a tidy way to write search loops without an
extra flag variable.

It surprises almost everyone the first time they see it, so it is worth
calling out. Reference:
<https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops>.

## 9. Iterating over strings

A string is an iterable of single-character strings:

```python
word = "hello"

for char in word:
    print(char.upper())
# H, E, L, L, O
```

You can also iterate with indices via `enumerate`:

```python
for i, char in enumerate(word):
    print(i, char)
```

Strings are *immutable* (Week 2), so the loop cannot change the original
string. To build a new string, append to a list and `"".join(...)` at
the end (we cover this in the next lecture).

## 10. Iterating over lists (and changing them safely)

```python
numbers = [10, 20, 30, 40]

for n in numbers:
    print(n * 2)
```

A common gotcha: **do not modify a list while iterating over it**. For
example, removing items mid-loop skips elements:

```python
numbers = [1, 2, 3, 4]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)   # bug: skips elements
print(numbers)
```

Build a new list instead, or iterate over a copy with `numbers[:]`. We
will see list comprehensions in Week 5 that make this safer and shorter.

## 11. Nested loops

A loop inside a loop is called a **nested loop**. The inner loop runs
*completely* for every iteration of the outer loop:

```python
for row in range(1, 4):
    for col in range(1, 4):
        print(f"({row},{col})", end=" ")
    print()  # newline at the end of each row
```

```text
(1,1) (1,2) (1,3)
(2,1) (2,2) (2,3)
(3,1) (3,2) (3,3)
```

Nested loops are how you process two-dimensional data (grids, matrices,
tables), produce coordinate pairs, or compare every element to every
other element.

**Performance warning**: if the outer loop runs `n` times and the inner
loop runs `m` times, the inner body runs `n * m` times. Two nested loops
over a list of 10,000 items perform 100,000,000 operations — that may be
slow. Keep an eye on it.

`break` and `continue` only affect the *innermost* loop. To break out of
multiple loops, the cleanest pattern is to put the loops inside a
function and `return`.

## 12. `pass`: do nothing on purpose

Sometimes you need an indented block but have nothing to put in it yet
(maybe you are sketching the structure). `pass` is a placeholder
statement that does nothing:

```python
for n in range(5):
    pass  # TODO: fill this in later
```

`pass` is rarely needed in finished code, but it is handy while
prototyping.

## 13. Worked example: count vowels in a string

Putting it together:

```python
text = input("Enter a sentence: ")
vowels = "aeiouAEIOU"
count = 0

for char in text:
    if char in vowels:
        count += 1

print(f"{text!r} contains {count} vowels.")
```

The `in` operator checks membership: `char in vowels` is `True` if `char`
appears anywhere in the string `vowels`. We will use the same `in` with
lists, tuples, and sets in the coming weeks.

## 14. Recap

- `while` loops run as long as a condition is true; always update the
  controlling variable, or you will loop forever.
- `for` loops walk over the items of any iterable.
- `range(start, stop, step)` is the standard way to count in a `for`
  loop; `stop` is excluded.
- Use `enumerate()` for index + value and `zip()` for parallel iteration
  — never `range(len(...))`.
- `break` leaves a loop, `continue` jumps to the next iteration.
- The `else` clause on a loop runs only if the loop was not broken out
  of. Great for searches.
- Nested loops run inner-completely-per-outer; remember `break` only
  exits the innermost.
- Don't modify a list while iterating over it.

In the next lecture we will look at the *patterns* you will reach for
over and over inside loop bodies: counting, accumulating, max/min,
filtering, and searching.
