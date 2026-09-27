# GPU Guard

**Find the unusual. Keep the uncertainty.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

An alert needs a healthy reference, an explicit threshold and visible false positives. GPU Guard fits Isolation Forest on a reference subset, calibrates anomaly-score ranks on a separate subset, and reports large robust metric deviations.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo gpu-guard
python -m reliable_ai_lab sample gpu-guard --output input.json
python -m reliable_ai_lab run gpu-guard --input input.json --output result.json
```

Input: `reference` and `current` matrices, ordered `feature_names`, per-sample `alpha`, and optional binary `labels` used only for evaluation.

## Keep the false positives visible

The seed-7 fixture has 500 reference rows, split into 300 training and 200 calibration rows. Of 100 current rows, 20 are injected anomalies. The detector flags 30 rows: **20 true positives and 10 false positives**, precision 0.667, recall 1.0 and F1 0.8. This intentionally simple synthetic result is not production accuracy.

Set alpha to 0.001. With 200 calibration rows the smallest attainable rank p-value is 1/201, so no sample can pass that threshold.

## Boundary

Rank calibration assumes exchangeability. Time dependence and drift can invalidate it. Alpha is per-sample, not a fleet-wide false-alert guarantee. Metric deviations are observations, not causal attribution. No GPU driver or telemetry collector is included.

[Implementation](../../reliable_ai_lab/gpu_guard.py) · [Tests](../../tests/test_gpu_guard.py) · [Validation](../../docs/VALIDATION.md)

Build the standalone ZIP with `python scripts/package.py`. Next work: time-aware calibration, approved telemetry and alert-budget evaluation. AI-assisted implementation.
