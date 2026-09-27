# Validation record

Initial local validation, September 26, 2026 (America/New_York).

- Main suite: **142 tests passed**.
- All ten seeded demos completed and returned JSON-serializable results without mutating inputs.
- All ten extracted ZIP packages passed their own tests in separate temporary directories: Evidence Gate 51; Budget RAG 51; Repair Agent 53; Incident Room 46; Inference Twin 51; GPU Guard 47; EvalForge 51; Research Lens 46; Topology RCA 48; Drift Radar 49. Shared tests are repeated in these totals, not additional unique tests.
- The recorded HTML gallery rendered all ten project views in Chromium with no JavaScript errors. Desktop width 1440 and mobile width 390 were inspected; no horizontal overflow was found at mobile width.
- Live browser navigation to localhost was blocked by the execution environment's browser policy. Local HTTP endpoints were exercised separately by Python integration tests. This is not a full end-to-end live-browser validation.
- Wheel build succeeded. Installing dependencies from the internet and optional local-model inference were not tested in this network-restricted environment.

Full local logs are included in the downloadable lab under docs/. Reproduce with `python -m pytest --junitxml=docs/test-results.xml`, `python scripts/package.py`, and `python scripts/check_downloads.py`. GitHub Actions results, when present, are separate evidence of the remote run.

These tests establish specific software behaviors, not production safety, model generalization, adoption, originality of algorithms, or independence from AI assistance.
