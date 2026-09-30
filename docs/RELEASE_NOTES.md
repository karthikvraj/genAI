# Reliable AI Lab v0.2.0

This release adds the first machine-readable **Reliable AI benchmark harness** and completes the first productization pass.

## Benchmark harness

- Adds deterministic synthetic regression scenarios for **grounding reliability** and **retrieval reliability**.
- Produces versioned JSON with per-case expected/observed outcomes and aggregate pass counts.
- Adds `python -m reliable_ai_lab benchmark` with optional `--output`.
- Keeps benchmark claims deliberately narrow: the included fixtures are regression scenarios, not estimates of production accuracy.

## Adoption and contributor readiness

- Repositions the project as a reliability-engineering toolkit for AI systems.
- Adds roadmap, benchmark policy, adopter-evidence policy and package-publishing guidance.
- Adds contributor issue forms, pull-request checklist and code of conduct.
- Corrects citation metadata and launch documentation.
- Keeps archived notebooks from defining the active repository language.

## Distribution

The GitHub release includes project ZIPs, the complete source bundle, Python wheel, recorded gallery, manifest and SHA-256 checksums. A separate manual PyPI Trusted Publishing workflow is prepared but requires the repository owner to configure the PyPI Trusted Publisher before first use.

All included benchmark data is synthetic or hand-authored. Passing the included fixtures does not establish production safety, security, accuracy or reliability.
