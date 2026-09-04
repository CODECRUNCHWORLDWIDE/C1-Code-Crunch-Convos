# Homework Problem 1 — Design an E-Commerce Schema

> **Topic:** turning a description of a shop into tables, keys, and constraints that make bad data impossible to store
> **Lecture:** [01 — Relational Databases & SQL](../lecture-notes/01-relational-databases-and-sql.md)
> **Difficulty:** Intermediate
> **Target time:** 45 minutes
> **Why this one:** every other database problem this week hands you a schema. This is the one where you *design* it. A good schema does your error-checking for you — the database refuses a six-star review and a duplicate email before a single line of your code runs — and that habit, letting the table hold the rules, is the whole point of the week.

## The Brief

Imagine a small online shop. People sign up, save a few delivery
addresses, browse a catalogue of products sorted into categories, place
orders, and leave reviews. Your job is to write the **shape** of that
shop as SQL tables — no Python at all — so that the database itself
guarantees the data always makes sense.

A schema is just a set of `CREATE TABLE` statements. Each table is a grid
with named columns, and each column can carry rules: this one can't be
empty (`NOT NULL`), this one has to be one-of-a-kind (`UNIQUE`), this
number has to stay in range (`CHECK`), this value has to point at a real
row in another table (a foreign key). Get those rules right and whole
categories of bug simply cannot happen.

You need eight tables:

