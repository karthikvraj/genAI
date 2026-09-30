"""Deterministic benchmark harness for selected Reliable AI Lab tracks.

These fixtures are synthetic regression scenarios, not production benchmarks.
"""
from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import version as package_version, PackageNotFoundError

from . import budget_rag, evidence_gate
from .common import demo_sources

SCHEMA_VERSION = "1.0"


def _version() -> str:
    try:
        return package_version("kv-reliable-ai-lab")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def _evidence_cases() -> list[dict]:
    sources = demo_sources()
    cases = [
        ("supported-number", "The inference queue limit is 128 requests.", ["queue"], "lexically_supported"),
        ("changed-number", "The cache time to live is 600 seconds.", ["cache"], "numeric_review"),
        ("missing-citation", "Scaling requires human approval.", ["missing-runbook"], "invalid_citation"),
        ("reversed-negation", "Scaling does not require human approval.", ["queue"], "negation_review"),
        ("unrelated-claim", "The outage was caused by a satellite.", ["network"], "insufficient_evidence"),
    ]
    rows = []
    for case_id, claim, source_ids, expected in cases:
        result = evidence_gate.check_claim(claim, sources, source_ids)
        rows.append({
            "id": case_id,
            "expected_status": expected,
            "observed_status": result["status"],
            "passed": result["status"] == expected,
        })
    return rows


def _retrieval_cases() -> list[dict]:
    standard = budget_rag.sample()
    standard_result = budget_rag.run(standard)
    oov = budget_rag.sample()
    oov["query"] = "saffron giraffe"
    oov_result = budget_rag.run(oov)
    return [
        {
            "id": "expected-sources-under-budget",
            "expected": {"source_recall": 1.0, "within_budget": True},
            "observed": {
                "source_recall": standard_result["metrics"]["source_recall"],
                "within_budget": standard_result["metrics"]["selected_words"] <= standard_result["metrics"]["word_budget"],
            },
            "passed": (
                standard_result["metrics"]["source_recall"] == 1.0
                and standard_result["metrics"]["selected_words"] <= standard_result["metrics"]["word_budget"]
            ),
        },
        {
            "id": "out-of-vocabulary-abstention",
            "expected": {"decision": "abstain", "selected_chunks": 0},
            "observed": {
                "decision": oov_result["decision"],
                "selected_chunks": oov_result["metrics"]["selected_chunks"],
            },
            "passed": oov_result["decision"] == "abstain" and oov_result["metrics"]["selected_chunks"] == 0,
        },
    ]


def run_benchmarks() -> dict:
    evidence = _evidence_cases()
    retrieval = _retrieval_cases()
    all_cases = evidence + retrieval
    return {
        "schema_version": SCHEMA_VERSION,
        "project_version": _version(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provenance": "Synthetic deterministic regression fixtures shipped with Reliable AI Lab.",
        "tracks": {
            "grounding": {
                "cases": evidence,
                "summary": {"passed": sum(x["passed"] for x in evidence), "total": len(evidence)},
            },
            "retrieval": {
                "cases": retrieval,
                "summary": {"passed": sum(x["passed"] for x in retrieval), "total": len(retrieval)},
            },
        },
        "summary": {
            "passed": sum(x["passed"] for x in all_cases),
            "total": len(all_cases),
            "all_passed": all(x["passed"] for x in all_cases),
        },
        "limitations": [
            "These are synthetic regression fixtures, not estimates of production accuracy.",
            "Passing results show expected behavior on the included cases only.",
            "The grounding checks are lexical heuristics and the retrieval benchmark uses the included TF-IDF implementation.",
        ],
    }
