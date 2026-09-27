import pytest
from reliable_ai_lab import inference_twin as m

def test_capacity_loss_and_out_of_domain_guard():
    r=m.run(m.sample())
    assert r['server_loss_scenario']['p95_latency_ms']>r['baseline']['p95_latency_ms']
    assert not r['server_loss_scenario']['steady_state_possible']
    assert r['server_loss_scenario']['surrogate_p95_ms'] is None
    assert r['metrics']['training_points']==120 and r['metrics']['holdout_points']==40

def test_identical_scenarios_when_no_loss():
    p=m.sample();p['lost_servers']=0;r=m.run(p)
    assert r['baseline']==r['server_loss_scenario']

def test_more_capacity_does_not_increase_sample_path_wait():
    a=m.simulate(100,30,3,500,9);b=m.simulate(100,30,8,500,9)
    assert b['p95_wait_ms']<=a['p95_wait_ms']

def test_single_server_default_is_valid():
    r=m.run({'arrival_rps':5,'service_ms':40,'servers':1,'requests':100})
    assert r['baseline']['servers']==1

@pytest.mark.parametrize('key,value',[('servers',0),('lost_servers',8),('service_ms',0),('arrival_rps',-1),('requests',5)])
def test_parameter_validation(key,value):
    p=m.sample();p[key]=value
    with pytest.raises(ValueError):m.run(p)
