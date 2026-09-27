"""Independent statistical and retrieval analysts; never execute remediation."""
from __future__ import annotations
import numpy as np
from sklearn.ensemble import IsolationForest
from .common import matrix, documents, text, integer, number, lexical_index, demo_sources


def run(payload: dict) -> dict:
    baseline = matrix(payload.get("baseline"), "baseline", 30)
    current = matrix(payload.get("current"), "current", 1)
    if baseline.shape[1] != current.shape[1]:
        raise ValueError("baseline and current must have the same columns")
    names = payload.get("feature_names")
    if not isinstance(names, list) or len(names) != baseline.shape[1] or len(set(names)) != len(names):
        raise ValueError("feature_names must be unique and match the columns")
    names = [text(n, "feature name", 100) for n in names]
    seed = integer(payload.get("seed", 7), "seed", 0, 1000000)
    threshold = number(payload.get("z_threshold", 3.5), "z_threshold", 0.1, 100)
    runbooks = documents(payload.get("runbooks"))
    # Fit only on the supplied reference window. Current incidents are never fitted.
    forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=seed, n_jobs=1).fit(baseline)
    unusual = forest.predict(current) == -1
    center = np.median(baseline, axis=0)
    scale = 1.4826 * np.median(np.abs(baseline - center), axis=0)
    scale = np.maximum(scale, np.maximum(np.std(baseline, axis=0) * 0.01, 1e-8))
    z = np.abs((np.median(current, axis=0) - center) / scale)
    telemetry = [{"feature": names[i], "robust_shift": round(float(z[i]), 4),
                  "baseline_median": float(center[i]), "current_median": float(np.median(current[:, i]))}
                 for i in np.argsort(-z)]
    elevated = [r for r in telemetry if r["robust_shift"] >= threshold]
    query = " ".join(r["feature"].replace("_", " ") for r in elevated)
    evidence = []
    if query:
        scores, _ = lexical_index([r["text"] for r in runbooks], query)
        evidence = [{"source_id": runbooks[i]["id"], "quote": runbooks[i]["text"],
                     "similarity": round(float(scores[i]), 6)}
                    for i in np.argsort(-scores)[:3] if scores[i] > 0.05]
    fraction = float(unusual.mean())
    triage = bool(elevated) or fraction >= 0.30
    return {"project": "incident-room", "decision": "human_triage" if triage else "no_escalation_signal",
            "metrics": {"anomalous_fraction": fraction, "shifted_features": len(elevated),
                        "reference_rows": len(baseline), "current_rows": len(current), "actions_executed": 0},
            "analysts": {"telemetry": telemetry, "runbook_evidence": evidence,
                         "safety": {"human_approval_required": True, "execution_enabled": False}},
            "next_steps": ["Validate collection quality and compare an unaffected peer.",
                           "Review the cited runbooks and recent changes with the service owner."] if triage else [],
            "limitations": ["These are deterministic analyst modules, not independent autonomous LLM agents.",
                            "A shifted metric is an observation, not a root cause. Contamination and escalation thresholds are illustrative.",
                            "No live infrastructure connector, paging integration, or remediation executor is included."]}


def sample(seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    center = np.array([55, 0.2, 30, 70])
    scale = np.array([8, 0.04, 5, 4])
    baseline = rng.normal(center, scale, size=(300, 4))
    current = rng.normal(center + [4, 0.35, 28, 7], scale, size=(45, 4))
    return {"_provenance": "Synthetic telemetry; no employer or customer data.", "seed": seed,
            "feature_names": ["gpu_utilization", "packet_retransmissions", "inference_latency", "gpu_memory_pressure"],
            "baseline": baseline.tolist(), "current": current.tolist(), "runbooks": demo_sources()}
