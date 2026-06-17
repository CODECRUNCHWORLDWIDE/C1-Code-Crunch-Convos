# Lecture 01 — Classes and Instances

> **Reading time:** ~40 minutes. **Prerequisites:** Weeks 1–6.

In Weeks 1–6 you wrote functions that operated on values: `parse_csv(path)`,
`average(numbers)`, `safe_divide(a, b)`. That style is called **procedural
programming**. It works beautifully — until your program grows enough that the
*same data* keeps showing up in many functions, and you find yourself passing
the same dictionary around like a folder of papers.

This lecture introduces **classes**, Python's main tool for bundling that
shared data with the functions that operate on it. We cover only the
fundamentals: what a class is, how to define one, what `self` is, the
difference between *instance attributes* and *class attributes*, and how to
make your objects print nicely with `__repr__` and `__str__`. Inheritance,
dataclasses, and dunder methods come in lectures 02 and 03.

---

## 1. What problem does OOP solve?

Imagine you are writing a tiny banking program. You need to track several
accounts. Each account has:

- a holder's name,
- a balance,
- a list of past transactions,

and you need to be able to **deposit**, **withdraw**, and **print a
statement**. With only functions and dictionaries you might write:

```python
def make_account(name: str, opening_balance: float) -> dict:
    return {"name": name, "balance": opening_balance, "history": []}

def deposit(account: dict, amount: float) -> None:
    account["balance"] += amount
    account["history"].append(("deposit", amount))

def withdraw(account: dict, amount: float) -> None:
    if amount > account["balance"]:
        raise ValueError("insufficient funds")
    account["balance"] -= amount
    account["history"].append(("withdraw", amount))
```

This works. But notice three pain points:

1. **Nothing stops you from corrupting the dict.** A teammate writes
   `account["balance"] = "oops"` and your program will crash much later, far
   from the cause.
2. **The functions and the data are not visibly connected.** A new reader has
   to grep the codebase to find every function that touches an `account` dict.
3. **There is no clean way to add behavior.** Where does `apply_interest()`
   live? `print_statement()`? You end up with a `bank_account.py` module of
   loose functions that all take the same `account` argument.

A **class** lets you fix all three at once. The class is a kind of *blueprint*
that ties the data and the behavior together. Every individual account is then
an **instance** of that blueprint.

> **Definition.** A **class** describes the shape and behavior of a kind of
> thing. An **instance** is one specific thing built from that blueprint. The
> class `Dog` describes what every dog has and can do. The instance `fido =
> Dog("Fido", 3)` is one specific dog.

OOP is **not** the answer to every problem — small scripts and pure data
transformations are often clearer as plain functions. But when state and
behavior live together for a long time, OOP usually wins.

---

## 2. Defining your first class

The minimal Python class looks like this:

```python
class Dog:
    pass
```

`class` is the keyword. `Dog` is the **class name** — by PEP 8 convention,
class names use `CamelCase` (also called PascalCase). `pass` is a placeholder
saying "this class has no body yet".

You **create an instance** by calling the class like a function:

```python
fido = Dog()
rex = Dog()
print(type(fido))   # <class '__main__.Dog'>
print(fido is rex)  # False — two distinct objects
```

`fido` and `rex` are both `Dog` instances, but they are independent objects.
You can prove this by checking their identity with `is` or by looking at their
memory addresses with `id()`.

---

## 3. `__init__`: the initializer

A class with no attributes is not very useful. To give each new dog a name and
an age, define an **initializer** called `__init__`:

```python
class Dog:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
```

A few things to notice:

- `__init__` (two underscores on each side — these are called **dunder**
  methods, short for "double underscore") is automatically called by Python
  when you do `Dog("Fido", 3)`.
- It does **not** return anything. Its only job is to set up the brand-new
  instance.
- The first parameter is `self`. We explain `self` in the next section.
- The other parameters (`name`, `age`) are the values *you* supply when you
  create the dog.

Now creation looks like this:

```python
fido = Dog("Fido", 3)
print(fido.name)  # "Fido"
print(fido.age)   # 3
```

> **Type hints are optional but encouraged.** From here on, every `__init__`
> in this course uses type hints. They serve as documentation and let editors
> catch mistakes.

