"""A compact, deterministic tour through three flagship AI failure modes."""
from __future__ import annotations

from . import evidence_gate, inference_twin, repair_agent


def run_tour(seed: int = 7) -> dict:
    """Run three local demos and return a small shareable summary."""
    evidence = evidence_gate.run(evidence_gate.sample(seed))
    repair = repair_agent.run(repair_agent.sample(seed))
    inference = inference_twin.run(inference_twin.sample(seed))

    claims = int(evidence["metrics"]["claims"])
    needs_review = int(evidence["metrics"]["needs_review"])
    attempts = int(repair["metrics"]["attempts"])
    multiplier = float(inference["metrics"]["failure_latency_multiplier"])

    return {
        "tour": "reliable-ai-lab",
        "seed": seed,
        "headline": "Three failure modes. Three inspectable checks. Zero production actions.",
        "scenarios": [
            {
                "track": "grounding",
                "project": "evidence-gate",
                "failure": "A generated answer cites evidence but changes numbers, misses a source, or reverses a negation.",
                "decision": evidence["decision"],
                "signal": f"{needs_review} of {claims} sample claims need review",
                "try_next": "Edit the 600-second cache claim or a citation and run Evidence Gate again.",
            },
            {
                "track": "agents",
                "project": "repair-agent",
                "failure": "A proposed agent plan references invented evidence, requests an unsupported action, and skips approval.",
                "decision": repair["decision"],
                "signal": f"bounded validation reached its decision in {attempts} attempt(s); actions executed = 0",
                "try_next": "Change the action allowlist or source reference and inspect the audit chain.",
            },
            {
                "track": "infrastructure",
                "project": "inference-twin",
                "failure": "An inference service loses serving capacity while offered load stays constant.",
                "decision": inference["decision"],
                "signal": f"sample p95 latency multiplier after server loss = {multiplier:.2f}x",
                "try_next": "Change arrival rate, service time, server count, or lost servers and rerun the simulation.",
            },
        ],
        "limitations": [
            "The tour uses synthetic teaching fixtures, not production traffic or customer data.",
            "The checks are deliberately inspectable prototypes; they are not proof of production safety, accuracy, or reliability.",
            "No infrastructure action is executed by the tour.",
        ],
    }
