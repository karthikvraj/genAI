"""Explicit project registry; only bundled modules are loadable."""
from __future__ import annotations
import importlib

PROJECTS = {
    "evidence-gate": {"title": "Evidence Gate", "module": "evidence_gate", "tagline": "Check cited claims against source text.", "category": "Evidence", "method": "TF-IDF claim screening and citation validation"},
    "budget-rag": {"title": "Budget RAG", "module": "budget_rag", "tagline": "Select context within a word budget.", "category": "Retrieval", "method": "Cost-aware greedy maximum marginal relevance"},
    "repair-agent": {"title": "Repair Agent", "module": "repair_agent", "tagline": "Validate and repair plans without executing them.", "category": "Agents", "method": "Bounded validation-repair loop; optional local LLM"},
    "incident-room": {"title": "Incident Room", "module": "incident_room", "tagline": "Match telemetry changes to runbook passages.", "category": "Operations", "method": "Isolation Forest, robust shifts and runbook retrieval"},
    "inference-twin": {"title": "Inference Twin", "module": "inference_twin", "tagline": "Simulate queue behavior after server loss.", "category": "Infrastructure", "method": "Discrete-event queue simulation and random-forest surrogate"},
    "gpu-guard": {"title": "GPU Guard", "module": "gpu_guard", "tagline": "Detect telemetry anomalies against a reference set.", "category": "Infrastructure", "method": "Isolation Forest with held-out rank calibration"},
    "evalforge": {"title": "EvalForge", "module": "evalforge", "tagline": "Compare saved answers and confidence scores.", "category": "Evaluation", "method": "Paired bootstrap, risk-coverage and calibration metrics"},
    "research-lens": {"title": "Research Lens", "module": "research_lens", "tagline": "Extract source passages with content hashes.", "category": "Evidence", "method": "Extractive retrieval with source identity hashes"},
    "topology-rca": {"title": "Topology RCA", "module": "topology_rca", "tagline": "Rank fault hypotheses from dependency graphs.", "category": "Operations", "method": "Single-fault Bayesian inference over dependency graphs"},
    "drift-radar": {"title": "Drift Radar", "module": "drift_radar", "tagline": "Measure changes in input distributions.", "category": "Evaluation", "method": "Holm-corrected KS tests and held-out domain classification"},
}


def get_project(name: str):
    if name not in PROJECTS:
        raise ValueError(f"Unknown project: {name}")
    return importlib.import_module(f"reliable_ai_lab.{PROJECTS[name]['module']}")
