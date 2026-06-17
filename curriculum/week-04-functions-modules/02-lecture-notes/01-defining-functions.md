# Lecture Note 1 — Defining Functions

> Estimated reading time: 40 minutes. Have a Python REPL open while you read.

## 1. What is a function, really?

A function is a **named, reusable block of code** that takes inputs and (optionally) produces an output. You have already used functions all week: `print`, `len`, `int`, `input`. Now you will write your own.

Three reasons functions matter:

1. **Reuse.** Write the logic once, call it many times.
2. **Naming.** A good function name is documentation. `calculate_tax(income)` is clearer than seven lines of arithmetic inline.
3. **Isolation.** Inside a function, you can think locally. Bugs stay small.

Python's official tutorial covers all of this in [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions). Read it alongside these notes.

---

## 2. The `def` statement

The simplest function looks like this:

```python
def greet() -> None:
    """Print a friendly greeting."""
    print("Hello, world!")
```

Then we **call** it:

```python
greet()  # prints: Hello, world!
```

Five things to notice:

1. `def` is a keyword. It tells Python "a function definition starts here".
2. `greet` is the function's name. Use `snake_case` per [PEP 8](https://peps.python.org/pep-0008/).
3. The parentheses `()` hold the parameter list. Empty here.
4. `-> None` is a **return type hint**: it says "this function does not return a useful value".
5. The triple-quoted string is a **docstring**. We will explore that more in section 8.

A function definition does **not** run the function. It just remembers the body. The body runs only when you call it.

---

## 3. Parameters and arguments

A **parameter** is a name in the function definition. An **argument** is the value you pass at the call site.

```python
def greet(name: str) -> None:
    """Greet `name` by name."""
    print(f"Hello, {name}!")


greet("Amina")   # "Amina" is the argument; `name` is the parameter
greet("Diego")
```

The distinction matters when you read documentation:

> "The parameter `name` must be a non-empty string."

translates as

> "Whatever you pass as the first argument has to be a non-empty string."

You can have many parameters. They are matched **by position** at the call site:

```python
def rectangle_area(width: float, height: float) -> float:
    """Return the area of a rectangle."""
    return width * height


print(rectangle_area(3.0, 5.0))   # 15.0
```

If you swap `3.0` and `5.0`, you get the same answer because multiplication is commutative — but the bug would still be there if the function were `subtract`. Order matters.

---

## 4. Returning values

`return` ends the function and hands a value back to the caller:

```python
def square(n: int) -> int:
    """Return `n` squared."""
    return n * n


result = square(7)   # result is 49
```

A function that has no `return` statement (or has a bare `return`) returns the special value `None`:

```python
def shout(text: str) -> None:
    """Print `text` in uppercase. Returns nothing."""
    print(text.upper())


value = shout("hi")  # value is None; "HI" was printed
```

A `return` with no expression is the same as `return None`. It is mostly used to bail out early:

```python
def divide(numerator: float, denominator: float) -> float | None:
    """Return numerator / denominator, or None if denominator is 0."""
    if denominator == 0:
        return None
    return numerator / denominator
```

(`float | None` is the modern way to say "either a float or None". It works on Python 3.10+. On older versions write `Optional[float]` from the `typing` module.)

### Side effects vs return values

This is one of the most important distinctions in programming.

- A **return value** is the answer your function hands back.
- A **side effect** is anything else the function does: print to the screen, write to a file, modify a list passed in, change a global variable, send a network request.

Compare:

```python
def total_with_tax(price: float, tax_rate: float) -> float:
    """Return price + tax. Pure: no side effects."""
    return price * (1 + tax_rate)


def total_with_tax_and_log(price: float, tax_rate: float) -> float:
    """Return price + tax. Also prints to the screen."""
    total = price * (1 + tax_rate)
    print(f"Computed total: {total}")   # side effect!
    return total
```

The first version is **pure**: same inputs, same outputs, no surprises. Pure functions are easier to test, easier to reason about, and easier to reuse in unexpected places. Aim for them when you can. Section 9 of Lecture Note 2 has more on this.

