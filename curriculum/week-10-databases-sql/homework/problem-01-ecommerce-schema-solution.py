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
