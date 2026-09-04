# Homework 3 — Merge two DataFrames

> **Topic:** `merge(how="left")`, the `indicator` column, filling what the join missed, and `to_csv`
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** real data never arrives in one table. Orders live in one
> place and customers in another, and joining them is the most common single
> operation in all of data work. It is also where rows disappear without a
> sound. This problem plants one order with a customer who does not exist, so
> you find out now rather than in a report somebody is reading.

## The Brief

You have two lists. One is a stack of order slips: an order number, a customer
number, and an amount. The other is the customer address book: customer number,
name, country.

Neither list is any use alone. The order slip says customer 2 spent 75, and
that means nothing until the address book tells you customer 2 is Linus in
Finland. Sticking them together on the shared customer number is a **join**,
and the number they share — `customer_id` — is the **key**.

There is a catch, planted on purpose. Order 105 was placed by customer 99, and
customer 99 is not in the address book. Somebody typed it wrong, or the address
book export is stale. Whatever the reason, that order exists and it cannot be
allowed to vanish just because its customer cannot be found.

So the join must be a **left join**: keep every order, matched or not, and
leave the customer details blank where there is nobody to look up. Then count
the blanks, say so out loud, fill them with the literal word `"UNKNOWN"`, and
save the result.

Here are the two frames, exactly as you will build them:

```python
orders = pd.DataFrame({
    "order_id":    [101, 102, 103, 104, 105],
    "customer_id": [1, 2, 1, 3, 99],
    "amount":      [50.0, 75.0, 20.0, 120.0, 9.0],
})

customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "name":        ["Ada", "Linus", "Grace", "Tim"],
    "country":     ["UK", "FI", "US", "GB"],
})
```

Note that customer 4, Tim, has never ordered anything. A left join from orders
drops him, and that is correct — you were asked about orders, not customers.

## Starter

Copy this into `problem-03-merge-dataframes.py` in your homework folder.

```python
"""problem-03-merge-dataframes.py — left-join orders to customers.

Keeps every order, reports the ones with no matching customer, fills the gaps
with "UNKNOWN", and writes merged.csv.
"""

from __future__ import annotations

import pandas as pd


def build_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    """The two frames exactly as the homework specifies them."""
    orders = pd.DataFrame({
        "order_id":    [101, 102, 103, 104, 105],
        "customer_id": [1, 2, 1, 3, 99],
        "amount":      [50.0, 75.0, 20.0, 120.0, 9.0],
    })
    customers = pd.DataFrame({
        "customer_id": [1, 2, 3, 4],
        "name":        ["Ada", "Linus", "Grace", "Tim"],
        "country":     ["UK", "FI", "US", "GB"],
    })
    return orders, customers


def main() -> None:
    orders, customers = build_frames()

    # TODO 1: left join. orders.merge(customers, on=..., how=..., indicator=True)
    #         Print it with .to_string(index=False).

    # TODO 2: the rows the join could not match have _merge == "left_only".
    #         Count them and print the count, then print those rows.

    # TODO 3: drop the _merge column, then fillna("UNKNOWN") on name and
    #         country only. Print the filled frame.

    # TODO 4: write it out with to_csv("merged.csv", index=False).


if __name__ == "__main__":
    main()
```

It runs as pasted, builds both frames, and prints nothing. Work down the TODOs
in order, running after each one.

## Requirements

1. Perform a **left join** of `orders` onto `customers` on `customer_id`, so
   every one of the five orders survives.
2. Print how many orders failed to match a customer, and which ones.
3. Fill the missing `name` and `country` with the literal string
   `"UNKNOWN"`.
4. Save the merged frame as `merged.csv`, with no index column.
5. Show that nothing is missing afterwards.
6. Top-of-file docstring, typed function signatures, no hard-coded path
   outside your homework folder.

## Constraints

