# Reliable AI Lab

**AI that can show its work. Infrastructure experiments you can reproduce.**

An independent, local-first portfolio by **Karthik Coimbatore Varadaraj**. Ten focused AI and ML reliability projects, not ten wrappers around the same chatbot.

> Development preview: code is being assembled and validated. Do not treat this branch as a production release.

```bash
python -m pip install -e '.[dev]'
python -m reliable_ai_lab list
python -m reliable_ai_lab demo evidence-gate
```

Each project ships a seeded synthetic example, explicit assumptions, input validation, and JSON results. No API key or GPU is required for the default demos. An optional local Ollama adapter is available for Repair Agent. The examples contain no employer or customer data.

## Projects

| Project | Question it tackles |
|---|---|
| Evidence Gate | Which claims lack support in the cited text? |
| Budget RAG | Which excerpts fit a strict context budget? |
| Repair Agent | Can an invalid plan be repaired without executing it? |
| Incident Room | What changed, and which runbook passages are relevant? |
| Inference Twin | What happens when inference-serving capacity is lost? |
| GPU Guard | Which telemetry rows differ from a healthy reference? |
| EvalForge | Does an answer system improve on the paired baseline? |
| Research Lens | Which exact source excerpts address the question? |
| Topology RCA | Which single-fault hypotheses explain observed symptoms? |
| Drift Radar | Have the input distributions changed? |

## Engineering standard

Evidence first. Bounded behavior. Reproducible results. Honest limits.

These are research and engineering prototypes, not production incident responders, universally reliable hallucination detectors, or independently validated benchmarks. Synthetic demo performance is not evidence of production performance. AI-assisted implementation; review and validation remain part of the work.

## Existing work

The pre-existing facial-emotion-detection notebooks and PDFs remain unchanged. They are separate from this portfolio.
