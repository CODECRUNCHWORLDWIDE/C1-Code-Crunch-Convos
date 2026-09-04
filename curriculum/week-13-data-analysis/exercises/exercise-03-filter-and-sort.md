# Exercise 3 — Filter and Sort

> **Topic:** Boolean masks, combining conditions, and sorting by a column
> **Lecture:** [02 — Cleaning & Transforming Data](../lecture-notes/02-cleaning-and-transforming.md)
> **Difficulty:** Easy
> **Target time:** 25 minutes
> **Why this one:** filtering and sorting are the two operations you will
> perform more than all the others combined. They are also where beginners
> collect their first two scars: using `and` instead of `&`, and assigning to
> a filtered slice. Both scars are cheap here and expensive in a real report.

## The Brief

A community night school runs a beginner Python course on Tuesday and
Thursday evenings. Twelve learners finished the mid-term. The coordinator has
their scores and the number of minutes each person logged in the practice
tracker, and she wants three things before Monday: who passed, a ranked list
of the passers, and whether one session is outperforming the other.

Passing is 70 or above. That boundary matters — two learners scored exactly
70, and whether they appear in your results is the difference between a
correct report and an apology email. Read the requirement twice before you
type the comparison operator.

## Starter

Copy this into `exercise-03-filter-and-sort.py` in your practice repo.

```python
"""exercise-03-filter-and-sort.py — who passed, and in what order.

Filters a cohort DataFrame by score and produces a ranked pass list.
"""

import pandas as pd

PASSING_SCORE = 70

COHORT: dict[str, list] = {
    "learner": [
        "Amara", "Bo", "Chen", "Dalia", "Emeka", "Farrah",
        "Gustavo", "Hana", "Idris", "Jo", "Kiran", "Lena",
    ],
    "session": [
        "Tuesday", "Thursday", "Tuesday", "Thursday", "Tuesday", "Thursday",
        "Tuesday", "Thursday", "Tuesday", "Thursday", "Tuesday", "Thursday",
    ],
    "score":   [88, 64, 70, 95, 52, 79, 70, 91, 45, 83, 68, 76],
    "minutes": [240, 90, 150, 310, 60, 200, 175, 285, 45, 220, 130, 190],
}


def main() -> None:
    """Print the cohort, the passers, the ranking, and two means."""
    df = pd.DataFrame(COHORT)
    print("--- all rows ---")
    print(df)

    # TODO: build `passing` — every row whose score reaches PASSING_SCORE.
    #       End the expression with .copy() and read the constraint below
    #       for why.
    # print("--- passing ---")
    # print(passing)
    # print(f"Passed: {len(passing)} of {len(df)}")

    # TODO: build `ranked` — the passers sorted by score descending, with
    #       minutes as the tiebreaker, and a fresh 0..n index.

    # TODO: pull the first row of `ranked` with .iloc[0] and print
    #       "Top scorer: <name> with <score>".

    # TODO: build `tuesday_pass` — passing AND session == "Tuesday".
    #       Parenthesize each condition and join them with &.

    # TODO: print the mean score for everyone and for the passers,
    #       both to two decimal places.


if __name__ == "__main__":
    main()
```

## Requirements

1. Print the whole frame under `--- all rows ---`.
2. Build `passing` with a boolean mask on `score`. Print it under
   `--- passing ---`, then print `Passed: 8 of 12`.
3. Build `ranked` by sorting `passing` on `["score", "minutes"]`, both
   descending, then `.reset_index(drop=True)`. Print it under
   `--- ranked ---`.
4. Print `Top scorer: Dalia with 95`, reading the name and score out of
   `ranked.iloc[0]`.
5. Build `tuesday_pass` with two conditions joined by `&`. Print it under
   `--- Tuesday passers ---`.
6. Print `Mean score, all: 73.42` and `Mean score, passing: 81.50`, both
   formatted with `:.2f`.
7. Compare `PASSING_SCORE` with `>=`. A learner who scored exactly 70 passed.

## Constraints

- **Use `&`, not `and`, to combine masks — and parenthesize both sides.**
  `and` asks Python for the truth value of a twelve-element array, which is
  undefined, so it raises. `&` is the element-wise operator pandas overloads
  for exactly this job. The parentheses are not optional: `&` binds tighter
  than `==`, so `df["score"] >= 70 & df["session"] == "Tuesday"` parses as
  something you did not mean and fails with a confusing error.
- **End the filter with `.copy()`.** `df[mask]` may hand you a view onto the
  original frame. Assigning a new column to that view triggers
  `SettingWithCopyWarning` and may or may not affect `df` — pandas does not
  promise. `.copy()` makes it a new frame and ends the ambiguity for good.
  You do not add a column in this exercise, but the habit costs one method
  call and saves an afternoon.
