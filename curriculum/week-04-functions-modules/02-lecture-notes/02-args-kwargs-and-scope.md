# Lecture Note 2 — `*args`, `**kwargs`, and Scope

> Estimated reading time: 40 minutes. Have a Python REPL open.

This lecture covers two themes that often confuse beginners: **variable-length argument lists** (`*args` and `**kwargs`) and **scope rules** (LEGB, `global`, `nonlocal`, closures). The two are connected because both are about how names get bound to values.

---

## 1. Why we need `*args` and `**kwargs`

Suppose you want a function that sums any number of numbers. With what you know so far you would have to pick a maximum:

```python
def add_three(a: int, b: int, c: int) -> int:
    return a + b + c
```

But what about four numbers? Five? Twelve? Hard-coding the count is brittle. Python gives you two operators to handle this:

- `*` in a parameter list collects extra **positional** arguments into a tuple.
- `**` in a parameter list collects extra **keyword** arguments into a dict.

The convention is to name them `args` and `kwargs`, but the names are arbitrary. The asterisks are what matter. The official docs explain this in [Arbitrary Argument Lists](https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists).

---

## 2. `*args` — variable positional arguments

```python
def add_all(*nums: int) -> int:
    """Return the sum of all positional integer arguments."""
    total = 0
    for n in nums:
        total += n
    return total


print(add_all())              # 0
print(add_all(1))             # 1
print(add_all(1, 2, 3))       # 6
print(add_all(1, 2, 3, 4, 5)) # 15
```

Inside `add_all`, the name `nums` is a `tuple`. You can iterate over it, index it, get its length — everything you can do with any tuple.

A common gotcha: if you pass a list and want it to be "spread", you have to **unpack** it with `*`:

```python
my_numbers = [10, 20, 30]
print(add_all(my_numbers))    # 60? No -- this is wrong.
                              # nums is now ([10, 20, 30],), a tuple of one list.

print(add_all(*my_numbers))   # 60 -- correct. The * unpacks the list.
```

The `*` in `add_all(*my_numbers)` is the **unpacking** operator. It is the mirror image of `*nums` in the definition. One asterisk in a definition packs; one asterisk at a call unpacks.

You can combine fixed and variadic parameters:

```python
def log(level: str, *messages: str) -> None:
    """Print each message prefixed with `level`."""
    for msg in messages:
        print(f"[{level}] {msg}")


log("INFO", "starting up", "loading config", "ready")
# [INFO] starting up
# [INFO] loading config
# [INFO] ready
```

Anything you write **after** `*args` becomes **keyword-only**:

```python
def book(*guests: str, room: str) -> str:
    """Return a booking summary."""
    return f"{', '.join(guests)} -> {room}"


print(book("Amina", "Diego", room="Suite"))
# print(book("Amina", "Diego", "Suite"))   # TypeError: missing 'room'
```

This is a great trick for forcing readability at call sites.

---

## 3. `**kwargs` — variable keyword arguments

```python
def make_user(**fields: object) -> dict[str, object]:
    """Build a user dict from keyword arguments."""
    return dict(fields)


u = make_user(name="Amina", age=29, country="Tunisia")
print(u)
# {'name': 'Amina', 'age': 29, 'country': 'Tunisia'}
```

Inside `make_user`, the name `fields` is a `dict`. The keys are the parameter names you passed at the call site; the values are the values.

The mirror unpacking operator at the call site is `**`:

```python
profile = {"name": "Diego", "age": 31}
u = make_user(**profile, country="Mexico")
print(u)
# {'name': 'Diego', 'age': 31, 'country': 'Mexico'}
```

`**profile` unpacks the dict so each key-value pair becomes a keyword argument. Useful when you have a config dict and want to pass it to a function.

You can combine `*args` and `**kwargs` in one function:

```python
def trace(func_name: str, *args: object, **kwargs: object) -> None:
    """Log a function call with all its arguments."""
    parts = [repr(a) for a in args]
    parts += [f"{k}={v!r}" for k, v in kwargs.items()]
    print(f"{func_name}({', '.join(parts)})")


trace("connect", "localhost", 5432, timeout=10, ssl=True)
# connect('localhost', 5432, timeout=10, ssl=True)
```

This pattern is how decorators forward arguments. You will write decorators later in the bootcamp; remember this shape.

---

## 4. Putting the parameter ordering rule together

Repeating from Lecture Note 1, the legal order is:

