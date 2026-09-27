import pytest
from reliable_ai_lab import topology_rca as m

def test_probability_normalization_and_shared_dependency():
    r=m.run(m.sample())
    assert sum(x['model_posterior'] for x in r['ranking'])==pytest.approx(1)
    assert r['ranking'][0]['candidate']=='fabric'

def test_healthy_evidence_favors_no_fault():
    p=m.sample();p['observed']={n:False for n in p['nodes']};r=m.run(p)
    assert r['ranking'][0]['candidate']=='no_fault'

def test_zero_priors_are_honored():
    p=m.sample();p['priors']={n:0 for n in p['nodes']+['no_fault']};p['priors']['fabric']=1
    r=m.run(p);assert r['ranking'][0]['model_posterior']==1

def test_learned_likelihood_mode():
    p=m.sample();p['training_cases']=[{'fault':'fabric','observed':p['observed']}]*3
    r=m.run(p);assert r['likelihood_mode']=='learned_with_topology_fallback'
    assert r['training_counts']['fabric']==3

def test_unknown_edge_rejected():
    p=m.sample();p['edges'].append(['fabric','unknown'])
    with pytest.raises(ValueError):m.run(p)

def test_cycles_terminate():
    p=m.sample();p['edges'].append(['client','fabric']);r=m.run(p)
    assert len(r['ranking'])==7
