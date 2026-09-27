import pytest
from reliable_ai_lab import gpu_guard as m

def test_reference_split_and_synthetic_labels():
    r=m.run(m.sample());a=r['metrics']
    assert a['training_rows']+a['calibration_rows']==500
    assert 0<=a['precision']<=1 and 0<=a['recall']<=1
    assert len(r['all_flags'])==100
    assert all(0<x['rank_p_value']<=1 for x in r['ranked_rows'])

def test_unattainable_significance_flags_nothing():
    p=m.sample();p['alpha']=0.001;r=m.run(p)
    assert r['metrics']['flagged_rows']==0

def test_labels_are_not_used_for_detection():
    p=m.sample();r=m.run(p);p['labels']=[0]*100;s=m.run(p)
    assert r['all_flags']==s['all_flags']

def test_bad_labels():
    p=m.sample();p['labels']=[1]
    with pytest.raises(ValueError):m.run(p)

def test_nonfinite_is_rejected():
    p=m.sample();p['current'][0][0]=float('nan')
    with pytest.raises(ValueError):m.run(p)
