"""Offline answer evaluation with paired bootstrap, calibration, and abstention."""
from __future__ import annotations
import re
from collections import Counter
import numpy as np
from .common import number, integer, text


def normalize(answer: str) -> str:
    if not isinstance(answer, str) or len(answer) > 100000:
        raise ValueError("answers must be strings of at most 100000 characters")
    return " ".join(re.findall(r"\w+", answer.casefold()))


def token_f1(answer: str, reference: str) -> float:
    a, b = normalize(answer).split(), normalize(reference).split()
    if not a or not b:
        return float(a == b)
    overlap = sum((Counter(a) & Counter(b)).values())
    return 2.0 * overlap / (len(a) + len(b))


def run(payload: dict) -> dict:
    rows = payload.get("records")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 10000:
        raise ValueError("records must contain 1..10000 objects")
    seed = integer(payload.get("seed", 7), "seed", 0, 1000000)
    draws = integer(payload.get("bootstrap_draws", 1000), "bootstrap_draws", 100, 3000)
    correct, baseline, confidences, latencies, costs, f1s, groups = [], [], [], [], [], [], []
    ids = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each record must be an object")
        ident = text(row.get("id"), "id", 100)
        if ident in ids:
            raise ValueError("record ids must be unique")
        ids.add(ident)
        reference = text(row.get("reference"), "reference")
        answer = row.get("answer")
        correct.append(float(normalize(answer) == normalize(reference)))
        f1s.append(token_f1(answer, reference))
        confidence = number(row.get("confidence"), "confidence", 0, 1)
        confidences.append(confidence)
        latencies.append(number(row.get("latency_ms", 0), "latency_ms", 0, 1e12))
        costs.append(number(row.get("cost_usd", 0), "cost_usd", 0, 1e6))
        groups.append(text(row.get("group", "all"), "group", 100))
        baseline.append(float(normalize(row["baseline_answer"]) == normalize(reference)) if "baseline_answer" in row else None)
    y, confidence = np.asarray(correct), np.asarray(confidences)
    ece, calibration_bins = 0.0, []
    for index in range(10):
        mask = (confidence >= index / 10) & ((confidence < (index + 1) / 10) if index < 9 else (confidence <= 1))
        if not mask.any():
            continue
        accuracy, mean_confidence = float(y[mask].mean()), float(confidence[mask].mean())
        ece += float(mask.mean()) * abs(accuracy - mean_confidence)
        calibration_bins.append({"lower": index / 10, "upper": (index + 1) / 10,
                                 "count": int(mask.sum()), "exact_match": accuracy, "mean_confidence": mean_confidence})
    coverage = []
    for threshold in [0, 0.25, 0.5, 0.75, 0.9, 0.95, 1.0]:
        accepted = confidence >= threshold
        coverage.append({"threshold": threshold, "coverage": float(accepted.mean()),
                         "accepted": int(accepted.sum()), "error_rate": float(1 - y[accepted].mean()) if accepted.any() else None})
    comparison = None
    if any(v is not None for v in baseline):
        if any(v is None for v in baseline):
            raise ValueError("baseline_answer must be provided for all records or none")
        delta = y - np.asarray(baseline)
        rng = np.random.default_rng(seed)
        # One draw at a time bounds memory even for large evaluation sets.
        bootstrap = np.array([delta[rng.integers(0, len(rows), len(rows))].mean() for _ in range(draws)])
        comparison = {"baseline_exact_match": float(np.mean(baseline)), "paired_exact_match_delta": float(delta.mean()),
                      "percentile_95_interval": np.quantile(bootstrap, [0.025, 0.975]).tolist(), "bootstrap_draws": draws}
    return {"project": "evalforge", "decision": "evaluation_complete",
            "metrics": {"examples": len(rows), "exact_match": float(y.mean()), "mean_token_f1": float(np.mean(f1s)),
                        "brier_score": float(np.mean((confidence - y) ** 2)), "ece_10_bins": ece,
                        "p95_latency_ms": float(np.percentile(latencies, 95)), "total_cost_usd": float(sum(costs))},
            "paired_comparison": comparison, "risk_coverage": coverage, "calibration_bins": calibration_bins,
            "group_metrics": [{"group": group, "examples": groups.count(group),
                               "exact_match": float(y[np.asarray(groups) == group].mean())} for group in sorted(set(groups))],
            "limitations": ["Exact match and token overlap do not measure semantic correctness, harmlessness, or factuality.",
                            "Confidence and cost are supplied by the caller; this tool does not infer or verify them.",
                            "Bootstrap intervals assume independent paired examples. Small synthetic examples cannot establish real-world superiority."]}


def sample(seed: int = 7) -> dict:
    examples = [("128 requests", "128 requests", "64 requests", 0.96),
                ("60 seconds", "600 seconds", "60 seconds", 0.94),
                ("human approval", "human approval", "human approval", 0.88),
                ("inspect link counters", "inspect link counters", "restart cluster", 0.72),
                ("reduce batch size", "increase batch size", "increase batch size", 0.40),
                ("check memory headroom", "check memory headroom", "check memory headroom", 0.80),
                ("rollback condition", "rollback condition", "rollback condition", 0.67),
                ("owner", "service owner", "operator", 0.35)]
    return {"_provenance": "Eight hand-authored synthetic examples; an API demonstration, not a benchmark claim.", "seed": seed,
            "records": [{"id": f"q{i}", "reference": ref, "answer": ans, "baseline_answer": base, "confidence": conf,
                         "latency_ms": 100 + i * 17, "cost_usd": 0.0001, "group": "runbook" if i < 4 else "operations"}
                        for i, (ref, ans, base, conf) in enumerate(examples)]}
