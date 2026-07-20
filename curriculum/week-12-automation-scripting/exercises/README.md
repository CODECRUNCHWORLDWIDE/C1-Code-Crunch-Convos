# Week 12 — Exercises

Five short, focused exercises. Each one targets a specific topic from the lectures and should take **20–40 minutes**. Read the lecture notes first; come back here for practice.

Run every script with `python <file>.py --help` first to see its CLI surface.

| # | File                              | Lecture          | Topic                          | Time     |
|---|-----------------------------------|------------------|--------------------------------|----------|
| 1 | `exercise-01-greet-cli.py`        | 01               | argparse basics                | 20 min   |
| 2 | `exercise-02-bulk-rename.py`      | 01 + 02          | argparse + pathlib             | 30 min   |
| 3 | `exercise-03-run-shell.py`        | 02               | subprocess, parsing output     | 25 min   |
| 4 | `exercise-04-scrape-quotes.py`    | 03               | requests + BeautifulSoup       | 35 min   |
| 5 | `exercise-05-schedule.py`         | 03               | schedule / time.sleep loop     | 25 min   |

## How to do these

1. **Read** the script's docstring and CLI help.
2. **Run** it as-is — make sure it works.
3. **Modify it** to do the "Stretch" task in each docstring.
4. **Optionally**: write a test for `main()` in a separate `test_*.py`.

## Dependencies

Most exercises use only the standard library. Two need extras:

```bash
pip install requests beautifulsoup4 schedule
```

Use a virtual environment.

## Solutions

Try the problem first. Solutions are intentionally not shipped — compare with a peer or with your instructor. The exercises are simple enough that you should know when your code is right (it produces the expected output and exits 0).
