# Evidence Gate

Check cited claims against source text.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/evidence-gate-v0.1.1.zip)

## What it does

LLM answers can cite real documents while introducing unsupported numbers or claims.

Resolve citations, split cited text into sentences, rank lexical overlap, and flag unmatched numbers and negation changes. Keep the exact supporting excerpt.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo evidence-gate
python -m reliable_ai_lab sample evidence-gate --output input.json
python -m reliable_ai_lab run evidence-gate --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- sources: unique id/text records
- claims: text plus source_ids
- threshold: lexical similarity cutoff, default 0.35

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Try changing 128 requests to 256 requests, removing a citation, or reversing a negation.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| claims | 5 |
| lexically_supported | 1 |
| needs_review | 4 |

## Code and tests

[Implementation](../../reliable_ai_lab/evidence_gate.py) · [Tests](../../tests/test_evidence_gate.py)

## Limitations

- Similarity is not a probability of truth.
- Numbers and negations are heuristic checks; paraphrases, units, entities and multi-hop claims can be misclassified.
- A passing lexical check must not authorize a consequential action.

## Next work

Replace lexical screening with a separately evaluated entailment model; add multilingual, unit-conversion and adversarial datasets.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
