"""Single-fault Bayesian ranking with assumed or learned symptom likelihoods."""
from __future__ import annotations
from collections import deque
import math
import numpy as np
from .common import text, number, integer


def topology(payload: dict):
    nodes = payload.get("nodes")
    if not isinstance(nodes, list) or not 2 <= len(nodes) <= 50:
        raise ValueError("nodes must contain 2..50 unique names")
    nodes = [text(n, "node", 100) for n in nodes]
    if len(set(nodes)) != len(nodes) or "no_fault" in nodes:
        raise ValueError("nodes must be unique; no_fault is reserved")
    edges = payload.get("edges", [])
    if not isinstance(edges, list) or len(edges) > 2500:
        raise ValueError("edges must be a list with at most 2500 pairs")
    graph = {n: [] for n in nodes}
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 2 or any(n not in graph for n in edge) or edge[0] == edge[1]:
            raise ValueError("edges must join two different known nodes")
        graph[edge[0]].append(edge[1])
    distances = {}
    for root in nodes:
        distance, queue = {root: 0}, deque([root])
        while queue:
            node = queue.popleft()
            for child in graph[node]:
                if child not in distance:
                    distance[child] = distance[node] + 1
                    queue.append(child)
        distances[root] = distance
    return nodes, distances


def observation(value: dict, nodes: list[str]) -> dict:
    if not isinstance(value, dict) or not value or any(n not in nodes or not isinstance(v, bool) for n, v in value.items()):
        raise ValueError("observed must map known nodes to true/false values")
    return value


def run(payload: dict) -> dict:
    nodes, distances = topology(payload)
    observed = observation(payload.get("observed"), nodes)
    candidates = nodes + ["no_fault"]
    false_alarm = number(payload.get("false_alarm_probability", 0.03), "false_alarm_probability", 0.0001, 0.49)
    likelihood = {root: {node: (0.90 * 0.85 ** distances[root][node] if root != "no_fault" and node in distances[root] else false_alarm)
                         for node in nodes} for root in candidates}
    training = payload.get("training_cases")
    learned_counts = {}
    if training is not None:
        if not isinstance(training, list) or not 1 <= len(training) <= 5000:
            raise ValueError("training_cases must contain 1..5000 labeled records")
        counts = {root: {n: [0, 0] for n in nodes} for root in candidates}
        for case in training:
            if not isinstance(case, dict) or case.get("fault") not in candidates:
                raise ValueError("training fault must be a known node or no_fault")
            obs = observation(case.get("observed"), nodes)
            for node, value in obs.items():
                counts[case["fault"]][node][0] += int(value)
                counts[case["fault"]][node][1] += 1
        for root in candidates:
            learned_counts[root] = max(v[1] for v in counts[root].values())
            for node, (positive, count) in counts[root].items():
                if count:
                    likelihood[root][node] = (positive + 1) / (count + 2)
    prior_input = payload.get("priors", {c: 1.0 for c in candidates})
    if not isinstance(prior_input, dict) or set(prior_input) != set(candidates):
        raise ValueError("priors must give one nonnegative value per candidate, including no_fault")
    priors = {c: number(prior_input[c], "prior", 0, 1e10) for c in candidates}
    total = sum(priors.values())
    if not total > 0:
        raise ValueError("at least one prior must be positive")
    logs = []
    for root in candidates:
        logp = math.log(priors[root] / total) if priors[root] else -math.inf
        for node, value in observed.items():
            p = likelihood[root][node]
            logp += math.log(p if value else 1 - p)
        logs.append(logp)
    weights = np.exp(np.asarray(logs) - max(logs))
    weights /= weights.sum()
    ranking = [{"candidate": candidates[i], "model_posterior": float(weights[i]),
                "symptom_likelihoods": likelihood[candidates[i]],
                "reachable_nodes": sorted(distances[candidates[i]]) if candidates[i] != "no_fault" else []}
               for i in np.argsort(-weights, kind="stable")]
    return {"project": "topology-rca", "decision": "ranked_hypotheses_not_causal_proof",
            "metrics": {"candidates": len(candidates), "observed_nodes": len(observed),
                        "posterior_entropy_bits": float(-np.sum(weights[weights > 0] * np.log2(weights[weights > 0]))),
                        "top_model_posterior": ranking[0]["model_posterior"]},
            "ranking": ranking, "likelihood_mode": "learned_with_topology_fallback" if training else "assumed_from_topology",
            "training_counts": learned_counts,
            "limitations": ["Assumes at most one fault and conditionally independent symptom flags. Correlated symptoms can produce overconfidence.",
                            "Posterior values are conditional on the supplied model and priors, not calibrated real-world confidence.",
                            "Edge direction is dependency-to-consumer. Rankings require operator validation; they do not demonstrate causation."]}


def sample(seed: int = 7) -> dict:
    return {"_provenance": "Synthetic dependency graph with manually supplied observations and assumed likelihoods.",
            "nodes": ["fabric", "gpu-a", "gpu-b", "scheduler", "inference-api", "client"],
            "edges": [["fabric", "gpu-a"], ["fabric", "gpu-b"], ["gpu-a", "inference-api"],
                      ["gpu-b", "inference-api"], ["scheduler", "inference-api"], ["inference-api", "client"]],
            "observed": {"gpu-a": True, "gpu-b": True, "inference-api": True, "client": True, "scheduler": False}}
