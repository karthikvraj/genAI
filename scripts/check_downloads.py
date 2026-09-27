"""Verify checksums and test all extracted project archives."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reliable_ai_lab import __version__
from reliable_ai_lab.registry import PROJECTS


def main() -> None:
    dist = ROOT / "dist"
    manifest = json.loads((dist / "manifest.json").read_text())
    if manifest["version"] != __version__:
        raise SystemExit("Manifest version does not match the source")
    for artifact in manifest["artifacts"]:
        name = artifact["file"]
        if Path(name).name != name:
            raise SystemExit("Invalid artifact filename")
        payload = (dist / name).read_bytes()
        if len(payload) != artifact["bytes"] or hashlib.sha256(payload).hexdigest() != artifact["sha256"]:
            raise SystemExit(f"Checksum or size mismatch: {name}")

    expected = {f"{name}-v{__version__}.zip" for name in PROJECTS}
    listed = {item["file"] for item in manifest["artifacts"]}
    if not expected.issubset(listed):
        raise SystemExit("Manifest is missing a project archive")
    results = []
    for name in sorted(expected):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory).resolve()
            with zipfile.ZipFile(dist / name) as bundle:
                for member in bundle.infolist():
                    target = (destination / member.filename).resolve()
                    if target != destination and destination not in target.parents:
                        raise SystemExit(f"Unsafe archive path in {name}")
                    if member.external_attr >> 16 & 0o170000 == 0o120000:
                        raise SystemExit(f"Symlink in archive: {name}")
                bundle.extractall(destination)
            entries = list(destination.iterdir())
            if len(entries) != 1 or not entries[0].is_dir():
                raise SystemExit(f"Expected one project directory in {name}")
            environment = {
                **os.environ,
                "PYTHONPATH": str(entries[0]),
                "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            }
            run = subprocess.run(
                [sys.executable, "-m", "pytest"], cwd=entries[0], env=environment,
                capture_output=True, text=True, timeout=120,
            )
            results.append({
                "archive": name, "passed": run.returncode == 0,
                "output": run.stdout + run.stderr,
            })
            print(name, "PASS" if run.returncode == 0 else "FAIL", flush=True)
    (ROOT / "docs" / "standalone-test-results.json").write_text(
        json.dumps(results, indent=2) + "\n"
    )
    if len(results) != len(PROJECTS) or not all(item["passed"] for item in results):
        raise SystemExit("A standalone download failed verification")


if __name__ == "__main__":
    main()
