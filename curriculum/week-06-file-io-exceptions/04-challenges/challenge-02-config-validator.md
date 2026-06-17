# Challenge 02 — Config validator

Build a JSON config validator. Given a config file and a hand-written schema, your validator should either accept it silently or raise a descriptive error pinpointing the first problem — ideally with the line and column number.

This is exactly what tools like [`jsonschema`](https://python-jsonschema.readthedocs.io/) do, but you will build a tiny version yourself so you understand the principles.

---

## Specification

Write a script `challenge-02-solution.py` that exposes:

```python
class ConfigError(Exception):
    """Base class for all config validation errors."""

class ConfigParseError(ConfigError):
    """Raised when the file is not valid JSON."""

class ConfigSchemaError(ConfigError):
    """Raised when the JSON is valid but does not match the schema."""

def validate_config(path: Path, schema: dict) -> dict:
    """Load and validate a JSON config file. Return the parsed dict.

    Raises:
        ConfigParseError: if the file cannot be parsed as JSON.
            The error message should include the offending line and column.
        ConfigSchemaError: if the JSON does not match `schema`.
            The error message should name the offending key and the expected type.
    """
```

### Schema format

A schema is a `dict[str, type | tuple[type, ...]]` that maps required keys to their expected Python type(s). For example:

```python
SCHEMA = {
    "log_level": str,
    "debug": bool,
    "port": int,
    "tags": list,
    "database": dict,
}
```

This means a valid config must have **all five** keys, with values of those exact types.

### What "validate" means

For each `(key, expected_type)` pair in the schema:

1. If `key` is missing from the config, raise `ConfigSchemaError` with a message like `"missing required key: 'debug'"`.
2. If the value is not an instance of `expected_type`, raise `ConfigSchemaError` with a message like `"key 'port' expected int, got str"`.

Extra keys in the config that are NOT in the schema are fine — do not raise on them. (Real schemas have stricter rules but this is enough for a beginner challenge.)

### Error chaining

`ConfigParseError` should be raised `from` the underlying `json.JSONDecodeError`. The traceback should preserve the cause so a maintainer can see both.

### Example session

Given `config.json`:

```json
{
  "log_level": "INFO",
  "debug": true,
  "port": "5432",
  "tags": [],
  "database": {}
}
```

`validate_config(...)` should raise:

```
ConfigSchemaError: key 'port' expected int, got str
```

Given an invalid JSON file (trailing comma):

```json
{ "debug": true, }
```

It should raise:

```
ConfigParseError: invalid JSON at line 1, column 17: Expecting property name enclosed in double quotes
```

The script's `__main__` should demonstrate at least three cases: a valid config, a schema mismatch, and a parse error. Use `try/except` to catch and print each one.

---

## Stretch goals

1. **Nested schemas** — let schema values themselves be dicts (so you can validate `"database": {"host": str, "port": int}` recursively).
2. **Optional keys** — let a key be marked optional, e.g. `"description": (str, type(None))`.
3. **Range constraints** — validate that `port` is between 1 and 65535.
4. **Multiple errors at once** — collect every validation error instead of stopping at the first one. Raise a single `ConfigSchemaError` whose message lists them all.

---

## Rubric (10 pts)

| Criterion | Points |
|---|---|
| Three exception classes defined correctly | 2 |
| `validate_config` returns the dict on success | 1 |
| Missing keys produce a clear `ConfigSchemaError` | 2 |
| Wrong-type values produce a clear `ConfigSchemaError` | 2 |
| `JSONDecodeError` is wrapped with `raise ... from e` | 2 |
| Error messages include the offending key/type/line | 1 |
