# Contributors

Reliable AI Lab recognizes external contributors for merged, verifiable work.

## Community contributors

### [@PandaHUN777](https://github.com/PandaHUN777)

Merged contributions:

- [#14 — Prompt Boundary: cover response marker leaks](https://github.com/karthikvraj/reliable-ai-lab/pull/14)
  - Added a synthetic saved trace where a protected marker appears in the final response.
  - Added regression coverage for literal marker leakage in response text.
  - Updated documentation to explain the scope and limitations of the signal.

- [#15 — Rollout Lab: add a noisy staged-rollout guardrail example](https://github.com/karthikvraj/reliable-ai-lab/pull/15)
  - Added a synthetic single-outlier latency scenario.
  - Added regression coverage for the existing p95 rollout guardrail behavior.
  - Updated documentation to explain why the sample remains a promotion candidate under the stated fixture policy.

Both contributions were reviewed, validated through the repository test/build/package workflow, and merged into `main`.

## How credits are maintained

Contributors are credited for merged pull requests or other clearly attributable work. Descriptions here are factual summaries of accepted contributions and do not imply employment, endorsement, or production validation.

If you contribute a merged change and your credit is missing or inaccurate, open an issue or pull request to correct it.
