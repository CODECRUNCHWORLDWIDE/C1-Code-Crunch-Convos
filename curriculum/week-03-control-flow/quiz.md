# Week 3 — Quiz

Ten multiple-choice questions covering this week's material. Answer
each one in your head before opening the fold beneath it. Aim for
**8 / 10 or better** before moving on. Re-read the matching lecture for
anything you miss.

---

## 1. Which of these values is **truthy**?

A. `0`
B. `[]`
C. `"False"`
D. `None`

<details>
<summary>Answer</summary>

**C** — `"False"` is a non-empty string, therefore truthy. `0`, `[]`,
and `None` are all falsy.

</details>

---

## 2. What does this code print?

```python
x = 5
if x > 0:
    print("positive")
elif x > 3:
    print("big")
else:
    print("small")
```

A. `positive`
B. `big`
C. `positive` then `big`
D. `small`

<details>
<summary>Answer</summary>

**A** — The first matching branch wins. Even though `x > 3` is also
true, the `elif` is never checked because `x > 0` matched first.

</details>

---

## 3. Which loop construct best fits "repeat until the user types
`quit`"?

A. `for _ in range(100):`
B. `while count < quit:`
C. `while True:` paired with `break`
D. `for line in quit:`

<details>
<summary>Answer</summary>

**C** — `while True:` with a `break` is the idiomatic pattern for
"until the user says quit".

</details>

---

## 4. What does `range(2, 10, 3)` produce?

A. `2, 3, 4, 5, 6, 7, 8, 9`
B. `2, 5, 8`
C. `2, 5, 8, 10`
D. `3, 6, 9`

<details>
<summary>Answer</summary>

**B** — `range(start, stop, step)` excludes `stop`. So it yields
`2, 5, 8` and stops before reaching `11`.

</details>

---

## 5. Which of these is the **idiomatic** way to iterate over a list
with both the index and the value?

A. `for i in range(len(items)): item = items[i]`
B. `for index, item in enumerate(items):`
C. `for item in items: index = items.index(item)`
D. `while i < len(items): item = items[i]; i += 1`

<details>
<summary>Answer</summary>

**B** — `enumerate(items)` returns `(index, value)` pairs. Never
write `for i in range(len(items))` when `enumerate` exists.

</details>

---

## 6. What does the `else` clause on a `for` loop do?

A. It runs only when the loop body is empty.
B. It is a `SyntaxError` — `for` loops cannot have `else`.
C. It runs only if the loop completed without hitting `break`.
D. It runs every time the loop variable is `None`.

<details>
<summary>Answer</summary>

**C** — The `else` on a loop runs when the loop completes normally
(without `break`). It is the cleanest way to write "I searched and
did not find it".

</details>

---

## 7. What is the value of `result` after this snippet?

```python
result = "yes" if 0 else "no"
```

A. `"yes"`
B. `"no"`
C. `True`
D. A `SyntaxError`

<details>
<summary>Answer</summary>

**B** — `0` is falsy, so the conditional expression picks the `else`
branch: `"no"`.

</details>

---

## 8. Which line contains a bug (assume the intent is "if `x` equals
5")?

A. `if x == 5:`
B. `if 5 == x:`
C. `if x = 5:`
D. `if not (x != 5):`

<details>
<summary>Answer</summary>

**C** — `=` is assignment, `==` is comparison. In Python, `if x = 5:`
is a `SyntaxError` (which is the language helping you, not insulting
you).

</details>

---

## 9. What does this code print?

```python
for i in range(1, 4):
    for j in range(1, 4):
        if i == j:
            continue
        print(i, j)
```

A. Nine pairs of numbers including `1 1`, `2 2`, `3 3`.
B. Six pairs of numbers, none with `i == j`.
C. Three pairs: `1 1`, `2 2`, `3 3`.
D. Nothing — `continue` ends the loop.

<details>
<summary>Answer</summary>

**B** — `continue` skips the `i == j` cases, so the diagonal is
excluded. Six off-diagonal pairs print.

</details>

---

## 10. Which of the following correctly explains the performance hint
from Lecture 3 about building strings in a loop?

A. Strings are mutable, so appending is O(1).
B. Strings are immutable, so `result += "x"` allocates a new string
   each time, making the whole loop O(n²). Use a list and
   `"".join(...)` instead.
C. Lists are immutable, so `append` is slow; use string concatenation.
D. There is no difference — both are O(n).

<details>
<summary>Answer</summary>

**B** — Strings are immutable; repeated `+=` is O(n²). Collect into
    a list and join once.

---

</details>

---

## How did you do?

- **10 / 10** — Outstanding. Push on to homework and the mini-project.
- **8–9 / 10** — Good. Re-read the lecture for the ones you missed.
- **5–7 / 10** — Honest signal that you should reread the lectures and
  redo a couple of exercises before homework.
- **Below 5** — No shame. Skim the lectures, watch a Corey Schafer
  video from `resources.md`, and try the quiz again tomorrow.
