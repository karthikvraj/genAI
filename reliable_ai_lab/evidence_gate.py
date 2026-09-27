"""Claim-to-source checking. Lexical screening, NOT semantic truth verification."""
from __future__ import annotations
import re
from .common import documents, text, number, lexical_index, sentences, demo_sources

_NUMBERS = re.compile(r"(?<!\w)-?\d+(?:\.\d+)?%?")
_NEGATION = re.compile(r"\b(no|not|never|without|cannot)\b", re.I)


def check_claim(claim: str, sources: list[dict], source_ids: list[str],
                threshold: float = 0.35) -> dict:
    claim = text(claim, "claim", 5000)
    threshold = number(threshold, "threshold", 0.0, 1.0)
    known = {row["id"]: row for row in sources}
    if not isinstance(source_ids, list) or any(not isinstance(x, str) for x in source_ids):
        raise ValueError("source_ids must be a list of strings")
    missing = sorted(set(source_ids) - set(known))
    if missing:
        return {"claim": claim, "status": "invalid_citation", "missing_sources": missing,
                "similarity": 0.0, "evidence": None}
    if not source_ids:
        return {"claim": claim, "status": "uncited", "similarity": 0.0, "evidence": None}
    candidates = [(ident, sentence) for ident in dict.fromkeys(source_ids)
                  for sentence in sentences(known[ident]["text"])]
    scores, _ = lexical_index([s for _, s in candidates], claim)
    best = int(scores.argmax())
    ident, evidence = candidates[best]
    score = float(scores[best])
    absent_numbers = sorted(set(_NUMBERS.findall(claim)) - set(_NUMBERS.findall(evidence)))
    negation_mismatch = bool(_NEGATION.search(claim)) != bool(_NEGATION.search(evidence))
    if score <= 0 or score < threshold:
        status = "insufficient_evidence"
    elif absent_numbers:
        status = "numeric_review"
    elif negation_mismatch:
        status = "negation_review"
    else:
        status = "lexically_supported"
    return {"claim": claim, "status": status, "similarity": round(score, 6),
            "evidence": {"source_id": ident, "quote": evidence},
            "unmatched_numbers": absent_numbers, "negation_mismatch": negation_mismatch}


def run(payload: dict) -> dict:
    sources = documents(payload.get("sources"))
    claims = payload.get("claims")
    if not isinstance(claims, list) or not 1 <= len(claims) <= 100:
        raise ValueError("claims must contain 1..100 objects")
    threshold = number(payload.get("threshold", 0.35), "threshold", 0, 1)
    results = []
    for row in claims:
        if not isinstance(row, dict):
            raise ValueError("each claim must be an object")
        results.append(check_claim(row.get("text"), sources, row.get("source_ids", []), threshold))
    supported = sum(r["status"] == "lexically_supported" for r in results)
    return {"project": "evidence-gate", "decision": "review_required" if supported < len(results) else "lexical_checks_passed",
            "metrics": {"claims": len(results), "lexically_supported": supported,
                        "needs_review": len(results) - supported},
            "claims": results,
            "limitations": ["Similarity is not a probability of truth.",
                            "Numbers and negations are heuristic checks; paraphrases, units, entities and multi-hop claims can be misclassified.",
                            "A passing lexical check must not authorize a consequential action."]}


def sample(seed: int = 7) -> dict:
    return {"_provenance": "Synthetic teaching fixture, not a real incident.",
            "sources": demo_sources(), "claims": [
                {"text": "The inference queue limit is 128 requests.", "source_ids": ["queue"]},
                {"text": "The cache time to live is 600 seconds.", "source_ids": ["cache"]},
                {"text": "Scaling requires human approval.", "source_ids": ["missing-runbook"]},
                {"text": "Scaling does not require human approval.", "source_ids": ["queue"]},
                {"text": "The outage was caused by a satellite.", "source_ids": ["network"]},
            ]}