- **`how="left"` is not the default, so say it.** The default is
  `how="inner"`, which keeps only rows that matched on both sides — and that
  would silently throw order 105 away. The whole point of the problem is the
  order that does not match. Type the `how`.
- **Join `orders.merge(customers, ...)`, in that order.** "Left" means the
  frame on the left of the dot. Write `customers.merge(orders, how="left")`
  and you keep every *customer* instead, including Tim who has never ordered,
  and you lose order 105. Same word, opposite result.
- **Use `indicator=True` rather than hunting for `NaN`.** It adds a `_merge`
  column saying `both` or `left_only` for every row. Detecting misses by
  looking for a missing `name` works right up until a customer genuinely has no
  name recorded — then a real customer looks like a failed join. The indicator
  answers the question you actually asked: did this row find a match?
- **Drop `_merge` before saving.** It is scaffolding for the report, not data.
  Ship it in the CSV and the next person to read the file has to work out
  whether it means something.
- **Fill only `name` and `country`.** A blanket `merged.fillna("UNKNOWN")`
  would put the word `UNKNOWN` into `amount` too the day an amount goes
  missing, turning a number column into text and breaking every sum
  downstream. Name the columns you mean.
- **`index=False` when you write the CSV.** Without it pandas writes its row
  numbers as a first, nameless column. Read that file back and you get a stray
  `Unnamed: 0` column, and this is the single most common piece of grit in
  shared CSVs.

## Expected output

The shipped answer,
[`problem-03-merge-dataframes-solution.py`](./problem-03-merge-dataframes-solution.py),
does exactly the four steps and then writes `merged.csv` into a throwaway
temporary folder, prints the file's contents back, and lets Python delete the
folder on the way out — so running the download does not scatter files into
whatever directory you happened to be in. Your own version writes `merged.csv`
beside your script, as requirement 4 asks. Real captured run:

```text
$ python problem-03-merge-dataframes.py
After the left join:
 order_id  customer_id  amount  name country    _merge
      101            1    50.0   Ada      UK      both
      102            2    75.0 Linus      FI      both
      103            1    20.0   Ada      UK      both
      104            3   120.0 Grace      US      both
      105           99     9.0   NaN     NaN left_only

Orders with no matching customer: 1
 order_id  customer_id  amount
      105           99     9.0

After filling:
 order_id  customer_id  amount    name country
      101            1    50.0     Ada      UK
      102            2    75.0   Linus      FI
      103            1    20.0     Ada      UK
      104            3   120.0   Grace      US
      105           99     9.0 UNKNOWN UNKNOWN

Remaining missing values: 0

wrote merged.csv
order_id,customer_id,amount,name,country
101,1,50.0,Ada,UK
102,2,75.0,Linus,FI
103,1,20.0,Ada,UK
104,3,120.0,Grace,US
105,99,9.0,UNKNOWN,UNKNOWN
```

Read the first table carefully. Order 105 is still there, which is the left
join doing its job, and its `name` and `country` are `NaN` — the blank that
means "no value here". The `_merge` column marks it `left_only`: present on the
left, absent on the right. Every other row says `both`. Tim never appears
anywhere, because he placed no orders.

## Steps

1. Paste the starter and run it. Two frames built, nothing printed.
2. Do TODO 1 with `how="inner"` first, on purpose, and count the rows. Four.
   Now switch to `how="left"` and count again. Five. That difference is the
   entire lesson; do not skip it.
3. Add `indicator=True` and look at the `_merge` column.
4. Do TODO 2. `merged["_merge"].eq("left_only")` gives you a True/False mask,
   `.sum()` counts it, and `merged.loc[mask, [...]]` shows you the rows.
5. Do TODO 3. Drop `_merge`, then fill the two columns. Confirm with
   `merged.isna().sum().sum()` that the total number of holes is 0.
6. Do TODO 4 and open `merged.csv` in a text editor. Five data rows, one
   header, no leading index column.