`__init__` is sometimes called the **constructor**, but technically Python's
constructor is `__new__`. You will almost never override `__new__`. Treat
`__init__` as "the constructor" for daily work.

---

## 4. What is `self`?

`self` is the conventional name for **"this particular instance"**. When you
write:

```python
fido = Dog("Fido", 3)
```

Python roughly does this behind the scenes:

1. Allocate a new empty object.
2. Call `Dog.__init__(<that new object>, "Fido", 3)`.
3. Bind the new object to the name `fido`.

So inside `__init__`, `self` *is* the new object. When you write
`self.name = name`, you are saying "attach an attribute called `name` to this
new object, with the value the caller gave us".

`self` is not a keyword. You could legally name it `this` or `me`, and Python
would not care. **Do not do that.** Every Python codebase in the world uses
`self`. Following the convention is part of being a good citizen.

When you later call `fido.bark()`, Python again rewrites it: `Dog.bark(fido)`.
The instance you call the method on is automatically passed as the first
argument. That is the entire mystery of `self`.

---

## 5. Methods

A **method** is just a function defined inside a class. It almost always takes
`self` as its first parameter:

```python
class Dog:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def bark(self) -> str:
        return f"{self.name} says woof!"

    def have_birthday(self) -> None:
        self.age += 1
```

Use it like this:

```python
fido = Dog("Fido", 3)
print(fido.bark())     # "Fido says woof!"
fido.have_birthday()
print(fido.age)        # 4
```

Notice how `bark` reads `self.name` and `have_birthday` *mutates* `self.age`.
Methods are how an instance does work on its own data.

A subtle but important point: **methods do not need to return anything.** A
method that mutates state (`have_birthday`, `deposit`, `withdraw`) usually
returns `None`. A method that computes a value (`bark`, `area`, `balance`)
returns that value. Mixing both — mutating *and* returning — is a smell;
prefer one or the other per method.

---

## 6. Instance attributes vs class attributes

There are two kinds of attribute, and beginners constantly mix them up.

### Instance attribute — one per object

Anything you set on `self` inside a method (most often inside `__init__`) is
an **instance attribute**. Each instance gets its own copy:

```python
class Dog:
    def __init__(self, name: str, age: int) -> None:
        self.name = name   # instance attribute
        self.age = age     # instance attribute

fido = Dog("Fido", 3)
rex = Dog("Rex", 5)
fido.name = "Fido Jr."     # only affects fido
print(rex.name)            # "Rex"
```

### Class attribute — one shared by all instances

Anything you set *directly in the class body*, outside any method, is a
**class attribute**. It is shared across every instance:

```python
class Dog:
    species: str = "Canis familiaris"   # class attribute

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

fido = Dog("Fido", 3)
rex = Dog("Rex", 5)
print(fido.species)   # "Canis familiaris"
print(rex.species)    # "Canis familiaris"
print(Dog.species)    # also "Canis familiaris"
```

Class attributes are good for **constants** that apply to every instance
(`species`, `wheels = 4` on a `Car`, `MAX_BALANCE = 1_000_000` on a bank
account). They are **bad** for mutable defaults — and this is one of Python's
most famous footguns:

```python
class Dog:
    tricks = []   # BAD — shared list

    def learn(self, trick: str) -> None:
        self.tricks.append(trick)

fido = Dog()
rex = Dog()
fido.learn("sit")
print(rex.tricks)   # ["sit"]  -- yikes, rex learned a trick too!
```

The fix is to put the list on the instance:

```python
class Dog:
    def __init__(self) -> None:
        self.tricks: list[str] = []   # one list per dog
```

Rule of thumb: **immutable** values (numbers, strings, tuples) are usually fine
as class attributes. **Mutable** values (lists, dicts, sets) almost always
belong on the instance.

---

## 7. Attribute access and dot notation

Reading or writing an attribute uses **dot notation**: `object.attribute`.
Python looks up the name in this order:

1. The instance's own `__dict__`.
2. The class's `__dict__`.
3. The parent classes (we cover this in lecture 02).
4. If still not found, `AttributeError`.

You can see the dictionaries directly:

