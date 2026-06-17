# Lecture 2 — JOINs and Aggregations

> Reading time: ~30 minutes. Bring a SQLite shell, an empty `bookshop.db`, and snacks.

In Lecture 1 we learned to model and query a single table. Today we cross the river: combining data from **multiple tables** with `JOIN`, then summarizing data with `GROUP BY` and the aggregate functions. These are the two SQL skills that separate "I can store a list" from "I can answer questions about my data."

## 1. A two-table playground

Let's set up the schema we'll use throughout this lecture:

```sql
CREATE TABLE authors (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT
);

CREATE TABLE books (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT NOT NULL,
    author_id INTEGER,
    year      INTEGER,
    price     REAL,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

INSERT INTO authors (name, country) VALUES
    ('Ursula K. Le Guin', 'USA'),
    ('Italo Calvino',     'Italy'),
    ('Chimamanda Ngozi Adichie', 'Nigeria'),
    ('Haruki Murakami',   'Japan');

INSERT INTO books (title, author_id, year, price) VALUES
    ('A Wizard of Earthsea',          1, 1968, 14.95),
    ('The Left Hand of Darkness',     1, 1969, 16.50),
    ('Invisible Cities',              2, 1972, 13.00),
    ('If on a Winter''s Night a Traveler', 2, 1979, 15.00),
    ('Half of a Yellow Sun',          3, 2006, 17.99),
    ('Norwegian Wood',                4, 1987, 14.00),
    ('Kafka on the Shore',            4, 2002, 15.99),
    ('Some Anonymous Pamphlet',       NULL, 1800, 2.00);   -- no known author
```

Note the last row: a book with `author_id = NULL` — no associated author. This matters for joins.

## 2. The need for a JOIN

Suppose I want a list of book titles together with the *name* of each author. The titles are in `books`. The names are in `authors`. The link is `books.author_id = authors.id`. A `JOIN` is how we make SQL follow that link.

## 3. INNER JOIN — only matched rows

```sql
SELECT books.title, authors.name AS author
FROM   books
INNER JOIN authors ON books.author_id = authors.id
ORDER BY books.title;
```

Result:

| title                                | author                  |
|--------------------------------------|-------------------------|
| A Wizard of Earthsea                 | Ursula K. Le Guin       |
| Half of a Yellow Sun                 | Chimamanda Ngozi Adichie|
| If on a Winter's Night a Traveler    | Italo Calvino           |
| Invisible Cities                     | Italo Calvino           |
| Kafka on the Shore                   | Haruki Murakami         |
| Norwegian Wood                       | Haruki Murakami         |
| The Left Hand of Darkness            | Ursula K. Le Guin       |

Notice that the "Anonymous Pamphlet" is *missing*. `INNER JOIN` keeps only the rows where the join condition matches in both tables. Since that row had `author_id = NULL`, there is no matching author, so it's dropped.

### Picture it

Two overlapping circles. `INNER JOIN` returns only the overlap:

```
authors  books
   ( A  [ overlap ]  B )
              ^
              |
        INNER JOIN keeps only this
```

### Aliases

Typing `books.title` and `authors.name` gets old. Use **aliases**:

```sql
SELECT b.title, a.name AS author
FROM   books   AS b
INNER JOIN authors AS a ON b.author_id = a.id;
```

The `AS` keyword is optional in most dialects but recommended for readability.

## 4. LEFT JOIN — keep all of the "left" table

What if I *want* the pamphlet to show up, even though it has no author? Use `LEFT JOIN`:

```sql
SELECT b.title, a.name AS author
FROM   books   AS b
LEFT JOIN authors AS a ON b.author_id = a.id
ORDER BY b.title;
```

The result now includes:

| title                                | author                  |
|--------------------------------------|-------------------------|
| ...                                  | ...                     |
| Some Anonymous Pamphlet              | NULL                    |

A `LEFT JOIN` returns **every** row from the left table (`books`), plus the matching columns from the right table (`authors`) — or `NULL` if no match.

### Picture it

```
authors  books
   ( A  [ overlap ]  B )
              |
        LEFT JOIN keeps overlap + all of left (B)
```

> A `RIGHT JOIN` is the mirror image: every row of the right table plus matched rows from the left. SQLite did not support `RIGHT JOIN` until version 3.39; portable code usually writes a `LEFT JOIN` and swaps the table order to achieve the same effect.

