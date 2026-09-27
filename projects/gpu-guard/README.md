# GPU Guard

Detect telemetry anomalies against a reference set.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/gpu-guard-v0.1.1.zip)

## What it does

A useful GPU alert needs a healthy reference, a defensible threshold, and visible false positives.

Split reference data into fitting and calibration sets. Fit Isolation Forest, compute rank-based anomaly p-values, and report large robust metric deviations. Optional labels are used only for evaluation.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo gpu-guard
python -m reliable_ai_lab sample gpu-guard --output input.json
python -m reliable_ai_lab run gpu-guard --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- reference and current: matching numeric matrices
- feature_names: unique ordered metric names
- alpha: per-sample rank threshold
- labels: optional binary current-window labels

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Set alpha to 0.001. The sample calibration set cannot attain that significance level, and no row should be flagged.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| flagged_rows | 30 |
| current_rows | 100 |
| flagged_fraction | 0.3 |
| training_rows | 300 |
| calibration_rows | 200 |
| minimum_attainable_p_value | 0.00497512 |
| precision | 0.666667 |
| recall | 1 |
| f1 | 0.8 |

## Code and tests

[Implementation](../../reliable_ai_lab/gpu_guard.py) · [Tests](../../tests/test_gpu_guard.py)

## Limitations

- Rank calibration assumes exchangeable healthy reference and future healthy samples; telemetry autocorrelation or drift can invalidate it.
- The alpha setting is per-sample, not a fleet-wide false-alert guarantee.
- Largest deviations explain observed metrics, not causal attribution. No GPU driver access or production telemetry collector is included.

## Next work

Use real approved telemetry, temporally aware calibration and fleet-wide alert budgeting. Validate GPU-specific failure modes.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
