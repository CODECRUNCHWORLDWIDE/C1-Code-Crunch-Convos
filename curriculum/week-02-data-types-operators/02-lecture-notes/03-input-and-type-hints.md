# Lecture 03 — Reading Input and Type Hints

So far your programs have used hard-coded values. That's fine for
learning, but real programs talk to humans (and other programs). This
lecture covers two complementary topics: how to **read input** from the
command line with `input()`, and how to **document your intent** with type
hints so that your code is self-explanatory and machine-checkable.

## 1. The `input()` Built-in

`input()` pauses your program, waits for the user to type a line and press
Enter, and returns whatever they typed as a **string**.

```python
name = input("What's your name? ")
print(f"Hello, {name}!")
```

Run that script and you'll see:

```text
What's your name? Ada
Hello, Ada!
```

The argument to `input()` is the **prompt** — the text shown to the user.
Conventionally it ends with a space so the cursor doesn't bump into the
question.

## 2. The Number One Beginner Bug

`input()` *always* returns a string. Always. Even if the user types `5`.

```python
n = input("Pick a number: ")
print(n + 1)
# TypeError: can only concatenate str (not "int") to str
```

The fix is to **cast** the input to the type you need:

```python
n = int(input("Pick a number: "))
print(n + 1)   # works!
```

Internalize this: any time you read a number from `input()`, wrap the call
in `int()` or `float()`.

```python
age = int(input("Age? "))
height_m = float(input("Height in meters? "))
```

## 3. Handling Bad Input

What if the user types `"banana"` when you asked for a number?

```python
n = int(input("Pick a number: "))
# Input: banana
# ValueError: invalid literal for int() with base 10: 'banana'
```

The program crashes with a `ValueError`. We'll cover exception handling
properly in Week 6, but for now you can already use the basic shape:

```python
raw = input("Pick a number: ")
try:
    n = int(raw)
    print(f"Doubled: {n * 2}")
except ValueError:
    print(f"Sorry, {raw!r} is not a whole number.")
```

The `!r` inside the f-string calls `repr()` on the value, which quotes
strings — useful for error messages so the user can see if they typed an
extra space.

## 4. Reading Multiple Values

A common pattern is to read several space-separated numbers from one
line:

```python
line = input("Enter two numbers separated by a space: ")
parts = line.split()           # ['10', '20']
a = int(parts[0])
b = int(parts[1])
print(a + b)                   # 30
```

Or, more idiomatically with tuple unpacking (you'll see this everywhere):

```python
a_str, b_str = input("Two numbers: ").split()
a = int(a_str)
b = int(b_str)
```

If the user types the wrong number of values, the unpacking raises
`ValueError: not enough values to unpack` or `too many values to unpack`.

## 5. Why `input()` is Slow

`input()` blocks the program until the user presses Enter. For
interactive scripts this is fine. For automation or scripts that need to
process a lot of data, you'll later learn to:

- Read from `sys.stdin` (faster, can pipe).
- Read from command-line arguments via `sys.argv` or `argparse`.
- Read from files.

For Week 2 we'll stick with `input()`.

## 6. Type Hints — A First Look

Recall that Python is dynamically typed: the type lives on the *value*,
not the *name*. That makes Python fast to write but also makes it harder
to remember, six months later, what kind of value a function expects.

**Type hints** (sometimes called *type annotations*) let you write down
the type you intend. They are **not enforced at runtime** by the
interpreter — Python ignores them for execution. They exist for
*readers*: humans, IDEs, and type checkers like `mypy`.

### 6.1 Variable annotations

The syntax is `name: Type = value`:

```python
age: int = 30
pi: float = 3.14159
name: str = "Ada"
is_active: bool = True
result: None = None
```

You can also annotate without an initial value (rare for locals, common
for class attributes which we'll see in Week 7):

```python
total: float  # declared but not yet assigned
```

### 6.2 Function annotations

You can annotate every parameter and the return type:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9

def log(message: str) -> None:
    print(f"[LOG] {message}")
```

`-> None` means "this function doesn't return a useful value." Functions
that don't have a `return` statement implicitly return `None`.

### 6.3 The hints are advisory

Python does not stop you from passing the wrong type:

```python
def add(a: int, b: int) -> int:
    return a + b

print(add("hello", "world"))  # 'helloworld' — runs without error!
```

The hints say "I intended this to take two ints." A type checker would
flag the bad call; the interpreter does not.

### 6.4 Common hint shapes

A small starter set:

```python
def names_of(count: int) -> list[str]: ...
def lookup(key: str) -> dict[str, int]: ...
def first_or_none(items: list[int]) -> int | None: ...
```

The `int | None` syntax (Python 3.10+) means "either an int or None." In
older Python you'd write `Optional[int]` after importing it from `typing`.

We'll use type hints throughout this bootcamp from Week 2 onward. They
make every function feel like documentation.

## 7. Brief `mypy` Demo

`mypy` is the most popular static type checker for Python. It reads your
source files, looks at the type hints, and tells you about mismatches —
*without running your code*.

### 7.1 Installing

Inside your Week 2 virtual environment:

```bash
pip install mypy
```

### 7.2 A file with a type error

Save the following as `bad_types.py`:

```python
def add(a: int, b: int) -> int:
    return a + b

result = add("hello", "world")
print(result)
```

Now run:

```bash
mypy bad_types.py
```

You'll get something like:

```text
bad_types.py:4: error: Argument 1 to "add" has incompatible type "str";
expected "int"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

`mypy` found the bug without ever executing the code. That's the
superpower: type errors at *write* time, not at *run* time.

### 7.3 A clean file

```python
def add(a: int, b: int) -> int:
    return a + b

result: int = add(2, 3)
print(result)  # 5
```

```bash
$ mypy good_types.py
Success: no issues found in 1 source file
```

### 7.4 When to use mypy

Don't worry about running `mypy` after every single change in Week 2.
Just install it once, run it on each exercise when you finish, and try to
get a clean report. The habit pays off as your programs get bigger.

## 8. Putting It All Together

A small, fully-annotated program that reads two numbers, validates them,
and prints their average:

```python
"""Read two numbers from the user and print the average."""


def average(a: float, b: float) -> float:
    """Return the arithmetic mean of two numbers."""
    return (a + b) / 2


def read_float(prompt: str) -> float:
    """Prompt until the user enters a valid float."""
    while True:
        raw: str = input(prompt)
        try:
            return float(raw)
        except ValueError:
            print(f"  {raw!r} isn't a number. Try again.")


def main() -> None:
    x: float = read_float("First number: ")
    y: float = read_float("Second number: ")
    print(f"Average: {average(x, y):.2f}")


if __name__ == "__main__":
    main()
```

This single script demonstrates:

- A function with parameter and return type hints.
- A docstring on every function (PEP 257 — read it later).
- Defensive `input()` with `try/except`.
- A `while True` loop for "ask again until it's valid."
- The `if __name__ == "__main__":` idiom (Week 4 covers this fully).
- f-string formatting with `:.2f`.

You'll write code that looks like this every week from now on. Get
comfortable with the shape.

## 9. Wrap-up

You've learned:

- `input()` returns a string — always cast it before doing math.
- How to defend against bad input with `try/except ValueError`.
- How to annotate variables and functions with types.
- That hints are advisory; `mypy` is what enforces them.

You now have every ingredient you need for the Week 2 mini-project: read
input, parse it, compute, format, print.

## Further Reading

- [docs.python.org — input() and print()](https://docs.python.org/3/tutorial/inputoutput.html)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [PEP 604 — Allow writing `int | None`](https://peps.python.org/pep-0604/)
- [mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
