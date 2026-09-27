# Inference Twin

Simulate queue behavior after server loss.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/inference-twin-v0.1.1.zip)

## What it does

Capacity loss can push a service from manageable waiting time into an unstable queue.

Simulate Poisson arrivals and exponential service on identical servers. Train a random-forest latency surrogate on independent simulated operating points and report held-out MAE against a constant predictor.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo inference-twin
python -m reliable_ai_lab sample inference-twin --output input.json
python -m reliable_ai_lab run inference-twin --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- arrival_rps: positive arrival rate
- service_ms: mean service time in milliseconds
- servers and lost_servers: integer capacity
- requests and seed: finite simulation controls

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Change lost_servers from 3 to 0. Read offered_utilization and steady_state_possible before interpreting p95 latency.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| synthetic_holdout_mae_ms | 23.0823 |
| constant_baseline_mae_ms | 93.4542 |
| holdout_points | 40 |
| training_points | 120 |
| failure_latency_multiplier | 17.3055 |

## Code and tests

[Implementation](../../reliable_ai_lab/inference_twin.py) · [Tests](../../tests/test_inference_twin.py)

## Limitations

- Not a calibrated digital twin of hardware or an inference engine.
- At utilization >=1 there is no steady state; finite-window latency is illustrative only.
- The random forest learns from this simulator, not real hardware. Surrogate estimates are withheld outside its sampled parameter bounds.

## Next work

Calibrate to measured inference traces, batching and prefill/decode behavior; add repeated simulation intervals and out-of-distribution checks.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
