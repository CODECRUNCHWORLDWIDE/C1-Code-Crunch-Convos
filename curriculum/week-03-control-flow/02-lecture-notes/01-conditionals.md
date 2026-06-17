# Lecture 1 — Conditionals: Deciding What Runs

So far, every script you have written has executed line by line, from top
to bottom, every single time. That is fine for "Hello, world", but real
programs need to *make decisions*: log the user in only if the password
matches, charge a discounted price only for members, send an email only if
the recipient address is valid. The grammar Python gives us for these
decisions is the **conditional statement** built from three keywords: `if`,
`elif`, and `else`. By the end of this lecture you will be fluent in those
three, understand exactly which Python values count as "true" and which as
"false", be comfortable with chained comparisons and the ternary
expression, and know how to flatten messy nested `if` blocks using
**guard clauses**.

## 1. The `if` statement

The simplest conditional is just an `if` and an indented block underneath
it:

```python
age = 18

if age >= 18:
    print("You can vote in most countries.")
```

Three things to notice:

1. The line starts with the keyword `if`, followed by an expression that
   evaluates to either `True` or `False` (here, `age >= 18`).
2. The line ends with a **colon** (`:`). Forgetting the colon is the
   single most common typo for beginners — Python will raise a
   `SyntaxError`.
3. The body of the `if` is **indented** by four spaces (per PEP 8 — see
   <https://peps.python.org/pep-0008/#indentation>). Every line at that
   indentation level belongs to the `if`. The block ends when the
   indentation goes back to where the `if` was.

If the expression is `True`, Python runs the indented block. If it is
`False`, Python silently skips it. There is no warning, no error — the
block simply does not run.

## 2. Adding `else`

`else` says "...otherwise, do this":

```python
age = 15

if age >= 18:
    print("You can vote in most countries.")
else:
    print("You cannot vote yet.")
```

Exactly one of the two branches runs, never both. `else` has no condition
of its own — it is the catch-all for "the `if` was false".

## 3. Chaining with `elif`

`elif` is short for "else if". Use it when you have more than two cases:

```python
score = 76

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(grade)
```

Python checks the conditions **in order, top to bottom**, and stops at the
first one that is `True`. The order matters: if you wrote `score >= 60`
first, *every* passing score would be tagged "D". A good rule of thumb is
to test from the most specific (or highest threshold) to the most general.

You can have as many `elif` branches as you like. The final `else` is
optional, but it is good practice to include it whenever the cases are
supposed to cover every possibility — it forces you to think about the
"none of the above" case.

## 4. Truthiness: not just `True` and `False`

Here is something that surprises learners coming from other languages:
**any** Python value can be used directly inside an `if` condition. Python
will silently ask "is this value *truthy*?" and treat it as `True` or
`False`.

The following built-in values are **falsy** — they behave like `False`
when used in a condition:

- The boolean `False` itself
- The number `0` (and `0.0`, `0j`)
- The empty string `""`
- The empty list `[]`, tuple `()`, set `set()`, and dict `{}`
- The special value `None`

Everything else is **truthy**. Yes, that includes the string `"False"`
(which is non-empty), the list `[0]` (which has one element, even if that
element is itself falsy), and the float `-1.5`.

The full official rule is at
<https://docs.python.org/3/library/stdtypes.html#truth-value-testing>.

This lets us write very natural-looking checks:

```python
shopping_cart = []

if shopping_cart:
    print(f"You have {len(shopping_cart)} items.")
else:
    print("Your cart is empty.")
```

Compare that to the wordier (but equivalent) `if len(shopping_cart) > 0:`.
Pythonic code leans on truthiness when the meaning is obvious.

A common pitfall: **`None` is not the same as `False`, and neither is the
same as `0`**, even though all three are falsy. Use `is None` to check
specifically for `None`:

```python
result = None

if result is None:
    print("No result yet.")
```

Use `==` to compare values; use `is` only for the singletons `None`,
`True`, and `False`.

## 5. Comparison operators (quick review)

You met these in Week 2 — here they are again as a reference card:

| Operator | Meaning                  | Example         |
|----------|--------------------------|-----------------|
| `==`     | equal to                 | `x == 10`       |
| `!=`     | not equal to             | `x != 10`       |
| `<`      | less than                | `x < 10`        |
| `<=`     | less than or equal       | `x <= 10`       |
| `>`      | greater than             | `x > 10`        |
| `>=`     | greater than or equal    | `x >= 10`       |

Each returns a `bool` (`True` or `False`). You can store the result:

```python
is_adult = age >= 18
print(is_adult)  # True or False
```

## 6. Logical operators: `and`, `or`, `not`

Combine multiple conditions with `and`, `or`, and `not`:

```python
age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("Welcome in.")

if age < 18 or not has_ticket:
    print("Sorry, you cannot enter.")
```

Two important facts:

1. `and` and `or` **short-circuit**: Python evaluates left to right and
   stops as soon as the answer is known. In `False and expensive_call()`,
   `expensive_call()` is never invoked.
2. `and` / `or` return the *last value they evaluated*, not necessarily
   `True` or `False`. For instance, `"" or "fallback"` evaluates to
   `"fallback"`. This is occasionally useful, but it surprises people, so
   prefer explicit booleans in conditions until you have a reason to use
   the trick.

## 7. Chained comparisons

Python lets you chain comparisons in a way that reads like math:

```python
x = 7

if 0 < x < 10:
    print("x is a single positive digit.")
```

`0 < x < 10` is exactly equivalent to `0 < x and x < 10`, and `x` is only
evaluated once. You can chain more than two: `a <= b < c <= d` works and
reads naturally. Use this when the relationship really is a range — it is
clearer than the equivalent `and` expression.

## 8. Conditional expressions (the "ternary")

Sometimes you want a single value that depends on a condition. You *could*
write:

```python
if score >= 60:
    status = "pass"
else:
    status = "fail"
```

…but for a one-liner you can use a **conditional expression**:

```python
status = "pass" if score >= 60 else "fail"
```

Read it left-to-right: "set `status` to `'pass'` if the score is at least
60, else `'fail'`". The form is:

```python
value_if_true if condition else value_if_false
```

Use it when the alternatives are short and the meaning is obvious. If the
expression starts to wrap onto multiple lines, fall back to a regular
`if`/`else` — clarity beats cleverness.

## 9. Guard clauses and early returns

Deeply nested `if` statements are hard to read:

```python
def can_drive(person):
    if person is not None:
        if person.has_license:
            if person.age >= 16:
                if not person.is_banned:
                    return True
    return False
```

The same logic flattens nicely with **guard clauses** — short `if`
statements that bail out early when something is wrong:

```python
def can_drive(person):
    if person is None:
        return False
    if not person.has_license:
        return False
    if person.age < 16:
        return False
    if person.is_banned:
        return False
    return True
```

The reader of the second version sees the rules up front and only has to
keep one level of indentation in their head. This pattern is called
**early return** or **guard clause**, and you should reach for it whenever
your `if`s start nesting more than two levels deep.

Even outside functions, the equivalent inside a loop is `continue` (skip
to the next iteration) — we will see this in the next lecture.

## 10. Common bugs to avoid

- **`=` vs `==`**: a single `=` is assignment, a double `==` is
  comparison. `if x = 5:` is a `SyntaxError` in Python (which is good — in
  some other languages it silently sets `x` to `5` and is always truthy).
- **Missing colon**: `if x > 0` without the colon gives `SyntaxError:
  expected ':'`.
- **Inconsistent indentation**: mixing tabs and spaces inside the same
  block raises `IndentationError: unindent does not match any outer
  indentation level`. Configure your editor to insert four spaces when you
  press Tab.
- **Comparing floats with `==`**: floating-point arithmetic is
  approximate, so `0.1 + 0.2 == 0.3` is `False`. For floats, compare with
  `math.isclose(...)`.
- **Assuming `None` is `False`**: `None == False` is `False`. Use
  `if value is None:` or `if not value:` (the latter only if any falsy
  value should trigger the branch).
- **Forgetting that `or` returns a value, not always a bool**: `x = a or
  b` sets `x` to `a` if `a` is truthy, otherwise to `b`. Useful, but
  don't be surprised.

## 11. A worked example

Let's tie it all together with a tiny tax calculator. (Numbers are
made-up; this is a teaching example.)

