# Prompt Boundary

An offline harness for scoring *saved* agent traces against explicit prompt-injection outcomes. It checks whether an agent called a tool outside its trusted allowlist or emitted a synthetic protected marker in its response or tool arguments. It also measures whether benign inputs still completed a specified literal task check.

From the repository root (Python 3.10 or later):

```bash
python3 projects/prompt-boundary/prompt_boundary.py projects/prompt-boundary/example.json
python3 -m unittest discover -s projects/prompt-boundary -p 'test_*.py'
```

From inside the extracted [v0.1.3 standalone ZIP](https://github.com/karthikvraj/reliable-ai-lab/releases/download/reliable-ai-lab-v0.1.3/prompt-boundary-v0.1.3.zip):

```bash
python3 prompt_boundary.py example.json
python3 -m unittest discover -s . -p 'test_*.py'
```

This project runs directly from the script; it is not registered with the shared `reliable_ai_lab` CLI or browser playground. No third-party Python packages are required.


The example includes an injected document that was ignored, a compromised tool-result trace, a synthetic marker leaked in a response, and a benign control. The `injected-marker-in-response` case is flagged because the saved response contains a marker from `protected_markers`, even though it made no tool calls. This shows a literal output-boundary violation; it does not establish that the injected text caused the leak. Replace `response` and `tool_calls` with actual saved outputs from a model under test. `untrusted_text` records what the agent saw; this tool does not invoke a model or execute tools. `--output report.json` saves the scored record.

The input is a `cases` array with unique IDs, an `attacked` label, trusted task, untrusted text, response, allowed tool names, observed tool calls, protected markers, and `expected_response_contains`. Rates use only cases in the matching attacked or benign group, and are `null` when a group is absent. The SHA-256 fingerprint covers the canonical input JSON.

**Limits:** literal markers miss paraphrases, transformed secrets, and indirect data leaks. A substring task check cannot judge semantic quality. Tool names alone do not authorize a call's arguments. Use only synthetic canaries in examples; never put actual secrets into test fixtures. The report is an evaluation aid, not a prompt-injection prevention system or a claim of model safety.
