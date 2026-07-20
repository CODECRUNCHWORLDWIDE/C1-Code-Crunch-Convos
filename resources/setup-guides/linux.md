# Linux Setup Guide

Tested on Ubuntu 22.04+ and Debian 12+. Commands map cleanly to Fedora, Arch, etc. — adjust the package manager as needed.

## 1. Update your package list

```bash
sudo apt update && sudo apt upgrade -y
```

## 2. Install Python 3.11+

Most modern distros ship Python 3.10+. Check what you have first:

```bash
python3 --version
```

If it's older than 3.11, install a newer version:

### Ubuntu/Debian

```bash
sudo apt install -y python3 python3-pip python3-venv
```

For newer Python versions on older Ubuntu, use the deadsnakes PPA:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv
```

### Fedora

```bash
sudo dnf install -y python3 python3-pip
```

### Arch

```bash
sudo pacman -S python python-pip
```

## 3. Install Git

```bash
sudo apt install -y git        # Debian/Ubuntu
sudo dnf install -y git        # Fedora
sudo pacman -S git             # Arch
```

Configure your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## 4. Install VS Code

The cleanest method is the official Microsoft repo:

```bash
sudo apt install -y wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
rm packages.microsoft.gpg
sudo apt update
sudo apt install -y code
```

On Arch, use the AUR: `yay -S visual-studio-code-bin`.

Or use **Flatpak / Snap** if you prefer sandboxed installs.

## 5. Install VS Code extensions

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
```

## 6. Test your setup

```bash
mkdir -p ~/python-bootcamp && cd ~/python-bootcamp
echo 'print("Hello, world!")' > hello.py
python3 hello.py
```

You should see `Hello, world!`. ✅

## Common issues

- **`pip install` says "externally-managed-environment"** — modern distros (Debian 12+, Ubuntu 23.04+) prevent system-wide pip installs. Use a virtual environment (we cover this in Week 1).
- **`python` command not found** — use `python3`. Optionally add `alias python=python3` to `~/.bashrc` or `~/.zshrc`.

## What's next

You're ready. Continue to [Week 1 — Python Foundations](../../curriculum/week-01-python-foundations/).
