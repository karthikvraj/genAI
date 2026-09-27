import pytest
from reliable_ai_lab import drift_radar as m

def test_holm_known_values():
    assert m.holm_adjust([.01,.04,.03])==pytest.approx([.03,.06,.06])

def test_seeded_shift_detected():
    r=m.run(m.sample());assert r['metrics']['drifted_features']>=2
    assert 0<=r['metrics']['domain_classifier_holdout_auc']<=1

def test_identical_samples_no_shift():
    p=m.sample();p['current']=p['reference'];r=m.run(p)
    assert r['metrics']['drifted_features']==0
    assert all(f['holm_p_value']==1 for f in r['features'])

@pytest.mark.parametrize('p', [[],[-.1],[1.2],[float('nan')]])
def test_holm_invalid_values(p):
    with pytest.raises(ValueError):m.holm_adjust(p)