7. Change customer 99 in `orders` to customer 3 and rerun. The unmatched count
   drops to zero and nothing else in your code has to change.

## The Solution

```python
"""hw-03-merge.py — left-join orders to customers, report and fill the misses.

The merged table is written to a throwaway temporary directory that Python
deletes on the way out, then printed, so the script leaves nothing behind.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd


def build_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    """The two frames exactly as the homework specifies them."""
    orders = pd.DataFrame({
        "order_id":    [101, 102, 103, 104, 105],
        "customer_id": [1, 2, 1, 3, 99],
        "amount":      [50.0, 75.0, 20.0, 120.0, 9.0],
    })
    customers = pd.DataFrame({
        "customer_id": [1, 2, 3, 4],
        "name":        ["Ada", "Linus", "Grace", "Tim"],
        "country":     ["UK", "FI", "US", "GB"],
    })
    return orders, customers


def main() -> None:
    orders, customers = build_frames()

    # 1. Left join: every order survives, matched or not.
    merged = orders.merge(customers, on="customer_id", how="left", indicator=True)
    print("After the left join:")
    print(merged.to_string(index=False))

    # 2. How many orders failed to match a customer?
    unmatched = merged["_merge"].eq("left_only")
    print(f"\nOrders with no matching customer: {unmatched.sum()}")
    print(merged.loc[unmatched, ["order_id", "customer_id", "amount"]]
                .to_string(index=False))

    # 3. Fill the gaps left by the join.
    merged = merged.drop(columns="_merge")
    merged[["name", "country"]] = merged[["name", "country"]].fillna("UNKNOWN")
    print("\nAfter filling:")
    print(merged.to_string(index=False))
    print("\nRemaining missing values:", int(merged.isna().sum().sum()))

    # 4. Save to a temp dir, print it back, and let it be cleaned up.
    with tempfile.TemporaryDirectory() as workspace:
        out = Path(workspace) / "merged.csv"
        merged.to_csv(out, index=False)
        print(f"\nwrote {out.name}")
        print(out.read_text().rstrip())


if __name__ == "__main__":
    main()
```

**`how="left"` means "keep everything on the left, whatever happens".** The
frame on the left of the dot — `orders` — sets the rows. Every order comes
through. Where `customers` has a matching `customer_id`, its `name` and
`country` ride along; where it does not, pandas fills those two cells with
`NaN` and moves on. Order 105 survives with holes rather than being deleted,
and holes are something you can see and count. A deleted row is not.

**`indicator=True` adds a `_merge` column that says where each row came
from.** It holds `both` when the key matched on both sides and `left_only` when
it matched only on the left. `merged["_merge"].eq("left_only")` turns that into
a mask of True and False, `.sum()` counts the Trues — one — and
`merged.loc[unmatched, [...]]` prints the offending row so the report names the
order rather than just counting it. Testing for a missing `name` instead would
give the same answer today and the wrong answer the first time a real customer
has a blank name.

**The count and the rows come from the same mask.** `unmatched` is computed
once and used twice: once for `.sum()` and once for `.loc`. A count that
disagreed with the list under it would be a small disaster in a report, and
computing them separately is how that happens.

**Filling names two columns at a time keeps `amount` a number.**
`merged[["name", "country"]] = merged[["name", "country"]].fillna("UNKNOWN")`
selects the two text columns, fills them, and assigns the result straight back
into those same two columns. `merged.fillna("UNKNOWN")` would work identically
*today*, because those are the only holes — and would quietly poison the
`amount` column the day an amount is missing, since a column holding one string
stops being numeric and every `sum` after it fails or, worse, concatenates.

**`_merge` is dropped before the fill and before the save.** It was a
diagnostic. `merged.drop(columns="_merge")` returns a new frame without it,
which is then reassigned to `merged`. What lands in the CSV is the five columns
the brief asked for.