The second version is not wrong, but it makes assumptions: "the caller has a terminal", "the caller wants logging". Sometimes that is fine. Sometimes it makes the function useless inside a web server or a notebook.

Rule of thumb: **prefer returning values over printing them**. The caller can always print the return value if they want. They cannot un-print something your function already shouted.

---

## 5. Default parameter values

You can give a parameter a default value. If the caller omits it, the default is used:

```python
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting message."""
    return f"{greeting}, {name}!"


print(greet("Amina"))                  # Hello, Amina!
print(greet("Diego", "Hola"))          # Hola, Diego!
print(greet("Yuki", greeting="Konnichiwa"))  # Konnichiwa, Yuki!
```

Defaults must come **after** non-defaulted parameters. This is a syntax error:

```python
def bad(x: int = 0, y: int) -> int:   # SyntaxError
    return x + y
```

Defaults are evaluated **once**, when the `def` statement runs — not every time the function is called. For immutable defaults like `0`, `"Hello"`, `None`, `True`, this never matters. For **mutable** defaults like lists and dicts, it matters a lot.

### The mutable-default gotcha (read this carefully)

```python
def append_item(item: int, bucket: list[int] = []) -> list[int]:
    """Append `item` to `bucket` and return it. BUGGY."""
    bucket.append(item)
    return bucket


print(append_item(1))   # [1]
print(append_item(2))   # [1, 2]  -- surprise!
print(append_item(3))   # [1, 2, 3]  -- the SAME list keeps growing
```

What happened? Python created the empty list `[]` **once** when the `def` ran. Every call that does not pass `bucket` reuses that one shared list. This is one of the most famous beginner traps in the language. The Python docs warn about it explicitly in [Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values).

The fix: use `None` as the sentinel and create a fresh list inside the body.

```python
def append_item(item: int, bucket: list[int] | None = None) -> list[int]:
    """Append `item` to `bucket` (or to a new list) and return it."""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


print(append_item(1))   # [1]
print(append_item(2))   # [2]  -- correct
```

Remember this pattern. You will use it for the rest of your career:

```python
def f(arg: list[int] | None = None) -> None:
    if arg is None:
        arg = []
    ...
```

---

## 6. Positional and keyword arguments

Arguments come in two flavors at the call site:

- **Positional**: matched by position. `f(1, 2)`.
- **Keyword**: matched by name. `f(x=1, y=2)`.

You can mix them, but positional must come first:

```python
def book_room(room: str, nights: int, breakfast: bool = False) -> str:
    """Build a booking summary."""
    extras = " with breakfast" if breakfast else ""
    return f"Booked {room} for {nights} night(s){extras}."


# All positional:
print(book_room("Suite", 3, True))

# Mixed: position then keyword:
print(book_room("Suite", 3, breakfast=True))

# Keyword-only at the call site is fine:
print(book_room(nights=3, room="Suite", breakfast=True))

# This is a SyntaxError -- positional after keyword:
# print(book_room(room="Suite", 3, True))
```

Use keyword arguments to **document intent at the call site**. Compare:

```python
draw_circle(100, 200, 50, True, False)
```

vs.

```python
draw_circle(x=100, y=200, radius=50, filled=True, dashed=False)
```

The second version reads like English. A code reviewer can tell at a glance that `filled` is `True` and `dashed` is `False`. The first version forces them to go look up the function definition.

A useful heuristic: any boolean argument should usually be passed by name. `func(True)` tells you nothing; `func(verbose=True)` tells you everything.

### Positional-only and keyword-only parameters

Python 3.8+ supports `/` and `*` markers in the parameter list:

```python
def f(pos_only, /, normal, *, kw_only):
    """Demonstrates parameter kinds."""
    return pos_only, normal, kw_only


f(1, 2, kw_only=3)   # OK
# f(1, 2, 3)        # TypeError: kw_only is keyword-only
# f(pos_only=1, ...) # TypeError: pos_only is positional-only
```

