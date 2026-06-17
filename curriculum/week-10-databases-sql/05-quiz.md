# Week 10 Quiz — Databases & SQL

Ten questions. One correct answer each. Answers and explanations are at the bottom — don't peek until you've done all ten.

---

### 1. What is a primary key?

- **A.** A password used to access the database.
- **B.** A column or set of columns whose values uniquely identify each row in a table.
- **C.** The first column declared in a `CREATE TABLE`.
- **D.** A column that always contains an integer.

---

### 2. Which SQL statement reads data from a table?

- **A.** `READ`
- **B.** `FETCH`
- **C.** `SELECT`
- **D.** `GET`

---

### 3. What happens if you run `UPDATE products SET price = 0;` *without* a `WHERE` clause?

- **A.** SQLite refuses to run it and raises an error.
- **B.** Every single row in `products` is updated — every product is now free.
- **C.** Only the first row is updated.
- **D.** The statement is treated as a no-op.

---

### 4. Which clause filters **groups** that have already been aggregated?

- **A.** `WHERE`
- **B.** `GROUP BY`
- **C.** `HAVING`
- **D.** `FILTER`

---

### 5. You write `SELECT * FROM users WHERE email = NULL`. Why does it return zero rows even when there are rows with a NULL email?

- **A.** Because `NULL` is not a real value, so `= NULL` is never true. You must use `IS NULL`.
- **B.** Because SQLite optimizes out the query.
- **C.** Because email is a TEXT column and TEXT can never be NULL.
- **D.** Because you should use `==` instead of `=`.

---

### 6. Which JOIN keeps every row from the **left** table even when there is no matching row in the right table?

- **A.** `INNER JOIN`
- **B.** `LEFT JOIN`
- **C.** `CROSS JOIN`
- **D.** `OUTER JOIN ALL`

---

### 7. A user types this into your search box:

```
alice'; DROP TABLE users; --
```

You then run:

```python
cursor.execute(f"SELECT * FROM users WHERE name = '{search}'")
```

What is most likely to happen?

- **A.** Nothing — Python automatically escapes user input in f-strings.
- **B.** The query fails with a syntax error but the database is unharmed.
- **C.** A SQL injection: the attacker's `DROP TABLE users` runs, deleting the table.
- **D.** SQLite refuses to execute multiple statements.

---

### 8. Which Python pattern is the correct way to pass `name` into a SQL query safely?

- **A.** `cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")`
- **B.** `cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)`
- **C.** `cursor.execute("SELECT * FROM users WHERE name = ?", (name,))`
- **D.** `cursor.execute("SELECT * FROM users WHERE name = " + repr(name))`

---

### 9. What does `conn.commit()` do?

- **A.** Closes the connection.
- **B.** Saves the pending transaction's changes to disk so they become permanent.
- **C.** Reverts the pending changes.
- **D.** Reloads the schema.

---

### 10. In SQLAlchemy ORM, which method on a `Session` would you call to save new objects you added with `session.add()` to the database?

- **A.** `session.flush_all()`
- **B.** `session.persist()`
- **C.** `session.commit()`
- **D.** `session.save_all()`

---

## Answers

1. **B** — A primary key uniquely identifies each row.
2. **C** — `SELECT` is the SQL read statement.
3. **B** — Forgetting `WHERE` updates *every* row. This is the classic accidental-mass-update bug; always preview with a `SELECT` first.
4. **C** — `HAVING` filters after `GROUP BY`. `WHERE` filters before grouping; `HAVING` filters the resulting groups.
5. **A** — `NULL` is not equal to anything (not even `NULL`). Use `IS NULL` / `IS NOT NULL`. This is the rule that catches everybody at least once.
6. **B** — `LEFT JOIN`. Rows from the left side with no right-side match still appear, with NULLs for the right-side columns.
7. **C** — Classic SQL injection. The f-string interpolation embeds the attacker's payload directly into the SQL. The lesson of Week 10: **never** build SQL with f-strings, `+`, or `%`.
8. **C** — A parameterized query with `?` placeholders and a tuple of values. The database receives the SQL and the values separately; the values are never parsed as SQL.
9. **B** — `commit()` makes the pending transaction permanent. Without it (and outside a `with conn:` block), your changes are lost when the connection closes.
10. **C** — `session.commit()` flushes any pending changes and commits the transaction. (`flush()` exists but doesn't commit; `persist` and `save_all` are not SQLAlchemy methods.)

---

**Scoring**

- 9–10 correct: you're ready for Week 11.
- 7–8 correct: skim the section you missed and try again next week.
- 5–6 correct: re-read Lecture 3, especially Section 5 (SQL injection). Then retake.
- 0–4 correct: rewind to Lecture 1 and code along — don't just read.
