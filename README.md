# Reliable AI Lab

**Karthik Coimbatore Varadaraj**

Ten Python projects for testing model outputs, retrieval, agent plans and infrastructure behavior.

The focus is failure handling: an answer with a bad citation, a plan with an unsupported action, a service losing capacity, or data changing after deployment. Each project includes code, tests and an example you can change and run locally.

[Downloads](../../releases/tag/reliable-ai-lab-v0.1.1) · [Tests](../../actions/workflows/reliable-ai-lab.yml) · [Architecture](docs/ARCHITECTURE.md) · [Validation](docs/VALIDATION.md)

## Start with these three

**[Evidence Gate](projects/evidence-gate)** checks a claim against its cited text. Change a number in the answer and inspect the flag and source excerpt. It uses lexical checks, not a general fact-checking model.

**[Repair Agent](projects/repair-agent)** checks plan fields, references and allowed actions. It makes bounded repairs and stops when it cannot produce a valid plan. It does not execute the plan.

**[Inference Twin](projects/inference-twin)** simulates a service losing capacity. Compare queue latency before and after server loss, then inspect prediction error on held-out simulated cases.

## Run locally

Python 3.10 or later is required. Default examples need no API key or GPU. Install the dependencies before running offline.

```bash
git clone https://github.com/karthikvraj/genAI.git reliable-ai-lab
cd reliable-ai-lab
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo evidence-gate
python -m reliable_ai_lab serve
```

Open `http://127.0.0.1:8765` to change inputs and run the examples in your browser. On Windows, activate the environment with `.venv\Scripts\activate`.

The clone command uses the current repository address and creates a local directory named `reliable-ai-lab`.

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

## Downloads

The [v0.1.1 release](../../releases/tag/reliable-ai-lab-v0.1.1) contains a ZIP for each project, the complete lab, a Python wheel and SHA-256 checksums.

[Complete source ZIP](../../releases/download/reliable-ai-lab-v0.1.1/reliable-ai-lab-v0.1.1.zip) · [Recorded demo gallery](../../releases/download/reliable-ai-lab-v0.1.1/reliable-ai-lab-demo-gallery.html)

The HTML gallery shows saved results. It does not run Python. Use the local browser app to compute results from your own inputs.

To build and check the downloads:

```bash
python -m pytest
python -m build --wheel
python scripts/package.py
python scripts/check_downloads.py
```

## Use your own data

```bash
python -m reliable_ai_lab sample gpu-guard --output input.json
python -m reliable_ai_lab run gpu-guard --input input.json --output result.json
```

Only use data you are allowed to share with the local process. Repair Agent also has an optional local Ollama adapter, selected explicitly with `--ollama-model YOUR_INSTALLED_MODEL`. Other projects do not use a model provider.

## Scope

This is a research prototype. The included data is synthetic or hand-authored; sample results are not production benchmarks. The default tests do not validate optional Ollama inference. Project READMEs describe the assumptions, methods and known failure cases.

No employer or customer data is included. Earlier facial-emotion work is preserved under [legacy/](legacy/README.md) and is not included in the lab downloads.

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [References](docs/REFERENCES.md) · [License](LICENSE) · [License scope](LICENSE_SCOPE.md)
