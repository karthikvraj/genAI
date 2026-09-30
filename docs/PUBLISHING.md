# Package publishing readiness

The repository builds a wheel in CI. Publishing to a package index should be treated as a separate release action so downloads and downstream dependencies represent real installs.

## Before first PyPI publication

1. Confirm the intended distribution name is available and appropriate. The current distribution name is `kv-reliable-ai-lab`; the import package is `reliable_ai_lab`.
2. Create the PyPI project/maintainer configuration and prefer Trusted Publishing from GitHub Actions.
3. Verify project URLs, license metadata, README rendering and wheel contents.
4. Test installation in a clean environment.
5. Publish a test release before a stable public release.

Do not rename an already-published distribution casually: package names become part of users' dependency files and supply-chain expectations.
