# Security and responsible use

This is a local research playground, not a production service. The demo server binds only to 127.0.0.1, validates Host and Origin, rejects cross-site requests, requires a custom header on JSON execution requests, caps request size, and serves only fixed routes. Do not expose it through a public tunnel, bind it to a public interface, or use it as a security boundary.

Default demos do not call model providers, load pickled models, execute model-generated code, run shell commands, or connect to infrastructure. Models are fitted in memory. Repair Agent has no remediation executor. Its optional Ollama adapter sends supplied evidence to the user's explicitly chosen local model at 127.0.0.1:11434. Redirects and environment proxies are disabled. Review the selected model's provenance and license; the adapter is not a guarantee against prompt injection.

Do not submit credentials, personal information, internal runbooks, customer logs or confidential data to public issues. Use synthetic reproductions. For a sensitive vulnerability, use GitHub private vulnerability reporting when enabled, or request a private reporting channel without disclosing the issue publicly.

No secret scanning, penetration test, external security audit, or production hardening is claimed.