### A common LEFT JOIN pattern: finding missing matches

```sql
-- Authors who have not yet written any books in our database
SELECT a.name
FROM   authors AS a
LEFT JOIN books AS b ON b.author_id = a.id
WHERE  b.id IS NULL;
```

The trick: do a `LEFT JOIN`, then keep only rows where the right side is `NULL` — those are the unmatched left-side rows.

## 5. Joining more than two tables

You just keep chaining. Imagine a `genres` table:

```sql
CREATE TABLE genres (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE book_genres (
    book_id  INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, genre_id),
    FOREIGN KEY (book_id)  REFERENCES books(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);
```

`book_genres` is a **junction table** (sometimes called an associative or join table), used to model a many-to-many relationship: a book can have many genres, a genre can have many books.

To list books with their author and *all* their genres:

```sql
SELECT b.title, a.name AS author, g.name AS genre
FROM   books AS b
INNER JOIN authors    AS a  ON b.author_id = a.id
INNER JOIN book_genres AS bg ON bg.book_id = b.id
INNER JOIN genres     AS g  ON g.id = bg.genre_id
ORDER BY b.title, g.name;
```

If a book has three genres, it'll appear three times in the result — once per genre. We'll see how to collapse this with `GROUP_CONCAT` shortly.

## 6. Aggregations: summarizing many rows into one

Sometimes you don't want every row — you want a *summary*. SQL has five core aggregate functions:

| Function | Returns                                 |
|----------|-----------------------------------------|
| `COUNT(x)`| number of non-NULL values of `x`       |
| `COUNT(*)`| number of rows (NULLs counted)          |
| `SUM(x)` | sum of `x` (only numeric)               |
| `AVG(x)` | arithmetic mean of `x`                  |
| `MIN(x)` | smallest value of `x`                   |
| `MAX(x)` | largest value of `x`                    |

Simple examples:

```sql
SELECT COUNT(*)        AS total_books FROM books;
SELECT SUM(price)      AS inventory_value FROM books;
SELECT AVG(price)      AS average_price FROM books;
SELECT MIN(year), MAX(year) FROM books;
```

`COUNT(*)` and `COUNT(column)` differ when there are NULLs. `COUNT(year)` ignores rows where `year IS NULL`; `COUNT(*)` includes them.

## 7. GROUP BY — aggregation, but per category

A `GROUP BY` clause says *"group the rows by this column, then run the aggregate per group"*.

> Books per author:

```sql
SELECT a.name AS author, COUNT(b.id) AS num_books
FROM   authors AS a
LEFT JOIN books AS b ON b.author_id = a.id
GROUP BY a.id, a.name
ORDER BY num_books DESC;
```

| author                  | num_books |
|-------------------------|-----------|
| Ursula K. Le Guin       | 2         |
| Italo Calvino           | 2         |
| Haruki Murakami         | 2         |
| Chimamanda Ngozi Adichie| 1         |

