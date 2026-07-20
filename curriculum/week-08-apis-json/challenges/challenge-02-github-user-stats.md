# Challenge 02 — GitHub User Stats

> ~3 hours. Uses the public GitHub REST API. No token required (60 requests/hour limit applies; if you have a token in `.env`, the client should use it).

## Story

Recruiters and journalists often want a quick snapshot of a developer's public GitHub footprint. Build a CLI that prints one.

## Goal

Build a script `challenge-02-github-user-stats.py` that runs like this:

```bash
$ python challenge-02-github-user-stats.py octocat
User:     octocat (The Octocat)
Bio:      —
Location: San Francisco
Followers: 18472
Public repos: 8
Total stars: 1521
Top 5 repos by stars:
  1. Spoon-Knife            (★ 12483) — This repo is for demonstration purposes only.
  2. Hello-World            (★  2510)
  3. octocat.github.io      (★   232)
  4. git-consortium         (★    98)
  5. test-repo1             (★    23)
```

```bash
$ python challenge-02-github-user-stats.py does-not-exist-9999
Error: GitHub returned 404 for user 'does-not-exist-9999'.
```

## API

Base URL: `https://api.github.com`

Endpoints you will need:

| Endpoint | Purpose |
|---|---|
| `GET /users/{login}` | User profile (name, bio, location, follower count, public_repos count) |
| `GET /users/{login}/repos?per_page=100&page=N` | Paginated list of public repos |

Sample response shape from `/users/{login}`:

```json
{
  "login": "octocat",
  "name": "The Octocat",
  "bio": null,
  "location": "San Francisco",
  "followers": 18472,
  "public_repos": 8
}
```

Each repo in the `/users/{login}/repos` response has at least these keys:

```json
{
  "name": "Hello-World",
  "stargazers_count": 2510,
  "description": "My first repository on GitHub!"
}
```

## Requirements

The script must:

1. Accept one positional argument: the GitHub `username`.
2. Fetch the user profile.
3. Fetch **all pages** of the user's public repos (Exercise 04 pattern).
4. Compute and print:
   - Name (or login if `name` is null), bio (`—` if null), location (`—` if null)
   - Follower count, public repo count
   - **Sum of stargazers_count across all repos.**
   - The top 5 repos by stars, with name, star count, and (truncated) description.
5. Be polite to the API:
   - Set `User-Agent: code-crunch-bootcamp/1.0`.
   - If `GITHUB_TOKEN` is set in the environment (via `.env`), include `Authorization: Bearer <token>` to lift the rate limit.
   - Set `timeout=` on every request.
6. Handle errors:
   - 404 → "User not found" message, exit non-zero, no traceback.
   - 403 with "rate limit exceeded" → tell the user to wait or set `GITHUB_TOKEN`.
   - Any other failure → print a short message, exit non-zero, no traceback.

## Grading rubric

| Criterion | Points |
|---|---|
| Profile lookup works | 15 |
| Repository pagination correctly fetches *all* pages | 20 |
| Total stars correctly computed | 10 |
| Top-5 sort correct (descending by stars; ties broken by name) | 10 |
| `GITHUB_TOKEN` from `.env` is used when present | 10 |
| 404 and 403 handled with helpful messages | 15 |
| Code organized into small typed functions | 10 |
| Output formatted cleanly (aligned columns or similar) | 5 |
| Write-up answers all three questions | 5 |
| **Total** | **100** |

## Hints

- Reuse the `make_session()` helper from Exercise 05 (or copy and adapt). Add the `Authorization` header conditionally.
- For "top 5 by stars", use `sorted(repos, key=lambda r: (-r["stargazers_count"], r["name"]))[:5]`. The negative star count gives descending order; the secondary `r["name"]` breaks ties alphabetically.
- Truncate long descriptions with `desc[:50] + "..."` (or use `textwrap.shorten`).
- For the `403 rate-limit` case, GitHub returns a body with `{"message": "API rate limit exceeded for ..."}`. Match on `"rate limit"` in the message text.

## Stretch (optional)

- Add a `--json` flag that prints the result as a JSON document instead of formatted text.
- Add a `--save FILE` flag that appends the result to a JSON history file (Week 6 patterns).
- Display each repo's `language` alongside the star count.
- Use the `GET /search/users?q=...` endpoint to make the lookup case-insensitive when the user mistypes their own login.
