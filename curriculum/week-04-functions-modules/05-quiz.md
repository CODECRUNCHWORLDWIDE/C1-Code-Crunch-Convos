# Week 4 — Quiz

10 multiple-choice questions. Pick **one** answer per question. The answer key is at the bottom; do not peek until you have written down your answers.

Recommended time: 20 minutes. Open book is fine; the goal is to find out what you remember and what you need to revisit.

---

### Q1. Which keyword defines a function in Python?

A. `function`
B. `def`
C. `define`
D. `fn`

---

### Q2. What does this function return?

```python
def f(x: int) -> int | None:
    if x > 0:
        return x
```

A. The value of `x`.
B. Always `0`.
C. The value of `x` if positive, otherwise `None`.
D. `SyntaxError`.

---

### Q3. Read this code carefully. What does it print?

```python
def make_list(item, bucket=[]):
    bucket.append(item)
    return bucket


print(make_list(1))
print(make_list(2))
print(make_list(3))
```

A. `[1]` then `[2]` then `[3]`
B. `[1]` then `[1, 2]` then `[1, 2, 3]`
C. `[1, 2, 3]` three times
D. `TypeError: bucket cannot have a default value`

---

### Q4. Which call is valid for this function?

```python
def book(room: str, *, nights: int = 1) -> str:
    return f"{room} for {nights}"
```

A. `book("Suite", 3)`
B. `book("Suite", nights=3)`
C. `book(nights=3)`
D. `book(room=Suite, nights=3)`

---

### Q5. What does LEGB stand for?

A. Local, External, Global, Bound
B. Logical, Enclosing, Generic, Built-in
C. Local, Enclosing, Global, Built-in
D. List, Element, Generator, Bool

---

### Q6. What does this code print?

```python
x = 1


def f():
    print(x)
    x = 2


f()
```

A. `1`
B. `2`
C. `None`
D. `UnboundLocalError`

---

### Q7. Inside a function, `*args` is what type?

A. `list`
B. `tuple`
C. `dict`
D. `set`

---

### Q8. Which import statement is considered poor style by PEP 8?

A. `import math`
B. `from math import pi, sqrt`
C. `import numpy as np`
D. `from math import *`

---

### Q9. What does `if __name__ == "__main__":` do?

A. Renames the module to `"__main__"`.
B. Prevents the file from being run directly.
C. Runs the code in the block only when the file is run as a script, not when it is imported.
D. Marks the file as the program's entry point so Python will run it first.

---

### Q10. Which of these is the safest way to handle a default mutable argument?

A. `def f(items=[]): ...`
B. `def f(items={}): ...`
C. `def f(items=set()): ...`
D. `def f(items=None): items = [] if items is None else items; ...`

---

## Answer key

Resist the urge to peek until you have written your answers.

. . .

. . .

. . .

1. **B**. `def` is the keyword. `function` and `fn` are not Python; `define` is not a keyword.
2. **C**. When `x <= 0`, the function falls off the end with no explicit `return`, which means it returns `None`. The return type annotation is `int | None`.
3. **B**. The classic mutable-default trap. The default list `[]` is created **once** when the `def` runs and is shared across every call that does not pass `bucket`. See Lecture Note 1, section 5.
4. **B**. The `*` in the parameter list makes `nights` keyword-only. Option A fails because `3` would have to be passed by keyword. Option C fails because `room` has no default. Option D fails because `Suite` is not in quotes.
5. **C**. Local, Enclosing, Global, Built-in. Python searches these in order when resolving a name. See Lecture Note 2, section 5.
6. **D**. `UnboundLocalError`. Because `f` assigns to `x` somewhere, Python treats `x` as local **everywhere** in `f`, including the `print(x)` before the assignment. To make this work, add `global x` at the top of `f`.
7. **B**. `*args` collects extra positional arguments into a `tuple`. (Note: `**kwargs` would be a `dict`.)
8. **D**. `from math import *` is a wildcard import. It pulls every public name into your namespace, hides where each name came from, and risks shadowing built-ins. PEP 8 advises against it.
9. **C**. `__name__` is set to `"__main__"` when the file is run directly, and to the module name when it is imported. The idiom uses this to run script-only code only when running directly. See Lecture Note 3, section 6.
10. **D**. Use `None` as the sentinel and create the mutable default inside the function. Options A, B, and C all share state across calls.

## Scoring

- 9–10: Excellent. Move on with confidence.
- 7–8: Solid. Re-skim the question(s) you missed.
- 5–6: Good base. Re-read the relevant lecture note and retry.
- 0–4: Slow down. Re-read all three lecture notes and redo exercises 1, 2, and 4 from scratch.

Take note of the questions you missed and add them to a personal "weak spots" list. Revisit them before Week 5.