```python
fido = Dog("Fido", 3)
print(fido.__dict__)   # {'name': 'Fido', 'age': 3}
print(Dog.__dict__)    # includes 'species', '__init__', 'bark', ...
```

This lookup order is why an instance attribute *shadows* a class attribute of
the same name: once you write `fido.species = "Wolf"`, lookups on `fido` find
the instance one first.

---

## 8. `__repr__` vs `__str__`

By default, printing an instance gives you something useless:

```python
fido = Dog("Fido", 3)
print(fido)
# <__main__.Dog object at 0x10a8c7f10>
```

You fix this by defining the two **representation dunders**:

```python
class Dog:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, age={self.age!r})"

    def __str__(self) -> str:
        return f"{self.name} (age {self.age})"
```

Now:

```python
fido = Dog("Fido", 3)
print(fido)         # uses __str__   -> "Fido (age 3)"
print(repr(fido))   # uses __repr__  -> "Dog(name='Fido', age=3)"
fido                # in the REPL, also uses __repr__
```

### Which one do I write?

- **`__repr__`** is for **developers**. The goal is an *unambiguous* string —
  ideally one that, if you pasted it back into the REPL, would recreate an
  equivalent object. Always implement `__repr__`.
- **`__str__`** is for **end users**. The goal is *readable*. It is optional —
  if you do not define it, Python falls back to `__repr__`.

A rule of thumb that has served generations of Python developers well:
**always write `__repr__`; write `__str__` only when the user-facing form is
clearly different from the developer-facing form.**

The `!r` in the f-string above calls `repr()` on the value, which is why the
string `'Fido'` shows up with quotes — exactly what you would type to recreate
it. See the [Data model docs](https://docs.python.org/3/reference/datamodel.html#object.__repr__)
for the full contract.

---

## 9. Putting it together

Here is the full `Dog` class with everything from this lecture:

```python
class Dog:
    """A very small dog model."""

    species: str = "Canis familiaris"   # class attribute (constant)

    def __init__(self, name: str, age: int) -> None:
        self.name = name                # instance attributes
        self.age = age
        self.tricks: list[str] = []     # mutable default -> instance

    def bark(self) -> str:
        return f"{self.name} says woof!"

    def have_birthday(self) -> None:
        self.age += 1

    def learn(self, trick: str) -> None:
        self.tricks.append(trick)

    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, age={self.age!r})"

    def __str__(self) -> str:
        return f"{self.name}, age {self.age}, knows: {', '.join(self.tricks) or 'no tricks yet'}"


if __name__ == "__main__":
    fido = Dog("Fido", 3)
    fido.learn("sit")
    fido.learn("roll over")
    fido.have_birthday()

    print(fido)            # user form
    print(repr(fido))      # developer form
    print(fido.species)    # "Canis familiaris"
    print(fido.bark())
```

Run it. Change one of the methods. Add a class attribute for the longest age
any dog has reached. Try setting `Dog.species = "Test"` and see how it affects
all instances.

---

## 10. When **not** to write a class

Beginners often over-class. If a problem is one function plus one transient
value, do not wrap it in a class. Some red flags that you do not need OOP yet:

- Your class has only one method and no real attributes — that is just a
  function with extra steps.
- Your class only holds data, never behavior — consider a `dataclass`
  (lecture 03) or a `NamedTuple`.
- You only ever create one instance and use it as a global — you may have
  written a module with extra ceremony.

Use classes when:

- The same set of values needs to flow through many functions together.
- You want the same data type to behave differently in different cases
  (polymorphism — see lecture 02).
- You expect to extend the type later with new behavior (a plugin system, a
  hierarchy, a state machine).

---

## 11. Recap

- A **class** is a blueprint. An **instance** is one object built from it.
- `__init__(self, ...)` runs at creation time and sets up the instance.
- `self` is "this instance" — Python passes it automatically.
- **Instance attributes** live on `self` and are per-object.
- **Class attributes** live on the class itself and are shared by all
  instances. Avoid mutable class attributes.
- Always implement **`__repr__`**; add **`__str__`** when the user-facing form
  differs.
- Reach for OOP when state and behavior must live together long enough to
  earn the extra structure.

**Next lecture:** inheritance, `super()`, and why "composition over
inheritance" is the most repeated piece of OOP advice for a reason.
