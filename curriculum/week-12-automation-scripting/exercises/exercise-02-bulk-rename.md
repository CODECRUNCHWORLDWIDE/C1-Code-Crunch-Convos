# Exercise 2 — Bulk Rename

> **Topic:** `argparse` + `pathlib` — a destructive script that is safe by default
> **Lecture:** [01 — CLI Scripts with `argparse`](../lecture-notes/01-cli-scripts-with-argparse.md) and [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Medium
> **Target time:** 30 min
> **Why this one:** this is the first script you will write that can destroy something. Lecture 1 §10 shows a bulk renamer that previews by default; it is a good sketch and it is not safe enough to point at your photos folder, because it will happily rename a file over the top of another one. You are going to close that gap. The habits you build here — sandbox first, dry-run by default, refuse to clobber — are the difference between a tool you trust and a tool you run once and regret.

## The Brief

A folder of files has picked up a naming convention nobody wants any more.
Every filename with `draft` in it should say `final` instead. Doing it by hand
is fine for five files and impossible for five hundred.

Your script takes a directory, a substring to find, and a substring to put in
its place. It **previews** by default: one line per planned rename, nothing
touched. Only `--apply` moves any bytes.

The interesting part is what happens when two files want the same new name. If
`report draft.txt` and `report final.txt` both live in the folder, renaming the
first destroys the second. On macOS and Linux, `Path.rename` does that
silently — no error, no warning, the file is simply gone. Your script has to
notice and refuse.

A rename is not undoable. There is no recycle bin, no `Ctrl-Z`, and the
original names are written down nowhere. When you get the arguments slightly
wrong — a `--pattern` that matches more than you meant, a substring that turns
up inside a word you did not think about — your only chance to catch it is
*before* the change happens. So the safe thing is the default and the dangerous
thing needs a flag, never the other way round. You typing the wrong argument at
11pm is the risk, not the code being wrong.

## Set up a sandbox first

Do not run this on anything you care about. Build a throwaway folder next to
your script with files whose only purpose is to be renamed badly:

```bash
mkdir -p rename-sandbox/"old drafts"
cd rename-sandbox
touch "report draft.txt" "report final.txt" "budget draft.txt" "photo.png"
cd ..
```

In PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "rename-sandbox\old drafts"
foreach ($f in "report draft.txt", "report final.txt", "budget draft.txt", "photo.png") {
    New-Item -ItemType File -Path "rename-sandbox\$f"
}
```

Five things are in there on purpose. `budget draft.txt` renames cleanly.
`report draft.txt` collides with `report final.txt`. `photo.png` has no match.
And `old drafts` is a **directory** whose name contains `draft` — the trap a
naive loop renames along with everything else. (The shipped answer builds this
exact sandbox in a temp folder for you; you build one of your own to point your
own script at.)

## Starter

```python
"""exercise-02-bulk-rename.py — preview and apply bulk filename edits.

Replaces OLD with NEW in the names of files directly inside DIRECTORY.
Previews by default; renames only when --apply is passed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """Return the parser for the bulk renamer."""
    parser = argparse.ArgumentParser(
        prog="bulk-rename",
        description="Replace OLD with NEW in filenames inside DIRECTORY.",
    )
    parser.add_argument("directory", type=Path, help="Folder to operate on")
    parser.add_argument("old", help="Substring to look for in each filename")
    parser.add_argument("new", help="Replacement substring")
    parser.add_argument("--pattern", default="*",
                        help="Glob to limit the files considered (default: %(default)s)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename. Without this flag, only preview.")
    return parser


def plan_renames(directory: Path, old: str, new: str, pattern: str) -> list[tuple[Path, Path]]:
    """Return (source, target) pairs for files whose name contains old.

    Directories are ignored. Pairs where the name would not change are
    ignored. The list is sorted by source name so repeated runs print the
    same lines in the same order.
    """
    # TODO: build a list, skip anything that is not a file, use
    # path.with_name(path.name.replace(old, new)) for the target
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Preview or apply the planned renames. Return an exit code."""
    args = build_parser().parse_args(argv)

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    planned = plan_renames(args.directory, args.old, args.new, args.pattern)
    renamed = 0
    skipped = 0

    for source, target in planned:
        # TODO: if target.exists(), print the SKIP line, count it, continue
        # TODO: otherwise print DRY-RUN or RENAMED, and rename only if --apply
        ...

    # TODO: print the summary line, plus the --apply hint when previewing
    return 1 if skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. Preview lines are `DRY-RUN  <old name> -> <new name>`, two spaces after the
   label. Applied lines say `RENAMED  ` in the same column. Refusals say
   `SKIP     <old name> -> <new name> (target exists)`.
2. Print the **names**, not the full paths. The directory is already on the
   command line and repeating it on every line makes the output unreadable.
3. Directories are never renamed, whatever their name contains.
4. A file whose target already exists is skipped. Not overwritten, not
   renamed to `name (1).txt`, not prompted about — skipped, with a reason.
5. The summary is `N file(s) would be renamed, M skipped` when previewing and
   `N file(s) renamed, M skipped` after `--apply`. Previewing also prints
   `Re-run with --apply to make these changes.`
6. Exit 0 when everything you asked for happened. Exit 1 when it did not —
   either the directory was wrong, or at least one rename was refused.

## Constraints

- **Materialize the glob into a sorted list before you rename anything.**
  `Path.glob` is a lazy generator reading the directory as you iterate. Rename
  a file mid-iteration and the OS may hand you the new name again, or drop a
  file you had not reached yet — a class of bug you will never reproduce
  reliably. Sorting on top of that makes two runs comparable, because
  directory order is whatever the filesystem feels like today.
- **Use `path.with_name(...)`, never `str(path).replace(old, new)`.** The
  second edits the whole path string, so running it inside a folder named
  `rename-sandbox` with `old="rename"` rewrites the directory part too and
  your file lands somewhere you did not intend.
- **Check `target.exists()` before every rename, not once at the start.**
  Earlier renames in the same run create new files. A check done up front is
  already stale by the third file.
- **`--apply` guards the `path.rename()` call only.** Scanning, planning, and
  printing run identically in both modes. If the modes take different code
  paths, the preview stops predicting the real run, which is the only thing a
  preview is for.
- **No `shutil.rmtree`, no `unlink`, no cleanup of "leftovers".** This script
  renames. A tool that also deletes is a tool nobody can reason about.

## Expected output

The shipped answer, [`exercise-02-bulk-rename-solution.py`](./exercise-02-bulk-rename-solution.py),
builds the sandbox above inside a temp directory, drives `main()` across it —
preview, apply, then a second apply — and deletes the sandbox on the way out, so
it proves itself with no folder for you to build first. Yours points at a
sandbox of your own; the renamer is the same. Real captured output:

```text
$ python exercise-02-bulk-rename.py
Bulk Rename — proven headless on a sandbox this file builds and deletes.

Preview (the default — nothing on disk is touched):
DRY-RUN  budget draft.txt -> budget final.txt
SKIP     report draft.txt -> report final.txt (target exists)
1 file(s) would be renamed, 1 skipped
Re-run with --apply to make these changes.
[exit 1]

Apply (only --apply moves a byte):
RENAMED  budget draft.txt -> budget final.txt
SKIP     report draft.txt -> report final.txt (target exists)
1 file(s) renamed, 1 skipped
[exit 1]

Apply again — idempotent, the collision is still refused:
SKIP     report draft.txt -> report final.txt (target exists)
0 file(s) renamed, 1 skipped
[exit 1]
```

Notice what is **not** there: no line for `photo.png`, which has no match, and
no line for `old drafts`, which is a directory. Notice too that every run exits
1 — a refused rename is still a refusal, even in a preview, and a script in a
pipeline needs to hear about it.

## Steps

1. Build the sandbox with the commands above and list it, so you know the
   starting state by heart.
2. Implement `plan_renames`. Print the list and eyeball it before you write a
   single line that renames anything.
3. Implement the loop in `main()`, but leave `path.rename()` commented out.
   Run the preview and confirm it matches the first block above.
4. Uncomment the rename, run with `--apply`, then list the folder. Exactly one
   name should have changed.
5. Run the same `--apply` command again. This is the idempotence check from
   Lecture 1 §1: the second run must be harmless and must say so.
6. Now try to break it. Run with `--pattern "*.txt"`, then with `new` set to
   an empty string, then against a directory that does not exist. Each should
   fail politely or do nothing, never traceback.

## The Solution

The shipped file is your answer — `build_parser`, `plan_renames`, `describe`,
`main` — with a `demo()` that builds the sandbox, runs the three commands, and
tidies up. Your own file stops at `raise SystemExit(main())`; the demo exists so
a download can prove itself headless.

```python
"""exercise-02-bulk-rename-solution.py — the bulk renamer, proven headless.

The exercise part is the starter with its TODOs filled in: replace OLD with NEW
in the names of files inside DIRECTORY, previewing by default and moving a byte
only when --apply is passed, never clobbering an existing target.

Your own exercise-02-bulk-rename.py ends in ``raise SystemExit(main())`` and is
run from the shell against a sandbox you build by hand. A published answer
cannot ask you to build a folder first, so this file builds the exact sandbox
the exercise describes inside a temp directory, drives ``main()`` across it —
preview, apply, then a second apply to show the run is idempotent — and deletes
the sandbox on the way out. The renamer being tested is identical either way.

Run it with::

    python exercise-02-bulk-rename-solution.py
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

LABEL_WIDTH = 7


def build_parser() -> argparse.ArgumentParser:
    """Return the parser for the bulk renamer."""
    parser = argparse.ArgumentParser(
        prog="bulk-rename",
        description="Replace OLD with NEW in filenames inside DIRECTORY.",
    )
    parser.add_argument("directory", type=Path, help="Folder to operate on")
    parser.add_argument("old", help="Substring to look for in each filename")
    parser.add_argument("new", help="Replacement substring")
    parser.add_argument("--pattern", default="*",
                        help="Glob to limit the files considered (default: %(default)s)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename. Without this flag, only preview.")
    return parser


def plan_renames(directory: Path, old: str, new: str, pattern: str) -> list[tuple[Path, Path]]:
    """Return (source, target) pairs for files whose name contains old.

    Directories are ignored. Pairs where the name would not change are
    ignored. The list is sorted by source name so repeated runs print the
    same lines in the same order.
    """
    planned: list[tuple[Path, Path]] = []
    for source in sorted(directory.glob(pattern), key=lambda path: path.name):
        if not source.is_file():
            continue
        new_name = source.name.replace(old, new)
        if new_name == source.name:
            continue
        planned.append((source, source.with_name(new_name)))
    return planned


def describe(label: str, source: Path, target: Path, note: str = "") -> str:
    """Format one output line: a fixed-width label, then old -> new."""
    line = f"{label:<{LABEL_WIDTH}}  {source.name} -> {target.name}"
    return f"{line} {note}" if note else line


def main(argv: list[str] | None = None) -> int:
    """Preview or apply the planned renames. Return an exit code."""
    args = build_parser().parse_args(argv)

    if not args.directory.is_dir():
        print(f"error: {args.directory} is not a directory", file=sys.stderr)
        return 1

    planned = plan_renames(args.directory, args.old, args.new, args.pattern)
    renamed = 0
    skipped = 0

    for source, target in planned:
        if target.exists():
            print(describe("SKIP", source, target, "(target exists)"))
            skipped += 1
            continue
        print(describe("RENAMED" if args.apply else "DRY-RUN", source, target))
        if args.apply:
            source.rename(target)
        renamed += 1

    verb = "renamed" if args.apply else "would be renamed"
    print(f"{renamed} file(s) {verb}, {skipped} skipped")
    if not args.apply:
        print("Re-run with --apply to make these changes.")
    return 1 if skipped else 0


# --------------------------------------------------------------------------- #
# The headless demo — the sandbox from the exercise page, built in a temp
# directory and deleted when the ``with`` block ends. Your own file has no
# demo; you point it at a sandbox you built yourself.
# --------------------------------------------------------------------------- #


def demo() -> None:
    """Build the exercise sandbox, drive the renamer over it, then tidy up."""
    print("Bulk Rename — proven headless on a sandbox this file builds and deletes.")
    print()
    with tempfile.TemporaryDirectory(prefix="rename-sandbox-") as tmp:
        sandbox = Path(tmp)
        for name in ("budget draft.txt", "report draft.txt",
                     "report final.txt", "photo.png"):
            (sandbox / name).write_text("", encoding="utf-8")
        (sandbox / "old drafts").mkdir()  # a directory whose name contains 'draft'
        target = str(sandbox)

        print("Preview (the default — nothing on disk is touched):")
        code = main([target, "draft", "final"])
        print(f"[exit {code}]")
        print()

        print("Apply (only --apply moves a byte):")
        code = main([target, "draft", "final", "--apply"])
        print(f"[exit {code}]")
        print()

        print("Apply again — idempotent, the collision is still refused:")
        code = main([target, "draft", "final", "--apply"])
        print(f"[exit {code}]")


if __name__ == "__main__":
    demo()
```

**`plan_renames` decides; `main` acts.** `plan_renames` reads the directory and
returns a list. It renames nothing, prints nothing, and exits nothing. That is
why a preview mode was even possible to add: the plan exists as data before
anything happens to it. Had the target path been computed inside the `rename()`
call, there would be no plan to print and no dry run to write.

**`sorted(directory.glob(pattern), ...)` does two jobs in one expression.**
`Path.glob` is a lazy generator that reads the directory as you iterate it.
Renaming a file while that generator is still open means mutating the thing you
are reading. `sorted()` drains it completely, first, into a list — after which
the directory can change all it likes and your list does not. The second job is
determinism: directory order is whatever the filesystem hands back, so without
the sort, two runs of the preview can print the same lines in a different order
and you cannot diff them against each other. The sort key is `path.name`, not
the `Path` itself, so the printed names sort the way they read.

**`with_name` edits the filename; `str(path).replace` edits the whole path.**
Run the renamer inside a folder called `rename-sandbox` with `old="rename"` and
`with_name` gives you `rename-sandbox\budget final.txt` while `str().replace`
gives you `backup-sandbox\budget draft.txt` — it has silently changed which
directory the file is going to.

**`target.exists()` is checked inside the loop, once per file.** Earlier
renames in the same run create new files, so a check performed once at the start
is stale by the second iteration. `Path.rename` refuses to clobber on Windows
and silently clobbers on POSIX, so the answer cannot lean on the OS being
careful — the check is what gives you the same behaviour everywhere.

**`describe()` is one format string for all three labels.** Written as three
separate f-strings, the column alignment is three counted-by-hand runs of spaces
that drift the first time someone renames a label. `f"{label:<7}  "` is one
left-justified seven-wide field plus two spaces, and `SKIP` pads itself.

**`renamed` counts the same thing in both modes.** It is incremented after the
skip check and outside the `if args.apply:`, so a dry run and a real run compute
an identical number. That is the entire contract of a preview: the number you
are shown is the number you will get. The only line that behaves differently
between the two modes is `source.rename(target)`.

## Run it

Copy the worked answer on this page into `exercise-02-bulk-rename.py` and run it:

```bash
python exercise-02-bulk-rename.py
```

It needs nothing but the standard library, builds its own sandbox in a temp
folder, and deletes it when it finishes — it never touches a file of yours.
Because the answer is pure stdlib, you can also
[run it in the online editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-12-automation-scripting/exercises/exercise-02-bulk-rename.md).
The `-solution` in the name keeps it from colliding with your own
`exercise-02-bulk-rename.py`.

## Common bugs to catch

- **`FileExistsError: [WinError 183] Cannot create a file when that file
  already exists: 'report draft.txt' -> 'report final.txt'`.** You skipped the
  `target.exists()` check and you are on Windows, where the OS refuses. On
  macOS and Linux the same code raises nothing and the target file is
  destroyed. The platform that crashed did you a favor.
- **The folder `old drafts` becomes `old finals`.** You iterated
  `directory.glob(pattern)` without `path.is_file()`. A glob of `*` matches
  directories too, and a tool that renames directories when you asked it to
  rename files is a tool that will one day rename the folder your project
  lives in.
- **A file appears twice in the output, or one goes missing.** You renamed
  inside the `for path in directory.glob(...)` loop. Build the list first,
  then iterate the list. This one depends on the filesystem and the entry
  count, so it passes on your laptop and eats a file on someone else's.
- **`AttributeError: 'str' object has no attribute 'is_dir'`.** You forgot
  `type=Path` on the `directory` argument, so `args.directory` is still a
  string. Everything from argparse is a string until a `type=` says otherwise.
- **Every filename prints as `rename-sandbox/budget draft.txt`.** You printed
  the `Path` instead of `path.name`.
- **`0 file(s) would be renamed` when you can see matching files.** Your
  substring check is case-sensitive and the files say `Draft`. Decide whether
  that is the behavior you want, then say so in the `--help` text either way.
- **The preview and the real run disagree.** You put part of the planning
  logic behind `if args.apply:`. Only the `rename()` call belongs there.

## Under the hood

<details>
<summary>Under the hood — why iterating a directory you are changing is a real trap, not a style nit</summary>

`Path.glob` returns a generator that walks the directory's entries lazily —
it reads them from the filesystem as you ask for the next one, not all at once.
That is efficient, and it is a landmine when the loop body changes the very
directory being walked. The operating system does not promise that a directory
listing stays stable while you mutate it: a rename can make an entry you already
saw appear again under its new name, or push an entry you had not reached out of
the window the OS hands back, so it is silently skipped.

On the NTFS run captured for this exercise — five entries, Windows 11 — the
naive "rename as you iterate" loop behaved perfectly, saw each name once, and
renamed the right two files. That is exactly why the bug is dangerous: it
depends on the filesystem, the entry count, and where in the listing the rename
lands, so it passes every test on your machine and corrupts someone else's. The
fix is one word: `sorted(...)` drains the generator into a list before the loop
body runs, and after that the list is a fixed snapshot the renames cannot
disturb.

</details>

## Acceptance checklist

- [ ] Running with no `--apply` changes nothing on disk, verified by listing
      the folder before and after.
- [ ] `report draft.txt` still exists and `report final.txt` is untouched
      after an `--apply` run.
- [ ] The directory `old drafts` is never renamed.
- [ ] A second `--apply` run reports `0 file(s) renamed` and exits 1.
- [ ] A nonexistent directory prints to stderr and exits 1, with no traceback.
- [ ] The file is committed to Git with a message like
      `Add Week 12 exercise 2: bulk rename with dry-run default`.

## Stretch

- Add `--recursive` that swaps `glob` for `rglob`. Decide first what happens
  when a nested file and a top-level file end up with the same target name.
- Add `-v/--verbose` with `action="count"` and route the per-file lines
  through `logging` at INFO, keeping only the summary on `print`. Lecture 1 §10
  shows the verbosity-to-level arithmetic.
- Write the plan to a JSON file before applying it, and add `--undo FILE` that
  reverses every rename that file recorded. It is the closest thing to an undo
  button a filesystem tool can have.

When your sandbox survives every run, move on to
[Exercise 3 — Run Shell](./exercise-03-run-shell.md).
