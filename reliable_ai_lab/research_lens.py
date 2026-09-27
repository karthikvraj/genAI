"""Extract-only, source-hashed research notes that can abstain."""
from __future__ import annotations
import hashlib
import re
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from .common import documents, text, number, integer, sentences, lexical_index, demo_sources


def run(payload: dict) -> dict:
    docs = documents(payload.get("documents"))
    query = text(payload.get("query"), "query", 5000)
    limit = integer(payload.get("max_excerpts", 4), "max_excerpts", 1, 20)
    minimum = number(payload.get("minimum_similarity", 0.12), "minimum_similarity", 0.001, 1)
    candidates = [{"source_id": d["id"], "quote": sentence, "sentence_index": index,
                   "source_sha256": hashlib.sha256(d["text"].encode()).hexdigest()}
                  for d in docs for index, sentence in enumerate(sentences(d["text"]))]
    if len(candidates) > 5000:
        raise ValueError("maximum 5000 source sentences")
    scores, _ = lexical_index([c["quote"] for c in candidates], query)
    selected, seen = [], set()
    for i in np.argsort(-scores, kind="stable"):
        if scores[i] < minimum or len(selected) == limit:
            break
        normalized = " ".join(candidates[i]["quote"].casefold().split())
        if normalized in seen:
            continue
        seen.add(normalized)
        selected.append({**candidates[i], "similarity": round(float(scores[i]), 6)})
    query_terms = set(re.findall(r"\w+", query.casefold())) - ENGLISH_STOP_WORDS
    evidence_terms = set(re.findall(r"\w+", " ".join(s["quote"] for s in selected).casefold()))
    uncovered = sorted(query_terms - evidence_terms)
    note = "\n".join(f'[{s["source_id"]}:{s["sentence_index"]}] {s["quote"]}' for s in selected)
    return {"project": "research-lens", "decision": "extracts_available" if selected else "abstain",
            "metrics": {"excerpts": len(selected), "distinct_sources": len({s['source_id'] for s in selected}),
                        "query_term_coverage": len(query_terms & evidence_terms) / len(query_terms) if query_terms else 0.0},
            "extractive_note": note, "excerpts": selected, "uncovered_query_terms": uncovered,
            "source_manifest": [{"id": d["id"], "characters": len(d["text"]),
                                 "sha256": hashlib.sha256(d["text"].encode()).hexdigest()} for d in docs],
            "limitations": ["No generated answer or interpretation: every displayed excerpt is copied from supplied text.",
                            "Source hashes provide identity checks, not authenticity or truth guarantees.",
                            "Lexical retrieval and term coverage can miss paraphrases and do not establish evidence sufficiency. No web scraping or PDF parser is included."]}


def sample(seed: int = 7) -> dict:
    return {"_provenance": "Synthetic source documents supplied as text.", "documents": demo_sources(),
            "query": "How can GPU memory pressure and packet retransmissions affect inference latency?", "max_excerpts": 4}
