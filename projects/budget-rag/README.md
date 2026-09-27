# Budget RAG

**Useful context. A hard budget.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

Fixed-top-k retrieval can exceed a context budget and repeat the same information. Budget RAG combines TF-IDF relevance, a diversity penalty and a length-aware greedy selector. It exposes selected excerpts alongside a fixed-top-three baseline.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo budget-rag
python -m reliable_ai_lab sample budget-rag --output input.json
python -m reliable_ai_lab run budget-rag --input input.json --output result.json
```

Input: unique `documents`, a `query`, a positive `word_budget`, and optional labeled `expected_source_ids`.

## Inspect the tradeoff

The seed-7 sample selects 22 words under a 38-word limit and retrieves both labeled source IDs. Reduce the limit to **15 words**: the selected context remains within budget while the fixed-top-three baseline exceeds it. An unrelated question produces abstention.

## Boundary

The limit counts whitespace-delimited excerpt words, not model tokens or citation prefixes. Retrieval is lexical; there is no answer generator. Greedy selection is not guaranteed optimal. Smaller context alone does not prove lower actual token cost or better answer quality.

[Implementation](../../reliable_ai_lab/budget_rag.py) · [Tests](../../tests/test_budget_rag.py) · [Validation](../../docs/VALIDATION.md)

Build an independent ZIP with `python scripts/package.py`; use `python -m reliable_ai_lab serve` for the local playground. Next work: tokenizer-aware budgets, dense retrieval, held-out answer quality and latency evaluation. Synthetic data; AI-assisted implementation; no production validation claimed.
