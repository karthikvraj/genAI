# Reliable AI Lab

**AI that can show its work. Infrastructure experiments you can reproduce.**

Independent engineering by **Karthik Coimbatore Varadaraj** · **v0.1.0 research preview**

I care less about an AI system sounding confident and more about what happens when it is wrong. This lab turns that question into ten focused, inspectable projects: evidence, agent controls, retrieval, GPU telemetry, inference capacity, evaluation and drift.

**Start here:** [Evidence Gate](projects/evidence-gate) · [Repair Agent](projects/repair-agent) · [Inference Twin](projects/inference-twin)

## Run an experiment

```bash
git clone https://github.com/karthikvraj/genAI.git
cd genAI
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo evidence-gate
python -m reliable_ai_lab serve
```

Open **http://127.0.0.1:8765** for the local browser playground. On Windows, activate with `.venv\Scripts\activate`. Python 3.10+ is required; default demos need no API key or GPU. Dependencies must be installed first.

## Ten projects

| Project | What you can inspect | Method |
|---|---|---|
| [Evidence Gate](projects/evidence-gate) | Invalid citations, unsupported numbers and negation changes | Lexical claim-to-source screening |
| [Budget RAG](projects/budget-rag) | Context selection under a hard word budget | Cost-aware, diversity-aware retrieval |
| [Repair Agent](projects/repair-agent) | A bad plan repaired or stopped without executing it | Bounded validator/repair loop; optional local LLM |
| [Incident Room](projects/incident-room) | Telemetry changes alongside relevant runbook excerpts | Anomaly detection and robust shifts |
| [Inference Twin](projects/inference-twin) | Capacity-loss scenarios and surrogate prediction error | Queue simulation and random forest |
| [GPU Guard](projects/gpu-guard) | Anomaly ranks, reference splits and false positives | Isolation Forest and held-out rank calibration |
| [EvalForge](projects/evalforge) | Baselines, confidence errors, uncertainty and abstention | Paired bootstrap and evaluation metrics |
| [Research Lens](projects/research-lens) | Exact excerpts with source identity hashes | Extractive retrieval |
| [Topology RCA](projects/topology-rca) | Competing single-fault hypotheses and negative evidence | Bayesian dependency-graph inference |
| [Drift Radar](projects/drift-radar) | Input-distribution changes and effect sizes | Corrected statistical tests and domain classification |

## Downloads

Each project can be packaged independently. Build all ten ZIPs, the full source bundle, SHA-256 checksums and a **read-only HTML gallery of computed sample results**:

```bash
python -m pytest
python scripts/package.py
```

Artifacts are written to `dist/`. The HTML gallery replays recorded sample outputs; the Python browser playground computes new results from edited inputs. These are deliberately different modes.

**[Download v0.1.0](https://github.com/karthikvraj/genAI/releases/tag/reliable-ai-lab-v0.1.0)** · [Offline demo gallery](https://github.com/karthikvraj/genAI/releases/download/reliable-ai-lab-v0.1.0/reliable-ai-lab-demo-gallery.html) · [Complete lab ZIP](https://github.com/karthikvraj/genAI/releases/download/reliable-ai-lab-v0.1.0/reliable-ai-lab-v0.1.0.zip)

The public research-preview release is published. [GitHub verification](https://github.com/karthikvraj/genAI/actions/runs/36283821103) passed on Python 3.10 and 3.12, including testing every extracted project ZIP before release. The initial local suite passed 142 tests. Package checksums are attached to the release.

## Bring your own approved input

```bash
python -m reliable_ai_lab list
python -m reliable_ai_lab sample gpu-guard --output input.json
python -m reliable_ai_lab run gpu-guard --input input.json --output result.json
```

For Repair Agent only, a local Ollama model can be selected explicitly with `--ollama-model YOUR_INSTALLED_MODEL`. The adapter sends evidence to 127.0.0.1:11434, rejects redirects, and never falls back to a remote provider. Its model behavior is not covered by the deterministic demo results.

## What is verified—and what is not

The test suite checks reproducible outputs, input validation, budget bounds, evidence references, non-execution, calibration splits, statistical invariants, CLI behavior and local HTTP request restrictions. See [validation record](docs/VALIDATION.md) and the sample results in each project README.

These are **research and engineering prototypes**, not production incident responders, universal hallucination detectors or independently validated benchmarks. Synthetic results do not demonstrate real-world performance. Similarity scores, model posteriors and sample accuracy are not interchangeable with calibrated confidence.

## Engineering principles

Evidence first. Bounded behavior. Reproducible results. Honest limits.

All example data is synthetic or hand-authored for this lab. No employer or customer data is included. The initial implementation was developed with AI assistance. No historical adoption, deployment, performance impact or algorithmic novelty is claimed.

[Architecture](docs/ARCHITECTURE.md) · [References](docs/REFERENCES.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [License scope](LICENSE_SCOPE.md)

## Existing work

The pre-existing facial-emotion-detection notebooks and PDFs in this repository remain unchanged and are separate from this lab. The downloadable lab bundles do not include those older artifacts.