- **Sort on two keys, not one.** Chen and Gustavo both scored 70.
  `sort_values("score")` uses quicksort by default, which is not stable, so
  the order of those two rows is whatever the algorithm happened to produce —
  it can differ between pandas versions. Naming `minutes` as the tiebreaker
  makes the output deterministic and defensible: the learner who practiced
  more ranks higher. Any time your sort key has ties, name the tiebreaker.
- **Call `reset_index(drop=True)` on `ranked`, and nowhere else.** After a
  filter, the index keeps the original row labels — that is why `passing`
  shows 0, 2, 3, 5, 6, 7, 9, 11. Those gaps are useful, because they let you
  trace a row back to the source. A published ranking is the one place you
  want 0 through 7 instead, and `drop=True` throws the old labels away rather
  than keeping them as a column.
- **Read the top scorer out of `ranked`, not out of `df`.** They agree here,
  but the whole point of building a ranked frame is that position 0 *is* the
  answer. Recomputing it with a second `max()` call gives you two sources of
  truth that can drift apart.

## Expected output

```text
$ python exercise-03-filter-and-sort.py
--- all rows ---
    learner   session  score  minutes
0     Amara   Tuesday     88      240
1        Bo  Thursday     64       90
2      Chen   Tuesday     70      150
3     Dalia  Thursday     95      310
4     Emeka   Tuesday     52       60
5    Farrah  Thursday     79      200
6   Gustavo   Tuesday     70      175
7      Hana  Thursday     91      285
8     Idris   Tuesday     45       45
9        Jo  Thursday     83      220
10    Kiran   Tuesday     68      130
11     Lena  Thursday     76      190
--- passing ---
    learner   session  score  minutes
0     Amara   Tuesday     88      240
2      Chen   Tuesday     70      150
3     Dalia  Thursday     95      310
5    Farrah  Thursday     79      200
6   Gustavo   Tuesday     70      175
7      Hana  Thursday     91      285
9        Jo  Thursday     83      220
11     Lena  Thursday     76      190
Passed: 8 of 12
--- ranked ---
   learner   session  score  minutes
0    Dalia  Thursday     95      310
1     Hana  Thursday     91      285
2    Amara   Tuesday     88      240
3       Jo  Thursday     83      220
4   Farrah  Thursday     79      200
5     Lena  Thursday     76      190
6  Gustavo   Tuesday     70      175
7     Chen   Tuesday     70      150
Top scorer: Dalia with 95
--- Tuesday passers ---
   learner  session  score  minutes
0    Amara  Tuesday     88      240
2     Chen  Tuesday     70      150
6  Gustavo  Tuesday     70      175
Mean score, all: 73.42
Mean score, passing: 81.50
```

Three details in that output punish the obvious wrong approach.

The `passing` frame has 8 rows. If you used `>` instead of `>=` you get 6,
because Chen and Gustavo drop out. Nothing in the code will tell you; the
report is simply wrong.

The index of `passing` skips 1, 4, 8, and 10. That is correct and expected —
those are Bo, Emeka, Idris, and Kiran, who did not pass. A filtered frame
keeps its original labels.

And in `ranked`, Gustavo sits above Chen despite the identical score, because
of the `minutes` tiebreaker. Without it the order is not guaranteed.

## Steps

1. Create the file, paste the starter, and run it. You should see the full
   twelve-row table.
2. Add the `passing` filter. Run it and count the rows before you trust the
   `Passed: 8 of 12` line.
3. Add the ranking. Run it once with `sort_values("score", ascending=False)`
   and once with the two-key version, and see whether Chen and Gustavo swap on
   your machine.
4. Add the top-scorer line. `ranked.iloc[0]` returns a Series, so
   `top["learner"]` reads one field out of it.
5. Add the Tuesday filter. Before you run it, deliberately write it with
   `and` instead of `&` and read the exception — you want to recognize that
   message instantly.
6. Add the two mean lines and run the whole file.
7. Change `PASSING_SCORE` to `76` and rerun. Six learners pass, down from
   eight — the two who scored exactly 70 drop out, and Lena's 76 stays in
   because the filter is `>=`. Change it back to 70.

## The Solution

