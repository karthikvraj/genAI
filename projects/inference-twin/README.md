# Inference Twin

**Lose capacity in a simulator, not in production.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

Explore how capacity loss changes waiting time, then inspect a learned latency surrogate against a held-out baseline. The simulator uses Poisson arrivals, exponential service, identical servers and one FIFO queue. A random forest learns from independent simulated operating points.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo inference-twin
python -m reliable_ai_lab sample inference-twin --output input.json
python -m reliable_ai_lab run inference-twin --input input.json --output result.json
```

Input: `arrival_rps`, mean `service_ms`, `servers`, `lost_servers`, `requests` and `seed`.

## Reproduced synthetic result

Seed 7 uses 120 simulated training points and 40 holdout points. Surrogate holdout MAE is approximately **23.08 ms**, versus **93.45 ms** for a constant training-mean predictor. This is a result on this simulator, not measured GPU performance.

The default scenario loses three of eight servers. Check `offered_utilization` and `steady_state_possible` before interpreting latency. Set `lost_servers` to zero to reproduce identical scenarios.

## Boundary

Not a calibrated hardware digital twin. No batching, prefill/decode separation, memory limits or network simulation. Utilization at or above one has no steady state; finite-window p95 is illustrative. Surrogate predictions are withheld outside its sampled parameter bounds.

[Implementation](../../reliable_ai_lab/inference_twin.py) · [Tests](../../tests/test_inference_twin.py) · [Validation](../../docs/VALIDATION.md)

Build the independent ZIP with `python scripts/package.py`. Next work: real approved traces, repeated-simulation intervals and inference-engine-specific calibration. Synthetic data; AI-assisted implementation.
