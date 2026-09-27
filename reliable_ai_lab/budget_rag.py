"""Word-budgeted, diversity-aware retrieval with an explicit fixed-top-k baseline."""
from __future__ import annotations
import numpy as np
from .common import documents, text, integer, number, lexical_index, sentences, demo_sources


def run(payload: dict) -> dict:
    docs = documents(payload.get("documents"))
    query = text(payload.get("query"), "query", 5000)
    budget = integer(payload.get("word_budget", 80), "word_budget", 1, 5000)
    alpha = number(payload.get("relevance_weight", 0.75), "relevance_weight", 0, 1)
    minimum = number(payload.get("minimum_similarity", 0.08), "minimum_similarity", 0, 1)
    chunks = [{"id": d["id"], "text": s, "words": len(s.split())}
              for d in docs for s in sentences(d["text"])]
    if len(chunks) > 5000:
        raise ValueError("too many sentences; maximum 5000")
    relevance, vectors = lexical_index([c["text"] for c in chunks], query)
    selected, remaining, used = [], set(range(len(chunks))), 0
    while remaining:
        candidates = []
        for idx in sorted(remaining):
            if relevance[idx] < minimum or used + chunks[idx]["words"] > budget:
                continue
            redundancy = 0.0 if not selected else float((vectors[idx] @ vectors[selected].T).toarray().max())
            # Cost-aware greedy MMR, not an optimal knapsack solver.
            utility = (alpha * relevance[idx] - (1 - alpha) * redundancy) / np.sqrt(chunks[idx]["words"])
            candidates.append((float(utility), -idx, idx))
        if not candidates:
            break
        utility, _, idx = max(candidates)
        if utility <= 0:
            break
        selected.append(idx)
        remaining.remove(idx)
        used += chunks[idx]["words"]
    baseline_ids = sorted(range(len(chunks)), key=lambda i: (-relevance[i], i))[:3]
    baseline_ids = [i for i in baseline_ids if relevance[i] >= minimum]
    baseline_words = sum(chunks[i]["words"] for i in baseline_ids)
    output = [{**chunks[i], "similarity": round(float(relevance[i]), 6)} for i in selected]
    result = {"project": "budget-rag", "decision": "context_ready" if output else "abstain",
              "metrics": {"selected_words": used, "word_budget": budget,
                          "selected_chunks": len(output), "fixed_top3_words": baseline_words,
                          "fixed_top3_over_budget": baseline_words > budget},
              "context": output,
              "context_text": "\n".join(f"[{c['id']}] {c['text']}" for c in output),
              "baseline": [chunks[i] for i in baseline_ids],
              "limitations": ["The budget counts whitespace-delimited words in excerpts, not model tokens or citation prefixes.",
                              "TF-IDF retrieval is lexical, not dense semantic search. No answer generation is performed.",
                              "The greedy objective does not guarantee optimal retrieval or improved answer quality."]}
    expected = payload.get("expected_source_ids")
    if expected is not None:
        if not isinstance(expected, list) or not expected or any(x not in {d['id'] for d in docs} for x in expected):
            raise ValueError("expected_source_ids must be a nonempty list of known ids")
        expected = set(expected)
        result["metrics"]["source_recall"] = len(expected & {c["id"] for c in output}) / len(expected)
    return result


def sample(seed: int = 7) -> dict:
    return {"_provenance": "Synthetic runbook retrieval example.", "documents": demo_sources(),
            "query": "GPU memory pressure and packet retransmissions increase inference latency",
            "word_budget": 38, "expected_source_ids": ["gpu", "network"]}
