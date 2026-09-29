"""ChangeGuard: deterministic, explainable preflight for infrastructure changes.

This is a decision-support prototype. It never executes a change.
"""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import sys


class ValidationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(data: dict) -> None:
    _require(isinstance(data, dict), "input must be an object")
    nodes = data.get("services")
    _require(isinstance(nodes, list) and nodes, "services must be a nonempty list")
    names = set()
    for node in nodes:
        _require(isinstance(node, dict), "each service must be an object")
        name = node.get("id")
        _require(isinstance(name, str) and name.strip() and name not in names,
                 "service IDs must be unique, nonempty strings")
        names.add(name)
        _require(type(node.get("criticality")) is int and 1 <= node["criticality"] <= 5,
                 f"{name}: criticality must be an integer from 1 to 5")
        deps = node.get("depends_on", [])
        _require(isinstance(deps, list) and all(isinstance(x, str) for x in deps)
                 and len(deps) == len(set(deps)), f"{name}: invalid depends_on")
    for node in nodes:
        _require(set(node.get("depends_on", [])) <= names, f"{node['id']}: unknown dependency")
        _require(node["id"] not in node.get("depends_on", []), "self dependency")
    change = data.get("change")
    _require(isinstance(change, dict), "change must be an object")
    _require(change.get("target") in names, "change.target must name a service")
    for key in ("canary_percent", "rollback_minutes", "observation_minutes"):
        _require(type(change.get(key)) in (int, float) and 0 <= change[key] <= 10080,
                 f"change.{key} must be a number between 0 and 10080")
    for key in ("rollback_tested", "health_checks"):
        _require(type(change.get(key)) is bool, f"change.{key} must be boolean")
    _require(isinstance(change.get("owner"), str) and change["owner"].strip(),
             "change.owner must be nonempty")
    policy = data.get("policy", {})
    _require(isinstance(policy, dict), "policy must be an object")
    allowed = {"max_canary_percent", "max_rollback_minutes", "min_observation_minutes"}
    _require(set(policy) <= allowed, "unknown policy key")
    for key, default in (("max_canary_percent", 10), ("max_rollback_minutes", 15),
                         ("min_observation_minutes", 10)):
        value = policy.get(key, default)
        _require(type(value) in (int, float) and 0 <= value <= 10080,
                 f"policy.{key} must be a number between 0 and 10080")


def evaluate(data: dict) -> dict:
    """Return a reproducible assessment; cycles are supported via visited traversal."""
    validate(data)
    services = {n["id"]: n for n in data["services"]}
    change = data["change"]
    policy = {"max_canary_percent": 10, "max_rollback_minutes": 15,
              "min_observation_minutes": 10, **data.get("policy", {})}
    reverse = {name: set() for name in services}
    for node in services.values():
        for dep in node.get("depends_on", []):
            reverse[dep].add(node["id"])
    distances = {change["target"]: 0}
    queue = deque([change["target"]])
    while queue:
        current = queue.popleft()
        for dependent in sorted(reverse[current]):
            if dependent not in distances:
                distances[dependent] = distances[current] + 1
                queue.append(dependent)

    total_weight = sum(n["criticality"] for n in services.values())
    exposed_weight = sum(services[n]["criticality"] for n in distances)
    exposure = round(exposed_weight / total_weight, 3)
    reasons = []
    def flag(code: str, detail: str) -> None:
        reasons.append({"code": code, "detail": detail})
    if change["canary_percent"] > policy["max_canary_percent"]:
        flag("CANARY_TOO_LARGE", "Canary exceeds configured maximum")
    if change["rollback_minutes"] > policy["max_rollback_minutes"]:
        flag("ROLLBACK_TOO_SLOW", "Rollback estimate exceeds configured maximum")
    if change["observation_minutes"] < policy["min_observation_minutes"]:
        flag("OBSERVATION_TOO_SHORT", "Observation period is below configured minimum")
    if not change["rollback_tested"]:
        flag("ROLLBACK_UNTESTED", "Rollback has not been tested")
    if not change["health_checks"]:
        flag("NO_HEALTH_CHECKS", "No health checks are configured")
    if exposure >= 0.75:
        flag("WIDE_BLAST_RADIUS", "At least 75% of criticality weight is downstream")

    blockers = {"ROLLBACK_UNTESTED", "NO_HEALTH_CHECKS"}
    if any(r["code"] in blockers for r in reasons):
        decision = "BLOCK"
    elif reasons:
        decision = "REVIEW"
    else:
        decision = "READY_FOR_HUMAN_APPROVAL"
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return {
        "schema_version": "1.0", "input_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "decision": decision, "target": change["target"], "owner": change["owner"],
        "affected_services": [{"id": n, "hops": distances[n],
                               "criticality": services[n]["criticality"]}
                              for n in sorted(distances, key=lambda n: (distances[n], n))],
        "criticality_exposure": exposure, "policy": policy, "findings": reasons,
        "limitations": "Dependency reachability is potential impact, not failure probability. "
                       "This tool does not execute changes or replace human approval.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Assess a proposed infrastructure change")
    parser.add_argument("input", type=Path, help="JSON change scenario")
    parser.add_argument("--output", type=Path, help="Write assessment JSON to this path")
    args = parser.parse_args(argv)
    try:
        report = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"Invalid scenario: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
