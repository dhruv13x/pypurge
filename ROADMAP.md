# 🗺️ Project Roadmap

Welcome to the **Master Plan** for `pypurge`. This document outlines our trajectory from a solid utility to a legendary, ecosystem-defining tool. We categorize our goals by ambition, stability, and integration depth.

---

## Phase 1: Foundation (CRITICALLY MUST HAVE) - Q1
**Focus**: Core functionality, stability, security, and basic usage.
*Prioritizing items that are partially built or standard for this type of tool.*

- [x] **Core Python Cleanup**: Safely remove `__pycache__`, `.pyc`, `build/`, `dist/`, and `.egg-info`.
- [x] **Safety Architecture**: Root directory protection (`/`, `$HOME`) and stale lockfile handling.
- [x] **Smart Preview**: Detailed dry-run mode (`--preview`) showing exactly what will happen.
- [x] **Concurrency Control**: robust `.pypurge.lock` implementation to prevent race conditions.
- [x] **Configuration Wizard**: Interactive `pypurge --init` to generate JSON configs.
- [x] **Age-Based Filtering**: cleaning based on `mtime`, `atime`, or `ctime` (`--older-than`).
- [x] **Atomic Backups**: Zip-based backups with manifests before deletion.
- [x] **CI/CD Readiness**: JSON log formatting (`--log-format json`) and non-interactive modes (`--yes`).
- [x] **.gitignore Awareness**: Respect `.gitignore` files to avoid cleaning untracked but necessary files (Gap Analysis).
- [ ] **Advanced Config Validation**: Strict schema validation for `.pypurge.json` to prevent runtime errors.

---

## Phase 2: The Standard (MUST HAVE) - Q2
**Focus**: Feature parity with top competitors, user experience improvements, and robust reporting.

- [ ] **Shell Completions**: Native auto-completion for `bash`, `zsh`, and `fish` to speed up CLI usage.
- [ ] **Structured Reporting**: Generate audit reports in **HTML** and **CSV** formats for compliance and analysis.
- [ ] **Interactive TUI Dashboard**: Upgrade the confirmation prompt to a rich, interactive Terminal User Interface (using `Textual` or `Rich`) allowing users to toggle specific files before confirming.
- [ ] **Plugin Architecture**: A lightweight system for loading external cleanup modules (e.g., `pypurge-django`).
- [ ] **"Undo" Capability**: A dedicated `pypurge --restore <backup_id>` command to easily apply atomic backups.

---

## Phase 3: The Ecosystem (INTEGRATION & SHOULD HAVE) - Q3
**Focus**: Webhooks, API exposure, 3rd party plugins, SDK generation, and extensibility.

- [ ] **Pre-commit Hook**: Official support for `pre-commit` to sanitize repos before pushing.
- [ ] **Modern Tooling Integrations**: Specialized cleaning for `poetry` (cache), `uv` (venvs), and `hatch` environments.
- [ ] **SDK / Library Mode**: Decouple the CLI from the core logic, exposing a stable Python API (`import pypurge`) for other tools to build upon.
- [ ] **IDE Extensions**: VS Code and PyCharm extensions to "Right Click -> Purge" specific folders.
- [ ] **Webhooks & Notifications**: Send a payload to Slack/Discord/Teams summarizing the cleanup results (Space saved, file count).

---

## Phase 4: The Vision (GOD LEVEL) - Q4+
**Focus**: "Futuristic" features, AI integration, advanced automation, and industry-disrupting capabilities.

- [ ] **AI-Powered "Junk" Detection**: Train a lightweight model to identify redundant or "dead" files that don't match standard patterns but haven't been touched in years.
- [ ] **The "Time Machine"**: Deep integration with Git to identify build artifacts that *should* be ignored but aren't, comparing filesystem state vs. git index history.
- [ ] **Polyglot Cleaning**: Extend beyond Python to intelligently clean hybrid projects (e.g., `node_modules` in a Django React app, `target/` in Rust extensions).
- [ ] **Cloud Sync Configuration**: Sync your preferred cleanup rules and "Safe Lists" across your entire engineering team via a remote config URL.

---

## The Sandbox (OUT OF THE BOX / OPTIONAL)
**Focus**: Wild, creative, experimental ideas that set the project apart.

- [ ] **"The Vacuum" Daemon**: A background service that watches directories and auto-cleans them based on rules (Risky, but powerful).
- [ ] **Disk Usage Flame Graph**: A visual CLI flame graph to show exactly where the space is going before you delete it.
- [ ] **Gamification**: "Space Ranger" badges and leaderboards for bytes reclaimed.
