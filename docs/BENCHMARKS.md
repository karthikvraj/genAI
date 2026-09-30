# Reliable AI Benchmark Plan

Reliable AI Lab includes demonstrations and tests, but synthetic examples should not be presented as production benchmarks. This document defines the path toward reproducible benchmark artifacts.

## Benchmark families

| Track | Example failure | Candidate measures |
|---|---|---|
| Grounding | changed number, missing citation, reversed negation | detection rate, false-positive rate, abstention/review rate |
| Retrieval | relevant evidence dropped under a context budget | recall@k, precision@k, hit rate, budget utilization |
| Agents | invalid references or unauthorized actions | violation detection, valid-plan rate, repair success, stop correctness |
| Drift | deployed inputs differ from reference data | detection power, false-alarm rate, calibration sensitivity |
| GPU / inference | telemetry anomaly or capacity loss | anomaly detection, latency/queue error, calibration error |
| Rollout | canary regression | correct continue/pause/rollback decision across staged windows |

## Rules for benchmark claims

- Separate fitting, calibration and evaluation data when a method learns thresholds or parameters.
- Include negative and no-change cases, not only failures that are easy to detect.
- Record seeds, versions, inputs and configuration.
- Report limitations and counterexamples.
- Do not infer production performance from synthetic scenarios.
- Prefer machine-readable result files that can be compared across releases.

## Contribution opportunities

Contributors can add scenario packs, metrics, baselines or analysis scripts. A benchmark PR should state the hypothesis, data origin/license, expected outcome and how to reproduce the result.
