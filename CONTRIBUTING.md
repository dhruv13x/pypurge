# Contributing to pypurge

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to `pypurge`. These are just guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md) (if available). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for `pypurge`. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

*   **Use a clear and descriptive title** for the issue to identify the problem.
*   **Describe the exact steps which reproduce the problem** in as much detail as possible.
*   **Provide specific examples** to demonstrate the steps.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for `pypurge`, including completely new features and minor improvements to existing functionality.

*   **Use a clear and descriptive title** for the issue to identify the suggestion.
*   **Provide a step-by-step description of the suggested enhancement** in as much detail as possible.
*   **Explain why this enhancement would be useful** to most `pypurge` users.

### Pull Requests

*   Fill in the required template
*   Do not include issue numbers in the PR title
*   Include screenshots and animated GIFs in your pull request whenever possible.
*   Follow the Python style guides (Black, Ruff).

## Development Setup

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/dhruv13x/pypurge.git
    cd pypurge
    ```

2.  **Install dependencies**:
    ```bash
    pip install -e ".[dev]"
    ```

3.  **Run tests**:
    ```bash
    tox
    ```
    or
    ```bash
    pytest
    ```

## Style Guide

*   Use [Black](https://github.com/psf/black) for code formatting.
*   Use [Ruff](https://github.com/astral-sh/ruff) for linting.
*   Write clean, documented code.

Thanks! ❤️