**`merged.isna().sum().sum()` is the double-check, and the two `.sum()`s are
not a typo.** The first collapses the True/False grid down each column into a
per-column count; the second adds those counts into one number. Zero means the
frame has no holes left anywhere. `int(...)` around it prints `0` instead of
NumPy's `0`.

**The output goes to a temporary folder so the download is polite.**
`tempfile.TemporaryDirectory()` used as a `with` block creates a real folder,
hands you its path, and deletes it — and everything in it — when the block
ends. The file is genuinely written and genuinely read back with
`out.read_text()`, so `to_csv` is really being exercised; it just does not
leave a `merged.csv` in your home directory. Your own homework file should
write `merged.csv` next to itself, because you *want* to keep that one.

## Run it

Copy the worked answer on this page into `problem-03-merge-dataframes.py` and run it:

```bash
python -m pip install pandas
python problem-03-merge-dataframes.py
```

It needs only pandas, builds both frames itself, and writes its CSV into a
temporary folder it cleans up, so it runs anywhere and leaves nothing behind.
The `-solution` suffix keeps it from colliding with your own
`problem-03-merge-dataframes.py`. Its docstring still carries the older
`hw-03-` filename from the original brief; the code is unchanged.

## Common bugs to catch

- **Four rows instead of five.** You got the default `how="inner"`. Order 105
  was dropped because customer 99 does not exist. Add `how="left"`.
- **Six rows instead of five.** You kept Tim, so you ran the join the other way
  round or used `how="outer"`. Left means the frame before the dot.
- **`MergeError: No common columns to perform merge on`.** The key column is
  spelled differently on the two sides. Either rename one, or use
  `left_on="cust_id", right_on="customer_id"`.
- **`ValueError: You are trying to merge on int64 and object columns`.** One
  frame loaded `customer_id` as text — usually from a CSV where one value was
  blank or had a stray space. Cast first:
  `df["customer_id"] = df["customer_id"].astype(int)`.
- **Columns named `amount_x` and `amount_y`.** Both frames had a column with
  the same name that was not the key, so pandas disambiguated them. Decide
  which one you want, or pass `suffixes=("_order", "_customer")` to say what
  they should be called.
- **More rows out than you had orders.** The key is duplicated on the *right*
  side — two rows for customer 1 in the address book — so every matching order
  is duplicated too. Check with
  `customers["customer_id"].duplicated().any()` before you join.
- **`amount` becomes text after filling.** You called `fillna("UNKNOWN")` on
  the whole frame. Fill only the columns that hold words.
- **`merged.csv` has an extra unnamed first column.** You left out
  `index=False`.
- **`FutureWarning` about downcasting on the fill.** Fill by assigning the
  result back, as the answer does, rather than using `inplace=True` — which
  pandas is retiring across the board.

## Under the hood

<details>
<summary>Under the hood — the four joins, and what each one throws away</summary>

`how` takes four values, and the difference between them is only ever "which
unmatched rows survive". With these two frames — five orders, four customers,
one bad key on the left and one never-ordering customer on the right:

| `how` | Keeps | Rows here |
|---|---|---|
| `"inner"` | only keys present on **both** sides | 4 |
| `"left"` | every row of the **left** frame | 5 |
| `"right"` | every row of the **right** frame | 5 |
| `"outer"` | every row of **both** frames | 6 |

`"inner"` is the default, and it is the default because it is the only one that
cannot invent a blank cell. It is also the one that loses data silently, which
is why the habit worth building is: type the `how` you mean, every time, even
when it is `inner`.

`"outer"` is the audit view. Run it once with `indicator=True` on any pair of
frames you are about to join for real, and count the three categories —
`both`, `left_only`, `right_only`. Six rows here: the four matches, order 105
with no customer, and Tim with no orders. Those two odd rows are exactly the
questions worth asking before you trust the join.

There is a fifth, `how="cross"`, which pairs every row with every row and takes
no key at all. It is occasionally what you want and much more often a sign that
you forgot the `on=` argument.

</details>

