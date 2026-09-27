"""CPU-only queue experiment with a learned surrogate and a held-out baseline."""
from __future__ import annotations
import heapq
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from .common import number, integer


def simulate(arrival_rps: float, service_ms: float, servers: int,
             requests: int = 1500, seed: int = 7) -> dict:
    arrival_rps = number(arrival_rps, "arrival_rps", 0.01, 100000)
    service_ms = number(service_ms, "service_ms", 0.01, 10000)
    servers = integer(servers, "servers", 1, 64)
    requests = integer(requests, "requests", 100, 10000)
    rng = np.random.default_rng(seed)
    arrivals = np.cumsum(rng.exponential(1000.0 / arrival_rps, requests))
    service = rng.exponential(service_ms, requests)
    availability = [0.0] * servers
    heapq.heapify(availability)
    latencies, waits = [], []
    for arrival, duration in zip(arrivals, service):
        free = heapq.heappop(availability)
        start = max(float(arrival), free)
        heapq.heappush(availability, start + float(duration))
        waits.append(start - float(arrival))
        latencies.append(start + float(duration) - float(arrival))
    warmup = requests // 10
    utilization = arrival_rps * service_ms / (1000.0 * servers)
    return {"servers": servers, "offered_utilization": utilization,
            "steady_state_possible": utilization < 1,
            "p95_latency_ms": float(np.percentile(latencies[warmup:], 95)),
            "p95_wait_ms": float(np.percentile(waits[warmup:], 95)),
            "requests": requests, "discarded_warmup_requests": warmup}


def run(payload: dict) -> dict:
    rate = number(payload.get("arrival_rps"), "arrival_rps", 0.01, 100000)
    service = number(payload.get("service_ms"), "service_ms", 0.01, 10000)
    servers = integer(payload.get("servers"), "servers", 1, 64)
    lost = integer(payload.get("lost_servers", 1), "lost_servers", 0, servers - 1)
    requests = integer(payload.get("requests", 1500), "requests", 100, 10000)
    seed = integer(payload.get("seed", 7), "seed", 0, 1000000)
    baseline = simulate(rate, service, servers, requests, seed)
    failure = simulate(rate, service, servers - lost, requests, seed)
    # Independent synthetic operating points; holdout is never used for fitting.
    rng = np.random.default_rng(seed + 101)
    features, targets = [], []
    for index in range(160):
        count = int(rng.integers(1, 17))
        duration = float(rng.uniform(10, 100))
        load = float(rng.uniform(0.10, 0.90))
        result = simulate(load * count * 1000 / duration, duration, count, 700, seed + index + 300)
        features.append([duration, count, load])
        targets.append(result["p95_latency_ms"])
    x, y = np.asarray(features), np.asarray(targets)
    train, test = np.arange(120), np.arange(120, 160)
    model = RandomForestRegressor(n_estimators=100, min_samples_leaf=2, random_state=seed, n_jobs=1).fit(x[train], y[train])
    learned_mae = float(mean_absolute_error(y[test], model.predict(x[test])))
    constant_mae = float(mean_absolute_error(y[test], np.full(len(test), y[train].mean())))
    for scenario in [baseline, failure]:
        load = scenario["offered_utilization"]
        within = 10 <= service <= 100 and 1 <= scenario["servers"] <= 16 and 0.1 <= load <= 0.9
        scenario["surrogate_in_training_domain"] = within
        scenario["surrogate_p95_ms"] = float(model.predict([[service, scenario["servers"], load]])[0]) if within else None
    return {"project": "inference-twin", "decision": "simulation_only",
            "metrics": {"synthetic_holdout_mae_ms": learned_mae, "constant_baseline_mae_ms": constant_mae,
                        "holdout_points": len(test), "training_points": len(train),
                        "failure_latency_multiplier": failure["p95_latency_ms"] / baseline["p95_latency_ms"]},
            "baseline": baseline, "server_loss_scenario": failure,
            "assumptions": ["Poisson arrivals; exponential service times; identical independent servers; one FIFO queue.",
                            "No batching, prefill/decode separation, networking, memory limits, autoscaling, or admission control."],
            "limitations": ["Not a calibrated digital twin of hardware or an inference engine.",
                            "At utilization >=1 there is no steady state; finite-window latency is illustrative only.",
                            "The random forest learns from this simulator, not real hardware. Surrogate estimates are withheld outside its sampled parameter bounds."]}


def sample(seed: int = 7) -> dict:
    return {"_provenance": "Synthetic queue assumptions, not measured GPU performance.", "seed": seed,
            "arrival_rps": 160, "service_ms": 40, "servers": 8, "lost_servers": 3, "requests": 1500}
