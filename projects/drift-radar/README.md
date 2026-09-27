# Drift Radar

Measure changes in input distributions.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/drift-radar-v0.1.1.zip)

## What it does

Inputs can change after deployment without an immediate visible change in aggregate metrics.

Run per-feature two-sample KS tests with Holm correction and a standardized Wasserstein effect filter. Separately train a reference/current classifier and report its held-out AUC.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo drift-radar
python -m reliable_ai_lab sample drift-radar --output input.json
python -m reliable_ai_lab run drift-radar --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- reference and current: matching numeric matrices
- feature_names: ordered unique feature names
- alpha and minimum_effect: statistical and practical filters

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Set current equal to reference. Feature-shift flags should disappear.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| drifted_features | 2 |
| features | 4 |
| domain_classifier_holdout_auc | 0.758403 |
| reference_rows | 400 |
| current_rows | 400 |
| classifier_holdout_rows | 240 |

## Code and tests

[Implementation](../../reliable_ai_lab/drift_radar.py) · [Tests](../../tests/test_drift_radar.py)

## Limitations

- Detects covariate shift, not concept drift or a measured reduction in model quality. Labels and outcome evaluation are needed for that.
- KS assumptions and Holm correction do not handle repeated sequential monitoring or time-series dependence.
- The domain classifier uses a random holdout; use time-aware splits for temporally dependent data. Thresholds require application-specific validation.

## Next work

Add time-aware splits, sequential false-alert controls and labeled outcome evaluation; input drift alone is not concept drift.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
