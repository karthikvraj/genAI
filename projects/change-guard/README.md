# ChangeGuard

An explainable preflight for proposed infrastructure changes. It traces downstream services in a dependency graph, estimates criticality-weighted exposure, checks canary and rollback controls, and emits a deterministic JSON decision record.

No API key, model, GPU, or third-party package is required. All sample data is synthetic.

## Run

```bash
python3 projects/change-guard/change_guard.py projects/change-guard/example.json
python3 -m unittest discover -s projects/change-guard -p 'test_*.py'
```

Use `--output report.json` to save the report. Change `target` in `example.json` from `dns` to `offline-training` to compare a broad dependency impact with an isolated service.

## Input contract

- `services`: unique service IDs, criticality 1–5, and `depends_on` links. A link from `api` to `dns` means `api` may be affected when `dns` changes.
- `change`: target, accountable owner, canary percentage, rollback and observation times, tested rollback, and health check availability.
- `policy`: optional maximum canary percentage (default 10), maximum rollback minutes (15), and minimum observation minutes (10).

The report lists every reachable downstream service and its hop distance. `criticality_exposure` is the sum of affected criticalities divided by the sum for all modeled services. It is **not** a calibrated risk probability.

`BLOCK` means rollback is untested or health checks are absent. Other failed thresholds or exposure of at least 75% yield `REVIEW`. Passing all checks yields `READY_FOR_HUMAN_APPROVAL`, never automatic deployment. Findings have stable codes so another system can review them. `input_sha256` fingerprints the submitted JSON content for audit comparisons.

## Scope and limitations

The graph is user-supplied and may omit hidden dependencies. Reachability is possible impact, not observed outage. Criticality scores and thresholds are operator choices. The prototype does not ingest live telemetry, predict failure probability, execute changes, or certify safety. A production deployment would need provenance and freshness checks for graph inputs, authenticated approvals, change window rules, telemetry gates, and a tested rollback controller.

This complements Topology RCA, which diagnoses observed symptoms. ChangeGuard assesses a *proposed* change before execution.
