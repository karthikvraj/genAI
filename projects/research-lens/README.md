# Research Lens

**Read the evidence. Keep the receipts.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

Create an extractive note that readers can audit. Retrieve and deduplicate exact sentences, attach source IDs and SHA-256 identity hashes, show uncovered query terms, and abstain when no lexical match meets the cutoff.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo research-lens
python -m reliable_ai_lab sample research-lens --output input.json
python -m reliable_ai_lab run research-lens --input input.json --output result.json
```

Input: unique `documents` containing `id` and `text`, a `query`, `max_excerpts` and a minimum lexical similarity.

## Inspect the provenance

The default synthetic question retrieves two excerpts from two sources. Every displayed quote is copied from supplied text. Modify a source and its manifest hash changes. Ask about an unrelated subject and inspect the empty note and abstention state.

## Boundary

This does not generate an answer, parse PDFs or browse the web. Source hashes establish content identity, not authenticity or truth. Lexical retrieval can miss paraphrases; word coverage does not establish sufficient evidence.

[Implementation](../../reliable_ai_lab/research_lens.py) · [Tests](../../tests/test_research_lens.py) · [Validation](../../docs/VALIDATION.md)

Build the independent ZIP with `python scripts/package.py`; run `python -m reliable_ai_lab serve` for the local playground. Next work: approved parsers, page offsets, semantic retrieval and evidence-quality evaluation. Synthetic examples; AI-assisted implementation.
