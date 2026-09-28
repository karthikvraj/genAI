# A cited answer changed 60 seconds to 600. Can a small local check catch it?

A citation can look convincing while the number in the answer no longer matches the source. I built a small, reproducible example to make that failure visible.

In the sample, the source says: “The cache time to live is 60 seconds.” The answer says: “The cache time to live is 600 seconds.” The [Evidence Gate demo](https://github.com/karthikvraj/reliable-ai-lab/tree/main/projects/evidence-gate) returns `numeric_review`, shows the cited excerpt and reports `600` as an unmatched number.

It also tests a citation that points to a missing source and a statement that reverses “requires human approval” into “does not require human approval.” The point is to expose cases worth human review before a cited answer is trusted.

## Try it locally

```bash
git clone https://github.com/karthikvraj/reliable-ai-lab.git
cd reliable-ai-lab
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m reliable_ai_lab demo evidence-gate
```

Python 3.10 or later is required. The default demo does not need an API key or GPU. On Windows, activate the environment with `.venv\\Scripts\\activate`.

The output includes a decision of `review_required`, five claims, one lexically supported claim and four that need review. Those figures describe the included example, not a benchmark on real-world answers.

## What the check can and cannot do

This is a deliberately limited lexical check. It can flag changed numbers, reversed negation, missing citations and weak overlap with the cited passage. A paraphrase, unit conversion, entity mismatch or multi-hop claim may be misclassified. Similarity is not a probability of truth, and a passing check should never authorize a consequential action.

That boundary matters. I want a useful review signal with an inspectable source excerpt, not a claim that a small heuristic has solved factuality.

## The wider lab

[Reliable AI Lab](https://github.com/karthikvraj/reliable-ai-lab) includes nine other independent experiments covering retrieval budgets, bounded agent-plan repair, model drift, infrastructure telemetry, GPU anomalies, evaluation and simulated inference capacity. The examples use synthetic or hand-authored data. The [release](https://github.com/karthikvraj/reliable-ai-lab/releases/tag/reliable-ai-lab-v0.1.1) has a project ZIP, full source ZIP and a recorded demo gallery.

If you try Evidence Gate on a case it gets wrong, open an issue with a shareable input and expected behavior. That would be more valuable than a star alone. If the project helps you, a star makes it easier for others to find.

— Karthik Coimbatore Varadaraj
