# Topology RCA

**Rank explanations. Do not invent certainty.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

The loudest downstream alert need not be the best explanation. This project ranks single-fault hypotheses using a directed dependency graph, positive and negative symptoms, explicit priors and a no-fault hypothesis. Optional labeled cases update symptom likelihoods with smoothing.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo topology-rca
python -m reliable_ai_lab sample topology-rca --output input.json
python -m reliable_ai_lab run topology-rca --input input.json --output result.json
```

Input: unique `nodes`, dependency-to-consumer `edges`, and an `observed` mapping from node names to booleans. Priors and labeled `training_cases` are optional.

## Inspect competing explanations

The synthetic six-node graph ranks a shared fabric hypothesis above individual downstream nodes under its assumed likelihoods. Mark all observed nodes healthy: `no_fault` becomes the leading hypothesis. Set all prior mass on a single candidate to verify the role of prior assumptions.

## Boundary

At most one fault and conditionally independent symptoms are assumed. Correlated alerts can produce overconfidence. Model posteriors are conditional on the supplied assumptions—not calibrated real-world confidence or causal proof. No network probing or infrastructure access occurs.

[Implementation](../../reliable_ai_lab/topology_rca.py) · [Tests](../../tests/test_topology_rca.py) · [Validation](../../docs/VALIDATION.md)

Build the independent ZIP with `python scripts/package.py`. Next work: independent incident labels, multiple-fault inference and calibration evaluation. Synthetic topology; AI-assisted implementation.
