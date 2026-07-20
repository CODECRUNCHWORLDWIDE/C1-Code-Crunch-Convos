# Contributing to Code Crunch Convos

Thank you for considering a contribution. This curriculum belongs to the community — every learner who passes through can help make it better for the next.

By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Ways to Contribute

You don't need to be an expert to contribute. Useful contributions include:

- 🐛 **Fixing typos, broken links, or unclear instructions**
- 🧪 **Adding or improving exercises, challenges, or quiz questions**
- 📝 **Improving lecture notes** — clearer explanations, better examples
- 🌐 **Translating** a week (or the whole curriculum) into another language
- 🧑‍🏫 **Sharing teaching notes** if you've run this as a cohort
- 🔧 **Improving tooling** — CI, formatting, testing scripts
- 💡 **Proposing new modules or stretch topics** via a Discussion or Issue

If you're unsure whether your idea is welcome, **open an Issue or Discussion first** — we'll happily talk it through.

---

## Getting Set Up

```bash
# 1. Fork on GitHub, then clone your fork
git clone https://github.com/<your-username>/C1-Code-Crunch-Convos.git
cd C1-Code-Crunch-Convos

# 2. Add the upstream remote
git remote add upstream https://github.com/CODE-CRUNCH-CLUB/C1-Code-Crunch-Convos.git

# 3. Create a virtual environment
python -m venv .venv
source .venv/bin/activate         # macOS / Linux
.venv\Scripts\activate            # Windows

# 4. (Optional) install dev tools used by exercises
pip install ruff black pytest
```

---

## Workflow

1. **Sync with upstream** before starting:

   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a topic branch.** Use a short, descriptive name:

   ```bash
   git checkout -b fix/week-03-typo
   git checkout -b feat/week-08-stretch-rate-limiting
   git checkout -b docs/improve-getting-started
   ```

3. **Make your changes.** Keep commits focused — one logical change per commit.

4. **Run the checks** (if your change touches Python code):

   ```bash
   ruff check .
   black --check .
   pytest           # if tests exist for the area you touched
   ```

5. **Commit with a clear message.**

   ```text
   fix(week-03): correct off-by-one in loop example

   The range() in lecture-notes/03-while-loops.md was iterating
   0..9 but the prose described 1..10.
   ```

6. **Push and open a Pull Request** against `main`.

7. A maintainer will review. We aim for first response within **7 days**. Be patient — this is a volunteer-run project.

---

## Contributing Curriculum

When adding or editing weekly content, keep these standards:

### Voice & style

- Write for the **absolute beginner**. Define jargon the first time you use it.
- Use the **second person** ("you'll write a function…") not the imperial "we".
- Prefer **short paragraphs** and **runnable code samples** over long prose.
- Show one concept at a time. A 20-line example that introduces five new ideas is a teaching failure.
- Every code block should specify the language: ` ```python ` not ` ``` `.

### Citations

- Link to the **official Python docs** wherever possible (https://docs.python.org).
- Cite a primary source for any factual claim (PEPs, library docs, original papers).
- Use the [PEP system](https://peps.python.org/) when referencing language design decisions.

### Exercise design

Every exercise should have:

- A clear, single learning objective.
- A worked example or hint, if it introduces a new pattern.
- A way to verify correctness (expected output, doctest, or pytest stub).
- An estimated time-to-complete (~5–30 minutes for exercises; 30–90 for challenges).

### Reusing copyrighted material

**Don't.** This is a GPL-3.0 project — only contribute material you wrote yourself or that is compatibly licensed (CC0, CC-BY, MIT, Apache-2.0, GPL-compatible). Always credit the original author.

---

## Translations

We welcome translations into any language.

- Create a top-level folder: `translations/<language-code>/` (use ISO 639-1, e.g. `es`, `fr`, `pt-BR`).
- Mirror the structure of the original `curriculum/` tree.
- Keep code samples and identifiers in English (`def add_numbers(a, b):` not `def sumar_numeros(...)`) so learners can match what they see in real-world codebases — but translate **all surrounding prose**.
- Open a single PR per week you translate; smaller PRs are easier to review.

---

## Pull Request Checklist

Before opening a PR, please confirm:

- [ ] My branch is up to date with `upstream/main`.
- [ ] My commits have descriptive messages.
- [ ] I've checked spelling and grammar.
- [ ] All code blocks specify a language.
- [ ] All links work and use relative paths within the repo where possible.
- [ ] If I added Python files, they pass `ruff check` and `black --check`.
- [ ] If I added exercises, I included expected output or a test stub.
- [ ] I have not committed any personal info, API keys, or `.env` files.

---

## Code of Conduct

Read and follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). We take it seriously.

## License

By contributing, you agree that your contributions will be licensed under **GPL-3.0**, the same license as the rest of the project.

---

Thank you! Every typo fix, every clearer example, every new exercise pushes this resource forward for thousands of future learners. 🚀
