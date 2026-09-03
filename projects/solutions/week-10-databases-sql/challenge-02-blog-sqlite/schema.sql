-- ---------------------------------------------------------------------------
-- The single source of truth for the blog's shape.
--
-- This file is DESTRUCTIVE on purpose: `flask --app app init-db` drops
-- everything and rebuilds it. That is the right trade for a course project
-- with a seed command; the moment you have data you care about, you stop
-- editing this file and start writing migrations instead.
--
-- Timestamps are ISO-8601 TEXT, filled in by SQLite's DATETIME('now'), which
-- yields 'YYYY-MM-DD HH:MM:SS' in UTC. Storing them this way means ORDER BY
-- on the string is also ORDER BY on the instant -- ISO-8601 sorts correctly as
-- text, which is the whole reason to prefer it over '13/05/2026'.
-- ---------------------------------------------------------------------------

DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- users: one row per account. We store a *hash*, never a password. The column
-- is named password_hash so that nobody, reading any query in this project,
-- can mistake it for the real thing.
CREATE TABLE users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT NOT NULL UNIQUE,
    password_hash  TEXT NOT NULL,
    created_at     TEXT NOT NULL DEFAULT (DATETIME('now'))
);

-- posts: authored by exactly one user. ON DELETE CASCADE means deleting an
-- account takes its posts with it rather than leaving orphan rows pointing at
-- a user id that no longer exists.
CREATE TABLE posts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title         TEXT NOT NULL,
    body          TEXT NOT NULL,
    published_at  TEXT NOT NULL DEFAULT (DATETIME('now'))
);

-- comments: belong to one post, and optionally to one user. author_id is
-- NULLable because guests may comment -- so it gets ON DELETE SET NULL rather
-- than CASCADE: deleting an account should not delete the conversation, it
-- should just stop attributing it.
--
-- post_id, on the other hand, is ON DELETE CASCADE. That is required feature
-- 6: deleting a post removes its comments, enforced by the database instead of
-- by remembering to write a second DELETE in the route.
CREATE TABLE comments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id     INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id   INTEGER          REFERENCES users(id) ON DELETE SET NULL,
    body        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (DATETIME('now'))
);

-- The homepage sorts every post by published_at DESC. Without this index that
-- is a full scan plus a sort on every page load.
CREATE INDEX idx_posts_published ON posts(published_at DESC);

-- The post detail page fetches one post's comments in time order. This index
-- serves both the lookup and the ORDER BY.
CREATE INDEX idx_comments_post ON comments(post_id, created_at);