- **customers** — one row per person: name, a unique email, when they joined.
- **addresses** — many per customer; one of them is the default to ship to.
- **products** — the catalogue: a unique SKU, name, description, price, stock.
- **categories** — a *tree*: a category can have a parent category (or none, if it's a top-level one).
- **product_categories** — the many-to-many link: a product sits in several categories, a category holds many products.
- **orders** — the header: who ordered, what state it's in, when.
- **order_items** — one line per product in an order, with the quantity and the price *at the time of purchase*.
- **reviews** — a customer's rating (1–5) and words about a product.

The deliverable is the SQL. To *prove* the SQL is right rather than ask
anyone to trust it, the solution loads the schema into an in-memory
database, lists what it built, inserts one legal row into every table,
and then tries three illegal rows so you can watch the constraints throw
them out.

## Starter

Save this as `schema_demo.py` and fill in the `TODO`s. It runs as
pasted — with an empty schema it just reports zero tables.

```python
"""Design an e-commerce schema, then prove it with an in-memory database."""

import sqlite3
from typing import Final

SCHEMA: Final[str] = """
-- TODO: CREATE TABLE customers (...)
-- TODO: CREATE TABLE addresses (...)      many per customer, one is default
-- TODO: CREATE TABLE products (...)       sku UNIQUE, price/stock CHECK >= 0
-- TODO: CREATE TABLE categories (...)     parent_id REFERENCES categories(id)
-- TODO: CREATE TABLE product_categories   many-to-many, composite primary key
-- TODO: CREATE TABLE orders (...)
-- TODO: CREATE TABLE order_items (...)     unit_price copied in at purchase
-- TODO: CREATE TABLE reviews (...)         rating CHECK BETWEEN 1 AND 5
-- TODO: a few CREATE INDEX lines for the common lookups
"""


def build(conn: sqlite3.Connection) -> None:
    """Load the schema into an open connection."""
    conn.executescript(SCHEMA)
    conn.commit()


def main() -> None:
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        build(conn)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        print(f"Created {len(tables)} tables:")
        for (name,) in tables:
            print(f"  {name}")
        # TODO: insert one legal row into every table (the happy path)
        # TODO: try three illegal rows and print the IntegrityError each earns
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-10-databases-sql/homework/problem-01-ecommerce-schema.md) and run it there. `sqlite3` ships with Python, so there is nothing to install.

## Requirements

1. Eight tables with sensible primary keys, and a foreign key everywhere
   one table points at another (`addresses.customer_id`,
   `order_items.order_id`, and so on).
2. `NOT NULL` on every column that must have a value, and `UNIQUE` on
   `customers.email` and `products.sku`.
3. At least these `CHECK` constraints: `price >= 0`, `stock >= 0`,
   `quantity > 0`, and `rating BETWEEN 1 AND 5`.
4. `categories` is a tree — a nullable `parent_id` that references
   `categories(id)`. A top-level category has `parent_id` NULL.
5. `product_categories` is the many-to-many junction, with a
   **composite primary key** `(product_id, category_id)` so the same
   pairing cannot be stored twice.
6. `order_items` copies `unit_price` in at purchase time, so changing a
   product's price later never rewrites an old receipt.
7. At least three indexes on the columns common queries filter by.
8. Running the file prints the tables and indexes it created, seeds one
   legal row per table, and shows three illegal rows being refused.

## Constraints

- **Let the schema do the checking, not your application code.** Every
  rule you push into a `CHECK`, a `UNIQUE`, or a foreign key is a rule
  you never have to remember to enforce in Python — and can never forget.
  A rating column with no `CHECK` will hold `7` the first day someone
  fat-fingers the API.
- **`unit_price` lives on the order line, not just on the product.** The
  price on `products` is today's price. The price on `order_items` is
  what the customer actually paid. If you only store one, a price change
  next week silently rewrites the history of every past order — an
  accounting nightmare that starts as a "harmless" normalisation.
- **Turn foreign keys on.** SQLite ships with foreign-key enforcement
  *off* for backwards compatibility. `PRAGMA foreign_keys = ON` per
  connection is what makes "an order item for a product that doesn't
  exist" actually fail instead of quietly storing a dangling reference.
- **No Python in the deliverable schema.** The `SCHEMA` string is pure
  SQL. The Python around it only exists to load and test it — it is the
  witness, not the work.

## Expected output

```text
Created 8 tables:
  addresses
  categories
  customers
  order_items
  orders
  product_categories
  products
  reviews
Created 5 indexes:
  idx_addresses_customer
  idx_order_items_order
  idx_orders_customer
  idx_product_categories_category
  idx_reviews_product

Happy path: one legal row in every table. All accepted.

Now the rows the schema exists to refuse:
  a six-star review
    sqlite3.IntegrityError: CHECK constraint failed: rating BETWEEN 1 AND 5
  a second customer with the same email
    sqlite3.IntegrityError: UNIQUE constraint failed: customers.email
  an order item for a product that does not exist
    sqlite3.IntegrityError: FOREIGN KEY constraint failed

Every refusal above is the schema doing the checking, so no
application code ever has to remember to.
```

## Steps

1. Sketch the eight tables on paper first. Draw an arrow from every
   foreign key to the table it points at. If two tables point at each
   other, you probably have the direction of one wrong.
2. Write `customers`, `products`, and `categories` first — the tables
   nothing depends on. Run the file; you should see three tables listed.
3. Add the tables that reference them: `addresses`, `orders`,
   `order_items`, `reviews`, and the `product_categories` junction. Run
   again after each.
4. Add the `CHECK` constraints and the indexes. Rerun and confirm the
   counts match the Expected output.
5. Fill in the happy-path inserts and the three illegal inserts. Watch
   each `IntegrityError` name the exact rule it broke.

## The Solution

```python
"""problem-01-ecommerce-schema-solution.py — an e-commerce schema that defends itself.

The deliverable is the SQL in ``SCHEMA`` below: eight tables covering
customers, addresses, products, a category tree, a many-to-many junction,
orders, order items, and reviews — with the keys, constraints and indexes
that make bad data impossible to store.

Running this file proves the schema instead of asking you to trust it: it
loads the DDL into an in-memory database, lists what was created, inserts a
valid happy path, and then tries two illegal rows so you can watch the
constraints refuse them. Nothing is written to disk.

Run it with::

    python problem-01-ecommerce-schema-solution.py
"""

import sqlite3
from typing import Final

SCHEMA: Final[str] = """
-- customers: one row per person who can place an order.
CREATE TABLE customers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);

-- addresses: many per customer; is_default flags the one to ship to.
CREATE TABLE addresses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    line1       TEXT NOT NULL,
    city        TEXT NOT NULL,
    postcode    TEXT NOT NULL,
    country     TEXT NOT NULL,
    is_default  INTEGER NOT NULL DEFAULT 0 CHECK (is_default IN (0, 1))
);

-- products: the catalogue; sku is the human-facing unique code.
CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    sku         TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    price       REAL NOT NULL CHECK (price >= 0),
    stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- categories: a tree — parent_id points at another category, NULL at a root.
CREATE TABLE categories (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL UNIQUE,
    parent_id INTEGER REFERENCES categories(id)
);

-- product_categories: many-to-many; the two-column primary key stops
-- the same pairing being stored twice.
CREATE TABLE product_categories (
    product_id  INTEGER NOT NULL REFERENCES products(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    PRIMARY KEY (product_id, category_id)
);

-- orders: the header — who ordered, what state it is in, when.
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status      TEXT NOT NULL DEFAULT 'open'
                CHECK (status IN ('open', 'paid', 'shipped', 'cancelled')),
    placed_at   TEXT NOT NULL
);

-- order_items: one line per product in an order. unit_price is copied in
-- at purchase time, so later price changes cannot rewrite old receipts.
CREATE TABLE order_items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id   INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id)
);

-- reviews: one per customer per product, rating locked to 1-5.
CREATE TABLE reviews (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    product_id  INTEGER NOT NULL REFERENCES products(id),
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    body        TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL,
    UNIQUE (customer_id, product_id)
);

-- Indexes for the lookups every shop page makes: a customer's addresses
-- and orders, an order's lines, a product's reviews and categories.
CREATE INDEX idx_addresses_customer          ON addresses(customer_id);
CREATE INDEX idx_orders_customer             ON orders(customer_id);
CREATE INDEX idx_order_items_order           ON order_items(order_id);
CREATE INDEX idx_reviews_product             ON reviews(product_id);
CREATE INDEX idx_product_categories_category ON product_categories(category_id);
"""


def build(conn: sqlite3.Connection) -> None:
    """Load the schema into an open connection."""
    conn.executescript(SCHEMA)
    conn.commit()


def created_objects(conn: sqlite3.Connection, kind: str) -> list[str]:
    """Return the names of tables or indexes, straight from sqlite_master."""
    cursor = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = ? AND name NOT LIKE 'sqlite_%' ORDER BY name",
        (kind,),
    )
    return [name for (name,) in cursor.fetchall()]


