# Reliable AI Lab v0.1.1

Documentation and packaging update. Project algorithms are unchanged.

- Rewrote the main README, project pages and demo text.
- Moved the four earlier facial-emotion notebooks and PDFs under `legacy/facial-emotion-detection/` without changing their contents.
- Used relative repository links and removed the fixed release tag from the workflow and archive checker.
- Added checksum verification to the extracted-package tests.

The release includes ten project ZIPs, the full source bundle, a Python wheel, the recorded HTML gallery and SHA-256 checksums. The workflow tests the main suite and each extracted project before publishing.

The previous v0.1.0 release is retained. This release does not complete the repository-name change; that requires the owner's GitHub Settings page.

The examples use synthetic data. The HTML gallery shows saved results; run `python -m reliable_ai_lab serve` for editable inputs and fresh results. Optional Ollama inference is not covered by the default tests.
