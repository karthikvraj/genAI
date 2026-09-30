from reliable_ai_lab.benchmark import run_benchmarks


def test_benchmark_is_machine_readable_and_passes():
    result = run_benchmarks()
    assert result["schema_version"] == "1.0"
    assert result["summary"] == {"passed": 7, "total": 7, "all_passed": True}
    assert result["tracks"]["grounding"]["summary"] == {"passed": 5, "total": 5}
    assert result["tracks"]["retrieval"]["summary"] == {"passed": 2, "total": 2}


def test_benchmark_contains_no_production_claim():
    result = run_benchmarks()
    assert "synthetic" in result["provenance"].lower()
    assert any("not estimates of production accuracy" in x for x in result["limitations"])
