# Coding Standards

Industry-standard conventions for the Python code you'll write in this bootcamp. These rules exist so that **your code is easy for other people (and future-you) to read**.

> 📚 **Authoritative references**
>
> - [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
> - [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
> - [PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/) (`import this`)
> - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

## 1. Formatting (let a tool do it)

Don't argue about formatting. Run [`black`](https://black.readthedocs.io/) and [`ruff`](https://github.com/astral-sh/ruff). They handle indentation, line length, quote style, and most spacing decisions.

```bash
pip install black ruff
black .
ruff check . --fix
```

Add this to your editor so it runs on save.

---

## 2. Naming

| Thing                        | Convention             | Example                              |
| ---------------------------- | ---------------------- | ------------------------------------ |
| Variables                    | `snake_case`           | `user_age`, `total_price`            |
| Functions                    | `snake_case`           | `def calculate_total(...)`           |
| Constants                    | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES = 3`                    |
| Classes                      | `PascalCase`           | `class ShoppingCart:`                |
| Modules / files              | `snake_case.py`        | `data_loader.py`                     |
| Private (by convention)      | leading underscore     | `_internal_helper`                   |

Names should be **pronounceable, searchable, and accurate**.

```python
# Bad
d = 7                      # what is d?
def calc(x, y): ...        # calc what?

# Good
days_since_signup = 7
def calculate_shipping(weight_kg, distance_km): ...
```

---

## 3. Functions

- Do **one** thing. If your function is longer than ~20 lines or has more than ~3 parameters, consider splitting it.
- Use **keyword arguments** for booleans: `connect(timeout=30, retry=True)` not `connect(30, True)`.
- Return early to avoid deep nesting.

```python
# Bad
def get_user_status(user):
    if user is not None:
        if user.is_active:
            if user.has_paid:
                return "active"
            else:
                return "unpaid"
        else:
            return "inactive"
    else:
        return "unknown"

# Good
def get_user_status(user):
    if user is None:
        return "unknown"
    if not user.is_active:
        return "inactive"
    if not user.has_paid:
        return "unpaid"
    return "active"
```

---

## 4. Type hints (PEP 484)

Use type hints starting from Week 4. They're free documentation and tools can check them.

```python
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}!\n" * times
```

Reference: [typing module docs](https://docs.python.org/3/library/typing.html).

---

## 5. Docstrings

Every public function, class, and module should have a docstring.

```python
def calculate_tax(amount: float, rate: float) -> float:
    """Compute tax on `amount` at the given `rate`.

    Args:
        amount: Pre-tax amount in dollars.
        rate: Tax rate as a decimal (e.g. 0.07 for 7%).

    Returns:
        Tax owed in dollars, rounded to 2 decimal places.
    """
    return round(amount * rate, 2)
```

Use [Google-style](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods) or [NumPy-style](https://numpydoc.readthedocs.io/en/latest/format.html) — pick one and stick to it within a project.

---

## 6. Comments

Comments explain **why**, not **what**. The code already shows what.

```python
# Bad
x = x + 1   # increment x

# Good
# Retry once on transient network errors — boto3 stops retrying after 3.
x = x + 1
```

If you're tempted to write a "what" comment, rename the variable or extract a function instead.

---

## 7. Imports

```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party
import requests
from flask import Flask

# 3. Local
from .models import User
from .utils import format_date
```

- One import per line.
- No `from module import *`.
- No unused imports.

---

## 8. Error handling

Don't swallow exceptions silently.

```python
# Bad
try:
    risky_operation()
except Exception:
    pass

# Good
try:
    risky_operation()
except SpecificError as e:
    logger.warning("risky_operation failed: %s", e)
    raise
```

Catch the **narrowest** exception type that's appropriate.

---

## 9. The Zen of Python

```text
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
...
```

Run `python -c "import this"` to read the full poem.

---

## 10. Tooling summary

| Purpose       | Tool                                                          | Command                  |
| ------------- | ------------------------------------------------------------- | ------------------------ |
| Formatter     | [black](https://black.readthedocs.io/)                        | `black .`                |
| Linter        | [ruff](https://github.com/astral-sh/ruff)                     | `ruff check .`           |
| Type checker  | [mypy](https://mypy.readthedocs.io/) (Week 11+)               | `mypy .`                 |
| Tests         | [pytest](https://docs.pytest.org/)                            | `pytest`                 |
| Imports sort  | `ruff check --select I --fix`                                 | (covered by ruff)        |

Configure these once in `pyproject.toml`. We'll set that up in [Week 11](../curriculum/week-11-testing-debugging/).
