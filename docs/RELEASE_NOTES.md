# Reliable AI Lab v0.1.0

Ten independent AI/ML reliability prototypes by Karthik Coimbatore Varadaraj.

Includes ten project ZIPs, a full lab source bundle, a Python wheel, a read-only HTML gallery, and SHA-256 checksums. Each standalone ZIP contains its implementation, tests, documentation and a seeded synthetic example.

Run `python -m pip install -e '.[dev]'`, then `python -m reliable_ai_lab serve` from an extracted project directory. Default demos need no API key or GPU. The HTML gallery replays recorded results; it does not compute new predictions.

The repository workflow tests the suite and every extracted project before publishing these assets. See the Actions run for the exact Python versions and result logs.

This is a research preview, not a production deployment. Synthetic results do not establish real-world performance. Optional Ollama model execution is not validated by the deterministic offline tests. Existing facial-emotion notebooks and PDFs are not part of these downloads.
