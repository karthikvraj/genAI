# Repair Agent

**A bad plan should stop, not escalate.**

Karthik Coimbatore Varadaraj · v0.1.0 · Research prototype

A plausible plan can contain invented references and unauthorized actions. This project validates the plan, repairs bounded structural errors, detects repeated plans and retains a hash-linked audit trace. It has **no infrastructure executor**.

## Try it

From the repository root, after `python -m pip install -e '.[dev]'`:

```bash
python -m reliable_ai_lab demo repair-agent
python -m reliable_ai_lab sample repair-agent --output input.json
python -m reliable_ai_lab run repair-agent --input input.json --output result.json
```

Input: source documents, a plan containing `hypothesis`, `source_ids`, `actions`, and `human_approval_required`, plus `max_attempts` from 1 to 5.

## Show the failure path

The synthetic example starts with an invented source and a restart action. It reaches `awaiting_human_review` after two attempts; **zero actions execute**. Delete the hypothesis: the default repairer stops rather than inventing missing reasoning.

Optional local model use is explicit: append `--ollama-model YOUR_INSTALLED_MODEL` to the `run` command. This sends evidence only to the loopback Ollama endpoint, rejects redirects, and has no remote fallback. Actual model behavior has not been validated by the offline tests.

## Boundary

The default repairer is deterministic, not an LLM. Validation checks structure and references, not truth. An unkeyed hash chain detects accidental edits, not malicious rewriting or truncation.

[Implementation](../../reliable_ai_lab/repair_agent.py) · [Tests](../../tests/test_repair_agent.py) · [Validation](../../docs/VALIDATION.md)

Build the independent ZIP with `python scripts/package.py`. Next work: adversarial model evaluation and authenticated audit storage. Synthetic data; AI-assisted implementation; no autonomous remediation or production validation claimed.
