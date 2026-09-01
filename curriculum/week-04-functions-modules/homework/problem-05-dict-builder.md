# Homework Problem 5 — Dict Builder

> **Topic:** `**kwargs` and `*args`, filtering on `is not None` instead of truthiness, and returning new objects instead of changing the caller's
> **Lecture:** [Lecture Note 2 — `*args`, `**kwargs`, and Scope](../lecture-notes/02-args-kwargs-and-scope.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** it contains the single most common silent bug in beginner Python — writing `if value:` when you meant `if value is not None:`. It throws away zeroes, empty strings and `False` without a word of complaint, and the data is simply gone by the time anybody notices. Once you have watched it happen you will never write it again.

## The Brief

A **record** is a dict describing one thing: a person, an order, a
booking. Something like this:

```python
{"name": "Amina", "age": 29}
```

Records get built from forms, and forms have blank boxes. If somebody did
not fill in their email, you do not want `{"email": None}` sitting in the
record — you want no `email` key at all. There is a difference between
"we do not know" and "it is empty", and a missing key says the first one
cleanly.

Write two functions.

**`build_record(**fields)`** takes any number of named values and returns
a dict of just the ones that are not `None`.

```python
build_record(name="Amina", age=29, email=None)
# {"name": "Amina", "age": 29}

build_record()
# {}

build_record(a=None, b=None)
# {}
```

The `**` in front of `fields` is the new piece. It means "collect every
keyword argument I am given into a dict called `fields`". You do not
declare the names in advance. Whatever the caller types before the `=`
becomes a key.

**`merge_records(*records: dict) -> dict`** takes any number of dicts and
returns one dict with all of them combined. When two of them use the same
key, the later one wins.

```python
merge_records({"a": 1}, {"b": 2}, {"a": 99})
# {"a": 99, "b": 2}
```

The single `*` is the sibling of `**`. It collects **positional**
arguments — the ones with no name in front of them — into a tuple.

One rule sits over both functions: neither one may change anything the
caller handed it. Both build something new and hand that back.

## Starter

Save this as `dict_builder.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it just returns empty things:

```python
"""Build and merge plain dict records from keyword and positional arguments."""


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
    # TODO: walk fields.items() and copy across every pair whose value
    #       is not None. Use `is not None`, not `if value`.
    return record


def merge_records(*records: dict) -> dict:
    """Return one dict merged from `records`, later records winning collisions."""
    result: dict = {}
    # TODO: update result with each record in turn, left to right
    return result


def _demo() -> None:
    """Print the three examples from the brief plus one merge."""
    print(build_record(name="Amina", age=29, email=None))
    print(build_record())
    print(build_record(a=None, b=None))
    print(merge_records({"a": 1}, {"b": 2}, {"a": 99}))


if __name__ == "__main__":
    _demo()
```

`merge_records` is missing its `Args:`, `Returns:` and `Example:`.
Writing those is part of the work.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/homework/problem-05-dict-builder.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `build_record` accepts any number of keyword arguments and returns a
   new dict.
2. A key whose value is `None` is left out. Every other key is kept,
   including ones whose value is `0`, `False` or `""`.
3. `build_record()` with no arguments returns `{}`.
4. `merge_records` accepts any number of dicts and returns a new dict
   with all their pairs.
5. On a repeated key, the value from the later dict wins.
6. `merge_records()` with no arguments returns `{}`.
7. Neither function modifies any dict it was given.
8. Type hints and a full docstring on all three functions.

## Constraints

- **Filter with `is not None`, never with `if value:`.** The brief says
  "values that are not `None`". It does not say "values that are truthy".
  `0`, `False`, `""`, `[]` and `0.0` are all falsy and all perfectly real
  data. Common bugs to catch shows what `if value:` does to a record with
  an age of zero.
- **Use `is`, not `==`, when comparing to `None`.** `None` is a single
  object that exists exactly once in a running program, so `is` asks the
  one question that cannot be faked: "is this that object". `==` calls a
  method the object is allowed to redefine.
- **`merge_records` starts from `{}`.** Starting from `records[0]` gives
  you two bugs for the price of one: it crashes on no arguments, and when
  it does not crash it quietly rewrites the caller's first dict.
- **Do not special-case the empty call.** `**fields` with no keyword
  arguments is an empty dict, and the loop over it runs zero times.
  `*records` with no positional arguments is an empty tuple, same story.
  Both functions get `{}` for free, and code you did not write cannot be
  wrong.
- **`_demo` prints; the other two do not.** Same split as every other
  problem this week.

## Expected output

```text
$ python problem-05-dict-builder.py
{'name': 'Amina', 'age': 29}
{}
{}
{'a': 99, 'b': 2}
```

The first three lines are the brief's own examples, in order. The fourth
is the merge.

Now prove the falsy values survive, because that is the thing this
problem is really about:

```bash
python -c "from dict_builder import build_record; print(build_record(age=0, active=False, note='', email=None))"
```

```text
{'age': 0, 'active': False, 'note': ''}
```

Three keys kept, one dropped. Only the `None` went.

And prove the inputs are untouched:

```bash
python -c "from dict_builder import merge_records as m; a={'x':1}; print(m(a, {'x':2}), a)"
```

```text
{'x': 2} {'x': 1}
```

The merged dict says `2`. The original still says `1`. That is what
"returns a new dict" means, and it is checkable in one line.

The docstring examples are real tests:

```bash
python -m doctest dict_builder.py -v
```

The last three lines:

```text
2 tests in 4 items.
2 passed.
Test passed.
```

## Steps

1. Activate your Week 4 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `dict_builder.py`. Run it. Four empty results.
3. Look at what `**fields` actually gives you before you filter it. Add
   `print(fields)` as the first line of `build_record`, run the file, and
   read the three dicts that come out. Take the print back out.
4. Write the loop. Two lines: walk `fields.items()`, and copy the pair
   across when `value is not None`.
5. Run it. The first line should now be `{'name': 'Amina', 'age': 29}`.
6. Write `merge_records`. Two lines: loop over `records`, call
   `result.update(record)`.
7. Run the falsy-value check from **Expected output**. If any of `0`,
   `False` or `''` is missing, you wrote `if value:` somewhere.
8. Run the mutation check. If the original dict came back changed, you
   started from `records[0]`.
9. Finish `merge_records`'s docstring, then run
   `python -m doctest dict_builder.py -v`.
10. Compare against **The Solution**, tick the acceptance checklist, and
    commit: `git add homework/dict_builder.py` then
    `git commit -m "Week 4 homework: dict builder"`.

## The Solution

```python
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
```

**Why it works.**

**`**fields` in the `def` line packs every keyword argument into a dict.**
Inside the function, `fields` is an ordinary dict — nothing special about
it — so `fields.items()` hands you `(key, value)` pairs exactly as it
would for any other dict. The keys are always strings, because the caller
typed them as Python names.

The type hint reads oddly the first time. `**fields: object` annotates the
*value* type, not the dict: it says "the values can be anything". The
return hint `dict[str, object]` describes the dict that comes back — string
keys, any values.

**`if value is not None` is identity, and that is load-bearing.** `is`
asks "are these the same object". There is exactly one `None` in a running
Python program, so `value is None` is a question with a definite answer
that no object can lie about. `if value:` asks a completely different
question — "is this thing truthy" — and gets `False` for `0`, `False`,
`""`, `[]`, `{}` and `0.0`, every one of which is real data somebody typed
on purpose.

**`merge_records` builds a new dict and never touches its inputs.**
`result` starts empty, and `result.update(record)` copies pairs *into*
`result`. It changes `result`, which the function owns, and reads
`record`, which the caller owns. Note the order: applied left to right,
each later record overwrites keys the earlier ones set, which is exactly
the rule the brief specifies. `{"a": 1}` then `{"a": 99}` leaves `99`.
Loop the other way and you would get `1`.

**`*records: dict` packs positional arguments into a tuple.** One star
packs by position, two stars pack by name — the same asymmetry you already
know from the call site, mirrored in the definition:

| In the `def` line | Collects | Into a |
|---|---|---|
| `*records` | positional arguments | tuple |
| `**fields` | keyword arguments | dict |

**Both empty cases fall out for free.** `merge_records()` gets an empty
tuple, so the loop runs zero times and `{}` comes back — which is the
right answer and needed no `if`. `build_record()` is the same story with
an empty dict.

**Insertion order survives.** Since Python 3.7 the language guarantees a
dict remembers the order its keys went in, and `**kwargs` preserves the
order the caller wrote them. That is why the example prints
`{'name': 'Amina', 'age': 29}` and not some other arrangement, and it is
why a doctest on a dict is stable enough to be worth writing at all.

## Download and run

Download [problem-05-dict-builder-solution.py](./problem-05-dict-builder-solution.py)
and run it:

```bash
python problem-05-dict-builder-solution.py
```

Save your own copy as `dict_builder.py` in your homework folder, and
commit that one. The longer download name keeps it from landing on top of
your work.

## Common bugs to catch

- **Filtering on truthiness instead of on `None`.** This is the bug the
  problem exists to teach.

  ```python
  def build_record(**fields):
      return {k: v for k, v in fields.items() if v}     # WRONG
  ```

  Run it on realistic data and watch three real values disappear:

  ```text
  {'name': 'Amina'}
  ```

  That was called with `name="Amina", age=0, active=False, email=None,
  note=""`. An age of zero, an explicit `False` flag and a deliberately
  empty note were all things the caller meant. There is no exception and
  no warning — just missing data, discovered three weeks later by
  somebody else.
- **Writing `if value != None`.** It works for ordinary values, but `!=`
  calls the object's `__ne__` method, which an object is allowed to
  redefine to say anything at all:

  ```text
  False True
  ```

  That is `w != None` and `w is not None` on the same object, disagreeing.
  `is not` asks the one question that cannot be overridden.
  [PEP 8](https://peps.python.org/pep-0008/) says comparisons to `None`
  always use `is` or `is not`.
- **Starting `merge_records` from the first record.**

  ```python
  def merge_records(*records):
      result = records[0]          # WRONG: this is an alias, not a copy
      for record in records[1:]:
          result.update(record)
      return result
  ```

  Two bugs in three lines. With no arguments it raises:

  ```text
  IndexError: tuple index out of range
  ```

  And when it does not raise, `result` *is* the caller's first dict, so
  merging rewrites it:

  ```text
  {'x': 2}
  {'x': 2}
  ```

  That is the merged result and then the caller's original, which used to
  say `1`. Starting from `{}` costs nothing and removes the whole class
  of bug.
- **Mixing up `*` and `**` at the call site.**

  ```python
  merge_records(**{"a": 1})      # WRONG
  ```

  ```text
  TypeError: merge_records() got an unexpected keyword argument 'a'
  ```

  `**` at a call site *unpacks* the dict into keyword arguments, and
  `merge_records` takes none. `merge_records({"a": 1})` passes the dict
  as one positional argument, which is what the signature wants.
- **Returning `fields` itself from `build_record`.** It happens to be a
  fresh dict that Python built for the call, so nothing breaks today. But
  the function's contract says "the pairs that are not `None`", and
  returning the unfiltered dict quietly keeps them. Build the new dict.
- **Annotating `_demo` as returning something.** It prints and returns
  nothing. `-> None` is the honest hint.

## Under the hood

<details>
<summary>Under the hood — one star, two stars, and which side of the function you are on</summary>

`*` and `**` mean opposite things depending on whether they appear in a
`def` line or in a call. That is the entire source of the confusion, and
it clears up the moment you see the four cases side by side.

**In a `def` line, the stars PACK.** Loose arguments get gathered into one
container.

```python
def show(*args, **kwargs) -> None:
    """Print whatever was packed into args and kwargs."""
    print(args, kwargs)


show(1, 2, a=3)
```

```text
(1, 2) {'a': 3}
```

`1` and `2` had no names, so they went into the tuple. `a=3` had a name,
so it went into the dict.

**At a call site, the stars UNPACK.** One container gets spread back out
into loose arguments.

```python
show(*[1, 2], **{"a": 3})
```

```text
(1, 2) {'a': 3}
```

Identical output. The list was spread into two positional arguments and
the dict into one keyword argument, and then the `def` line packed them
straight back up.

The four cases in one table:

| Where | Symbol | Does | Container |
|---|---|---|---|
| `def f(*args)` | `*` | packs positional arguments | tuple |
| `def f(**kwargs)` | `**` | packs keyword arguments | dict |
| `f(*items)` | `*` | unpacks a sequence into positions | any iterable |
| `f(**mapping)` | `**` | unpacks a mapping into keywords | any dict |

Two things worth knowing that follow from this.

**The names `args` and `kwargs` are convention, not syntax.** The stars do
the work. `def show(*things, **named)` is exactly as valid, and in a
function where the arguments mean something specific — `*records` here —
a real name reads better than `args`.

**Unpacking is how you forward arguments.** A wrapper that has to pass
everything along unchanged writes it once:

```python
def logged(func, *args, **kwargs):
    """Call func with whatever it was given, and say so."""
    print(f"calling {func.__name__}")
    return func(*args, **kwargs)
```

It packs on the way in and unpacks on the way out, so it works for any
function with any signature without knowing a thing about it. That is the
shape every decorator in Python is built on.

For `merge_records`, unpacking is also the answer to "what if my dicts are
already in a list":

```python
records = [{"a": 1}, {"b": 2}, {"a": 99}]
merge_records(*records)
```

The star spreads the list into three separate arguments, which is what the
signature is expecting. Without it you would be passing one argument that
happens to be a list, and `result.update(a_list)` is not the same thing at
all.

</details>

<details>
<summary>Under the hood — dicts remember their order, and that is newer than you think</summary>

The doctest in `build_record` says:

```text
>>> build_record(name="Amina", age=29, email=None)
{'name': 'Amina', 'age': 29}
```

`name` before `age`, every time. That only works because a dict keeps its
keys in the order they were first inserted, and that promise is more
recent than most of Python.

The history, briefly:

- Before **3.6**, dict order was genuinely arbitrary and could differ
  between two runs of the same program. Code that relied on it was
  broken, and printed dicts were a menace to test.
- In **3.6**, CPython got a new dict layout that used less memory and, as
  a side effect, happened to preserve insertion order. It was explicitly
  an implementation detail, and the release notes told people not to rely
  on it.
- In **3.7**, insertion order became part of the language specification.
  Every Python that calls itself Python 3.7 or later must do it.

So `{'name': 'Amina', 'age': 29}` is a promise now, not a coincidence.

Two consequences you will meet:

**`**kwargs` preserves the call site's order.** Python builds that dict in
the order the caller typed the arguments, so `build_record`'s output
mirrors its input. That is what makes its doctest stable.

**Merging order is visible.** `merge_records({"a": 1}, {"b": 2}, {"a": 99})`
gives `{'a': 99, 'b': 2}` — `a` first, even though the winning value came
from the last dict. `update` changes an existing key's *value* in place
and leaves its *position* alone. The key was inserted first, so it stays
first.

If a key is deleted and re-added, it goes to the end. Order is about
insertion, not about the key.

One more thing, since dict keys are on the table. A key has to be
**hashable** — usable as a lookup fingerprint — which means it has to be
immutable. Strings, numbers and tuples work. Lists do not:

```python
{[1, 2]: "nope"}
```

```text
TypeError: unhashable type: 'list'
```

`**kwargs` never runs into this, because its keys come from Python
identifiers and those are always strings.

</details>

## Acceptance checklist

- [ ] `python dict_builder.py` prints the four lines from **Expected
      output**, in that order.
- [ ] `build_record(name="Amina", age=29, email=None)` gives
      `{'name': 'Amina', 'age': 29}`.
- [ ] `build_record()` gives `{}`.
- [ ] `build_record(age=0, active=False, note="")` keeps all three keys.
- [ ] The filter is written `is not None`, not `if value` and not
      `!= None`.
- [ ] `merge_records({"a": 1}, {"b": 2}, {"a": 99})` gives
      `{'a': 99, 'b': 2}`.
- [ ] `merge_records()` gives `{}` and does not raise.
- [ ] After a merge, the caller's original dicts are unchanged.
- [ ] All three functions have type hints and a docstring.
- [ ] `python -m doctest dict_builder.py -v` ends with `Test passed.`
- [ ] Committed with a message like `Week 4 homework: dict builder`.

## Stretch

- **Add `drop_keys(record: dict, *keys: str) -> dict`.** Return a new dict
  without the named keys, leaving the original alone. Same discipline as
  `merge_records`: build a new thing. Then check that
  `drop_keys(r, "email")` on a record with no `email` is not an error —
  removing something that is not there should be quiet.
- **Let the caller choose what counts as empty.** Add a keyword-only
  parameter: `build_record(*, drop=(None,), **fields)`, keeping any value
  not in `drop`. Now `drop=(None, "")` also skips empty strings, and the
  default still does exactly what the brief asked. The bare `*` in the
  signature is what forces `drop` to be passed by name, so it can never be
  mistaken for a field.
- **Merge with `|` instead.** Python 3.9 added `a | b` for dicts, which
  merges with the same later-wins rule. `merge_records` becomes a
  `functools.reduce` over `|`, or a one-liner loop with `result = result |
  record`. Compare the two versions and decide which you would rather
  read at seven in the morning.
- **Merge nested dicts properly.** `merge_records({"a": {"x": 1}},
  {"a": {"y": 2}})` currently gives `{'a': {'y': 2}}` — the whole inner
  dict is replaced. Write `deep_merge` that recurses into a value when
  both sides are dicts. That is problem 4's recursion applied to a shape
  where the depth is small and the recursion is the right tool.
- **Count how many fields were dropped.** Return
  `tuple[dict[str, object], int]` — the record and the number of `None`s
  skipped. Then decide whether you actually like that signature, or
  whether a caller who wants the count should just compare lengths.

Next: [Homework Problem 6 — Importing From a Custom Module](./problem-06-importing-from-a-custom-module.md).
