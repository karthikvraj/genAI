# Rollout Lab

Evaluate a staged rollout from saved baseline and canary telemetry windows. It compares error rates with Wilson intervals, applies an absolute error-rate tolerance, and checks a sampled p95 latency ratio. Its outputs are recommendations for a human operator; it never changes traffic.

```bash
python3 projects/rollout-lab/rollout_lab.py projects/rollout-lab/example.json
python3 -m unittest discover -s projects/rollout-lab -p 'test_*.py'
```

The synthetic example starts with a clean 5% canary window and then shows a substantial error regression at 20%, producing `ROLLBACK_RECOMMENDED`. Change the second canary's errors to `7` and latencies to `[92,96,100,105,120]` to see `PROMOTION_CANDIDATE`. Use `--output report.json` to save a report.

Each named window supplies `baseline` and `canary` arms with request counts, error counts, and sampled positive latency values in milliseconds. Policy sets minimum requests and latency sample counts, required clean windows, maximum absolute error-rate increase, and maximum p95 latency ratio. Underpowered windows `HOLD`; an observed guardrail exceedance calls for `REVIEW`; a conservative Wilson separation beyond tolerance recommends rollback. Promotion requires enough clean windows and is only a candidate for human review.

**Limits:** Wilson intervals assume independent Bernoulli requests and do not correct for repeated window peeking or multiple tests. Latency p95 from a short sample is illustrative, not a defensible tail estimate. Real rollouts need representative cohorts, time-aware windows, telemetry quality checks, SLOs, and a separate authorized controller. The demo is synthetic and does not assert operational safety.
