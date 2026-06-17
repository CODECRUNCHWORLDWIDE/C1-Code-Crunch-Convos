# Week 10 — Resources

A focused list of high-quality, free (or free-tier) resources for databases and SQL. Read the docs. The docs are good.

---

## Official documentation

### Python standard library

- **`sqlite3` — DB-API 2.0 interface for SQLite databases**
  <https://docs.python.org/3/library/sqlite3.html>
  Your primary reference this week. Read the introduction, the section on "How-to guides" (especially placeholders), and the "Connection objects" section.

- **PEP 249 — Python Database API Specification v2.0**
  <https://peps.python.org/pep-0249/>
  The interface contract that `sqlite3`, `psycopg2`, `mysql-connector`, and many others all follow. Read it once and you can pick up any Python DB library quickly.

### SQLite

- **SQLite homepage and docs**
  <https://www.sqlite.org/docs.html>
  The canonical reference for the SQLite dialect. Start with:
  - "When to use SQLite" — <https://www.sqlite.org/whentouse.html>
  - "Datatypes in SQLite" — <https://www.sqlite.org/datatype3.html>
  - "SQL As Understood By SQLite" — <https://www.sqlite.org/lang.html>

### SQLAlchemy

- **SQLAlchemy homepage**
  <https://www.sqlalchemy.org/>

- **SQLAlchemy Unified Tutorial (1.4 / 2.0)**
  <https://docs.sqlalchemy.org/en/20/tutorial/index.html>
  The official walkthrough. If you read only one tutorial about SQLAlchemy, make it this one. Covers Core and ORM side by side.

- **SQLAlchemy ORM Quick Start**
  <https://docs.sqlalchemy.org/en/20/orm/quickstart.html>

### PostgreSQL (for when you outgrow SQLite)

- **PostgreSQL documentation**
  <https://www.postgresql.org/docs/>
  Read the "Tutorial" section first; it's surprisingly approachable.

---

## Tutorials

- **SQLBolt — Learn SQL with interactive exercises**
  <https://sqlbolt.com/>
  The fastest way to get SQL into your fingers. Eighteen short lessons, each with an in-browser exercise. Finish at least lessons 1–12 this week.

- **Mode Analytics SQL Tutorial**
  <https://mode.com/sql-tutorial/>
  Excellent intermediate material, with practice problems against a real dataset.

- **Select Star SQL (by Zi Chong Kao)**
  <https://selectstarsql.com/>
  A free, interactive textbook that uses a death-row inmate dataset to teach intermediate SQL. Surprisingly poignant.

---

## Books (free online)

- **Use The Index, Luke! — A guide to database performance for developers**
  <https://use-the-index-luke.com/>
  Markus Winand's free book about SQL performance and indexing. Once your queries start getting slow, this is the book to read. Covers PostgreSQL, MySQL, Oracle, SQL Server, and the lessons port directly to SQLite.

- **The Architecture of Open Source Applications: SQLite (chapter)**
  <https://aosabook.org/en/v1/sqlite.html>
  How SQLite is actually built. Read it once you're comfortable using SQLite — it makes the design decisions click.

---

## Cheat sheets and quick references

- **SQL cheat sheet from SQLZoo**
  <https://sqlzoo.net/wiki/SQL_Tutorial>
  Compact reference and practice problems.

- **The "SQL style guide" by Simon Holywell**
  <https://www.sqlstyle.guide/>
  How to format SQL so other humans can read it.

---

## Tools you may install

- **DB Browser for SQLite** — <https://sqlitebrowser.org/> — a GUI for poking around `.sqlite` files. Free, cross-platform.
- **`sqlite3` CLI** — already installed on macOS and most Linux distros; on Windows, get it from <https://www.sqlite.org/download.html>.
- **Alembic** — <https://alembic.sqlalchemy.org/> — migrations for SQLAlchemy. Touched on briefly this week.

---

## Videos (optional, for different learning styles)

- **"SQL Tutorial - Full Database Course for Beginners" — freeCodeCamp** (YouTube, ~4 hours). Long but well-paced.
- **"Intro to Databases" — MIT 6.830 lecture notes** — heavier, more academic; for the curious.

---

Stick with the docs as your primary source. Tutorials are scaffolding; documentation is the building.
