# Repository settings

The project name is Reliable AI Lab. The current repository address is `karthikvraj/genAI`; the requested name is `karthikvraj/reliable-ai-lab`.

## Rename

The connected editor can change files but cannot change repository settings. In the repository's Settings page, set **Repository name** to `reliable-ai-lab` and select **Rename**. Do not create a second repository named `genAI`; that would break the old-address redirects.

The release and project links in the READMEs are relative to this repository. The workflow uses `github.repository`, not a fixed owner/name. The old clone address remains a compatibility alias after the rename. Once the rename is complete, update the clone command in README.md and `repository-code` in CITATION.cff to the new address.

For a local checkout:

```bash
git remote set-url origin https://github.com/karthikvraj/reliable-ai-lab.git
```

## About

Description:

> Python projects for model evaluation, evidence checks, agent validation, retrieval and infrastructure reliability.

Topics:

`machine-learning`, `llm-evaluation`, `rag`, `agents`, `observability`, `anomaly-detection`, `gpu`, `model-monitoring`, `python`

These are proposed repository settings, not settings changed by this update.

## Release checks

Open the release, download the lab ZIP and verify SHA256SUMS.txt. Check the Actions run for the current commit and run the local setup instructions after renaming.

Reference: [GitHub repository renaming](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).