def seed_happy_path(conn: sqlite3.Connection) -> None:
    """Insert one legal row into every table, proving the shape fits together."""
    with conn:
        conn.execute(
            "INSERT INTO customers (name, email, created_at) VALUES (?, ?, ?)",
            ("Ada Lovelace", "ada@example.com", "2026-05-01"),
        )
        conn.execute(
            "INSERT INTO addresses (customer_id, line1, city, postcode, country, is_default) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (1, "12 Analytical Row", "London", "N1 9GU", "GB", 1),
        )
        conn.execute(
            "INSERT INTO products (sku, name, description, price, stock) "
            "VALUES (?, ?, ?, ?, ?)",
            ("KB-045", "Mechanical keyboard", "Clicky.", 45.00, 12),
        )
        conn.execute(
            "INSERT INTO categories (name, parent_id) VALUES (?, ?)",
            ("Peripherals", None),
        )
        conn.execute(
            "INSERT INTO categories (name, parent_id) VALUES (?, ?)",
            ("Keyboards", 1),
        )
        conn.execute(
            "INSERT INTO product_categories (product_id, category_id) VALUES (?, ?)",
            (1, 2),
        )
        conn.execute(
            "INSERT INTO orders (customer_id, status, placed_at) VALUES (?, ?, ?)",
            (1, "paid", "2026-05-02"),
        )
        conn.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) "
            "VALUES (?, ?, ?, ?)",
            (1, 1, 2, 45.00),
        )
        conn.execute(
            "INSERT INTO reviews (customer_id, product_id, rating, body, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (1, 1, 5, "Louder than my thoughts.", "2026-05-09"),
        )


def prove_constraint(conn: sqlite3.Connection, label: str, sql: str, values: tuple) -> None:
    """Try an illegal insert and print the exact refusal it earns."""
    print(f"  {label}")
    try:
        with conn:
            conn.execute(sql, values)
        print("    ACCEPTED - the schema is missing a constraint!")
    except sqlite3.IntegrityError as exc:
        print(f"    sqlite3.IntegrityError: {exc}")


