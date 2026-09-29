# Reliable AI Lab v0.1.3

Adds two independently runnable, synthetic-data projects:

- **Prompt Boundary** scores saved agent traces for unauthorized tool calls, literal synthetic marker leakage, and benign task completion. It does not run or defend a model.
- **Rollout Lab** checks staged baseline and canary windows using error-rate Wilson intervals and sampled latency guardrails. It recommends review or rollback but never changes live traffic.

Both projects include documented input formats, limitations, sample traces, and focused tests. The main CI suite runs their command-line examples. The release includes standalone ZIPs for both, plus the previous eleven project ZIPs, full source ZIP, wheel, recorded gallery, manifest, and SHA-256 checksums. Extracted archives are tested before publication.

Results are illustrative and based on synthetic examples; neither project establishes production safety or model security. v0.1.2 remains available and unchanged.
