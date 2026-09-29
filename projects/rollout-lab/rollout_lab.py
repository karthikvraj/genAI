"""Offline guardrail analysis for a staged rollout; never changes live traffic."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


class InvalidWindow(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise InvalidWindow(message)


def wilson(errors, requests, z=1.96):
    p = errors / requests
    d = 1 + z * z / requests
    center = (p + z * z / (2 * requests)) / d
    half = z * math.sqrt(p * (1 - p) / requests + z * z / (4 * requests * requests)) / d
    return max(0.0, center - half), min(1.0, center + half)


def p95(values):
    ordered = sorted(values)
    rank = math.ceil(0.95 * len(ordered)) - 1
    return ordered[rank]


def evaluate(data):
    require(isinstance(data, dict), "input must be an object")
    policy = data.get("policy")
    require(isinstance(policy, dict), "policy must be an object")
    defaults = {"min_requests": 100, "min_latency_samples": 5, "required_clean_windows": 2,
                "max_error_rate_increase": 0.01, "max_p95_ratio": 1.25}
    require(set(policy) <= set(defaults), "unknown policy field")
    policy = {**defaults, **policy}
    for key in ("min_requests", "min_latency_samples", "required_clean_windows"):
        require(type(policy[key]) is int and policy[key] > 0, f"{key} must be a positive integer")
    require(type(policy["max_error_rate_increase"]) in (int, float)
            and math.isfinite(policy["max_error_rate_increase"])
            and 0 <= policy["max_error_rate_increase"] <= 1, "invalid max_error_rate_increase")
    require(type(policy["max_p95_ratio"]) in (int, float)
            and math.isfinite(policy["max_p95_ratio"])
            and policy["max_p95_ratio"] >= 1, "invalid max_p95_ratio")
    windows = data.get("windows")
    require(isinstance(windows, list) and windows, "windows must be nonempty")
    names = set()
    results = []
    for window in windows:
        require(isinstance(window, dict), "window must be an object")
        name = window.get("id")
        require(isinstance(name, str) and name and name not in names, "window IDs must be unique strings")
        names.add(name)
        arms = []
        for label in ("baseline", "canary"):
            arm = window.get(label)
            require(isinstance(arm, dict), f"{name}: {label} must be an object")
            count, errors, latency = arm.get("requests"), arm.get("errors"), arm.get("latency_ms")
            require(type(count) is int and count > 0 and type(errors) is int
                    and 0 <= errors <= count, f"{name}: invalid {label} request/error counts")
            require(isinstance(latency, list) and all(type(x) in (int, float)
                    and math.isfinite(x) and x > 0 for x in latency),
                    f"{name}: invalid {label} latency samples")
            arms.append((count, errors, latency))
        (bn, be, bl), (cn, ce, cl) = arms
        enough = min(bn, cn) >= policy["min_requests"] and min(len(bl), len(cl)) >= policy["min_latency_samples"]
        b_interval, c_interval = wilson(be, bn), wilson(ce, cn)
        delta = ce / cn - be / bn
        latency_ratio = p95(cl) / p95(bl) if bl and cl else None
        findings = []
        if not enough:
            findings.append("INSUFFICIENT_SAMPLES")
            status = "HOLD"
        else:
            if c_interval[0] > b_interval[1] + policy["max_error_rate_increase"]:
                findings.append("ERROR_REGRESSION_CONFIDENT")
                status = "ROLLBACK_RECOMMENDED"
            elif delta > policy["max_error_rate_increase"] or latency_ratio > policy["max_p95_ratio"]:
                findings.append("GUARDRAIL_EXCEEDED")
                status = "REVIEW"
            else:
                status = "CLEAN"
        results.append({"id": name, "status": status, "findings": findings,
                        "baseline_error_rate": round(be / bn, 4),
                        "canary_error_rate": round(ce / cn, 4),
                        "error_rate_delta": round(delta, 4),
                        "baseline_wilson_95": [round(x, 4) for x in b_interval],
                        "canary_wilson_95": [round(x, 4) for x in c_interval],
                        "p95_latency_ratio": round(latency_ratio, 3) if latency_ratio is not None else None})
    if any(x["status"] == "ROLLBACK_RECOMMENDED" for x in results):
        decision = "ROLLBACK_RECOMMENDED"
    elif any(x["status"] == "REVIEW" for x in results):
        decision = "REVIEW"
    elif len(results) < policy["required_clean_windows"] or any(x["status"] == "HOLD" for x in results):
        decision = "HOLD"
    else:
        decision = "PROMOTION_CANDIDATE"
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return {"schema_version": "1.0", "input_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
            "decision": decision, "policy": policy, "windows": results,
            "limitations": "Intervals assume independent Bernoulli requests; sampled p95 is descriptive. "
                           "Window peeking, correlated traffic, uneven cohorts and repeated tests can invalidate inference. "
                           "No live rollback or promotion is performed."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, InvalidWindow) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
