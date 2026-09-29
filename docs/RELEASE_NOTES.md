# Reliable AI Lab v0.1.2

Adds ChangeGuard, a deterministic preflight for proposed infrastructure changes. Given a service dependency graph and a change plan, it reports reachable downstream services, criticality-weighted exposure, rollout and rollback findings, and a reproducible input fingerprint. It never executes or approves a change.

- Includes a synthetic DNS change example and tests for wide impact, rollback blocking, isolated changes, graph cycles, and invalid dependencies.
- Adds ChangeGuard to the project index and CI smoke checks.
- Ships a standalone `change-guard-v0.1.2.zip` alongside the ten existing project ZIPs, the complete source ZIP, wheel, recorded gallery, manifest, and checksums.

The example is synthetic. Exposure is potential impact, not a measured failure probability. Existing projects retain their algorithms; the version update creates new downloadable artifacts without modifying v0.1.1.
