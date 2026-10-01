# Reliable AI Lab v0.2.1

This release packages the first set of **external community contributions** and several small reliability/usability improvements on top of v0.2.0.

## Evidence Gate

- Normalizes recognized full spellings of seconds, minutes and hours before numeric comparison.
- Treats equivalent quantities such as **1 minute** and **60 seconds** as the same normalized time value.
- Keeps unsupported abbreviations, bare values and other units conservative rather than silently converting them.
- Preserves the original 60→600 mismatch behavior and documents the remaining heuristic limitations.

## Community contributions

Thanks to [@PandaHUN777](https://github.com/PandaHUN777) for four merged contributions:

- Prompt Boundary final-response marker-leak regression coverage ([#14](https://github.com/karthikvraj/reliable-ai-lab/pull/14)).
- Rollout Lab single-noisy-latency scenario and regression coverage ([#15](https://github.com/karthikvraj/reliable-ai-lab/pull/15)).
- Copyable downstream GitHub Actions example ([#26](https://github.com/karthikvraj/reliable-ai-lab/pull/26)).
- Evidence Gate time-quantity normalization ([#27](https://github.com/karthikvraj/reliable-ai-lab/pull/27)).

## Downstream CI

- Adds an inert example workflow that downstream repositories can copy into their own `.github/workflows/` directory.
- Runs a deterministic Evidence Gate check and uploads the JSON result.
- Keeps any policy that fails CI explicitly opt-in and project-specific.

## Verification

The repository workflow verifies supported Python versions, runs the test suite and benchmark, builds the wheel, packages all project archives, and checks the generated downloads before publishing a release.

All included benchmark and example data remains synthetic or hand-authored. Passing these checks does not establish production safety, security, accuracy or reliability.