1. Positional-or-keyword parameters, no default.
2. Positional-or-keyword parameters, with default.
3. `*args` (or bare `*` to start keyword-only without args).
4. Keyword-only parameters.
5. `**kwargs`.

A function that uses every category:

```python
def big(
    required_pos: str,
    optional_pos: str = "x",
    *args: int,
    kw_only: bool = False,
    **kwargs: object,
) -> None:
    """Demonstrates every parameter category."""
    print(required_pos, optional_pos, args, kw_only, kwargs)


big("a", "b", 1, 2, 3, kw_only=True, extra="hi", other=42)
# a b (1, 2, 3) True {'extra': 'hi', 'other': 42}
```

You will rarely use all five at once. But when you read library code, you will see this shape often.

---

## 5. Scope: where do names live?

When you write `x` in Python, the interpreter has to figure out **which** `x` you mean. The same name can refer to different things in different places. The rule for resolving names is called **LEGB**.

LEGB stands for the four scopes Python searches, in order:

1. **L — Local**: the function you are currently inside.
2. **E — Enclosing**: any outer function(s), if you are nested.
3. **G — Global**: the top level of the current module (the file).
4. **B — Built-in**: names like `print`, `len`, `range` that Python ships with.

Python looks in L first. If `x` is not there, it looks in E. Then G. Then B. If none of them have `x`, you get a `NameError`.

### A diagram

```text
+---------------------------------------------------+
| B  (built-in: print, len, range, ...)             |
|  +---------------------------------------------+  |
|  | G  (global: module-level names)             |  |
|  |  +---------------------------------------+  |  |
|  |  | E  (enclosing function, if any)       |  |  |
|  |  |  +---------------------------------+  |  |  |
|  |  |  | L  (local: inside current func) |  |  |  |
|  |  |  +---------------------------------+  |  |  |
|  |  +---------------------------------------+  |  |
|  +---------------------------------------------+  |
+---------------------------------------------------+
```

Reads name `x`: Python searches L -> E -> G -> B. First hit wins.

### A worked example

```python
x = "global x"   # G


def outer() -> None:
    x = "outer x"   # E (from inner()'s point of view)

    def inner() -> None:
        x = "inner x"   # L
        print(x)        # "inner x"

    inner()
    print(x)            # "outer x"


outer()
print(x)                # "global x"
```

Three different `x` values exist at the same time, and each `print(x)` resolves to whichever `x` is **closest** to its enclosing function.

If we delete the `x = "inner x"` line, `inner` no longer has a local `x`. The lookup proceeds to E, finds `"outer x"`, and prints that.

### Reads vs. writes

Reads follow LEGB. **Writes always create a local name**, unless you say otherwise.

```python
counter = 0   # G


def bump() -> None:
    counter = counter + 1   # UnboundLocalError!


bump()
```

Why the error? Because Python sees `counter = ...` and decides "this function has a local `counter`". When it then evaluates the right-hand side, the local `counter` has not been assigned yet, so the read fails. This trips up almost every beginner.

There are two fixes:

1. **`global`** to mark the name as global.
2. Stop modifying globals. Pass the value in and return the new one.

---

## 6. `global` — explicit but unloved

```python
counter = 0


def bump() -> None:
    global counter
    counter = counter + 1


bump()
bump()
print(counter)   # 2
```

`global counter` tells Python "when I assign to `counter` in this function, modify the module-level variable". It works. It is also a code smell, because it makes the function depend on hidden state. The function's behavior changes based on something invisible to its callers.

A purer alternative:

```python
def bump(counter: int) -> int:
    """Return counter incremented by one."""
    return counter + 1


count = 0
count = bump(count)
count = bump(count)
print(count)   # 2
```

Now `bump` is **pure**: same input, same output, no hidden state. You can test it without setting up globals. You can call it ten times in parallel without races.

Use `global` only when you genuinely have a single piece of program-wide state and refactoring is not worth it. Even then, a class or a dataclass is usually cleaner.

---

## 7. `nonlocal` — for nested functions

`global` reaches all the way out to module scope. `nonlocal` reaches out to the **nearest enclosing function** scope:

```python
def make_counter() -> tuple:
    """Return (increment, get) closure-based counter."""
    count = 0

    def increment() -> None:
        nonlocal count
        count += 1

    def get() -> int:
        return count

    return increment, get


inc, get = make_counter()
inc()
inc()
inc()
print(get())   # 3
```

