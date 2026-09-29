"""Exercise standalone project CLIs in the main pytest suite."""
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(project, script):
    folder = ROOT / "projects" / project
    result = subprocess.run([sys.executable, str(folder / script), str(folder / "example.json")],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def test_prompt_boundary_sample():
    report = run("prompt-boundary", "prompt_boundary.py")
    assert report["metrics"]["observed_attack_success_rate"] == 0.5
    assert report["metrics"]["benign_task_completion_rate"] == 1.0


def test_rollout_lab_sample():
    report = run("rollout-lab", "rollout_lab.py")
    assert report["decision"] == "ROLLBACK_RECOMMENDED"
    assert report["windows"][0]["status"] == "CLEAN"
