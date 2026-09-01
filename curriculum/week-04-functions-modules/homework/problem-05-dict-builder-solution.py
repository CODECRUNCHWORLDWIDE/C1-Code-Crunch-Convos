"""Build and merge plain dict records from keyword and positional arguments.

Week 4 homework, problem 5, Code Crunch Convos.

Save your own copy as ``dict_builder.py`` in your ``homework/`` folder.

``build_record`` collects named values with ``**fields``. ``merge_records``
collects whole dicts with ``*records``. Neither one changes anything the
caller handed it - both return a new dict.
"""


def build_record(**fields: object) -> dict[str, object]:
    """Return a dict of the keyword arguments whose value is not None.

    Args:
        **fields: Any number of named values.

    Returns:
        A new dict containing only the pairs whose value is not None.

    Example:
        >>> build_record(name="Amina", age=29, email=None)
        {'name': 'Amina', 'age': 29}
    """
    record: dict[str, object] = {}
    for key, value in fields.items():
        if value is not None:
            record[key] = value
    return record


def merge_records(*records: dict) -> dict:
    """Return one dict merged from `records`, later records winning collisions.

    Args:
        *records: Any number of dicts.

    Returns:
        A new dict. The inputs are not modified.

    Example:
        >>> merge_records({"a": 1}, {"b": 2}, {"a": 99})
        {'a': 99, 'b': 2}
    """
    result: dict = {}
    for record in records:
        result.update(record)
    return result


def _demo() -> None:
    """Print the three examples from the brief plus one merge."""
    print(build_record(name="Amina", age=29, email=None))
    print(build_record())
    print(build_record(a=None, b=None))
    print(merge_records({"a": 1}, {"b": 2}, {"a": 99}))


if __name__ == "__main__":
    _demo()
