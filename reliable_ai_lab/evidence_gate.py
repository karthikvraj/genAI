"""Claim-to-source checking. Lexical screening, NOT semantic truth verification."""
from __future__ import annotations
import re
from decimal import Decimal
from .common import documents, text, number, lexical_index, sentences, demo_sources

_QUANTITIES = re.compile(
    r"(?<!\w)(?P<number>-?\d+(?:\.\d+)?%?)(?:\s+(?P<unit>seconds?|minutes?|hours?)\b)?",
    re.I,
)
_TIME_SECONDS = {
    "second": Decimal("1"),
    "seconds": Decimal("1"),
    "minute": Decimal("60"),
    "minutes": Decimal("60"),
    "hour": Decimal("3600"),
    "hours": Decimal("3600"),
}
_NEGATION = re.compile(r"\b(no|not|never|without|cannot)\b", re.I)


def _numeric_values(value: str) -> list[tuple[str, tuple[str, Decimal | str]]]:
    result = []
    for match in _QUANTITIES.finditer(value):
        number_text = match.group("number")
        unit = match.group("unit")
        if unit and not number_text.endswith("%"):
            normalized = ("time", Decimal(number_text) * _TIME_SECONDS[unit.lower()])
        else:
            normalized = ("number", number_text)
        result.append((number_text, normalized))
    return result


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
    evidence_numbers = {normalized for _, normalized in _numeric_values(evidence)}
    absent_numbers = sorted({number_text for number_text, normalized in _numeric_values(claim)
                             if normalized not in evidence_numbers})
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
                            "Numeric comparison normalizes only full singular/plural spellings of seconds, minutes and hours; abbreviations, bare values and other units are not converted.",
                            "Numbers and negations are heuristic checks; paraphrases, unsupported or ambiguous units, entities and multi-hop claims can be misclassified.",
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
