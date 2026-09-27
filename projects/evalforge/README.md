# EvalForge

**A better answer needs a better test.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

Evaluate saved answers with an explicit paired baseline, confidence diagnostics, uncertainty intervals and abstention tradeoffs. Includes normalized exact match, token F1, Brier score, ten-bin calibration error, risk/coverage, per-group results and paired bootstrap intervals.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo evalforge
python -m reliable_ai_lab sample evalforge --output input.json
python -m reliable_ai_lab run evalforge --input input.json --output result.json
```

Input: records with unique `id`, `reference`, `answer`, and `confidence`. `baseline_answer` must appear on all records or none. Latency, cost and groups are optional caller-supplied data.

## Inspect the metric, not the headline

Eight hand-authored examples produce exact match 0.625. This is an API demonstration, not an evaluation of a named model. Change the confidence on a wrong answer and inspect Brier score and calibration. At thresholds accepting no answers, error rate is null—not a fabricated zero-error result.

## Boundary

Exact match and token overlap are not semantic factuality metrics. Confidence, cost and latency are supplied by the caller, not independently measured here. Paired bootstrap assumes independent examples; tiny synthetic sets cannot establish superiority.

[Implementation](../../reliable_ai_lab/evalforge.py) · [Tests](../../tests/test_evalforge.py) · [Validation](../../docs/VALIDATION.md)

Build the independent ZIP with `python scripts/package.py`. Next work: independently labeled semantic evaluation, clustered bootstrap and held-out threshold selection. No answer generator or paid model API is required. AI-assisted implementation.