```python
"""exercise-03-filter-and-sort.py — who passed, and in what order.

Filters a cohort DataFrame by score and produces a ranked pass list.
"""

import pandas as pd

PASSING_SCORE = 70

COHORT: dict[str, list] = {
    "learner": [
        "Amara", "Bo", "Chen", "Dalia", "Emeka", "Farrah",
        "Gustavo", "Hana", "Idris", "Jo", "Kiran", "Lena",
    ],
    "session": [
        "Tuesday", "Thursday", "Tuesday", "Thursday", "Tuesday", "Thursday",
        "Tuesday", "Thursday", "Tuesday", "Thursday", "Tuesday", "Thursday",
    ],
    "score":   [88, 64, 70, 95, 52, 79, 70, 91, 45, 83, 68, 76],
    "minutes": [240, 90, 150, 310, 60, 200, 175, 285, 45, 220, 130, 190],
}


def main() -> None:
    """Print the cohort, the passers, the ranking, and two means."""
    df = pd.DataFrame(COHORT)
    print("--- all rows ---")
    print(df)

    passing = df[df["score"] >= PASSING_SCORE].copy()
    print("--- passing ---")
    print(passing)
    print(f"Passed: {len(passing)} of {len(df)}")

    ranked = passing.sort_values(
        ["score", "minutes"], ascending=False
    ).reset_index(drop=True)
    print("--- ranked ---")
    print(ranked)

    top = ranked.iloc[0]
    print(f"Top scorer: {top['learner']} with {top['score']}")

    tuesday_pass = df[
        (df["score"] >= PASSING_SCORE) & (df["session"] == "Tuesday")
    ].copy()
    print("--- Tuesday passers ---")
    print(tuesday_pass)

    print(f"Mean score, all: {df['score'].mean():.2f}")
    print(f"Mean score, passing: {passing['score'].mean():.2f}")


if __name__ == "__main__":
    main()
```

**`>=` is a decision about people, and it is written down once.** The brief says
passing is "70 or above". Two learners scored exactly 70, so the operator is
worth two learners' results. Putting the threshold in `PASSING_SCORE` and
comparing with `>=` in both places it is needed means the boundary is defined
once. Changing the pass mark to 76 is then a one-character edit, not a hunt
through the file — and it is worth actually doing, because the count goes from
eight to six. (The exercise page's Step 7 says five; five is what strict `>`
would give. With the `>=` the brief requires, Lena's exactly-76 counts and the
answer is six.)

**`&`, not `and`, and parentheses around both sides.** `and` is a Python keyword
that calls `bool()` on its left operand, and a twelve-element Series has no
single truth value, so it raises. `&` is an operator pandas overloads to mean
"element-wise AND over two boolean Series". The parentheses are not style: `&`
binds *tighter* than `==` and `>=`, so `df["score"] >= 70 & df["session"] ==
"Tuesday"` groups as `df["score"] >= (70 & df["session"]) == "Tuesday"`, which is
a different program. Write every mask as `(this) & (that)` and the question never
comes up.

**`.copy()` ends an ambiguity rather than fixing a bug.** `df[mask]` may return a
view onto the original frame or a fresh frame; pandas does not promise which,
and the answer can depend on the dtypes and the memory layout. The consequence
only shows up when you assign to the result — you get
`SettingWithCopyWarning`, and whether `df` changes too is genuinely unpredictable.
This exercise never assigns to `passing`, so `.copy()` changes nothing today.
It costs one method call and it means the next person to add a column to
`passing` does not inherit a coin flip. Lecture 2, section 14 is the long version.

**Two sort keys, because the first one ties.** Chen and Gustavo both scored 70.
`sort_values` uses quicksort by default, which is not a stable sort, so the
relative order of tied rows is whatever the algorithm produced — it can differ
between pandas versions and even between runs on different data lengths. Naming
`minutes` as the tiebreaker makes the output deterministic *and* defensible:
Gustavo logged 175 minutes to Chen's 150, so Gustavo ranks higher, and you can
say why to the coordinator. The general rule: any time your sort key can tie,
name the tiebreaker. If you want stability without a second key,
`kind="mergesort"` gives it to you, but a stated tiebreaker is easier to defend
than "whatever order the input happened to be in".

**The index gaps in `passing` are a feature.** `passing` shows labels 0, 2, 3, 5,
6, 7, 9, 11 — the missing 1, 4, 8, and 10 are Bo, Emeka, Idris, and Kiran, who
did not pass. Those labels are a trail back to the source row, which is exactly
what you want when someone queries a number. `ranked` is the one place you throw
them away, because a published ranking wants to read 0 through 7, and
`drop=True` discards the old labels instead of parking them in a new `index`
column.

**`ranked.iloc[0]` is the answer, not a second opinion.** The whole reason to
build a ranked frame is that position 0 is now defined to be the top. Reading it
back with a separate `df["score"].max()` would give you two independent
calculations of "the winner" that can disagree the moment the tiebreak rule
changes. `.iloc[0]` returns that row as a Series, so `top["learner"]` and
`top["score"]` read fields out of it by column name.

## Run it

Copy the worked answer on this page into `exercise-03-filter-and-sort.py` and run it:

