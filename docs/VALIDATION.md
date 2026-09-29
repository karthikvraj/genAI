# Validation

## Version 0.1.3

This release adds Prompt Boundary and Rollout Lab to the eleven projects present in v0.1.2. It includes thirteen standalone project ZIPs. Ten projects use the shared runtime; ChangeGuard, Prompt Boundary, and Rollout Lab run as independent scripts.

The release workflow passed on Python 3.10 and 3.12 in [run 36616235545](https://github.com/karthikvraj/reliable-ai-lab/actions/runs/36616235545). It runs the main test suite and CLI smoke tests, builds the wheel, creates the archives, verifies manifest checksums and sizes, and tests each extracted project ZIP in a temporary directory before publication. The three standalone scripts are tested through their extracted ZIPs as well as through CLI smoke tests in the main suite.

The new projects have four Prompt Boundary tests and six Rollout Lab tests. ChangeGuard has five focused tests from v0.1.2. These exercise the documented outcomes, input validation, graph cycles, allowed tool calls, synthetic marker leakage, sample-size gates, and error and latency guardrails. They do not constitute an independent security or production benchmark.

From the repository root, run their focused tests with:

```bash
python3 -m unittest discover -s projects/change-guard -p 'test_*.py'
python3 -m unittest discover -s projects/prompt-boundary -p 'test_*.py'
python3 -m unittest discover -s projects/rollout-lab -p 'test_*.py'
```

To repeat the complete release checks:

```bash
python -m pip install -e '.[dev]'
python -m pytest --junitxml=docs/test-results.xml
python -m build --wheel
python scripts/package.py
python scripts/check_downloads.py
```

The wheel and browser gallery still contain only the original ten shared-runtime projects. No new visual browser test was performed for v0.1.3.

## Version 0.1.2

ChangeGuard and its standalone archive were added. The release workflow passed in [run 36597039079](https://github.com/karthikvraj/reliable-ai-lab/actions/runs/36597039079), including tests for all eleven extracted project archives.

## Version 0.1.1

That update changed documentation, repository layout and release packaging. It did not change the ten original project algorithms.

The workflow tests Python 3.10 and 3.12. It runs the main suite, builds the wheel and checks every extracted project ZIP before publishing. Read the [Actions results](../../../actions/workflows/reliable-ai-lab.yml) for the outcome of each run. Downloadable logs identify their Python and dependency versions.

```bash
python -m pytest --junitxml=docs/test-results.xml
python -m build --wheel
python scripts/package.py
python scripts/check_downloads.py
```

The archive check verifies checksums, tests each project in a separate temporary directory, and confirmed that all ten packages expected for v0.1.1 were present. Shared tests run again in each package; those totals are not additional unique tests.

## Initial version 0.1.0

The initial local suite passed 142 tests. All ten extracted project ZIPs passed their tests. GitHub verification also passed on Python 3.10 and 3.12 in [run 36283821103](../../../actions/runs/36283821103).

The initial recorded HTML gallery was checked at desktop width 1440 and mobile width 390. That check found no JavaScript errors or mobile horizontal overflow. Live browser navigation to localhost was blocked in that environment; HTTP endpoints were tested separately. The earlier browser check is not a new browser test for v0.1.1.

## Limits

The tests cover input validation, output structure, evidence references, budget bounds, calibration splits, stop conditions, CLI behavior and local HTTP restrictions. They do not establish production safety or performance on independent data. Optional Ollama inference requires separate testing.
