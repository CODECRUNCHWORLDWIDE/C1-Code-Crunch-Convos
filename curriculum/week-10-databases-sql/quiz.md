# Week 10 Quiz — Databases & SQL

Ten questions. One correct answer each. Each answer and its explanation are folded under the question — don't open one until you have committed to your answer.

---

### 1. What is a primary key?

- **A.** A password used to access the database.
- **B.** A column or set of columns whose values uniquely identify each row in a table.
- **C.** The first column declared in a `CREATE TABLE`.
- **D.** A column that always contains an integer.

<details>
<summary>Answer</summary>

**B** — A primary key uniquely identifies each row.

</details>

---

### 2. Which SQL statement reads data from a table?

- **A.** `READ`
- **B.** `FETCH`
- **C.** `SELECT`
- **D.** `GET`

<details>
<summary>Answer</summary>

**C** — `SELECT` is the SQL read statement.

</details>

---

### 3. What happens if you run `UPDATE products SET price = 0;` *without* a `WHERE` clause?

- **A.** SQLite refuses to run it and raises an error.
- **B.** Every single row in `products` is updated — every product is now free.
- **C.** Only the first row is updated.
- **D.** The statement is treated as a no-op.

<details>
<summary>Answer</summary>

**B** — Forgetting `WHERE` updates *every* row. This is the classic accidental-mass-update bug; always preview with a `SELECT` first.

</details>

---

### 4. Which clause filters **groups** that have already been aggregated?

- **A.** `WHERE`
- **B.** `GROUP BY`
- **C.** `HAVING`
- **D.** `FILTER`

<details>
<summary>Answer</summary>

**C** — `HAVING` filters after `GROUP BY`. `WHERE` filters before grouping; `HAVING` filters the resulting groups.

</details>

---

### 5. You write `SELECT * FROM users WHERE email = NULL`. Why does it return zero rows even when there are rows with a NULL email?

- **A.** Because `NULL` is not a real value, so `= NULL` is never true. You must use `IS NULL`.
- **B.** Because SQLite optimizes out the query.
- **C.** Because email is a TEXT column and TEXT can never be NULL.
- **D.** Because you should use `==` instead of `=`.

<details>
<summary>Answer</summary>

**A** — `NULL` is not equal to anything (not even `NULL`). Use `IS NULL` / `IS NOT NULL`. This is the rule that catches everybody at least once.

</details>

---

### 6. Which JOIN keeps every row from the **left** table even when there is no matching row in the right table?

- **A.** `INNER JOIN`
- **B.** `LEFT JOIN`
- **C.** `CROSS JOIN`
- **D.** `OUTER JOIN ALL`

<details>
<summary>Answer</summary>

**B** — `LEFT JOIN`. Rows from the left side with no right-side match still appear, with NULLs for the right-side columns.

</details>

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

<details>
<summary>Answer</summary>

**C** — Classic SQL injection. The f-string interpolation embeds the attacker's payload directly into the SQL. The lesson of Week 10: **never** build SQL with f-strings, `+`, or `%`.

</details>

---

### 8. Which Python pattern is the correct way to pass `name` into a SQL query safely?

- **A.** `cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")`
- **B.** `cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)`
- **C.** `cursor.execute("SELECT * FROM users WHERE name = ?", (name,))`
- **D.** `cursor.execute("SELECT * FROM users WHERE name = " + repr(name))`

<details>
<summary>Answer</summary>

**C** — A parameterized query with `?` placeholders and a tuple of values. The database receives the SQL and the values separately; the values are never parsed as SQL.

</details>

---

### 9. What does `conn.commit()` do?

- **A.** Closes the connection.
- **B.** Saves the pending transaction's changes to disk so they become permanent.
- **C.** Reverts the pending changes.
- **D.** Reloads the schema.

<details>
<summary>Answer</summary>

**B** — `commit()` makes the pending transaction permanent. Without it (and outside a `with conn:` block), your changes are lost when the connection closes.

</details>

---

### 10. In SQLAlchemy ORM, which method on a `Session` would you call to save new objects you added with `session.add()` to the database?

- **A.** `session.flush_all()`
- **B.** `session.persist()`
- **C.** `session.commit()`
- **D.** `session.save_all()`

<details>
<summary>Answer</summary>

**C** — `session.commit()` flushes any pending changes and commits the transaction. (`flush()` exists but doesn't commit; `persist` and `save_all` are not SQLAlchemy methods.)

---

**Scoring**

- 9–10 correct: you're ready for Week 11.
- 7–8 correct: skim the section you missed and try again next week.
- 5–6 correct: re-read Lecture 3, especially Section 5 (SQL injection). Then retake.
- 0–4 correct: rewind to Lecture 1 and code along — don't just read.

</details>

---
