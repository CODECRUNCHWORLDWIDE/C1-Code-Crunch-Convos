# Week 11 Quiz — Testing, Debugging & Code Quality

Ten multiple-choice questions. Pick the **single best** answer. Answer key at the bottom — no peeking.

---

**1. By default, `pytest` collects test functions from files matching which pattern?**

A. Any `.py` file in the current directory.
B. Files named `test_*.py` or `*_test.py`.
C. Files inside a directory called `pytest/`.
D. Only `tests.py`.

---

**2. What does this fixture's `scope="module"` argument do?**

```python
@pytest.fixture(scope="module")
def db_connection():
    ...
```

A. It runs the fixture once per test function in the module.
B. It runs the fixture exactly once per test file.
C. It runs the fixture once per test class.
D. It runs the fixture once for the entire `pytest` session.

---

**3. You want to test five values against the same assertion logic. Which feature avoids copy-pasting the test five times?**

A. `pytest.skip`
B. `pytest.fixture`
C. `pytest.mark.parametrize`
D. `pytest.raises`

---

**4. Your code does `import requests` at the top of `myapp.py` and later calls `requests.get(...)`. Which patch target is correct?**

A. `patch("requests.get")`
B. `patch("myapp.requests.get")`
C. `patch("myapp.get")`
D. Both A and B are valid; B is usually the safer choice because it patches the exact lookup path used by `myapp`.

---

**5. Which statement about line coverage versus branch coverage is correct?**

A. They always produce the same number.
B. Branch coverage is a subset of line coverage and is always lower.
C. Branch coverage can be lower than line coverage because it requires *both* sides of every conditional to be exercised.
D. Line coverage is more accurate than branch coverage.

---

**6. Inside a `(Pdb)` prompt, you want to advance one line of code without stepping into the function being called on that line. Which command do you use?**

A. `s`
B. `n`
C. `c`
D. `r`

---

**7. Which tool is primarily a code *formatter* (not a linter)?**

A. `ruff`
B. `mypy`
C. `black`
D. `pytest`

---

**8. Which `pyproject.toml` snippet enables `mypy`'s strict mode?**

A.
```toml
[tool.mypy]
warn_return_any = true
```

B.
```toml
[tool.mypy]
strict = true
```

C.
```toml
[tool.mypy]
disallow_typed_defs = false
```

D.
```toml
[tool.black]
mypy_strict = true
```

---

**9. Where do GitHub Actions workflow files live in a repository?**

A. `.github/`
B. `.github/workflows/`
C. `actions/`
D. The repository root, named `actions.yml`.

---

**10. According to the testing pyramid, which mix is healthy?**

A. Many end-to-end tests, few integration tests, very few unit tests.
B. Equal numbers of all three.
C. Many unit tests, fewer integration tests, very few end-to-end tests.
D. Only unit tests — integration and end-to-end tests are not needed.

---

## Answer key

1. **B** — `test_*.py` or `*_test.py`. Cite: <https://docs.pytest.org/en/stable/explanation/goodpractices.html#test-discovery>
2. **B** — module scope runs the fixture once per test file.
3. **C** — `@pytest.mark.parametrize` is the table-driven test feature.
4. **D** — Both work, but patching the path where the name is looked up (`myapp.requests.get`) is the recommended pattern for isolating the patch to one module.
5. **C** — A single test can cover every line without covering every branch.
6. **B** — `n` (next) steps *over* function calls; `s` (step) steps *into* them.
7. **C** — `black` formats; `ruff` lints (and optionally formats); `mypy` type-checks; `pytest` runs tests.
8. **B** — `strict = true` is the one-line opt-in.
9. **B** — Workflows must live in `.github/workflows/` and use `.yml` or `.yaml`.
10. **C** — Many fast unit tests, fewer integration tests, fewest end-to-end tests. The inverse is called the ice-cream-cone anti-pattern.
