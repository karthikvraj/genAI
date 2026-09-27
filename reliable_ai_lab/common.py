"""Small, explicit validation and retrieval primitives shared by the projects."""
from __future__ import annotations
import hashlib
import json
import re
from typing import Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def number(value: Any, name: str, low: float | None = None,
           high: float | None = None) -> float:
    if isinstance(value, (bool, str)):
        raise ValueError(f"{name} must be a finite number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not np.isfinite(result) or (low is not None and result < low) or (high is not None and result > high):
        raise ValueError(f"{name} is outside its valid range")
    return result


def integer(value: Any, name: str, low: int = 1, high: int = 10000) -> int:
    result = number(value, name, low, high)
    if result != int(result):
        raise ValueError(f"{name} must be an integer")
    return int(result)


def matrix(value: Any, name: str, min_rows: int = 1) -> np.ndarray:
    try:
        x = np.asarray(value, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a numeric matrix") from exc
    if x.ndim != 2 or not min_rows <= len(x) <= 20000 or not 1 <= x.shape[1] <= 64:
        raise ValueError(f"{name}: expected {min_rows}..20000 rows and 1..64 columns")
    if not np.isfinite(x).all():
        raise ValueError(f"{name} contains non-finite values")
    return x


def text(value: Any, name: str, limit: int = 100000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{name} must be nonempty text, at most {limit} characters")
    return value


def documents(value: Any, field: str = "text") -> list[dict]:
    if not isinstance(value, list) or not 1 <= len(value) <= 500:
        raise ValueError("documents must contain 1..500 records")
    output, seen = [], set()
    total = 0
    for row in value:
        if not isinstance(row, dict):
            raise ValueError("each document must be an object")
        ident = text(row.get("id"), "document id", 100)
        body = text(row.get(field), field)
        total += len(body)
        if ident in seen:
            raise ValueError("document ids must be unique")
        seen.add(ident)
        output.append({**row, "id": ident, field: body})
    if total > 1000000:
        raise ValueError("corpus exceeds the one-million-character demo limit")
    return output


def lexical_index(corpus: list[str], query: str):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True,
                                 token_pattern=r"(?u)\b\w+\b", max_features=20000)
    try:
        vectors = vectorizer.fit_transform(corpus)
    except ValueError as exc:
        raise ValueError("corpus has no searchable words") from exc
    scores = (vectors @ vectorizer.transform([query]).T).toarray().ravel()
    return scores, vectors


def fingerprint(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                      allow_nan=False).encode()).hexdigest()


def sentences(body: str) -> list[str]:
    # Deliberately preserve decimal points. This is not a linguistic sentence model.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", body) if s.strip()]


def demo_sources() -> list[dict]:
    return [
        {"id": "queue", "text": "The inference queue limit is 128 requests. Scale workers only after checking memory headroom. Scaling requires human approval."},
        {"id": "cache", "text": "The cache time to live is 60 seconds. Cache failures increase database load. Do not flush the cache during an incident without approval."},
        {"id": "network", "text": "Packet retransmissions can increase inference latency. Inspect link counters and compare them with a healthy baseline."},
        {"id": "gpu", "text": "GPU memory pressure can increase batch latency. Reduce batch size after validating throughput and memory headroom."},
        {"id": "change", "text": "A change plan needs an owner, a rollback condition, and human approval. A simulation is not evidence of production safety."},
    ]
