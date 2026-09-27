# Validation

## Version 0.1.1

This update changes documentation, repository layout and release packaging. It does not change the ten project algorithms.

The workflow tests Python 3.10 and 3.12. It runs the main suite, builds the wheel and checks every extracted project ZIP before publishing. Read the [Actions results](../../../actions/workflows/reliable-ai-lab.yml) for the outcome of each run. Downloadable logs identify their Python and dependency versions.

```bash
python -m pytest --junitxml=docs/test-results.xml
python -m build --wheel
python scripts/package.py
python scripts/check_downloads.py
```

The archive check verifies checksums, tests each project in a separate temporary directory, and confirms that all ten expected packages are present. Shared tests run again in each package; those totals are not additional unique tests.

## Initial version 0.1.0

The initial local suite passed 142 tests. All ten extracted project ZIPs passed their tests. GitHub verification also passed on Python 3.10 and 3.12 in [run 36283821103](../../../actions/runs/36283821103).

The initial recorded HTML gallery was checked at desktop width 1440 and mobile width 390. That check found no JavaScript errors or mobile horizontal overflow. Live browser navigation to localhost was blocked in that environment; HTTP endpoints were tested separately. The earlier browser check is not a new browser test for v0.1.1.

## Limits

The tests cover input validation, output structure, evidence references, budget bounds, calibration splits, stop conditions, CLI behavior and local HTTP restrictions. They do not establish production safety or performance on independent data. Optional Ollama inference requires separate testing.
