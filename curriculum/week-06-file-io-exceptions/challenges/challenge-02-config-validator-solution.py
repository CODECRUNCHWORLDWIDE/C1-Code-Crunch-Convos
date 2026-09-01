"""challenge-02-config-validator-solution.py — a tiny JSON config validator.

Three exception classes in a one-parent tree (ConfigError is the type callers
catch when they do not care *why* the config was bad), and one public function
that does load-then-validate in two clearly separated phases. A file that is not
JSON at all and a file that is JSON but the wrong shape are different kinds of
wrong, so they get different exception types — and both are a ConfigError.

Trade-off: validation stops at the first problem. That keeps the code and the
message simple. Collecting every problem in one pass is the fourth stretch goal
on the page, and it is what you would actually ship.

The four demonstration configs are written into a throwaway temporary directory
at run time, so the download runs on any machine with nothing set up beforehand
and leaves nothing behind.

Run it with::

    python challenge-02-config-validator-solution.py
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


class ConfigError(Exception):
    """Base class for all config validation errors."""


class ConfigParseError(ConfigError):
    """Raised when the file is not valid JSON."""


class ConfigSchemaError(ConfigError):
    """Raised when the JSON is valid but does not match the schema."""


SCHEMA: dict[str, type | tuple[type, ...]] = {
    "log_level": str,
    "debug": bool,
    "port": int,
    "tags": list,
    "database": dict,
}


def _type_name(expected: type | tuple[type, ...]) -> str:
    """Return a human-readable name for a single type or a tuple of them."""
    if isinstance(expected, tuple):
        return " or ".join(t.__name__ for t in expected)
    return expected.__name__


def _matches(value: object, expected: type | tuple[type, ...]) -> bool:
    """Return isinstance(value, expected), with the bool/int trap closed.

    ``bool`` is a subclass of ``int`` in Python, so ``isinstance(True, int)`` is
    True. A config that says ``"port": true`` would otherwise sail through an
    ``int`` check. Unless bool was explicitly asked for, reject bools.
    """
    wants_bool = expected is bool or (isinstance(expected, tuple) and bool in expected)
    if isinstance(value, bool) and not wants_bool:
        return False
    return isinstance(value, expected)


def load_json(path: Path) -> object:
    """Read *path* and parse it as JSON.

    Raises:
        ConfigParseError: the file cannot be read, or is not valid JSON. The
            message carries the parser's own line, column and explanation.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ConfigParseError(f"cannot read {path.name}: {e.strerror}") from e

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ConfigParseError(
            f"invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
        ) from e


def check_schema(config: dict, schema: dict[str, type | tuple[type, ...]]) -> None:
    """Raise ConfigSchemaError on the first key that is missing or mistyped."""
    for key, expected in schema.items():
        if key not in config:
            raise ConfigSchemaError(f"missing required key: {key!r}")
        value = config[key]
        if not _matches(value, expected):
            raise ConfigSchemaError(
                f"key {key!r} expected {_type_name(expected)}, "
                f"got {type(value).__name__}"
            )


def validate_config(path: Path, schema: dict) -> dict:
    """Load and validate a JSON config file. Return the parsed dict.

    Raises:
        ConfigParseError: if the file cannot be parsed as JSON.
            The error message includes the offending line and column.
        ConfigSchemaError: if the JSON does not match *schema*.
            The error message names the offending key and the expected type.
    """
    config = load_json(path)
    if not isinstance(config, dict):
        raise ConfigSchemaError(
            f"top-level value must be an object, got {type(config).__name__}"
        )
    check_schema(config, schema)
    return config


#: One config per outcome the validator has to produce.
CASES: dict[str, str] = {
    "good.json": """{
  "log_level": "INFO",
  "debug": true,
  "port": 5432,
  "tags": ["prod", "eu-west"],
  "database": {"host": "db-primary"},
  "comment": "extra keys are allowed"
}
""",
    "wrong-type.json": """{
  "log_level": "INFO",
  "debug": true,
  "port": "5432",
  "tags": [],
  "database": {}
}
""",
    "missing-key.json": """{
  "log_level": "INFO",
  "port": 5432,
  "tags": [],
  "database": {}
}
""",
    "bad-json.json": '{ "debug": true, }\n',
}


def main() -> None:
    """Write the four demonstration configs and validate each one."""
    with tempfile.TemporaryDirectory() as workspace:
        scratch = Path(workspace) / "configs"
        scratch.mkdir(parents=True, exist_ok=True)

        for name, text in CASES.items():
            path = scratch / name
            path.write_text(text, encoding="utf-8")
            try:
                config = validate_config(path, SCHEMA)
            except ConfigParseError as e:
                print(f"{name}: ConfigParseError: {e}")
            except ConfigSchemaError as e:
                print(f"{name}: ConfigSchemaError: {e}")
            else:
                print(f"{name}: OK - {len(config)} keys, port={config['port']}")


if __name__ == "__main__":
    main()
