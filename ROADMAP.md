# 🗺️ Strategic Roadmap (V3.0)

This document serves as the **Master Plan** for `pypurge`. It balances **Innovation**, **Stability**, and **Debt** to transform the tool from a utility into an ecosystem.

> **Legend**:
> - `[Debt]`: Technical debt, refactoring, or maintenance.
> - `[Feat]`: New user-facing feature.
> - `[Bug]`: Bug fix or stability improvement.
> - **Size**: `S` (Days), `M` (Weeks), `L` (Months), `XL` (Quarter).

---

## 🏁 Phase 0: The Core (Stability & Debt)
**Goal**: Solid foundation. Ensure the current codebase is bulletproof before scaling.

- [x] **Testing**: Maintain Coverage > 85% `[Debt]` `S`
    - *Status*: Current coverage is ~94%.
- [x] **CI/CD**: Linting (Ruff/Black), Type Checking (mypy) `[Debt]` `S`
    - *Status*: Enforced via `tox`.
- [ ] **Documentation**: Comprehensive README & Architecture Diagrams `[Feat]` `M`
    - *Detail*: Add Mermaid diagrams to `README.md` to explain the safety logic.
- [ ] **Refactoring**: Decouple `scan.py` for better testability `[Debt]` `M`
    - *Detail*: Simplify nested logic to prepare for Async IO.

## 🚀 Phase 1: The Standard (Feature Parity)
**Goal**: Competitiveness. Match and exceed standard industry expectations.

- [ ] **UX**: Interactive TUI Dashboard `[Feat]` `L` *Requires Phase 0*
    - *Detail*: Use `Textual` or `Rich` for a clickable file selection interface.
- [ ] **Reporting**: HTML/CSV Audit Reports `[Feat]` `M` *Requires Phase 0*
    - *Detail*: Generate compliance-ready artifacts of deleted files.
- [ ] **Config**: Robust Settings Management `[Feat]` `S` *Requires Phase 0*
    - *Detail*: Support global `~/.pypurge.json` cascading to local config.
- [ ] **Performance**: Async IO Scanning `[Feat]` `L` *Requires Refactoring*
    - *Detail*: Parallelize file walking for large monorepos.

## 🔌 Phase 2: The Ecosystem (Integration)
**Goal**: Interoperability. Allow other tools to build on top of `pypurge`.

- [ ] **API**: Decouple CLI from Core (SDK Mode) `[Feat]` `XL` *Requires Phase 1*
    - *Detail*: Allow `import pypurge; pypurge.clean()` for Python scripts.
- [ ] **Plugins**: Extension System `[Feat]` `L` *Requires API*
    - *Detail*: Load external modules (e.g., `pypurge-django`, `pypurge-rust`).
- [ ] **Integrations**: Pre-commit Hooks `[Feat]` `S` *Requires Phase 1*
    - *Detail*: Official hook to clean artifacts before commit.

## 🔮 Phase 3: The Vision (Innovation)
**Goal**: Market Leader. Features that no other cleanup tool has.

- [ ] **AI**: LLM-based "Junk" Detection `[Feat]` `XXL` *Requires Phase 2*
    - *Detail*: Analyze file names and content to suggest deletions for unknown patterns.
- [ ] **Time Machine**: Git-aware historic analysis `[Feat]` `XL` *Requires Phase 1*
    - *Detail*: "What would have been deleted 3 days ago?" based on git history.
- [ ] **Cloud**: Team Policy Sync (K8s/Docker compatible) `[Feat]` `L` *Requires Phase 2*
    - *Detail*: Enforce cleanup rules across a distributed team or CI runners.
