# Week 12 — Challenges

Two larger problems that combine multiple concepts. Each takes **1.5–3 hours**. Solutions are not shipped — share yours with a peer for review.

| # | Challenge                              | Combines                                        |
|---|----------------------------------------|-------------------------------------------------|
| 1 | [Website watcher](./challenge-01-website-watcher.md) | requests, hashing, scheduling, logging |
| 2 | [PDF renamer](./challenge-02-pdf-renamer.md)         | pathlib, regex, third-party libs (`pypdf`) |

## Definition of done

For each challenge:

- The script runs successfully on a happy-path input.
- A `--dry-run` (or default-to-preview) mode exists for any state-modifying behavior.
- Errors are reported to stderr; success goes to stdout.
- The script exits 0 on success, non-zero on failure.
- README-like comments at the top explain how to invoke it.
- At least one **manual test plan** is described (what to type, what you expect to see).

If you can write a `pytest` test that exercises `main()` with mocked I/O, even better.
