# Lecture 02 — CSV and JSON

> **Read time:** ~25 min. **Type-along time:** ~45 min. Have your REPL open and a scratch directory ready.

Plain text is great for prose, but most of the data you will work with as a developer is **structured**. Two formats dominate:

- **CSV** (Comma-Separated Values) — tabular, row/column data. Excel exports, database dumps, scientific data.
- **JSON** (JavaScript Object Notation) — nested key/value data. API responses, config files, document stores.

Python's standard library ships excellent modules for both. You will use them constantly.

---

## 1. CSV — the format

CSV looks like this:

```
name,age,city
Alice,30,Boston
Bob,25,Seattle
"Chen, Lin",42,"New York"
```

A CSV file is a sequence of **records** (rows). Each record is a sequence of **fields** (columns), separated by a **delimiter** (usually `,`). Fields that contain the delimiter, a newline, or a quote character are wrapped in **quotes** (usually `"`). A `"` inside a quoted field is escaped by doubling it: `""`.

That sounds simple, and most of the time it is. But CSV is not really one format — it is a family of slightly-incompatible conventions. Different programs use different delimiters (`,`, `;`, `\t`), different quote characters, and different rules for line endings (`\n` vs `\r\n`). This is why we never try to parse CSV with `.split(",")` — use the `csv` module.

---

## 2. The `csv` module — `reader` and `writer`

The lowest-level interface treats rows as **lists** of strings.

### Reading

```python
import csv
from pathlib import Path

with Path("students.csv").open("r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)              # first row is the header
    for row in reader:
        print(row)                     # ['Alice', '30', 'Boston']
```

A few things to notice:

- We pass `newline=""` when opening the file. The `csv` module handles its own line-ending logic; if you let Python translate newlines for you it can split rows incorrectly. **Always pass `newline=""` to `open()` when using `csv`.**
- Every field comes back as a `str`. Even `30` is the string `"30"`. If you want an integer, convert it: `int(row[1])`.
- `csv.reader` is an iterator — it reads lazily, one row at a time.

### Writing

```python
import csv
from pathlib import Path

rows = [
    ["name", "age", "city"],
    ["Alice", 30, "Boston"],
    ["Bob", 25, "Seattle"],
]

with Path("out.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
```

`writer.writerow(row)` writes a single row; `writer.writerows(rows)` writes many. The module handles quoting for you — if a field contains a comma, it will be wrapped in quotes automatically.

### Delimiters and dialects

If your file uses `;` (common in European locales) or `\t` (tab-separated values, TSV):

```python
reader = csv.reader(f, delimiter=";")
reader = csv.reader(f, delimiter="\t")
```

For more complex configurations you can register a **dialect**:

```python
csv.register_dialect("excel_eu", delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
reader = csv.reader(f, dialect="excel_eu")
```

`csv.QUOTE_MINIMAL` (the default) quotes only fields that need it. `csv.QUOTE_ALL` quotes every field. `csv.QUOTE_NONNUMERIC` quotes everything that is not a number (and converts unquoted fields to `float` when reading — useful but surprising).

---

## 3. `DictReader` and `DictWriter` — rows as dicts

For files with a header row, working with **dicts** is almost always cleaner than working with lists. You refer to columns by name (`row["age"]`) instead of by index (`row[1]`), and your code does not break when someone reorders columns.

### `DictReader`

```python
import csv
from pathlib import Path

with Path("students.csv").open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"], row["city"])
```

`DictReader` reads the first row as the header automatically. Each subsequent row is yielded as a `dict[str, str]`. You can override the field names with `fieldnames=` if the file has no header.

### `DictWriter`

```python
import csv
from pathlib import Path

rows = [
    {"name": "Alice", "age": 30, "city": "Boston"},
    {"name": "Bob", "age": 25, "city": "Seattle"},
]

with Path("out.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows(rows)
```

`fieldnames` is **required** — it determines column order. `writeheader()` writes the header row. If a dict is missing a key, you get `ValueError` by default; pass `extrasaction="ignore"` to silently drop extras, or `restval=""` to fill missings.

### A typical filter-and-write pattern

```python
import csv
from pathlib import Path

INPUT = Path("students.csv")
OUTPUT = Path("passing.csv")

with INPUT.open("r", encoding="utf-8", newline="") as src, \
     OUTPUT.open("w", encoding="utf-8", newline="") as dst:
    reader = csv.DictReader(src)
    writer = csv.DictWriter(dst, fieldnames=reader.fieldnames or [])
    writer.writeheader()
    for row in reader:
        if int(row["grade"]) >= 70:
            writer.writerow(row)
```

You will write this exact shape of code dozens of times in your career.