You will not need this often as a beginner, but you will see it in library code. The Python docs cover it in [Special parameters](https://docs.python.org/3/tutorial/controlflow.html#special-parameters).

---

## 7. Type hints

Python is a dynamically typed language: you do not have to annotate types. But you **should**, because hints:

- Document the function for human readers.
- Let your editor catch mistakes before you run the code.
- Let tools like `mypy` check your whole codebase for type errors.

Basic syntax (see [PEP 484](https://peps.python.org/pep-0484/)):

```python
def add(a: int, b: int) -> int:
    """Return a + b."""
    return a + b


def first_name(full_name: str) -> str:
    """Return the substring before the first space."""
    return full_name.split(" ", 1)[0]


def average(values: list[float]) -> float:
    """Return the mean of `values`."""
    return sum(values) / len(values)
```

Built-in generic syntax (`list[float]`, `dict[str, int]`, `tuple[int, int]`) works on Python 3.9+. On older Pythons you must import from `typing`: `List[float]`, `Dict[str, int]`.

A type hint is just a hint. Python will not stop you from passing a `str` where you said `int`. Use a static checker if you want enforcement.

---

## 8. Docstrings (PEP 257)

A **docstring** is a string literal that is the first statement in a function body. Python stores it as `function.__doc__` and `help(function)` will print it.

```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit.

    Example:
        >>> celsius_to_fahrenheit(0)
        32.0
    """
    return celsius * 9 / 5 + 32
```

[PEP 257](https://peps.python.org/pep-0257/) describes the conventions. The short version:

- Every public function gets a docstring.
- Use triple double-quotes, not triple single-quotes.
- The first line is a short summary in imperative mood ("Return the area" not "Returns the area").
- Leave a blank line, then add details.

Common docstring styles:

- **Google style** (used in the example above): readable, popular.
- **NumPy style**: heading bars, used in scientific Python.
- **reST / Sphinx style**: machine-friendly, common in pip packages.

Pick one style per project. We use Google style in Code Crunch Convos.

---

## 9. Ordering rules: a quick reference

The parameter list goes in this order:

1. Positional-or-keyword parameters with no default.
2. Positional-or-keyword parameters with a default.
3. `*args` (we will cover in Lecture Note 2).
4. Keyword-only parameters (after `*` or `*args`).
5. `**kwargs`.

You will rarely use all five at once. The most common pattern is "required positional, then optional with default":

```python
def fetch(url: str, *, timeout: float = 5.0, retries: int = 3) -> str:
    """Fetch `url` and return the response body."""
    ...
```

Here `timeout` and `retries` are keyword-only because the bare `*` separator forces it. That makes the call site much more readable: `fetch("https://...", timeout=10.0)`.

---

## 10. Putting it all together

Here is a complete, runnable example that uses everything from this lecture:

```python
"""A tiny module of geometry helpers."""

from math import pi


def area_of_circle(radius: float) -> float:
    """Return the area of a circle with the given radius.

    Args:
        radius: A non-negative radius.

    Returns:
        The area of the circle.

    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError("radius must be non-negative")
    return pi * radius * radius


def area_of_rectangle(width: float, height: float = 1.0) -> float:
    """Return the area of a rectangle. Height defaults to 1.0."""
    return width * height


if __name__ == "__main__":
    print(f"Circle radius 3 -> area {area_of_circle(3):.2f}")
    print(f"Rectangle 4 x 5 -> area {area_of_rectangle(4, 5)}")
    print(f"Strip width 10 (h=1) -> area {area_of_rectangle(10)}")
```

Save this file as `geometry.py` and run it: `python geometry.py`. You should see three lines of output.

---

## 11. Checklist before you move on

- [ ] You can write a function with `def`, parameters, type hints, and a docstring.
- [ ] You can explain the difference between a parameter and an argument.
- [ ] You can explain the mutable-default trap and write the `None` sentinel fix.
- [ ] You can call a function with both positional and keyword arguments.
- [ ] You know the difference between a return value and a side effect.
- [ ] You can run `help(your_function)` and see your docstring.

If any of those are shaky, open the [Python tutorial on defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) and read it once more, then attempt **Exercise 01**.

Next up: [Lecture Note 2 — `*args`, `**kwargs`, and scope](./02-args-kwargs-and-scope.md).
