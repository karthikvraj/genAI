# Launch kit

## Portfolio introduction

I care less about an AI system sounding confident and more about what happens when it is wrong.

Reliable AI Lab is a set of ten small, inspectable projects around that problem: evidence checks, bounded agent behavior, retrieval budgets, GPU telemetry, inference capacity, evaluation and drift.

Each project has runnable code, a seeded example, tests, and explicit limitations. Default demos run locally without a paid model API. The sample data is synthetic; I am not presenting it as production validation.

Start with Evidence Gate, Repair Agent, or Inference Twin. Change an input, inspect the output, and share a counterexample.

## Three distinct demo stories

**Evidence Gate:** An answer cites the right document but changes 60 seconds to 600 seconds. Show the exact quote and the numeric-review flag. Also show a paraphrase or entity substitution the lexical checker cannot reliably judge. The point is inspectable screening, not a universal hallucination detector.

**Repair Agent:** Start with a plan containing an invented reference and an unauthorized restart action. Show validation errors, the bounded repair, and the final human-review state. Delete the hypothesis to show that the default repairer stops rather than inventing reasoning.

**Inference Twin:** Compare eight servers with a loss of three under the same synthetic arrival stream. Explain offered utilization, finite-window latency and why an overloaded queue has no steady state. Show the held-out surrogate error, not a claim about a particular GPU product.

## Suggested distribution

Lead with one reproducible problem and one short screen recording, not a ten-project announcement with ten unsupported superlatives. Use the relevant engineering community's self-promotion rules. Answer technical questions with code, examples and limitations. Invite counterexamples and contributions rather than asking for automatic stars.

## Measurement

Track actual GitHub traffic, external referrals, release asset downloads, reproducible bug reports and meaningful contributions. Keep source-archive downloads separate from release-asset download counts. Record the observation window and source of every number. There is no guarantee of traffic, stars or virality.

## Publishing sequence

These are communication themes, not instructions to fabricate development history. The code can be published together. Feature different projects only when there is a real demonstration or improvement to discuss.
