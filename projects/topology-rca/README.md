# Topology RCA

Rank fault hypotheses from dependency graphs.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/topology-rca-v0.1.1.zip)

## What it does

The loudest downstream alert is not necessarily the best explanation of an incident.

Use a dependency graph to construct single-fault likelihoods, condition on both positive and negative symptoms, and rank hypotheses including no_fault. Optional labeled cases update likelihoods with smoothing.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo topology-rca
python -m reliable_ai_lab sample topology-rca --output input.json
python -m reliable_ai_lab run topology-rca --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- nodes: unique component names
- edges: dependency-to-consumer pairs
- observed: component-to-boolean symptom mapping
- training_cases and priors: optional labeled model inputs

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Mark every observed node healthy. Compare no_fault against the original shared-fabric hypothesis.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| candidates | 7 |
| observed_nodes | 5 |
| posterior_entropy_bits | 0.651433 |
| top_model_posterior | 0.884175 |

## Code and tests

[Implementation](../../reliable_ai_lab/topology_rca.py) · [Tests](../../tests/test_topology_rca.py)

## Limitations

- Assumes at most one fault and conditionally independent symptom flags. Correlated symptoms can produce overconfidence.
- Posterior values are conditional on the supplied model and priors, not calibrated real-world confidence.
- Edge direction is dependency-to-consumer. Rankings require operator validation; they do not demonstrate causation.

## Next work

Evaluate on independent labeled incidents, account for symptom dependence and multiple simultaneous faults, and test probability calibration.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
