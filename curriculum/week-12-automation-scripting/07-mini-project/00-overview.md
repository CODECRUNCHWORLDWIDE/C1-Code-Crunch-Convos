# Mini-Project — File Organizer Bot

Build a CLI tool, `organize`, that takes a directory and tidies it into subfolders by file type: `Images/`, `Documents/`, `Code/`, `Archives/`, `Music/`, `Video/`, `Other/`. It can run once or watch a directory and react when new files appear. Every action is logged. The category-to-extension map is configurable via `config.json`.

This is the week's capstone. Spend 6–10 hours on it.

---

## What you're building

A single file (or small package) that exposes a CLI:

```bash
# Run once on a directory
python organize.py ~/Downloads --config sample-config.json --apply

# Preview what would happen (default — no --apply)
python organize.py ~/Downloads --config sample-config.json

# Watch and keep organizing as new files arrive
python organize.py ~/Downloads --config sample-config.json --watch --interval 5 --apply
```

When the bot runs, files are moved according to the config:

```text
Downloads/
├── Images/
│   ├── beach.jpg
│   └── chart.png
├── Documents/
│   ├── invoice.pdf
│   └── notes.md
├── Code/
│   └── script.py
├── Archives/
│   └── backup.zip
├── Other/
│   └── weird_thing.xyz
└── organize.log
```

---

## Requirements

### CLI (use `argparse`)

| Flag                  | Meaning                                                          |
|-----------------------|------------------------------------------------------------------|
| `DIRECTORY` (pos.)    | The folder to organize.                                          |
| `--config PATH`       | Path to `config.json`. Default: `./config.json`.                 |
| `--apply`             | Actually move files. Without it, dry-run.                        |
| `--watch`             | Keep running and re-check the directory every `--interval`s.     |
| `--interval SECONDS`  | Poll interval (only with `--watch`). Default 10.                 |
| `--log PATH`          | Append-only log file. Default: `<DIRECTORY>/organize.log`.       |
| `-v` / `--verbose`    | More verbose logging.                                            |

### Config file (JSON)

```json
{
  "Images":    [".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"],
  "Documents": [".pdf", ".docx", ".md", ".txt", ".rtf"],
  "Code":      [".py", ".js", ".ts", ".rs", ".go", ".java"],
  "Archives":  [".zip", ".tar", ".gz", ".7z", ".rar"],
  "Music":     [".mp3", ".wav", ".flac", ".ogg"],
  "Video":     [".mp4", ".mov", ".mkv", ".avi"],
  "Other":     []
}
```

The category whose extension list contains the file's suffix wins. Anything that doesn't match goes to the **first category with an empty list** (`Other` in the example).

### Behavior

- Skip directories — only move regular files.
- Skip files that are already inside a category folder (don't re-move).
- Skip the log file itself.
- Refuse to overwrite: if the destination exists, append a numeric suffix (`name-1.ext`, `name-2.ext`, …).
- Log every action to the log file *and* the terminal: `2026-05-13 10:00:00 INFO  moved beach.jpg -> Images/beach.jpg`.
- In dry-run mode, log `would move ...` instead of `moved ...`.
- Exit 0 on success, 1 on bad input (missing dir, malformed config), 2 on argparse error.

### Code quality

- Type hints on every public function.
- Use `pathlib.Path` everywhere — no raw string paths.
- Use `logging`, not `print`, for status output.
- Functions are small and individually testable.
- At least **two** unit tests using `pytest` and `tmp_path`.

---

## Hand-in checklist

- [ ] `organize.py` (or `organize/` package) runs from a clean venv.
- [ ] `config.json` provided. (You may use the supplied `sample-config.json`.)
- [ ] `README.md` (this file is fine — link from your project) describing the CLI.
- [ ] `tests/test_organize.py` with at least two passing tests.
- [ ] Sample run output committed to the README.

---

## Rubric (25 points)

| Category                                            | Pts |
|-----------------------------------------------------|-----|
| Correctness on the happy path                       | 5   |
| Dry-run default + `--apply` works as specified      | 3   |
| `--watch` polling implementation                    | 3   |
| Config loading + sensible "Other" fallback          | 2   |
| Collision-safe rename (`name-1.ext`)                | 2   |
| Logging to file + console                           | 2   |
| Type hints, `pathlib`, code organization            | 3   |
| `pytest` tests pass and cover non-trivial behavior  | 3   |
| README + sample run output                          | 2   |

**Pass: 15/25. Distinction: 21/25.**

---

## Hints

- `from pathlib import Path`
- `import shutil; shutil.move(str(src), str(dst))`
- `import json; json.loads(Path("config.json").read_text())`
- For collision-safe names:

  ```python
  def unique_path(dst: Path) -> Path:
      if not dst.exists():
          return dst
      stem, suffix = dst.stem, dst.suffix
      i = 1
      while True:
          candidate = dst.with_name(f"{stem}-{i}{suffix}")
          if not candidate.exists():
              return candidate
          i += 1
  ```

- For the watch loop, see `lecture-notes/02-file-system-and-subprocess.md` §4.
- For tests, `tmp_path` is a built-in pytest fixture that gives you a fresh temp directory.

Good luck. The first time you save 10 minutes of file shuffling because *your own script* did it for you is a great feeling.