```python
income = float(input("Enter your annual income: "))
is_student = input("Are you a student? (y/n) ").strip().lower() == "y"

if income < 0:
    print("Income cannot be negative.")
elif income == 0:
    tax = 0.0
elif income < 10_000:
    tax = income * 0.05
elif 10_000 <= income < 50_000:
    tax = income * 0.15
else:
    tax = income * 0.25

# Students get a flat 10% discount on positive taxes.
if income >= 0:
    if is_student and tax > 0:
        tax *= 0.90
    print(f"Estimated tax: {tax:,.2f}")
```

Notice the guard-style check for negative income at the top, the
`elif` chain ordered from smallest to largest threshold, the chained
comparison `10_000 <= income < 50_000`, and the truthy boolean
`is_student` used directly in the `if`. That is a lot of this lecture's
ideas in one short program.

## 12. Recap

- `if`, `elif`, `else` let your program branch based on conditions.
- The body of each branch is indented (four spaces, no tabs).
- Any value can be used in a condition; falsy values are `False`, `0`,
  `0.0`, `""`, `[]`, `()`, `{}`, `set()`, and `None`.
- Combine conditions with `and`, `or`, `not`. They short-circuit.
- Chained comparisons (`0 < x < 10`) read like math and are equivalent to
  two ANDed conditions.
- Use the ternary `a if cond else b` for short value-choosing expressions.
- Flatten nested `if`s with guard clauses and early returns.
- Watch out for `=` vs `==`, float equality, and the `None` / `False` /
  `0` distinction.

Next up: loops. Conditionals decide *whether* to do something. Loops
decide *how many times* to do something.
