"""Reference-only anomaly training, held-out calibration, and robust deviations."""
from __future__ import annotations
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_fscore_support
from .common import matrix, integer, number, text


def run(payload: dict) -> dict:
    reference = matrix(payload.get("reference"), "reference", 50)
    current = matrix(payload.get("current"), "current", 1)
    if reference.shape[1] != current.shape[1]:
        raise ValueError("reference and current must have matching columns")
    names = payload.get("feature_names")
    if not isinstance(names, list) or len(names) != reference.shape[1]:
        raise ValueError("feature_names must match the matrix columns")
    names = [text(n, "feature name", 100) for n in names]
    if len(set(names)) != len(names):
        raise ValueError("feature_names must be unique")
    alpha = number(payload.get("alpha", 0.05), "alpha", 0.001, 0.5)
    seed = integer(payload.get("seed", 7), "seed", 0, 1000000)
    order = np.random.default_rng(seed).permutation(len(reference))
    cut = int(len(reference) * 0.6)
    train, calibration = reference[order[:cut]], reference[order[cut:]]
    model = IsolationForest(n_estimators=120, random_state=seed, contamination="auto", n_jobs=1).fit(train)
    calibration_scores = -model.score_samples(calibration)
    scores = -model.score_samples(current)
    # Larger score = more anomalous. Rank p-values include the new sample (+1).
    pvalues = np.array([(1 + np.sum(calibration_scores >= s)) / (len(calibration_scores) + 1) for s in scores])
    flagged = pvalues <= alpha
    center = np.median(train, axis=0)
    scale = np.maximum(1.4826 * np.median(np.abs(train - center), axis=0), 1e-8)
    deviations = np.abs((current - center) / scale)
    rows = []
    for i in np.argsort(pvalues, kind="stable")[:min(20, len(current))]:
        top = np.argsort(-deviations[i])[:3]
        rows.append({"row": int(i), "flagged": bool(flagged[i]), "rank_p_value": float(pvalues[i]),
                     "anomaly_score": float(scores[i]),
                     "largest_deviations": [{"feature": names[j], "robust_z": float(deviations[i, j])} for j in top]})
    metrics = {"flagged_rows": int(flagged.sum()), "current_rows": len(current),
               "flagged_fraction": float(flagged.mean()), "training_rows": len(train),
               "calibration_rows": len(calibration), "minimum_attainable_p_value": 1 / (len(calibration) + 1)}
    labels = payload.get("labels")
    if labels is not None:
        y = np.asarray(labels)
        if y.shape != (len(current),) or not np.isin(y, [0, 1]).all():
            raise ValueError("labels must be one binary label per current row")
        precision, recall, f1, _ = precision_recall_fscore_support(y, flagged, average="binary", zero_division=0)
        metrics.update({"precision": float(precision), "recall": float(recall), "f1": float(f1)})
    return {"project": "gpu-guard", "decision": "review_anomalies" if flagged.any() else "no_anomaly_flag",
            "metrics": metrics, "ranked_rows": rows, "all_flags": flagged.tolist(),
            "limitations": ["Rank calibration assumes exchangeable healthy reference and future healthy samples; telemetry autocorrelation or drift can invalidate it.",
                            "The alpha setting is per-sample, not a fleet-wide false-alert guarantee.",
                            "Largest deviations explain observed metrics, not causal attribution. No GPU driver access or production telemetry collector is included."]}


def sample(seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    center = np.array([65, 72, 0.15, 45, 250])
    scale = np.array([8, 5, 0.04, 6, 20])
    reference = rng.normal(center, scale, (500, 5))
    healthy = rng.normal(center, scale, (80, 5))
    abnormal = rng.normal(center + [15, 15, 0.35, 35, 90], scale, (20, 5))
    return {"_provenance": "Seeded synthetic GPU-like telemetry, not hardware measurements.", "seed": seed, "alpha": 0.05,
            "feature_names": ["utilization_pct", "memory_pct", "retransmit_pct", "batch_latency_ms", "power_w"],
            "reference": reference.tolist(), "current": np.vstack([healthy, abnormal]).tolist(), "labels": [0] * 80 + [1] * 20}
