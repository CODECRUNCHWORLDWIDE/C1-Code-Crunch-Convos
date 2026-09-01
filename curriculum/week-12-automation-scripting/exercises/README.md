# Week 12 — Exercises

Five short, focused exercises. Each one targets a specific topic from the lectures and should take **20–40 minutes**. Read the lecture notes first; come back here for practice.

Each exercise is a page, not a file you download. The page gives you the brief, a starter you copy into your own `.py` file in your practice repo, the exact output to aim for, and the bugs to expect. You create the file, you run it, you own it.

## Index

| # | Exercise                                                        | Lecture | Topic                      | Difficulty | Time   |
|---|-----------------------------------------------------------------|---------|----------------------------|-----------:|-------:|
| 1 | [exercise-01-greet-cli.md](./exercise-01-greet-cli.md)           | 01      | argparse basics            | Beginner   | 20 min |
| 2 | [exercise-02-bulk-rename.md](./exercise-02-bulk-rename.md)       | 01 + 02 | argparse + pathlib         | Medium     | 30 min |
| 3 | [exercise-03-run-shell.md](./exercise-03-run-shell.md)           | 02      | subprocess, parsing output | Medium     | 25 min |
| 4 | [exercise-04-scrape-quotes.md](./exercise-04-scrape-quotes.md)   | 03      | requests + BeautifulSoup   | Medium     | 35 min |
| 5 | [exercise-05-schedule.md](./exercise-05-schedule.md)             | 03      | schedule / time.sleep loop | Easy       | 25 min |

## How to do these

1. **Read** the whole page before you type anything, including the Common bugs section.
2. **Create** the `.py` file the page names — for exercise 1, `exercise-01-greet-cli.py` — and paste the starter in.
3. **Fill in** the `# TODO:` markers.
4. **Run** it and compare against the Expected output block, character for character. Then run `python exercise-01-greet-cli.py --help` and read the help text as if you had never seen the tool.
5. **Work the checklist** at the bottom of the page. Commit when every box is ticked.
6. **Optionally**: write a test for `main()` in a separate `test_*.py`. Every starter takes `main(argv=None)` specifically so you can.

## Safety

Two of these exercises touch things you cannot get back.

- **Exercise 2 renames files.** Build the throwaway sandbox folder the page describes and point the script at that, never at anything real. The script previews by default and needs `--apply` before it moves a byte. Keep it that way.
- **Exercise 4 fetches web pages.** It targets `https://quotes.toscrape.com`, a site published for practice, and it has no flag to repoint it. Every other site has Terms of Service and a `robots.txt` that you read *before* you write the script.

## Dependencies

Most exercises use only the standard library. Two need extras:

```bash
pip install requests beautifulsoup4 schedule
```

Use a virtual environment.

## Solutions

Try the problem first, then check yourself. Each exercise page carries its own worked answer under `## The Solution`, plus a downloadable `-solution.py` beside it that runs headless and prints the page's Expected output. Read the answer only after your own version produces that output and exits 0 — the twenty minutes you spend before you scroll down are the whole point of a short exercise.
