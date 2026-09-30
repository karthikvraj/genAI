# Reliable AI Lab

[![Tests](https://github.com/karthikvraj/reliable-ai-lab/actions/workflows/reliable-ai-lab.yml/badge.svg)](https://github.com/karthikvraj/reliable-ai-lab/actions/workflows/reliable-ai-lab.yml)
[![Release](https://img.shields.io/github/v/release/karthikvraj/reliable-ai-lab)](https://github.com/karthikvraj/reliable-ai-lab/releases)
[![Downloads](https://img.shields.io/github/downloads/karthikvraj/reliable-ai-lab/total)](https://github.com/karthikvraj/reliable-ai-lab/releases)
[![License](https://img.shields.io/github/license/karthikvraj/reliable-ai-lab)](LICENSE)

**Karthik Coimbatore Varadaraj**

**Reliability engineering for AI systems — before production.**

Reliable AI Lab is an open-source Python toolkit for **LLM evaluation, RAG testing, AI-agent validation, model drift detection, GPU anomaly detection, inference reliability, and deployment guardrails**.

Reliable AI Lab contains thirteen independently runnable projects for testing what happens when AI systems fail: citations become inconsistent, retrieval budgets get tight, agent plans contain unsupported actions, infrastructure loses capacity, telemetry drifts, or deployed data changes.

**No API key or GPU is required for the default demos.**

[Download v0.2.0](../../releases/tag/reliable-ai-lab-v0.2.0) · [Try the demos](#try-it-in-60-seconds) · [Architecture](docs/ARCHITECTURE.md) · [Validation](docs/VALIDATION.md)

### See a failure before installing

In the [Evidence Gate demo](projects/evidence-gate), a cited source says the cache time to live is **60 seconds**, while the generated claim says **600 seconds**. The tool returns `numeric_review`, points to the source, and lists `600` as an unmatched number. It also flags a missing citation and a reversed negation in the same sample. These are review prompts from lexical checks, not proof that an answer is true or false.

```bash
python -m reliable_ai_lab demo evidence-gate
```

[View the recorded demo gallery](../../releases/download/reliable-ai-lab-v0.2.0/reliable-ai-lab-demo-gallery.html) · [Download the Evidence Gate project](../../releases/download/reliable-ai-lab-v0.2.0/evidence-gate-v0.1.3.zip)

## Why this exists

AI demos often show the happy path. This repository focuses on the failure path.

Use it to explore:

- grounded-answer and citation checks
- retrieval under fixed context budgets
- bounded agent-plan repair
- incident and runbook matching
- inference-capacity failure simulation
- GPU telemetry anomaly detection
- evaluation, calibration and abstention
- reproducible research evidence extraction
- dependency-graph root-cause hypotheses
- statistical and classifier-based drift detection
- preflight checks for proposed infrastructure changes
- prompt-injection outcomes in saved agent traces
- staged rollout guardrails from baseline and canary windows

Each project includes code, tests, synthetic or hand-authored examples, and documented assumptions.

## Try it in 60 seconds

Python 3.10 or later is required.

```bash
git clone https://github.com/karthikvraj/reliable-ai-lab.git
cd reliable-ai-lab
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo evidence-gate
```

To launch the local browser playground:

```bash
python -m reliable_ai_lab serve
```

Open `http://127.0.0.1:8765`. On Windows, activate the environment with `.venv\Scripts\activate`.

## Flagship reliability tracks

**[Evidence Gate](projects/evidence-gate)** checks a claim against its cited text. Change a number in the answer and inspect the flag and source excerpt. It uses lexical checks, not a general fact-checking model.

**[Repair Agent](projects/repair-agent)** checks plan fields, references and allowed actions. It makes bounded repairs and stops when it cannot produce a valid plan. It does not execute the plan.

**[Inference Twin](projects/inference-twin)** simulates a service losing capacity. Compare queue latency before and after server loss, then inspect prediction error on held-out simulated cases.

Together these provide three entry points: **grounding reliability**, **agent reliability**, and **AI infrastructure reliability**. The remaining projects extend those tracks with retrieval budgets, evaluation, drift, change safety, prompt boundaries, root-cause hypotheses, and rollout guardrails.

## Projects

| Project | What it tests |
|---|---|
| [Evidence Gate](projects/evidence-gate) | Citation validity, changed numbers and negation in cited claims |
| [Budget RAG](projects/budget-rag) | Context selection under a fixed word budget |
| [Repair Agent](projects/repair-agent) | Plan validation, bounded repairs and stop conditions |
| [Incident Room](projects/incident-room) | Telemetry changes and related runbook passages |
| [Inference Twin](projects/inference-twin) | Queue behavior after capacity loss and latency prediction error |
| [GPU Guard](projects/gpu-guard) | Telemetry anomalies using separate fitting and calibration data |
| [EvalForge](projects/evalforge) | Answer quality, calibration, paired comparisons and abstention |
| [Research Lens](projects/research-lens) | Extracted source passages with identifiers and content hashes |
| [Topology RCA](projects/topology-rca) | Fault hypotheses using dependency graphs and healthy observations |
| [Drift Radar](projects/drift-radar) | Input-distribution changes using statistical tests and a classifier |
| [ChangeGuard](projects/change-guard) | Proposed changes, downstream blast radius and rollback readiness |
| [Prompt Boundary](projects/prompt-boundary) | Unauthorized tool calls and synthetic marker leakage in saved agent traces |
| [Rollout Lab](projects/rollout-lab) | Canary error and latency guardrails across staged windows |

### Run the three standalone projects

ChangeGuard, Prompt Boundary, and Rollout Lab run directly from Python scripts. They are included in the source bundle and their own ZIPs; the wheel, shared CLI, browser playground, and recorded gallery currently cover the original ten projects.

From the repository root:

```bash
python3 projects/change-guard/change_guard.py projects/change-guard/example.json
python3 projects/prompt-boundary/prompt_boundary.py projects/prompt-boundary/example.json
python3 projects/rollout-lab/rollout_lab.py projects/rollout-lab/example.json
```

Each project README also has commands for running its extracted standalone ZIP.

## Downloads

The [v0.2.0 release](../../releases/tag/reliable-ai-lab-v0.2.0) contains ZIPs for all thirteen projects, the complete lab, a Python wheel and SHA-256 checksums.

[Complete source ZIP](../../releases/download/reliable-ai-lab-v0.2.0/reliable-ai-lab-v0.2.0.zip) · [Recorded demo gallery](../../releases/download/reliable-ai-lab-v0.2.0/reliable-ai-lab-demo-gallery.html)

The HTML gallery shows saved results. It does not run Python. Use the local browser app to compute results from your own inputs.

To build and check the downloads:

```bash
python -m pytest
python -m build --wheel
python scripts/package.py
python scripts/check_downloads.py
```

## Run the reproducible benchmark

The first benchmark harness covers deterministic grounding and retrieval regression scenarios:

```bash
python -m reliable_ai_lab benchmark
python -m reliable_ai_lab benchmark --output benchmark-results.json
```

The shipped cases are synthetic regression fixtures, not production performance estimates. See [Benchmarks](docs/BENCHMARKS.md).

## Use your own data

```bash
python -m reliable_ai_lab sample gpu-guard --output input.json
python -m reliable_ai_lab run gpu-guard --input input.json --output result.json
```

Only use data you are allowed to share with the local process. Repair Agent also has an optional local Ollama adapter, selected explicitly with `--ollama-model YOUR_INSTALLED_MODEL`. Other projects do not use a model provider.

## Scope

This is a research prototype. The included data is synthetic or hand-authored; sample results are not production benchmarks. The default tests do not validate optional Ollama inference. Project READMEs describe the assumptions, methods and known failure cases.

No employer or customer data is included. Earlier facial-emotion work is preserved under [legacy/](legacy/README.md) and is not included in the lab downloads.

If this project is useful, consider starring the repository, sharing a project example, or opening an issue with feedback.

[Contributing](CONTRIBUTING.md) · [Roadmap](docs/ROADMAP.md) · [Benchmarks](docs/BENCHMARKS.md) · [Adopters](docs/ADOPTERS.md) · [Security](SECURITY.md) · [References](docs/REFERENCES.md) · [Cite](CITATION.cff) · [License](LICENSE)