```bash
python exercise-03-filter-and-sort.py
```

It needs only pandas and prints the cohort, the passers, the ranking, and the two means. The `-solution` suffix keeps it from colliding with your own `exercise-03-filter-and-sort.py`.

## Common bugs to catch

- **`ValueError: The truth value of a Series is ambiguous. Use a.empty,
  a.bool(), a.item(), a.any() or a.all()`.** You joined two masks with `and`
  or `or`. Use `&` and `|`, and parenthesize each side.
- **`TypeError: unsupported operand type(s) for &: 'float' and 'bool'`** or a
  wildly wrong row count. You forgot the parentheses:
  `df["score"] >= 70 & df["session"] == "Tuesday"` evaluates
  `70 & df["session"]` first. Wrap each comparison:
  `(df["score"] >= 70) & (df["session"] == "Tuesday")`.
- **Six passers instead of eight.** You used `>` where the brief says 70 or
  above. Chen and Gustavo scored exactly 70.
- **`SettingWithCopyWarning: A value is trying to be set on a copy of a slice
  from a DataFrame`.** You assigned to a column of a filtered frame without
  `.copy()`. Either add `.copy()` at the filter, or write the assignment as
  `df.loc[mask, "column"] = value` on the original frame.
- **`KeyError: 0` when you try `ranked[0]` or `passing[0]`.** Single brackets
  on a DataFrame select a *column*, and there is no column named `0`. To get
  the first row use `ranked.iloc[0]`.
- **`KeyError: 0` even with `.loc`.** After a filter, label `0` may not exist —
  `passing.loc[0]` happens to work here because Amara passed, but
  `passing.loc[1]` raises, because Bo was filtered out. `.iloc[1]` always
  works: it counts positions, not labels.
- **The ranked list still shows the old index numbers.** You called
  `reset_index()` without `drop=True`, which moves the old labels into a new
  column called `index` instead of discarding them, or you forgot the call
  entirely.
- **`Mean score, all: 73.416666666666664`.** You printed the raw float. Use
  `:.2f` inside the f-string.

## Under the hood

<details>
<summary>Under the hood — copy, view, and the warning that predicts a bug</summary>

`df[mask]` may hand back a **view** onto the original frame or a brand-new
**copy**, and pandas does not promise which — the answer can depend on the
column dtypes and the memory layout. While you only ever *read* the result, the
difference is invisible. The moment you *assign* to it, it stops being
invisible: you get `SettingWithCopyWarning`, and whether the write also lands in
the original `df` becomes a coin flip you cannot see.

`passing = df[df["score"] >= PASSING_SCORE].copy()` ends the ambiguity by asking
for a guaranteed independent frame. It costs one method call and changes nothing
about today's output, because this exercise never assigns to `passing`. It means
the next person to add a column to `passing` does not inherit a bug that only
shows up on some pandas versions and some machines.

The gaps in `passing`'s index — labels 0, 2, 3, 5, 6, 7, 9, 11 — are the other
half of the same idea. A filter keeps the original row labels, so a label is a
receipt pointing back at the source row. `ranked` throws them away with
`reset_index(drop=True)` only because a published ranking wants to read 0
through 7; without `drop=True` the old labels move into a new `index` column
instead of being discarded.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and no warnings.
- [ ] `Passed: 8 of 12`, and Chen and Gustavo are both in the list.
- [ ] The `passing` frame still shows its original index labels, with gaps.
- [ ] `ranked` is indexed 0 through 7 and Gustavo appears above Chen.
- [ ] Both means print to exactly two decimal places.
- [ ] Every mask uses `&` with parentheses around each condition.
- [ ] The file is committed to Git with a message like
      `Add Week 13 exercise 3: filter and sort`.

## Stretch

- Rewrite the Tuesday filter using `df.query("score >= 70 and session ==
  'Tuesday'")` and confirm you get the same three rows. Inside `query`, `and`
  is correct — it is a string that pandas parses, not Python boolean logic.
  Decide which form you find easier to read six months from now.
- Add a `passed` boolean column with `df["passed"] = df["score"] >=
  PASSING_SCORE`, then compare `df["passed"].sum()` to `len(passing)`. Summing
  a boolean column counts the `True` values, an idiom you will use constantly.
- Use `df.nlargest(3, "score")` and compare it to
  `df.sort_values("score", ascending=False).head(3)`. Same answer, and on a
  large frame `nlargest` is much faster because it never sorts the rest.
- Answer the coordinator's third question: use `~(df["session"] == "Tuesday")`
  to get the Thursday rows and compare the two session means. Which evening is
  ahead, and by how much?

When your ranking is deterministic, move on to
[Exercise 4 — Groupby](./exercise-04-groupby.md).
