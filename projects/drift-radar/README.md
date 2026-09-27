# Drift Radar

**Know when the inputs have changed.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

Monitor covariate shift without conflating it with model failure. Drift Radar combines per-feature two-sample KS tests, Holm multiple-testing correction, standardized Wasserstein effect sizes and a held-out reference/current logistic classifier.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo drift-radar
python -m reliable_ai_lab sample drift-radar --output input.json
python -m reliable_ai_lab run drift-radar --input input.json --output result.json
```

Input: matching `reference` and `current` numeric matrices, ordered unique `feature_names`, `alpha`, and `minimum_effect`.

## Inspect the shift

The seeded fixture includes 400 reference and 400 current observations across four features. Two deliberately shifted features are flagged. The domain classifier's synthetic holdout AUC is approximately 0.758. Replace current with reference: feature-shift flags disappear.

## Boundary

This detects input-distribution differences, not concept drift or measured degradation in outcomes. Tests assume suitable sample independence; Holm correction does not solve repeated sequential monitoring. The classifier uses a random holdout, not a time-aware split. Thresholds need application-specific validation.

[Implementation](../../reliable_ai_lab/drift_radar.py) · [Tests](../../tests/test_drift_radar.py) · [Validation](../../docs/VALIDATION.md)

Build the independent ZIP with `python scripts/package.py`. Next work: time-aware splits, sequential alert controls and labeled outcome evaluation. All examples are synthetic; AI-assisted implementation.