The `LEFT JOIN` is what makes an author with zero books still appear (they'd have `num_books = 0`).

### The two rules of GROUP BY

1. **Every non-aggregated column in `SELECT` must be in `GROUP BY`**. The query above lists `a.name` in `SELECT`, so `a.name` is in `GROUP BY`. (SQLite is lenient and won't always complain, but PostgreSQL will. Get used to writing it correctly.)
2. **The `WHERE` clause filters rows *before* grouping. The `HAVING` clause filters groups *after* grouping.**

## 8. HAVING — filtering groups

`WHERE` cannot reference aggregate functions because aggregates don't exist until after grouping. That's what `HAVING` is for:

```sql
-- Authors with more than 1 book
SELECT a.name AS author, COUNT(b.id) AS num_books
FROM   authors AS a
LEFT JOIN books AS b ON b.author_id = a.id
GROUP BY a.id, a.name
HAVING COUNT(b.id) > 1
ORDER BY num_books DESC;
```

To remember: **`WHERE` filters rows, `HAVING` filters groups**.

## 9. Putting the clauses together

The canonical SQL evaluation order — which is *not* the order you write them — is:

1. `FROM` (and `JOIN`s)
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`
7. `LIMIT`

Read top to bottom: tables get built, rows get filtered, rows get grouped, groups get filtered, columns get computed, results get sorted, then trimmed.

A query that uses every clause:

```sql
SELECT  a.country, COUNT(*) AS book_count, AVG(b.price) AS avg_price
FROM    books AS b
INNER JOIN authors AS a ON a.id = b.author_id
WHERE   b.year >= 1970
GROUP BY a.country
HAVING  COUNT(*) >= 1
ORDER BY avg_price DESC
LIMIT   5;
```

Reading it: *"For books published in 1970 or later, count how many came from each country and what the average price was, keeping only countries with at least one such book, sorted by average price, top 5."*

## 10. Subqueries (briefly)

A **subquery** is a query inside a query. Useful when you need the result of one query to feed into another.

### Subquery in `WHERE`

```sql
-- Books written by the author with the most books
SELECT title FROM books
WHERE author_id = (
    SELECT author_id
    FROM   books
    WHERE  author_id IS NOT NULL
    GROUP BY author_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
```

### Subquery in `FROM` (a derived table)

```sql
SELECT author_id, max_price
FROM (
    SELECT author_id, MAX(price) AS max_price
    FROM   books
    GROUP BY author_id
) AS author_max
WHERE max_price > 15;
```

### Correlated subqueries

A correlated subquery references a column from the outer query. They are powerful but can be slow:

```sql
-- Each book, with the count of all books published the same year
SELECT b.title, b.year,
       (SELECT COUNT(*) FROM books b2 WHERE b2.year = b.year) AS same_year_count
FROM   books AS b;
```

Rule of thumb: if you can write the same thing as a JOIN, prefer the JOIN — the database optimizer is usually better at JOINs than at correlated subqueries.

## 11. Useful patterns to keep in your back pocket

### "Top N per group"

Most expensive book per author:

```sql
SELECT b.title, b.price, a.name AS author
FROM   books AS b
INNER JOIN authors AS a ON a.id = b.author_id
WHERE  b.price = (
    SELECT MAX(b2.price) FROM books b2 WHERE b2.author_id = b.author_id
);
```

### Counting rows that satisfy a condition with `SUM(CASE ...)`

```sql
SELECT
    COUNT(*)                                            AS total_books,
    SUM(CASE WHEN year < 1980 THEN 1 ELSE 0 END)        AS old_books,
    SUM(CASE WHEN year >= 1980 THEN 1 ELSE 0 END)       AS newer_books
FROM books;
```

This avoids running the query three times.

### Concatenating grouped strings: `GROUP_CONCAT`

```sql
SELECT a.name AS author,
       GROUP_CONCAT(b.title, '; ') AS titles
FROM   authors AS a
LEFT JOIN books AS b ON b.author_id = a.id
GROUP BY a.id, a.name;
```

In SQLite this is `GROUP_CONCAT`; in PostgreSQL it's `STRING_AGG`. Useful for collapsing many rows into one.

### `DISTINCT`

Want unique values?

```sql
SELECT DISTINCT country FROM authors;
```

`DISTINCT` operates over all the selected columns together.

## 12. Pitfalls

- **Forgetting to group by every non-aggregated column** — works in SQLite, breaks in PostgreSQL.
- **Using `WHERE` to filter an aggregate** — use `HAVING`.
- **Reading INNER JOIN when you meant LEFT JOIN** — INNER silently drops unmatched rows; if you wanted "every author, even the ones with no books", you need LEFT.
- **Joining on the wrong column** — if you join `books.id = authors.id` (both are primary keys) instead of `books.author_id = authors.id`, you'll get correct-looking nonsense.
- **`COUNT(column)` vs `COUNT(*)`** — they differ when NULLs exist. Pick the one you actually mean.

## 13. Recap

You can now:

- Pull data from two or more tables together with `INNER JOIN` and `LEFT JOIN`.
- Distinguish the cases where each is appropriate.
- Aggregate data with `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- Slice aggregates per group with `GROUP BY` and filter groups with `HAVING`.
- Sketch subqueries and recognize when a JOIN would be cleaner.

Take a break, then jump into Lecture 3 where we wire all of this into Python with the `sqlite3` module — and learn the most important security lesson of the week.

### References

- SQLite SELECT syntax: <https://www.sqlite.org/lang_select.html>
- SQLBolt lessons 6–13: <https://sqlbolt.com/>
- "Use The Index, Luke": <https://use-the-index-luke.com/> (skim the JOIN performance chapter once you're comfortable with the syntax)
