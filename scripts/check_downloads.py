"""Test each extracted project independently. Never import the parent checkout."""
from pathlib import Path
import json
import os
import subprocess
import tempfile
import zipfile
ROOT = Path(__file__).resolve().parents[1]
results = []
for archive in sorted((ROOT / "dist").glob("*-v0.1.0.zip")):
    if archive.name == "reliable-ai-lab-v0.1.0.zip":
        continue
    with tempfile.TemporaryDirectory() as directory:
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(directory)
        project = next(Path(directory).iterdir())
        environment = {**os.environ, "PYTHONPATH": str(project), "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
        result = subprocess.run([os.sys.executable, "-m", "pytest"], cwd=project,
                                env=environment, capture_output=True, text=True, timeout=90)
        results.append({"archive": archive.name, "passed": result.returncode == 0,
                        "output": result.stdout + result.stderr})
        print(archive.name, "PASS" if result.returncode == 0 else "FAIL")
(ROOT / "docs" / "standalone-test-results.json").write_text(json.dumps(results, indent=2) + "\n")
if len(results) != 10 or not all(item["passed"] for item in results):
    raise SystemExit("A standalone download failed verification")
