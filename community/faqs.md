# Frequently Asked Questions

## About the program

### Is this really free?

Yes. The curriculum is licensed under [GPL-3.0](../LICENSE) — you can read, copy, modify, redistribute, and even teach from it commercially, as long as derivative works stay open source. There are no paid tiers, no upsells, no required services.

### Do I get a certificate?

Not by default — we're a public curriculum, not an accredited institution. However:

- Your **public GitHub portfolio** is the certificate that actually matters to employers.
- Clubs and instructors running this as a cohort may issue their own.
- The Code Crunch Worldwide community recognizes capstone completions in our showcase.

### How long does it take?

Designed for ~36 hours/week × 15 weeks = ~540 hours full-time. Most learners take 6–12 months part-time. Pace yourself — finishing matters more than speeding.

### I have some Python experience. Can I skip ahead?

You can, but we recommend at least skimming earlier weeks for any gaps. Take the **quiz** at the start of each week — if you score above 80%, the topic is safe to skim.

### Can I use this to teach a course?

Yes! That's why we built it. See [CONTRIBUTING.md](../CONTRIBUTING.md) and please share your experience back with the community.

---

## About the work

### How much should a mini-project look like a "real" project?

By Week 5 your mini-projects should have:

- A `README.md` explaining what it does and how to run it.
- A `requirements.txt` or `pyproject.toml` listing dependencies.
- A `.gitignore`.
- Code organized in files, not one giant script.
- At least one test, by Week 11.

### Do I have to do every exercise?

The **homework** and **mini-project** are the must-dos. Exercises and challenges are "as many as you need to feel solid." Stretch goals are optional.

### My code works but it's ugly. Does that count?

Working code is the first goal. **Clean** code is the second goal, learned over time. Run `black` and `ruff` (see [coding standards](../resources/coding-standards.md)) and you'll catch 80% of style issues automatically.

### Can I use AI assistants (Copilot, ChatGPT, Claude)?

See [community/support.md § 6](support.md#6-using-ai-assistants-responsibly). Short answer: yes for explanations and review, no for "do my homework." You will not learn by copy-pasting LLM output.

---

## About the tools

### Why Python 3.11+ and not 3.x.y?

Python 3.11 introduced significant performance and error-message improvements that meaningfully help beginners (the [PEP 657](https://peps.python.org/pep-0657/) error locations are huge). 3.12 and 3.13 are even better. Use the newest stable release on your platform.

### Why VS Code and not PyCharm / Vim / etc.?

VS Code is free, cross-platform, has the lowest learning curve, and the largest Python-extension ecosystem. **Use whatever editor you like**, but our screenshots and tips assume VS Code. PyCharm Community Edition, Vim, and JetBrains Fleet are all excellent alternatives.

### Why Flask in Week 9 and not Django or FastAPI?

Flask is the smallest "real" web framework — perfect for one week of teaching the request/response cycle without burying you in conventions. Once you understand Flask, picking up FastAPI (which we touch on as a stretch) or Django is mostly learning their conventions, not new concepts.

### Why GPL-3.0 and not MIT?

GPL-3.0 ensures the curriculum stays open. If someone forks it and improves it, those improvements must remain open for everyone. MIT would allow proprietary forks — fine for libraries, but at odds with our mission for an educational resource.

---

## About careers

### Will this get me a job?

This curriculum will give you the *skills* to interview for entry-level Python roles. Getting a job also requires: networking, polishing a resume, practicing interviews, and lots of applications. Skill is necessary but not sufficient — keep that in mind.

### What kind of roles does this prepare me for?

- Python developer / backend engineer (entry-level)
- Data analyst (with extra SQL/dashboard practice)
- Junior data scientist (with more ML coursework on top)
- Automation / DevOps engineer (with more sysadmin practice)
- Technical roles at startups where Python is the lingua franca

### What should I do after Week 15?

- **Specialize.** Pick a track: web (Django/FastAPI), data (deep dive on pandas + SQL), ML (full Andrew Ng course), DevOps (Docker, K8s), or systems (C, Rust).
- **Contribute to open source.** Find a Python project on GitHub with "good first issue" labels.
- **Build more, larger projects.** Aim for 3–5 portfolio projects beyond the capstone.
- **Interview prep.** [LeetCode](https://leetcode.com), [NeetCode](https://neetcode.io), system design.

---

## About contributing

### I found a bug / typo. What do I do?

[Open an Issue](https://github.com/CODECRUNCHWORLDWIDE/C1-Code-Crunch-Convos/issues/new) or, even better, a Pull Request. See [CONTRIBUTING.md](../CONTRIBUTING.md).

### I want to translate a week into Spanish. How?

Awesome! See [CONTRIBUTING.md § Translations](../CONTRIBUTING.md#translations).

### Can I sponsor / donate?

Code Crunch Worldwide is a learner-led volunteer effort. We don't currently accept donations — but **starring the repo** and sharing it with friends helps more than you might think.

---

## Anything else?

Open a [Discussion](https://github.com/CODECRUNCHWORLDWIDE/C1-Code-Crunch-Convos/discussions) and we'll add to this FAQ.
