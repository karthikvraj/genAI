# EvalForge

Compare saved answers and confidence scores.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/evalforge-v0.1.1.zip)

## What it does

A model comparison can hide uncertainty, confidence errors and the cost of abstaining.

Evaluate saved answers with normalized exact match and token F1. Compute Brier score, ten-bin calibration error, risk/coverage and paired bootstrap intervals. Preserve per-group results.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo evalforge
python -m reliable_ai_lab sample evalforge --output input.json
python -m reliable_ai_lab run evalforge --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- records: unique id/reference/answer/confidence records
- baseline_answer: present on all rows or none
- latency_ms and cost_usd: caller-supplied measurements
- group: optional evaluation slice

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Change an incorrect answer with high confidence. Watch calibration and Brier score rather than just aggregate accuracy.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| examples | 8 |
| exact_match | 0.625 |
| mean_token_f1 | 0.854167 |
| brier_score | 0.176175 |
| ece_10_bins | 0.3225 |
| p95_latency_ms | 213.05 |
| total_cost_usd | 0.0008 |

## Code and tests

[Implementation](../../reliable_ai_lab/evalforge.py) · [Tests](../../tests/test_evalforge.py)

## Limitations

- Exact match and token overlap do not measure semantic correctness, harmlessness, or factuality.
- Confidence and cost are supplied by the caller; this tool does not infer or verify them.
- Bootstrap intervals assume independent paired examples. Small synthetic examples cannot establish real-world superiority.

## Next work

Add independently labeled semantic evaluation, clustered bootstrap for related prompts and held-out threshold selection.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
