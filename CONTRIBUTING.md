# Contributing

Thanks for considering a contribution to Reliable AI Lab. Contributions should stay focused, reproducible, and safe to run locally.

## Quick contribution workflow

1. **Fork** the repository on GitHub.
2. Clone your fork and create a focused branch:
   ```bash
   git clone https://github.com/YOUR-USERNAME/reliable-ai-lab.git
   cd reliable-ai-lab
   git checkout -b feature/short-description
   ```
3. Install the project and development dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -e '.[dev]'
   ```
   On Windows, activate with `.venv\Scripts\activate`.
4. Make one focused change and add or update tests.
5. Run:
   ```bash
   python -m pytest
   ```
6. Push the branch to your fork and open a pull request against `main`.

New contributors can start with issues labeled **good first issue**. Issues labeled **help wanted** are open for community contributions.

## Before opening a bug report

Open an issue with a reproducible example: the project, input, Python and dependency versions, expected behavior and actual result. Use synthetic data or data you have permission to share.

## Engineering expectations

Keep changes focused. Add a test for a bug fix and run `python -m pytest` before submitting a pull request.

For model or statistical changes, separate fitting, calibration and evaluation data. Name the baseline and include negative results. Synthetic examples are not evidence of production improvement.

Do not add automatic infrastructure execution or send input to an external service without an explicit opt-in. Attribute any external code and check dataset and model licenses.

## Pull request checklist

- The change has a clear purpose and stays within the issue/PR scope.
- Tests cover the new behavior or bug fix.
- Documentation is updated when behavior or usage changes.
- Examples use synthetic or appropriately licensed/shareable data.
- Claims distinguish demonstrations from production evidence.
- `python -m pytest` passes locally.

Small, well-tested pull requests are preferred over large unrelated changes.
