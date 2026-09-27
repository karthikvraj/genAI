# Incident Room

**Evidence before remediation.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

Connect observed telemetry changes to relevant operational guidance without pretending a correlated metric proves root cause. Statistical analyst modules combine Isolation Forest anomaly detection, robust median shifts, lexical runbook retrieval and a non-executing safety report.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo incident-room
python -m reliable_ai_lab sample incident-room --output input.json
python -m reliable_ai_lab run incident-room --input input.json --output result.json
```

Input: `baseline` and `current` numeric matrices with matching columns, ordered unique `feature_names`, and runbook `id`/`text` records. The anomaly model fits only the reference window.

## Inspect the behavior

The seeded synthetic fixture uses 300 reference rows and 45 current rows. It reports two median-shifted features and relevant runbook passages. Replace the current window with the baseline: median-shift findings disappear. No remediation action is executed.

## Boundary

These are deterministic analyst modules, not autonomous LLM agents. Thresholds are illustrative. An anomaly is not a causal explanation; no live collector, pager or production connector is included.

[Implementation](../../reliable_ai_lab/incident_room.py) · [Tests](../../tests/test_incident_room.py) · [Validation](../../docs/VALIDATION.md)

Build the standalone ZIP with `python scripts/package.py`. Next work: approved telemetry schemas, time-aware evaluation and labeled incidents. All example data is synthetic, not employer or customer telemetry. AI-assisted implementation.
