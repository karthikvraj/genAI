import json

from reliable_ai_lab.__main__ import main
from reliable_ai_lab.tour import run_tour


def test_tour_runs_three_flagship_failure_modes():
    result = run_tour(seed=7)

    assert result["tour"] == "reliable-ai-lab"
    assert result["seed"] == 7
    assert len(result["scenarios"]) == 3

    by_project = {row["project"]: row for row in result["scenarios"]}
    assert by_project["evidence-gate"]["decision"] == "review_required"
    assert by_project["repair-agent"]["decision"] == "awaiting_human_review"
    assert by_project["inference-twin"]["decision"] == "simulation_only"
    assert "actions executed = 0" in by_project["repair-agent"]["signal"]
    assert by_project["inference-twin"]["signal"].endswith("x")


def test_tour_cli_writes_json(tmp_path):
    output = tmp_path / "tour.json"

    assert main(["tour", "--seed", "7", "--output", str(output)]) == 0

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["headline"].startswith("Three failure modes.")
    assert [row["track"] for row in data["scenarios"]] == [
        "grounding",
        "agents",
        "infrastructure",
    ]
