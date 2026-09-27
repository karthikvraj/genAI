# Repair Agent

Validate and repair plans without executing them.

Karthik Coimbatore Varadaraj · v0.1.1

[Lab README](../../README.md) · [Download ZIP](../../../../releases/download/reliable-ai-lab-v0.1.1/repair-agent-v0.1.1.zip)

## What it does

A plan that looks plausible can contain invented references or unauthorized actions.

Validate references, required fields and an action allowlist. Run a bounded repair loop, detect repeated plans and keep a hash-linked audit trace. All plans require human review.

## Run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo repair-agent
python -m reliable_ai_lab sample repair-agent --output input.json
python -m reliable_ai_lab run repair-agent --input input.json --output result.json
python -m reliable_ai_lab serve
```

On Windows, activate with `.venv\Scripts\activate`. The browser app runs at `http://127.0.0.1:8765`. Default examples need no API key or GPU; install the Python dependencies first.

## Inputs

- sources: unique id/text records
- plan: hypothesis/source_ids/actions/human_approval_required
- max_attempts: 1..5

The `sample` command writes a valid input. See `run()` in the implementation for parameter limits. Matrices use rows for observations and columns in `feature_names` order.

## Try a change

Delete hypothesis. The agent should stop rather than manufacture one. The optional Ollama path is explicit opt-in.

## Example results

Seed 7, using synthetic or hand-authored data. These results illustrate the code; they are not production benchmarks. Small numeric differences can occur across dependency versions.

| Metric | Result |
|---|---:|
| attempts | 2 |
| remaining_validation_errors | 0 |
| actions_executed | 0 |
| audit_chain_valid | True |

## Code and tests

[Implementation](../../reliable_ai_lab/repair_agent.py) · [Tests](../../tests/test_repair_agent.py)

## Limitations

- The default repairer is deterministic, not an LLM. Local Ollama is optional and opt-in.
- Validation checks plan shape and references, not whether the hypothesis is true.
- An unkeyed hash chain detects accidental edits, not malicious rewriting or truncation. No autonomous execution exists.

## Next work

Evaluate the optional local model adapter on adversarial plans. Add authenticated audit storage; do not confuse schema validation with reasoning correctness.

## Data and license

The examples contain no employer or customer data. The lab code is MIT-licensed; see [LICENSE](../../LICENSE) and [license scope](../../LICENSE_SCOPE.md). Check third-party data and model licenses before using them.
