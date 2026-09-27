# Research Lens

Extract source passages with content hashes.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/research-lens-v0.1.1.zip)

## What it does

A research note should let the reader inspect the exact text behind every excerpt.

Retrieve and deduplicate source sentences, attach stable source identifiers and SHA-256 hashes, expose uncovered query terms, and abstain when lexical evidence is absent.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo research-lens
python -m reliable_ai_lab sample research-lens --output input.json
python -m reliable_ai_lab run research-lens --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- documents: unique id/text records
- query: nonempty research question
- max_excerpts: 1..20
- minimum_similarity: retrieval cutoff

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Ask a question unrelated to the supplied corpus. The tool should return an empty extractive note.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| excerpts | 2 |
| distinct_sources | 2 |
| query_term_coverage | 0.875 |

## Code and tests

[Implementation](../../reliable_ai_lab/research_lens.py) · [Tests](../../tests/test_research_lens.py)

## Limitations

- No generated answer or interpretation: every displayed excerpt is copied from supplied text.
- Source hashes provide identity checks, not authenticity or truth guarantees.
- Lexical retrieval and term coverage can miss paraphrases and do not establish evidence sufficiency. No web scraping or PDF parser is included.

## Next work

Add approved document parsers, page offsets, semantic retrieval and an evidence-quality assessment dataset.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
