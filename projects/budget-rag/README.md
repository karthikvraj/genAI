# Budget RAG

Select context within a word budget.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/budget-rag-v0.1.1.zip)

## What it does

A fixed number of retrieved chunks can exceed a context budget or repeat the same information.

Use TF-IDF relevance, diversity penalties and a length-aware greedy selector. Compare its word count with a fixed-top-three retrieval baseline.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo budget-rag
python -m reliable_ai_lab sample budget-rag --output input.json
python -m reliable_ai_lab run budget-rag --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- documents: unique id/text records
- query: nonempty question
- word_budget: positive whitespace-word limit
- expected_source_ids: optional labeled source set

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Reduce word_budget from 38 to 15. Compare selected_words with fixed_top3_words.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| selected_words | 22 |
| word_budget | 38 |
| selected_chunks | 3 |
| fixed_top3_words | 22 |
| fixed_top3_over_budget | False |
| source_recall | 1 |

## Code and tests

[Implementation](../../reliable_ai_lab/budget_rag.py) · [Tests](../../tests/test_budget_rag.py)

## Limitations

- The budget counts whitespace-delimited words in excerpts, not model tokens or citation prefixes.
- TF-IDF retrieval is lexical, not dense semantic search. No answer generation is performed.
- The greedy objective does not guarantee optimal retrieval or improved answer quality.

## Next work

Add tokenizer-specific budgets, dense retrieval and answer-quality evaluation before claiming context or cost improvements.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
