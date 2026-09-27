# Incident Room

Match telemetry changes to runbook passages.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/incident-room-v0.1.1.zip)

## What it does

On-call engineers need evidence that connects a telemetry change to relevant operational guidance.

Fit an Isolation Forest on the reference window, compute robust median shifts and retrieve relevant runbook text. Combine observations in a non-executing triage report.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo incident-room
python -m reliable_ai_lab sample incident-room --output input.json
python -m reliable_ai_lab run incident-room --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- baseline and current: numeric matrices with matching columns
- feature_names: unique ordered names
- runbooks: unique id/text records

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Set current equal to baseline. Median-shift findings should disappear.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| anomalous_fraction | 1 |
| shifted_features | 2 |
| reference_rows | 300 |
| current_rows | 45 |
| actions_executed | 0 |

## Code and tests

[Implementation](../../reliable_ai_lab/incident_room.py) · [Tests](../../tests/test_incident_room.py)

## Limitations

- These are deterministic analyst modules, not independent autonomous LLM agents.
- A shifted metric is an observation, not a root cause. Contamination and escalation thresholds are illustrative.
- No live infrastructure connector, paging integration, or remediation executor is included.

## Next work

Integrate approved telemetry schemas, time-aware validation and operator feedback. Evaluate against labeled incidents before paging anyone.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