Without `nonlocal count`, the line `count += 1` would try to create a new local `count` inside `increment`, and we would get the same `UnboundLocalError` as before.

Like `global`, `nonlocal` is a tool of last resort. Most of the time you can rework the code to pass values explicitly. A class with one attribute would do the same job more clearly.

---

## 8. Closures (lightly)

The example above is a **closure**: the inner functions `increment` and `get` "close over" the `count` variable from the enclosing scope and keep it alive after `make_counter` has returned. Each call to `make_counter()` creates a **new** `count`, so each pair of `(inc, get)` is independent.

```python
inc_a, get_a = make_counter()
inc_b, get_b = make_counter()

inc_a()
inc_a()
inc_b()

print(get_a())   # 2
print(get_b())   # 1
```

Closures are how decorators are built. You do not need to master them this week, but you should recognize the shape: "function returns function, inner function uses outer variable".

---

## 9. Pure functions: a manifesto in five bullets

A function is **pure** if:

1. Its output depends only on its arguments. (No `global`, no I/O.)
2. It does not modify its arguments.
3. It does not mutate any external state.
4. Same inputs always produce the same output.
5. It has no side effects that the caller has to know about.

Pure functions are the easiest kind of code to:

- Read (you only need the signature to understand it).
- Test (no setup, no teardown).
- Reuse (no hidden dependencies).
- Run in parallel (no shared state).

You cannot make every function pure (programs have to do *something* eventually), but you can keep the **core logic** of your code pure and confine side effects to a thin shell around it. That is one of the most useful design heuristics in all of programming.

A loose example. The core is pure; the shell does the I/O:

```python
def parse_cents(value: str) -> int:
    """Pure: turn '$12.34' into 1234 cents."""
    cleaned = value.strip().lstrip("$")
    dollars, _, cents = cleaned.partition(".")
    return int(dollars) * 100 + int((cents + "00")[:2])


def main() -> None:
    """Impure: reads from input, prints to output."""
    raw = input("Enter a price: ")
    print(f"That is {parse_cents(raw)} cents.")
```

`parse_cents` is unit-testable. `main` is the bit that talks to the real world.

---

## 10. `lambda` expressions — briefly

A `lambda` is a tiny, anonymous function expression:

```python
square = lambda x: x * x
print(square(4))   # 16
```

That is exactly equivalent to:

```python
def square(x: int) -> int:
    return x * x
```

There is **almost never** a reason to assign a `lambda` to a name. If you want a function, use `def`. Lambdas earn their keep when you need a throwaway function as an argument to another function:

```python
people = [
    {"name": "Amina", "age": 29},
    {"name": "Diego", "age": 31},
    {"name": "Yuki", "age": 24},
]

people.sort(key=lambda p: p["age"])
print(people)
# Sorted by age ascending.
```

Without the lambda you would have to write a named helper just to extract `p["age"]`. The lambda is fine here. Rules of thumb:

- Lambdas should fit on one line.
- Lambdas cannot contain statements (no `if`/`for`/`return`).
- If you find yourself wanting a multiline lambda, write a `def` instead.

---

## 11. Quick LEGB drills

Predict the output before you run each snippet.

**Drill A**

```python
x = 1
def f():
    print(x)
f()
```

**Drill B**

```python
x = 1
def f():
    x = 2
    print(x)
f()
print(x)
```

**Drill C**

```python
x = 1
def f():
    print(x)
    x = 2   # ???
f()
```

**Drill D**

```python
def outer():
    x = "outer"
    def inner():
        print(x)
    inner()
outer()
```

Answers:

- A: `1` (reads global).
- B: `2` then `1` (local `x` shadows global; global is untouched).
- C: `UnboundLocalError`. Because `f` assigns to `x`, Python treats `x` as local everywhere in `f`, including the `print(x)` before the assignment.
- D: `outer`. `inner` reads `x` from its enclosing function scope.

If you got all four right, you understand LEGB well enough to move on.

---

## 12. Checklist before you move on

- [ ] You can write a function that uses `*args` and call it with both lists and bare values.
- [ ] You can write a function that uses `**kwargs` and unpack a dict at the call site.
- [ ] You can name the four scopes in LEGB order without looking.
- [ ] You can explain why `global` is usually a code smell.
- [ ] You can predict whether a snippet will raise `UnboundLocalError`.
- [ ] You can describe what a pure function is and why we prefer them.

Next up: [Lecture Note 3 — Modules and imports](./03-modules-and-imports.md).