def main() -> None:
    """Build the schema in memory, list it, seed it, and attack it."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        build(conn)
        tables = created_objects(conn, "table")
        indexes = created_objects(conn, "index")
        print(f"Created {len(tables)} tables:")
        for name in tables:
            print(f"  {name}")
        print(f"Created {len(indexes)} indexes:")
        for name in indexes:
            print(f"  {name}")

        seed_happy_path(conn)
        print("\nHappy path: one legal row in every table. All accepted.")

        print("\nNow the rows the schema exists to refuse:")
        prove_constraint(
            conn,
            "a six-star review",
            "INSERT INTO reviews (customer_id, product_id, rating, body, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (1, 1, 6, "Off the scale.", "2026-05-10"),
        )
        prove_constraint(
            conn,
            "a second customer with the same email",
            "INSERT INTO customers (name, email, created_at) VALUES (?, ?, ?)",
            ("Ada L.", "ada@example.com", "2026-05-11"),
        )
        prove_constraint(
            conn,
            "an order item for a product that does not exist",
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) "
            "VALUES (?, ?, ?, ?)",
            (1, 999, 1, 9.99),
        )
        print("\nEvery refusal above is the schema doing the checking, so no")
        print("application code ever has to remember to.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

**Why it works.**

**A schema is a contract the database enforces for free.** Everything in
those eight `CREATE TABLE` statements is a promise SQLite keeps on every
write, forever, without your code lifting a finger. `email TEXT NOT NULL
UNIQUE` means no customer without an email and no two customers sharing
one — checked at insert time, so a duplicate is a caught error rather
than a support ticket three months later.

**Foreign keys wire the tables into one shape.** `addresses.customer_id
REFERENCES customers(id)` says an address must belong to a real customer.
With `PRAGMA foreign_keys = ON`, inserting an `order_items` row for
product `999` — which does not exist — fails with `FOREIGN KEY
constraint failed`. That is the database refusing to let the graph of
data develop a hole.

**The composite key on the junction is doing quiet work.** `PRIMARY KEY
(product_id, category_id)` on `product_categories` means the pair is the
identity of the row. Try to file the same product under the same category
twice and the second insert is refused. A plain `id` primary key there
would happily store the duplicate.

**`CHECK` is the cheapest validation you will ever write.** `rating
BETWEEN 1 AND 5` is nine characters that make a six-star review
impossible to store. Compare the alternative: validating the range in
every code path that ever writes a review, and hoping you found them all.

**Copying `unit_price` onto the line item is the one modelling decision
that separates a toy from a real shop.** A receipt has to be immutable.
Storing the price on the order line, at the moment of purchase, means
next month's sale cannot travel back in time and change what a customer
paid in March.

## Run it

Copy the worked answer on this page into `problem-01-ecommerce-schema.py` and run it:
and run it:

```bash
python problem-01-ecommerce-schema.py
```

It builds the whole schema in an in-memory database, lists it, seeds it,
and attacks it — then throws the database away. Nothing is written to
disk and no `.db` file is left behind.

Your hand-in is the SQL itself. Copy the `SCHEMA` string into a
`schema.sql` file and confirm it loads on its own:

```bash
sqlite3 ecommerce.db < schema.sql
```

## Common bugs to catch

- **`sqlite3.IntegrityError: FOREIGN KEY constraint failed` never
  fires — the bad row goes in.** You forgot `PRAGMA foreign_keys = ON`.
  SQLite parses the `REFERENCES` clause but does not enforce it unless
  the pragma is set, per connection, every time.
- **`sqlite3.OperationalError: near "REFERENCES": syntax error`.** A
  column-level foreign key is written `customer_id INTEGER REFERENCES
  customers(id)` — the `REFERENCES` comes right after the type, with no
  `FOREIGN KEY` keyword. That keyword is only for the table-level form.
- **The category tree references a table that doesn't exist yet.**
  `parent_id INTEGER REFERENCES categories(id)` inside the `categories`
  table is a self-reference, and that is legal — a table may reference
  itself. If you split it into two tables to "fix" it, you have
  misread the tree.
- **`sqlite3.IntegrityError: UNIQUE constraint failed:
  product_categories.product_id`.** You gave the junction table a normal
  single-column primary key on `product_id`, so a product can belong to
  exactly one category. The key has to be the *pair*.
- **Storing only `products.price` and reading it back for old orders.**
  No error, ever — which is what makes it dangerous. The bug only shows
  up the day a price changes and every historical total silently moves.

## Under the hood

<details>
<summary>Under the hood — normalization, and why one fact lives in one place</summary>

The reason this schema has eight tables instead of one giant
"everything" table is a idea called **normalization**: every fact lives
in exactly one place, and everywhere else refers to it by key.

A customer's email is stored once, in `customers`. An order does not
copy the email in; it stores a `customer_id` and follows the reference
when it needs the email. So when a customer changes their email, you
update one row and every order instantly sees the new value, because no
order ever had its own copy.

The famous exception in this very schema is `order_items.unit_price`,
and it is worth understanding *why* it breaks the rule. Normalization
says "don't copy the price, reference the product". But the price on the
product is a *current* fact, and the price on the order is a *historical*
fact — they are genuinely two different things that happen to share a
number on the day of purchase. Storing both is not duplication; it is
recording two facts that will diverge. Recognising when a value is
"the same" versus "the same right now" is most of the art of schema
design.

The tradeoff has a cost. Normalized data means joins: to show an order
with the customer's name and each product's name, you gather rows from
four tables. That is what Week 10's joins are for, and it is a good
trade — a little query complexity in exchange for data that can never
contradict itself.

</details>

<details>
<summary>Under the hood — what an index actually is, and why five of them</summary>

An index is a second, sorted copy of one or more columns, kept in a
structure (a B-tree) that the database can binary-search. Without one, a
query like "all addresses for customer 12" has to read *every* address
row and check each `customer_id` — a full scan. With
`idx_addresses_customer` it jumps straight to the matching rows.

The five indexes here are not decoration; each one backs a lookup a shop
page makes constantly:

| Index | The query it rescues |
|---|---|
| `idx_addresses_customer` | this customer's saved addresses |
| `idx_orders_customer` | this customer's order history |
| `idx_order_items_order` | the lines on this order |
| `idx_reviews_product` | the reviews under this product |
| `idx_product_categories_category` | the products in this category |

Every index also has a cost: it is extra storage, and every `INSERT` or
`UPDATE` has to update the index too, so writes get slightly slower. The
rule of thumb is to index the columns you filter or join on and nothing
else — Problem 4 is where you learn to *measure* whether an index is
earning its keep with `EXPLAIN QUERY PLAN`, rather than guessing.

Notice what is *not* indexed: the primary keys. SQLite indexes those
automatically, because it has to enforce their uniqueness anyway. Adding
your own index on a primary key is pure waste.

</details>

## Acceptance checklist

- [ ] Eight tables, each with a primary key.
- [ ] Every cross-table reference is a real foreign key, and
      `PRAGMA foreign_keys = ON` is set.
- [ ] `customers.email` and `products.sku` are `UNIQUE`.
- [ ] `CHECK` guards `price`, `stock`, `quantity`, and `rating`.
- [ ] `categories` has a nullable self-referencing `parent_id`.
- [ ] `product_categories` uses a composite `(product_id, category_id)`
      primary key.
- [ ] `order_items` stores `unit_price` on the line, not just on the product.
- [ ] At least three indexes exist.
- [ ] Running the file prints eight tables, five indexes, the happy path,
      and three refusals matching the Expected output.

## Stretch

- **Add an `updated_at` to `products` and a trigger** that sets it on
  every `UPDATE`. Triggers are SQL that runs automatically on a write —
  the database keeping a timestamp honest without any application help.
- **Add a partial unique index** so that each customer can have at most
  one default address: `CREATE UNIQUE INDEX ... ON addresses(customer_id)
  WHERE is_default = 1`. Try to set two defaults and watch it refuse.
- **Model a discount.** Add a `coupons` table and a nullable
  `order.coupon_id`. Where should the discounted amount be stored so an
  old order still shows what was actually charged? (The same reasoning as
  `unit_price`.)
- **Write five `SELECT`s against your schema** — a customer's orders, a
  product's average rating, the top category by product count — to feel
  whether the shape you chose makes the real questions easy or hard. If a
  question needs a five-table join, the shape might be telling you
  something.

Next: [Problem 2 — A Migration Script](./problem-02-migration-script.md),
where you change a schema that already has data in it without losing a row.