Full reference: [`csv` module docs](https://docs.python.org/3/library/csv.html).

---

## 4. JSON — the format

JSON looks like this:

```json
{
  "name": "Alice",
  "age": 30,
  "tags": ["python", "beginner"],
  "active": true,
  "manager": null
}
```

It maps almost directly to Python data structures:

| JSON | Python |
|---|---|
| object `{...}` | `dict` |
| array `[...]` | `list` |
| string | `str` |
| number (int) | `int` |
| number (float) | `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Two notable mismatches:

- JSON **object keys must be strings**. Python dicts can use any hashable key, but if you serialize a `dict` with non-string keys, the `json` module converts them (ints become strings) or refuses (`TypeError` for tuples).
- JSON has **no date/time type**. You have to encode dates as strings yourself (see section 7).

---

## 5. The `json` module — four functions you need

The `json` module has four core functions. The `s` suffix means "string"; no `s` means "file".

| Function | Input | Output |
|---|---|---|
| `json.loads(s)` | `str` | Python object |
| `json.dumps(obj)` | Python object | `str` |
| `json.load(f)` | file-like (read) | Python object |
| `json.dump(obj, f)` | Python object, file-like (write) | `None` (writes to file) |

### From a string

```python
import json

raw = '{"name": "Alice", "age": 30}'
data = json.loads(raw)
print(data["name"])    # Alice

back = json.dumps(data)
print(back)            # {"name": "Alice", "age": 30}
```

### From a file

```python
import json
from pathlib import Path

with Path("config.json").open("r", encoding="utf-8") as f:
    config = json.load(f)

config["debug"] = True

with Path("config.json").open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
```

That snippet — load, mutate, dump back — is the basic "edit a JSON config" pattern. You will recognize it from Exercise 03.

---

## 6. Pretty-printing — `indent` and `sort_keys`

By default `json.dumps` produces a single line with no spaces:

```python
>>> json.dumps({"b": 2, "a": 1})
'{"b": 2, "a": 1}'
```

That is the right default for machine-to-machine APIs (it is compact). For files humans will read, pass `indent=2` (or `4`):

```python
>>> print(json.dumps({"b": 2, "a": 1, "nested": [1, 2, 3]}, indent=2))
{
  "b": 2,
  "a": 1,
  "nested": [
    1,
    2,
    3
  ]
}
```

`sort_keys=True` produces deterministic output (alphabetical key order), which is great for files you check into git — diffs become readable:

```python
>>> print(json.dumps({"b": 2, "a": 1}, indent=2, sort_keys=True))
{
  "a": 1,
  "b": 2
}
```

For configs and snapshots, I recommend `indent=2, sort_keys=True` as your default.

---

## 7. Datetime — the most common gotcha

JSON has no native date type, so `datetime` objects do not serialize directly:

```python
>>> import json, datetime
>>> json.dumps({"when": datetime.datetime.now()})
TypeError: Object of type datetime is not JSON serializable
```

You have three options.

### Option A — convert to ISO 8601 strings yourself

ISO 8601 is the universally recognized format (`"2026-05-13T14:30:00"`). The `.isoformat()` method on a `datetime` produces it.

```python
import json, datetime

event = {"name": "launch", "when": datetime.datetime.now().isoformat()}
print(json.dumps(event, indent=2))
```

To read it back: `datetime.datetime.fromisoformat(s)`.

### Option B — pass a `default=` function

`json.dumps(obj, default=...)` calls your function for objects it doesn't know how to serialize.

```python
import json, datetime

def encode_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Cannot serialize {type(obj).__name__}")

event = {"name": "launch", "when": datetime.datetime.now()}
print(json.dumps(event, default=encode_default, indent=2))
```

### Option C — subclass `json.JSONEncoder`

Heavier-weight version of Option B. You will see it in larger projects.

```python
import json, datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

print(json.dumps({"when": datetime.datetime.now()}, cls=DateTimeEncoder))
```

**Beginner advice:** stick with Option A — convert to strings before passing to `json.dumps`. It is the easiest to read and debug.

---

## 8. JSON errors

The main error you will see is `json.JSONDecodeError` (a subclass of `ValueError`). It comes with `.lineno`, `.colno`, and `.pos` attributes that tell you where the parser choked.

```python
import json

bad = '{"name": "Alice",}'   # trailing comma — not valid JSON!
try:
    json.loads(bad)
except json.JSONDecodeError as e:
    print(f"Bad JSON at line {e.lineno} column {e.colno}: {e.msg}")
```

Common mistakes that produce `JSONDecodeError`:

- **Trailing commas** — `[1, 2, 3,]` is invalid JSON (though valid Python).
- **Single quotes** — JSON requires double quotes around strings.
- **Comments** — JSON has no comments. (For configs, consider TOML or JSONC instead.)
- **Unquoted keys** — `{name: "Alice"}` is invalid; must be `{"name": "Alice"}`.

If you are debugging a malformed JSON file, paste it into [JSONLint](https://jsonlint.com/) — it will point you straight at the problem.

---

## 9. A worked example — student grades

We will read a CSV of students, compute average grade per class, and write the result as JSON.

```python
import csv
import json
import statistics
from pathlib import Path
from collections import defaultdict

INPUT = Path("grades.csv")
OUTPUT = Path("class-averages.json")

def class_averages(path: Path) -> dict[str, float]:
    by_class: dict[str, list[float]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            by_class[row["class"]].append(float(row["grade"]))
    return {cls: round(statistics.mean(grades), 2) for cls, grades in by_class.items()}

if __name__ == "__main__":
    averages = class_averages(INPUT)
    OUTPUT.write_text(json.dumps(averages, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {len(averages)} class averages to {OUTPUT}")
```

Notes:

- We use `csv.DictReader` to access columns by name.
- `float(row["grade"])` does the string-to-number conversion explicitly.
- We use `pathlib.Path.write_text` (the shortcut) for the small JSON output.
- The `dict` comprehension at the end is from Week 5 — comprehensions and file I/O are a beautiful combination.

---

## 10. When **not** to use CSV or JSON

A quick reality check:

- **CSV** is fine for tabular data **up to a few million rows**. Beyond that you want a real database (Week 10) or a columnar format like Parquet.
- **JSON** is fine for **structured data up to a few megabytes**. Beyond that, look at JSON Lines (one JSON object per line — perfect for streaming) or Protocol Buffers.
- **Neither** is ideal for binary data. If you need to store images or audio, store them on disk and put **paths** in your JSON/CSV.

You will see all of these in later weeks. For now, CSV and JSON cover 90% of beginner data work.

---

## What's next

Reading and writing data is half the job. The other half is **handling failure** — what happens when the file is missing, the CSV has a malformed row, or the JSON is corrupted? That is the next lecture.

Continue to [`03-exceptions-and-logging.md`](./03-exceptions-and-logging.md).
