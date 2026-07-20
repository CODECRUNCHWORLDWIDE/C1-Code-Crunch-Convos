# Windows Setup Guide

Tested on Windows 10 and 11.

## 1. Install Python 3.11+

1. Download the **Windows installer (64-bit)** from [python.org/downloads](https://www.python.org/downloads/).
2. Run it. **CRITICAL:** Check the box **"Add python.exe to PATH"** at the bottom of the first screen before clicking *Install Now*.
3. After installation, open **PowerShell** and verify:

   ```powershell
   python --version    # → Python 3.12.x
   pip --version
   ```

If `python` opens the Microsoft Store, see "Common issues" below.

## 2. Install Git

1. Download Git from [git-scm.com/download/win](https://git-scm.com/download/win).
2. During installation, accept the defaults. Choose **"Visual Studio Code"** as the default editor if asked.
3. Verify:

   ```powershell
   git --version
   ```

Then configure your identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## 3. Install VS Code

Download and install from [code.visualstudio.com](https://code.visualstudio.com/).

During installation, check **"Add to PATH"** and **"Register Code as an editor for supported file types"**.

Verify:

```powershell
code --version
```

## 4. Install VS Code extensions

In PowerShell:

```powershell
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
```

## 5. Test your setup

```powershell
mkdir python-bootcamp
cd python-bootcamp
echo "print('Hello, world!')" > hello.py
python hello.py
```

You should see `Hello, world!`. ✅

## (Optional) Use WSL for a Linux-like experience

If you want a Linux development environment without leaving Windows, install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install):

```powershell
wsl --install
```

Then follow the [Linux setup guide](linux.md) inside your WSL terminal. Many professional Python developers use WSL on Windows.

## Common issues

- **Typing `python` opens the Microsoft Store** — the installer didn't add Python to `PATH`. Either re-run the installer with the *Add to PATH* checkbox, or open **Settings → Apps → Advanced app settings → App execution aliases** and turn off the `python.exe` aliases.
- **`pip` not found** — close and reopen PowerShell. If still missing, re-run the Python installer and choose **Modify → Add Python to environment variables**.
- **PowerShell script execution policy blocks venv activation** — run once in an admin PowerShell:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

## What's next

You're ready. Head to [Week 1 — Python Foundations](../../curriculum/week-01-python-foundations/).
