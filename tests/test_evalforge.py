import pytest
from reliable_ai_lab import evalforge as m

@pytest.mark.parametrize('a,b,value',[('A B','a b',1),('a b','a c',.5),('','x',0),('','',1),('x x','x',2/3)])
def test_token_f1(a,b,value):
    assert m.token_f1(a,b)==pytest.approx(value)

def test_pairing_and_zero_coverage():
    r=m.run(m.sample());assert r['metrics']['examples']==8
    assert r['risk_coverage'][-1]['error_rate'] is None
    interval=r['paired_comparison']['percentile_95_interval']
    assert interval[0]<=r['paired_comparison']['paired_exact_match_delta']<=interval[1]

def test_perfect_predictor_calibration():
    p={'records':[{'id':'a','reference':'yes','answer':'yes','confidence':1}, {'id':'b','reference':'yes','answer':'no','confidence':0}]}
    r=m.run(p);assert r['metrics']['brier_score']==0 and r['metrics']['ece_10_bins']==0

def test_incomplete_pairing_rejected():
    p=m.sample();p['records'][0].pop('baseline_answer')
    with pytest.raises(ValueError):m.run(p)

def test_duplicate_record_rejected():
    p=m.sample();p['records'].append(p['records'][0])
    with pytest.raises(ValueError):m.run(p)
