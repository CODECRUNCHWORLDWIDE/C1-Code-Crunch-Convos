# Week 5 — Data Structures & Comprehensions

Welcome to Week 5 of **Code Crunch Convos**, our open-source Python bootcamp. This is the week the language stops feeling like a calculator and starts feeling like a toolkit. You will learn the four built-in container types that almost every real Python program is built from — **lists, tuples, sets, and dictionaries** — and how to write idiomatic, Pythonic code with **comprehensions**.

By the end of this week you will be able to model real-world data (contacts, inventories, word counts, student rosters) and pick the right structure for the job.

---

## Learning objectives

By the end of Week 5 you will be able to:

1. Create, index, slice, and mutate **lists** using the full set of common methods (`append`, `extend`, `insert`, `pop`, `remove`, `sort`, `reverse`).
2. Explain **mutability** and **aliasing**, and use `list.copy()` and `copy.deepcopy()` correctly.
3. Use **tuples** for fixed records, unpack them, and create lightweight types with `collections.namedtuple`.
4. Use **sets** for uniqueness and fast membership testing, and apply set operations (`|`, `&`, `-`, `^`).
5. Use **dictionaries** for key/value lookup, choosing between `d[key]`, `d.get()`, and `d.setdefault()` appropriately.
6. Read and write **nested data structures** (lists of dicts, dicts of lists, dicts of dicts).
7. Write **list, dict, and set comprehensions**, including conditional forms.
8. Understand **generator expressions** at a preview level.
9. Reason about **Big-O** trade-offs: why `x in some_set` is O(1) but `x in some_list` is O(n).
10. Build a small CRUD application (a contact book) that persists to disk as JSON.

---

## Prerequisites

You should be comfortable with everything from Weeks 1–4:

- **Week 1** — Python installation, the REPL, running `.py` files.
- **Week 2** — Primitive types (`int`, `float`, `str`, `bool`) and operators.
- **Week 3** — `if`/`elif`/`else`, `for`, `while`, `break`/`continue`.
- **Week 4** — Defining functions, parameters, return values, importing modules, basic type hints.

If any of those feel shaky, take an hour to revisit them before tackling this week's comprehensions — they will be much harder otherwise.

---

## Topics

| # | Topic | Where |
|---|---|---|
| 1 | Lists — creation, indexing, slicing, methods | `lecture-notes/01-lists-and-tuples.md` |
| 2 | Mutability and aliasing | `lecture-notes/01-lists-and-tuples.md` |
| 3 | Tuples and `namedtuple` | `lecture-notes/01-lists-and-tuples.md` |
| 4 | Sets and set operations | `lecture-notes/02-sets-and-dicts.md` |
| 5 | Dictionaries and common patterns | `lecture-notes/02-sets-and-dicts.md` |
| 6 | Nested data structures | `lecture-notes/02-sets-and-dicts.md` |
| 7 | List/dict/set comprehensions | `lecture-notes/03-comprehensions-and-big-o.md` |
| 8 | Generator expressions (preview) | `lecture-notes/03-comprehensions-and-big-o.md` |
| 9 | Big-O intuition and choosing the right structure | `lecture-notes/03-comprehensions-and-big-o.md` |

---

## Suggested schedule (~36 hours)

This is a self-paced suggestion. Most learners spend **30–40 hours** on this week.

| Block | Hours | Activity |
|---|---|---|
| Day 1 | 4 | Read `01-lists-and-tuples.md`, type along in REPL |
| Day 1 | 2 | Exercise 01 (list operations) |
| Day 2 | 4 | Read `02-sets-and-dicts.md`, type along |
| Day 2 | 3 | Exercises 02–04 (dedupe, word frequency, sets) |
| Day 3 | 4 | Read `03-comprehensions-and-big-o.md` |
| Day 3 | 3 | Exercise 05 (convert loops to comprehensions) |
| Day 4 | 4 | Challenge 01 (anagram groups) |
| Day 4 | 3 | Challenge 02 (inventory tracker) |
| Day 5 | 6 | Mini-project: contact book manager |
| Day 6 | 2 | Homework problems |
| Day 6 | 1 | Quiz + reflection |

Total: **~36 hours**.

---

## Navigation

- **Lecture notes** — `lecture-notes/01-lists-and-tuples.md` → `02-sets-and-dicts.md` → `03-comprehensions-and-big-o.md`
- **Exercises** — `exercises/README.md` (start small, finish all five)
- **Challenges** — `challenges/README.md` (harder, open-ended)
- **Quiz** — `quiz.md` (10 multiple-choice questions, self-graded)
- **Homework** — `homework.md` (6 problems, due before Week 6)
- **Mini-project** — `mini-project/README.md` (the capstone for this week)
- **Resources** — `resources.md` (official docs, articles, references)

---

## Stretch goals

If you finish early and want to push further:

1. **`collections` deep dive** — learn `defaultdict`, `Counter`, `deque`, `OrderedDict` from the [collections module docs](https://docs.python.org/3/library/collections.html). Rewrite Exercise 03 using `Counter`.
2. **Dataclasses preview** — read [PEP 557](https://peps.python.org/pep-0557/) and rewrite the contact book using `@dataclass` instead of dicts (you will revisit this in Week 7).
3. **Profile your code** — use `timeit` to compare `x in big_list` vs `x in big_set` for `len = 100_000`. Confirm the Big-O claims yourself.
4. **CSV export** — extend the contact book to also export to CSV using `csv.DictWriter` (preview of Week 6 file I/O).
5. **Type stubs** — add full `typing.TypedDict` annotations to the contact book.

---

## Up next

Once you finish this week, head to **[Week 6 — File I/O & Exceptions](../week-06-file-io-exceptions/)**. You already touched JSON files in the mini-project; next week we go deep on reading/writing text, CSV, and JSON files, plus handling errors with `try`/`except`.

---

## Submission checklist

Before marking this week complete:

- [ ] Read all three lecture notes
- [ ] Completed exercises 01–05 (working code, runs without error)
- [ ] Attempted both challenges (write-up in markdown)
- [ ] Passed the quiz (8/10 or higher; retake until you do)
- [ ] Submitted homework problems
- [ ] Mini-project runs end-to-end with JSON persistence
- [ ] Pushed everything to your fork of the bootcamp repo

Happy crunching!
