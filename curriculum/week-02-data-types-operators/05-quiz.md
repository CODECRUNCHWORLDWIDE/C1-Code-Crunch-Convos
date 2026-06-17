# Week 2 — Quiz

Ten multiple-choice questions covering this week's material. Answer
honestly without running code first; *then* try each in the REPL to
confirm. Use the collapsed answer key at the bottom only after you've
written down your own answers.

---

### Question 1

What is the value of `type(3.0)` in Python?

- A. `<class 'int'>`
- B. `<class 'float'>`
- C. `<class 'double'>`
- D. `<class 'number'>`

---

### Question 2

Which of the following is **not** a valid variable name in Python?

- A. `_total`
- B. `total_2`
- C. `2_total`
- D. `TOTAL`

---

### Question 3

What does `10 // 3` evaluate to?

- A. `3.333...`
- B. `3`
- C. `4`
- D. `1`

---

### Question 4

Which expression below is **falsy** in Python?

- A. `"False"`
- B. `[0]`
- C. `" "`
- D. `0.0`

---

### Question 5

What is printed by this snippet?

```python
x = 5
y = "5"
print(x == y)
```

- A. `True`
- B. `False`
- C. `5`
- D. It raises `TypeError`.

---

### Question 6

What does `"abcdef"[1:4]` evaluate to?

- A. `"abc"`
- B. `"bcd"`
- C. `"bcde"`
- D. `"cd"`

---

### Question 7

Which f-string format spec right-aligns a number in a width-8 field
with two decimals?

- A. `f"{x:.2f>8}"`
- B. `f"{x:>8.2f}"`
- C. `f"{x:8>.2f}"`
- D. `f"{x:.2>8f}"`

---

### Question 8

What is the result of `input("Age: ")` when the user types `25`?

- A. The integer `25`.
- B. The float `25.0`.
- C. The string `"25"`.
- D. A `ValueError`.

---

### Question 9

What does this code print?

```python
a = True
b = False
print(a and not b)
```

- A. `True`
- B. `False`
- C. `None`
- D. It raises a `SyntaxError`.

---

### Question 10

Which of the following best describes Python type hints, such as
`def f(x: int) -> int`?

- A. They are enforced by the Python interpreter at runtime.
- B. They are checked by tools like `mypy` but ignored by the
  interpreter at runtime.
- C. They prevent the function from being called with the wrong type.
- D. They are compiled into faster machine code.

---

## Answer Key

<details>
<summary>Click to reveal answers</summary>

1. **B** — `<class 'float'>`. Any literal with a decimal point is a
   `float`, even when the fractional part is zero.
2. **C** — `2_total`. Names cannot start with a digit. (`_total`,
   `total_2`, and `TOTAL` are all valid.)
3. **B** — `3`. `//` is floor division: it returns the integer part of
   the quotient when both operands are integers.
4. **D** — `0.0`. The other three are truthy: `"False"` is a non-empty
   string, `[0]` is a list with one element, and `" "` is a non-empty
   string (it contains a space).
5. **B** — `False`. Python does not consider an `int` and a `str` equal
   even if they look "the same." Use `int(y)` or `str(x)` to compare.
6. **B** — `"bcd"`. Slicing is `[start:stop]` where `start` is included
   and `stop` is excluded. Indices 1, 2, 3 give `b`, `c`, `d`.
7. **B** — `f"{x:>8.2f}"`. The grammar is
   `[fill]align width [,] .precision type`. Width comes before
   precision.
8. **C** — The string `"25"`. `input()` always returns a string. Cast
   it with `int()` or `float()` if you need a number.
9. **A** — `True`. `not b` is `True`; `True and True` is `True`.
10. **B** — Type hints are advisory. Tools like `mypy` use them for
    static analysis, but the Python interpreter ignores them at runtime
    (with rare exceptions like `dataclasses`).

</details>

## Scoring

- **9–10 correct**: You've nailed this week. Move on with confidence.
- **6–8 correct**: Solid. Re-read the lecture sections that map to the
  questions you missed.
- **0–5 correct**: Spend another day on the lectures and exercises
  before pushing into the mini-project. There's no rush.