<details>
<summary>Under the hood — one-to-many, and the join that multiplies your rows</summary>

The quiet danger in a merge is not missing rows. It is extra ones.

A join matches *every* left row against *every* right row with the same key. In
this problem the address book has one row per customer, so every order matches
at most one customer and the row count cannot grow. Duplicate customer 1 in the
address book — a stale export, two records for the same person — and both
orders for customer 1 now match two rows each. Five orders in, seven rows out,
and the total of `amount` is suddenly larger than the money that was actually
spent.

pandas will tell you if you ask. `validate` raises instead of guessing:

```python
orders.merge(customers, on="customer_id", how="left", validate="many_to_one")
```

`"many_to_one"` says "many orders may share a customer, but each customer
appears once on the right". If that is not true, you get a `MergeError` naming
the problem instead of a report with inflated numbers. The other values are
`"one_to_one"`, `"one_to_many"` and `"many_to_many"`.

The cheap habit, when you have not added `validate`: compare `len(merged)` to
`len(orders)` after every left join. They should be equal. When they are not,
the right-hand key is duplicated, and you have found it in seconds rather than
in a meeting.

</details>

<details>
<summary>Under the hood — merge, join, concat, and when the index is the key</summary>

pandas has three combining tools and they are not interchangeable.

`merge` is the SQL-style join on *columns*, which is what this problem needs
and what you will use nearly always.

`join` is a thin wrapper over `merge` that defaults to matching on the **index**
rather than a column. `orders.set_index("customer_id").join(
customers.set_index("customer_id"))` does this problem's work too. It is
shorter when your data is already indexed by the key, and confusing when it is
not — its default is `how="left"`, the opposite of `merge`'s, which is a fine
trap to have met once.

`concat` does not join at all; it stacks. `pd.concat([jan, feb])` puts February's
rows under January's, and `pd.concat([a, b], axis=1)` puts frames side by side
by index position. Reach for it when the frames have the same *columns* and
different rows, and for nothing else.

One more thing merge does under the hood: for the common case it builds a hash
table of the right frame's keys and probes it once per left row, which is why a
join of a million rows against ten thousand takes a moment rather than an
afternoon. `merge_asof` is the specialist cousin for time series — it matches
each left row to the *nearest earlier* key on the right, which is how you attach
a price quote to a trade that happened between quotes.

</details>

## Acceptance checklist

- [ ] The merged frame has five rows — every order survived.
- [ ] Tim, who never ordered, does not appear.
- [ ] The script prints that exactly one order had no matching customer, and
      names it as order 105.
- [ ] `name` and `country` read `UNKNOWN` on that row, and only that row.
- [ ] `amount` is still a number column after the fill.
- [ ] `merged.csv` exists, has a header and five data rows, and no unnamed
      index column.
- [ ] `merged.isna().sum().sum()` is 0.
- [ ] The file has a docstring and typed signatures.
- [ ] Committed to Git with a message like
      `Add Week 13 homework 3: merge DataFrames`.

## Stretch

- Run the same merge with all four `how` values and print the row count for
  each. Write one sentence per value saying which rows it lost.
- Add `validate="many_to_one"`, then deliberately duplicate customer 1 in the
  address book and watch it raise. That error message is a friend.
- Add a `flagged` boolean column that is `True` for orders whose customer could
  not be found, and keep it in the CSV. `UNKNOWN` in two text columns is easy
  to miss; a boolean column is easy to filter.
- Give `customers` a `discount_rate` column, join it, fill the misses with
  `0.0`, and compute a `net_amount`. Notice that the fill value for a number
  column is a number, not `"UNKNOWN"` — the right filler depends on the column,
  which is the whole reason you fill by name.
- Write the unmatched orders to their own `unmatched.csv`. In a real system
  that file is the one somebody has to work through by hand.

When your join keeps all five orders, head back to the
[Week 13 overview](../README.md) for the rest of the homework set.
