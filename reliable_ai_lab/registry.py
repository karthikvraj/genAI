"""Explicit project registry; only bundled modules are loadable."""
from __future__ import annotations
import importlib

PROJECTS = {
    "evidence-gate": {"title": "Evidence Gate", "module": "evidence_gate", "tagline": "Show the source. Flag the claim.", "category": "Evidence", "method": "TF-IDF claim screening and citation validation"},
    "budget-rag": {"title": "Budget RAG", "module": "budget_rag", "tagline": "Useful context. A hard budget.", "category": "Retrieval", "method": "Cost-aware greedy maximum marginal relevance"},
    "repair-agent": {"title": "Repair Agent", "module": "repair_agent", "tagline": "A bad plan should stop, not escalate.", "category": "Agents", "method": "Bounded validation-repair loop; optional local LLM"},
    "incident-room": {"title": "Incident Room", "module": "incident_room", "tagline": "Evidence before remediation.", "category": "Operations", "method": "Isolation Forest, robust shifts and runbook retrieval"},
    "inference-twin": {"title": "Inference Twin", "module": "inference_twin", "tagline": "Lose capacity in a simulator, not in production.", "category": "Infrastructure", "method": "Discrete-event queue simulation and random-forest surrogate"},
    "gpu-guard": {"title": "GPU Guard", "module": "gpu_guard", "tagline": "Find the unusual. Keep the uncertainty.", "category": "Infrastructure", "method": "Isolation Forest with held-out rank calibration"},
    "evalforge": {"title": "EvalForge", "module": "evalforge", "tagline": "A better answer needs a better test.", "category": "Evaluation", "method": "Paired bootstrap, risk-coverage and calibration metrics"},
    "research-lens": {"title": "Research Lens", "module": "research_lens", "tagline": "Read the evidence. Keep the receipts.", "category": "Evidence", "method": "Extractive retrieval with source identity hashes"},
    "topology-rca": {"title": "Topology RCA", "module": "topology_rca", "tagline": "Rank explanations. Do not invent certainty.", "category": "Operations", "method": "Single-fault Bayesian inference over dependency graphs"},
    "drift-radar": {"title": "Drift Radar", "module": "drift_radar", "tagline": "Know when the inputs have changed.", "category": "Evaluation", "method": "Holm-corrected KS tests and held-out domain classification"},
}


def get_project(name: str):
    if name not in PROJECTS:
        raise ValueError(f"Unknown project: {name}")
    return importlib.import_module(f"reliable_ai_lab.{PROJECTS[name]['module']}")
