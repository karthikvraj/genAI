"""Distribution-shift checks plus a held-out reference/current classifier."""
from __future__ import annotations
import numpy as np
from scipy.stats import ks_2samp, wasserstein_distance
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from .common import matrix, number, integer, text


def holm_adjust(pvalues: list[float]) -> list[float]:
    p = np.asarray(pvalues, dtype=float)
    if p.ndim != 1 or not len(p) or not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("pvalues must be finite values in [0,1]")
    order = np.argsort(p)
    adjusted = np.empty(len(p))
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(p) - rank) * float(p[index])))
        adjusted[index] = running
    return adjusted.tolist()


def run(payload: dict) -> dict:
    reference = matrix(payload.get("reference"), "reference", 30)
    current = matrix(payload.get("current"), "current", 30)
    if reference.shape[1] != current.shape[1]:
        raise ValueError("reference and current columns must match")
    names = payload.get("feature_names")
    if not isinstance(names, list) or len(names) != reference.shape[1]:
        raise ValueError("feature_names must match the matrix columns")
    names = [text(n, "feature name", 100) for n in names]
    if len(set(names)) != len(names):
        raise ValueError("feature_names must be unique")
    alpha = number(payload.get("alpha", 0.05), "alpha", 0.0001, 0.5)
    effect_min = number(payload.get("minimum_effect", 0.25), "minimum_effect", 0, 100)
    seed = integer(payload.get("seed", 7), "seed", 0, 1000000)
    features, raw_p = [], []
    for i, name in enumerate(names):
        a, b = reference[:, i], current[:, i]
        ks = ks_2samp(a, b, method="auto")
        scale = max(float(np.std(a)), 1e-8)
        distance = float(wasserstein_distance(a, b) / scale)
        raw_p.append(float(ks.pvalue))
        features.append({"feature": name, "ks_statistic": float(ks.statistic),
                         "raw_p_value": float(ks.pvalue), "wasserstein_reference_std_units": distance})
    corrected = holm_adjust(raw_p)
    for feature, p in zip(features, corrected):
        feature["holm_p_value"] = p
        feature["drift_flag"] = bool(p < alpha and feature["wasserstein_reference_std_units"] >= effect_min)
    x = np.vstack([reference, current])
    y = np.array([0] * len(reference) + [1] * len(current))
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3, random_state=seed, stratify=y)
    classifier = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=seed, class_weight="balanced"))
    classifier.fit(train_x, train_y)
    auc = float(roc_auc_score(test_y, classifier.predict_proba(test_x)[:, 1]))
    flags = sum(f["drift_flag"] for f in features)
    return {"project": "drift-radar", "decision": "distribution_shift_detected" if flags else "no_feature_shift_flag",
            "metrics": {"drifted_features": flags, "features": len(names), "domain_classifier_holdout_auc": auc,
                        "reference_rows": len(reference), "current_rows": len(current), "classifier_holdout_rows": len(test_y)},
            "features": features,
            "limitations": ["Detects covariate shift, not concept drift or a measured reduction in model quality. Labels and outcome evaluation are needed for that.",
                            "KS assumptions and Holm correction do not handle repeated sequential monitoring or time-series dependence.",
                            "The domain classifier uses a random holdout; use time-aware splits for temporally dependent data. Thresholds require application-specific validation."]}


def sample(seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    reference = rng.normal(size=(400, 4))
    current = rng.normal(size=(400, 4))
    current[:, 0] += 1.0
    current[:, 2] *= 1.9
    return {"_provenance": "Seeded synthetic feature distributions, not customer model data.", "seed": seed,
            "feature_names": ["prompt_length_normalized", "retrieval_similarity", "latency_normalized", "answer_length_normalized"],
            "reference": reference.tolist(), "current": current.tolist()}
