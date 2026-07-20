# macOS Setup Guide

Tested on macOS 12 Monterey and later. Should work on any recent Mac, Intel or Apple Silicon.

## 1. Install Homebrew (recommended)

[Homebrew](https://brew.sh) is the standard package manager for macOS. It makes installing developer tools painless.

Open the **Terminal** app and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After it finishes, follow the on-screen instructions to add Homebrew to your `PATH`. Verify:

```bash
brew --version
```

## 2. Install Python 3.11+

```bash
brew install python@3.12
```

Verify:

```bash
python3 --version    # → Python 3.12.x
```

> **Tip.** Use `python3` (not `python`) on macOS. Many guides use `python` but macOS reserves that for a now-removed system Python. Alias it if you want: add `alias python=python3` to your `~/.zshrc`.

## 3. Install Git

```bash
brew install git
git --version
```

Then configure your identity (this attaches your name to every commit you make):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## 4. Install VS Code

```bash
brew install --cask visual-studio-code
```

Or download from [code.visualstudio.com](https://code.visualstudio.com/).

Verify the `code` command works from the terminal:

```bash
code --version
```

If `code` is not found, open VS Code → `Cmd+Shift+P` → search **"Shell Command: Install 'code' command in PATH"**.

## 5. Install VS Code extensions

Run these in the terminal:

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
```

## 6. Test your setup

Create a folder and a tiny Python file:

```bash
mkdir ~/python-bootcamp && cd ~/python-bootcamp
echo 'print("Hello, world!")' > hello.py
python3 hello.py
```

You should see `Hello, world!`. ✅

## Common issues

- **`command not found: python3`** — re-run `brew install python@3.12` and make sure your terminal restarts after install. On Apple Silicon Macs you may also need to add `/opt/homebrew/bin` to your `PATH`.
- **Permission errors when running `pip`** — never use `sudo pip`. Always use a [virtual environment](../../curriculum/week-01-python-foundations/lecture-notes/) instead.

## What's next

You're ready. Go to [Week 1 — Python Foundations](../../curriculum/week-01-python-foundations/).
