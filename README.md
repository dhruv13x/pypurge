<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/pypurge/main/pypurge_logo.png" alt="pypurge logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/pypurge.svg)](https://pypi.org/project/pypurge/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/pypurge.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/pypurge/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/pypurge/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/pypurge/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/pypurge/graph/badge.svg)](https://codecov.io/gh/dhruv13x/pypurge)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/pypurge/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/pypurge.svg)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/pypurge.svg)](https://pypi.org/project/pypurge/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Docs -->
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://your-docs-link)

</div>


---

# 🧹 pypurge — Safe & Powerful Python Project Cleaner

**pypurge** is a production-grade Python cleanup utility designed to safely remove auto-generated files, caches, virtualenv leftovers, test artifacts, temporary files, and clutter — **without putting your system at risk.**

Think of it as a **precision broom for Python projects**.  
No more `find . -name __pycache__ -delete` or risky scripts — **clean confidently, with safety rails.**

---

## ✅ Key Features

- 🔐 **Safety-first design** — prevents accidental root-level deletion
- 🎯 **Python-specific cleanup**
  - `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `build/`, `dist/`, etc.
- 🧠 **Smart preview mode** — shows counts, groups & disk usage before deleting
- 🪪 **Stale lock & lockfile protection** — avoids multi-process conflicts
- 🕒 **Age-based filtering** — delete only items older than N days
- 📦 **Atomic backup mode** — zip backup with SHA256 manifest
- 🧪 Cleans testing & packaging leftovers
- 🧹 Optional **virtualenv purge**
- 💬 Colored interactive interface (or JSON for automation)
- 🛑 Root & dangerous directory protection
- ⚙️ Configurable via JSON (`.pypurge.json`)
- 🤖 Works safely in CI & scripts

---

## 📦 Installation

```bash
pip install pypurge

Or in development mode:

pip install -e .


---

🚀 Usage

Clean current project interactively

pypurge

Preview everything — no deletions

pypurge --preview

Clean without prompt (CI-safe)

pypurge --yes

Clean a specific folder

pypurge myproject/

Exclude files or directories

pypurge --exclude "*.log" --exclude "re:.*tmp.*"

Force deletion of stubborn files

pypurge --force

Run in non-interactive (quiet) mode

pypurge --quiet

Backup before deleting 🛟

pypurge --backup

Clean virtual environments too

pypurge --clean-venv

Delete only files older than 7 days

pypurge --older-than 7

Allow root / system scans (⚠️ expert mode)

pypurge --allow-root --allow-broad-root


---

✨ Example Output

=== Preview: grouped cleanup summary for .
Group                         Items   Size        Paths (truncated)
----------------------------------------------------------------------
Python Caches                 84      12.4MB
Testing/Linting/...           36      4.2MB
Build/Packaging               12      2.1MB

📁 Python Caches — 84 items, 12.4MB
  src/app/__pycache__/       — 340KB
  tests/__pycache__/         — 290KB
  ...
... and 60 more


---

### ⚙️ Advanced Usage & Configuration

While `pypurge` works great out of the box, you can fine-tune its behavior with command-line arguments or a configuration file.

#### CLI Arguments

| Argument                  | Short | Description                                                              | Default                  |
| ------------------------- | ----- | ------------------------------------------------------------------------ | ------------------------ |
| `root...`                 |       | Directories to clean.                                                    | `.` (current directory)  |
| `--preview`               | `-p`  | Preview targets without deleting anything.                               | `False`                  |
| `--yes`                   | `-y`  | Skip the interactive confirmation prompt.                                | `False`                  |
| `--quiet`                 | `-q`  | Suppress all output except for critical errors.                          | `False`                  |
| `--clean-venv`            |       | Include virtual environment directories (`.venv`, `venv`, etc.) in the scan. | `False`                  |
| `--exclude <pattern>`     |       | Exclude files/directories matching a glob or `re:` pattern.              | (none)                   |
| `--older-than <days>`     |       | Only target files older than `N` days.                                   | `0` (all ages)           |
| `--age-type <type>`       |       | Choose age metric: `mtime` (modified), `atime` (accessed), `ctime` (created). | `mtime`                  |
| `--force`                 |       | Attempt to `chmod` files to ensure deletion.                             | `False`                  |
| `--backup`                |       | Create a `.zip` backup of all targets before deletion.                   | `False`                  |
| `--backup-dir <path>`     |       | Specify a directory to store backups.                                    | (root of scan)           |
| `--backup-name <name>`    |       | Set a reproducible base name for backup archives.                        | (auto-generated)         |
| `--delete-symlinks`       |       | Also delete symbolic links (the link itself, not the target).            | `False`                  |
| `--config <path>`         |       | Path to a `.pypurge.json` configuration file.                            | (auto-detect in root)    |
| `--allow-broad-root`      |       | **DANGEROUS**: Allow running in broad directories like `/` or `$HOME`.     | `False`                  |
| `--allow-root`            |       | **DANGEROUS**: Allow running as the `root` user.                         | `False`                  |
| `--lockfile <name>`       |       | Name of the lockfile to prevent concurrent runs.                         | `.pypurge.lock`          |
| `--lock-stale-seconds <N>`|       | Time in seconds before a lock is considered stale.                       | `86400` (24 hours)       |
| `--log-file <path>`       |       | Path to a file for logging output.                                       | (none)                   |
| `--log-format <format>`   |       | Log format: `text` or `json`.                                            | `text`                   |
| `--no-color`              |       | Disable colored terminal output.                                         | `False`                  |
| `--version`               | `-v`  | Show the application version and exit.                                   | `False`                  |

#### Configuration File

You can create a `.pypurge.json` file in the root of your project to define custom patterns and exclusions:

```json
{
  "exclude_patterns": ["re:.*migrations.*", "data/"],
  "dir_groups": {
    "CustomData": ["temp_run/", "scratch/"]
  },
  "file_groups": {
    "Logs": ["*.log"]
  }
}
```

---

🔒 Safety Rules

By default pypurge REFUSES to run in:

/

$HOME

/usr, /etc, /bin, /sbin


Unless you explicitly pass:

--allow-broad-root

Running as root also requires:

--allow-root


---

### 🏗️ Architecture

The project follows a modular structure to separate concerns:

```
src/pypurge/
├── cli.py          # Main entry point, argument parsing
└── modules/
    ├── backup.py   # Atomic backup logic
    ├── deletion.py # Safe file/directory removal
    ├── locking.py  # Cross-process lock management
    ├── logging.py  # Logging setup
    ├── safety.py   # Guards against dangerous operations
    ├── scan.py     # Core target scanning logic
    ├── ui.py       # Rich terminal output
    └── utils.py    # Helper functions
```

The core logic flow is:
1.  **Parse Arguments**: `cli.py` handles user input.
2.  **Acquire Lock**: `locking.py` prevents concurrent runs in the same directory.
3.  **Scan for Targets**: `scan.py` identifies files and directories to be deleted based on predefined and custom patterns.
4.  **Confirm & Backup**: The user is prompted to confirm, and an optional backup is created using `backup.py`.
5.  **Delete**: `deletion.py` removes the targets.
6.  **Release Lock**: The lock is released.

---

### 🗺️ Roadmap

-   [ ] **Plugin System**: Allow users to define custom cleanup modules.
-   [ ] **More Output Formats**: Add support for `csv` or `html` reports.
-   [ ] **Configuration Wizard**: An interactive mode to generate a `.pypurge.json` file.

---

🤝 Trusted Publishing & CI

This project uses PyPI Trusted Publishing (OIDC) + GitHub Actions for secure releases.

Push tag to publish:

git tag v0.1.0
git push origin v0.1.0


---

🧠 Requirements

Python >= 3.8

- **rich** (for beautiful console output)



---

🪪 License

MIT © Dhruv


---

⭐ Support the Project

If this tool saved you from rm -rf nightmares…
Give it a ⭐ on GitHub — it helps a lot!


---