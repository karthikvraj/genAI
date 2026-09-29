"""Smoke test the standalone ChangeGuard entry point in the main CI suite."""
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "change-guard"


def test_sample_cli_report():
    result = subprocess.run(
        [sys.executable, str(PROJECT / "change_guard.py"), str(PROJECT / "example.json")],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    assert report["decision"] == "REVIEW"
    assert report["criticality_exposure"] == 0.889
    assert report["findings"][0]["code"] == "WIDE_BLAST_RADIUS"
