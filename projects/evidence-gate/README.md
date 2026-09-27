# Evidence Gate

**Show the source. Flag the claim.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

An answer can cite a real document while changing its numbers or meaning. Evidence Gate resolves citations, retrieves the closest source sentence, and flags uncited claims, nonexistent references, unmatched numbers and negation changes. Every finding exposes the exact source excerpt.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo evidence-gate
python -m reliable_ai_lab sample evidence-gate --output input.json
python -m reliable_ai_lab run evidence-gate --input input.json --output result.json
python -m reliable_ai_lab serve
```

Input: `sources` with unique `id`/`text`, and `claims` with `text`/`source_ids`. The optional `threshold` is a lexical-similarity cutoff, not a calibrated confidence level.

## What the sample demonstrates

The synthetic five-claim fixture returns one lexical pass and four review findings. A claim changes the source's **60 seconds** to **600 seconds**: the exact quote stays visible, and `numeric_review` identifies the discrepancy. Try removing a citation or changing a negation.

## Boundary

This uses TF-IDF and literal heuristics, not semantic entailment or universal hallucination detection. Entity substitutions, paraphrases, units and multi-hop claims can defeat it. Passing the lexical check does not establish truth or authorize an action.

[Implementation](../../reliable_ai_lab/evidence_gate.py) · [Tests](../../tests/test_evidence_gate.py) · [Validation](../../docs/VALIDATION.md)

Build the standalone ZIP with `python scripts/package.py`. The package includes complete example input/output and expanded documentation. Default demo: no API key, no GPU, synthetic data only. Next work: independent entailment evaluation and adversarial examples. AI-assisted implementation; no production validation or algorithmic novelty claimed.
