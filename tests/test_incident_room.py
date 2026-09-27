import pytest
from reliable_ai_lab import incident_room as m

def test_shift_and_runbook_evidence():
    r=m.run(m.sample());assert r['decision']=='human_triage'
    assert r['metrics']['shifted_features']>=2
    assert r['analysts']['runbook_evidence']
    assert r['metrics']['actions_executed']==0

def test_identical_window_has_no_median_shift():
    p=m.sample();p['current']=p['baseline'];r=m.run(p)
    assert r['metrics']['shifted_features']==0
    assert r['decision']=='no_escalation_signal'

def test_bad_feature_count():
    p=m.sample();p['feature_names']=['wrong']
    with pytest.raises(ValueError):m.run(p)

def test_mismatched_dimensions():
    p=m.sample();p['current']=[[1,2]]
    with pytest.raises(ValueError):m.run(p)
